# The Missing Paper

An original 45-second animated detective film promoting Aaron Tay's free online
textbook, *How Search Decides What You See*. The landscape and vertical versions
have independent compositions. The complete narrative is visible without sound.

## Reproduce the film

Run from the repository root on Windows with Python 3.11 or newer:

```powershell
py -3 -m venv outputs/promo-video/.venv
& './outputs/promo-video/.venv/Scripts/python.exe' -m pip install -r tools/promo-video/requirements.txt
& './outputs/promo-video/.venv/Scripts/python.exe' tools/promo-video/render.py --preview
& './outputs/promo-video/.venv/Scripts/python.exe' tools/promo-video/render.py --format both
```

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
- `poster-landscape.jpg`, `poster-vertical.jpg` — final-card poster previews.
- `contact-sheet-*.jpg` and `previews/` — storyboard frames for visual review.
- `score-original.wav`, `soundtrack.wav` — original and mastered stereo scores.
- `share-copy.txt` — sharing caption, both reader links, and video description.
- `preview.html` — local browser player with both videos and download links.
- `verification.json` and FFmpeg logs — export dimensions, duration, codecs,
  frame count, complete decoding, loudness, peak level, fast-start MP4 atom order,
  and SHA-256 hashes.

No external artwork, screenshots, stock footage, prerecorded music, or synthetic
narration is used. The score is synthesized from oscillators and seeded noise:
a sparse minor-key motif, typewriter clicks, paper rustle, rewind, and stamp;
it resolves into a major chord when the case is reopened. Mastering targets
−16 LUFS and −2 dBTP before AAC encoding, reserving a decibel for codec peak
overshoot. Verification measures the final AAC audio and enforces a −1 dBTP
ceiling.

Core vertical copy stays within x=86–994 and y=326–1670, avoiding the top and
bottom social-interface zones. Landscape headline/CTA copy uses x=130–1270;
illustrations are separately laid out to the right or beneath the headline.
Decorative borders, case time, and file numbers are not narrative information.

Inspect the contact sheets, transitional frames, and completed videos before
sharing. Publishing is a separate action. Put the supplied reader links in the
post accompanying the video, as promised by its "Link in post" CTA.
