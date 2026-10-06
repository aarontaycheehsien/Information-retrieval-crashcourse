"""Render three narrated Chapter 14 explainers using the shared media engine."""
from __future__ import annotations

import argparse
from concurrent.futures import ProcessPoolExecutor
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
spec = importlib.util.spec_from_file_location("chapter14_media", COMMON / "render.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
sys.path.insert(0, str(HERE))
from scenes import Film, validate_examples  # noqa: E402

# Reuse the existing, entirely local Windows speech adapter.
sys.path.insert(0, str(ROOT / "tools" / "chapter-4-videos"))
import offline_voice  # noqa: E402
offline_voice.install()

DEFAULT_OUT = ROOT / "outputs" / "chapter-14-videos"
engine.Film = Film


def call_film(fn, *args):
    # Also works with the committed engine, before the newer film_class API.
    if "film_class" in inspect.signature(fn).parameters:
        return fn(*args, film_class=Film)
    return fn(*args)


def read_config():
    script = (HERE / "episodes.json").read_bytes()
    cfg = json.loads(script)
    source = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
    start = source.index('id="sec-evaluation"')
    end = source.index('id="sec-library-practice"', start)
    chapter = source[start:end]
    for required in ("Chapter 14", "Measuring whether retrieval worked", "Precision@10",
                     "Mean reciprocal rank", "Mean average precision", "nDCG", "pooling"):
        assert required in chapter, f"Chapter source changed: missing {required}"
    cfg["source_sha256"] = hashlib.sha256(chapter.encode()).hexdigest()
    production = b"".join(path.read_bytes() for path in (
        HERE / "episodes.json", HERE / "scenes.py", HERE / "render.py",
        COMMON / "render.py", COMMON / "visuals.py", ROOT / "tools/pick-a-card/narrate.py",
        ROOT / "tools/chapter-4-videos/offline_voice.py", ROOT / "tools/chapter-4-videos/synthesize.ps1"))
    cfg["production_sha256"] = hashlib.sha256(production).hexdigest()
    assert len(cfg["episodes"]) == len({e["id"] for e in cfg["episodes"]}) == 3
    for number, episode in enumerate(cfg["episodes"], 1):
        assert episode["chapter"] == 14 and episode["id"].startswith(f"{number:02d}-")
        assert len(episode["scenes"]) == len({s["id"] for s in episode["scenes"]}) == 8
        for scene in episode["scenes"]:
            assert all(scene[k].strip() for k in ("title", "claim", "narration"))
            assert scene["id"] in Film.SCENES[number], scene["id"]
            assert f'id="{scene["source_anchor"]}"' in chapter, scene["source_anchor"]
    validate_examples()
    return cfg


def prepare(cfg, episode, out, ff):
    timeline = engine.prepare(cfg, episode, out, ff)
    transcript = "\n\n".join(s["title"] + "\n" + s["narration"] for s in episode["scenes"])
    (out / episode["id"] / "transcript.txt").write_text(
        episode["title"] + "\n\n" + transcript +
        f"\n\nAdapted from Chapter 14, {cfg['book']}, by {cfg['author']}.\n"
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
                    "-metadata", "comment=Original animation and music; synthetic narration; adapted from Chapter 14 by Aaron Tay; CC BY 4.0",
                    "-t", str(duration), "-movflags", "+faststart", str(folder / (episode["id"] + ".mp4"))],
                   folder / "mux.log")
    print(f"Exported {episode['id']}.mp4", flush=True)


engine.mux = mux


def preview(cfg, out):
    cards = []
    for number, episode in enumerate(cfg["episodes"], 1):
        if not (out / episode["id"] / "timeline.json").exists():
            continue
        timeline = engine.load_timeline(out, episode)
        seconds = round(timeline["duration"])
        rel = episode["id"] + "/"
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
<title>Chapter 14 — Measuring retrieval, animated</title><style>
*{box-sizing:border-box}body{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}
main{max-width:1120px;margin:auto;padding:48px 24px}h1{font-size:clamp(36px,6vw,68px);line-height:1.08;margin:12px 0}
h2{font-size:clamp(25px,4vw,36px);line-height:1.2;margin:8px 0}.lead,article>p{color:#a8bbd8}
.kicker{letter-spacing:.14em;color:#68e0bb!important;font-size:13px;font-weight:700}
article{margin:40px 0;padding:28px;background:#1d2b50;border-radius:24px}video{display:block;width:100%;border-radius:16px;background:#101833}
nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}a{color:#68e0bb}footer{font-size:15px;color:#a8bbd8}
a:focus-visible,video:focus-visible{outline:3px solid #ffd36a;outline-offset:5px}
@media(max-width:600px){main{padding:28px 14px}article{padding:16px}}
</style></head><body><main><p class="kicker">CHAPTER 14 · HOW SEARCH DECIDES WHAT YOU SEE</p>
<h1>Did the search<br>actually work?</h1><p class="lead">Three animated explainers about precision and recall, ranking metrics, and building a local evaluation set. Adapted from Aaron Tay's Chapter 14.</p>
<p class="lead">Original vector animation and music, English synthetic narration, and captions.</p>'''
    page += "".join(cards)
    page += '''<footer><p><a href="chapter-14-videos.zip" download>Download the complete video set</a></p>
<p><a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#evaluation">Read Chapter 14</a></p>
<p>Figure 14.1 uses a controlled, complete judgement set; Table 14.3 is hypothetical. Ranking-metric examples are fully judged toy lists with stipulated relevance. Seed recovery is reported separately from absolute recall.</p>
<p>Adaptation credit: Aaron Tay, <em>How Search Decides What You See</em>. CC BY 4.0. Local synthetic voice: Microsoft David Desktop.</p></footer></main></body></html>'''
    (out / "preview.html").write_text(page, encoding="utf-8")


def render_episode(cfg, episode, out, ff, args):
    # Workers write only their own film directory; the parent owns the gallery.
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", choices=["1", "2", "3", "all"], default="all")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--jobs", type=int, choices=[1, 2, 3], default=1,
                        help="Independent film processes; use 3 to encode the set concurrently")
    modes = parser.add_mutually_exclusive_group()
    for flag in ("prepare-only", "stills-only", "render-only", "verify-only", "check-only"):
        modes.add_argument("--"+flag, action="store_true")
    args = parser.parse_args()
    cfg = read_config()
    if args.check_only:
        print("Chapter source, scripts, scene coverage, and calculated examples passed.")
        return
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    ff = engine.imageio_ffmpeg.get_ffmpeg_exe()
    episodes = cfg["episodes"] if args.episode == "all" else [cfg["episodes"][int(args.episode)-1]]
    if args.jobs == 1 or len(episodes) == 1:
        for episode in episodes:
            render_episode(cfg, episode, out, ff, args)
    else:
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(render_episode, cfg, episode, out, ff, args) for episode in episodes]
            for future in futures:
                future.result()
    preview(cfg, out)
    if all((out/e["id"]/"verification.json").exists() for e in cfg["episodes"]):
        reports = [json.loads((out/e["id"]/"verification.json").read_text(encoding="utf-8")) for e in cfg["episodes"]]
        (out/"verification.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
