# Chapter 7: Dense retrieval at collection scale

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 7, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **Same vectors, different winner** — independent encoding, cosine,
   dot product, normalisation, dimensionality and score interpretation.
2. **The neighbour you never visited** — term pointers and dense search;
   flat comparison; the chapter's six-point exact/approximate example;
   schematic HNSW navigation; top-k and separate candidate controls.
3. **Where does meaning enter?** — semantic goals and mechanisms;
   expansion, dense comparison and reranking; vocabulary bridging and
   compression; thresholds and stage budgets; the opening puzzle and
   dated Semantic Scholar/OpenAlex documentation accounts.

The direction continues the series with original paper-and-ink artwork,
curiosity-led questions, prediction pauses and evidence-led reveals.
Independently produced, with no affiliation with Veritasium. Narration uses
the standard Microsoft Andrew Multilingual synthetic voice. The adaptation
uses original drawings without presenter likeness, voice cloning, third-party
footage, copied product screenshots or reproductions of research figures.

## Reproduce and review

The production is isolated in new directories. The textbook, earlier tools
and exports are preserved. Generated media remain local and Git-ignored;
production sources are committed. Generation does not publish or push files.

From the repository root, with Python 3.12:

```bash
python -m pip install -r tools/chapter-7-investigations/requirements.txt
python tools/chapter-7-investigations/render.py --prepare-only
python tools/chapter-7-investigations/render.py --stills-only
python tools/chapter-7-investigations/render.py --render-only --workers 3
```

FFmpeg must be on PATH, or set `CHAPTER_FFMPEG`. System DejaVu fonts are used;
`PREFACE_FONT_DIR` can choose a folder containing `DejaVuSans.ttf`,
`DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf`. `--episode 1`, `2` or `3` selects
a film; `--output` chooses a destination. Shared media, speech-cache and
drawing helpers are reused without modification. No GPU, embedding model or
large search index is needed to reproduce the declared teaching examples.

Public narration text is sent to Microsoft's speech service through edge-tts.
The managed proxy CA is trusted with TLS verification retained. Narration is
cached by request and preserves its natural pace. Animation reveals follow
actual word timings; completed takes survive network failures.

Exports include 1920×1080, 30 fps H.264/AAC MP4s, burnt-in and embedded English
captions, SRT/VTT, timed transcripts, source-linked storyboards, posters,
review frames, contact sheets and verification reports. The responsive watch
gallery and ZIP contain all three films and supporting material. `plots`
contains standalone Matplotlib PNG/SVG figures, CSV similarity and neighbour
data, and a manifest verifying the assets against their recipe and values.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-7-investigations --port 8824
python tools/chapter-7-investigations/check-preview.py
python tools/chapter-7-investigations/render.py --package-only
```

Open `http://127.0.0.1:8824/index.html`. Browser checks require Playwright and
Chromium; they cover playback, seeking, captions, scene buttons, byte ranges
and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 7 section. Its hash, the full-book
hash and source commit appear in `source-provenance.json`. Each scene names
a chapter anchor. Source, script, shared helper and production hashes reject
stale timelines. Plot manifests verify figures and numeric data.

- Similarity figures use declared toy vectors Q=(1,0), A=(0.9,0.3), B=(1,1),
  C=(-0.4,0.8). Cosine ranks A/B/C; unnormalised dot product ranks B/A/C.
  Normalising query and candidates to unit length makes the scores agree.
  Scale invariance and cosine landmarks 1/0/−1 are independently checked.
  The exact coordinates are original teaching values, not model measurements
  or a claim to reproduce the chapter's raster similarity figure.
- The neighbour example preserves the chapter's exact coordinates:
  Q=(0,0), A=(1,0), B=(0,2), C=(2,2), D=(3,1), E=(4,3), F=(1,5).
  The renderer checks them against the pinned source SVG positions. This
  example uses Euclidean distance, not cosine at the zero vector. Distances
  are 1, 2, √8, √10, 5 and √26. Exact search examines all six and returns A/B/C.
  The stipulated approximate run examines A/B/D/F and returns A/B/D, missing
  the closer C. Both request k=3. Reference-distance tables include all six
  points for teaching; they do not imply the approximate run examined them all.
- The approximate example illustrates a possible miss, not a simulation of
  HNSW or a claim that ANN always misses. The multi-layer navigation graph is
  schematic, not an algorithm trace or measured path. No latency or speedup
  benchmark is claimed.
- Exactness is under a comparison rule, not a relevance guarantee. Nearest
  means best available under that rule. Dense scores are not calibrated
  relevance probabilities, and model/normalisation/comparison settings
  should match the encoder's training.
- Semantic describes an intended capability. The three routes across the
  heart-attack/myocardial-infarction wording gap are possible mechanisms, not
  guaranteed matches. In the reranking route, expansion supplies the lexical
  bridge before the document enters the shortlist.
- Vocabulary bridging requires suitable training. Compression can blur small
  decisive details. Threshold examples are possible yields, not measured score
  distributions. The 40→8→3 handoff counts are explicitly invented teaching
  budgets, independent of the chapter's named product budgets.
- The August 2026 Semantic Scholar counts and the author's quality assessment
  are reported from the pinned chapter. Its documented 2025 keyword→1,000
  candidates→LightGBM account does not identify the precise processing of
  those later interface queries. No general keyword superiority is claimed.
- OpenAlex Alice's 2026 account describes GTE Large EN, 1,024-dimensional
  title/abstract embeddings and cosine comparison. The April account reports
  413 million embeddings, including title-only works. Its semantic request
  is documented as an alternative to lexical request modes, not automatically
  a hybrid query. These are dated source accounts, not newly tested services.

Checks cover source hashes and anchors; exact ANN source coordinates;
cosine/dot scores, scale invariance, unit normalisation, Euclidean distances
and top-three sets; full caption/script/word agreement and nonoverlapping
timing; sampled layout bounds and visual review; full audio/video decoding,
exact frames, codecs, 1080p and 30 fps; stereo 48 kHz audio, −16 LUFS ±1 and
peak below −1 dBTP; fast-start metadata and embedded-caption equality.
Packaging checks MP4 hashes and ZIP CRCs. Chromium verifies playback and
responsive layouts. Earlier video hashes are checked before the local commit.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 7](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#dense-at-scale),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author
and book when sharing. This adaptation adds original narration and illustrations.
