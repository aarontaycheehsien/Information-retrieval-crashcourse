# A universe of research

An original 72-second animated promotion for Aaron Tay's free online textbook,
*How Search Decides What You See*, aimed at librarians. Saturated flat shapes,
cosmic metaphors, playful character animation, and clear science narration draw
on the broad qualities of Kurzgesagt-style explainers. All illustrations,
characters, cover artwork, and music are original; the film is independently
produced. The illustrated cover promotes the online textbook.

## Deliverables

Generated files live in `outputs/librarian-promo/`, ignored by Git:

- `how-search-decides-librarian-promo.mp4`: 1920 × 1080, 30 fps, H.264/AAC;
  narrated, with an optional embedded English subtitle track.
- Matching `.srt` and `.vtt` captions, `transcript.txt`, and `share-copy.txt`.
- `preview.html`: browser player, scene navigation, and downloads.
- `poster.jpg`, `contact-sheet.jpg`, and three review stills per scene.
- `timeline.json`, `captions.json`, and `verification.json`.
- Cached speech, separate original music/effects, voice stem, and mastered mix.
- `encoded-contact-sheet.jpg` and `encoded-review.json` from `review.py`.

The rendered duration follows the narration; changing the script or voice can
change the duration. The initial production runs 72.30 seconds with a five-second
final quiet hold. There is no time compression or voice cloning.

## Reproduce

Use Python 3.12 on Windows. Run from the repository root:

```powershell
py -3.12 -m venv outputs/librarian-promo/.venv
& './outputs/librarian-promo/.venv/Scripts/python.exe' -m pip install -r tools/librarian-promo/requirements.txt
& './outputs/librarian-promo/.venv/Scripts/python.exe' tools/librarian-promo/render.py
& './outputs/librarian-promo/.venv/Scripts/python.exe' tools/librarian-promo/review.py
```

The renderer uses the existing narration/cache module at
`tools/pick-a-card/narrate.py` and the encoding/verification engine at
`tools/chapter-1-video/render.py`. It changes their settings only in its own
Python process. It does not edit their files or existing films.

Narration uses Microsoft's synthetic `en-GB-RyanNeural` voice through `edge-tts`.
First synthesis requires internet access and sends the public script to the
Microsoft speech service. Unchanged cached takes are reused offline. Fonts are
read from `C:/Windows/Fonts` (Segoe UI regular and bold); set `CHAPTER_FONT_DIR`
to another directory containing those files. Font files are not redistributed.
`imageio-ffmpeg` supplies FFmpeg, or set `CHAPTER_FFMPEG` to an executable with
H.264/AAC support.

Use `--prepare-only` for voice, music, captions, and the timeline; `--stills-only`
to review layouts; `--render-only` to encode from a current prepared timeline;
and `--verify-only` to repeat full decoding and audio measurement. Production
and source hashes prevent using a stale timeline. `--output <directory>` selects
another export directory. Two encoding processes are used by default; change
this with `--workers` (1–8).

Start the existing byte-range-enabled server for reliable playback and seeking:

```powershell
& './outputs/librarian-promo/.venv/Scripts/python.exe' tools/promo-video/serve.py --port 8785 --directory outputs/librarian-promo
```

Open `http://127.0.0.1:8785/preview.html`. The server binds only to localhost.

## Creative and source grounding

`script.json` holds spoken copy, voice settings, source references, and scene
order. `scenes.py` contains original vector illustrations, layouts, the robot
librarian, and animations. Selected word timings synchronize the missing-paper
reveal and search-method highlights. Each scene transitions with a brief dissolve.

| Beat | Librarian-facing message |
|---|---|
| Universe of papers | A relevant paper can be absent from a plausible search. |
| Search pipeline | Retrieval, ranking, and presentation shape visible evidence. |
| Book reveal | A free online guide written for librarians; no prior IR knowledge or mathematics required. |
| Concept map | Boolean, BM25, embeddings, hybrid search, reranking, and agentic search. |
| Library practice | Teach search, investigate gaps, question vendors, and inspect evidence coverage. |
| Companions | Interactive labs, evaluation kit, vendor questionnaire, and teaching notes. |
| Closing invitation | Read free; begin with the 45-minute *Read This First* route. |

The maintained textbook and companion pages supply the claims. Source anchors
and prerequisite wording are checked before production. The pipeline is a
simplified conceptual illustration; no particular product or study is depicted.
The six methods form a conceptual map, not a claim that every system uses all
six. The promotion promises understanding and practical tools, not guaranteed
search completeness or a graduate-level qualification.

The score is synthesized locally from oscillators and seeded noise, with speech
ducking and a gentle final fade. Mastering targets −16 LUFS and −2.5 dBTP.
Verification fully decodes both streams, requires 2,169 frames in the initial
production, measures final audio within −17 to −15 LUFS and below −1 dBTP,
checks streaming atom order, and compares embedded captions to the supplied SRT.
`review.py` checks all scene boundaries and word-triggered frames for layout
errors, confirms visible animation within every scene, compares representative
decoded frames against their rendered source, and creates an encoded contact
sheet for visual review. Human listening and viewing still matter.

The output player and transcript credit the textbook under CC BY 4.0 and
identify synthetic speech. Use the links in `share-copy.txt` when sharing.
The local export is the deliverable; uploading or publishing is a separate action.
