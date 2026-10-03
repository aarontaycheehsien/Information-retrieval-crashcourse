# Whole-book consistency review

Reviewed 18 September 2026 on branch `fable-1` against commit `da468c8` (the teaching
notes and labs pass). The findings below **have been applied** to
`search-textbook.html`, `tools/README.md` and `CHANGELOG.md`; the two labs, the
handout, the teaching notes and the README were checked and not changed.

Four passes had edited Parts I–III and the companion files since 12 September. This
review read the parts of the book those passes did not — the Preface (1,807 words),
the seven appendices (17,769), the glossary (81 entries), all 56 footnotes and the
back matter (figures index, *Where to go deeper*, reuse, disclosure, references) —
and ran automated cross-checks over every file: reading-time sums against every
stated total; chapter, appendix and version counts in all eight files; every product
fact and date that appears more than once; all 100 unlinked chapter, appendix,
figure, table and part mentions; the six lists of the book's core distinctions; the
reference list against the sources the text cites, and its alphabetical order; and
the companion files' links into the book.

What holds: every internal and cross-file link resolves; all 100 unlinked mentions
name the right chapter, appendix, figure or table; the Part I, Part II, Chapter 4 and
closing-section distinction lists agree; every repeated product fact (9.4 million and
1,000; 13 and 35,300; 30 and 5; 500; c = 60; k1 = 1.2 and b = 0.75; 413 million;
1,024; the dated documentation checks) is stated the same way everywhere it recurs;
Appendix C's worked BM25 arithmetic re-derives exactly; the labs and teaching notes
match the chapters; the version string is 1.2.1 in every file that carries one.

What did not hold is below. Nothing changes an argument; each item is a statement the
book makes about itself, or a definition, that another part of the book contradicted.

## Findings applied

### 1. The Preface's reading-time totals were stale for Parts II and III

The orientation panel said "about 99 for Part II, and about 76 for Part III". The
Part II divider says 107 and its chapter labels sum to 107; Part III says 82 and sums
to 82. The 9 September review fixed Part I's figure; the other two had moved in 1.2.
Now "about 107 for Part II, and about 82 for Part III".

### 2. Footnote 51 ran a different string from the figure it verifies

The footnote's authoritative tokeniser check used `Unbelievable scenes!`, the pre-1.2
example. Figure B.1 and `tools/wordpiece_example.py` use `Unbelievable rizzlord
scenes!`, chosen because it splits. Both strings in the footnote's code now match.

### 3. The glossary lacked entries the book twice says it holds

The Part III divider says "the glossary holds the short definitions" for five terms,
and *the candidate boundary* had none. Chapter 1's *Seven terms to carry forward*
panel says "The complete glossary is in the end matter", and *Retrieval*, *Candidate
set* and *Generation* had no entry (*Index*, *Ranking* and *Reranking* are covered by
*Inverted index*, *Ranked retrieval* and *Reranker*). Three entries added, in the
glossary's own markup and alphabetical order, worded from the book's own definitions:
*Candidate set / candidate boundary*, *Generation* and *Retrieval*. The page script's
term-mark list is untouched, so no new term marks appear. The teaching notes' "around
eighty short definitions" stays true at 84.

### 4. The glossary's TF-IDF entry contradicted Chapter 3

The entry said "BM25 refines the same two signals, which is why it largely replaced
TF-IDF". Chapter 3 says BM25 "is not a revision of the TF-IDF formula … the
resemblance is convergent, not genealogical", and Chapter 8 repeats the caution. Now:
"BM25 weighs the same two signals, with saturation and length normalisation added,
and has largely replaced TF-IDF for ranked retrieval — though it was not derived from
the TF-IDF formula."

### 5. The reuse section disagreed with the README and the teaching notes

- "Three combinations have been designed to hold together without the rest" listed
  Part I; Chapters 13 and 14; Chapter 15 with Appendix D. The README and the teaching
  notes' audience routes list Part I; Chapters 2, 11 and 13 to 15 with Appendix F for
  evidence synthesis; Chapter 15 with Appendix D. The book's list now matches theirs.
- "Part I alone … ends with the two distinctions it exists to establish" — Chapter 4
  settles one category error and hands the rest to Part II, which is how the teaching
  notes put it. Now "ends by settling the category error it exists to correct".
- The sentence listing what the fuller teaching notes contain omitted their headline
  item since 1.2. It now opens with "a one-hour workshop with a participant handout".

### 6. The reference list did not hold sources the text cites, and was out of order

*Where to go deeper* claimed the list "records every source this book draws on".
Chapter 12 cites the author's "From Fixed Search Workflows to Agentic Academic
Search" and "What Changes When an LLM Agent Searches Your Library Catalogue?" and
Clarivate's April 2026 Research Assistant post as its evidence, none with an entry;
Appendix G's history paragraph cites DrQA, ORQA, REALM, Fusion-in-Decoder and RETRO by
author and year, none with an entry; Rackauckas (2024), named in Appendix G and in
*Where to go deeper*, was absent. Sources cited in full inside footnotes (BioBERT,
PubMedBERT, DSSM and the like) are complete where they stand.

- **Nine entries added**, in the list's style and alphabetical position: Borgeaud
  et al. (2022, RETRO); Chen, Fisch, Weston and Bordes (2017, DrQA); Clarivate (2026b,
  the 9 April blog post, title checked against the live page; the existing Clarivate
  help-centre entry becomes 2026a); Guu et al. (2020, REALM); Izacard and Grave (2021,
  Fusion-in-Decoder); Lee, Chang and Toutanova (2019, ORQA); Rackauckas (2024,
  RAG-Fusion); Tay (2026b, "From Fixed Search Workflows…", with the learning-to-rank
  post relettered 2026c so the same-year titles stay alphabetical); Tay (2026d, "What
  Changes When an LLM Agent…", 24 June). The text cites by link, never by author-year
  label, so the relettering breaks nothing.
- **Nine entries moved** into alphabetical order: Agrawal before Apache Lucene, and
  Apache Lucene after Alammar; Clarke before Cleverdon; Cormack after Cleverdon; Firth
  before Fletcher; Peters before Qin; Robertson and Zaragoza (2009) before Robertson,
  Zaragoza and Taylor (2004); Santos before Saracevic; Weller, Chang et al. before
  Weller, Lawrie and Van Durme. No entry's text changed.
- **The claim softened** to "records the sources cited in the main text; a source cited
  in full inside a footnote is not repeated here."

### 7. Six vague back-references in the appendices and footnotes

The same class the readability passes fixed in the chapters: a pointer that says
"later" or "the section on" without naming where.

| Where | Was | Now |
|---|---|---|
| Appendix A, opening | "the bi-encoders of Chapters 5–8" | "the bi-encoders of Chapters 6 to 8" (Chapter 5 has none) |
| Appendix A, two strands | "the bargain described in the chapter on embeddings" | "… described in Chapter 5" |
| Appendix A, decoder paragraph | "the bidirectional reading described in the section on BERT" | "… described in Chapter 5's section on BERT" |
| Appendix B, opening | "the short account of subword tokenisation given in the main text" | "… given in Chapter 6" (now linked) |
| Footnote 3 | "A later section separates them properly." | "Chapter 12 separates them properly." |
| Footnote 9 | "The later explanation of multi-stage search pipelines … the LLM section" | "Chapter 9's explanation of multi-stage search pipelines … Chapter 9's LLM section" |

Existing links kept; unlinked mentions stay unlinked.

### 8. Two records of how the book is built

- `tools/README.md` gave "Appendix F's section *Applying Chapter 12 to active
  learning*" as its example of a heading that names a chapter; the section is now
  *Applying Chapter 15 to active learning*. Example updated.
- `CHANGELOG.md` had no entry for the five passes on this branch. An `## Unreleased`
  section now summarises them. No version bump: the header, footer, README, notes,
  handout and cite section all say 1.2.1, and that is a release decision.

## Flags for the author, not changed

- **Model-name spelling.** Chapter 1 says Primo Research Assistant's writer is
  "GPT-4.1 Mini"; Table 11.4 says Primo VE NDE Natural Language Search uses "ChatGPT
  4.1 Mini". Different Ex Libris features, possibly different vendor wording; worth
  checking the two documentation pages and using one spelling if they name the same
  model.
- **Generative AI disclosure.** It names "OpenAI's ChatGPT and Codex"; the commits on
  this branch are co-authored by Claude. The wording ("including") is non-exhaustive
  and otherwise accurate; whether to name it is the author's call.
- **CHANGELOG 1.1's "thirteen chapters and six appendices"** is a historical entry,
  left as the 1.2 review decided.

## Checked and consistent

Reading-time sums for all three parts against their dividers; the Part I panel's six
distinctions against the closing section's six and Part II's five; all 100 unlinked
mentions; every "Chapter N" in Appendices D–G; Appendix C's IDF and BM25 values,
re-derived; Appendix B's `ri · ##zz · ##lord` against Chapter 13; Appendix E's PubMed
500 and Semantic Scholar 1,000 against Chapters 3, 7 and 9; Appendix F's "August
2026" practice note against Chapter 14's; Appendix G's chapter attributions; the
glossary's other 80 entries against the chapters (hybrid and multi-stage, RRF, the
two pooling entries, relevance levels, agentic search, top-k, learnt sparse,
normalisation all match); the *Where to go deeper* chapter pointers; the teaching
notes and both labs (previous pass); README counts and version.

## What was checked

- Every edit an exact-match replacement asserted to occur exactly once; glossary and
  reference insertions positional by neighbouring entry; reference moves by sorted
  key, with the multiset of entries asserted unchanged and the file length unchanged.
- `python tools/maintain.py` — "no changes needed", "no problems found".
  `python tools/renumber_footnotes.py` — "already in order (56 footnotes)".
- `node tools/test-labs.cjs` and `node tools/test-vector-tour.cjs` — PASS (labs
  untouched).
- Byte-identical against the pre-edit file: everything from the Part I divider to
  Appendix A's opening paragraph, which covers every chapter, chapter close,
  self-check, application exercise and part divider; and everything before the one
  Preface sentence. `git status` shows only the three intended files changed.
- No in-text author-year label for Clarivate or Tay anywhere before the reference
  list, so the 2026a/b/c/d relettering has nothing to break.
- Rendered check, served locally: the glossary panel holds 84 entries in alphabetical
  order, with the new ones between *BM25* and *Chunk*, *Embedding search* and *Hard
  negative*, and *Result diversification* and *Retrieval control*; the Preface panel
  reads 67, 107 and 82; footnote 51 shows the rizzlord string twice; the reference
  list has 126 entries (117 plus 9) and all sixteen order checks pass; 223 term marks,
  unchanged; no console errors.
- Textbook visible words 97,683 → 98,022 (+339: the nine reference entries, the
  three glossary entries and the fuller sentences).
