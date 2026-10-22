# Chapter 3: BM25 and ranked lexical retrieval

Three original animated explainers adapted from Aaron Tay's *How Search Decides
What You See*, Chapter 3, on `more-readable` at commit
`37b16f7ffa64e858adc454fc4c40ce528ef433b4`.

1. **Which word deserves more weight?** — shared analysed terms, collection
   rarity, document versus term frequency, additive evidence and score limits.
2. **Twenty mentions. Twice the credit?** — calculated saturation curves,
   k₁, document-length normalisation, b and the limits of a score.
3. **Same index. Three different controls.** — the D1–D4 worked example,
   eligibility versus scoring versus top-k, documented academic pipelines and
   valid score bounds for safe pruning.

The creative direction continues the previous series: original paper cards,
curiosity-led questions, prediction pauses and evidence-led reveals. Independently
produced, with no affiliation with Veritasium. Narration uses the standard
Microsoft Andrew Multilingual synthetic voice. No voice cloning, presenter
likeness, third-party footage, product screenshots or brand assets are used.

## Generate and review

This production uses separate new directories. The textbook, earlier scripts
and previous exports are preserved. Generated media are local and Git-ignored;
production sources are committed separately. Nothing is remotely published.

From the repository root, using Python 3.12:

```bash
python -m pip install -r tools/chapter-3-investigations/requirements.txt
python tools/chapter-3-investigations/render.py --prepare-only
python tools/chapter-3-investigations/render.py --stills-only
python tools/chapter-3-investigations/render.py --render-only --workers 3
```

FFmpeg must be on PATH, or set `CHAPTER_FFMPEG`. DejaVu fonts are loaded locally;
`PREFACE_FONT_DIR` can select the folder containing `DejaVuSans.ttf`,
`DejaVuSans-Bold.ttf` and `DejaVuSerif.ttf`. `--episode 1`, `2` or `3` selects a
film, `--output` changes the export folder, and `--workers` controls local
encoder processes. The original Chapter 1 media engine, shared speech helper
and preface drawing primitives are reused without modifying those productions.
No GPU or paid video-generation API is required.

The public adaptation script is sent to Microsoft's speech service through
edge-tts. TLS verification remains enabled, with the managed proxy CA trusted
when configured. Takes are cached and never cropped or sped up to fit the
picture. Actual speech timings determine the timeline and reveal cues.

Each film exports a 1920×1080, 30 fps H.264/AAC MP4 with burnt-in and embedded
English captions; SRT/VTT; timed transcript; source-linked storyboard; poster;
review frames; contact sheet and verification report. A gallery and ZIP contain
the complete series. Matplotlib figures are included separately as PNG and SVG,
along with CSV data and full-precision toy scores, for inspection and reuse.

```bash
python tools/promo-video/serve.py --directory outputs/chapter-3-investigations --port 8820
python tools/chapter-3-investigations/check-preview.py
python tools/chapter-3-investigations/render.py --package-only
```

Open `http://127.0.0.1:8820/index.html`. Browser checks need Playwright and
Chromium and cover playback, seeking, scene buttons, captions, byte ranges and
desktop/tablet/mobile layouts. Layout screenshots capture the original posters
after functional checks, with native browser controls hidden for the capture.

## Model and evidence limits

The pinned Chapter 3 snapshot and supporting Chapter 2 collection accompany the
script. Source and production hashes reject stale timelines. Every scene names
an anchor in Chapter 3; the D1–D4 texts are verified against Chapter 2.

The explicit teaching model is single-field BM25 with a common positive-IDF
variant. Production implementations and related variants can differ:

```text
IDF = ln(1 + (N − df + 0.5) / (df + 0.5))
frequency factor = tf × (k₁ + 1) / [tf + k₁ × (1 − b + b × dl / avgdl)]
term contribution = IDF × frequency factor
document score = sum of matching-query-term contributions
```

At tf = 0, contribution is zero, including when k₁ = 0. The average-length
factor at k₁ = 1.2 is 1.000 for one occurrence, 1.375 for two and approximately
2.075 for twenty; the limiting value is 2.2. Curves share linear axes and
scales. Frequency factors, contributions and document scores are never labeled
as probabilities of relevance. k₁ = 0 gives factor 1 for positive frequencies;
it does not make an absent term contribute.

The length illustration fixes one occurrence, term rarity and avgdl = 100,
comparing dl = 40 with dl = 400. With b = .75 the factors are approximately
1.325 and .449; with b = 0 they are both 1. Card drawings are not to scale.
The rarity example uses the chapter's 2-of-10 and 9-of-10 counts. Its weights
and average-length sum of approximately 1.63 belong to this explicit variant.

The toy D1–D4 analyser lowercases and retains all words. Lengths are 4, 4, 3, 5,
with average 4. At k₁ = 1.2 and b = .75, D1 scores approximately .80 and D4
.72. Full-precision contributions are summed before rounding. Strict AND
admits D1 and D4; direct any-term matching gives D1, D4, D3, D2. Top-k changes
the retained output, not the scoring rule.

PubMed's published Best Match account is attributed to the chapter: BM25
first, LambdaMART on the top 500. Scopus and Primo CDI documentation is used as
evidence of lexical signals, not proof of plain BM25. Lucene-family defaults
identify text similarity, not every configuration's final ranking. No current
service behavior is represented as freshly tested for these films.

The pruning example uses separate hypothetical numbers. Once a full current
top-k has cutoff 5, a valid block upper bound of 3 permits skipping it; a bound
of 7 needs inspection and does not guarantee a winner. Validity is stipulated,
not inferred from an observed score. No response time or speedup is measured.
Performance depends on hardware, index design, query mix and accuracy settings.

Checks cover the chapter's independent worked values, exact arithmetic reference
fractions, monotonic diminishing gains, length-control cases, source records,
toy eligibility/rankings, plot hashes, every spoken word and caption, timing and
layout samples, complete media decoding, exact frame counts, resolution/codecs,
30 fps, stereo 48 kHz, −16 LUFS ±1, peaks below −1 dBTP, fast-start metadata and
embedded subtitle text. Packaging verifies MP4 and plot hashes and ZIP CRCs.

Adapted from [Aaron Tay, *How Search Decides What You See*, Chapter 3](https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#bm25-ranking),
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Credit Aaron Tay and
the book when sharing. This adaptation adds original narration and figures.
