"""Render three narrated Chapter 9 films with the repository's media engine."""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import math
import subprocess
import time
import zipfile
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMON = ROOT / "tools" / "chapter-2-videos"
sys.path.insert(0, str(COMMON))
spec = importlib.util.spec_from_file_location("chapter_nine_media", COMMON / "render.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
sys.path.insert(0, str(HERE))
from scenes import Film, validate_examples  # noqa: E402

DEFAULT_OUT = ROOT / "outputs" / "chapter-9-videos"


def render(episode, timeline, out, ff):
    """Send frames in bounded writes for Windows pipes under memory pressure."""
    folder = out / episode["id"]
    film = Film(episode, timeline)
    info = engine.skia.ImageInfo.Make(engine.W, engine.H, engine.skia.kBGRA_8888_ColorType,
                                      engine.skia.kPremul_AlphaType)
    surface = engine.skia.Surface.MakeRaster(info)
    buffer = engine.np.empty((engine.H, engine.W, 4), dtype=engine.np.uint8)
    count = math.ceil(timeline["duration"] * engine.FPS)
    args = [ff, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s",
            f"{engine.W}x{engine.H}", "-r", str(engine.FPS), "-i", "-", "-an",
            "-c:v", "libx264", "-preset", "fast", "-crf", "19", "-tune", "animation",
            "-pix_fmt", "yuv420p", "-threads", "2", str(folder / "picture.mp4")]
    started = time.monotonic()
    with (folder / "encode.log").open("wb") as log:
        process = subprocess.Popen(args, stdin=subprocess.PIPE, stderr=log, bufsize=0)
        try:
            for frame in range(count):
                pixels = engine.draw_frame(film, surface, frame / engine.FPS, buffer=buffer)
                data = memoryview(pixels).cast("B")
                offset = 0
                while offset < len(data):
                    written = process.stdin.write(data[offset:offset+65536])
                    if not written:
                        raise RuntimeError(f"Encoder pipe closed; see {folder/'encode.log'}")
                    offset += written
                if frame % 900 == 0:
                    print(f"{episode['id']}: {frame}/{count} frames ({time.monotonic()-started:.0f}s)", flush=True)
            process.stdin.close()
            if process.wait() != 0:
                raise RuntimeError(f"Picture encoding failed; see {folder/'encode.log'}")
        except BaseException:
            process.kill()
            process.wait()
            raise
    engine.mux(episode, timeline, out, ff)


def read_config():
    script = (HERE / "episodes.json").read_bytes()
    cfg = json.loads(script)
    source = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
    a = source.index('id="sec-reranking-and-hybrid"')
    b = source.index('id="sec-hybrid-and-fusion"', a)
    chapter = source[a:b]
    for required in ("Chapter 9", "Reranking and multi-stage retrieval", "MaxSim",
                     "cross-encoder", "LambdaMART", "500", "30", "diversification"):
        assert required.lower() in chapter.lower(), f"Chapter source changed: missing {required}"
    cfg["source_sha256"] = hashlib.sha256(chapter.encode()).hexdigest()
    # All prepared assets must be rebuilt after script or artwork changes.
    production = (HERE / "render.py").read_bytes() + script + (HERE / "scenes.py").read_bytes() + (COMMON / "render.py").read_bytes() + (COMMON / "visuals.py").read_bytes() + (ROOT / "tools" / "pick-a-card" / "narrate.py").read_bytes()
    cfg["production_sha256"] = hashlib.sha256(production).hexdigest()
    assert len(cfg["episodes"]) == 3
    assert len({e["id"] for e in cfg["episodes"]}) == 3
    for number, episode in enumerate(cfg["episodes"], 1):
        assert episode["chapter"] == 9 and episode["id"].startswith(f"{number:02d}-")
        assert len(episode["scenes"]) == len({s["id"] for s in episode["scenes"]}) == 8
        for scene in episode["scenes"]:
            assert all(scene[k].strip() for k in ("title", "claim", "narration"))
    validate_examples()
    return cfg


def preview(cfg, out):
    cards = []
    for number, episode in enumerate(cfg["episodes"], 1):
        timeline = engine.load_timeline(out, episode)
        seconds = round(timeline["duration"])
        rel = episode["id"] + "/"
        title = html.escape(episode["title"])
        cards.append(f'''<article><p class="kicker">FILM {number:02d} · {seconds//60}:{seconds%60:02d}</p>
<h2>{title}</h2><p>{html.escape(episode['subtitle'])}</p>
<video aria-label="{title}" controls playsinline preload="metadata" poster="{rel}poster.jpg">
<source src="{rel}{episode['id']}.mp4" type="video/mp4">
<track kind="captions" src="{rel}captions.vtt" srclang="en" label="English"></video>
<nav aria-label="Downloads for {title}"><a href="{rel}{episode['id']}.mp4" download>Download MP4</a>
<a href="{rel}captions.srt" download>Captions</a><a href="{rel}transcript.txt">Transcript</a>
<a href="{rel}contact-sheet.jpg">Storyboard</a></nav></article>''')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter 9 — Animated explainers</title><style>
*{box-sizing:border-box}body{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}
main{max-width:1120px;margin:auto;padding:48px 24px}h1{font-size:clamp(36px,6vw,64px);line-height:1.08;margin:12px 0}
h2{font-size:clamp(25px,4vw,36px);line-height:1.2;margin:8px 0}.lead,article>p{color:#a8bbd8}
.kicker{letter-spacing:.14em;color:#68e0bb!important;font-size:13px;font-weight:700}
article{margin:40px 0;padding:28px;background:#1d2b50;border-radius:24px}video{display:block;width:100%;border-radius:16px;background:#101833}
nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}a{color:#68e0bb}footer{font-size:15px;color:#a8bbd8}
a:focus-visible,video:focus-visible{outline:3px solid #ffd36a;outline-offset:5px}
@media(max-width:600px){main{padding:28px 14px}article{padding:16px}}
</style></head><body><main><p class="kicker">CHAPTER 9 · HOW SEARCH DECIDES WHAT YOU SEE</p>
<h1>The shortlist,<br>the score, and the list</h1><p class="lead">Three animated films adapted from Aaron Tay's Chapter 9, “Reranking and multi-stage retrieval.” Original flat-vector animation and music, English synthetic narration, and captions.</p>'''
    page += "".join(cards)
    page += '''<footer><p><a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#reranking-and-hybrid">Read Chapter 9</a> · <a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#hybrid-and-fusion">Continue to Chapter 10</a></p>
<p>Candidate labels, precision and recall calculations, MaxSim similarities, comparison cycles, and diversified selections are teaching illustrations. The animations do not report trained-model results. Product examples refer to documented architectures; see the <a href="production-notes.md">production notes</a> for sources.</p>
<p>Adaptation credit: Aaron Tay, <em>How Search Decides What You See</em>. CC BY 4.0. Synthetic voice: Microsoft en-GB-RyanNeural.</p><p><a href="chapter-9-videos.zip" download>Download all three films and captions</a> · <a href="verification.json">Media verification</a></p></footer></main></body></html>'''
    (out / "preview.html").write_text(page, encoding="utf-8")
    (out / "production-notes.md").write_bytes((HERE / "README.md").read_bytes())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", choices=["1", "2", "3", "all"], default="all")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    modes = parser.add_mutually_exclusive_group()
    for flag in ("prepare-only", "stills-only", "render-only", "verify-only"):
        modes.add_argument("--"+flag, action="store_true")
    parser.add_argument("--check-only", action="store_true", help="Validate source, script and worked examples without synthesis")
    args = parser.parse_args()
    if args.check_only:
        read_config()
        print("Chapter 9 source, 24 scenes, and worked examples: passed")
        return
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    cfg, ff = read_config(), engine.imageio_ffmpeg.get_ffmpeg_exe()
    episodes = cfg["episodes"] if args.episode == "all" else [cfg["episodes"][int(args.episode)-1]]
    for episode in episodes:
        if args.stills_only or args.render_only or args.verify_only:
            timeline = engine.load_timeline(out, episode)
            assert timeline["source_sha256"] == cfg["source_sha256"], "Chapter changed; prepare again"
            assert timeline["production_sha256"] == cfg["production_sha256"], "Production changed; prepare again"
        else:
            timeline = engine.prepare(cfg, episode, out, ff)
            timeline["production_sha256"] = cfg["production_sha256"]
            (out / episode["id"] / "timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
        if not args.verify_only:
            engine.reviews(episode, timeline, out, film_class=Film)
        if not (args.prepare_only or args.stills_only or args.verify_only):
            render(episode, timeline, out, ff)
        if not (args.prepare_only or args.stills_only):
            report = engine.verify(episode, timeline, out, ff)
            report["production_sha256"] = cfg["production_sha256"]
            (out/episode["id"]/"verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if all((out/e["id"]/"timeline.json").exists() for e in cfg["episodes"]):
        preview(cfg, out)
    if all((out/e["id"]/"verification.json").exists() for e in cfg["episodes"]):
        reports = [json.loads((out/e["id"]/"verification.json").read_text(encoding="utf-8")) for e in cfg["episodes"]]
        assert all(r.get("production_sha256") == cfg["production_sha256"] and r["source_sha256"] == cfg["source_sha256"] for r in reports), "An export is stale; render it again"
        (out/"verification.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
        with zipfile.ZipFile(out/"chapter-9-videos.zip", "w", zipfile.ZIP_DEFLATED, compresslevel=1) as archive:
            for name in ("preview.html", "verification.json"):
                archive.write(out/name, name)
            for episode in cfg["episodes"]:
                for name in (episode["id"]+".mp4", "captions.srt", "captions.vtt", "transcript.txt", "poster.jpg", "contact-sheet.jpg", "verification.json"):
                    path = out/episode["id"]/name
                    archive.write(path, path.relative_to(out))
            archive.write(HERE/"README.md", "production-notes.md")
        print(f"Packaged {out/'chapter-9-videos.zip'}", flush=True)


if __name__ == "__main__":
    main()
