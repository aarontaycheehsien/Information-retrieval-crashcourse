# Pick a Card

A 93-second narrated promo for *How Search Decides What You See*. An unseen
close-up magician narrates. The search engine performs three tricks, and the
free textbook explains how tricks like these work.

> “Pick a card. Any card. … It was the one on top, wasn't it? Don't worry.
> That's the one most people pick. Magicians call that a force.”

The film turns the book's title into a magician's *force*: a choice that feels
free but was made for you. The three tricks are the book's three opening
puzzles from Chapter 1:

| Trick | What the viewer sees | Source in the book |
|---|---|---|
| The Impossible Word | A nonsense word (“shazamblix”) should empty a Boolean result list. Smoke clears and the results are all still there. | Chapter 1, Puzzle 1 |
| The Bottomless Deck | 9,400,000 results are reported, but dealing stops dead at page 100, after 1,000 results. | Chapter 1, Puzzle 2 |
| The Shrinking Question | A full-sentence question pulls 13 results from one hat. Its keywords spray ≈35,300 from the other. | Chapter 1, Puzzle 3 (observed August 2026) |

Then: “Magicians never reveal their secrets. And search tools don't always
explain theirs, either.” The book is dealt with Boolean, BM25, Embeddings,
Reranking, Hybrid search and Evaluation cards. When the tablecloth is whipped
away, the retrieval pipeline appears underneath. The end card turns into the
top card of a fan for the last line: “Oh, and this video? You didn't pick it
either.”

## Run it

From the repository root, on Windows:

```bash
uv venv outputs/pick-a-card/.venv --python 3.12
uv pip install --python outputs/pick-a-card/.venv/Scripts/python.exe -r tools/pick-a-card/requirements.txt
outputs/pick-a-card/.venv/Scripts/python.exe tools/pick-a-card/render.py
```

Other modes:

- `--stills 5.9,33.5,88.6` renders single review frames to `stills/`. Add `c` to
  a time, as in `33.5c`, to include burned-in captions.
- `--sheet` writes only `contact-sheet.jpg`: 36 frames across the film.
- `--verify-only` re-checks the existing MP4s.
- `--no-captioned` skips the burned-caption edition.
- `--workers N` sets the number of parallel frame workers.

Rendering is CPU-bound. The Windows skia-python wheels run Skia's 8-bit raster
pipeline without SIMD, so frames render on float16 surfaces, which are about
twice as fast, and are then read back as 8-bit. Frame chunks render in
independent worker processes and are joined losslessly. Each worker needs
about 0.65 GB because it runs two x264 encoders. By default, the number of
workers is set by free memory and cores. One worker takes about half an hour;
several workers take a few minutes. The picture-only intermediates are kept
until both exports pass verification.

The renderer loads Bodoni MT, Engravers MT, Playbill, Consolas, Segoe UI, Ink
Free and Georgia from `C:/Windows/Fonts`. To use another font directory, set
`PROMO_FONT_DIR`. To use another FFmpeg executable, set `PROMO_FFMPEG`. Fonts
are loaded locally and are not redistributed.

## How the narration stays human

The voice drives the film's timing.

- **Picture follows voice.** Each line is synthesised once, and only
  exterior silence is trimmed. Each line is placed after the previous line
  with a scripted pause from `script.json`. No take is sped up, slowed down or
  squeezed into a scene. Scene lengths and every animation are keyed to the
  word timings returned with the speech (`scenes.py: keys()`). The smoke clears
  on “here”, the hat pops on “thirteen”, and each topic card is dealt as it is
  named.
- **Written to be spoken.** The script uses contractions, asides (“Got one?”, “Go on…”, “Oh,
  and this video?”), ellipses for breaths and separate takes where a
  performer would pause. It runs at the voice's natural rate. One fixed gain
  per take levels the lines without compressing their dynamics.
- **A room, not a void.** A short synthetic room reflection is added at −17 dB,
  with faint room tone under the pauses. The music ducks 10 dB and the
  foley 8 dB under speech.
- **Voice:** Microsoft `en-US-AndrewMultilingualNeural` through
  [edge-tts](https://github.com/rany2/edge-tts). In a four-voice comparison
  (Andrew, Ava, Brian, Emma Multilingual), it was intelligible on the hard words
  and had lively but unforced pitch movement. “Written by Aaron Tay” is its own
  take because, inside the longer sentence, the name ran together. The voice
  is synthetic; there is no voice cloning.

Synthesis needs an internet connection and sends the public script to
Microsoft's speech service. Takes are cached under `voice-cache/` by text,
voice, rate and pitch. Unchanged lines are never re-requested. To change a
line, edit `script.json`. The cut, captions and sound effects follow
automatically.

## Quality checks

- Every render measures voice over music and foley, per line, in
  `mix-balance.json`. In the current mix, the worst line is 10 dB, and most
  lines are 12–17 dB.
- A local Whisper `base.en` transcription of the mastered mix during
  development had a 6.8% word error rate against the script. Nearly all
  differences were numerals written as digits, the invented word, or the
  author's name; the author's line transcribes correctly on its own. This QA
  step is not part of `render.py`.
- Every render fully decodes each export and checks frame count, −16 LUFS ±1
  integrated loudness, a true peak below −0.9 dBFS and fast-start MP4 atom
  order: `manifest.json`.

## Outputs (`outputs/pick-a-card/`, Git-ignored)

- `pick-a-card.mp4`: 1920×1080, 30 fps, H.264 and AAC, with no captions in the
  picture. Upload `pick-a-card.srt` with it where the platform supports caption
  files.
- `pick-a-card-captioned.mp4`: the same film with burned-in captions for muted
  feeds.
- `pick-a-card.srt`, `.vtt`: captions timed from word boundaries.
- `soundtrack.wav`, `stem-voice.wav`, `stem-music.wav`, `stem-foley.wav`.
- `poster.jpg`, `contact-sheet.jpg`, `transcript.txt`, `share-copy.txt`,
  `preview.html`, `manifest.json`, `mix-balance.json` and FFmpeg logs.

## Accuracy notes

- The three tricks are dated observations recorded in the book. They are not
  new product tests. On-screen footnotes say “a real observation in an
  academic search tool” and cite the chapter and puzzle. Products are not
  named, because the observations can change.
- “The one most people pick” rests on the book's point that a result at rank
  one is more likely to be seen and clicked because it is at rank one
  (Appendix E, on clicks as training signals).
- The film says that the book teaches how tricks *like these* work. It does not
  claim to reveal each product's internals. Chapter 1 says that some puzzles
  cannot be resolved from the outside.
- Search results on the cards, their authors and the book cover are original
  illustrations, not real papers or the book's own artwork.
- The score, including the waltz, drum roll, stamps and ta-da, is synthesised
  from oscillators and seeded noise. No samples, stock audio or music are used.

## Files

- `script.json`: spoken lines, pauses, voice settings and book links.
- `narrate.py`: speech synthesis, caching, trimming, the narration-led
  timeline and captions.
- `draw.py`: the Skia toolkit for palette, fonts, easing, cards, wand and
  stamps.
- `scenes.py`: the seven scenes and their word-keyed timings.
- `audio.py`: score, foley, voice room, ducking, balance checks and mastering.
- `render.py`: the CLI, frame rendering, encoding, mux and verification.
