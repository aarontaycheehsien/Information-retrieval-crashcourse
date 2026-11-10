# Appendix E (Learning to rank, diversification and rerankers): review

Reviewed 10 November 2026 against commit `1f1b409`. The appendix is about 4,030
words with five tables and one HTML figure. Eight findings were reported. A
rethink requested by the author kept six and changed the proposed fix for two.
The author then asked for all to be applied.

## What was verified before any change

- **The Semantic Scholar account matches its source.** The 2020 engineering
  post (Feldman, "Building a Better Search Engine for Semantic Scholar", 20
  July 2020) was read in full. Every claim in Table E.5 and in the click-log
  section is in it: almost 190 million papers and a top 1,000; a LightGBM
  ranker with a LambdaRank objective; 22 features; KenLM chosen because it
  could be called dozens of times; random position-swap experiments and
  inverse-propensity weighting; removal of about a third of the data; a
  250-query hand-analysed evaluation set; and post-hoc correction rules.
- **The worked MMR example is correct.** All four values in the MMR table
  recompute as printed.

## Applied

- **Order.** Diversification sat between the three learning-to-rank
  formulations and "Why LTR often becomes a reranker", splitting the
  learning-to-rank argument with about 900 words on another subject. It now
  follows "Fusion and reranking solve different problems", which is also the
  order in which the appendix's opening lists its four ideas. The diversification
  tables are now E.1 and E.2 and the learning-to-rank tables E.3 and E.4. Table
  E.5, to which six product-claim locations are anchored, keeps its number, so
  no claim data changed. Section anchors are unchanged.
- **Hand-over sentence.** "The worked explanation of reciprocal rank fusion is
  now in Chapter 10" referred to a restructuring the reader never saw. The
  sentence now says Chapter 10 covers rank and score fusion, links both, and
  announces the new order.
- **Score fusion.** The toy-mixture section's sentence on score fusion links
  Chapter 10's section on combining scores.
- **Position bias.** The sentence that a result at rank one is more likely to be
  clicked because it is at rank one cites Joachims et al. (2005).
- **α-nDCG.** Two consecutive sentences said the same thing. They are merged.
- **MMR example.** "Slightly lower relevance" described 0.75 against 0.90; it now
  says "lower".
- **Closing questions.** The heading "What to ask about either method" dated
  from when the section covered two methods; it now says "each method". The
  fusion prompt, headed "Before RRF", asked only about lists, depths and
  weights; it is now "Before fusion" and also asks whether ranks or scores were
  combined and how scores were normalised. The reranking prompt gains a clause
  asking whether the list was diversified and by what notion of difference.

`vendor-questionnaire.html` was regenerated: the first ranking-method prompt is
now labelled "Before fusion" and two prompts carry the new wording. The mapping
file and its "listen for" cues are unchanged.

## Changes to the plan as first proposed

- **A fifth prompt was not added.** The first proposal was to add a separate
  diversification prompt. The questionnaire test asserts exactly four
  ranking-method prompts, so that would have meant changing the mapping file,
  the test and the maintenance guide. The clause added to the reranking prompt
  covers the point without touching them.
- **The section moved forward, not to the end.** The first proposal was to move
  diversification after "A reranker is broader than learning to rank". That
  would have renumbered the Semantic Scholar table from E.5 to E.3 and required
  six claim anchors to be updated. Second position needs none.

## Limits of what was verified

- Joachims et al. (2005) was not read. It is cited for the general point that
  click data are biased by position, which its title supports.
- The sources for the diversification methods and for the RankNet, LambdaRank
  and LambdaMART lineage were not read; their links were checked to be present.
- The PubMed feature list was not rechecked against its source.
- The page and the regenerated questionnaire were not inspected in a browser.

## What was checked

- The block move was cut and pasted whole; every replacement was an exact match
  asserted to occur once.
- `tools/maintain.py` renumbered the tables and reports no problems, including
  no stale cross-references. The footnote check, the four builder `--check`s,
  `check-product-claims.py --as-of 2026-09-19` and the four Python test suites
  pass. The Node browser checks were not run.
