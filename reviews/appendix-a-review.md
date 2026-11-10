# Appendix A (The Transformer): review

Reviewed 10 November 2026 against commit `b83e744`. The appendix is about 1,300
words with one HTML figure and one table. Eleven findings were reported; a
recheck requested by the author withdrew one, downgraded three and located
sources for two. The author then asked for all remaining findings to be applied.

## Applied

- **Decoder description.** "Able to see only what it has produced so far" could
  be read as saying the original decoder never sees the source sentence. It now
  says the decoder sees the encoder's reading of the input and, of its own
  output, only what it has produced so far.
- **BERT attribution.** The appendix said a left-to-right model is, "in its
  terms, unnecessarily constrained". The phrase could not be checked against the
  paper from the review environment. The sentence is now a paraphrase that
  claims only what the paper's title and abstract support: that it presents
  reading in both directions as its advantage over left-to-right models.
- **Figure A.1 caption.** It said a model with "only distance or grammar to go
  on could not make the distinction". It now says a rule fixed in advance by
  distance alone would treat both sentences alike.
- **Citations.** T5 and BART are linked and have reference entries (Raffel et
  al., 2019; Lewis et al., 2020). The claim that current embedding models are
  initialised from decoder-style models, which Chapter 5 sends readers here
  for, cites Wang et al. (2024) and BehnamGhader et al. (2024), with reference
  entries.
- **Maximum input length.** One sentence says a model accepts a fixed maximum
  number of tokens and that longer text is cut off or split, alongside
  quadratic cost as a reason for chunking.
- **Takeaway.** A short paragraph before *What this appendix leaves out* gives
  two questions for reading documentation: which strand a named model descends
  from, and what training it then received.
- **Repetition.** The paragraph restating Chapter 5's account of self-supervised
  objectives is cut to two sentences and a link.

Visible words rise from about 1,310 to about 1,415. The reading-time label
(about 6 minutes) is unchanged. No `id` was added or removed.

## Limits of what was verified

- arxiv.org and aclanthology.org were outside the review environment's allowed
  network domains, and a full-text service returned a different paper for the
  BERT DOI. No cited paper was read for this review.
- The four new references were confirmed to exist in OpenAlex, which returned
  the first five authors of each and a count of the rest. The remaining author
  names, and the page range for Lewis et al. (2020), were supplied from memory;
  the author counts match. Check them before release.
- OpenAlex holds T5 as a 2019 preprint. A journal version is believed to exist
  (*Journal of Machine Learning Research*, 2020) but was not confirmed, so the
  preprint is cited.
- Wang et al. (2024) and BehnamGhader et al. (2024) are cited on the strength of
  their titles. The appendix does not describe their methods.
- The statement about a fixed maximum input length is generic and carries no
  citation.

## Corrections to the review as first reported

- **Withdrawn.** "Vaswani and colleagues" was reported as lacking a year. The
  book uses "and colleagues" 29 times and gives a year beside it three times;
  the appendix follows house style.
- **Downgraded.** The decoder sentence was called misleading; in context it was
  ambiguous. Table A.1's "Trained to" column was said to describe BERT rather
  than the encoder half; the column is headed "Half kept" and the caption covers
  it, so nothing was changed. The GPT link was called fragile; it matches the
  reference list.

## What was checked

- Every replacement was an exact match asserted to occur once.
- `tools/maintain.py`, the footnote check, the four builder `--check`s,
  `check-product-claims.py --as-of 2026-09-19` and the four Python test suites
  pass. The Node browser checks were not run, and the page was not inspected in
  a browser.
