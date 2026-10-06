# Part III (Chapters 12–15) and closing section: second readability pass

Reviewed 25 September 2026 against commit `c41cd68`. Before planning, the
connections were mapped:

- about 165 incoming links, mostly from Appendices D and G;
- the teaching notes' targets (`diagnosing-failure`, `library-practice`,
  `exercise3`);
- the vendor questionnaire, generated from the `vendor-q*` list items;
- the digest's closing puzzle panel and its two guarded closing paragraphs;
- 40 evidence-register locations.

Applied in commits `5f6f083` (Chapter 12), `5a2ce41` (13), `135b73b` (14),
`7d9bddb` (15) and `bb554f9` (closing section).

The 18 September pass (`part-iii-readability-review.md`) had fixed the obvious
problems and deliberately added no subheadings to Chapter 12. Three things
remained:

- the same points made several times in a row;
- long stretches without a heading, including about 1,100 words at the start of
  Chapter 13 holding its diagnostic core;
- a few misplaced paragraphs and one wrong chapter reference.

## Applied

### Chapter 12
- **12.1** The Chapters 9–11 recap is now folded into the opening, removing a
  second "decided before any user arrived". The pseudo-relevance feedback
  paragraph keeps only where the fixed, adaptive and agentic lines fall.
- **12.2** New h4 subheadings, overriding the earlier pass's decision:
  `#placing-a-tool-from-its-documentation` (Web of Science Research Assistant,
  placed from a vendor post rather than by testing),
  `#an-experiment-with-zero-result-searches` and `#what-the-loop-cannot-know`.
- **12.3** "What the loop is for" no longer opens with the scoring-versus-process
  point that its closing pull quote and the chapter summary both carry.

### Chapter 13
- **13.1** Two new h3 sections now appear in the table of contents:
  `#could-the-record-have-been-returned` (the eligibility questions and
  Figure 13.1) and `#four-diagnostic-lenses` (Table 13.1). The legacy anchors
  `diagnosing-where-retrieval-goes-wrong` and
  `three-different-ways-vocabulary-can-go-wrong` stay where they were.
- **13.2** "Not mutually exclusive / may coexist" was stated five times. The
  opening's sentence and Figure 13.1's clause are removed; Table 13.1's
  caption, the explanation after it, the remedy section and the summary keep
  it.
- **13.3** Eligibility questions 4 and 5 are merged into one question that
  links to Chapter 4's four explanations. The lead-in now says "four
  questions", and nothing else in the repo quoted "five".
- **13.4** The scope restatement in the opening is gone; its diagnostic point
  is kept.
- **13.5** "Diagnose before choosing a remedy" links back to the eligibility
  section instead of re-explaining it.

### Chapter 14
- **14.1** The second relevance paragraph keeps only its test-collection
  point. The superseded, retracted and neighbouring-question examples moved
  into it.
- **14.2** Changes to the precision-and-recall section:
  - The recall-measurement paragraph (footnote 44) moved up beside the
    trade-off; footnote order is unchanged.
  - New h4 `#where-recall-is-decided`.
  - The worked-number block quote is replaced by a pointer to Figure 14.1.
  - The repeated ceiling sentence and a clause of Figure 14.2's caption are
    removed.
  - The ledger's claim B canonical sentence (Chapter 9) is untouched.
- **14.3** Test-collection pooling was contrasted with vector pooling "in
  Chapter 5". The link now points to Chapter 6
  (`#model-tokens-are-not-indexed-terms`, Figure 6.1), where pooling is
  explained.
- **14.4** "Building an evaluation set you own" opens with its argument; the
  evaluation-kit link follows it.

### Chapter 15
- **15.1** The paragraph repeating the opening's three consequences is removed,
  and the next paragraph now names "the three sections below". The governance
  section states "require in advance" once, without re-arguing it.
- **15.2** The three reproducibility points are set as a list.
- **15.3** After Table 15.2, "Across all methods" keeps its new content, and
  the bold determinism paragraph, which restated the section's first point and
  the interpretability section's close, is removed.

### Closing section
- **C.1** The paragraph after the puzzle map no longer repeats the map's own
  "two unsettled, one settled by a document" verdict.
- **C.2** Puzzle 1's verdict links to Chapter 4's four explanations instead of
  listing them a fifth time. The `scite-nonsense-query` excerpt was updated and
  the digest rebuilt.

## Kept as-is

These were left untouched: the chapter summaries (including Chapter 12's ten
bullets), self-checks, footnotes, both detail tables in Chapter 15, the 19
vendor-question list items, Exercise III, the digest's guarded closing
paragraphs, and every existing `id`. The lecturer passage near the end echoes
the preface almost verbatim; it is treated as a deliberate bookend. The "loss
function" line and "iteration is not agency" recur by design.

## Verification

- `maintain.py` reports no problems. `renumber_footnotes.py` shows 56
  footnotes in order. The product-claims, glossary, digest and vendor
  questionnaire builders pass `--check`, as do
  `check-product-claims.py --as-of 2026-09-19` and the Python test suites.
- The four Playwright checks pass: product claims, digest, glossary hub and
  vendor questionnaire.
- Rendered comparison with `c41cd68`: no broken internal links and no console
  errors. The 224 `.term-mark`s are identical in position. The table of
  contents gained the two Chapter 13 entries (165 → 167). Part III rendered
  words fell from 16,766 to 16,450. The new Chapter 13 heading was inspected
  in a screenshot.
