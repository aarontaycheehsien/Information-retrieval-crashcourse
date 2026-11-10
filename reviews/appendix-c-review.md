# Appendix C (Advanced inverted-index execution): review

Reviewed 10 November 2026 against commit `1fdeef8`. The appendix was about
2,150 words with four HTML figures and one table. Eleven findings were reported.
A recheck requested by the author confirmed two against the cited paper,
withdrew one, restated two and added one. The author then asked for all to be
applied, following the reviewer's two recommendations.

## What was verified before any change

- **The worked BM25 example is correct.** All four document scores, every term
  contribution and the heap threshold were recomputed from Table 2.3's records
  with the stated parameters and match Figures C.2 and C.3.
- **Figures C.1 and C.4 are correct** step by step: the two-cursor
  intersection, the essential and non-essential split for MaxScore, and the
  WAND pivot.
- **Lassance and Clinchant (2022) was read in full** through a full-text
  service (https://doi.org/10.1145/3477495.3531833).

## Applied

### The paragraph on Lassance and Clinchant (2022)

The appendix said the paper closed the latency gap through three moves:
query-side regularisation, separate encoders and "pruning of the longest
posting lists". The paper's four contributions are separate query and document
encoders, L1 regularisation for queries, a middle-training step with FLOPS
regularisation, and a smaller query encoder. Posting-list pruning is not among
them.

The appendix also said "published measurements" put SPLADE-style latency at
"several times BM25's … with short queries the worst case", naming no source.
The paper does not say short queries are the worst case. It cites a reported
265 milliseconds for the earlier model, measures a total of 691 on its own
machine and gives BM25 as about 4.

The paragraph was rewritten to state those figures and the four changes. It
also adds what the appendix had omitted: the paper reports that the gains
reduced effectiveness outside the training domain, and that combining scores
with BM25 offset the loss. The paragraph links Chapter 13 on transfer and
Chapter 10 on score fusion. The link, and the reference-list entry, now point
to the SIGIR record instead of arXiv.

### Other changes

- **An unsourced claim softened.** "The terms such a model adds are
  disproportionately frequent ones" had no source. It now says that every added
  term brings its posting list, and a common one brings a long list.
- **The formula.** The book gave the IDF and query-frequency parts of BM25 in
  Chapter 3's footnotes but never the term-frequency part, so D4's 0.629 could
  not be reproduced. The factor is now shown, with D1 and D4 worked.
- **The four records.** "Consider the same four records" followed a section
  whose example uses a larger collection. The sentence now links Table 2.3 and
  the records are reprinted.
- **Positions.** One paragraph says postings may also hold positions, used by
  phrase and proximity operators, and links Chapter 2's section on them.
  That section links back.
- **Wording.** "The dictionary table above" now names and links Figure C.2. A
  sentence about individual upper bounds that was hard to parse is replaced by
  a shorter one.

Visible words rise to about 2,410. The reading-time label moves from about 11
to about 12 minutes. No `id` was added or removed.

## Not applied, on the reviewer's recommendation

- **Lucene's variant of the formula.** The example keeps the classic (k₁ + 1)
  numerator. The reviewer recalls that Lucene dropped that factor in version 8,
  which would scale every score without changing the order, so the example's
  numbers would not match an Elasticsearch explanation. This could not be
  checked from the review environment and was left out. The book uses the
  classic form consistently, so the example is internally sound either way.
- **Mackenzie, Trotman and Lin (2021)** was a candidate source for the softened
  claim. It was confirmed to exist in OpenAlex but not read, so it is not cited.

## Corrections to the review as first reported

- **Withdrawn.** Figure C.4's three level-five headings were reported as
  breaking a maintenance rule. The rule covers figure titles; the book uses
  level-five headings 14 times and the table-of-contents builder skips headings
  nested in figures.
- **Restated.** "Chapter 3 shows no formula" was wrong: its footnotes give two
  parts of it. The missing part was the term-frequency factor.
- **Simpler than proposed.** Table 2.3's caption already says it is returned to
  in Appendix C; the appendix lacked only the link back.

## What was checked

- Every replacement was an exact match asserted to occur once. A first attempt
  failed on one pattern and wrote nothing; it was corrected and rerun.
- `tools/maintain.py`, the footnote check, the four builder `--check`s,
  `check-product-claims.py --as-of 2026-09-19` and the four Python test suites
  pass. The Node browser checks were not run.
- The page was not inspected in a browser. The new formula uses the same
  display-mathematics markup as Chapter 10's, but its rendering was not seen.
