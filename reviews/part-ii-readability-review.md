# Part II (Chapters 5–11): readability and consistency review

Reviewed 18 September 2026 on branch `fable-1` against commit `a6fbb11` (the Part I
pass). The findings below **have been applied** to `search-textbook.html`; locations
name section anchors, since the file's lines are long and shift with each pass.

The brief was the same as Part I — readability with the content held fixed — plus an
explicit check that Part II stays consistent with Part I, Part III and the two labs.
The 6 September review (`chapter-5-11-review.md`) had already had its ten consistency
findings applied in 1.2 and 1.2.1; its per-chapter readability table was only partly
applied, and the prose-only remainder is taken up here. The repetition ledger's Part II
dispositions (claims B, D and E, canonical in Chapters 7 and 9) are respected.

Consistency was checked from the anchors outward: 200 Part II ids; three links from
Part II to the Vector Similarity Lab and two back; one from the teaching notes; about
ninety from Part III and the back matter into Part II sections; thirty-two from
Part I. None of those ids changed. Part III's *Carried forward* panel relies on Part
II's chapter closes restating five terms, and the closes are untouched.

Constraints kept: no `id` removed or renamed; figures, tables, footnotes and
reading-time labels unchanged; the exempt zones (self-checks, chapter closes,
glossary, footnotes, both exercises) byte-identical; everything outside Part II
byte-identical, including both labs and the teaching notes. Two structural changes,
both flagged in the plan: three `<h4>` subheadings added to Chapter 6, and one `<h5>`
corrected to `<h4>` in Chapter 11. The tables of contents are built from h2 and h3
only, so neither touches a TOC.

## Consistency findings applied

### 1. Figure 7.1 no longer matched the Vector Similarity Lab it cited

**Location:** `#fig-7-1`. The image draws Candidate B at length 1.65 with dot product
1.798 against A's 1.736, and the caption said "The exact values are the defaults used
in the Vector Similarity Lab." Version 1.2 lengthened the lab's default B to 1.90
(`vector-similarity-lab.html`, `DEFAULTS`) so its dot-product step is no longer
knife-edge: B now scores 2.07, a 19% margin. The lab's tour still opens with B at
1.65, so the drawing is a real lab state, but not the defaults and not the state in
which the lab demonstrates the reversal.

**Applied (caption only):** "…so the longer B overtakes A — narrowly at the length
drawn here; the Vector Similarity Lab's guided tour lengthens B further so the
reversal is unmistakable. None of these values is a relevance probability." The alt
text's "narrowly overtake" is true of the image and stays. Regenerating the PNG with
B = 1.90 would let the caption drop the caveat; that is an asset change and was not
done.

### 2. Chapter 7 omitted the lab's rule for choosing a comparison

The lab says twice that a production model's comparison rule should match its
training and that a model can learn to use magnitude; Chapter 7 explained cosine and
dot product without saying how the choice is made. **Applied**, one sentence after the
dot-product paragraph: "Which rule applies is not a free choice: a model can learn to
use magnitude, so a production system's comparison rule should match the one its
encoder was trained with." The one content addition in this pass.

### 3. Chapter 9's opening still promised hybrid retrieval

`#reranking-and-hybrid` orientation: "And it explains hybrid retrieval, which runs more
than one retriever at once and must then decide how to combine what they return."
Hybrid became Chapter 10 in 1.1. **Applied:** "Hybrid retrieval, which runs more than
one retriever at once and must then combine what they return, is Chapter 10's
subject" (linked).

### 4. A stale figure number in Chapter 9

"Two things follow from reading Figure 9.5 as a chain" — Figure 9.5 is the
pointwise/pairwise/listwise diagram; the Primo chain is Figure 9.7. Unlinked, so
`maintain.py` could not see it. **Applied:** "Figure 9.7", linked to `#fig-9-7` so it is
checkable from now on.

### 5. The Part II divider's five identical "Read the distinction" links

`#distinction-map-vocabulary`. The Part I pass made Chapter 4's one equivalent link
name its destination. **Applied:** each now reads "Read the distinction in Chapter N"
(5, 8, 7, 7, 9), hrefs unchanged, texts verifiable by the maintenance pass.

### 6. Chapter 5's panel overstated what follows

"This is where the book stops being about words" — Chapter 8 then shows lexical
vectors and Chapter 9 learnt sparse retrieval, "lexical in shape but learnt
throughout." **Applied:** "stops being only about words." The 1.1 changelog quotes the
original as a description of the panel's purpose and is left as the record it is.

## Placement and duplication

### 7. Chapter 6's 1,164-word section had no internal structure

`#how-a-contextual-encoder-becomes-a-retrieval-encoder`: 73 sentences under one
heading, with four movements — pooling and retrieval training, the worked example,
where the training signal comes from, what the space ends up preserving. The 6
September review asked for visible subheadings; not applied until now. **Applied:**
three `<h4>` headings in the pattern Chapter 11 already uses —
`#a-worked-training-example`, `#where-the-training-signal-comes-from`,
`#what-the-space-ends-up-preserving`. They render at the same size and weight as
Chapter 11's existing h4 (18px/700, checked in the browser).

### 8. Chapter 5: a figure separated a question from its answer

Figure 5.1 (*Where the numbers come from*) sat between "what target can a body of
text supply for itself?" and "The answer comes from linguistics…", although it
illustrates the paragraph before the question. **Applied:** the figure block moved up
one paragraph; it keeps its number, and question and answer are now adjacent.

### 9. Chapter 9: the budget point made twice around an interrupting definition

`#reranking-in-two-documented-academic-pipelines`: "These values of k are
stage-specific candidate budgets…", then the learning-to-rank definition, then "The
two numbers are budgets, not statements about relevance…". **Applied:** the first
sentence dropped (the second paragraph carries the whole point plus the PubMed/Primo
tail difference); the learning-to-rank paragraph now follows the budgets paragraph.

### 10. Chapter 10 stated RRF's properties four times in 1,842 words

Orientation, the preview paragraph before the RRF section, the section's own
definition, and the paragraph after the worked example. **Applied:** the preview
paragraph keeps its unique content — arrangement versus combination method, routing
as a separate decision — and ends "RRF is a fusion rule, not a relevance model or
reranker; the formula and a worked example follow." Every property it previewed is
stated where it is derived.

### 11. Chapter 8 restated the representation / vector / embedding definitions a third time

The "Terminology varies across fields and systems" paragraph repeated Chapter 5's
key-distinction panel and Chapter 7's disambiguation. **Applied:** reduced to its
unique content — the three-way classification (BM25 specified-rule sparse; SPLADE
learnt sparse; dense bi-encoder learnt dense) with a link to the Chapter 5 panel,
and the "sparse embeddings" note with its footnote. The 190-word learnt-sparse
paragraph is also split in two at "What the two share is the shape".

### 12. Chapter 11's open-access-status caution was a non sequitur before Table 11.1

"A filter on the retrieved paper's open-access status would change a search about the
open-access citation advantage…" explained why Figure 11.1's programmatic-predicate
example filters by year, but appeared before any filter example. **Applied:** moved to
directly after Figure 11.1 — "One caution on the seventh door: … which is why the
example filters by year instead." The teaching point the previous plan promoted is
kept where it applies.

## Sentence-level, captions and link text

- **Chapter 5 pointed at Appendix A twice with the same clause.** The first pointer
  now reads "Appendix A sets out what self-attention does and why nearly every model
  named in this book is built from it"; the two-halves clause stays in its later,
  in-context sentence.
- **Seven links whose text did not name their destination**, hrefs unchanged: "A later
  section" → "Chapter 8"; "The appendix on the Transformer" → "Appendix A"; "the
  discussion of out-of-distribution transfer" → "Chapter 13's discussion…"; "The
  earlier lexical sections" → "Chapters 2 to 4"; "The inverted index described
  earlier" → "The inverted index of Chapter 2" (now linked); "the earlier single-vector
  similarity explanation" → "Chapter 7's similarity explanation"; "the section on BERT"
  → "Chapter 5's section on BERT".
- **Chapter 9:** "This section explains why systems accept the constraint…" precedes
  four separate sections → "The sections that follow explain…". The editorial clause
  "; the architecture itself belongs in the main chapter" is removed. "A reranker
  therefore usually does not search the complete collection" repeated the section's
  opening and is removed; the paragraph's other two sentences stand.
- **Chapter 11:** the one `<h5>` in Part II, sitting directly under an `<h3>`, is now an
  `<h4>` (id unchanged). The closing paragraph's re-argument of the PRF point made
  after Table 11.3 is now a clause: "…one reranker in advance — even the two-pass
  feedback workflow above."
- **Three sentence splits:** Chapter 5's Firth sentence at the semicolon; Chapter 6's
  48-word "Pretraining gives the model broad linguistic patterns…" after "for
  search"; Chapter 10's 41-word "Selecting a route and combining results…" after
  "definition".
- **Four captions that repeated the adjacent body sentence verbatim** (Figures 7.4,
  7.6, 8.7, 8.8) keep only the clause the body does not state, and still stand alone:
  7.4 "At search time only the query is encoded, then compared with the vectors stored
  in advance"; 7.6 "One vector must stand for everything in the passage, so broad
  similarity can dominate an exact code, a rare name or a negation"; 8.7 "How finely
  the source is cut, how each unit is represented and how matches are grouped back
  into results are separate choices, and only the last is visible in a result list";
  8.8 "Many independently searchable units do not mean that the complete paper has
  been captured faithfully, nor that evidence spread across chunks will be combined."

## Considered and not applied

- **Chapter 7's top-k section, Table 7.1 and close** — ledger claim D, canonical.
- **Chapter 5's *Before you start* panel and *Start with the output* box** — deliberate
  1.1 and 5 September additions; only finding 6's one word changed.
- **Chapter 9's five learnt-sparse paragraphs** — the Chapter 8 (representation) /
  Chapter 9 (pipeline role, cost, visibility) split holds.
- **"Before it knows which query will arrive"** in Chapters 7 and 9, a close and a
  self-check — a deliberate recurring image.
- **"Neutral baseline" (Chapter 10 close) and "reliably partial" (Chapter 11 close)** —
  exempt zones, and the body wording is consistent with each.
- **Table 11.1 and Figure 11.1** presenting the eight query objects twice — a table
  restructure is an asset change.
- **Figures 8.7 and 8.8 as images, and the Figure 7.1 PNG** — asset follow-ups.
- **CHANGELOG.md** — untouched; whether these two passes join a 1.2.2 entry is a
  release decision.

## What was checked

- Forty edits, each an exact-match replacement asserted to occur once, plus three
  positional block moves (Figure 5.1; the learning-to-rank paragraph; the open-access
  caution).
- `python tools/maintain.py` — "no changes needed", "no problems found"; the renamed
  and newly linked cross-references pass the stale-cross-reference check; figure and
  table numbers unchanged after the Figure 5.1 move.
- `python tools/renumber_footnotes.py` — "already in order (56 footnotes)".
- `node tools/test-labs.cjs` and `node tools/test-vector-tour.cjs` — both PASS (the
  labs were not edited; this confirms the repo state is intact).
- Byte-identical against the pre-edit file: all 15 chapter closes, all 15
  self-checks, both exercises, the glossary and the footnotes section (34 blocks); the
  front matter, Preface and Part I; and everything from the Part III divider onward.
  `git status` shows only the textbook and this file.
- Ids 603 → 606, exactly the three new h4 ids; none removed; no duplicates; every
  internal `href` resolves. `common-confusion`, `ir-figure`, `figcaption`,
  `pull-quote`, chapter-close, self-check and footnote-reference counts unchanged.
  Part II h4 count 7 → 11 (three new, one corrected from h5); h5 count 1 → 0.
- Rendered page, served locally: the three new h4s render at 18px/700, the same as
  Chapter 11's existing h4; Figure 5.1 now sits between "BM25 computes term weights…"
  and "Training, though…"; the open-access caution is the element after Figure 11.1;
  the chain paragraph reads "Figure 9.7"; the five divider links read "Read the
  distinction in Chapter N"; no console errors. Term marks 223 in the book before and
  after, and per chapter 5 / 5 / 15 / 16 / 18 / 8 / 13 for Chapters 5–11 before and
  after, so the moves lost no first-use mark.
- Visible words in Part II: 21,665 → 21,549 (−116). No reading-time label moves at
  the book's 211 words per minute.
