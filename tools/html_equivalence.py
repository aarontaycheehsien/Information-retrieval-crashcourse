"""Compare two HTML files for rendering-relevant equivalence.

Phase 1 of the Markdown conversion (reviews/markdown-conversion-plan.md).
Both files are parsed into a tree and serialised to a canonical form, one
node per line. Two files are equivalent when their canonical forms match.

Differences that are ignored:

- attribute order, and the order of tokens within ``class``;
- character references versus literal characters (``&amp;``/``&``,
  ``&#8217;``/``’``, ``&nbsp;``/U+00A0);
- ``<br>`` versus ``<br/>``; an empty attribute value versus none
  (``defer=""``/``defer``);
- runs of ASCII whitespace inside text, which collapse to one space;
- whitespace-only text between block-level elements, and leading or
  trailing whitespace at a block boundary.

Everything else is significant: text, element order and nesting, ids,
classes, every other attribute value, comments (the generators rely on
BEGIN/END markers), and the content of ``script``, ``style``, ``pre`` and
``textarea``, which is compared verbatim. A non-breaking space is never
treated as ordinary whitespace.

Input must be well-formed: every non-void element closed explicitly and in
order. Mismatched or missing end tags are reported as errors rather than
repaired, because a silent repair could hide exactly the drift this check
exists to catch. The current book and Pandoc's HTML writer both satisfy this.

Usage:

    python tools/html_equivalence.py A.html B.html [--section ID]
    python tools/html_equivalence.py A.html --canonical OUT.txt
    python tools/html_equivalence.py --record-baseline [--commit REV]
    python tools/html_equivalence.py --check-baseline [FILE]

Exit status: 0 equivalent, 1 different, 2 error. Standard library only.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "search-textbook.html"
BASELINE_MANIFEST = ROOT / "data" / "markdown-baseline.json"
BASELINE_DIR = ROOT / "outputs" / "markdown-conversion"

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}
VERBATIM = {"script", "style", "pre", "textarea"}
# Elements whose content takes part in inline layout, so whitespace beside
# them can be significant. Everything else is treated as block-level for
# whitespace purposes, including SVG structure other than text content.
INLINE = {
    "a", "abbr", "b", "bdi", "bdo", "br", "button", "cite", "code", "data",
    "del", "dfn", "em", "i", "img", "input", "ins", "kbd", "label", "mark",
    "math", "output", "q", "s", "samp", "select", "small", "span", "strong",
    "sub", "sup", "svg", "time", "u", "var", "wbr",
    # SVG text content.
    "text", "tspan", "textpath",
}
ASCII_WS = re.compile(r"[ \t\n\r\f]+")


class EquivalenceError(Exception):
    """Input could not be parsed strictly."""


class Node:
    __slots__ = ("kind", "tag", "attrs", "children", "text", "pos")

    def __init__(self, kind, tag="", attrs=None, text="", pos=(0, 0)):
        self.kind = kind  # "element", "text", "comment", "decl", "pi", "root"
        self.tag = tag
        self.attrs = attrs or []
        self.children: list[Node] = []
        self.text = text
        self.pos = pos

    def get(self, name):
        for key, value in self.attrs:
            if key == name:
                return value
        return None


class _TreeBuilder(HTMLParser):
    def __init__(self, label):
        super().__init__(convert_charrefs=True)
        self.label = label
        self.root = Node("root")
        self.stack = [self.root]

    def _fail(self, message):
        line, col = self.getpos()
        raise EquivalenceError(f"{self.label}:{line}:{col + 1}: {message}")

    def _append(self, node):
        self.stack[-1].children.append(node)

    def handle_starttag(self, tag, attrs):
        node = Node("element", tag, attrs, pos=self.getpos())
        self._append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        # <br/> and SVG's <path/>: an element with no children either way.
        self._append(Node("element", tag, attrs, pos=self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            self._fail(f"end tag for void element </{tag}>")
        current = self.stack[-1]
        if current.kind != "element" or current.tag != tag:
            opened = (
                f"<{current.tag}> opened at line {current.pos[0]}"
                if current.kind == "element" else "no open element"
            )
            self._fail(f"</{tag}> does not close the current element ({opened})")
        self.stack.pop()

    def handle_data(self, data):
        self._append(Node("text", text=data, pos=self.getpos()))

    def handle_comment(self, data):
        self._append(Node("comment", text=data, pos=self.getpos()))

    def handle_decl(self, decl):
        self._append(Node("decl", text=decl, pos=self.getpos()))

    def handle_pi(self, data):
        self._append(Node("pi", text=data, pos=self.getpos()))

    def unknown_decl(self, data):
        self._fail(f"unsupported declaration <![{data}]>")


def parse(source: str, label: str = "<input>") -> Node:
    builder = _TreeBuilder(label)
    builder.feed(source)
    builder.close()
    if len(builder.stack) > 1:
        node = builder.stack[-1]
        raise EquivalenceError(
            f"{label}:{node.pos[0]}:{node.pos[1] + 1}: <{node.tag}> is never closed"
        )
    return builder.root


def _is_inline(node: Node | None) -> bool:
    if node is None:
        return False
    if node.kind == "text":
        return True
    return node.kind == "element" and node.tag in INLINE


def _quote(text: str) -> str:
    out = json.dumps(text, ensure_ascii=False)
    # Make invisible but significant characters visible in reports.
    return (out.replace("\u00a0", "\\u00a0").replace("\u200b", "\\u200b")
               .replace("\u202f", "\\u202f").replace("\u2009", "\\u2009"))


def _attrs(node: Node) -> str:
    parts = []
    for key, value in sorted(node.attrs, key=lambda kv: kv[0]):
        value = "" if value is None else value
        if key == "class":
            value = " ".join(sorted(ASCII_WS.split(value.strip()))) if value.strip() else ""
        parts.append(f" {key}={_quote(value)}")
    return "".join(parts)


class Line:
    __slots__ = ("text", "context")

    def __init__(self, text, context):
        self.text = text
        self.context = context


def canonical(root: Node, ignore_comments: bool = False) -> list[Line]:
    """Serialise a parsed tree to canonical lines with diagnostic context."""
    lines: list[Line] = []
    last_id = ["(document start)"]  # nearest preceding id, in document order

    def walk(node: Node, depth: int, verbatim: bool):
        children = node.children
        if ignore_comments:
            children = [c for c in children if c.kind != "comment"]
        block_parent = node.kind == "root" or (
            node.kind == "element" and node.tag not in INLINE)
        for index, child in enumerate(children):
            pad = " " * depth
            if child.kind == "text":
                text = child.text
                if not verbatim:
                    text = ASCII_WS.sub(" ", text)
                    if block_parent:
                        before = children[index - 1] if index else None
                        after = children[index + 1] if index + 1 < len(children) else None
                        if not _is_inline(before):
                            text = text.lstrip(" ")
                        if not _is_inline(after):
                            text = text.rstrip(" ")
                    if not text:
                        continue
                lines.append(Line(f"{pad}#text {_quote(text)}", last_id[0]))
            elif child.kind == "comment":
                text = child.text if verbatim else ASCII_WS.sub(" ", child.text).strip()
                lines.append(Line(f"{pad}#comment {_quote(text)}", last_id[0]))
            elif child.kind == "decl":
                lines.append(Line(f"{pad}<!{ASCII_WS.sub(' ', child.text).strip().lower()}>", last_id[0]))
            elif child.kind == "pi":
                lines.append(Line(f"{pad}<?{child.text}>", last_id[0]))
            else:
                ident = child.get("id")
                if ident:
                    last_id[0] = f"#{ident}"
                lines.append(Line(f"{pad}<{child.tag}{_attrs(child)}>", last_id[0]))
                if child.tag not in VOID:
                    walk(child, depth + 1, verbatim or child.tag in VERBATIM)
                    lines.append(Line(f"{pad}</{child.tag}>", last_id[0]))

    walk(root, 0, False)
    return lines


def find_id(root: Node, ident: str) -> Node:
    matches = []
    todo = [root]
    while todo:
        node = todo.pop()
        if node.kind == "element" and node.get("id") == ident:
            matches.append(node)
        todo.extend(node.children)
    if len(matches) != 1:
        raise EquivalenceError(f"expected one element with id={ident!r}, found {len(matches)}")
    wrapper = Node("root")
    wrapper.children = matches
    return wrapper


def load(path: Path | str, label: str | None = None, section: str | None = None,
         ignore_comments: bool = False, source: str | None = None) -> list[Line]:
    if source is None:
        source = Path(path).read_text(encoding="utf-8")
    root = parse(source, label or str(path))
    if section:
        root = find_id(root, section)
    return canonical(root, ignore_comments)


def digest(lines: list[Line]) -> str:
    h = hashlib.sha256()
    for line in lines:
        h.update(line.text.encode("utf-8"))
        h.update(b"\n")
    return h.hexdigest()


def compare(a: list[Line], b: list[Line], label_a="A", label_b="B",
            max_diffs: int = 10, context: int = 2) -> list[str]:
    """Return a human-readable report; an empty list means equivalent."""
    text_a = [line.text for line in a]
    text_b = [line.text for line in b]
    if text_a == text_b:
        return []
    matcher = difflib.SequenceMatcher(None, text_a, text_b, autojunk=False)
    report = []
    hunks = list(matcher.get_grouped_opcodes(context))
    for hunk in hunks[:max_diffs]:
        first = next(op for op in hunk if op[0] != "equal")
        _, i1, _, j1, _ = first
        where_a = a[min(i1, len(a) - 1)].context if a else "(empty)"
        where_b = b[min(j1, len(b) - 1)].context if b else "(empty)"
        where = where_a if where_a == where_b else f"{where_a} / {where_b}"
        report.append(f"@@ near {where} (canonical lines {i1 + 1} / {j1 + 1})")
        for tag, i1, i2, j1, j2 in hunk:
            if tag == "equal":
                report.extend("  " + t for t in text_a[i1:i2])
                continue
            report.extend(f"- {t}" for t in text_a[i1:i2])
            report.extend(f"+ {t}" for t in text_b[j1:j2])
    if len(hunks) > max_diffs:
        report.append(f"... {len(hunks) - max_diffs} further difference(s) not shown")
    report.insert(0, f"Not equivalent: {label_a} (-) vs {label_b} (+), {len(hunks)} difference(s)")
    return report


def _git_show(rev: str, path: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), "show", f"{rev}:{path}"],
        check=True, capture_output=True, text=True, encoding="utf-8",
    ).stdout


def _git_rev(rev: str) -> str:
    return subprocess.run(
        ["git", "-C", str(ROOT), "rev-parse", rev],
        check=True, capture_output=True, text=True,
    ).stdout.strip()


def record_baseline(rev: str) -> int:
    commit = _git_rev(rev)
    source = _git_show(commit, BOOK.name)
    lines = load(BOOK.name, f"{commit[:7]}:{BOOK.name}", source=source)
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    snapshot = BASELINE_DIR / "baseline.canonical.txt"
    snapshot.write_text("\n".join(l.text for l in lines) + "\n", encoding="utf-8")
    elements = sum(1 for l in lines if l.text.lstrip().startswith("<") and not l.text.lstrip().startswith("</"))
    manifest = {
        "purpose": "Reference for the Markdown conversion: the built book must be equivalent to this.",
        "source": BOOK.name,
        "commit": commit,
        "canonical_sha256": digest(lines),
        "canonical_lines": len(lines),
        "elements": elements,
        "ids": sum(1 for l in lines if ' id="' in l.text),
        "checker": "tools/html_equivalence.py",
    }
    BASELINE_MANIFEST.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Recorded baseline {commit[:7]}: {len(lines)} canonical lines, sha256 {manifest['canonical_sha256'][:12]}")
    print(f"Manifest: {BASELINE_MANIFEST.relative_to(ROOT)}; snapshot: {snapshot.relative_to(ROOT)}")
    return 0


def check_baseline(path: Path, max_diffs: int) -> int:
    manifest = json.loads(BASELINE_MANIFEST.read_text(encoding="utf-8"))
    lines = load(path)
    if digest(lines) == manifest["canonical_sha256"]:
        print(f"Equivalent to baseline {manifest['commit'][:7]} ({len(lines)} canonical lines).")
        return 0
    reference = load(manifest["source"], f"baseline {manifest['commit'][:7]}",
                     source=_git_show(manifest["commit"], manifest["source"]))
    if digest(reference) != manifest["canonical_sha256"]:
        print("Baseline manifest does not match its own commit; the checker's rules have changed. "
              "Re-record deliberately.", file=sys.stderr)
        return 2
    print("\n".join(compare(reference, lines, f"baseline {manifest['commit'][:7]}", str(path), max_diffs)))
    return 1


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("files", nargs="*", type=Path)
    parser.add_argument("--section", help="compare only the element with this id")
    parser.add_argument("--ignore-comments", action="store_true")
    parser.add_argument("--max-diffs", type=int, default=10)
    parser.add_argument("--canonical", type=Path, metavar="OUT",
                        help="write the canonical form of one file and exit")
    parser.add_argument("--record-baseline", action="store_true",
                        help=f"record {BOOK.name} at --commit as the conversion reference")
    parser.add_argument("--commit", default="HEAD")
    parser.add_argument("--check-baseline", action="store_true",
                        help="compare FILE (default the book) with the recorded baseline")
    args = parser.parse_args(argv)
    try:
        if args.record_baseline:
            return record_baseline(args.commit)
        if args.check_baseline:
            return check_baseline(args.files[0] if args.files else BOOK, args.max_diffs)
        if args.canonical:
            if len(args.files) != 1:
                parser.error("--canonical takes exactly one input file")
            lines = load(args.files[0], section=args.section, ignore_comments=args.ignore_comments)
            args.canonical.parent.mkdir(parents=True, exist_ok=True)
            args.canonical.write_text("\n".join(l.text for l in lines) + "\n", encoding="utf-8")
            print(f"Wrote {len(lines)} canonical lines to {args.canonical}")
            return 0
        if len(args.files) != 2:
            parser.error("give two files to compare")
        a, b = (load(f, section=args.section, ignore_comments=args.ignore_comments) for f in args.files)
        report = compare(a, b, str(args.files[0]), str(args.files[1]), args.max_diffs)
        if not report:
            print(f"Equivalent ({len(a)} canonical lines).")
            return 0
        print("\n".join(report))
        return 1
    except (EquivalenceError, OSError, subprocess.CalledProcessError, KeyError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
