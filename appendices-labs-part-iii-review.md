# Appendices, labs, teaching notes and Part III: proposed improvements

Reviewed 6 September 2026 against commit `2675662`, version 1.1. Unlike
`part-iii-review.md`, which was a consistency pass with repairs already made,
this is mainly a proposal document: most of it asks for substantive additions
and structural changes that need an author decision before anyone edits the
source of truth.

**Status.** Fifteen items marked **Applied** below have been made: the five that
needed no decision, the Chapter 12 apparatus (§4.4) once the author supplied its
source, and a further eight approved as a batch because none of them changes an
argument. Everything else is still a proposal. Each applied item is marked at its
own heading, so this file stays usable as a working list.

## What was checked, and what passed

- **Appendices A–G** read in full (roughly 14,000 visible words), plus the
  glossary and the four Appendix D tables.
- **Both labs** read as prose and as code. The BM25 lab's scoring model was
  reimplemented independently in Python and every tour claim recomputed.
- **Teaching notes** read in full, and every asset reference in the
  "before you teach it" list checked against the textbook.
- **Part III (Chapters 12–15)** read in full, after the `part-iii-review.md`
  repairs.

Four things came back clean and are worth recording, because they narrow where
the remaining problems can be:

1. **`python tools/maintain.py`** — "no problems found". Asset numbering, both
   tables of contents, anchors, duplicate ids, internal links and stale
   cross-references are all consistent. **`python tools/renumber_footnotes.py`**
   — already in order, 55 footnotes. **`node tools/test-labs.cjs`** — passes.
2. **Every numerical claim in the BM25 lab's guided tour is correct.**
   Independently recomputed: strict `AND` admits Record A alone; IDF(`delulu`) =
   1.030 against IDF(`job`) = 0.241, a ratio of 4.3 ("roughly four times");
   Record D's `delulu` contribution moves 1.882 → 2.151 from three occurrences to
   twenty (+14.3%, "roughly 15 per cent"); Record C at 75 tokens scores 1.229
   against Record F's 1.350; D overtakes A at exactly six appendix paragraphs
   (2.322 against 2.277); `unrealistic` and `foolish` carry identical IDF of
   1.540 and lift B and F respectively to first place. The lab's claim that
   every number on the page can be checked by hand holds.
3. **The vector lab's tour arithmetic is correct.** cos 24° = 0.914, cos 55° =
   0.574; under dot product B (1.798) does beat A (1.736); normalisation does
   make the two rules identical.
4. **Appendix F is the best-cited section in the book** — 15 external links, 11
   of them DOIs or arXiv identifiers, covering Cochrane, ASReview, SAFE, the
   Kempny, König and Repke validation work and the CMH stopping method.

Everything below is therefore about design, coverage and structure, not about
arithmetic or link rot.

---

## The ten changes worth making first

| # | Change | Where | Effort |
|---|---|---|---|
| 1 | Give appendices the chapter furniture they lack: Previous/Next navigation, and *Check yourself* for D, E, F and G | All appendices | Medium |
| 2 | ~~Recalibrate the appendix reading times, or document the convention~~ **Applied** | Appendices F (29 min) and G (12 min) | Small |
| 3 | Rerun Appendix B's worked example on a string that actually splits | Appendix B, Figure B.1 | Small |
| 4 | ~~Add a `top-k` boundary control to the BM25 lab~~ **Applied** | `bm25-evidence-lab.html` | Medium |
| 5 | ~~Add Table 14.3: one filled-in row of a local evaluation set~~ **Applied** | Chapter 14 | Small |
| 6 | ~~Draw the RAG Fusion pipeline as Figure G.1~~ **Applied** | Appendix G | Medium |
| 7 | ~~Fix two links that resolve to a "this moved" stub rather than to the content~~ **Applied** | Appendices D and E | Trivial |
| 8 | ~~Give Chapter 12's Primo experiment the evidentiary apparatus the rest of the book uses~~ **Applied** | Chapter 12 | Small |
| 9 | ~~Add a cost, quota and deprecation question to the procurement checklist~~ **Applied** | Chapter 15 | Small |
| 10 | ~~Cross-link Appendix C and the BM25 lab in both directions~~ **Applied** | Appendix C, `bm25-evidence-lab.html` | Trivial |

---

## 1. The appendices

### 1.1 Appendices are missing the furniture that makes chapters assignable — **Check yourself declined; navigation still open**

Every one of the fifteen chapters carries a `chapter-nav` (Previous/Next) and a
*Check yourself* block. **No appendix carries either.** No appendix carries a
"What this appendix established" summary; the only closing device in the set is
Appendix A's "What this appendix leaves out".

This matters more than a consistency complaint, because the README and the
teaching notes both promise that appendices are assignable on their own and
carry stable links. A student sent directly to Appendix F — which the teaching
notes designate **core** for the evidence-synthesis cohort — lands in a 29-minute
section with no route forward, no route back to the chapters, and no way to test
their own understanding. It is the only core reading in the book without
self-check questions.

**Proposed:** add `chapter-nav` to all seven appendices (A→B→…→G, with A's
Previous pointing at *What you can now ask* and G's Next at the glossary). Add
*Check yourself* to D, E, F and G.

**Author's decision: no appendix gets *Check yourself*, Appendix D included.**
The device belongs to chapters, which carry an argument the reader is meant to
have followed; appendices are expansions and references, and a self-check would
imply a test the appendix is not setting. The candidate questions below stay in
this file as a record of what was considered, not as pending work. The
navigation half is untouched by that decision and remains available.

Three candidate questions for Appendix F, to show the register:

> *A team reports 97% recall against their labelled benchmark and stopped
> screening at 40% of the pool. What has that established about the review?*
> Recall against a labelled evaluation set at a simulated stopping point.
> Nothing about the studies absent from the candidate pool, and nothing about
> whether a live reviewer could have known when to stop.

> *A reviewer switches ASReview from TF-IDF to SBERT features and finds relevant
> records sooner. Has coverage improved?* No. Active learning reprioritises a
> fixed pool. Coverage changes only if another retrieval route adds records, a
> screener errs, or screening stops early.

> *Which of the three boundaries in Figure F.3 can a downstream stage repair?*
> None. Each is upstream of everything that follows it.

### 1.2 Two appendix reading times are out by roughly a factor of two — **Applied**

Measured against visible word counts, the book's reading-time convention is
tight: fifteen chapters plus the Preface run at 199–270 words per minute, median
**211**. Appendices A (223), B (228) and C (193) sit inside that band. Two do not:

| Section | Visible words | Stated | Implied rate | At 211 wpm |
|---|---|---|---|---|
| Appendix E | 3,412 | 19 min | 180 wpm | ~16 min |
| **Appendix F** | 3,586 | **29 min** | **124 wpm** | **~17 min** |
| **Appendix G** | 1,332 | **12 min** | **111 wpm** | **~6 min** |

Appendix G is the clearest case, because it is the *least* dense appendix in the
set — no table, no figure, no formula — and carries the second-slowest implied
rate. Appendix F at least has three figures and three tables to justify some
slowing.

This is not cosmetic. The teaching notes build three course shapes on these
numbers, and Appendix F's 29 minutes is what an instructor uses when deciding
whether it fits a session.

**Proposed:** either recalculate F and G at the book's own convention, or state
the convention somewhere (for example, that appendix times assume study rather
than reading) so an instructor knows the two numbers are not comparable.

*Also worth a look while in there:* Chapter 4 runs at 270 wpm — 2,700 words in a
stated 10 minutes — which is the outlier in the other direction. Out of scope
for this review, but the same recalculation would catch it.

### 1.3 Appendix B's worked example never exercises the mechanism it exists to explain

Appendix B follows "Unbelievable scenes!" through six stages. The text concedes
the problem itself: "Here all three items are complete vocabulary tokens, so no
word needs a continuation piece." Figure B.1's caption then opens by explaining
what `##` means — a marker the figure never displays.

So the appendix whose stated job is to "follow one named tokeniser through every
stage" has chosen an example where WordPiece's single most distinctive behaviour,
subword splitting, does not fire. A reader learns the shape of the pipeline but
never sees the thing the pipeline is for.

The book already has the right string. Table B.1, on the same page, uses
`rizzlord`. Chapter 13 asserts that "`rizzlord` is partly compositional. A model
may infer a plausible meaning if its tokeniser produces useful pieces resembling
`rizz` and `lord`" — a claim made in prose and demonstrated nowhere, although
Appendix B has the diagram already drawn.

**Proposed:** run `rizzlord` (or `delulu`) through the same six stages as a
second panel, or replace the current example outright. The `##` caption then
earns its place, Chapter 13's compositionality claim acquires evidence, and
Appendix B connects to the OOV diagnosis instead of sitting beside it.

**One caveat on execution:** the current pieces and IDs are stated to follow the
published `google-bert/bert-base-uncased` vocabulary, and I could not verify them
— outbound access to huggingface.co is blocked in this environment. Any new
segmentation must be taken from the actual vocabulary file, not predicted, and
the existing IDs (23653, 5019, 999, 101, 102) are worth re-checking at the same
time.

### 1.4 Appendix D has no external citations, and cannot be used the way it is described — **Both halves declined**

Appendix D is the only appendix with **zero external links**. Four tables of
roughly forty rows assert what each label "usually describes" across research,
product documentation and marketing, entirely on the author's authority. That is
defensible for a crosswalk, and the appendix says so. But the claim that usage
varies is the appendix's whole premise, and it is the one claim never evidenced.

The second problem is functional. Chapter 15 tells the reader that Appendix D
"is worth having to hand while the questions are being asked", and the teaching
notes repeat it. What is actually to hand is four static tables spanning about
2,700 words, with no way to jump to a term. Someone in a renewal meeting who
hears "hybrid semantic reranking" has to scan four tables.

**Proposed, in order of value:**

1. ~~Add a filter box above the Appendix D tables.~~ **Declined by the author.**
   The case for it was real — the book is one 851KB page of 92,283 words, so a
   browser find for "hybrid" searches all fifteen chapters rather than the 28
   rows of this appendix, which is exactly the lookup the appendix is described
   as supporting. The case against it is that this would be the only part of the
   book whose intended use depends on JavaScript, and it carries print, no-JS,
   accessibility and anchor obligations that the rest of the text does not. A
   cheaper alternative was offered and also not taken: per-table anchors and a
   one-line jump row, which survives printing and saving. Appendix D stays a
   text.
2. ~~Add one citation per row family where usage genuinely diverges.~~
   **Declined by the author: the absence of citations is a design choice.** The
   appendix is a practitioner's reading of usage, not a survey of it, and citing
   it would misrepresent what it is. What was applied instead is one sentence in
   the framing paragraph saying so, because the choice was previously invisible
   — a reader could only read it as an omission in a book that cites everything
   else. Each entry is now framed as a prompt to check what a particular vendor
   or paper means, not a finding about what a word must mean.

### 1.5 Appendix E's title leads with material that is no longer in it — **Applied**

Appendix E is titled "Rank fusion, diversification, learning to rank and
rerankers". Following the G0 decision, the worked RRF explanation moved to
Chapter 10, and the fusion section is now four paragraphs ending "The worked
explanation of reciprocal rank fusion is now in Chapter 10."

**Proposed:** retitle to lead with what the appendix actually contains —
"Learning to rank, diversification and rerankers" — and let the fusion paragraphs
stand as the distinction they now are (fusion and reranking solve different
problems) rather than as a placeholder for a section that left.

### 1.6 Two links land on a "this moved" stub instead of the content — **Applied**

`search-textbook.html:3442` places a `legacy-anchor` span,
`#appendix-how-rrf-combines-ranked-lists`, immediately before the sentence
announcing that RRF moved to Chapter 10. Two live in-prose links target it:

- **`:3381`** — Table D.2's "Read in this book" cell for the rank-and-score-fusion
  family, labelled *RRF and score fusion compared*.
- **`:3462`** — Appendix E's own sentence, "the same score-compatibility problem
  that made **RRF attractive**".

Both therefore send a reader looking for the RRF explanation to a signpost saying
it is elsewhere. The failure is invisible to `maintain.py`, because the id exists
and the link text names no chapter number, so the stale-cross-reference check has
nothing to catch.

A third link compounds it: the signpost at `:3442` points at
`#why-hybrid-retrieval-remains-attractive`, Chapter 10's opening section, rather
than at `#how-reciprocal-rank-fusion-combines-ranked-lists`, the section that
actually holds the explanation.

**Proposed:** repoint all three at
`#how-reciprocal-rank-fusion-combines-ranked-lists`. Retain the legacy anchor —
it is doing its job for inbound external links.

**And a lint rule worth adding to `maintain.py`:** no in-prose `href` may target
an id declared on a `legacy-anchor` span. A scan found 24 such links across the
book. Twenty-two are harmless, because the legacy span sits immediately before
the current heading and the reader lands in the right place. The two above are
not, and only a rule distinguishes them cheaply.

### 1.7 Appendix G has no figure, no table, and hedges the one pointer a librarian needs — **Applied**

Appendix G is the only appendix with neither a figure nor a table. It also
contains the book's cleanest stage-by-stage mapping of a product onto its own
chapters — Scopus AI's variants (Ch 11) → vector search per variant (Ch 7) → RRF
(Ch 10) → generation (the only new stage). That mapping is currently four
paragraphs of prose and it is the single most diagrammable passage in the book's
back matter. Drawn, it would say in one glance what the appendix argues in
several hundred words: everything left of the last box is this book.

Second, the evaluation section says faithfulness and attribution "are real and
measurable properties, and evaluation frameworks for them exist" and names none.
Everywhere else the book names and links its sources — this is the one place it
tells a librarian a literature exists and withholds the pointer. For someone
being asked at a renewal how a product's generated answers would be evaluated,
that sentence is the one that fails them.

**Proposed:** name two or three. Candidates worth verifying before insertion,
which the book's own practice requires in any case:

- **RAGAS** (Es et al.), a reference-free framework scoring faithfulness, answer
  relevance and context relevance.
- **ARES** (Saad-Falcon et al.), which trains lightweight judges with confidence
  intervals.
- **Attributable to Identified Sources (AIS)** (Rashkin et al.), the framework
  behind most attribution measurement, and the related *Attributed QA* work
  (Bohnet et al.).
- The **TREC RAG track**, if a shared-task anchor is wanted.

**Applied.** Figure G.1 is a five-step `query-flow` track reusing the component
Figures 12.1 and 14.1 already use, so no new CSS. Two frameworks are named
rather than four, and both were verified against ACL Anthology before insertion:
RAGAs (Es et al., EACL 2024 system demonstrations) for faithfulness, answer
relevance and context relevance, and Attributable to Identified Sources (Rashkin
et al., *Computational Linguistics* 49(4), 2023) for attribution. The pair was
chosen because it maps onto the two questions the paragraph already asks —
faithful, and attributable — and because the contrast between them is the useful
part: one is a model-prompted metric a pipeline computes, the other a human
annotation protocol. ARES and the TREC RAG track were dropped rather than
inserted unverified.

Appendix G's stated time moves from 6 to 7 minutes: the figure took it from
1,332 to 1,559 visible words.

### 1.8 Appendix F: three smaller points — **Table F.3 and deduplication applied; exercise marking open**

**Deduplication is treated as bookkeeping. — Applied as an aside, not a fourth boundary.** The
appendix lists "deduplication and any removal or enrichment before screening"
among the things to record, and Figure F.2's candidate pool is described as
"already retrieved and deduplicated", but nothing explains that near-duplicate
matching across databases is itself a recall-affecting decision that drops
records without a human eligibility judgement. Figure F.3 names three boundaries
— coverage, retrieval, stopping. On the appendix's own logic there are four.
This is a genuine content gap, not a presentational one, and it is the boundary
evidence-synthesis librarians manage most often in practice.

**Author's decision, and the right one:** deduplication is too minor and too
contingent to sit on Figure F.3 beside coverage, retrieval and stopping, where it
would carry equal visual weight. It is now an `orientation` aside after Figure
F.2 — the point in the text where the pool is first described as arriving
"deduplicated" — and it says explicitly that this is *not* a fourth boundary in
the sense of the three that follow, because it removes records thought to be
copies of ones already in the pool rather than records the workflow never
reached. The three-boundary argument is untouched. What the aside adds is the
mechanism (fields compared, at what tolerance), the failure in both directions
(a conference abstract absorbed into its journal article; a tighter rule raising
the screening burden), and the reason deduplication already appears in the
reporting list rather than only in a methods sentence.

**Table F.3 has four cells that all say "Yes".** The "Sparse possible?" and
"Dense possible?" rows read Yes/Yes and Yes/Yes. The point they carry — that
stage and representation are independent dimensions — is already made, and made
better, by Table F.1. Dropping the two rows would tighten a table that is
otherwise the appendix's best summary.

**The controlled TAR comparison is the only exercise in the book with no marking
guidance.** It specifies a corpus, what to fix, what to vary and what to record,
which is more rigour than most textbook exercises get. But the teaching notes
give worked responses and a four-criterion rubric for Application exercises I–III
and say nothing about this one — so the cohort for whom Appendix F is *core* has
an unassessed exercise, while the three exercises aimed at everyone are fully
supported. See §3.2.

### 1.9 Appendix A and E would each be transformed by one figure — **Applied**

Appendix A explains self-attention and has **no figure**. Its own worked contrast
— `bank` drawing on `loan` and `refused` in one sentence, on `river` in another —
is a diagram described in words. One panel showing the two sentences with
attention weight as line thickness on `bank` would carry the appendix, and the
book builds exactly this kind of panel in HTML elsewhere.

Appendix E is the second-longest appendix, has **no figure**, and its four tables
are dense. The natural one is the LTR loop: features and labels in, learnt
ranking function out, applied at query time to a shortlist the retriever fixed —
with the click-to-propensity correction shown as a separate input. It would also
make visible the appendix's best point, that the model was learnt offline while
the order is computed on the fly.

*Also:* Table A.1's decoder row ran to three sentences against the encoder row's
seven words. **Applied:** the cell is now "Causal attention: each position sees
only earlier positions and itself", and the parallel-training-under-a-causal-mask
point moved below the table as prose, where it can be made properly — reading
left to right constrains what each position sees but does not force training to
proceed one position at a time; generation is the sequential part.

**Applied.** Figure A.1 uses the `score-grid` / `score-card` / `score-line`
components from Figure C.3, so the only new CSS is one colour rule beside the
existing `score-*` colours. Bar widths are qualitative and the caption says so
outright — they illustrate the mechanism and are not measurements from a model,
which is the same disclaimer the Vector Similarity Lab makes about its
coordinates. Figure E.1 uses the two-track `query-flow` component from Figure
14.1 to separate what is learnt offline from what happens per query, which is the
section's own best point and was previously only a sentence. Appendix A's stated
time moves from 5 to 6 minutes; Appendix E stays at 19.

### 1.10 PubMed gets one sentence where Semantic Scholar gets a five-row table — **Applied**

Appendix E gives the 2020 Semantic Scholar system a full worked table (Table
E.4) and PubMed a single sentence: "BM25 supplies 500 candidates and LambdaMART
reorders them." For this book's audience that emphasis is the wrong way round.
PubMed's Best Match is the ranked retrieval that information-literacy and
evidence-synthesis librarians teach, use and are asked about weekly; Semantic
Scholar's historical pipeline is an illustration.

**Proposed:** expand PubMed into a parallel short table, or at least three or
four sentences covering what its features were, what the labels were, and what
the documented candidate depth means for a searcher who scrolls past 500.

---

## 2. The labs

The labs are in good shape. The arithmetic is right, `tools/test-labs.cjs`
guards the exact tour numbers (including the 1.882 baseline and the 1.143
ratio), and both pages state their own limits honestly. The suggestions below
are about what the labs *do not yet let a student do*.

### 2.1 The book's central claim has no interactive demonstration — **Applied**

*What you can now ask* nominates one thing to carry out of the book: "candidate
generation sets the ceiling on a fixed pool. Reranking and display cut-offs can
improve precision and recall at a chosen depth, but cannot add a record absent
from that fixed candidate pool." Chapters 9, 13, 14 and 15, Appendix F and
Appendix G all restate it.

Neither lab demonstrates it. The BM25 lab always shows all six records.

**Proposed:** add a "return the top k" control to the BM25 lab, with the excluded
records greyed below a visible cut line rather than removed. Then wire it into
the tour: at the step where Record D overtakes Record A, set k = 1 and ask what a
reranker could now do for Record A. The answer — nothing, because A is no longer
in the candidate set — is the book's thesis in one interaction, and the lab
currently has all the machinery needed to show it.

This would also make Appendix C's `θ` threshold tangible: the top-two min-heap in
Figure C.3 is precisely this control, and the lab could display the threshold as
the cut-off moves.

### 2.2 Tour step 3 attributes to saturation an effect that is partly length — **Applied**

The repeat slider raises Record D's `delulu` count, but it also lengthens D from
10 tokens to 27 and lifts the collection average from 29.0 to 31.8. The displayed
move from 1.882 to 2.151 is therefore saturation *minus* a length penalty. With
D's length held fixed, the same change gives 1.883 → 2.199, or +16.8% rather than
+14.3%.

The step is titled "Repetition helps, then stops helping" and its takeaway is
entirely about term-frequency saturation. Step 4 explicitly names this effect for
the *other* slider ("It changes A's length and the collection average; other
records' scores can therefore change too"), and the page header names it
globally. Step 3 does not.

**Proposed, either:** one clause in the answer text — "some of the shortfall is
length: those repetitions also lengthen D, and BM25 charges for that" — or a
"hold document length constant" checkbox for the step. The first is a five-minute
change and enough. The lab's stated principle is that every number on the page
can be checked by hand, and this is the one number whose cause is not what the
step says it is.

### 2.3 The strict-AND toggle is used once and then locked — **Applied**

Admission and ranking as separate controls is the lab's opening point and Part
I's central one. The toggle is exercised in step 1 and disabled for the remaining
five steps. Step 6 adds synonym expansion — the operation an evidence-synthesis
librarian performs constantly — but there is no way to see what strict `AND` does
to an expanded query, which is exactly where the interaction between admission
and expansion becomes visible and surprising.

**Proposed:** re-enable the toggle at step 6, and add a prediction: with
`unrealistic` added under strict `AND`, how many records survive? (None, because
no record holds all six terms.) That single result is the OR-versus-AND lesson
that Chapter 2 and Appendix F both depend on.

### 2.4 The vector lab warns and then offers no remedy

The lab's final step is excellent: Candidate A scores highest, Candidate C is the
only record satisfying the date and study-design criteria, and C scores worst.
But the lab stops there. A student's takeaway is "similarity is not relevance and
nothing can be done", where the book's actual position — Chapter 8's four
questions about a representation, Chapter 15's procurement questions — is that
this is a fixable design choice: filters, metadata, hybrid routes, a different
indexed unit.

**Proposed:** add one control, "apply the 2024-or-later limit as a hard
constraint before ranking". Candidate A drops out, C wins, and the final step
turns from a warning into the book's argument. It is the same admission-versus-
ranking distinction the BM25 lab teaches, arriving in the dense setting where
students least expect it.

### 2.5 The vector lab's dot-product step is knife-edge — **Applied**

Step 3 demonstrates magnitude outweighing angle with A at 1.736 against B at
1.798 — a 3.6% margin. The claim is correct and the test suite guards it, but a
student who nudges anything in the sandbox will flip the ordering and conclude
the lesson was wrong.

**Proposed:** raise B's tour magnitude from 1.65 to about 1.9, giving 2.07
against 1.736. Nothing else changes: step 2's cosine claim (0.914 against 0.574)
is magnitude-independent, and step 4's normalisation identity is unaffected.

### 2.6 Appendix C and the BM25 lab do not know about each other — **Applied**

Appendix C reproduces the same worked BM25 arithmetic the lab implements — the
same Lucene IDF form, the same `k1` = 1.2 and `b` = 0.75, the same
document-at-a-time traversal. The BM25 lab is linked from Chapters 3 and 4 and
from nowhere else. Appendix C links to no lab.

Meanwhile the vector lab *is* linked from Appendix D. The asymmetry is
accidental rather than principled.

**Proposed:** add a "Try it" link from Appendix C's BM25 walkthrough to the lab,
and a "the machinery underneath" link from the lab's advanced-parameters panel
back to Appendix C. Two lines, and it turns two isolated treatments of the same
arithmetic into a progression.

### 2.7 Small: the test fixture states slider bounds the page does not have — **Applied**

`tools/test-labs.cjs:44` mocks the vector lab's controls as
`angle:{min:'-170',max:'170'}`; the page declares `min="-180" max="180"`. Nothing
is asserted against the mock, so no test fails, but anyone reading the suite to
learn the lab's bounds is misled. Align the fixture, or assert against it so it
cannot drift again.

---

## 3. Teaching notes

The notes are the strongest instructor document in the repository, and "Before
you teach it: what will have moved" is the best section in it. Every asset it
names — Table 7.2, Table 9.2, Figure 9.5, Tables 11.4 and 11.5, Table 12.3,
Figure 1.3 — exists and is correctly numbered. The gaps are all of omission.

### 3.1 The re-verification list is a bullet list where the book would demand a table — **Applied**

The notes tell instructors to "record the product, mode, date of the documented
architecture and date checked separately", then present the nine items to
re-verify as an undated bullet list. The book's own standard, applied to the
book's own instructor material, would be a table.

**Proposed:**

| Item | Product and mode | Documented as of | Last checked | What would change it |
|---|---|---|---|---|
| Table 9.2, Figure 9.5 | Primo Research Assistant | | | Documented candidate cut-offs |
| Table 12.3 | Six academic tools | April 2026 | | A vendor renaming or re-scoping a mode |
| … | | | | |

An instructor then fills the "last checked" column and hands it to the next
person teaching the module. It also models the practice Chapter 15 argues for,
which is worth more than the table itself.

### 3.2 Appendix F's exercise has no marking guidance, for the cohort the notes centre — **Applied**

The notes give Application exercises I–III a paragraph each of what is being
tested, what a strong answer does, and the common wrong turn — plus worked
responses and a four-criterion rubric. Appendix F's controlled TAR comparison
gets nothing, although the notes elsewhere designate Appendix F core for
evidence synthesis and centre that cohort throughout.

**Proposed:** add a fourth exercise entry. The material for it already exists in
Appendix F: what is tested (separating representation effects from stopping
effects), the strong answer (attributing recall differences to the stopping rule
rather than the feature extractor, and reporting what each simulated stop would
have missed), and the common wrong turn (reading a WSS@95 improvement as evidence
that a live reviewer could have stopped safely). The non-coding route Appendix F
already describes — hand students two prepared screening logs and have them plot
recall against records screened — should be named here too, since most cohorts
will take it.

### 3.3 The thirteen-week course has three assessments for fifteen chapters — **Applied**

The six-week module maps each fortnight onto one application exercise, which
works. The thirteen-week course inherits the same three exercises and says
nothing about the other ten weeks. The half-day workshop has no assessment at
all, which is probably right, but is not stated.

**Proposed:** say explicitly that the three exercises are the summative
assessment and that *Check yourself* serves as the weekly formative check, or
suggest what fills the gap. The re-verification task the notes already propose —
"assign a student the job of re-checking one of these tables against current
vendor documentation" — is the obvious candidate and is currently buried at the
end of a section as an aside. It deserves promotion to an assessed exercise, with
one item per student and nine items available.

### 3.4 The notes never mention the glossary, the CHANGELOG or how to report an error — **Applied**

Three omissions, each small, each with an easy fix:

- **The glossary** is roughly 2,500 words of definitions and is the single most
  assignable artefact for an information-literacy cohort. The notes do not
  mention it. It also sits inside a collapsed `<details>` — reachable by direct
  link, which the page handles correctly, but not discoverable by an instructor
  who never opens it.
- **The CHANGELOG** is what lets an instructor tell which text a student read.
  The notes stress citing the version and never say a changelog exists.
- **How to report an error.** The notes predict that students will catch the
  instructor out on product claims, and the licence invites reuse. Nothing says
  where a correction should go.

### 3.5 The Part III discussion prompts skip Chapter 12 — **Applied**

Chapter 12 is the longest chapter in Part III at 21 minutes, carries the table
the notes single out as dating fastest, and contains the book's only original
experiment. The three "After Part III" prompts cover agency-as-a-trade,
evaluation sets and PRISMA-S, but none touches the invisible menu, the stopping
rule or what a library would need to see in an agentic trace.

**Proposed prompt:** *A vendor demonstrates an agentic mode that answers your
test question well. What could you ask to find out what it could not have done?*
That is the "invisible menu" problem, and it is the one distinction in Chapter 12
that has no discussion prompt anywhere.

### 3.6 No time estimate for the labs or exercises — **Applied**

The notes say reading-time estimates exclude lab and exercise work, and then give
no estimate for either. Someone planning the three-hour workshop has no number
for the thing they would actually run. Even rough figures — the BM25 tour is six
prediction steps, the vector tour five — would help.

---

## 4. Part III

The `part-iii-review.md` pass fixed the compressed restatements. What follows is
about coverage rather than consistency.

### 4.1 Part III has two figures across four chapters — **Chapter 15 applied; Chapter 13 declined**

| Part | Chapters | Figures | Tables |
|---|---|---|---|
| I | 1–4 | 15 | 5 |
| II | 5–11 | 30 | 13 |
| **III** | **12–15** | **2** | **12** |

Chapters 13 and 15 have no figure at all. Part III is 76 minutes of reading with
Figure 12.1 and Figure 14.1 to break it up, against Part II's thirty figures.
The visual register changes completely at the part boundary, and the effect is
that Part III reads as reference material where Parts I and II read as
explanation.

The two strongest candidates:

- **Chapter 13**, the four diagnostic lenses shown as what each stage failed to
  preserve — the argument the chapter makes in its closing section and states
  is "what separates the four lenses from a list of complaints about products".
  A single panel with the query on one side, the record on the other, and four
  labelled points of loss between them would do it.
- **Chapter 15**, the inspection trail as a trace. **Applied as Figure 15.1**,
  but walked *backwards* from the record rather than forwards, because the
  forward order is what the seven-item list already gives. The chapter's own
  test is whether a librarian can "move from the displayed record backwards",
  and where that trail stops is what a product is actually selling.

**Chapter 13's figure was considered and declined.** The chapter now carries
Table 13.1 (four lenses), Table 13.3 (what three first-stage methods preserve)
and, since §4.7, a five-item eligibility pre-check. A fourth restatement of the
same four lenses would be repetition rather than illustration, which is what
`repetition-ledger.md` exists to catch. Part III now has three figures across
four chapters; Chapter 13 is the one without, and it is also the chapter with
the most scaffolding in other forms.

### 4.2 Chapter 14 tells the reader to build an evaluation set and shows them no example — **Applied**

*What you can now ask* ends on it: "If you do one thing with it, make it the
evaluation set." Chapter 14 gives the recipe — thirty to fifty queries, known
relevant records, a fixed depth, four deliberately planted probes. It gives no
example of a filled-in row.

Compare Chapter 15, which gives three detailed tables for the *record*. The thing
the book ends by asking readers to build has less scaffolding than the thing it
asks them to write down.

**Proposed — Table 14.3, one row of a local evaluation set, filled in:**

| Query | Source | Probe type | Known relevant | Depth | Run A p@10 | Run B p@10 | Notes |
|---|---|---|---|---|---|---|---|
| `SLC6A4 promoter polymorphism depression` | Reference enquiry, Mar 2026 | Identifier / exact match | 3 PMIDs | 10 | 0.3 | 0.1 | B's expansion dropped the gene symbol |

One row is enough. It shows that the probe type is a column, that runs are
compared side by side, that the note records *why* rather than *what*, and that
the whole thing fits in a spreadsheet.

### 4.3 The same gap for per-query analysis — **Applied**

Chapter 14 makes per-query difference its central practical advice — "The
per-query differences are where the information is: a handful of queries that
moved sharply matters more than a small shift in the average" — and then shows no
per-query comparison. If Table 14.3 is added, three or four rows with one query
moving sharply against a flat average would make the point arithmetically rather
than by assertion. It is the same table, extended.

### 4.4 Chapter 12's Primo experiment is the book's best evidence and its least documented — **Applied**

*What the loop is for* is the most original section in the book. It reports:
pointing a model at the author's own Primo index over MCP, replaying real
zero-result queries from institutional search logs, beating Primo's own Natural
Language Search, and two ablations — a plain CSV of holdings reproduced most of
the result, and a much smaller model performed nearly as well.

It reports no numbers. Not how many queries were replayed, not over what period
the logs run, not which models, not how "performed nearly as well" was judged,
not what counted as success. Four examples are named (`autism`, `cost of living`,
`Rolex watches`, two misspellings).

Every other empirical claim in the book carries a date, a source and an explicit
statement of what it does not establish. Table 12.3 carries "Tested April 2026;
products have changed since" and a full paragraph of caveat. The probe in *Where
current academic tools actually sit* is linked to a written-up source and
qualified as "a single task type". This section — the author's own work, and the
strongest claim in the book — carries the least apparatus of any evidence in it.

**Proposed:** give it the same treatment as everything else. How many queries,
from what period, selected how; which models; what counted as a resolved
zero-result query and who judged it; and one sentence on what the comparison does
not establish. If the work was exploratory rather than systematic, say that
plainly and label it an observation — which costs the section nothing, because
the argument it supports ("what the loop adds is a second chance") does not
depend on a success rate.

The section is currently the one place a hostile reader could say the book
applies a lower standard to its author's evidence than to a vendor's. That is
worth closing, and it is a paragraph of work.

**Applied, using the source supplied by the author:** “What Changes When an LLM
Agent Searches Your Library Catalogue?”, 24 June 2026. The section now records
the query set (database searches from the institution's 2023 zero-result logs),
the template used, the citation and date, and the author's own framing that these
are exploratory demonstrations of failure recovery rather than a measured success
rate. Two things the source corrected rather than merely documented:

1. **The quoted NLS expansion was half its real length.** The book gave
   `(autism) OR (autistic disorder) OR (ASD)` with no ellipsis. The post records
   six terms — the three above plus `(autism spectrum)`, `(neurodevelopmental
   disorder)` and `(pervasive developmental disorder)` — all returning zero. Six
   synonyms failing is a stronger version of the book's own argument than three,
   so the correction pays for itself. The full string is now quoted, along with
   the post's footnote that both runs searched the same index, which pre-empts
   the obvious objection to the comparison.
2. **The book cited the example its own source flags as weakest.** The post
   singles out `refinituv` → LSEG as the clearest case of 2026 models answering
   2023 queries, since the rebrand postdates the query. The book used it as one
   of four illustrations with no caveat. The caveat now travels with it.

The model-tier claim checked out and is now specific: a mini model at low
reasoning effort against the frontier model at extra-high effort, with little
difference in output.

### 4.5 Chapter 15's procurement checklist asks nothing about cost, quota or deprecation — **Applied**

Table 12.4 makes "Cost and speed" the *first* row of the agency trade: agentic
search is "slower and dearer. A model is invoked to choose, and often to justify,
each successive action — and every round adds latency and tokens." Chapter 15
then asks roughly twenty procurement questions across five groups and none of
them is about money, rate limits, per-query cost, or what happens when a vendor
changes its token budget.

For a chapter whose stated job is to convert the book's distinctions into things
a library can require, and in a book that made cost half of the agency argument,
that is a real hole. Two adjacent gaps in the same list:

- **Deprecation and exit.** The checklist asks whether model, index and ranking
  changes are disclosed. It does not ask what happens to saved searches, saved
  sets and stored traces when a mode is retired. The book supplies its own
  evidence that this happens: Table 12.3 documents Ai2 Paper Finder becoming Asta
  Find Paper and Undermind's original deep search being joined by Projects,
  within the span of one version.
- **Prioritisation.** Twenty questions with no ranking is not usable in a renewal
  meeting. The chapter does this well elsewhere — Chapter 13's "the order matters
  more than the list". Marking the five or six whose answers change a purchase
  decision, as against those that merely inform one, would make the section
  survive contact with an actual meeting.

**Proposed additions to *Retrieval coverage and architecture* or a new group:**

> **What does a search cost, and what limits apply?** Is pricing per seat, per
> query or per token? What are the rate and iteration limits, and what happens
> when they are reached — a refusal, a truncated result, or a silently shallower
> search? Does an agentic mode cost differently from the ordinary one, and can
> the library see per-query consumption?

> **What happens when a mode is retired?** Can saved searches, saved sets and
> stored traces be exported before a mode is withdrawn, and how much notice is
> given? A search documented under a mode that no longer exists is not
> reproducible in any sense the library can act on.

### 4.6 Table 15.1 flattens the distinction Chapter 12 exists to draw — **Applied**

Table 15.1, the four-row summary a librarian will actually copy, has a row
labelled "Agentic control". Chapter 12 spends its first third establishing that
the useful three-way distinction is fixed / adaptive / agentic, and
`part-iii-review.md` had to repair the procurement checklist for collapsing it.
Table 15.2's expanded "Agentic orchestration" row does handle it — "Fixed and
adaptive workflows can document their rules in advance" — but the summary table
does not, and the summary is what gets copied.

**Proposed:** rename the row **Retrieval control**, and make its "what should be
recorded" cell begin with the arrangement itself: *which control arrangement
(fixed, adaptive or agentic); for an adaptive workflow, the branch taken and the
rule that chose it; for an agentic one, every query executed, each tool selected,
the observations returned, the sequence and the stopping point.* Otherwise the
record cannot distinguish a workflow whose branch varied from one whose sequence
was planned — which is the distinction the whole chapter was written to enable.

### 4.7 Chapter 13's eligibility checks are prose where they should be a checklist — **Applied**

Chapter 13 is explicit that eligibility comes first: "Before any of that,
establish that the record could have been returned at all." What follows is a
dense single paragraph covering absence from the collection, indexing lag, date
and format and access filters, passage-split evidence, Chapter 4's four
explanations for a missing typed word, and matches in non-displayed fields.

These are the cheapest and most often decisive checks in the chapter, and the
part a librarian would want at the desk. They are also the only part of the
chapter's diagnostic apparatus not given a table, while the four lenses — which
the chapter says to reach for *afterwards* — get Table 13.1.

**Proposed:** promote them to a short numbered pre-check, or a "row zero" in
Table 13.1 labelled *eligibility*. The chapter's own sentence — "These checks are
cheap, and they eliminate causes that no amount of representation work would
address" — is the argument for giving them the same visual weight as the causes
they eliminate.

---

## Two things noticed in passing, outside the review's scope

- **`CHANGELOG.md`**, in the 1.1 entry, says the book is "still three parts,
  thirteen chapters and six appendices". It is fifteen chapters and seven
  appendices, as the README correctly states and as the section eyebrows confirm.
- **`NEEDS-DECISION.md`** records the G0 and G4 gates as approved on 3 September
  2026 and says "the separate G4 gate remains required before judged reference
  substitutions" while also recording G4's approval. Worth a tidy so the file
  reads as a decision log rather than a live blocker.

---

## Suggested sequencing

**Done** (items 7 and 10 above, plus §2.2, §2.7, §1.5): the three RRF link
repairs, the Appendix C ↔ lab cross-links, the step 3 clause in the BM25 lab,
the test fixture bounds, the Appendix E retitle. All were small and none
changed an argument. `maintain.py`, `renumber_footnotes.py` and `test-labs.cjs`
all pass afterwards, and both tables of contents were rebuilt for the retitle.

**Needs an author decision on scope** (items 1 and 3): appendix navigation and
self-checks, and the Appendix B example, which is waiting on tokeniser output.

**Applied as a batch of eight**, none of which changes an argument: the reading
times (§1.2), Table F.3's redundant rows (§1.8), PubMed in Appendix E (§1.10),
the vector lab's dot-product margin (§2.5), Table 14.3 and its per-query note
(§4.2, §4.3), the sixth procurement group (§4.5), Table 15.1's control row (§4.6)
and Chapter 13's eligibility pre-check (§4.7).

Three decisions taken inside that batch, each reversible: reading times were
recalculated rather than the convention documented; Appendix E was left at 19
minutes, since 179 wpm is close to the band's floor and its tables and formulas
plausibly justify the rest; and the procurement additions became a sixth group
rather than being folded into an existing one, which required renumbering the
last group from 15 to 17.

**Larger, worth a separate pass:** only §1.4 remains — Appendix D's citations
and filter box, and the citations half is a genuine editorial question rather
than a task. Items 4 and 6, §1.9 and the Chapter 15 half of §4.1 are done.

The Appendix F deduplication gap (§1.8) is closed as an aside rather than a
fourth boundary, on the author's judgement that it does not carry the weight of
the other three. Figure F.3 is unchanged.
