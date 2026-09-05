# -*- coding: utf-8 -*-
"""Renumber the book's footnotes to follow document order.

The book numbers footnotes by hand in three places: the superscript ref, the
"Jump back to footnote N" title on the backref, and the order of the <li> items
in the footnotes list. Moving a passage breaks all three. This pass reads the
refs in document order and rewrites the numbers and the list order to match.

Re-runnable and idempotent. Run it after any edit that moves or adds a footnote.
"""
import io, os, re, sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(REPO, "search-textbook.html")

src = io.open(SRC, encoding="utf-8").read()

split = src.index('<section class="footnotes">')
body, notes = src[:split], src[split:]

REF_RE = re.compile(
    r'<sup id="fnref:(?P<key>[^"]+)"><a class="footnote-ref" href="#fn:(?P=key)">'
    r'(?P<num>\d+)</a></sup>')

order = [m.group("key") for m in REF_RE.finditer(body)]
if len(set(order)) != len(order):
    sys.exit("a footnote is referenced twice: " + str(order))

# ------------------------------------------------------------ renumber the refs
rank = {k: i + 1 for i, k in enumerate(order)}
body = REF_RE.sub(lambda m: m.group(0).replace(
    ">%s</a></sup>" % m.group("num"), ">%d</a></sup>" % rank[m.group("key")]), body)

# --------------------------------------------- split the list into its <li> items
head_end = notes.index("<ol>") + len("<ol>")
tail_start = notes.rindex("</ol>")
head, items_html, tail = notes[:head_end], notes[head_end:tail_start], notes[tail_start:]

items, pos = {}, 0
LI_RE = re.compile(r'<li id="fn:(?P<key>[^"]+)">')
marks = list(LI_RE.finditer(items_html))
for i, m in enumerate(marks):
    end = marks[i + 1].start() if i + 1 < len(marks) else len(items_html)
    items[m.group("key")] = items_html[m.start():end]

missing = [k for k in order if k not in items]
orphan = [k for k in items if k not in rank]
if missing or orphan:
    sys.exit("ref without note: %s / note without ref: %s" % (missing, orphan))

# ------------------------------- reorder the items and fix each backref's title
BACKREF_RE = re.compile(r'(title="Jump back to footnote )\d+( in the text")')
rebuilt = []
for k in order:
    chunk = BACKREF_RE.sub(lambda m: m.group(1) + str(rank[k]) + m.group(2), items[k])
    rebuilt.append(chunk.rstrip() + "\n")

out = body + head + "\n" + "".join(rebuilt) + tail
if out != src:
    io.open(SRC, "w", encoding="utf-8").write(out)
    print("renumbered %d footnotes" % len(order))
else:
    print("already in order (%d footnotes)" % len(order))

for i, k in enumerate(order, 1):
    print("  %2d  %s" % (i, k))
