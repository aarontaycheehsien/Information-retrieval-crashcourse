"""Convert a section of search-textbook.html to the book's Markdown conventions.

Migration tool for phases 3 and 4 of reviews/markdown-conversion-plan.md.
It writes book/<name>.md plus raw-HTML islands under book/figures/, and
reports every construct it could only keep as raw HTML. It is judged by the
round trip: build the Markdown back with build_md.py, splice it into the
book, run the generators and compare with tools/html_equivalence.py.

Usage:
    python tools/markdown/html_to_md.py SECTION-ID OUT.md

Standard library only.
"""

from __future__ import annotations

import html
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent))

import build_md  # noqa: E402

ROOT = HERE.parents[1]
BOOK = ROOT / "search-textbook.html"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
ASIDES = {"common-confusion", "practice-callout", "question-callout", "orientation", "distinction-map",
          "part-recap", "ai-disclosure-notice"}
PARA_CLASSES = {"chapter-transition", "key-distinction-label", "exercise-deliverable", "worked-note",
                "ir-figure-note", "practice-callout", "equation-scroll"}
PLAIN_DIVS = {"terminology-overlaps", "terminology-overlap", "svg-scroll", "semantic-scholar-comparison",
              "semantic-scholar-shot", "evidence-stack"}
ELEMENT_SPANS = {"var", "small", "b", "output"}
CLAIMS = re.compile(r"<!-- BEGIN PRODUCT CLAIMS LINKS .*?<!-- END PRODUCT CLAIMS LINKS [^>]*-->\n?", re.S)
WS = re.compile(r"[ \t\n\r\f]+")
MATH = re.compile(r"\\\((.+?)\\\)|\$\$(.+?)\$\$", re.S)
SENTENCE_BREAK = re.compile(r"(?<=[.?!])([”’)]?) (?=[A-Z“‘])")


class N:
    __slots__ = ("kind", "tag", "attrs", "children", "text", "start", "end")

    def __init__(self, kind, tag="", attrs=None, text="", start=0):
        self.kind, self.tag, self.attrs, self.text, self.start = kind, tag, dict(attrs or {}), text, start
        self.children, self.end = [], start

    @property
    def classes(self):
        return (self.attrs.get("class") or "").split()

    def elements(self):
        return [c for c in self.children if c.kind == "element"]


class Parser(HTMLParser):
    """Tree with source offsets, so raw islands keep their original markup."""

    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.source = source
        self.lines = [0]
        for m in re.finditer("\n", source):
            self.lines.append(m.end())
        self.root = N("root")
        self.stack = [self.root]

    def _pos(self):
        line, col = self.getpos()
        return self.lines[line - 1] + col

    def handle_starttag(self, tag, attrs):
        start = self._pos()
        node = N("element", tag, attrs, start=start)
        node.end = self.source.index(">", start) + 1
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        start = self._pos()
        node = N("element", tag, attrs, start=start)
        node.end = self.source.index(">", start) + 1
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag):
        node = self.stack.pop()
        if node.tag != tag:
            raise ValueError(f"</{tag}> closes <{node.tag}>")
        node.end = self.source.index(">", self._pos()) + 1

    def handle_data(self, data):
        self.stack[-1].children.append(N("text", text=data, start=self._pos()))

    def handle_comment(self, data):
        start = self._pos()
        node = N("comment", text=data, start=start)
        node.end = self.source.index("-->", start) + 3
        self.stack[-1].children.append(node)


def find(node, ident):
    if node.kind == "element" and node.attrs.get("id") == ident:
        return node
    for child in node.children:
        hit = find(child, ident)
        if hit:
            return hit
    return None


def text_of(node):
    if node.kind == "text":
        return node.text
    return "".join(text_of(c) for c in node.children)


def quote_attr(value):
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def attr_block(ident=None, classes=(), pairs=()):
    parts = [f"#{ident}"] if ident else []
    parts += [f".{c}" for c in classes]
    parts += [f"{k}={quote_attr(v)}" for k, v in pairs]
    return "{" + " ".join(parts) + "}"


class Converter:
    def __init__(self, source, figures_dir: Path, figures_rel="figures"):
        self.source = source
        self.figures_dir = figures_dir
        self.figures_rel = figures_rel
        self.warnings: list[str] = []
        self.islands: dict[str, str] = {}
        self.footnotes: list[str] = []

    def slice(self, node):
        return self.source[node.start:node.end]

    def warn(self, node, why):
        ident = node.attrs.get("id") or ""
        self.warnings.append(f"<{node.tag} {'.'.join(node.classes)}#{ident}> {why}")

    def raw_block(self, node_or_text, why=None, node=None):
        text = node_or_text if isinstance(node_or_text, str) else self.slice(node_or_text)
        if why and node is not None:
            self.warn(node, why)
        fence = "```"
        while fence in text:
            fence += "`"
        return f"{fence}{{=html}}\n{CLAIMS.sub('', text).strip()}\n{fence}"

    # ---- inline -------------------------------------------------------

    def esc(self, text, breaks):
        """Escape prose; MathJax-delimited TeX in the text becomes Pandoc maths."""
        parts = MATH.split(text)
        if len(parts) > 1:
            out = []
            for i, part in enumerate(parts):
                if i % 3 == 0:
                    out.append(self.esc_plain(part, breaks))
                elif i % 3 == 1 and part is not None:
                    out.append("$" + WS.sub(" ", part).strip() + "$")
                elif i % 3 == 2 and part is not None:
                    out.append("$$\n" + part.strip("\n") + "\n$$")
            return "".join(out)
        return self.esc_plain(text, breaks)

    def esc_plain(self, text, breaks):
        text = WS.sub(" ", text)
        text = text.replace("\\", "\\\\")
        text = re.sub(r"([`*_\[\]<>$^~#|{}])", r"\\\1", text)
        text = re.sub(r"&(?=[A-Za-z#][A-Za-z0-9]*;)", r"\\&", text)
        text = text.replace(" ", "\\ ")
        if breaks:
            text = SENTENCE_BREAK.sub(lambda m: m[1] + "\n", text)
        return text

    def inline(self, nodes, breaks=True):
        out = []
        for n in nodes:
            if n.kind == "text":
                out.append(self.esc(n.text, breaks))
            elif n.kind == "comment":
                out.append(f"<!--{n.text}-->")
            else:
                out.append(self.inline_element(n, breaks))
        return "".join(out)

    def wrap(self, mark, inner):
        lead = len(inner) - len(inner.lstrip(" "))
        trail = len(inner) - len(inner.rstrip(" "))
        core = inner.strip(" ")
        if not core:
            return inner
        return " " * lead + mark + core + mark + " " * trail

    def inline_element(self, n, breaks):
        tag, a, cls = n.tag, n.attrs, n.classes
        if tag in ("strong", "em") and not a:
            return self.wrap("**" if tag == "strong" else "*", self.inline(n.children, breaks))
        if tag == "em" and cls == ["verdict"]:
            return f"[*{self.inline(n.children, breaks)}*]{{.verdict}}"
        if tag == "code" and not a:
            text = WS.sub(" ", text_of(n))
            ticks = "`"
            while ticks in text:
                ticks += "`"
            pad = " " if text.startswith("`") or text.endswith("`") else ""
            return f"{ticks}{pad}{text}{pad}{ticks}"
        if tag == "a" and "href" in a:
            href = a["href"]
            dest = f"<{href}>" if re.search(r"[ ()<>]", href) else href
            title = f' "{a["title"]}"' if "title" in a else ""
            rest = [(k, v or "") for k, v in a.items() if k not in ("href", "title", "class", "id")]
            extra = attr_block(a.get("id"), cls, rest) if (rest or cls or a.get("id")) else ""
            return f"[{self.inline(n.children, breaks)}]({dest}{title}){extra}"
        if tag == "span":
            rest = [(k, v or "") for k, v in a.items() if k not in ("class", "id")]
            if len(cls) == 1 and cls[0] in ELEMENT_SPANS:
                pass
            return f"[{self.inline(n.children, breaks)}]{attr_block(a.get('id'), cls, rest)}"
        if tag in ELEMENT_SPANS and not a:
            return f"[{self.inline(n.children, breaks)}]{{.{tag}}}"
        if tag == "br" and not a:
            return "\\\n"
        if tag == "sup" and a.get("id", "").startswith("fnref:"):
            name = a["id"][len("fnref:"):]
            self.footnotes.append(name)
            return f"[^{name}]"
        if tag == "sub" and not a:
            return "~" + self.inline(n.children, False).replace(" ", "\\ ") + "~"
        self.warn(n, "inline element kept as raw HTML")
        return self.slice(n) if tag in VOID else (
            self.source[n.start:self.open_end(n)] + self.inline(n.children, breaks) + f"</{tag}>")

    def open_end(self, n):
        return self.source.index(">", n.start) + 1

    # ---- block helpers ------------------------------------------------

    def para_text(self, nodes, breaks=True):
        text = self.inline(nodes, breaks).strip()
        text = re.sub(r" *\n *", "\n", text)
        # A paragraph must not start like another block.
        text = re.sub(r"^(\d+|[A-Za-z]|[ivxlcdmIVXLCDM]+|#)([.)])(?=[ \n]|$)", r"\1\\\2", text)
        text = re.sub(r"^([-+:>%=]|\(@)", r"\\\1", text)
        return text

    def blocks(self, nodes):
        out = []
        skip_claims = False
        for n in nodes:
            if n.kind == "comment":
                if n.text.strip().startswith("BEGIN PRODUCT CLAIMS LINKS"):
                    skip_claims = True
                elif n.text.strip().startswith("END PRODUCT CLAIMS LINKS"):
                    skip_claims = False
                else:
                    out.append(f"<!--{n.text}-->")
                continue
            if skip_claims:
                continue
            if n.kind == "text":
                if n.text.strip():
                    self.warnings.append(f"loose text at block level: {n.text.strip()[:40]!r}")
                    out.append(self.para_text([n]))
                continue
            converted = self.block(n, nodes)
            if converted is not None:
                out.append(converted)
        return [b for b in out if b != ""]

    def join(self, blocks):
        return "\n\n".join(blocks)

    def indent(self, text, prefix):
        return "\n".join((prefix + line) if line else "" for line in text.split("\n"))

    def fenced(self, attrs, body, colons=3):
        inner = body
        depth = max([len(m) for m in re.findall(r"^(:{3,})", inner, re.M)] or [0])
        fence = ":" * max(colons, depth + 1)
        return f"{fence} {attrs}\n{inner}\n{fence}" if inner else f"{fence} {attrs}\n{fence}"

    # ---- blocks -------------------------------------------------------

    def block(self, n, siblings):
        tag, a, cls = n.tag, n.attrs, n.classes
        if getattr(self, "_consumed", None) is n:
            return ""
        if tag == "p":
            return self.paragraph(n, siblings)
        if tag in ("h3", "h4", "h5"):
            kids = [c for c in n.children if not (c.kind == "element" and "heading-anchor" in c.classes)]
            extra = [f"#{a['id']}"] if "id" in a else []
            extra += [f".{c}" for c in cls]
            text = self.inline(kids, False).strip().replace("{", "\\{")
            return "#" * int(tag[1]) + " " + text + (" {" + " ".join(extra) + "}" if extra else "")
        if tag == "blockquote":
            inner = self.join(self.blocks(n.children))
            quoted = "\n".join(("> " + line) if line else ">" for line in inner.split("\n"))
            if cls == ["pull-quote"] and len(a) == 1:
                return self.fenced(".pull-quote", quoted).replace("::: .pull-quote", "::: pull-quote")
            if a:
                return self.raw_block(n, "blockquote with attributes", n)
            return quoted
        if tag in ("ul", "ol") and not (set(a) - {"start"}):
            return self.listing(n)
        if tag == "pre" and not a:
            kids = n.elements()
            if len(kids) != 1 or kids[0].tag != "code" or kids[0].attrs or any(
                    c.kind == "text" and c.text.strip() for c in n.children):
                return self.raw_block(n, "pre without a single plain code child", n)
            text = text_of(kids[0])
            fence = "```"
            while fence in text:
                fence += "`"
            return f"{fence}\n{text}\n{fence}"
        if tag == "div" and cls == ["table-wrap"]:
            return None  # emitted with its label paragraph
        if tag == "figure" and "ir-figure" in cls:
            return self.figure(n)
        if tag == "aside" and len(cls) == 1 and cls[0] in ASIDES:
            return self.aside(n)
        if tag == "aside" and cls == ["chapter-close"]:
            return self.chapter_close(n)
        if tag == "section" and cls == ["self-check"]:
            return self.self_check(n)
        if tag == "details" and set(a) <= {"class"} and not ({"claim-links", "self-check-q"} & set(cls)):
            kids = n.elements()
            summary = kids[0]
            body = self.blocks(n.children[n.children.index(summary) + 1:])
            classes = ".details" + "".join(f" .{c}" for c in cls)
            return self.fenced("{" + classes + "}", self.join([self.para_text(summary.children, False)] + body))
        if tag == "div" and cls == ["chapter-orient"]:
            return self.fenced("chapter-orient", self.join(self.blocks(n.children)))
        if tag == "div" and cls == ["stage-map"]:
            return self.stage_map(n)
        if tag == "nav" and cls == ["chapter-nav"]:
            return ""  # derived
        if tag == "span" and cls == ["legacy-anchor"] and not n.children:
            return f"::: {{#{a['id']} .legacy-anchor}}\n:::"
        if tag == "div" and len(cls) == 1 and cls[0] in PLAIN_DIVS and set(a) == {"class"}:
            return self.fenced("{." + cls[0] + "}", self.join(self.blocks(n.children)))
        return self.raw_block(n, "block kept as raw HTML", n)

    def paragraph(self, n, siblings):
        a, cls = n.attrs, n.classes
        if cls == ["asset-label"]:
            return self.table(n, siblings)
        text = self.para_text(n.children)
        if not a:
            return text
        if set(a) <= {"id", "class"} and (not cls or (len(cls) == 1 and cls[0] in PARA_CLASSES)):
            return self.fenced(attr_block(a.get("id"), cls), text)
        if set(a) <= {"id", "class", "tabindex", "role", "aria-label"} and cls == ["equation-scroll"]:
            pairs = [(k, v) for k, v in a.items() if k not in ("id", "class")]
            return self.fenced(attr_block(a.get("id"), cls, pairs), text)
        return self.raw_block(n, "paragraph with unmapped attributes", n)

    def listing(self, n):
        ordered = n.tag == "ol"
        items = [c for c in n.children if c.kind == "element"]
        if any(c.tag != "li" for c in items):
            return self.raw_block(n, "list with non-li children", n)
        blocky = {"p", "blockquote", "pre", "div", "figure", "table", "details", "aside", "dl"}
        loose = any(k.kind == "element" and k.tag in blocky for li in items for k in li.children)
        out = []
        number = int(n.attrs.get("start", "1"))
        for li in items:
            marker = f"{number}. " if ordered else "- "
            number += 1
            if loose:
                body = self.join(self.blocks(li.children))
            else:
                parts, run = [], []
                for k in li.children:
                    if k.kind == "element" and k.tag in ("ul", "ol"):
                        if run:
                            parts.append(self.para_text(run))
                            run = []
                        parts.append(self.listing(k))
                    else:
                        run.append(k)
                if run:
                    parts.append(self.para_text(run))
                body = "\n".join(parts)
            if li.attrs:
                if set(li.attrs) == {"id"}:
                    body = f"[]{{#{li.attrs['id']} .li-id}}" + body
                else:
                    self.warn(li, "list item attributes dropped")
            lines = body.split("\n")
            out.append(marker + lines[0] + ("\n" + self.indent("\n".join(lines[1:]), " " * len(marker)) if len(lines) > 1 else ""))
        return ("\n\n" if loose else "\n").join(out)

    def table(self, label, siblings):
        i = siblings.index(label)
        wrap = next((s for s in siblings[i + 1:] if s.kind == "element"), None)
        if not (wrap is not None and wrap.tag == "div" and wrap.classes == ["table-wrap"]):
            return self.raw_block(label, "asset label not followed by a table", label)
        table = wrap.elements()[0]
        caption = self.inline(label.children, False).strip()
        caption = re.sub(r"^Table [0-9A-Z]+\.\d+ — ", "", caption)
        rows = []
        for section in table.elements():
            for tr in section.elements():
                rows.append((section.tag, [self.inline(td.children, False).strip().replace("|", "\\|") for td in tr.elements()]))
        if not rows or rows[0][0] != "thead" or table.attrs or any(
                td.attrs for s in table.elements() for tr in s.elements() for td in tr.elements()):
            return self.raw_block(self.source[label.start:wrap.end], "table kept as raw HTML", label)
        head = rows[0][1]
        lines = ["| " + " | ".join(head) + " |", "|" + "|".join("---" for _ in head) + "|"]
        lines += ["| " + " | ".join(r[1]) + " |" for r in rows[1:]]
        return "\n".join(lines) + "\n\n: " + caption

    def figure(self, n):
        a = n.attrs
        kids = n.elements()
        title, caption = kids[0], kids[-1]
        if not ("figure-title" in title.classes and caption.tag == "figcaption"):
            return self.raw_block(n, "figure without title and caption", n)
        title_id = title.attrs.get("id")
        key = (title_id or a.get("aria-labelledby") or "").removesuffix("-title")
        pairs = [("key", key)]
        if title_id != f"{key}-title":
            pairs.append(("title-id", title_id or ""))
        if a.get("aria-labelledby") != (title_id or None):
            pairs.append(("aria-labelledby", a.get("aria-labelledby", "")))
        for k in a:
            if k not in ("class", "aria-labelledby"):
                pairs.append((k, a[k]))
        classes = ["figure"] + [c for c in n.classes if c != "ir-figure"]
        body_nodes = n.children[n.children.index(title) + 1:n.children.index(caption)]
        body = []
        elements, in_claims = [], False
        for b in body_nodes:  # generated claims blocks are not part of the island
            if b.kind == "comment" and "PRODUCT CLAIMS LINKS" in b.text:
                in_claims = b.text.strip().startswith("BEGIN")
            elif b.kind == "element" and not in_claims:
                elements.append(b)
        if len(elements) == 1 and elements[0].tag == "img":
            body.append(self.image(elements[0]))
        elif elements:
            text = CLAIMS.sub("", self.source[elements[0].start:elements[-1].end])
            path = f"{self.figures_rel}/{key}.html"
            self.islands[path] = text.strip() + "\n"
            body.append(f"::: {{.include src={quote_attr(path)}}}\n:::")
        cap_kids = [c for c in caption.children if not (c.kind == "element" and "asset-label-inline" in c.classes)]
        cap_attrs = attr_block(caption.attrs.get("id"), ["caption"]) if caption.attrs.get("id") else "caption"
        cap = self.fenced(cap_attrs, self.para_text(cap_kids))
        inner = self.join([self.para_text(title.children, False)] + body + [cap])
        return self.fenced(attr_block(None, classes, pairs), inner)

    def image(self, img):
        a = dict(img.attrs)
        src = a.pop("src")
        alt = a.pop("alt", "")
        pairs = []
        derived = derive_srcset(src, a.get("width"))
        if derived and a.get("srcset") == derived and a.get("sizes") == DEFAULT_SIZES:
            a.pop("srcset")
            a.pop("sizes")
        elif derived and "srcset" not in a:
            a["srcset"] = "none"  # the filter would otherwise derive one
        if a.get("loading") == "lazy":
            a.pop("loading")
        for k in ("width", "height", "loading", "srcset", "sizes"):
            if k in a:
                pairs.append((k, a.pop(k)))
        if a:
            self.warn(img, f"image attributes dropped: {sorted(a)}")
        dest = f"<{src}>" if re.search(r"[ ()<>]", src) else src
        return f"![{self.esc(alt, False)}]({dest}){attr_block(None, (), pairs)}"

    def aside(self, n):
        cls = n.classes[0]
        a = n.attrs
        kids = n.elements()
        pairs = []
        body_start = 0
        if kids and kids[0].tag == "p" and len(kids[0].classes) == 1 and kids[0].classes[0].endswith("label"):
            pairs.append(("label", text_of(kids[0])))
            if kids[0].classes[0] != f"{cls}-label":
                pairs.append(("label-class", kids[0].classes[0]))
            body_start = n.children.index(kids[0]) + 1
        rest = n.children[body_start:]
        first = next((c for c in rest if c.kind == "element"), None)
        derived = first.attrs.get("id") if first is not None and first.tag in ("h4", "h5", "h3") and "aria-label" not in a else None
        if a.get("aria-labelledby") != derived:
            if "aria-labelledby" in a:
                pairs.append(("aria-labelledby", a["aria-labelledby"]))
        if "aria-label" in a:
            pairs.append(("aria-label", a["aria-label"]))
        unknown = set(a) - {"class", "id", "aria-labelledby", "aria-label"}
        if unknown:
            return self.raw_block(n, f"aside attributes {sorted(unknown)}", n)
        return self.fenced(attr_block(a.get("id"), [cls], pairs), self.join(self.blocks(rest)))

    def chapter_close(self, n):
        kids = n.elements()
        pairs = []
        if n.attrs.get("aria-label") != "Chapter summary":
            pairs.append(("aria-label", n.attrs.get("aria-label", "")))
        label = kids[0]
        if text_of(label) != "What this chapter established":
            pairs.append(("label", text_of(label)))
        body = self.blocks(n.children[n.children.index(label) + 1:])
        return self.fenced(attr_block(None, ["chapter-close"], pairs) if pairs else "chapter-close", self.join(body))

    def self_check(self, n):
        items = []
        for d in n.elements()[1:]:
            if d.tag != "details" or d.classes != ["self-check-q"]:
                return self.raw_block(n, "unexpected self-check child", n)
            summary = d.elements()[0]
            answer = self.join(self.blocks(d.children[d.children.index(summary) + 1:]))
            items.append(self.para_text(summary.children, False).replace("\n", " ") + "\n\n:   "
                         + self.indent(answer, "    ").lstrip())
        return self.fenced("self-check", "\n\n".join(items))

    def stage_map(self, n):
        data = build_md.load_stage_map()
        label_to_key = {s["label_html"]: s["key"] for s in data["stages"]}
        source = self.slice(n)
        on = [label_to_key.get(x, "?") for x in re.findall(r'class="stage on"[^>]*>(.*?)</a>', source)]
        controller = "on" if "stage-controller on" in source else "off"
        label = html.unescape(n.attrs.get("aria-label", ""))
        label = "" if label == data["default_label"] else label
        try:
            if build_md.render_stage_map(on, controller, label, data) == source:
                pairs = [("on", " ".join(on))]
                if controller == "on":
                    pairs.append(("controller", "on"))
                if label:
                    pairs.append(("label", label))
                return f"::: {attr_block(None, ['stage-map'], pairs)}\n:::"
        except build_md.BuildError:
            pass
        return self.raw_block(n, "stage map does not match the template", n)

    # ---- footnotes ----------------------------------------------------

    def footnote_definitions(self, root):
        """[^name]: definitions for the references met, in order of use."""
        out = []
        for name in self.footnotes:
            li = find(root, f"fn:{name}")
            if li is None:
                self.warnings.append(f"footnote {name} has no definition")
                continue
            blocks = [c for c in li.children if not (c.kind == "text" and not c.text.strip())]
            last = blocks[-1]
            kids = last.children
            if not (kids and kids[-1].kind == "element" and "footnote-backref" in kids[-1].classes):
                self.warn(li, "footnote without a trailing backlink")
            else:
                kids = kids[:-1]
                if kids and kids[-1].kind == "text":
                    kids[-1].text = kids[-1].text.rstrip(" \u00a0")
                last.children = kids
            body = self.join(self.blocks(blocks))
            first, _, rest = body.partition("\n")
            out.append(f"[^{name}]: {first}" + ("\n" + self.indent(rest, "    ") if rest else ""))
        return "\n\n".join(out)

    # ---- chapter ------------------------------------------------------

    def chapter(self, section):
        meta = {}
        cls = section.classes
        kind = "appendix" if "appendix" in cls else "backsection" if "backsection" in cls else "chapter"
        sid = section.attrs["id"]
        legacy = []
        header = None
        body_nodes = []
        for c in section.children:
            if header is None and c.kind == "element" and c.tag == "span" and c.classes == ["legacy-anchor"]:
                legacy.append(c.attrs["id"])
            elif header is None and c.kind == "element" and c.tag == "header":
                header = c
            elif header is not None:
                body_nodes.append(c)
        head_blocks = []
        for c in header.elements():
            if c.classes == ["chapter-eyebrow"]:
                meta["eyebrow"] = text_of(c)
            elif c.classes == ["chapter-meta"]:
                meta["meta"] = text_of(c)
            elif c.tag == "h2":
                key = c.attrs["id"]
                title = self.inline(c.children, False).strip()
            elif c.classes == ["chapter-question"]:
                kids = c.children[1:] if c.children and c.children[0].kind == "element" and c.children[0].tag == "span" else c.children
                meta["question"] = self.inline(kids, False).strip()
            else:
                head_blocks.append(self.block(c, header.children))
        if sid != f"sec-{key}":
            self.warnings.append(f"section id {sid} is not sec-{key}")
        front = {"key": key, "kind": kind, **meta}
        if legacy:
            front["legacy_anchors"] = legacy
        lines = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in front.items()] + ["---"]
        body = [f"## {title} {{#{key}}}"] + head_blocks + self.blocks(body_nodes)
        return "\n".join(lines) + "\n\n" + self.join(body) + "\n"


DEFAULT_SIZES = "(max-width: 800px) 100vw, 760px"


def derive_srcset(src, width):
    """The rule book.lua applies: only when the .960.webp sibling exists."""
    if not src.endswith(".png") or not width:
        return None
    webp = src[:-4].replace(",", "%2C") + ".960.webp"
    if not (ROOT / unquote(webp)).exists():
        return None
    return f"{webp} 960w, {src} {width}w"


def convert(section_id, out_md: Path, source=None):
    source = source if source is not None else BOOK.read_text(encoding="utf-8")
    parser = Parser(source)
    parser.feed(source)
    parser.close()
    section = find(parser.root, section_id)
    if section is None:
        raise SystemExit(f"no element with id {section_id}")
    conv = Converter(source, out_md.parent / "figures")
    text = conv.chapter(section)
    notes = conv.footnote_definitions(parser.root)
    if notes:
        text += "\n" + notes + "\n"
    out_md.parent.mkdir(parents=True, exist_ok=True)
    out_md.write_text(text, encoding="utf-8")
    for rel, content in conv.islands.items():
        path = out_md.parent / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    return conv


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 2:
        raise SystemExit(__doc__)
    conv = convert(argv[0], Path(argv[1]))
    print(f"Wrote {argv[1]} and {len(conv.islands)} raw-HTML island(s).")
    for w in conv.warnings:
        print("warning:", w)
    return 0


if __name__ == "__main__":
    sys.exit(main())
