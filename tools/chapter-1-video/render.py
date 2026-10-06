"""Render a narration-led Chapter 1 explainer and verify the resulting MP4."""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import wave

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NAME = "chapter-1-the-retrieval-problem"
FPS, W, H, SR = 30, 1920, 1080, 48000

# Reuse the book's existing, independently editable speech/cache implementation.
spec = importlib.util.spec_from_file_location("chapter_voice", HERE.parent / "pick-a-card" / "narrate.py")
voice = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = voice
spec.loader.exec_module(voice)


def run(cmd, log):
    result = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    log.write_text(result.stdout + result.stderr, encoding="utf-8")
    if result.returncode:
        raise RuntimeError(f"Command failed: see {log}")
    return result.stderr


def check_source(script):
    source = ROOT / "search-textbook.html"
    book = source.read_text(encoding="utf-8")
    chapter = book.split('<section class="chapter" id="sec-intro">', 1)[1].split('<section class="chapter"', 1)[0]
    for scene in script["scenes"]:
        if scene["source_anchor"] != "sec-intro":
            assert f'id="{scene["source_anchor"]}"' in chapter, scene["source_anchor"]
    for evidence in ["up to 30", "top five", "35,300", "9.4 million", "13 results", "1,000", "September 2026", "August 2026"]:
        assert evidence in chapter, f"Recheck script against changed source: {evidence}"
    relevance = chapter.split('<h3 id="what-does-relevant-actually-mean">', 1)[1].split('<aside class="orientation"', 1)[0]
    relevance_text = " ".join(html.unescape(re.sub(r"<[^>]+>", "", relevance)).split()).casefold()
    for phrase in script["relevance_source_phrases"]:
        assert phrase.casefold() in relevance_text, f"Recheck relevance adaptation against changed source: {phrase}"
    return {"source": script["source"], "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "relevance_source_sha256": hashlib.sha256(relevance.encode("utf-8")).hexdigest(),
            "script_sha256": hashlib.sha256((HERE / "script.json").read_bytes()).hexdigest()}


def write_wave(path, samples):
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(2)
        wav.setsampwidth(2)
        wav.setframerate(SR)
        samples = np.clip(samples, -1, 1)
        wav.writeframes((np.repeat(samples[:, None], 2, axis=1) * 32767).astype("<i2").tobytes())


def prepare(script, out, ff):
    source = check_source(script)
    tl = voice.build(script, out, ff)
    # Round upward to a complete picture frame; preserve the final quiet hold.
    duration = math.ceil(tl.duration * FPS) / FPS
    timeline = {"duration": duration, "scenes": tl.scenes,
                "takes": [{"id": tk.id, "scene": tk.scene, "text": tk.text, "start": tk.start,
                           "end": tk.end, "words": tk.words} for tk in tl.takes], **source}
    timeline["scenes"] = {name: list(bounds) for name, bounds in tl.scenes.items()}
    timeline["scenes"][script["scenes"][-1]["id"]][1] = duration
    (out / "timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    track = voice.voice_track(tl)
    track = np.pad(track, (0, int(round(duration * SR)) - len(track)))
    write_wave(out / "narration-unmastered.wav", track)
    run([ff, "-y", "-i", str(out / "narration-unmastered.wav"), "-af",
         "loudnorm=I=-16:TP=-2.5:LRA=9", "-ar", str(SR), str(out / "narration.wav")], out / "mastering.log")
    cues = voice.captions(tl)
    for cue in cues:
        assert isinstance(cue["start"], (int, float)) and 0 <= cue["start"] < cue["end"] <= duration
    for a, b in zip(cues, cues[1:]):
        assert a["end"] <= b["start"], "overlapping captions"
    (out / "captions.json").write_text(json.dumps(cues, indent=2), encoding="utf-8")
    srt = [f"{i}\n{voice.stamp(c['start'], ',')} --> {voice.stamp(c['end'], ',')}\n{c['text']}\n"
           for i, c in enumerate(cues, 1)]
    vtt = ["WEBVTT\n"] + [f"{voice.stamp(c['start'], '.')} --> {voice.stamp(c['end'], '.')}\n{c['text']}\n" for c in cues]
    (out / f"{NAME}.srt").write_text("\n".join(srt), encoding="utf-8")
    (out / f"{NAME}.vtt").write_text("\n".join(vtt), encoding="utf-8")
    transcript = "\n\n".join(f"[{voice.stamp(tk.start, '.')}] {tk.text}" for tk in tl.takes)
    (out / "transcript.txt").write_text(f"{script['title']} — Chapter 1\n\n{transcript}\n\n"
        f"Adapted from Aaron Tay, How Search Decides What You See (v1.2.1), Chapter 1.\n{script['book_url']}\n"
        f"CC BY 4.0; adaptation with original geometric animations.\n"
        f"Synthetic narrator: Microsoft {script['voice']['name']} via edge-tts. No voice cloning.\n", encoding="utf-8")
    print(f"Timeline ready: {duration:.2f}s, {len(tl.takes)} voice takes, {len(cues)} captions", flush=True)
    return timeline


def picture_surface():
    import skia
    return skia.Surface.MakeRaster(skia.ImageInfo.Make(W, H, skia.kRGBA_F16_ColorType, skia.kPremul_AlphaType))


def read_picture(surface, buffer):
    import skia
    assert surface.readPixels(skia.ImageInfo.Make(W, H, skia.kBGRA_8888_ColorType, skia.kPremul_AlphaType), buffer, W * 4)
    return buffer


def worker(job):
    from scenes import Film
    film = Film(job["timeline"], job["script"])
    surface = picture_surface()
    buffer = np.empty((H, W, 4), np.uint8)
    cmd = [job["ff"], "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
           "-r", str(FPS), "-i", "-", "-an", "-c:v", "libx264", "-preset", "fast", "-crf", "18",
           "-tune", "animation", "-pix_fmt", "yuv420p", "-threads", "2", "-g", "60", job["segment"]]
    with subprocess.Popen(cmd, stdin=subprocess.PIPE) as proc:
        try:
            for frame in range(job["first"], job["last"]):
                film.frame(surface.getCanvas(), frame / FPS)
                proc.stdin.write(read_picture(surface, buffer).tobytes())
        finally:
            proc.stdin.close()
        if proc.wait():
            raise RuntimeError("frame encoder failed")


def render(timeline, script, out, ff, workers):
    total = round(timeline["duration"] * FPS)
    segments = out / "segments"
    segments.mkdir(exist_ok=True)
    bounds = np.linspace(0, total, workers * 2 + 1).round().astype(int)
    jobs = []
    for i, (first, last) in enumerate(zip(bounds, bounds[1:])):
        job = {"timeline": timeline, "script": script, "first": int(first), "last": int(last),
               "ff": ff, "segment": str(segments / f"part-{i:03d}.mp4")}
        path = segments / f"job-{i:03d}.json"
        path.write_text(json.dumps(job), encoding="utf-8")
        jobs.append(path)
    pending, running, done = list(enumerate(jobs)), [], 0
    start = time.monotonic()
    print(f"Rendering {total:,} frames in {workers} worker processes", flush=True)
    try:
        while pending or running:
            while pending and len(running) < workers:
                i, path = pending.pop(0)
                log = (segments / f"worker-{i:03d}.log").open("w", encoding="utf-8")
                proc = subprocess.Popen([sys.executable, str(HERE / "render.py"), "--worker", str(path)],
                                        stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT)
                running.append((i, proc, log))
            time.sleep(0.5)
            for i, proc, log in list(running):
                if proc.poll() is None:
                    continue
                log.close()
                running.remove((i, proc, log))
                if proc.returncode:
                    raise RuntimeError(f"Frame worker failed; see {segments / f'worker-{i:03d}.log'}")
                done += 1
                print(f"  {done}/{len(jobs)} chunks complete, {time.monotonic() - start:.0f}s", flush=True)
    finally:
        for _, proc, log in running:
            proc.terminate()
            proc.wait()
            log.close()
    listing = segments / "concat.txt"
    listing.write_text("".join(f"file 'part-{i:03d}.mp4'\n" for i in range(len(jobs))), encoding="utf-8")
    run([ff, "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy",
         str(out / "picture.mp4")], out / "concat.log")


def stills(timeline, script, out):
    from scenes import Film
    film = Film(timeline, script)
    surface = picture_surface()
    buffer = np.empty((H, W, 4), np.uint8)
    frames = out / "stills"
    frames.mkdir(exist_ok=True)
    samples = []
    for scene in script["scenes"]:
        a, b = timeline["scenes"][scene["id"]]
        samples.extend((scene["id"], a + (b - a) * ratio) for ratio in (0.22, 0.6, 0.88))
    sheet = Image.new("RGB", (1600, math.ceil(len(samples) / 4) * 249), "#090c13")
    d = ImageDraw.Draw(sheet)
    for i, (name, at) in enumerate(samples):
        film.frame(surface.getCanvas(), at)
        read_picture(surface, buffer)
        im = Image.fromarray(buffer[..., [2, 1, 0]])
        im.save(frames / f"{i:02d}-{name}.jpg", quality=92)
        x, y = (i % 4) * 400, (i // 4) * 249
        sheet.paste(im.resize((400, 225), Image.Resampling.LANCZOS), (x, y))
        d.text((x + 8, y + 230), f"{at:6.1f}s  {name}", fill="#b0becf")
    sheet.save(out / "contact-sheet.jpg", quality=93)
    film.poster(surface.getCanvas())
    read_picture(surface, buffer)
    Image.fromarray(buffer[..., [2, 1, 0]]).save(out / "poster.jpg", quality=95)
    print("Review stills and contact sheet ready", flush=True)


def mux(timeline, script, out, ff):
    dest = out / f"{NAME}.mp4"
    temp = out / f"{NAME}.partial.mp4"
    run([ff, "-y", "-i", str(out / "picture.mp4"), "-i", str(out / "narration.wav"),
         "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-ar", str(SR), "-t", str(timeline["duration"]), "-metadata", f"title={script['title']} — Chapter 1",
         "-metadata", "artist=Aaron Tay", "-metadata:s:a:0", "language=eng",
         "-movflags", "+faststart", str(temp)], out / "mux.log")
    info = verify(temp, timeline, out, ff)
    temp.replace(dest)
    info["file"] = dest.name
    (out / "verification.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    return dest


def verify(path, timeline, out, ff):
    # Decode both streams completely; corrupt packets make the command fail.
    decode = run([ff, "-hide_banner", "-xerror", "-i", str(path), "-map", "0:v:0", "-map", "0:a:0",
                  "-f", "null", "-"], out / "decode.log")
    loud = run([ff, "-hide_banner", "-i", str(path), "-map", "0:a:0", "-af", "ebur128=peak=true",
                "-f", "null", "-"], out / "loudness.log")
    count = int(re.findall(r"frame=\s*(\d+)", decode)[-1])
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", loud)[-1])
    peak = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", loud)[-1])
    video = re.findall(r"Video: (h264[^\n]*)", decode)[0]
    audio = re.findall(r"Audio: (aac[^\n]*)", decode)[0]
    assert f"{W}x{H}" in video and "30 fps" in video and "yuv420p" in video, video
    assert "48000 Hz" in audio and "stereo" in audio, audio
    assert count == round(timeline["duration"] * FPS), f"frame count: {count}"
    assert -17 <= lufs <= -15, f"loudness: {lufs}"
    assert peak <= -1, f"true peak: {peak}"
    atoms = []
    digest = hashlib.sha256()
    with path.open("rb") as f:
        while header := f.read(8):
            size = int.from_bytes(header[:4], "big")
            atoms.append(header[4:8].decode("ascii"))
            if size == 1:
                size = int.from_bytes(f.read(8), "big")
                f.seek(size - 16, 1)
            elif size >= 8:
                f.seek(size - 8, 1)
            else:
                break
        f.seek(0)
        while data := f.read(1024 * 1024):
            digest.update(data)
    assert atoms.index("moov") < atoms.index("mdat"), "missing faststart"
    info = {"file": path.name, "width": W, "height": H, "fps": FPS, "duration_seconds": timeline["duration"],
            "decoded_frames": count, "integrated_lufs": lufs, "true_peak_dbfs": peak, "video": video,
            "audio": audio, "faststart": True, "sha256": digest.hexdigest(), "bytes": path.stat().st_size,
            "source_sha256": timeline["source_sha256"], "relevance_source_sha256": timeline["relevance_source_sha256"],
            "script_sha256": timeline["script_sha256"], "passed": True}
    print(f"Verified {count:,} frames; {lufs:.1f} LUFS, {peak:.1f} dBTP; H.264/AAC, faststart", flush=True)
    return info


def preview(timeline, script, out):
    chapters = []
    for i, scene in enumerate(script["scenes"], 1):
        a, b = timeline["scenes"][scene["id"]]
        chapters.append(f"{i}\n{voice.stamp(a, '.')} --> {voice.stamp(b, '.')}\n{scene['title']}\n")
    (out / "chapters.vtt").write_text("WEBVTT\n\n" + "\n".join(chapters), encoding="utf-8")
    chapter_buttons = "\n".join(f'<button data-time="{timeline["scenes"][s["id"]][0]:.3f}">'
        f'<span>{voice.stamp(timeline["scenes"][s["id"]][0], ".")[3:8]}</span>{s["title"]}</button>' for s in script["scenes"])
    (out / "preview.html").write_text(f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter 1 · The retrieval problem</title>
<style>
*{{box-sizing:border-box}}body{{margin:0;background:#090c13;color:#e7edf5;font:16px/1.6 system-ui}}
main{{max-width:1280px;margin:auto;padding:36px 28px}}.eyebrow{{color:#59c8b7;letter-spacing:.2em;font-size:12px}}
h1{{font:44px/1.2 Georgia,serif;margin:12px 0}}p{{color:#b0becf}}video{{width:100%;background:#090c13;border:1px solid #283646;border-radius:12px}}
a{{color:#74c7eb}}nav{{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));gap:8px;margin:24px 0}}
button{{text-align:left;padding:12px;background:#101722;border:1px solid #283646;border-radius:6px;color:#dbe5ef;cursor:pointer}}
button:hover,button:focus-visible{{border-color:#59c8b7}}button span{{color:#59c8b7;margin-right:14px;font-variant-numeric:tabular-nums}}
.credit{{font-size:13px}}@media(max-width:600px){{main{{padding:20px 12px}}h1{{font-size:32px}}}}
</style><main><div class="eyebrow">HOW SEARCH DECIDES WHAT YOU SEE · CHAPTER 1</div>
<h1>The retrieval problem</h1><p>What decided which papers your AI answer could cite?</p>
<video id="film" controls playsinline preload="metadata" poster="poster.jpg" src="{NAME}.mp4">
<track kind="captions" src="{NAME}.vtt" srclang="en" label="English">
<track kind="chapters" src="chapters.vtt" srclang="en" label="Chapters">
</video><nav aria-label="Jump to a scene">{chapter_buttons}</nav>
<p><a href="{NAME}.mp4" download>Download MP4</a> · <a href="{NAME}.srt" download>SRT captions</a> · <a href="transcript.txt">Transcript</a> · <a href="{script['book_url']}">Read Chapter 1</a></p>
<p class="credit">Adapted from Aaron Tay's <em>How Search Decides What You See</em>, v1.2.1, Chapter 1 (CC BY 4.0).
Original geometric animation inspired by the visual teaching approach of 3Blue1Brown; independently produced.
Synthetic narrator: Microsoft Andrew Multilingual. Product examples retain the dates reported in the chapter.
The paper tokens and sets are teaching illustrations.</p></main>
<script>const film=document.getElementById('film');document.querySelectorAll('button[data-time]').forEach(b=>b.onclick=()=>{{film.currentTime=Number(b.dataset.time);film.play().catch(()=>{{}})}});</script></html>''', encoding="utf-8")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--output", type=Path, default=ROOT / "outputs" / "chapter-1-video")
    ap.add_argument("--prepare-only", action="store_true")
    ap.add_argument("--stills-only", action="store_true")
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--workers", type=int, default=min(6, max(1, (os.cpu_count() or 2) - 2)))
    ap.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.worker:
        worker(json.loads(args.worker.read_text(encoding="utf-8")))
        return
    assert 1 <= args.workers <= 8
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    ff = os.environ.get("CHAPTER_FFMPEG") or imageio_ffmpeg.get_ffmpeg_exe()
    script = json.loads((HERE / "script.json").read_text(encoding="utf-8"))
    if args.verify_only or args.stills_only:
        timeline = json.loads((out / "timeline.json").read_text(encoding="utf-8"))
    else:
        timeline = prepare(script, out, ff)
    if args.verify_only:
        info = verify(out / f"{NAME}.mp4", timeline, out, ff)
        (out / "verification.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
        return
    if args.prepare_only:
        return
    stills(timeline, script, out)
    if args.stills_only:
        preview(timeline, script, out)
        return
    render(timeline, script, out, ff, args.workers)
    dest = mux(timeline, script, out, ff)
    preview(timeline, script, out)
    print(f"Completed: {dest}", flush=True)


if __name__ == "__main__":
    main()
