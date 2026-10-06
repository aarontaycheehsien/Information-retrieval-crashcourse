"""Render the three Chapter 3 BM25 explainers using the existing media engine."""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMON = ROOT / "tools" / "chapter-2-videos"
sys.path.insert(0, str(COMMON))
spec = importlib.util.spec_from_file_location("chapter_video_engine", COMMON / "render.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
sys.path.insert(0, str(HERE))
from scenes import Film, validate_math  # noqa: E402

DEFAULT_OUT = ROOT / "outputs" / "chapter-3-videos"


def read_config():
    cfg = json.loads((HERE / "episodes.json").read_text(encoding="utf-8"))
    source = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
    a, b = source.index('id="sec-bm25-ranking"'), source.index('id="sec-beyond-boolean"')
    chapter = source[a:b]
    for required in ("Chapter 3", "BM25 and ranked lexical retrieval", "1.375", "2.2", "top-", "same inverted index"):
        assert required in chapter, f"Source chapter changed: missing {required}"
    cfg["source_sha256"] = hashlib.sha256(chapter.encode()).hexdigest()
    assert len(cfg["episodes"]) == 3
    for e in cfg["episodes"]:
        assert e["chapter"] == 3 and len(e["scenes"]) == 8
        assert len({s["id"] for s in e["scenes"]}) == 8
    validate_math()
    return cfg


def preview(cfg, out):
    cards = []
    for i, ep in enumerate(cfg["episodes"], 1):
        tl = engine.load_timeline(out, ep)
        seconds = int(round(tl["duration"]))
        rel = ep["id"] + "/"
        cards.append(f'''<article><p class="kicker">CHAPTER 3 · FILM {i:02d} · {seconds//60}:{seconds%60:02d}</p>
<h2>{html.escape(ep['title'])}</h2><p>{html.escape(ep['subtitle'])}</p>
<video aria-label="{html.escape(ep['title'])}" controls preload="metadata" poster="{rel}poster.jpg"><source src="{rel}{ep['id']}.mp4" type="video/mp4"></video>
<nav><a href="{rel}{ep['id']}.mp4" download>Download MP4</a><a href="{rel}captions.srt" download>Captions</a><a href="{rel}transcript.txt">Transcript</a><a href="{rel}contact-sheet.jpg">Storyboard</a></nav></article>''')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter 3 — Animated explainers</title><style>body{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}main{max-width:1080px;margin:auto;padding:48px 24px}h1{font-size:clamp(36px,6vw,64px);line-height:1.1;margin:12px 0}h2{font-size:32px;margin:8px 0}.lead,article>p{color:#a8bbd8}.kicker{letter-spacing:.15em;color:#68e0bb!important;font-size:13px;font-weight:700}article{margin:40px 0;padding:28px;background:#192344;border-radius:24px}video{display:block;width:100%;border-radius:16px;background:#101833}nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}a{color:#68e0bb}footer{font-size:15px;color:#a8bbd8}</style>
<main><p class="kicker">HOW SEARCH DECIDES WHAT YOU SEE</p><h1>What earns a place<br>at the top?</h1><p class="lead">Three animated explainers adapted from Chapter 3: BM25 and ranked lexical retrieval, by Aaron Tay. Original vector animation and music, English synthetic narration, and captions.</p>'''
    page += "".join(cards)
    page += '''<footer><p><a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#bm25-ranking">Read Chapter 3</a> · <a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/bm25-evidence-lab.html">Explore the BM25 Evidence Lab</a></p><p>Scores use an illustrative single-field BM25 with positive IDF. Production variants, analysers and extra ranking signals can change results.</p></footer></main></html>'''
    (out / "preview.html").write_text(page, encoding="utf-8")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--episode", choices=["1", "2", "3", "all"], default="all")
    p.add_argument("--output", type=Path, default=DEFAULT_OUT)
    for flag in ("prepare-only", "stills-only", "render-only", "verify-only"):
        p.add_argument("--" + flag, action="store_true")
    args = p.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    cfg, ff = read_config(), engine.imageio_ffmpeg.get_ffmpeg_exe()
    episodes = cfg["episodes"] if args.episode == "all" else [cfg["episodes"][int(args.episode)-1]]
    for ep in episodes:
        if args.stills_only or args.render_only or args.verify_only:
            tl = engine.load_timeline(out, ep)
            assert tl["source_sha256"] == cfg["source_sha256"], "Chapter changed; prepare the episode again"
        else:
            tl = engine.prepare(cfg, ep, out, ff)
        if not args.verify_only:
            engine.reviews(ep, tl, out, film_class=Film)
        if not (args.prepare_only or args.stills_only or args.verify_only):
            engine.render(ep, tl, out, ff, film_class=Film)
        if not (args.prepare_only or args.stills_only):
            engine.verify(ep, tl, out, ff)
    if all((out/e["id"]/"timeline.json").exists() for e in cfg["episodes"]):
        preview(cfg, out)
    if all((out/e["id"]/"verification.json").exists() for e in cfg["episodes"]):
        reports = [json.loads((out/e["id"]/"verification.json").read_text(encoding="utf-8")) for e in cfg["episodes"]]
        (out/"verification.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
