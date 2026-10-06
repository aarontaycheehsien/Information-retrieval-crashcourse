# Chapter 5: embeddings, animated

Three narrated films adapted from Aaron Tay's *How Search Decides What You See*,
`search-textbook.html#embeddings`. Original flat geometric animation uses a dark
cosmic palette, paper characters, an encoder robot, moving diagrams, and playful
visual metaphors inspired by animated science explainers.

| Film | Initial duration | Content |
|---|---|---|
| A map made from words | 2:38 | Representations, learnt mappings, the distributional hypothesis, CBOW/Skip-gram, analogy directions, and projection limits |
| One word, two worlds | 2:37 | Static versus contextual word vectors, self-attention, model tokens versus index terms, pooling, and vector comparison |
| Language knowledge is not relevance | 2:40 | CBOW, masked language modelling, next-token prediction, domain pretraining, retrieval training, and model roles |

## Render

The existing Chapter 2 Python environment can run the films:

```powershell
& outputs/chapter-2-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-5-videos/render.py
```

For a fresh Python 3.12 environment, create a venv and install
`tools/chapter-5-videos/requirements.txt`. The requirements reuse Chapter 2's
media dependencies: Skia, NumPy, Pillow, edge-tts, and imageio-ffmpeg.

```powershell
# Generate voice, music, captions, timelines, and review frames.
& outputs/chapter-2-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-5-videos/render.py --prepare-only
# Render a prepared film; independent episodes can render in separate processes.
& outputs/chapter-2-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-5-videos/render.py --render-only --episode 1
# Rebuild storyboards or verify completed exports without re-rendering.
& outputs/chapter-2-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-5-videos/render.py --stills-only
& outputs/chapter-2-videos/.venv/Scripts/python.exe -X utf8 tools/chapter-5-videos/render.py --verify-only
# Serve the local gallery with video seeking support.
& outputs/chapter-2-videos/.venv/Scripts/python.exe tools/promo-video/serve.py --directory outputs/chapter-5-videos --port 8776
```

Open `http://127.0.0.1:8776/preview.html`. `--episode 1`, `2`, or `3` selects one
film. `--output` chooses another directory. Generated assets are ignored by the
scoped `outputs/chapter-5-videos/.gitignore`.

The media engine in `tools/chapter-2-videos/render.py` provides cached speech,
word timings, music synthesis, audio mastering, captions, encoding, and export
verification. The wrapper supports both its original API and the newer
`film_class` parameter. Chapter 5 owns its scene frame, transcript attribution,
and MP4 metadata so it can run without unrelated Chapter 3 changes.

Speech uses Microsoft's `en-GB-RyanNeural` synthetic voice at a −3% rate.
Synthesis requires network access and sends the public narration to Microsoft's
speech service. Scene lengths follow actual speech durations; speech is never
cut or time-stretched. The music is generated locally. System Segoe UI fonts
are loaded from `C:/Windows/Fonts` and are not redistributed.

## Teaching boundaries

- All map coordinates, vector bars, arrows, and training movements are
  illustrative, not measurements from a trained model. The country/capital
  diagram is newly drawn rather than a reproduction of the book's research
  figure. No pretrained model or numerical PCA result is claimed.
- The analogy is described as a demonstration that works in some trained
  spaces, with input words excluded from candidate answers, not a universal
  equation or a guarantee about a model's knowledge.
- BM25 also calculates numeric representations. The comparison concerns the
  origin of the mapping: specified weighting rules versus learnt parameters.
- CBOW and Skip-gram are distinguished. The hidden-word illustration is
  explicitly CBOW, not a definition of all Word2Vec training.
- The model-token illustration uses a declared character-level toy tokenizer.
  The word boxes in the prediction games simplify model-token tasks.
- Contextual token representations and a complete-text embedding are separate
  stages. The pooling illustration is a generic combination, not a claimed
  implementation of BERT or a production retrieval model.
- Language pretraining, domain pretraining, and retrieval training are
  separated. Retrieval signals need not be human relevance labels.
- A vector-comparison score does not certify truth or relevance. A model name
  alone does not establish either task training or its place in the pipeline.

## Verification and outputs

Each film exports a 1920×1080, 30 fps H.264/AAC MP4 with burnt-in and embedded
English captions, plus SRT/VTT files, a transcript, eight scene stills, a contact
sheet, and a poster. Timelines record hashes of the chapter and episode script;
stale prepared files are rejected when either source changes.

Export verification fully decodes every frame, checks the expected frame count,
dimensions and codecs, compares extracted embedded captions with the timed
cues, checks fast-start MP4 atom order, and measures encoded loudness and peak.
Audio must be within 1 LU of −16 LUFS, with true peak at or below −1 dBTP.
Per-take narration must exceed the music by at least 10 dB. Verification JSON
files include output SHA-256 hashes. Review the contact sheets and frames
extracted from the encoded videos before delivery.

Scripts, original drawings, and generated adaptations follow the repository's
CC BY 4.0 licence. Credit Aaron Tay and the book when sharing.
