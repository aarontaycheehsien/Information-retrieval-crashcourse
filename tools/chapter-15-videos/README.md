# Chapter 15: library practice and tool evaluation, animated

Three narrated films adapted from **Implications for library practice and tool
evaluation** in Aaron Tay's *How Search Decides What You See*. The maintained
source is `search-textbook.html#library-practice`. Every scene has a source anchor;
the final film maps all nineteen vendor questions to scenes, in order.

| Film | Duration | Focus |
|---|---|---|
| Save the search, not just the question | 3:33 | Conditional reproducibility, exact inputs, four record areas, trajectories, exports and comparison |
| Follow the evidence behind a result | 3:31 | Transparency, interpretability, faithful traces, the chapter's mock paper P and backward inspection |
| Questions to ask before you buy | 3:50 | Starting inputs and all nineteen questions across six procurement groups |

The Kurzgesagt-inspired direction uses original geometric artwork, vivid colors,
a cosmic search observatory, a robot archivist, paper characters, a flight
recorder, moving signals, orbiting particles and explanatory diagrams. Artwork
is drawn and animated with Skia. Narration uses the installed **Microsoft David
Desktop** synthetic voice, which sounds more mechanical than a human narrator.
Music is synthesized locally without recorded samples. Windows Segoe UI fonts
are loaded locally and are not distributed.

## Generate and verify

From the repository root on Windows, reuse the existing Chapter 2 environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-15-videos/test-examples.py
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-15-videos/render.py --prepare-only
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-15-videos/render.py --render-only --jobs 3
```

For a separate Python 3.12 environment, install `requirements.txt`. Windows
System.Speech and Microsoft David Desktop must be installed. This renderer
reuses the Chapter 2 media engine and Chapter 4 local speech adapter without
editing them. It supports the engine's explicit `film_class` argument and its
earlier global Film interface. No content is sent to an external speech service.

Modes are mutually exclusive: `--check-only`, `--prepare-only`, `--render-only`,
`--stills-only`, and `--verify-only`. `--episode 1`, `2`, or `3` selects a film;
`--output` selects the export folder. `--jobs 3` uses separate media processes
for the three films. Only the parent writes the gallery and aggregate report.
Source and production hashes reject stale prepared timelines.

Speech sets scene lengths and supplies actual word timings for captions. It is
neither cropped nor time-stretched. Windows speech access may require sandbox
approval. The soundtrack targets −16 LUFS; music is ducked beneath narration,
with at least a 10 dB voice-over-music margin in every take.

## Watch and download

Exports stay in `outputs/chapter-15-videos/`, ignored by its scoped `.gitignore`.
The gallery links to the films, captions, transcripts, storyboards and complete
ZIP. Every film includes 1920×1080/30 fps H.264/AAC video, burnt-in and embedded
English captions, SRT/VTT sidecars, eight review frames, a contact sheet, poster,
voice/music stems, mastered audio and a verification report.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-15-videos --port 8815
```

Open `http://127.0.0.1:8815/preview.html`. Set `CHAPTER15_NODE_MODULES` to the
bundled Node `node_modules` directory and run
`node tools/chapter-15-videos/check-preview.cjs`. `CHAPTER15_PREVIEW_URL` overrides
the server URL. The browser check plays and seeks each film, checks captions,
byte-range serving, responsive widths and page errors, and saves screenshots.

After verification, run `python tools/chapter-15-videos/package.py` in the same
environment to create `chapter-15-videos.zip`. Packaging checks source and
production freshness, MP4 hashes and archive CRCs. The ZIP includes films,
captions, transcripts, storyboards, posters, reports and the gallery.

## Accuracy and checks

- Figure 15.1's paper P is hypothetical: candidate 18 of 100, reranked to 3,
  displayed inside the first 10. Internal reranker scoring remains undisclosed.
  A generated explanation does not establish the executed retrieval path.
- Figure 15.2 runs backwards for inspection. It does not describe the system's
  execution order. Visible layers have limits: eligibility is not relevance,
  lexical scores are not probabilities, and highlights are not proof of ranking.
- Reproducibility depends on fixed records, analysis, versions and configuration.
  Dense retrieval is not inherently random. LLM rewrites should be saved exactly;
  reuse of saved input differs from regenerating a transformation.
- Fixed, adaptive and agentic control have different recording requirements.
  Action and observation traces are distinguished from narrated reasoning.
  Observed evidence, vendor documentation and unknowns remain separate.
- All nineteen questions appear once across their six original groups. Training
  evidence is question 11 within group 3. Starting-input questions are retained.
  The full printable questionnaire is linked from the gallery.
- Orbiting records, identifiers `GENE-17` / `GENE-71`, configuration panels and
  route diagrams are schematic illustrations. No current product specification,
  measured benchmark result, price, or performance ranking is asserted.

Six checks cover source fixtures, rank boundaries, question coverage, evidence
limits, script structure and every scene at five animation times. Export
verification fully decodes the films and checks frame counts, dimensions, fps,
codecs, exact ordered embedded caption text, fast-start atom order, SHA-256,
encoded audio within 1 LU of −16 LUFS and true peaks below −1 dBTP.

Scripts and original artwork follow the repository's CC BY 4.0 licence.
Credit Aaron Tay and the book when sharing the adaptations.
