# Chapter 1: The retrieval problem

A 7-minute, 9-second narrated geometric explainer adapted from Chapter 1 of
Aaron Tay's *How Search Decides What You See*, version 1.2.1. Its dark canvas,
colored geometric objects, evolving sets, and speech-led reveals are inspired
by 3Blue1Brown's visual teaching approach. All animation is original; this is
an independently produced adaptation.

The film covers the chapter's central question, the documented Primo example,
retrieval versus generation, the shortlist bottleneck, the six-stage map,
the output/iteration matrix, information need versus query, four relevance
perspectives, all three opening puzzles, and a closing diagnostic exercise.
It preserves the chapter's open questions about undocumented mechanisms.

## Reproduce

From the repository root, with Python 3.12 and `uv`:

```powershell
uv venv outputs/chapter-1-video/.venv --python 3.12
uv pip install --python outputs/chapter-1-video/.venv/Scripts/python.exe -r tools/chapter-1-video/requirements.txt
& './outputs/chapter-1-video/.venv/Scripts/python.exe' tools/chapter-1-video/render.py --workers 6
```

If Python is supplied by the Codex bundled runtime, pass its executable path
to `uv venv --python` instead. Nothing needs Manim, LaTeX, a GPU, or a video
generation API.

- `--prepare-only`: synthesize/cache speech and write the timeline, captions,
  transcript, and mastered narration before working on pictures.
- `--stills-only`: use that prepared timeline to generate 45 review stills,
  a contact sheet, poster, and browser player.
- `--verify-only`: completely decode and measure the final MP4 again.
- `--workers N`: use one to eight frame-rendering processes; reduce this on
  machines with limited RAM. Six processes need approximately 4 GB free RAM.
- `--output PATH`: keep exports and voice caches in another directory.

The renderer imports `tools/pick-a-card/narrate.py` for speech synthesis,
word-boundary validation, cached takes, exterior-silence trimming, and cue
construction. It does not edit that tool or its output. Unchanged takes are
reused, and animation changes require no new speech requests. The video
timeline follows the speech without shortening or speeding up takes.

The synthetic voice is Microsoft's `en-US-AndrewMultilingualNeural`, at a
−5% rate and natural pitch, using [edge-tts](https://github.com/rany2/edge-tts).
Synthesis sends the public narration script to Microsoft's online speech
service and requires an internet connection for uncached takes. No voice
cloning, recorded music, stock artwork, or product screenshots are used.
The soundtrack contains narration only.

Georgia, Segoe UI, Consolas, and Segoe UI Symbol are loaded locally from
`C:/Windows/Fonts`; set `CHAPTER_FONT_DIR` to another directory containing the
same filenames if necessary. Font files are not redistributed. FFmpeg is
supplied by `imageio-ffmpeg`; `CHAPTER_FFMPEG` can select an existing binary
with H.264 and AAC support.

## Editable source

`script.json` contains the spoken lines, scene order, voice settings, pauses,
and each scene's source anchor. `scenes.py` contains the original vector-like
geometry, typography, and transformations. Reveals are anchored to spoken
words, including the shortlist selection, information-need requirements,
pipeline stages, four quadrants, and puzzle quantities.

`render.py` prepares sound and captions, renders independent frame chunks,
joins them without re-encoding, muxes sound, and verifies the export before
replacing a previous completed video. It retains intermediates for diagnosis.
The mathematical subset symbols use an explicit symbol font; the paper-dot
animation retains faint copies to show that retrieval does not delete records
from the index. The Google Scholar count comparison uses a labelled logarithmic
scale. The Semantic Scholar bars are illustrative, with the enlargement of the
13-result bar disclosed and the approximately 2,715-fold ratio stated separately.

## Source and limits

The maintained source is `search-textbook.html#intro`. These scenes map to
the chapter's own sections; the renderer checks anchors and distinctive
quantities before building sound and records source/script SHA-256 hashes.
These guards detect some source drift; they do not replace editorial review.

| Scenes | Chapter source |
| --- | --- |
| An answer appears | `#an-answer-appears` |
| Two machines; bottleneck; missing paper | `#retrieval-not-generation` |
| Primo pipeline; six-stage map | `#anatomy-of-a-cited-answer` |
| Output versus retrieval iteration | `#retrieval-not-generation` |
| Need; matching; relevance perspectives | `#what-does-relevant-actually-mean` |
| Three puzzles | `#three-familiar-search-results-and-three-puzzles` |
| Diagnostic exercise | Chapter 1's first self-check |
| Closing questions | `#a-map-of-the-arguments-ahead` |

Primo's steps retain the chapter's September 2026 documentation date. The
[Ex Libris guide](https://knowledge.exlibrisgroup.com/Primo/Product_Documentation/020Primo_VE/Primo_VE_%28English%29/015_Getting_Started_with_Primo_Research_Assistant)
was also read while preparing this adaptation and supports the Boolean-OR,
up-to-30, embedding-rerank, five-source, abstract-based overview sequence.
[Google Scholar help](https://scholar.google.com/intl/en/scholar/help.html)
documents the 1,000-result display boundary. The 9.4-million total and
Semantic Scholar's 13/35,300 comparison remain the chapter's recorded
observations; the latter is dated August 2026. The film makes no new
behavioural-test claim about those products.

Paper tokens are illustrative records. The subset relationship applies to
one illustrated retrieval round with a fixed candidate pool; a further
retrieval action can add candidates. Supplied evidence constrains
source-supported coverage, while generation can still use model parameters,
invent unsupported claims, or omit a supplied source. The visual matrix
classifies output and iteration, not agency. Matching is evidence about
relevance rather than a substitute for the reader's judgement.

Text is adapted under CC BY 4.0, with Aaron Tay credited in the video, player,
and transcript. Third-party figures and logos are not reproduced.

## Outputs and checks

Everything generated stays under Git-ignored `outputs/chapter-1-video/`:

- `chapter-1-the-retrieval-problem.mp4`: 1920×1080, 30 fps, H.264/AAC stereo,
  429.43 seconds, with fast-start metadata for browser playback.
- Matching `.srt` and `.vtt`: 176 optional English caption cues.
- `chapters.vtt` and `preview.html`: player with fifteen clickable scene links.
- `transcript.txt`: timed narration, attribution, and synthetic-voice credit.
- `poster.jpg`, `contact-sheet.jpg`, and `stills/`: visual QA artifacts.
- `timeline.json`, `captions.json`, `voice-cache/`: reproducible timing/assets.
- `narration.wav`, intermediate pictures, logs, and `verification.json`.

Each export completely decodes both streams and checks exact frame count,
resolution, frame rate, pixel format, stereo AAC sample rate, −16 LUFS ±1
integrated loudness, a −1 dBTP peak ceiling, and MP4 atom order. Captions are
checked for positive durations, bounds, and non-overlap. Inspect the stills
and playback as well: those automatic checks do not assess teaching quality
or the narrator's performance.

For a local player with seeking support, reuse the book's byte-range server:

```powershell
& './outputs/chapter-1-video/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-1-video --port 8772
```

Open `http://127.0.0.1:8772/preview.html`. This binds only to localhost.
Publication or uploading the film is a separate action.
