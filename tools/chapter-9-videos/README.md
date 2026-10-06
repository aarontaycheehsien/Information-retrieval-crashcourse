# Chapter 9: three animated explainers

Three narrated films adapted from **Reranking and multi-stage retrieval** in
Aaron Tay's *How Search Decides What You See*. The maintained source is
`search-textbook.html#reranking-and-hybrid`.

| Film | Focus |
|---|---|
| The shortlist is the ceiling | Multi-stage search, candidate recall versus visible ranking, text boundaries, budgets |
| Three ways to compare a question and a paper | Pooled bi-encoders, joint cross-encoders, cost, late interaction and MaxSim |
| How to build a useful result list | Pointwise/pairwise/listwise LLM reranking, diversity, academic pipelines, neural IR |

The requested Kurzgesagt-inspired direction uses colorful original flat-vector
art, space-like backdrops, geometric characters, moving signals, animated lists
and visual metaphors. The renderer draws the artwork directly with Skia.
The music is synthesized from the repository's original musical loop. Narration
uses Microsoft's synthetic `en-GB-RyanNeural` voice. Segoe UI fonts are loaded
from Windows and are not distributed with the exports.

## Render

Use the existing Chapter 2 environment from the repository root:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-9-videos/render.py --check-only
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-9-videos/render.py
```

For a separate environment, install `requirements.txt` with Python 3.12.
The Chapter 2 renderer, visual primitives and `tools/pick-a-card/narrate.py`
supply cached word-timed speech, music, mastering, H.264/AAC encoding, captions
and verification. Speech synthesis sends the public narration script to
Microsoft's service and requires internet access.

The local picture encoder sends frames in 64 KiB pipe writes and limits itself
to two encoder threads. This avoids large Windows pipe writes failing when
several chapter productions compete for memory. The shared Chapter 2 engine
continues to provide audio, muxing and verification.

`--episode 1`, `2`, or `3` selects a film; the default renders all three.
Mutually exclusive modes are `--prepare-only`, `--stills-only`, `--render-only`
and `--verify-only`. `--check-only` validates the source, script and calculations
without calling the speech service. `--output` changes the export directory.
Source and production hashes guard against reuse of stale prepared assets.

## Watch and download

The local output directory is `outputs/chapter-9-videos/`; its small tracked
`.gitignore` excludes generated media and caches without changing existing
repository ignore rules. Exports include three 1920×1080, 30 fps MP4s, burned-in
and embedded English captions, SRT/VTT sidecars, transcripts, posters, scene
stills, contact sheets, word-timed timelines and separate audio stems.

`preview.html` is the local player. After all three exports pass verification,
`chapter-9-videos.zip` bundles the films, captions, transcripts, posters,
storyboards, player, verification reports and these production notes.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-9-videos --port 8809
```

Open `http://127.0.0.1:8809/preview.html`. The existing server supports byte
ranges for seeking. MP4s are also directly playable outside the browser.

## Accuracy and verification

- Reranking permutes a fixed candidate pool. An explicit new retrieval can widen
  the pool; reordering alone cannot. Fusion of several retrieved lists is the
  next chapter's subject.
- The six-candidate precision/recall example is invented: A, D, E and excluded G
  are relevant. Pool recall stays 3/4; precision at three improves from 1/3 to
  3/3. Recall at three improves from 1/4 to 3/4. These are not model results.
- The job-expectations labels follow the chapter's stated interpretation.
  A different search need could make the interview-performance passage useful.
- Cost bars are schematic and do not report latency. Batching may group pair
  evaluations; it does not eliminate the individual query–candidate comparisons.
- MaxSim uses the chapter's invented 2×4 similarities: row maxima 0.90 and 0.80,
  total 1.70. Whole-word labels simplify real model tokenisation. Many query
  tokens may select the same document token. Scoring alignments show contributors,
  not the reasons a model learned their similarities.
- The pairwise preference cycle is invented. The listwise output is illustrative.
  Pointwise/pairwise/listwise describe inference formulations here; classical
  learning-to-rank research also uses the labels for training objectives.
- A/B/C versus A/D/E follows the chapter's schematic aspect-coverage example,
  without claiming to calculate a diversification algorithm. B and C remain
  distinct studies; F is weakly related. Diversity does not guarantee balanced
  evidence or replace high-recall searching.
- The PubMed example describes the architecture published by Fiorini et al.
  (2018), [Best Match: New relevance search for PubMed](https://pmc.ncbi.nlm.nih.gov/articles/PMC6112631/):
  BM25 followed by LambdaMART on the top 500. It is a published architectural
  example, not an independently tested claim about every current endpoint.
- The Primo example follows [Ex Libris's documentation](https://knowledge.exlibrisgroup.com/Primo/Product_Documentation/020Primo_VE/Primo_VE_%28English%29/015_Getting_Started_with_Primo_Research_Assistant):
  CDI retrieval, up to 30 reranked with embeddings, five abstracts for generation.
  These limits were cross-checked against the documentation on 2026-10-04.
  Neither this description nor the chapter identifies that embedding reranker
  as a cross-encoder. The illustration keeps those categories separate.
- Every MP4 must fully decode to the expected frame count at 1080p/30 fps, retain
  every embedded caption in order, and put the MP4 metadata before the media for
  fast-start playback. Encoded loudness must be within 1 LU of −16 LUFS, with true
  peak below −1 dBTP. Each voice take must exceed the music by at least 10 dB.

Source scripts and original artwork follow the repository's CC BY 4.0 licence.
Credit Aaron Tay and the book when sharing these adaptations.
