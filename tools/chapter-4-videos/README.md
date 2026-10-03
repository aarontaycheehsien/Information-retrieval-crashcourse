# Chapter 4: lexical search beyond strict Boolean

Three narrated 1080p films adapted from Aaron Tay's *How Search Decides What
You See*, Chapter 4, `search-textbook.html#beyond-boolean`.

| Film | Topic | Initial duration |
|---|---|---|
| Three doors into the same search | All-term, minimum-match and any-match admission; ranking and output size | 2:45 |
| One bad word, two kinds of damage | Compulsory-term exclusion, optional-term scoring influence and saturation | 2:40 |
| The four lives of a missing word | Analysis, rewriting, optional clauses, hidden indexed evidence and pipeline diagnosis | 3:10 |

The original flat-vector artwork uses vibrant colors, geometric scenery,
anthropomorphic fruit and paper records, a small index robot, gates, magnets,
moving signals and smooth transitions. The broad visual approach is inspired
by colorful science animation such as Kurzgesagt. Artwork, characters and
music are original; no studio branding or assets are included.

## Generate

From the repository root on Windows:

```powershell
uv venv outputs/chapter-4-videos/.venv --python 3.12
uv pip install --python outputs/chapter-4-videos/.venv/Scripts/python.exe -r tools/chapter-4-videos/requirements.txt
& outputs/chapter-4-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-4-videos/render.py
```

An existing Chapter 2 or Chapter 3 Python environment can run the same script.
The fonts are loaded from `C:/Windows/Fonts`. Narration uses the installed
offline Windows `Microsoft David Desktop` voice through `System.Speech`.
No narration is sent to an external service. The local COM speech engine may
require approval outside a restricted sandbox. Speech is cached; actual
`SpeakProgress` word timings determine the film durations. No take is cut or
time-stretched. The speech adapter fixes the output at David's native 16 kHz;
using another installed voice requires validating its word clock first.

```powershell
# Source and example checks without synthesis or rendering.
& outputs/chapter-2-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-4-videos/render.py --check
# Prepare audio, timed captions and review frames first.
& outputs/chapter-2-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-4-videos/render.py --prepare-only
# Render a prepared episode (1, 2 or 3), or verify existing exports.
& outputs/chapter-2-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-4-videos/render.py --render-only --episode 1
& outputs/chapter-2-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-4-videos/render.py --verify-only
# Regenerate review frames after artwork edits.
& outputs/chapter-2-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-4-videos/render.py --stills-only
# Local player, with byte-range video support.
& outputs/chapter-2-videos/.venv/Scripts/python.exe tools/promo-video/serve.py --directory outputs/chapter-4-videos --port 8775
```

Open `http://127.0.0.1:8775/preview.html`. The generated player also opens
directly from disk. Every film has an MP4 with burned-in and embedded captions,
SRT/VTT sidecars, a transcript, poster, eight review stills, a contact sheet,
audio stems and a verification report. The default output folder contains a
generated `.gitignore` that excludes its media and caches. The maintained
scripts and artwork live here; the book itself is unchanged.

## Grounding and verification

`validate_examples()` checks the chapter's four fruit records and admission
sets: A for all three, A/B for two, and A/B/C for any one. The order B/A/C is
stipulated in the book and film; it is not a calculated BM25 ranking. Top two
keeps B/A. C was eligible, while D never qualified.

The bad-term story uses the book's A/F lab records. With all five terms
required, both are excluded; any-match admits both. Only F in the lab contains
`foolish`. The film asserts scoring influence, not a numerical order. The
saturation curve uses the average-length factor `tf * 2.2 / (tf + 1.2)` on
linear axes; it does not measure synonym quality or final relevance.

The missing-word mechanisms are possibilities, not diagnoses of current
products. The films retain the distinction between routine analysis,
execution rules, understanding and transformation. They avoid inferring
architecture from a snippet, result count, display limit or product name.

Source-chapter and script hashes bind cached timelines to the inputs. The
Chapter 2 media engine supplies timelines, mixing, encoding and full-file
verification; the local adapter supplies offline speech and word boundaries.
This wrapper supports its original API as well as newer film
class arguments, without requiring edits to shared files. Final checks decode
every video frame, check 1920×1080 at 30 fps, H.264/AAC and embedded caption
text, confirm fast-start MP4 atom order, and require loudness within 1 LU of
-16 LUFS, peaks below -1 dBTP and voice at least 10 dB above music per take.
Review the contact sheets and encoded frames visually before sharing.

Source scripts and illustrations follow the repository's CC BY 4.0 licence.
Credit Aaron Tay and the book when distributing adaptations.
