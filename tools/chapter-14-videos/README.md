# Chapter 14: measuring retrieval, animated

Three narrated films adapted from **Measuring whether retrieval worked** in
Aaron Tay's *How Search Decides What You See*. The maintained source is
`search-textbook.html#evaluation`. Each of the 24 scenes records its supporting
chapter anchor in `episodes.json`.

| Film | Duration | Focus |
|---|---|---|
| Two questions. One search. | 3:11 | Relevance judgements, precision, recall, seed recovery, reranking and candidate boundaries |
| What does better mean? | 3:08 | Precision@k, MRR, MAP, nDCG, aspect coverage and independent depth budgets |
| Build a test your library owns | 3:26 | Test collections, pooling, transfer, local protocols, stress tests and hidden regressions |

The requested Kurzgesagt-inspired direction uses original geometric artwork,
vivid colors, a cosmic evaluation laboratory, a small robot, paper characters,
moving signals, animated gauges, rankings and diagrams. Music is synthesised
locally without recorded samples. Narration uses the installed **Microsoft David
Desktop** synthetic voice; its delivery is more mechanical than a human narrator.
Windows Segoe UI fonts are loaded locally and are not distributed.

## Generate and verify

From the repository root on Windows, reuse the Chapter 2 Python environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-14-videos/test-examples.py
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-14-videos/render.py
```

For a separate Python 3.12 environment, install `requirements.txt`. Microsoft
David Desktop and Windows `System.Speech` must be installed. The renderer reuses
the Chapter 2 media engine and Chapter 4 speech adapter without editing them.
It supports both the engine's explicit `film_class` argument and its earlier
global Film interface.

Modes are mutually exclusive: `--check-only` checks source anchors, scripts and
arithmetic; `--prepare-only` creates speech, mastered audio, captions and
storyboards; `--render-only` encodes prepared films; `--stills-only` refreshes
review frames; `--verify-only` verifies exports. `--episode 1`, `2`, or `3`
selects one film. `--output` changes the output directory. Source and production
hashes reject stale prepared timelines after chapter or renderer changes.
`--jobs 3 --render-only` encodes the three prepared films concurrently in
separate processes; only the parent writes the gallery and aggregate report.

All narration is synthesised locally; no chapter content is sent to an external
speech service. The installed voice's native 16 kHz clock supplies word timings.
Speech determines scene lengths and is neither cropped nor time-stretched.
Access to the Windows speech runtime may require sandbox approval. Music is
ducked beneath narration; each take must have at least a 10 dB voice-over-music
margin. The mastered soundtrack targets −16 LUFS.

## Watch and download

Exports are in `outputs/chapter-14-videos/`, excluded by that directory's scoped
`.gitignore`. The generated gallery links to MP4s, captions, transcripts,
storyboards and a complete ZIP. Each film has 1920×1080, 30 fps H.264/AAC video,
burnt-in and embedded English captions, SRT/VTT sidecars, a transcript, eight
review frames, a contact sheet, poster, voice/music stems, mastered audio and a
verification report.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-14-videos --port 8814
```

Open `http://127.0.0.1:8814/preview.html`. With the server running, set
`CHAPTER14_NODE_MODULES` to the bundled Node `node_modules` path and run
`node tools/chapter-14-videos/check-preview.cjs`. `CHAPTER14_PREVIEW_URL` overrides
the server URL. The browser check plays and seeks all films, checks captions,
tests byte-range requests and mobile widths, and saves player screenshots.
Finally, run `python tools/chapter-14-videos/package.py` in the rendering
environment to create `chapter-14-videos.zip`. Packaging checks production
freshness, media hashes and archive CRCs.

## Grounding and examples

- Figure 14.1 supplies the complete, controlled 20-record pool and both orders.
  All ten relevant records A–J remain candidates. Precision@10 and recall@10
  rise from 0.2 to 0.6, while candidate-pool recall remains 1.0. Equal numeric
  denominators count different things. These are stipulated judgements, not
  measured real-world relevance.
- All known seeds are relevant; the dimmed fourth seed is missed, rather than
  non-relevant. Seed recovery and relative recall do not reveal absolute recall
  in a live collection. Fresh-retrieval cards are schematic identities.
- MRR, MAP and nDCG examples are supplementary, fully judged toy lists. RR is
  1/first relevant rank; MRR averages over queries. AP is the sum of precisions
  at relevant hits divided by the complete relevant count, including missed
  relevant records. MAP averages AP over queries. The nDCG example explicitly
  uses gain `2^grade − 1`, discount `1/log2(rank + 1)`, and ideal-order
  normalisation at depth 3. This is one conventional gain formulation.
- Conventional relevance metrics do not explicitly reward aspect coverage.
  Aspect-aware evaluation requires further judgements. Retrieval, reranking
  and evaluation depths are independent; the 100/40/10 budgets are illustrative.
- Pooling means deduplicating result identities here. An unjudged card displays
  `?`, and common scoring treatment is distinguished from actual irrelevance.
- Table 14.3 is hypothetical. Its three equally weighted row means improve
  from 0.30 to approximately 0.33 while identifier precision loses two thirds.
  The composition row itself averages two separately judged queries; the
  displayed average is not an equally weighted mean of four individual queries.
- A local evaluation uses fixed depth, shared criteria, pooled judgements,
  separate seed recovery and an explicit fewer-than-k convention. Thirty to
  fifty queries is the chapter's starting range, not a coverage guarantee.
- No current product ranking or new benchmark result is asserted. Measurement
  finds differences; diagnosis investigates causes. Generated-answer checks
  remain conditioned on the retrieved shortlist.

Seven checks validate the arithmetic, candidate boundaries, source fixtures and
all 24 scenes at five animation times. Full export verification decodes every
frame, checks frame counts, dimensions, codecs, exact ordered embedded captions,
fast-start atom ordering, SHA-256, encoded audio within 1 LU of −16 LUFS and
true peaks below −1 dBTP. All three contact sheets are visually reviewed.

Scripts and original artwork follow the repository's CC BY 4.0 licence.
Credit Aaron Tay and the book when sharing these adaptations.
