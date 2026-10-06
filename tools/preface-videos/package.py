"""Package completed Preface MP4s and their reader-facing companions."""
import argparse
import hashlib
import json
from pathlib import Path
import zipfile

import render


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=render.DEFAULT_OUT)
    args = parser.parse_args()
    out, cfg = args.output.resolve(), render.read_config()
    files = [out / "verification.json"]
    for episode in cfg["episodes"]:
        folder = out / episode["id"]
        timeline = json.loads((folder / "timeline.json").read_text(encoding="utf-8"))
        report = json.loads((folder / "verification.json").read_text(encoding="utf-8"))
        assert timeline["source_sha256"] == cfg["source_sha256"], "Source changed; rebuild first"
        assert timeline["production_sha256"] == cfg["production_sha256"], "Production changed; rebuild first"
        media = folder / (episode["id"] + ".mp4")
        with media.open("rb") as handle:
            assert hashlib.file_digest(handle, "sha256").hexdigest() == report["sha256"], "Media changed after verification"
        assert report["production_sha256"] == cfg["production_sha256"], "Media production changed; rebuild first"
        assert report["source_sha256"] == cfg["source_sha256"], "Media source changed; rebuild first"
        assert report["full_decode"] == report["embedded_captions"] == "passed"
        files.extend(folder / name for name in (media.name, "captions.srt", "captions.vtt",
                    "transcript.txt", "storyboard.json", "contact-sheet.jpg", "poster.jpg", "verification.json"))
    if (out / "player-verification.json").exists():
        files.append(out / "player-verification.json")
    assert all(path.is_file() for path in files)
    target = out / "preface-videos.zip"
    with zipfile.ZipFile(target, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(out), compress_type=zipfile.ZIP_STORED if path.suffix in (".mp4", ".jpg") else zipfile.ZIP_DEFLATED)
        page = (out / "preview.html").read_text(encoding="utf-8")
        page = page.replace('<p><a href="preface-videos.zip" download>Download the complete video set</a></p>', '')
        archive.writestr("preview.html", page)
        archive.writestr("READ-ME.txt", "Preface: Why this book exists\n\n"
            "Three narrated 1080p animated explainers, adapted from Aaron Tay's How Search Decides What You See.\n"
            "Open an MP4 in your video player, or serve this directory locally to use preview.html.\n"
            "Captions are burnt in, embedded, and supplied as SRT/VTT. The web caption track is optional.\n"
            "Original artwork and music; offline Microsoft David Desktop synthetic narration.\n"
            "Credit Aaron Tay and the book. CC BY 4.0.\n"
            "Source: https://aarontaycheehsien.github.io/Information-retrieval-crashcourse/search-textbook.html#preface\n")
    with zipfile.ZipFile(target) as archive:
        assert archive.testzip() is None, "Archive CRC failed"
    print(f"Packaged and CRC-checked {target} ({target.stat().st_size/1e6:.1f} MB)")


if __name__ == "__main__":
    main()
