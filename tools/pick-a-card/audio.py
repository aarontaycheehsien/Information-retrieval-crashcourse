"""Original soundtrack: a sly pizzicato waltz, table-top foley and a room for the voice.

Everything is synthesised from oscillators and seeded noise. The score follows
the scenes; foley lands on the frames where cards move; the narration sits in a
small, quiet room so it sounds recorded rather than pasted on.
"""
from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path

import numpy as np
from scipy.signal import butter, fftconvolve, sosfilt

import narrate

SR = narrate.SR
RNG = np.random.default_rng(709)

# --- helpers -------------------------------------------------------------
NOTE = {n: i for i, n in enumerate(["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"])}
NOTE.update({"Db": 1, "Eb": 3, "Gb": 6, "Ab": 8, "Bb": 10})


def hz(name: str) -> float:
    m = re.fullmatch(r"([A-G][b#]?)(-?\d)", name)
    semis = NOTE[m.group(1)] + 12 * (int(m.group(2)) + 1)
    return 440.0 * 2 ** ((semis - 69) / 12)


def filt(x, kind, freq, order=2):
    sos = butter(order, freq, btype=kind, fs=SR, output="sos")
    return sosfilt(sos, x)


def env_adsr(n, a=0.005, d=0.0, s=1.0, r=0.05):
    """Linear attack, exponential decay towards the sustain level, linear release."""
    t = np.arange(n) / SR
    after = np.maximum(0, t - a)
    e = np.where(t < a, t / max(a, 1e-6), s + (1 - s) * (np.exp(-after / d) if d else 0))
    nr = min(n, max(1, int(r * SR)))
    e[-nr:] *= np.linspace(1, 0, nr)
    return e


class Bus:
    def __init__(self, duration: float):
        self.n = int(round(duration * SR))
        self.x = np.zeros((self.n + SR * 4, 2))

    def add(self, t: float, sig: np.ndarray, gain: float = 1.0, pan: float = 0.0) -> None:
        if t < 0:
            sig = sig[int(-t * SR):]
            t = 0
        i = int(round(t * SR))
        if i >= len(self.x):
            return
        sig = sig[: len(self.x) - i]
        if sig.ndim == 1:
            ang = (pan + 1) * np.pi / 4
            self.x[i:i + len(sig), 0] += sig * gain * np.cos(ang)
            self.x[i:i + len(sig), 1] += sig * gain * np.sin(ang)
        else:
            self.x[i:i + len(sig)] += sig * gain

    def out(self) -> np.ndarray:
        return self.x[: self.n]


def noise(dur):
    return RNG.standard_normal(int(dur * SR))


def tvec(dur):
    return np.arange(int(dur * SR)) / SR


# --- instruments ---------------------------------------------------------
def pizz(f: float, vel: float = 1.0, dur: float = 0.7) -> np.ndarray:
    t = tvec(dur)
    y = np.zeros_like(t)
    for k in range(1, 14):
        if f * k > 9000:
            break
        y += (1 / k ** 1.1) * np.sin(2 * np.pi * f * k * t + RNG.uniform(0, 0.4)) * np.exp(-t * (6 + 2.2 * k))
    y += filt(noise(dur), "bandpass", [max(80, f * 0.8), min(9000, f * 6)]) * np.exp(-t * 90) * 0.35
    return y * vel * env_adsr(len(t), a=0.002, r=0.05)


def bell(f: float, vel: float = 1.0, dur: float = 2.2) -> np.ndarray:
    t = tvec(dur)
    y = np.zeros_like(t)
    for ratio, amp, dec in ((1, 1, 1.6), (2.0, 0.42, 2.6), (3.0, 0.2, 4.0), (4.16, 0.12, 6), (5.43, 0.06, 8)):
        y += amp * np.sin(2 * np.pi * f * ratio * t) * np.exp(-t * dec)
    return y * vel * env_adsr(len(t), a=0.003, r=0.2)


def pad(freqs, dur: float, vel: float = 1.0, attack: float = 0.5) -> np.ndarray:
    t = tvec(dur)
    y = np.zeros_like(t)
    for f in freqs:
        vib = 1 + 0.003 * np.sin(2 * np.pi * 5.1 * t + RNG.uniform(0, 6))
        ph = 2 * np.pi * np.cumsum(f * vib) / SR
        for k in range(1, 9):
            y += (1 / k) * np.sin(k * ph) * (0.6 ** (k - 1))
    y = filt(y, "lowpass", 2400)
    return y * vel / len(freqs) * env_adsr(len(t), a=attack, r=min(0.8, dur * 0.4))


def brass(freqs, dur: float = 0.9, vel: float = 1.0) -> np.ndarray:
    t = tvec(dur)
    y = np.zeros_like(t)
    bright = 0.35 + 0.65 * np.exp(-t * 5)
    for f in freqs:
        for k in range(1, 12):
            y += (1 / k) * np.sin(2 * np.pi * f * k * t) * bright ** (k * 0.5)
    y = filt(y, "lowpass", 3800)
    return y * vel / len(freqs) * env_adsr(len(t), a=0.018, d=0.25, s=0.55, r=0.3)


# --- foley ---------------------------------------------------------------
def click(vel=1.0):
    d = 0.03
    t = tvec(d)
    return (filt(noise(d), "highpass", 1800) * np.exp(-t * 400) + np.sin(2 * np.pi * 140 * t) * np.exp(-t * 120) * 0.6) * vel


def flick(vel=1.0, bright=3000):
    d = 0.05
    t = tvec(d)
    return filt(noise(d), "bandpass", [bright * 0.5, min(bright * 2.4, 16000)]) * np.exp(-t * 140) * vel


def snap(vel=1.0):
    d = 0.12
    t = tvec(d)
    body = filt(noise(d), "bandpass", [600, 5000]) * np.exp(-t * 70)
    thump = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 60) * 0.5
    return (body + thump) * vel


def whoosh(dur=0.6, f0=400, f1=3000, vel=1.0):
    n = int(dur * SR)
    x = noise(dur)
    out = np.zeros(n)
    seg = 256
    zi = None
    for i in range(0, n, seg):
        fc = f0 * (f1 / f0) ** (i / n)
        sos = butter(2, [max(40, fc * 0.6), min(18000, fc * 1.6)], btype="bandpass", fs=SR, output="sos")
        if zi is None:
            zi = np.zeros((sos.shape[0], 2))
        out[i:i + seg], zi = sosfilt(sos, x[i:i + seg], zi=zi)
    e = np.sin(np.pi * np.linspace(0, 1, n)) ** 1.5
    return out * e * vel


def thud(f=70, vel=1.0, dur=0.5):
    t = tvec(dur)
    f_t = f * (1 + 0.8 * np.exp(-t * 30))
    y = np.sin(2 * np.pi * np.cumsum(f_t) / SR) * np.exp(-t * 9)
    y += filt(noise(dur), "lowpass", 900) * np.exp(-t * 40) * 0.6
    return y * vel


def stamp_fx(vel=1.0):
    return thud(95, 0.8 * vel, 0.35) + np.pad(snap(0.9 * vel), (0, int(0.23 * SR)))


def poof(vel=1.0):
    d = 1.6
    t = tvec(d)
    y = filt(noise(d), "lowpass", 1800) * (np.exp(-t * 3.2) * (1 - np.exp(-t * 80)))
    y += np.sin(2 * np.pi * 55 * t) * np.exp(-t * 6) * 0.8
    return y * vel


def crash(vel=1.0, dur=2.4):
    t = tvec(dur)
    return filt(noise(dur), "highpass", 4500) * np.exp(-t * 2.2) * (1 - np.exp(-t * 300)) * vel


def drumroll(dur, vel=1.0):
    n = int(dur * SR)
    y = np.zeros(n)
    rate = 26
    for k in range(int(dur * rate)):
        i = int(k / rate * SR + RNG.uniform(-60, 60))
        if 0 <= i < n:
            hit = filt(noise(0.06), "bandpass", [900, 7000]) * np.exp(-tvec(0.06) * 70)
            hit += np.sin(2 * np.pi * 190 * tvec(0.06)) * np.exp(-tvec(0.06) * 50) * 0.5
            g = 0.25 + 0.75 * (k / (dur * rate)) ** 1.6
            y[i:i + len(hit)] += hit[: n - i] * g * RNG.uniform(0.8, 1.1)
    return y * vel


def pop(vel=1.0):
    d = 0.18
    t = tvec(d)
    f = 300 + 1500 * (1 - np.exp(-t * 40))
    return (np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30) + filt(noise(d), "highpass", 2000) * np.exp(-t * 120) * 0.4) * vel


def slide(f0, f1, dur, vel=1.0):
    t = tvec(dur)
    f = f0 * (f1 / f0) ** (t / dur)
    vib = 1 + 0.02 * np.sin(2 * np.pi * 6 * t)
    y = np.sin(2 * np.pi * np.cumsum(f * vib) / SR) + 0.25 * np.sin(4 * np.pi * np.cumsum(f * vib) / SR)
    return y * env_adsr(len(t), a=0.03, r=0.12) * vel


def gliss(notes, step=0.06, vel=1.0):
    total = step * len(notes) + 2.0
    y = np.zeros(int(total * SR))
    for j, n in enumerate(notes):
        b = bell(hz(n), 0.6, 1.6)
        i = int(j * step * SR)
        y[i:i + len(b)] += b
    return y * vel


def wind(dur, vel=1.0):
    t = tvec(dur)
    x = filt(noise(dur), "bandpass", [200, 900])
    lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.7 * t)
    return x * lfo * env_adsr(len(t), a=0.4, r=0.6) * vel


def flutter(dur, vel=1.0):
    n = int(dur * SR)
    y = np.zeros(n)
    for k in range(int(dur * 14)):
        i = int((k / 14 + RNG.uniform(0, 0.03)) * SR)
        f = flick(RNG.uniform(0.3, 0.7), 2200)
        y[i:i + len(f)] += f[: max(0, n - i)]
    return y * vel


# --- score ---------------------------------------------------------------
CHORDS = {
    "Dm": ["D", "F", "A"], "Gm": ["G", "A#", "D"], "A7": ["A", "C#", "E", "G"], "Bb": ["A#", "D", "F"],
    "F": ["F", "A", "C"], "C": ["C", "E", "G"], "D": ["D", "F#", "A"], "G": ["G", "B", "D"], "C7": ["C", "E", "G", "A#"],
}
PROGRESSIONS = {
    "pick": ["Dm", "Dm", "Gm", "A7"],
    "force": ["Dm", "Bb", "Gm", "A7"],
    "trick1": ["Dm", "Bb", "Gm", "A7"],
    "trick2": ["Dm", "Gm", "A7", "Dm"],
    "trick3": ["Dm", "Bb", "Gm", "A7"],
    "reveal": ["F", "C", "Dm", "Bb", "F", "Bb", "C7", "F"],
    "end": ["D", "G", "A7", "D"],
}


def pc(name: str, octave: int) -> str:
    return f"{name}{octave}"


def score(tl, k, bus: Bus) -> list[tuple[float, float]]:
    bpm = 132
    beat = 60 / bpm
    bar = 3 * beat
    start = 0.75
    mutes = [
        (k.t1b_end + 0.05, k.here - 0.05),           # drum roll and the poof
        (k.thousand - 0.16, k.where - 0.05),         # the hard stop at a thousand
        (k.under - 0.1, k.under + 1.0),              # cloth whip: let it breathe
        (k.oh - 0.05, k.zoom_back - 0.05),           # the last trick plays almost dry
    ]
    order = list(tl.scenes)
    first_bar = {}
    b = 0
    while start + b * bar < tl.duration - 0.6:
        t0 = start + b * bar
        scene = next(s for s in order if tl.scenes[s][0] <= t0 + 0.2 < tl.scenes[s][1]) if t0 + 0.2 < tl.duration else order[-1]
        first_bar.setdefault(scene, b)
        if any(a <= t0 < z for a, z in mutes):
            b += 1
            continue
        prog_ = PROGRESSIONS[scene]
        chord = prog_[(b - first_bar[scene]) % len(prog_)]
        tones = CHORDS[chord]
        root = tones[0]
        sparse = scene == "pick"
        bright = scene in ("reveal", "end")
        # bass on one
        bus.add(t0, pizz(hz(pc(root, 2)), 0.9 if not sparse else 0.7, 0.9), 0.55, -0.05)
        if not sparse:
            for j in (1, 2):
                for n in tones[:3]:
                    octv = 4 if n in ("C", "C#", "D", "D#", "E") else 3
                    bus.add(t0 + j * beat, pizz(hz(pc(n, octv)), 0.33, 0.45), 0.5, -0.3)
        # celesta line: chord tones walking down, with a high answer every other bar
        line = [tones[2 % len(tones)], tones[1], tones[0]]
        if (b - first_bar[scene]) % 2 == 0:
            for j, n in enumerate(line):
                bus.add(t0 + j * beat, bell(hz(pc(n, 5)), 0.32 if sparse else 0.26), 0.5, 0.35)
        else:
            bus.add(t0, bell(hz(pc(tones[0], 6)), 0.2), 0.5, 0.4)
            if scene in ("trick2", "trick3"):
                bus.add(t0 + 1.5 * beat, bell(hz(pc(tones[1], 5)), 0.15), 0.5, 0.4)
        if bright:
            bus.add(t0, pad([hz(pc(n, 4)) for n in tones[:3]], bar + 0.4, 0.5, attack=0.25), 0.55)
        b += 1
    return mutes


def foley(tl, k, bus: Bus) -> None:
    # 1. pick a card
    bus.add(0.35, click(0.9), 0.45)
    bus.add(0.36, thud(52, 0.4, 0.4), 0.6)
    for j in range(16):
        bus.add(k.pick + 0.02 + j * 0.036, flick(RNG.uniform(0.5, 0.9)), 0.55, -0.6 + j * 0.075)
    for j in range(7):
        bus.add(k.got - 0.12 + j * 0.07, flick(0.55, 4200), 0.5, -0.5 + j * 0.16)
    bus.add(k.top - 0.18, gliss(["A5", "D6", "F6", "A6"], 0.07, 0.5), 0.45, 0.1)
    bus.add(k.top - 0.2, whoosh(0.4, 600, 2500, 0.3), 0.5)
    # 2. the force
    for j in range(8):
        bus.add(k.magicians - 0.25 + j * 0.04, flick(0.5), 0.5, 0.4 - j * 0.1)
    bus.add(k.force - 0.08, stamp_fx(1.0), 0.75)
    bus.add(k.force - 0.06, crash(0.25, 1.8), 0.3)
    for j in range(18):
        bus.add(k.made - 0.12 + j * 0.045, flick(RNG.uniform(0.5, 0.9)), 0.55, -0.8 + j * 0.095)
    for j in range(13):
        bus.add(k.made + 0.15 + j * 0.03, flick(0.4, 4500), 0.4, -0.8 + j * 0.13)
    bus.add(k.allday - 0.45, whoosh(0.6, 2500, 300, 0.6), 0.6, -0.5)
    bus.add(k.allday - 0.15, whoosh(0.55, 300, 1800, 0.7), 0.6)
    bus.add(k.allday + 0.35, snap(0.7), 0.6)
    bus.add(k.thani - 0.02, slide(880, 470, 0.75, 0.22), 0.5, 0.6)
    # 3. trick one
    bus.add(k.t1 - 0.6, whoosh(0.5, 1800, 300, 0.5), 0.5)
    bus.add(k.t1 - 0.2, bell(hz("D6"), 0.4), 0.45)
    bus.add(k.take - 0.35, whoosh(0.4, 400, 1500, 0.4), 0.5)
    for j in range(30):
        bus.add(k.take + 0.2 + j * (1.15 / 30) + RNG.uniform(-0.01, 0.01), click(RNG.uniform(0.25, 0.45)), 0.5, -0.2)
    for j in range(11):
        bus.add(k.shaz - 0.05 + j * 0.04, click(0.4), 0.5, 0.2)
    bus.add(k.shaz + 0.3, gliss(["D6", "F6", "A6", "C7", "D7"], 0.05, 0.6), 0.45, 0.35)
    for j in range(5):
        bus.add(k.take + 1.25 + j * 0.09, snap(0.55), 0.5, -0.6 + j * 0.3)
    bus.add(k.boolean - 0.1, thud(110, 0.5, 0.3), 0.5)
    bus.add(k.vanish - 0.05, bell(hz("A4"), 0.4), 0.4)
    poof_t = k.t1b_end + 1.5
    bus.add(k.t1b_end + 0.12, drumroll(poof_t - k.t1b_end - 0.12, 1.0), 0.55)
    bus.add(poof_t, poof(1.0), 0.75)
    bus.add(poof_t, crash(0.7), 0.45)
    bus.add(k.here - 0.32, brass([hz("D4"), hz("F#4"), hz("A4"), hz("D5")], 0.3, 0.8), 0.35)
    bus.add(k.here - 0.02, brass([hz("D4"), hz("F#4"), hz("A4"), hz("D5")], 1.1, 0.9), 0.3)
    for j in range(5):
        bus.add(k.here + j * 0.07, flick(0.6), 0.5, -0.6 + j * 0.3)
    bus.add(k.here + 0.1, filt(noise(0.25), "highpass", 2500) * np.exp(-tvec(0.25) * 12) * 0.4, 0.5, 0.5)
    # 4. trick two
    bus.add(k.t2 - 0.6, whoosh(0.5, 1800, 300, 0.5), 0.5)
    bus.add(k.t2 - 0.2, bell(hz("F6"), 0.4), 0.45)
    bus.add(k.t2 - 0.1, thud(80, 0.5, 0.4), 0.5, -0.4)
    for j in range(40):
        p = j / 40
        bus.add(k.about + 0.15 + (k.results - k.about - 0.05) * p ** 0.7, click(0.22), 0.5, 0.4)
    start, stop = k.tryit, k.thousand - 0.16
    N = 44
    for i in range(N):
        ti = start + (stop - start) * (i / (N - 1)) ** 0.62
        bus.add(ti, flick(RNG.uniform(0.55, 0.85)), 0.55, -0.5 + 0.8 * min(1, (i % 7) / 6))
    bus.add(stop, thud(60, 1.2, 0.7), 0.8)
    bus.add(stop + 0.02, stamp_fx(0.9), 0.6, 0.4)
    bus.add(k.where - 0.1, wind(2.2, 0.5), 0.35, -0.4)
    bus.add(k.where + 0.1, gliss(["A5", "F5", "D5", "A4"], 0.18, 0.5), 0.4, -0.4)
    # 5. trick three
    bus.add(k.t3 - 0.6, whoosh(0.5, 1800, 300, 0.5), 0.5)
    bus.add(k.t3 - 0.2, bell(hz("A6"), 0.4), 0.45)
    for x, pan in ((k.t3 - 0.1, -0.35), (k.t3 + 0.02, 0.35)):
        bus.add(x, thud(90, 0.45, 0.3), 0.5, pan)
    bus.add(k.ask + 0.15, flutter(k.sentence + 0.3 - k.ask, 0.6), 0.5, -0.4)
    bus.add(k.sentence + 0.42, thud(150, 0.4, 0.25), 0.5, -0.4)
    bus.add(k.keywords - 0.05, flutter(0.75, 0.6), 0.5, 0.4)
    bus.add(k.keywords + 0.72, thud(150, 0.4, 0.25), 0.5, 0.4)
    bus.add(k.thirteen - 0.05, pop(0.8), 0.6, -0.4)
    bus.add(k.thirteen, gliss(["D6", "F6"], 0.08, 0.4), 0.4, -0.4)
    f0 = k.thirtyfive - 0.08
    bus.add(f0, pop(1.0), 0.65, 0.4)
    bus.add(f0, whoosh(1.2, 300, 5000, 0.8), 0.35, 0.4)
    for j in range(50):
        bus.add(f0 + RNG.uniform(0, 1.6), flick(RNG.uniform(0.3, 0.7)), 0.3, RNG.uniform(-0.1, 0.9))
    bus.add(f0 + 0.05, gliss(["D6", "E6", "F#6", "A6", "B6", "D7", "E7", "F#7"], 0.04, 0.6), 0.25, 0.4)
    for j in range(30):
        bus.add(k.thirtyfive + (0.95 * (j / 30) ** 0.6), click(0.2), 0.45, 0.4)
    bus.add(k.very - 0.05, stamp_fx(0.6), 0.5)
    # 6. reveal
    bus.add(k.real_line - 0.4, whoosh(0.5, 1800, 300, 0.5), 0.5)
    for j in range(3):
        bus.add(k.real + j * 0.2 - 0.02, stamp_fx(0.85), 0.4, -0.5 + j * 0.5)
    bus.add(k.chapter - 0.15, whoosh(0.4, 500, 2500, 0.4), 0.5)
    bus.add(k.secrets - 0.35, whoosh(0.5, 2000, 300, 0.5), 0.5)
    bus.add(k.secrets + 0.05, flutter(0.3, 0.6), 0.5, -0.4)
    bus.add(k.secret_word - 0.03, stamp_fx(0.8), 0.55, -0.35)
    bus.add(k.tools - 0.1, thud(65, 0.7, 0.5), 0.6, 0.35)
    bus.add(k.tools + 0.3, click(0.6), 0.5, 0.35)
    bus.add(k.book - 0.3, whoosh(0.5, 2000, 300, 0.5), 0.5)
    bus.add(k.book - 0.05, gliss(["F5", "A5", "C6", "F6", "A6"], 0.06, 0.6), 0.45, -0.4)
    bus.add(k.free - 0.03, stamp_fx(0.6), 0.5, -0.3)
    for j, tt in enumerate(k.topics):
        bus.add(tt - 0.12, flick(0.7), 0.5, -0.2 + 0.12 * j)
        bus.add(tt + 0.3, snap(0.6), 0.5, 0.2 + 0.1 * (j % 3))
    bus.add(k.under - 0.1, whoosh(1.4, 200, 4000, 1.1), 0.75)
    bus.add(k.under + 0.6, pad([hz("F3"), hz("C4"), hz("A4"), hz("E5")], 2.6, 0.7, attack=0.6), 0.5)
    # 7. end
    bus.add(k.title_words[0][1] - 0.25, bell(hz("D5"), 0.5), 0.3)
    bus.add(k.oh - 0.05, whoosh(0.7, 3000, 400, 0.6), 0.55)
    for j in range(7):
        bus.add(k.oh + 0.2 + j * 0.05, flick(0.5), 0.45, -0.6 + j * 0.2)
    bus.add(k.pick_word - 0.08, click(0.5), 0.3, 0.3)
    bus.add(k.either_end + 0.05, gliss(["A5", "D6", "F#6", "A6", "D7"], 0.05, 0.6), 0.4, 0.2)
    bus.add(k.zoom_back - 0.05, whoosh(0.9, 400, 3000, 0.6), 0.5)
    bus.add(k.zoom_back + 0.75, brass([hz("D3"), hz("A3"), hz("D4"), hz("F#4"), hz("A4")], 2.4, 0.95), 0.6)
    bus.add(k.zoom_back + 0.75, crash(0.35, 3.0), 0.35)
    bus.add(k.zoom_back + 0.75, pizz(hz("D2"), 1.0, 1.4), 0.6)


# --- the voice's room ----------------------------------------------------
def room_ir() -> np.ndarray:
    dur = 0.45
    t = tvec(dur)
    ir = np.zeros(len(t))
    for ms, g in ((7, 0.5), (11, 0.4), (17, 0.32), (23, 0.25), (31, 0.18)):
        ir[int(ms / 1000 * SR)] += g
    tail = filt(noise(dur), "lowpass", 4500) * np.exp(-t * (6.9 / 0.32))
    tail[: int(0.012 * SR)] = 0
    ir += tail * 0.35
    return ir / np.sqrt(np.sum(ir ** 2))


def voice_chain(v: np.ndarray) -> np.ndarray:
    v = filt(v, "highpass", 75)
    ir_l, ir_r = room_ir(), room_ir()
    wet_l = fftconvolve(v, ir_l)[: len(v)]
    wet_r = fftconvolve(v, ir_r)[: len(v)]
    g = 10 ** (-17 / 20)
    return np.stack([v + wet_l * g, v + wet_r * g], axis=1)


def speech_mask(tl, n) -> np.ndarray:
    m = np.zeros(n)
    for take in tl.takes:
        a, b = int(max(0, take.start - 0.12) * SR), int(min(n, (take.end + 0.3) * SR))
        m[a:b] = 1
    # smooth: ~120 ms attack/350 ms release via one-pole filters both ways
    k_up, k_dn = np.exp(-1 / (0.06 * SR)), np.exp(-1 / (0.25 * SR))
    from scipy.signal import lfilter
    out = lfilter([1 - k_dn], [1, -k_dn], m)
    out = np.maximum(out, lfilter([1 - k_up], [1, -k_up], m[::-1])[::-1])
    return np.clip(out, 0, 1)


def ffmpeg_loudnorm(ff: str, raw: Path, dest: Path, out: Path) -> dict:
    base = [ff, "-hide_banner", "-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw)]
    first = subprocess.run(base + ["-af", "loudnorm=I=-16:TP=-2:LRA=11:print_format=json", "-f", "null", "-"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
    stats = json.loads(first.stderr[first.stderr.rindex("{"):first.stderr.rindex("}") + 1])
    af = ("loudnorm=I=-16:TP=-2:LRA=11:linear=true:"
          f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:measured_LRA={stats['input_lra']}:"
          f"measured_thresh={stats['input_thresh']}:offset={stats['target_offset']}")
    second = subprocess.run(base + ["-af", af + ",aresample=48000", "-c:a", "pcm_s16le", "-y", str(dest)],
                            capture_output=True, text=True, encoding="utf-8", errors="replace")
    (out / "loudnorm.log").write_text(first.stderr + "\n----\n" + second.stderr, encoding="utf-8")
    if second.returncode:
        raise SystemExit("mastering failed; see loudnorm.log")
    return stats


def write_wav(path: Path, x: np.ndarray) -> None:
    import wave
    x = np.clip(x, -1, 1)
    if x.ndim == 1:
        x = x[:, None]
    with wave.open(str(path), "wb") as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((x * 32767).astype("<i2").tobytes())


def build(tl, k, out: Path, ff: str) -> Path:
    n = int(round(tl.duration * SR))
    voice = voice_chain(narrate.voice_track(tl))[:n]
    music, fx = Bus(tl.duration), Bus(tl.duration)
    mutes = score(tl, k, music)
    foley(tl, k, fx)
    m, f = music.out(), fx.out()
    # hard musical stops, softened by 25 ms
    gate = np.ones(n)
    for a, z in mutes:
        ia, iz = int(a * SR), int(z * SR)
        r = int(0.025 * SR)
        gate[ia:iz] = 0
        gate[max(0, ia - r):ia] = np.minimum(gate[max(0, ia - r):ia], np.linspace(1, 0, ia - max(0, ia - r)))
    m *= gate[:, None]
    m = m / (np.sqrt(np.mean(m ** 2)) + 1e-9) * 10 ** (-26 / 20)
    f = f / (np.sqrt(np.mean(f[np.abs(f[:, 0]) > 1e-4] ** 2)) + 1e-9) * 10 ** (-24 / 20)
    mask = speech_mask(tl, n)[:, None]
    m *= 1 - (1 - 10 ** (-10 / 20)) * mask
    f *= 1 - (1 - 10 ** (-8 / 20)) * mask
    # faint room tone so the pauses between lines sound like a room, not a void
    ramp = np.clip((np.arange(n) / SR - 0.3) / 0.5, 0, 1)
    room = np.stack([filt(RNG.standard_normal(n), "lowpass", 900) for _ in range(2)], 1) * 10 ** (-66 / 20) * ramp[:, None]
    mix = voice + m + f + room
    balance = []
    for take in tl.takes:
        a, b = int(take.start * SR), int(take.end * SR)
        bed = m[a:b] + f[a:b]
        db = 20 * np.log10(np.sqrt(np.mean(voice[a:b] ** 2)) / (np.sqrt(np.mean(bed ** 2)) + 1e-12))
        balance.append({"line": take.id, "voice_over_bed_db": round(float(db), 1)})
    (out / "mix-balance.json").write_text(json.dumps(balance, indent=1), encoding="utf-8")
    worst = min(balance, key=lambda x: x["voice_over_bed_db"])
    print(f"  voice over music+foley: worst line {worst['line']} at {worst['voice_over_bed_db']} dB", flush=True)
    tail = int(0.6 * SR)
    mix[-tail:] *= np.linspace(1, 0, tail)[:, None] ** 2
    peak = np.max(np.abs(mix))
    mix = mix / peak * 0.89 if peak > 0.89 else mix
    write_wav(out / "stem-voice.wav", voice / max(1, np.max(np.abs(voice))))
    write_wav(out / "stem-music.wav", m / max(1e-9, np.max(np.abs(m))) * 0.8)
    write_wav(out / "stem-foley.wav", f / max(1e-9, np.max(np.abs(f))) * 0.8)
    raw = out / "mix.f32"
    raw.write_bytes(mix.astype("<f4").tobytes())
    dest = out / "soundtrack.wav"
    stats = ffmpeg_loudnorm(ff, raw, dest, out)
    raw.unlink()
    print(f"  mix measured {stats['input_i']} LUFS -> mastered to -16 LUFS", flush=True)
    return dest
