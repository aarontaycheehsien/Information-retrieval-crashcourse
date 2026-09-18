# Part III (Chapters 12–15): readability and consistency review

Reviewed 18 September 2026 on branch `fable-1` against commit `367a517` (the Part II
pass). The findings below **have been applied** to `search-textbook.html`; locations
name section anchors.

The brief was the same as the Part I and Part II passes — readability with the
content held fixed — plus an explicit check that Part III stays consistent with
Parts I–II and the two labs. Part III had been reviewed twice already
(`part-iii-review.md`, `part-iii-review-2.md`) and every finding in both is applied;
the one readability pass attempted on it (`6f95554`) was reverted. So this is the
first readability pass Part III has actually kept.

Consistency was checked from the anchors outward: 88 Part III ids; no links between
Part III and either lab in either direction; seven from the teaching notes (the
one-hour workshop targets Chapter 13's diagnosis sections, Chapter 15 and Exercise
III); about forty from the appendices and back matter; thirty from Parts I–II. None
of those ids changed. Every Part II claim Part III leans on — pseudo-relevance
feedback as a fixed two-pass workflow, Scopus AI routing, the Wiley chunk unit, the
Primo 30-candidate and 5-abstract budgets, Chapter 9's note that ColBERT and learnt
sparse retrieval can be first-stage, Chapter 4's four explanations for a missing typed
word — was re-read against its source and agrees.

Constraints kept: no `id` added, removed or renamed; figures, tables, footnotes and
reading-time labels unchanged; the exempt zones (self-checks, chapter closes
including Chapter 12's ten-bullet close, glossary, footnotes, all three exercises)
byte-identical; the front matter, Part I, the appendices onward, both labs and the
teaching notes byte-identical. Part II differs by exactly one tag pair (finding 1).

## Consistency findings applied

### 1. A correction to the Part II pass: Chapter 11's heading is an `<h5>` again

The Part II plan called `#natural-language-filter-extraction-is-useful-but-limited`
"the only h5 in the book's chapters" and promoted it to h4. The premise was wrong.
The stylesheet defines `.chapter h5` as the "fourth-level prose heading, created by
demoting old in-flow h4s", and it is used that way by Chapter 15's six
procurement-question groups and seven headings in Appendices C and D, all directly
under an h3 as Chapter 11's was. **Applied:** the `<h5>` is restored; it renders at the
same size as Chapter 15's six (checked in the browser), and those six are left as they
are. Chapter 6's three added h4s stay: they follow the in-flow, linkable h4 pattern of
`#when-a-system-writes-the-boolean-query` and mark subsections, not group labels.

### 2. Chapter 14 never pointed at the lab built to demonstrate its central claim

The 1.2 changelog records that the BM25 Evidence Lab's candidate-limit slider was
added because "the claim the book turns on had no interactive demonstration
anywhere"; its seventh tour step, *The boundary that scoring cannot cross*, is
Figures 14.1 and 14.2 made interactive. Nothing in Part III linked to either lab.
**Applied:** one sentence after Figure 14.2, linked to the lab: "The BM25 Evidence
Lab's tour step *The boundary that scoring cannot cross* makes this concrete with six
records: set k to one and ask what any later stage could do for the record just below
the line."

### 3. Chapter 13's "matched but hidden" check has a lab demonstration it did not name

The Vector Similarity Lab's optional experiment — *Can the relevant record reach the
next stage?* — applies two metadata filters before or after the top-k cut-off, which
is exactly the pre-check's second question. **Applied:** one sentence at the end of
that bullet, linked to the lab.

### 4. The closing puzzle map's link texts

"Where it was left" (twice, to Chapter 4's verdicts) and "How it was traced" (to
Chapter 7's Puzzle 3 section) were the last links in the book whose text did not say
where they went. **Applied:** "Chapter 4's verdict" and "Chapter 7's account"; hrefs
unchanged.

### 5. Chapter 12's "the opening diagram" named no figure

Two links to the Figure 1.3 caption read "opening diagram". **Applied:** "Figure 1.3",
now pointing at the asset anchor `#fig-1-3`, which is what the maintenance pass
verifies figure references against.

### 6. Four other back-references that did not say where they go

| Where | Was | Now |
|---|---|---|
| Ch 13, vocabulary mismatch | "The earlier `delulu` example…" (unlinked) | "Chapter 6's `delulu` example…", linked to Chapter 6's worked training example |
| Ch 13, OOV | "The earlier sections on index analysis, word and subword tokenisation and the difference between model tokens and indexed terms explain why." | "Chapter 2's index analysis and Chapter 6's account of word and subword tokenisation, and of the difference between model tokens and indexed terms, explain why." (same three hrefs) |
| Ch 14, test collections | "the BEIR result cited when OOD transfer was introduced" | "…cited in Chapter 13 when OOD transfer was introduced" |
| Ch 14, test collections | "the argument already made about training data" (unlinked) | "Chapter 6's argument about training data", linked to *Where the training signal comes from* |

## Placement and duplication

### 7. Chapter 15: a colon that promised a table, then a panel

"At minimum, a record should cover four areas of the pipeline:" was followed by the
*Start with a record you can make today* box and only then by Table 15.1. **Applied:**
the box now precedes the sentence; the table follows its colon.

### 8. Chapter 14: a disambiguation clause split the definition of pooling

The 57-word sentence "…so evaluations instead use pooling — a different operation
from the pooling that compresses token representations into one vector in Chapter 5:
run many different systems…" now defines pooling in one sentence and states the
disambiguation in the next.

### 9. Chapter 12, *What the loop is for*: two overloaded paragraphs

The experiment paragraph (setup, citation, two limits, four worked examples and the
`refinituv` caveat) is split before the examples; the qualifications paragraph is
split before "This is the strongest evidence in the book…". No words changed.

### 10. Chapter 13: a two-line blockquote saying one thing twice

"A learnt retriever may transfer its operational model of relevance badly." /
"OOD is the question of whether what was learnt travels to this retrieval
situation." **Applied:** one line, joined with a colon.

### 11. Two captions that repeated the adjacent body

Figure 12.2's closing sentence restated the chapter's "iteration is not agency"
refrain (stated three times in the body) and was off the figure's subject; dropped.
Figure 14.2's opening sentence repeated the body's "The rule names a boundary, not a
position in a pipeline diagram" from one paragraph above; dropped, keeping the
sentence that adds the fusion-fed-by-two example.

## Sentence-level

- **Chapter 12:** the 48-word stopping-rule sentence splits after the harness list;
  the 45-word Web of Science approval-gate sentence splits into two, with the second
  quotation kept intact ("The post adds that 'the search runs only after the user
  reviews and approves the strategy.'"); the label-and-mechanism sentence splits
  before the Consensus example; "made little difference in these examples; this does
  not establish…" and "…recover when the query is poor — which is a different
  property…" each become two sentences.
- **Chapter 14:** "Note what the averages do…" (44 words) is three sentences; the
  per-query sentence (42 words) splits at its semicolon.
- **Closing section:** the Preface-test sentence is a statement and a question; the
  84-word six-collapse sentence keeps its shape but separates the six "why" clauses
  with semicolons and sets off the consequence with a dash.

## Considered and not applied

- **Chapter 12's length** (5,338 words, the book's longest): its long sections are
  narrative; the paragraph splits are the right grain and no subheadings were added.
- **"Iteration is not agency"** in the body, the close and the self-checks: the
  chapter's thesis. Only the off-subject caption instance went.
- **The faithful-trace refrain in Chapter 15** and the "loss function" line in
  Chapters 14 and 15: signature phrasing, two instances in exempt zones.
- **Chapter 14's mirror of Exercise III's judging protocol**: deliberate (1.2.1) and
  the chapter says so.
- **The closing section's two catalogue sentences** (51 and 43 words): lists of the
  book's machinery, read as lists.
- **Chapter 13 without a figure**: declined in the 1.2 review; Figure 13.1 has since
  been added anyway.
- **Chapter 15's six h5 headings**: the book's convention (finding 1).
- **CHANGELOG.md** untouched across all three passes; a release decision.

## What was checked

- Twenty-seven edits, each an exact-match replacement asserted to occur once (the
  closing-map link exactly twice), plus one positional block move and one positional
  insertion.
- `python tools/maintain.py` — "no changes needed", "no problems found"; the renamed
  links and the `#fig-1-3` references pass the stale-cross-reference check.
- `python tools/renumber_footnotes.py` — "already in order (56 footnotes)".
- `node tools/test-labs.cjs` and `node tools/test-vector-tour.cjs` — both PASS (labs
  not edited).
- Byte-identical against the pre-edit file: all 15 chapter closes, 15 self-checks,
  the three exercises, the glossary and the footnotes section (35 blocks); the front
  matter and Part I; the appendices onward. Part II differs by the one `<h5>` tag
  pair. `git status` shows only the textbook and this file.
- Ids 606 → 606; every internal `href` resolves; figure, caption, pull-quote,
  blockquote, chapter-close, self-check and footnote-reference counts unchanged; h5
  count 13 → 14.
- Rendered page, served locally: Chapter 11's heading renders as an h5 at the same
  size and weight as Chapter 15's six (15.68px/800); the practical-record box is the
  element before "At minimum…" and Table 15.1's label the element after; the pooling
  paragraph ends on the Chapter 5 disambiguation; the closing map's three links read
  "Chapter 4's verdict" / "Chapter 7's account" with their hrefs intact; the two lab
  links resolve; both Figure 1.3 links render; Figure 14.2 is followed by the lab
  pointer; no console errors. Term marks 223 in the book before and after, and per
  chapter 12 / 14 / 18 / 8 for Chapters 12–15 before and after.
- Visible words in Part III: 18,976 → 19,010 (+34, the two lab pointers). No
  reading-time label moves.
