# Changelog

Versions of *How Search Decides What You See*. The published page is live, so
this file is what lets a reader — or an instructor who assigned a chapter — tell
which text they were working from.

The version shown in the page header and footer always matches the most recent
entry here.

## Version 1.0 — August 2026

First versioned release. The textbook edition is now the source of truth;
`how-search-decides-what-you-see.html` remains published as the earlier
single-flow article and is frozen.

### Added

- **Chapter 10, "Measuring whether retrieval worked."** Relevance as a judgement;
  precision and recall and the trade between them; precision@k, MRR, MAP and
  nDCG; test collections, pooling and what a benchmark number is worth; how to
  build a local evaluation set; what a number cannot settle.
- **Appendix D, Table D.4, "Evaluation and performance claims"** — retrieval
  measures, judgements and test collections, benchmarks and transfer, and
  comparative claims — plus a seventh misleading overlap, "'State of the art'
  names a benchmark, not a capability."
- **Licence, suggested citation and reuse guidance**, as a new back-matter
  section and a `LICENSE` file. The book is CC BY 4.0; third-party screenshots
  and trademarks are excluded and flagged as such.
- **Three "Check yourself" questions at the end of every chapter** — 36 in all,
  answers hidden in a `<details>` until clicked. They are discrimination
  questions rather than recall: one on the chapter's central distinction, one
  scenario to classify, one to put to a vendor. Note that printing a chapter
  reveals the answers, by the same rule that stops any collapsed content being
  lost on paper.
- **Teaching notes** (`teaching-notes.html`) — three course shapes, what a
  strong answer to each application exercise contains and the common wrong
  turns, discussion prompts per part, guidance on reusing the figures, and the
  list of product claims to re-verify before teaching.
- **"Where to go deeper"** — a dozen entry points for further reading grouped
  by what you would be trying to learn, all drawn from sources already cited.
- **Date stamps on every claim about how a named product currently works**
  (Tables 2.1, 6.2, 7.2, 7.3, 8.3 and Figure 0.1), plus a note in the
  orientation explaining that undated claims are about mechanisms, which move
  far more slowly than the products built on them.
- **A permalink control on every chapter and appendix heading**, so a reading
  list can point at one of them.
- **Nav links on the three application exercises.** Previous/Next previously
  skipped them and dead-ended at the last chapter; the chain now runs unbroken
  from the introduction to the back matter.
- Glossary entries for relevance judgement, precision, recall, precision@k, MRR,
  MAP, nDCG, test collection and pooling.

### Changed

- **Chapter 4 split in two.** At 5,469 words it was more than twice the median
  chapter, and it already carried three internal group dividers. It now breaks
  at its own seam into **Chapter 4, "Embeddings and the retrieval encoder"**
  (what a learnt vector is, context, BERT, subword tokenisation, retrieval
  training) and **Chapter 5, "Dense retrieval at collection scale"**
  (bi-encoder deployment, nearest-neighbour indexing, the top-*k* boundary,
  sparse versus dense, and chunking). Roughly 2,750 and 2,850 words. Chapters 5
  to 10 shifted up by one as a result.
- **Chapter ids are now name-based** (`#dense-retrieval` rather than `#ch4`), so
  they survive chapters being inserted, split or reordered. Every old
  `#ch1`–`#ch9` link still resolves to the chapter it originally pointed at.
- **"Implications for library practice and tool evaluation" is now Chapter 11**,
  following the insertion of the evaluation chapter and the Chapter 4 split.
  Its tables renumbered accordingly.
- **Heading levels made consistent.** Twenty-one section headings that were
  marked up below their true level are now in both tables of contents —
  including *Cross-encoder reranking*, *LLMs as rerankers* and *Where
  ColBERT-style late interaction fits*, which were previously unreachable from
  the contents list. Nine genuinely nested headings moved down a level.
- Application exercise III gained a measurement step and now references the
  renumbered chapters.
- The reranking and diagnosis chapters gained forward pointers into the new
  evaluation chapter, and the diagnosis chapter's closing transition no longer
  describes the one after it as the final chapter.

### Fixed

- The page footer described the book as "generated from the single-flow web
  article." That pipeline was retired in August 2026 and the two texts have
  diverged.
- The header described the book as having nine chapters.
