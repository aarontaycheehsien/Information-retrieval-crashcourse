# Chapter 1: the retrieval problem, animated

Three narrated films adapted from Aaron Tay's *How Search Decides What You See*,
Chapter 1 (`search-textbook.html#intro`). The Kurzgesagt-inspired direction uses
original flat-vector artwork, a colorful search cosmos, a little index robot,
paper astronauts, moving signals, animated candidate sets, and a quiet musical
score. Everything is drawn and animated with Skia.

| Film | Duration | Focus |
| --- | --- | --- |
| Why these five papers? | 3:27 | Retrieval versus generation, documented Primo pipeline, candidate bottleneck, diagnosis, six stages and two axes |
| A match is not relevance | 3:27 | Detailed search construction, the need-to-judgement chain, one study serving two purposes, refinement and four relevance perspectives |
| Three clues hiding in a search box | 2:14 | The three opening puzzles, evidence limits, and a diagnostic exercise |

The narrator is Microsoft's `en-US-AndrewMultilingualNeural`, at −5% rate and
natural pitch. Films 1 and 3 reuse 37 word-timed narration takes from the existing
Chapter 1 adaptation. Film 2 uses 19 new takes for the revised relevance section.
The earlier single-film adaptation is a separate production.
Music is synthesized locally without recorded samples. Segoe UI fonts are
loaded locally from Windows and are not distributed.

## Generate

From the repository root, reuse the existing Chapter 2 environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-1-videos/test-examples.py
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-1-videos/render.py --prepare-only
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-1-videos/render.py --render-only --jobs 3
```

For a fresh Python 3.12 environment, install `requirements.txt`. The renderer
reuses the Chapter 2 media engine and the existing narration helper without
editing them, supporting both versions of the shared Film interface.

Modes are mutually exclusive: `--check-only`, `--prepare-only`, `--stills-only`,
`--render-only`, and `--verify-only`. `--episode 1`, `2`, or `3` selects a film;
`--output` selects the export folder. `--jobs 3` runs independent film encoders.
Only the parent writes the gallery and aggregate verification report.

`episodes.json` contains every narration line, source anchor, scene title,
claim, voice setting, and film grouping. `scenes.py` contains editable original
artwork. The voice is the master clock: takes are never cut or time-stretched,
and key reveals use actual word timings. Source and production hashes reject
stale prepared timelines and outdated exports during packaging.

Existing voice caches are copied into the new output directory when present.
Uncached or edited narration uses edge-tts and sends the public spoken script
to Microsoft's online speech service. The initial production reused 47 cached
takes. The 6 October 2026 relevance revision adds 19 newly synthesized public
narration takes; subsequent builds reuse their cache.

Film 2 follows the substantially revised “What does ‘relevant’ actually mean?”
section. The earlier broad-keyword/opinion-piece example is replaced with a
skilled synonym-and-date strategy and one hypothetical demonstration study.
The same study contributes differently to an introductory workshop and an
adoption decision. Seven scenes include the five-box need-to-judgement chain,
feedback, search refinement and the limits of a computed suitability estimate.
Films 1 and 3 retain their narration and scene definitions. All exports are
rebuilt and verified together to keep the complete bundle's source and
production hashes current. The previous relevance film and complete ZIP are
preserved locally in `outputs/chapter-1-videos/previous-relevance/`.

## Watch and download

Exports stay under `outputs/chapter-1-videos/`, ignored by its scoped `.gitignore`.
The gallery links to the films and complete ZIP. Each film includes:

- 1920×1080, 30 fps H.264/AAC MP4 with burnt-in and embedded English captions.
- SRT/VTT caption sidecars, transcript and JSON storyboard.
- Three review frames per scene, a contact sheet and poster.
- Narration, music and mastered soundtrack stems, timeline and verification report.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-1-videos --port 8801
```

Open `http://127.0.0.1:8801/preview.html`. The server binds only to localhost
and supports byte ranges for seeking. Publication is a separate action.

Set `CHAPTER1_NODE_MODULES` to the bundled Node `node_modules` directory and
run `node tools/chapter-1-videos/check-preview.cjs` for browser QA.
`CHAPTER1_PREVIEW_URL` overrides the URL. The check plays and seeks every film,
loads exact captions, checks byte-range serving, tests desktop/mobile widths,
and writes screenshots and `player-verification.json`.

After verification, run `python tools/chapter-1-videos/package.py` in the same
environment. This creates `chapter-1-videos.zip`, validates production and
source freshness and media hashes, and checks archive CRCs.

## Source and evidence limits

- Primo's Boolean variations joined by OR, up-to-30 candidates, embedding
  reranking to five sources, and abstract-based overview retain the chapter's
  September 2026 documentation date. The scene does not assert a new product test.
- The fixed candidate-pool illustration does not delete records from the index.
  Reranking permutes the thirty displayed candidates. Another retrieval round
  can add evidence that this round missed.
- Supplied evidence constrains source-supported coverage. It does not guarantee
  that every generated claim uses that evidence or that every supplied paper is cited.
- Output format and retrieval iteration are separate axes. Agency is a third
  question; repeated searching alone does not identify who chooses actions.
- Queries, filters and task briefs can communicate substantial detail about a
  need. The five-box chain shows what the system works with directly and how
  detailed requests and feedback can inform suitability estimates.
- The hypothetical strategy retains the three terminology alternatives and
  publication limit of 2024 onwards. It seeks empirical library research-support
  studies; it is not a demonstrated database query or a newly observed paper.
- The same demonstration study meets the conditions and is topically suitable.
  Positive participant reactions help an introductory workshop, but offer limited
  evidence about accuracy, workload or actual consultations for an adoption
  decision. The paper does not become wholly irrelevant; its match is unchanged.
- Refining a search for accuracy evaluations or operational evidence helps
  express the need. The resulting studies still require assessment. A model can
  estimate topical or task-specific suitability; a high score cannot change
  what a study measured into evidence of something it did not measure.
- The scite puzzle challenges a strict-AND assumption without diagnosing its
  implementation. `xqzblorp` is an invented illustrative word, not a rerun query.
- Google Scholar's approximately 9.4-million count and 1,000-record viewing
  window remain separate quantities. The planet/window illustration explicitly
  is not to scale and makes no claim about the unseen scoring process.
- Semantic Scholar's 13 and approximately 35,300 counts retain the August 2026
  observation date. Bars use labelled `log10(count + 1)` lengths. The ratio is
  stated separately as approximately 2,715-fold. The architecture remains open.

Six checks cover source-grounded examples, uncertainty, scene-aware word
timing, and every scene at five animation times. Each completed film is fully
decoded with FFmpeg's strict error mode, then checked for frame count,
dimensions, fps, codecs, exact embedded caption text, fast-start metadata,
SHA-256, encoded audio within 1 LU of −16 LUFS and true peaks below −1 dBTP.
Every narration take must exceed its accompanying music by at least 10 dB RMS.
Review stills and real playback accompany these automatic checks.

Scripts and original artwork follow the repository's CC BY 4.0 licence.
Credit Aaron Tay and the book when sharing the adaptations.
