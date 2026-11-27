"""Phase 3 round trip: Markdown chapter -> HTML -> spliced book -> generators.

Makes two copies of the repository (without .git and outputs; images are
hard-linked) under the ignored outputs/markdown-conversion/: "control" is
unchanged, "pilot" has the given chapters replaced by their Markdown builds.
The existing generators run in both. The pilot passes when every generator
behaves as in the control (same exit status and messages, so known
problems in the live book are not blamed on the conversion) and the pilot
book is equivalent to the live book (tools/html_equivalence.py).

Usage:
    python tools/markdown/pilot.py book/02-boolean-admission.md [...]   # splice chapters
    python tools/markdown/pilot.py --book BOOK-DIR                       # whole book

Exit 0 when equivalent. Standard library plus pandoc.
"""

from __future__ import annotations

import difflib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import build_md  # noqa: E402
import html_equivalence as eq  # noqa: E402
from html_to_md import Parser, find  # noqa: E402

ROOT = HERE.parents[1]
OUT = ROOT / "outputs" / "markdown-conversion"
# Build passes fill the build's placeholders, so their messages may differ
# from the control ("updated" rather than "no changes"); their exit status
# must not. Verification passes must match the control exactly.
GENERATORS = [
    ["tools/maintain.py"],
    ["tools/renumber_footnotes.py"],
    ["tools/build-product-claims.py"],
    ["tools/build-glossary-hub.py"],
    ["tools/build-digest.py"],
    ["tools/build-vendor-questionnaire.py"],
]
CHECKS = [
    ["tools/maintain.py"],
    ["tools/renumber_footnotes.py"],
    ["tools/build-product-claims.py", "--check"],
    ["tools/build-glossary-hub.py", "--check"],
    ["tools/build-digest.py", "--check"],
    ["tools/build-vendor-questionnaire.py", "--check"],
    ["tools/check-product-claims.py", "--as-of", "2026-09-19"],
    ["tools/test-product-claims.py"],
    ["tools/test-glossary-hub.py"],
    ["tools/test-digest.py"],
    ["tools/test-vendor-questionnaire.py"],
    ["tools/test-html-equivalence.py"],
    ["tools/test-markdown-mapping.py"],
]


def link_or_copy(src, dst):
    """Hard-link a file, or copy it where a link is impossible.

    A hard link cannot cross filesystems or drives: a temporary directory on
    another drive (Windows) or on tmpfs (many Linux systems) would otherwise
    make the scratch copy fail."""
    try:
        os.link(src, dst)
    except OSError:
        shutil.copy2(src, dst)
    return dst


def make_workspace(work: Path, *, exclude=()):
    ignore = shutil.ignore_patterns(".git", "outputs", "images", "__pycache__", *exclude)
    shutil.copytree(ROOT, work, ignore=ignore)
    # Real files, not symlinks: the claims validator rejects evidence outside
    # the repository. Hard links are cheap; copies are the fallback.
    shutil.copytree(ROOT / "images", work / "images", copy_function=link_or_copy,
                    ignore=shutil.ignore_patterns(*exclude))


def splice(book: str, md_path: Path) -> str:
    fragment, notes = build_md.build_file(md_path)
    key = re.search(r'<section class="[^"]*" id="(sec-[^"]+)">', fragment)[1]
    parser = Parser(book)
    parser.feed(book)
    parser.close()
    section = find(parser.root, key)
    book = book[:section.start] + fragment.rstrip("\n") + book[section.end:]
    if notes:
        for li in re.finditer(r'<li id="(fn:[^"]+)">.*?</li>', notes, re.S):
            parser = Parser(book)
            parser.feed(book)
            old = find(parser.root, li[1])
            book = book[:old.start] + li[0] + book[old.end:]
    return build_md.fill_chapter_navs(book)


def run_chain(work: Path):
    """Run generators then checks; return (command, exit status, output) for each."""
    results = []
    for cmd in GENERATORS + CHECKS:
        r = subprocess.run([sys.executable, *cmd], cwd=work, capture_output=True, text=True)
        output = (r.stdout + r.stderr).strip()
        output = re.sub(r"Ran (\d+) tests? in [0-9.]+s", r"Ran \1 tests", output)
        results.append((" ".join(cmd), r.returncode, output))
    return results


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    book_mode = len(argv) == 2 and argv[0] == "--book"
    sources = [] if book_mode else [Path(a) for a in argv]
    if not (book_mode or sources):
        raise SystemExit(__doc__)
    control, pilot = OUT / "control", OUT / "pilot"
    for work in (control, pilot):
        if work.exists():
            shutil.rmtree(work)
        make_workspace(work)
    if book_mode:
        # The whole book from Markdown: nothing of the live article is kept.
        result = build_md.build_book(Path(argv[1]).resolve(), pilot)
        print(f"Built the whole book from {result['files']} source files; "
              f"generators settled in {result['rounds']} round(s).")
        bad = [entry for entry in result["log"] if entry[2]]
        for round_no, cmd, rc, out in bad:
            print(f"  round {round_no} {cmd}: exit {rc}\n    " + "\n    ".join(out.splitlines()[-4:]))
    else:
        target = pilot / "search-textbook.html"
        book = target.read_text(encoding="utf-8")
        for src in sources:
            book = splice(book, src)
            print(f"Spliced {src}")
        target.write_text(book, encoding="utf-8")
    expected, actual = run_chain(control), run_chain(pilot)
    mismatches = 0
    print("Generators and checks (pilot against control):")
    for i, ((cmd, rc_c, out_c), (_, rc_p, out_p)) in enumerate(zip(expected, actual)):
        strict = i >= len(GENERATORS)
        same = rc_c == rc_p and (out_c == out_p or not strict)
        mismatches += not same
        kind = "check" if strict else "build"
        print(f"  {kind} {cmd}: exit {rc_p} ({'as control' if same else f'control exit {rc_c}, output differs'})")
        if not same:
            for line in difflib.unified_diff(out_c.splitlines(), out_p.splitlines(), "control", "pilot", lineterm="", n=1):
                print("    " + line)
    # The book and every generated companion page must be equivalent to the
    # live files; byte differences in generated pages are rebuild noise.
    pages = sorted(p.name for p in ROOT.glob("*.html"))
    for work, label in ((control, "control"), (pilot, "pilot")):
        failed = []
        for page in pages:
            report = eq.compare(eq.load(ROOT / page), eq.load(work / page),
                                f"live {page}", f"{label} {page}", max_diffs=8)
            if report:
                failed.append(page)
                print("\n".join(report))
        print(f"{label}: {len(pages) - len(failed)} of {len(pages)} pages equivalent to the live files"
              + (f"; differ: {', '.join(failed)}" if failed else "."))
        mismatches += bool(failed)
    return 1 if mismatches else 0


if __name__ == "__main__":
    sys.exit(main())
