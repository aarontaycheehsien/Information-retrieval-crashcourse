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

    def test_config_names_a_known_source(self):
        config = json.loads(build_book.CONFIG.read_text(encoding="utf-8"))
        self.assertIn(config["source_of_truth"], ("html", "markdown"))


if __name__ == "__main__":
    unittest.main()
