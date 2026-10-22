# Chapter 2: Boolean admission and the inverted index

Three original animated explainers adapted from Aaron Tay's *How Search Decides
What You See*, Chapter 2, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **The word that opened the gate** — AND, OR, NOT, weak expansion,
   compulsory conditions, eligibility, ranking and relevance.
2. **The word you never searched** — tokens, optional analysis, stemming,
   lemmatisation, compatibility, truncation and different field analysers.
3. **Search without rereading the papers** — the D1–D4 collection, inverted
   indexes, posting lists, set operations, selective and ordered access, richer
   postings, full-text-search terminology and the transition to ranking.

The direction continues the previous series with original paper-card artwork,
curiosity-led questions, prediction pauses, moving diagrams and evidence-led
reveals. Independently produced, with no affiliation with Veritasium. Narration
uses the standard Microsoft Andrew Multilingual synthetic voice, with no voice
clone, presenter likeness, third-party footage or product screenshot.

## Reproduce and review

The production is isolated in new folders. It preserves the textbook, earlier
productions and existing exports. Generated media are local and Git-ignored;
production sources are committed separately. No publication or remote push is
part of generation.

From the repository root, with Python 3.12:

```bash
python -m pip install -r tools/chapter-2-investigations/requirements.txt
python tools/chapter-2-investigations/render.py --prepare-only
python tools/chapter-2-investigations/render.py --stills-only
python tools/chapter-2-investigations/render.py --render-only --workers 3
```

FFmpeg must be on PATH, or set `CHAPTER_FFMPEG`. System DejaVu fonts are used;
`PREFACE_FONT_DIR` can select a folder containing `DejaVuSans.ttf`,
`DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf`. `--episode 1`, `2` or `3` selects a
film; `--output` chooses the destination. `--workers` controls local encoder
processes. The existing Chapter 1 media engine, shared speech helper and
preface drawing primitives are reused without modification. No GPU or paid
video-generation API is required.

Public narration text is sent to Microsoft's speech service through edge-tts.
The managed proxy CA is trusted with TLS verification retained. Speech is
cached by its request, never cut or sped up to fit the picture. Reveals use
actual speech timings. Network failures preserve completed takes.

Exports include 1920×1080, 30 fps H.264/AAC MP4s, burnt-in and embedded English
captions, SRT/VTT, timed transcripts, source-linked storyboards, posters,
review frames, contact sheets and verification reports. The gallery and ZIP
contain all three films and their supporting material.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-2-investigations --port 8819
python tools/chapter-2-investigations/check-preview.py
python tools/chapter-2-investigations/render.py --package-only
```

Open `http://127.0.0.1:8819/index.html`. Browser checks require Playwright and
Chromium and cover playback, seeking, scene buttons, caption loading, byte
ranges and desktop/tablet/mobile layout.

## Grounding and limits

The pinned chapter snapshot and provenance accompany the script. Source,
script and production hashes reject stale timelines. Every scene names an
anchor in that chapter. The source anchor is `#boolean-admission`; the legacy
`#ch2` anchor is not used.

- D1–D4 retain the chapter's exact texts. The six displayed posting lists are
  checked against both the chapter and an independent calculation from those
  records. AND, OR and NOT results are computed, not entered as untested labels.
- Example E, illustrating a weak OR expansion, is additional and labeled as
  invented. Whether a record is useful remains conditional on the information
  need; `delulu` is not used as a real relevance benchmark.
- Analysis outputs are explicitly illustrative. Lowercasing, removal and
  stemming are separate operations; optional steps are not presented as
  universal database behavior. Stems need not be words. Lemmatisation depends
  on grammatical interpretation. Neither operation is equated with synonyms,
  controlled vocabulary, truncation or guaranteed semantics.
- An incompatible `jobs`/`job` lookup misses without an additional mapping.
  Compatible query and document analysis need not run identical operations.
  The exact tokenizer, stop list or stemmer of a named product is not inferred.
- The pointer animation uses separate illustrative sorted lists. The trace
  advances only forwards and returns the independently checked intersection
  `{4, 13}`. No response time, measured speedup or universal latency is claimed.
- The richer posting is illustrative: D1 contains one `job` at one-based word
  position 2. Its field name is an example, not a claim about a real index.
- Full-text search is a capability, not a guarantee of complete-publication
  coverage, retention of every word or one particular admission/ranking method.
- Boolean admission, ordering and usefulness are kept separate throughout.

Checks validate source records and anchors, Boolean sets and pointer motion,
caption/script/word agreement and nonoverlapping timing, layout samples,
complete video/audio decoding and exact frame counts, codecs and dimensions,
30 fps, stereo 48 kHz audio, −16 LUFS ±1 and peaks below −1 dBTP, fast-start
metadata and embedded subtitle text. Packaging verifies MP4 hashes and ZIP
CRCs. Real Chromium playback accompanies these checks.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 2](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#boolean-admission),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author and
book when sharing. This adaptation adds original narration and illustrations.
