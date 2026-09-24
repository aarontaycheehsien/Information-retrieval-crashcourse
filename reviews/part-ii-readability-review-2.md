# Part II (Chapters 5–11): second readability pass

Reviewed 24 September 2026 against commit `34b3e7e`, with links into and out of
Part II mapped first: about 330 incoming links, mostly from Appendices D, E and
G; the evidence-register anchors; the glossary's heading destinations; and the
repetition ledger's canonical sentences. Applied in commits `663ca2e`
(Chapter 5), `7597297` (6), `534a85c` (7), `fa33c9d` (8), `3f0f543` (9, plus
Chapter 8's pointer), `2e57e2e` (10) and `43f28ec` (11).

The 18 September pass (`part-ii-readability-review.md`) had fixed the large
placement problems. What remained fell into three groups: chapter openings that
gave the same route three times; captions and body text that repeated each
other; and headings that no longer matched what sat under them, together with a
few wrong cross-references.

## Applied

### Chapter 5
- **5.1** The opening no longer repeats the Chapter 6/7 route that the panel and
  the "Start with the output" box give. This also removes the inaccurate
  "Chapter 6 first explains the encoder architecture".
- **5.2** The paragraph restating the formula-versus-learnt contrast (already
  in panel bullet 1 and Figure 5.1) keeps only its point about reproducibility
  and interpretability.
- **5.3** New h4 `#text-that-supplies-its-own-targets` gives the training-target
  half of "From Word2Vec to retrieval embeddings" its own subheading.

### Chapter 6
- **6.1** Figure 6.2's caption no longer repeats "Two texts can sit close
  together…", which also appears in Chapter 5's panel and in the body.
- **6.2** The phrase "operational model of relevance" is stated once, in the
  chapter's concluding paragraph. This is lighter than the planned merge, so
  that the section's closing statement stays where it is.

### Chapter 7
- **7.1** The two adjacent statements that dense retrieval is the popular route
  to the semantic goal are merged. The four-term distinction and the ledger's
  claim E wording are kept.
- **7.2** The gains-and-compression section now has a lead-in sentence before
  its first figure. Figure 7.5's caption no longer repeats the body's opening
  words. The paragraph after Figure 7.6 is folded into the compression
  paragraph.
- **7.3** Table 7.1, its framing pull quote, its lead-in and the
  vector-database paragraph moved from the top-k section into "Candidate
  boundaries in lexical and dense retrieval", which had been a 91-word stub.
  The ledger's claim D sentence and the top-k section are otherwise unchanged,
  and table order is preserved.
- **7.4** The Puzzle 3 recap is shorter but keeps both result counts, since
  Chapter 1's table sends readers here. The claim excerpt was updated.
- **7.5** The Chapter 3 comparison moved into the paragraph about what a
  similarity score means.

### Chapter 8
- **8.1** Steps 1–5 are now h4 subsections of "A vector does not have to be
  dense or semantic". Ids are unchanged; the glossary accepts h4 destinations;
  the table of contents has five fewer entries (170 → 165 links).
- **8.2** The terminology paragraph keeps only the "sparse embeddings" naming
  note and its footnote; the classification is in Figure 8.6 and Table 8.2.
- **8.3** What chunking into 50 passages produces is stated once.
- **8.4** Chapter 8 said learnt sparse retrieval's pipeline role was "Chapter
  10's subject", linking to a section that never mentions it. The link now
  points to the new Chapter 9 subsection. Applied in the Chapter 9 commit,
  which creates the target.

### Chapter 9
- **9.1** Removed the "Rerankers" section's roadmap sentence and the
  post-Table 9.1 restatement of cheap-then-careful retrieval. The ledger's
  claim B sentence is unchanged.
- **9.2** A second "All three arrangements" meant a different triple from the
  first. It now reads "All three ways of encoding—independent, joint and
  token-level".
- **9.3** Figures 9.2, 9.3 and 9.5 had captions repeating the body; these are
  trimmed. The cross-encoder section's closing echo of its own opening is
  removed.
- **9.4** The Primo Research Assistant table was labelled both Table 9.3 and
  Figure 9.7. Its caption also said the budgets were discussed after it, when
  they are discussed before. It is now only Table 9.3: the wrapper is a
  `div.ir-figure` with `role="group"`, the caption is a
  `p.ir-figure-note`, and one CSS rule was added. The two `#fig-9-7` links now
  point to `#tbl-9-3`, `maintain.py` rebuilt the figure index, and three claim
  excerpts were updated. Figure numbers 9.1–9.6 are unchanged, and nothing
  outside the book referred to Figure 9.7.
- **9.5** New h4 `#learnt-sparse-in-the-pipeline` in the neural IR section.

### Chapter 10
- **10.1** The hybrid/multi-stage examples paragraph keeps only the case
  Figure 10.1 doesn't show.
- **10.2** The third statement of routing-then-fusion is now a pointer to the
  blending section. Its link into Chapter 11 is kept.
- **10.3** "as those sections will add" now names and links Chapter 12.

### Chapter 11
- **11.1** No longer re-announces Chapter 4's distinction ("We can now return…
  during the lexical sections"). The paragraph now links it as "Chapter 4's".
- **11.2** Figure 11.2 moved from the end of "Phrase for the mechanism" to open
  "What a system can do with your query", which had no text of its own. A
  one-line lead-in was added, and figure order is preserved.
- **11.3** New h4 `#what-changed-and-when` before Table 11.3.
- **11.4** The Primo NDE versus Primo Research Assistant note moved to NDE's
  first mention. Its two claim locations were re-anchored from `tbl-11-5` to
  `when-a-system-writes-the-boolean-query`.
- **11.5** There is now one hand-over to Chapter 12, at the end of the chapter.
  The link was moved there rather than dropped.
- **11.6** New h4 `#using-several-query-objects-together` in the query-object
  section.

## Kept as-is

These were left untouched: chapter summaries (relied on by Part III's *Carried
forward* panel and the digest), self-checks, footnotes, Application Exercise II,
Chapter 5's *Before you start* panel and output box, Table 11.1 and Figure
11.1, and every existing `id`.

## Verification

- `maintain.py` reports no problems. `renumber_footnotes.py` shows 56
  footnotes in order. The product-claims, glossary and digest builders pass
  `--check`, as do `check-product-claims.py --as-of 2026-09-19` and the Python
  test suites.
- The three Playwright checks pass: `check-product-claims.mjs`,
  `check-digest.mjs` and `check-glossary-hub.mjs`.
- Rendered comparison with `34b3e7e`: no broken internal links and no console
  errors. There are 224 `.term-mark`s, with the same count in every chapter;
  Chapter 10's first *cross-encoder* mark now falls on a capitalised instance.
  Part II rendered words fell from 21,156 to 20,903. Table 9.3 and the moved
  Table 7.1 were inspected in screenshots.
