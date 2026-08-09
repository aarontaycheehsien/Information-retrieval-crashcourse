# Tooling

`search-textbook.html` is the **source of truth**. Edit it directly. Nothing
generates it, and nothing overwrites your prose.

Two maintenance passes keep the machine-owned parts consistent. Both are
idempotent — safe to run any time, and they report "no changes needed" when
there is nothing to do.

## After editing

```bash
python tools/maintain.py
python tools/renumber_footnotes.py
```

### `maintain.py`

Rewrites, in place:

- **Table and figure numbers.** Derived from each chapter's own eyebrow
  (`Chapter 4` → `Table 4.1`, `Table 4.2`, …). To renumber a chapter, edit the
  eyebrow and re-run — the assets follow.
- **Appendix letters.** Derived from the order the appendices appear in, in both
  the eyebrow and the asset prefixes. Reorder them and the letters follow.
- **Both tables of contents.** Rebuilt from the actual headings, so a new
  chapter or section appears automatically. Sections nested inside a figure,
  aside or `<details>` are skipped, as are group-divider headings.
- **Asset anchors.** Each table label and figure label gets an `id` derived from
  the number just assigned — `tbl-4-1`, `fig-3-4` — so any asset can be linked
  to directly.
- **The Figures and tables index.** The two lists in the `#figures-and-tables`
  back-matter section are rebuilt from the assets themselves, in document order.
  Figure entries take their text from the figure's `<p class="figure-title">`;
  table entries take the first sentence after the em dash. The index therefore
  cannot disagree with the numbers in the text.

Then it reports what it cannot fix and exits non-zero:

- a table or figure with no `Table n.n` / `Figure n.n` label
- a table label that is a bare number with no caption sentence after the dash
- a figure with no `<p class="figure-title">` for the index to quote
- duplicate `id` attributes
- broken internal links

**Caption text lives in the HTML**, not in the tool. `maintain.py` only owns the
number prefix; everything after the em dash is yours.

### `renumber_footnotes.py`

Reads the superscript refs in document order and rewrites the numbers, the
`<li>` order in the footnotes list, and each backref's "Jump back to footnote N"
title so all three agree. Run it after moving or adding a footnote.

## Conventions the tools rely on

Keep these shapes when hand-editing, or the passes will not find the pieces:

| Thing | Markup |
|---|---|
| Chapter | `<section class="chapter" id="sec-KEY">` with `<p class="chapter-eyebrow">Chapter N</p>` then `<h2 id="KEY">` |
| Appendix | `<section class="chapter appendix" id="app-X">` with an `Appendix X` eyebrow |
| Table label | `<p class="asset-label drafted">Table 4.1 — caption sentence.</p>` immediately before the `.table-wrap` |
| Figure label | `<span class="asset-label-inline drafted">Figure 4.1</span>` as the first child of the `<figcaption>` |
| Figure title | `<p class="figure-title" id="SLUG-title">` as the first child of the `<figure>`. Not a heading — figure titles must stay out of the document's heading outline |
| Asset index | `<ol id="figure-index">` and `<ol id="table-index">`, emptied and refilled on every run. Do not hand-edit their contents |
| Back-matter section | `<section class="chapter backsection">` with an `<h2 id="…">`. Gets a TOC row, no sub-entries, and no asset numbering |
| Pinned TOC links | `<ul class="toc-pinned">` sits *outside* `<ol id="toc-list">`, which is why it survives the rebuild. Both TOCs carry a copy |
| Chapter reading time | `<p class="chapter-meta">` immediately after the eyebrow; the page's own script moves it into the chapter-head row |
| Drafted prose | any element carrying `class="… drafted"`. The Review mode button that reveals it is hidden unless the page is loaded at `#review` |

The `data-ch` attribute on a TOC chapter row must match its section id minus the
`sec-` prefix; `maintain.py` writes this for you.

Two things the page does at runtime rather than in the markup, so nothing needs
maintaining by hand: the **Copy link** control on every chapter heading, and the
first-use **term marks**, whose definitions are read out of the `#glossary`
definition list. To add a term mark, add the term to the glossary and, if it is
unambiguous enough to match safely in prose, to the `MARKED` list in the page
script.

## `legacy/`

Until August 2026 the textbook was generated from
`how-search-decides-what-you-see.html` by `legacy/build_textbook.py`, with new
prose held in `legacy/book_data.py` and a prose-preservation check in
`legacy/verify.py`.

That pipeline is retired. **Do not run `build_textbook.py`** — it would
overwrite `search-textbook.html` from the old article and discard everything
written since. The files are kept only as a record of how the chapter structure,
apparatus and captions were originally produced.

`how-search-decides-what-you-see.html` remains published as the earlier
single-flow edition. It is now frozen and will drift from the book.
