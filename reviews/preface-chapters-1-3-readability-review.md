# Preface and Chapters 1–3: second readability pass

Reviewed 24 September 2026 against commit `6476dee`. The findings below **have
been applied** in commits `220a400` (Preface), `8a484f3` and `6c206bd`
(Chapter 1 and evidence-register labels), `aaa4dc0` (Chapter 2) and `ef2a1b1`
(Chapter 3).

The brief was readability with the content held fixed. The earlier pass
(`part-i-readability-review.md`) had fixed the large placement problems. What
remained was repetition in sequence, stacked closing paragraphs, stub sections,
and hedges that ended paragraphs on a qualification.

## Applied

### Preface

- **P1.** "Before you start" and "How to read this" were two orientation blocks
  back to back. The 45-minute route is now the first of the shorter routes.
- **P2.** The routes list now says "five shorter routes" and leads with the
  short orientation.
- **P3.** "Three things this book is not" was one semicolon sentence. It is now
  a list, and the RAG scope note moved into it from the end of the reading
  guide.
- **P4.** "Six of these confusions" named none. One example is given, with a
  link to the Part I checklist.

### Chapter 1

- **C1.** "Read that list again" now ends on its point, with the
  cost-and-importance qualification moved earlier. The "Strip away the product
  names" paragraph no longer restates Table 1.1's mapping. Inline dates were
  removed from the list lead-in and table header; the chapter's dated note
  still covers them.
- **C2.** The chapter's missing-evidence paragraph no longer repeats the
  preface's fabricated-citation sentence. The LLM panel no longer repeats the
  RAG definition's Appendix G sentence.
- **C3.** The Primo five-source paragraph moved up beside the
  `AI academic libraries` example, so "Keep that in mind for fourteen chapters"
  closes the relevance section.
- **C4.** The three puzzles were stated four times in a row. The "Keep these
  questions open" panel and the first map paragraph are now Table 1.2 (question,
  tempting mistake, where it is taken up). The text names Puzzles 1 and 2 as the
  shared mistake. The table's link targets were checked against Chapter 4:
  Puzzles 1 and 2 are settled there, and Puzzle 3 waits for Part II and
  Chapter 7. The `opening-puzzles-title` id is kept as a legacy anchor.
- **C5.** Evidence registers: claim locations were moved beside the passages
  they support (Puzzle 2 and 3 claims, the Scopus 2024 account, and a new
  `#puzzles-under-answer-layers` anchor). `tools/product_claims.py` now prefixes
  each register link with product and mode, because many claims share wording
  ("Figure 1.3 places this mode in quick search" appeared five times). It also
  pluralises the count.

### Chapter 2

- **C6.** The inverted-index stub heading is kept, since many links and the
  register's book locations cite it. Its dead-end sentence is now a roadmap of
  the five sections that build the index. The duplicate bridge above it and the
  "In practice" panel's section roadmap were removed.
- **C7.** Removed the sentence restating the one before it; the definition of
  *eligible* is kept.
- **C8.** "Compatibility matters" points to Figure 2.2 for the mismatch example
  and keeps its collection-statistics point.
- **C9.** The full-text search panel moved beside the term-first map section,
  so the sets, speed and bridge sequence is no longer interrupted before the
  chapter close.

### Chapter 3

- **C10.** Three TF-IDF paragraphs are now one, with the historical caution kept
  as a parenthesis. The "four observable things" preview moved into the list
  lead-in. The pull quote keeps only the not-relevance point.
- **C11.** The dangling "But how much should it be?" is rewritten as a
  statement defining term saturation.
- **C12.** PubMed's BM25-plus-learning-to-rank architecture is stated once, in
  the academic-search section. The `pubmed-bm25` register location at the
  opening section was removed, and three other excerpts were updated.
- **C13.** The academic-search section has a lead-in sentence before its first
  figure.
- **C14.** MaxScore, WAND and Block-Max WAND are named only at the Appendix C
  pointer.
- **Chapter close.** "BM25 is a first-stage ranker in production library and
  scholarly systems" claimed more than the body. It now says that PubMed
  documents BM25 in Best Match and that other systems document lexical evidence.

## Verification

- All Python checks pass: `build-product-claims.py --check`,
  `build-glossary-hub.py --check`, `build-digest.py --check`,
  `check-product-claims.py --as-of 2026-09-19`, and the product-claims, digest
  and glossary test suites. `maintain.py` found no problems.
- The Playwright checks pass: `check-product-claims.mjs`, `check-digest.mjs`
  and `check-glossary-hub.mjs`.
- Rendered page: no console errors and no broken internal links. There are 224
  `.term-mark`s in total, the same as before. Chapter 1 lost the
  *retrieval-augmented generation* first-use mark with the removed Appendix G
  sentence; the key-definition box still defines it. The Preface gained a
  *dense retrieval* mark from P4.

## Noted, not changed

- At a 1280px viewport, 48 of 49 tables overflow by 28px. The global rule
  `table { min-width: 620px }` is wider than the 592px text column. This was
  true before this pass.
