# Chapter 6: three animated explainers

Three narrated films adapted from **From language model to retrieval encoder**
in Aaron Tay's *How Search Decides What You See*. The maintained source is
`search-textbook.html#retrieval-encoder`.

| Film | Duration | Focus |
|---|---|---|
| How words become a search vector | 2:30 | Model tokens versus indexed terms; IDs, context, pooling, independent encoding |
| Teaching an encoder what to retrieve | 2:34 | The stated search need, positives, easy and hard negatives, retrieval training |
| Whose relevance does the model learn? | 2:44 | Clicks, answer pairs, citations, transfer, fine distinctions, local diagnosis |

The visual direction follows the requested colorful flat-vector science
explainer style, with geometric characters, animated machinery, orbiting
particles, moving signals and diagrams. All artwork and music are original.
The narrator is Microsoft's synthetic `en-GB-RyanNeural`, rather than a cloned
performer. Windows Segoe UI fonts are loaded locally and are not bundled.

## Render

From the repository root on Windows, use the existing Chapter 2 environment:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-6-videos/render.py
```

Or create an independent Python 3.12 environment:

```powershell
uv venv outputs/chapter-6-videos/.venv --python 3.12
uv pip install --python outputs/chapter-6-videos/.venv/Scripts/python.exe -r tools/chapter-6-videos/requirements.txt
& './outputs/chapter-6-videos/.venv/Scripts/python.exe' -X utf8 tools/chapter-6-videos/render.py
```

Modes: `--prepare-only` creates cached speech, mastered audio, captions and
storyboards; `--render-only` encodes prepared pictures; `--stills-only` refreshes
review frames; `--verify-only` checks final MP4s. `--episode 1`, `2`, or `3`
selects one film; default is all three. `--output` changes the export folder.
Modes are mutually exclusive. Source, script, artwork, and media-helper hashes
prevent reusing a prepared production after its inputs change.

The Chapter 2 media engine and `tools/pick-a-card/narrate.py` supply speech
caching, actual word timings, musical synthesis, mastering, H.264/AAC encoding,
and MP4 verification. Synthesis sends the public script to Microsoft's speech
service and requires internet. No narration is cropped or time-stretched.

## Watch and download

Generated files stay in Git-ignored `outputs/chapter-6-videos/`. `preview.html`
links the three MP4s, SRT captions, transcripts and storyboards. Each film has
eight review stills, a contact sheet, a poster, timed captions, separate voice
and music stems, a mastered soundtrack, a timeline and a verification report.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/chapter-6-videos --port 8806
```

Open `http://127.0.0.1:8806/preview.html`. The server supports byte-range requests
for scrubbing. Captions are burned into the picture, embedded in the MP4 and
exported as SRT/VTT. The optional web caption track can be enabled in the player.

## Accuracy and verification

- The `delulu` split and token IDs are explicitly illustrative. Actual pieces
  depend on the tokeniser. Input coverage does not imply understanding.
- Four-coordinate token vectors and their mean are toy examples, not measured
  embeddings. `validate_examples()` independently checks the illustrated mean
  `(0.6, 0.4, 0.5, 0.3)`.
- Query and passage encoders may share parameters or use distinct parameters.
  Independent encoding supports preparing passage vectors before a query.
- The positive and both negatives follow the chapter's stipulated search need.
  The interview passage can be useful under a different reading of that need.
- The moving training geometry uses unit-circle coordinates and calculated
  cosine similarity. The positive moves from 82 to 22 degrees, the hard negative
  from 28 to 68, and the easy negative from 145 to 150. The resulting order is
  checked. This is an illustration of a training objective, not an experiment,
  a universal training trajectory or a probability of relevance.
- `CMP-104` and `CMP-140` are invented identifiers. No model was scored on them.
- Training mismatch is presented as a hypothesis. Coverage, fields, query
  processing and candidate cut-offs must also be investigated.
- Each MP4 must fully decode at 1920×1080 and 30 fps with the expected frame
  count. Embedded subtitle text is checked against every ordered cue. MP4 atom
  order is checked for fast-start playback. Final audio must be within 1 LU of
  −16 LUFS and below −1 dBTP; each narration take exceeds the music by 10 dB.

Source scripts and original artwork follow the repository's CC BY 4.0 licence.
Credit Aaron Tay and the book when sharing the adaptation.
