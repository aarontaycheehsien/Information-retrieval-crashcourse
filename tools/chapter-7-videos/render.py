"""Render three narrated Chapter 7 films using original animated diagrams."""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import inspect
import json
import math
from pathlib import Path
import re
import sys
import tempfile
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMON = ROOT / "tools" / "chapter-2-videos"
OFFLINE = ROOT / "tools" / "chapter-4-videos"
sys.path.insert(0, str(COMMON))
spec = importlib.util.spec_from_file_location("chapter_seven_media", COMMON / "render.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
sys.path.insert(0, str(OFFLINE))
import offline_voice  # noqa: E402
offline_voice.install()
sys.path.insert(0, str(HERE))
from scenes import Film, validate_examples  # noqa: E402

DEFAULT_OUT = ROOT / "outputs" / "chapter-7-videos"


def read_config():
    cfg = json.loads((HERE / "episodes.json").read_text(encoding="utf-8"))
    source = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
    a = source.index('id="sec-dense-at-scale"')
    b = source.index('id="sec-', a+5)
    chapter = source[a:b]
    plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", chapter)))
    for required in ("Chapter 7", "Dense retrieval at collection scale", "Cosine similarity",
                     "Dot product", "HNSW", "Semantic search is a goal", "LightGBM", "Alice"):
        assert required in plain, f"Chapter source changed: missing {required}"
    cfg["source_sha256"] = hashlib.sha256(chapter.encode()).hexdigest()
    inputs = [HERE/"episodes.json", HERE/"scenes.py", HERE/"render.py",
              COMMON/"render.py", COMMON/"visuals.py", OFFLINE/"offline_voice.py",
              OFFLINE/"synthesize.ps1", ROOT/"tools"/"pick-a-card"/"narrate.py"]
    cfg["production_sha256"] = hashlib.sha256(b"".join(p.read_bytes() for p in inputs)).hexdigest()
    assert cfg["chapter"] == 7 and len(cfg["episodes"]) == 3
    assert cfg["voice"]["name"] == "Microsoft David Desktop"
    assert len({e["id"] for e in cfg["episodes"]}) == 3
    for i, episode in enumerate(cfg["episodes"], 1):
        assert episode["chapter"] == 7 and episode["id"].startswith(f"{i:02d}-")
        assert len(episode["scenes"]) == len({s["id"] for s in episode["scenes"]}) == 8
        assert all(s[k].strip() for s in episode["scenes"] for k in ("id", "title", "claim", "narration"))
    validate_examples()
    return cfg


def mux(episode, timeline, out, ff):
    folder = out / episode["id"]
    target = folder / (episode["id"]+".mp4")
    duration = math.ceil(timeline["duration"]*engine.FPS)/engine.FPS
    engine.command([ff, "-y", "-v", "error", "-i", str(folder/"picture.mp4"),
                    "-i", str(folder/"soundtrack.wav"), "-i", str(folder/"captions.srt"),
                    "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text", "-disposition:s:0", "0",
                    "-metadata:s:s:0", "language=eng", "-metadata", "title="+episode["title"],
                    "-metadata", "comment=Original animation; offline synthetic narration; adapted from Chapter 7 by Aaron Tay",
                    "-t", str(duration), "-movflags", "+faststart", str(target)], folder/"mux.log")
    print(f"Exported {target.name}", flush=True)


# Compatibility with both the committed and newer shared engine APIs.
engine.Film = Film
engine.mux = mux


def with_film(fn, *args):
    kwargs = {"film_class": Film} if "film_class" in inspect.signature(fn).parameters else {}
    return fn(*args, **kwargs)


def prepare(cfg, episode, out, ff):
    timeline = engine.prepare(cfg, episode, out, ff)
    timeline["production_sha256"] = cfg["production_sha256"]
    folder = out/episode["id"]
    (folder/"timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    transcript = "\n\n".join(s["title"]+"\n"+s["narration"] for s in episode["scenes"])
    (folder/"transcript.txt").write_text(episode["title"]+"\n\n"+transcript+
        f"\n\nAdapted from Chapter 7, {cfg['book']}, by {cfg['author']}.\n"
        f"Source: {cfg['source']}\nSynthetic voice: {cfg['voice']['name']} (offline).\n", encoding="utf-8")
    return timeline


def preview(cfg, out):
    cards = []
    for i, episode in enumerate(cfg["episodes"], 1):
        timeline = engine.load_timeline(out, episode)
        seconds = round(timeline["duration"])
        rel = episode["id"]+"/"
        title = html.escape(episode["title"])
        cards.append(f'''<article><p class="kicker">FILM {i:02d} · {seconds//60}:{seconds%60:02d}</p>
<h2>{title}</h2><p>{html.escape(episode['subtitle'])}</p>
<video aria-label="{title}" controls playsinline preload="metadata" poster="{rel}poster.jpg">
<source src="{rel}{episode['id']}.mp4" type="video/mp4">
<track kind="captions" src="{rel}captions.vtt" srclang="en" label="English"></video>
<nav aria-label="Downloads for {title}"><a href="{rel}{episode['id']}.mp4" download>Download MP4</a>
<a href="{rel}captions.srt" download>Captions</a><a href="{rel}transcript.txt">Transcript</a>
<a href="{rel}contact-sheet.jpg">Storyboard</a></nav></article>''')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter 7 — Animated explainers</title><style>
*{box-sizing:border-box}body{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}
main{max-width:1120px;margin:auto;padding:48px 24px}h1{font-size:clamp(36px,6vw,64px);line-height:1.08;margin:12px 0}
h2{font-size:clamp(25px,4vw,36px);line-height:1.2;margin:8px 0}.lead,article>p{color:#a8bbd8}
.kicker{letter-spacing:.14em;color:#68e0bb!important;font-size:13px;font-weight:700}
article{margin:40px 0;padding:28px;background:#1d2b50;border-radius:24px}video{display:block;width:100%;border-radius:16px;background:#101833}
nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}a{color:#68e0bb}footer{font-size:15px;color:#a8bbd8}
a:focus-visible,video:focus-visible{outline:3px solid #ffd36a;outline-offset:5px}
@media(max-width:600px){main{padding:28px 14px}article{padding:16px}}
</style></head><body><main><p class="kicker">CHAPTER 7 · HOW SEARCH DECIDES WHAT YOU SEE</p>
<h1>The constellation,<br>the shortcut, and the boundary.</h1><p class="lead">Three animated films adapted from Aaron Tay's Chapter 7, “Dense retrieval at collection scale.” Original colorful geometric animation, music, offline English narration, and captions.</p>'''
    page += "".join(cards)
    page += '''<footer><p><a href="chapter-7-videos.zip" download>Download all three films, captions, transcripts and storyboards</a></p>
<p><a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#dense-at-scale">Read Chapter 7</a> · <a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/vector-similarity-lab.html">Explore the Vector Similarity Lab</a></p>
<p>Arrows, score distributions, compression, and budgets are teaching illustrations. The six-point Euclidean example is calculated; its approximate run is stipulated and does not simulate HNSW. Product pipelines are the chapter's dated 2025 and 2026 snapshots, not claims about current services.</p>
<p>Adaptation credit: Aaron Tay, <em>How Search Decides What You See</em>. CC BY 4.0. Synthetic voice: Microsoft David Desktop, generated locally. Original artwork, characters and music.</p></footer></main></body></html>'''
    (out/"preview.html").write_text(page, encoding="utf-8")


def package(cfg, out, reports):
    """Only package files whose source, production, and MP4 digests still match."""
    for episode, report in zip(cfg["episodes"], reports):
        assert report["source_sha256"] == cfg["source_sha256"]
        assert report["production_sha256"] == cfg["production_sha256"]
        with (out/episode["id"]/report["file"]).open("rb") as stream:
            assert hashlib.file_digest(stream, "sha256").hexdigest() == report["sha256"]
    # Separate render processes may finish together; replace the ZIP atomically.
    with tempfile.NamedTemporaryFile(dir=out, suffix=".zip", delete=False) as stream:
        temporary = Path(stream.name)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as archive:
            gallery = (out/"preview.html").read_text(encoding="utf-8")
            gallery = gallery.replace('<p><a href="chapter-7-videos.zip" download>Download all three films, captions, transcripts and storyboards</a></p>', "")
            archive.writestr("preview.html", gallery)
            archive.write(out/"verification.json", "verification.json")
            for episode in cfg["episodes"]:
                folder = out/episode["id"]
                names = [episode["id"]+".mp4", "captions.srt", "captions.vtt", "transcript.txt",
                         "poster.jpg", "contact-sheet.jpg", "timeline.json", "verification.json"]
                for path in [*(folder/name for name in names), *folder.glob("scene-*.jpg")]:
                    archive.write(path, path.relative_to(out))
        temporary.replace(out/"chapter-7-videos.zip")
    finally:
        temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", choices=["1", "2", "3", "all"], default="all")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    modes = parser.add_mutually_exclusive_group()
    for flag in ("prepare-only", "stills-only", "render-only", "verify-only", "check"):
        modes.add_argument("--"+flag, action="store_true")
    args = parser.parse_args()
    cfg = read_config()
    if args.check:
        print("Chapter 7 source, scripts, cosine/dot-product examples and nearest neighbours: passed")
        return
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    if out == DEFAULT_OUT.resolve():
        (out/".gitignore").write_text("*\n!.gitignore\n", encoding="utf-8")
    ff = engine.imageio_ffmpeg.get_ffmpeg_exe()
    episodes = cfg["episodes"] if args.episode == "all" else [cfg["episodes"][int(args.episode)-1]]
    for episode in episodes:
        if args.stills_only or args.render_only or args.verify_only:
            timeline = engine.load_timeline(out, episode)
            assert timeline["source_sha256"] == cfg["source_sha256"], "Chapter changed; prepare again"
            assert timeline["production_sha256"] == cfg["production_sha256"], "Production changed; prepare again"
        else:
            timeline = prepare(cfg, episode, out, ff)
        if not args.verify_only:
            with_film(engine.reviews, episode, timeline, out)
        if not (args.prepare_only or args.stills_only or args.verify_only):
            with_film(engine.render, episode, timeline, out, ff)
        if not (args.prepare_only or args.stills_only):
            report = engine.verify(episode, timeline, out, ff)
            report["production_sha256"] = cfg["production_sha256"]
            (out/episode["id"]/"verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if all((out/e["id"]/"timeline.json").exists() for e in cfg["episodes"]):
        preview(cfg, out)
    if all((out/e["id"]/"verification.json").exists() for e in cfg["episodes"]):
        reports = [json.loads((out/e["id"]/"verification.json").read_text(encoding="utf-8")) for e in cfg["episodes"]]
        if all(r.get("production_sha256") == cfg["production_sha256"] and r["source_sha256"] == cfg["source_sha256"] for r in reports):
            (out/"verification.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
            package(cfg, out, reports)


if __name__ == "__main__":
    main()
