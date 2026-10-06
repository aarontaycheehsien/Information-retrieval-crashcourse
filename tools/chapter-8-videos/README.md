# Chapter 8: three animated explainers

Three narrated films adapted from **Representations and indexed units** in
Aaron Tay's *How Search Decides What You See*. Maintained source:
`search-textbook.html#representations-and-units`.

| Film | Duration | Focus |
|---|---|---|
| Vectors without magic | 2:55 | Fixed vocabulary, binary presence, retrieval rules, TF, TF–IDF and BM25 |
| Sparse vectors can learn | 2:56 | Density, provenance, latent coordinates, bibliographic counterexample and SPLADE |
| What does it mean to search a paper? | 2:47 | Indexed units, chunking, pooled vectors, result grouping and later context |

The requested visual direction is expressed through original colourful flat
vector artwork, geometric characters, animated signals, orbiting terms and
diagrams. Speech determines every scene's duration. The soundtrack is original
procedural music; the narrator is Microsoft's synthetic `en-GB-RyanNeural`.
Local Windows Segoe UI fonts are used but not bundled.

## Generate

Run from the repository root using the existing Chapter 2 environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-8-videos/render.py
```

Or create an independent Python 3.12 environment:

```powershell
uv venv outputs/chapter-8-videos/.venv --python 3.12
uv pip install --python outputs/chapter-8-videos/.venv/Scripts/python.exe -r tools/chapter-8-videos/requirements.txt
& './outputs/chapter-8-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-8-videos/render.py
```

Use `--episode 1`, `2`, or `3` to select a film. Default is all three. Mutually
exclusive modes: `--prepare-only` produces speech, mastered audio, captions and
storyboards; `--stills-only` refreshes review frames; `--render-only` encodes
prepared animation; `--verify-only` checks final MP4s. `--output` changes the
export folder. Chapter and production hashes reject stale prepared timelines.

The shared Chapter 2 media engine supplies H.264/AAC encoding, music, mastering
and verification; `tools/pick-a-card/narrate.py` supplies speech caching, actual
word timings and captions. Compatibility covers both the committed shared
engine and its explicit `film_class` API. The wrapper supplies Chapter 8 credits
independently. Synthesis sends the public narration script to Microsoft's speech
service and requires internet. Narration is never cropped or time-stretched.

## Watch and download

Exports are in `outputs/chapter-8-videos/`. The renderer creates a local
`.gitignore` in its export folder to exclude generated media without changing
the repository's shared ignore file.

`preview.html` plays the films and links captions, transcripts and storyboards.
`chapter-8-videos.zip` contains all three MP4s and their viewing companions.
Each film has eight review stills, a contact sheet, poster, SRT/VTT captions,
voice and music stems, mastered soundtrack, timeline and verification report.
Captions appear in the picture, are embedded in each MP4 and are also available
as an optional web caption track.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-8-videos --port 8808
```

Open `http://127.0.0.1:8808/preview.html`. The server supports byte ranges for
scrubbing. Unzip the download to retain all relative gallery links.

## Accuracy and verification

- `validate_examples()` independently checks the chapter's fixed seven-term
  vocabulary, binary vectors, heart-treatment overlap scores, AND/OR eligibility,
  document frequencies, diminishing returns and four-chunk/two-paper grouping.
- TF–IDF bars illustrate `IDF = log(N/DF)`. Exact weighting formulas vary. The
  BM25 curve illustrates `k1=1.2` at average document length with IDF omitted.
  This is a comparison of representations, not a historical derivation of BM25.
- Binary coordinates record evidence. They do not specify Boolean operators.
  BM25's vector view does not imply dense storage or nearest-neighbour search.
- Dense coordinates and learnt expansion weights are explicitly illustrative.
  Whole-word expansion labels are schematic; SPLADE activates its own output
  vocabulary, typically WordPiece subword units. No model output was measured.
- Chunk boundaries and overlap are illustrations, not measured performance.
  One vector per unit is scoped to conventional single-vector bi-encoders.
- Grouping by source identity is separate from combining scores or evidence.
  Indexed text, retrieved units and later generator context are distinguished.
- Each MP4 must fully decode at 1920×1080, 30 fps, with the expected frame count.
  Embedded subtitle text must match every ordered cue; MP4 atoms must allow
  fast-start playback. Final audio must be within 1 LU of −16 LUFS, below
  −1 dBTP, and narration must exceed the music by at least 10 dB per take.

Source scripts and original artwork follow the repository's CC BY 4.0 licence.
Credit Aaron Tay and the book when sharing this adaptation.
