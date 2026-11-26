# Markdown sources (converted, not yet the source of truth)

These files are the whole book converted to Markdown by phase 4 of
[the conversion plan](../reviews/markdown-conversion-plan.md). Until cut-over,
`search-textbook.html` remains the source of truth and **these files are
regenerated from it, not edited**:

```bash
python tools/markdown/html_to_md.py --book book     # regenerate after editing the HTML
python tools/markdown/html_to_md.py --check book    # is book/ stale?
python tools/markdown/pilot.py --book book          # build from book/ and compare (about a minute)
```

- `NN-*.md`: one file per top-level part of the article, in book order. The
  front matter says what kind it is (chapter, appendix, exercise, part,
  backsection, glossary, fragment).
- `39-product-claims-register.html`: empty markers that the claims builder
  fills.
- `template.html`: the page shell, with head, styles, scripts, hero and empty
  TOC lists.
- `figures/`: raw-HTML bodies of bespoke worked diagrams, included from the
  chapter files.

The conventions are in
[`reviews/markdown-mapping-spec.md`](../reviews/markdown-mapping-spec.md).
