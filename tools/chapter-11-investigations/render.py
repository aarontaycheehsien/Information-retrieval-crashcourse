"""Render three original experiment-led films from the pinned more-readable Chapter 11."""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.metadata
import importlib.util
import json
import math
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import zipfile

import numpy as np
import skia

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEFAULT_OUTPUT = ROOT / "outputs" / "chapter-11-investigations"
spec = importlib.util.spec_from_file_location("chapter11_media", HERE.parent / "chapter-1-video" / "render.py")
media = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = media
spec.loader.exec_module(media)
media.HERE = HERE
media.voice.ENGINE = "edge-tts-" + importlib.metadata.version("edge-tts")


def configure_speech():
    # Trust the managed environment's CA while retaining TLS verification.
    import edge_tts.communicate
    certificate = os.environ.get("CODEX_PROXY_CERT")
    if certificate:
        edge_tts.communicate._SSL_CTX.load_verify_locations(certificate)
    proxy = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if proxy:
        from functools import partial
        edge_tts.Communicate = partial(edge_tts.Communicate, proxy=proxy)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def production_hash():
    h = hashlib.sha256()
    for path in [HERE / "render.py", HERE / "scenes.py", HERE / "facts.py", HERE / "plots.py", HERE / "episodes.json",
                 HERE / "source-chapter.html", HERE / "source-provenance.json",
                 HERE.parent / "pre-chapter-1-investigations" / "scenes.py",
                 HERE.parent / "chapter-1-video" / "render.py",
                 HERE.parent / "pick-a-card" / "narrate.py"]:
        h.update(path.name.encode())
        h.update(path.read_bytes())
    return h.hexdigest()


def check_source(script):
    provenance = json.loads((HERE / "source-provenance.json").read_text())
    book = (HERE / "source-chapter.html").read_text()
    assert digest(HERE / "source-chapter.html") == provenance["chapter_sha256"]
    chapter_text = " ".join(html.unescape(re.sub(r"<[^>]+>", "", book)).split())
    for phrase in ["495 included sources", "30%", "51%", "Query2doc", "HyDE", "screening feedback", "six OR-connected permutations", "GPT-4.1 Mini", "does not identify the model as an LLM", "fixed and non-agentic", "weighted vocabulary representation", "PY=(2020-2024) AND OG_SMART=(university of california) AND TS=(apple) AND TS=(oranges) AND TS=(bananas)"]:
        assert phrase.casefold() in chapter_text.casefold(), f"Recheck source: {phrase}"
    from lxml import html as lx
    from facts import QUERY_OBJECTS, RECEIVERS, GENERATED_TEXT, check_examples
    doc = lx.fromstring(book)
    for anchor, expected in [("tbl-11-1", QUERY_OBJECTS), ("tbl-11-2", RECEIVERS)]:
        table=doc.xpath(f'//*[@id="{anchor}"]/following::table[1]')[0]
        values=[" ".join(row.xpath('./td')[0].text_content().split()) for row in table.xpath('.//tr') if row.xpath('./td')]
        assert values==list(expected), (anchor, values)
    assert GENERATED_TEXT in chapter_text, "Source hypothetical wording changed"
    check_examples()
    for scene in script["scenes"]:
        assert f'id="{scene["source_anchor"]}"' in book, scene["source_anchor"]
    assert script["source_commit"] == provenance["commit"]
    return {
        "source": script["source"], "source_commit": provenance["commit"],
        "source_sha256": provenance["source_sha256"],
        "chapter_sha256": provenance["chapter_sha256"],
        # Compatibility with the existing media verifier's source field.
        "relevance_source_sha256": provenance["chapter_sha256"],
        "script_sha256": digest(HERE / "episodes.json"),
        "production_sha256": production_hash(),
    }


media.check_source = check_source


def load_scripts():
    series = json.loads((HERE / "episodes.json").read_text())
    scripts = []
    for index, ep in enumerate(series["episodes"], 1):
        script = {k: v for k, v in series.items() if k != "episodes"}
        script.update(ep, episode_number=index, lead_in=0.7, tail=3.0)
        lines = []
        for scene in script["scenes"]:
            for i, text in enumerate(scene["narration"]):
                lines.append({"id": f"{scene['id']}_{i}", "scene": scene["id"], "text": text,
                              "gap": scene.get("pause_before_second", .65) if i else 1.0})
        script["lines"] = lines
        scripts.append(script)
    return series, scripts


def prepare(script, out, ff):
    from plots import ensure_plots
    plot_directory = out.parent / "plots"
    plot_hash = ensure_plots(plot_directory)
    configure_speech()
    media.NAME = script["id"]
    tl = media.prepare(script, out, ff)
    tl["plot_directory"] = str(plot_directory)
    tl["plot_manifest_sha256"] = plot_hash
    tl["production_sha256"] = production_hash()
    (out / "timeline.json").write_text(json.dumps(tl, indent=2))
    (out / "storyboard.json").write_text(json.dumps(script, indent=2))
    transcript = "\n\n".join(f"[{media.voice.stamp(t['start'], '.')}]: {t['text']}" for t in tl["takes"])
    credit = (f"Adapted from Aaron Tay, How Search Decides What You See, Chapter 11.\n"
              f"Source: more-readable, commit {script['source_commit']}\n{script['book_url']}\n"
              "CC BY 4.0. Original narration adaptation and animated teaching illustrations.\n"
              "Synthetic voice: Microsoft Andrew Multilingual; no voice cloning.\n"
              "Independently produced; no affiliation with Veritasium.\n")
    (out / "transcript.txt").write_text(f"{script['title']}\n\n{transcript}\n\n{credit}")
    return tl


def load_timeline(script, out):
    tl = json.loads((out / "timeline.json").read_text())
    for k, value in check_source(script).items():
        assert tl[k] == value, f"Stale prepared timeline: {k}; run --prepare-only"
    from plots import verify_plots
    verify_plots(tl["plot_directory"], tl["plot_manifest_sha256"])
    return tl


def picture_surface():
    return skia.Surface(media.W, media.H)


media.picture_surface = picture_surface


def worker(job):
    from scenes import Film
    from facts import check_examples
    check_examples()
    film = Film(job["timeline"], job["script"])
    surface = picture_surface()
    buffer = np.empty((media.H, media.W, 4), np.uint8)
    command = [job["ff"], "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
               "-s", "1920x1080", "-r", "30", "-i", "-", "-an", "-c:v", "libx264",
               "-preset", "veryfast", "-crf", "19", "-tune", "zerolatency",
               "-pix_fmt", "yuv420p", "-threads", "1", "-g", "60", job["segment"]]
    with subprocess.Popen(command, stdin=subprocess.PIPE) as process:
        try:
            for frame in range(job["first"], job["last"]):
                film.frame(surface.getCanvas(), frame / media.FPS)
                media.read_picture(surface, buffer)
                process.stdin.write(memoryview(buffer).cast("B"))
        finally:
            process.stdin.close()
        if process.wait():
            raise RuntimeError("Frame encoding failed")


def mux(script, tl, out, ff):
    media.NAME = script["id"]
    target = out / f"{script['id']}.mp4"
    partial = target.with_suffix(".partial.mp4")
    media.run([ff, "-y", "-i", str(out / "picture.mp4"), "-i", str(out / "narration.wav"),
               "-i", str(out / f"{script['id']}.srt"), "-map", "0:v", "-map", "1:a", "-map", "2:0",
               "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-c:s", "mov_text",
               "-ar", "48000", "-t", str(tl["duration"]), "-metadata", f"title={script['title']}",
               "-metadata", "comment=Adapted from Aaron Tay; original animation; CC BY 4.0",
               "-metadata:s:a:0", "language=eng", "-metadata:s:s:0", "language=eng",
               "-movflags", "+faststart", str(partial)], out / "mux.log")
    report = media.verify(partial, tl, out, ff)
    extracted = out / "embedded-captions.srt"
    media.run([ff, "-y", "-i", str(partial), "-map", "0:s:0", str(extracted)], out / "caption-check.log")
    def cue_text(path):
        return [line for line in path.read_text(encoding="utf-8-sig").splitlines()
                if line.strip() and not line.isdigit() and " --> " not in line]
    assert cue_text(extracted) == cue_text(out / f"{script['id']}.srt")
    partial.replace(target)
    report.pop("relevance_source_sha256")
    report.update(file=target.name, chapter_sha256=tl["chapter_sha256"],
                  source_commit=script["source_commit"], production_sha256=production_hash(),
                  embedded_captions_verified=True)
    (out / "verification.json").write_text(json.dumps(report, indent=2))
    return report


def check_timeline(script, tl, out):
    assert list(tl["scenes"]) == [s["id"] for s in script["scenes"]]
    cues = json.loads((out / "captions.json").read_text())
    assert all(0 <= c["start"] < c["end"] <= tl["duration"] for c in cues)
    assert all(a["end"] <= b["start"] for a, b in zip(cues, cues[1:]))
    # Reconstruct every spoken word; this catches omitted narration and bad timing maps.
    normal = media.voice.normalized
    assert normal(" ".join(c["text"] for c in cues)) == normal(" ".join(t["text"] for t in tl["takes"]))
    for take in tl["takes"]:
        assert take["words"] and take["start"] < take["end"]
        assert normal("".join(w["text"] for w in take["words"])) == normal(take["text"])
        assert all(take["start"] <= w["start"] < w["end"] <= take["end"] for w in take["words"])
    assert [(t["id"], t["text"]) for t in tl["takes"]] == [(t["id"], t["text"]) for t in script["lines"]]
    from scenes import Film
    film = Film(tl, script)
    surface = picture_surface()
    # Layout bounds are asserted by the drawing primitive. Include every reveal and transition.
    times = {0., tl["duration"] - .01}
    for a, b in tl["scenes"].values():
        times.update(a + (b-a)*f for f in (.01, .15, .4, .7, .95))
    for take in tl["takes"]:
        times.update([take["start"], take["start"]+.2, take["end"]-.01])
    for t in sorted(times):
        film.frame(surface.getCanvas(), t)
    from facts import check_examples
    return {"caption_cues": len(cues), "reviewed_animation_times": len(times), "worked_examples": check_examples(), "passed": True}


def gallery(series, scripts, dest):
    panels = []
    for script in scripts:
        folder = dest / script["id"]
        if not (folder / "timeline.json").exists():
            continue
        tl = json.loads((folder / "timeline.json").read_text())
        duration = f"{int(tl['duration']//60)}:{int(tl['duration']%60):02d}"
        ident = script["id"]
        chapters = []
        buttons = []
        for scene in script["scenes"]:
            start, end = tl["scenes"][scene["id"]]
            chapters.append(f"{media.voice.stamp(start, '.')} --> {media.voice.stamp(end, '.')}\n{scene['title']}\n")
            buttons.append(f'<button data-film="film-{script["episode_number"]}" data-time="{start:.3f}">'
                           f'<span>{int(start//60)}:{int(start%60):02d}</span>{html.escape(scene["title"])}</button>')
        (folder / "chapters.vtt").write_text("WEBVTT\n\n" + "\n".join(chapters))
        panels.append(f'''<article id="episode-{script['episode_number']}">
          <div class="number">FILM {script['episode_number']:02d} · {duration}</div>
          <h2>{html.escape(script['title'])}</h2><p>{html.escape(script['subtitle'])}</p>
          <video id="film-{script['episode_number']}" controls playsinline preload="metadata" poster="{ident}/poster.jpg" src="{ident}/{ident}.mp4">
            <track kind="captions" src="{ident}/{ident}.vtt" srclang="en" label="English">
            <track kind="chapters" src="{ident}/chapters.vtt" srclang="en" label="Scenes">
          </video><details><summary>Jump to a scene</summary><nav>{''.join(buttons)}</nav></details>
          <p class="downloads"><a href="{ident}/{ident}.mp4" download>Download MP4</a>
            <a href="{ident}/{ident}.srt" download>SRT captions</a>
            <a href="{ident}/transcript.txt">Transcript</a>
            <a href="{ident}/contact-sheet.jpg">Storyboard</a></p></article>''')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Understanding, transforming and routing queries · Three films</title><style>
*{box-sizing:border-box}body{margin:0;background:#eee9e0;color:#252728;font:17px/1.65 system-ui,sans-serif}
main{max-width:1140px;margin:auto;padding:60px 28px}header{max-width:850px;margin-bottom:65px}
.eyebrow,.number{font-weight:750;font-size:12px;letter-spacing:.16em;color:#a34230}
h1{font-size:clamp(44px,7vw,82px);line-height:1.03;letter-spacing:-.055em;margin:18px 0 28px}
h2{font-size:clamp(27px,4vw,42px);line-height:1.14;letter-spacing:-.035em;margin:10px 0}
p{max-width:880px}a{color:#88402e;text-underline-offset:4px}article{margin:0 0 74px}
video{display:block;width:100%;aspect-ratio:16/9;background:#252728;border-radius:8px;margin-top:24px}
.downloads{display:flex;flex-wrap:wrap;gap:10px 26px;font-size:14px}summary{cursor:pointer;margin:14px 0}
nav{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:8px}
button{font:inherit;font-size:14px;text-align:left;padding:12px;background:#faf8f3;border:1px solid #ccc3b5;border-radius:4px;cursor:pointer}
button span{color:#a34230;display:inline-block;width:46px}button:hover,button:focus-visible{outline:2px solid #a34230}
footer{border-top:1px solid #ccc3b5;padding-top:24px;font-size:13px;color:#615f59}
@media(max-width:600px){main{padding:32px 15px}header{margin-bottom:44px}.downloads{gap:8px 18px}}
</style><main><header><div class="eyebrow">HOW SEARCH DECIDES WHAT YOU SEE · CHAPTER 11</div>
<h1>What did<br>you ask search?</h1><p>Three narrated investigations into query objects, rewritten requests, feedback, and imagined documents used to find real sources.
Adapted from Chapter 11 of Aaron Tay's <em>How Search Decides What You See</em>.</p>
<p><a href="chapter-11-videos.zip" download>Download the complete series</a> · <a href="SOURCE.md">Source and production notes</a></p>
<p class="downloads"><a href="plots/query-objects.svg">Query objects</a><a href="plots/generated-paths.svg">Generated retrieval aids</a><a href="plots/query-objects.csv" download>Reference data</a></p></header>'''
    page += "".join(panels)
    page += f'''<footer><p>Adapted from <a href="{series['book_url']}">Aaron Tay, <em>How Search Decides What You See</em>, Chapter 11</a>.
CC BY 4.0. Source branch: more-readable, commit {series['source_commit'][:12]}.</p>
<p>Original animated teaching illustrations and script adaptation. Synthetic narration: Microsoft Andrew Multilingual.
Independently produced; no affiliation with Veritasium. Curiosity-driven questions, prediction pauses and evidence-led reveals.
The query-object distinctions, structured-query example and hypothetical retrieval text follow the pinned chapter. Generated text is a retrieval aid, not evidence. Product accounts are documentation snapshots; diagrams do not claim new service tests or model measurements.</p></footer></main>
<script>document.querySelectorAll('button[data-film]').forEach(b=>b.onclick=()=>{{const v=document.getElementById(b.dataset.film);v.currentTime=Number(b.dataset.time);v.play().catch(()=>{{}})}});</script></html>'''
    (dest / "index.html").write_text(page)
    shutil.copy2(HERE / "source-provenance.json", dest / "source-provenance.json")
    (dest / "SOURCE.md").write_text((HERE / "README.md").read_text())


def package(dest, scripts):
    included = [dest / n for n in ["index.html", "SOURCE.md", "source-provenance.json", "verification.json"]]
    included.extend(p for p in [dest / "browser-verification.json", dest / "gallery-1440.png",
                               dest / "gallery-768.png", dest / "gallery-390.png"] if p.is_file())
    included.extend(sorted((dest / "plots").iterdir()))
    for script in scripts:
        folder = dest / script["id"]
        load_timeline(script, folder)
        report = json.loads((folder / "verification.json").read_text())
        assert report["passed"] and report["production_sha256"] == production_hash()
        assert digest(folder / report["file"]) == report["sha256"]
        included.extend(folder / n for n in [report["file"], f"{script['id']}.srt", f"{script['id']}.vtt",
                                            "transcript.txt", "storyboard.json", "poster.jpg", "contact-sheet.jpg",
                                            "verification.json", "chapters.vtt"])
    archive = dest / "chapter-11-videos.zip"
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_STORED) as z:
        for path in included:
            z.write(path, path.relative_to(dest))
    with zipfile.ZipFile(archive) as z:
        assert z.testzip() is None
    print(f"Packaged: {archive} ({archive.stat().st_size/1e6:.1f} MB)", flush=True)


def aggregate_reports(dest, scripts):
    reports = [json.loads(p.read_text()) for s in scripts if (p := dest / s["id"] / "verification.json").is_file()]
    if reports:
        (dest / "verification.json").write_text(json.dumps({"films": reports, "passed": all(r["passed"] for r in reports)}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--episode", type=int, choices=(1, 2, 3))
    parser.add_argument("--workers", type=int, default=3, choices=range(1, 5))
    modes = parser.add_mutually_exclusive_group()
    for mode in ["prepare-only", "render-only", "stills-only", "verify-only", "package-only"]:
        modes.add_argument(f"--{mode}", action="store_true")
    parser.add_argument("--worker", type=Path, help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        worker(json.loads(args.worker.read_text()))
        return
    series, all_scripts = load_scripts()
    scripts = [s for s in all_scripts if args.episode is None or s["episode_number"] == args.episode]
    dest = args.output.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    if args.package_only:
        gallery(series, all_scripts, dest)
        aggregate_reports(dest, all_scripts)
        package(dest, all_scripts)
        return
    ff = os.environ.get("CHAPTER_FFMPEG") or shutil.which("ffmpeg") or media.imageio_ffmpeg.get_ffmpeg_exe()
    reports = []
    for script in scripts:
        print(f"\nFilm {script['episode_number']}: {script['title']}", flush=True)
        out = dest / script["id"]
        out.mkdir(exist_ok=True)
        media.NAME = script["id"]
        if args.render_only or args.stills_only or args.verify_only:
            tl = load_timeline(script, out)
        else:
            tl = prepare(script, out, ff)
        if args.prepare_only:
            continue
        checks = check_timeline(script, tl, out)
        if args.verify_only:
            report = media.verify(out / f"{script['id']}.mp4", tl, out, ff)
            reports.append(report)
            continue
        media.stills(tl, script, out)
        if args.stills_only:
            continue
        media.render(tl, script, out, ff, args.workers)
        report = mux(script, tl, out, ff)
        report.update(checks)
        (out / "verification.json").write_text(json.dumps(report, indent=2))
        reports.append(report)
    gallery(series, all_scripts, dest)
    if reports:
        aggregate_reports(dest, all_scripts)
    if len(reports) == 3 and not args.verify_only:
        package(dest, all_scripts)


if __name__ == "__main__":
    main()
