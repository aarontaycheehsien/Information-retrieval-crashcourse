"""Produce the original investigation-style Chapter 1 film using the media engine."""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import math
import os
from pathlib import Path
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NAME = "chapter-1-the-paper-your-ai-never-saw"
OUTPUT = ROOT / "outputs" / "chapter-1-investigation"
spec = importlib.util.spec_from_file_location("investigation_media", HERE.parent / "chapter-1-video" / "render.py")
media = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = media
spec.loader.exec_module(media)
media.HERE, media.NAME = HERE, NAME


def picture_surface():
    import skia
    return skia.Surface(media.W, media.H)


media.picture_surface = picture_surface


def worker(job):
    """Bound encoder memory and avoid copying an entire pixel buffer per frame."""
    import numpy as np
    from scenes import Film
    film = Film(job["timeline"], job["script"])
    surface = picture_surface()
    buffer = np.empty((media.H, media.W, 4), np.uint8)
    command = [job["ff"], "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
               "-s", "1920x1080", "-r", "30", "-i", "-", "-an", "-c:v", "libx264",
               "-preset", "veryfast", "-crf", "18", "-tune", "zerolatency",
               "-pix_fmt", "yuv420p", "-threads", "1", "-g", "60", job["segment"]]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as process:
        try:
            for frame in range(job["first"], job["last"]):
                film.frame(surface.getCanvas(), frame / media.FPS)
                media.read_picture(surface, buffer)
                process.stdin.write(memoryview(buffer).cast("B"))
        finally:
            process.stdin.close()
        if process.wait():
            raise RuntimeError("Frame encoder failed")


media.worker = worker


def production_hash():
    digest = hashlib.sha256()
    for path in [HERE / "script.json", HERE / "scenes.py", HERE / "render.py",
                 HERE.parent / "chapter-1-video" / "render.py", HERE.parent / "pick-a-card" / "narrate.py"]:
        digest.update(path.name.encode())
        digest.update(path.read_bytes())
    return digest.hexdigest()


def config():
    return json.loads((HERE / "script.json").read_text(encoding="utf-8"))


def seed_cache(script, out):
    previous = ROOT / "outputs" / "chapter-1-video"
    for line in script["lines"]:
        request = media.voice.request_for(line, script["voice"])
        src, dst = media.voice.cache_dir(previous, request), media.voice.cache_dir(out, request)
        if src.is_dir() and not dst.exists():
            shutil.copytree(src, dst)


def prepare(script, out, ff):
    seed_cache(script, out)
    timeline = media.prepare(script, out, ff)
    timeline["production_sha256"] = production_hash()
    (out / "timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    return timeline


def load_timeline(out, script):
    timeline = json.loads((out / "timeline.json").read_text(encoding="utf-8"))
    current = media.check_source(script)
    for key in ["source_sha256", "script_sha256"]:
        assert timeline[key] == current[key], f"Stale timeline: {key}; prepare again"
    assert timeline["production_sha256"] == production_hash(), "Production changed; prepare again"
    return timeline


def preview(timeline, script, out):
    chapters = []
    buttons = []
    for i, scene in enumerate(script["scenes"], 1):
        a, b = timeline["scenes"][scene["id"]]
        chapters.append(f"{i}\n{media.voice.stamp(a, '.')} --> {media.voice.stamp(b, '.')}\n{scene['title']}\n")
        buttons.append(f'<button data-time="{a:.3f}"><span>{media.voice.stamp(a,".")[3:8]}</span>{html.escape(scene["title"])}</button>')
    (out / "chapters.vtt").write_text("WEBVTT\n\n" + "\n".join(chapters), encoding="utf-8")
    minutes, seconds = divmod(round(timeline["duration"]), 60)
    (out / "preview.html").write_text(f'''<!doctype html>
<html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The paper your AI never saw · Chapter 1</title>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#eee9e0;color:#252728;font:16px/1.6 system-ui}}
main{{max-width:1260px;margin:auto;padding:40px 28px}}.eyebrow{{font-size:12px;letter-spacing:.18em;color:#b43e30;font-weight:700}}
h1{{font-size:clamp(34px,5vw,62px);line-height:1.05;letter-spacing:-.045em;margin:16px 0}}p{{max-width:880px}}
video{{width:100%;background:#252728;border-radius:8px}}a{{color:#9d3429}}nav{{display:grid;grid-template-columns:repeat(auto-fit,minmax(285px,1fr));gap:8px;margin:24px 0}}
button{{background:#faf8f3;border:1px solid #cbc4b9;border-radius:5px;text-align:left;padding:12px;color:#252728;cursor:pointer}}
button:hover,button:focus-visible{{border-color:#b43e30}}button span{{display:inline-block;width:55px;color:#b43e30;font-variant-numeric:tabular-nums}}
.credit{{font-size:13px;color:#615f59}}@media(max-width:600px){{main{{padding:24px 12px}}}}</style>
<main><div class="eyebrow">HOW SEARCH DECIDES WHAT YOU SEE · CHAPTER 1</div>
<h1>The paper your AI never saw</h1><p>Five real citations. One invisible problem. A {minutes}:{seconds:02d} narrated investigation into the retrieval machinery behind an AI answer.</p>
<video id="film" controls playsinline preload="metadata" poster="poster.jpg" src="{NAME}.mp4">
<track kind="captions" src="{NAME}.vtt" srclang="en" label="English">
<track kind="chapters" src="chapters.vtt" srclang="en" label="Chapters"></video>
<nav aria-label="Jump to a scene">{''.join(buttons)}</nav>
<p><a href="{NAME}.mp4" download>Download MP4</a> · <a href="{NAME}.srt" download>Captions</a> · <a href="transcript.txt">Transcript</a> · <a href="{script['book_url']}">Read Chapter 1</a></p>
<p class="credit">Adapted from Aaron Tay's <em>How Search Decides What You See</em>, Chapter 1, CC BY 4.0.
Original experiment-led science explainer inspired by Veritasium's curiosity-driven storytelling. Independently produced.
Synthetic narration: Microsoft Andrew Multilingual. Card experiments are teaching illustrations.
Product observations and documentation retain the chapter's August/September 2026 dates.</p></main>
<script>const film=document.getElementById('film');document.querySelectorAll('button[data-time]').forEach(b=>b.onclick=()=>{{film.currentTime=Number(b.dataset.time);film.play().catch(()=>{{}})}});</script></html>''', encoding="utf-8")


def mux(timeline, script, out, ff):
    dest = out / f"{NAME}.mp4"
    temp = out / f"{NAME}.partial.mp4"
    media.run([ff, "-y", "-i", str(out / "picture.mp4"), "-i", str(out / "narration.wav"),
               "-i", str(out / f"{NAME}.srt"), "-map", "0:v:0", "-map", "1:a:0", "-map", "2:0",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text",
               "-ar", "48000", "-t", str(timeline["duration"]), "-metadata", f"title={script['title']}",
               "-metadata", "artist=Aaron Tay", "-metadata:s:a:0", "language=eng",
               "-metadata:s:s:0", "language=eng", "-movflags", "+faststart", str(temp)], out / "mux.log")
    info = media.verify(temp, timeline, out, ff)
    embedded = out / "embedded-captions.srt"
    media.run([ff, "-y", "-i", str(temp), "-map", "0:s:0", str(embedded)], out / "caption-check.log")
    def cue_text(path):
        return [line for line in path.read_text(encoding="utf-8-sig").splitlines()
                if line.strip() and not line.isdigit() and " --> " not in line]
    assert cue_text(embedded) == cue_text(out / f"{NAME}.srt"), "Embedded caption mismatch"
    temp.replace(dest)
    info.update(file=dest.name, production_sha256=timeline["production_sha256"], embedded_captions_verified=True)
    (out / "verification.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
    return dest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    modes = parser.add_mutually_exclusive_group()
    for mode in ["prepare-only", "stills-only", "render-only", "verify-only"]:
        modes.add_argument(f"--{mode}", action="store_true")
    parser.add_argument("--workers", type=int, default=2)
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        media.worker(json.loads(args.worker.read_text(encoding="utf-8")))
        return
    assert 1 <= args.workers <= 8
    script, out = config(), args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    ff = os.environ.get("CHAPTER_FFMPEG") or media.imageio_ffmpeg.get_ffmpeg_exe()
    if args.prepare_only or not (args.stills_only or args.render_only or args.verify_only):
        timeline = prepare(script, out, ff)
    else:
        timeline = load_timeline(out, script)
    if args.prepare_only:
        return
    if args.verify_only:
        info = media.verify(out / f"{NAME}.mp4", timeline, out, ff)
        info["production_sha256"] = timeline["production_sha256"]
        (out / "verification.json").write_text(json.dumps(info, indent=2), encoding="utf-8")
        return
    media.stills(timeline, script, out)
    preview(timeline, script, out)
    if args.stills_only:
        return
    media.render(timeline, script, out, ff, args.workers)
    print(f"Completed: {mux(timeline, script, out, ff)}", flush=True)


if __name__ == "__main__":
    main()
