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

## Phase 4 — proposal gate

- Emitted `phase4-proposal.md` with all seven original Chapter 5 occurrences, all 18 original Chapter 8 occurrences, the three newly correct Chapter 8 results created by Phase 3, all 13 Appendix E occurrences, all 13 protected Appendix F occurrences, and the currency paragraph.
- No Phase 4 substitutions have been applied; G4 approval is pending.
