# Preface: why this book exists, animated

Three narrated films adapted from the complete preface of Aaron Tay's *How
Search Decides What You See*, including its reading orientation. The maintained
source is `search-textbook.html#preface`; every scene names its source anchor.

| Film | Duration | Focus |
|---|---|---|
| Open the search box | 2:55 | Admission versus ranking, librarians' questions, search labels, documentation and unknowns |
| The evidence you never see | 2:53 | Retrieval versus writing, fabricated citations, misrepresentation, missing evidence and library responsibility |
| Your route through the book | 3:10 | Three audiences, teaching principles, dated examples, scope and all five reading routes |

The Kurzgesagt-inspired direction uses original geometric artwork, a colorful
cosmic library, paper explorers, an index robot, an animated book, telescopes,
moving signals, orbiting particles and explanatory diagrams. Skia draws and
animates the artwork. The installed **Microsoft David Desktop** synthetic voice
provides narration; it sounds more mechanical than a human narrator. Music is
synthesized locally without recorded samples. Windows Segoe UI fonts are loaded
locally and are not distributed. Characters, music and artwork are original.

## Generate and verify

From the repository root on Windows, reuse the existing Chapter 2 environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/preface-videos/test-examples.py
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/preface-videos/render.py --prepare-only --jobs 3
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/preface-videos/render.py --render-only
```

For a separate Python 3.12 environment, install `requirements.txt`. The renderer
reuses the Chapter 2 media engine and Chapter 4 offline speech adapter without
editing them. It supports both versions of the shared Film interface. Windows
System.Speech and Microsoft David Desktop must be installed. Local speech access
can require approval outside a restricted sandbox. No script is sent to an
external speech service.

Modes are mutually exclusive: `--check-only`, `--prepare-only`, `--render-only`,
`--stills-only`, and `--verify-only`. Select a film with `--episode 1`, `2`, or `3`;
`--output` changes the export folder. `--jobs 3` runs independent media processes
for the three films when sufficient memory is available. Use the default single
process on machines with limited memory. Only the parent writes the gallery
and aggregate report.

Speech sets scene lengths and supplies actual word timings for captions. Takes
are neither cropped nor time-stretched. Source and production hashes reject
stale prepared timelines. The soundtrack targets −16 LUFS, with voice at least
10 dB above accompanying music per take.

## Watch and download

Exports stay in `outputs/preface-videos/`, ignored by its scoped `.gitignore`.
Each film includes a 1920×1080, 30 fps H.264/AAC MP4, burnt-in and embedded
English captions, SRT/VTT sidecars, a transcript, JSON storyboard, poster,
contact sheet, three review frames per scene, audio stems and verification
report. The gallery links to the films and complete ZIP.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/preface-videos --port 8800
```

Open `http://127.0.0.1:8800/preview.html`, or open an MP4 in a video player. The
server binds only to localhost and supports byte ranges for seeking.

Set `PREFACE_NODE_MODULES` to the bundled Node `node_modules` directory, then run
`node tools/preface-videos/check-preview.cjs` for browser QA. `PREFACE_PREVIEW_URL`
overrides the default URL. The check plays and seeks each film, loads captions,
checks byte ranges, tests desktop/mobile widths, and saves screenshots and a
player verification report.

After verification, run `python tools/preface-videos/package.py` in the same
environment to create `preface-videos.zip`. Packaging checks source and production
freshness, verified MP4 hashes and archive CRCs. Films, captions, transcripts,
storyboards, posters, contact sheets, verification reports and a gallery are
included in the ZIP.

## Accuracy and quality checks

- The gate, paper identities, ranking positions and missing paper P are
  schematic illustrations. They assert no scores or measured product behavior.
- The author’s account of changing professional needs is presented as his
  experience. Marketing labels leave mechanisms open; semantic search is not
  equated with dense retrieval.
- Reference existence, faithful writing and adequate retrieval remain separate
  questions. A real reference can be misrepresented, and fluent writing can
  conceal missing evidence.
- All three audiences, three teaching principles and five shorter routes are
  retained. Appendix F stays core for evidence synthesis; Appendix D remains
  a terminology map for procurement. The films are orientations to those
  routes, with the original preface linked for their full chapter selections.
- Named product examples are dated illustrations. The film makes no current
  product recommendation. Answer generation stays outside the book's main scope.

Five checks cover source grounding, labels and reading routes, evidence limits,
actual word-timed reveals, and every scene at five animation times. Media checks
fully decode each film, inspect dimensions, fps and codecs, match embedded
captions against the timeline, confirm fast-start MP4 atom order, measure
loudness and true peaks, and record SHA-256 hashes. Review frames and real
browser playback accompany these checks.

Source scripts and original illustrations follow the repository's CC BY 4.0
licence. Credit Aaron Tay and the book when sharing the adaptations.
