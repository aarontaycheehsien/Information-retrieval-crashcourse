# Chapter 7: dense retrieval at collection scale

Three narrated films adapted from Aaron Tay's *How Search Decides What You See*,
Chapter 7, `search-textbook.html#dense-at-scale`.

| Film | Duration | Focus |
|---|---|---|
| When the same vectors disagree | 2:37 | Cosine, dot product, normalisation, dimensions, score interpretation |
| Searching a hundred million vectors | 2:45 | Stored vectors, postings, exhaustive search, ANN, HNSW, top-k |
| Where does meaning enter search? | 2:59 | Semantic goals, vocabulary bridging, compression, thresholds, stage budgets |

The requested visual direction is expressed through original colorful geometric
science animation: a dark cosmic palette, paper astronauts, a small index robot,
moving signals, orbiting particles, animated rankings and numerical diagrams.
The broad approach is inspired by Kurzgesagt. Characters, artwork and music are
original. Narration uses the installed offline `Microsoft David Desktop` voice.

## Generate

From the repository root on Windows, reuse the Chapter 2 Python environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-7-videos/render.py
```

Or create a Python 3.12 environment and install the local requirements:

```powershell
uv venv outputs/chapter-7-videos/.venv --python 3.12
uv pip install --python outputs/chapter-7-videos/.venv/Scripts/python.exe -r tools/chapter-7-videos/requirements.txt
& './outputs/chapter-7-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-7-videos/render.py
```

`--check` validates the source and numerical examples without speech or video.
`--prepare-only` caches speech and prepares audio, captions and review frames.
`--render-only` renders prepared assets; `--stills-only` refreshes storyboards;
`--verify-only` checks the exported MP4s. Modes are mutually exclusive.
`--episode 1`, `2`, or `3` selects one film; the default is all three.
`--output` chooses another output directory. Input hashes reject stale prepared
assets after chapter, narration, renderer, artwork or shared-helper changes.

The media engine is `tools/chapter-2-videos/render.py`. The wrapper supports its
committed API and its newer `film_class` argument without modifying shared code.
The offline adapter and PowerShell speech exporter are reused from Chapter 4.
They synthesize at David's native 16 kHz, record actual `SpeakProgress` word times,
and validate those events against the script and the WAV clock. No narration is
sent to an external service. The local speech engine may require running outside
a restricted sandbox. After speech is cached, preparation and rendering work
inside the sandbox. Speech is never cropped or time-stretched.

Original music is synthesized locally, ducked under the narrator and mastered
to approximately −16 LUFS. Windows Segoe UI fonts are loaded locally and are not
bundled. Scripts, original artwork and adaptations follow the repository's
CC BY 4.0 licence; credit Aaron Tay and the book when sharing.

## Watch and share

The generated gallery is `outputs/chapter-7-videos/preview.html`. Each film has a
1920×1080, 30 fps H.264/AAC MP4 with burned-in and embedded English captions,
SRT/VTT sidecars, transcript, poster, eight scene stills, contact sheet, timeline,
separate audio stems and verification report. The optional web caption track
can be enabled in the player. Generated media and caches are Git-ignored by the
output directory's own `.gitignore`, leaving the root ignore file untouched.

When all three exports have current verification reports and matching MP4
SHA-256 hashes, the renderer creates `chapter-7-videos.zip` with the films,
gallery, captions, transcripts, posters, storyboards, timelines and reports.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-7-videos --port 8807
```

Open `http://127.0.0.1:8807/preview.html`. The server supports byte ranges for
seeking. The gallery also opens directly from disk.

## Grounding and verification

- The similarity illustration uses declared toy vectors: Q=(1,0), A=(0.9,0.3),
  B=(1,1). Calculated cosine scores are approximately 0.949 and 0.707; dot
  products are 0.9 and 1. Unit normalisation makes both comparisons agree.
  `validate_examples()` checks the reversal, scale invariance, normalisation
  equivalence and the cosine landmarks 1, 0 and −1.
- The six-point adaptation preserves the chapter's distances and result sets.
  It uses Q=(0,0), A=(1,0), B=(0,2), C=(2,2), D=(1,3), E=(3,4), F=(5,1).
  D, E and F have different angular positions from the book's figure but retain
  their distances from Q. Euclidean distances give exact top three A/B/C.
  The stipulated approximate run examines A/B/D/F and returns A/B/D, missing C.
  Both ask for k=3. This illustrates a possible miss and does not simulate HNSW
  or imply that ANN always misses a neighbour.
- The multi-layer graph is schematic. Anonymous higher-dimensional arrows are
  teaching illustrations, not actual model coordinates or a measured projection.
- Vocabulary bridging is conditional on suitable training. The vector grids,
  score distributions, compression diagram and CMP-104 identifier are invented
  illustrations. Similarity is not a calibrated relevance probability.
- The 30 → 5 → 3 pipeline has explicitly invented budgets, independent of the
  chapter's named products. Admission, scoring, execution and output size remain
  separate decisions. A reranker cannot rescue an upstream excluded passage.
- Semantic Scholar's lexical → LightGBM pipeline is the chapter's documented
  2025 snapshot; OpenAlex Alice's embedding → cosine route is its 2026 snapshot.
  Neither animation asserts a current implementation or diagnoses a particular
  query. Product names, natural input and visible counts do not establish the
  first retrieval stage.
- MP4 verification fully decodes every frame, checks dimensions, frame rate,
  codecs and expected frame count, compares every embedded subtitle with its
  timed cue, checks fast-start atom order and measures encoded loudness and peak.
  Integrated loudness must be within 1 LU of −16 LUFS; true peak must be at or
  below −1 dBTP. Each narration take must exceed the music by at least 10 dB.
  Review storyboards and frames extracted from the final encoded videos.
