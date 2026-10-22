# Chapter 8: Representations and indexed units

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 8, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **The vector hiding in keyword search** — the chapter's fixed seven-term
   vocabulary, binary presence, overlap versus Boolean admission, raw term
   frequency, TF–IDF, BM25 and inverted storage.
2. **Dense does not mean semantic** — independent questions about vectors,
   density, provenance and evidence; bibliographic facts, latent dimensions,
   learnt sparse weights and schematic SPLADE-style expansion.
3. **One paper, fifty searchable objects** — source documents, indexed units,
   independently pooled passage vectors, split evidence, indexed text versus
   later context, and grouping passage matches by paper identity.

The films continue the series with original paper-and-ink artwork,
curiosity-led questions, prediction pauses and evidence-led reveals.
Independently produced, with no affiliation with Veritasium. Narration uses
the standard Microsoft Andrew Multilingual synthetic voice. All drawings
and scripts are original adaptations; no presenter likeness, voice cloning,
third-party footage or copied product screenshots are used.

## Reproduce and review

The production lives in new isolated directories. Generated media remain
local and Git-ignored; production sources are committed. Generation does
not publish or push files. Shared media, speech-cache and drawing helpers
are reused without modification; earlier productions and textbook files
are preserved.

From the repository root with Python 3.12 and FFmpeg on PATH:

```bash
python -m pip install -r tools/chapter-8-investigations/requirements.txt
python tools/chapter-8-investigations/render.py --prepare-only
python tools/chapter-8-investigations/render.py --stills-only
python tools/chapter-8-investigations/render.py --render-only --workers 3
```

`CHAPTER_FFMPEG` can specify FFmpeg. System DejaVu fonts are used;
`PREFACE_FONT_DIR` can choose a folder containing `DejaVuSans.ttf`,
`DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf`. `--episode 1`, `2` or `3` selects
a film; `--output` chooses the destination. No GPU, embedding model or
large search index is needed for these declared teaching cases.

Public narration text is sent to Microsoft's speech service through
edge-tts. The managed proxy CA is trusted with TLS verification retained.
Takes are cached by text, voice and engine. Animation reveals follow real
word timings; natural narration is not cut or accelerated to fit visuals.

Exports include 1920×1080, 30 fps H.264/AAC MP4s, burnt-in and embedded English
captions, SRT/VTT, timed transcripts, source-linked storyboards, posters,
review frames, contact sheets and verification reports. The responsive
watch gallery and ZIP include all three films and supporting material.
`plots` contains standalone Matplotlib PNG/SVG figures, precise CSV data
and a hash manifest linking assets to the figure recipe and worked checks.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-8-investigations --port 8825
python tools/chapter-8-investigations/check-preview.py
python tools/chapter-8-investigations/render.py --package-only
```

Open `http://127.0.0.1:8825/index.html`. Browser checks require Playwright and
Chromium; they cover real playback, seeking, captions, scene buttons, byte
ranges and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 8 section. Its hash, the full-book
hash and source commit are recorded in `source-provenance.json`. Every scene
names a source anchor. Source, script, production and shared-helper hashes
reject stale timelines; figure manifests reject changed assets.

- The vocabulary order is exactly `[attack, cancer, heart, interview, job,
  tips, treatment]`. D1 is `heart attack treatment`, D2 `job interview tips`,
  D3 `cancer treatment`. Their source-exact binary vectors are respectively
  `[1,0,1,0,0,0,1]`, `[0,0,0,1,1,1,0]` and `[0,1,0,0,0,0,1]`.
- Query `heart treatment` has vector `[0,0,1,0,0,0,1]`. Shared-term counts
  are D1=2, D2=0, D3=1. Strict AND admits D1; OR admits D1/D3. Binary
  presence records evidence without specifying those retrieval operators.
- Repeating treatment three times in D1 gives raw TF `[1,0,1,0,0,0,3]`.
  This repeated collection has document lengths 5/3/2, average 10/3;
  heart has df=1 and treatment df=2. The original and repeated versions
  are clearly separated in the figures and arithmetic.
- TF–IDF numbers use the declared variant `raw TF × ln(N/df)`. BM25 numbers
  use `IDF × f(k1+1)/(f+k1(1−b+bL/avgL))`, with `k1=1.2`, `b=0.75` and
  `IDF=ln(1+(N−df+0.5)/(df+0.5))`. These are illustrative formula choices,
  not a claim that every implementation uses those variants. Comparisons
  describe representations, not a chronology of derivation.
- BM25's dot-product-style mathematical view does not establish dense
  storage, full scans or nearest-neighbour execution. Active vocabulary
  entries support efficient inverted-index accumulation.
- The fully active bibliographic example `[2026,14,32,87]` preserves the
  source's year/pages/references/citations values. Density alone establishes
  no semantic text-matching capability. Latent coordinate values illustrate
  structure, not measured encoder outputs or interpretable single concepts.
- The learnt sparse example follows the chapter's heart/attack versus
  myocardial/infarction bridge. Weights 1.2/1.0/0.8/0.7 are invented and
  labelled, not model measurements. Whole-word labels simplify the real
  standard SPLADE WordPiece output vocabulary. The drawn grids are schematic,
  not measured sparsity rates. Training-dependent expansion is possible,
  not guaranteed for a particular model or input.
- A vocabulary expansion can create shared coordinates for an appropriately
  represented query. This does not itself establish useful ranking or a
  performance advantage. Sparsity constraints affect active entries;
  implementation and posting distributions determine actual retrieval cost.
- Sparse/dense describes shape; specified/learnt describes rule provenance;
  dimensions preserve different evidence. Dot product and cosine can apply
  to different representations without determining their shape or capability.
- One abstract, ten sections and fifty overlapping passages are the chapter's
  alternative teaching choices for an illustrative 20-page article, not
  measured product settings. The conventional bi-encoder maps each indexed
  unit to one pooled vector. Ten drawn passage/vector pairs illustrate the
  mapping; the film explicitly states that fifty units imply fifty vectors.
- The adults/outcome/limitation example is an original illustration. Splitting
  or overlapping passages does not automatically combine evidence spread
  across units. No numerical outcome or retrieval score is fabricated.
- The source describes Wiley AI Gateway full-text chunks, contrasted with
  discovery records described by metadata/abstracts. This is a pinned source
  account, not a fresh service test. An abstract-only stage cannot directly
  match absent results text, but may select the paper on other evidence.
  A later fetch may supply full text or neighbouring/parent material.
- The source-exact passage matches are A2/A7/B3/A9, grouped as paper A with
  passages 2/7/9 and paper B with passage 3. Four matches are two papers.
  Source grouping specifies neither a paper-score formula nor answer synthesis.
  Indexed text, retrieved units and supplied generator context are separate.

Checks cover source hashes and anchors; vocabulary/order, binary vectors,
overlap/admission sets, raw TF, df, declared TF–IDF and BM25 arithmetic,
diminishing returns and grouping counts; complete caption/script/word
agreement and timing; sampled layout bounds and visual review; full media
decoding, exact frame counts, 1080p/30fps H.264, stereo 48kHz AAC, −16 LUFS ±1
and peak below −1 dBTP; fast-start metadata and embedded-caption equality.
Packaging checks final MP4 hashes and ZIP CRCs. Chromium verifies actual
playback and responsive layouts. Earlier MP4 hashes are checked for preservation.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 8](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#representations-and-units),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author
and book when sharing. This adaptation adds original narration and illustrations.
