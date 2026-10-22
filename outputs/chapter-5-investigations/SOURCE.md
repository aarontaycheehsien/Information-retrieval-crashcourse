# Chapter 5: Embeddings: what the learnt geometry encodes

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 5, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **The map nobody drew** — representations, vectors and embeddings;
   calculated weights and learnt parameters; self-supervised targets; CBOW
   and Skip-gram; analogy directions; projection loss and retrieval limits.
2. **One word, two locations** — static and contextual representations;
   self-attention; model tokens versus index terms; complete-text pooling;
   reproducibility, interpretation and relevance.
3. **The wrong prediction game** — CBOW, masked prediction and next-token
   prediction; language, domain and retrieval training; domain models;
   task suitability and a model's position in the search pipeline.

The direction continues the previous series with original paper-and-ink
artwork, curiosity-led questions, prediction pauses and evidence-led reveals.
Independently produced, with no affiliation with Veritasium. Narration uses
the standard Microsoft Andrew Multilingual synthetic voice. The adaptation
uses original drawings, without presenter likeness, voice cloning,
third-party footage or reproductions of research figures.

## Reproduce and review

The production is isolated in new directories. The textbook, earlier tools
and existing exports are preserved. Generated media remain local and
Git-ignored; production sources are committed. Nothing is published or pushed
as part of generation.

From the repository root, with Python 3.12:

```bash
python -m pip install -r tools/chapter-5-investigations/requirements.txt
python tools/chapter-5-investigations/render.py --prepare-only
python tools/chapter-5-investigations/render.py --stills-only
python tools/chapter-5-investigations/render.py --render-only --workers 3
```

FFmpeg must be on PATH, or set `CHAPTER_FFMPEG`. System DejaVu fonts are used;
`PREFACE_FONT_DIR` can select a folder containing `DejaVuSans.ttf`,
`DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf`. `--episode 1`, `2` or `3` selects a
film; `--output` selects a destination. Shared media, speech-cache and drawing
helpers are reused without modification. No GPU or trained embedding model
is needed to reproduce these declared teaching examples.

Public narration text is sent to Microsoft's speech service through edge-tts.
The managed proxy CA is trusted with TLS verification retained. Narration is
cached by request and preserves its natural pace. Animation reveals follow
actual speech timings; completed takes survive network failures.

Exports include 1920×1080, 30 fps H.264/AAC MP4s, burnt-in and embedded English
captions, SRT/VTT, timed transcripts, source-linked storyboards, posters,
review frames, contact sheets and verification reports. The responsive watch
gallery and ZIP contain all three films and supporting material. The `plots`
directory includes standalone Matplotlib PNG/SVG figures, numeric CSV data
and a manifest verifying the figures against their recipe and data.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-5-investigations --port 8822
python tools/chapter-5-investigations/check-preview.py
python tools/chapter-5-investigations/render.py --package-only
```

Open `http://127.0.0.1:8822/index.html`. Browser checks require Playwright and
Chromium; they exercise playback, seeking, captions, scene buttons, byte
ranges and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 5 section. Its hash, the full-book
hash and the source commit appear in `source-provenance.json`. Every scene
names an anchor in the chapter. Source, script, helper and production hashes
reject stale timelines. Figure manifests reject altered or stale assets.

- Both BM25 and neural encoders calculate outputs. The contrast concerns how
  the mapping is obtained: specified weighting rules versus fitted parameters.
  Reproducibility is separate from interpreting individual dimensions.
- The analogy uses explicitly constructed coordinates, not trained vectors.
  `king - man + woman = (5, 5)` equals the toy queen coordinate by construction.
  Candidate selection excludes the three input words. Real analogies can fail;
  neither their success nor a nearby point certifies meaning or relevance.
- The projection example is original and distinct from the chapter's research
  figure. P=(2,2,0) and Q=(2,2,10) have Euclidean distance 10; discarding their
  third coordinate gives distance 0. This is coordinate projection, not PCA.
  The chapter's selected country/capital PCA figure is described but not copied.
- Context markers and arrows are schematic. No contextual model run,
  attention-weight matrix or disambiguation accuracy is claimed. ELMo's
  earlier recurrent contextual representations are distinguished from
  Transformer-based self-attention.
- A declared character tokenizer splits lowercase `jobs` into `j`, `o`, `b`,
  `s`. An independent illustrative index analyser stems `jobs` to `job`.
  Neither example specifies a named model or production platform's analysis.
- The declared mean-pooling example averages (1,3), (3,1), (2,2) to (2,2).
  It demonstrates arithmetic, not a claim that generic BERT is an effective
  retriever or that mean pooling is universally appropriate.
- Prediction games use the chapter's sentence. CBOW has a declared two-word
  window around `heart`; masked prediction hides `treatment`; next-token
  prediction receives only the prefix before `after`. Hidden targets never
  appear in model input, and the next-token input contains no future words.
  The separate target is used by the training comparison. Word boxes simplify
  model-token tasks, and Skip-gram's reversed direction is explained.
- Language pretraining, domain pretraining and retrieval training remain
  distinct. Retrieval signals need not be human labels. No trained-model
  benchmark, guaranteed transfer or architecture diagnosis from a product
  family name is asserted.

Checks cover source hashes and anchors; toy arithmetic, projection and pooling;
prediction-target exclusion and context boundaries; full caption/script/word
agreement and nonoverlapping timings; sampled layout bounds and visual review;
complete audio/video decoding, exact frames, codecs, 1080p and 30 fps; stereo
48 kHz audio, −16 LUFS ±1 and peak below −1 dBTP; fast-start metadata and
embedded-caption equality. Packaging checks video hashes and ZIP CRCs.
Chromium verifies playback and responsive layouts. Earlier video hashes are
checked for preservation before the local commit.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 5](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#embeddings),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author
and book when sharing. This adaptation adds original narration and illustrations.
