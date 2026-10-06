# The paper your AI never saw

An original 7:09 narrated adaptation of Chapter 1 of Aaron Tay's *How Search
Decides What You See*. The Veritasium-inspired direction uses a question,
prediction, paper-card thought experiment, reveal, three counterintuitive
search observations, and a closing investigation. All artwork and animation
are original. The narrator is Microsoft Andrew Multilingual.

The film uses a warm tabletop, numbered paper cards, slow camera pushes,
animated evidence selection, a study compared across two purposes, and carefully
labelled quantitative graphics. It covers retrieval versus generation, Primo's
documented pipeline, missing-source diagnosis, information need versus query,
four relevance perspectives, the three opening puzzles, the six-stage map,
and output versus retrieval iteration. Agency remains a separate question.

## Watch

The completed exports are in `outputs/chapter-1-investigation/`:

- `chapter-1-the-paper-your-ai-never-saw.mp4`: 1920×1080, 30 fps, H.264/AAC,
  stereo, 428.63 seconds, with burnt-in and embedded English captions.
- Matching `.srt` and `.vtt`, plus a timed transcript.
- `preview.html`, thirteen chapter links and `chapters.vtt`.
- Poster, 39 review stills, contact sheet and media verification report.
- Prepared timeline, word-timed voice cache and audio intermediates.

Use the existing local server for seeking:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-1-investigation --port 8816
```

Open `http://127.0.0.1:8816/preview.html`. It binds only to localhost.

## Reproduce

The production reuses the Chapter 1 single-film media engine and the
`pick-a-card` speech/timing helper without editing either. From the repository
root, use the existing Chapter 2 environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-1-investigation/render.py --workers 2
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-1-investigation/check.py
```

For a fresh environment, install `requirements.txt` into Python 3.12.
`--prepare-only`, `--stills-only`, `--render-only`, and `--verify-only` are
mutually exclusive. `--output` selects a different export directory;
`--workers` accepts one through eight. Voice preparation is cached separately
from picture rendering. Unchanged takes can be copied from the earlier
Chapter 1 voice cache. This revision reuses thirty-three unchanged takes and
records eight revised takes with the same narrator.

The voice is `en-US-AndrewMultilingualNeural` at −5% rate and natural pitch.
Uncached speech uses edge-tts and sends the public narration to Microsoft's
online speech service. Online failures stop preparation and preserve finished
takes. Rerun to resume. No speech is shortened or time-stretched. Animation
reveals follow the actual spoken-word timings. The soundtrack is narration.

Windows Segoe UI and Consolas fonts are loaded locally and are not distributed.
`CHAPTER_FONT_DIR` overrides their folder. `CHAPTER_FFMPEG` overrides the
imageio-ffmpeg executable. No GPU, LaTeX, Manim or video-generation API is needed.

## Checks and evidence limits

The renderer verifies source anchors and the chapter's distinctive dates and
quantities. Source, script and production hashes reject stale prepared
timelines. Before accepting a final MP4, it completely decodes the video and
audio, verifies all 12,859 frames, resolution, fps, codecs, sample rate,
stereo channels, integrated loudness of −16 LUFS ±1, true peak below −1 dBTP,
and fast-start metadata. Embedded caption text must match the SRT exactly.

`check.py` checks caption timing and wording and draws every scene throughout
its real speech timeline, including its transitions. The browser check plays,
seeks, loads caption cues, checks chapter links and byte-range requests, and
checks mobile/tablet/desktop layouts:

```powershell
$env:INVESTIGATION_NODE_MODULES = 'C:/Users/aaron/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules'
node tools/chapter-1-investigation/check-preview.cjs
```

`INVESTIGATION_PREVIEW_URL` overrides the localhost URL.

The paper-card experiment is illustrative, with a fixed thirty-candidate
pool for one round. Reranking permutes those same candidates. Faint copies
remain in the index; retrieving a record does not delete it. Further retrieval
can add evidence. A missing citation alone cannot locate the failure, and
directly finding a paper cannot reconstruct its path in an earlier run.

The Primo sequence retains the chapter's September 2026 documentation date.
The product observations are taken from the chapter, not rerun for this video.
Semantic Scholar's 13 versus approximately 35,300 observation retains its
August 2026 date. Its bars use `log10(count + 1)`; the approximately 2,715-fold
ratio is stated separately. The Google Scholar graphic contains exactly 9,400
equal marks, each representing 1,000 reported matches; one mark represents
the documented 1,000-record display cap. Reported counts are not claims that
every match was individually ranked or scored.

The relevance example follows the revised `#what-does-relevant-actually-mean`
section. A skilled strategy uses alternative terminology and a 2024-onwards
date limit. Queries, filters, purpose briefs and reader feedback can communicate
substantial detail; the system uses those representations to estimate
suitability, and the reader assesses usefulness. The hypothetical demonstration
study meets the search conditions and is topically suitable. Its positive
participant reactions make it a useful introductory-workshop example, but
provide limited evidence about accuracy, staff workload or actual research
consultations for a service-adoption decision. The paper still contributes;
its match has not changed. Refining the search for operational evidence and
judging what studies measured work together. This is not a cited real study.
The nonsense token `xqzblorp` is also illustrative. Observations challenge
assumptions about admission and ranking without establishing hidden mechanisms.

The source is `search-textbook.html#intro`. `script.json` records a source
anchor for every scene. Credit Aaron Tay and the book under CC BY 4.0 when
sharing this adaptation. Publication is a separate action.

The replaced export and its original transcript are preserved locally in
`outputs/chapter-1-investigation/previous-relevance-edition/`.
