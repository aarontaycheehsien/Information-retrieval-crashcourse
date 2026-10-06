"""Voice takes and the narration-led timeline.

The voice is the master clock. Each line is synthesised once, cached, trimmed of
exterior silence only, and placed after the previous line with the scripted
pause. Takes are never time-stretched; the picture is cut to the voice.
"""
from __future__ import annotations

import asyncio
import hashlib
import html
import json
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

SR = 48000
ENGINE = "edge-tts-7.2.8"


def normalized(text: str) -> str:
    return re.sub(r"[^\w]", "", html.unescape(text)).lower()


@dataclass
class Take:
    id: str
    scene: str
    text: str
    audio: np.ndarray
    words: list[dict]
    cache_key: str
    start: float = 0.0

    @property
    def duration(self) -> float:
        return len(self.audio) / SR

    @property
    def end(self) -> float:
        return self.start + self.duration


@dataclass
class Timeline:
    takes: list[Take]
    scenes: dict[str, tuple[float, float]]
    duration: float
    lookup: dict[str, Take] = field(default_factory=dict)

    def __post_init__(self) -> None:
        self.lookup = {take.id: take for take in self.takes}

    def start(self, line: str) -> float:
        return self.lookup[line].start

    def end(self, line: str) -> float:
        return self.lookup[line].end

    def word(self, line: str, text: str, nth: int = 0) -> dict:
        """Absolute timing of the nth word in a line whose letters match text."""
        hits = [w for w in self.lookup[line].words if normalized(w["text"]) == normalized(text)]
        if len(hits) <= nth:
            raise KeyError(f"{text!r} not spoken in line {line!r}")
        return hits[nth]

    def at(self, line: str, text: str, nth: int = 0) -> float:
        return self.word(line, text, nth)["start"]

    def scene(self, name: str) -> tuple[float, float]:
        return self.scenes[name]

    def speaking(self, t: float) -> bool:
        return any(take.start <= t < take.end for take in self.takes)


def request_for(line: dict, voice: dict) -> dict:
    return {
        "text": line["text"],
        "voice": voice["name"],
        "rate": line.get("rate", voice["rate"]),
        "pitch": line.get("pitch", voice["pitch"]),
        "engine": ENGINE,
        "boundary": "WordBoundary",
    }


def cache_dir(out: Path, request: dict) -> Path:
    key = hashlib.sha256(json.dumps(request, sort_keys=True).encode()).hexdigest()[:20]
    return out / "voice-cache" / key


async def synthesize(out: Path, line: dict, voice: dict, gate: asyncio.Semaphore, quiet: bool = False) -> Path:
    request = request_for(line, voice)
    directory = cache_dir(out, request)
    media, events_path = directory / "speech.mp3", directory / "events.json"
    if media.is_file() and events_path.is_file():
        if not quiet:
            print(f"  cached take  {line['id']}", flush=True)
        return directory
    import edge_tts

    directory.mkdir(parents=True, exist_ok=True)
    async with gate:
        for attempt in range(3):
            events, audio = [], bytearray()
            try:
                comm = edge_tts.Communicate(
                    line["text"], voice=request["voice"], rate=request["rate"], pitch=request["pitch"],
                    boundary="WordBoundary", connect_timeout=10, receive_timeout=30,
                )
                async for event in comm.stream():
                    if event["type"] == "audio":
                        audio += event["data"]
                    elif event["type"] == "WordBoundary":
                        events.append({k: event[k] for k in ("offset", "duration", "text")})
                assert len(audio) > 1000 and events, "no speech or word timings returned"
                spoken = normalized("".join(e["text"] for e in events))
                assert spoken == normalized(line["text"]), f"returned words differ from script: {spoken}"
                media.write_bytes(bytes(audio))
                events_path.write_text(json.dumps(events, indent=1), encoding="utf-8")
                (directory / "request.json").write_text(json.dumps(request, indent=1), encoding="utf-8")
                print(f"  new take     {line['id']}", flush=True)
                return directory
            except Exception as error:  # network hiccups are common; retry, then fail loudly
                if attempt == 2:
                    raise RuntimeError(f"voice synthesis failed for {line['id']}: {error}") from error
                await asyncio.sleep(1.5 * (attempt + 1))


def decode(ffmpeg: str, path: Path) -> np.ndarray:
    raw = subprocess.run(
        [ffmpeg, "-v", "error", "-i", str(path), "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
        capture_output=True, check=True,
    ).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)


def voiced_rms(x: np.ndarray) -> float:
    frame = SR // 50
    usable = x[: len(x) // frame * frame].reshape(-1, frame)
    rms = np.sqrt(np.mean(usable ** 2, axis=1))
    loud = rms[rms > 10 ** (-40 / 20)]
    return float(np.sqrt(np.mean(loud ** 2))) if len(loud) else 1e-9


def prepare(directory: Path, line: dict, ffmpeg: str) -> Take:
    samples = decode(ffmpeg, directory / "speech.mp3")
    active = np.flatnonzero(np.abs(samples) > 10 ** (-50 / 20))
    assert len(active), f"silent take: {line['id']}"
    first = max(0, int(active[0]) - int(0.03 * SR))
    last = min(len(samples), int(active[-1]) + int(0.12 * SR))
    clip = samples[first:last].copy()
    fade = int(0.012 * SR)
    clip[:fade] *= np.linspace(0, 1, fade)
    clip[-fade:] *= np.linspace(1, 0, fade)
    # One fixed gain per take: consistent level, natural dynamics untouched.
    clip *= 10 ** (-19 / 20) / voiced_rms(clip)
    events = json.loads((directory / "events.json").read_text(encoding="utf-8"))
    offset = first / SR
    words = []
    for e in events:
        s = e["offset"] / 1e7 - offset
        words.append({"text": e["text"], "start": max(0.0, s), "end": min(len(clip) / SR, s + e["duration"] / 1e7)})
    return Take(line["id"], line["scene"], line["text"], clip, words, directory.name)


def build(script: dict, out: Path, ffmpeg: str, quiet: bool = False) -> Timeline:
    lines = script["lines"]
    assert len({l["id"] for l in lines}) == len(lines), "line ids must be unique"

    async def run():
        gate = asyncio.Semaphore(3)
        return await asyncio.gather(*(synthesize(out, l, script["voice"], gate, quiet) for l in lines))

    if not quiet:
        print("Voice takes:", flush=True)
    dirs = asyncio.run(run())
    takes = [prepare(d, l, ffmpeg) for d, l in zip(dirs, lines)]

    t = script["lead_in"]
    for i, (take, line) in enumerate(zip(takes, lines)):
        if i:
            t = takes[i - 1].end + line["gap"]
        take.start = t
        for w in take.words:
            w["start"] += t
            w["end"] += t
    duration = takes[-1].end + script["tail"]

    order: list[str] = []
    for take in takes:
        if take.scene not in order:
            order.append(take.scene)
    starts = {}
    for name in order:
        idx = next(i for i, tk in enumerate(takes) if tk.scene == name)
        if idx == 0:
            starts[name] = 0.0
        else:
            gap = takes[idx].start - takes[idx - 1].end
            starts[name] = takes[idx].start - min(0.55, 0.6 * gap)
    scenes = {}
    for i, name in enumerate(order):
        scenes[name] = (starts[name], starts[order[i + 1]] if i + 1 < len(order) else duration)
    return Timeline(takes, scenes, duration)


def voice_track(tl: Timeline) -> np.ndarray:
    track = np.zeros(int(np.ceil(tl.duration * SR)) + SR)
    for take in tl.takes:
        i = int(round(take.start * SR))
        track[i:i + len(take.audio)] += take.audio
    return track[: int(round(tl.duration * SR))]


def captions(tl: Timeline) -> list[dict]:
    """Caption cues of at most ~42 characters, split at sentence or clause ends."""
    cues = []
    for take in tl.takes:
        tokens = re.findall(r"\S+", take.text)
        words = take.words
        # map each written token to spoken word timings by consuming normalized letters
        timed, wi = [], 0
        for tok in tokens:
            need = normalized(tok)
            got, s, e = "", None, None
            while wi < len(words) and len(got) < len(need):
                got += normalized(words[wi]["text"])
                s = words[wi]["start"] if s is None else s
                e = words[wi]["end"]
                wi += 1
            if not need:  # punctuation-only token
                s = e = timed[-1][2] if timed else take.start
            timed.append((tok, s, e))
        group: list = []
        for j, (tok, s, e) in enumerate(timed):
            group.append((tok, s, e))
            text = " ".join(g[0] for g in group)
            nxt = timed[j + 1][0] if j + 1 < len(timed) else None
            boundary = tok.endswith((".", "?", "!")) and len(text) > 14
            too_long = nxt is not None and len(text) + 1 + len(nxt) > 42
            if nxt is None or boundary or too_long:
                cues.append({"start": group[0][1], "end": group[-1][2] + 0.25, "text": text})
                group = []
    for a, b in zip(cues, cues[1:]):
        a["end"] = min(a["end"], b["start"] - 0.02)
    return cues


def stamp(seconds: float, sep: str) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d}{sep}{ms:03d}"


def write_captions(tl: Timeline, out: Path) -> list[dict]:
    cues = captions(tl)
    srt = [f"{i}\n{stamp(c['start'], ',')} --> {stamp(c['end'], ',')}\n{c['text']}\n" for i, c in enumerate(cues, 1)]
    (out / "pick-a-card.srt").write_text("\n".join(srt), encoding="utf-8")
    vtt = ["WEBVTT\n"] + [f"{stamp(c['start'], '.')} --> {stamp(c['end'], '.')}\n{c['text']}\n" for c in cues]
    (out / "pick-a-card.vtt").write_text("\n".join(vtt), encoding="utf-8")
    return cues
