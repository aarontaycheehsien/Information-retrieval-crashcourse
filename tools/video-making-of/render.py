"""Render a source-grounded retrospective about the earlier Chapter 1 films."""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import math
from pathlib import Path
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PREVIOUS = ROOT / 'tools/chapter-1-videos'
sys.path.insert(0, str(PREVIOUS))
spec = importlib.util.spec_from_file_location('makingof_shared', PREVIOUS / 'render.py')
shared = importlib.util.module_from_spec(spec)
spec.loader.exec_module(shared)
sys.path.insert(0, str(HERE))
from film import Film  # noqa: E402
shared.Film = shared.engine.Film = Film

DEFAULT_OUT = ROOT / 'outputs/video-making-of'
SOURCE_PATHS = [PREVIOUS / name for name in ('README.md', 'episodes.json', 'render.py',
                'scenes.py', 'test-examples.py', 'check-preview.cjs', 'package.py')]


def read_config():
    cfg = json.loads((HERE / 'script.json').read_text(encoding='utf-8'))
    old = json.loads((PREVIOUS / 'episodes.json').read_text(encoding='utf-8'))
    assert len(old['episodes']) == 3 and len(old['lines']) == 47
    assert old['voice']['name'] == 'en-US-AndrewMultilingualNeural'
    assert sum(len(e['scenes']) for e in old['episodes']) == 15
    episode = cfg['episode']
    assert len(episode['scenes']) == 8
    assert {s['id'] for s in episode['scenes']} == Film.SCENES
    assert all(s['title'] and s['claim'] and s['evidence'] and s['narration'] for s in episode['scenes'])
    for scene in episode['scenes']:
        scene['line_ids'] = [scene['id']]
    cfg['lines'] = [{'id': s['id'], 'scene': s['id'], 'text': s['narration'], 'gap': .8} for s in episode['scenes']]
    cfg['source_sha256'] = hashlib.sha256(b''.join(p.read_bytes() for p in SOURCE_PATHS) +
        (HERE / 'provenance.json').read_bytes()).hexdigest()
    production = [HERE / name for name in ('script.json', 'render.py', 'film.py')]
    production += [HERE / 'assets' / f'film-{i}.jpg' for i in (1, 2, 3)]
    production += [ROOT / 'tools/chapter-2-videos' / name for name in ('render.py', 'visuals.py')]
    production += [PREVIOUS / 'render.py', ROOT / 'tools/pick-a-card/narrate.py']
    sys.path.insert(0, str(ROOT / 'tools/chapter-4-videos'))
    import offline_voice
    offline_voice.install()
    assert cfg['voice']['name'] == 'Microsoft David Desktop'
    production += [ROOT / 'tools/chapter-4-videos' / name for name in ('offline_voice.py', 'synthesize.ps1')]
    cfg['production_sha256'] = hashlib.sha256(b''.join(p.read_bytes() for p in production) +
        json.dumps(cfg['voice'], sort_keys=True).encode()).hexdigest()
    return cfg


def mux(episode, timeline, out, ff):
    folder = out / episode['id']
    duration = math.ceil(timeline['duration'] * shared.engine.FPS) / shared.engine.FPS
    shared.engine.command([ff, '-y', '-v', 'error', '-i', str(folder / 'picture.mp4'),
        '-i', str(folder / 'soundtrack.wav'), '-i', str(folder / 'captions.srt'),
        '-map', '0:v', '-map', '1:a', '-map', '2:s', '-c:v', 'copy', '-c:a', 'aac',
        '-b:a', '192k', '-c:s', 'mov_text', '-disposition:s:0', '0',
        '-metadata:s:s:0', 'language=eng', '-metadata', 'title=' + episode['title'],
        '-metadata', 'comment=Production retrospective; original animation and music; local synthetic narration; Aaron Tay Chapter 1 adaptation; CC BY 4.0',
        '-t', str(duration), '-movflags', '+faststart', str(folder / (episode['id'] + '.mp4'))], folder / 'mux.log')
    print('Exported ' + episode['id'] + '.mp4', flush=True)


shared.engine.mux = mux


def prepare(cfg, out, ff):
    timeline = shared.prepare(cfg, cfg['episode'], out, ff)
    folder = out / cfg['episode']['id']
    transcript = cfg['episode']['title'] + '\n\n' + '\n\n'.join(
        scene['title'] + '\n' + scene['narration'] for scene in cfg['episode']['scenes'])
    transcript += (f"\n\nProduction retrospective about Aaron Tay's Chapter 1 animated adaptation. CC BY 4.0.\n"
        f"Current film's synthetic narrator: {cfg['voice']['name']}.\n"
        'The earlier films reused 47 Andrew neural voice takes; this retrospective uses new narration.\n'
        'The model/effort description is supplied by the user. The process account follows saved production files.\n\n'
        'Official OpenAI documentation for model support and the meaning of reasoning effort:\n'
        'https://developers.openai.com/api/docs/models/gpt-6.1-sol\n'
        'https://developers.openai.com/api/docs/guides/reasoning\n\n'
        'Local production evidence:\n' + '\n'.join(str(p.relative_to(ROOT)) for p in SOURCE_PATHS) + '\n')
    (folder / 'transcript.txt').write_text(transcript, encoding='utf-8')
    return timeline


def preview(cfg, out):
    episode = cfg['episode']
    timeline = shared.engine.load_timeline(out, episode)
    seconds, rel = round(timeline['duration']), episode['id'] + '/'
    title = html.escape(episode['title'])
    (out / 'preview.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title><style>
*{{box-sizing:border-box}}body{{margin:0;background:#101833;color:#f7f3df;font:18px/1.55 system-ui}}
main{{max-width:1120px;margin:auto;padding:48px 24px}}h1{{font-size:clamp(36px,6vw,66px);line-height:1.08}}
.kicker{{color:#68e0bb;letter-spacing:.13em;font-size:13px;font-weight:700}}.lead,footer{{color:#a8bbd8}}
article{{padding:24px;background:#1d2b50;border-radius:24px}}video{{display:block;width:100%;border-radius:16px;background:#101833}}
nav{{display:flex;gap:22px;flex-wrap:wrap;margin-top:22px}}a{{color:#68e0bb}}footer{{font-size:15px;margin-top:30px}}
a:focus-visible,video:focus-visible{{outline:3px solid #ffd36a;outline-offset:5px}}
@media(max-width:600px){{main{{padding:28px 14px}}article{{padding:14px}}}}
</style></head><body><main><p class="kicker">BEHIND THE ANIMATION · {seconds//60}:{seconds%60:02d}</p>
<h1>{title}</h1><p class="lead">A high-level account of how the earlier Chapter 1 films went from source material to a checked, playable animation.</p>
<article><video aria-label="{title}" controls playsinline preload="metadata" poster="{rel}poster.jpg">
<source src="{rel}{episode['id']}.mp4" type="video/mp4"><track kind="captions" src="{rel}captions.vtt" srclang="en" label="English"></video>
<nav aria-label="Downloads"><a href="{rel}{episode['id']}.mp4" download>Download video</a>
<a href="how-codex-built-the-videos.zip" download>Complete bundle</a><a href="{rel}captions.srt">Captions</a>
<a href="{rel}transcript.txt">Transcript and sources</a><a href="{rel}contact-sheet.jpg">Storyboard</a></nav></article>
<footer><p>The model and effort description follows your requested setup: GPT-6.1 Sol, Extra High. The workflow follows the saved scripts, drawings, and checks for the earlier films.</p>
<p>Reasoning effort guides the model's work on a task. See the official <a href="https://developers.openai.com/api/docs/guides/reasoning">OpenAI reasoning guide</a> and <a href="https://developers.openai.com/api/docs/models/gpt-6.1-sol">GPT-6.1 Sol model page</a>.</p>
<p>Earlier films: 47 cached Andrew neural narration takes. This retrospective: new synthetic narration using {html.escape(cfg['voice']['name'])}. Original artwork and synthesized music.</p>
<p>Credit: Aaron Tay, <em>How Search Decides What You See</em>, Chapter 1. CC BY 4.0.</p></footer></main></body></html>''', encoding='utf-8')


def package(cfg, out):
    episode, folder = cfg['episode'], out / cfg['episode']['id']
    report = json.loads((folder / 'verification.json').read_text(encoding='utf-8'))
    for key in ('source_sha256', 'production_sha256'):
        assert report[key] == cfg[key], 'Source or production changed; rebuild first'
    media = folder / (episode['id'] + '.mp4')
    with media.open('rb') as stream:
        assert hashlib.file_digest(stream, 'sha256').hexdigest() == report['sha256']
    files = [folder / name for name in (media.name, 'captions.srt', 'captions.vtt', 'transcript.txt',
             'storyboard.json', 'contact-sheet.jpg', 'poster.jpg', 'verification.json')]
    target = out / 'how-codex-built-the-videos.zip'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(out), compress_type=zipfile.ZIP_STORED
                          if path.suffix in ('.mp4', '.jpg') else zipfile.ZIP_DEFLATED)
        page = (out / 'preview.html').read_text(encoding='utf-8').replace(
            '<a href="how-codex-built-the-videos.zip" download>Complete bundle</a>', '')
        archive.writestr('preview.html', page)
        archive.write(HERE / 'provenance.json', 'provenance.json')
        if (out / 'player-verification.json').exists():
            archive.write(out / 'player-verification.json', 'player-verification.json')
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None
    print(f'Packaged and CRC-checked {target.name} ({target.stat().st_size/1e6:.1f} MB)', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUT)
    modes = parser.add_mutually_exclusive_group()
    for flag in ('check-only', 'prepare-only', 'stills-only', 'render-only', 'verify-only', 'package-only'):
        modes.add_argument('--' + flag, action='store_true')
    args = parser.parse_args()
    cfg, out = read_config(), args.output.resolve()
    if args.check_only:
        print('Earlier production evidence, narration, and scene coverage passed.')
        return
    if args.package_only:
        package(cfg, out)
        return
    out.mkdir(parents=True, exist_ok=True)
    ff, episode = shared.engine.imageio_ffmpeg.get_ffmpeg_exe(), cfg['episode']
    if args.render_only or args.stills_only or args.verify_only:
        timeline = shared.engine.load_timeline(out, episode)
        for key in ('source_sha256', 'production_sha256'):
            assert timeline[key] == cfg[key], 'Source or production changed; prepare again'
    else:
        timeline = prepare(cfg, out, ff)
    if not args.verify_only:
        shared.reviews(episode, timeline, out)
    if not (args.prepare_only or args.stills_only or args.verify_only):
        shared.call_film(shared.engine.render, episode, timeline, out, ff)
    if not (args.prepare_only or args.stills_only):
        folder = out / episode['id']
        shared.engine.command([ff, '-hide_banner', '-xerror', '-i', str(folder / (episode['id'] + '.mp4')),
            '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-'], folder / 'strict-decode.log')
        report = shared.engine.verify(episode, timeline, out, ff)
        report['production_sha256'] = cfg['production_sha256']
        (folder / 'verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
        (out / 'verification.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
    preview(cfg, out)


if __name__ == '__main__':
    main()
