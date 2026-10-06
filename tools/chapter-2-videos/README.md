# Chapter 2: three animated explainers

Three narrated films adapted from **Chapter 2, Boolean admission and the inverted
index**, in Aaron Tay's *How Search Decides What You See*. The maintained source
is `search-textbook.html#boolean-admission`, not the legacy `#ch2` anchor, which
now points to Chapter 3.

| Film | Topic | Initial duration |
|---|---|---|
| The gates of search | AND, OR, NOT; eligibility versus relevance; expansion and exclusion | 2:09 |
| What happens to your words? | Tokenisation, case normalisation, optional removal, stemming, lemmatisation, compatible analysers | 2:20 |
| The map that makes search fast | Inverted indexes, posting lists, set operations, sorted access, richer postings and coverage | 2:17 |

The visual direction is colorful flat-vector science animation: geometric
characters, a space library, living paper records, word-processing machines,
and diagrams with moving signals. All characters and artwork are original.
No studio characters, marks, footage, voice imitations, or music are used.
Segoe UI is loaded from Windows and is not redistributed.

## Reproduce

From the repository root on Windows, with Python 3.12:

```powershell
uv venv outputs/chapter-2-videos/.venv --python 3.12
uv pip install --python outputs/chapter-2-videos/.venv/Scripts/python.exe -r tools/chapter-2-videos/requirements.txt
& outputs/chapter-2-videos/.venv/Scripts/python.exe tools/chapter-2-videos/render.py
```

Useful modes:

```powershell
# Synthesize narration, master audio, write captions and review frames.
& outputs/chapter-2-videos/.venv/Scripts/python.exe tools/chapter-2-videos/render.py --prepare-only
# Render a prepared episode, retaining the cached speech and soundtrack.
& outputs/chapter-2-videos/.venv/Scripts/python.exe tools/chapter-2-videos/render.py --render-only --episode 1
# Rebuild review frames, or recheck completed exports.
& outputs/chapter-2-videos/.venv/Scripts/python.exe tools/chapter-2-videos/render.py --stills-only
& outputs/chapter-2-videos/.venv/Scripts/python.exe tools/chapter-2-videos/render.py --verify-only
# Local player with MP4 byte-range support.
& outputs/chapter-2-videos/.venv/Scripts/python.exe tools/promo-video/serve.py --directory outputs/chapter-2-videos --port 8773
```

Open `http://127.0.0.1:8773/preview.html`. `--episode 1`, `2`, or `3` selects a
single film; the default is all three. `--output` chooses another export folder.
Prepared episodes can be rendered in independent processes.

## Voice, timing and sound

The synthetic voice is Microsoft's `en-GB-RyanNeural` through `edge-tts`, at a
−3% rate, with no cloned voice. Synthesis sends only the public narration to
Microsoft's online speech service and needs internet access. Cached takes are
hashed by script, voice, rate, pitch and engine and reused on subsequent runs.
The narration helpers in `tools/pick-a-card/narrate.py` handle retries, exterior
silence trimming, per-take fixed gain, timeline construction and word timings.

The voice determines the scene durations. No word is cropped or time-stretched.
The case transformation and removal cues use returned word timings. English
captions are burned into the picture, embedded as a selectable MP4 subtitle
track, and exported as SRT and VTT files. A transcript is supplied for each film.

The score consists of original oscillator-generated, marimba-like arpeggios and
scene chimes. Smooth ducking keeps it below the narration. Separate voice and
music stems are exported. Each take must remain at least 10 dB above the score;
`mix-balance.json` records the measured margins. The mix is mastered in two passes to −16 LUFS with a
−2.5 dBTP pre-encoding target; final AAC measurements must be within 1 LU of
−16 LUFS and below −1 dBTP.

## Source and accuracy

- The scripts keep admission, relevance judgement and ranking separate.
- Text-analysis steps are explicitly illustrative or optional. Stemming and
  lemmatisation are not presented as synonym expansion or guaranteed semantics.
- D1–D4 and their selected posting lists follow the chapter's four-record
  example. Rendering checks those record texts against the maintained chapter
  and validates the demonstrated Boolean results. The A–D expansion records
  and the richer posting are illustrations.
- The sorted-pointer demonstration uses a separate, illustrative pair of lists.
- Full-text search is a capability, not a guarantee of complete-article coverage.
- The source chapter is hashed into each timeline and verification report.

## Outputs and checks

Generated media are local and Git-ignored under `outputs/chapter-2-videos/`.
`preview.html` presents all three films. Each episode folder contains:

- A 1920×1080, 30 fps MP4 with H.264 video, AAC stereo and embedded English captions.
- SRT, VTT, transcript, voice/music stems, mastered WAV and cached speech takes.
- Eight full-resolution scene stills, a poster and a contact sheet.
- Timeline, verification report, SHA-256 hashes and FFmpeg diagnostic logs.

Verification fully decodes every frame, confirms the frame count, dimensions,
frame rate and codecs, measures the final encoded audio, parses MP4 atom order
to check fast-start playback, and checks that extracted embedded subtitle text
matches every caption cue. Contact sheets and representative motion frames are
also visually reviewed. Automatic checks do not assess subjective performance.

The scripts, renderer and illustrations follow the repository's CC BY 4.0
licence. Credit Aaron Tay and the book when reusing adaptations.
