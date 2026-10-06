"""Render three narrated Chapter 4 films with the repository's media engine."""
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

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMON = ROOT / "tools" / "chapter-2-videos"
sys.path.insert(0, str(COMMON))
spec = importlib.util.spec_from_file_location("chapter_four_media_engine", COMMON / "render.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
sys.path.insert(0, str(HERE))
from scenes import Film, validate_examples  # noqa: E402
import offline_voice  # noqa: E402

offline_voice.install()

DEFAULT_OUT = ROOT / "outputs" / "chapter-4-videos"


def read_config():
    cfg = json.loads((HERE / "episodes.json").read_text(encoding="utf-8"))
    source = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
    a = source.index('id="sec-beyond-boolean"')
    b = source.index('id="exercise1"', a)
    chapter = source[a:b]
    plain = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", chapter)))
    for required in ("Chapter 4", "Lexical search beyond strict Boolean", "minimum match",
                     "foolish", "A missing word can have four different histories"):
        assert required in plain, f"Source chapter changed: missing {required}"
    validate_examples(plain)
    cfg["source_sha256"] = hashlib.sha256(chapter.encode()).hexdigest()
    cfg["adaptation_sha256"] = hashlib.sha256((HERE / "episodes.json").read_bytes()).hexdigest()
    assert cfg["chapter"] == 4 and len(cfg["episodes"]) == 3
    for episode in cfg["episodes"]:
        assert episode["chapter"] == 4 and len(episode["scenes"]) == 8
        assert len({s["id"] for s in episode["scenes"]}) == 8
        assert all(s.get(key) for s in episode["scenes"] for key in ("id", "title", "claim", "narration"))
    return cfg


def mux(episode, timeline, out, ff):
    """Chapter-specific export metadata, including with the older shared engine."""
    folder = out / episode["id"]
    target = folder / (episode["id"] + ".mp4")
    duration = math.ceil(timeline["duration"] * engine.FPS) / engine.FPS
    engine.command([ff, "-y", "-v", "error", "-i", str(folder / "picture.mp4"),
                    "-i", str(folder / "soundtrack.wav"), "-i", str(folder / "captions.srt"),
                    "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text", "-disposition:s:0", "0",
                    "-metadata:s:s:0", "language=eng", "-metadata", "title=" + episode["title"],
                    "-metadata", "comment=Original animation; synthetic narration; adapted from Chapter 4 by Aaron Tay",
                    "-t", str(duration), "-movflags", "+faststart", str(target)], folder / "mux.log")
    print(f"Exported {target.name}", flush=True)


# The older committed engine uses a global class; newer engines accept a class
# argument. Support both without editing or depending on another task's changes.
engine.Film = Film
engine.mux = mux


def with_film(fn, *args):
    kwargs = {"film_class": Film} if "film_class" in inspect.signature(fn).parameters else {}
    return fn(*args, **kwargs)


def prepare(cfg, episode, out, ff):
    tl = engine.prepare(cfg, episode, out, ff)
    tl["adaptation_sha256"] = cfg["adaptation_sha256"]
    folder = out / episode["id"]
    (folder / "timeline.json").write_text(json.dumps(tl, indent=2), encoding="utf-8")
    transcript = "\n\n".join(s["title"] + "\n" + s["narration"] for s in episode["scenes"])
    (folder / "transcript.txt").write_text(episode["title"] + "\n\n" + transcript +
        f"\n\nAdapted from Chapter 4, {cfg['book']}, by {cfg['author']}.\n"
        f"Synthetic voice: {cfg['voice']['name']}.\nSource: {cfg['source']}\n", encoding="utf-8")
    return tl


def preview(cfg, out):
    cards = []
    for i, ep in enumerate(cfg["episodes"], 1):
        tl = engine.load_timeline(out, ep)
        seconds = int(round(tl["duration"]))
        rel = ep["id"] + "/"
        cards.append(f'''<article><p class="kicker">CHAPTER 4 · FILM {i:02d} · {seconds//60}:{seconds%60:02d}</p>
<h2>{html.escape(ep['title'])}</h2><p>{html.escape(ep['subtitle'])}</p>
<video aria-label="{html.escape(ep['title'])}" controls preload="metadata" poster="{rel}poster.jpg"><source src="{rel}{ep['id']}.mp4" type="video/mp4"></video>
<nav><a href="{rel}{ep['id']}.mp4" download>Download MP4</a><a href="{rel}captions.srt" download>Captions</a><a href="{rel}transcript.txt">Transcript</a><a href="{rel}contact-sheet.jpg">Storyboard</a></nav></article>''')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter 4 — Animated explainers</title><style>body{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}main{max-width:1080px;margin:auto;padding:48px 24px}h1{font-size:clamp(36px,6vw,64px);line-height:1.1;margin:12px 0}h2{font-size:32px;margin:8px 0}.lead,article>p{color:#a8bbd8}.kicker{letter-spacing:.15em;color:#68e0bb!important;font-size:13px;font-weight:700}article{margin:40px 0;padding:28px;background:#192344;border-radius:24px}video{display:block;width:100%;border-radius:16px;background:#101833}nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}a{color:#68e0bb}footer{font-size:15px;color:#a8bbd8}</style>
<main><p class="kicker">HOW SEARCH DECIDES WHAT YOU SEE</p><h1>The word went missing.<br>The search stayed lexical.</h1><p class="lead">Three colorful science explainers adapted from Chapter 4, by Aaron Tay. Original geometric animation, playful paper characters, synthetic English narration, original music and captions.</p>'''
    page += "".join(cards)
    page += '''<footer><p><a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#beyond-boolean">Read Chapter 4</a> · <a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/bm25-evidence-lab.html">Explore the Evidence Lab</a></p><p>The fruit-record order is stipulated, not calculated. Query-processing examples illustrate possible mechanisms; they do not diagnose a named product. Adaptation credit: Aaron Tay, <em>How Search Decides What You See</em>, CC BY 4.0.</p></footer></main></html>'''
    (out / "preview.html").write_text(page, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", choices=["1", "2", "3", "all"], default="all")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    modes = parser.add_mutually_exclusive_group()
    for flag in ("prepare-only", "stills-only", "render-only", "verify-only", "check"):
        modes.add_argument("--" + flag, action="store_true")
    args = parser.parse_args()
    cfg = read_config()
    if args.check:
        print("Chapter source, scripts and admission examples: passed")
        return
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    # Keep generated media out of Git without altering staged .gitignore work.
    if out == DEFAULT_OUT.resolve():
        (out / ".gitignore").write_text("*\n", encoding="utf-8")
    ff = engine.imageio_ffmpeg.get_ffmpeg_exe()
    episodes = cfg["episodes"] if args.episode == "all" else [cfg["episodes"][int(args.episode)-1]]
    for ep in episodes:
        if args.stills_only or args.render_only or args.verify_only:
            tl = engine.load_timeline(out, ep)
            assert tl["source_sha256"] == cfg["source_sha256"], "Chapter changed; prepare again"
            assert tl["adaptation_sha256"] == cfg["adaptation_sha256"], "Script changed; prepare again"
        else:
            tl = prepare(cfg, ep, out, ff)
        if not args.verify_only:
            with_film(engine.reviews, ep, tl, out)
        if not (args.prepare_only or args.stills_only or args.verify_only):
            with_film(engine.render, ep, tl, out, ff)
        if not (args.prepare_only or args.stills_only):
            report = engine.verify(ep, tl, out, ff)
            report["adaptation_sha256"] = cfg["adaptation_sha256"]
            (out/ep["id"]/"verification.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    if all((out/e["id"]/"timeline.json").exists() for e in cfg["episodes"]):
        preview(cfg, out)
    if all((out/e["id"]/"verification.json").exists() for e in cfg["episodes"]):
        reports = [json.loads((out/e["id"]/"verification.json").read_text(encoding="utf-8")) for e in cfg["episodes"]]
        (out/"verification.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
