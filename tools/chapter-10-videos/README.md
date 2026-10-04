# Chapter 10: hybrid retrieval, animated

Three narrated films adapted from **Hybrid retrieval and rank fusion** in
Aaron Tay's *How Search Decides What You See*. The maintained source is
`search-textbook.html#hybrid-and-fusion`.

| Film | Duration | Focus |
|---|---|---|
| Two search scouts, one result list | 2:39 | Complementary evidence, identity, hybrid versus multi-stage, fusion and reranking |
| When ranks become votes | 2:38 | RRF formula, the chapter's A/B/C/D calculation, the constant, discarded score gaps and input cutoffs |
| Blend every time, or choose a route? | 2:42 | Blending, routing, agency, input/output depth, weighted fusion, query variants and local evaluation |

The requested Kurzgesagt-inspired direction uses original flat geometric
artwork, vivid colors, a cosmic library, two search scouts, animated signals,
orbiting records, and calculated diagrams. Music is synthesized locally.
Narration uses Microsoft's synthetic `en-GB-RyanNeural` voice. Windows Segoe UI
fonts are loaded locally and are not distributed.

## Render and check

From the repository root on Windows, reuse the Chapter 2 Python environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-10-videos/render.py
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-10-videos/test-examples.py
```

For an independent environment, create a Python 3.12 venv and install
`tools/chapter-10-videos/requirements.txt`.

Modes are mutually exclusive: `--check-only` checks source, scripts and examples;
`--prepare-only` generates speech, mastered audio, timed captions and storyboards;
`--render-only` encodes prepared films; `--stills-only` refreshes storyboards;
`--verify-only` verifies final MP4s. `--episode 1`, `2`, or `3` selects one film.
`--output` changes the export directory. Source and production hashes reject
stale timelines after the source, script, renderer, or shared media helpers change.

The renderer supports the committed Chapter 2 media engine and its newer
explicit film-class API. It supplies its own Chapter 10 frame, transcript and
MP4 metadata. It does not require edits to the Chapter 2 engine.

Speech synthesis requires internet and sends the public narration to Microsoft's
speech service. Actual word timings control captions and the contribution reveal.
Scene lengths follow recorded narration; speech is not cropped or time-stretched.

## Watch and download

Generated files stay in `outputs/chapter-10-videos/`, ignored by the directory's
scoped `.gitignore`. `preview.html` contains a player for each film and links to
MP4s, captions, transcripts, storyboards, and the complete delivery ZIP.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-10-videos --port 8810
```

Open `http://127.0.0.1:8810/preview.html`. The server supports byte-range requests
for seeking. Each film includes 1080p/30 fps H.264/AAC video, burnt-in and embedded
captions, SRT/VTT exports, eight review frames, a contact sheet, a poster, separate
voice/music stems, a mastered soundtrack, and a verification report.

With the local server running, set `CHAPTER10_NODE_MODULES` to the bundled Node
`node_modules` path, then run `node tools/chapter-10-videos/check-preview.cjs`.
The check uses installed Edge to play and seek all films, compare caption text
and count, request byte ranges, check mobile widths, and save player screenshots.

After export and player checks, run `python tools/chapter-10-videos/package.py`
in the same environment to create `chapter-10-videos.zip`. Packaging checks
production freshness, MP4 hashes and archive CRCs. It includes the finished
films, captions, transcripts, posters, storyboards, reports and a local gallery.

## Accuracy and verification

- A/B/C/D identities and equal-weight RRF values follow Table 10.1. They are
  schematic records without relevance judgements.
- The weighted example is calculated: lexical weight 1 and dense weight 2
  yield C, A, D, B. It does not establish better relevance.
- The constant illustration scales each chart separately and compares first
  versus third contribution ratios. The constant is distinct from input depth
  and output depth.
- Identifier distinctions, raw scores, paraphrase recovery and router choices
  are explicitly schematic; no model was measured. No current product behavior
  or universal best parameter is asserted.
- Hybrid combines candidate-generation evidence from multiple routes.
  Multi-stage concerns sequential operations. A separate fusion stage can
  make a hybrid arrangement multi-stage even without reranking.
- Query variants can supply RRF inputs from the same retrieval method; RRF alone
  does not demonstrate lexical/dense hybrid retrieval. Routing alone does not
  establish agency.
- Example checks cover exact arithmetic, weighted ordering, identity validation,
  input/output cutoffs and all 24 scenes at five animation times.
- Export verification fully decodes every MP4, checks frame count, 1920×1080
  dimensions, 30 fps, codecs, exact ordered embedded caption text, fast-start
  atom order and SHA-256. Encoded audio must be within 1 LU of −16 LUFS and
  below −1 dBTP; each take's narration exceeds the music by at least 10 dB.

Scripts and original artwork follow the repository's CC BY 4.0 licence.
Credit Aaron Tay and the book when sharing the adaptations.
