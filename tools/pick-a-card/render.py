"""Render "Pick a Card", a narrated promo for How Search Decides What You See.

    python tools/pick-a-card/render.py                 # full render, both editions
    python tools/pick-a-card/render.py --stills 5,33.5 # review frames only
    python tools/pick-a-card/render.py --verify-only   # re-check existing exports
"""
from __future__ import annotations

import argparse
import hashlib
import os
import json
import re
import subprocess
import sys
import time
from pathlib import Path

import numpy as np
import skia

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
sys.path.insert(0, str(HERE))

import audio  # noqa: E402
import narrate  # noqa: E402
from draw import CREAM, H, W, check_fonts, font, measure, paint, rrect, text  # noqa: E402
from scenes import Film  # noqa: E402

FPS = 30
NAME = "pick-a-card"


def ffmpeg_exe() -> str:
    if os.environ.get("PROMO_FFMPEG"):
        return os.environ["PROMO_FFMPEG"]
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run(cmd: list[str], log: Path) -> str:
    proc = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    log.write_text(proc.stdout + proc.stderr, encoding="utf-8")
    if proc.returncode:
        raise SystemExit(f"ffmpeg failed; see {log}")
    return proc.stderr


# Captions burned into the social edition --------------------------------
def draw_caption(c: skia.Canvas, cues: list[dict], t: float) -> None:
    for cue in cues:
        if cue["start"] - 0.05 <= t < cue["end"]:
            f = font("ui_b", 40)
            w = measure(cue["text"], f) + 56
            a = min(1.0, (t - cue["start"] + 0.05) / 0.12, (cue["end"] - t) / 0.12)
            y = H - 108
            c.drawRRect(rrect(W / 2 - w / 2, y - 46, W / 2 + w / 2, y + 18, 14), paint((0, 0, 0), 0.62 * a))
            text(c, cue["text"], W / 2, y, f, CREAM, a)
            return


# Skia's Windows wheels run the 8-bit raster pipeline without SIMD; float16
# surfaces blend about twice as fast. Frames render in F16 and are read back
# as 8-bit BGRA. Chunks of frames render in independent worker processes
# (plain subprocesses: no shared handles, which sandboxed shells can refuse).
F16 = skia.ImageInfo.Make(W, H, skia.kRGBA_F16_ColorType, skia.kPremul_AlphaType)
BGRA = skia.ImageInfo.Make(W, H, skia.kBGRA_8888_ColorType, skia.kPremul_AlphaType)
X264 = ["-c:v", "libx264", "-preset", "slow", "-crf", "17", "-tune", "animation", "-pix_fmt", "yuv420p",
        "-threads", "3", "-x264-params", "keyint=60:min-keyint=30:rc-lookahead=30"]
WORKER_GB = 0.65  # one worker: Python, Skia assets, an F16 surface and two x264 encoders


def default_workers() -> int:
    """As many workers as cores allow, limited by free physical memory."""
    cores = max(1, (os.cpu_count() or 2) - 2)
    free_gb = 2.0
    if sys.platform == "win32":
        import ctypes

        class MemoryStatus(ctypes.Structure):
            _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong), ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong), ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong)]
        status = MemoryStatus()
        status.dwLength = ctypes.sizeof(MemoryStatus)
        if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
            free_gb = status.ullAvailPhys / 2 ** 30
    return max(1, min(cores, 8, int(free_gb / WORKER_GB)))


def new_surface() -> skia.Surface:
    return skia.Surface.MakeRaster(F16)


def snapshot(surface: skia.Surface, buf: np.ndarray) -> np.ndarray:
    surface.readPixels(BGRA, buf, W * 4)
    return buf


def _render_chunk(job: dict) -> list[str]:
    """Worker: render frames [a, b) of each edition to its own MP4 segment."""
    script = job["script"]
    tl = narrate.build(script, Path(job["out"]), job["ff"], quiet=True)
    film = Film(tl, script)
    procs = []
    for seg in job["segments"]:
        cmd = [job["ff"], "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}", "-r", str(FPS),
               "-i", "-", *X264, seg]
        procs.append(subprocess.Popen(cmd, stdin=subprocess.PIPE))
    surface, buf = new_surface(), np.zeros((H, W, 4), np.uint8)
    for i in range(job["a"], job["b"]):
        t = i / FPS
        c = surface.getCanvas()
        c.clear(skia.ColorBLACK)
        film.frame(c, t)
        for captioned, proc in zip(job["captioned"], procs):
            if captioned:
                draw_caption(c, job["cues"], t)
            proc.stdin.write(snapshot(surface, buf).tobytes())
    for proc in procs:
        proc.stdin.close()
        if proc.wait():
            raise RuntimeError("video encoder failed")
    return job["segments"]


def render_frames(script: dict, duration: float, cues: list[dict], outputs: list[tuple[Path, bool]], ff: str, out: Path,
                  workers: int) -> None:
    total = int(round(duration * FPS))
    seg_dir = out / "segments"
    seg_dir.mkdir(exist_ok=True)
    bounds = np.linspace(0, total, workers * 2 + 1).round().astype(int)
    jobs = []
    for n, (a, b) in enumerate(zip(bounds, bounds[1:])):
        jobs.append({"script": script, "out": str(out), "ff": ff, "a": int(a), "b": int(b), "cues": cues,
                     "captioned": [cap for _, cap in outputs],
                     "segments": [str(seg_dir / f"{path.stem}-{n:03d}.mp4") for path, _ in outputs]})
    started = time.time()
    pending, running, done = list(enumerate(jobs)), [], 0
    while pending or running:
        while pending and len(running) < workers:
            n, job = pending.pop(0)
            path = seg_dir / f"job-{n:03d}.json"
            path.write_text(json.dumps(job), encoding="utf-8")
            log = open(seg_dir / f"job-{n:03d}.log", "w", encoding="utf-8")
            proc = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), "--chunk-job", str(path)],
                                    stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT)
            running.append((n, proc, log))
        time.sleep(0.5)
        for item in list(running):
            n, proc, log = item
            if proc.poll() is None:
                continue
            log.close()
            running.remove(item)
            if proc.returncode:
                for _, other, other_log in running:
                    other.kill()
                    other_log.close()
                raise SystemExit(f"frame worker {n} failed; see {seg_dir / f'job-{n:03d}.log'}")
            done += 1
            print(f"  chunk {done}/{len(jobs)}  {time.time() - started:5.0f}s elapsed", flush=True)
    for k, (path, _) in enumerate(outputs):
        listing = seg_dir / f"{path.stem}.txt"
        listing.write_text("".join(f"file '{Path(job['segments'][k]).name}'\n" for job in jobs), encoding="utf-8")
        run([ff, "-y", "-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(path)], out / f"concat-{path.stem}.log")
    for f in seg_dir.iterdir():
        f.unlink()
    try:
        seg_dir.rmdir()
    except OSError:  # another process may still have the empty folder open
        pass


def still(film: Film, t: float, path: Path, cues: list[dict] | None = None) -> None:
    surface, buf = new_surface(), np.zeros((H, W, 4), np.uint8)
    c = surface.getCanvas()
    c.clear(skia.ColorBLACK)
    film.frame(c, t)
    if cues:
        draw_caption(c, cues, t)
    snapshot(surface, buf)
    from PIL import Image
    Image.fromarray(buf[..., [2, 1, 0]]).save(path, quality=92)


def contact_sheet(film: Film, times: list[float], path: Path, cols: int = 6) -> None:
    from PIL import Image, ImageDraw
    tw, th = 480, 270
    rows = (len(times) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * (th + 26)), (12, 12, 12))
    surface, buf = new_surface(), np.zeros((H, W, 4), np.uint8)
    d = ImageDraw.Draw(sheet)
    for n, t in enumerate(times):
        c = surface.getCanvas()
        c.clear(skia.ColorBLACK)
        film.frame(c, t)
        snapshot(surface, buf)
        im = Image.fromarray(buf[..., [2, 1, 0]]).resize((tw, th), Image.LANCZOS)
        x, y = (n % cols) * tw, (n // cols) * (th + 26)
        sheet.paste(im, (x, y))
        d.text((x + 6, y + th + 5), f"{t:6.2f}s", fill=(220, 220, 220))
    sheet.save(path, quality=90)


# Mux, verify ------------------------------------------------------------
def mux(ff: str, video: Path, audio_wav: Path, dest: Path, out: Path) -> None:
    # No embedded subtitle track: the MP4 muxer always enables it, so players would
    # show captions on the clean edition. Captions ship as SRT/VTT sidecars and as
    # the burned-in edition instead.
    tmp = dest.with_suffix(".partial.mp4")
    cmd = [ff, "-y", "-i", str(video), "-i", str(audio_wav), "-map", "0:v", "-map", "1:a"]
    cmd += ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-metadata:s:a:0", "language=eng",
            "-metadata", "title=Pick a Card \u2014 How Search Decides What You See",
            "-metadata", "artist=Aaron Tay", "-movflags", "+faststart", str(tmp)]
    run(cmd, out / f"mux-{dest.stem}.log")
    tmp.replace(dest)


def verify(ff: str, path: Path, duration: float, out: Path) -> dict:
    log = run([ff, "-v", "info", "-i", str(path), "-map", "0:v", "-map", "0:a", "-f", "null", "-"], out / f"verify-{path.stem}.log")
    loud = run([ff, "-hide_banner", "-i", str(path), "-map", "0:a", "-af", "ebur128=peak=true", "-f", "null", "-"], out / f"loudness-{path.stem}.log")
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", loud)[-1])
    peak = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", loud)[-1])
    head = path.read_bytes()[:4096]
    frames = int(re.findall(r"frame=\s*(\d+)", log)[-1])
    info = {
        "file": path.name,
        "bytes": path.stat().st_size,
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "frames": frames,
        "expected_frames": int(round(duration * FPS)),
        "integrated_lufs": lufs,
        "true_peak_dbfs": peak,
        "faststart": head.find(b"moov") != -1 and (head.find(b"mdat") == -1 or head.find(b"moov") < head.find(b"mdat")),
        "video": re.findall(r"Video: (h264[^\n]*)", log)[0][:80],
        "audio": re.findall(r"Audio: (aac[^\n]*)", log)[0][:60],
    }
    problems = []
    if abs(frames - info["expected_frames"]) > 2:
        problems.append("frame count")
    if not -17.0 <= lufs <= -15.0:
        problems.append("loudness")
    if peak > -0.9:
        problems.append("true peak")
    if not info["faststart"]:
        problems.append("faststart")
    info["problems"] = problems
    return info


def write_extras(script: dict, tl: narrate.Timeline, out: Path, voice: dict) -> None:
    transcript = "\n".join(f"[{tk.start:5.2f}] {tk.text}" for tk in tl.takes)
    (out / "transcript.txt").write_text(
        f"Pick a Card \u2014 narration\n\n{transcript}\n\nVoice: synthetic ({voice['name']}, Microsoft neural TTS via edge-tts). "
        "No voice cloning.\n", encoding="utf-8")
    share = f"""Pick a card. Any card.

Search engines perform three real tricks in this 90-second film \u2014 and a free textbook shows you how tricks like these work.

How Search Decides What You See \u2014 a free textbook by {script['author']}
Read it: {script['book_url']}
New to the subject? Start here: {script['intro_url']}

All three tricks are real observations of academic search tools, documented in Chapter 1. The search results on the cards are illustrative.
"""
    (out / "share-copy.txt").write_text(share, encoding="utf-8")
    (out / "preview.html").write_text(f"""<!doctype html><meta charset="utf-8"><title>Pick a Card</title>
<style>body{{background:#111;color:#eee;font:16px system-ui;margin:24px auto;max-width:1280px}}video{{width:100%;border-radius:8px;margin:8px 0 28px}}a{{color:#e8c37c}}</style>
<h1>Pick a Card</h1>
<p>Clean edition (captions available in the player from the VTT file):</p>
<video controls preload="metadata" src="{NAME}.mp4"><track kind="captions" srclang="en" label="English" src="{NAME}.vtt"></video>
<p>Social edition with burned-in captions:</p>
<video controls preload="metadata" src="{NAME}-captioned.mp4"></video>
<p><a href="{NAME}.mp4" download>Download clean MP4</a> \u00b7 <a href="{NAME}-captioned.mp4" download>Download captioned MP4</a> \u00b7 <a href="{NAME}.srt" download>SRT captions</a></p>
""", encoding="utf-8")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--output", type=Path, default=ROOT / "outputs" / NAME)
    ap.add_argument("--stills", help="comma-separated times (seconds) to render as JPEGs")
    ap.add_argument("--sheet", action="store_true", help="write a contact sheet only")
    ap.add_argument("--verify-only", action="store_true")
    ap.add_argument("--no-captioned", action="store_true", help="skip the burned-caption edition")
    ap.add_argument("--workers", type=int, default=0, help="parallel frame workers (default: by cores and free memory)")
    ap.add_argument("--chunk-job", type=Path, help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.chunk_job:
        _render_chunk(json.loads(args.chunk_job.read_text(encoding="utf-8")))
        return

    check_fonts()
    out = args.output
    out.mkdir(parents=True, exist_ok=True)
    ff = ffmpeg_exe()
    script = json.loads((HERE / "script.json").read_text(encoding="utf-8"))
    tl = narrate.build(script, out, ff)
    print(f"Timeline: {tl.duration:.2f}s, {len(tl.takes)} takes", flush=True)

    if args.verify_only:
        report = [verify(ff, out / f"{NAME}{suffix}.mp4", tl.duration, out) for suffix in ("", "-captioned")
                  if (out / f"{NAME}{suffix}.mp4").exists()]
        print(json.dumps(report, indent=2))
        return

    cues = narrate.write_captions(tl, out)
    film = Film(tl, script)
    if args.stills:
        (out / "stills").mkdir(exist_ok=True)
        for s in args.stills.split(","):
            t = float(s.rstrip("c"))
            captioned = s.endswith("c")
            still(film, t, out / "stills" / f"t{t:06.2f}{'-captioned' if captioned else ''}.jpg", cues if captioned else None)
        print("stills written to", out / "stills")
        return
    sheet_times = [round(x, 2) for x in np.linspace(0.6, tl.duration - 0.1, 36)]
    contact_sheet(film, sheet_times, out / "contact-sheet.jpg")
    if args.sheet:
        print("contact sheet:", out / "contact-sheet.jpg")
        return

    print("Soundtrack:", flush=True)
    mix = audio.build(tl, film.k, out, ff)
    editions = [(out / f"{NAME}.video.mp4", False)]
    if not args.no_captioned:
        editions.append((out / f"{NAME}-captioned.video.mp4", True))
    workers = args.workers or default_workers()
    print(f"Pictures: {workers} worker(s)", flush=True)
    render_frames(script, tl.duration, cues, editions, ff, out, workers)
    results = []
    for video, captioned in editions:
        dest = out / (video.name.replace(".video", ""))
        mux(ff, video, mix, dest, out)
        results.append(verify(ff, dest, tl.duration, out))
        if not results[-1]["problems"]:
            video.unlink()  # the picture-only intermediate is kept for re-muxing if checks fail
    still(film, tl.duration - 0.2, out / "poster.jpg")
    write_extras(script, tl, out, script["voice"])
    manifest = {
        "duration": tl.duration,
        "voice": script["voice"],
        "takes": [{"id": tk.id, "start": round(tk.start, 3), "end": round(tk.end, 3), "text": tk.text, "cache_key": tk.cache_key,
                   "words": [{"text": w["text"], "start": round(w["start"], 3), "end": round(w["end"], 3)} for w in tk.words]}
                  for tk in tl.takes],
        "scenes": {k: [round(a, 3), round(b, 3)] for k, (a, b) in tl.scenes.items()},
        "exports": results,
    }
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    for r in results:
        status = "OK" if not r["problems"] else "PROBLEMS: " + ", ".join(r["problems"])
        print(f"{r['file']}: {r['frames']} frames, {r['integrated_lufs']} LUFS, peak {r['true_peak_dbfs']} dBFS \u2014 {status}")
    if any(r["problems"] for r in results):
        raise SystemExit("verification failed")


if __name__ == "__main__":
    main()
