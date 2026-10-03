"""Offline Windows speech adapter for the shared narration-led timeline."""
from __future__ import annotations

import asyncio
import json
from pathlib import Path
import wave

import narrate

ENGINE = "windows-system-speech-16khz-v3"


async def synthesize(out, line, voice, gate, quiet=False):
    request = narrate.request_for(line, voice)
    directory = narrate.cache_dir(out, request)
    media, events_path = directory / "speech.mp3", directory / "events.json"
    if media.is_file() and events_path.is_file():
        if not quiet:
            print(f"  cached offline take {line['id']}", flush=True)
        return directory
    directory.mkdir(parents=True, exist_ok=True)
    wav = directory / "speech.wav"
    raw_events = directory / "windows-events.json"
    control = directory / "offline-request.json"
    control.write_text(json.dumps({"text": line["text"], "voice": voice["name"],
                                 "wav": str(wav.resolve()), "events": str(raw_events.resolve())}), encoding="utf-8")
    async with gate:
        process = await asyncio.create_subprocess_exec(
            "powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File",
            str(Path(__file__).with_name("synthesize.ps1")), "-RequestPath", str(control.resolve()),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        try:
            stdout, stderr = await asyncio.wait_for(process.communicate(), timeout=60)
        except asyncio.TimeoutError:
            process.kill()
            await process.wait()
            raise RuntimeError("Offline Windows voice timed out; local speech may require sandbox approval")
        (directory / "synthesis.log").write_bytes(stdout + stderr)
        if process.returncode:
            raise RuntimeError(f"Offline speech failed: {directory / 'synthesis.log'}")
        words = json.loads(raw_events.read_text(encoding="utf-8-sig"))
        assert narrate.normalized("".join(w["text"] for w in words)) == narrate.normalized(line["text"]), "Offline words differ from script"
        with wave.open(str(wav), "rb") as handle:
            end = int(handle.getnframes()/handle.getframerate()*1e7)
        assert 0 <= words[0]["offset"] < words[-1]["offset"] < end, "Offline word clock does not match WAV"
        assert all(a["offset"] < b["offset"] for a,b in zip(words,words[1:])), "Offline word positions are unordered"
        events = []
        for i, word in enumerate(words):
            following = words[i+1]["offset"] if i+1 < len(words) else end
            events.append({"text": word["text"], "offset": word["offset"],
                           "duration": max(1, following-word["offset"])})
        # Preserve the common engine's audio format and trimming implementation.
        import imageio_ffmpeg
        encoder = await asyncio.create_subprocess_exec(
            imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-v", "error", "-i", str(wav),
            "-c:a", "libmp3lame", "-b:a", "192k", str(media),
            stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
        _, errors = await encoder.communicate()
        if encoder.returncode:
            raise RuntimeError(errors.decode(errors="replace"))
        events_path.write_text(json.dumps(events, indent=1), encoding="utf-8")
        (directory / "request.json").write_text(json.dumps(request, indent=1), encoding="utf-8")
        print(f"  new offline take {line['id']}", flush=True)
    return directory


def install():
    narrate.ENGINE = ENGINE
    narrate.synthesize = synthesize
