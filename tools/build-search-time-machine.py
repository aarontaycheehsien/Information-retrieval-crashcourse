#!/usr/bin/env python3
"""Build search-time-machine.html, the "one query, seven decades" companion.

The page searches the textbook itself with seven generations of retrieval
method. This builder:

  1. extracts the book's sections, paragraphs, cross-references and glossary
     from search-textbook.html (standard library only);
  2. embeds that corpus, the cached word vectors and the browser engine into
     tools/search-time-machine-template.html;
  3. writes search-time-machine.html at the repository root.

Usage:
  python -X utf8 tools/build-search-time-machine.py            # build
  python -X utf8 tools/build-search-time-machine.py --check    # fail if stale
  python -X utf8 tools/build-search-time-machine.py --corpus-json OUT.json
  python -X utf8 tools/build-search-time-machine.py --fragment OUT.html
  python -X utf8 tools/build-search-time-machine.py --vectors PATH/wink-embeddings-sg-100d.json

Only --vectors needs numpy and the GloVe-derived vector file (see
tools/README.md). Every other mode uses the cached subset in
data/search-time-machine-vectors.json.
"""
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import math
import re
import sys
from collections import Counter, defaultdict
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "search-textbook.html"
TEMPLATE = ROOT / "tools" / "search-time-machine-template.html"
ENGINE = ROOT / "assets" / "search-time-machine-engine.js"
APP = ROOT / "assets" / "search-time-machine-app.js"
VECTORS = ROOT / "data" / "search-time-machine-vectors.json"
GLOSSARY_MAP = ROOT / "data" / "glossary-map.json"
OUTPUT = ROOT / "search-time-machine.html"
BOOK_URL = "https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html"

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
# Containers whose text is navigation, generated register links, quizzes or
# diagram internals rather than the book's running prose.
SKIP_CLASSES = {
    "claim-links", "stage-map", "self-check", "self-check-q", "chapter-nav", "heading-anchor",
    "legacy-anchor", "chapter-meta", "chapter-eyebrow", "glossary-entry-nav", "toc-subs",
    "mobile-toc", "footnotes", "footnote-ref", "footnote-back", "hub-sr-only", "asset-label",
    "asset-label-inline", "term-permalink", "copy-link", "claim-coverage", "as-of",
}
SKIP_TAGS = {"script", "style", "svg", "nav", "figure", "sup", "button", "template"}
INLINE_TAGS = {"a", "em", "strong", "span", "code", "i", "b", "sub", "abbr", "cite", "q", "mark", "small", "u", "kbd", "var", "s"}
# Back matter that is listing or administration, not teaching prose.
SKIP_CHAPTER_IDS = {"figures-and-tables", "where-to-go-deeper", "how-to-cite-and-reuse",
                    "generative-ai-use-disclosure", "references", "product-evidence-currency"}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


class Node:
    __slots__ = ("tag", "attrs", "children", "parent")

    def __init__(self, tag, attrs, parent):
        self.tag = tag
        self.attrs = dict(attrs)
        self.children = []
        self.parent = parent

    @property
    def classes(self):
        return set((self.attrs.get("class") or "").split())

    def text(self) -> str:
        out = []
        stack = [self]
        while stack:
            n = stack.pop()
            if isinstance(n, str):
                out.append(n)
                continue
            if n is not self and (n.tag in SKIP_TAGS or n.classes & SKIP_CLASSES):
                continue
            if n.tag not in INLINE_TAGS:
                # block boundaries and <br> separate words
                out.append(" ")
                stack.append(" ")
            stack.extend(reversed(n.children))
        return norm("".join(out))

    def find_all(self, pred):
        stack = [self]
        while stack:
            n = stack.pop()
            if isinstance(n, str):
                continue
            if pred(n):
                yield n
            stack.extend(reversed(n.children))


class TreeBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("root", [], None)
        self.cur = self.root

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.cur)
        self.cur.children.append(node)
        if tag not in VOID:
            self.cur = node

    def handle_startendtag(self, tag, attrs):
        self.cur.children.append(Node(tag, attrs, self.cur))

    def handle_endtag(self, tag):
        n = self.cur
        while n is not None and n.tag != tag:
            n = n.parent
        if n is not None and n.parent is not None:
            self.cur = n.parent

    def handle_data(self, data):
        self.cur.children.append(data)


def parse_book(html: str) -> Node:
    tb = TreeBuilder()
    tb.feed(html)
    return tb.root


def extract(html: str) -> dict:
    root = parse_book(html)
    version = ""
    m = re.search(r"[Vv]ersion\s+(\d+\.\d+(?:\.\d+)?)", html)
    if m:
        version = m.group(1)

    chapters, docs = [], []
    id_to_doc: dict[str, int] = {}

    def new_doc(chapter_index, anchor, title, parent_title, level):
        doc = {"id": anchor, "c": chapter_index, "t": title, "pt": parent_title, "lvl": level,
               "ch": [], "x": [], "_links": [], "_ids": [anchor] if anchor else []}
        docs.append(doc)
        return doc

    for sec in root.find_all(lambda n: n.tag == "section" and "chapter" in n.classes):
        h2 = next(sec.find_all(lambda n: n.tag == "h2"), None)
        if h2 is None or not h2.attrs.get("id"):
            continue
        cid = h2.attrs["id"]
        if cid in SKIP_CHAPTER_IDS:
            continue
        eyebrow = next(sec.find_all(lambda n: n.tag == "p" and "chapter-eyebrow" in n.classes), None)
        label = norm("".join(c for c in eyebrow.children if isinstance(c, str))) if eyebrow else ""
        ctitle = h2.text().rstrip("#").strip()
        ci = len(chapters)
        chapters.append({"id": cid, "n": label, "t": ctitle})
        state = {"doc": new_doc(ci, cid, ctitle, "", 2), "h3": ""}
        id_to_doc.setdefault(sec.attrs.get("id", ""), len(docs) - 1)

        def walk(node, state=state, ci=ci):
            for child in node.children:
                if isinstance(child, str):
                    continue
                tag, classes = child.tag, child.classes
                if tag in SKIP_TAGS and tag != "figure":
                    continue
                if classes & SKIP_CLASSES:
                    continue
                if child.attrs.get("id"):
                    state["doc"]["_ids"].append(child.attrs["id"])
                if tag == "h2":
                    continue
                if tag == "h3" and child.attrs.get("id"):
                    title = child.text().rstrip("#").strip()
                    state["h3"] = title
                    state["doc"] = new_doc(ci, child.attrs["id"], title, "", 3)
                    continue
                if tag == "h4" and child.attrs.get("id"):
                    title = child.text().rstrip("#").strip()
                    state["doc"] = new_doc(ci, child.attrs["id"], title, state["h3"], 4)
                    continue
                if tag in ("h4", "h5", "h6"):
                    t = child.text()
                    if t:
                        state["doc"]["x"].append(t)
                    continue
                if tag == "figure":
                    for cap in child.find_all(lambda n: n.tag == "figcaption"):
                        t = cap.text()
                        if t:
                            state["doc"]["x"].append(t)
                    for n in child.find_all(lambda n: bool(n.attrs.get("id"))):
                        state["doc"]["_ids"].append(n.attrs["id"])
                    continue
                if tag == "table":
                    t = child.text()
                    if t:
                        state["doc"]["x"].append(t)
                    for a in child.find_all(lambda n: n.tag == "a"):
                        href = a.attrs.get("href", "")
                        if href.startswith("#"):
                            state["doc"]["_links"].append(href[1:])
                    continue
                if tag in ("p", "blockquote") or (tag in ("ul", "ol", "dl")):
                    t = child.text()
                    if "chapter-question" in classes:
                        # drop the inline "Central question" label
                        t = re.sub(r"^Central question\s*", "", t)
                    for n in child.find_all(lambda n: bool(n.attrs.get("id"))):
                        state["doc"]["_ids"].append(n.attrs["id"])
                    for a in child.find_all(lambda n: n.tag == "a"):
                        href = a.attrs.get("href", "")
                        if href.startswith("#"):
                            state["doc"]["_links"].append(href[1:])
                    if t:
                        if tag in ("ul", "ol", "dl") and state["doc"]["ch"] and len(state["doc"]["ch"][-1]) < 400 \
                                and state["doc"]["ch"][-1].rstrip().endswith(":"):
                            state["doc"]["ch"][-1] += " " + t
                        else:
                            state["doc"]["ch"].append(t)
                    continue
                walk(child)

        walk(sec)

    # Drop documents with no usable prose, but keep their anchors resolvable.
    kept, remap = [], {}
    pending_ids = []
    for doc in docs:
        body = sum(len(c) for c in doc["ch"])
        if body < 120:
            pending_ids.append(doc)
            continue
        idx = len(kept)
        kept.append(doc)
        for p in pending_ids:
            if p["c"] == doc["c"]:
                for i in p["_ids"]:
                    remap.setdefault(i, idx)
                doc["x"] = p["x"] + p["ch"] + doc["x"]
        pending_ids = []
        for i in doc["_ids"]:
            remap.setdefault(i, idx)
    for i, doc in enumerate(kept):
        # chapter section ids ("sec-...") resolve to the chapter's first doc
        pass
    first_doc_of_chapter = {}
    for i, doc in enumerate(kept):
        first_doc_of_chapter.setdefault(doc["c"], i)
    for ci, ch in enumerate(chapters):
        if ci in first_doc_of_chapter:
            remap.setdefault(ch["id"], first_doc_of_chapter[ci])

    for i, doc in enumerate(kept):
        links = []
        for target in doc["_links"]:
            j = remap.get(target)
            if j is not None and j != i and j not in links:
                links.append(j)
        doc["ln"] = links
        del doc["_links"], doc["_ids"]
        doc["x"] = " ".join(doc["x"])[:6000]

    used = sorted({d["c"] for d in kept})
    cmap = {old: new for new, old in enumerate(used)}
    chapters = [chapters[i] for i in used]
    for d in kept:
        d["c"] = cmap[d["c"]]

    # Glossary: the book's 89 defined terms act as the 1960s thesaurus, the
    # 1980s subject headings and the 2010s knowledge panel.
    gmap = json.loads(GLOSSARY_MAP.read_text(encoding="utf-8"))
    defs = {}
    for span in root.find_all(lambda n: n.tag == "span" and "glossary-definition" in n.classes):
        sid = span.attrs.get("id", "")
        if sid.startswith("definition-"):
            defs[sid[len("definition-"):]] = span.text()
    glossary = []
    for term in gmap["terms"]:
        targets = [remap[t] for t in term.get("targets", []) if t in remap]
        glossary.append({
            "id": term["id"], "label": term["label"], "aliases": term.get("aliases", []),
            "def": defs.get(term["id"], ""), "targets": sorted(set(targets)),
            "related": term.get("related", []),
        })

    return {
        "book": {"title": "How Search Decides What You See", "version": version, "url": BOOK_URL},
        "chapters": chapters, "docs": kept, "glossary": glossary,
    }


# ---------------------------------------------------------------------------
# Word vectors (optional step; needs numpy and the GloVe-derived source file)
# ---------------------------------------------------------------------------

WORD_RE = re.compile(r"[a-z0-9]+")
UK_US = [("isation", "ization"), ("isations", "izations"), ("ising", "izing"), ("ised", "ized"),
         ("ises", "izes"), ("ise", "ize"), ("iser", "izer"), ("isers", "izers"), ("ours", "ors"),
         ("our", "or"), ("oured", "ored"), ("ouring", "oring"), ("ogue", "og"), ("ogues", "ogs"),
         ("tre", "ter"), ("tres", "ters"), ("lled", "led"), ("lling", "ling"), ("ller", "ler"),
         ("yse", "yze"), ("ysed", "yzed"), ("ysing", "yzing"), ("ence", "ense")]


def words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower().replace("’", "'").replace("'", ""))


def us_variants(word: str):
    for uk, us in UK_US:
        if word.endswith(uk):
            yield word[: -len(uk)] + us


def build_vectors(source: Path, corpus: dict, general: int = 14000, dims: int = 100) -> dict:
    import numpy as np

    print("loading", source, file=sys.stderr)
    raw = json.loads(source.read_text(encoding="utf-8"))
    order, table = raw["words"], raw["vectors"]
    d = raw["dimensions"]

    def glove(word):
        row = table.get(word)
        if row is None:
            for v in us_variants(word):
                row = table.get(v)
                if row is not None:
                    break
        return None if row is None else np.asarray(row[:d], dtype=np.float32)

    # Tokenised chunks of the book, for context-based adaptation.
    chunks = []
    for doc in corpus["docs"]:
        chunks.append(words(doc["t"]))
        for c in doc["ch"]:
            chunks.append(words(c))
        if doc["x"]:
            chunks.append(words(doc["x"]))
    for g in corpus["glossary"]:
        chunks.append(words(g["label"] + " " + " ".join(g["aliases"]) + " " + g["def"]))
    freq = Counter(w for c in chunks for w in c)
    df = Counter(w for c in chunks for w in set(c))
    n_chunks = len(chunks)

    vocab = {}
    for w in freq:
        v = glove(w)
        if v is not None:
            vocab[w] = v
    book_known = len(vocab)
    taken = 0
    for w in order:
        if taken >= general:
            break
        if not WORD_RE.fullmatch(w):
            continue
        taken += 1
        if w not in vocab:
            vocab[w] = np.asarray(table[w][:d], dtype=np.float32)

    # Context vectors: what surrounds each word *in this book*. Used to place
    # words GloVe never saw (bm25, reranker) and to pull words whose news-corpus
    # sense differs (recall, bert, transformer) towards the book's sense.
    idf = {w: math.log(1 + n_chunks / df[w]) for w in df}
    ctx_sum = defaultdict(lambda: np.zeros(d, dtype=np.float32))
    ctx_w = Counter()
    win = 6
    for c in chunks:
        vecs = [(vocab.get(w), idf.get(w, 1.0)) for w in c]
        for i, w in enumerate(c):
            lo, hi = max(0, i - win), min(len(c), i + win + 1)
            for j in range(lo, hi):
                if j == i or vecs[j][0] is None:
                    continue
                ctx_sum[w] += vecs[j][0] * vecs[j][1]
                ctx_w[w] += vecs[j][1]
    ctx = {w: ctx_sum[w] / ctx_w[w] for w in ctx_sum if ctx_w[w] > 0}
    if ctx:
        mat = np.stack(list(ctx.values()))
        mean = mat.mean(axis=0)
        mat = mat - mean
        # remove the dominant shared directions so contexts discriminate
        _, _, vt = np.linalg.svd(mat, full_matrices=False)
        top = vt[:2]
        mat = mat - mat @ top.T @ top
        gl = np.stack([v for v in vocab.values()])
        scale = float(np.median(np.linalg.norm(gl, axis=1)))
        mat = mat / (np.linalg.norm(mat, axis=1, keepdims=True) + 1e-9) * scale
        ctx = dict(zip(ctx.keys(), mat))

    induced = 0
    for w, f in freq.items():
        cv = ctx.get(w)
        if cv is None:
            continue
        if w not in vocab:
            if f >= 2 and len(w) > 1:
                vocab[w] = cv
                induced += 1
        elif f >= 4:
            alpha = min(0.5, 0.12 * math.log(f))  # more book evidence, more book sense
            vocab[w] = (1 - alpha) * vocab[w] + alpha * cv

    names = sorted(vocab)
    mat = np.stack([vocab[w] for w in names]).astype(np.float32)
    mat -= mat.mean(axis=0, keepdims=True)
    if dims < d:
        _, _, vt = np.linalg.svd(mat[: min(len(names), 20000)], full_matrices=False)
        mat = mat @ vt[:dims].T
    mat /= (np.linalg.norm(mat, axis=1, keepdims=True) + 1e-9)
    q = np.clip(np.round(mat * 127), -127, 127).astype(np.int8)
    return {
        "source": "GloVe 100d (Pennington, Socher & Manning 2014; PDDL) via npm wink-embeddings-sg-100d 1.1.0 (MIT)",
        "dims": int(q.shape[1]), "count": len(names), "book_known": book_known, "induced": induced,
        "general": general, "words": names,
        "data": base64.b64encode(q.tobytes()).decode("ascii"),
    }


# ---------------------------------------------------------------------------


def render(corpus: dict, fragment: bool = False) -> str:
    """Return the standalone page, or the body-only fragment an Artifact publish expects."""
    template = TEMPLATE.read_text(encoding="utf-8")
    engine = ENGINE.read_text(encoding="utf-8")
    app = APP.read_text(encoding="utf-8")
    vectors = json.loads(VECTORS.read_text(encoding="utf-8"))
    payload = json.dumps(corpus, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    meta = {k: v for k, v in vectors.items() if k not in ("data",)}
    out = template
    for key, value in (
        ("/*__ENGINE__*/", engine),
        ("/*__APP__*/", app),
        ("__CORPUS_JSON__", payload),
        ("__VECTOR_META_JSON__", json.dumps(meta, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")),
        ("__VECTOR_DATA__", vectors["data"]),
        ("__BOOK_VERSION__", corpus["book"]["version"]),
        ("__DOC_COUNT__", str(len(corpus["docs"]))),
        ("__TERM_COUNT__", str(len(corpus["glossary"]))),
    ):
        if key not in out:
            raise SystemExit(f"template is missing placeholder {key}")
        out = out.replace(key, value)
    if "<!--BODY-->" not in out:
        raise SystemExit("template is missing the <!--BODY--> marker")
    head, body = out.split("<!--BODY-->", 1)
    if fragment:
        return head + body
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            + head + "</head>\n<body>\n" + body + "</body>\n</html>\n")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if search-time-machine.html is stale")
    ap.add_argument("--corpus-json", metavar="OUT", help="write the extracted corpus as JSON and stop")
    ap.add_argument("--vectors", metavar="SOURCE", help="rebuild the cached word-vector subset from SOURCE")
    ap.add_argument("--fragment", metavar="OUT", help="also write the body-only fragment used for Artifact publishing")
    ap.add_argument("--dims", type=int, default=100)
    ap.add_argument("--general", type=int, default=14000)
    args = ap.parse_args()

    corpus = extract(BOOK.read_text(encoding="utf-8"))
    if args.corpus_json:
        Path(args.corpus_json).write_text(json.dumps(corpus, ensure_ascii=False), encoding="utf-8")
        chunks = sum(len(d["ch"]) for d in corpus["docs"])
        print(f"{len(corpus['docs'])} sections, {chunks} passages, {len(corpus['glossary'])} glossary terms")
        return 0
    if args.vectors:
        vectors = build_vectors(Path(args.vectors), corpus, general=args.general, dims=args.dims)
        VECTORS.write_text(json.dumps(vectors, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
        print(f"wrote {VECTORS.relative_to(ROOT)}: {vectors['count']} words x {vectors['dims']} dims "
              f"({vectors['book_known']} book words known to GloVe, {vectors['induced']} induced from context)")
        return 0

    html = render(corpus)
    if args.fragment:
        Path(args.fragment).write_text(render(corpus, fragment=True), encoding="utf-8")
    if args.check:
        current = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        if hashlib.sha256(current.encode()).digest() != hashlib.sha256(html.encode()).digest():
            print("search-time-machine.html is stale: run tools/build-search-time-machine.py", file=sys.stderr)
            return 1
        print("search-time-machine.html is current")
        return 0
    OUTPUT.write_text(html, encoding="utf-8")
    chunks = sum(len(d["ch"]) for d in corpus["docs"])
    print(f"wrote {OUTPUT.name}: {len(html) / 1e6:.2f} MB, {len(corpus['docs'])} sections, {chunks} passages")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
