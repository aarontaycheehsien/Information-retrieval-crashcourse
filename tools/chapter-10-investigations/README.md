# Chapter 10: Hybrid retrieval and rank fusion

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 10, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **Two models do not make a hybrid** — complementary evidence, the chapter's
   distinction between hybrid candidate routes and sequential processing,
   single-stage blending, parallel retrieval plus reranking, and routing.
2. **How two lists become one** — the exact lexical A/B/C and dense C/A/D
   lists; per-record RRF contributions; identity reconciliation; the order
   A/C/B/D; input depth, fusion constant and display depth.
3. **What the fused ranking cannot tell you** — lost score gaps, the constant,
   input cutoffs, explicit route weights, blending versus query-time routing,
   Web of Science/Scopus documentation accounts, and Scopus AI's 2024
   query-variant RAG Fusion account.

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
python -m pip install -r tools/chapter-10-investigations/requirements.txt
python tools/chapter-10-investigations/render.py --prepare-only
python tools/chapter-10-investigations/render.py --stills-only
python tools/chapter-10-investigations/render.py --render-only --workers 3
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
contains standalone Matplotlib PNG/SVG figures, exact-fraction CSV data and
a manifest linking assets to the recipe and checked examples. Figure-level
notes are wrapped and their drawing bounds verified before export.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-10-investigations --port 8827
python tools/chapter-10-investigations/check-preview.py
python tools/chapter-10-investigations/render.py --package-only
```

Open `http://127.0.0.1:8827/index.html`. Browser checks require Playwright and
Chromium and exercise actual playback, seeking, captions, scene buttons,
byte-range responses and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 10 section. Source commit, full-book
hash and section hash are in `source-provenance.json`. Every scene names an
anchor from that section. Runtime checks parse the source table and compare
record identities, both input ranks, fused ranks and rounded scores with the
computed example. Source, script, production and shared-helper hashes reject
stale timelines. Prepared take IDs and text must match the final script;
plot manifests reject changed assets.

- The book's operational definition combines candidates or scores from
  multiple candidate-generation routes. BM25 followed by a cross-encoder is
  multi-stage with one such route. A single scoring stage blending lexical
  and dense candidate evidence is the source's counterexample of hybrid
  without a multi-stage cascade. Parallel retrieval, fusion and a later
  reranker can be both. Vendor use of the label can differ.
- AX-317A and the heart-attack/myocardial-infarction wording bridge are original
  illustrative strings, not model runs. Analysed lexical terms may preserve
  identifiers; trained dense representations may bridge paraphrases. Neither
  recovery nor better task performance is guaranteed by the diagram.
- The source's lexical list is A/B/C and dense list C/A/D. A/C occur in both;
  B/D occur in one supplied list each. The union has four distinct identities
  from six occurrences, not four new relevance judgements. A repeated record
  contributes from both lists but appears once in the fused output. Identity
  reconciliation is not a claim that similar texts are equivalent records.
- Equal-weight RRF computes the sum of `1/(c+rank)` for supplied occurrences;
  ranks begin at 1 and a missing occurrence contributes zero from that list.
  With source constant `c=60`, exact scores are A=`123/3782`, C=`124/3843`,
  B=`1/62`, D=`1/63`, rounded to 0.03252/0.03227/0.01613/0.01587. The fused
  order is A/C/B/D. Arithmetic uses Python Fraction, not rounded intermediate
  values. The formula is attributed in the textbook to Cormack, Clarke and
  Büttcher (2009). It is an unsupervised fusion rule, not a trained relevance
  model, a reranker reading text, or a relevance probability.
- The constant is `c` in the book to distinguish it from top-k output depth;
  the original paper used `k`. The source baseline 60 followed pilot testing
  and is not asserted optimal for every task. Our derived comparison with
  `c=0` shows first-versus-third contributions of 1 versus 1/3; at `c=60`
  they are 1/61 versus 1/63. Plotted curves normalise each to its rank-one
  contribution to show the change in relative advantage; the table and CSV
  preserve actual values. These are formula-derived curves, not model scores.
- Arbitrary raw-score sets A/B/C = 0.90/0.89/0.88 and 90/8/1 demonstrate lost
  gaps. Both have the same ranking and therefore identical RRF results when
  paired with the unchanged dense list. They are alternative teaching score
  sets, not measured BM25/embedding scores or two extra retrieval routes.
- Cutting both inputs to depth 2 supplies A/B and C/A. D disappears from the
  pool; C loses its lexical 1/63 contribution. Fusing the full inputs and
  showing only the top two instead retains all four identities in the fused
  pool and hides B/D at a later display boundary. Missing from a supplied
  input is not judged irrelevant or absent from the full collection.
- The explicitly weighted extension multiplies dense contributions by 2 and
  keeps lexical contributions at 1. Its order is C/A/D/B: C narrowly passes A,
  and D also passes B. This is a reproducible mathematical variation, not the
  chapter's equal-weight baseline or a recommended quality setting. Example
  ties are handled alphabetically for reproducibility; RRF itself does not
  prescribe that tie rule.
- Web of Science Smart Search's pinned account describes structured Boolean
  parsing and document search that can blend Boolean keyword and semantic
  vector paths. Parsing is query transformation; combining candidate paths
  is the hybrid component. Scopus AI's pinned routing account chooses lexical,
  vector or both per question. A one-route run combines nothing; both routes
  still need fusion. No particular fusion rule is inferred for either current
  product from these descriptions alone.
- Elsevier's separate 2024 Scopus AI RAG Fusion account describes generated
  variants, vector retrieval per variant, RRF merging and a summary from top
  merged results with references required for claims. This is multiple variant
  lists rather than lexical-plus-dense lists for one query. RRF's presence
  establishes neither different retrieval methods nor a later version's route
  choices. These are pinned documentation accounts, not fresh service tests.
- Routing can be implemented by a rule, classifier or model and does not
  alone establish agency. Fusion choices and the routes that actually ran
  must be exposed to explain a result. RRF is a baseline to compare with its
  individual retrievers on representative queries, not a quality guarantee.

Checks cover pinned source hashes/anchors and all source table ranks/scores;
exact fractions and fused order; set membership and cutoffs; weight changes;
constant ratios and score-gap invariance; final script/take/caption/word
agreement and timing; sampled drawing bounds, figure-note bounds and visual
review; full media decoding and exact frames; 1080p/30fps H.264, stereo 48kHz
AAC, −16 LUFS ±1 and peak below −1 dBTP; fast-start metadata and embedded-caption
equality. Packaging checks MP4 hashes and ZIP CRCs. Chromium checks actual
playback and responsive layouts. Earlier MP4 hashes are checked for preservation
before the local commit.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 10](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#hybrid-and-fusion),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author
and book when sharing. This adaptation adds original narration and illustrations.
