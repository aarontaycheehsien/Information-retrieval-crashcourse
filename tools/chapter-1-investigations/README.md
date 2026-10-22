# Chapter 1: The retrieval problem

Three original animated explainers based on Chapter 1 of Aaron Tay's *How Search
Decides What You See*, from the requested `more-readable` branch at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **The paper your AI never saw** — the documented Primo workflow, searchable
   scope, fixed candidate sets, diagnosis, six stages and RAG's evidence limits.
2. **A match is not a verdict** — information needs, the same study assessed
   against two purposes, follow-up searching, search-resistant concepts,
   screening and four perspectives on relevance.
3. **Three clues in a search box** — all three opening puzzles, what their
   observations establish, output versus iteration, agency, LLM roles and the
   chapter's closing investigation.

The creative direction follows the previous preface series: original paper-card
experiments, curiosity-led questions, prediction pauses and evidence-led reveals.
It is an independent adaptation, with no affiliation with Veritasium. It uses
original vector artwork and a standard Microsoft Andrew Multilingual synthetic
voice. No presenter likeness, voice clone, brand assets, existing footage or
third-party product screenshots are used.

## Generate and review

This production is isolated in new directories. Existing videos, scripts and
the maintained textbook are preserved. Nothing is pushed or published.

From the repository root, with Python 3.12:

```bash
python -m pip install -r tools/chapter-1-investigations/requirements.txt
python tools/chapter-1-investigations/render.py --prepare-only
python tools/chapter-1-investigations/render.py --stills-only
python tools/chapter-1-investigations/render.py --render-only --workers 3
```

FFmpeg must be on PATH, or set `CHAPTER_FFMPEG`. The artwork uses system DejaVu
fonts; set `PREFACE_FONT_DIR` to a folder containing `DejaVuSans.ttf`,
`DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf` on other operating systems.
`--episode 1`, `2` or `3` selects a film. `--output` changes the export folder.
`--workers` controls local encoder processes; no GPU or video-generation API is
required. The Chapter 1 media engine, shared voice helper and preface drawing
primitives are reused without changing those productions.

The public narration text is sent to Microsoft's speech service through
edge-tts. The configured proxy certificate is trusted with TLS verification
retained. Takes are cached; failures preserve completed takes. Speech is never
sped up or cut to fit a visual. Reveals use the returned speech timings.

Each film includes a 1920×1080, 30 fps H.264/AAC MP4; burnt-in and embedded
English captions; SRT/VTT; timed transcript; source-linked storyboard; poster;
review frames; contact sheet and verification report. The gallery and ZIP
contain all three films and supporting materials. Outputs are locally saved
and ignored by Git; production sources are committed separately.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-1-investigations --port 8818
python tools/chapter-1-investigations/check-preview.py
python tools/chapter-1-investigations/render.py --package-only
```

Open `http://127.0.0.1:8818/index.html`. The browser check needs Playwright and
Chromium, and tests playback, seeking, scene buttons, caption loading, byte
ranges and desktop/tablet/mobile layouts.

## Source fidelity and evidence limits

The complete Chapter 1 snapshot and provenance are stored beside the script.
Source, script and production hashes reject stale prepared timelines. Every
scene names an anchor within the pinned chapter. No live product tests are
represented as having been performed for these films.

- The Primo pipeline retains its September 2026 documentation date. Its content
  scope is a separate October 2026 documentation check. Scope drawings show no
  measured proportions. Availability in wider library discovery does not prove
  availability to the assistant. No separate Primo fusion stage is asserted.
- Scopus AI's RAG Fusion example is explicitly historical (2024), not a claim
  about every later mode. A documentation check is distinct from a behavioral
  test of every stage.
- The thirty-card experiment fixes membership for one round. Reranking is a
  permutation; a later retrieval round could add evidence. Faint original cards
  remain in the index. A missing citation alone cannot diagnose the loss point.
- The service demonstration study and numbered paper identities are invented,
  labeled illustrations. The study still contributes participant-reaction
  evidence; it does not establish accuracy, workload or consultation performance.
  Search-resistant criteria can be left to screening rather than forced into
  every query. Relevance perspectives have no fixed hierarchy.
- The scite nonsense token is illustrative; the observed behavior is attributed
  to the chapter's screenshot. It challenges strict-AND admission without
  proving a hidden architecture.
- The Google Scholar diagram has exactly 9,400 equal marks, each representing
  1,000 reported matches. One highlighted mark represents the documented
  1,000-record display cap. A reported total is not a fully ranked or scored set.
- Semantic Scholar's 13 versus approximately 35,300 comparison retains its
  August 2026 date. Bar lengths use `log10(count + 1)` with a labeled axis. The
  author's assessment of worse leading results is kept separate from counts.
- Output format and retrieval iteration are independent; agency remains a
  separate property. The film avoids claims about products' current quadrant.
  An LLM's presence alone identifies neither a retrieval method nor a stage.

Checks reconstruct every spoken word from captions, validate cue timing,
render every reveal and transition for layout review, verify the experimental
membership and chart quantities, completely decode all frames and audio,
check resolution/codecs/fps/stereo 48 kHz, measure −16 LUFS ±1 and peaks below
−1 dBTP, verify fast-start metadata and compare embedded subtitle text. ZIP
packaging checks verified MP4 hashes and archive CRCs.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 1](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#intro),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit Aaron Tay and
the book when sharing. This adaptation supplies new narration and illustrations.
