# Phase 4 judged-reference proposal

Status: **Gate G4 pending. None of the edits below have been applied.**

Positions refer to the Phase 3 snapshot (`phase3-audit.json`). Context cues, not numeric positions or occurrence counts, will be used when applying approved edits.

## Chapter 5 — seven original occurrences

| # | Position / location | Context cue | Proposed old → new | Rationale |
|---:|---|---|---|---|
| 1 | 51,419 · desktop TOC | `data-ch="embeddings"` | Defer; `Chapter 5` remains `Chapter 5` | Phase 5 regenerates the TOC and adds Chapter 6. |
| 2 | 70,814 · mobile TOC | `data-ch="embeddings"` | Defer; `Chapter 5` remains `Chapter 5` | Same generated structural surface. |
| 3 | 207,878 · `embeddings` eyebrow | revised geometry chapter head | Defer; `Chapter 5` remains `Chapter 5` | Phase 5 regenerates the 1–15 eyebrow sequence. |
| 4 | 338,559 · cross-encoder section | `training example` and the delulu pair | Keep `Chapter 5` | The pair is introduced while explaining what representations/training must encode, before the retrieval-infrastructure split. |
| 5 | 339,855 · cross-encoder section | `used that pair to explain what training has to teach` | Keep `Chapter 5` | Explicitly points back to the conceptual example retained in Chapter 5. |
| 6 | 468,870 · OOD section | `retrieval-training story` / positives / negatives | `Chapter 5` → `Chapter 6` | Retrieval-specific training moved to `retrieval-encoder`. |
| 7 | 713,490 · Where to go deeper | `leaves you wanting the mechanism` | Keep `Chapter 5` | The linked Word2Vec mechanism remains in Chapter 5. |

## Chapter 8 — 18 original occurrences plus three correct Phase 3 results

The three rows marked **already final** were old Chapter 7 references changed mechanically in Phase 3. They now correctly name the new Chapter 8 and must not be treated as old Chapter 8 references.

| # | Position / location | Context cue | Proposed old → new | Rationale |
|---:|---|---|---|---|
| 1 | 54,975 · desktop TOC | `data-ch="reranking-and-hybrid"` | Defer: `Chapter 8` → `Chapter 9` | Phase 5 regenerates the TOC for the slimmed reranking chapter. |
| 2 | 74,370 · mobile TOC | same TOC entry | Defer: `Chapter 8` → `Chapter 9` | Same generated structural surface. |
| 3 | 91,513 · preface | `sparse, reranking and hybrid arrangements can contribute` | `Chapter 8` → `Chapters 9 and 10` | The sentence spans the reranking and hybrid/fusion chapters. |
| 4 | 154,621 · Chapter 2 | `document and its searchable units` | Keep `Chapter 8` (**already final**) | This was old Chapter 7 and correctly points to representations/indexed units. |
| 5 | 206,154 · Part II overview | `opens the stored object` | Keep `Chapter 8` (**already final**) | This was old Chapter 7 and correctly names representations/indexed units. |
| 6 | 206,209 · Part II overview | `adds the stages that run after a candidate set exists` | `Chapter 8` → `Chapters 9 and 10` | Those stages are now divided between reranking and fusion. Phase 5 will rewrite the complete overview sentence. |
| 7 | 281,599 · dense retrieval | `30-record reranker budget` / Primo Research Assistant | `Chapter 8` → `Chapter 9` | The linked pipeline-budget discussion remains in reranking. |
| 8 | 287,245 · dense retrieval | `returns to the LightGBM stage once reranking is in view` | `Chapter 8` → `Chapter 9` | LightGBM is discussed as a reranking stage. |
| 9 | 315,706 · learnt sparse section | `main alternative to running a lexical and a dense retriever side by side` | `Chapter 8` → `Chapter 10` | The comparison is framed against hybrid retrieval, now Chapter 10. The existing link target will be reviewed because it currently points to the retained Chapter 9 umbrella section. |
| 10 | 327,319 · `reranking-and-hybrid` eyebrow | slimmed chapter head | Defer: `Chapter 8` → `Chapter 9` | Phase 5 regenerates the eyebrow sequence. |
| 11 | 358,023 · neural-IR umbrella section | `built the representation` | Keep `Chapter 8` (**already final**) | This was old Chapter 7 and correctly points back to representations/indexed units. |
| 12 | 376,215 · query-transformation opener | `added several retrievers, fusion and route selection` | `Chapter 8` → `Chapters 9 and 10` | The antecedent now spans reranking and hybrid/fusion. |
| 13 | 397,014 · query-understanding table | `fusion machinery of` | `Chapter 8` → `Chapter 10` | The linked fusion material now lives in Chapter 10. |
| 14 | 478,026 · diagnosing failure | `learnt sparse … ColBERT-style … first stage` | `Chapter 8` → `Chapter 9` | The neural-IR umbrella and first-stage placement remain in Chapter 9. |
| 15 | 492,285 · evaluation | `first-stage retriever is fast, shallow and broad` | `Chapter 8` → `Chapter 9` | The reranker/first-stage contrast remains in Chapter 9. |
| 16 | 622,809 · Appendix E intro | `introduced four ideas` | `Chapter 8` → `Chapters 9 and 10` | The four ideas are now introduced across both chapters. |
| 17 | 623,593 · Appendix E intro | `detail that Chapter 8 deliberately leaves out` | `Chapter 8` → `Chapters 9 and 10` | Appendix E elaborates material introduced across both chapters. The sentence will be smoothed to plural agreement. |
| 18 | 637,692 · Appendix E | `Chapter 8’s LLM discussion` | `Chapter 8` → `Chapter 9` | Pointwise/pairwise/listwise inference remains in the reranking chapter. |
| 19 | 638,489 · Appendix E | `introduces result diversification` | `Chapter 8` → `Chapter 9` | Diversification remains in the reranking chapter. |
| 20 | 645,454 · Appendix E | `retrieve a high-recall shortlist cheaply` | `Chapter 8` → `Chapter 9` | The production multi-stage pipeline remains in Chapter 9. |
| 21 | 714,814 · Where to go deeper | `three arrangements of Chapter 8` | `Chapter 8` → `Chapter 9` | Joint encoding, late interaction, and learnt sparse representations remain in Chapter 9. |

## Appendix E — all 13 occurrences

| # | Position / location | Context cue | Proposed old → new | Rationale |
|---:|---|---|---|---|
| 1 | 62,770 · desktop TOC | Appendix E entry | Keep; regenerate in Phase 5 | Appendix letter/title remain unchanged; the RRF subsection disappears from its sublist. |
| 2 | 82,165 · mobile TOC | Appendix E entry | Keep; regenerate in Phase 5 | Same structural surface. |
| 3 | 103,456 · preface reading path | `use Appendix E when a system combines or reranks` | `use Appendix E` → `use Chapter 10 and Appendix E` | Fusion is now in Chapter 10; Appendix E retains LTR/diversification/reranker detail. |
| 4 | 105,158 · currency paragraph | chapter list followed by `Appendix E and Appendix F` | Keep `Appendix E`; update surrounding chapter list | The appendix still contains time-sensitive product examples. |
| 5 | 336,261 · reranking pipeline | `reconstructs the earlier documented 2020 version in depth` | Keep `Appendix E` | The Semantic Scholar/LTR reconstruction remains there. |
| 6 | 348,643 · LLM rerankers | `separates them` | Keep `Appendix E` | Pointwise/pairwise/listwise method detail remains there. |
| 7 | 351,567 · diversification | `compares the main diversification methods` | Keep `Appendix E` | Diversification detail remains there. |
| 8 | 353,176 · academic pipelines | `develops the idea` | Keep `Appendix E` | Learning-to-rank detail remains there. |
| 9 | 367,710 · hybrid/fusion chapter | `gives the formula and a worked example` | Replace linked sentence with `The formula and a worked example follow.` | RRF now follows immediately in Chapter 10; the Appendix E cross-reference is stale. |
| 10 | 503,781 · evaluation | `explains diversity-aware metrics` | Keep `Appendix E` | Those metrics remain in Appendix E. |
| 11 | 605,863 · glossary/terminology map | `methods and metrics in Appendix E` | Keep `Appendix E` | The target diversification material remains. |
| 12 | 622,582 · Appendix E eyebrow | structural heading | Keep `Appendix E` | Appendix letters do not change. |
| 13 | 762,083 · references discussion | `introduces learning to rank more generally` | Keep `Appendix E` | LTR remains in Appendix E. |

## Appendix F — all 13 occurrences

Every `Appendix F` string remains verbatim under exclusion E4.

| # | Position / location | Context cue | Proposal |
|---:|---|---|---|
| 1 | 64,281 · desktop TOC | Appendix F entry | Keep verbatim; regenerate surrounding TOC only. |
| 2 | 83,676 · mobile TOC | Appendix F entry | Keep verbatim; regenerate surrounding TOC only. |
| 3 | 102,629 · evidence-synthesis reading path | `as the application that connects…` | Keep verbatim. |
| 4 | 102,767 · same reading path | `Appendix F is core rather than optional` | Keep verbatim. |
| 5 | 104,168 · appendix guidance | `exception is the evidence-synthesis route` | Keep verbatim. |
| 6 | 105,238 · currency paragraph | paired with Appendix E | Keep verbatim. |
| 7 | 138,366 · Boolean search | `wider process as a high-recall retrieval problem` | Keep verbatim. |
| 8 | 385,009 · query objects | `See Appendix F` | Keep verbatim. |
| 9 | 441,657 · agency costs | `defensible stopping rule` | Keep verbatim. |
| 10 | 468,364 · OOD | `systematic-review retrieval` | Keep verbatim. |
| 11 | 498,863 · precision/recall | `follows that boundary` | Keep verbatim. |
| 12 | 527,719 · library practice | `applies these reproducibility principles` | Keep verbatim. |
| 13 | 651,060 · Appendix F eyebrow | structural heading | Keep verbatim. |

## Currency paragraph

The current source still contains linked bare numbers, so it was intentionally excluded from Phase 3's singular `Chapter N` pass.

Proposed source-level result:

> Everything describing how a named product works—the product examples in Chapter 1, 3, 7, 9, 10, 11 and 12, and in Appendix E and Appendix F—carries the date it was checked…

The links will target `intro`, `bm25-ranking`, `dense-at-scale`, `reranking-and-hybrid`, `hybrid-and-fusion`, `query-transformation`, and `agentic-search`, respectively. Existing punctuation and spacing style will be preserved.

## Appendix F active-learning heading

Phase 3 already changed the visible heading and its accessible link label from `Applying Chapter 13 to active learning` to `Applying Chapter 15 to active learning`. Its ID remains `reproducibility-of-active-learning-screening`; no alias or further Phase 4 edit is proposed.

## Application guard

If G4 is approved, the application script will require each context cue to match exactly once. Any zero or multiple match will stop the phase without writing. After application it will rerun the anchor, exclusion, asset, footnote, script/style, and Appendix F guards before creating the Phase 4 snapshot.
