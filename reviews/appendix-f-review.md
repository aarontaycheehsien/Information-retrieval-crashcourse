# Appendix F (Evidence synthesis as a high-recall retrieval problem): review

Reviewed 10 November 2026 against commit `a0fb7d0`. The appendix is about 3,870
words with three HTML figures and three tables. Nine findings were reported. A
recheck requested by the author withdrew one and settled two open decisions.
The author then asked for all to be applied.

## What was verified before any change

- **Kempny et al. (2026)**, from the abstract: 35,000 simulations on five
  datasets, a range of 2.9% to 76.9%, and no stop criterion that worked across
  datasets (https://doi.org/10.1186/s12874-026-02866-5).
- **Byrne et al. (2024)**, from the abstract: model choice, and mostly the
  feature extractor, affected how late elusive papers were found
  (https://doi.org/10.1186/s13643-024-02587-0).
- **Repke et al. (2026)**, from the abstract and the first part of the full
  text: 15 stopping methods on 81 datasets; "only one method, CMH, is safe to
  use, but it does not use the full work-saving potential"
  (https://doi.org/10.1002/cesm.70068).
- **The WSS@95 worked example** computes as printed: 0.95 − 0.30 = 0.65.

## Applied

- **A note that preceded its subject.** A boxed note beginning "For the TAR
  comparison", with a second paragraph on a non-coding route, closed the
  section on reproducibility. The comparison it refers to is introduced in the
  next section. The note now closes that section.
- **The deduplication aside.** Figure F.2 shows active learning reordering a
  fixed pool. A boxed aside on deduplication followed it, ahead of the
  paragraph that completes the figure's point. The aside now follows that
  paragraph. It still precedes Figure F.3, so its reference to "the three
  below" holds.
- **The opening.** It named candidate retrieval, prioritisation and stopping as
  "distinct possible recall failures". Figure F.3's three boundaries are
  coverage, retrieval and stopping, and the appendix says prioritisation
  changes order, not membership. The opening now names coverage, says the three
  boundaries can each lose a record, and says prioritisation alone cannot.
- **"Known-item or key-study rules"** is now "Known-study or key-study rules".
  Since the Part III review, "known-item" in this book means a lookup task and
  the recovery check is "known-seed recovery".
- **Anchors.** The four stopping subsections that lacked anchors now have them
  (`stopping-fixed-effort`, `stopping-consecutive-irrelevant`,
  `stopping-known-studies`, `stopping-estimated-recall`).
- **The WSS source.** The link in the text and in the reference list pointed to
  a PDF on a personal university page. Both now use the DOI for Cohen, Hersh,
  Peterson and Yen (2006), https://doi.org/10.1197/jamia.M1929.
- **A long paragraph.** The 230-word paragraph on statistical stopping is split
  in three: the CMH method, the Repke comparison, and other statistical
  approaches. No wording changed.
- **Scope.** The appendix never mentioned screening by large language models.
  One sentence in the opening now says it is left aside, citing Repke et al.
  (2026), who describe it as subject to ongoing research.

Four `id`s were added; none was removed. Word count and the reading-time label
are essentially unchanged.

## Corrections to the review as first reported

- **Withdrawn.** It was reported that the appendix names the one reliable
  stopping method as CMH although the Repke abstract does not. The paper's
  introduction names it. The appendix was correct.
- **Weaker than reported.** The deduplication paragraphs and the TAR-comparison
  note are both boxed asides, not running text, so each interrupted less than
  the first report implied. Both were still moved.

## Limits of what was verified

- The Repke paper was read only as far as its methods section. König et al.,
  the SAFE procedure, the CMH paper, and the sources for Chao-type,
  point-process, decision-theoretic and conclusion-oriented stopping were not
  read.
- The Cochrane Handbook and the ASReview documentation were not rechecked; the
  appendix dates both to August 2026.
- The DOI for Cohen et al. was confirmed in OpenAlex, which gives the year as
  2005; the reference list gives 2006 with volume 13(2), and was left as it is.
- The page was not inspected in a browser.

## What was checked

- Both block moves were cut and pasted whole; every replacement was an exact
  match asserted to occur once, except the WSS link, which was replaced in its
  two known places.
- `tools/maintain.py`, the footnote check, the four builder `--check`s,
  `check-product-claims.py --as-of 2026-09-19` and the four Python test suites
  pass. The Node browser checks were not run.
