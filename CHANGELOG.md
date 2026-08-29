# Changelog

Versions of *How Search Decides What You See*. The published page is live, so
this file is what lets a reader — or an instructor who assigned a chapter — tell
which text they were working from.

The version shown in the page header and footer always matches the most recent
entry here.

## Unreleased

### Added

- **Both part dividers now carry a vocabulary checkpoint.** The book uses the
  device once, well — *Six terms to carry into Chapter 1* — and then never
  again, although the two places a reader most needs it are the part boundaries,
  which are also where the reading times invite them to stop. Part II now opens
  with the five things Part I established that it leans on (analysed term,
  posting list, candidate set, the three separate controls, lexical retrieval)
  and Part III with the five from Part II (embedding, indexed unit, the
  candidate boundary, reranker, hybrid and multi-stage). Each entry says what
  the coming part does with the term rather than only restating the glossary,
  and the panels sit on the same light ground as the Part II pipeline map, for
  the same reason: the coloured band would swallow them.
- **Chapter 13 says which of its three sections is aimed at whom.** Its largest
  section reads as procurement, in a book whose primary audiences are
  information-literacy and evidence-synthesis librarians, and nothing told those
  readers why they were being handed a tender checklist. A short paragraph now
  places the first two sections with anyone who documents or teaches a search,
  and frames the third as the shortest statement in the book of what the
  preceding twelve chapters were for — the point at which every distinction
  drawn becomes something a library can ask for and check.

- **Chapter 5 says in advance that it is the steepest chapter.** Part I stays
  with words a librarian can see on the page; Chapter 5 is where the book stops
  being about words, and it introduces more glossary terms than any other
  chapter. Nothing warned the reader, so a reader who was managing Part I
  comfortably could reasonably conclude at this point that the book had got away
  from them. A "Before you start" panel now names the three things that have to
  survive the chapter — an embedding is learnt rather than calculated, training
  decides what sits near what, and model tokens are not index terms — and,
  equally usefully, the three that can be read once and let go: Word2Vec's
  mechanism, the king − man + woman arithmetic, and the difference between the
  two pretraining objectives. It also points a reader who wants the payoff first
  at Chapter 6's opening.

- **The delulu thread now runs through Chapter 8.** The example runs from the
  Preface through Chapters 2 to 6, disappears for three chapters, and returns in
  Chapter 11 — so the hole in it sat exactly where the machinery is densest, and
  Chapter 8 carried no query example at all. The passage Chapter 5 introduced as
  a *hard negative*, "Ten signs that you performed well in your job interview",
  appeared once in the whole book and was then abandoned, despite being precisely
  the case a cross-encoder exists to catch. The cross-encoder section — the
  chapter's thinnest important section — now works it: the dense retriever of
  Chapter 6 returns a shortlist holding both that passage and the one that
  actually answers the question, they are hard to separate once each has been
  pooled into a single vector, and joint encoding is what weighs *whether the
  expectations are unrealistic* against *you performed well*. Chapter 5's account
  of what training must teach and Chapter 8's account of what reranking must do
  are now the same example.
- **Chapter 9 works its eight query objects against one need.** The chapter's
  thesis — that the object standing for the information need decides which
  mechanism the search addresses, and that phrasing is downstream of both —
  arrived as an eight-row table of abstract categories with no worked instance,
  in the only chapter of Part II with more tables than figures. A new Figure 9.1
  puts all eight against the question behind Puzzle 3, *is there an open access
  citation advantage?*: the typed string, the subject heading, the citation edge,
  the seed review, five marked records, an alert, an OpenAlex API predicate and a
  task brief. Every box is the same need and none is a rephrasing of another,
  which is the claim the table could state but not show. Table 9.1 stays as the
  reference it always was. Chapter 9's reading time moves from 17 to 19 minutes,
  Chapter 8's from 23 to 24, and Part II's stated sitting from 90 to 95.

- **Part II opens with a map of itself.** Every chapter head carries a pipeline
  map showing the stage it covers, but the part divider carried only a blurb, so
  a reader entered the longest stretch in the book — five chapters and about 90
  minutes — with no sense of its shape until they had finished it. The Part II
  divider now carries the same map at part level: which chapter owns which
  stage, with Presentation and the controller marked as Part III's business. The
  map reuses the existing `stage-map` component; the coloured band would have
  swallowed the stage colours, so it sits on its own light panel and the
  existing `.stage` rules then work unchanged.
- **Chapter 8 says what its four questions are before asking them.** At 23
  minutes it is the longest chapter in the book, and it covers five separable
  topics with no waypoint between the opening and the chapter close. A "Before
  you start" panel now names the four questions the chapter answers — why stages
  exist, what a second pass can afford, whether a good list is just a list of
  good items, and what happens when more than one retriever runs — links each to
  the section that answers it, and says that stopping between any two costs the
  reader nothing.
- **The encoder assembly line in Chapter 5 is now a figure.** The seven-step
  path from text to one stored vector was an ASCII chain in a `<pre>` block: the
  summary artefact of the whole chapter, rendered as the least visual element in
  a chapter carrying eight figures. It is now Figure 5.7, built from the same
  `query-flow` component Chapters 1, 4 and 9 use, with the second row picking up
  where the first stops. Its caption names the two boundaries the chapter turns
  on — model tokens never become index terms, and pooling is where the
  per-token detail is spent, which is what late interaction later declines to do.
- **Nine glossary entries for vocabulary Part II depends on.** The glossary and
  the first-use term marks were built around Parts I and III, so the part that
  introduces most of the book's machinery was the thinnest served. The most
  serious gap was that *query understanding*, *query transformation* and
  *retrieval control* — the spine of Chapter 9, set up in Chapter 4, and one of
  the distinctions the book exists to teach — were not defined anywhere a reader
  could look them up. Those three are now entries, along with *latent
  dimension*, *late interaction*, *learnt sparse retrieval*, *hard negative*,
  *blending / routing* and the encoder sense of *pooling*. Seven join the
  `MARKED` list, so they now carry first-use marks in the chapters that use them.

- **Chapter 7 shows the binary vector at collection scale.** The five-step
  lexical progression builds its vectors over a seven-term vocabulary so the
  arithmetic fits on a page, which understates how sparse a real one is. A new
  figure at the end of Step 2 carries the same three documents into a
  2.3-million-term dictionary, where each is a handful of ones in a sea of
  zeros — the reason an inverted index stores only the terms that occur.
  Three superseded draft diagrams that no longer appeared anywhere in the book
  are removed from the same folder.
- **One thread through Word2Vec, BERT and GPT training, in Chapter 5 and
  Appendix A.** The chapter introduced the idea that a corpus supplies its own
  training targets, then dropped it: BERT arrived pretrained “by predicting
  masked tokens” without the book ever saying that this is the same idea in a
  different shape, and GPT was never named in the chapter at all. A new section,
  *What the model was trained to predict*, names the family and the two
  objectives — **masked language modelling** and **next-token prediction** — and
  gives **self-supervised** learning as the umbrella term, a word the book had
  not used anywhere. A new figure shows one sentence hidden three ways, so the
  continuity is visible rather than asserted. The section hands the
  encoder/decoder lineage to Appendix A rather than repeating its table, and
  Appendix A gains the framing it lacked: both strands pretrain without anyone
  labelling anything, and differ only in which part of the text is hidden. Four
  glossary entries and Chapter 5's reading time follow.
- **Where a learnt vector comes from, in Chapter 5.** The opening section of
  the embeddings chapter previously asserted the Part I to Part II break—
  calculated weights giving way to learnt ones—without explaining it. It now
  says where the numbers come from: a BM25 weight can be recomputed by hand
  from a published formula, while an embedding holds neural-network parameters
  settled during training. Because training needs a target and nobody has
  labelled the meaning of every word, the section introduces Firth and the
  distributional hypothesis as the move that supplies one, and presents
  Word2Vec as a model acting on it—with the mechanism delegated to Jay
  Alammar's illustrated walkthrough rather than reproduced. A new section,
  *What the learnt geometry appears to encode*, adds the king−man+woman
  ≈ queen regularity and the country-to-capital offsets as two figures, and a
  footnote records why “appear to” is the right strength of claim: the
  analogy result is normally reported after excluding the input words from the
  candidate set. Firth, Harris, both further Mikolov papers and the three
  analogy-critique papers join the reference list; the licence gains a
  carve-out for the one figure reproduced from a published paper. Five new
  figures carry the argument: where a BM25 weight and an embedding value each
  come from, how a corpus supplies its own training targets, what survives
  when the prediction head is discarded, and the two analogy demonstrations.
  Chapter 5's stated reading time moves from 12 to 17 minutes to match its
  new length.
- **The Vector Similarity Lab and a plain-language Chapter 6 explanation.** The
  new interactive companion uses a gentle five-step tour from a drawable
  two-dimensional toy example through cosine similarity, dot product and
  normalisation to the difference between a score and a relevance judgement. Clearly separated off-axis defaults expose a
  cosine/dot-product rank reversal and a negative score, while the lab appendix
  explains how `[x, y]` extends to an n-coordinate embedding without pretending
  that the drawing is an actual semantic model. The resulting score remains
  explicitly separate from relevance and probability. Two new Chapter 6 figures
  make the rank reversal and the extension from two to many dimensions visible
  in the main text. The Preface and Appendix D connect the explanation to the
  book's existing distinctions rather than adding another category.
- **Diversity-aware ranking in Chapters 8 and 12.** A new Chapter 8 section
  explains why a list of individually relevant records can still be
  unhelpfully repetitive, distinguishes MMR, IA-Select, xQuAD and
  determinantal point processes, and locates diversification after candidate
  retrieval rather than treating it as a dense-search method. Chapter 12 adds
  the corresponding evaluation warning and introduces aspect-aware measures
  such as alpha-nDCG.
- **Relevance as a conceptual thread across the textbook.** Chapter 1 now
  separates matching from relevance and the query from the information need;
  brief callbacks connect Boolean retrieval, BM25, embeddings, semantic
  similarity, reranking and OOD transfer; and Chapter 12 develops the fuller
  relevance framework and defines metrics against judged relevance. The thread
  now also reaches Chapter 10: deciding to stop is a relevance judgement made on
  the user's behalf, on results the user never sees, against a criterion no
  interface states.
- **Cognitive relevance (pertinence) as a fourth level**, in both Chapter 1 and
  Chapter 12. Chapter 12's worked example — the same paper being right for a
  specialist, useless to a newcomer and excluded by a reviewer — turns on the
  reader's knowledge in the first two cases and on task criteria only in the
  third, which the previous three-level scheme could not distinguish. Chapter 12
  also now names the affective dimension as the one deliberately left out.
- **Figure 1.5, "From a need to a relevance judgement."** The need-to-judgement
  chain was previously the only titled diagram in the book that was not a
  numbered figure, so it was missing from the figure index and could not be
  cited or reused.
- **Figure 11.1, "Where recall is decided, and where precision is competed
  for."** Chapters 11 to 13 previously carried no figures at all.
- **A fourth "Check yourself" question in Chapter 1**, on what a set of records
  matching every search term does and does not establish. The chapter now
  carries two central distinctions and the existing three questions tested
  neither of the new one.
- **A "Check yourself" question on the cosine/dot-product rank reversal**, and
  a matching first point in the Chapter 6 summary. The chapter opens with the
  comparison rule and spends two figures and a lab on it, while the existing
  questions and summary points covered none of it. Chapter 6 still ends with
  three questions: the split below moved the full-text one to Chapter 7.
- Glossary entries for relevance, information need, and system/algorithmic,
  topical, cognitive and situational relevance. Only *relevance judgement* was
  defined before, so a reader meeting "situational relevance" had nowhere to
  look it up.
- **A glossary entry for vector normalisation**, distinguished from BM25's
  document-length normalisation. Chapter 6 and the Vector Similarity Lab both
  turn on it — the lab has a control for it — but it was previously defined
  only in passing inside the *dot product* entry. It is deliberately not added
  to the first-use term-mark list, because the book uses "normalisation" in
  both senses.
- **Appendix F, “Evidence synthesis as a high-recall retrieval problem.”** A
  dated application of candidate generation, recall, relevance feedback and
  reproducibility to systematic-review retrieval, TAR, ASReview and stopping
  rules. Short cross-references in Chapters 2, 9, 11 and 13 and one compact
  Chapter 12 call-out keep the extended treatment out of the main text.
- **Mechanism-based search guidance in Chapter 9.** A new framework starts
  with what the searcher is supplying—a text string, structured expression,
  citation edge, seed document, relevance judgement, browse target, API
  predicate or agentic brief—before asking how that input should be phrased.
  It also explains why high recall depends on combining methods rather than on
  finding one privileged query style.

### Changed

- **The Vector Similarity Lab shows its arithmetic, and its tour is five steps
  rather than eight.** Two of the eight steps were the only ones whose controls
  did nothing: they displayed a static figure and asked a question the arrows on
  screen could not answer, so a reader trained for four steps to read the plot
  found it suddenly decorative. Both belong to what is now Chapter 7, which
  makes their point with figures of its own. A third step, on extending `[x, y]`
  to *n* coordinates, was already said twice more — verbatim in the lab appendix
  below it, and again as Figure 6.2. Every remaining step moves the arrows.
- **The lab substitutes the live numbers into the formulas**, under the plot,
  for whichever candidate is selected: the two vectors as coordinates, the dot
  product as the sum of its coordinate products, and cosine as that total
  divided by both lengths, with the line for the active rule picked out. The
  normalisation step previously asserted that cosine's denominator becomes one;
  it now reads `cos = 0.914 ÷ (1.00 × 1.00) ≈ 0.914` while the reader watches.
  Rounded results are marked `≈`, as the lab's worked example already did.
- **In guided-tour mode the question now sits beside the evidence.** The tour
  card used to span the full width above a three-column instrument, so on a
  1400-pixel screen the plot a step asked about was below the fold. Above 1180
  pixels the card moves into a column of its own alongside the plot and the
  ranked list, and the controls — which the tour sets rather than the reader —
  move beneath them. Sandbox mode and every narrower layout are unchanged.

- **Chapter 6 is now two chapters.** The vector-similarity work had made it
  the longest chapter in the book at roughly 5,400 words — twice any chapter
  in Part I — carrying nine sections and two distinct arguments. It splits
  along the seam that was already there. Chapter 6, *Dense retrieval at
  collection scale*, keeps the scale-and-pipeline argument: the comparison
  rule, nearest-neighbour indexing, candidate boundaries, top-*k*, and the
  Puzzle 3 resolution that now closes it. A new **Chapter 7, *Representations
  and indexed units***, takes what had been appended to that argument rather
  than belonging to it: the lexical vector built one decision at a time from
  binary presence to BM25, the four questions separating numerical form,
  shape, provenance and evidence, and the distinction between a source
  document, an indexed unit and a vector. Each chapter carries its own central
  question, summary and questions, and they come to about 16 and 13 minutes —
  back in line with the rest of the book. No prose was rewritten to make the
  cut; the two halves shared no cross-references.
- **Chapters 7 to 12 are now Chapters 8 to 13**, and Part II runs from Chapter
  5 to Chapter 9. Every saved chapter link still resolves: chapter anchors are
  slugs rather than numbers, so `#dense-at-scale`, `#reranking-and-hybrid` and
  the rest are unchanged, as are the `#ch1`–`#ch9` anchors held over from the
  earlier single-flow edition. Figure and table numbers do move — what was
  Figure 6.6 is Figure 7.1, and the assets in Chapters 8 to 13 shift with their
  chapters — so a link saved to a specific figure or table may now land on a
  different one. The teaching notes' twelve-week course becomes a
  thirteen-week course.

- **The distinction between vector, dense, learnt and semantic is now example-led.** Chapter 7 builds one vocabulary-aligned representation from binary presence through term frequency, TF–IDF and BM25, while distinguishing Boolean operators from vector overlap and inverted-index execution from the mathematical vector view. Four independent questions then separate numerical form, density, provenance and represented evidence; explicit metadata and learnt sparse retrieval break the shortcut “dense means semantic”. Two supplied figures illustrate the lexical construction and its contrast with dense embeddings.
- **Chapter 6 now ends on the puzzle it opened with.** The two qualification
  sections — a vector need not be dense or semantic, and one document is not
  one vector — used to follow the Puzzle 3 resolution, so the chapter's
  heaviest passage, the binary-presence to TF to TF–IDF to BM25 progression,
  arrived after its own payoff. They now come before it and Puzzle 3 closes
  the chapter. The "Two qualifications the basic model needs" divider is gone
  with them: sitting in the chapter's natural order, the two sections no
  longer need announcing. No prose changed. Those two sections then became a
  chapter of their own — see below.
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
  them only in Chapter 12 and the further reading. Part I is designed to be
  assignable on its own.

### Fixed

- **The final chapter had the thinnest summary in the book.** Chapter 13 closed
  on four points where every other chapter offers five to ten, and none of them
  covered its longest section. Two more now do: that documentation and
  inspection cannot be retrofitted, which is why they are procurement questions
  rather than support tickets, and that separating a retrieval design from a
  marketing label needs no mathematics, only the distinctions the book has drawn.

- **The eight distinctions arrived about an hour before they could be read.**
  Five of the eight turn on *vector*, *embedding*, *dense*, *top-k* and
  *neural* — words the book does not introduce until Part II — yet the panel
  sits eight minutes into a Preface that has just promised no prior knowledge is
  assumed. It now says so: several will mean nothing yet, that is the intended
  state, and the panel is a checklist to return to rather than a prerequisite
  for starting.
- **One panel entry sent a beginner ninety minutes forward.** *The query is not
  the information need* linked only to Chapter 9's account of choosing a query
  object. Chapter 1 states the distinction itself, thirteen minutes away. It now
  links there first, and to Chapter 9 for what follows from it.
- **The "for awareness" escape hatch did not exist where it was promised.** The
  Preface offered it as though main-text sections carried the marker; both
  marked sections are in appendices, which the same sentence already makes
  optional. The sentence now describes what is actually there.
- **The currency warning omitted the chapter that ages fastest.** It named
  Chapters 3, 8, 9 and 10, while Chapter 6 carries the most dated product
  material in the book — Semantic Scholar's 2025 pipeline, OpenAlex Alice's
  February 2026 arrival and April 2026 documentation, and the August 2026 result
  counts. Chapter 1 and Appendix F were missing too. All are now listed.
- **A cross-reference named the wrong table.** Chapter 11's *Diagnose before
  choosing a remedy* pointed at Table 10.1, which is the control-arrangement
  table; the diagnostic map with the remedy column is Table 11.1. It is now a
  link as well as a correction, which puts it inside the set `maintain.py`
  checks rather than the unlinked prose it cannot see.

- **Four reading times no reading rate could reconcile.** Measured as visible
  chapter text excluding self-check answers, the book's stated times are
  consistent at about 192 words a minute — every chapter but four sits within a
  minute and a half of that. The Preface claimed 7 minutes for 2,377 words,
  which needs 340 words a minute; Chapter 12 claimed 17 for 3,831 words while
  Chapter 5 claimed 19 for 3,780; Appendix E ran slow and Appendix F badly fast.
  They now read 12, 20, 19 and 29. The Preface's own "three sittings" sentence
  and the Part I divider follow, at about 60 minutes.
- **The page scrolled sideways on a narrow phone.** The suggested citation ends
  in a bare URL, which is a single unbreakable token, and it pushed the whole
  document 15 to 35 pixels wide below about 400px. It now breaks. The pipeline
  map's stage boxes and the Copy link button spilled their rows at 320px, for
  the same reason a grid item will not shrink below its own content: both can
  now wrap. A 20px residue remains at 320px exactly, not traced to any element.
- **Sixteen straight quotes and apostrophes in prose**, where the rest of the
  book uses typographic ones — mostly possessives (CDI's, the model's, the
  searcher's) and two quoted phrases in Chapter 8.
- **"Four in Chapter 1" undercounted the self-checks.** Chapters 9 and 10 also
  carry four questions rather than three. The README and the teaching notes both
  said otherwise, and both now name all three chapters.
- **The teaching notes' part word counts were measured loosely.** Now 18,000 for
  Part II against 8,400 for Part I and 14,600 for Part III, on the same
  self-checks-excluded basis as the reading times.

- **The glossary defined the wrong sense of *pooling*.** Its single entry gave
  the Chapter 12 sense — judging only what several systems ranked highly, so a
  test collection stays affordable — while Part II uses the word about
  twenty-two times for the encoder step that turns contextual token
  representations into one vector, and Chapter 5 makes that step load-bearing. A
  reader who looked it up was misled rather than merely unhelped. There are now
  two entries, *Pooling (encoder)* and *Pooling (test collections)*, each
  pointing at the other.
- ***Latent* was used nine times and never defined.** Its first appearance was a
  Chapter 7 figure caption, which is also where a skim-reader lands first, and
  Chapters 5 and 6 never use the word at all. A short paragraph now introduces
  latent dimensions before the figure that contrasts them with vocabulary
  dimensions, which the figure had been left to do on its own.
- **Chapter 7's five-step build could not be navigated or linked.** Steps 1 to 5
  and the four questions that follow them were `<h4>` elements without ids, and
  `tools/maintain.py` builds both tables of contents from `<h3>` headings that
  carry one. The chapter therefore offered two contents rows for nearly 3,000
  words, and no single step of the progression it exists to teach — binary
  presence through TF, TF–IDF and BM25 — could be deep-linked or assigned. All
  seven are now `<h3>` with ids, taking Chapter 7 from two contents rows to nine.
- **The teaching notes understated Part II by about 6,000 words.** They put the
  heaviest fortnight at "roughly 11,000 words", a figure that appears to predate
  the Chapter 5 expansion recorded above; Part III was above it too. The note now
  gives all three parts, so the comparison an instructor is actually making is
  visible: about 17,700 words against 8,800 for Part I and 14,000 for Part III.

- **"Every stage after the first can improve precision; none of them can
  improve recall" was stated without its boundary condition**, in the body,
  the chapter summary, the self-check answer and the glossary. It contradicted
  Chapter 8, which justifies hybrid retrieval on the grounds that each route
  recovers material the other misses, and Chapter 10, which says iteration
  repairs recall failures as well as compounding them. The rule now names the
  candidate-set boundary rather than a position in a pipeline diagram, and
  Chapter 12 says why fusion over two retrievers and a second agentic round are
  not exceptions to it.
- **"Precision can be repaired by looking further down a list."** Reading
  further down a list normally lowers precision. The passage now contrasts the
  two costs directly: poor precision costs time, which can be spent; poor
  recall costs evidence, which cannot be reached by reading harder.
- Long words in a `.query-flow` step could overflow their box; the steps now
  break words.
- **Chapter 6's stated reading time still described the shorter chapter.** The
  vector-similarity explanation made Chapter 6 the longest chapter in the book
  by prose word count, yet it claimed 21 minutes against Chapter 8's 24 for
  fewer words. It now says 16, the split below having taken about 2,200 words
  out of it.
- **The Vector Similarity Lab appendix said cosine "also accounts for the
  vectors' lengths"**, which reads as the opposite of the lab's own "cosine
  compares direction and ignores length". It now says that cosine divides by
  both lengths, matching the wording the guided tour already used.
- The lab's direction control was marked up at 12° while candidate A's
  default relative angle is 24°, so the value shown before the script ran
  disagreed with the drawing.
- **The lab's direction control stopped at ±160°**, so the −1 cosine endpoint
  described in its own appendix — and in the glossary — could not actually be
  reached in the sandbox. It now runs to ±180°, and the control hint says what
  happens there rather than hedging.

### Removed

- **The earlier single-flow web article has been retired.** Its former public
  URL now redirects to the textbook, preserving shared fragment links; the
  article itself remains available through Git history.

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
