# Chapter 3: BM25 and ranked lexical retrieval

Three narrated 1080p explainers adapted from Aaron Tay's *How Search Decides
What You See*, Chapter 3, `search-textbook.html#bm25-ranking`:

| Film | Topic | Initial duration |
|---|---|---|
| Words are weighted clues | Shared analysed terms, document frequency, IDF, summed contributions, score versus relevance | 2:09 |
| Why more words stop helping | Saturation, k₁, document length, b, and interpreting a contribution | 2:15 |
| The same index, a ranked result | Boolean admission, scoring evidence, top-k, direct BM25 retrieval, and safe pruning | 2:22 |

The films continue the original flat-vector visual language of Chapter 2:
paper characters, index robots, moving evidence signals, clear diagrams and
colorful geometric scenery. The plots and numeric labels are calculated from
the formula used in the examples. All illustrations and music are original.

## Run

From the repository root, on Windows with Python 3.12:

```powershell
uv venv outputs/chapter-3-videos/.venv --python 3.12
uv pip install --python outputs/chapter-3-videos/.venv/Scripts/python.exe -r tools/chapter-3-videos/requirements.txt
& outputs/chapter-3-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-3-videos/render.py
```

The existing Chapter 2 environment can also run this renderer. The requirements
file includes the Chapter 2 requirements rather than duplicating them.

```powershell
# Speech, timeline, mastered sound, captions and scene review frames.
& outputs/chapter-3-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-3-videos/render.py --prepare-only
# Render a prepared film. Episodes can render in independent processes.
& outputs/chapter-3-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-3-videos/render.py --render-only --episode 1
# Review frames or check the existing MP4s without rendering again.
& outputs/chapter-3-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-3-videos/render.py --stills-only
& outputs/chapter-3-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-3-videos/render.py --verify-only
# Local player with byte-range support. Chapter 2 uses port 8773.
& outputs/chapter-3-videos/.venv/Scripts/python.exe tools/promo-video/serve.py --directory outputs/chapter-3-videos --port 8774
```

Open `http://127.0.0.1:8774/preview.html`. `--episode 1`, `2`, or `3` selects a
film; the default is all three. `--output` chooses a different export directory.

## Reused media engine

`render.py` loads the Chapter 2 engine for speech caching, audio mixing and
mastering, captions, image encoding, muxing and verification. The Chapter 2
renderer now accepts a film class; its default remains the Chapter 2 film.
`scenes.py` supplies Chapter 3 diagrams and the calculated BM25 examples.

The British English synthetic voice is Microsoft's `en-GB-RyanNeural`, at a
−3% speaking rate. Speech synthesis requires internet access and sends only
the public narration to Microsoft's speech service. Word timings drive the
scene durations and selected visual cues. Takes are cached and never cut or
time-stretched. Fonts are loaded from `C:/Windows/Fonts` and not bundled.

## Numeric and factual checks

The illustrations use a single-field BM25 with a common positive IDF variant:

```text
IDF = ln(1 + (N − df + 0.5) / (df + 0.5))
TF factor = tf × (k₁ + 1) / [tf + k₁ × (1 − b + b × dl / avgdl)]
term contribution = IDF × TF factor
```

At zero term frequency the contribution is zero. Production implementations
and related variants can differ, so the films label these numeric examples as
illustrative and identify the positive-IDF version.

- The average-length saturation curve matches the chapter's worked factors:
  1.00 at tf=1, 1.375 at tf=2 and approximately 2.08 at tf=20, with k₁=1.2.
- All curves use linear axes and the same scale. The factor is distinct from
  a score and from a probability of relevance.
- The length illustration holds rarity and tf fixed, uses avgdl=100, and
  compares dl=40 with dl=400. With b=0 the factors are equal.
- The four-record example reuses Chapter 2's D1–D4, with an explicit analyser
  that lowercases text and retains every word. The lengths are 4, 4, 3 and 5;
  the mean is 4. With k₁=1.2 and b=0.75, D1 scores about 0.80 and D4 about 0.72.
  Totals use full-precision contributions before rounding.
- Direct BM25 in the example admits any matching query term; the scored order
  is D1, D4, D3, D2. This is distinguished from the strict AND example.
- Safe pruning is explained using a separate hypothetical block example.
  A valid upper bound below the cutoff proves that a block cannot compete;
  the higher bound requires inspection.
- A relevance-sort label is not presented as proof of a particular formula,
  and scores are not described as relevance judgements or probabilities.

`validate_math()` checks the chapter's worked values and the four-record
example before preparing or rendering. The source chapter hash is stored in
each timeline and export report.

## Outputs and verification

All generated files stay under Git-ignored `outputs/chapter-3-videos/`.
The player links the three MP4s, SRT captions, transcripts and storyboards.
Each film has eight review stills, a poster, contact sheet, cached speech,
separate voice/music WAVs, mastered soundtrack, timeline and verification log.

Verification fully decodes each 1920×1080, 30 fps H.264/AAC MP4, confirms its
frame count, checks fast-start MP4 atom order and extracts the embedded captions
to compare them with the timed cues. The final encoded audio must be within
1 LU of −16 LUFS and below −1 dBTP. Per-take voice-to-music margins must exceed
10 dB. Contact sheets and frames from the encoded videos are visually reviewed.

Source scripts and artwork follow the repository's CC BY 4.0 licence. Credit
Aaron Tay and the book when sharing adaptations.
