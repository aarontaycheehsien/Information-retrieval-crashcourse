# -*- coding: utf-8 -*-
"""Build the chaptered textbook edition from the single-flow source article.

Re-runnable: edit the source, re-run, get an updated textbook edition.
Structural transform only -- the source prose is copied verbatim. All NEW prose
lives in book_data.py and is emitted with class="drafted".
"""
import io, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from book_data import STAGES, PARTS, CHAPTERS, EXERCISES, TABLE_CAPTIONS

REPO = r"C:\Users\aarontay\Downloads\Codex\informationretrievalcrashcourse"
SRC = os.path.join(REPO, "how-search-decides-what-you-see.html")
OUT = os.path.join(REPO, "search-textbook.html")

src = io.open(SRC, encoding="utf-8").read()

# ---------------------------------------------------------------- slice source
head = src[:src.index("</head>")]
body_start = src.index('<article id="article">') + len('<article id="article">')
foot_start = src.index('<section class="footnotes">')
article = src[body_start:foot_start]
footnotes = src[foot_start:src.index("</section></article>") + len("</section></article>")]

# ------------------------------------------------------------- split into blocks
HEAD_RE = re.compile(
    r'(?:<span id="(?P<legacy>[^"]*)" class="legacy-anchor"></span>)?'
    r'<h(?P<lvl>[23]) id="(?P<id>[^"]*)"[^>]*>(?P<inner>.*?)</h(?P=lvl)>',
    re.S)

marks = list(HEAD_RE.finditer(article))
preamble = article[:marks[0].start()]

blocks = []
for i, m in enumerate(marks):
    end = marks[i + 1].start() if i + 1 < len(marks) else len(article)
    inner = m.group("inner")
    inner = re.sub(r'<a aria-label[^>]*class="heading-anchor"[^>]*>#</a>\s*$', '', inner)
    title = re.sub(r'^<span>(.*)</span>$', r'\1', inner.strip(), flags=re.S).strip()
    blocks.append(dict(lvl=int(m.group("lvl")), id=m.group("id"), legacy=m.group("legacy"),
                       title=title, body=article[m.end():end]))

# ------------------------------------------------------------------ chapter map
# action: ("section", chapter)  -> H2 demoted to H3, its H3 children -> H4
#         ("title",   chapter)  -> H2 becomes the chapter title, H3 children stay H3
MAP = [
    ("retrieval-not-generation",                                   "section", "intro"),
    ("two-familiar-search-results-and-two-puzzles",                "section", "intro"),
    ("strict-boolean-search-words-as-admission-rules",             "section", "ch1"),
    ("how-boolean-search-uses-an-inverted-index",                  "section", "ch1"),
    ("bm25-words-as-weighted-clues",                               "section", "ch2"),
    ("how-bm25-uses-the-same-inverted-index",                      "section", "ch2"),
    ("lexical-search-does-not-have-to-mean-boolean-search",        "section", "ch3"),
    ("one-category-error-resolved-and-one-still-ahead",            "section", "ch3"),
    ("from-word2vec-to-retrieval-embeddings",                      "section", "ch4"),
    ("single-vector-dense-retrieval-compress-first-compare-later", "section", "ch4"),
    ("a-vector-does-not-have-to-be-dense-or-semantic",             "section", "ch4"),
    ("what-a-dense-bi-encoder-actually-learns",                    "section", "ch4"),
    ("one-document-one-chunk-and-one-vector-are-not-the-same-thing","section", "ch4"),
    ("for-awareness-two-neural-variants",                          "section", "ch4"),
    ("rerankers-compare-more-carefully-after-retrieval",           "section", "ch5"),
    ("why-hybrid-retrieval-remains-attractive",                    "section", "ch5"),
    ("beyond-one-query-expansion-decomposition-and-routing",       "title",   "ch6"),
    ("agentic-search-who-chooses-the-next-retrieval-action",       "title",   "ch7"),
    ("diagnosing-where-retrieval-goes-wrong",                      "title",   "ch8"),
    ("implications-for-library-practice",                          "title",   "ch9"),
]
ACTION = {hid: (act, ch) for hid, act, ch in MAP}
ORDER = ["intro", "ch1", "ch2", "ch3", "ch4", "ch5", "ch6", "ch7", "ch8", "ch9"]

# Section-group dividers inside the oversized Chapter 4.
GROUPS = {
    "from-word2vec-to-retrieval-embeddings":
        ("The basic dense-retrieval model",
         "How text becomes a vector, how similar vectors are found at scale, and where the "
         "result list is cut off."),
    "a-vector-does-not-have-to-be-dense-or-semantic":
        ("Four qualifications the basic model needs",
         "Each of these corrects something the account above leaves misleading. None is an "
         "optional extra."),
}

BACKMATTER = ["appendix-character-and-byte-tokenisation",
              "appendix-advanced-inverted-index-execution",
              "generative-ai-use-disclosure", "references"]

# --------------------------------------------------------- distribute the blocks
chapters = {k: [] for k in ORDER}
back = []
cur = None
for b in blocks:
    if b["lvl"] == 2:
        if b["id"] in ACTION:
            act, ch = ACTION[b["id"]]
            cur = (ch, act)
            chapters[ch].append(dict(b, role=act))
            continue
        if b["id"] in BACKMATTER:
            cur = None
            back.append(dict(b, role="back"))
            continue
        raise SystemExit("Unmapped H2: " + b["id"])
    # H3
    if cur is None:
        back.append(dict(b, role="back"))
    else:
        ch, act = cur
        chapters[ch].append(dict(b, role="sub" if act == "section" else "section"))

# ------------------------------------------------------------------- numbering
def label_for(ch):
    if ch == "intro":
        return "0"
    return ch[2:]

fig_n, tab_n = {}, {}
TABLE_WRAP_RE = re.compile(r'<div class="table-wrap"><table>')
FIGCAP_RE = re.compile(r'<figcaption(?P<attrs>[^>]*)>')

tbl_seen = [0]
def number_assets(html, chnum):
    """Prefix numbered labels onto tables and figures within one chapter."""
    fig_n.setdefault(chnum, 0)
    def do_table(m):
        tbl_seen[0] += 1
        fig_n[chnum] = fig_n[chnum]
        tab_n[chnum] = tab_n.get(chnum, 0) + 1
        cap = TABLE_CAPTIONS.get(tbl_seen[0], "")
        lbl = u'<p class="asset-label drafted">Table {}.{}{}</p>'.format(
            chnum, tab_n[chnum], (u' \u2014 ' + cap) if cap else '')
        return lbl + m.group(0)
    html = TABLE_WRAP_RE.sub(do_table, html)
    def do_fig(m):
        fig_n[chnum] += 1
        return u'<figcaption{}><span class="asset-label-inline drafted">Figure {}.{}</span> '.format(
            m.group("attrs"), chnum, fig_n[chnum])
    html = FIGCAP_RE.sub(do_fig, html)
    return html

# ------------------------------------------------------------ component builders
CONTAINER_RE = re.compile(r'<(figure|aside|details)\b.*?</\1>', re.S)
H4_RE = re.compile(r'<h4\b([^>]*)>(.*?)</h4>', re.S)

def demote_inflow_h4(html):
    """Old H3s became H4s, so any H4 in their prose must drop to H5.

    Figure/callout titles are styled by their container and keep their level."""
    masked = [(m.start(), m.end()) for m in CONTAINER_RE.finditer(html)]
    def inside(pos):
        return any(a <= pos < b for a, b in masked)
    parts, last = [], 0
    for m in H4_RE.finditer(html):
        if inside(m.start()):
            continue
        parts.append(html[last:m.start()])
        parts.append(u'<h5{}>{}</h5>'.format(m.group(1), m.group(2)))
        last = m.end()
    parts.append(html[last:])
    return u''.join(parts)

def stage_map(meta):
    on = set(meta.get("stages") or [])
    ctl = meta.get("controller")
    cells = u''.join(
        u'<span class="stage {}">{}</span>'.format("on" if k in on else "off", lab)
        for k, lab in STAGES)
    ctlbar = (u'<div class="stage-controller {}">Controller &mdash; chooses and sequences the '
              u'stages below</div>'.format("on" if ctl else "off"))
    return (u'<div class="stage-map drafted" role="img" aria-label="Pipeline map: the stage '
            u'this chapter covers is highlighted">{}<div class="stage-row">{}</div></div>'
            ).format(ctlbar, cells)

def chapter_head(key, meta):
    q = (u'<p class="chapter-question drafted"><span>Central question</span>{}</p>'
         .format(meta["question"]))
    orient = u''.join(u'<p>{}</p>'.format(p) for p in meta["orient"])
    return (u'<header class="chapter-head">'
            u'<p class="chapter-eyebrow">{eye}</p>'
            u'<h2 id="{cid}">{title}</h2>'
            u'{q}{smap}'
            u'<div class="chapter-orient drafted">{orient}</div>'
            u'</header>').format(eye=meta["eyebrow"], cid=key, title=meta["title"],
                                 q=q, smap=stage_map(meta), orient=orient)

def chapter_close(key, meta, nxt):
    props = u''.join(u'<li>{}</li>'.format(p) for p in meta["established"])
    trans = (u'<p class="chapter-transition">{}</p>'.format(meta["transition"])
             if meta.get("transition") else u'')
    return (u'<aside class="chapter-close drafted" aria-label="Chapter summary">'
            u'<p class="chapter-close-label">What this chapter established</p>'
            u'<ol>{}</ol>{}</aside>').format(props, trans)

def part_divider(pnum):
    tag, title, blurb = PARTS[pnum]
    return (u'<section class="part-divider" id="part{n}">'
            u'<p class="part-tag">{tag}</p><h2 class="part-title">{title}</h2>'
            u'<p class="part-blurb drafted">{blurb}</p></section>').format(
        n=pnum, tag=tag, title=title, blurb=blurb)

def exercise(pnum):
    e = EXERCISES[pnum]
    steps = u''.join(u'<li>{}</li>'.format(s) for s in e["steps"])
    return (u'<section class="exercise drafted" id="exercise{n}">'
            u'<p class="exercise-label">End of {tag}</p><h2>{title}</h2>'
            u'<p>{lead}</p><ol>{steps}</ol>'
            u'<p class="exercise-deliverable"><strong>Deliverable.</strong> {deliv}</p>'
            u'</section>').format(n=pnum, tag=PARTS[pnum][0], title=e["title"],
                                  lead=e["lead"], steps=steps, deliv=e["deliverable"])

def cap(s):
    return s[:1].upper() + s[1:] if s else s

def anchor(hid, title):
    return (u'<a aria-label="Link to {t}" class="heading-anchor" href="#{i}">#</a>'
            .format(t=re.sub(r'<[^>]+>', '', title), i=hid))

def legacy(b):
    return (u'<span id="{}" class="legacy-anchor"></span>'.format(b["legacy"])
            if b.get("legacy") else u'')

# --------------------------------------------------------------- emit chapters
def nav(prev, nxt):
    L = (u'<a class="cnav prev" href="#{}"><span>Previous</span>{}</a>'.format(prev[0], prev[1])
         if prev else u'<span class="cnav ghost"></span>')
    R = (u'<a class="cnav next" href="#{}"><span>Next</span>{}</a>'.format(nxt[0], nxt[1])
         if nxt else u'<span class="cnav ghost"></span>')
    return u'<nav class="chapter-nav" aria-label="Chapter navigation">{}{}</nav>'.format(L, R)

titles = [(k, CHAPTERS[k]["title"]) for k in ORDER]
out = [preamble]
emitted_parts = set()

for idx, key in enumerate(ORDER):
    meta = CHAPTERS[key]
    pnum = meta.get("part")
    if pnum and pnum not in emitted_parts:
        out.append(part_divider(pnum))
        emitted_parts.add(pnum)

    chnum = label_for(key)
    out.append(u'<section class="chapter" id="sec-{}">'.format(key))
    out.append(chapter_head(key, meta))

    for b in chapters[key]:
        if b["id"] in GROUPS:
            g, gb = GROUPS[b["id"]]
            out.append(u'<div class="section-group drafted"><h3 class="group-title">{}</h3>'
                       u'<p>{}</p></div>'.format(g, gb))
        lvl = {"title": None, "section": 3, "sub": 4}[b["role"]]
        body = number_assets(b["body"], chnum)
        if b["role"] == "sub":
            body = demote_inflow_h4(body)
        if b["role"] == "title":
            # the chapter head already carries the title; keep the old id reachable
            out.append(u'<span id="{}" class="legacy-anchor"></span>{}'.format(b["id"], legacy(b)))
            out.append(body)
        else:
            out.append(u'{lg}<h{l} id="{i}">{t}{a}</h{l}>{b}'.format(
                lg=legacy(b), l=lvl, i=b["id"], t=b["title"],
                a=anchor(b["id"], b["title"]), b=body))

    prev = (ORDER[idx - 1], CHAPTERS[ORDER[idx - 1]]["title"]) if idx else None
    nxt = (ORDER[idx + 1], CHAPTERS[ORDER[idx + 1]]["title"]) if idx + 1 < len(ORDER) else None
    out.append(chapter_close(key, meta, nxt))
    out.append(nav(prev, nxt))
    out.append(u'</section>')

    # exercise closes each part
    nxt_part = CHAPTERS[ORDER[idx + 1]].get("part") if idx + 1 < len(ORDER) else None
    if pnum and nxt_part != pnum:
        out.append(exercise(pnum))

# ------------------------------------------------------------- emit back matter
out.append(u'<section class="part-divider backmatter-divider" id="backmatter">'
           u'<p class="part-tag">End matter</p><h2 class="part-title">Appendices and references</h2></section>')
# group back-matter H3s under the H2 that precedes them, so sections stay nested
back_groups, cur_app = [], None
for b in back:
    if b["lvl"] == 2:
        back_groups.append([b])
    else:
        back_groups[-1].append(b)

app_letter = iter("AB")
for grp in back_groups:
    top, subs = grp[0], grp[1:]
    is_app = top["id"].startswith("appendix")
    key = next(app_letter) if is_app else None
    if key:
        cur_app = key
    num = cur_app if is_app else "—"
    body = number_assets(top["body"], num) if is_app else top["body"]
    inner = [body]
    for s in subs:
        inner.append(u'{lg}<h3 id="{i}">{t}{a}</h3>{b}'.format(
            lg=legacy(s), i=s["id"], t=s["title"], a=anchor(s["id"], s["title"]),
            b=number_assets(s["body"], num) if is_app else s["body"]))
    if is_app:
        out.append(u'<section class="chapter appendix" id="app-{k}">'
                   u'<header class="chapter-head"><p class="chapter-eyebrow">Appendix {k}</p>'
                   u'<h2 id="{i}">{t}</h2></header>{b}</section>'.format(
                       k=key, i=top["id"],
                       t=cap(re.sub(r'^Appendix:\s*', '', top["title"])), b=u''.join(inner)))
    else:
        out.append(u'<section class="chapter backsection">'
                   u'<h2 id="{i}">{t}{a}</h2>{b}</section>'.format(
                       i=top["id"], t=top["title"], a=anchor(top["id"], top["title"]),
                       b=u''.join(inner)))

article_html = u''.join(out)

# --------------------------------------------------------------- table of contents
def toc_html():
    rows = []
    for pnum in (None, 1, 2, 3):
        if pnum:
            rows.append(u'<li class="toc-part"><a href="#part{n}">{tag} \u00b7 {t}</a></li>'
                        .format(n=pnum, tag=PARTS[pnum][0], t=PARTS[pnum][1]))
        for key in ORDER:
            if CHAPTERS[key].get("part") != pnum:
                continue
            meta = CHAPTERS[key]
            subs = [b for b in chapters[key] if b["role"] in ("section",)]
            sub_html = u''.join(
                u'<li class="toc-sec"><a href="#{i}">{t}</a></li>'.format(
                    i=b["id"], t=re.sub(r'<[^>]+>', '', b["title"]))
                for b in subs)
            rows.append(
                u'<li class="toc-ch" data-ch="{k}"><a href="#{k}"><em>{eye}</em>{t}</a>'
                u'<ol class="toc-subs">{s}</ol></li>'.format(
                    k=key, eye=meta["eyebrow"], t=meta["title"], s=sub_html))
        if pnum:
            rows.append(u'<li class="toc-ex"><a href="#exercise{n}">Application exercise {r}</a></li>'
                        .format(n=pnum, r="I" * pnum))
    rows.append(u'<li class="toc-part"><a href="#backmatter">End matter</a></li>')
    letters = iter("AB")
    for b in back:
        if b["lvl"] != 2:
            continue
        if b["id"].startswith("appendix"):
            t = u'<em>Appendix {}</em>{}'.format(
                next(letters), cap(re.sub(r'^Appendix:\s*', '', b["title"])))
        else:
            t = b["title"]
        rows.append(u'<li class="toc-ch"><a href="#{i}">{t}</a></li>'.format(i=b["id"], t=t))
    return u''.join(rows)

TOC = toc_html()

# ------------------------------------------------------------------- extra CSS
EXTRA_CSS = u"""
    /* ============ textbook edition ============ */
    .part-divider {
      margin: 5rem 0 3rem; padding: 2.4rem 2rem; border-radius: 16px;
      background: linear-gradient(135deg, var(--teal), var(--accent-dark)); color: #fff;
    }
    .part-divider .part-tag {
      margin: 0 0 .5rem; font: 800 .74rem/1 var(--sans);
      letter-spacing: .16em; text-transform: uppercase; opacity: .85;
    }
    .part-divider .part-title {
      margin: 0; padding: 0; border: 0; color: #fff;
      font: 800 1.9rem/1.2 var(--sans);
    }
    /* the shared h2 accent bar is a red rule; it has no place on a coloured
       band, and between an eyebrow and its title it reads as a separator */
    .part-divider .part-title::before,
    .chapter-head h2::before,
    .exercise h2::before { display: none; }
    .part-divider .part-blurb { margin: .9rem 0 0; max-width: 46rem; opacity: .93; font-size: .98rem; }
    .backmatter-divider { background: linear-gradient(135deg, #5b6b68, #3f4b49); }

    .chapter { scroll-margin-top: 1.5rem; }
    .chapter + .chapter { margin-top: 4.5rem; }
    .chapter-head { margin: 3rem 0 2rem; }
    .chapter-eyebrow {
      margin: 0 0 .4rem; color: var(--accent-dark);
      font: 800 .76rem/1 var(--sans); letter-spacing: .16em; text-transform: uppercase;
    }
    .chapter-head h2 { margin-top: 0; }
    .chapter-question {
      margin: 1.2rem 0; padding: .9rem 1.15rem; border-left: 5px solid var(--accent);
      background: var(--paper-2); border-radius: 0 10px 10px 0;
      font: 700 1.06rem/1.45 var(--sans); color: var(--ink);
    }
    .chapter-question span {
      display: block; margin-bottom: .3rem; color: var(--accent-dark);
      font: 800 .68rem/1 var(--sans); letter-spacing: .14em; text-transform: uppercase;
    }
    .chapter-orient p:first-child { font-size: 1.06rem; }

    .stage-map { margin: 1.6rem 0; font-family: var(--sans); }
    .stage-controller {
      padding: .45rem .7rem; margin-bottom: .35rem; border-radius: 8px;
      font: 700 .72rem/1.3 var(--sans); text-align: center;
    }
    .stage-controller.on { background: var(--accent); color: #fff; }
    .stage-controller.off { background: #ece7dd; color: #9a9186; }
    .stage-row { display: grid; grid-template-columns: repeat(6, 1fr); gap: .3rem; }
    .stage {
      padding: .55rem .35rem; border-radius: 8px; text-align: center;
      font: 700 .68rem/1.25 var(--sans); border: 1px solid var(--line);
    }
    .stage.on { background: var(--teal); color: #fff; border-color: var(--teal); }
    .stage.off { background: #f4efe6; color: #a49a8d; }
    @media (max-width: 620px) {
      .stage-row { grid-template-columns: repeat(3, 1fr); }
    }

    /* fourth-level prose heading, created by demoting old in-flow h4s */
    .chapter h5 {
      margin: 1.8rem 0 .6rem; color: var(--ink);
      font: 800 .98rem/1.35 var(--sans); scroll-margin-top: 1.5rem;
    }

    .section-group { margin: 3rem 0 1.5rem; padding-top: 1.2rem; border-top: 2px solid var(--accent); }
    .section-group .group-title {
      margin: 0 0 .3rem; color: var(--accent-dark); font: 800 1.15rem/1.3 var(--sans);
    }
    .section-group p { margin: 0; font-size: .93rem; color: #5c554b; }

    .chapter-close {
      margin: 2.6rem 0 1.2rem; padding: 1.3rem 1.5rem;
      border: 1px solid var(--teal); border-radius: 12px; background: var(--paper-2);
    }
    .chapter-close-label {
      margin: 0 0 .7rem; color: var(--teal);
      font: 800 .72rem/1 var(--sans); letter-spacing: .14em; text-transform: uppercase;
    }
    .chapter-close ol { margin: 0; }
    .chapter-close li { font-size: .96rem; }
    .chapter-transition {
      margin: 1.1rem 0 0; padding-top: 1rem; border-top: 1px dashed var(--line);
      font-style: italic; color: #5c554b;
    }

    .exercise {
      margin: 3rem 0 4rem; padding: 1.6rem 1.8rem;
      border: 2px dashed var(--accent); border-radius: 14px; background: #fbf7f0;
    }
    .exercise-label {
      margin: 0 0 .4rem; color: var(--accent-dark);
      font: 800 .72rem/1 var(--sans); letter-spacing: .14em; text-transform: uppercase;
    }
    .exercise h2 { margin: 0 0 .8rem; padding: 0; border: 0; font-size: 1.3rem; }
    .exercise-deliverable {
      margin-top: 1.1rem; padding: .85rem 1.1rem; background: #fff;
      border-left: 4px solid var(--teal); border-radius: 0 8px 8px 0; font-size: .95rem;
    }

    .asset-label {
      margin: 2rem 0 -1.4rem; color: var(--accent-dark);
      font: 700 .78rem/1.4 var(--sans);
    }
    .asset-label-inline {
      font: 800 .74rem/1 var(--sans); color: var(--accent-dark);
      letter-spacing: .06em; text-transform: uppercase;
    }

    .chapter-nav {
      display: flex; gap: 1rem; justify-content: space-between;
      margin: 2rem 0 0; padding-top: 1.4rem; border-top: 1px solid var(--line);
    }
    .cnav {
      flex: 1; max-width: 48%; padding: .8rem 1rem; border: 1px solid var(--line);
      border-radius: 10px; text-decoration: none; color: var(--ink);
      font: 700 .92rem/1.35 var(--sans); background: var(--paper-2);
    }
    .cnav:hover { border-color: var(--accent); }
    .cnav span {
      display: block; color: var(--accent-dark);
      font: 800 .66rem/1 var(--sans); letter-spacing: .12em; text-transform: uppercase;
      margin-bottom: .3rem;
    }
    .cnav.next { text-align: right; }
    .cnav.ghost { border: 0; background: none; }

    /* three-level contents */
    .toc-part a {
      color: var(--teal) !important; font-weight: 800; text-transform: uppercase;
      letter-spacing: .08em; font-size: .68rem; padding-top: 1rem;
    }
    .toc-ch > a { font-weight: 700; }
    .toc-ch > a em {
      display: block; font-style: normal; color: var(--accent-dark);
      font-size: .64rem; letter-spacing: .1em; text-transform: uppercase;
    }
    .toc-ex a { font-style: italic; font-size: .74rem; }
    .toc-subs { list-style: none; padding: 0; margin: 0; border: 0; display: none; }
    .toc-ch.open .toc-subs { display: block; }
    .toc-sec a { padding-left: 1.8rem; font-size: .73rem; opacity: .85; }

    /* review mode: reveal every drafted passage */
    .review-toggle {
      position: fixed; right: 1rem; bottom: 1rem; z-index: 50;
      padding: .5rem .85rem; border: 1px solid var(--line); border-radius: 999px;
      background: #fff; color: var(--ink); cursor: pointer;
      font: 700 .74rem/1 var(--sans); box-shadow: 0 4px 14px rgba(40,35,28,.14);
    }
    body.review .drafted {
      outline: 2px dashed #c2410c; outline-offset: 4px;
      background: rgba(255, 237, 213, .5);
    }
    body.review .drafted::before {
      content: "DRAFT"; display: block; margin-bottom: .3rem;
      color: #c2410c; font: 800 .6rem/1 var(--sans); letter-spacing: .12em;
    }
    @media print {
      .part-divider { background: none !important; color: var(--ink) !important;
                      border: 2px solid var(--ink); }
      .part-divider .part-title { color: var(--ink) !important; }
      .chapter-nav, .review-toggle { display: none !important; }
      .chapter { break-before: page; }
      .part-divider, .exercise, .chapter-close, .chapter-head { break-inside: avoid; }
    }
"""

head = head.replace("</style>", EXTRA_CSS + "</style>", 1)
head = head.replace("<title>How Search Decides What You See</title>",
                    "<title>How Search Decides What You See \u2014 Textbook Edition</title>", 1)

# ------------------------------------------------------------------ assemble page
page = u"""{head}</head>
<body>
  <div class="progress" aria-hidden="true"></div>
  <header class="hero"><div class="hero-inner"><p class="kicker">Textbook edition \u00b7 Three parts, nine chapters</p>
      <h1>How Search Decides What You See</h1>
      <p class="subtitle">A librarian\u2019s guide to Boolean search, BM25, embeddings, reranking, and the retrieval pipelines behind hybrid and agentic search</p>
      <div class="tags" aria-label="Topics"><span>Boolean search</span><span>BM25</span><span>Dense retrieval</span><span>Reranking</span><span>Hybrid search</span><span>Agentic search</span><span>Retrieval vs generation</span></div>
    </div>
  </header>

  <div class="layout">
    <nav class="toc" aria-label="Table of contents">
      <strong>Contents</strong>
      <ol id="toc-list">{toc}</ol>
    </nav>
    <main>
      <details class="mobile-toc">
        <summary>Contents</summary>
        <ol id="mobile-toc-list">{toc}</ol>
      </details>
      <article id="article">{article}{footnotes}
    </main>
  </div>

  <button class="review-toggle" type="button" id="review-toggle">Review mode</button>
  <footer class="page-footer">Textbook edition \u00b7 generated from the single-flow web article. \u00b7 <a href="#generative-ai-use-disclosure">Generative AI use disclosure</a>.</footer>

  <script>
    const progress = document.querySelector('.progress');
    const updateProgress = () => {{
      const max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (max > 0 ? (window.scrollY / max) * 100 : 0) + '%';
    }};
    updateProgress();
    addEventListener('scroll', updateProgress, {{ passive: true }});
    addEventListener('resize', updateProgress);

    // Highlight the active chapter and reveal only its sections.
    const desktopToc = document.getElementById('toc-list');
    const chapterEls = [...document.querySelectorAll('.chapter[id^="sec-"]')];
    const setActive = (key) => {{
      desktopToc.querySelectorAll('.toc-ch').forEach(li => {{
        const on = li.dataset.ch === key;
        li.classList.toggle('open', on);
        const a = li.querySelector('a');
        if (a) a.classList.toggle('active', on);
      }});
    }};
    const chObs = new IntersectionObserver((entries) => {{
      entries.forEach(e => {{ if (e.isIntersecting) setActive(e.target.id.replace('sec-', '')); }});
    }}, {{ rootMargin: '-10% 0px -70% 0px', threshold: 0 }});
    chapterEls.forEach(c => chObs.observe(c));

    // Section-level highlight inside the open chapter.
    const secLinks = [...desktopToc.querySelectorAll('.toc-sec a')];
    const secObs = new IntersectionObserver((entries) => {{
      entries.forEach(e => {{
        if (e.isIntersecting) secLinks.forEach(a =>
          a.classList.toggle('active', a.getAttribute('href') === '#' + e.target.id));
      }});
    }}, {{ rootMargin: '-12% 0px -76% 0px', threshold: 0 }});
    document.querySelectorAll('#article h3[id]').forEach(h => secObs.observe(h));

    const rt = document.getElementById('review-toggle');
    rt.addEventListener('click', () => {{
      const on = document.body.classList.toggle('review');
      rt.textContent = on ? 'Review mode: on' : 'Review mode';
    }});
    if (location.hash === '#review') rt.click();
  </script>
</body></html>
""".format(head=head, toc=TOC, article=article_html, footnotes=footnotes)

io.open(OUT, "w", encoding="utf-8").write(page)

print("wrote", OUT)
print("chapters:", {k: len(v) for k, v in chapters.items()})
print("back-matter blocks:", len(back))
print("tables numbered:", tbl_seen[0])
print("figures per chapter:", fig_n)
