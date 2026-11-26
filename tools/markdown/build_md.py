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


def split_footnotes(fragment: str) -> tuple[str, str]:
    body, _, notes = fragment.partition("<!-- FOOTNOTE DEFINITIONS -->")
    return body.rstrip("\n") + "\n", notes.strip("\n")


def build_file(path: Path, book_dir: Path = BOOK_DIR) -> tuple[str, str]:
    """Return (section HTML, footnote <li> items) for one Markdown file."""
    text = Path(path).read_text(encoding="utf-8")
    return split_footnotes(postpass(pandoc(prepass(text), book_dir)))


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
