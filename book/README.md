# Markdown sources (pilot)

These files are **pilot outputs** of the Markdown conversion, not the book's
source yet. Until the phase 4 freeze in
[the conversion plan](../reviews/markdown-conversion-plan.md),
`search-textbook.html` remains the source of truth. Do not edit these files:
regenerate them.

```bash
python tools/markdown/html_to_md.py sec-boolean-admission book/02-boolean-admission.md
python tools/markdown/html_to_md.py sec-bm25-ranking book/03-bm25-ranking.md
python tools/markdown/pilot.py book/02-boolean-admission.md book/03-bm25-ranking.md
```

The conventions are in
[`reviews/markdown-mapping-spec.md`](../reviews/markdown-mapping-spec.md).
`figures/` holds the raw-HTML bodies of bespoke worked diagrams, included
from the chapter files.
