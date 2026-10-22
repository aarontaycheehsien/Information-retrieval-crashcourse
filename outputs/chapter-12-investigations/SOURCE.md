# Chapter 12: Agentic search

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 12, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **Who chooses the next search?** — fixed, adaptive and agentic control;
   task brief and harness; independent output and retrieval properties;
   dated mode comparisons; strategy approval; choosing control for the task.
2. **The blind spot that survives the loop** — an uncited-paper request and
   labelled set example; the author's dated single-task probe; available
   operations versus executed trace; MCP service boundaries; hypothetical
   compounding and repaired omissions; stopping and the record of a search.
3. **When zero results become a clue** — selected old catalogue queries,
   same-index synonym expansion versus subject broadening, reported database
   names, newer knowledge and temporal confounding, limits of the comparison,
   authoritative local information and evaluating the whole process.

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
python -m pip install -r tools/chapter-12-investigations/requirements.txt
python tools/chapter-12-investigations/render.py --prepare-only
python tools/chapter-12-investigations/render.py --stills-only
python tools/chapter-12-investigations/render.py --render-only --workers 3
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
contains standalone Matplotlib PNG/SVG figures, control-category and selected-recovery CSV data and
a manifest linking assets to the recipe and checked examples. Figure notes are wrapped; note and table-cell drawing bounds and note overlap
are checked before export.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-12-investigations --port 8829
python tools/chapter-12-investigations/check-preview.py
python tools/chapter-12-investigations/render.py --package-only
```

Open `http://127.0.0.1:8829/index.html`. Browser checks require Playwright and
Chromium and exercise actual playback, seeking, captions, scene buttons,
byte-range responses and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 12 section. Source commit, full-book
hash and section hash appear in `source-provenance.json`. Each scene names a
source anchor. Runtime checks parse the source's control and output tables,
verify the exact six-term OR expression, and check essential dated product,
coverage and comparison qualifications. Source, script, production and
shared-helper hashes reject stale timelines; prepared take IDs/text must
match the final script. Plot manifests reject changed assets.

- Fixed control can still have result-dependent content: two-pass PRF can
  construct a second query from a first ranking while its action sequence
  remains prescribed. Adaptive control selects among designer-enumerated
  branches, with a rule, classifier or model as chooser. Agentic search lets
  a model plan part of a multi-action trajectory within predefined tools,
  reachable sources and limits. These are reference points on a continuum.
- The task brief supplies scope, criteria, sources, coverage, stopping and
  required record. The harness bounds available operations, authentication,
  sources and budgets. A callable operation is different from the full
  product a library licenses. Reasoning cannot invent unavailable access.
- Output format and control are separate: either scripted or agentic
  retrieval can return records or feed generation. Agentic RAG is narrower
  than agentic search. Hybrid, multistage and agentic describe independent
  properties; a controller does not alter the scoring rule inside BM25,
  dense retrieval, fusion or a reranker merely by selecting their use.
- Product accounts are dated source snapshots, not new tests. April 2026
  describes Asta Find Paper as semi-rigid, Undermind's original deep search
  as predefined adaptive control, and Projects as dynamic tool chaining.
  Mode-specific evidence matters; brand, iteration, fluent output and a
  model inside a workflow do not by themselves establish agency.
- The April 2026 Web of Science Research Assistant post's fully-agentic
  label accompanies described task-route selection compatible with adaptive
  control. Whether novel sequences are possible remains unsettled by the
  post. It documents prior user strategy review/approval and a returned
  Advanced Search expression. That is separate from stopping an ongoing
  search, and is a described product property, not an approval requirement
  imposed on this video's production or its viewer.
- The December 2025 uncited-paper probe is one task type, not a league table
  or robust general capability test. Asta stopped at target lookup;
  Consensus returned already cited work despite four subagents; SciSpace
  attempted extraction and comparison, with metadata failures and unclear
  completion. General assistants were also constrained by full-text access.
  These reports do not isolate a sole cause or establish general agency.
- The set diagram is invented: related identities A/B/C/D minus cited A/C
  leaves B/D. These are candidates requiring timing, relevance and identity
  checks, not verified citation omissions. No literature search or citation
  audit was performed for this production.
- MCP describes callable operations, purpose, inputs and outputs. It is not
  a new index, retrieval algorithm, replacement for service APIs or competitor
  to RAG. Wiley AI Gateway returns relevant full-text chunks and metadata.
  The Scite documentation account, checked October 2026, describes filters
  but does not establish web-interface ranking parity; its Assistant is
  not exposed through MCP. Authentication and entitlements remain in force.
  No MCP service call or new endpoint test was performed for these films.
- Open-access/citation trajectories are explicitly hypothetical recorded
  actions and observations, not private reasoning. Following returned terms
  and references can perpetuate an early selection-bias-methods omission.
  A targeted alternative action might admit new methods candidates; neither
  that action nor success is guaranteed. Citation searching is not asserted
  to remain trapped in one aspect in all cases.
- A trace records one executed path, not the full available action menu.
  Record both, plus intermediate results, limits and stopping. Prescribed
  steps ending, budget exhaustion, user interruption, declining yield and
  a model judging enough are not proof of complete coverage. More rounds
  incur latency and tokens and can vary between runs; no cost benchmark
  or measured failure rate is invented.
- The June 2026 library demonstration replays selected, not sampled, 2023
  zero-result database queries with newer models. These exploratory cases
  do not provide a success rate, controlled comparison, human benchmark or
  isolated causal test. Reported database names are source outcomes; no
  fresh catalogue query was run to generate these videos.
- Primo single-pass Natural Language Search generated the exact source
  six-term autism OR expression over the same index and still returned
  zero. The drawing represents one expression, not six independent calls.
  The loop broadened to psychology, medicine, education and disability,
  returning PsycINFO, Education Research Complete and SocINDEX in this
  selected account. Useful recovery need not change a retriever's scoring
  function; it can change the sequence of its use.
- Other selected cases: cost of living broadened to inflation, household
  expenditure and consumer prices; Rolex watches led via luxury goods to
  Statista and Passport; statis resolved to Statista; refinituv reached
  LSEG. The last recovery used a rebrand postdating the original query,
  so newer knowledge is a temporal confound, not evidence for the loop alone.
- A keyword-oriented endpoint worked for these cases; so did a holdings
  CSV, and a smaller model made little difference there. This does not
  establish that capability is irrelevant, MCP caused the gain, agentic
  control was necessary or better retrieval unnecessary. Fixed/adaptive
  retries could also help. Setup changes prevent isolating a sole cause.
- Public subject knowledge cannot establish current local database coverage,
  embargoes, field quirks, entitlements or new licenses. Those require
  authoritative library information; a recovered name still needs checking.
  Obscure resources and specialised variable/company/year questions can
  exceed the available knowledge or operations.

Checks cover source hashes/anchors, source categories and the exact one-shot
expression; declared set arithmetic and scoped source examples;
script/take/caption/word agreement and timing; sampled drawing bounds,
figure-note/table-cell bounds, note overlap and visual review; complete media
decoding and exact frames; 1080p/30fps H.264, stereo 48kHz AAC, −16 LUFS ±1
and peak below −1 dBTP; fast-start metadata and embedded caption equality.
Packaging checks MP4 hashes and ZIP CRCs. Chromium checks real playback and
responsive layouts. Earlier MP4 hashes are checked for preservation before
the local commit.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 12](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#agentic-search),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author
and book when sharing. This adaptation adds original narration and illustrations.
