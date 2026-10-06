# Chapter 12: agentic search, animated

Three narrated films adapted from **Agentic search** in Aaron Tay's *How Search
Decides What You See*. The maintained source is
`search-textbook.html#agentic-search`. Each scene in `episodes.json` records its
supporting chapter anchor.

| Film | Duration | Focus |
|---|---|---|
| Who is steering the search? | 2:57 | Task briefs; fixed, adaptive and agentic control; harnesses; output and agentic RAG |
| The invisible menu | 3:14 | Tool capabilities; traces; compounding omissions and recovery; stopping; cost; MCP |
| Give a failed search a second chance | 3:14 | The chapter's historical zero-result demonstration, its limits, and local library knowledge |

The requested Kurzgesagt-inspired direction uses original flat geometric
artwork, vivid colors, a search spaceship and robot navigator, orbiting paper
records, moving signals, and animated diagrams. Artwork, characters and music
are original. Local Windows Segoe UI fonts are loaded without distributing them.
Narration uses the installed **Microsoft David Desktop** synthetic voice. Its
delivery is more mechanical than a human narrator.

## Generate and verify

From the repository root on Windows, reuse the Chapter 2 Python environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-12-videos/render.py
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-12-videos/test-examples.py
```

For an independent Python 3.12 environment, install `requirements.txt`.
The renderer uses the Chapter 2 media engine and Chapter 4 offline speech adapter
without editing either. It supports the original media engine's global Film
class and its newer explicit film-class argument.

Modes are mutually exclusive: `--check-only` checks the chapter, anchors, scripts
and examples; `--prepare-only` creates speech, mastered audio, word-timed captions
and storyboards; `--render-only` encodes prepared films; `--stills-only` refreshes
storyboards; `--verify-only` verifies exports. `--episode 1`, `2`, or `3` selects
one film; `--output` changes the directory. Source and production hashes reject
stale timelines after any source, script, renderer, or shared helper changes.

All narration is synthesised locally with Windows `System.Speech`; no network
connection or content transfer is required. The installed voice's native 16 kHz
clock supplies real word timings. Scene lengths follow narration, with no
speech cropping or time stretching. Local speech and browser processes may need
sandbox approval on restricted machines. Music is synthesised locally and
ducked beneath narration.

## Watch and download

Exports stay in `outputs/chapter-12-videos/`, excluded by that directory's scoped
`.gitignore`. The gallery links to each film, captions, transcript and storyboard.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-12-videos --port 8812
```

Open `http://127.0.0.1:8812/preview.html`. Each film has a 1920×1080, 30 fps
H.264/AAC MP4, burnt-in and embedded captions, SRT/VTT sidecars, a transcript,
eight review frames, a contact sheet, a poster, separate voice/music stems,
a mastered soundtrack and a verification report.

With the server running, set `CHAPTER12_NODE_MODULES` to the bundled Node
`node_modules` path and run `node tools/chapter-12-videos/check-preview.cjs`.
The check uses installed Edge to play and seek all films, compare captions,
exercise byte-range requests, check mobile widths and save player screenshots.
`CHAPTER12_PREVIEW_URL` overrides the server URL. Finally run
`python tools/chapter-12-videos/package.py` in the rendering environment to make
`chapter-12-videos.zip`. Packaging checks hashes, production freshness and CRCs.

## Grounding and checks

- Agency concerns control, rather than a new scoring function. Result-dependent
  query content can occur within a fixed sequence. A model choosing explicitly
  enumerated branches remains adaptive under the book's convention.
- The four uncited-record cards are a schematic identity-set example. They do
  not represent real papers or measured relevance. Subtracting reference
  identities A/C from related candidates A/B/C/D leaves B/D.
- The open-access citation-advantage trajectory follows Figure 12.2 and is
  explicitly hypothetical. Repeating an aspect can reinforce an omission;
  deliberately investigating another aspect may expand the cumulative pool.
- Repeated retrieval, control and output format are independent. Report polish
  does not establish agency. Agentic RAG is the narrower generated-answer case.
- The database-discovery scenes report the chapter's June 2026 exploratory
  demonstration: selected 2023 queries answered by 2026 models. They are not a
  fresh product test, a success rate, or current holdings advice. Four of the
  six reported autism expansion variants are shown, labelled as such.
- The same-index, holdings CSV and smaller-model comparisons do not isolate a
  single cause. Useful retries can also be fixed or adaptive. Library holdings,
  entitlements and coverage must come from accurate local data.
- No comparative cost or timing measurements, product league table, or current
  product architecture is asserted. The films emphasise general mechanisms
  and retain the chapter's dated evidence limits.
- Source/example checks validate the set subtraction, cumulative recovery,
  every source anchor, and all 24 scenes at five animation times. Full export
  verification decodes every frame, checks dimensions, frame count, codecs,
  exact ordered embedded caption text, fast-start atom order and SHA-256.
  Encoded audio must be within 1 LU of −16 LUFS, with peaks below −1 dBTP;
  each take's narration exceeds music by at least 10 dB.

Scripts and original artwork follow the repository's CC BY 4.0 licence.
Credit Aaron Tay and the book when sharing the adaptations.
