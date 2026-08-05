# -*- coding: utf-8 -*-
"""Confirm the textbook edition preserves every word of source prose."""
import io, os, re

REPO = r"C:\Users\aarontay\Downloads\Codex\informationretrievalcrashcourse"
src = io.open(os.path.join(REPO, "how-search-decides-what-you-see.html"), encoding="utf-8").read()
new = io.open(os.path.join(REPO, "search-textbook.html"), encoding="utf-8").read()

def article(h):
    a = h.index('<article id="article">')
    b = h.index("</section></article>")
    return h[a:b]

def strip_drafted(h):
    """Remove every element carrying class="...drafted..." (one nesting level deep)."""
    out, i = [], 0
    pat = re.compile(r'<(\w+)[^>]*\bclass="[^"]*\bdrafted\b[^"]*"[^>]*>')
    while True:
        m = pat.search(h, i)
        if not m:
            out.append(h[i:]); break
        out.append(h[i:m.start()])
        tag, depth, j = m.group(1), 1, m.end()
        # include the closing '>' so no stray bracket survives the slice
        open_re = re.compile(r'<(/?)%s\b[^>]*>' % tag)
        while depth and j < len(h):
            mm = open_re.search(h, j)
            if not mm: break
            depth += -1 if mm.group(1) else 1
            j = mm.end()
        i = j
    return u''.join(out)

def words(h):
    h = re.sub(r'<(script|style)\b.*?</\1>', ' ', h, flags=re.S)
    h = re.sub(r'<[^>]+>', ' ', h)
    h = h.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&mdash;', '-')
    return re.findall(r'\S+', h)

s_words = words(article(src))
n_words = words(strip_drafted(article(new)))

print("source words              :", len(s_words))
print("textbook words, drafts out:", len(n_words))
print("difference                :", len(n_words) - len(s_words))

# multiset diff -- what is present in one but not the other
from collections import Counter
cs, cn = Counter(s_words), Counter(n_words)
lost = (cs - cn)
added = (cn - cs)
print("\nwords in SOURCE not in textbook (should be ~0):", sum(lost.values()))
print(" ", list(lost.items())[:14])
print("\nwords in TEXTBOOK not in source (labels/anchors):", sum(added.values()))
print(" ", list(added.items())[:14])
