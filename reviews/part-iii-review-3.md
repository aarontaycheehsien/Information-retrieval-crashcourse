# Part III (Chapters 12–15) and closing section: third review

Reviewed 10 November 2026 against commit `6d5ebff` (version 1.2.1 with the
unreleased Part I and Part II review changes). All of Part III, Application
exercise III and *What you can now ask* were read. Part III has no raster
figures. Nineteen findings were reported; the author asked for them to be
rechecked, which withdrew one and corrected four, and then asked for all to be
applied.

Product claims were not rechecked against vendor sources. The appendices and the
narrated-video sources were not reviewed.

## Applied

### Closing section

- **Puzzle verdicts.** Table 1.2 says "the end of Part I settles both" of the
  first two puzzles and Chapter 4's summary says Part I explains them; the
  closing panel labelled both "Unresolved". Puzzle 1 now reads "Explained in
  kind; mechanism not identified" and Puzzle 2 "Explained in kind; scoring not
  shown".
- **Puzzle 2.** The November Part I edit changed Table 1.2's question to what
  the count and the display limit each measure, and how many matches were
  scored. The closing entry still answered the old question about ranking. It
  now answers the new one.
- The sentence after the panel keeps its opening words, which the digest test
  uses as a guard, and adds what "could not be settled" means.
- "Six collapses" is now "six confusions", the word the Preface and Parts I and
  II use.
- Three product-claim excerpts quoting the panel were updated
  (`scite-nonsense-query`, `scholar-reported-total`, `scholar-display-limit`).
  The claims themselves are unchanged.

### Chapter 12

- **Evidence base.** The caveat under Table 12.3 treated the table as resting on
  the December 2025 uncited-references probe, although the text says the table
  comes from a separate April 2026 exercise. The caveat now says so.
- **An unkept promise.** The chapter said recovery from a poor query was a
  property "Chapter 14 has to find a way to measure". Chapter 14 did not. The
  sentence now points to the local evaluation set, and Chapter 14's paragraph on
  choosing queries tells the reader to keep some as poorly formed as they
  arrived and to record whether anything useful returns.
- **Opening.** "Two retrieval problems that iteration makes worse" was ambiguous
  beside the three difficulties the chapter and its self-check list. It now
  names the limit no trace reveals as well.
- **Subheading.** New h4 `#retrievers-offered-as-tools` before the Model Context
  Protocol material, which followed the grep worked sequence with no heading.
- **Summary.** Ten points became eight: the two on adaptive control were merged,
  and the two on tools and traces.

### Chapter 13

- Figure 13.1's four panels are a different four from the eligibility questions
  above it. The caption now states the mapping: panels 1 and 2 are the first
  question, panel 4 the second, and panel 3 is where the last two questions and
  the lenses apply.
- The October paragraph on direct file search sat between the questions and the
  figure that illustrates them. It now follows the figure.

### Chapter 14

- **Terminology.** "Known-item seeding" in a footnote and a self-check clashed
  with "known-item lookup" in Table 14.1. Both now say "known-seed recovery",
  the term the body and the evaluation kit use.
- **Assessor disagreement.** The chapter argues that a metric measures agreement
  with whoever judged, but never said assessors disagree. The paragraph on
  judgements now says so, cites Voorhees (2000) and suggests double-judging a
  sample. A reference entry was added.
- **Metric footnotes.** The mean average precision and nDCG footnotes cited only
  Evidently AI pages written for recommender systems. Both now point first to
  chapter 8 of Manning, Raghavan and Schütze (2008).
- **Citations.** The evidence-synthesis note links Lefebvre et al. (2025); the
  pooling footnote links Buckley and Voorhees (2004); the Cranfield footnote
  links Cleverdon (1967). All three were already in the reference list.
- **Evidence-synthesis note.** Moved from between the recall and ranked-metric
  sections to the end of the chapter, after *What a number cannot settle*. Its
  anchor is unchanged.
- **Comparison prompt.** Now opens by saying it is for products that write
  answers. The sentence beginning "Document preparation", where "Document" was
  a verb, is rewritten.

### Chapter 15

- Table 15.2 said it expanded each row of Table 15.1 but had no row for fusion
  and reranking or for direct file search. Both rows were added and the lead-in
  reworded.
- "None of these questions requires reading a loss function" appeared in
  Chapter 14, Chapter 15's body and a self-check. Chapter 15's body now says
  "requires mathematics".
- The definitions of transparency, interpretability and understandability carry
  no source. They are now introduced as this book's working terms.

### Reading times

Visible words, excluding evidence registers: Chapter 12 5,720 → 5,744;
Chapter 13 3,850 → 3,880; Chapter 14 4,929 → 5,063; Chapter 15 4,172 → 4,306.
Labels: Chapter 14 22 → 23 minutes, Chapter 15 19 → 20; Part III about 84 →
about 86.

## Limits of what was verified

- **Voorhees (2000)** was confirmed in OpenAlex
  (https://doi.org/10.1016/S0306-4573(00)00010-8; *Information Processing &
  Management* 36(5), 697–716). The paper was not read. The text describes it
  only by what its title states, and the advice to double-judge a sample is the
  reviewer's, not the paper's.
- **Manning, Raghavan and Schütze (2008), chapter 8.** The chapter title is
  given from memory. The site could not be reached from the review environment,
  so the footnotes link the book's home page, as the reference list does, and
  not the chapter. Mean reciprocal rank was left with its existing source
  because it was not confirmed that chapter 8 covers it.
- **Lefebvre et al. (2025), Buckley and Voorhees (2004), Cleverdon (1967).**
  Links were matched to the reference list by author and topic; the sources
  were not reread.
- The changed blocks were not inspected in a browser. Block nesting was checked
  with a parser, and section order was confirmed from the source.

## Corrections to the review as first reported

- **Withdrawn.** It was reported that Chapter 14 never supplies the "proper
  name" Chapter 12 promises for the unwritten stopping judgement. The link goes
  to *Relevance is a judgement*, which names it as an operational definition of
  relevance. Nothing was changed.
- **Downgraded.** "Two retrieval problems" in Chapter 12's opening was called
  inconsistent with three difficulties. It was defensible but ambiguous.
- **Widened.** "Known-item seeding" was reported in one place; it was in two.
- **Overstated.** The 940-word section in Chapter 12 already had one subheading,
  and "Libraries do not need model weights" appears nearly verbatim twice, not
  three times.

## Open

- **Thirty to fifty queries** (Chapter 14) is a recommendation with no source.
- The **significance** and **recall-denominator** footnotes cite nothing.
- **Mean reciprocal rank** is still sourced only to a recommender-systems page.
- Chapter 15's body and summary both state that libraries do not need model
  weights. This was left as an ordinary echo between a chapter and its summary.
- Chapter 13 still presents three lists of four in quick succession; only the
  mapping between the first two was added.

## What was checked

- Every replacement was an exact match asserted to occur once; the three block
  moves were cut and pasted whole.
- `tools/maintain.py`: no problems found. Footnotes: 56, in order.
- `--check` passes for the product-claims, glossary, digest and vendor
  questionnaire builders, as do `check-product-claims.py --as-of 2026-09-19` and
  the four Python test suites. `test-digest.py` first failed on its guarded
  closing sentence, which was then restored.
- The Node browser checks were not run.
- One `id` added (`retrievers-offered-as-tools`); none removed.
- `read-this-first.html` regenerated for the Chapter 12 summary and the closing
  panel.
