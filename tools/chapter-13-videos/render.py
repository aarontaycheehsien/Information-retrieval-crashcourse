"""Render three narrated Chapter 13 explainers using the shared media engine."""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import inspect
import json
import math
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMON = ROOT / "tools" / "chapter-2-videos"
sys.path.insert(0, str(COMMON))
spec = importlib.util.spec_from_file_location("chapter13_media", COMMON / "render.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
sys.path.insert(0, str(HERE))
from scenes import Film, validate_examples  # noqa: E402

sys.path.insert(0, str(ROOT / "tools" / "chapter-4-videos"))
import offline_voice  # noqa: E402
offline_voice.install()
DEFAULT_OUT = ROOT / "outputs" / "chapter-13-videos"
engine.Film = Film


def call_film(fn, *args):
    if "film_class" in inspect.signature(fn).parameters:
        return fn(*args, film_class=Film)
    return fn(*args)


def read_config():
    cfg = json.loads((HERE / "episodes.json").read_text(encoding="utf-8"))
    source = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
    start = source.index('id="sec-diagnosing-failure"')
    end = source.index('id="sec-evaluation"', start)
    chapter = source[start:end]
    for required in ("Chapter 13", "Diagnosing retrieval failure", "myocardial infarction",
                     "DELULU-427", "##zz", "##lord", "distribution", "negation", "shortlist"):
        assert required in chapter, f"Chapter source changed: missing {required}"
    cfg["source_sha256"] = hashlib.sha256(chapter.encode()).hexdigest()
    files = (HERE / "episodes.json", HERE / "scenes.py", HERE / "render.py",
             COMMON / "render.py", COMMON / "visuals.py", ROOT / "tools/pick-a-card/narrate.py",
             ROOT / "tools/chapter-4-videos/offline_voice.py", ROOT / "tools/chapter-4-videos/synthesize.ps1")
    cfg["production_sha256"] = hashlib.sha256(b"".join(path.read_bytes() for path in files)).hexdigest()
    assert len(cfg["episodes"]) == len({e["id"] for e in cfg["episodes"]}) == 3
    for number, episode in enumerate(cfg["episodes"], 1):
        assert episode["chapter"] == 13 and episode["id"].startswith(f"{number:02d}-")
        assert len(episode["scenes"]) == len({s["id"] for s in episode["scenes"]}) == 8
        assert {s["id"] for s in episode["scenes"]} == Film.SCENES[number]
        for scene in episode["scenes"]:
            assert all(scene[k].strip() for k in ("title", "claim", "narration"))
            assert f'id="{scene["source_anchor"]}"' in chapter, scene["source_anchor"]
    validate_examples()
    return cfg


def prepare(cfg, episode, out, ff):
    timeline = engine.prepare(cfg, episode, out, ff)
    transcript = "\n\n".join(s["title"] + "\n" + s["narration"] for s in episode["scenes"])
    (out / episode["id"] / "transcript.txt").write_text(
        episode["title"] + "\n\n" + transcript +
        f"\n\nAdapted from Chapter 13, {cfg['book']}, by {cfg['author']}.\n"
        f"Source: {cfg['source']}. CC BY 4.0.\n"
        f"Synthetic voice: {cfg['voice']['name']}. Original artwork and music.\n", encoding="utf-8")
    timeline["production_sha256"] = cfg["production_sha256"]
    (out / episode["id"] / "timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
    return timeline


def mux(episode, timeline, out, ff):
    folder = out / episode["id"]
    duration = math.ceil(timeline["duration"] * engine.FPS) / engine.FPS
    engine.command([ff, "-y", "-v", "error", "-i", str(folder / "picture.mp4"),
        "-i", str(folder / "soundtrack.wav"), "-i", str(folder / "captions.srt"),
        "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "copy",
        "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text", "-disposition:s:0", "0",
        "-metadata:s:s:0", "language=eng", "-metadata", "title=" + episode["title"],
        "-metadata", "comment=Original animation and music; synthetic narration; adapted from Chapter 13 by Aaron Tay; CC BY 4.0",
        "-t", str(duration), "-movflags", "+faststart", str(folder / (episode["id"] + ".mp4"))], folder / "mux.log")
    print(f"Exported {episode['id']}.mp4", flush=True)


engine.mux = mux


def preview(cfg, out):
    cards = []
    for number, episode in enumerate(cfg["episodes"], 1):
        if not (out / episode["id"] / "timeline.json").exists():
            continue
        timeline = engine.load_timeline(out, episode)
        seconds, rel = round(timeline["duration"]), episode["id"] + "/"
        title = html.escape(episode["title"])
        cards.append(f'''<article><p class="kicker">FILM {number:02d} · {seconds//60}:{seconds%60:02d}</p>
<h2>{title}</h2><p>{html.escape(episode['subtitle'])}</p>
<video aria-label="{title}" controls playsinline preload="metadata" poster="{rel}poster.jpg">
<source src="{rel}{episode['id']}.mp4" type="video/mp4">
<track kind="captions" src="{rel}captions.vtt" srclang="en" label="English"></video>
<nav aria-label="Downloads for {title}"><a href="{rel}{episode['id']}.mp4" download>MP4</a>
<a href="{rel}captions.srt" download>Captions</a><a href="{rel}transcript.txt">Transcript</a>
<a href="{rel}contact-sheet.jpg">Storyboard</a></nav></article>''')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter 13 — Diagnosing retrieval failure, animated</title><style>
*{box-sizing:border-box}body{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}
main{max-width:1120px;margin:auto;padding:48px 24px}h1{font-size:clamp(36px,6vw,68px);line-height:1.08;margin:12px 0}
h2{font-size:clamp(25px,4vw,36px);line-height:1.2;margin:8px 0}.lead,article>p{color:#a8bbd8}
.kicker{letter-spacing:.14em;color:#68e0bb!important;font-size:13px;font-weight:700}
article{margin:40px 0;padding:28px;background:#1d2b50;border-radius:24px}video{display:block;width:100%;border-radius:16px;background:#101833}
nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}a{color:#68e0bb}footer{font-size:15px;color:#a8bbd8}
a:focus-visible,video:focus-visible{outline:3px solid #ffd36a;outline-offset:5px}
@media(max-width:600px){main{padding:28px 14px}article{padding:16px}}
</style></head><body><main><p class="kicker">CHAPTER 13 · HOW SEARCH DECIDES WHAT YOU SEE</p>
<h1>Find the failure.<br>Test the remedy.</h1><p class="lead">Three animated explainers about missing papers, missing meaning, and relationships lost in retrieval. Adapted from Aaron Tay's Chapter 13.</p>
<p class="lead">Original vector animation and music, English synthetic narration, and captions.</p>'''
    page += "".join(cards)
    page += '''<footer><p><a href="chapter-13-videos.zip" download>Download the complete video set</a></p>
<p><a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#diagnosing-failure">Read Chapter 13</a></p>
<p>Paper P, analysis paths, contrasting identifiers and performance bars are teaching illustrations. The BERT token pieces follow the chapter. No model was measured; remedy outcomes are not guaranteed. Missing internal traces remain unknown.</p>
<p>Adaptation credit: Aaron Tay, <em>How Search Decides What You See</em>. CC BY 4.0. Synthetic voice: Microsoft David Desktop, generated locally.</p></footer></main></body></html>'''
    (out / "preview.html").write_text(page, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", choices=["1", "2", "3", "all"], default="all")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    modes = parser.add_mutually_exclusive_group()
    for flag in ("prepare-only", "stills-only", "render-only", "verify-only", "check-only"):
        modes.add_argument("--"+flag, action="store_true")
    args = parser.parse_args()
    cfg = read_config()
    if args.check_only:
        print("Chapter source, scripts, scene coverage, and teaching examples passed.")
        return
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
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
            call_film(engine.reviews, episode, timeline, out)
        if not (args.prepare_only or args.stills_only or args.verify_only):
            call_film(engine.render, episode, timeline, out, ff)
        if not (args.prepare_only or args.stills_only):
            engine.verify(episode, timeline, out, ff)
    preview(cfg, out)
    if all((out/e["id"]/"verification.json").exists() for e in cfg["episodes"]):
        reports = [json.loads((out/e["id"]/"verification.json").read_text(encoding="utf-8")) for e in cfg["episodes"]]
        (out/"verification.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
