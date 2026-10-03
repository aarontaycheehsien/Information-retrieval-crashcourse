# Readability plan — revised against the current file

Status: **APPLIED** — all four items, 2026-09-05
Source reviewed: `search-textbook.html` at `f589966` (version 1.1)
Input: section 5 of the readability review, *Readability changes with the highest return*
Date: 2026-09-05

## The finding that reorders everything else

The review reads a snapshot that predates commits `84a9fba`, `4f41aab` and
`4df871f`. **Five of its ten recommendations are already in the file**, several
of them in wording close enough to the review's own that they read as having
been applied from it. Two more are substantially done and need only a residual
touch.

Applying the section as written would therefore mean re-doing finished work, and
in two places re-doing it in the wrong direction — 5.6 asks for a correction the
file already makes, and 5.3 asks for a new fictional corpus that the book's own
stated method argues against.

What follows keeps the review's diagnosis, which is sound, and replaces its task
list with what the current file actually needs.

## Verdicts

| # | Recommendation | Verdict |
|---|---|---|
| 5.1 | Reduce repeated argument | **Keep, retarget** — its named example is done; the live recurrer is a different one |
| 5.2 | Shorten Chapter 1's opening | **Keep, narrow** — mostly dissolves into 5.4; one new instance elsewhere |
| 5.3 | Two recurring example families | **Split** — document the two families; drop the fictional record set |
| 5.4 | Relevance: short entry, fuller evaluation | **Keep — highest remaining return**, and it fixes a live contradiction |
| 5.5 | Chapters 5 and 8 abruptness | **Done** — both, in the file, in the form asked for |
| 5.6 | Chapter 11 simplification and OA correction | **Done** — both halves |
| 5.7 | Stable identifiers for the six distinctions | **Keep, reduce** — the arithmetic already reconciles; one sentence remains |
| 5.8 | Disambiguate overloaded symbols | **Done for `k`; one clause remains for pooling** |
| 5.9 | Attainable practice levels | **Done** — both halves, near-verbatim |
| 5.10 | Qualify the absolutes | **Keep, revise method** — named examples fixed; the sweep needs a bounded scope |

## Already in the file

Recorded so the review is not run against this file a second time.

**5.5 — Chapter 5.** The chapter now opens on the output before the history:
"Start with the output. An encoder takes a query such as `delulu job
expectations` and produces a list of numbers… Chapter 6 opens that computation
and Chapter 7 uses it for retrieval." *From Word2Vec to retrieval embeddings*
follows it. The *Before you start* panel additionally lists Word2Vec's mechanism
among the things that "can be read once and let go".

**5.5 — Chapter 8.** The opening states the framing the review asks for, almost
in its words: "This chapter views the lexical machinery you already know as
coordinates: binary presence, term frequency, TF–IDF and BM25 weights. This is a
comparison of representations, not a chronological claim that BM25 was derived
from TF–IDF."

**5.6 — Chapter 11.** Both halves. The three groups exist ("Read the query
objects in three groups: text and structured conditions; known records and
relationships; and feedback, monitoring or delegated tasks. The table keeps the
exact distinctions available for reference"), and the open-access error is not
merely corrected but promoted into the teaching point the review suggested: "A
filter on the retrieved paper's open-access status would change a search about
the open-access citation advantage: a relevant study may itself be paywalled."
The OpenAlex card now filters on a year range instead.

**5.8 — the RRF constant.** Renamed, with the original-paper note kept exactly as
proposed: "The constant `c` softens the advantage of the very first positions…
The original paper calls this constant `k`; this book uses `c` to distinguish it
from top-`k` result depth."

**5.9 — practice levels.** Both halves. The minimal record: "Start with a record
you can make today: the input, product and mode, search date, visible
transformation, filters, result identifiers and observed limitation… The
detailed tables below are a reference checklist. Internal model versions and
candidate budgets may require vendor disclosure." And the test set: "Thirty to
fifty is a practical starting range. Rerunning an established set may fit an
afternoon; constructing the needs and judging hundreds of results can take much
longer."

**5.1 — the "uses BERT" example.** The near-duplicate is gone, and the split is
the one the review proposes. Chapter 5 tests pretraining versus task training
("Why does that not make generic BERT a retriever?") plus the vendor question;
Chapter 6 asks how positives and negatives change behaviour ("One encoder is
trained on citation-linked papers; another on question–answer pairs. Why might
they rank the same collection differently?"). `uses BERT` now occurs once in the
book.

**5.10 — two of three named absolutes.** ColBERT is qualified ("among the more
inspectable neural approaches"; "inspectable at the scoring layer without being
transparent end to end"). Cranfield is qualified ("It underpins much offline
retrieval evaluation; user studies, online experiments and task-based
evaluations…"). The phrase "no production search system" does not occur.

## The revised plan

Four items, ordered by return. Roughly one working session each for the first
two, an hour for the third, and a bounded afternoon for the fourth.

### R1 — Cut Chapter 1's relevance section to an entry, and fix its contradiction

*Serves 5.4, and most of 5.2.*

Chapter 1's `#what-does-relevant-actually-mean` runs 875 words including the
seven-term panel; Chapter 14's `#relevance-is-a-judgement` runs 654 and covers
the same four levels with the operational detail. This is the book's largest
straight duplication, and it sits third of six in the opening chapter, before
the puzzles.

There is also a defect. A partial fix left two adjacent claims contradicting
each other. The framing paragraph now reads:

> "Relevant" can refer to a computed match, topical suitability, what a person
> learns, or usefulness for a task. These are related perspectives, not a fixed
> ladder. **A model can estimate topical or task-specific suitability**; that
> estimate is not the reader's experienced usefulness.

Three sentences later the first bullet still reads:

> System (algorithmic) relevance … **This is the only level a machine can
> compute**; everything after it requires a person.

Chapter 14 already carries the corrected form of that bullet ("A system can also
estimate topical or task-specific suitability, but those estimates are not
identical to a person's experienced usefulness"). Chapter 1 was not updated to
match.

Do:

- Delete the four-level list from Chapter 1, which removes the contradiction
  with it. Keep the framing paragraph, Figure 1.4, the *AI academic libraries*
  worked example, and the closing pointer to Chapter 14.
- Keep the *Seven terms to carry forward* panel where it is; it is orientation,
  not theory, and it is the last thing before the puzzles.
- Leave Chapter 14 alone. It is already the fuller home and its wording is
  already right.

Expected: Chapter 1 loses roughly 400 words, the puzzles arrive around 500 words
earlier, and the relevance framework has one home instead of two.

### R2 — Thin the shortlist ceiling in Chapter 14

*Serves 5.1, retargeted.*

The review names four recurring claims. Three of them are no longer the problem:
the model-name warning is now concentrated in Chapters 5–6 where it belongs,
semantic-versus-dense occurs nine times across the whole book, and
interface-versus-architecture six. The live recurrer is the one the review lists
first — and its concentration is not where the review looks.

The shortlist-ceiling claim is stated 18 times. Seven are in Chapter 14 alone,
against one each in Chapters 2, 11 and 12, three in Chapter 9 and five across
the appendices and glossary. Chapter 9 is the canonical home.

Chapter 14's seven break down as: two in a self-check question and its answer,
one in the chapter-close list, one as a diagram label — all four legitimate
under the ledger's guardrails — and **three full restatements in running prose**.
Two of those three are near-verbatim with each other and with the chapter-close
bullet: "later stages can improve its ordering but cannot recover excluded
records" and "later stages can improve ordering but cannot recover exclusions".

Do:

- Keep the restatement at the recall/candidate-boundary explanation, which is
  where the claim does operational work. Reduce the other two to a clause that
  applies the ceiling to the metric under discussion, rather than re-deriving it.
- Leave the self-check, chapter close, diagram label and glossary entries alone;
  the ledger's guardrails already exempt those, and for good reason.
- Leave Chapters 2, 11, 12 and the appendices alone. One application each is the
  behaviour the review wants.

Note the repetition ledger's own conclusion here: Jaccard scoring cannot find
this class of repetition — "the repetition is in the referents, not the words".
This item has to be done by reading, and its scope is one chapter.

### R3 — Two small closures

*Serves 5.7 and the remainder of 5.8.*

- **Appendix D.** Its opening frames it as "a crosswalk rather than a controlled
  vocabulary", which is right, but does not say how its eight overlaps relate to
  the six distinctions the Preface promises. One sentence, in the existing
  opening paragraph, naming them as extensions and noting that the six core
  distinctions live in the two part-divider panels.
- **Pooling, Chapter 14.** The glossary already carries two entries and the
  cross-reference between them. The evaluation chapter's own use ("evaluations
  instead use pooling: run many different systems, collect the union…") carries
  no reminder that this is not the encoder sense from Chapter 5. One clause.

Do **not** build the six-item checklist mapped to assessment questions. The
Part I panel ("What a result screen can settle") and the Part II panel ("What
the words on the box do not name") already do exactly that, already reconcile
the arithmetic in the open — "Five confusions are left. Part I settled a sixth
by watching a system behave" — and already link each entry to the section that
supplies its mechanism. A third listing would add precisely the apparatus 5.1
and 5.2 ask to remove.

Vector normalisation needs nothing: of 36 uses of *normalis\**, 27 are
document-length normalisation and exactly one is vector normalisation, so the
collision the review anticipates does not occur in practice.

### R4 — A bounded absolutes pass

*Serves 5.10, with a scope the recommendation lacks.*

The principle is right and the general instruction is not actionable: the
visible text contains 191 *only*, 182 *every*, 95 *cannot*, 70 *nothing* and 56
*never* across 83,601 words, and most are correct. A book-wide review would cost
days and mostly confirm existing wording.

Scope it to where the review says the damage is — the places a qualifier cannot
sit nearby, because the block is read alone:

| Zone | Blocks | Containing an absolute |
|---|---:|---:|
| `figcaption` | 55 | 27 |
| `aside.chapter-close` | 15 | 13 |
| Glossary definitions | 122 | 32 |

Seventy-two blocks. Read each, and change only where the absolute states more
than the body text supports. Leave prose absolutes alone; in running text the
qualification is usually in the next sentence, and stripping them is what makes
the voice bland.

One live example to include: *documentation cannot be retrofitted*, stated three
times (chapter opening, section body, chapter close of Chapter 15). The
procurement argument holds, but "will not start doing so because a library asks
afterwards" overstates it — vendors do add export and logging under customer
pressure. The claim wanted is that a library cannot rely on it, which is both
true and stronger for being defensible.

## Applied

All four items applied on 2026-09-05, plus the 5.3 convention note. Prose only:
no IDs, headings, classes, assets or reading-time labels changed.

**R1.** Deleted the four-level list from Chapter 1 and merged the two paragraphs
around it into one. Chapter 1 falls 4,078 → 3,931 words, its relevance section
875 → 724 — less than the 400 words this plan estimated, because the instruction
that came with the estimate was to keep the framing paragraph, Figure 1.4, the
worked example and the pointer, and those are most of the section. Chapter 1 no
longer duplicates the Mizzaro and Saracevic citations, which Chapter 14 carries.

Two consequences, both necessary:

- Chapter 14's "The four perspectives **introduced** in Chapter 1" became
  "**named** in Chapter 1". This plan said to leave Chapter 14 alone; the
  cross-reference had to follow R1, and one word is the whole change.
- The glossary term-marks for *topical relevance*, *cognitive relevance* and
  *situational relevance* were attaching to Chapter 1's list. Marking runs per
  chapter, so they now attach in Chapter 14 instead — verified in the browser.
  That is the better home, and no mark was lost.

Also fixed in passing: "Keep that in mind for **twelve** chapters" was left over
from the thirteen-chapter edition. Now fourteen, which is what Chapter 15
already says.

**R2.** Chapter 14's three prose restatements are now one. The paragraph
beginning "Within a fixed candidate set…" lost its two opening sentences, which
re-derived what the paragraph immediately above it had just explained, and now
opens on the worked precision@10 example. The sensitivity passage recalls the
boundary in a clause instead of restating it. The Chapter 9 statement, the
Chapter 14 self-check, chapter close and diagram label are untouched.

**R3.** Appendix D's opening now says its overlaps extend the six confusions
rather than replacing them, and links both part-divider panels. Chapter 14's
evaluation *pooling* now carries a clause distinguishing it from encoder pooling
in Chapter 5.

**R4.** The sweep found far less than the block count suggested, and what it
found clustered. Of 27 figcaptions, 13 chapter closes and 22 glossary
definitions containing an absolute — 62 blocks, not the 72 estimated here; the
earlier count matched `<dd>` elements outside the glossary too — six overstated:

| Block | Was | Now |
|---|---|---|
| Figure 6.1 caption | model tokens "never become searchable index terms" | "do not themselves become searchable index terms here" — Chapter 8's learnt sparse puts weight on vocabulary-aligned dimensions |
| Figure 9.4 caption | pointwise "never compares candidates" | "never compares candidates directly", matching the body |
| Chapter 1 close | "Only system relevance can be computed." | "A system can estimate suitability; it cannot make the judgement." |
| Glossary, *System or algorithmic relevance* | "The only level a system can compute." | "A system can also estimate topical or task-specific suitability, but no estimate is the reader's judgement." |
| Chapter 14 close | "the only measurement a library controls" | "the one measurement whose definition of relevance the library chose" |
| Chapter 15 close | "cannot be retrofitted… will not start doing so because a library asks" | "cannot be assumed to arrive later. A vendor may add them, but… not on a library's timetable" |

The other 56 blocks were left alone. Their absolutes are correct — "a vector is
an ordered list of numbers and nothing more", "an agent can only choose among
the tools it has", "a downstream stage cannot repair an upstream exclusion" —
and are the voice the review asked to keep.

Worth noting what the cluster was: three of the six were the *same* claim. "Only
system relevance can be computed" survived in Chapter 1's body, its chapter
close and the glossary after an earlier pass corrected only the body's framing
paragraph. R1 caught the first; R4 caught the other two. The two Chapter 15
prose statements of the retrofit claim, which sit outside R4's zones, were
brought into line with the corrected chapter close: the near-duplicate second
one is now a back-reference.

**5.3.** The two example families and their jobs are recorded in
`tools/README.md`, including what `delulu` must not be used for and the standing
instruction to reuse the *AI academic libraries* need rather than invent records.

### Verification

| Check | Result |
|---|---|
| `python tools/maintain.py` | no changes needed; no problems found |
| `python tools/renumber_footnotes.py` | already in order (55 footnotes) |
| HTML parse | no errors, no unclosed elements at EOF |
| IDs | 553, all unique |
| Internal links | 1,254, none broken |
| Glossary | 81 entries, no duplicate labels |
| Footnotes | 55 definitions, 55 references, sets match |
| Asset indexes | 55 figures, 44 tables; TOC 36 rows |
| Browser console | no errors |
| Term marks | 218; the three relevance terms now mark in Chapter 14 |
| Reading times | unchanged; Chapter 1's 147-word loss is 0.7 min and does not move "About 17 min" |

Visible words 83,601 → 83,494.

### Not done, deliberately

`CHANGELOG.md` is untouched. The 1.1 entry is dated today and the last commit
folded the Unreleased section into it, so whether this work joins 1.1 or opens
1.2 is a release decision rather than an editorial one.

The Chapter 5 front-loading flagged below remains a flag. It was not in the four
items, and it needs a judgement about the *Before you start* panel that this
pass had no mandate to make.

## Two changes to the review's plan

**5.3 — drop the fictional record set.** The two example families exist and
already carry the jobs the review assigns them: `delulu` appears 45 times, in
the Preface, Chapters 2–7, 9 and 13 and Appendix C, always as a lexical stress
test; the open-access citation advantage appears in Chapters 1, 7 and 11 as the
realistic academic search, and is also the question behind Puzzle 3 and the
worked need in Chapter 11's eight-doors figure. Recording that as a convention
is worth doing — a line in `tools/README.md` — and costs nothing.

The third clause is a different matter. "Define a small, stable set of fictional
academic records, with dates and methods" would introduce a fabricated corpus
into a book whose stated method is the opposite: "Wherever possible, I tie a
concept to what a named library or academic search system is documented to do,
together with the date I checked it. When the documentation runs out, I say so
rather than infer what is happening." That sourcing discipline is the book's
strongest asset with the audience it is written for. Where a judged example is
genuinely needed, reuse the *AI academic libraries* need already worked in
Chapter 1 and Chapter 13 rather than inventing records.

**5.2 — do not restructure Chapter 1 further.** The review's remaining asks are
either done or dissolve into R1. The Scopus comparison is already marked
"Optional comparison"; the puzzles already arrive as a panel with their three
verdicts; the six-stage map is now the closing section, *A map of the arguments
ahead*, rather than front matter. What is left is the relevance section, which
R1 removes. Chapter 1 has been reordered three times (`0e57952`, `92c6d81`,
`4f41aab`) and each pass moves anchors that other chapters link to.

The front-loading the review diagnosed has, however, migrated. **Chapter 5 now
runs 1,383 words before its first section heading** — chapter head, stage map,
central question, the *Before you start* panel and *Start with the output* — out
of the chapter's 3,161 words. Everything
in it was added for a good reason and the chapter genuinely is the steepest, so
this is a flag rather than a task: if R1 shortens Chapter 1's entry and Chapter 5
is left as it is, Chapter 5 becomes the book's slowest start.

## Verification

Each item is prose-only; no IDs, headings, classes or assets change.

```bash
python tools/maintain.py
python tools/renumber_footnotes.py
```

Both are idempotent and should report no changes needed. Add, per the
established pattern: HTML parses with balanced tags; every internal `href`
resolves; glossary entry count and `MARKED` list unchanged; and for R1, that
Chapter 14's `#relevance-is-a-judgement` is byte-identical, since the whole
point is that it is already correct.
