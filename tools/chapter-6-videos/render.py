"""Render three narrated Chapter 6 films with the repository's media engine."""
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
spec = importlib.util.spec_from_file_location("chapter_six_media", COMMON / "render.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
sys.path.insert(0, str(HERE))
from scenes import Film, validate_examples  # noqa: E402

DEFAULT_OUT = ROOT / "outputs" / "chapter-6-videos"


def read_config():
    script = (HERE / "episodes.json").read_bytes()
    cfg = json.loads(script)
    source = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
    a = source.index('id="sec-retrieval-encoder"')
    b = source.index('id="sec-dense-at-scale"', a)
    chapter = source[a:b]
    for required in ("Chapter 6", "From language model to retrieval encoder", "pooling",
                     "hard negative", "SPECTER", "Ten signs that you performed well in your job interview",
                     "A history of agricultural employment", "How to recognise unrealistic expectations during a job search"):
        assert required in chapter, f"Chapter source changed: missing {required}"
    cfg["source_sha256"] = hashlib.sha256(chapter.encode()).hexdigest()
    # All prepared assets must be rebuilt after script or artwork changes.
    production = script + (HERE / "scenes.py").read_bytes() + (COMMON / "render.py").read_bytes() + (COMMON / "visuals.py").read_bytes() + (ROOT / "tools" / "pick-a-card" / "narrate.py").read_bytes()
    cfg["production_sha256"] = hashlib.sha256(production).hexdigest()
    assert len(cfg["episodes"]) == 3
    assert len({e["id"] for e in cfg["episodes"]}) == 3
    for number, episode in enumerate(cfg["episodes"], 1):
        assert episode["chapter"] == 6 and episode["id"].startswith(f"{number:02d}-")
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
<title>Chapter 6 — Animated explainers</title><style>
*{box-sizing:border-box}body{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}
main{max-width:1120px;margin:auto;padding:48px 24px}h1{font-size:clamp(36px,6vw,64px);line-height:1.08;margin:12px 0}
h2{font-size:clamp(25px,4vw,36px);line-height:1.2;margin:8px 0}.lead,article>p{color:#a8bbd8}
.kicker{letter-spacing:.14em;color:#68e0bb!important;font-size:13px;font-weight:700}
article{margin:40px 0;padding:28px;background:#1d2b50;border-radius:24px}video{display:block;width:100%;border-radius:16px;background:#101833}
nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}a{color:#68e0bb}footer{font-size:15px;color:#a8bbd8}
a:focus-visible,video:focus-visible{outline:3px solid #ffd36a;outline-offset:5px}
@media(max-width:600px){main{padding:28px 14px}article{padding:16px}}
</style></head><body><main><p class="kicker">CHAPTER 6 · HOW SEARCH DECIDES WHAT YOU SEE</p>
<h1>How a language model<br>learns to retrieve</h1><p class="lead">Three animated films adapted from Aaron Tay's Chapter 6, “From language model to retrieval encoder.” Original flat-vector animation and music, English synthetic narration, and captions.</p>'''
    page += "".join(cards)
    page += '''<footer><p><a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#retrieval-encoder">Read Chapter 6</a> · <a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#dense-at-scale">Continue to Chapter 7</a></p>
<p>Token pieces, IDs, four-dimensional vectors, moving coordinates, and scores are teaching illustrations. The animations do not report a trained model's behaviour. Relevance labels follow the stated search need.</p>
<p>Adaptation credit: Aaron Tay, <em>How Search Decides What You See</em>. CC BY 4.0. Synthetic voice: Microsoft en-GB-RyanNeural.</p></footer></main></body></html>'''
    (out / "preview.html").write_text(page, encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", choices=["1", "2", "3", "all"], default="all")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    modes = parser.add_mutually_exclusive_group()
    for flag in ("prepare-only", "stills-only", "render-only", "verify-only"):
        modes.add_argument("--"+flag, action="store_true")
    args = parser.parse_args()
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
            engine.render(episode, timeline, out, ff, film_class=Film)
        if not (args.prepare_only or args.stills_only):
            engine.verify(episode, timeline, out, ff)
    if all((out/e["id"]/"timeline.json").exists() for e in cfg["episodes"]):
        preview(cfg, out)
    if all((out/e["id"]/"verification.json").exists() for e in cfg["episodes"]):
        reports = [json.loads((out/e["id"]/"verification.json").read_text(encoding="utf-8")) for e in cfg["episodes"]]
        (out/"verification.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
