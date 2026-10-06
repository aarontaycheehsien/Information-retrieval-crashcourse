"""Create three narrated Chapter 1 films with original flat-vector animation."""
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
import re
import shutil
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont
import skia

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
COMMON = ROOT / 'tools/chapter-2-videos'
sys.path.insert(0, str(COMMON))
spec = importlib.util.spec_from_file_location('chapter1_media', COMMON / 'render.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)
sys.path.insert(0, str(HERE))
from scenes import Film  # noqa: E402

DEFAULT_OUT = ROOT / 'outputs/chapter-1-videos'
engine.Film = Film


def call_film(fn, *args):
    # Support both versions of the shared engine's original Film interface.
    if 'film_class' in inspect.signature(fn).parameters:
        return fn(*args, film_class=Film)
    return fn(*args)


def read_config():
    cfg = json.loads((HERE / 'episodes.json').read_text(encoding='utf-8'))
    source = (ROOT / 'search-textbook.html').read_text(encoding='utf-8')
    a = source.index('id="sec-intro"')
    chapter = source[a:source.index('id="sec-boolean-admission"', a)]
    for required in ('The retrieval problem', 'Chapter 1', 'up to 30', 'five abstracts',
                     '9.4 million', '35,300', '13 results', 'August 2026', 'September 2026'):
        assert required in chapter, f'Chapter changed: missing {required}'
    relevance = chapter[chapter.index('<h3 id="what-does-relevant-actually-mean"'):
                        chapter.index('<h3 id="three-familiar-search-results-and-three-puzzles"')]
    for required in ('Queries, filters and task briefs', 'large language models', '2024 onwards',
                     'positive participant reactions', 'short demonstration', 'workshop',
                     'answer accuracy', 'staff workload', 'actual research consultations',
                     'not wholly irrelevant', 'operational evidence', 'experienced usefulness'):
        assert required in relevance, f'Relevance example changed: missing {required}'
    cfg['source_sha256'] = hashlib.sha256(chapter.encode()).hexdigest()
    cfg['production_sha256'] = hashlib.sha256(b''.join(p.read_bytes() for p in (
        HERE / 'episodes.json', HERE / 'render.py', HERE / 'scenes.py',
        COMMON / 'render.py', COMMON / 'visuals.py', ROOT / 'tools/pick-a-card/narrate.py'))).hexdigest()
    assert len(cfg['episodes']) == 3
    used, lines = [], {line['id']: line for line in cfg['lines']}
    assert len(lines) == len(cfg['lines'])
    for i, episode in enumerate(cfg['episodes'], 1):
        assert episode['chapter'] == 1 and episode['id'].startswith(f'{i:02d}-')
        assert {s['id'] for s in episode['scenes']} == Film.SCENES[i]
        for scene in episode['scenes']:
            assert f'id="{scene["source_anchor"]}"' in chapter
            assert scene['narration'] == ' '.join(lines[k]['text'] for k in scene['line_ids'])
            assert all(lines[k]['scene'] == scene['id'] for k in scene['line_ids'])
            used.extend(scene['line_ids'])
    assert used == [line['id'] for line in cfg['lines']], 'Every narration take must appear once, in order'
    return cfg


def seed_cached_voice(cfg, lines, folder):
    # Read the previous adaptation's cache; never write to its files or exports.
    existing = ROOT / 'outputs/chapter-1-video'
    for line in lines:
        request = engine.narrate.request_for(line, cfg['voice'])
        src = engine.narrate.cache_dir(existing, request)
        dest = engine.narrate.cache_dir(folder, request)
        if all((src / name).is_file() for name in ('speech.mp3', 'events.json')):
            dest.mkdir(parents=True, exist_ok=True)
            for name in ('speech.mp3', 'events.json', 'request.json'):
                if (src / name).exists() and not (dest / name).exists():
                    shutil.copy2(src / name, dest / name)


def prepare(cfg, episode, out, ff):
    folder = out / episode['id']
    folder.mkdir(parents=True, exist_ok=True)
    ids = {k for s in episode['scenes'] for k in s['line_ids']}
    lines = [dict(line) for line in cfg['lines'] if line['id'] in ids]
    lines[0]['gap'] = 0
    seed_cached_voice(cfg, lines, folder)
    tl = engine.narrate.build({'voice': cfg['voice'], 'lead_in': 1.0, 'tail': 3.0, 'lines': lines}, folder, ff)
    cues = engine.narrate.captions(tl)
    assert all(0 <= c['start'] < c['end'] <= tl.duration for c in cues)
    assert all(a['end'] <= b['start'] for a, b in zip(cues, cues[1:]))
    timeline = {'duration': tl.duration, 'scenes': tl.scenes, 'cues': cues,
                'takes': [{'id': t.id, 'scene': t.scene, 'start': t.start, 'end': t.end,
                           'words': t.words, 'cache_key': t.cache_key} for t in tl.takes],
                'voice': cfg['voice'], 'source_sha256': cfg['source_sha256'],
                'production_sha256': cfg['production_sha256']}
    (folder / 'timeline.json').write_text(json.dumps(timeline, indent=2), encoding='utf-8')
    (folder / 'captions.srt').write_text('\n'.join(
        f"{i}\n{engine.narrate.stamp(c['start'], ',')} --> {engine.narrate.stamp(c['end'], ',')}\n{c['text']}\n"
        for i, c in enumerate(cues, 1)), encoding='utf-8')
    (folder / 'captions.vtt').write_text('WEBVTT\n\n' + '\n'.join(
        f"{engine.narrate.stamp(c['start'], '.')} --> {engine.narrate.stamp(c['end'], '.')}\n{c['text']}\n"
        for c in cues), encoding='utf-8')
    (folder / 'transcript.txt').write_text(episode['title'] + '\n\n' + '\n\n'.join(
        s['title'] + '\n' + s['narration'] for s in episode['scenes']) +
        f"\n\nAdapted from Chapter 1 of {cfg['book']}, by {cfg['author']}.\n"
        f"{cfg['book_url']}\nCC BY 4.0. Original animation and synthesized music.\n"
        f"Synthetic narrator: Microsoft {cfg['voice']['name']} via edge-tts.\n", encoding='utf-8')
    (folder / 'storyboard.json').write_text(json.dumps(episode, indent=2), encoding='utf-8')
    duration = math.ceil(tl.duration * engine.FPS) / engine.FPS
    voice = engine.narrate.voice_track(tl).astype(np.float32)
    voice = np.pad(voice, (0, round(duration * engine.narrate.SR) - len(voice)))
    music = engine.music_track(duration, tl)
    margins = {}
    for take in tl.takes:
        a, b = round(take.start * engine.narrate.SR), round(take.end * engine.narrate.SR)
        vrms = float(np.sqrt(np.mean(voice[a:b] ** 2)))
        mrms = float(np.sqrt(np.mean(music[a:b] ** 2)))
        margins[take.id] = 20 * math.log10(vrms / max(mrms, 1e-9))
    assert min(margins.values()) >= 10, 'Music obscures a narration take'
    (folder / 'mix-balance.json').write_text(json.dumps({
        'worst_voice_over_music_db': round(min(margins.values()), 2), 'take_margins_db': margins}, indent=2), encoding='utf-8')
    for name, signal in [('voice', voice), ('music', music), ('mix', voice[:, None] + music)]:
        engine.write_wav(folder / (name + '.wav'), signal)
    log = engine.command([ff, '-hide_banner', '-i', str(folder / 'mix.wav'), '-af',
        'loudnorm=I=-16:TP=-2.5:LRA=11:print_format=json', '-f', 'null', '-'], folder / 'loudness-analysis.log')
    m = json.loads(re.findall(r'\{\s*"input_i"[\s\S]*?\}', log)[-1])
    filt = (f"loudnorm=I=-16:TP=-2.5:LRA=11:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
            f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    engine.command([ff, '-y', '-v', 'error', '-i', str(folder / 'mix.wav'), '-af', filt,
        '-ar', '48000', '-c:a', 'pcm_s16le', str(folder / 'soundtrack.wav')], folder / 'master.log')
    print(f"Prepared {episode['id']}: {tl.duration:.2f}s; {len(cues)} captions", flush=True)
    return timeline


def reviews(episode, timeline, out):
    folder = out / episode['id']
    film, surface = Film(episode, timeline), skia.Surface(1920, 1080)
    count = len(episode['scenes'])
    sheet = Image.new('RGB', (1280, math.ceil(count / 2) * 396), '#101833')
    d = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 19)
    for i, scene in enumerate(episode['scenes']):
        a, b = timeline['scenes'][scene['id']]
        for fraction in (.08, .52, .88):
            pixels = engine.draw_frame(film, surface, a + (b-a) * fraction)
            image = Image.fromarray(pixels[:, :, :3])
            image.save(folder / f"scene-{i+1:02d}-{scene['id']}-{int(fraction*100):02d}.jpg", quality=92)
            if fraction == .52:
                x, y = (i % 2) * 640, (i // 2) * 396
                sheet.paste(image.resize((640, 360), Image.Resampling.LANCZOS), (x, y))
                d.text((x+12, y+367), f"{i+1:02d}  {scene['title']}", font=font, fill='white')
    sheet.save(folder / 'contact-sheet.jpg', quality=92)
    image = engine.draw_frame(film, surface, 9.0, cues=False)
    Image.fromarray(image[:, :, :3]).save(folder / 'poster.jpg', quality=94)


def preview(cfg, out):
    cards = []
    for number, episode in enumerate(cfg['episodes'], 1):
        folder = out / episode['id']
        if not (folder / 'timeline.json').exists():
            continue
        timeline = engine.load_timeline(out, episode)
        seconds, rel = round(timeline['duration']), episode['id'] + '/'
        title = html.escape(episode['title'])
        cards.append(f'''<article><p class="kicker">FILM {number:02d} · {seconds//60}:{seconds%60:02d}</p>
<h2>{title}</h2><p>{html.escape(episode['subtitle'])}</p>
<video aria-label="{title}" controls playsinline preload="metadata" poster="{rel}poster.jpg">
<source src="{rel}{episode['id']}.mp4" type="video/mp4">
<track kind="captions" src="{rel}captions.vtt" srclang="en" label="English"></video>
<nav aria-label="Downloads for {title}"><a href="{rel}{episode['id']}.mp4" download>MP4</a>
<a href="{rel}captions.srt" download>Captions</a><a href="{rel}transcript.txt">Transcript</a>
<a href="{rel}contact-sheet.jpg">Storyboard</a></nav></article>''')
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chapter 1 — The retrieval problem, animated</title><style>
*{box-sizing:border-box}body{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}
main{max-width:1120px;margin:auto;padding:48px 24px}h1{font-size:clamp(36px,6vw,68px);line-height:1.08;margin:12px 0}
h2{font-size:clamp(25px,4vw,36px);line-height:1.2;margin:8px 0}.lead,article>p{color:#a8bbd8}
.kicker{letter-spacing:.14em;color:#68e0bb!important;font-size:13px;font-weight:700}
article{margin:40px 0;padding:28px;background:#1d2b50;border-radius:24px}video{display:block;width:100%;border-radius:16px;background:#101833}
nav{display:flex;gap:20px;flex-wrap:wrap;margin-top:20px}a{color:#68e0bb}footer{font-size:15px;color:#a8bbd8}
a:focus-visible,video:focus-visible{outline:3px solid #ffd36a;outline-offset:5px}
@media(max-width:600px){main{padding:28px 14px}article{padding:16px}}
</style></head><body><main><p class="kicker">CHAPTER 1 · HOW SEARCH DECIDES WHAT YOU SEE</p>
<h1>Before the answer,<br>there was a search.</h1><p class="lead">Three animated explainers about the sources behind an AI answer, the gap between matching and relevance, and three puzzles hidden in familiar search boxes.</p>
<p class="lead">Original flat-vector artwork, synthetic English narration, a quiet musical score, and captions. Adapted from Aaron Tay's Chapter 1.</p>'''
    page += ''.join(cards)
    page += f'''<footer><p><a href="chapter-1-videos.zip" download>Download the complete video set</a></p>
<p><a href="{html.escape(cfg['book_url'])}">Read Chapter 1</a></p>
<p>Product examples reproduce the chapter's observations and documentation: August–September 2026. They are not new product tests. The three puzzles leave internal mechanisms open.</p>
<p>Adaptation credit: Aaron Tay, <em>How Search Decides What You See</em>. CC BY 4.0. Synthetic narrator: Microsoft Andrew Multilingual Neural. Original animation and synthesized music.</p></footer></main></body></html>'''
    (out / 'preview.html').write_text(page, encoding='utf-8')


def render_episode(cfg, episode, out, ff, args):
    if args.render_only or args.stills_only or args.verify_only:
        timeline = engine.load_timeline(out, episode)
        assert timeline['source_sha256'] == cfg['source_sha256'], 'Chapter changed; prepare again'
        assert timeline['production_sha256'] == cfg['production_sha256'], 'Production changed; prepare again'
    else:
        timeline = prepare(cfg, episode, out, ff)
    if not args.verify_only:
        reviews(episode, timeline, out)
    if not (args.prepare_only or args.stills_only or args.verify_only):
        call_film(engine.render, episode, timeline, out, ff)
    if not (args.prepare_only or args.stills_only):
        folder = out / episode['id']
        engine.command([ff, '-hide_banner', '-xerror', '-i', str(folder / (episode['id'] + '.mp4')),
                        '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'], folder / 'strict-decode.log')
        report = engine.verify(episode, timeline, out, ff)
        report['production_sha256'] = cfg['production_sha256']
        (out / episode['id'] / 'verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--episode', choices=['1', '2', '3', 'all'], default='all')
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    parser.add_argument('--jobs', type=int, choices=[1, 2, 3], default=1)
    modes = parser.add_mutually_exclusive_group()
    for flag in ('check-only', 'prepare-only', 'stills-only', 'render-only', 'verify-only'):
        modes.add_argument('--' + flag, action='store_true')
    args = parser.parse_args()
    cfg = read_config()
    if args.check_only:
        print('Chapter source, narration order, anchors, and scene coverage passed.')
        return
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=True)
    ff = engine.imageio_ffmpeg.get_ffmpeg_exe()
    episodes = cfg['episodes'] if args.episode == 'all' else [cfg['episodes'][int(args.episode)-1]]
    if args.jobs == 1 or len(episodes) == 1:
        for episode in episodes:
            render_episode(cfg, episode, out, ff, args)
    else:
        with ProcessPoolExecutor(max_workers=args.jobs) as pool:
            futures = [pool.submit(render_episode, cfg, episode, out, ff, args) for episode in episodes]
            for future in futures:
                future.result()
    preview(cfg, out)
    reports = []
    for episode in cfg['episodes']:
        path = out / episode['id'] / 'verification.json'
        if path.exists():
            report = json.loads(path.read_text(encoding='utf-8'))
            if report.get('production_sha256') == cfg['production_sha256']:
                reports.append(report)
    if len(reports) == 3:
        (out / 'verification.json').write_text(json.dumps(reports, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
