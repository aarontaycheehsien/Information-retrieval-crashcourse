# Chapter 4: Lexical search beyond strict Boolean

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 4, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **Three doors, one index** — all-term, minimum-match and any-match
   admission; stipulated ranking; top-k output; reported counts and display caps.
2. **One bad word, two failures** — compulsory exclusion versus optional
   scoring influence; the six-record Evidence Lab; rarity, synonym quality
   and the limits of term-frequency saturation.
3. **Four lives of a missing word** — analysis, rewriting, optional evidence
   and out-of-view matches; four query-processing jobs; natural-language
   input leading to lexical retrieval; evidence needed to identify a pipeline.

The direction continues the previous series with original paper-card artwork,
curiosity-led questions, prediction pauses, moving diagrams and evidence-led
reveals. Independently produced, with no affiliation with Veritasium. Narration
uses the standard Microsoft Andrew Multilingual synthetic voice. All artwork
and narration adaptation are original; no presenter likeness, voice cloning,
third-party footage or product screenshots are used.

## Reproduce and review

The new production directories preserve the textbook, existing tools and
earlier exports. Generated media remain local and Git-ignored; the reproducible
production sources are committed. Generation does not publish or push files.

From the repository root, with Python 3.12:

```bash
python -m pip install -r tools/chapter-4-investigations/requirements.txt
python tools/chapter-4-investigations/render.py --prepare-only
python tools/chapter-4-investigations/render.py --stills-only
python tools/chapter-4-investigations/render.py --render-only --workers 3
```

FFmpeg must be on PATH, or set `CHAPTER_FFMPEG`. System DejaVu fonts are used;
`PREFACE_FONT_DIR` can choose another folder containing `DejaVuSans.ttf`,
`DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf`. `--episode 1`, `2` or `3` selects
a film; `--output` selects its destination. Existing media, speech-cache and
drawing helpers are reused without modification. No GPU is required.

Public narration text is sent to Microsoft's speech service through edge-tts.
The managed proxy CA is trusted with TLS verification retained. Speech is
cached by request and keeps its natural pace. Reveals follow actual word
timings. Completed takes survive network failures.

Exports include 1920×1080, 30 fps H.264/AAC MP4s, burnt-in and embedded English
captions, SRT/VTT, timed transcripts, source-linked storyboards, posters,
review frames, contact sheets and verification reports. The responsive gallery
and ZIP contain all three films and their supporting material.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-4-investigations --port 8821
python tools/chapter-4-investigations/check-preview.py
python tools/chapter-4-investigations/render.py --package-only
```

Open `http://127.0.0.1:8821/index.html`. Browser checks require Playwright and
Chromium and cover actual playback, seeking, scene buttons, caption loading,
byte ranges and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 4 section; `source-lab.html` is the
supporting Evidence Lab from the same commit. Their hashes and the full-book
hash are recorded in `source-provenance.json`. Each scene names a source
anchor. Script, source, helper and production hashes reject stale timelines.

- The fruit cards preserve the chapter's term presence. Admission sets are
  computed independently. The order **B, A, C is stipulated**, not calculated
  from unspecified frequencies or lengths. The top-two example retains B/A;
  C was eligible and D was not.
- A and F preserve the lab's titles and matching evidence. Conditions and
  `foolish` document frequency are checked against all six original lab
  records. Only F contains `foolish`. No numerical A/F scores or ordering are
  asserted. The matched-term chips indicate presence, not equal score weights.
- Rarity is not synonym quality. Saturation limits gains from repetition
  inside a record; it cannot determine whether a query term serves the need.
  Suggested query comparisons are instructional, not new relevance experiments.
- The four missing-word histories are possible mechanisms. Optional analysis,
  explicit rewrites, unmatched optional terms and indexed-field differences
  are not inferred as the actual mechanism of a named product.
- Understanding interprets; transformation changes retrieval input.
  Understanding alone is not a fifth history removing a term. The illustrated
  question-to-Boolean rewrite is a teaching example, not a recorded model run.
- Google Scholar's supplied count and documented display cap are attributed
  to the pinned chapter. No current-service test is claimed. A display cap
  does not establish global top-k scoring or the complete retrieval architecture.
- Neither a natural-language input, a product name, a snippet nor a result
  count identifies dense retrieval. Semantic capability, representation and
  pipeline stage remain separate questions for Part II.

Checks cover source hashes and anchors; computed eligible sets and lab terms;
complete caption/script/word agreement and nonoverlapping timings; visual
layout samples; full audio/video decoding, exact frames, dimensions and codecs;
30 fps, stereo 48 kHz audio, −16 LUFS ±1, peak below −1 dBTP, fast-start metadata
and embedded-caption equality. Packaging checks MP4 hashes and ZIP CRCs.
Chromium verifies playback and responsive layouts. Previous video hashes are
checked for preservation before the local commit.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 4](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#beyond-boolean),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author and
book when sharing. This adaptation adds original narration and illustrations.
