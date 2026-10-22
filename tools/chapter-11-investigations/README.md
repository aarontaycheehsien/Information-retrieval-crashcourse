# Chapter 11: Understanding, transforming and routing queries

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 11, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **What if your query is a paper?** — eight query objects, text and structured
   conditions, seeds and citation relationships, feedback and monitoring,
   API predicates and task briefs, a scoped review audit, receiving components
   and known-record evaluation.
2. **Who changed your question?** — understanding, transformation and control;
   the chapter's visible Boolean example; distinct Primo workflows; retrieval
   feedback versus screening; fixed two-pass PRF; language rewrites versus
   weighted vocabulary representations; recording the actual procedure.
3. **The paper that never existed** — the source's hypothetical paragraph,
   Query2doc and HyDE paths, unsupported assumptions, product arrangements,
   partial natural-language constraint handling, inferred/manual filters and
   the evidence needed to reconstruct a search.

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
python -m pip install -r tools/chapter-11-investigations/requirements.txt
python tools/chapter-11-investigations/render.py --prepare-only
python tools/chapter-11-investigations/render.py --stills-only
python tools/chapter-11-investigations/render.py --render-only --workers 3
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
contains standalone Matplotlib PNG/SVG figures, source-reference and reported-audit CSV data and
a manifest linking assets to the recipe and checked examples. Figure notes are wrapped; note and table-cell drawing bounds and note overlap
are checked before export.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-11-investigations --port 8828
python tools/chapter-11-investigations/check-preview.py
python tools/chapter-11-investigations/render.py --package-only
```

Open `http://127.0.0.1:8828/index.html`. Browser checks require Playwright and
Chromium and exercise actual playback, seeking, captions, scene buttons,
byte-range responses and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 11 section. Source commit, full-book
hash and section hash appear in `source-provenance.json`. Each scene names a
source anchor. Runtime checks parse the source's first two tables to verify
all eight query-object names and five receiver categories. They also verify
the exact structured expression, source hypothetical paragraph, audit figures
and required product/control distinctions. Source, script, production and
shared-helper hashes reject stale timelines; prepared take IDs/text must
match the final script. Plot manifests reject changed assets.

- The eight source query objects are free text; controlled/structured
  expressions; citation edges; seed documents; relevance judgements;
  browse/monitoring targets; programmatic predicates; and task briefs. These
  overlap: an API can carry text and a seed can start citation traversal.
  They are different mechanisms, not eight mutually exclusive phrasing styles.
- Directed citation diagrams are original schematics, with arrows from citing
  to cited paper. Direct citation is A→R; coupling is A→R←B; co-citation has
  one citing paper C pointing to both A and B. No graph search was run. PubMed
  Similar Articles is described by the source as word-weighted title/abstract/
  MeSH similarity; seed input does not establish embeddings.
- A paper about open access can itself be paywalled. An API filter on the
  retrieved paper's OA status could therefore exclude a relevant study of OA
  citation advantage; the source instead illustrates a publication-year
  filter. No live API call or literature search is claimed.
- The Greenhalgh/Peacock example is one audit of one complex-evidence review,
  with 495 included sources. The chapter reports 30% from protocol-defined
  database/hand searches and 51% from snowballing. Only these two reported
  shares are plotted. They are not universal review estimates, exact counts,
  an exhaustive partition calculated by this production, or new measurements.
  In particular, percentages are not multiplied by 495 to invent paper counts.
- Berrypicking, combining query objects, and testing different input forms
  explain why one well-phrased text query can still cover only one route.
  Receiver recommendations depend on model training, domain and supported
  syntax. Generated Boolean strategies may contain invalid MeSH terms;
  detailed instructions are not automatically followed by a retrieval model.
- Understanding interprets; transformation creates changed/additional inputs;
  retrieval control chooses paths, coordination and another search. Recognising
  a date alone does not establish that a filter or routing change occurred.
- The visible Web of Science Smart Search example preserves the exact source
  clauses `PY=(2020-2024)`, `OG_SMART=(university of california)`, `TS=(apple)`,
  `TS=(oranges)`, `TS=(bananas)`, all joined with AND. The original drawing
  replaces the source screenshot. No product execution or interpretation
  accuracy test is claimed. Inspecting the generated query matters because
  changed conditions can alter eligibility before ranking.
- Primo VE NDE Natural Language Search's source account identifies GPT-4.1
  Mini, a basic Boolean expression and six related OR-connected permutations,
  received by inspectable/editable Advanced Search. This does not establish
  six independent retrieval calls. It is distinct from Primo Research
  Assistant's Boolean-variation→CDI→embedding-reranking pipeline; feature
  architecture and budgets are not transferred between the two.
- Explicit retrieval feedback uses searcher judgements; PRF assumes top
  ranked results relevant and constructs a later query after an initial
  ranking. An off-topic ranking can reinforce an early mistake. Diagrams
  are schematic, not a measured PRF run. Active-learning screening instead
  reprioritises an existing pool and does not inherently add candidates or
  construct a later retrieval pass.
- A fixed two-pass workflow can have result-dependent query contents while
  retaining a prescribed sequence. This alone does not establish agency.
  Chapter 12 asks who chooses the next action during a search.
- An LLM rewrite yields language/structured expressions, while SPLADE yields
  weighted vocabulary dimensions. Both can be inspected and passed between
  components; the form of the retrieval input is the distinction. No SPLADE
  weights or model outputs are measured in these drawings.
- The hypothetical text is the source's exact illustrative wording: “A study
  of the open-access citation advantage compares citation counts for open
  and subscription articles, accounting for discipline and publication year.”
  It names no identified study, supplies no finding and is labelled as a
  generated retrieval aid throughout. Query2doc expands a query using generated
  language, for lexical or dense retrieval. HyDE embeds the generated document
  and searches for real indexed sources from that vector. Real retrieval does
  not retroactively validate the generated assumptions. No actual Query2doc,
  HyDE or source-verification experiment was conducted.
- Product accounts are pinned documentation snapshots checked by the source
  in August 2026. EBSCO's cited public page does not identify its parser as an
  LLM. Web of Science Smart Search is distinct from Web of Science Research
  Assistant; the latter's supported document-request constraints do not imply
  support for complex field-tagged Boolean queries. No fresh service test,
  current support inventory or common architecture is inferred.
- Natural-language filter recognition is partial. Primo NDE has a defined
  list and documented author/OR failures. Primo Research Assistant has
  limited auto-refinements; manually changing a refinement switches that
  field to manual handling. Query-inferred and explicitly selected filters
  should be tested separately against known relevant records.
- Recording recommendations preserve the original input, generated text,
  structured conditions, routes, inferred/manual filters and intermediate
  results used for later queries. They are evaluation guidance, not claims
  that a fluent request is obeyed by every receiving component.

Checks cover source hashes/anchors, source table categories, the structured
expression and hypothetical text; reference taxonomy/feedback sequencing and
scoped reported audit shares; script/take/caption/word agreement and timing;
sampled drawing bounds, figure-note/table-cell bounds, note overlap and visual
review; complete media decoding and exact frames; 1080p/30fps H.264, stereo
48kHz AAC, −16 LUFS ±1 and peak below −1 dBTP; fast-start metadata and embedded
caption equality. Packaging checks MP4 hashes and ZIP CRCs. Chromium checks
real playback and responsive layouts. Earlier MP4 hashes are checked for
preservation before the local commit.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 11](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#query-transformation),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author
and book when sharing. This adaptation adds original narration and illustrations.
