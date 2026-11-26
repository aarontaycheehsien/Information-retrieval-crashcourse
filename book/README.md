# The book's Markdown source

These files are the **source of truth** for *How search decides what you see*
since the cut-over in phase 6 of
[the conversion plan](../reviews/markdown-conversion-plan.md).
`search-textbook.html` and `read-this-first.html` are built from them and must
not be edited by hand.

```bash
python tools/build-book.py           # rebuild after editing (Python 3 and Pandoc 3.1)
python tools/build-book.py --check   # do the committed pages match a fresh build?
python tools/test-build-book.py      # build checks, including determinism
```

Once merged into `main`, a GitHub Actions workflow
(`.github/workflows/build-book.yml`) rebuilds and commits the pages whenever
`book/` changes, so you can edit these files without Pandoc installed.

- `NN-*.md`: one file per top-level part of the book, in reading order. The
  two-digit prefix sets the order; the front matter says what kind each is
  (chapter, appendix, exercise, part, backsection, glossary, fragment).
- `39-product-claims-register.html`: empty markers that the claims builder
  fills.
- `template.html`: the page shell, with head, styles, scripts, hero and empty
  TOC lists. Edit it for changes outside the book's body.
- `figures/`: raw-HTML bodies of bespoke worked diagrams, included from the
  chapter files.
- `book.json`: records that Markdown is the source of truth.

The writing conventions (headings, figures, tables, asides, self-checks,
footnotes, maths) are in
[`reviews/markdown-mapping-spec.md`](../reviews/markdown-mapping-spec.md).
Navigation, numbering, tables of contents, footnote numbers, the glossary
lookup and the product-evidence blocks are generated, so never write them by
hand.
