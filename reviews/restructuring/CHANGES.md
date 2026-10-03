# Restructuring change log

## Phase 0 — baseline and reconnaissance

- Target snapshot: Git `65469bbd4e7aa811db0f0511ae10a4386299308f`; book SHA-256 `c434f1042446ac8b9749fc3d3f9475e893b487df82b0661fc3087f96e4b19718`.
- Added the read-only `audit.py`, `baseline.json`, `recon.md`, and gate record.
- Confirmed 525 unique IDs, zero duplicates, zero broken internal href targets, 55 globally sequential footnote pairs, and 36 legacy anchors.
- Adopted 200 visible chapter/appendix references and 3,474 visible Appendix F words as the approved baselines.
- Corrected the audit's initial single-digit chapter-number pattern during Phase 3 preparation; Chapters 10–13 are now included, bringing the visible reference total to the expected 200. Regenerated the baseline and Phase 1/2 audits from their byte-exact Git snapshots.
- Classified the toy-mixture section as an LTR illustration that remains in Appendix E.
- Confirmed that the moved RRF section includes `Table E.1`, which will become `Table 10.1`.
- G0 approved by the user on 2026-09-03.

## Phase 1 — structural moves

- Split old Chapter 5 at `Model tokens are not indexed terms`, keeping `embeddings` for the revised Chapter 5 and adding `retrieval-encoder` for the new Chapter 6.
- Split old Chapter 8 after `Neural information retrieval is broader than dense retrieval`, keeping `reranking-and-hybrid` for reranking and adding `hybrid-and-fusion` for the new hybrid/fusion chapter.
- Moved the RRF section and its worked `Table E.1` into the new hybrid/fusion chapter, after `Why hybrid retrieval remains attractive`.
- Preserved the old RRF slug as a `legacy-anchor` at its Appendix E location; the moved heading uses `how-reciprocal-rank-fusion-combines-ranked-lists`.
- Divided the original chapter-close points and self-checks by topic. Current self-check counts are 0 / 3 for the split Chapter 5 pair and 1 / 2 for the split Chapter 8 pair; the shortfalls are marked `TODO-PROSE` for Phase 6.
- Rebuilt the six navigation links around both split boundaries.
- Verification: all substantive words from the split/moved source ranges are preserved; 530 IDs are unique; all 399 internal targets resolve; all 55 footnote pairs remain intact and sequential; styles, scripts, and Appendix F are byte-identical to baseline.
- The full-section Chapter 5-family word count is 4,524 versus 4,459 before the split (+1.46%) because the mandatory new chapter header, central question, stage map, and structural labels add 65 words. The moved substantive content itself is exactly word-preserved, which is the Phase 1 tolerance check used by `verify.py`.
- Snapshot audit: `phase1-audit.json`.

## Phase 2 — figure and table renumbering

- Kept Figures 5.1–5.6 in Chapter 5.
- Renumbered the moved Chapter 6 assets to Table 6.1 and Figures 6.1–6.3.
- Shifted all Chapter 6–13 asset prefixes to 7–15 using temporary ASCII tokens, including labels, IDs, hrefs, prose references, and the back-matter indexes.
- Renumbered the moved RRF worked example from Table E.1 / `tbl-e-1` to Table 10.1 / `tbl-10-1`. Appendix E retains Tables E.2–E.5 as required by the plan's no-renumbering rule for remaining lettered assets.
- Verification: all 195 asset occurrences remain; all 96 physical labels and generated IDs are unique and mutually consistent; every occurrence has a physical label; no asset token remains; Appendix F, scripts, and styles are byte-identical to baseline.
- Snapshot audit: `phase2-audit.json`.

## Phase 3 — unambiguous chapter references

- Updated 45 singular internal chapter references in prose and end matter: old 6→7 (7), 7→8 (3), 9→11 (6), 10→12 (5), 11→13 (5), 12→14 (9), and 13→15 (10).
- Updated seven specified range constructions, including the two linked `Chapters 11–13` reading-path ranges to `Chapters 13 to 15`.
- Updated the accessible label for `Applying Chapter 15 to active learning` while retaining its existing non-numeric ID.
- Left TOCs, chapter navigation, chapter heads, all Chapter 5/8 judged references, external-work titles, and every non-shifting exclusion untouched.
- Verification: the output is exactly reproducible from the Phase 2 snapshot; all six exclusion strings retain their baseline counts; Appendix F remains within its 0.5% word-count guard, all six F.x label blocks are byte-identical, and all 13 textual `Appendix F` references remain.
- Snapshot audit: `phase3-audit.json`.

## Phase 4 — judged chapter references

- Emitted `phase4-proposal.md` with all seven original Chapter 5 occurrences, all 18 original Chapter 8 occurrences, the three newly correct Chapter 8 results created by Phase 3, all 13 Appendix E occurrences, all 13 protected Appendix F occurrences, and the currency paragraph.
- G4 was approved by the user on 2026-09-03.
- Applied 19 uniquely guarded substitutions: the retrieval-training reference now points to Chapter 6; old Chapter 8 references were distributed across Chapters 9 and 10; the preface reading path and currency list now include the new chapter sequence; and the stale Appendix E RRF cross-reference was replaced because the worked example now follows in Chapter 10.
- Kept the three newly correct Chapter 8 references, the conceptual Chapter 5 references, all LTR/diversification Appendix E references, and all 13 protected `Appendix F` strings.
- Updated the learnt-sparse comparison link to the Chapter 10 hybrid section so its target agrees with its new visible chapter number.
- Verification: the output is exactly reproducible from the Phase 3 snapshot; IDs, hrefs, footnotes, assets, styles, scripts, exclusions, and the Appendix F guard all pass.
- Snapshot audit: `phase4-audit.json`.

## Phase 5 — structural regeneration

- Resolved the four deferred new-chapter and reading-time tokens and set the chapter-eyebrow sequence to 1–15; appendix eyebrows remain A–F.
- Recomputed the split chapters at approximately 210 words per minute, consistent with neighbouring chapter labels: Chapters 5, 6, 9, and 10 are currently 14, 8, 19, and 6 minutes. The new prose pass will trigger one final time check.
- Regenerated both static TOCs directly from top-level sections and headings. They now include Chapters 6 and 10, the two split section lists, and a slimmed Appendix E list without the moved RRF heading.
- Updated every repeated stage map to Chapter 11 for query transformation, Chapters 5–8 for first-stage retrieval, Chapter 10 for fusion, Chapter 9 for reranking, Chapter 8 for indexed-unit analysis in the Part II map, and Chapter 15 for presentation.
- Rewrote the Part II overview for seven chapters, updated its aggregate reading time to 97 minutes, identified Chapters 5–11 explicitly in Exercise II, and extended the Appendix A bi-encoder range to Chapters 5–8.
- Ran the global footnote-ordering script. All 55 footnotes were already sequential after the moves, so it made no byte change.
- Verification: both TOCs contain the new chapters; all structural tokens are gone; chapter and appendix sequences, anchors, assets, scripts, styles, and the Appendix F guard pass.
- Snapshot audit: `phase5-audit.json`.

## Phase 6 — review-quarantined prose

- Replaced all six empty `TODO-PROSE` placeholders with chapter-opening, chapter-closing, or self-check prose and marked every new item `TODO-PROSE-REVIEW`.
- Added a Chapter 5 closing that hands the encoder to Chapter 6, a Chapter 6 opening that restates the status of the `delulu` example, a Chapter 9 closing that points to candidate-list combination, and a Chapter 10 opening and closing that distinguish blend, route, and rank fusion.
- Added two Chapter 5 self-checks and a second Chapter 9 self-check. Each of Chapters 5, 6, 9, and 10 now has at least two questions.
- Marked the revised Appendix E introduction for review and added two review-marked paragraphs to “What you can now ask” that explicitly distinguish Chapters 5/6 and Chapters 9/10.
- Final split-chapter reading times, rounded at the calibrated rate, are 15, 8, 19, and 7 minutes for Chapters 5, 6, 9, and 10. Part II totals about 99 minutes.
- TODO inventory: 11 `TODO-PROSE-REVIEW` markers and zero empty `TODO-PROSE` placeholders.
- Verification: Phase 6 is exactly reproducible from the Phase 5 snapshot; all self-check, anchor, footnote, script/style, token, and Appendix F guards pass.
- Snapshot audit: `phase6-audit.json`.

## Phase 7 — final verification

- Added a comprehensive `verify.py --phase final` pass covering the approved reference dispositions, legacy anchors, exclusions, assets and indexes, TODO inventory, footnotes, navigation, chapter/appendix sequences, HTML parsing, script/style hashes, and the Appendix F guard.
- The rendered smoke test found and corrected one stale hero string (`thirteen chapters` → `fifteen chapters`). It also found that moved Table 10.1 remained in its former Appendix E position in the back-matter table index; the index is now regenerated into physical reading order without changing labels or captions.
- Browser smoke test: the desktop and mobile TOCs each render Preface plus Chapters 1–15; Chapters 6 and 10 are present; representative Part I, II, and III links navigated to Chapters 3, 10, and 12; the hero reports fifteen chapters; Table 10.1 precedes Chapter 11 tables in the index; and the browser console reported no warnings or errors. The local preview server and temporary tab were closed afterwards.
- Navigation follows the book’s established model: the 20 chapter-nav blocks form the mirrored sequence across Preface, all 15 chapters, three exercises, and the closing recap, ending at the End matter band. Part dividers are encountered in document order and reached from the TOC; they do not carry chapter-nav controls in the baseline design.
- Baseline variance retained rather than forced: the plan estimated 149 labels, while the audited source has 96 physical labels and 195 total label/reference/index occurrences. G0 approved those audited counts; final verification preserves all 96 physical objects and all 195 occurrences, with both indexes complete and ordered.
- Final audit: `final-audit.json` records 215 textual chapter/appendix references, 530 unique IDs, zero duplicate IDs, zero broken internal hrefs, 55 globally sequential footnotes, 37 legacy anchors, 11 prose-review markers, and zero placeholder tokens.
- Appendix F remains within the approved 0.5% word-count guard; every F.x label block is byte-identical to baseline; all 13 textual `Appendix F` references remain; and its only authorised heading change is `Applying Chapter 15 to active learning`.
