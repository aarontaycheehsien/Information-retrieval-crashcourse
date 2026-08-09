# -*- coding: utf-8 -*-
"""Maintain search-textbook.html in place. The HTML is the source of truth.

Edit the book directly, then run this. It rewrites only the machine-owned parts
and never touches prose:

  * table and figure numbers, derived from each chapter's own eyebrow label
  * appendix letters, derived from the order the appendices appear in
  * both tables of contents, rebuilt from the actual headings

Then it reports anything it cannot fix: unlabelled assets, captions with no
text, broken internal links, duplicate ids.

Idempotent -- running it twice makes no second change. Run it after any edit
that adds, moves or removes a table, figure, heading, chapter or appendix.
Footnotes are handled separately by renumber_footnotes.py.
"""
import io, os, re, string, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(REPO, "search-textbook.html")

original = io.open(BOOK, encoding="utf-8").read()
doc = original

ART_START = doc.index('<article id="article">')
ART_END = doc.index('<section class="footnotes">')

# --------------------------------------------------------- top-level sections
def top_level_sections(html, lo, hi):
    """Yield (start, end, open_tag) for each non-nested <section> in [lo, hi)."""
    out, depth, start, tag = [], 0, None, None
    for m in re.finditer(r'<section\b([^>]*)>|</section>', html[lo:hi]):
        if m.group(0).startswith('</'):
            depth -= 1
            if depth == 0:
                out.append((start, lo + m.end(), tag))
        else:
            if depth == 0:
                start, tag = lo + m.start(), m.group(1)
            depth += 1
    return out

def attr(tag, name):
    m = re.search(r'%s="([^"]*)"' % name, tag)
    return m.group(1) if m else ''

def text_of(html):
    return re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', '', html)).strip()

sections = top_level_sections(doc, ART_START, ART_END)

# ------------------------------------------------- classify and label sections
EYEBROW_RE = re.compile(r'<p class="chapter-eyebrow">(.*?)</p>', re.S)
H2_RE = re.compile(r'<h2[^>]*\bid="([^"]+)"[^>]*>(.*?)</h2>', re.S)

def heading_text(raw):
    raw = re.sub(r'<a aria-label[^>]*class="heading-anchor"[^>]*>#</a>\s*$', '', raw)
    return text_of(raw)

items, app_letters = [], iter(string.ascii_uppercase)
problems = []

for start, end, tag in sections:
    cls = attr(tag, 'class')
    sid = attr(tag, 'id')
    html = doc[start:end]
    h2 = H2_RE.search(html)
    kind = ('part' if 'part-divider' in cls else
            'exercise' if 'exercise' in cls else
            'appendix' if 'appendix' in cls else
            'backsection' if 'backsection' in cls else
            'chapter' if 'chapter' in cls else 'other')

    label = None            # prefix used for Table/Figure numbers
    if kind == 'appendix':
        label = next(app_letters)
    elif kind == 'chapter':
        eye = EYEBROW_RE.search(html)
        eye_txt = text_of(eye.group(1)) if eye else ''
        if eye_txt.lower().startswith('introduction'):
            label = '0'
        else:
            m = re.match(r'Chapter\s+(\d+)', eye_txt)
            if m:
                label = m.group(1)
            else:
                problems.append('chapter %s has an unrecognised eyebrow: %r'
                                % (sid or '?', eye_txt))
                label = '?'

    items.append(dict(start=start, end=end, cls=cls, sid=sid, kind=kind,
                      label=label,
                      h2id=h2.group(1) if h2 else None,
                      title=heading_text(h2.group(2)) if h2 else ''))

# ------------------------------------------------------ renumber assets in place
# The optional id is one this script wrote on an earlier run: it is rewritten
# from the number being assigned now, which keeps the pass idempotent.
TABLE_LBL_RE = re.compile(
    r'<p class="(asset-label[^"]*)"(?:\s+id="[^"]*")?>Table\s+[0-9A-Za-z]+\.\d+')
FIG_LBL_RE = re.compile(
    r'<span class="(asset-label-inline[^"]*)"(?:\s+id="[^"]*")?>Figure\s+[0-9A-Za-z]+\.\d+')
TABLE_RE = re.compile(r'<div class="table-wrap"><table>')
FIGCAP_RE = re.compile(r'<figcaption')
EYEBROW_SUB = re.compile(r'(<p class="chapter-eyebrow">)Appendix\s+[A-Z](</p>)')

renumbered = []
for it in items:
    if it['label'] is None:
        continue
    html = doc[it['start']:it['end']]

    if it['kind'] == 'appendix':
        html = EYEBROW_SUB.sub(r'\g<1>Appendix %s\g<2>' % it['label'], html)

    def anchor(prefix, num):
        return u'%s-%s-%d' % (prefix, it['label'].lower(), num)

    n = [0]
    def next_table(m):
        n[0] += 1
        return u'<p class="%s" id="%s">Table %s.%d' % (
            m.group(1), anchor('tbl', n[0]), it['label'], n[0])
    html = TABLE_LBL_RE.sub(next_table, html)

    f = [0]
    def next_fig(m):
        f[0] += 1
        return u'<span class="%s" id="%s">Figure %s.%d' % (
            m.group(1), anchor('fig', f[0]), it['label'], f[0])
    html = FIG_LBL_RE.sub(next_fig, html)

    # anything unlabelled cannot be numbered -- report it
    tables, labels = len(TABLE_RE.findall(html)), n[0]
    figs, figlabels = len(FIGCAP_RE.findall(html)), f[0]
    if tables != labels:
        problems.append('%s: %d table(s) but %d "Table n.n" label(s)'
                        % (it['title'] or it['sid'], tables, labels))
    if figs != figlabels:
        problems.append('%s: %d figcaption(s) but %d "Figure n.n" label(s)'
                        % (it['title'] or it['sid'], figs, figlabels))

    renumbered.append((it['start'], it['end'], html))

for start, end, html in reversed(renumbered):
    doc = doc[:start] + html + doc[end:]

# captions that are just a bare number with no sentence after it
for m in re.finditer(r'<p class="asset-label[^"]*">(.*?)</p>', doc, re.S):
    body = text_of(m.group(1))
    if not re.search(r'—\s*\S', body):
        problems.append('table label has no caption text: %r' % body)

# ------------------------------------------------------------ rebuild both TOCs
# recompute offsets: the doc changed length above
ART_START = doc.index('<article id="article">')
ART_END = doc.index('<section class="footnotes">')
sections = top_level_sections(doc, ART_START, ART_END)

H3_RE = re.compile(r'<h3[^>]*\bid="([^"]+)"[^>]*>(.*?)</h3>', re.S)
CONTAINER_RE = re.compile(r'<(figure|aside|details)\b.*?</\1>', re.S)

rows, app_letters = [], iter(string.ascii_uppercase)
for start, end, tag in sections:
    cls, sid = attr(tag, 'class'), attr(tag, 'id')
    html = doc[start:end]
    h2 = H2_RE.search(html)

    if 'part-divider' in cls:
        tagline = re.search(r'<p class="part-tag">(.*?)</p>', html, re.S)
        title = heading_text(re.search(r'<h2[^>]*>(.*?)</h2>', html, re.S).group(1))
        label = text_of(tagline.group(1)) if tagline else ''
        # the end-matter band's tag already names it; the numbered parts need both
        shown = label if ('backmatter-divider' in cls or not label) else (label + u' · ' + title)
        rows.append(u'<li class="toc-part"><a href="#%s">%s</a></li>' % (sid, shown or title))
        continue

    if 'exercise' in cls:
        title = heading_text(re.search(r'<h2[^>]*>(.*?)</h2>', html, re.S).group(1))
        rows.append(u'<li class="toc-ex"><a href="#%s">%s</a></li>'
                    % (sid, title.split(u'—')[0].strip()))
        continue

    if not h2:
        continue

    eye = EYEBROW_RE.search(html)
    eye_txt = text_of(eye.group(1)) if eye else ''
    if 'appendix' in cls:
        eye_txt = 'Appendix ' + next(app_letters)

    subs = u''
    if 'chapter' in cls and 'backsection' not in cls:
        masked = [(m.start(), m.end()) for m in CONTAINER_RE.finditer(html)]
        for m in H3_RE.finditer(html):
            if any(a <= m.start() < b for a, b in masked):
                continue
            if 'group-title' in m.group(0):
                continue
            subs += u'<li class="toc-sec"><a href="#%s">%s</a></li>' % (
                m.group(1), heading_text(m.group(2)))

    data = u' data-ch="%s"' % sid[4:] if sid.startswith('sec-') else u''
    inner = (u'<em>%s</em>%s' % (eye_txt, heading_text(h2.group(2)))) if eye_txt \
            else heading_text(h2.group(2))
    rows.append(u'<li class="toc-ch"%s><a href="#%s">%s</a>%s</li>'
                % (data, h2.group(1), inner,
                   u'<ol class="toc-subs">%s</ol>' % subs if subs else u''))

TOC = u''.join(rows)

def replace_list(html, list_id, inner):
    """Swap the contents of <ol id=...>, honouring the nested toc-subs lists.

    A non-greedy match would stop at the first nested </ol> and leave the tail
    of the old list in place, appending a fresh copy on every run."""
    open_tag = '<ol id="%s">' % list_id
    i = html.index(open_tag) + len(open_tag)
    depth, j = 1, i
    for m in re.finditer(r'<ol\b[^>]*>|</ol>', html[i:]):
        depth += -1 if m.group(0) == '</ol>' else 1
        if depth == 0:
            j = i + m.start()
            break
    return html[:i] + inner + html[j:]

for list_id in ('toc-list', 'mobile-toc-list'):
    doc = replace_list(doc, list_id, TOC)

# ------------------------------------------------- rebuild the asset index
# Numbers and anchors were assigned above; this reads them back in document
# order, so the index cannot disagree with the book.
KEEP_INLINE = re.compile(r'</?(?!em\b|code\b|sub\b|sup\b|strong\b)[a-zA-Z][^>]*>')

def index_title(raw):
    """Plain-ish text: keep the small inline tags, drop links and the rest."""
    txt = KEEP_INLINE.sub('', raw)
    return re.sub(r'\s+', ' ', txt).strip()

def first_sentence(txt):
    m = re.search(r'^(.{25,}?[.?!])\s+[A-Z(]', txt)
    return m.group(1) if m else txt

def index_rows(entries):
    return u''.join(
        u'<li><a href="#%s">%s</a><span>%s</span></li>' % (aid, num, title)
        for aid, num, title in entries)

figures = []
for m in re.finditer(r'<figure\b.*?</figure>', doc, re.S):
    blk = m.group(0)
    lbl = re.search(r'<span class="asset-label-inline[^"]*" id="([^"]+)">'
                    r'(Figure\s+[0-9A-Za-z]+\.\d+)', blk)
    ttl = re.search(r'<p class="figure-title[^"]*"[^>]*>(.*?)</p>', blk, re.S)
    if not lbl:
        problems.append('figure with no numbered label near: %r' % text_of(blk)[:60])
        continue
    if not ttl:
        problems.append('%s has no <p class="figure-title">' % lbl.group(2))
        continue
    figures.append((lbl.group(1), lbl.group(2), index_title(ttl.group(1))))

tables = []
for m in re.finditer(u'<p class="asset-label[^"]*" id="([^"]+)">'
                     u'(Table\\s+[0-9A-Za-z]+\\.\\d+)\\s*(?:—|&#8212;)\\s*(.*?)</p>',
                     doc, re.S):
    tables.append((m.group(1), m.group(2), first_sentence(index_title(m.group(3)))))

if '<ol id="figure-index">' in doc:
    doc = replace_list(doc, 'figure-index', index_rows(figures))
    doc = replace_list(doc, 'table-index', index_rows(tables))
else:
    problems.append('no <ol id="figure-index"> to hold the asset index')

# ------------------------------------------------------------- integrity checks
ids = re.findall(r'\sid="([^"]+)"', doc)
dupes = sorted({i for i in ids if ids.count(i) > 1})
if dupes:
    problems.append('duplicate id(s): ' + ', '.join(dupes))

idset = set(ids)
broken = sorted({h for h in re.findall(r'href="#([^"]+)"', doc) if h and h not in idset})
if broken:
    problems.append('broken internal link(s): ' + ', '.join(broken))

# ------------------------------------------------------------------------ write
if doc != original:
    io.open(BOOK, "w", encoding="utf-8").write(doc)
    print("updated", os.path.basename(BOOK))
else:
    print("no changes needed")

print("\nsections:")
for it in items:
    if it['kind'] in ('chapter', 'appendix'):
        print(u"  %-3s %s" % (it['label'], it['title']))

if problems:
    print("\n%d problem(s) found:" % len(problems))
    for p in problems:
        print("  - " + p)
    sys.exit(1)
print("\nno problems found")
