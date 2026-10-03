# Part III (Chapters 12–15): consistency review

Reviewed 6 September 2026 against commit `2675662`. Unlike the chapters 5–11 review, the findings below **have been applied** to `search-textbook.html` in the same commit; line numbers refer to the file as reviewed, before revision.

Part III is broadly consistent. The problems are all of one kind: a compressed restatement — in a table cell, a summary bullet or a procurement question — that drops a qualification the body text established correctly. Five of the seven repairs simply import wording that already exists elsewhere in the book.

## Findings applied

### 1. Table 12.4 explained the cost of a fixed or adaptive workflow with a reason that contradicts Table 12.1

**Locations:** `search-textbook.html:2480` and `2483`; compare Table 12.1 at `2415`.

The cost row said fixed and adaptive workflows are cheap "so nothing has to be reasoned out at query time." Table 12.1 says the branch chooser in an adaptive workflow "may be a written rule, classifier or model" — so something may well be reasoned out per question. The unanticipated-tasks row had the matching problem: "it does not adapt — it runs the script anyway" is true of a fixed workflow and false of an adaptive one.

The verdict of both rows is right; only the justification was wrong, so the repair keeps the comparison and fixes the reason.

**Applied:** "Cheaper and faster. Most of the sequence is decided in advance; at most a branch is selected at query time, so little has to be reasoned out per question." And: "**Fails.** Both handle only the cases their designer foresaw. A fixed sequence runs the script anyway; an adaptive one can choose only among the branches it was given."

### 2. Agent stopping was stated too absolutely for the harness definition

**Location:** `search-textbook.html:2490`; compare the harness definition at `2424` and the procurement question at `2990`.

"An agent stops because a model decided that what it had was good enough" ignores the harness, which the book itself defines as setting "how many rounds it is allowed, when it must stop." The heading — *the stopping rule is a relevance judgement nobody wrote down* — still earns its place, and the paragraph's argument is about the model-chosen case, so the qualification belongs in one sentence rather than in a rewrite.

**Applied:** "An agent may stop because its harness makes it — a round limit, a budget, a user's interruption — but the consequential case is the other one: a model decided that what it had was good enough…"

### 3. Chapter 14 said hybrid retrieval and agentic loops raise recall, where the rest of the chapter says they can

**Locations:** `search-textbook.html:2686` and the Figure 14.1 caption at `2717`; compare `2676`, `2680`, the chapter summary and the self-check answer, all of which use "can expand" or "may still add it."

An extra route or round raises cumulative candidate recall only when it contributes relevant records the other routes missed. Duplicates and irrelevant additions enlarge the pool without raising recall, and can push relevant records below the displayed cut-off, so recall at a fixed depth can fall. The paragraph at `2686` was the only place in the chapter stating this unconditionally.

**Applied:** both verbs changed to "can raise", plus: "In both cases the gain is real only when a route or a round contributes relevant records the others missed; duplicates and irrelevant additions enlarge the pool without raising recall, and can push relevant records below the displayed cut-off." The figure caption now reads "only if it adds relevant candidates the other routes missed."

### 4. The Chapter 14 summary flattened the precision–recall trade the body had qualified

**Location:** `search-textbook.html:2811`; compare `2678`.

The body says changing the cut-off on one ranking trades precision against recall, and that this "is not an unavoidable trade between different systems. A better representation or ranking can improve both at a chosen depth." The summary said only that they "trade against each other." The replacement keeps the point about library tasks sitting at opposite ends of the trade, which is worth retaining.

**Applied:** "Changing the depth returned from one ranking trades precision against recall, and library tasks sit at opposite ends of that trade; a better system can improve both at the same depth."

### 5. The procurement question on indexed units conflated the index with the pipeline

**Location:** `search-textbook.html:3002`; the correctly qualified statement is in Chapter 8 at `2019`, not Appendix G.

An abstract-only index cannot *match* full-text-only evidence at that retrieval stage, but the pipeline may fetch it afterwards — which is exactly what Chapter 8 says: "A later fetch of full text, neighbouring passages or a parent section may nevertheless supply that evidence. Ask separately what the system indexes, what it retrieves and what it supplies as context." A vendor can answer the unqualified question truthfully and leave the buyer misinformed, so the checklist is the worst place for the compression.

**Applied:** "A product whose index holds only abstracts cannot match evidence that occurs only in the full text at that retrieval stage, however sophisticated its vectors are. Ask separately whether it later fetches the full text, and what it passes on as context."

### 6. The procurement checklist sliced control in a way that files a model-chosen branch under agentic

**Location:** `search-textbook.html:2990`; compare Table 12.1 at `2414–2416`.

"Rules written in advance" versus "selected by a model" is not the chapter's distinction. Chapter 12 cuts between selecting among enumerated branches — by rule, classifier *or* model — and planning a sequence of actions. The checklist wording made adaptive branching sound agentic, which is the specific confusion Chapter 12 exists to prevent.

**Applied:** "Is the sequence fixed in advance, chosen from branches the designer enumerated — whether a rule, a classifier or a model picks the branch — or planned by a model from what it has observed?"

### 7. Two smaller repairs

**Chapter 13 diagnosis preamble (`2589`).** "Confirm the record was eligible and inside the result boundary" asks for something the interface usually cannot show, and treats the boundary question as a precondition rather than as part of the diagnosis. Note that falling outside the candidate set does not by itself identify the cause — vocabulary mismatch is precisely why a record fails to be retrieved — so the repair says which stage to interrogate rather than claiming the diagnosis is settled. **Applied:** "Establish whether the record was eligible at all, and whether it crossed the candidate boundary or was merely ranked below where you looked. The two point at different stages."

**Chapter 14 probe 2 (`2791`).** A full-text phrase that returns nothing is confounded: the index may not cover full text, or the record may have been retrieved and buried. **Applied:** "which is evidence about the indexed unit rather than about the ranking."

## Considered and not applied

**The glossary's agent-terminology row (`3386`).** The proposal was to qualify "a process that may plan, reformulate, search repeatedly, follow evidence or call several tools" with Chapter 12's distinction. Declined: that row sits under the column heading "What the label usually describes", whose job is to report loose vendor usage, and its "Read in this book" column already links to *Fixed, adaptive and agentic*. Qualifying it would blur what Table D.1 is for.

## What was checked

- Read, against the Part III review supplied for assessment: Chapter 12 in full, Chapter 13's diagnosis section, Chapter 14's precision–recall material and probe list, Chapter 15's procurement checklist, Chapter 8's indexed-unit section and Table D.1 in the glossary. Each finding was verified in the file before revision rather than accepted as reported.
- One attribution in the source review was corrected: the qualified indexed-unit statement is in Chapter 8, not Appendix G.
- `python tools/maintain.py` — "no changes needed", no problems found (asset numbering, both tables of contents, anchors, duplicate IDs, internal links, stale cross-references).
- `python tools/renumber_footnotes.py` — "already in order (55 footnotes)".
- Two of the three items the source review found sound were re-checked and agree: the Chapter 13 diagnosis framework, and Appendix F's retrieval-versus-screening distinction at `3590–3591`, which matches Chapter 11 at `2236`. Exercise III's separation of seed recovery from precision@10 was not independently re-verified in this pass.
- Net effect is about sixty words across Part III. Each repair is confined to one clause, table cell or summary bullet, because the risk in a pass of this kind is sanding the declarative voice down into hedging.
