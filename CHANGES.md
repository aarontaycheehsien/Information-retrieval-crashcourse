# Restructuring change log

## Phase 0 — baseline and reconnaissance

- Target snapshot: Git `65469bbd4e7aa811db0f0511ae10a4386299308f`; book SHA-256 `c434f1042446ac8b9749fc3d3f9475e893b487df82b0661fc3087f96e4b19718`.
- Added the read-only `audit.py`, `baseline.json`, `recon.md`, and gate record.
- Confirmed 525 unique IDs, zero duplicates, zero broken internal href targets, 55 globally sequential footnote pairs, and 36 legacy anchors.
- Adopted 154 visible chapter/appendix references and 3,474 visible Appendix F words as the approved baselines.
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
