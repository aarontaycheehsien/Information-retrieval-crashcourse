"""Check the real gallery in Chromium: play, seek, captions, ranges and narrow screens."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil
import urllib.request

from playwright.sync_api import sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", default="http://127.0.0.1:8817/index.html")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[2]/"outputs/pre-chapter-1-investigations")
    args = parser.parse_args()
    results = {"url": args.url, "films": [], "layouts": [], "errors": []}
    with sync_playwright() as p:
        executable = shutil.which("chromium") or shutil.which("google-chrome")
        browser = p.chromium.launch(executable_path=executable, args=["--no-sandbox", "--disable-dev-shm-usage"])
        page = browser.new_page(viewport={"width": 1440, "height": 1000})
        page.on("pageerror", lambda error: results["errors"].append(str(error)))
        page.goto(args.url, wait_until="networkidle")
        assert page.locator("video").count() == 3
        for number in range(1, 4):
            selector = f"#film-{number}"
            page.eval_on_selector(selector, "v=>{v.muted=true;v.load();}")
            page.wait_for_function("s=>document.querySelector(s).readyState>=1", arg=selector, timeout=30000)
            info = page.eval_on_selector(selector, "v=>({src:v.currentSrc,duration:v.duration,width:v.videoWidth,height:v.videoHeight})")
            assert info["width"] == 1920 and info["height"] == 1080
            assert info["duration"] > 120
            page.eval_on_selector(selector, "v=>v.play()")
            page.wait_for_function("s=>document.querySelector(s).currentTime>.4", arg=selector, timeout=15000)
            page.eval_on_selector(selector, "v=>{v.pause();v.currentTime=v.duration*.5;v.textTracks[0].mode='hidden'}")
            page.wait_for_function("s=>{const v=document.querySelector(s);return !v.seeking&&v.readyState>=2&&v.currentTime>v.duration*.49}", arg=selector, timeout=20000)
            page.wait_for_function("s=>document.querySelector(s).textTracks[0].cues?.length>0", arg=selector)
            info["caption_cues"] = page.eval_on_selector(selector, "v=>v.textTracks[0].cues.length")
            info["seek_seconds"] = page.eval_on_selector(selector, "v=>v.currentTime")
            # Exercise the actual scene button handler.
            page.eval_on_selector(f'button[data-film="film-{number}"]:last-child', "b=>b.click()")
            page.wait_for_function("s=>{const v=document.querySelector(s);return !v.seeking&&v.currentTime>v.duration*.75}", arg=selector, timeout=20000)
            page.eval_on_selector(selector, "v=>v.pause()")
            request = urllib.request.Request(info["src"], headers={"Range": "bytes=0-1023"})
            with urllib.request.urlopen(request, timeout=10) as response:
                assert response.status == 206 and len(response.read()) == 1024
                info["byte_range"] = response.headers["Content-Range"]
            info["playback"] = True
            results["films"].append(info)
        # Capture the initial gallery, after resetting the playback checks.
        page.reload(wait_until="networkidle")
        page.wait_for_function("[...document.querySelectorAll('video')].every(v=>v.readyState>=1)")
        for width, height in [(1440, 1000), (768, 1024), (390, 844)]:
            page.set_viewport_size({"width": width, "height": height})
            page.wait_for_timeout(200)
            assert page.evaluate("document.documentElement.scrollWidth<=innerWidth+1"), f"Horizontal overflow at {width}"
            assert page.locator("h1").is_visible()
            page.screenshot(path=str(args.output/f"gallery-{width}.png"), full_page=True)
            results["layouts"].append({"width": width, "horizontal_overflow": False})
        assert not results["errors"], results["errors"]
        browser.close()
    results["passed"] = True
    (args.output/"browser-verification.json").write_text(json.dumps(results, indent=2))
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
