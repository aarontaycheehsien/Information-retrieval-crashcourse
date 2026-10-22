# Chapter 15: Implications for library practice and tool evaluation

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 15, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **Same question. Same search?** — conditional reproducibility, four record
   areas, Boolean/lexical and dense conditions, sparse and late-interaction
   records, saved versus regenerated transformations, workflow traces and
   a practical record that supports later comparison.
2. **Why is this paper here?** — a generated rationale versus the source's
   hypothetical rank-3 paper, transparency/interpretability/understandability,
   the exact mock inputs and rank path, backwards inspection, stage-specific
   limits, action/observation evidence and preserving unknowns.
3. **What are you actually licensing?** — supported starting inputs and all
   nineteen source vendor questions in six groups: control, architecture,
   exactness, auditability, cost/continuity and institutional evaluation.
   A companion CSV leaves answers, evidence and verification fields blank.

Original paper-and-ink artwork, curiosity-led questions, prediction pauses and
word-timed reveals continue the series. Independently produced, with no
affiliation with Veritasium. Narration uses the standard Microsoft Andrew
Multilingual synthetic voice. Original drawings and script adaptations use
no presenter likeness, voice cloning, third-party footage or copied screenshots.

## Reproduce and review

The production lives in new isolated directories. Generated media stay local
and Git-ignored; production sources are committed. Nothing is published or
pushed. Shared media, speech-cache and drawing helpers are reused without
modification; earlier productions and textbook files are preserved.

From the repository root with Python 3.12 and FFmpeg on PATH:

```bash
python -m pip install -r tools/chapter-15-investigations/requirements.txt
python tools/chapter-15-investigations/render.py --prepare-only
python tools/chapter-15-investigations/render.py --stills-only
python tools/chapter-15-investigations/render.py --render-only --workers 3
```

`CHAPTER_FFMPEG` can specify FFmpeg. System DejaVu fonts are used;
`PREFACE_FONT_DIR` can choose a folder containing `DejaVuSans.ttf`,
`DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf`. `--episode 1`, `2` or `3` selects
a film; `--output` chooses the destination. No GPU, retrieval model or large
index is required for these declared teaching examples.

Public narration text is sent to Microsoft's speech service through edge-tts.
The managed proxy CA is trusted with TLS verification retained. Takes are
cached by text, voice and engine. Speech is not cut or accelerated to fit
animation; reveals follow actual word timings.

Exports include 1920×1080, 30 fps H.264/AAC MP4s, burnt-in and embedded English
captions, SRT/VTT, timed transcripts, source-linked storyboards, posters,
review frames, contact sheets and verification reports. The responsive watch
gallery and ZIP contain all three films and supporting material. `plots`
contains standalone Matplotlib PNG/SVG figures, hypothetical trace and blank vendor-question CSV data and
a manifest linking assets to the recipe and checked examples. Figure notes are wrapped; note and table-cell drawing bounds and note overlap
are checked before export.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-15-investigations --port 8832
python tools/chapter-15-investigations/check-preview.py
python tools/chapter-15-investigations/render.py --package-only
```

Open `http://127.0.0.1:8832/index.html`. Browser checks require Playwright and
Chromium and exercise actual playback, seeking, captions, scene buttons,
byte-range responses and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 15 section. Source commit, full-book
hash and section hash appear in `source-provenance.json`. Each scene names a
source anchor. Runtime checks parse all three source tables: four record areas,
seven reporting methods and seven inspection stages. They also compare the six
vendor group headings and all nineteen exact question titles, all eight mock
trace fields, the source rationale and the backwards-inspection labels. Film 3's
scene metadata must cover vendor-q01 through vendor-q19 exactly once in order.
Source, script, production and shared-helper hashes reject stale timelines;
prepared take IDs/text must match the final script. Plot manifests reject
changed assets.

- Reproducibility is conditional on fixed records, indexing, representations,
  interpretation and configuration. No method guarantees identical records
  or ranking forever. Preserving an actual search procedure and result export
  enables later comparison even when exact future recreation is impossible.
  Saving the question alone is insufficient after rewriting or orchestration.
- The four record areas are query interpretation, candidate retrieval,
  ranking/fusion and retrieval control. Some are visible at the interface;
  internal versions, candidate budgets, traces and change notices may require
  vendor disclosure or institutional requirements. Unknown details are not
  filled with invented mechanisms.
- Strict Boolean eligibility should repeat with the same records, indexing,
  analyser and query interpretation. Record exact input, platform/database,
  fields, limits, vocabulary version, date and count. Ranked lexical retrieval
  also needs analysis, rewriting, field weights, ranking configuration, sort
  and depth. BM25's target collection statistics can change when records are
  added; an unchanged formula is not a frozen ranking.
- Dense retrieval is not inherently random. Fixed encoder, indexed units,
  stored vectors, similarity function and exact procedure can repeat scores.
  Record embedded content, metadata, chunking, model/tokeniser and index
  versions, filters, depth/threshold and exact versus approximate search.
  ANN construction and parameters may affect candidates near a boundary;
  this is distinct from variable query generation.
- Learnt sparse records include generated terms/weights where exposed, model,
  tokeniser, index, scoring and depth. Late interaction additionally needs
  indexed-unit and compression versions, similarity/MaxSim, pruning/ANN and
  depth. Visible alignments expose a useful layer without making contextual
  vectors portable between model versions or describing the entire decision.
- Generated Boolean expressions, expansions, subqueries and hypothetical text
  must be retained exactly, with inferred filters, route, prompt/template,
  model/parser versions and sampling settings/seed if exposed. Ask whether a
  rerun reuses a saved transformation or regenerates it. Sampling can vary;
  model, prompt and hosted-inference changes can matter even at temperature
  zero/greedy decoding. This does not claim every call must vary. An actual
  tested guarantee is needed before assuming identical system output.
- Fixed/adaptive rules can be documented in advance, while adaptive branches
  and result-dependent inputs still need a record of the actual path. Agentic
  runs need permitted tools/sources, controller/instructions, queries, routes,
  intermediate observations, sequence, budgets, stopping and final identifiers.
  The requested evidence is an action/observation trace, not private or
  narrated model reasoning. Source discussions of agents do not authorise
  delegation during this production; no subagents were used.
- Practical documentation starts with input, product/mode, date, visible
  transformations, filters, count, identifiers, observed limits and raw export
  where possible. Keep observed, documented and unknown information distinct.
  The chapter aligns this with PRISMA-S reporting while recognising limits;
  the films do not claim an undocumented search is fully replicable.
- Transparency exposes information; interpretability traces inclusion,
  exclusion, scoring or reranking; understandability supplies an accurate,
  usable mental model. A broad disclosure, detailed score view and rerunnable
  record do not automatically supply all three properties. Useful inspection
  does not require disclosure of every model weight or engineering detail.
- Figure 15.1 is explicitly hypothetical. Mock P concerns disciplinary
  differences in open-access citation advantage. The original input is
  `Does open access increase citations?`; the exact transformed expression
  is `“open access” AND citation*`. The route is lexical retrieval over indexed
  abstracts, and the mock abstract contains open access and citations.
  Candidate rank is 18 of 100, reranking moves P to 3, and the display shows
  ten. Internal reranker scoring is not disclosed. Code checks these source
  fields and the rank/cutoff relationship without executing any search.
- The displayed rationale is the source's exact illustrative wording:
  “This paper closely addresses your question about open access and citations.”
  It is not a new model generation or evidence that its words caused a score.
  No actual paper, product trace, ranking, benchmark or vendor disclosure was
  obtained. In a real product, trace facts must derive from the executed
  input, index, candidate and scoring path; narrative must not fill gaps.
- Figure 15.2 follows an inspection backwards: result, fusion/display,
  scoring/reranking, matched evidence, candidate source, transformed input,
  original input. The drawing labels inspection order, not execution order.
  Showing a matched word while withholding transformed inputs supplies only
  part of the requested trail. Its stopping point is evidence about disclosure,
  not proof of an undisclosed mechanism.
- Stage-specific explanations carry limits. A transformation does not alone
  prove preserved intent; Boolean eligibility does not prove relevance;
  lexical score contributions do not make a score a probability or rule out
  a later reranker. Dense similarity/metadata do not automatically give a
  human-readable latent-feature cause. Sparse terms/token alignments are one
  inspectable layer. Fusion/display inspection needs component lists, rules,
  ordering, cutoffs and presentation. Highlighting, citation counts, snippets
  and generated rationales are not by themselves causal evidence.
- Agentic inspection exposes actions, inputs, returned observations and stops.
  A model's narrative about its own reasoning does not establish what caused
  its choices. A helpful post-hoc account should be labelled interpretation.
  Documentation can be complete while individual result causes remain opaque;
  clear prose does not supply the saved versions/outputs required for reruns.
- Before the nineteen questions, ask what starting inputs are supported:
  text, fields, seeds, citation links, judgements, API predicates and, where
  applicable, exportable task briefs plus generated queries. A text-box label
  is not an architecture description. No product is assigned an architecture
  based on its marketing vocabulary in these films.
- Question groups contain 2/5/4/3/2/3 items. Q1–2 separate inference,
  transformation and control. Q3–7 ask components, neural-model role, indexed
  units, passage assembly and hybrid fusion. An abstract-only index cannot
  match full-text-only evidence at that stage; later fetching/context is a
  separate operation. Two retrievers do not establish material contribution
  by both to a final ranking.
- Q8–11 ask an exact lexical route, compatible analysis/tokenisation, failures
  of identity/negation/exclusion and relevance-model training/adaptation.
  Q12–14 ask actual inspection, export/reuse versus regeneration and disclosed
  changes with version provenance. These are questions to verify, not invented
  vendor answers or promises of permanent result identity.
- Q15–16 ask pricing, rate/iteration limits, limit behaviour, agentic usage,
  mode retirement, export and notice. The chapter's renamed/distinct mode
  examples motivate the questions; no new retirement event or pricing test
  is claimed. Q17–19 ask local evaluation, known failure cases and comparisons
  across an update. No real vendor benchmark or procurement negotiation was
  performed for these films.
- `vendor-questions.csv` contains the nineteen exact source question titles,
  group/number metadata and blank vendor-answer, evidence, library-verification
  and follow-up fields. It is a concise companion sheet, not fabricated vendor
  responses or the optional specialist appendix questionnaire. Institutional
  requirements for visibility, documentation and local testing should be
  established in advance; later additions cannot be relied on to arrive on
  a library's timetable. This task closes the main course at Chapter 15;
  it does not continue into application exercises or appendices.

Checks cover source hashes/anchors, tables, exact mock trace and rationale,
inspection order and all nineteen questions; declared rank/cutoff relationships;
script/take/caption/word agreement and timing; sampled drawing bounds,
figure-note/table-cell bounds, note overlap and visual review; complete media
decoding and exact frames; 1080p/30fps H.264, stereo 48kHz AAC, −16 LUFS ±1 and
peak below −1 dBTP; fast-start metadata and embedded caption equality. Packaging
checks MP4 hashes and ZIP CRCs. Chromium checks real playback and responsive
layouts. Earlier MP4 hashes are checked for preservation before the local commit.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 15](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#library-practice),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author
and book when sharing. This adaptation adds original narration and illustrations.
