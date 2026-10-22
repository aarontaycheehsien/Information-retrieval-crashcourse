"""Original paper-and-ink experiments; reveals follow the narrated takes."""
from __future__ import annotations

from functools import lru_cache
import math
import os
from pathlib import Path

import skia

W, H = 1920, 1080
CREAM, PAPER = (238, 233, 224), (250, 248, 243)
INK, MUTED, RULE = (37, 39, 40), (110, 107, 99), (204, 196, 182)
RED, BLUE, TEAL, GOLD = (173, 61, 45), (47, 87, 123), (37, 108, 99), (190, 137, 35)
FONT_DIR = Path(os.environ.get("PREFACE_FONT_DIR", "/usr/share/fonts/truetype/dejavu"))


def clamp(x):
    return min(1., max(0., x))


def ease(x):
    x = clamp(x)
    return x*x*(3-2*x)


def lerp(a, b, p):
    return a+(b-a)*p


def paint(rgb, a=1, stroke=None):
    p = skia.Paint(AntiAlias=True, Color=skia.Color(*rgb, round(255*clamp(a))))
    if stroke is not None:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
    return p


@lru_cache(maxsize=None)
def font(size, bold=False, serif=False):
    name = "DejaVuSerif.ttf" if serif else "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = FONT_DIR/name
    assert path.is_file(), f"Missing font {path}; set PREFACE_FONT_DIR"
    f = skia.Font(skia.Typeface.MakeFromFile(str(path)), size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def text(c, s, x, y, size=32, color=INK, a=1, bold=False, align="left", width=None, serif=False):
    if a < .003:
        return
    f = font(size, bold, serif)
    if width and f.measureText(s) > width:
        f = font(size*width/f.measureText(s), bold, serif)
    w = f.measureText(s)
    x = x-w/2 if align == "center" else x-w if align == "right" else x
    assert -1 <= x and x+w <= W+1, f"Text outside frame: {s}"
    assert 0 <= y-f.getSize() and y <= H, f"Vertical overflow: {s}"
    c.drawString(s, x, y, f, paint(color, a))


def rows(c, labels, x, y, size=32, color=INK, a=1, step=None, **kw):
    for i, label in enumerate(labels):
        text(c, label, x, y+i*(step or size*1.45), size, color, a, **kw)


def rect(c, x, y, w, h, color=PAPER, a=1, radius=7, stroke=None):
    c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), radius, radius, paint(color, a, stroke))


def line(c, x, y, xx, yy, color=RULE, a=1, stroke=2):
    c.drawLine(x, y, xx, yy, paint(color, a, stroke))


def arrow(c, x, y, xx, yy, color=RED, a=1, stroke=3):
    line(c, x, y, xx, yy, color, a, stroke)
    angle = math.atan2(yy-y, xx-x)
    for delta in [-.5, .5]:
        line(c, xx, yy, xx-18*math.cos(angle+delta), yy-18*math.sin(angle+delta), color, a, stroke)


def circle(c, x, y, r, color=INK, a=1, stroke=None):
    c.drawCircle(x, y, r, paint(color, a, stroke))


def pill(c, label, x, y, color=RED, a=1, size=22):
    w = font(size, True).measureText(label)+30
    rect(c, x, y, w, 40, color, a, 4)
    text(c, label, x+15, y+28, size, PAPER, a, True)


def card(c, x, y, label="", w=190, h=230, color=BLUE, a=1, angle=0, detail=None):
    c.save()
    c.rotate(angle, x+w/2, y+h/2)
    rect(c, x+7, y+9, w, h, INK, .1*a, 5)
    rect(c, x, y, w, h, PAPER, a, 5)
    rect(c, x, y, w, 6, color, a, 1)
    rect(c, x, y, w, h, RULE, a, 5, 1)
    text(c, label, x+18, y+48, min(32, w*.22), color, a, True, width=w-36)
    if detail:
        rows(c, detail, x+18, y+95, min(26, w*.1), INK, a, width=w-36)
    else:
        for i in range(4):
            line(c, x+18, y+h*(.47+i*.105), x+w*(.86 if i%2 == 0 else .68), y+h*(.47+i*.105), RULE, a, 2)
    c.restore()


def panel(c, x, y, w, h, title, body, color=BLUE, a=1):
    rect(c, x+6, y+8, w, h, INK, .06*a)
    rect(c, x, y, w, h, PAPER, a)
    rect(c, x, y, w, 7, color, a, 1)
    text(c, title, x+30, y+65, 32, color, a, True, width=w-60)
    rows(c, body, x+30, y+130, 27, INK, a, step=48, width=w-60)


class Film:
    def __init__(self, timeline, script):
        self.tl, self.script = timeline, script
        self.takes = {t["id"]: t for t in timeline["takes"]}
        self.scenes = script["scenes"]
        self.accent = {"blue": BLUE, "red": RED, "teal": TEAL}[script["accent"]]
        import sys
        from types import SimpleNamespace
        voice = sys.modules.get("chapter_voice")
        if voice is None:
            import importlib.util
            spec = importlib.util.spec_from_file_location("chapter_voice", Path(__file__).parents[1]/"pick-a-card"/"narrate.py")
            voice = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = voice
            spec.loader.exec_module(voice)
        self.captions = voice.captions(SimpleNamespace(takes=[SimpleNamespace(**t) for t in timeline["takes"]]))

    def reveal(self, t, scene, n=1, delay=0, duration=.8):
        return ease((t-self.takes[f"{scene['id']}_{n}"]["start"]-delay)/duration)

    def frame(self, c, t):
        c.clear(skia.Color(*CREAM))
        scene = next((s for s in self.scenes if self.tl["scenes"][s["id"]][0] <= t < self.tl["scenes"][s["id"]][1]), self.scenes[-1])
        start, end = self.tl["scenes"][scene["id"]]
        for y in range(230, 930, 70):
            line(c, 60, y, 1860, y, RULE, .14, 1)
        text(c, "HOW SEARCH DECIDES WHAT YOU SEE", 100, 63, 21, MUTED, bold=True)
        text(c, f"BEFORE CHAPTER 1   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
        line(c, 100, 87, 1820, 87)
        text(c, scene["title"], 100, 165, 49, INK, bold=True, width=1700)
        c.save()
        zoom = 1+.014*ease((t-start)/(end-start))
        c.translate(960, 550)
        c.scale(zoom, zoom)
        c.translate(-960, -550)
        getattr(self, scene["visual"])(c, t, scene)
        c.restore()
        fade = max(1-ease((t-start)/.25), ease((t-end+.2)/.2))
        if fade:
            rect(c, 0, 200, W, 730, CREAM, fade, 0)
        for cue in self.captions:
            if cue["start"] <= t < cue["end"]:
                w = min(1710, font(30).measureText(cue["text"])+62)
                rect(c, (W-w)/2, 950, w, 56, INK, .96, 5)
                text(c, cue["text"], 960, 989, 30, PAPER, align="center", width=1650)
                break
        text(c, "Adapted from Aaron Tay · Preface · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original teaching illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Schematic teaching illustration · No product behavior measured"):
        text(c, message, 960, 900, 21, MUTED, align="center", width=1700)

    def prediction(self, c, t, s):
        p = self.reveal(t, s)
        text(c, "THE COLLECTION", 155, 280, 24, MUTED, bold=True)
        selected = [1, 3, 7]
        for i in range(8):
            card(c, 155+(i%4)*222, 320+(i//4)*252, chr(65+i), 170, 210,
                 BLUE if i in selected else MUTED, 1 if i in selected else 1-.65*p, angle=(i%3-1)*1.5)
        arrow(c, 1060, 535, 1195, 535, BLUE)
        text(c, "THREE RESULTS", 1280, 280, 24, BLUE, bold=True)
        for i, label in enumerate(["B", "D", "H"]):
            newpos = {"H": 0, "B": 1, "D": 2}[label]
            y = 340+lerp(i, newpos, p)*144
            rect(c, 1260, y, 500, 110, PAPER)
            text(c, str(round(lerp(i, newpos, p))+1), 1300, y+70, 42, BLUE, bold=True)
            text(c, f"Paper {label}", 1390, y+68, 34, INK)
        pill(c, "What about the unseen five?", 1235, 812, RED, p)
        self.note(c, "Eight imaginary papers · Three selected results · Reordering preserves membership")

    def admission(self, c, t, s):
        p = self.reveal(t, s)
        text(c, "AVAILABLE COLLECTION", 150, 290, 24, MUTED, bold=True)
        for i in range(8):
            card(c, 160+(i%4)*172, 340+(i//4)*205, chr(65+i), 135, 170, MUTED, .85)
        line(c, 990, 310, 990, 805, BLUE, stroke=8)
        rect(c, 950, 430, 80, 240, CREAM)
        pill(c, "ADMISSION", 890, 255, BLUE)
        arrow(c, 860, 550, 1110, 550, BLUE, stroke=4)
        for i, label in enumerate(["B", "D", "H"]):
            card(c, 1180+i*195, 410, label, 170, 230, BLUE, angle=(i-1)*2)
        rows(c, ["Which papers", "get through?"], 1450, 750, 40, BLUE, p, align="center", bold=True)
        self.note(c)

    def ranking(self, c, t, s):
        p = self.reveal(t, s)
        text(c, "THE SAME THREE CANDIDATES", 960, 285, 26, BLUE, bold=True, align="center")
        for i, label in enumerate(["B", "D", "H"]):
            destination = {"H": 0, "B": 1, "D": 2}[label]
            x = lerp(500+i*330, 500+destination*330, p)
            card(c, x, 380-30*math.sin(p*math.pi)*(i+1), label, 230, 280, BLUE, angle=(i-1)*2*(1-p))
        for i in range(3):
            circle(c, 615+i*330, 740, 36, BLUE)
            text(c, str(i+1), 615+i*330, 752, 32, PAPER, bold=True, align="center")
        text(c, "Position changes. Membership stays fixed.", 960, 837, 35, RED, p, bold=True, align="center")
        self.note(c)

    def history(self, c, t, s):
        p = self.reveal(t, s)
        line(c, 290, 480, 1650, 480, RULE, stroke=4)
        for x, label, body, col in [(350, "LIBRARY SCHOOL", ["Search syntax", "TF-IDF: a brief introduction"], MUTED),
                                    (960, "AROUND 2022", ["The machinery matters", "A scattered learning journey"], BLUE),
                                    (1570, "THIS BOOK", ["Practical questions", "One connected explanation"], TEAL)]:
            circle(c, x, 480, 14, col)
            text(c, label, x, 410, 25, col, bold=True, align="center")
            rows(c, body, x, 570, 26, INK, align="center", width=490)
        rect(c, 280, 700, 1360, 100, PAPER, p)
        text(c, "Different engine → different query choices → different papers found", 960, 760, 29, BLUE, p, align="center", width=1280)
        self.note(c, "The timeline reflects the author's own account in the preface")

    def labels(self, c, t, s):
        p = self.reveal(t, s)
        rect(c, 660, 360, 600, 310, INK)
        text(c, "SEARCH", 960, 485, 62, PAPER, bold=True, align="center")
        text(c, "What's inside?", 960, 570, 36, PAPER, align="center")
        tags = [(180, 290, "semantic"), (1430, 290, "vector"), (150, 530, "neural"),
                (1460, 530, "embedding"), (330, 745, "agentic"), (1280, 745, "AI-powered")]
        for i, (x, y, label) in enumerate(tags):
            drift = 4*math.sin(t*.45+i)
            pill(c, label, x, y+drift, BLUE if i%2 else RED)
        text(c, "A label alone does not specify a mechanism.", 960, 850, 33, RED, p, bold=True, align="center", width=1690)
        self.note(c, "Semantic search is not simply another name for dense retrieval")

    def mechanisms(self, c, t, s):
        p = self.reveal(t, s)
        for x, title, body, col in [(140, "DOCUMENTED", ["What the vendor states", "Which layer it describes", "When it was checked"], TEAL),
                                    (710, "OBSERVED", ["What your search shows", "What you can repeat", "What it can establish"], BLUE),
                                    (1280, "UNKNOWN", ["What remains hidden", "What needs investigation", "What a label cannot settle"], RED)]:
            panel(c, x, 340, 500, 385, title, body, col)
        text(c, "Keep each claim attached to its evidence.", 960, 825, 38, INK, p, bold=True, align="center")
        self.note(c, "No single neural architecture has simply replaced lexical retrieval")

    def twoquestions(self, c, t, s):
        p = self.reveal(t, s)
        for x, n, title, body, col in [(180, "01", "WHO GETS IN?", ["Candidate-set membership", "Which papers are available?"], BLUE),
                                      (1020, "02", "WHO COMES FIRST?", ["Ordering the candidates", "Which papers are easiest to see?"], RED)]:
            text(c, n, x, 400, 124, col, bold=True)
            line(c, x, 445, x+700, 445, col, stroke=3)
            text(c, title, x, 520, 40, col, bold=True, width=710)
            rows(c, body, x, 600, 30, INK, width=710)
        text(c, "Ask both.", 960, 823, 58, INK, p, bold=True, align="center")
        self.note(c, "The central distinction in Aaron Tay's preface")

    def answer(self, c, t, s):
        p = self.reveal(t, s)
        panel(c, 220, 300, 940, 490, "AN IMAGINARY AI ANSWER", ["A fluent explanation of the evidence.", "A confident conclusion.", "Three neatly formatted citations.", "[A]             [B]             [C]"], RED)
        for i, label in enumerate(["A", "B", "C"]):
            card(c, 1300+i*25, 360+i*100, label, 280, 210, TEAL, angle=(i-1)*4)
        pill(c, "All references exist", 1200, 760, TEAL)
        text(c, "What did that actually prove?", 700, 850, 36, RED, p, bold=True, align="center")
        self.note(c, "Fictional answer and references; the example tests a distinction")

    def existence(self, c, t, s):
        p = self.reveal(t, s)
        for i in range(3):
            card(c, 350+i*470, 360, chr(65+i), 260, 300, TEAL)
            pill(c, "EXISTS", 400+i*470, 710, TEAL)
        text(c, "One question answered.", 960, 280, 39, TEAL, bold=True, align="center")
        text(c, "Faithfulness?      Evidence selection?", 960, 835, 37, RED, p, bold=True, align="center")
        self.note(c)

    def faithfulness(self, c, t, s):
        p = self.reveal(t, s)
        panel(c, 160, 350, 650, 380, "WHAT THE PAPER SAYS", ["The result is uncertain.", "More investigation is needed."], TEAL)
        arrow(c, 850, 545, 1040, 545, RED)
        panel(c, 1100, 350, 650, 380, "WHAT THE ANSWER CLAIMS", ["The conclusion is settled.", "The evidence is conclusive."], RED, 1-p)
        panel(c, 1100, 350, 650, 380, "THE CORRECTED DESCRIPTION", ["The result is uncertain.", "More investigation is needed."], TEAL, p)
        text(c, "Real reference ≠ faithful description", 960, 830, 40, RED, bold=True, align="center", width=1680)
        self.note(c, "Invented uncertain-result example; no claim about a real study")

    def missing(self, c, t, s):
        p = self.reveal(t, s)
        rect(c, 180, 320, 900, 430, PAPER)
        text(c, "EVIDENCE THE WRITER RECEIVED", 630, 385, 27, RED, bold=True, align="center")
        for i in range(3):
            card(c, 270+i*250, 440, chr(65+i), 190, 230, TEAL)
        arrow(c, 1100, 540, 1260, 540, RED)
        panel(c, 1290, 390, 450, 310, "THE ANSWER", ["Fluent", "Carefully cited", "Still incomplete?"], RED)
        card(c, 750, 760, "P", 170, 115, GOLD, p)
        text(c, "Relevant paper never supplied", 980, 829, 29, GOLD, p, bold=True, width=790)
        self.note(c)

    def envelopes(self, c, t, s):
        p = self.reveal(t, s)
        for x, title, labels, col in [(200, "ENVELOPE ONE", ["A", "B", "C", "P"], TEAL),
                                       (1050, "ENVELOPE TWO", ["A", "B", "C"], RED)]:
            text(c, title, x+300, 290, 30, col, bold=True, align="center")
            for i, label in enumerate(labels):
                card(c, x+30+i*110, 350+15*(i%2), label, 160, 220, GOLD if label == "P" else col)
            rect(c, x, 505, 650, 225, PAPER)
            line(c, x, 505, x+325, 660, RULE)
            line(c, x+650, 505, x+325, 660, RULE)
            text(c, "Perfect description", x+325, 800, 34, col, p, bold=True, align="center")
        text(c, "Different evidence available", 960, 864, 33, INK, p, bold=True, align="center")
        self.note(c, "Thought experiment · Good writing cannot supply an absent paper")

    def diagnosis(self, c, t, s):
        p = self.reveal(t, s)
        labels = ["Collection", "Candidates", "Ranking", "Supplied", "Cited"]
        for i, label in enumerate(labels):
            x = 145+i*342
            rect(c, x, 400, 265, 160, PAPER)
            text(c, label, x+132, 468, 28, RED, bold=True, align="center", width=235)
            text(c, "?", x+132, 532, 42, MUTED, align="center")
            if i < 4:
                arrow(c, x+278, 480, x+322, 480, RED)
            circle(c, x+132, 645, 8, RED, .4+.5*math.sin(t*.8-i)**2)
        rows(c, ["An omission is a clue.", "Its location still needs evidence."], 960, 760, 39, INK, p, bold=True, align="center")
        self.note(c, "Diagnostic possibilities, not a finding about a particular product")

    def responsibility(self, c, t, s):
        p = self.reveal(t, s)
        for i, (title, body, col) in enumerate([("01  EXISTS?", ["Does the reference", "identify a real source?"], TEAL),
                                                ("02  FAITHFUL?", ["Does the writing", "represent it accurately?"], BLUE),
                                                ("03  ADEQUATE?", ["Was enough relevant", "evidence available?"], RED)]):
            panel(c, 140+i*570, 330, 500, 365, title, body, col)
        text(c, "License. Configure. Evaluate. Ask.", 960, 810, 43, INK, p, bold=True, align="center")
        self.note(c, "The preface argues for retrieval competence within library work")

    def expertise(self, c, t, s):
        p = self.reveal(t, s)
        panel(c, 180, 345, 650, 360, "YOUR SEARCH EXPERTISE", ["Questions and vocabulary", "Search strategies", "Professional judgement"], TEAL)
        arrow(c, 860, 520, 1050, 520, TEAL, p, stroke=5)
        panel(c, 1090, 345, 650, 360, "THE MACHINERY BELOW", ["Admission and ranking", "Representations and stages", "Evidence and trade-offs"], BLUE, p)
        text(c, "Connect what you know to what the system does.", 960, 820, 36, INK, p, bold=True, align="center", width=1700)
        self.note(c, "Orientation to retrieval, with professional search knowledge as the starting point")

    def audiences(self, c, t, s):
        p = self.reveal(t, s)
        for i, (title, body, col) in enumerate([("INFORMATION LITERACY", ["Turn questions into searches", "Teach interface choices", "Help people interpret results"], TEAL),
                                                ("EVIDENCE SYNTHESIS", ["Build high-recall strategies", "Document and rerun searches", "Connect retrieval to screening"], BLUE),
                                                ("SYSTEMS & DISCOVERY", ["Configure and integrate", "Inspect indexes and vendors", "Evaluate and procure"], RED)]):
            panel(c, 140+i*570, 330, 500, 390, title, body, col)
        text(c, "Different expertise. Shared retrieval questions.", 960, 825, 37, INK, p, bold=True, align="center", width=1700)
        self.note(c, "Information literacy and evidence synthesis are the primary audiences")

    def principles(self, c, t, s):
        p = self.reveal(t, s)
        for i, (n, title, desc, col) in enumerate([("1", "UNDERSTANDING FIRST", "Enough mechanism to reason about behavior", TEAL),
                                                  ("2", "FAMILIAR EXAMPLES", "Dated library and academic search systems", BLUE),
                                                  ("3", "FORMULAS WITH A JOB", "Explanations in words carry the main argument", RED)]):
            y = 310+i*170
            circle(c, 245, y+45, 37, col)
            text(c, n, 245, y+58, 34, PAPER, bold=True, align="center")
            text(c, title, 340, y+28, 34, col, bold=True)
            text(c, desc, 340, y+82, 29, INK, width=1380)
        text(c, "Understand what a method responds to—and what it misses.", 960, 862, 31, TEAL, p, bold=True, align="center", width=1700)
        self.note(c, "The three teaching principles stated in the preface")

    def dates(self, c, t, s):
        p = self.reveal(t, s)
        card(c, 270, 320, "DOCUMENTATION", 540, 430, TEAL, detail=["Named product", "Mechanism described", "Date checked", "Limits acknowledged"])
        panel(c, 1040, 350, 640, 350, "BEFORE RELYING ON IT", ["Check the current account.", "Keep the example's date.", "Mark what remains unknown."], RED)
        arrow(c, 850, 535, 1000, 535, TEAL)
        text(c, "Product illustration ≠ product recommendation", 960, 835, 36, RED, p, bold=True, align="center", width=1700)
        self.note(c, "Product details can change faster than retrieval mechanisms")

    def scope(self, c, t, s):
        p = self.reveal(t, s)
        for i, label in enumerate(["Search", "Select evidence", "Available sources"]):
            x = 160+i*440
            rect(c, x, 390, 360, 180, PAPER)
            text(c, label, x+180, 495, 31, TEAL, bold=True, align="center", width=320)
            if i < 2:
                arrow(c, x+375, 480, x+425, 480, TEAL)
        line(c, 1485, 340, 1485, 640, RED, stroke=3)
        rows(c, ["Answer", "writing"], 1670, 455, 34, MUTED, align="center")
        text(c, "THE BOOK'S MAIN FOCUS", 810, 690, 28, TEAL, bold=True, align="center")
        line(c, 160, 625, 1400, 625, TEAL, stroke=3)
        text(c, "A practical floor for asking better technical questions.", 960, 825, 34, INK, p, bold=True, align="center", width=1700)
        self.note(c, "Answer generation stays outside the book's main scope")

    def routes1(self, c, t, s):
        p = self.reveal(t, s)
        panel(c, 130, 300, 510, 450, "01  SHORT ORIENTATION", ["45-minute route", "Reading and reflection", "Summaries and distinctions", "Closing puzzle map"], TEAL)
        panel(c, 705, 300, 510, 450, "02  INSTRUCTION", ["Protect Part I", "Chapter 11", "Chapters 13–15", "Query, failure, evaluation"], BLUE)
        panel(c, 1280, 300, 510, 450, "03  EVIDENCE SYNTHESIS", ["Chapters 2 and 11", "Chapters 13–15", "Appendix F is CORE", "Retrieval to screening"], RED, .45+.55*p)
        pill(c, "Appendix F is core reading", 700, 805, RED, p)
        self.note(c, "Reading straight through remains the default; routes follow the more-readable branch")

    def routes2(self, c, t, s):
        p = self.reveal(t, s)
        panel(c, 160, 300, 760, 450, "04  PROCUREMENT", ["Category errors and distinctions", "Failure diagnosis and library practice", "Keep Appendix D open", "Combining/reranking: Ch. 10 + App. E"], RED)
        panel(c, 1010, 300, 750, 450, "05  CURIOSITY", ["Already know Boolean and BM25?", "Begin at learnt representations", "Return to mechanisms as needed", "Lexical is broader than Boolean"], TEAL, .45+.55*p)
        text(c, "Choose a purpose. Keep the mechanisms connected.", 960, 837, 34, INK, p, bold=True, align="center", width=1690)
        self.note(c, "The original preface links the full chapter selections for each route")

    def practice(self, c, t, s):
        p = self.reveal(t, s)
        for i, label in enumerate(["PART I", "PART II", "PART III"]):
            x = 200+i*570
            card(c, x, 340, label, 400, 360, [TEAL, BLUE, RED][i], detail=["Read at your pace", "Run an application", "Record what you find"])
        pill(c, "Public-access route in the teaching notes", 620, 800, TEAL, p)
        self.note(c, "Chapter reading times support shorter sessions; exercises are optional")

    def finale(self, c, t, s):
        p = self.reveal(t, s)
        for i, (label, col) in enumerate([("Admission  /  Ranking", BLUE),
                                         ("Existence  /  Faithfulness  /  Adequacy", RED),
                                         ("Documented  /  Observed  /  Unknown", TEAL)]):
            y = 310+i*140
            rect(c, 240, y, 1440, 100, PAPER)
            text(c, label, 960, y+65, 35, col, bold=True, align="center", width=1350)
        text(c, "Now, to the machine itself.", 960, 850, 48, INK, p, bold=True, align="center")
        self.note(c, "Continue with Chapter 1: The retrieval problem")

    def poster(self, c):
        c.clear(skia.Color(*CREAM))
        text(c, "BEFORE CHAPTER 1", 130, 120, 30, self.accent, bold=True)
        line(c, 130, 155, 1790, 155, self.accent, stroke=3)
        titles = {
            1: ["Two decisions", "hiding in", "every search."],
            2: ["The evidence", "you never", "see."],
            3: ["Your route", "through the", "machine."],
        }
        rows(c, titles[self.script["episode_number"]], 130, 360, 100, INK, bold=True, step=125, width=1140)
        for i in range(3):
            card(c, 1390+i*22, 340+i*100, ["?", "A", "P"][i], 290, 340,
                 [self.accent, MUTED, GOLD][i], angle=(i-1)*6)
        text(c, self.script["subtitle"], 130, 850, 36, self.accent, width=1150)
        text(c, "Adapted from Aaron Tay · How Search Decides What You See", 130, 981, 26, MUTED)
        text(c, f"FILM {self.script['episode_number']:02d}", 1790, 981, 28, self.accent, bold=True, align="right")
