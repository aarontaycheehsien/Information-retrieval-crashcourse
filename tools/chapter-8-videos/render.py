"""Render three original narrated Chapter 8 films using the shared media engine."""
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
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMON = ROOT / "tools" / "chapter-2-videos"
sys.path.insert(0, str(COMMON))
spec = importlib.util.spec_from_file_location("chapter8_media", COMMON / "render.py")
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
sys.path.insert(0, str(HERE))
from scenes import Film, validate_examples  # noqa: E402

DEFAULT_OUT = ROOT / "outputs" / "chapter-8-videos"
# Compatibility with the committed shared engine and its explicit film-class API.
engine.Film = Film


def call_film(fn, *args):
    return fn(*args, film_class=Film) if "film_class" in inspect.signature(fn).parameters else fn(*args)


def read_config():
    script = (HERE / "episodes.json").read_bytes()
    cfg = json.loads(script)
    source = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
    a = source.index('id="sec-representations-and-units"')
    b = source.index('id="sec-reranking-and-hybrid"', a)
    chapter = source[a:b]
    for required in ("Chapter 8", "Representations and indexed units", "heart attack treatment",
                     "SPLADE", "WordPiece", "50 overlapping", "result aggregation"):
        assert required.lower() in chapter.lower(), f"Chapter changed: missing {required}"
    cfg["source_sha256"] = hashlib.sha256(chapter.encode()).hexdigest()
    files = [HERE / "render.py", HERE / "scenes.py", COMMON / "render.py",
             COMMON / "visuals.py", ROOT / "tools" / "pick-a-card" / "narrate.py"]
    cfg["production_sha256"] = hashlib.sha256(script + b"".join(p.read_bytes() for p in files)).hexdigest()
    assert len(cfg["episodes"]) == len({e["id"] for e in cfg["episodes"]}) == 3
    for n, episode in enumerate(cfg["episodes"], 1):
        assert episode["chapter"] == 8 and episode["id"].startswith(f"{n:02d}-")
        assert len(episode["scenes"]) == len({s["id"] for s in episode["scenes"]}) == 8
        assert all(s[k].strip() for s in episode["scenes"] for k in ("title", "claim", "narration"))
    validate_examples()
    return cfg


def mux(episode, timeline, out, ff):
    folder = out / episode["id"]
    duration = math.ceil(timeline["duration"] * engine.FPS) / engine.FPS
    engine.command([ff, "-y", "-v", "error", "-i", str(folder / "picture.mp4"),
                    "-i", str(folder / "soundtrack.wav"), "-i", str(folder / "captions.srt"),
                    "-map", "0:v", "-map", "1:a", "-map", "2:s", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text", "-disposition:s:0", "0",
                    "-metadata:s:s:0", "language=eng", "-metadata", "title=" + episode["title"],
                    "-metadata", "comment=Original animation and music; synthetic narration; adapted from Chapter 8 by Aaron Tay",
                    "-t", str(duration), "-movflags", "+faststart", str(folder / (episode["id"] + ".mp4"))],
                   folder / "mux.log")
    print(f"Exported {episode['id']}.mp4", flush=True)


engine.mux = mux


def preview(cfg, out):
    cards = []
    for n, episode in enumerate(cfg["episodes"], 1):
        timeline = engine.load_timeline(out, episode)
        seconds = round(timeline["duration"])
        rel, title = episode["id"] + "/", html.escape(episode["title"])
        cards.append(f'''<article><p class="kicker">FILM {n:02d} · {seconds//60}:{seconds%60:02d}</p>
<h2>{title}</h2><p>{html.escape(episode['subtitle'])}</p>
<video aria-label="{title}" controls playsinline preload="metadata" poster="{rel}poster.jpg">
<source src="{rel}{episode['id']}.mp4" type="video/mp4">
<track kind="captions" src="{rel}captions.vtt" srclang="en" label="English"></video>
<nav aria-label="Downloads for {title}"><a href="{rel}{episode['id']}.mp4" download>Download MP4</a>
<a href="{rel}captions.srt" download>Captions</a><a href="{rel}transcript.txt">Transcript</a>
<a href="{rel}contact-sheet.jpg">Storyboard</a></nav></article>''')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter 8 — Animated explainers</title><style>
*{box-sizing:border-box}body{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}
main{max-width:1120px;margin:auto;padding:48px 24px}h1{font-size:clamp(36px,6vw,64px);line-height:1.08;margin:12px 0}
h2{font-size:clamp(25px,4vw,36px);line-height:1.2;margin:8px 0}.lead,article>p{color:#a8bbd8}
.kicker{letter-spacing:.14em;color:#68e0bb!important;font-size:13px;font-weight:700}
article{margin:40px 0;padding:28px;background:#1d2b50;border-radius:24px}video{display:block;width:100%;border-radius:16px;background:#101833}
nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}a{color:#68e0bb}footer{font-size:15px;color:#a8bbd8}
a:focus-visible,video:focus-visible{outline:3px solid #ffd36a;outline-offset:5px}
@media(max-width:600px){main{padding:28px 14px}article{padding:16px}}
</style></head><body><main><p class="kicker">CHAPTER 8 · HOW SEARCH DECIDES WHAT YOU SEE</p>
<h1>The numbers, the words,<br>and the pieces.</h1><p class="lead">Three animated films adapted from Aaron Tay's Chapter 8, “Representations and indexed units.” Original flat-vector animation and music, English synthetic narration, and captions.</p>
<p><a href="chapter-8-videos.zip" download>Download all three films, captions, and transcripts</a></p>'''
    page += "".join(cards)
    page += '''<footer><p><a href="https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#representations-and-units">Read Chapter 8</a></p>
<p>Dense coordinates and learnt expansion weights are teaching illustrations, not measured model output. Whole-word expansion labels are schematic; SPLADE uses its own vocabulary. Grouping chunks by source does not specify a score-combination rule.</p>
<p>Adaptation credit: Aaron Tay, <em>How Search Decides What You See</em>. CC BY 4.0. Original artwork and music. Synthetic voice: Microsoft en-GB-RyanNeural.</p></footer></main></body></html>'''
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
    # Keep generated media out of Git without changing the shared root ignore file.
    (out / ".gitignore").write_text("*\n", encoding="utf-8")
    cfg, ff = read_config(), engine.imageio_ffmpeg.get_ffmpeg_exe()
    episodes = cfg["episodes"] if args.episode == "all" else [cfg["episodes"][int(args.episode)-1]]
    for episode in episodes:
        folder = out / episode["id"]
        if args.stills_only or args.render_only or args.verify_only:
            timeline = engine.load_timeline(out, episode)
            assert timeline["source_sha256"] == cfg["source_sha256"], "Chapter changed; prepare again"
            assert timeline["production_sha256"] == cfg["production_sha256"], "Production changed; prepare again"
        else:
            timeline = engine.prepare(cfg, episode, out, ff)
            timeline["production_sha256"] = cfg["production_sha256"]
            (folder / "timeline.json").write_text(json.dumps(timeline, indent=2), encoding="utf-8")
            # The committed older shared engine hard-codes Chapter 2's transcript credit.
            transcript = "\n\n".join(s["title"] + "\n" + s["narration"] for s in episode["scenes"])
            (folder / "transcript.txt").write_text(episode["title"] + "\n\n" + transcript +
                "\n\nAdapted from Chapter 8, How Search Decides What You See, by Aaron Tay.\n"
                "CC BY 4.0. Synthetic voice: Microsoft en-GB-RyanNeural. Original animation and music.\n", encoding="utf-8")
        if not args.verify_only:
            call_film(engine.reviews, episode, timeline, out)
        if not (args.prepare_only or args.stills_only or args.verify_only):
            call_film(engine.render, episode, timeline, out, ff)
        if not (args.prepare_only or args.stills_only):
            engine.verify(episode, timeline, out, ff)
    if all((out/e["id"]/"timeline.json").exists() for e in cfg["episodes"]):
        preview(cfg, out)
    if all((out/e["id"]/"verification.json").exists() for e in cfg["episodes"]):
        reports = [json.loads((out/e["id"]/"verification.json").read_text(encoding="utf-8")) for e in cfg["episodes"]]
        (out/"verification.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")
        with zipfile.ZipFile(out / "chapter-8-videos.zip", "w", zipfile.ZIP_STORED) as archive:
            for path in (out / "preview.html", out / "verification.json"):
                archive.write(path, path.relative_to(out))
            for episode in cfg["episodes"]:
                folder = out / episode["id"]
                for name in (episode["id"] + ".mp4", "captions.srt", "captions.vtt", "transcript.txt",
                             "contact-sheet.jpg", "poster.jpg", "verification.json"):
                    archive.write(folder / name, (folder / name).relative_to(out))


if __name__ == "__main__":
    main()
