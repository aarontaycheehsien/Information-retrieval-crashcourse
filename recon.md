# Phase 0 reconnaissance — chapter restructuring

Status: **Gate G0 pending. No edits have been made to `search-textbook.html`.**

## Snapshot

- Git baseline: `65469bbd4e7aa811db0f0511ae10a4386299308f`
- `search-textbook.html` SHA-256: `c434f1042446ac8b9749fc3d3f9475e893b487df82b0661fc3087f96e4b19718`
- The complete machine-readable audit is in `baseline.json`; `audit.py` regenerates it without modifying the book.

## Baseline results

| Check | Actual | Plan expectation | Result |
|---|---:|---:|---|
| Visible chapter/appendix references | 200 | about 200 | exact |
| References including markup attributes | 285 | diagnostic only | recorded |
| Chapter asset occurrences | 149 | 149 | exact |
| Appendix asset occurrences | 46 | 46 from the supplied prefix counts | exact |
| Labelled figure/table objects | 96 | not separately stated | recorded |
| Unique IDs | 525 | not stated | no duplicates |
| Internal hrefs | 1,144 to 396 targets | not stated | no broken targets |
| Legacy anchors | 36 | 36 | exact |
| Footnote refs / notes | 55 / 55 | not stated | complete |
| Placeholder markers (`%%`) | 0 | 0 | exact |

The asset-prefix counts are exact for every supplied prefix: Chapters 1–13 contribute 149 occurrences, and Appendices A–F contribute 46, for 195 total occurrences. The count includes labels, prose references, and the back-matter asset index. There are 96 physical labelled figure/table objects.

The exact high-risk textual counts also match the plan: `Chapter 5` occurs 7 times, `Chapter 8` 18 times, `Appendix E` 13 times, and `Appendix F` 13 times.

Audit correction recorded during Phase 3 preparation: the supplied sketch regex used a single-character number class and therefore omitted Chapters 10–13. `audit.py` uses the intended multi-digit form. The corrected visible total is exactly 200; all snapshot audits were regenerated from their Git commits.

## Structure and word-count reconnaissance

- Chapter 5 is 4,459 visible words, close to the plan's approximately 4,492. The requested split heading exists uniquely: `model-tokens-are-not-indexed-terms` follows `what-bert-is-and-what-it-still-needs`.
- Chapter 8 is 4,847 visible words. Both requested hybrid headings exist uniquely and follow `neural-ir-broader-than-dense-retrieval`.
- Appendix E is 3,732 visible words. The RRF and toy-mixture headings both exist uniquely.
- Appendix F is 3,474 visible words. The plan later cites approximately 5,580 words, a −37.7% difference. The actual 3,474-word value must become the Appendix F guard baseline if G0 is approved.
- Chapter 5 currently has no `self-check-q` blocks. Chapter 8 has three, all centred on representation/retrieval distinctions rather than hybrid fusion. The new Chapters 5, 6, and 10 will therefore need Phase 6 review-marked questions to satisfy the two-question target.

## Scripts, TOC, anchors, and generated surfaces

The document has four script blocks:

1. A 53-character inline script adds the `js` class to the root element.
2. Inline MathJax configuration contains no structural data.
3. The external MathJax loader contains no inline data.
4. A 10,567-character UI script handles TOC highlighting, generic chapter permalinks, glossary behaviour, term marking, and related presentation behaviour. It contains no chapter-order/title/asset data structure. Its one `Appendix D` literal is a generic term-marking exclusion, not numbering data.

The desktop and mobile TOCs are static HTML. `tools/maintain.py` already rebuilds both from the document's real headings, renumbers assets from chapter eyebrows, and rebuilds the figure/table index. Heading-anchor links, reading-time strings, figure/table labels, and footnote links are static markup. The chapter permalink control is generated generically at runtime and automatically applies to new chapter heads.

No script block needs to change for this restructure. Script and style hashes are captured in `baseline.json` for later byte-comparison. The structural maintenance script should be used after the controlled chapter moves, with its diff inspected before acceptance.

## Footnotes

Footnotes are document-wide and globally sequential: refs 1–55 appear in reading order and map one-to-one to 55 note entries. No missing or orphan notes were found. Moving content can put numbering out of order, so Phase 5 should run `tools/renumber_footnotes.py`, followed by a pair/order audit.

## End-matter inventory

The surfaces that can carry chapter or asset references are:

- three application exercises;
- `What you can now ask`;
- Appendices A–F;
- the complete glossary (`details#glossary`);
- `Figures and tables` and its two generated indexes;
- `Where to go deeper`;
- `How to cite and reuse this book`;
- `Generative AI use disclosure`;
- the references list;
- desktop/mobile TOCs and pinned end-matter links.

There is no separate top-level glossary chapter; the glossary is a standalone `<details>` element between Appendix F and the figures/tables section.

## Judgement calls established in reconnaissance

### Toy mixture

`A toy mixture—and why raw scores cannot simply be added` is primarily a learning-to-rank illustration. It starts with a manually weighted feature mixture, explains feature scaling/calibration, and ends by contrasting hand-set weights with coefficients or nonlinear interactions learned from training evidence. It should remain in Appendix E.

### RRF section

Contrary to the plan's provisional expectation, the RRF section contains a labelled worked example, `Table E.1`. Because the whole RRF section moves, that table must move with it and become Chapter 10's first table (`Table 10.1`), including its generated ID and all index/prose references.

### Appendix F heading anchor

The heading text is `Applying Chapter 13 to active learning`, but its ID is `reproducibility-of-active-learning-screening`. The ID does not embed `13`, so it should stay unchanged and no legacy alias is needed. The static heading anchor already targets that ID; the TOC entry will be regenerated from the revised heading text.

## Anchor-sensitive findings

The supplied inbound-link counts match exactly:

- `#reranking-and-hybrid`: 38
- `#why-hybrid-retrieval-remains-attractive`: 9
- `#two-hybrids-that-combine-differently`: 7
- `#appendix-how-rrf-combines-ranked-lists`: 6

All existing IDs are unique, all current internal hrefs resolve, and the 36 current `legacy-anchor` aliases are intact. These counts are captured for post-phase comparison.

## G0 conclusion

Phase 0 is complete. The plan's structural targets exist and its sensitive-reference, total-reference, asset-prefix, legacy-anchor, and inbound-link counts match. Structural editing was paused because the Appendix F word-count estimate differs by more than 10%. G0 approval adopted the actual Appendix F baseline of 3,474 words.
