# Part III (Chapters 12–15): second consistency review

Reviewed 9 September 2026 against commit `6f95554` ("Improve Part III readability and continuity with Part II"). Nothing has been applied; this is a findings list. Line numbers refer to `search-textbook.html` at that commit.

The first Part III review (`part-iii-review.md`, 6 September) found compressed restatements that dropped a qualification. This pass finds a different failure mode: the readability rewrite in `6f95554` shortened or relocated several passages and left four cross-references pointing at things that are no longer there — or never were. Two of the four were introduced by that commit.

Structural checks are clean: `tools/maintain.py` reports "no changes needed" and "no problems found"; `tools/renumber_footnotes.py` reports "already in order (55 footnotes)"; all 120-odd anchor targets in Part III resolve, and Part III's footnotes 42–49 run in order. The arithmetic in §2802–2804, the averages in Table 14.3 (0.30 → 0.33), the three puzzle figures in the epilogue and Part III's 76-minute reading total were each recalculated and are correct.

## Substantive

### 1. Chapter 14 cites an information need that does not exist

**Location:** `search-textbook.html:2802`. Introduced by `6f95554`.

> Use the **AI in academic libraries** information need from Chapter 1 to make the distinction concrete.

The string "AI in academic libraries" occurs exactly once in the whole file — here. Chapter 1's worked information need is the open-access citation advantage one at `1196`: a reader who "needs empirical studies published since 2024 that measure this advantage". That is also the need Chapter 11 and Chapter 12 return to, and the one Chapter 15's record template at `2963` returns to.

The commit replaced "The metrics make that asymmetry arithmetic. Suppose ten papers are known to be relevant…" with a version that anchors the example to a named need. The anchoring is a good move; the name is wrong. Reading it as the open-access citation advantage need makes the paragraph correct and consistent with the rest of Part III.

### 2. Figure 12.1 contradicts §2551 on output format, and its caption contradicts the figure

**Location:** `search-textbook.html:2492–2521`; compare `2551` and Table 12.2 at `2539`.

The figure's fourth box reads **Records** for the fixed and adaptive tracks and **Records or report** for the agentic one. Chapter 12 spends two paragraphs denying exactly that association:

> Output format is separate: an agentic search may return a ranked list, while a fixed workflow may write a report. (`2551`)

and Table 12.2 has a *Scripted deep research* row whose main output is "Report or answer". The figure hands agency an output property the chapter has just taken away from it. The subtext of all three boxes is about the path ("one path, documented once", "path chosen per question"), not the output, so the fix is to make the bold label identical across the three tracks and let the subtext carry the difference.

The caption then compounds it:

> The three arrangements differ **only at the third box** … The retrieval inside the second box is identical in all three.

Two boxes falsify it. The fourth differs, as above. The second differs too: "Run the preset steps — the same operations, in the same order, for every question" against "Run the search — a first pass returns a yield". The claim the caption wants is the right one, and it survives if the figure is made to match it.

### 3. Chapter 15 attributes to Table 12.3 something Table 12.3 does not record

**Location:** `search-textbook.html:3206`; compare Table 12.3 at `2561–2566`.

> **Table 12.3** records two products renaming or re-scoping a mode inside a single year.

Table 12.3 records neither renaming nor any date beyond its own "Tested April 2026" note. It distinguishes "Undermind's original deep search" from "Undermind Projects", which is one vendor re-scoping. The other case the sentence seems to want — Paper Finder becoming Ai2 Asta Find Paper — is stated in the body at `2531`, not in the table. A third candidate, Scopus AI adding a deep-search mode, is in Chapter 1 at `1170`. Nothing anywhere supports "inside a single year".

This matters more than a normal miscitation because the procurement question it supports ("What happens when a mode is retired?") is meant to be evidence a librarian can put in front of a vendor. Either point the reference at `2531` and drop the count and the interval, or state the two cases in the sentence itself.

### 4. Chapter 1 promises Part III will examine a product Part III never mentions

**Location:** `search-textbook.html:1170`, linking to `#where-current-academic-tools-actually-sit` (`2556`).

> Web of Science Research Assistant now describes itself as *agentic* — a claim **examined**, along with where these tools actually sit, near the end of this book.

Chapter 12 examines Undermind, Consensus Deep Search, Ai2 Asta Find Paper, Elicit, SciSpace, Scopus AI, Scite and the Wiley AI Gateway. Web of Science Research Assistant appears nowhere in it; its only other substantive appearance in the book is Chapter 11's query-transformation table at `2464`. The forward reference resolves to a live anchor, which is why `maintain.py` does not catch it, but the promise is not kept.

Either Table 12.3 gains a row (which would need testing this review cannot supply), or Chapter 1's verb weakens to something the chapter delivers — the *kind* of claim is examined there, not this product's.

## Smaller

### 5. Table 13.1's third column points forward, not back

**Location:** `search-textbook.html:2631`; column heading at `2627`.

The heading is "Earlier chapter to remember". Three of the four rows link only to earlier chapters. The OOD row links "Retrieval training" to Chapter 6 and "evaluation transfer" to Chapter 14's *Test collections, and what a benchmark number is worth* — a chapter the reader has not reached. Either retitle the column ("Where this was set up") or move the evaluation link into the remedy cell, which already says "compare performance on a local query set".

### 6. Table 14.2's caption calls precision@k rank-aware, five lines after the text denies it

**Locations:** caption at `2865`; body at `2857`.

> Table 14.2 — **Rank-aware** metrics …

> Its weakness is that it treats every position inside the cut-off as equal. A relevant record at rank 1 and the same record at rank 10 score identically. (`2857`)

The body is right and the point is load-bearing: precision@k is introduced precisely as the measure that stops short of being rank-aware, and MRR, MAP and nDCG are then introduced as "three conventional relevance-only refinements" of it. The table's own row for precision@k lists "Order within the cut-off" under *What it ignores*, so the caption contradicts its own first row. "Metrics for a ranked list" would carry the same meaning without the clash.

### 7. A dangling referent in the evidence-synthesis note

**Location:** `search-textbook.html:2848`.

> That boundary is not unique to dense retrieval; BM25 and other ranked methods can impose it too. **This is where it costs most:** the empirical question is whether the complete workflow has adequate sensitivity for the task.

The colon promises to say where the cost falls and instead changes subject. Neither "this" nor "it" has a clear antecedent — the boundary, ranked retrieval, or high-recall evidence synthesis are all available readings. The paragraph is in a dated methodological note where precision is doing real work.

### 8. The caveat at §2572 is attached to the wrong study

**Location:** `search-textbook.html:2572`; compare `2557` and `2560`.

Section 2557 describes a single-task probe ("find the papers that could have been cited … but were not"), written up as *Deep Research, Shallow Agency*. Section 2560 says sorting the tools "is a separate exercise, done in April 2026", and Table 12.3 reports that exercise. Section 2572 then opens "One caveat about the evidence. That testing used a single task type … A tool could fail it" — which is the probe, not the sorting exercise — before closing "Treat the table as an illustration". Two studies, one pronoun. Naming the probe would settle it.

### 9. Chapter 15 opens twice with the same sentence

**Locations:** `search-textbook.html:2953` (chapter orientation) and `3143`.

> Most librarians will never train a retriever. They will license one, teach with it, document searches performed in it…

> Most librarians will never train a retriever. They will license one, or license a database containing one.

Both openings work; having both, 190 lines apart in one chapter, reads as an editing residue rather than a deliberate return. The repetition ledger's usual test — does the second occurrence do new work? — is passed only by the second half of `3143`.

### 10. The closing check names four of the six collapses

**Location:** `search-textbook.html:3243`; compare the Preface at `1044` and the checklist at `1099`.

The epilogue says the Preface "promised six collapses would be named where they could be checked. This is the point to go back and check", then offers four: vector/embedding, semantic/dense, top-*k*, and neural IR. Two are missing, including the one the book leans on hardest — *lexical search is broader than Boolean search*, which Chapter 4 calls "the most important thing this book does early". The four it does offer are worth keeping; the sentence should stop claiming to be the check on all six, or should carry all six.

Note also that "a vector need not be an **embedding**" matches neither checklist entry as worded: item 4 is "A vector need not be dense or semantic" and item 6 is about *embedding search* and *vector embedding search* as labels. The epilogue's phrasing is defensible on its own but is not the distinction the reader was told to check.

## Found in passing, outside Part III

### 11. The Preface's reading-time totals no longer match the chapters

**Locations:** `search-textbook.html:1080` and the Part I divider at `1092`.

Both say "about 59 min" for the Preface and Part I. The chapter meta values now sum to 62: Preface 8, Chapter 1 17, Chapter 2 13, Chapter 3 11, Chapter 4 13. Chapter 1 was 14 minutes before `c8fd1ae`, which is where the three minutes came from. Part II (99) and Part III (76) are both still exact.

### 12. `6f95554` has no CHANGELOG entry

The three sibling readability passes — `a6cede8` (Chapter 11), `6e7dc5b` (Chapters 5–9) and `c8fd1ae` (Chapters 1–4) — each updated `CHANGELOG.md`. The Part III pass did not, so the changelog now describes three quarters of the readability work.

## What was checked

- Chapters 12–15 read in full, plus Application exercises II and III, the Part III divider and carried-forward recap, and *What you can now ask*.
- Every internal link in Part III (about 120, after deduplication) resolved to its containing chapter or appendix and compared against its link text. All targets exist; findings 4 and 5 are the two whose text and target disagree.
- Arithmetic re-derived: §2802–2804 (precision@10, recall@10, candidate-pool recall), the Chapter 14 self-check at 6 ÷ 20, Table 14.3's row values and both averages, and the reading-time sums for all three parts.
- Factual cross-checks against Chapter 1: the three puzzles' figures (9.4 million / 1,000; 13 / 35,300), the August 2026 and 2025 dates in the epilogue, and the axes of Figure 1.4 — Ai2 Asta Find Paper is correctly placed in the upper-left quadrant at `2571`.
- Citations spot-checked for internal consistency only, not against the sources: Furnas et al. 1987, Jeong et al. 2021, Chen et al. 2022, Thakur et al. 2021, Lupart et al. 2023, Liu et al. 2025, Weller et al. 2024, Zhang et al. 2024.
- `python tools/maintain.py` and `python tools/renumber_footnotes.py`, both clean.
- Findings 1–4 are the ones worth acting on before the next release. Findings 5–10 are one clause or one caption each.
