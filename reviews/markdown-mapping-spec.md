# Markdown mapping specification

Date: 2026-11-26. Reviewed edition: version 1.2.1, book unchanged since
commit `0e3d4f8`. Phase 2 of the [conversion plan](markdown-conversion-plan.md).

The machine-readable version is [`data/markdown-mapping.json`](../data/markdown-mapping.json).
`python tools/markdown_mapping.py` checks that every one of the book's 191
classes and 71 element types has exactly one mapping. This document explains
the choices. Where the two disagree, the JSON is what the tests check.

## Reader settings

Pandoc 3.1 reader `markdown-smart-auto_identifiers-implicit_figures`.

- **`smart` off.** Curly quotes, en and em dashes and ellipsis characters are
  written literally, as in the HTML now. Straight quotes stay straight.
- **`auto_identifiers` off.** Only explicit `{#id}` attributes create ids, so no
  new ids appear.
- **`implicit_figures` off.** Figures are built by the book filter, not by
  Pandoc's image-alone-in-a-paragraph rule.
- **Kept on:** `fenced_divs`, `bracketed_spans`, `header_attributes`,
  `link_attributes`, `footnotes`, `pipe_tables`, `table_captions`,
  `definition_lists`, `raw_html`, `tex_math_dollars`. The book contains no
  literal single `$` in prose, so dollar maths is safe.
- **Non-breaking space:** written as `\ ` (backslash, space), which Pandoc reads
  as U+00A0. The 60 `&nbsp;` entities become this.

## File layout (phase 4)

```
book/
  template.html            page shell: head, CSS, scripts, hero, nav, footer
  00-front.md              disclosure notice, preface
  parts/01-part-i.md       part divider and its asides
  01-retrieval-problem.md  one file per chapter, appendix, exercise, back section
  figures/SLUG.html        raw-HTML islands for bespoke diagrams
data/stage-map.json        stage labels, links and tooltips, written once
```

Each file starts with YAML front matter: `key`, `kind`
(chapter|appendix|exercise|backsection|front|part), `eyebrow`, `meta`,
`question`, `legacy_anchors`. File order is book order.

## What the author writes

| Construct | Markdown | Status |
|---|---|---|
| Chapter wrapper, header, eyebrow, reading time, central question | Front matter; body starts `## Title {#key}` | derived |
| Chapter orientation | `::: chapter-orient` as the first block | filter |
| Stage map (15) | `::: {.stage-map on="analysis"}` marker, then `:::` | derived |
| Previous/next navigation (27) | Nothing; from file order | derived |
| Section heading | `### Title {#id}`; the `#` link is added | filter |
| Footnote | `[^name]` and `[^name]: text` in the same file | filter, with a pre-pass |
| Figure | `:::: {.figure key=SLUG}`: title paragraph, body, `::: caption` | filter |
| Table | Pipe table and `: caption sentence` | filter |
| Query-flow diagram (9) | `:::: {.query-flow key=SLUG}` with one list per track | filter |
| Asides (common confusion, practice, question, orientation, distinction map, part recap, chapter close) | `::: {.common-confusion label="IR terminology"}` with optional `#### Heading {#id}` | filter |
| Self-check | `::: self-check` around a definition list (question, then answer) | filter |
| Collapsible detail | `::: {.details}`; the first paragraph is the summary | filter |
| Paragraph with a class or id | `::: {.chapter-transition}` around one paragraph | filter |
| Maths | `$…$` and `$$…$$`, wrapped in `::: math` or `::: {.equation-scroll}` | filter |
| `<var>`, `<small>`, `<b>`, `<output>` in prose | `[d]{.var}` | filter |
| Date stamp | `[Checked September 2026.]{.as-of}` | native |
| Old anchor | `[]{#ch1 .legacy-anchor}` | native |
| Plain styled block | `::: {.terminology-overlap}` | native |
| Bespoke diagram body | `::: {.include src=figures/SLUG.html}` or a `` ```{=html} `` block | raw |

## What the author never writes

These are generated, and the Markdown has at most a placeholder:

- **Tables of contents, figure and table numbers, the figures-and-tables
  index:** `maintain.py`.
- **Product-claims register, evidence links and coverage:**
  `build-product-claims.py`. The Markdown holds nothing: the builder
  re-inserts every evidence-links block after its recorded anchor.
- **Glossary term ids, entry navigation and lookup index:**
  `build-glossary-hub.py`. The Markdown holds the plain definition list.
- **Footnote numbers:** the filter writes 0 and `renumber_footnotes.py` sets
  them, as it does now. (The plan's idea of replacing it is dropped: keeping
  it costs nothing and keeps one owner for numbering.)

## Raw HTML

Raw-HTML islands are the bodies of bespoke worked diagrams: score bars,
posting lists, pruning panels, evidence streams, and the inline SVG plots.
Their titles and captions stay in Markdown.

Measured on the current book:

| Measure | Raw HTML share |
|---|---|
| Authored words | 3.7% |
| Authored elements | 14.1% |

Both are under the plan's 25% stop threshold. Element share is the more honest
measure, because diagrams are markup-heavy.

Raw islands do not block the other-formats goal:

- **EPUB** is XHTML and keeps them, with the book CSS.
- **PDF** should come from the HTML print stylesheet that already exists, not
  from Pandoc's LaTeX route, which would drop raw HTML.

## Why semantic conventions rather than raw HTML

Self-checks as definition lists, query flows as lists and asides as labelled
divs keep meaning in the Markdown. A future EPUB or PDF writer can render them
differently, and an AI editor sees prose rather than markup. The cost is a
larger Lua filter, which the equivalence check verifies.

## Pandoc behaviours the filter must override

These were checked against Pandoc 3.1.3 on 2026-11-26.

- **Footnote labels are dropped from the AST.** The pre-pass must keep
  `[^name]` so that ids stay `fn:name` and `fnref:name`.
- **Tables gain extra markup.** Pandoc adds a `<caption>`, `class="header"` and
  `class="odd"`/`"even"` on rows. The filter writes the book's table markup.
- **Ordered lists gain `type="1"`.** Avoid it with `#.` items or by clearing the
  list style in the filter.
- **Maths is wrapped.** Pandoc emits `<span class="math …">`. The filter writes
  the book's raw delimiters for MathJax instead.
- **List items cannot carry ids.** The 30 vendor-question items start with
  `[]{#vendor-q01 .li-id}`, and the filter moves the id to the `<li>`.

## To verify in phase 3

1. **Stage maps.** All 16 must fit one template plus `stages`. Any that differ
   stay raw until reconciled deliberately.
2. **Previous/next navigation.** Find the rule for the first and last items:
   there are 26 prev and 27 next links.
3. **`maintain.py` placeholders.** Check that it fills empty table-of-contents
   containers and placeholder labels (`Figure ?`, `Table ? —`), not only
   existing ones.
4. **Image `srcset`.** Encoding is inconsistent: `%2C` in the WebP entry and a
   literal comma in the PNG entry. Derive it by a rule only if the rule
   reproduces every image.
5. **Figure variants.** Evidence cards have a title without an id and an id on
   the figcaption. `div.ir-figure` uses `role="group"`.
6. **Maths whitespace.** The text around display-maths delimiters must still be
   equivalent.
7. **Footnote markup.** The exact backreference markup, including the
   non-breaking space before it.
8. **Heading link labels.** The `aria-label` text when a heading contains inline
   markup.
9. **Placeholder positions.** Product-claims links sit inside figures and after
   figcaptions, as well as after headings.

## Phase 3 outcomes (2026-11-26)

Chapters 2 and 3 were converted and rebuilt (see the plan's phase 3 status).
The nine points above were settled as follows:

1. **Stage maps.** There are 15, not 16. Fourteen render byte for byte from
   `data/stage-map.json`. The Part II map is bespoke and stays raw. The stage
   map is a block marker, not front matter, because one map sits in a chapter
   body rather than its header.
2. **Previous/next navigation.** The default rule (neighbour heading id and
   text) reproduces 13 of the 20 standard navigation bars. Exercises use short
   titles, appendices use `Appendix X ·` and "Previous/Next appendix", and the
   last chapter links to the back matter. Phase 4 needs a front-matter
   `nav_title` and appendix handling.
3. **`maintain.py` placeholders.** It fills `Table 0.0 — ` and `Figure 0.0`
   labels and adds their ids. Its regular expressions need the book's exact
   attribute order (class before id) and the `<div class="table-wrap"><table>`
   adjacency, so the filter writes those strings itself.
4. **Image `srcset`.** One rule covers the PNGs with a `.960.webp` sibling:
   commas are percent-encoded in the WebP entry only. The filter derives it
   only when the WebP file exists. Other images carry explicit attributes, and
   `srcset="none"` suppresses derivation.
5. **Figure variants.** Covered by `title-id`, `aria-labelledby`, `tag` and
   `role` attributes and a caption id. Not yet exercised by a converted
   chapter.
6. **Maths whitespace.** The book stores MathJax delimiters as text. The
   converter turns them into Pandoc maths, and the filter writes them back with
   the same surrounding newlines.
7. **Footnote markup.** Reference, definition and backlink reproduced, with a
   no-break space before the backlink. Verified on Chapter 3's seven notes.
8. **Heading link labels.** `aria-label` is the heading's plain text. The
   book's two headings with emphasis (Chapter 7's top-*k* headings) follow the
   same rule. That is checked by a unit test, not yet by a converted chapter.
9. **Placeholder positions.** Not needed (see "What the author never
   writes").

Further findings:

- **`<pre>` already contains `<code>` in the book**, which is Pandoc's native
  output, so no override is needed.
- **The read-this-first digest copies excerpts byte for byte.** Rebuilt HTML
  has different whitespace, so the digest must be regenerated after every book
  build. The regenerated digest is equivalent to the live one.
- **Generated claims blocks can sit inside a figure.** The converter excludes
  them from raw islands, or the builder would add a second copy.
