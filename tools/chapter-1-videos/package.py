"""Package verified Chapter 1 films, captions, scripts and browser gallery."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile
import render


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=render.DEFAULT_OUT)
    args = parser.parse_args()
    out, cfg = args.output.resolve(), render.read_config()
    files = [out / 'verification.json']
    for episode in cfg['episodes']:
        folder = out / episode['id']
        timeline = json.loads((folder / 'timeline.json').read_text(encoding='utf-8'))
        report = json.loads((folder / 'verification.json').read_text(encoding='utf-8'))
        for key in ('source_sha256', 'production_sha256'):
            assert timeline[key] == report[key] == cfg[key], 'Source or production changed; rebuild first'
        media = folder / (episode['id'] + '.mp4')
        with media.open('rb') as handle:
            assert hashlib.file_digest(handle, 'sha256').hexdigest() == report['sha256'], 'Media changed after verification'
        assert report['full_decode'] == report['embedded_captions'] == 'passed'
        files.extend(folder / name for name in (media.name, 'captions.srt', 'captions.vtt',
            'transcript.txt', 'storyboard.json', 'contact-sheet.jpg', 'poster.jpg', 'verification.json'))
    if (out / 'player-verification.json').exists():
        files.append(out / 'player-verification.json')
    assert all(path.is_file() for path in files)
    target = out / 'chapter-1-videos.zip'
    with zipfile.ZipFile(target, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(out), compress_type=zipfile.ZIP_STORED
                          if path.suffix in ('.mp4', '.jpg') else zipfile.ZIP_DEFLATED)
        page = (out / 'preview.html').read_text(encoding='utf-8').replace(
            '<p><a href="chapter-1-videos.zip" download>Download the complete video set</a></p>', '')
        archive.writestr('preview.html', page)
        archive.writestr('READ-ME.txt', 'Chapter 1: The retrieval problem\n\n'
            'Three narrated 1080p films adapted from Aaron Tay, How Search Decides What You See.\n'
            'Original flat-vector artwork and synthesized music; Microsoft Andrew neural synthetic narration.\n'
            'Captions are burnt in, embedded, and supplied as SRT/VTT.\n'
            'Open an MP4 in a video player, or serve this folder locally to use preview.html.\n'
            'Product observations and documentation retain the chapter dates, August-September 2026.\n'
            'Credit Aaron Tay and the book. CC BY 4.0.\n' + cfg['book_url'] + '\n')
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None, 'Archive CRC failed'
    print(f'Packaged and CRC-checked {target} ({target.stat().st_size/1e6:.1f} MB)')


if __name__ == '__main__':
    main()
