# The Missing Paper

An original 45-second animated detective film promoting Aaron Tay's free online
textbook, *How Search Decides What You See*. The landscape and vertical versions
have independent compositions. The complete narrative is visible without sound.
The default edition adds a warm female investigator voice, with optional English
captions. The narration is synthetic: Microsoft `en-GB-SoniaNeural`, generated
through [edge-tts](https://github.com/rany2/edge-tts).

## Reproduce the film

Run from the repository root on Windows with Python 3.11 or newer:

```powershell
py -3 -m venv outputs/promo-video/.venv
& './outputs/promo-video/.venv/Scripts/python.exe' -m pip install -r tools/promo-video/requirements.txt
& './outputs/promo-video/.venv/Scripts/python.exe' tools/promo-video/render.py --preview
& './outputs/promo-video/.venv/Scripts/python.exe' tools/promo-video/render.py --format both
```

To add or revise narration on the existing MP4s without rendering any pictures:

```powershell
& './outputs/promo-video/.venv/Scripts/python.exe' tools/promo-video/render.py --audio-only --format both
```

Speech synthesis requires an internet connection and sends the public narration
script to Microsoft's online speech service. Each scene's MP3 and returned word
timings are cached by script, voice, rate, and pitch under `narration-cache/` in
the output directory. Unchanged cached takes are reused without contacting the
service. Preserve that directory for local audio rebuilds. Changing a take's
text or settings creates a new cache entry; synthesis retries three times on
failure and does not replace an existing video with an unverified export.

`--audio-only` mixes the score and voice, uses FFmpeg `-c:v copy`, and verifies
SHA-256 identity of every compressed picture packet before replacing each MP4.
The first rebuild saves the original files as `*-music-only.mp4`. Subsequent
audio-only rebuilds leave those originals intact. `--music-only` produces the
original instrumental edition during a full render; use a separate `--output`
directory to retain the current narrated exports.

The renderer uses the Windows Georgia and Consolas font files in
`C:/Windows/Fonts`. Set `PROMO_FONT_DIR` to another directory containing those
files if needed. Fonts are loaded locally and are not redistributed. The
`imageio-ffmpeg` package supplies FFmpeg; `PROMO_FFMPEG` can point to an existing
FFmpeg executable with libx264 and AAC support instead.

`--format landscape` or `--format vertical` renders one composition.
`--output <directory>` changes the export directory. `--verify-only` fully
decodes and measures existing videos without rendering them again. The renderer
fails when its required fonts, source-book claims, or export checks do not pass.

For the local browser player, run the byte-range-enabled preview server:

```powershell
& './outputs/promo-video/.venv/Scripts/python.exe' tools/promo-video/serve.py
```

Open `http://127.0.0.1:8770/preview.html`. The server binds only to localhost;
Ctrl+C stops it. Byte ranges allow browser buffering and seeking through MP4s.

## Creative source

`storyboard.json` contains the timeline, principal copy, book identity, links,
and random seed. `render.py` contains the original paper character, illustrated
props, promotional cover, typography, animation, and synthesized score. Some
supporting labels and format-specific title breaks live in the renderer.
`narration.json` holds the editable spoken script, scene placements, synthesis
settings, ducking, and mastering targets. `narration.py` generates cached takes,
fits them within their scenes, mixes separate music/effects stems, writes word
timed captions, and replaces audio while retaining the picture stream.

The default voice uses natural pitch and a −5% rate. The opening and dense
chapter-list passages have +10% and +15% rate overrides to fit their scenes.
Exterior silence is trimmed while preserving pauses inside each take. The
renderer permits at most 10% additional pitch-preserving time compression; it
fails rather than cutting a word or crossing a scene boundary. All narration
ends before 44.5 seconds. Captions retain script punctuation and follow returned
word timings, adjusted for trimming and fitting. There is no voice cloning.

| Time | Story beat | Animated action |
|---|---|---|
| 0–4s | Missing: one relevant paper | Lamp switch, typewriter reveal, swinging poster |
| 4–10s | Real citations; crucial evidence absent | Genuine magnification of the answer graphic, citation stamps, empty evidence slot |
| 10–17s | Follow the search backwards | Camera pulls back; crooked red evidence thread straightens into the pipeline |
| 17–24s | The paper missed the candidate list | Three papers leave the index; Paper 07 stays behind and is circled |
| 24–30s | Reranking cannot add an excluded paper | Shortlisted papers change order; Paper 07 remains outside the boundary |
| 30–37s | Learn to investigate the pipeline | A librarian opens the book; an illuminated pipeline rises from its pages |
| 37–45s | Case reopened; read the textbook | Poster becomes the promotional cover; final title and CTA hold for eight seconds |

The search interface and papers are illustrative. They represent no named
product or actual research article. The cover is original promotional artwork
for the **online** textbook. The story identifies a possible failure location;
it does not suggest that all search omissions occur there, that citations alone
verify an answer's claims, or that reading the book recovers every missing paper.

The main explanation is grounded in the Preface and Chapter 9: reranking changes
a candidate pool's order but cannot add an excluded record. Chapters 13 and 14
provide the diagnosis and evaluation context. A fresh retrieval route can add
candidates; the illustrated reranker operates on its existing fixed pool.

## Exports and verification

Everything generated is kept in the Git-ignored `outputs/promo-video/`:

- `missing-paper-landscape.mp4` — 1920×1080, 30 fps, 45 seconds.
- `missing-paper-vertical.mp4` — 1080×1920, 30 fps, 45 seconds.
- `missing-paper-*-music-only.mp4` — preserved original instrumental editions.
- `poster-landscape.jpg`, `poster-vertical.jpg` — final-card poster previews.
- `contact-sheet-*.jpg` and `previews/` — storyboard frames for visual review.
- `score-original.wav`, `soundtrack.wav` — original and mastered stereo scores.
- `music-original.wav`, `effects-original.wav` — separately mixed score stems.
- `narration-only.wav`, `soundtrack-narrated.wav` — placed voice and final mix.
- `narration.srt`, `narration.vtt` — optional, timed English narration captions.
  The MP4s also contain an optional English subtitle track.
- `narration-transcript.txt` — complete spoken script and synthetic voice credit.
- `narration-manifest.json` — cached take hashes, placements, fitting, word
  timings, and caption timings.
- `share-copy.txt` — sharing caption, both reader links, and video description.
- `preview.html` — local browser player with both videos and download links.
- `verification.json` and FFmpeg logs — export dimensions, duration, codecs,
  frame count, complete decoding, loudness, peak level, fast-start MP4 atom order,
  and SHA-256 hashes.

No external artwork, screenshots, stock footage, or prerecorded music is used.
The score is synthesized from oscillators and seeded noise:
a sparse minor-key motif, typewriter clicks, paper rustle, rewind, and stamp;
it resolves into a major chord when the case is reopened. Speech is centered.
The unmastered music stem is raised by 8 dB to balance the leveled voice, then
falls by 10 dB and effects by 5 dB during each passage, with smooth
150 ms attacks and 400 ms releases. Each take is leveled before mixing.
Narrated mastering targets −16 LUFS and −2.5 dBTP before AAC encoding, allowing
for codec peak overshoot. Verification measures the final AAC audio, enforces
−16 LUFS within 1 LU and a −1 dBTP ceiling, and checks caption survival and
picture-stream identity. The instrumental edition retains its −2 dBTP target.

Core vertical copy stays within x=86–994 and y=326–1670, avoiding the top and
bottom social-interface zones. Landscape headline/CTA copy uses x=130–1270;
illustrations are separately laid out to the right or beneath the headline.
Decorative borders, case time, and file numbers are not narrative information.

Inspect the contact sheets, transitional frames, and completed videos before
sharing. For voice changes, check “Boolean,” “reranking,” and “Aaron Tay,” the
scene reveals, the final pause, and intelligibility with the music and effects.
The automatic timing and loudness checks do not judge voice performance.
Publishing is a separate action. Put the supplied reader links in the
post accompanying the video, as promised by its "Link in post" CTA.
