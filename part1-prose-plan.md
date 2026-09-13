# Part I prose readability — diagnosis and plan

Scope: Preface, Part I front matter, Chapters 1–4 and Application exercise I
(`search-textbook.html`, lines ~1063–1667). Body prose only — figures, tables,
captions, check-yourself answers and asides excluded from the measurements.

Status: **PROPOSED**. Nothing applied.

## Measurements

Body paragraphs of 15+ words, tags stripped, Flesch–Kincaid grade level.

| Section | Words | Avg sentence | Avg paragraph | FK grade | Sentences 40w+ | Paras with 2+ em dashes | Negatively framed sentences |
|---|---|---|---|---|---|---|---|
| Preface | 1,418 | 22.9 | 68 | 12.1 | 6 | 6/22 | 16% |
| Ch 1 The retrieval problem | 2,536 | 16.2 | 55 | 10.5 | 2 | 14/46 | 14% |
| Ch 2 Boolean admission | 2,041 | 16.2 | 41 | 11.2 | 0 | 0/51 | 17% |
| Ch 3 BM25 | 1,614 | 19.0 | 47 | 12.2 | 0 | 2/34 | 18% |
| Ch 4 Beyond strict Boolean | 2,084 | 19.7 | 53 | 11.8 | 4 | 4/42 | 23% |

Across Part I: 100 em dashes per 9,600 words (10.4 per 1,000), 41 semicolons,
248 `-tion` nominalisations (25.7 per 1,000).

## Diagnosis

**1. The hardest prose in the book is the first prose in the book.** The Preface
has the longest sentences, the longest paragraphs, the highest dash density and
half of Part I's 40-word-plus sentences. Chapter 2, which carries the heaviest
technical load in Part I, is the easiest to read. The difficulty gradient runs
the wrong way at exactly the point where a reader decides whether to continue.

**2. The em dash is carrying three unrelated jobs.** It marks apposition
("the information need"), contrast ("not because the ideas are difficult, but
because"), and afterthought ("— and where the interface stops answering"). A
reader cannot predict from the mark which is coming, so each one costs a
re-parse. Chapter 2 uses none of this and loses nothing, which is the proof that
the register does not depend on them.

**3. Definition by negation.** Nearly a quarter of Chapter 4's sentences are
framed as what something is not: "non-Boolean does not mean non-lexical", "a
record lacking a typed word does not establish semantic matching", "neither
axis records that choice". Each is individually correct and the book's whole
argument is corrective, so some of this is load-bearing. But a reader who does
not yet hold the positive statement cannot assemble one from a stack of
negations. Chapter 4 asks them to do this five or six times consecutively.

**4. Hedge stacking.** 8% of Chapter 4's sentences carry two or more of
*may / can / often / usually / some / possibly*. Individually these are honest
epistemic caution, which this book is right to insist on. Stacked, they produce
sentences that assert nothing a reader could check, verify or disagree with.

**5. Prose about the book's structure competes with prose about retrieval.**
"A map of the arguments ahead" (Ch 1) and "What Part I settles, and what it
hands on" (Ch 4) are written at the book's highest abstraction — "temptations",
"instances", "the same category error every time" — while carrying the least
new information per word. These are the passages most likely to be skimmed and
they are currently the ones most punished by skimming.

**6. Abstract subjects.** "The admission decision is now clear"; "the ordering
problem is still open"; "query transformation is not a kind of retrieval". The
chapters explain mechanisms whose actors (the analyser, the index, the ranker,
the searcher) are concrete and available, but the sentences often take an
abstraction as subject instead.

**7. What already works and should become the template.** The short declarative
pull-lines are the strongest writing in Part I: "A match is not relevance. A
match is evidence." / "Boolean decides who gets into the competition. Ranking
decides who finishes first." / "Text becomes tokens; analysis turns selected
tokens into searchable terms." They are short, concrete, unhedged, and placed
where a reader needs a handhold. There are roughly eight in Part I. The fix
throughout is to write more sentences like these, not to simplify vocabulary.

## Plan

Five packages, ordered by return per hour of work.

### P1 — Rewrite the Preface's first three paragraphs and "What this book is"
*Highest return. Roughly 600 words touched.*

Target: FK 12.1 → about 10.5; average sentence 22.9 → under 19; no sentence over
40 words. Method: split the six long sentences at their natural colon or dash
break; convert the three-item dash-separated list in "three things this book is
not" into the bulleted list it already is semantically. Keep the anecdote about
library school — it is the most human writing in the book and it should not be
compressed.

### P2 — Halve the em dash count in the Preface and Chapter 1
*Roughly 40 dashes.*

Rule to apply: keep the dash where it marks a genuine interruption of voice;
replace it with a full stop where it introduces an independent clause; replace
it with a comma or brackets where it marks apposition. Chapter 2's dash
discipline is the target. This is mechanical and can be done in one pass with
review at each site.

### P3 — Convert Chapter 4's negations into positive-then-limit pairs
*Highest conceptual return. Roughly 15 sentences.*

Pattern: state the positive claim first in its own sentence, then the boundary.
"Non-Boolean does not mean non-lexical" becomes "A system can drop one of your
words and still be scoring on nothing but words. Boolean is one lexical rule
among several." Target: negatively framed sentences 23% → under 15%, which
leaves the corrective argument intact while giving the reader something to hold.

### P4 — De-hedge Chapter 4 and tighten "What Part I settles"
*Roughly 10 sentences plus one section.*

For each stacked-hedge sentence, keep the strongest single hedge and delete the
rest, or move the qualification into its own short sentence. For the closing
section, cut the meta-commentary about which temptation is of which kind and
state plainly what Part I established and what remains open. The three-way
distinction between the puzzles is already carried by the chapter-close lists.

### P5 — Fix on one wording for the three controls
*Small, but it compounds.*

Admission / ranking / output boundary is restated at least four times in Part I
in four different phrasings. Choose one form of words, use it verbatim at every
recurrence, and let repetition do the teaching. Same treatment for "analysed
term" and "candidate set".

### Deliberately not in scope

- Vocabulary simplification. The audience is expert; the difficulty is
  structural, not lexical.
- Shortening Chapter 2 or 3. They measure hardest on FK because of technical
  terms, and they read the most easily. FK is a poor instrument here and should
  not be optimised against on its own.
- The dated product examples and the epistemic caution about undocumented
  systems. Both are the book's distinguishing virtue; P4 trims stacking, not
  the caution itself.

## Verification

Re-run the same measurement over `search-textbook.html` after each package and
check against the targets above. Then `python tools/maintain.py` and
`python tools/renumber_footnotes.py`, since P1 and P4 move text across footnote
markers.

Read-aloud check for P1 and P3: any sentence that cannot be read aloud in one
breath without re-reading is still too long.

## Basis

The diagnosis is drawn from the text itself; the principles behind it are
standard. Gopen and Swan's argument that readers attach meaning to structural
position, so the difficult material should arrive late in the sentence rather
than early (*American Scientist*, 1990, 78(6), 550–559), and Williams and
Bizup, *Style: Lessons in Clarity and Grace*, on concrete subjects and
nominalisation. Flesch–Kincaid grade level follows Kincaid and colleagues
(1975). A database check of these references returned irrelevant results in the
session that produced this plan, so treat the bibliographic detail as
unverified.
