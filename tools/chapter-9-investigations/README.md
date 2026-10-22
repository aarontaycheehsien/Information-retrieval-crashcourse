# Chapter 9: Reranking and multi-stage retrieval

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 9, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **The paper the reranker never saw** — candidate ceilings, fast retrieval
   and richer second passes, independent versus joint encoding, the chapter's
   job-search hard negative, pointwise/pairwise/listwise LLM prompting, and
   the documented Semantic Scholar keyword-to-LightGBM route.
2. **One vector, or many clues?** — ColBERT-style independent token encoding,
   the source's invented MaxSim arithmetic, inspectable alignments and latent
   features, storage/compression, learnt sparse retrieval and Elicit's dated
   development account, and the breadth of neural information retrieval.
3. **The best next result may rank lower** — diversification versus individual
   relevance, deduplication and high-recall review; source-exact schematic
   selections; PubMed and Primo budgets, Primo's documented lexical-to-embedding
   stages, and the distinction between five abstracts and complete papers.

Original paper-and-ink artwork, curiosity-led questions, prediction pauses and
word-timed reveals continue the earlier series. Independently produced, with
no affiliation with Veritasium. Narration uses the standard Microsoft Andrew
Multilingual synthetic voice. Original drawings and script adaptations use
no presenter likeness, voice cloning, third-party footage or product screenshots.

## Reproduce and review

The production lives in new isolated directories. Generated media stay local
and Git-ignored; production sources are committed. Nothing is published or
pushed. Shared media, speech-cache and drawing helpers are reused without
modification; earlier productions and textbook files are preserved.

From the repository root with Python 3.12 and FFmpeg on PATH:

```bash
python -m pip install -r tools/chapter-9-investigations/requirements.txt
python tools/chapter-9-investigations/render.py --prepare-only
python tools/chapter-9-investigations/render.py --stills-only
python tools/chapter-9-investigations/render.py --render-only --workers 3
```

`CHAPTER_FFMPEG` can specify FFmpeg. System DejaVu fonts are used;
`PREFACE_FONT_DIR` can choose a folder containing `DejaVuSans.ttf`,
`DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf`. `--episode 1`, `2` or `3` selects
a film; `--output` chooses the destination. No GPU, embedding model or
large search index is required for the declared teaching examples.

Public narration text is sent to Microsoft's speech service through edge-tts.
The managed proxy CA is trusted with TLS verification retained. Takes are
cached by text, voice and engine. Natural speech is not cut or accelerated
to fit animation; reveals follow real word timings.

Exports include 1920×1080, 30 fps H.264/AAC MP4s, burnt-in and embedded English
captions, SRT/VTT, timed transcripts, source-linked storyboards, posters,
review frames, contact sheets and verification reports. A responsive watch
gallery and ZIP include the three films and supporting material. `plots`
contains standalone Matplotlib PNG/SVG tables, precise CSV data and an asset
manifest linked to the figure recipe and worked checks.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-9-investigations --port 8826
python tools/chapter-9-investigations/check-preview.py
python tools/chapter-9-investigations/render.py --package-only
```

Open `http://127.0.0.1:8826/index.html`. Browser checks require Playwright and
Chromium and exercise actual playback, seeking, captions, scene buttons,
byte-range responses and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 9 section, despite its historical
`reranking-and-hybrid` anchor. Hybrid retrieval is the next chapter's topic.
Source commit, full-book hash and section hash are in `source-provenance.json`.
Every scene names a section anchor. Source, scripts, production and shared
helper hashes reject stale timelines. Prepared take IDs/text must match the
current script. Plot manifests reject modified assets.

- The A/B/C shortlist, reordered B/A/C with stipulated useful X outside it,
  is an original card illustration. It carries no measured scores or claim
  to objective relevance. Reranking cannot add a record absent from its pool;
  a separate retrieval or fetch operation must be documented separately.
- The delulu/unrealistic-expectations/job-interview example preserves the
  chapter's information need and intended positive/hard-negative distinction.
  No model run or ranking accuracy is claimed. Joint encoding makes finer
  comparison possible while remaining subject to training and truncation.
- Roughly 100 evaluations for 100 cross-encoder candidates is the source's
  order-of-work example, not measured latency. The frame draws 100 cards.
  Batching organises work without changing the number of candidate pairs.
- Pointwise, pairwise and listwise describe LLM prompting at inference time
  here, distinct from similarly named classical learning-to-rank objectives.
  Calibration, inconsistent preferences, context size, input order, prompting,
  model version and sampling can affect rankings. Generated rationales are
  not validation that a ranking is correct.
- Semantic Scholar's cited 2025 main-relevance account is keyword retrieval
  over titles/abstracts/author names, up to 1,000 candidates, then LightGBM
  using signals including title matches, citations and recency. This is not
  a current-service test, evidence of dense first-stage retrieval or an LLM
  reranker, or an explanation of later interface result counts.
- MaxSim uses the source's exact invented table: query tokens citation/benefit,
  document tokens open/access/citation/advantage, rows `[.10,.20,.90,.40]`
  and `[.20,.30,.50,.80]`. Runtime checks parse the pinned HTML table and
  compare every value. Row maxima .90/.80 sum to 1.70. These are contextual
  token similarities invented for teaching, not model outputs or word counts.
  Whole words simplify real tokenisation. MaxSim independently maximises each
  row and does not require one-to-one matches. A repeated-row check verifies
  that reuse of the same winning column is allowed.
- Alignments expose score composition, not why a model learnt those latent
  similarities. ColBERT can retrieve or rerank depending on implementation.
  Its token vectors remain independently encoded before late interaction.
- A simplified 100-token example compares 1 pooled vector with 100 retained
  token vectors, assuming equal vector dimensions. It is not a byte/latency
  benchmark. ColBERTv2's reported 6–10× reduction is attributed to residual
  compression relative to earlier late-interaction systems; it is not a
  universal storage guarantee for another pipeline.
- Elicit's June 2024 SPLADE/full-text account describes development work,
  not a confirmed production rollout. Learnt sparse active dimensions must
  overlap for the described nonzero term-matching score. Expansions may
  create overlap and increase posting work; familiar index infrastructure
  does not establish equal query latency. Limited public deployment
  documentation for late interaction does not establish absence.
- The source's schematic six-paper pool is A/B/C overall citation advantage,
  D disciplinary differences, E selection-bias methods, F weakly related.
  A/B/C versus A/D/E are stipulated selections illustrating an objective,
  not computed MMR/other algorithm output, measured paper scores or findings
  about actual studies. They cover 1 versus 3 stipulated useful aspects.
  F stays outside both; difference alone is insufficient. A/B/C are distinct
  studies, not duplicate records. Topic coverage guarantees neither viewpoint
  diversity, fairness nor balanced evidence; high-recall review can need all
  relevant near-neighbours.
- The published PubMed Best Match account uses BM25 then LambdaMART on the
  top 500; its list continues beyond that reranked region in Best Match order.
  Primo Research Assistant reranks up to 30 CDI candidates using embeddings
  and supplies five selected abstracts for generation. Candidate budgets
  are not relevance counts, and the products handle their tails differently.
- Primo's pinned documentation chain uses LLM-generated OR-connected Boolean
  variations, supported auto-refinements, largely lexical CDI retrieval and
  lexical/static first-stage ranking, then embedding reranking. Five abstracts
  are not five full texts: a detail only in full text was not supplied in that
  documented context. No fresh vendor/service or full-text access test is claimed.
- Learning to rank can combine lexical and other available features without
  using embeddings. Neural IR spans several representations and stages;
  a Transformer or model name alone does not establish retrieval architecture.

Checks cover source hashes/anchors and exact MaxSim table cells; row maxima,
scores and reused-token behaviour; candidate membership and source selection
counts; full script/take/caption/word agreement and timing; sampled drawing
bounds and visual review; complete media decoding and exact frame counts;
1080p/30fps H.264, stereo 48kHz AAC, −16 LUFS ±1 and peak below −1 dBTP;
fast-start metadata and embedded-caption equality. Packaging checks MP4
hashes and ZIP CRCs. Chromium checks actual playback and responsive layouts.
Earlier MP4 hashes are checked for preservation before the local commit.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 9](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#reranking-and-hybrid),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author
and book when sharing. This adaptation adds original narration and illustrations.
