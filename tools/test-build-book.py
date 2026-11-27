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
from unittest import mock

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
            b.mkdir()  # --out accepts both a new path and an existing empty directory
            for target in (a, b):
                code, output = run("--out", str(target))
                self.assertEqual(code, 0, output)
            for page in build_book.pages(a):
                with self.subTest(page=page):
                    self.assertEqual((a / page).read_bytes(), (b / page).read_bytes())

    def test_output_preserves_existing_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            existing = Path(tmp) / "author-notes.txt"
            existing.write_text("keep me", encoding="utf-8")
            code, message = run("--out", tmp)
            self.assertEqual(code, 2)
            self.assertIn("new or empty directory", message)
            self.assertEqual(existing.read_text(encoding="utf-8"), "keep me")

    def test_check_reports_missing_expected_pages(self):
        with tempfile.TemporaryDirectory() as tmp:
            checkout, fresh = Path(tmp) / "checkout", Path(tmp) / "fresh"
            checkout.mkdir()
            fresh.mkdir()
            for page in build_book.build_md.WRITTEN_PAGES:
                (fresh / page).write_text("<p>Generated</p>", encoding="utf-8")
            output = io.StringIO()
            with mock.patch.object(build_book, "ROOT", checkout), redirect_stdout(output):
                failures = build_book.compare(fresh, strict_bytes=True)
            self.assertEqual(failures, len(build_book.build_md.WRITTEN_PAGES))
            for page in build_book.build_md.WRITTEN_PAGES:
                self.assertIn(f"{page}: missing from checkout", output.getvalue())

    def test_output_preserves_files_added_during_the_build(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "preview"
            dest.mkdir()
            added = dest / "new-notes.txt"

            def add_file(book_dir, work):
                added.write_text("new notes", encoding="utf-8")
                return {"files": 1, "rounds": 1}

            with mock.patch.object(build_book.build_md, "build_book", side_effect=add_file):
                code, _ = run("--out", str(dest))
            self.assertEqual(code, 2)
            self.assertEqual(added.read_text(encoding="utf-8"), "new notes")

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

    def test_line_endings_never_differ_by_platform(self):
        # The existing generators write with the platform's line ending (CRLF
        # on Windows). Simulate that, and check the build normalises it and
        # --check ignores CRLF-only differences in a checkout.
        with tempfile.TemporaryDirectory() as tmp:
            repo = Path(tmp)
            for name in build_book.build_md.WRITTEN_PAGES:
                (repo / name).write_bytes(b"<p>a</p>\r\n<p>b</p>\r\n")
            build_book.build_md.normalise_newlines(repo)
            for name in build_book.build_md.WRITTEN_PAGES:
                self.assertEqual((repo / name).read_bytes(), b"<p>a</p>\n<p>b</p>\n")
        self.assertEqual(build_book.lf(b"x\r\ny\n"), b"x\ny\n")

    def test_scratch_copy_survives_a_failed_hard_link(self):
        # Hard links cannot cross drives or filesystems; the copy must fall back.
        import os
        with tempfile.TemporaryDirectory() as tmp:
            src, dst = Path(tmp) / "a.png", Path(tmp) / "b.png"
            src.write_bytes(b"image")
            with mock.patch.object(os, "link", side_effect=OSError(18, "Invalid cross-device link")):
                build_book.make_workspace.__globals__["link_or_copy"](src, dst)
            self.assertEqual(dst.read_bytes(), b"image")

    def test_config_names_a_known_source(self):
        config = json.loads(build_book.CONFIG.read_text(encoding="utf-8"))
        self.assertIn(config["source_of_truth"], ("html", "markdown"))


if __name__ == "__main__":
    unittest.main()
