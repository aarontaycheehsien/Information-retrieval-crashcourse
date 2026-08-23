# Changelog

Versions of *How Search Decides What You See*. The published page is live, so
this file is what lets a reader — or an instructor who assigned a chapter — tell
which text they were working from.

The version shown in the page header and footer always matches the most recent
entry here.

## Unreleased

### Added

- **The Vector Similarity Lab and a plain-language Chapter 6 explanation.** The
  new interactive companion uses a gentle eight-step tour from a drawable
  two-dimensional toy example to cosine similarity, dot product, normalisation
  and higher-dimensional vectors. Clearly separated off-axis defaults expose a
  cosine/dot-product rank reversal and a negative score, while the lab appendix
  explains how `[x, y]` extends to an n-coordinate embedding without pretending
  that the drawing is an actual semantic model. The resulting score remains
  explicitly separate from relevance and probability. Two new Chapter 6 figures
  make the rank reversal and the extension from two to many dimensions visible
  in the main text. The Preface and Appendix D connect the explanation to the
  book's existing distinctions rather than adding another category.
- **Diversity-aware ranking in Chapters 7 and 11.** A new Chapter 7 section
  explains why a list of individually relevant records can still be
  unhelpfully repetitive, distinguishes MMR, IA-Select, xQuAD and
  determinantal point processes, and locates diversification after candidate
  retrieval rather than treating it as a dense-search method. Chapter 11 adds
  the corresponding evaluation warning and introduces aspect-aware measures
  such as alpha-nDCG.
- **Relevance as a conceptual thread across the textbook.** Chapter 1 now
  separates matching from relevance and the query from the information need;
  brief callbacks connect Boolean retrieval, BM25, embeddings, semantic
  similarity, reranking and OOD transfer; and Chapter 11 develops the fuller
  relevance framework and defines metrics against judged relevance. The thread
  now also reaches Chapter 9: deciding to stop is a relevance judgement made on
  the user's behalf, on results the user never sees, against a criterion no
  interface states.
- **Cognitive relevance (pertinence) as a fourth level**, in both Chapter 1 and
  Chapter 11. Chapter 11's worked example — the same paper being right for a
  specialist, useless to a newcomer and excluded by a reviewer — turns on the
  reader's knowledge in the first two cases and on task criteria only in the
  third, which the previous three-level scheme could not distinguish. Chapter 11
  also now names the affective dimension as the one deliberately left out.
- **Figure 1.5, "From a need to a relevance judgement."** The need-to-judgement
  chain was previously the only titled diagram in the book that was not a
  numbered figure, so it was missing from the figure index and could not be
  cited or reused.
- **Figure 11.1, "Where recall is decided, and where precision is competed
  for."** Chapters 10 to 12 previously carried no figures at all.
- **A fourth "Check yourself" question in Chapter 1**, on what a set of records
  matching every search term does and does not establish. The chapter now
  carries two central distinctions and the existing three questions tested
  neither of the new one.
- **A fourth "Check yourself" question in Chapter 6**, on the cosine/dot-product
  rank reversal, and a matching first point in the chapter summary. The chapter
  now opens with the comparison rule and spends two figures and a lab on it,
  while the existing three questions and five summary points covered none of
  it.
- Glossary entries for relevance, information need, and system/algorithmic,
  topical, cognitive and situational relevance. Only *relevance judgement* was
  defined before, so a reader meeting "situational relevance" had nowhere to
  look it up.
- **Appendix F, “Evidence synthesis as a high-recall retrieval problem.”** A
  dated application of candidate generation, recall, relevance feedback and
  reproducibility to systematic-review retrieval, TAR, ASReview and stopping
  rules. Short cross-references in Chapters 2, 8, 10 and 12 and one compact
  Chapter 11 call-out keep the extended treatment out of the main text.
- **Mechanism-based search guidance in Chapter 8.** A new framework starts
  with what the searcher is supplying—a text string, structured expression,
  citation edge, seed document, relevance judgement, browse target, API
  predicate or agentic brief—before asking how that input should be phrased.
  It also explains why high recall depends on combining methods rather than on
  finding one privileged query style.

### Changed

- **The distinction between vector, dense, learnt and semantic is now example-led.** Chapter 6 builds one vocabulary-aligned representation from binary presence through term frequency, TF–IDF and BM25, while distinguishing Boolean operators from vector overlap and inverted-index execution from the mathematical vector view. Four independent questions then separate numerical form, density, provenance and represented evidence; explicit metadata and learnt sparse retrieval break the shortcut “dense means semantic”. Two supplied figures illustrate the lexical construction and its contrast with dense embeddings, while the Vector Similarity Lab adds two guided-tour steps without changing its scoring controls.
- **Audience and reading-route guidance.** The README, Preface and teaching
  notes now identify information literacy and evidence synthesis librarians as
  the primary audiences, systems/discovery librarians as a secondary audience,
  and Appendix F as core reading for the evidence-synthesis route.
- **The Preface's distinction map is now eight distinctions, not six.** It
  gained *a match is not a relevance judgement* and *the query is not the
  information need*, which had become the book's organising distinctions
  without appearing in the map that collects them. Both are phrased as the
  correction rather than the error, so a reader skimming the list cannot
  mistake the heading for a claim the book endorses.
- **Chapter 1 now cites Mizzaro and Saracevic directly**, rather than
  attributing richer accounts of relevance to unnamed researchers and linking
  them only in Chapter 11 and the further reading. Part I is designed to be
  assignable on its own.

### Fixed

- **"Every stage after the first can improve precision; none of them can
  improve recall" was stated without its boundary condition**, in the body,
  the chapter summary, the self-check answer and the glossary. It contradicted
  Chapter 7, which justifies hybrid retrieval on the grounds that each route
  recovers material the other misses, and Chapter 9, which says iteration
  repairs recall failures as well as compounding them. The rule now names the
  candidate-set boundary rather than a position in a pipeline diagram, and
  Chapter 11 says why fusion over two retrievers and a second agentic round are
  not exceptions to it.
- **"Precision can be repaired by looking further down a list."** Reading
  further down a list normally lowers precision. The passage now contrasts the
  two costs directly: poor precision costs time, which can be spent; poor
  recall costs evidence, which cannot be reached by reading harder.
- Long words in a `.query-flow` step could overflow their box; the steps now
  break words.
- **Chapter 6's stated reading time still described the shorter chapter.** The
  vector-similarity explanation made Chapter 6 the longest chapter in the book
  by prose word count, yet it claimed 21 minutes against Chapter 7's 24 for
  fewer words. It now says 25.
- **The Vector Similarity Lab appendix said cosine "also accounts for the
  vectors' lengths"**, which reads as the opposite of the lab's own "cosine
  compares direction and ignores length". It now says that cosine divides by
  both lengths, matching the wording the guided tour already used.
- The lab's direction control was marked up at 12° while candidate A's
  default relative angle is 24°, so the value shown before the script ran
  disagreed with the drawing.

## Version 1.0 — August 2026

First versioned release. The textbook edition is now the source of truth;
`how-search-decides-what-you-see.html` remains published as the earlier
single-flow article and is frozen.

### Added

- **A Preface, “Why this book exists.”** It explains the gap the book is meant
  to fill, the expertise it assumes from librarians, the choices made about
  mechanism and mathematics, and three routes through the text.
- **Chapter 11, "Measuring whether retrieval worked."** Relevance as a judgement;
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
  (Tables 3.1, 7.2, 8.2, 8.3, 9.3 and Figure 1.1), plus a note in the
  orientation explaining that undated claims are about mechanisms, which move
  far more slowly than the products built on them.
- **A permalink control on every chapter and appendix heading**, so a reading
  list can point at one of them.
- **Nav links on the three application exercises.** Previous/Next previously
  skipped them and dead-ended at the last chapter; the chain now runs unbroken
  from Chapter 1 to the back matter.
- Glossary entries for relevance judgement, precision, recall, precision@k, MRR,
  MAP, nDCG, test collection and pooling.

### Changed

- **Chapter 6 now makes “semantic search is a goal, not an architecture” a main-text distinction.** It separates the capability claim from BM25, ontology or query expansion, dense retrieval and neural reranking; uses Semantic Scholar’s documented keyword-retrieval-plus-reranking pipeline as the counterexample; and leaves the appendix as a terminology reminder rather than the place where the argument is introduced.
- **Appendix E now develops learning to rank and reranking in depth.** It adds
  a scaled toy feature mixture; separates supervision, formulation, objective
  and model; explains click and position bias; distinguishes LTR from a
  reranker; and uses Semantic Scholar's documented 2020 pipeline as a worked
  production example. Chapter 7 and the appendix now cross-link at the points
  where architecture gives way to training and deployment detail.
- **“The retrieval problem” is now Chapter 1.** With the new Preface carrying
  the genuinely prefatory work, the former Introduction now begins Part I.
  The three parts contain four chapters each, and Part I is now titled
  “Retrieval foundations and lexical search.”
- **The Preface now unpacks the “semantic search” label.** A definition callout
  presents it as search by meaning, usually contrasted with lexical search;
  identifies dense retrieval over vector embeddings as the common contemporary
  implementation without treating it as the definition; and links forward to
  the chapters and appendix that develop the distinction. The surrounding text
  names several materially different retrieval pipelines that may sit behind
  the same claim and characterises the post-Transformer period as rapid
  experimentation, while explicitly retaining the standards, benchmarks and
  mature methods that do exist.
- **Chapter 5 split in two.** At 5,469 words it was more than twice the median
  chapter, and it already carried three internal group dividers. It now breaks
  at its own seam into **Chapter 5, "Embeddings and the retrieval encoder"**
  (what a learnt vector is, context, BERT, subword tokenisation, retrieval
  training) and **Chapter 6, "Dense retrieval at collection scale"**
  (bi-encoder deployment, nearest-neighbour indexing, the top-*k* boundary,
  sparse versus dense, and chunking). Roughly 2,750 and 2,850 words. Chapters 6
  to 11 shifted up by one as a result.
- **Chapter ids are now name-based** (`#dense-retrieval` rather than `#ch4`), so
  they survive chapters being inserted, split or reordered. Every old
  `#ch1`–`#ch9` link still resolves to the chapter it originally pointed at.
- **"Implications for library practice and tool evaluation" is now Chapter 12**,
  following the promotion of “The retrieval problem,” the insertion of the
  evaluation chapter and the Chapter 5 split.
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
