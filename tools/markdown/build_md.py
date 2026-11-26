"""Build textbook HTML from the Markdown sources.

Phase 3 of reviews/markdown-conversion-plan.md. One Markdown file becomes
one HTML fragment:

1. pre-pass: keep footnote names, which Pandoc's AST would drop;
2. Pandoc with tools/markdown/book.lua renders the mapping's conventions;
3. post-pass: expand stage-map placeholders from data/stage-map.json.

Book-level steps run after the fragments are assembled: fill_chapter_navs()
derives previous/next navigation from section order. Existing generators
(maintain.py, product claims, glossary) then run on the assembled page as now.

Standard library plus the pandoc executable (3.1 tested).
"""

from __future__ import annotations

import html
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BOOK_DIR = ROOT / "book"
FILTER = Path(__file__).with_name("book.lua")
STAGE_MAP = ROOT / "data" / "stage-map.json"
READER = "markdown-smart-auto_identifiers-implicit_figures-citations-raw_tex"

FOOTNOTE_DEF = re.compile(r"^\[\^([A-Za-z0-9_:.-]+)\]:[ \t]*", re.M)
STAGE_PLACEHOLDER = re.compile(r'<!-- STAGE MAP on="([^"]*)" controller="([^"]*)" label="([^"]*)" -->')


class BuildError(Exception):
    pass


def prepass(text: str) -> str:
    """Start each footnote definition with a span carrying its name."""
    return FOOTNOTE_DEF.sub(lambda m: f"[^{m[1]}]: []{{.fn-name name={m[1]}}}", text)


def pandoc(text: str, book_dir: Path = BOOK_DIR) -> str:
    env = dict(os.environ, BOOK_DIR=str(book_dir), ROOT_DIR=str(ROOT))
    result = subprocess.run(
        ["pandoc", "-f", READER, "-t", "html5", "--wrap=none", "--lua-filter", str(FILTER)],
        input=text, capture_output=True, text=True, encoding="utf-8", env=env,
    )
    if result.returncode != 0:
        raise BuildError(result.stderr.strip())
    return result.stdout


def load_stage_map() -> dict:
    return json.loads(STAGE_MAP.read_text(encoding="utf-8"))


def render_stage_map(on: list[str], controller: str = "off", label: str = "", data: dict | None = None) -> str:
    data = data or load_stage_map()
    keys = [s["key"] for s in data["stages"]]
    unknown = set(on) - set(keys)
    if unknown:
        raise BuildError(f"unknown stage key(s): {', '.join(sorted(unknown))}")
    if controller not in ("on", "off"):
        raise BuildError(f"controller must be on or off, not {controller!r}")
    links = "".join(
        f'<a class="stage {"on" if s["key"] in on else "off"}" href="{s["href"]}" '
        f'title="{html.escape(s["title"], quote=True)}">{s["label_html"]}</a>'
        for s in data["stages"])
    return (f'<div class="stage-map" role="group" aria-label="{html.escape(label or data["default_label"], quote=True)}">'
            f'<div class="stage-controller {controller}">{data["controller_text"]}</div>'
            f'<div class="stage-row">{links}</div></div>')


def postpass(fragment: str) -> str:
    data = None

    def expand(m):
        nonlocal data
        data = data or load_stage_map()
        return render_stage_map(m[1].split(), m[2], html.unescape(m[3]), data)

    return STAGE_PLACEHOLDER.sub(expand, fragment)


FILE_RECORD = re.compile(r"<!-- BOOK FILE (\{.*?\}) -->\n?")


def split_footnotes(fragment: str) -> tuple[str, str]:
    body, _, notes = fragment.partition("<!-- FOOTNOTE DEFINITIONS -->")
    return body.rstrip("\n") + "\n", notes.strip("\n")


def build_file_with_record(path: Path, book_dir: Path = BOOK_DIR) -> tuple[str, str, dict]:
    """Return (HTML, footnote <li> items, file record) for one source file.

    An .html file is a verbatim fragment (generated-region markers)."""
    path = Path(path)
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".html":
        return text.rstrip("\n") + "\n", "", {"kind": "html", "nav": "none"}
    html_out = postpass(pandoc(prepass(text), book_dir))
    record = FILE_RECORD.search(html_out)
    if not record:
        raise BuildError(f"{path}: the filter wrote no file record")
    info = json.loads(record[1])
    info["source"] = path.name
    body, notes = split_footnotes(FILE_RECORD.sub("", html_out, count=1))
    return body, notes, info


def build_file(path: Path, book_dir: Path = BOOK_DIR) -> tuple[str, str]:
    """Return (section HTML, footnote <li> items) for one Markdown file."""
    body, notes, _ = build_file_with_record(path, book_dir)
    return body, notes


# --- Book-level derivation -------------------------------------------------

SECTION_OPEN = re.compile(r'<section class="(chapter[^"]*|exercise)" id="([^"]+)">')
H2 = re.compile(r'<h2(?: [^>]*)?>(.*?)</h2>', re.S)
NAV_PLACEHOLDER = "<!-- CHAPTER NAV -->"


def _sections(book: str):
    """Top-level navigable sections in order: (start, id, h2 id, h2 inner HTML)."""
    out = []
    for m in SECTION_OPEN.finditer(book):
        h2 = H2.search(book, m.end())
        h2_id = re.search(r'\bid="([^"]+)"', h2.group(0))
        out.append((m.start(), m[2], h2_id[1] if h2_id else m[2], h2[1]))
    return out


def fill_chapter_navs(book: str) -> str:
    """Replace each nav placeholder with links to the neighbouring sections.

    Default rule only: the neighbour's h2 id and h2 text. The current book
    hand-shortens exercise titles and labels appendices "Appendix X · …";
    those cases need front-matter overrides before they can be derived (phase 4).
    """
    sections = _sections(book)
    pieces, last = [], 0
    for m in re.finditer(re.escape(NAV_PLACEHOLDER), book):
        index = max(i for i, s in enumerate(sections) if s[0] < m.start())
        links = []
        if index > 0:
            _, _, href, title = sections[index - 1]
            links.append(f'<a class="cnav prev" href="#{href}"><span>Previous</span>{title}</a>')
        if index + 1 < len(sections):
            _, _, href, title = sections[index + 1]
            links.append(f'<a class="cnav next" href="#{href}"><span>Next</span>{title}</a>')
        pieces += [book[last:m.start()], f'<nav class="chapter-nav" aria-label="Chapter navigation">{"".join(links)}</nav>']
        last = m.end()
    pieces.append(book[last:])
    return "".join(pieces)


def nav_title(rec: dict) -> str:
    """How neighbours refer to a file in previous/next navigation."""
    if rec.get("nav_title"):
        return rec["nav_title"]
    title = rec["title"]
    if rec["kind"] == "exercise":
        return title.split(" — ")[0]
    if rec["kind"] == "appendix":
        return f'{rec["eyebrow"]} · {title}'
    return title


def render_nav(rec: dict, prev: dict | None, nxt: dict | None) -> str:
    appendix = rec["kind"] == "appendix"
    links = []
    for side, other, word in (("prev", prev, "Previous"), ("next", nxt, "Next")):
        if other is None:
            continue
        label = f"{word} appendix" if appendix and other["kind"] == "appendix" else word
        links.append(f'<a class="cnav {side}" href="#{other["href"]}"><span>{label}</span>{nav_title(other)}</a>')
    aria = "Appendix navigation" if appendix else "Chapter navigation"
    return f'<nav class="chapter-nav" aria-label="{aria}">{"".join(links)}</nav>'


def assemble(parts: list[tuple[str, str, dict]], template: str) -> str:
    """Join built files in order, derive navigation, append the footnotes."""
    # "both": has a bar and is linked to; "target": linked to only as the
    # next item (the back-matter divider, the glossary), never as previous.
    sequence = [rec for _, _, rec in parts if rec["nav"] in ("both", "target")]
    bodies = []
    for html_body, _, rec in parts:
        if rec["nav"] == "both":
            i = sequence.index(rec)
            prev = next((r for r in reversed(sequence[:i]) if r["nav"] == "both"), None)
            nav = render_nav(rec, prev, sequence[i + 1] if i + 1 < len(sequence) else None)
            if html_body.count(NAV_PLACEHOLDER) != 1:
                raise BuildError(f"{rec['source']}: expected one navigation placeholder")
            html_body = html_body.replace(NAV_PLACEHOLDER, nav)
        bodies.append(html_body.rstrip("\n"))
    notes = [n for _, n, _ in parts if n]
    if notes:
        bodies.append('<section class="footnotes">\n<hr>\n<ol>\n' + "\n".join(notes) + "\n</ol>\n</section>")
    if template.count(BODY_PLACEHOLDER) != 1:
        raise BuildError("template needs exactly one body placeholder")
    return template.replace(BODY_PLACEHOLDER, "\n".join(bodies))


BODY_PLACEHOLDER = "<!-- BOOK BODY -->"
TEMPLATE = BOOK_DIR / "template.html"
GENERATOR_PASSES = [
    ["tools/maintain.py"],
    ["tools/renumber_footnotes.py"],
    ["tools/build-product-claims.py"],
    ["tools/build-glossary-hub.py"],
]
COMPANION_BUILDERS = [["tools/build-digest.py"], ["tools/build-vendor-questionnaire.py"]]


def source_files(book_dir: Path = BOOK_DIR) -> list[Path]:
    files = sorted(p for p in book_dir.iterdir() if re.match(r"\d{2}-.*\.(md|html)$", p.name))
    if not files:
        raise BuildError(f"no NN-*.md or NN-*.html files in {book_dir}")
    return files


def build_book(book_dir: Path = BOOK_DIR, repo: Path = ROOT, passes: int = 4) -> dict:
    """Build repo/search-textbook.html from book_dir, then run the generators
    until a whole round changes nothing, then rebuild the companion pages.

    repo is normally a scratch copy of the repository until cut-over."""
    import sys
    template = (book_dir / "template.html").read_text(encoding="utf-8")
    parts = [build_file_with_record(p, book_dir) for p in source_files(book_dir)]
    target = Path(repo) / "search-textbook.html"
    target.write_text(assemble(parts, template), encoding="utf-8")
    log = []
    for round_no in range(1, passes + 1):
        before = target.read_bytes()
        for cmd in GENERATOR_PASSES:
            r = subprocess.run([sys.executable, *cmd], cwd=repo, capture_output=True, text=True)
            log.append((round_no, " ".join(cmd), r.returncode, (r.stdout + r.stderr).strip()))
            if r.returncode and cmd[0] != "tools/maintain.py":
                raise BuildError(f"{' '.join(cmd)} failed:\n{(r.stdout + r.stderr).strip()}")
        if target.read_bytes() == before:
            break
    else:
        raise BuildError(f"generators did not settle after {passes} rounds")
    # maintain.py may report links to generated targets in early rounds; by
    # the settled round it must report nothing.
    final = [e for e in log if e[0] == round_no and e[1] == "tools/maintain.py"]
    if final and final[-1][2]:
        raise BuildError(f"maintain.py still reports problems after settling:\n{final[-1][3]}")
    for cmd in COMPANION_BUILDERS:
        r = subprocess.run([sys.executable, *cmd], cwd=repo, capture_output=True, text=True)
        log.append(("companion", " ".join(cmd), r.returncode, (r.stdout + r.stderr).strip()))
        if r.returncode:
            raise BuildError(f"{' '.join(cmd)} failed:\n{(r.stdout + r.stderr).strip()}")
    return {"files": len(parts), "rounds": round_no, "log": log}
