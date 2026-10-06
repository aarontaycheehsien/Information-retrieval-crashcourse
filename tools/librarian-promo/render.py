"""Render an original, narrated cosmic science-animation textbook promotion."""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import wave

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
NAME = "how-search-decides-librarian-promo"
OUTPUT = ROOT / "outputs" / "librarian-promo"
spec = importlib.util.spec_from_file_location("promo_media", HERE.parent / "chapter-1-video" / "render.py")
media = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = media
spec.loader.exec_module(media)
media.HERE, media.NAME = HERE, NAME
SR, FPS = media.SR, media.FPS


def production_hash():
    h = hashlib.sha256()
    for p in [HERE / "render.py", HERE / "scenes.py", HERE / "script.json",
              HERE.parent / "chapter-1-video" / "render.py", HERE.parent / "pick-a-card" / "narrate.py"]:
        h.update(p.name.encode())
        h.update(p.read_bytes())
    return h.hexdigest()


def check_source(script):
    """Require the named source sections and advertised companion artifacts."""
    for scene in script["scenes"]:
        for ref in scene["sources"]:
            name, _, anchor = ref.partition("#")
            path = ROOT / name
            assert path.is_file(), f"Missing source: {ref}"
            if anchor:
                assert f'id="{anchor}"' in path.read_text(encoding="utf-8"), f"Missing anchor: {ref}"
    book = (ROOT / "search-textbook.html").read_text(encoding="utf-8")
    for claim in ["How Search Decides What You See", "No mathematics is required", "No prior knowledge of information retrieval is assumed"]:
        assert claim in book, f"Recheck the marketing claim: {claim}"
    digest = hashlib.sha256()
    for name in sorted({ref.split("#")[0] for s in script["scenes"] for ref in s["sources"]}):
        digest.update(name.encode())
        digest.update((ROOT / name).read_bytes())
    return {"source_sha256": digest.hexdigest(), "script_sha256": hashlib.sha256((HERE / "script.json").read_bytes()).hexdigest(),
            "production_sha256": production_hash()}


def wave_write(path, samples):
    assert samples.ndim == 2 and samples.shape[1] == 2
    with wave.open(str(path), "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes((np.clip(samples, -1, 1) * 32767).astype("<i2").tobytes())


def score(timeline, out):
    """Original gently propulsive oscillator score; duck under every voice take."""
    count = round(timeline["duration"] * SR)
    music = np.zeros((count, 2), dtype=np.float64)
    effects = np.zeros_like(music)
    rng = np.random.default_rng(42)

    def add(target, at, length, frequency, amplitude, pan=0, pad=False):
        first = round(at * SR)
        n = min(round(length * SR), count - first)
        if n <= 0:
            return
        t = np.arange(n) / SR
        if pad:
            env = np.minimum(t / .65, 1) * np.minimum((length - t) / .75, 1)
            signal = (np.sin(2 * math.pi * frequency * t) + .15 * np.sin(2 * math.pi * frequency * 2.003 * t)) * env
        else:
            env = (1 - np.exp(-t * 140)) * np.exp(-t * 5)
            signal = (np.sin(2 * math.pi * frequency * t) + .3 * np.sin(2 * math.pi * frequency * 2 * t) * np.exp(-t * 9)) * env
        target[first:first+n, 0] += signal * amplitude * math.sqrt((1-pan)/2)
        target[first:first+n, 1] += signal * amplitude * math.sqrt((1+pan)/2)

    def hz(midi):
        return 440 * 2 ** ((midi - 69) / 12)

    beat = .6
    chords = [(60, 64, 67, 71), (57, 60, 64, 67), (53, 57, 60, 64), (55, 59, 62, 67)]
    for bar in range(math.ceil(timeline["duration"] / (beat * 4))):
        at = bar * beat * 4
        chord = chords[(bar // 2) % 4]
        for note in chord:
            add(music, at, beat * 4 + .25, hz(note-12), .012, pad=True)
        add(music, at, 1.2, hz(chord[0]-24), .035)
        for j in range(8):
            add(music, at + j*beat/2, .9, hz(chord[[0, 2, 1, 3, 2, 1, 3, 2][j]]+12), .035, math.sin(j)*.6)
    for start, _ in timeline["scenes"].values():
        if start < .1:
            continue
        first, n = round(start*SR), round(.5*SR)
        n = min(n, count-first)
        t = np.arange(n)/SR
        noise = rng.normal(0, 1, n)
        smooth = np.convolve(noise, np.ones(12)/12, mode="same")
        effects[first:first+n] += (smooth * np.sin(math.pi*t/.5)**2 * .045)[:, None]
        add(effects, start+.12, .8, hz(84), .025)
    duck = np.ones(count)
    for take in timeline["takes"]:
        a, b = round(take["start"]*SR), round(take["end"]*SR)
        first, last = max(0, a-round(.18*SR)), min(count, b+round(.4*SR))
        duck[a:b] = .28
        if a > first:
            duck[first:a] = np.minimum(duck[first:a], np.linspace(1, .28, a-first))
        if last > b:
            duck[b:last] = np.minimum(duck[b:last], np.linspace(.28, 1, last-b))
    fade = np.minimum(np.arange(count)/(SR*.7), 1) * np.minimum((count-np.arange(count))/(SR*2.5), 1)
    wave_write(out / "music-original.wav", music*fade[:, None])
    wave_write(out / "effects-original.wav", effects)
    return (music*duck[:, None]+effects)*fade[:, None]


def prepare(script, out, ff):
    fingerprints = check_source(script)
    tl = media.voice.build(script, out, ff)
    duration = math.ceil(tl.duration*FPS)/FPS
    timeline = {"duration": duration, "scenes": {k:list(v) for k,v in tl.scenes.items()},
                "takes": [{"id":t.id,"scene":t.scene,"text":t.text,"start":t.start,"end":t.end,"words":t.words} for t in tl.takes],
                **fingerprints}
    timeline["scenes"][script["scenes"][-1]["id"]][1] = duration
    track = media.voice.voice_track(tl)
    track = np.pad(track, (0, round(duration*SR)-len(track)))
    wave_write(out / "voice-only.wav", np.repeat(track[:, None], 2, axis=1))
    mixed = np.repeat(track[:, None], 2, axis=1) + score(timeline, out)
    wave_write(out / "mix-unmastered.wav", mixed)
    media.run([ff,"-y","-i",str(out/"mix-unmastered.wav"),"-af","loudnorm=I=-16:TP=-2.5:LRA=9",
               "-ar",str(SR),str(out/"soundtrack.wav")], out/"mastering.log")
    cues = media.voice.captions(tl)
    assert all(0 <= c["start"] < c["end"] <= duration for c in cues)
    assert all(a["end"] <= b["start"] for a,b in zip(cues,cues[1:]))
    assert " ".join(c["text"] for c in cues).split() == " ".join(l["text"] for l in script["lines"]).split()
    (out/"captions.json").write_text(json.dumps(cues,indent=2),encoding="utf-8")
    for extension, separator, header in [("srt",",",""),("vtt",".","WEBVTT\n\n")]:
        lines = [f"{i}\n{media.voice.stamp(c['start'],separator)} --> {media.voice.stamp(c['end'],separator)}\n{c['text']}\n" for i,c in enumerate(cues,1)]
        (out/f"{NAME}.{extension}").write_text(header+"\n".join(lines),encoding="utf-8")
    transcript = "\n\n".join(f"[{media.voice.stamp(t.start,'.')}] {t.text}" for t in tl.takes)
    (out/"transcript.txt").write_text(f"{script['title']}\n\n{transcript}\n\nBook: {script['book_title']} — {script['author']}\n{script['book_url']}\n"
        f"Start here: {script['intro_url']}\n\nSynthetic narration: Microsoft {script['voice']['name']} via edge-tts.\n"
        "Original animation and oscillator music. Textbook adaptation: CC BY 4.0.\n",encoding="utf-8")
    (out/"timeline.json").write_text(json.dumps(timeline,indent=2),encoding="utf-8")
    print(f"Timeline ready: {duration:.2f}s; {len(cues)} caption cues",flush=True)
    return timeline


def picture_surface():
    import skia
    return skia.Surface(media.W,media.H)


media.picture_surface = picture_surface


def worker(job):
    import subprocess
    from scenes import Film
    film = Film(job["timeline"],job["script"])
    surface = picture_surface()
    buffer = np.empty((media.H,media.W,4),np.uint8)
    cmd = [job["ff"],"-y","-v","error","-f","rawvideo","-pix_fmt","bgra","-s","1920x1080","-r","30","-i","-",
           "-an","-c:v","libx264","-preset","veryfast","-crf","18","-tune","animation","-pix_fmt","yuv420p","-threads","1","-g","60",job["segment"]]
    with subprocess.Popen(cmd,stdin=subprocess.PIPE) as proc:
        try:
            for frame in range(job["first"],job["last"]):
                film.frame(surface.getCanvas(),frame/FPS)
                media.read_picture(surface,buffer)
                proc.stdin.write(memoryview(buffer).cast("B"))
        finally:
            proc.stdin.close()
        if proc.wait():
            raise RuntimeError("Video encoder failed")


media.worker = worker


def preview(timeline, script, out):
    chapters = []
    buttons = []
    for i,scene in enumerate(script["scenes"],1):
        a,b = timeline["scenes"][scene["id"]]
        chapters.append(f"{i}\n{media.voice.stamp(a,'.')} --> {media.voice.stamp(b,'.')}\n{scene['title']}\n")
        buttons.append(f'<button data-time="{a:.3f}"><span>{media.voice.stamp(a,".")[3:8]}</span>{html.escape(scene["title"])}</button>')
    (out/"chapters.vtt").write_text("WEBVTT\n\n"+"\n".join(chapters),encoding="utf-8")
    seconds = round(timeline["duration"])
    (out/"preview.html").write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>A universe of research · A textbook for librarians</title>
<style>*{{box-sizing:border-box}}body{{margin:0;background:#101035;color:#faf4df;font:16px/1.6 system-ui}}main{{max-width:1280px;margin:auto;padding:38px 24px}}
.eyebrow{{color:#63e0cd;letter-spacing:.16em;font-size:12px;font-weight:750}}h1{{font-size:clamp(32px,5vw,58px);line-height:1.1;letter-spacing:-.035em;margin:16px 0}}
p{{max-width:950px;color:#c0bfde}}video{{width:100%;border-radius:16px;background:#14143e}}a{{color:#63e0cd}}nav{{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:9px;margin:22px 0}}
button{{color:#faf4df;background:#24204c;border:1px solid #4b4383;border-radius:8px;text-align:left;padding:12px;cursor:pointer}}button:hover,button:focus-visible{{border-color:#63e0cd}}button span{{color:#63e0cd;margin-right:14px}}.credit{{font-size:13px}}</style></head>
<body><main><div class="eyebrow">AN ORIGINAL ANIMATED PROMO FOR LIBRARIANS</div><h1>A universe of research.<br>A clearer way to search.</h1>
<p>{seconds//60}:{seconds%60:02d} of colorful cosmic animation introducing Aaron Tay’s free online textbook, <em>How Search Decides What You See</em>.</p>
<video id="film" controls playsinline preload="metadata" poster="poster.jpg" src="{NAME}.mp4">
<track kind="captions" src="{NAME}.vtt" srclang="en" label="English"><track kind="chapters" src="chapters.vtt" srclang="en" label="Scenes"></video>
<nav aria-label="Jump to a scene">{''.join(buttons)}</nav>
<p><a href="{NAME}.mp4" download>Download MP4</a> · <a href="{NAME}.srt" download>English captions</a> · <a href="transcript.txt">Transcript</a></p>
<p><a href="{script['book_url']}">Read the free textbook</a> · <a href="{script['intro_url']}">Start with Read This First</a></p>
<p class="credit">Original geometric illustrations and synthesized music. Synthetic narration: Microsoft Ryan, via edge-tts.
Adapted from Aaron Tay’s textbook, CC BY 4.0. Inspired by colorful flat science animation and cosmic visual metaphors; independently produced.</p></main>
<script>const film=document.getElementById('film');document.querySelectorAll('button[data-time]').forEach(b=>b.onclick=()=>{{film.currentTime=Number(b.dataset.time);film.play().catch(()=>{{}})}});</script></body></html>''',encoding="utf-8")
    (out/"share-copy.txt").write_text(f"A convincing answer can still leave crucial evidence out.\nExplore the machinery behind search with Aaron Tay's free online textbook for librarians: {script['book_title']}.\n\nRead free: {script['book_url']}\nStart with the 45-minute guided route: {script['intro_url']}\n\nAnimated video with synthetic narration and original music.\n",encoding="utf-8")


def mux(timeline,script,out,ff):
    dest = out/f"{NAME}.mp4"
    temp = out/f"{NAME}.partial.mp4"
    media.run([ff,"-y","-i",str(out/"picture.mp4"),"-i",str(out/"soundtrack.wav"),"-i",str(out/f"{NAME}.srt"),
               "-map","0:v:0","-map","1:a:0","-map","2:0","-c:v","copy","-c:a","aac","-b:a","192k","-c:s","mov_text",
               "-ar",str(SR),"-t",str(timeline["duration"]),"-metadata",f"title={script['title']}","-metadata","artist=Aaron Tay",
               "-metadata","comment=Original animation and music; synthetic Microsoft Ryan narration",
               "-metadata:s:a:0","language=eng","-metadata:s:s:0","language=eng","-disposition:s:0","0","-movflags","+faststart",str(temp)],out/"mux.log")
    info = media.verify(temp,timeline,out,ff)
    extracted = out/"embedded-captions.srt"
    media.run([ff,"-y","-i",str(temp),"-map","0:s:0",str(extracted)],out/"caption-check.log")
    def cue_text(path):
        return [l for l in path.read_text(encoding="utf-8-sig").splitlines() if l.strip() and not l.isdigit() and " --> " not in l]
    assert cue_text(extracted) == cue_text(out/f"{NAME}.srt"), "Embedded caption mismatch"
    temp.replace(dest)
    info.update(file=dest.name,production_sha256=production_hash(),embedded_captions_verified=True,synthetic_voice=script["voice"]["name"],original_music=True)
    (out/"verification.json").write_text(json.dumps(info,indent=2),encoding="utf-8")
    return dest


def load_timeline(out,script):
    timeline = json.loads((out/"timeline.json").read_text(encoding="utf-8"))
    for key,value in check_source(script).items():
        assert timeline[key] == value, f"Stale timeline: {key}; run --prepare-only again"
    return timeline


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=OUTPUT)
    modes = parser.add_mutually_exclusive_group()
    for mode in ["prepare-only","stills-only","render-only","verify-only"]:
        modes.add_argument(f"--{mode}",action="store_true")
    parser.add_argument("--workers",type=int,default=2)
    parser.add_argument("--worker",type=Path,help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker:
        worker(json.loads(args.worker.read_text(encoding="utf-8")))
        return
    assert 1 <= args.workers <= 8
    out = args.output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    script = json.loads((HERE/"script.json").read_text(encoding="utf-8"))
    ff = os.environ.get("CHAPTER_FFMPEG") or media.imageio_ffmpeg.get_ffmpeg_exe()
    timeline = load_timeline(out,script) if args.stills_only or args.render_only or args.verify_only else prepare(script,out,ff)
    if args.prepare_only:
        return
    if args.verify_only:
        info = media.verify(out/f"{NAME}.mp4",timeline,out,ff)
        # Verify-only preserves the richer successful mux report.
        existing = json.loads((out/"verification.json").read_text(encoding="utf-8"))
        existing.update(info)
        (out/"verification.json").write_text(json.dumps(existing,indent=2),encoding="utf-8")
        return
    media.stills(timeline,script,out)
    preview(timeline,script,out)
    if args.stills_only:
        return
    media.render(timeline,script,out,ff,args.workers)
    print(f"Completed: {mux(timeline,script,out,ff)}",flush=True)


if __name__ == "__main__":
    main()
