"""Audit the encoded film against source frames, transitions, captions and motion."""
from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import subprocess

import numpy as np
from PIL import Image, ImageDraw

import render
from scenes import Film


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output",type=Path,default=render.OUTPUT)
    args = parser.parse_args()
    out = args.output.resolve()
    script = json.loads((render.HERE/"script.json").read_text(encoding="utf-8"))
    tl = render.load_timeline(out,script)
    film = Film(tl,script)
    ff = os.environ.get("CHAPTER_FFMPEG") or render.media.imageio_ffmpeg.get_ffmpeg_exe()
    surface = render.picture_surface()
    buf = np.empty((1080,1920,4),np.uint8)

    def source(at):
        film.frame(surface.getCanvas(),at)
        render.media.read_picture(surface,buf)
        return buf[..., [2,1,0]].copy()

    # Cover the transitions and every spoken word used to trigger an animation.
    times = {0.,tl["duration"]-1/30}
    for a,b in tl["scenes"].values():
        times.update(max(0,min(tl["duration"]-1/30,a+d)) for d in [-1/30,0,.1,.3,.55,.6])
    for take in tl["takes"]:
        times.update(w["start"] for w in take["words"])
    for at in sorted(times):
        source(at)
    captions = json.loads((out/"captions.json").read_text(encoding="utf-8"))
    assert all(0 <= c["start"] < c["end"] <= tl["duration"] for c in captions)
    assert all(a["end"] <= b["start"] for a,b in zip(captions,captions[1:]))
    assert " ".join(c["text"] for c in captions).split() == " ".join(t["text"] for t in tl["takes"]).split()

    sheet = Image.new("RGB",(1440,math.ceil(len(script["scenes"])/2)*430),"#101035")
    draw = ImageDraw.Draw(sheet)
    report = []
    for i,scene in enumerate(script["scenes"]):
        a,b = tl["scenes"][scene["id"]]
        at = round((a+(b-a)*.72)*30)/30
        expected = source(at)
        raw = subprocess.run([ff,"-v","error","-ss",str(at),"-i",str(out/f"{render.NAME}.mp4"),
            "-frames:v","1","-pix_fmt","rgb24","-f","rawvideo","-"],capture_output=True,check=True).stdout
        decoded = np.frombuffer(raw,np.uint8).reshape(1080,1920,3)
        error = float(np.mean(np.abs(expected.astype(float)-decoded.astype(float))))
        assert error < 4, f"Encoded frame differs from source: {scene['id']} ({error})"
        future = source(min(at+.6,b-.05))
        pixels = int(np.count_nonzero(np.any(expected != future,axis=2)))
        assert pixels > 500, f"Scene has no visible animation: {scene['id']}"
        x,y = (i%2)*720,(i//2)*430
        sheet.paste(Image.fromarray(decoded).resize((720,405),Image.Resampling.LANCZOS),(x,y))
        draw.text((x+10,y+409),f"{at:.2f}s | {scene['title']} | source MAE {error:.2f}",fill="#faf4df")
        report.append({"scene":scene["id"],"time":at,"source_mean_absolute_pixel_error":error,"changed_pixels_over_600ms":pixels})
    sheet.save(out/"encoded-contact-sheet.jpg",quality=94)
    info = {"passed":True,"layout_samples":len(times),"captions":len(captions),"caption_text_complete":True,
            "caption_timing_valid":True,"encoded_frames":report,"production_sha256":render.production_hash()}
    (out/"encoded-review.json").write_text(json.dumps(info,indent=2),encoding="utf-8")
    print(f"Passed: {len(times)} layout samples, {len(report)} encoded scenes, complete timed captions and visible motion.",flush=True)


if __name__ == "__main__":
    main()
