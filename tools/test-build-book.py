"""Integration tests for tools/build-book.py (phase 5 of the Markdown conversion).

Each test builds the whole book from book/ in scratch copies of the
repository, so the suite takes about half a minute. Requires pandoc.
"""
import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("build_book", HERE / "build-book.py")
build_book = importlib.util.module_from_spec(spec)
spec.loader.exec_module(build_book)
import html_to_md  # noqa: E402  (tools/markdown is on the path after build-book.py loads)


def run(*args):
    out, err = io.StringIO(), io.StringIO()
    with redirect_stdout(out), redirect_stderr(err):
        code = build_book.main(list(args))
    return code, out.getvalue() + err.getvalue()


class BuildBookTests(unittest.TestCase):
    def test_check_reproduces_every_published_page(self):
        code, output = run("--check")
        self.assertEqual(code, 0, output)
        self.assertIn("search-textbook.html: ", output)
        self.assertIn("Build check passed.", output)

    def test_in_place_build_is_refused_while_html_is_the_source(self):
        if build_book.source_of_truth() != "html":
            self.skipTest("cut-over done: in-place builds are the normal workflow")
        before = (build_book.ROOT / "search-textbook.html").read_bytes()
        code, output = run()
        self.assertEqual(code, 2)
        self.assertIn("Refusing to build in place", output)
        self.assertEqual((build_book.ROOT / "search-textbook.html").read_bytes(), before)

    def test_builds_are_deterministic(self):
        with tempfile.TemporaryDirectory() as tmp:
            a, b = Path(tmp) / "a", Path(tmp) / "b"
            for target in (a, b):
                code, output = run("--out", str(target))
                self.assertEqual(code, 0, output)
            for page in build_book.pages(a):
                with self.subTest(page=page):
                    self.assertEqual((a / page).read_bytes(), (b / page).read_bytes())

    def test_converter_round_trip_reproduces_the_page(self):
        # Convert the committed page to Markdown, build that, and compare the
        # result with the committed page. This keeps the converter faithful
        # (for porting HTML edits from older branches) without requiring the
        # authored sources to match its formatting byte for byte.
        with tempfile.TemporaryDirectory() as tmp:
            source, work = Path(tmp) / "book", Path(tmp) / "repo"
            html_to_md.convert_book(source)
            build_book.make_workspace(work)
            build_book.build_md.build_book(source, work)
            report = build_book.eq.compare(build_book.eq.load(build_book.ROOT / "search-textbook.html"),
                                           build_book.eq.load(work / "search-textbook.html"))
            self.assertEqual(report, [], "\n".join(report[:40]))

    def test_config_names_a_known_source(self):
        config = json.loads(build_book.CONFIG.read_text(encoding="utf-8"))
        self.assertIn(config["source_of_truth"], ("html", "markdown"))


if __name__ == "__main__":
    unittest.main()
