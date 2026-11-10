# Part II (Chapters 5–11): third review

Reviewed 10 November 2026 against commit `33f3fa5` (version 1.2.1 with the
unreleased Part I, grep and exact-match/best-match additions). The whole of
Part II was read, and all 13 raster figures in it were opened and compared with
their titles, captions and surrounding text. Findings were applied in four
commits: `3251d0b` (text corrections), `ff2f437` (figures), `5ec12c4`
(Chapter 9 order) and `7f9e6b2` (gaps).

The September passes (`part-ii-readability-review.md` and
`part-ii-readability-review-2.md`) fixed placement and duplication. This pass
found what they could not: figures that no longer matched the text around them,
sequencing damage from the October additions, and content gaps.

Product claims were not rechecked against vendor sources. The narrated-video
sources under `tools/chapter-*-investigations/` are dated snapshots and were not
changed.

## Applied

### Figures that contradicted or did not match the text

- **Figure 6.2** was titled *Pretraining gives language patterns; retrieval
  training teaches what should rank together* but its artwork was "Why the hard
  negative is hard". It used hard negatives a section before the worked example
  defines them and labelled one arrow "True relevance". Redrawn in HTML as two
  cards, pretraining and retrieval training, each giving the target, what is
  rewarded and what pooling then yields.
- **Figure 7.6** was captioned as the compression bottleneck but its artwork was
  "Precompute once, search many times", which is about efficiency. No image in
  the repository showed the bottleneck. Redrawn in HTML: one invented passage
  encoded once, then three later queries (broad topic, exact code, negation)
  meeting the same vector.
- **Figure 7.5** labelled its axes "general topic" and "topic nuance", although
  Chapters 5 and 8 say dense dimensions cannot be named. It also used "learned".
  Redrawn in HTML with the lexical and dense routes side by side.
- **Figure 9.5** listed "cross-encoder" and "ColBERT" inside the listwise panel's
  LLM reranker and called listwise "often best", which the text does not claim.
  Redrawn in HTML as three cards giving the question asked, the number of calls,
  the output and the main weakness.
- **Figures 8.7 and 8.8** showed the same split of one article with different
  numbers (words 1–200 and 120–320 in one; tokens 1–200 and 150–350 in the
  other). Figure 8.7's raster half also said an abstract-only index "preserves
  full context". The raster half is redrawn in HTML using the body text's own
  figures (1, about 10, about 50 units); Figure 8.8 is removed and its caption
  sentence joins Figure 8.7's. Figure 8.8 was the chapter's last figure and
  nothing linked to it, so no number changes.
- **Alt text.** Figures 6.3, 7.4, 9.1, 9.2 and 9.3 had alt text that only
  repeated the title. Each now describes what is shown. Figure 7.4's caption
  says its scores are illustrative similarity scores; Figure 9.2's caption says
  the drawing repeats one document encoder.

Titles, numbers and anchors of the redrawn figures are unchanged. The replaced
PNG files remain in `images/` but nothing references them. No CSS was added.

### Errors in the text

- Chapter 7's third self-check paired a "gene identifier" with "near-miss
  compounds". It now says "chemical identifier".
- Chapter 10 said "Hybrid retrieval protects against systems with different and
  partly complementary blind spots". It now says hybrid retrieval combines
  systems whose blind spots differ.
- Chapter 7's opening said it "resolves the first of the two distinctions Part I
  left open". Part I now leaves five. It reads "settles one of the five
  confusions listed at the start of Part II".
- Chapter 8's summary mentioned direct file search, which the chapter body never
  discussed. The body now makes the point, linking to the grep section, so the
  summary and the digest are unchanged.
- Table 11.2 cited Gupta and Bendersky (2015) for dense retrievers. That survey
  of verbose queries predates dense retrieval. The row now attributes the
  finding to pre-neural retrieval, links the DOI, and says that a dense model's
  behaviour has to be tested.

### Sequencing

- Chapter 6's second paragraph used "positive pairs and hard negatives" and "the
  passage about unrealistic expectations" before the worked example. Reworded so
  that it needs neither.
- Figure 8.3's caption introduced SPLADE two sections early. It now says the
  lower panel looks ahead and links the section.
- Chapter 7's box *Why not return everything above a similarity score?* answered
  a top-k question before top-k was taught. It moved to the end of the top-k
  section. The pull quote that followed it now sits after Table 7.1.
- Chapter 11's grep paragraph was stranded after a pull quote. It is now a row
  of Table 11.2.
- Figure 7.7 ranked by Euclidean distance, a term used nowhere else. Its note
  now names it as another comparison rule.
- Chapter 11 said to read Table 11.1 "in three groups" that the row order did
  not show. The sentence now names which rows belong to each group.
- Chapter 6 stated twice that a negative label depends on the stated need. The
  second statement is removed and its footnote moved to the first; the footnote
  is now 24 and the four after it each move up by one.
- Figure 7.4 opened its section with no lead-in. One sentence added.

### Chapter 9

- The neural IR key distinction and its learnt sparse subsection moved from the
  end of the chapter to follow *LLMs as rerankers*. The chapter now covers every
  neural arrangement, then diversification, and closes on the two documented
  pipelines and the Primo walk-through. The September review placed the learnt
  sparse subsection last so that it would sit beside Chapter 10; the subsection
  now says why it matters for Chapter 10 instead. No anchor, table or figure
  number changes.
- Two of about ten statements that a reranker cannot add an excluded record were
  removed (the orientation panel's closing sentence and the LightGBM clause).
  The sentence "Everything outside the first stage's results is unreachable
  either way" stays because two product-claim excerpts quote it.
- One of two section openings beginning "Many production search systems" was
  reworded.

### Gaps

- **Chapter 5.** The summary's first point was about dense retrievers, which the
  chapter does not cover, and nothing in the summary or self-checks tested the
  three ideas the opening panel asks the reader to carry forward. Two summary
  points now cover the embedding and vector distinction and specified versus
  learnt calculation; two self-checks were added.
- **Chapter 6.** The summary gains pooling and training-signal proxies.
- **Chapter 10.** New section *Combining scores instead of ranks*
  (`#combining-scores-instead-of-ranks`), about 190 words, after the RRF section.
  The summary gains a point on RRF and one on score fusion, moved out of the
  hand-off paragraph. One self-check on RRF was added; its arithmetic (1/61 ≈
  0.0164 against 2/110 ≈ 0.0182) was checked by hand.
- **Chapter 8.** The indexed-units section now says the question applies to
  lexical indexes too.
- **Part II return.** The opening panel told readers to come back "at the end"
  and linked the book's closing section, which does not restate the five
  confusions. Application exercise II now opens by returning to them, and the
  panel links there.
- **Citations.** Harris, Greenhalgh and Peacock, Sjögårde and Ahlgren, Bates,
  Wang and colleagues (two papers) and FollowIR were named in the text without
  links, although all are in the reference list. Each now links to the URL its
  reference entry gives. Firth has no URL in the reference list; the year was
  added.

### Reading times

Visible words, excluding evidence registers: Chapter 5 2,966 → 3,161; Chapter 6
1,747 → 1,876; Chapter 7 3,613 → 3,899; Chapter 8 3,403 → 3,562; Chapter 9
4,064 → 4,173; Chapter 10 1,681 → 2,057; Chapter 11 4,342 → 4,384. Part of the
increase is figure text that used to be inside images. Labels: Chapter 5 15 →
16 minutes, Chapter 6 8 → 9, Chapter 7 18 → 19, Chapter 8 16 → 17, Chapter 10
9 → 11; Part II about 107 → about 113.

## Limits of what was verified

- **Bruch, Gai and Ingber (2023).** The record was confirmed in OpenAlex
  (https://doi.org/10.1145/3596512; *ACM Transactions on Information Systems*
  42(1), 1–35). Only the abstract could be read in the review environment. The
  new section therefore claims only what the abstract states: that RRF is
  sensitive to its parameters, that a convex combination outperformed it in
  in-domain and out-of-domain settings, and that it needed only a small set of
  training examples to tune its one parameter. The description of normalisation
  ("for example by rescaling between the lowest and highest score") is generic
  and carries no citation. Read the full paper before extending the section.
- **Wang et al. (2023a)** is linked from "outputs varied and could contain
  invalid MeSH terms". The link was matched to the reference list by topic; the
  paper was not reread.
- **Cormack, Clarke and Büttcher (2009)** is described from its title.

## Corrections to the review as first reported

Two findings given to the author before the work began were wrong in part.

- It was reported that Chapter 10's RRF conclusions sat in a hand-off paragraph
  "which the digest drops". The digest manifest sets `keep_transition` for
  Chapter 10, so the digest kept them. The points were still moved into the
  summary list, where the other chapters keep theirs; `keep_transition` is left
  set, and the digest now carries the short hand-off.
- It was reported that nothing returns the reader to the five confusions. The
  panel did link the book's closing section. That section does not restate them,
  so the return was added at the end of Part II.

## Open

- **Wiley AI Gateway** (Chapter 8) is described from the author's own Substack
  post and has no evidence-register entry. Adding one needs a vendor source.
- **Table 9.2 sits inside Figure 9.4**, the same double labelling the September
  review removed for Table 9.3.
- **Figures 6.3, 7.4, 8.4, 8.5, 9.1, 9.2 and 9.3** remain raster images. Their
  embedded text is not searchable or translatable. Figures 9.2 and 9.3 label
  the output "Relevance score"; Figure 7.4 says "most relevant passages".
- **Chapter 9's central question** ("How are several retrieval and ranking
  components assembled into a pipeline?") describes Chapters 9 and 10 together
  and does not match the chapter's own three questions.
- **Table 10.1 and Figure 10.2**, and **Table 11.1 and Figure 11.1**, each
  present the same content twice. The September review kept both pairs
  deliberately.
- **The Part II stage strip** files Chapter 8 under "Analysis & execution
  rules", which is Chapter 4's subject.
- The Scopus AI evidence register in Chapter 10 is attached to Figure 10.2's
  title, two paragraphs above the sentence it supports.

## What was checked

- Every replacement was an exact match asserted to occur once; block moves were
  cut and pasted whole.
- `tools/maintain.py`: no problems found. `tools/renumber_footnotes.py`: 56
  footnotes, renumbered once after the Chapter 6 change, then in order.
- `--check` passes for the product-claims, glossary, digest and vendor
  questionnaire builders, as do `check-product-claims.py --as-of 2026-09-19`,
  `test-product-claims.py`, `test-glossary-hub.py`, `test-digest.py` and
  `test-vendor-questionnaire.py`. No product-claim excerpt needed updating.
- The Node browser checks (`check-*.mjs`) were not run; they need Microsoft
  Edge.
- Figures 6.2, 7.5, 7.6, 8.7 and 9.5 were rendered in headless Chromium at
  1,100 pixels wide and inspected. No page errors. Narrow-screen and print
  layouts were not inspected.
- One `id` added (`combining-scores-instead-of-ranks`); none removed except
  those belonging to Figure 8.8 (`fig-8-8`, `paper-as-many-vectors-title`).
- `read-this-first.html` regenerated for the changed Chapter 5, 6 and 10
  summaries.
