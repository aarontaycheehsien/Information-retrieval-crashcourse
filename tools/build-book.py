"""Build search-textbook.html and its generated companions from book/.

Phase 5 of reviews/markdown-conversion-plan.md: one command reproduces the
published page. It builds every file in book/ with Pandoc and
tools/markdown/book.lua, assembles them into book/template.html, derives
navigation and footnotes, runs maintain.py, renumber_footnotes.py and the
product-claims and glossary builders until a whole round changes nothing,
then rebuilds the read-this-first digest and the vendor questionnaire.

    python tools/build-book.py --check        # build in a scratch copy and compare
    python tools/build-book.py --out DIR      # build into a copy of the repository at DIR
    python tools/build-book.py                # build in place (after cut-over)

book/book.json records which copy is the source of truth. While it says
"html", an in-place build is refused, because it would replace hand edits in
search-textbook.html that book/ does not have yet; regenerate book/ with
tools/markdown/html_to_md.py --book book instead. --check never writes to the
repository.

--check passes when the built book and every root HTML page are equivalent to
the committed files (tools/html_equivalence.py). Once the source of truth is
"markdown", they must also be byte-identical, so a stale committed build fails.

Standard library plus pandoc 3.1. Exit 0 on success, 1 on a failed check,
2 on a build error.
"""

from __future__ import annotations

import argparse
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE / "markdown"))
sys.path.insert(0, str(HERE))

import build_md  # noqa: E402
import html_equivalence as eq  # noqa: E402
from pilot import make_workspace  # noqa: E402

ROOT = HERE.parent
BOOK_DIR = ROOT / "book"
CONFIG = BOOK_DIR / "book.json"


def source_of_truth() -> str:
    return json.loads(CONFIG.read_text(encoding="utf-8"))["source_of_truth"]


def pages(repo: Path) -> list[str]:
    return sorted(p.name for p in repo.glob("*.html"))


def compare(built: Path, strict_bytes: bool) -> int:
    failed = 0
    for page in pages(ROOT):
        committed, fresh = ROOT / page, built / page
        report = eq.compare(eq.load(committed), eq.load(fresh), f"committed {page}", f"built {page}", max_diffs=5)
        same_bytes = committed.read_bytes() == fresh.read_bytes()
        if report:
            failed += 1
            print("\n".join(report))
        elif strict_bytes and not same_bytes:
            failed += 1
            print(f"{page}: equivalent but not byte-identical; commit a fresh build (python tools/build-book.py)")
        else:
            print(f"  {page}: {'identical' if same_bytes else 'equivalent'}")
    return failed


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="build in a scratch copy and compare with the committed pages")
    mode.add_argument("--out", type=Path, help="build into a fresh copy of the repository at this directory")
    args = parser.parse_args(argv)
    truth = source_of_truth()
    try:
        if args.check:
            with tempfile.TemporaryDirectory() as tmp:
                work = Path(tmp) / "repo"
                make_workspace(work)
                result = build_md.build_book(BOOK_DIR, work)
                print(f"Built {result['files']} source files; generators settled in {result['rounds']} round(s).")
                failed = compare(work, strict_bytes=truth == "markdown")
            print("Build check passed." if not failed else f"Build check failed: {failed} page(s).")
            return 1 if failed else 0
        if args.out:
            make_workspace(args.out)
            result = build_md.build_book(BOOK_DIR, args.out)
            print(f"Built {result['files']} source files into {args.out}; "
                  f"generators settled in {result['rounds']} round(s).")
            return 0
        if truth != "markdown":
            print("Refusing to build in place: book/book.json says search-textbook.html is the source of truth.\n"
                  "Regenerate book/ with python tools/markdown/html_to_md.py --book book, or use --check / --out.",
                  file=sys.stderr)
            return 2
        result = build_md.build_book(BOOK_DIR, ROOT)
        print(f"Built {result['files']} source files in place; generators settled in {result['rounds']} round(s).")
        return 0
    except build_md.BuildError as exc:
        print(f"build error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
