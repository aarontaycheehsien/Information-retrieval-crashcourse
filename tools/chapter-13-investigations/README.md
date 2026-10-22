# Chapter 13: Diagnosing retrieval failure

Three original narrated animated investigations adapted from Aaron Tay's
*How Search Decides What You See*, Chapter 13, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **Where did the paper go?** — collection and eligibility, candidates and
   display cutoffs, indexed units and excerpts, four diagnostic lenses,
   vocabulary mismatch and remedies tested against known relevant records.
2. **It can spell it. Can it find it?** — component-relative OOV, lexical
   index versus model tokenisation versus learnt representation, the source's
   BERT pieces, encoding coverage, declared exact-keyword identity, pooling
   and preserving a lexical route when identity determines relevance.
3. **Every word was there** — direction and negation contrasts, query/corpus/
   task shift, training's operational meaning of relevance, local evidence,
   BEIR's qualified finding, explicit term logic and proximity, interaction
   architectures and NevIR's limits, first-stage preservation and next tests.

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
python -m pip install -r tools/chapter-13-investigations/requirements.txt
python tools/chapter-13-investigations/render.py --prepare-only
python tools/chapter-13-investigations/render.py --stills-only
python tools/chapter-13-investigations/render.py --render-only --workers 3
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
contains standalone Matplotlib PNG/SVG figures, declared identity and relation contrast CSV data and
a manifest linking assets to the recipe and checked examples. Figure notes are wrapped; note and table-cell drawing bounds and note overlap
are checked before export.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-13-investigations --port 8830
python tools/chapter-13-investigations/check-preview.py
python tools/chapter-13-investigations/render.py --package-only
```

Open `http://127.0.0.1:8830/index.html`. Browser checks require Playwright and
Chromium and exercise actual playback, seeking, captions, scene buttons,
byte-range responses and desktop/tablet/mobile layouts.

## Grounding and limits

`source-chapter.html` is the pinned Chapter 13 section. Source commit, full-book
hash and section hash appear in `source-provenance.json`. Each scene names a
source anchor. Runtime checks parse all three source tables: diagnostic
notices, vocabulary questions and first-stage method names. They also check
essential eligibility, component-vocabulary, distribution and research
qualifications. Source, script, production and shared-helper hashes reject
stale timelines; prepared take IDs/text must match the final script. Plot
manifests reject changed assets.

- A missing paper is a symptom, not a cause. The four illustrated paths are
  alternative hypothetical explanations for paper P: outside collection,
  filtered out, absent from the candidate pool, or retrieved below the
  display boundary. No traced service search was run. Coverage, indexing
  lag, applied limits and metadata need evidence. An unavailable trace or
  failed lookup is not proof of internal candidate exclusion.
- A paper absent from a shortlist cannot be rescued by a reranker that never
  receives it. Candidate limits, later display limits and filter/cutoff
  ordering are distinct boundaries. Passage indexing can split relevant
  evidence across units. A visible excerpt may omit a match in another
  indexed field or version; it does not show the entire indexed record.
- The four diagnostic lenses are different kinds of claim, nonexclusive
  prompts rather than exhaustive categories: vocabulary mismatch is a
  query–record relationship; OOV is relative to a named vocabulary; OOD is
  a training–deployment relationship; composition concerns matching or model
  capability. Several hypotheses can apply to the same failure.
- The heart-attack-recovery query and Rehabilitation after myocardial
  infarction title are the chapter's text example. Different terminology
  does not establish OOV. Synonyms, controlled vocabulary, explicit OR,
  citation searching and reformulation are established bridges to test.
  BM25 can use partial lexical overlap but does not itself make two phrases
  synonymous. Analysis and expansion elsewhere are separate operations.
  Suitably trained dense retrieval may bridge wording without exact overlap;
  no paraphrase guarantee or live medical retrieval test is claimed.
- The three OOV questions are separate: corresponding analysed index term and
  posting list, encodability in a named model vocabulary, and useful learnt
  retrieval representation. The third is a representation/training-exposure
  gap, not literal OOV. Indexed terms and model tokens are not interchangeable.
- The source reports BERT tokenising rizzlord as `ri`, `##zz`, `##lord`, rather
  than a reader's rizz/lord decomposition. The production displays that
  reported output; it does not run a new tokeniser or transfer the split to
  another model. A pure byte-level model can encode valid UTF-8 input;
  character coverage depends on inventory or fallback. Encoding form alone
  does not establish understanding or useful retrieval behaviour.
- The source supposes DELULU-427 in three indexed documents. Our declared
  keyword-field illustration invents D1/D2/D3 with literal DELULU-427 and D4
  with DELULU-428. Exact string equality yields three matches, verified by
  code. This is not a real index, BM25 run, model score or demonstration of
  an ordinary text analyser. Such an analyser might instead split word and
  number; query and document analysis must agree. Rare matching components
  can contribute to BM25 without model-training exposure to the identifier.
- Pooled dense representations may blur exact identifiers or decisive local
  details; better training can mitigate that weakness. The source does not
  claim dense retrieval always fails on identifiers. The contrast contains
  no invented vectors or measured similarity/ranking. Preserve an appropriate
  lexical route when exact identity determines relevance and inspect fields.
- OOD can involve query style, register, length or intent; corpus/domain
  discipline, genre, language, document type or period; and task/relevance
  relationships. These are useful sites, not a fixed formal partition.
  Familiar words do not prove successful transfer. One bad result cannot
  prove OOD; systematic local differences and training information strengthen
  the hypothesis. Unknown vendor training limits conclusions.
- Training positives, negatives and labels reward an operational relevance
  relationship. Finding one answer-bearing passage differs from high-recall
  evidence sets, known items and citation discovery. Synonyms alone do not
  resolve task shift. The cited BEIR finding describes heterogeneous benchmark
  tasks: BM25 was a robust zero-shot baseline while some more expensive neural
  and reranking approaches did better on average. No new benchmark, universal
  lexical-transfer law or general dense-transfer failure is asserted.
- A causes B versus B causes A is an original controlled illustration of
  the source's direction contrast. Code verifies equal bag-of-term counts;
  no retrieval scores are computed. The intervention does not increase risk
  versus does increase risk illustrates a decisive negation difference.
  Explicit Boolean term logic does not automatically bind roles or negation
  scope. Excluding a word is not semantic interpretation of a proposition.
  Phrase/proximity controls preserve adjacency and local order, which alone
  do not solve causality, negation or relation binding.
- A cross-encoder's joint query/candidate interaction offers the strongest
  architectural opportunity for relations; it is not a correctness guarantee.
  Late interaction retains more token evidence than pooling while encoding
  query and document separately. The cited NevIR evaluation found cross-
  encoders strongest and late interaction next, yet most evaluated systems
  were at or below a random ranking baseline. That full qualification is
  retained. Neither architecture guarantees logic or repairs missing
  first-stage candidates. No models were run for this production.
- Boolean, BM25 and single-vector dense are three reference patterns, not an
  exhaustive list. Learnt sparse and late interaction can also retrieve
  first-stage candidates. Transformation changes inputs, control chooses
  operations, and rerankers compare shortlists. Product labels such as uses
  vectors do not identify which evidence the full pipeline preserves.
- Recommendations are tests against suspected causes: establish eligibility,
  use known relevant records or controlled contrasts, retain observations,
  identify unknowns and compare the predicted effect of an intervention.
  Multiple causes and remedies can coexist; none guarantees complete recovery.
  The chapter ends with hypotheses to compare in Chapter 14.

Checks cover source hashes/anchors and source categories; declared exact
identity and equal-term-count contrasts; script/take/caption/word agreement
and timing; sampled drawing bounds, figure-note/table-cell bounds, note overlap
and visual review; complete media decoding and exact frames; 1080p/30fps
H.264, stereo 48kHz AAC, −16 LUFS ±1 and peak below −1 dBTP; fast-start metadata
and embedded caption equality. Packaging checks MP4 hashes and ZIP CRCs.
Chromium checks real playback and responsive layouts. Earlier MP4 hashes are
checked for preservation before the local commit.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 13](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#diagnosing-failure),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit the author
and book when sharing. This adaptation adds original narration and illustrations.
