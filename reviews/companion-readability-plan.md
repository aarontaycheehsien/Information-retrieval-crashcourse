# Companion materials: readability plan

Drafted 25 September 2026 on branch `fable-1` against commit `1d4f344`, with the
uncommitted README, CHANGELOG and `reviews/` reorganisation present in the working
tree. The plan was applied the same day; see [Applied](#applied) at the end for
what changed, what was done differently and what was left.

Scope is everything a reader or instructor meets outside `search-textbook.html`:

| File | Reader words | Generated from |
|---|---:|---|
| `read-this-first.html` | 4,530 | `data/digest-selections.json`, `tools/digest-template.html`, book excerpts |
| `teaching-notes.html` | 7,642 | Hand-authored, except the verification groups (`data/product-claims.json`) |
| `teaching-workshop-handout.html` | 449 | Hand-authored |
| `vendor-questionnaire.html` | 3,357 | `tools/build-vendor-questionnaire.py`, `tools/templates/` |
| `evaluation-kit.html` + two XLSX | 1,452 | `tools/build-evaluation-kit.mjs` |
| `bm25-evidence-lab.html` | 574 static + 7 tour steps | Hand-authored (tour text in `STEPS`) |
| `vector-similarity-lab.html` | 1,121 static + 7 tour steps | Hand-authored (tour text in `TOURS`) |
| `rank-fusion-lab.html` + `assets/rank-fusion-lab.js` | 564 static + 4 experiments | Hand-authored |
| `README.md` | 892 | Hand-authored (currently has uncommitted edits by someone else) |

`tools/README.md` and the WYSIWYG editor are maintainer tools and are out of scope
except where noted. Earlier reviews of this material
([teaching and labs](teaching-and-labs-review.md),
[appendices, labs and Part III](appendices-labs-part-iii-review.md)) checked
**consistency** with the book; this plan is about **ease of reading and use**.

## What the companions have in common

The labs and the workshop are the strongest writing in the repository: short
steps, a concrete prediction, one takeaway. The weaker pages share three habits
that the book's readability passes have already removed from the chapters.

1. **Caveats before the task.** Pages open with what they are *not* ("not a live
   product evaluation", "provisional", "not tested", "not a substitute") before the
   reader knows what to do. `teaching-notes.html` alone has 21 "not a …"
   constructions and four "provisional" timings. Each caveat is true; stacked at
   the top, they read as defensive and bury the first action.
2. **Generated bulk displayed as prose.** The teaching notes' verification groups
   (2,663 words, 35% of the page) repeat the string "Evidence: Unknown / not
   recorded; supporting check: Unknown / not recorded; finding: No recorded
   verification finding" 19 times. The questionnaire repeats a seven-field form
   block 30 times. Both are correct outputs of their data; neither is laid out for
   reading.
3. **Book context assumed.** The digest and questionnaire use terms (posting list,
   `b`, MaxSim, OOV, "the category error", "the verdict above") that only make sense
   after the chapters they summarise.

**Principle for every item below:** lead with the action, keep one caveat where it
changes what the reader does, and move the rest to a single "Limits" note at the
point of use or the end.

## Constraints

- **Generated pages are edited at their source.** Change the manifest, template or
  builder, rebuild, then run the page's `--check` and tests (`tools/README.md`).
  Never hand-edit `read-this-first.html`, `vendor-questionnaire.html`,
  `evaluation-kit.html` or the marked product-evidence blocks.
- **The digest's excerpts are verbatim.** Rewording a chapter summary is a book
  edit, outside this plan. The digest can change *which* passages it selects, its
  prompts, stage budgets, link text and template prose.
- **Stable anchors and URLs stay.** The book and README link to
  `teaching-notes.html#one-hour-workshop`, `#currency` and the lab pages.
- **Figures quoted in both places must move together:** tour step counts (seven,
  seven, four experiments), the eight-point rubric, nine verification groups,
  nineteen core questions, 45-minute route.
- The README has uncommitted edits by another author; coordinate before touching it.

## Priorities

| # | Change | File | Effort | Reader gain |
|---|---|---|---|---|
| P1 | Render verification groups as a compact table | teaching notes (via generator) | M | High |
| P2 | Put the task menu before the preamble | teaching notes | S | High |
| P3 | Trim the digest and fix orphaned references | read-this-first (manifest/template) | M | High |
| P4 | Give each questionnaire question a "listen for" line; collapse repeated form fields | vendor questionnaire (builder) | M | High |
| P5 | Split the evaluation guide's six steps into do / detail | evaluation kit (builder) | S–M | Medium |
| P6 | Lab intros and two overloaded tour answers | vector and BM25 labs | S | Medium |
| P7 | Reorder the README for first-time readers | README | S | Medium |
| P8 | Cross-cutting: caveat pass, link text, consistent navigation | all | S | Medium |

Recommended order: P2 → P1 → P3 → P4 → P5 → P6 → P7 → P8 (P2 is a quick win that
changes how the rest of the teaching notes reads; P7 waits for the README edits
in progress to land).

---

## P1 — Teaching notes: make the verification groups scannable

**Problem.** "Before you teach it: what will have moved" lists 62 claims as
paragraphs: a machine ID (`apache-lucene-bm25`), the claim, then a status sentence.
For the 19 unchecked claims the status is the same 20-word string. The four
Lucene-family claims repeat the same claim text four times. An instructor looking
for "what do I need to recheck before Chapter 9" has to read ~2,600 words.

**Proposal** (in `tools/build-product-claims.py` / its teaching-notes block):

- One `<details>` per group, closed by default, with the group's guiding question
  as the `<summary>` and a count: *"Primo Research Assistant pipeline — 7 claims,
  all checked 2026-09"*.
- Inside, a table: **Claim · Evidence date · Last checked · Finding**. Show "—" for
  unknown rather than "Unknown / not recorded"; state once, above the groups, what
  "—" means.
- Move the claim ID to a small secondary column or `title` attribute; it is for
  corrections, not for reading.
- Collapse identical claims across engines into one row (*"Lucene, Elasticsearch,
  Solr, OpenSearch: BM25 is the default text similarity"*) if the data model
  permits; otherwise keep rows but keep them one line each.
- Keep the instructions paragraph (what to record, pass it on) above the groups,
  cut to three sentences, and keep `#currency` as the section anchor.

**Check.** `tools/check-product-claims.py`, `tools/test-product-claims.py`,
`tools/check-product-claims.mjs`; confirm the book's `teaching-notes.html#currency`
link still lands on the section; print preview expands `<details>`.

## P2 — Teaching notes: menu first, preamble second

**Problem.** Six paragraphs (digest, workshop, evaluation kit, questionnaire,
audiences, licence) precede "Choose what you need". Most restate what the menu
links to.

**Proposal.**

- Subtitle → "Choose what you need" menu immediately.
- Fold the digest, evaluation-kit and questionnaire paragraphs into one-line
  descriptions on the relevant menu items or into the sections they serve (the kit
  under *The application exercises*, the questionnaire under *Before you teach it*).
- Keep the audience sentence under *Choose the emphasis for the cohort*; move the
  licence line to *Figures, and reusing them* (which already repeats it).

**Also in the teaching notes** (smaller):

- *Using the three labs* reads in the wrong order (Rank Fusion begins "Before the
  exercises…" and its timing sentence explains itself). Make it a three-row table:
  **Lab · Use after · Tour length · Protect time for**. The BM25 step-6 advice
  becomes the last cell.
- State once, in *Run of session*, that all timings are first-run estimates; drop
  the repeats in the labs and half-day sections.
- *Three longer course shapes*: the six-week paragraph under the table ("Part II
  covers seven chapters…") is a trimming route; label it *If Part II is too heavy*.
- *Worked responses and a short rubric*: the rubric sentence appears twice (before
  and as the table caption). Keep the caption.

## P3 — Read this first: shorter route, no orphaned references

**Problems.**

- **Stage 3 is overloaded.** "Mechanisms" carries eight chapter summaries plus a
  distinction panel (~2,000 words, nearly half the digest) in a 15-minute budget;
  stages 1 and 5 carry a few hundred words each.
- **Bridge paragraphs repeat the next heading.** Each summary ends with the book's
  hand-off ("The next chapter opens the stored object itself…"). In the book they
  link chapters; in the digest the next chapter's heading follows immediately.
  At 40–70 words each they are roughly 15% of the text.
- **References to context the digest omits:** "This is the one collapse of this
  kind…", "The verdict above sets out…", "Five confusions are left. Part I settled
  a sixth…", "the category error".
- **Twenty identical links** reading "Read the full explanation and evidence" —
  poor for screen readers and scanning.
- **The opening meta-paragraph** (word count, 200 wpm, "provisional suggestions,
  not tested completion times", evaluation outside the session) is the first thing
  read.

**Proposals** (manifest, template and selector changes; no excerpt rewording):

1. Exclude each summary's trailing bridge paragraph by default; keep it only for
   Chapters 4 and 12, where it marks a part boundary. Update the guarded selectors
   and tests deliberately (`tools/README.md` requires this).
2. Rebalance stages: split Mechanisms into *Representations* (Ch. 5–8) and
   *Pipelines* (Ch. 9–12), or move Chapter 12 to Professional practice. Re-derive
   the budgets from the word counts the builder already computes.
3. Replace the two panel lead-ins that refer to absent context with a one-line
   template-authored framing ("A result screen can settle one confusion; the five
   below need the mechanism first"), or select the panels without their lead-in
   paragraphs.
4. Generate descriptive link text: "Chapter 7 in full", "Distinction: vector search
   ≠ semantic search". Keep one uniform label only if a test depends on it.
5. Reduce the opening to one sentence of what the route is and one of how long it
   takes; move the method (200 wpm, provisional) to a footnote-style line under the
   route list.
6. Move the evidence register in stage 5 below "The three puzzles", so the reader
   meets the resolution before its sources.

**Check.** `build-digest.py --check`, `test-digest.py`, `check-digest.mjs`
(desktop, mobile, print screenshots under `outputs/digest/`). Confirm the
displayed word count and the teaching notes' and README's "45-minute" still hold,
or update all three.

## P4 — Vendor questionnaire: easier to use in a live meeting

**Problems.**

- Questions are written for someone who has read Chapter 15. Q01 packs four
  sub-questions; Q13 lists a dozen export items in one sentence. A librarian in a
  demonstration has no cue for what a good or evasive answer sounds like.
- The seven-field response block is printed after every question — 30 times — so
  the questions themselves are hard to scan on screen.
- The specialist sections are inconsistent: E01–E04 headings are fragments
  ("Before RRF:") with the question in the body; G01–G07 put the whole question in
  the heading and have no explanatory body.
- "Supported retrieval inputs" sits unnumbered before Q01 and is easy to skip.

**Proposals** (builder and template):

1. Add one **"Listen for"** line per question: what a documented answer contains
   and what a non-answer sounds like (e.g. Q04: *a named model without a stage —
   "we use GPT" — does not answer this*). Source each line from the book's existing
   Chapter 15 text where possible.
2. Break Q01, Q02, Q12 and Q13 into lettered sub-prompts (a, b, c) so answers can
   cite "Q13c".
3. On screen, show questions first with the response block collapsed or as a
   compact grid; keep the full writing space in print CSS only.
4. Normalise E and G items to the Q pattern: short question heading, one-sentence
   context, source link, "already covered by" pointer.
5. Number the retrieval-inputs block (Q00 or "Before Q01") so it is included in
   the question count and the action log.
6. Put a 19-item "question list only" summary at the top, for sending to a vendor
   in advance.

**Check.** `test-vendor-questionnaire.py`, `check-vendor-questionnaire.mjs`;
print preview on A4 still paginates cleanly; README and book still say "nineteen".

## P5 — Evaluation kit guide: separate the action from the edge cases

**Problem.** Each of the six steps is a single dense paragraph mixing the action
with edge cases (duplicates within a run, empty lists, short lists, blank vs zero
ranks). Step 4 is 90 words, of which the action is ten.

**Proposals** (builder):

- Each step: one bold imperative line, then a short "If…" list for edge cases.
- Move the capture-depth arithmetic (three results at depth ten → count 3, depth
  10) into *What the scores count*, where the same rule is already explained.
- Put *A completed, controlled example* before *Six steps* — the page already
  tells readers to open the example first.
- Consider a short "Start here" worksheet in both XLSX files that points to the
  guide URL and names the four sheets; today the workbook's only instruction is a
  one-line banner on *Comparison*.

**Check.** `test-evaluation-kit.py`, `test-evaluation-kit.ps1`,
`check-evaluation-guide.mjs`; screenshots under `outputs/evaluation-kit/`.

## P6 — Labs: lighter intros, two overloaded tour answers

**Vector Similarity Lab**

- The intro paragraph carries four ideas plus the sharing tip, then a second
  paragraph about signed angles that means nothing before the first step. Cut the
  intro to what the lab does and the tour/sandbox split; move "signed angles" to the
  angle control's help text and the sharing tip to the sandbox.
- The sandbox's "Optional: can the relevant record reach the next stage?" block
  explains the experiment before the reader has loaded it; move the explanation
  into the reveal after *Load cutoff experiment*.
- Tour step 7 reports Candidate C's cosine as −0.530 with no warning that the
  relevant record is the *least* similar; add a half-sentence pointing to the
  appendix note on negative scores.

**BM25 Evidence Lab**

- Step 1's intro has two short sentences that read as disclaimers ("Boolean also
  supports OR and NOT. Admission rules and BM25 scoring are separate controls.");
  fold them into one. Its takeaway mentions "any-match admission" before the term
  is introduced; say "With the toggle off".
- Step 3's answer spends a paragraph on the length side effect (15% vs 17%).
  Keep it, but as a secondary "Why not exactly…?" disclosure.
- Step 7's answer is three paragraphs; move the admission-toggle paragraph into
  its own short closing note or an eighth, unscored "Try this" step. (If a step is
  added, the "seven-step" count in the book, teaching notes and changelog must
  change with it — prefer the closing note.)

**Rank Fusion Lab** is already short. Only: the header says "Both input depths
are 3; c = 60; output depth is 4" in one line — present as a four-item definition
list matching the control labels below.

**Check.** `node tools/test-labs.cjs`, `test-vector-tour.cjs`,
`test-rank-fusion.cjs`, `check-rank-fusion.mjs`; a mobile-width pass in the
browser preview.

## P7 — README: first-time reader first

After the in-progress README edits are committed:

- Move **Read this first** to the second paragraph, directly after the textbook
  link; it is the intended entry point and currently appears seventh.
- Group the companions into one short list (labs, evaluation kit, questionnaire,
  teaching notes) instead of a paragraph each.
- Move the maintenance paragraph ("sole maintained edition… generated from
  maintained mappings") and the repository map under a **For contributors**
  heading; "Migration preserves the book's existing evidence" is internal.
- *For instructors* is currently an `###` under *Licence and reuse*; promote it to
  `##` and place it before the licence.
- Use one link style: relative links (they work on GitHub and the Pages site).

## P8 — Cross-cutting pass

- **Caveat audit.** For each "not a…/provisional/stipulated" sentence, keep it only
  where it changes the reader's action; otherwise merge into a single *Limits*
  line. Target: halve the count in the teaching notes and digest.
- **Consistent top navigation.** Every companion should offer the same three
  links: Textbook (relevant chapter) · Teaching notes · the other companions. The
  BM25 lab currently has only a back link.
- **One name per thing.** "Candidate limit", "k", "cut-off/cutoff", "output
  depth" and "boundary" vary across the three labs; align hyphenation (the book's
  choice) and label controls with the same term the tour uses.
- **Handout.** Already clear. Only move the printing instruction off the printed
  page (screen-only) so it does not consume page 1.

## Not in this plan

- Rewording any book excerpt shown in the digest (book edit, separate pass).
- Tooling docs (`tools/README.md`) and the WYSIWYG editor.
- New content (extra lab steps, new exercises) beyond the optional "Start here"
  worksheet.

## Verification for the whole pass

1. Rebuild every generated page and run each `--check`; no stale output.
2. Run the full test set listed in `tools/README.md`.
3. Link check: all companion → book and book → companion anchors resolve
   (the 18 September review found 25 + 11 + 5; recount).
4. Recount cross-file figures: seven-step tours, four experiments, nineteen core
   questions, nine groups, eight-point rubric, 45 minutes.
5. Browser preview at desktop and 375 px widths, and print preview for the handout,
   questionnaire and teaching notes.
6. Record applied changes in `CHANGELOG.md` and append an *Applied* section here.

## Applied

Applied 25 September 2026 on `fable-1`, in seven commits after `e69ba00`:

| Commit | Item | Result |
|---|---|---|
| `b7af628` | P1, P2 | Teaching notes: menu first; the six-paragraph preamble folded into the menu, *Choose the emphasis* and *The application exercises* (new `#product-review` anchor); one timing caveat; labs as a table; claim groups as one-line claims with a status line and a per-group count in the summary. Page 7,642 → 6,771 words. |
| `0b73ba3` | P3 | Read this first: hand-offs dropped except Chapter 10's substantive one; interface and vocabulary panels lose the paragraphs that referred to absent context, with a short authored `lead` in their place; six stages (5 + 9 + 9 + 9 + 8 + 5 minutes); descriptive link text; evidence register moved below the puzzle verdicts. Reading text 4,260 → 3,593 words (page 4,530 → 3,850). |
| `b808bae` | P4 | Questionnaire: authored "Listen for" cue on all 30 questions; bodies made only of questions lettered (Q01, Q02, Q03, Q12, Q13, Q15); answer spaces hidden on screen behind a toggle, always printed; question-only list for sending ahead; intake headed "Before Q01". Print still 13 pages (core) and 19 (all sections). |
| `a7b64b9` | P5 | Evaluation guide: worked example before the six steps; each step one action plus edge-case bullets; short-list arithmetic left only in *What the scores count*. |
| `887e036` | P6 | Vector lab intro, hints and cut-off experiment reordered; step 7 notes C is least similar. BM25 step 1 intro and takeaway, step 3 aside as a disclosure, step 7 closing experiment set apart. Rank Fusion example settings as a list. Step counts unchanged. |
| `64a4109` | P7 | README: Read this first straight after the textbook link, companions as a list, maintenance notes under their own heading, *For instructors* promoted and moved before the licence. Committed around the other author's uncommitted repository-map block, which is untouched. |
| `72d5e7a` | P8 | Visible lab text uses "cut-off", the book's majority spelling (31 uses to 8); BM25 and vector labs link to the other labs and teaching notes. |

A final commit adds the changelog entry and this record.

### Done differently

- **Links in the README are absolute, not relative.** P7 proposed relative links,
  but the README is read on GitHub, where a relative `.html` link opens source, not
  the page. The test that required `(vendor-questionnaire.html)` now accepts either.
- **The questionnaire's intake is not numbered Q00.** Numbering it would change
  the "nineteen core questions" quoted in the book, README and notes; it is headed
  "Before Q01" instead.
- **Only whole paragraphs are dropped from the digest.** The builder's `omit`
  names paragraphs by their opening words and fails if one no longer matches, as
  the other selectors do.

### Not done

- **"Start here" worksheet in the XLSX files.** Both workbooks already carry a
  guide link and a banner, and adding a sheet changes the four-sheet structure the
  tests and guide assume. Left for a workbook release.
- **Evaluation kit keeps "cutoff".** Its guide quotes workbook labels ("Cutoff k");
  changing one without the other would mismatch.

Identical claims about several products (the four Lucene-family BM25 claims)
now share one row in the teaching notes, as P1 proposed.

### Verification

`build-product-claims.py --check`, `test-product-claims.py`, `check-product-claims.mjs`;
`build-digest.py --check`, `test-digest.py` (new checks for dropped hand-offs,
orphaned phrases, link text, register order and a missing `omit` target),
`check-digest.mjs`; `build-vendor-questionnaire.py --check`,
`test-vendor-questionnaire.py` (word-for-word check of lettered bodies),
`check-vendor-questionnaire.mjs` with PDF page counts; `test-evaluation-kit.py`,
`check-evaluation-guide.mjs`; `test-labs.cjs`, `test-vector-tour.cjs`,
`test-rank-fusion.cjs`, `check-rank-fusion.mjs`. All pass. Browser checks ran
with the bundled Playwright runtime and Microsoft Edge.
