# Chapter 14: Measuring whether retrieval worked

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 14, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **Can both scores improve?** — relational relevance and judgement criteria,
   precision/recall denominators, the source's complete 20-record reranking
   example, candidate-pool ceilings versus displayed depth, fresh retrieval,
   unknown recall totals and task-specific methodological practice.
2. **The number that ignores the rest** — evaluation depth versus budgets,
   reciprocal rank and average precision for the controlled source query,
   MRR/MAP as query means, graded nDCG's goal, aspect-coverage limits,
   Cranfield comparison controls, BEIR's qualifications and judgement pooling.
3. **The average went up. The search got worse.** — the source's hypothetical
   precision regression hidden by an equal-row mean, building local queries,
   fixed-depth pooled judging, separate seed recovery, deliberate diagnostic
   probes, run variation, answer faithfulness and repeatable local baselines.

Original paper-and-ink artwork, curiosity-led questions, prediction pauses and
word-timed reveals continue the series. Independently produced, with no
affiliation with Veritasium. Narration uses the standard Microsoft Andrew
Multilingual synthetic voice. Original drawings and script adaptations use
no presenter likeness, voice cloning, third-party footage or copied screenshots.

## Reproduce and review

The production lives in new isolated directories. Generated media stay local
and Git-ignored; production sources are committed. Nothing is published or
pushed. Shared media, speech-cache and drawing helpers are reused without
modification; earlier productions and textbook files are preserved.

From the repository root with Python 3.12 and FFmpeg on PATH:

```bash
python -m pip install -r tools/chapter-14-investigations/requirements.txt
python tools/chapter-14-investigations/render.py --prepare-only
python tools/chapter-14-investigations/render.py --stills-only
python tools/chapter-14-investigations/render.py --render-only --workers 3
```

`CHAPTER_FFMPEG` can specify FFmpeg. System DejaVu fonts are used;
`PREFACE_FONT_DIR` can choose a folder containing `DejaVuSans.ttf`,
`DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf`. `--episode 1`, `2` or `3` selects
a film; `--output` chooses the destination. No GPU, retrieval model or large
index is required for these declared teaching examples.

Public narration text is sent to Microsoft's speech service through edge-tts.
The managed proxy CA is trusted with TLS verification retained. Takes are
cached by text, voice and engine. Speech is not cut or accelerated to fit
animation; reveals follow actual word timings.

Exports include 1920×1080, 30 fps H.264/AAC MP4s, burnt-in and embedded English
captions, SRT/VTT, timed transcripts, source-linked storyboards, posters,
review frames, contact sheets and verification reports. The responsive watch
gallery and ZIP contain all three films and supporting material. `plots`
contains standalone Matplotlib PNG/SVG figures, controlled source rankings and local-regression CSV data and
a manifest linking assets to the recipe and checked examples. Figure notes are wrapped; note and table-cell drawing bounds and note overlap
are checked before export.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-14-investigations --port 8831
python tools/chapter-14-investigations/check-preview.py
python tools/chapter-14-investigations/render.py --package-only
```

Open `http://127.0.0.1:8831/index.html`. Browser checks require Playwright and
Chromium and exercise actual playback, seeking, captions, scene buttons,
byte-range responses and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 14 section. Source commit, full-book
hash and section hash appear in `source-provenance.json`. Each scene names a
source anchor. Runtime checks parse all three source tables, the four source
relevance perspectives, both exact 20-record rankings and their relevance
labels, and the local table's known counts and before/after values. Essential
methodological qualifications are checked too. Source, script, production and
shared-helper hashes reject stale timelines; prepared take IDs/text must
match the final script. Plot manifests reject changed assets.

- Relevance is relational: information, represented need, person and situation.
  The four perspectives are system/algorithmic, topical, cognitive/pertinence
  and situational/usefulness. This is the chapter's teaching simplification,
  not a complete taxonomy; affective dimensions are outside its four-part
  account. Scores and similarity estimates are not human usefulness itself.
  A topical item can fail task-specific inclusion criteria. Metrics inherit
  assessor instructions, binary/graded labels and the operational relevance
  definition rather than measuring abstract objective correctness.
- Figure 14.1 stipulates exactly ten relevant records A–J in a 20-record
  candidate pool, with K–T judged non-relevant. Both source orders are copied
  exactly and checked against the source DOM. First-page precision and recall
  change from 2/10 to 6/10; whole-pool recall remains 10/10. The denominators
  happen to equal ten while counting different things. This is a controlled
  source illustration, not a retrieval run or observed product improvement.
  No additional candidates or relevance grades are invented.
- Reranking fixed membership can improve precision@10 and recall@10 together.
  Candidate generation creates a ceiling only for stages processing its fixed
  output. A fresh route/round can add relevant identities to the cumulative
  pool. Duplicates and irrelevant additions do not raise recall, and cutoff
  effects still determine which useful records are displayed. A hybrid or
  agentic label alone does not establish that new relevant records were added.
- Increasing depth on a fixed ranking cannot lower recall; precision can rise
  or fall. Better systems can improve both measures at the same depth.
  Precision requires judging returned records, while absolute recall needs
  the complete relevant total under the protocol. Known-seed recovery and
  relative recall against a discovered relevant union are useful scoped
  checks, not an absolute live-collection denominator.
- The August 2026 evidence-synthesis note describes structured database
  searching as the formal core, supplemented by other routes. It is a dated
  methodological account, not an inherent Boolean recall advantage. Boolean
  omissions, analysis, coverage and operators matter. Ranked candidate limits
  can constrain BM25 as well as dense retrieval. Evaluate the complete
  workflow's sensitivity for the task.
- Evaluation depth k is distinct from a retriever's candidate boundary and a
  reranker budget. Precision@k gives positions inside the depth equal credit
  and gives records beyond it no credit at that depth. Compare at a stable
  depth and document capture and denominator conventions for shorter lists.
- The single-query RR and AP numbers are calculated from the complete source
  rankings and stipulated binary judgements. RR is 1/first relevant rank,
  which stays 1 in both orders. AP sums precision at each relevant rank and
  divides by the complete judged-relevant count of ten: approximately 0.487
  before and 0.764 after. MRR and MAP average query-level RR and AP; these
  one-query calculations are not a multiquery benchmark. No retrieval model,
  reranker or product was executed to generate the rankings.
- nDCG's graded, rank-discounted goal is explained relative to an ideal
  ordering at the evaluation depth. An explicit gain/discount convention and
  defensible graded labels are needed for a numerical calculation. No grades
  or nDCG values are invented for the source's binary example. All four
  conventional metrics treat record judgements independently; good scores
  need not establish coverage across known aspects.
- Cranfield-style offline comparisons hold collection, topics and judgements
  fixed. User/task studies and online evaluation address complementary
  questions. Judgement pooling unions top records from multiple systems; it
  is different from token-to-vector pooling. Under the described scoring
  convention, unjudged items count as non-relevant even when useful, which
  can disadvantage approaches unlike those contributing to the pool.
- The source's BEIR account is conditional on its topics, collections and
  assessors: BM25 was robust across unseen collections while several more
  expensive neural systems did better on average. This is neither a new
  benchmark nor a universal transfer claim for a library's subjects,
  languages, document types or actual questions.
- Table 14.3 describes a hypothetical update. Identifier precision@10 drops
  0.3→0.1; vocabulary-mismatch precision rises 0.2→0.5; the composition row
  stays 0.4. The source attributes the hypothetical identifier regression to
  an expansion dropping SLC6A4. No actual discovery update or causal test was
  performed. The relative loss is two thirds, or 0.2 absolute precision.
- The displayed-row mean weights exactly three rows equally: 0.30→1/3,
  shown rounded to 0.33. The composition row averages two separately judged
  opposite-meaning queries. This is not a four-query equally weighted mean.
  Source known-relevant counts 3/5/4 are retained as seed information and
  never used to invent exhaustive recall. Charts and CSVs carry the scope.
- A practical local set starts with 30–50 real queries and known difficult
  cases. An afternoon rerun is not an estimate for constructing criteria and
  judging hundreds of results. Fix depth, union/deduplicate both runs there,
  judge every pooled record under the same criteria and ideally hide which
  run supplied it. Calculate fixed-depth precision and report known-seed
  recovery separately. This production explains that protocol; it does not
  claim to have created or judged a real library benchmark.
- Deliberate probes cover exact identifiers, full-text-only phrases,
  near-zero-overlap known relevant records and opposite-meaning queries.
  These investigate lexical routes, indexed units, vocabulary bridging and
  composition. They do not make a metric identify the internal cause.
- Per-query losses and differences by discipline/language/type can disappear
  in a mean. A change smaller than run-to-run variation needs further
  evidence. The videos do not invent uncertainty intervals or significance
  results. Ask for topic provenance, criteria, judges, depth, metric, grades
  and baseline, then test the hard local queries.
- Answer faithfulness and claim-to-source support are additional evaluation
  layers. They inherit the retrieval shortlist and cannot reveal every
  excluded relevant source. A faithful summary of the wrong records does not
  repair retrieval. Rerun the local baseline after updates/migration or before
  renewal; retain the protocol and investigate differences. Chapter 15 turns
  to recording, inspection and requirements; this task stops at Chapter 14.

Checks cover source hashes/anchors, categories, complete source rankings and
local table cells; exact fraction arithmetic, ranking membership, monotone
fixed-ranking recall and variable precision; script/take/caption/word agreement
and timing; sampled drawing bounds, figure-note/table-cell bounds, note overlap
and visual review; complete media decoding and exact frames; 1080p/30fps
H.264, stereo 48kHz AAC, −16 LUFS ±1 and peak below −1 dBTP; fast-start metadata
and embedded caption equality. Packaging checks MP4 hashes and ZIP CRCs.
Chromium checks real playback and responsive layouts. Earlier MP4 hashes are
checked for preservation before the local commit.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 14](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#evaluation),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author
and book when sharing. This adaptation adds original narration and illustrations.
