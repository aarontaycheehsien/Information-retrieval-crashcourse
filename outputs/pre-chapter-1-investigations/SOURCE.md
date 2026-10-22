# Before the search begins

Three original, narrated science explainers adapting **all of the preface and
reading orientation before Chapter 1** of Aaron Tay's *How Search Decides What
You See*. The source is the requested `more-readable` branch, pinned to commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`. The preface snapshot and provenance
are included beside the script. Chapter 1 itself is outside this adaptation.

1. **Two decisions hiding in every search** — admission and ranking, the
   author's motivation, terminology, documentation and unknowns.
2. **The evidence you never see** — reference existence, faithful writing,
   adequate retrieval, and why libraries need to investigate evidence selection.
3. **Your route through the machine** — three audiences, three teaching
   principles, dated examples, scope, all five reading routes and exercises.

The Veritasium-inspired direction uses curiosity-driven questions, prediction
pauses, tangible paper-card experiments, animated comparisons and evidence-led
reveals. Artwork and adaptation are original; no existing video footage,
branding or cloned voice is used. Independently produced, with no affiliation
with Veritasium. The standard synthetic narrator is Microsoft Andrew Multilingual.
Speech uses edge-tts and sends only the public adaptation script to Microsoft's
speech service. The renderer trusts a managed proxy CA when configured, with
TLS verification retained. No paid video-generation API is needed.

## Generate

From the repository root, on Linux, macOS or Windows with Python 3.12:

```bash
python -m pip install -r tools/pre-chapter-1-investigations/requirements.txt
python tools/pre-chapter-1-investigations/render.py --prepare-only
python tools/pre-chapter-1-investigations/render.py --stills-only
python tools/pre-chapter-1-investigations/render.py --render-only --workers 3
```

FFmpeg must be on PATH, or set `CHAPTER_FFMPEG`. Fonts default to system
DejaVu Sans/Serif on Linux. `PREFACE_FONT_DIR` can select a folder containing
`DejaVuSans.ttf`, `DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf` on other systems.
The renderer reuses the repository's Chapter 1 media engine and shared
speech/cache helper without changing them. `--output` changes the export folder;
`--episode 1`, `2` or `3` selects one film. `--workers` controls local encoder
processes. Prepared timelines reject stale source, script or production hashes.
Voice takes are cached and never sped up or shortened to fit the picture.

Exports: 1920×1080, 30 fps H.264/AAC MP4; burnt-in and embedded English captions;
SRT/VTT; timed transcript; source-linked storyboard; poster; review frames;
contact sheet; verification report; a responsive video gallery; complete ZIP.

For browser playback, serve the export directory using the repository's
byte-range-capable server:

```bash
python tools/promo-video/serve.py --directory outputs/pre-chapter-1-investigations --port 8817
```

Open `http://127.0.0.1:8817/index.html`. MP4s can also be opened directly.
With Playwright and Chromium installed, run
`python tools/pre-chapter-1-investigations/check-preview.py` for playback, scene buttons,
caption loading, byte-range requests and desktop/tablet/mobile layout checks.
Run `render.py --package-only` afterward to include the browser report and
gallery screenshots in the ZIP.

## Verification and interpretation

Checks validate source anchors, script/word/caption agreement, nonoverlapping
caption timings, every animation reveal and transition, complete video/audio
decoding, exact frame count, resolution, codecs, 30 fps, stereo 48 kHz audio,
−16 LUFS ±1, true peaks below −1 dBTP, fast-start metadata and embedded subtitle
text. ZIP packaging checks the verified MP4 hashes and archive CRCs.

All paper sets, gates, ranks, envelopes and the uncertain-result example are
explicitly invented teaching illustrations. No counts, rankings or omissions
are presented as observations of a real product. A missing citation is a reason
to investigate, not proof of a particular pipeline failure. The author's
professional history is attributed to his account. Semantic search is not
equated with dense retrieval. No neural method is said to have displaced all
lexical retrieval. Existence, faithfulness and adequacy remain distinct.

All five routes follow the requested branch, including its 45-minute orientation
route. Appendix F remains core for evidence synthesis; procurement keeps
Appendix D and the Chapter 10/Appendix E guidance. The films orient readers to
the routes; the original preface provides the linked full explanations.

Adapted from [Aaron Tay, *How Search Decides What You See*, Preface](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#preface),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author and
book when sharing. This production is an adaptation with new narration and
original explanatory illustrations.
