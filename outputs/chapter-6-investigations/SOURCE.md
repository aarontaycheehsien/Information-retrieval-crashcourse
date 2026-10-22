# Chapter 6: From language model to retrieval encoder

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 6, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **The vector we actually store** — model tokens versus indexed terms;
   input coverage; token IDs, initial and contextual vectors; pooling;
   independent encoding; single-vector and late-interaction boundaries.
2. **The result that almost answers** — the chapter's stated information
   need, positive, easy negative and hard negative; desired comparisons;
   SBERT and DPR; the ingredients shaping retrieval training.
3. **Whose idea of relevance?** — clicks, answers, titles and citations;
   SPECTER; transfer across tasks and collections; fine distinctions;
   diagnosis before attributing a failure to training.

The direction continues the series with original paper-and-ink artwork,
curiosity-led questions, prediction pauses and evidence-led reveals.
Independently produced, with no affiliation with Veritasium. Narration uses
the standard Microsoft Andrew Multilingual synthetic voice. The adaptation
uses original drawings without presenter likeness, voice cloning, third-party
footage or copied product screenshots or research figures.

## Reproduce and review

The production is isolated in new directories. The textbook, earlier tools
and exports are preserved. Generated media remain local and Git-ignored;
production sources are committed. Generation does not publish or push files.

From the repository root, with Python 3.12:

```bash
python -m pip install -r tools/chapter-6-investigations/requirements.txt
python tools/chapter-6-investigations/render.py --prepare-only
python tools/chapter-6-investigations/render.py --stills-only
python tools/chapter-6-investigations/render.py --render-only --workers 3
```

FFmpeg must be on PATH, or set `CHAPTER_FFMPEG`. System DejaVu fonts are used;
`PREFACE_FONT_DIR` can choose a folder containing `DejaVuSans.ttf`,
`DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf`. `--episode 1`, `2` or `3` selects
a film; `--output` chooses a destination. Shared media, speech-cache and
drawing helpers are reused without modification. No GPU or trained encoder
is needed to reproduce the declared numeric teaching examples.

Public narration text is sent to Microsoft's speech service through edge-tts.
The managed proxy CA is trusted with TLS verification retained. Narration is
cached by request and preserves its natural pace. Animation reveals follow
actual word timings; completed takes survive network failures.

Exports include 1920×1080, 30 fps H.264/AAC MP4s, burnt-in and embedded English
captions, SRT/VTT, timed transcripts, source-linked storyboards, posters,
review frames, contact sheets and verification reports. The responsive watch
gallery and ZIP contain all three films and supporting material. `plots`
contains standalone Matplotlib PNG/SVG figures, CSV score and pooling data,
and a manifest verifying the assets against their recipe and source data.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-6-investigations --port 8823
python tools/chapter-6-investigations/check-preview.py
python tools/chapter-6-investigations/render.py --package-only
```

Open `http://127.0.0.1:8823/index.html`. Browser checks require Playwright and
Chromium; they cover playback, seeking, captions, scene buttons, byte ranges
and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 6 section. Its hash, the full-book
hash and source commit appear in `source-provenance.json`. Each scene names
a chapter anchor. Source, script, shared helper and production hashes reject
stale timelines. Plot manifests verify exported figures and numeric data.

- The query and three passages preserve the chapter's exact text. The stated
  need is judging unrealistic expectations. The interview passage is a hard
  negative for that need and could be useful under another interpretation.
  The example does not demonstrate a pretrained model understanding slang.
- The declared tokenizer splits `delulu` into six characters. Its limited toy
  vocabulary maps d/e/l/u to IDs 3/8/11/21. These IDs and the initial vectors
  are invented lookup examples, not any named model's tokenizer or embedding.
  Being able to tokenize a string does not establish understanding.
- Six supplied contextual vectors sum to (6,6,12), with mean (1,1,2).
  This is checked arithmetic, not a contextual encoder run. The repeated `l`
  input starts from the same toy lookup vector but has different supplied
  contextual representations at different positions. Model tokens are not
  the dimensions of the final pooled vector.
- Independent query and passage encoding can share or use distinct parameters.
  The stored-vector boundary describes conventional single-vector retrieval;
  late-interaction methods can retain multiple token vectors instead.
- The cosine comparison is a constructed two-dimensional example. The query
  is (1,0), and all passage vectors have unit length. The positive has angle
  80° initially and 20° in the desired arrangement; the hard negative has
  30° and 70°; the easy negative has 140° and 150°. The initial order is
  hard/positive/easy and the desired order positive/hard/easy. Neither picture
  is measured model behavior or an actual training state. Their transition
  does not assert an optimisation trajectory. Scores are not probabilities.
- SBERT and DPR are described as influential examples of training independent
  representations for intended comparisons. The film does not claim that
  pooling or a model family name alone makes an effective retriever.
- Clicks, answers, titles, citations and other labels teach different proxies
  for usefulness. The citation graph is schematic, not SPECTER training data.
  Citations do not establish agreement, direct answers or review eligibility.
- `CMP-104` and `CMP-140` are invented identifiers. No chemical facts, trained
  model scores, benchmark results or measured identifier failures are asserted.
- Training mismatch is a hypothesis. Coverage, fields, query processing and
  candidate cut-offs also require inspection and local evaluation. The source
  scenario does not establish whether domain pretraining took place.

Checks cover source hashes, anchors and exact passage text; lookup IDs,
pooling sums, vector norms, cosine values and ranking order; caption/script/
word agreement and nonoverlapping timing; sampled layout bounds and visual
review; full audio/video decoding, exact frames, codecs, 1080p and 30 fps;
stereo 48 kHz audio, −16 LUFS ±1 and peak below −1 dBTP; fast-start metadata
and embedded-caption equality. Packaging checks MP4 hashes and ZIP CRCs.
Chromium verifies playback and responsive layouts. Earlier video hashes are
checked for preservation before the local commit.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 6](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#retrieval-encoder),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author
and book when sharing. This adaptation adds original narration and illustrations.
