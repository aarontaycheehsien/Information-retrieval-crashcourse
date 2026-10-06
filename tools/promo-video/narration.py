"""Cached scene narration, captions, mixing, and lossless picture-track remuxing."""
from __future__ import annotations

import asyncio
import hashlib
import html
import json
import math
from pathlib import Path
import re
import shutil
import subprocess
import wave

import numpy as np

HERE = Path(__file__).resolve().parent
SR = 48000


def config():
    return json.loads((HERE / "narration.json").read_text(encoding="utf-8"))


def normalized(text):
    return re.sub(r"[^\w]", "", html.unescape(text)).lower()


def validate(settings, story):
    scenes = {scene["id"]: scene for scene in story["scenes"]}
    assert [cue["scene"] for cue in settings["cues"]] == list(scenes)
    previous = 0
    for cue in settings["cues"]:
        scene = scenes[cue["scene"]]
        assert scene["start"] <= cue["start"] < cue["deadline"] <= scene["end"]
        assert previous <= cue["start"]
        assert cue["text"].strip()
        previous = cue["deadline"]
    assert previous <= story["duration"] - .5
    assert 1 <= settings["max_time_compression"] <= 1.1


def write_wav(path, data):
    data = np.asarray(data)
    if data.ndim == 1:
        data = data[:, None]
    peak = float(np.max(np.abs(data)))
    assert peak < 1, f"PCM would clip at {peak}"
    with wave.open(str(path), "wb") as handle:
        handle.setnchannels(data.shape[1])
        handle.setsampwidth(2)
        handle.setframerate(SR)
        handle.writeframes((data * 32767).astype("<i2").tobytes())


def read_wav(path):
    with wave.open(str(path), "rb") as handle:
        assert handle.getframerate() == SR and handle.getsampwidth() == 2
        channels = handle.getnchannels()
        return np.frombuffer(handle.readframes(handle.getnframes()), dtype="<i2").astype(np.float64).reshape(-1, channels) / 32768


def cache_paths(out, cue, settings):
    request = {"text": cue["text"], "voice": settings["voice"], "rate": cue.get("rate", settings["rate"]), "pitch": settings["pitch"], "engine": "edge-tts-7.2.8", "boundary": "WordBoundary"}
    key = hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()[:20]
    directory = out / "narration-cache" / key
    return directory, request


async def synthesize(out, cue, settings, gate):
    directory, request = cache_paths(out, cue, settings)
    directory.mkdir(parents=True, exist_ok=True)
    media = directory / "speech.mp3"
    metadata = directory / "events.json"
    if media.is_file() and metadata.is_file():
        print(f"Cached voice: {cue['scene']}", flush=True)
        return directory
    import edge_tts
    async with gate:
        for attempt in range(3):
            events = []
            partial = directory / "speech.partial.mp3"
            try:
                voice = edge_tts.Communicate(cue["text"], voice=request["voice"], rate=request["rate"], pitch=request["pitch"], boundary="WordBoundary", connect_timeout=10, receive_timeout=25)
                with partial.open("wb") as handle:
                    async for event in voice.stream():
                        if event["type"] == "audio":
                            handle.write(event["data"])
                        elif event["type"] == "WordBoundary":
                            events.append(event)
                assert partial.stat().st_size > 1000 and events, "Speech or word timings were not returned"
                assert normalized("".join(event["text"] for event in events)) == normalized(cue["text"]), "Returned speech text differs from script"
                partial.replace(media)
                metadata.write_text(json.dumps(events, indent=2), encoding="utf-8")
                (directory / "request.json").write_text(json.dumps(request, indent=2), encoding="utf-8")
                print(f"Generated voice: {cue['scene']}", flush=True)
                return directory
            except Exception as error:
                if attempt == 2:
                    raise RuntimeError(f"Voice synthesis failed for {cue['scene']} after three attempts ({type(error).__name__}); existing videos were preserved") from error
                await asyncio.sleep(attempt + 1)


async def generate_all(out, settings):
    gate = asyncio.Semaphore(2)
    return await asyncio.gather(*(synthesize(out, cue, settings, gate) for cue in settings["cues"]))


def prepare_clip(directory, cue, settings, ffmpeg):
    # Remove only exterior digital silence, retaining natural pauses in the take.
    decoded = directory / "decoded.wav"
    ffmpeg(["-i", str(directory / "speech.mp3"), "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(decoded)], directory / "decode.log")
    samples = read_wav(decoded)[:, 0]
    active = np.flatnonzero(np.abs(samples) > .0015)
    assert len(active), f"Empty speech: {cue['scene']}"
    first = max(0, int(active[0]) - round(.035 * SR))
    last = min(len(samples), int(active[-1]) + round(.14 * SR))
    samples = samples[first:last]
    available = cue["deadline"] - cue["start"]
    tempo = max(1, (len(samples) / SR) / (available - .05))
    assert tempo <= settings["max_time_compression"], f"{cue['scene']} needs a shorter take, not a cut word: speed factor {tempo:.3f}"
    trimmed = directory / "trimmed.wav"
    write_wav(trimmed, samples)
    ready = directory / "leveled.wav"
    ffmpeg(["-i", str(trimmed), "-af", f"atempo={tempo:.6f},loudnorm=I=-18:TP=-4:LRA=7", "-ac", "1", "-ar", str(SR), "-c:a", "pcm_s16le", str(ready)], directory / "prepare.log")
    samples = read_wav(ready)[:, 0]
    end = cue["start"] + len(samples) / SR
    assert end <= cue["deadline"] + .001, f"Speech crosses the scene boundary: {cue['scene']}"
    events = json.loads((directory / "events.json").read_text(encoding="utf-8"))
    words = []
    for event in events:
        start = cue["start"] + (event["offset"] / 1e7 - first / SR) / tempo
        finish = start + event["duration"] / 1e7 / tempo
        words.append({"text": event["text"], "start": max(cue["start"], start), "end": min(end, finish)})
    return samples, {"scene": cue["scene"], "start": cue["start"], "end": end, "deadline": cue["deadline"], "text": cue["text"], "rate": cue.get("rate", settings["rate"]), "tempo": tempo, "trimmed_leading_seconds": first / SR, "cache_key": directory.name, "speech_sha256": hashlib.sha256((directory / "speech.mp3").read_bytes()).hexdigest(), "words": words}


def caption_cues(placements):
    result = []
    for cue in placements:
        # Map original punctuation to service word timings using character spans.
        # This also handles providers splitting contractions into two boundaries.
        events = []
        position = 0
        for word in cue["words"]:
            length = len(normalized(word["text"]))
            events.append((position, position + length, word))
            position += length
        tokens = []
        position = 0
        for word in cue["text"].split():
            length = len(normalized(word))
            matches = [event[2] for event in events if event[0] < position + length and event[1] > position]
            assert matches, f"Caption word has no speech timing: {word}"
            tokens.append({"text": word, "start": matches[0]["start"], "end": matches[-1]["end"]})
            position += length
        group = []
        for index, token in enumerate(tokens):
            group.append(token)
            if len(group) >= 7 or token["text"].endswith((".", "?", "!", "…")) or index == len(tokens) - 1:
                start = max(cue["start"], group[0]["start"])
                end = min(cue["end"], group[-1]["end"] + .12)
                value = " ".join(word["text"] for word in group)
                result.append({"start": start, "end": max(start + .1, end), "text": value})
                group = []
    for current, following in zip(result, result[1:]):
        current["end"] = min(current["end"], following["start"])
    assert all(0 <= cue["start"] < cue["end"] <= 44.5 for cue in result)
    return result


def stamp_time(seconds, srt=False):
    milliseconds = round(seconds * 1000)
    hours, milliseconds = divmod(milliseconds, 3600000)
    minutes, milliseconds = divmod(milliseconds, 60000)
    seconds, milliseconds = divmod(milliseconds, 1000)
    return f"{hours:02}:{minutes:02}:{seconds:02}{',' if srt else '.'}{milliseconds:03}"


def captions(out, placements, settings):
    cues = caption_cues(placements)
    srt = []
    vtt = ["WEBVTT\n"]
    for index, cue in enumerate(cues, 1):
        srt.append(f"{index}\n{stamp_time(cue['start'], True)} --> {stamp_time(cue['end'], True)}\n{cue['text']}\n")
        vtt.append(f"{stamp_time(cue['start'])} --> {stamp_time(cue['end'])}\n{html.escape(cue['text'])}\n")
    (out / "narration.srt").write_text("\n".join(srt), encoding="utf-8")
    (out / "narration.vtt").write_text("\n".join(vtt), encoding="utf-8")
    transcript = ["The Missing Paper — narration transcript", f"Synthetic voice: {settings['voice']}", ""]
    for cue in placements:
        transcript.append(f"{stamp_time(cue['start'])}–{stamp_time(cue['end'])}\n{cue['text']}\n")
    (out / "narration-transcript.txt").write_text("\n".join(transcript), encoding="utf-8")
    return cues


def duck_envelope(count, placements, gain, attack, release):
    result = np.ones(count, dtype=np.float64)
    for cue in placements:
        start, end = round(cue["start"] * SR), round(cue["end"] * SR)
        a, b = max(0, start - round(attack * SR)), min(count, end + round(release * SR))
        if start > a:
            phase = np.linspace(0, math.pi, start - a)
            ramp = gain + (1 - gain) * (1 + np.cos(phase)) / 2
            result[a:start] = np.minimum(result[a:start], ramp)
        result[start:end] = np.minimum(result[start:end], gain)
        if b > end:
            phase = np.linspace(0, math.pi, b - end)
            ramp = gain + (1 - gain) * (1 - np.cos(phase)) / 2
            result[end:b] = np.minimum(result[end:b], ramp)
    return result


def mix(out, story, ffmpeg):
    settings = config()
    validate(settings, story)
    directories = asyncio.run(generate_all(out, settings))
    voice = np.zeros(SR * story["duration"], dtype=np.float64)
    placements = []
    for directory, cue in zip(directories, settings["cues"]):
        samples, placement = prepare_clip(directory, cue, settings, ffmpeg)
        start = round(cue["start"] * SR)
        voice[start:start + len(samples)] += samples
        placements.append(placement)
        print(f"Voice timing: {cue['scene']} {cue['start']:.2f}–{placement['end']:.2f}s", flush=True)
    assert placements[-1]["end"] <= story["duration"] - .5
    write_wav(out / "narration-only.wav", voice)
    music = read_wav(out / "music-original.wav") * 10 ** (settings["music_gain_db"] / 20)
    effects = read_wav(out / "effects-original.wav")
    assert music.shape == effects.shape == (len(voice), 2)
    gains = []
    for key in ("music", "effects"):
        gains.append(duck_envelope(len(voice), placements, 10 ** (settings[f"{key}_duck_db"] / 20), settings["duck_attack_seconds"], settings["duck_release_seconds"]))
    combined = voice[:, None] + music * gains[0][:, None] + effects * gains[1][:, None]
    peak = float(np.max(np.abs(combined)))
    pre_gain = min(1, .95 / peak)
    unmastered = out / "narrated-mix-unmastered.wav"
    write_wav(unmastered, combined * pre_gain)
    master = out / "soundtrack-narrated.wav"
    ffmpeg(["-i", str(unmastered), "-af", f"loudnorm=I={settings['master_lufs']}:TP={settings['master_true_peak_db']}:LRA=7", "-ar", str(SR), "-c:a", "pcm_s16le", str(master)], out / "narration-mastering.log")
    caption_records = captions(out, placements, settings)
    manifest = {"voice": settings["voice"], "synthetic": True, "rate": settings["rate"], "pitch": settings["pitch"], "sample_rate": SR, "music_gain_db": settings["music_gain_db"], "music_duck_db": settings["music_duck_db"], "effects_duck_db": settings["effects_duck_db"], "unmastered_peak": peak, "pre_master_gain": pre_gain, "final_silence_seconds": story["duration"] - placements[-1]["end"], "cues": placements, "captions": caption_records}
    (out / "narration-manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    return master, manifest


def picture_hash(path, executable):
    result = subprocess.run([executable, "-hide_banner", "-loglevel", "error", "-i", str(path), "-map", "0:v:0", "-c:v", "copy", "-f", "data", "pipe:1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return hashlib.sha256(result.stdout).hexdigest()


def remux(out, fmt, audio, ffmpeg, executable, verify):
    video = out / f"missing-paper-{fmt}.mp4"
    original = out / f"missing-paper-{fmt}-music-only.mp4"
    assert video.is_file(), f"Render the {fmt} picture first"
    if not original.exists():
        shutil.copy2(video, original)
    before = picture_hash(video, executable)
    pending = out / f"missing-paper-{fmt}-pending.mp4"
    ffmpeg(["-i", str(video), "-i", str(audio), "-i", str(out / "narration.srt"), "-map", "0:v:0", "-map", "1:a:0", "-map", "2:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", str(SR), "-c:s", "mov_text", "-metadata:s:a:0", "language=eng", "-metadata:s:s:0", "language=eng", "-disposition:s:0", "0", "-metadata", "comment=Synthetic narration: Microsoft en-GB-SoniaNeural", "-t", "45", "-movflags", "+faststart", str(pending)], out / f"narration-remux-{fmt}.log")
    after = picture_hash(pending, executable)
    assert before == after, "Picture stream changed during audio replacement"
    info = verify(out, pending, fmt)
    assert abs(info["integrated_lufs"] + 16) <= 1, "Final mix is outside the loudness target"
    # Ensure all supplied captions survive the MP4 timed-text conversion.
    extracted = subprocess.run([executable, "-hide_banner", "-loglevel", "error", "-i", str(pending), "-map", "0:s:0", "-c:s", "srt", "-f", "srt", "pipe:1"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True).stdout.decode("utf-8")
    assert all(cue["text"] in extracted for cue in caption_cues(json.loads((out / "narration-manifest.json").read_text(encoding="utf-8"))["cues"]))
    pending.replace(video)
    info.update({"file": video.name, "narrated": True, "voice": config()["voice"], "synthetic_voice": True, "embedded_captions": "English", "picture_stream_sha256": after, "picture_stream_unchanged": True, "music_only_file": original.name})
    return info
