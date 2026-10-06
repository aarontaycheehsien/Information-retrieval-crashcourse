# How Codex built these videos

One narrated, high-level production retrospective about the earlier three
Chapter 1 films. It keeps the same original flat-vector direction: cosmic
background, vivid palette, index robot, paper characters, moving signals,
and a quiet synthesized musical score.

The film explains the visible work: read the chapter, choose three stories,
organize scenes, draw and animate with Python/Skia, follow the narration clock,
mix music, inspect pictures, render, verify and package. It includes an actual
example of a revision: moving candidate dots across a retrieval boundary while
keeping the missed gold paper visible.

`script.json` contains eight scenes, their narration and evidence pointers.
`film.py` draws the new original scenes. Three reduced original posters in
`assets/` illustrate the earlier output. `provenance.json` saves the earlier
verification reports, production counts and official documentation links.

The model and effort label follows the user's description of the earlier run:
**GPT-6.1 Sol at Extra High effort**. It is not independently recovered from
runtime telemetry. The film gives a high-level account of observable actions.
Official OpenAI documentation supports the definition of reasoning effort and
GPT-6.1 Sol's support for `xhigh`:

- [GPT-6.1 Sol](https://developers.openai.com/api/docs/models/gpt-6.1-sol)
- [Reasoning models](https://developers.openai.com/api/docs/guides/reasoning)

The earlier films reused **47 cached Microsoft Andrew neural takes**. This new
retrospective uses **new local Microsoft David Desktop narration**, which sounds
more mechanical. No production script is sent to an external speech service.
The online voice attempt was blocked by automatic approval review; the delivered
workflow uses the existing local Windows speech adapter.

## Generate and inspect

From the repository root on Windows:

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/video-making-of/test-production.py
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/video-making-of/render.py --prepare-only
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' -X utf8 tools/video-making-of/render.py --render-only
```

For a fresh Python 3.12 environment, install `requirements.txt`. Windows
System.Speech and Microsoft David Desktop are required. Local speech may need
sandbox approval to access the installed Windows speech components. The
renderer reuses the Chapter 1 preparation and review helpers, Chapter 2 media
engine and Chapter 4 speech adapter without changing those files.

Mutually exclusive modes: `--check-only`, `--prepare-only`, `--stills-only`,
`--render-only`, `--verify-only`, and `--package-only`. `--output` changes the
export folder. Source and production hashes reject stale prepared timelines.
The local voice sets the scene lengths, word timings, captions and key reveals.
Speech is never time-stretched or cut short.

Exports stay in Git-ignored `outputs/video-making-of/`, including the 1080p,
30 fps H.264/AAC video, burnt-in and embedded captions, SRT/VTT sidecars,
transcript, storyboard, three review stills per scene, contact sheet, poster,
voice/music stems and verification report.

```powershell
& './outputs/chapter-2-videos/.venv/Scripts/python.exe' tools/promo-video/serve.py --directory outputs/video-making-of --port 8820
```

Watch at `http://127.0.0.1:8820/preview.html`. Set `MAKINGOF_NODE_MODULES` to the
bundled Node `node_modules` path and run
`node tools/video-making-of/check-preview.cjs` to check real playback, seeking,
exact caption text, byte-range support and desktop/mobile layout.
`MAKINGOF_PREVIEW_URL` overrides the URL.

After verification, run the renderer with `--package-only` to create
`how-codex-built-the-videos.zip`. Packaging checks the current source/production
hashes, MP4 digest and archive CRCs.

Four checks cover the earlier production facts, the model/tool distinction,
the historical voice versus the new local voice, and all eight animated scenes
at five times, including intact poster decoding. Export verification completely decodes both streams in strict
error mode, checks frame counts, dimensions, fps, embedded captions and
fast-start metadata, and measures loudness within 1 LU of −16 LUFS with peaks
below −1 dBTP. Voice must exceed music by at least 10 dB RMS in every take.

Original code and artwork follow the repository's CC BY 4.0 licence. Credit
Aaron Tay and *How Search Decides What You See* when sharing the film.
