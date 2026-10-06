"""Generate three narrated 1080p Chapter 5 films and a local video gallery."""
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
spec = importlib.util.spec_from_file_location("chapter5_media_engine", COMMON / "render.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
sys.path.insert(0, str(HERE))
from scenes import Film  # noqa: E402

DEFAULT_OUT = ROOT / "outputs" / "chapter-5-videos"
# Support the committed Chapter 2 engine and its newer explicit film-class API.
engine.Film = Film


def call_film(fn, *args):
    return fn(*args, film_class=Film) if "film_class" in inspect.signature(fn).parameters else fn(*args)


def read_config():
    cfg = json.loads((HERE / "episodes.json").read_text(encoding="utf-8"))
    source = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
    start = source.index('id="sec-embeddings"')
    end = source.index('id="sec-retrieval-encoder"', start)
    chapter = source[start:end]
    for required in ("Chapter 5", "distributional hypothesis", "Skip-gram", "pooling", "self-supervised", "retrieval-oriented training"):
        assert required in chapter, f"Chapter source changed: missing {required}"
    cfg["source_sha256"] = hashlib.sha256(chapter.encode()).hexdigest()
    assert len(cfg["episodes"]) == 3
    for episode in cfg["episodes"]:
        assert episode["chapter"] == 5 and len(episode["scenes"]) == 8
        assert len({s["id"] for s in episode["scenes"]}) == 8
        assert all(s["title"] and s["claim"] and s["narration"] for s in episode["scenes"])
    return cfg


def prepare(cfg, episode, out, ff):
    timeline = engine.prepare(cfg, episode, out, ff)
    # Correct source credit even when running with the original Chapter 2 engine.
    transcript = "\n\n".join(s["title"] + "\n" + s["narration"] for s in episode["scenes"])
    (out / episode["id"] / "transcript.txt").write_text(
        episode["title"] + "\n\n" + transcript +
        f"\n\nAdapted from Chapter 5, {cfg['book']}, by {cfg['author']}.\n"
        f"Synthetic voice: {cfg['voice']['name']}. Original animation and music.\n", encoding="utf-8")
    timeline["script_sha256"] = hashlib.sha256(json.dumps(episode, sort_keys=True).encode()).hexdigest()
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
                    "-metadata", "comment=Original animation and music; synthetic narration; adapted from Chapter 5 by Aaron Tay",
                    "-t", str(duration), "-movflags", "+faststart", str(folder / (episode["id"] + ".mp4"))],
                   folder / "mux.log")
    print(f"Exported {episode['id']}.mp4", flush=True)


engine.mux = mux


def preview(cfg, out):
    cards = []
    for i, episode in enumerate(cfg["episodes"], 1):
        folder = out / episode["id"]
        if not (folder / "timeline.json").exists():
            continue
        tl = engine.load_timeline(out, episode)
        sec = round(tl["duration"])
        rel = episode["id"] + "/"
        cards.append(f'''<article><p class="kicker">FILM {i:02d} · {sec//60}:{sec%60:02d}</p>
<h2>{html.escape(episode['title'])}</h2><p>{html.escape(episode['subtitle'])}</p>
<video aria-label="{html.escape(episode['title'])}" controls playsinline preload="metadata" poster="{rel}poster.jpg">
<source src="{rel}{episode['id']}.mp4" type="video/mp4">
<track kind="captions" src="{rel}captions.vtt" srclang="en" label="English"></video>
<nav><a href="{rel}{episode['id']}.mp4" download>Download MP4</a><a href="{rel}captions.srt" download>Captions</a>
<a href="{rel}transcript.txt">Transcript</a><a href="{rel}contact-sheet.jpg">Storyboard</a></nav></article>''')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter 5 · Embeddings, animated</title><style>
*{box-sizing:border-box}body{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}
main{max-width:1120px;margin:auto;padding:52px 24px}h1{font-size:clamp(40px,7vw,76px);line-height:1.05;margin:18px 0 24px}
h2{font-size:clamp(25px,4vw,38px);line-height:1.2;margin:8px 0}.lead,article>p{color:#a8bbd8}
.kicker{letter-spacing:.16em;color:#68e0bb!important;font-size:13px;font-weight:700}
article{margin:42px 0;padding:28px;background:#1d2b50;border-radius:26px}video{display:block;width:100%;border-radius:16px;background:#101833}
nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}a{color:#68e0bb}a:focus-visible{outline:3px solid #ffd36a;outline-offset:5px}
footer{font-size:15px;color:#a8bbd8}@media(max-width:600px){main{padding:30px 16px}article{padding:18px}}
</style></head><body><main><p class="kicker">HOW SEARCH DECIDES WHAT YOU SEE · CHAPTER 5</p>
<h1>A map made<br>from language.</h1><p class="lead">Three animated explainers about embeddings: how training shapes the map, how context changes a word, and why knowing language is not the same as ranking answers.</p>
<p class="lead">Adapted from Aaron Tay's book. Original geometric animation and music, British English synthetic narration, and captions.</p>'''
    page += "".join(cards)
    page += '''<footer><p><a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#embeddings">Read Chapter 5</a> · <a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/vector-similarity-lab.html">Explore the Vector Similarity Lab</a></p>
<p>Maps and coordinates are schematic, not plotted from trained models. The token split is a toy example. Credit Aaron Tay and the book when sharing these CC BY 4.0 adaptations.</p></footer></main></body></html>'''
    (out / "preview.html").write_text(page, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", choices=["1", "2", "3", "all"], default="all")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    modes = parser.add_mutually_exclusive_group()
    for flag in ("prepare-only", "stills-only", "render-only", "verify-only"):
        modes.add_argument("--" + flag, action="store_true")
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    cfg, ff = read_config(), engine.imageio_ffmpeg.get_ffmpeg_exe()
    episodes = cfg["episodes"] if args.episode == "all" else [cfg["episodes"][int(args.episode)-1]]
    for episode in episodes:
        if args.stills_only or args.render_only or args.verify_only:
            tl = engine.load_timeline(out, episode)
            assert tl["source_sha256"] == cfg["source_sha256"], "Chapter changed; prepare again"
            assert tl["script_sha256"] == hashlib.sha256(json.dumps(episode, sort_keys=True).encode()).hexdigest(), "Script changed; prepare again"
        else:
            tl = prepare(cfg, episode, out, ff)
        if not args.verify_only:
            call_film(engine.reviews, episode, tl, out)
        if not (args.prepare_only or args.stills_only or args.verify_only):
            call_film(engine.render, episode, tl, out, ff)
        if not (args.prepare_only or args.stills_only):
            engine.verify(episode, tl, out, ff)
    preview(cfg, out)
    if all((out/e["id"]/"verification.json").exists() for e in cfg["episodes"]):
        reports = [json.loads((out/e["id"]/"verification.json").read_text(encoding="utf-8")) for e in cfg["episodes"]]
        (out / "verification.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
