# Follow the Evidence

An original pop-song companion for Aaron Tay’s *How Search Decides What You See*:
bright synth-pop at 120 BPM in C major, with a repeating hook, two verses,
pre-choruses, three choruses, a quieter bridge, and a resolving outro.
The song lasts 2:58 (88 bars plus a two-second ring-out).

This is a locally produced **synthetic vocal demo**. It has a written sung melody
and intentionally electronic vocals, not a human performance. Original synthetic
speech from Microsoft Jenny is resynthesized with musical pitch and rhythm;
no voice is cloned. Drums, bass, piano, pads, arpeggios, risers, arrangement,
melody and lyrics are original. No stock tracks, commercial songs or samples
are used.

## Listen and reuse

Generated artifacts are kept in Git-ignored `outputs/textbook-pop-song/`:

- `follow-the-evidence.mp3`: complete song, 320 kbps stereo.
- `follow-the-evidence.wav`: 44.1 kHz, 16-bit stereo master.
- `follow-the-evidence-instrumental.mp3` and `.wav`: vocal-free mix.
- `follow-the-evidence.mid`: standard type-1 MIDI with lead melody, bass,
  arpeggio and chord tracks. The MIDI represents composition, not identical timbre.
- `lyrics.txt`, matching SRT/VTT, and `lyrics-timing.json`.
- `preview.html`: audio player, synchronized lyric highlights, line seeking,
  downloads and textbook links.
- Separate drums, bass, synths, electronic-vocal and dry-lead WAV stems.
- Speech and singing caches, timeline, pitch audit and export verification.

The maintained [lyrics](lyrics.md) are readable independently of production.
`song.json` is the source of truth for each sung word, its beat duration, notes,
tempo, voice settings and section order.

## Reproduce

From the repository root with Python 3.12 on Windows:

```powershell
py -3.12 -m venv outputs/textbook-pop-song/.venv
& './outputs/textbook-pop-song/.venv/Scripts/python.exe' -m pip install -r tools/textbook-pop-song/requirements.txt
& './outputs/textbook-pop-song/.venv/Scripts/python.exe' tools/textbook-pop-song/render.py
```

First synthesis sends only the original lyric phrases to Microsoft’s online
speech service via `edge-tts`. Unchanged takes are reused locally. Use
`--prepare-only` to create/check the sung phrases, then `--render-only` for
offline arrangement and mastering. Render-only verifies the current lyric
words, note/duration assignments, voice settings and singing implementation
against its caches. `--output` selects another folder. `SONG_FFMPEG` may point
to a local FFmpeg executable; otherwise `imageio-ffmpeg` supplies it.

The existing speech cache code at `tools/pick-a-card/narrate.py` is imported
without modifying it. Praat’s [pitch manipulation](https://parselmouth.readthedocs.io/en/stable/examples/pitch_manipulation.html)
and [DurationTier](https://praat.org/manual/Create_DurationTier___.html) provide
the resynthesis. Voiced regions sustain the tune while consonants keep shorter
durations. Very short source vowels use cascaded bounded stretches because
Praat limits individual duration factors. The synthetic sound is part of this
demo’s aesthetic; a vocalist can use the supplied lyrics and MIDI for a human
recording.

Serve the player locally with byte-range support for reliable audio seeking:

```powershell
& './outputs/textbook-pop-song/.venv/Scripts/python.exe' tools/textbook-pop-song/serve.py
```

Open `http://127.0.0.1:8787/preview.html`. The server binds only to localhost.

## Checks and source grounding

Source anchors point to the textbook’s introduction, Boolean admission, BM25,
embeddings, retrieval/generation distinction, and library practice sections.
The chorus includes the book’s short title. The bridge emphasizes that real
citations do not establish what was missed, and asks listeners to inspect the
working set. The imagery is metaphorical, not a claim about a named product.

Production checks every phrase’s beat count and notes, aligns every lyric word
with the source speech, checks non-overlapping timed lyric lines, measures the
actual sung pitch against the written tune, rejects clipping and non-finite
samples, and fully decodes both WAV/MP3 mixes. Each phrase must have median pitch
error under 65 cents and over 65% of measured voiced frames within a semitone;
transition frames are excluded. An independent MIDI parser checks every track,
note pair and end marker, rejecting hanging or overlapping same-pitch notes.
Export mastering targets −14 LUFS and −2 dBTP.
Verification requires −15 to −13 LUFS, at most −1 dBTP, stereo at 44.1 kHz, and
duration within 150 ms of the composition. Automated checks establish tuning
and export integrity, not human-level vocal quality or lyric intelligibility.

The lyrics, melody and arrangement are new companion material. Textbook topic
credit goes to Aaron Tay; its CC BY 4.0 terms continue to apply to textbook
material. The generated player identifies the synthetic voice and demo status.
