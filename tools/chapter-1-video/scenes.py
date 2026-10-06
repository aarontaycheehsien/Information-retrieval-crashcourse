"""Original geometric animations for Chapter 1; picture follows speech timings."""
from __future__ import annotations

from functools import lru_cache
import math
import os
from pathlib import Path
import re

import numpy as np
import skia

W, H = 1920, 1080
BG = (9, 12, 19)
WHITE = (231, 237, 245)
MUTED = (143, 164, 187)
BLUE = (112, 194, 233)
TEAL = (80, 207, 181)
GOLD = (255, 214, 110)
RED = (245, 116, 137)
PURPLE = (183, 151, 239)
DIM = (39, 53, 72)
FONT_DIR = Path(os.environ.get("CHAPTER_FONT_DIR", "C:/Windows/Fonts"))
FONTS = {"serif": "georgia.ttf", "italic": "georgiai.ttf", "ui": "segoeui.ttf",
         "bold": "segoeuib.ttf", "mono": "consola.ttf", "math": "seguisym.ttf"}


def clamp(p):
    return max(0.0, min(1.0, p))


def ease(p):
    p = clamp(p)
    return p * p * (3 - 2 * p)


def mix(a, b, p):
    return a + (b - a) * p


def color(rgb, a=1):
    return skia.Color(*rgb, round(clamp(a) * 255))


def paint(rgb, a=1, stroke=None):
    p = skia.Paint(AntiAlias=True, Color=color(rgb, a))
    if stroke is not None:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


@lru_cache(maxsize=None)
def font(kind, size):
    path = FONT_DIR / FONTS[kind]
    assert path.is_file(), f"Missing font: {path}; set CHAPTER_FONT_DIR"
    f = skia.Font(skia.Typeface.MakeFromFile(str(path)), size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    f.setSubpixel(True)
    return f


def text(c, s, x, y, size=34, rgb=WHITE, a=1, kind="ui", align="center", width=None):
    if a < .002 or not s:
        return
    f = font(kind, size)
    if width is not None and f.measureText(s) > width:
        f = font(kind, size * width / f.measureText(s))
    w = f.measureText(s)
    x0 = x - w / 2 if align == "center" else x - w if align == "right" else x
    # Every authored line has a checked position; fail before a long render if it clips.
    assert -1 <= x0 and x0 + w <= W + 1, f"Text outside frame: {s}"
    c.drawString(s, x0, y, f, paint(rgb, a))


def mixed(c, runs, x, y, size=35, rgb=GOLD, a=1):
    """Centre a formula with explicit math fonts, avoiding missing serif glyphs."""
    widths = [font(kind, size).measureText(s) for s, kind in runs]
    at = x - sum(widths) / 2
    for (s, kind), w in zip(runs, widths):
        text(c, s, at, y, size, rgb, a, kind, align="left")
        at += w


def lines(c, items, x, y, size=32, rgb=WHITE, a=1, kind="ui", step=46, width=None):
    for i, s in enumerate(items):
        text(c, s, x, y + i * step, size, rgb, a, kind, width=width)


def line(c, x1, y1, x2, y2, rgb=BLUE, a=1, stroke=3, p=1):
    if p <= 0 or a < .002:
        return
    c.drawLine(x1, y1, mix(x1, x2, p), mix(y1, y2, p), paint(rgb, a, stroke))


def arrow(c, start, end, rgb=BLUE, a=1, p=1, stroke=3):
    x1, y1 = start
    x2, y2 = end
    line(c, x1, y1, x2, y2, rgb, a, stroke, p)
    if p > .95:
        angle = math.atan2(y2 - y1, x2 - x1)
        for shift in (-.5, .5):
            line(c, x2, y2, x2 - 15 * math.cos(angle + shift), y2 - 15 * math.sin(angle + shift), rgb, a, stroke)


def box(c, x, y, w, h, rgb=BLUE, a=1, radius=18, fill=.04, stroke=2):
    rr = skia.RRect.MakeRectXY(skia.Rect.MakeXYWH(x, y, w, h), radius, radius)
    if fill:
        c.drawRRect(rr, paint(rgb, fill * a))
    c.drawRRect(rr, paint(rgb, a, stroke))


def dot(c, x, y, rgb=BLUE, radius=8, a=1, halo=False):
    if a <= .002:
        return
    if halo:
        for r, alpha in ((radius * 3, .07), (radius * 2, .14)):
            c.drawCircle(x, y, r, paint(rgb, alpha * a))
    c.drawCircle(x, y, radius, paint(rgb, a))


def ring(c, x, y, r, rgb=BLUE, a=1, p=1, stroke=3):
    if p <= .002:
        return
    c.drawArc(skia.Rect.MakeXYWH(x - r, y - r, r * 2, r * 2), -90, 360 * p, False, paint(rgb, a, stroke))


def paper(c, x, y, rgb=BLUE, a=1, scale=1, label=None):
    w, h = 52 * scale, 66 * scale
    c.save()
    c.translate(x - w / 2, y - h / 2)
    path = skia.Path()
    path.moveTo(0, 0)
    path.lineTo(w - 14 * scale, 0)
    path.lineTo(w, 14 * scale)
    path.lineTo(w, h)
    path.lineTo(0, h)
    path.close()
    c.drawPath(path, paint(BG, a))
    c.drawPath(path, paint(rgb, a, max(1.5, 2.5 * scale)))
    line(c, w - 14 * scale, 0, w - 14 * scale, 14 * scale, rgb, a, 1.5 * scale)
    line(c, w - 14 * scale, 14 * scale, w, 14 * scale, rgb, a, 1.5 * scale)
    if label:
        f = font("mono", 19 * scale)
        c.drawString(label, (w - f.measureText(label)) / 2, h * .62, f, paint(rgb, a))
    else:
        for i in range(3):
            line(c, 10 * scale, (28 + 10 * i) * scale, (37 - 4 * (i % 2)) * scale,
                 (28 + 10 * i) * scale, rgb, .55 * a, 2 * scale)
    c.restore()


class Film:
    def __init__(self, timeline, script):
        self.tl = timeline
        self.script = script
        self.takes = {tk["id"]: tk for tk in timeline["takes"]}
        self.ordered = script["scenes"]
        rng = np.random.default_rng(1081)
        self.cloud = np.column_stack((rng.uniform(230, 675, 160), rng.uniform(360, 730, 160)))

    def at(self, take, word=None, nth=0):
        tk = self.takes[take]
        if word is None:
            return tk["start"]
        norm = lambda s: re.sub(r"[^\w]", "", s).lower()
        hits = [w for w in tk["words"] if norm(w["text"]) == norm(word)]
        assert len(hits) > nth, f"Missing speech anchor: {take} / {word}"
        return hits[nth]["start"]

    def p(self, t, take, word=None, duration=.8, delay=0, nth=0):
        return ease((t - self.at(take, word, nth) - delay) / duration)

    def raw(self, t, take, word=None, duration=1, delay=0):
        return clamp((t - self.at(take, word) - delay) / duration)

    def header(self, c, title, number, t):
        text(c, "HOW SEARCH DECIDES WHAT YOU SEE", 96, 61, 20, MUTED, kind="mono", align="left")
        text(c, "CHAPTER 1", 1824, 61, 20, TEAL, kind="mono", align="right")
        text(c, title, 960, 159, 54, WHITE, kind="serif", width=1710)
        line(c, 96, 207, 1824, 207, DIM, stroke=1)
        text(c, f"{number:02d} / {len(self.ordered):02d}", 1824, 1034, 19, MUTED, kind="mono", align="right")
        text(c, "Aaron Tay · Chapter 1 · geometric teaching illustrations", 96, 1034, 18, MUTED, align="left")
        line(c, 96, 1070, 1824, 1070, DIM, stroke=2)
        line(c, 96, 1070, 1824, 1070, TEAL, stroke=2, p=t / self.tl["duration"])

    def note(self, c, s, rgb=MUTED, a=1, size=30):
        text(c, s, 960, 920, size, rgb, a, kind="italic", width=1660)

    def frame(self, c, t):
        c.clear(color(BG))
        for i, scene in enumerate(self.ordered):
            a, b = self.tl["scenes"][scene["id"]]
            if a <= t < b or (i == len(self.ordered) - 1 and t >= a):
                self.header(c, scene["title"], i + 1, t)
                getattr(self, scene["id"])(c, t)
                opacity = min(clamp((t - a) / .45), clamp((b - t) / .35))
                if opacity < 1:
                    c.drawRect(skia.Rect.MakeWH(W, H), paint(BG, 1 - opacity))
                return

    def opening(self, c, t):
        question = self.p(t, "o1", "ask")
        text(c, "Is there an open access citation advantage?", 960, 325, 43, BLUE, question, kind="serif")
        for i in range(5):
            p = self.p(t, "o2", "five", delay=i * .16)
            x = 510 + i * 225
            paper(c, x, mix(550, 480, p), TEAL, p, 1.65, str(i + 1))
        ans = self.p(t, "o2", "answer")
        box(c, 460, 605, 1000, 200, WHITE, ans, fill=.02)
        for i, (w, n) in enumerate(((760, "[1]"), (610, "[2,3]"), (730, "[4,5]"))):
            p = self.p(t, "o2", "summary", delay=i * .2)
            line(c, 510, 655 + i * 48, 510 + w * p, 655 + i * 48, MUTED, p, 4)
            text(c, n, 1345, 664 + i * 48, 27, TEAL, p, kind="mono")
        why = self.p(t, "o3", "Why")
        for i in range(5):
            ring(c, 510 + i * 225, 480, 83, GOLD, why, p=why, stroke=2)
        self.note(c, "Why these five papers?", GOLD, why, 44)

    def machines(self, c, t):
        p = self.p(t, "m1", "Retrieval")
        q = self.p(t, "m1", "Generation")
        box(c, 310, 380, 500, 300, BLUE, p)
        box(c, 1110, 380, 500, 300, TEAL, q)
        text(c, "RETRIEVAL", 560, 439, 32, BLUE, p, kind="mono")
        text(c, "GENERATION", 1360, 439, 32, TEAL, q, kind="mono")
        for i in range(4):
            paper(c, 425 + i * 90, 528, BLUE, p, .95)
        lines(c, ["select records", "order records"], 560, 614, 29, MUTED, p, step=42)
        for i in range(3):
            line(c, 1190, 505 + i * 45, 1520 - i * 28, 505 + i * 45, TEAL, q, 4,
                 self.p(t, "m1", "prose", delay=i * .15))
        text(c, "write an answer", 1360, 627, 29, MUTED, q)
        arrow(c, (830, 530), (1090, 530), WHITE, p=q)
        text(c, "supplied evidence", 960, 494, 24, MUTED, q)
        zoom = self.p(t, "m2", "first")
        ring(c, 560, 530, 274, GOLD, zoom, zoom, 3)
        self.note(c, "The writing step comes after evidence selection.", GOLD, self.p(t, "m2"))

    def primo(self, c, t):
        text(c, "Primo Research Assistant · documented example, September 2026", 960, 279, 25, MUTED)
        xs = [250, 610, 970, 1330, 1690]
        labels = [("Question", "natural language", BLUE), ("Query", "Boolean variants + OR", BLUE),
                  ("Candidates", "up to 30", BLUE), ("Working set", "5 abstracts", GOLD),
                  ("Overview", "generated prose", TEAL)]
        ps = [self.p(t, "p1"), self.p(t, "p1", "rewrites"), self.p(t, "p2", "thirty"),
              self.p(t, "p3", "five"), self.p(t, "p3", "write")]
        for i, (label, desc, rgb) in enumerate(labels):
            box(c, xs[i] - 135, 396, 270, 250, rgb, ps[i])
            text(c, label, xs[i], 444, 30, rgb, ps[i])
            if i == 0:
                text(c, "?", xs[i], 552, 83, BLUE, ps[i], kind="serif")
            elif i == 1:
                lines(c, ["query A", "OR query B"], xs[i], 512, 28, BLUE, ps[i], kind="mono")
            elif i == 2:
                for k in range(12):
                    dot(c, xs[i] - 60 + (k % 4) * 40, 484 + (k // 4) * 38, BLUE, 7, ps[i])
            elif i == 3:
                for k in range(5):
                    paper(c, xs[i] - 88 + k * 44, 530, GOLD, ps[i], .58)
            else:
                for k in range(3):
                    line(c, xs[i] - 88, 497 + k * 31, xs[i] + 83 - 15 * k, 497 + k * 31, TEAL, ps[i], 3)
            text(c, desc, xs[i], 617, 23, MUTED, ps[i], width=244)
            if i:
                arrow(c, (xs[i - 1] + 143, 526), (xs[i] - 143, 526), MUTED, p=ps[i])
        text(c, "LLM", xs[1], 734, 28, GOLD, ps[1], kind="mono")
        text(c, "embedding rerank", 1150, 354, 25, GOLD, self.p(t, "p3"))
        text(c, "LLM", xs[4], 734, 28, GOLD, ps[4], kind="mono")
        llm = self.p(t, "p4", "LLM")
        line(c, xs[1], 775, xs[4], 775, GOLD, llm, 2, llm)
        self.note(c, "“Uses an LLM” does not locate the retrieval method.", GOLD, llm)

    def sets(self, c, t):
        retrieve = self.p(t, "s1", "moves", duration=1.8)
        rerank = self.p(t, "s2", "order", duration=1.6)
        select = self.p(t, "s2", "five", duration=1.6)
        gold = self.p(t, "s3", "gold")
        box(c, 185, 320, 550, 480, BLUE, 1, radius=45, fill=.01)
        box(c, 820, 380, 410, 365, PURPLE, retrieve, radius=35)
        box(c, 1370, 440, 360, 255, TEAL, select, radius=30)
        text(c, "SEARCHABLE INDEX", 460, 295, 25, BLUE, kind="mono")
        text(c, "CANDIDATE SET", 1025, 350, 25, PURPLE, retrieve, kind="mono")
        text(c, "WORKING SET", 1550, 410, 25, TEAL, select, kind="mono")
        for i, (x, y) in enumerate(self.cloud):
            if i < 30:
                # Retain faint copies: selection does not remove records from the index.
                dot(c, x, y, BLUE, 4.5, .22 * retrieve)
                tx = 860 + i % 6 * 63
                ty = 426 + i // 6 * 64
                rank = (i * 7) % 30
                rx, ry = 860 + rank % 6 * 63, 426 + rank // 6 * 64
                tx, ty = mix(tx, rx, rerank), mix(ty, ry, rerank)
                px, py = mix(x, tx, retrieve), mix(y, ty, retrieve)
                if rank < 5:
                    dot(c, tx, ty, PURPLE, 6, .28 * select)
                    wx, wy = 1430 + rank * 60, 565
                    px, py = mix(px, wx, select), mix(py, wy, select)
                    dot(c, px, py, TEAL if select > .5 else PURPLE if retrieve > .5 else BLUE, 8, 1)
                else:
                    dot(c, px, py, PURPLE if retrieve > .5 else BLUE, 6, 1 - .58 * select)
            else:
                dot(c, x, y, BLUE, 4.5, .4)
        dot(c, 370, 585, GOLD, 11, gold, True)
        ring(c, 370, 585, 27, GOLD, gold, self.p(t, "s3", "never"), 2)
        text(c, "relevant, excluded", 445, 755, 25, GOLD, gold)
        arrow(c, (748, 565), (802, 565), PURPLE, p=retrieve)
        arrow(c, (1247, 565), (1352, 565), TEAL, p=select)
        text(c, "≤ 30", 1025, 802, 36, PURPLE, retrieve, kind="mono")
        text(c, "5", 1550, 750, 42, TEAL, select, kind="mono")
        if t >= self.at("s4"):
            mixed(c, [("Working set ", "italic"), ("⊆", "math"), (" candidate set ", "italic"),
                      ("⊆", "math"), (" searchable index", "italic")], 960, 920, a=self.p(t, "s4"))
        else:
            self.note(c, "Reordering candidates cannot add an excluded record.", GOLD, self.p(t, "s3", "Reordering"))
        text(c, "Within one retrieval round; a new retrieval route can add candidates.", 960, 976, 23,
             MUTED, self.p(t, "s5"))

    def missing(self, c, t):
        xs = [260, 610, 960, 1310, 1660]
        labels = ["Index", "Query", "Candidates", "Working set", "Answer"]
        for i, x in enumerate(xs):
            ring(c, x, 395, 58, DIM)
            paper(c, x, 395, BLUE if i < 3 else TEAL, 1, .88)
            text(c, labels[i], x, 302, 28, MUTED)
            if i:
                arrow(c, (xs[i - 1] + 70, 395), (x - 70, 395), DIM)
        events = [("d1", "outside", ["not indexed", "not available"], 0),
                  ("d1", "query", ["query misses it", "not admitted"], 1),
                  ("d1", "boundary", ["candidate cutoff", "never supplied"], 2),
                  ("d2", "five", ["selection cutoff", "never supplied"], 3),
                  ("d2", "omitted", ["supplied to writer", "omitted in answer"], 4)]
        for take, word, label, i in events:
            p = self.p(t, take, word)
            arrow(c, (xs[i], 465), (xs[i], 555), RED if i < 4 else GOLD, p=p)
            paper(c, xs[i], mix(480, 613, p), RED if i < 4 else GOLD, p, 1.3)
            lines(c, label, xs[i], 730, 25, MUTED, p, step=37)
        self.note(c, "A missing citation alone does not locate the failure.", GOLD, self.p(t, "d3"), 34)

    def map(self, c, t):
        names = [("Query", "transformation"), ("Analysis &", "execution"), ("First-stage", "retrieval"),
                 ("Fusion", "combine lists"), ("Reranking", "compare again"), ("Presentation", "what you see")]
        words = ["transformation", "analysis", "first", "fusion", "reranking", "presentation"]
        xs = [230 + i * 292 for i in range(6)]
        for i, (x, label, word) in enumerate(zip(xs, names, words)):
            p = self.p(t, "g1", word)
            rgb = [BLUE, BLUE, PURPLE, PURPLE, GOLD, TEAL][i]
            box(c, x - 120, 470, 240, 206, rgb, p)
            ring(c, x, 527, 23, rgb, p)
            text(c, str(i + 1), x, 535, 22, rgb, p, kind="mono")
            lines(c, label, x, 588, 26, WHITE, p, step=39)
            if i:
                arrow(c, (xs[i - 1] + 128, 571), (x - 128, 571), MUTED, p=p)
        ctrl = self.p(t, "g3", "controller")
        box(c, 112, 307, 1696, 85, TEAL, ctrl)
        text(c, "CONTROLLER · chooses and sequences the actions", 960, 362, 28, TEAL, ctrl, kind="mono")
        for x in xs:
            line(c, x, 394, x, 447, TEAL, ctrl, 1.5, ctrl)
        f = self.p(t, "g2", "Fusion")
        for i, rgb in enumerate((BLUE, TEAL)):
            for j in range(3):
                dot(c, xs[3] - 40 + i * 80, 750 + j * 23, rgb, 5, f)
        self.note(c, "A map of possible stages, not a universal recipe.", GOLD, self.p(t, "g2", "every"))

    def matrix(self, c, t):
        x0, y0, x1, y1 = 480, 770, 1490, 330
        px = self.p(t, "x1", "axis", duration=1)
        py = self.p(t, "x2", "axis", duration=1)
        arrow(c, (x0 - 70, y0 + 40), (x1 + 110, y0 + 40), BLUE, p=px)
        arrow(c, (x0 - 100, y0 + 10), (x0 - 100, y1 - 30), TEAL, p=py)
        line(c, 985, y1, 985, y0, DIM, p=px)
        line(c, x0, 550, x1, 550, DIM, p=py)
        text(c, "ranked records", 705, 869, 31, BLUE, px)
        text(c, "written answer", 1230, 869, 31, BLUE, px)
        lines(c, ["repeated", "retrieval"], 260, 435, 28, TEAL, py, step=40)
        lines(c, ["single", "pass"], 260, 667, 28, TEAL, py, step=40)
        labels = [(705, 667, "Quick search", "quick"), (1230, 667, "Quick answer", "answer"),
                  (705, 435, "Iterative search", "iterative"), (1230, 435, "Deep research", "deep")]
        for x, y, s, word in labels:
            p = self.p(t, "x2", word)
            box(c, x - 208, y - 67, 416, 112, BLUE if x == 705 else TEAL, p)
            text(c, s, x, y + 5, 33, WHITE, p, kind="serif")
        self.note(c, "Agency is a separate question: who chooses the next action?", GOLD, self.p(t, "x3"), 31)

    def need(self, c, t):
        explicit = self.p(t, "n1", "explicit")
        text(c, "Explicit · inspectable · reproducible", 960, 279, 30, MUTED, explicit)
        q = self.p(t, "n2")
        box(c, 120, 366, 505, 414, GOLD, q)
        text(c, "INFORMATION NEED", 373, 341, 26, GOLD, q, kind="mono")
        requirements = [("Recent empirical studies", "empirical"), ("Generative-AI services", "generative"),
                        ("Academic libraries", "academic"), ("Research support", "support")]
        for i, (s, word) in enumerate(requirements):
            reveal = self.p(t, "n2", word)
            dot(c, 165, 451 + i * 77, GOLD, 5, reveal)
            text(c, s, 192, 461 + i * 77, 28, WHITE, reveal, align="left", width=398)
        strategy = self.p(t, "n3", "terminology")
        box(c, 810, 366, 990, 414, BLUE, strategy)
        text(c, "SEARCHABLE REPRESENTATION", 1305, 341, 26, BLUE, strategy, kind="mono")
        alternatives = [("generative AI", "large language models", "generative"),
                        ("academic library", "university library", "academic"),
                        ("research support", "research consultation", "research")]
        for i, (left, right, word) in enumerate(alternatives):
            reveal = self.p(t, "n3", word)
            y = 450 + i * 77
            text(c, left, 1050, y, 28, BLUE, reveal, width=390)
            text(c, "OR", 1280, y, 24, GOLD, reveal, kind="mono")
            text(c, right, 1545, y, 28, BLUE, reveal, width=430)
            if i < 2:
                text(c, "AND", 1305, y + 39, 18, MUTED, self.p(t, "n3", alternatives[i + 1][2]), kind="mono")
        date = self.p(t, "n3", "date")
        line(c, 866, 658, 1744, 658, DIM, a=date, stroke=1)
        text(c, "Publication date: 2024 onwards", 1305, 726, 28, BLUE, date)
        arrow(c, (650, 565), (785, 565), GOLD, p=strategy)
        detailed = self.p(t, "n4", "detail")
        text(c, "Queries + filters + task briefs can express substantial detail.", 960, 852, 30, TEAL, detailed)
        self.note(c, "The representation informs suitability estimates; usefulness still needs assessment.", GOLD,
                  self.p(t, "n4", "suitability"), 28)

    def match(self, c, t):
        text(c, "Hypothetical example from Chapter 1", 960, 260, 24, MUTED)
        study = self.p(t, "r1", "study")
        box(c, 585, 312, 750, 247, BLUE, study)
        paper(c, 667, 425, BLUE, study, 1.65)
        facts = [("Empirical study of a library service", "empirical"),
                 ("Short demonstration", "demonstration"), ("Positive participant reactions", "positive")]
        for i, (label, word) in enumerate(facts):
            text(c, label, 730, 370 + i * 55, 29, WHITE, self.p(t, "r1", word), align="left", width=570)
        text(c, "MEETS THE STRATEGY · TOPICALLY SUITABLE", 960, 533, 21, BLUE,
             self.p(t, "r1", "conditions"), kind="mono")
        workshop = self.p(t, "r2", "workshop")
        decision = self.p(t, "r3", "purpose")
        arrow(c, (700, 574), (440, 652), TEAL, p=workshop)
        arrow(c, (1220, 574), (1470, 652), GOLD, p=decision)
        box(c, 140, 672, 630, 189, TEAL, workshop)
        text(c, "INTRODUCTORY WORKSHOP", 455, 711, 24, TEAL, workshop, kind="mono")
        lines(c, ["A useful example of an application", "and participants' responses"], 455, 763, 28,
              WHITE, self.p(t, "r2", "useful"), step=42)
        box(c, 1070, 672, 710, 189, GOLD, decision)
        text(c, "SERVICE-ADOPTION DECISION", 1425, 711, 24, GOLD, decision, kind="mono")
        for i, (label, word) in enumerate([("Answer accuracy?", "accuracy"), ("Staff workload?", "workload"),
                                           ("Actual consultations?", "consultations")]):
            text(c, label, 1425, 751 + i * 34, 25, WHITE, self.p(t, "r4", word))
        fixed = self.p(t, "r3", "fixed")
        lines(c, ["same study", "same match"], 920, 746, 24, BLUE, fixed, kind="mono", step=40)
        limited = self.p(t, "r4", "limited")
        text(c, "Useful illustration", 455, 900, 25, TEAL, workshop)
        text(c, "Limited evidence for this decision", 1425, 900, 25, GOLD, limited)
        text(c, "The paper contributes something; its contribution depends on the purpose.", 960, 968, 29, GOLD,
             self.p(t, "r5", "contribution"), kind="italic", width=1660)

    def lenses(self, c, t):
        refine = self.p(t, "l3", "refine", duration=1.2)
        px, py = 960, 570
        paper(c, px, mix(py, 335, refine), WHITE, 1, mix(2, 1.2, refine))
        lenses = [(450, 372, "Computed match", "system / algorithmic", BLUE, "computed"),
                  (1470, 372, "Topical suitability", "about the topic", PURPLE, "topical"),
                  (450, 731, "What someone learns", "cognitive", GOLD, "learns"),
                  (1470, 731, "Usefulness for a task", "situational", TEAL, "usefulness")]
        for x, y, title, label, rgb, word in lenses:
            p = self.p(t, "l1", word) * (1 - refine)
            arrow(c, (px + (75 if x > px else -75), py + (35 if y > py else -35)),
                  (x + (-220 if x > px else 220), y), rgb, .6 * (1 - refine), p)
            box(c, x - 250, y - 60, 500, 132, rgb, p)
            text(c, title, x, y - 3, 31, rgb, p)
            text(c, label, x, y + 47, 24, MUTED, p)
        text(c, "Related perspectives, not a fixed ladder", 960, 260, 28, MUTED,
             self.p(t, "l2") * (1 - refine))
        text(c, "Detailed requests + feedback can inform suitability estimates.", 960, 870, 28, TEAL,
             self.p(t, "l2", "feedback") * (1 - refine))
        if refine > .002:
            text(c, "Bring the representation closer to the need", 960, 410, 32, MUTED, refine)
            box(c, 135, 472, 505, 214, BLUE, refine)
            text(c, "REFINE THE STRATEGY", 388, 519, 24, BLUE, refine, kind="mono")
            text(c, "Accuracy evaluations", 388, 585, 29, WHITE, self.p(t, "l3", "accuracy"))
            text(c, "Operational evidence", 388, 633, 29, WHITE, self.p(t, "l3", "operational"))
            box(c, 725, 472, 470, 214, PURPLE, self.p(t, "l3", "studies"))
            text(c, "RETRIEVED STUDIES", 960, 519, 24, PURPLE, self.p(t, "l3", "studies"), kind="mono")
            for i in range(3):
                paper(c, 875 + i * 85, 599, PURPLE, self.p(t, "l3", "studies"), .9)
            box(c, 1280, 472, 505, 214, TEAL, self.p(t, "l3", "assess"))
            text(c, "ASSESS THE EVIDENCE", 1533, 519, 24, TEAL, self.p(t, "l3", "assess"), kind="mono")
            for i, (s, word) in enumerate([("What did they measure?", "measure"),
                                           ("Under what conditions?", "conditions"),
                                           ("Support for this decision?", "support")]):
                text(c, s, 1533, 564 + i * 42, 27, WHITE, self.p(t, "l3", word), width=450)
            arrow(c, (655, 581), (708, 581), BLUE, p=self.p(t, "l3", "studies"))
            arrow(c, (1210, 581), (1263, 581), TEAL, p=self.p(t, "l3", "assess"))
            feedback = self.p(t, "l4", "together", duration=1.8)
            line(c, 1533, 701, 1533, 782, GOLD, p=clamp(feedback * 3))
            line(c, 1533, 782, 388, 782, GOLD, p=clamp(feedback * 3 - 1))
            arrow(c, (388, 782), (388, 701), GOLD, p=clamp(feedback * 3 - 2))
            text(c, "Use assessment to refine the next search", 960, 837, 29, GOLD, feedback)
        self.note(c, "Relevant to someone, for something.", GOLD, self.p(t, "l4", "Relevant"), 43)

    def puzzle1(self, c, t):
        p = self.p(t, "b1", "word")
        text(c, "open access citation advantage", 960, 300, 33, BLUE)
        text(c, "+ shazamblix", 960, 361, 42, RED, p, kind="mono")
        strict = self.p(t, "b1", "AND")
        ring(c, 530, 611, 126, BLUE, strict, strict)
        for i in range(7):
            angle = i * math.tau / 7
            dot(c, 530 + 71 * math.cos(angle), 611 + 71 * math.sin(angle), BLUE, 7, strict)
        ring(c, 835, 611, 104, RED, strict, strict)
        text(c, "∩", 696, 628, 55, WHITE, strict, kind="math")
        text(c, "∅", 835, 634, 58, RED, strict, kind="math")
        text(c, "=", 982, 628, 43, WHITE, strict, kind="mono")
        text(c, "∅", 1110, 634, 63, RED, strict, kind="math")
        text(c, "real terms", 530, 787, 26, BLUE, strict)
        text(c, "required nonsense", 835, 787, 26, RED, strict)
        obs = self.p(t, "b2", "returns")
        box(c, 1330, 482, 310, 282, TEAL, obs)
        for i in range(3):
            paper(c, 1410 + i * 75, 604, TEAL, obs, .92)
        text(c, "observed: results", 1485, 718, 24, TEAL, obs)
        self.note(c, "This challenges strict AND; it does not prove semantic retrieval.", GOLD,
                  self.p(t, "b2", "prove"), 30)
        text(c, "scite example in Chapter 1 · mechanism left open", 960, 978, 23, MUTED, obs)

    def puzzle2(self, c, t):
        p = self.p(t, "h1", "million", duration=2)
        q = self.p(t, "h1", "thousand", duration=1.1)
        n = round(9_400_000 * p)
        text(c, f"{n:,}", 650, 380, 78, BLUE, kind="mono")
        text(c, "reported results", 650, 435, 28, MUTED)
        text(c, f"{round(1000 * q):,}", 1430, 380, 78, TEAL, q, kind="mono")
        text(c, "viewable records", 1430, 435, 28, MUTED, q)
        # Logarithmic scale is labelled: the small visible boundary remains legible.
        line(c, 240, 732, 1640, 732, DIM, stroke=3)
        for exponent in range(8):
            x = 240 + exponent * 200
            line(c, x, 720, x, 745, MUTED, stroke=1)
            text(c, f"10^{exponent}", x, 789, 22, MUTED, kind="mono")
        c.drawRect(skia.Rect.MakeXYWH(240, 590, 1394 * p, 64), paint(BLUE, .65))
        c.drawRect(skia.Rect.MakeXYWH(240, 668, 600 * q, 36), paint(TEAL, .85))
        text(c, "logarithmic scale · count and accessible window are different quantities", 960, 849, 25, MUTED)
        self.note(c, "Reported total ≠ a demonstrated set of individually ranked records.", GOLD,
                  self.p(t, "h3"), 30)
        text(c, "Chapter 1's observed count; Google Scholar help documents a 1,000-result display limit.", 960, 977, 22, MUTED)

    def puzzle3(self, c, t):
        a = self.p(t, "q1", "thirteen")
        b = self.p(t, "q2", "hundred", duration=1.6)
        text(c, "Semantic Scholar · chapter observation, August 2026", 960, 270, 25, MUTED)
        text(c, "Is there an open access citation advantage", 960, 364, 39, BLUE, kind="serif")
        text(c, "13", 1640, 449, 49, BLUE, a, kind="mono")
        c.drawRect(skia.Rect.MakeXYWH(230, 410, 5 + 32 * a, 56), paint(BLUE, .85 * a))
        text(c, "open access citation advantage", 960, 604, 39, TEAL, self.p(t, "q2"), kind="serif")
        text(c, "≈ 35,300", 1580, 692, 49, TEAL, b, kind="mono")
        c.drawRect(skia.Rect.MakeXYWH(230, 650, 1060 * b, 56), paint(TEAL, .85 * b))
        text(c, "Bars show direction; the smaller bar is enlarged for visibility.", 960, 787, 24, MUTED, b)
        text(c, "35,300 ÷ 13 ≈ 2,715×", 960, 849, 35, GOLD, b, kind="mono")
        self.note(c, "A product label does not specify the retrieval architecture.", GOLD, self.p(t, "q3"), 33)

    def test(self, c, t):
        prompt = self.p(t, "t1")
        for i in range(5):
            paper(c, 760 + i * 100, 340, TEAL, prompt, .93, str(i + 1))
        paper(c, 400, 340, GOLD, prompt, 1.5, "?")
        text(c, "Landmark paper missing", 960, 452, 42, GOLD, prompt, kind="serif")
        root = self.p(t, "t2", "working")
        text(c, "Did it enter the working set?", 960, 549, 35, WHITE, root)
        yes = self.p(t, "t2", "did")
        no = self.p(t, "t2", "not")
        arrow(c, (885, 580), (570, 670), TEAL, p=yes)
        arrow(c, (1035, 580), (1350, 670), BLUE, p=no)
        text(c, "YES", 705, 625, 26, TEAL, yes, kind="mono")
        text(c, "NO", 1215, 625, 26, BLUE, no, kind="mono")
        box(c, 240, 686, 660, 132, TEAL, yes)
        lines(c, ["Inspect how supplied sources", "were selected and used in generation"], 570, 736, 29, TEAL, yes, step=43)
        box(c, 1020, 686, 660, 132, BLUE, no)
        lines(c, ["Trace query → index → candidates", "→ reranking → supplied sources"], 1350, 736, 29, BLUE, no, step=43)
        self.note(c, "A new direct search tests availability, not the original exclusion point.", GOLD,
                  self.p(t, "t3"), 29)

    def closing(self, c, t):
        p = self.p(t, "c1", "backwards", duration=1.8)
        xs = [425, 960, 1495]
        for i, (x, s, rgb) in enumerate(zip(xs, ["What was searched?", "What was selected?", "What was supplied?"], [BLUE, GOLD, TEAL])):
            q = self.p(t, "c1", ["searched", "selected", "supplied"][i])
            ring(c, x, 486, 98, rgb, q, q)
            if i == 0:
                for j in range(9):
                    dot(c, x - 43 + j % 3 * 43, 443 + j // 3 * 43, rgb, 6, q)
            else:
                paper(c, x, 486, rgb, q, 1.5)
            text(c, s, x, 645, 32, rgb, q, kind="serif")
        arrow(c, (1378, 486), (1078, 486), GOLD, p=p)
        arrow(c, (842, 486), (543, 486), BLUE, p=p)
        end = self.p(t, "c2")
        text(c, "THE RETRIEVAL PROBLEM", 960, 785, 36, WHITE, end, kind="mono")
        text(c, "Next: Chapter 2 · Boolean admission and the inverted index", 960, 858, 29, MUTED, end)
        text(c, "Adapted from Aaron Tay's Chapter 1 · CC BY 4.0 · original animation", 960, 942, 22, MUTED, end)
        text(c, "Synthetic narration: Microsoft Andrew Multilingual", 960, 979, 21, MUTED, end)

    def poster(self, c):
        c.clear(color(BG))
        text(c, "HOW SEARCH DECIDES WHAT YOU SEE · CHAPTER 1", 960, 140, 27, TEAL, kind="mono")
        text(c, "The retrieval problem", 960, 284, 90, WHITE, kind="serif")
        text(c, "What decided which papers your AI answer could cite?", 960, 376, 37, MUTED)
        for i in range(55):
            x, y = 275 + (i % 11) * 38, 501 + (i // 11) * 41
            dot(c, x, y, BLUE, 6, .7)
        box(c, 235, 458, 465, 267, BLUE)
        arrow(c, (742, 590), (970, 590), BLUE)
        box(c, 1010, 482, 595, 218, TEAL)
        for i in range(5):
            paper(c, 1080 + i * 112, 590, TEAL, 1, 1.2, str(i + 1))
        dot(c, 466, 581, GOLD, 11, 1, True)
        ring(c, 466, 581, 30, GOLD)
        text(c, "The evidence you see began with a selection.", 960, 853, 42, GOLD, kind="italic")
        text(c, "Aaron Tay · narrated geometric explainer", 960, 957, 25, MUTED)
