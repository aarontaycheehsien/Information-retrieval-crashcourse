"""Render three original vector explainers adapted from Chapter 2.

Speech sets the scene durations; no speech is cut or time-stretched. All generated
media and caches stay under outputs/chapter-2-videos, which is Git-ignored.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import math
import re
import subprocess
import sys
import time
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import skia
import imageio_ffmpeg

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
# Reuse the repository's narration cache, audio trimming and word-timed captions.
sys.path.insert(0, str(ROOT / "tools" / "pick-a-card"))
import narrate  # noqa: E402
sys.path.insert(0, str(HERE))
from visuals import Film, W, H, RECORDS, caption, surface_pixels  # noqa: E402

FPS = 30
DEFAULT_OUT = ROOT / "outputs" / "chapter-2-videos"


def read_config():
    cfg = json.loads((HERE / "episodes.json").read_text(encoding="utf-8"))
    source = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
    start = source.index('id="sec-boolean-admission"')
    end = source.index('id="sec-bm25-ranking"', start)
    chapter = source[start:end]
    for required in ("Boolean admission and the inverted index", "Chapter 2", "D1", "D4", "Posting list", "lemmatisation"):
        assert required in chapter, f"Chapter source changed: missing {required}"
    plain = html.unescape(re.sub(r"<[^>]+>", " ", chapter))
    plain = re.sub(r"\s+", " ", plain)
    for ident, value in RECORDS.items():
        assert value in plain, f"Chapter example changed: {ident}"
    posting = lambda term: {ident for ident, value in RECORDS.items() if term in value.lower().split()}
    d, j, i, u = (posting(term) for term in ("delulu", "job", "interview", "unrealistic"))
    assert d & j == {"D1", "D4"}
    assert d | u == {"D1", "D3", "D4"}
    assert d - i == {"D4"}
    assert d & i == {"D1"}
    assert d | i == {"D1", "D2", "D4"}
    assert len(cfg["episodes"]) == 3
    for e in cfg["episodes"]:
        assert len(e["scenes"]) == 8
        assert len({s["id"] for s in e["scenes"]}) == 8
    cfg["source_sha256"] = hashlib.sha256(chapter.encode()).hexdigest()
    return cfg


def command(args, log):
    p = subprocess.run(args, capture_output=True, text=True, encoding="utf-8", errors="replace")
    log.write_text(p.stdout + p.stderr, encoding="utf-8")
    if p.returncode:
        raise RuntimeError(f"Command failed: {log}")
    return p.stdout + p.stderr


def write_wav(path, audio):
    data = np.round(np.clip(audio, -0.999, 0.999) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2 if data.ndim == 2 else 1)
        w.setsampwidth(2)
        w.setframerate(narrate.SR)
        w.writeframes(data.tobytes())


def music_track(duration, tl):
    """Original quiet marimba-like arpeggio, soft pad and transition chimes."""
    sr = narrate.SR
    n = int(round(duration * sr))
    music = np.zeros((n, 2), dtype=np.float32)
    # Harmonic loop in C major; fixed seed and no recorded samples.
    chords = [(48, 55, 60, 64), (45, 52, 57, 60), (41, 48, 53, 57), (43, 50, 55, 59)]
    def add(at, sig, gain, pan=0):
        i = int(round(at * sr))
        if i >= n:
            return
        sig = sig[:n-i]
        angle = (pan + 1) * math.pi / 4
        music[i:i+len(sig), 0] += sig * gain * math.cos(angle)
        music[i:i+len(sig), 1] += sig * gain * math.sin(angle)
    for k, at in enumerate(np.arange(0.0, duration, 0.75)):
        chord = chords[(k // 16) % 4]
        midi = chord[k % 4] + 12
        f = 440 * 2 ** ((midi - 69) / 12)
        tt = np.arange(int(sr * 1.4), dtype=np.float32) / sr
        env = np.minimum(1, tt / 0.012) * np.exp(-tt * 4.5)
        tone = (np.sin(2 * np.pi * f * tt) + 0.25 * np.sin(2 * np.pi * 2*f * tt)) * env
        add(float(at), tone, 0.022, (-0.35, 0.35)[k % 2])
    for k, (start, _) in enumerate(tl.scenes.values()):
        tt = np.arange(int(sr * 0.8), dtype=np.float32) / sr
        env = np.minimum(1, tt / 0.02) * np.exp(-tt * 6)
        for f in (523.25, 659.25, 783.99):
            add(start + 0.12, np.sin(2*np.pi*f*tt)*env, 0.011, 0)
    # Smooth ducking retains a bed in scene pauses and suppresses it under speech.
    gain = np.ones(n, dtype=np.float32)
    for take in tl.takes:
        a, b = max(0, int((take.start - 0.15)*sr)), min(n, int((take.end + 0.2)*sr))
        gain[a:b] = 0.34
    gain = np.convolve(gain[::480], np.ones(15)/15, mode="same")
    gain = np.interp(np.arange(n), np.arange(len(gain))*480, gain).astype(np.float32)
    fade = int(0.8*sr)
    gain[:fade] *= np.linspace(0, 1, fade)
    gain[-fade:] *= np.linspace(1, 0, fade)
    return music * gain[:, None] * 4.0


def prepare(cfg, episode, out, ff):
    folder = out / episode["id"]
    folder.mkdir(parents=True, exist_ok=True)
    script = {"voice": cfg["voice"], "lead_in": 0.75, "tail": 2.8,
              "lines": [{"id": s["id"], "scene": s["id"], "text": s["narration"], "gap": 0.8}
                        for s in episode["scenes"]]}
    tl = narrate.build(script, folder, ff)
    cues = narrate.captions(tl)
    assert all(0 <= c["start"] < c["end"] <= tl.duration for c in cues)
    timeline = {"duration": tl.duration, "scenes": tl.scenes, "cues": cues,
                "takes": [{"id": t.id, "start": t.start, "end": t.end, "words": t.words, "cache_key": t.cache_key}
                          for t in tl.takes], "voice": cfg["voice"], "source_sha256": cfg["source_sha256"]}
    (folder / "timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    srt = [f"{i}\n{narrate.stamp(c['start'], ',')} --> {narrate.stamp(c['end'], ',')}\n{c['text']}\n" for i, c in enumerate(cues, 1)]
    (folder / "captions.srt").write_text("\n".join(srt), encoding="utf-8")
    (folder / "captions.vtt").write_text("WEBVTT\n\n" + "\n".join(
        f"{narrate.stamp(c['start'], '.')} --> {narrate.stamp(c['end'], '.')}\n{c['text']}\n" for c in cues), encoding="utf-8")
    transcript = "\n\n".join(s["title"] + "\n" + s["narration"] for s in episode["scenes"])
    (folder / "transcript.txt").write_text(episode["title"] + "\n\n" + transcript +
        f"\n\nAdapted from Chapter {cfg['chapter']}, {cfg['book']}, by {cfg['author']}.\nSynthetic voice: {cfg['voice']['name']}.\n", encoding="utf-8")
    frames = math.ceil(tl.duration * FPS)
    duration = frames / FPS
    voice = narrate.voice_track(tl).astype(np.float32)
    voice = np.pad(voice, (0, int(round(duration*narrate.SR))-len(voice)))
    music = music_track(duration, tl)
    margins = []
    for take in tl.takes:
        a, b = int(round(take.start*narrate.SR)), int(round(take.end*narrate.SR))
        vrms = float(np.sqrt(np.mean(voice[a:b]**2)))
        mrms = float(np.sqrt(np.mean(music[a:b]**2)))
        margins.append(20*math.log10(vrms/max(mrms, 1e-9)))
    assert min(margins) >= 10, "Music obscures a narration take"
    (folder / "mix-balance.json").write_text(json.dumps({"worst_voice_over_music_db": round(min(margins), 2),
        "take_margins_db": dict(zip((t.id for t in tl.takes), (round(m, 2) for m in margins)))}, indent=2), encoding="utf-8")
    mix = music + voice[:, None]
    write_wav(folder / "voice.wav", voice)
    write_wav(folder / "music.wav", music)
    write_wav(folder / "mix.wav", mix)
    log = command([ff, "-hide_banner", "-i", str(folder / "mix.wav"), "-af",
                   "loudnorm=I=-16:TP=-2.5:LRA=11:print_format=json", "-f", "null", "-"], folder / "loudness-analysis.log")
    m = json.loads(re.findall(r'\{\s*"input_i"[\s\S]*?\}', log)[-1])
    filt = (f"loudnorm=I=-16:TP=-2.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    command([ff, "-y", "-v", "error", "-i", str(folder / "mix.wav"), "-af", filt,
             "-ar", "48000", "-c:a", "pcm_s16le", str(folder / "soundtrack.wav")], folder / "master.log")
    print(f"Prepared {episode['id']}: {tl.duration:.2f}s, {len(cues)} caption cues", flush=True)
    return timeline


def load_timeline(out, episode):
    return json.loads((out / episode["id"] / "timeline.json").read_text(encoding="utf-8"))


def draw_frame(film, surface, t, cues=True, buffer=None):
    c = surface.getCanvas()
    film.draw(c, t)
    if cues:
        caption(c, film.timeline["cues"], t)
    if buffer is not None:
        info = skia.ImageInfo.Make(W, H, skia.kBGRA_8888_ColorType, skia.kPremul_AlphaType)
        assert surface.readPixels(info, buffer, W*4)
        return buffer
    return surface_pixels(surface)


def reviews(episode, timeline, out, film_class=Film):
    folder = out / episode["id"]
    film = film_class(episode, timeline)
    surface = skia.Surface(W, H)
    images = []
    for i, (name, (a, b)) in enumerate(timeline["scenes"].items()):
        t = a + (b-a) * 0.52
        pix = draw_frame(film, surface, t)
        im = Image.fromarray(pix[:, :, :3], "RGB")
        im.save(folder / f"scene-{i+1:02d}-{name}.jpg", quality=92)
        images.append(im.resize((640, 360), Image.Resampling.LANCZOS))
    sheet = Image.new("RGB", (1280, 4*396), "#101833")
    d = ImageDraw.Draw(sheet)
    f = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 19)
    for i, im in enumerate(images):
        x, y = (i % 2)*640, (i // 2)*396
        sheet.paste(im, (x, y))
        d.text((x+12, y+367), f"{i+1:02d}  {episode['scenes'][i]['title']}", font=f, fill="white")
    sheet.save(folder / "contact-sheet.jpg", quality=92)
    pix = draw_frame(film, surface, 3.0, cues=False)
    Image.fromarray(pix[:, :, :3], "RGB").save(folder / "poster.jpg", quality=94)


def render(episode, timeline, out, ff, film_class=Film):
    folder = out / episode["id"]
    film = film_class(episode, timeline)
    # Native BGRA readback avoids per-frame snapshot conversion and copying.
    info = skia.ImageInfo.Make(W, H, skia.kBGRA_8888_ColorType, skia.kPremul_AlphaType)
    surface = skia.Surface.MakeRaster(info)
    buffer = np.empty((H, W, 4), dtype=np.uint8)
    n = math.ceil(timeline["duration"] * FPS)
    args = [ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
            "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "19",
            "-tune", "animation", "-pix_fmt", "yuv420p", "-threads", "3", str(folder / "picture.mp4")]
    started = time.monotonic()
    with (folder / "encode.log").open("wb") as err:
        p = subprocess.Popen(args, stdin=subprocess.PIPE, stderr=err)
        try:
            for frame in range(n):
                pixels = draw_frame(film, surface, frame / FPS, buffer=buffer)
                p.stdin.write(memoryview(pixels))
                if frame % 900 == 0:
                    print(f"{episode['id']}: {frame}/{n} frames ({time.monotonic()-started:.0f}s)", flush=True)
            p.stdin.close()
            assert p.wait() == 0, "picture encoder failed"
        except BaseException:
            p.kill()
            p.wait()
            raise
    mux(episode, timeline, out, ff)


def mux(episode, timeline, out, ff):
    folder = out / episode["id"]
    n = math.ceil(timeline["duration"] * FPS)
    target = folder / (episode["id"] + ".mp4")
    command([ff, "-y", "-v", "error", "-i", str(folder / "picture.mp4"), "-i", str(folder / "soundtrack.wav"),
             "-i", str(folder / "captions.srt"), "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "copy",
             "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text", "-disposition:s:0", "0", "-metadata:s:s:0", "language=eng",
             "-metadata", "title=" + episode["title"], "-metadata", f"comment=Original animation; synthetic narration; adapted from Chapter {episode.get('chapter', 2)} by Aaron Tay",
             "-t", str(n/FPS), "-movflags", "+faststart", str(target)], folder / "mux.log")
    print(f"Exported {target.name}", flush=True)


def verify(episode, timeline, out, ff):
    folder = out / episode["id"]
    target = folder / (episode["id"] + ".mp4")
    log = command([ff, "-hide_banner", "-i", str(target), "-map", "0:v", "-map", "0:a", "-af",
                   "loudnorm=I=-16:TP=-2.5:LRA=11:print_format=json", "-progress", "pipe:1", "-f", "null", "-"], folder / "verify.log")
    measurements = json.loads(re.findall(r'\{\s*"input_i"[\s\S]*?\}', log)[-1])
    frames = int(re.findall(r"^frame=(\d+)", log, re.MULTILINE)[-1])
    n = math.ceil(timeline["duration"]*FPS)
    assert frames == n, (frames, n)
    assert abs(float(measurements["input_i"])+16) <= 1, measurements
    assert float(measurements["input_tp"]) <= -1.0, measurements
    assert "1920x1080" in log and "30 fps" in log and "h264" in log and "aac" in log and "mov_text" in log
    # Inspect top-level MP4 atoms, not accidental byte substrings inside media.
    atoms = []
    with target.open("rb") as stream:
        while (head := stream.read(8)):
            assert len(head) == 8
            size, kind = int.from_bytes(head[:4], "big"), head[4:].decode("ascii", errors="replace")
            if size == 1:
                size = int.from_bytes(stream.read(8), "big")
                skip = size - 16
            else:
                skip = size - 8
            atoms.append(kind)
            if size == 0:
                break
            assert skip >= 0
            stream.seek(skip, 1)
    assert atoms.index("moov") < atoms.index("mdat"), atoms
    # Verify that embedded subtitles retain the exact ordered caption text.
    extracted = folder / "embedded-captions.srt"
    command([ff, "-y", "-v", "error", "-i", str(target), "-map", "0:s:0", str(extracted)], folder / "subtitle-check.log")
    texts = [line.strip() for line in extracted.read_text(encoding="utf-8").splitlines()
             if line.strip() and not line.isdigit() and "-->" not in line]
    assert texts == [c["text"] for c in timeline["cues"]]
    with target.open("rb") as handle:
        digest = hashlib.file_digest(handle, "sha256").hexdigest()
    report = {"file": target.name, "duration": n/FPS, "size_mb": round(target.stat().st_size/1e6, 2),
              "dimensions": [W, H], "fps": FPS, "decoded_frames": frames, "full_decode": "passed",
              "integrated_lufs": float(measurements["input_i"]), "true_peak_dbtp": float(measurements["input_tp"]),
              "caption_cues": len(texts), "embedded_captions": "passed", "fast_start": True,
              "sha256": digest,
              "source_sha256": timeline["source_sha256"]}
    (folder / "verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report), flush=True)
    return report


def preview(cfg, out):
    cards = []
    for e in cfg["episodes"]:
        timeline = load_timeline(out, e)
        relative = e["id"] + "/"
        duration = int(round(timeline["duration"]))
        cards.append(f'''<article><div class="episode">CHAPTER 2 · FILM {len(cards)+1:02d} · {duration//60}:{duration%60:02d}</div>
<h2>{html.escape(e['title'])}</h2><p>{html.escape(e['subtitle'])}</p>
<video controls preload="metadata" poster="{relative}poster.jpg"><source src="{relative}{e['id']}.mp4" type="video/mp4"></video>
<nav><a href="{relative}{e['id']}.mp4" download>Download MP4</a><a href="{relative}captions.srt" download>Captions</a><a href="{relative}transcript.txt">Transcript</a><a href="{relative}contact-sheet.jpg">Storyboard</a></nav></article>''')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter 2 — Animated explainers</title><style>body{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}main{max-width:1080px;margin:auto;padding:48px 24px}h1{font-size:clamp(36px,6vw,64px);line-height:1.1;margin:12px 0}h2{font-size:32px;margin:8px 0}.lead{color:#adbcd7;max-width:750px}.kicker,.episode{letter-spacing:.16em;color:#68e0bb;font-size:13px;font-weight:700}article{margin:40px 0;padding:28px;background:#192344;border-radius:24px}article p{margin:0 0 20px;color:#adbcd7}video{width:100%;border-radius:16px;background:#101833;display:block}nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}a{color:#68e0bb}footer{font-size:15px;color:#adbcd7}summary{cursor:pointer}</style>
<main><div class="kicker">HOW SEARCH DECIDES WHAT YOU SEE</div><h1>The gates, the words,<br>and the map.</h1><p class="lead">Three original animated explainers adapted from Chapter 2: Boolean admission and the inverted index, by Aaron Tay. English synthetic narration, original vector illustrations and music, and captions.</p>'''
    page += "".join(cards)
    page += '''<footer><p>Source: <a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#boolean-admission">Read Chapter 2</a>. Analysis steps and field rules are illustrative; check the database you use.</p></footer></main></html>'''
    (out / "preview.html").write_text(page, encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--episode", choices=["1", "2", "3", "all"], default="all")
    p.add_argument("--output", type=Path, default=DEFAULT_OUT)
    p.add_argument("--prepare-only", action="store_true")
    p.add_argument("--stills-only", action="store_true")
    p.add_argument("--render-only", action="store_true")
    p.add_argument("--verify-only", action="store_true")
    args = p.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    cfg = read_config()
    ff = imageio_ffmpeg.get_ffmpeg_exe()
    selected = cfg["episodes"] if args.episode == "all" else [cfg["episodes"][int(args.episode)-1]]
    for episode in selected:
        if args.render_only or args.verify_only or args.stills_only:
            timeline = load_timeline(out, episode)
        else:
            timeline = prepare(cfg, episode, out, ff)
        if not args.verify_only:
            reviews(episode, timeline, out)
        if not (args.prepare_only or args.stills_only or args.verify_only):
            render(episode, timeline, out, ff)
        if not (args.prepare_only or args.stills_only):
            verify(episode, timeline, out, ff)
    if all((out / e["id"] / "timeline.json").is_file() for e in cfg["episodes"]):
        preview(cfg, out)


if __name__ == "__main__":
    main()
