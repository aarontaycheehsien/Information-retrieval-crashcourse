# Teaching notes, handout and labs: readability and consistency review

Reviewed 18 September 2026 on branch `fable-1` against commit `dee1984` (the Part III
pass). The findings below **have been applied** to `teaching-notes.html` and
`vector-similarity-lab.html`; the handout, the BM25 Evidence Lab, the README and the
textbook were checked and not changed.

Three readability passes had changed the textbook since 12 September, when the
changelog last synchronised the lab tour counts and timings, so the companion files
were checked against the book as it now stands. The cross-file plumbing is sound:
all 25 links from the notes, handout, labs and README into the textbook resolve;
every link text that names a chapter or appendix matches its target's chapter; the
eleven links from the textbook out to the companions, and the five between them,
resolve. The labs' seven-step tours match Chapter 3's "seven-step guided tour" and
the notes' "seven prediction steps"; the notes' account of the BM25 lab's sixth step
(the candidate-limit slider) and seventh (vocabulary and admission) matches the lab;
the vector lab's defaults and cosine values (0.914, 0.574) match Figure 7.1's
corrected caption; the rubric is the eight-point one the README promises; and the
exercise protocols in the notes match Exercises I–III in the book.

What was inconsistent was small and sat in the teaching notes: one stale figure and
table number, two claims about the book that are not true of it, and a
re-verification table missing the book's newest dated product claim.

## Teaching notes — consistency findings applied

### 1. Stale figure and table numbers in the re-verification table

The Primo Research Assistant row cited **Table 9.2, Figure 9.5** — the MaxSim example
and the pointwise/pairwise/listwise diagram. The Primo trace is **Table 9.3 and
Figure 9.7**, the same stale number the Part II pass corrected in Chapter 9's prose.
**Applied.**

### 2. The table omitted the book's newest dated product claim

Chapter 12 now places Web of Science Research Assistant from Clarivate's April 2026
post ("fully agentic", with an approval gate before retrieval), added on 11
September; it is exactly the kind of claim the table exists to re-check. **Applied:**
a ninth row after Table 12.3's — Chapter 12 · Web of Science Research Assistant
described as fully agentic, with an approval gate before retrieval · April 2026 ·
"A later post naming the routes, or the approval gate being removed or made
optional". The thirteen-week course now assigns "nine items".

### 3. "Documented as of" left blank where the book states the date

Two rows were prefilled and the book states dates for four more. **Applied:** Primo
"August 2026 (Table 9.3); September 2026 (Chapter 1)"; Table 7.2 "2025 (Semantic
Scholar); 2026 (OpenAlex)"; Tables 11.4–11.5 "August 2026"; Figure 1.3 "August
2026". The Chapter 3 and Chapter 10 rows stay blank, since the book gives no single
date for them.

### 4. Two claims about the book that were not true of it

- "The running examples deliberately use recent internet slang — delulu, rizz,
  cooked, touch grass." Neither "cooked" nor "touch grass" occurs in the book, which
  uses `delulu` (67 times), `rizz` and `rizzlord` (5), and `iykyk`, `frfr` and
  `skibidi` once each in Chapter 13. **Applied:** "delulu, rizz and rizzlord, with
  iykyk, frfr and skibidi in Chapter 13".
- "around a hundred short definitions": the glossary has 81. **Applied:** "around
  eighty". (The "collapsed panel" claim is right; the glossary is a `<details>`.)

### 5. Exercise I's summary omitted Chapter 4's fourth explanation

"…using only query analysis, the execution rule, or query transformation." Chapter 4,
Chapter 13 and the closing map give four lexical explanations for a missing word; the
fourth, a match outside the visible excerpt, is what the exercise's own third
observation tests. **Applied:** "…query transformation, or a match outside the
visible excerpt."

## Teaching notes — readability

- The 52-word "A strong answer attributes recall differences…" sentence in the
  Appendix F task is now three sentences.
- The 42-word vector-lab sentence in the six-week module splits at its semicolon.
- "Reading-time estimates in the book exclude all of this" repeated the course-shapes
  statement that estimates exclude lab and exercise work; the second is dropped.

## Vector Similarity Lab — readability

The control note under the header mixed three interface-mechanics sentences with the
lab's one conceptual rule, "A production model's comparison rule should match its
training", which Chapter 7 now states in the same words. **Applied:** that sentence
moved to the subtitle paragraph, where the lab's framing lives; the hint keeps the
mechanics. Two text nodes; no ids, classes, script, tour titles or parameters
changed.

## Checked and left as they are

- **Handout:** consistent with the notes' stipulated case (30 candidates, five to the
  writer) and with the book; ten-word average sentence.
- **BM25 Evidence Lab:** k1 = 1.2 and b = 0.75 and the Lucene IDF form match Chapter 3
  and Appendix C; records A and F match Figure 4.2; the step-3 saturation-versus-
  length note and the step-6 boundary demonstration match the chapters and Part III's
  new pointer, which names the step by its exact title.
- **Vector lab tour:** the cutoff experiment matches Chapter 13's new pointer; the
  back and forward links resolve.
- **README:** version, rubric, course shapes and audience routes match the notes.
- **The notes' three "provisional timings" statements** and the three "Assign the full
  instructions" links: each clear in its own context.

## What was checked

- Thirteen edits (eleven in the notes, two in the lab), each an exact-match
  replacement asserted to occur once, plus one positional table-row insertion.
- `node tools/test-labs.cjs` and `node tools/test-vector-tour.cjs` — both PASS after
  the lab edit (the suites find tour steps by title and read slider bounds from the
  page; neither changed).
- `python tools/maintain.py` — textbook untouched; "no changes needed", "no problems
  found".
- Cross-file link check re-run: 25 textbook anchors across the companions, all
  resolving, no chapter-text mismatches, no missing fragments.
- `git status`: only `teaching-notes.html` and `vector-similarity-lab.html` changed;
  the vector lab's word diff is exactly the two moved text nodes.
- Rendered check, served locally: the re-verification table has nine rows with the
  new Chapter 12 row and the prefilled dates; the corrected slang, glossary and
  Exercise I sentences render; the vector lab's subtitle carries the rule and its
  hint does not; both pages log no console errors.
- Teaching notes visible words 4,945 → 5,019 (+74, the new row and the dates).
