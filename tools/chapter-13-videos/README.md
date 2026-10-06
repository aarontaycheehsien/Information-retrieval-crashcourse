# Chapter 13: diagnosing retrieval failure, animated

Three narrated films adapted from **Diagnosing retrieval failure** in Aaron
Tay's *How Search Decides What You See*. The maintained source is
`search-textbook.html#diagnosing-failure`.

| Film | Duration | Focus |
|---|---|---|
| Where did the paper go? | 2:59 | Coverage, filters, candidate and display boundaries, indexed units, vocabulary mismatch |
| Missing words, or missing meaning? | 3:15 | Index vocabulary, BERT token pieces, identifier identity, representations, OOD and local evaluation |
| All the words. The wrong relationship. | 3:20 | Direction, negation, composition, interaction, diagnostic lenses and remedy tests |

The requested Kurzgesagt-inspired direction uses original geometric vector
artwork, vivid colors, a cosmic library, a search robot, a detective's lens,
orbiting records, animated signals and explanatory diagrams. Narration is the
local Microsoft David Desktop synthetic voice. Music is synthesized locally
without recorded samples. Windows Segoe UI fonts are loaded locally and are
not distributed. No raster generation is needed for this code-native artwork.

## Render and check

From the repository root on Windows, reuse the existing Chapter 2 environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-13-videos/test-examples.py
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-13-videos/render.py
```

For a separate environment, create a Python 3.12 venv and install
`tools/chapter-13-videos/requirements.txt`. Microsoft David Desktop and Windows
System.Speech must be installed. The shared offline speech adapter is in
`tools/chapter-4-videos/`. Speech generation requires access to the local Windows
speech runtime; it sends no narration to an external service.

Modes are mutually exclusive: `--check-only` validates source and examples;
`--prepare-only` creates audio, timed captions and storyboards; `--render-only`
encodes prepared films; `--stills-only` refreshes storyboards; `--verify-only`
checks exports. `--episode 1`, `2`, or `3` selects a film; `--output` changes
the export directory. Source and production hashes reject stale timelines.

The renderer uses the Chapter 2 engine, supplies its own film class, transcript
and export metadata, and does not edit shared helpers. Scene durations follow
the recorded speech. Captions use actual word timings. Speech is not cropped
or time-stretched.

## Watch and download

Exports stay in `outputs/chapter-13-videos/`, ignored by that directory's scoped
`.gitignore`. `preview.html` contains three players and links to the MP4s,
captions, transcripts and storyboards.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-13-videos --port 8813
```

Open `http://127.0.0.1:8813/preview.html`. Each film includes 1920×1080/30 fps
H.264/AAC video, burnt-in and embedded captions, SRT/VTT exports, eight review
frames, a contact sheet, a poster, separate voice/music stems, a mastered
soundtrack and a verification report.

With the server running, set `CHAPTER13_NODE_MODULES` to the bundled Node
`node_modules` directory and run `node tools/chapter-13-videos/check-preview.cjs`.
It checks playback, seeking, caption count and first cue, byte-range serving,
responsive widths and page errors, and saves player screenshots.

After verification, run `python tools/chapter-13-videos/package.py` in the same
environment to create `chapter-13-videos.zip`. Packaging verifies freshness,
MP4 hashes and archive CRCs. The ZIP includes films, captions, transcripts,
posters, storyboards, reports and a local gallery.

## Accuracy and verification

- Paper P follows Figure 13.1's four alternative hypothetical explanations.
  Coverage, eligibility, candidates and display are separate boundaries.
  Missing documentation remains unknown and does not establish exclusion.
- Heart attack / myocardial infarction and BERT's `ri`, `##zz`, `##lord` example
  follow the chapter. Token pieces are quoted source examples, not newly
  measured tokeniser outputs.
- The contrasting identifier `DELULU-428`, analysis paths, split passages and
  performance bars are schematic teaching illustrations. No model is measured.
  The identity example assumes a keyword field with consistent analysis.
- Vocabulary mismatch, OOV, weak representation, OOD and composition are
  distinct questions that may overlap. One poor result cannot prove OOD.
- BM25 does not itself introduce synonyms. Lexical matching depends on fields
  and analysis. Dense retrieval and reranking do not guarantee correct logic.
  A later reranker cannot recover an absent first-stage candidate.
- The three first-stage approaches are reference patterns, not an exhaustive
  taxonomy. Remedies are hypotheses to test against a stable requirement.
- Example checks cover boundary attribution and unknowns, identifier identity,
  opposing relation term counts, token pieces and all 24 scenes at five times.
- Export verification fully decodes every MP4, checks frame count, dimensions,
  fps, codecs, exact ordered embedded caption text, fast-start atom order and
  SHA-256. Encoded audio must be within 1 LU of −16 LUFS and below −1 dBTP;
  each take's narration exceeds the music by at least 10 dB.

Scripts and original artwork follow the repository's CC BY 4.0 licence.
Credit Aaron Tay and the book when sharing the adaptations.
