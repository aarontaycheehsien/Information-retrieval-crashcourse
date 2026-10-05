"""Original flat-vector motion graphics, drawn directly with Skia.

No borrowed studio characters, logos, artwork, footage, or fonts are bundled.
The helper is an original little index robot; records are paper astronauts.
"""
from __future__ import annotations

from functools import lru_cache
import math
from pathlib import Path

import numpy as np
import skia

W, H = 1920, 1080
RECORDS = {"D1": "Delulu job interview expectations", "D2": "Job interview preparation guide",
           "D3": "Unrealistic job expectations", "D4": "Delulu about my dream job"}
C = {"bg": "#101833", "panel": "#1d2b50", "panel2": "#263761", "ink": "#101833",
     "white": "#f7f3df", "muted": "#a8bbd8", "blue": "#6aa9ff", "mint": "#68e0bb",
     "yellow": "#ffd36a", "coral": "#ff827b", "pink": "#de92ee", "violet": "#756ce5"}


def clamp(x):
    return max(0, min(1, x))


def smooth(x):
    x = clamp(x)
    return x*x*(3-2*x)


def pop(x):
    x = clamp(x)
    return 1-(1-x)**3


def color(name, alpha=1):
    h = C.get(name, name).lstrip("#")
    return skia.Color(int(h[:2], 16), int(h[2:4], 16), int(h[4:], 16), int(255*clamp(alpha)))


def paint(name="white", alpha=1, stroke=0):
    p = skia.Paint(AntiAlias=True, Color=color(name, alpha))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


@lru_cache(maxsize=128)
def font(size, bold=False):
    path = Path("C:/Windows/Fonts") / ("segoeuib.ttf" if bold else "segoeui.ttf")
    f = skia.Font(skia.Typeface.MakeFromFile(str(path)), size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    f.setSubpixel(True)
    return f


def text(c, value, x, y, size=40, fill="white", bold=False, align="center", max_width=None):
    f = font(size, bold)
    width = f.measureText(value)
    if max_width and width > max_width:
        f = font(size*max_width/width, bold)
        width = f.measureText(value)
    if align == "center":
        x -= width/2
    elif align == "right":
        x -= width
    c.drawString(value, x, y, f, paint(fill))


def circle(c, x, y, r, fill="mint", alpha=1, stroke=0):
    c.drawCircle(x, y, max(0, r), paint(fill, alpha, stroke))


def rect(c, x, y, w, h, fill="panel", radius=24, alpha=1, stroke=0):
    c.drawRoundRect(skia.Rect.MakeXYWH(x, y, w, h), radius, radius, paint(fill, alpha, stroke))


def line(c, points, fill="mint", width=6, alpha=1):
    p = skia.Path()
    p.moveTo(*points[0])
    for point in points[1:]:
        p.lineTo(*point)
    c.drawPath(p, paint(fill, alpha, width))


def polygon(c, points, fill="white", alpha=1):
    p = skia.Path()
    p.moveTo(*points[0])
    for pt in points[1:]:
        p.lineTo(*pt)
    p.close()
    c.drawPath(p, paint(fill, alpha))


def arrow(c, x1, y1, x2, y2, fill="mint", width=7):
    line(c, [(x1, y1), (x2, y2)], fill, width)
    a = math.atan2(y2-y1, x2-x1)
    polygon(c, [(x2, y2), (x2-24*math.cos(a-.5), y2-24*math.sin(a-.5)),
                (x2-24*math.cos(a+.5), y2-24*math.sin(a+.5))], fill)


def flow(c, x1, y1, x2, y2, t, fill="mint"):
    arrow(c, x1, y1, x2, y2, fill, 5)
    k = (t*.32) % 1
    circle(c, x1+(x2-x1)*k, y1+(y2-y1)*k, 9, "white")


def chip(c, value, x, y, w=220, fill="blue", size=38, h=78):
    rect(c, x-w/2, y-h/2, w, h, fill, h/2)
    text(c, value, x, y+size*.35, size, "ink", True, max_width=w-25)


def check(c, x, y, yes=True, size=25):
    circle(c, x, y, size+12, "mint" if yes else "coral")
    if yes:
        line(c, [(x-size*.6, y), (x-size*.1, y+size*.48), (x+size*.7, y-size*.55)], "ink", 7)
    else:
        line(c, [(x-size*.45, y-size*.45), (x+size*.45, y+size*.45)], "ink", 7)
        line(c, [(x+size*.45, y-size*.45), (x-size*.45, y+size*.45)], "ink", 7)


def robot(c, x, y, t, scale=1, fill="yellow"):
    c.save()
    c.translate(x, y+math.sin(t*2)*8*scale)
    c.scale(scale, scale)
    # A round index robot with a drawer-shaped body and small orbiting antenna.
    line(c, [(0, -76), (0, -120), (24*math.sin(t), -140)], fill, 10)
    circle(c, 24*math.sin(t), -140, 14, "pink")
    rect(c, -93, -85, 186, 160, fill, 56)
    rect(c, -74, -60, 148, 72, "ink", 30)
    blink = 0.15 if t % 4.7 < .13 else 1
    for xx in (-33, 33):
        rect(c, xx-10, -43, 20, 30*blink, "mint", 9)
    rect(c, -40, 37, 80, 11, "ink", 5)
    for sign in (-1, 1):
        line(c, [(sign*88, 0), (sign*128, -22+math.sin(t*2+sign)*20)], fill, 17)
        circle(c, sign*128, -22+math.sin(t*2+sign)*20, 17, "white")
        line(c, [(sign*42, 74), (sign*55, 113)], fill, 18)
        rect(c, sign*55-25, 101, 50, 23, "white", 10)
    c.restore()


def paper(c, x, y, ident, tags, t, scale=1, fill="white", happy=True):
    c.save()
    c.translate(x, y+math.sin(t*1.6+x*.006)*8)
    c.rotate(math.sin(t+x*.005)*2)
    c.scale(scale, scale)
    # Paper astronaut, with folded corner and a dark little face plate.
    line(c, [(-55, 118), (-70, 160), (-98, 160)], "blue", 15)
    line(c, [(55, 118), (70, 160), (98, 160)], "blue", 15)
    line(c, [(-110, 20), (-145, 40+math.sin(t)*12)], "blue", 13)
    line(c, [(110, 20), (145, 40-math.sin(t)*12)], "blue", 13)
    rect(c, -117, -137, 234, 272, fill, 24)
    polygon(c, [(68, -137), (117, -88), (68, -88)], "blue")
    text(c, ident, -87, -94, 29, "ink", True, "left")
    rect(c, -71, -58, 142, 56, "ink", 24)
    for xx in (-29, 29):
        circle(c, xx, -31, 9, "mint" if happy else "coral")
    for i, tag in enumerate(tags[:3]):
        chip(c, tag, 0, 38+i*40, 188, "yellow" if tag in ("delulu", "job") else "pink", 26, 32)
    c.restore()


def gate(c, x, y, t, open=True, label="AND", scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    fill = "mint" if open else "coral"
    rect(c, -180, -220, 360, 390, "panel2", 150)
    rect(c, -153, -194, 306, 340, fill, 124, stroke=16)
    if not open:
        for k in range(-100, 101, 50):
            line(c, [(k, -155), (k, 120)], "coral", 10)
    else:
        for k in range(6):
            a = t*.7+k*math.pi/3
            circle(c, math.cos(a)*148, -24+math.sin(a)*170, 6, "white")
    rect(c, -188, 167, 376, 42, fill, 14)
    chip(c, label, 0, -214, 180, fill, 36, 68)
    c.restore()


def docbubble(c, ident, x, y, fill="blue", r=42):
    circle(c, x+3, y+6, r, "ink")
    circle(c, x, y, r, fill)
    text(c, ident, x, y+13, 34, "ink", True)


def postings(c, label, ids, x, y, t, fill="mint", selected=()):
    chip(c, label, x, y, 300, fill, 39)
    flow(c, x+170, y, x+280, y, t, fill)
    for i, ident in enumerate(ids):
        xx = x+355+i*125
        if i:
            line(c, [(xx-78, y), (xx-44, y)], "muted", 4)
        docbubble(c, ident, xx, y, "yellow" if ident in selected else fill)


def pipeline(c, labels, y, active, t):
    gap, x0 = 510, 450
    for i, label in enumerate(labels):
        x = x0+i*gap
        rect(c, x-195, y-60, 390, 120, "mint" if i == active else "panel2", 32)
        text(c, label, x, y+15, 38, "ink" if i == active else "white", True, max_width=340)
        if i < len(labels)-1:
            flow(c, x+205, y, x+gap-205, y, t, "yellow")


def caption(c, cues, t):
    for cue in cues:
        if cue["start"] <= t < cue["end"]:
            f = font(42, True)
            width = f.measureText(cue["text"])+80
            rect(c, W/2-width/2, 965, width, 76, "ink", 22, alpha=.92)
            text(c, cue["text"], W/2, 1017, 42, "white", True, max_width=1740)
            return


def surface_pixels(surface):
    return surface.makeImageSnapshot().toarray(colorType=skia.kRGBA_8888_ColorType)


class Film:
    def __init__(self, episode, timeline):
        self.episode, self.timeline = episode, timeline
        self.number = int(episode["id"][:2])
        self.chapter = episode.get("chapter", 2)
        self.accent = episode["accent"]
        rng = np.random.default_rng(22)
        self.stars = rng.uniform([30, 240, 1], [1890, 860, 3], (65, 3))

    def spoken_at(self, scene, word, fallback=1):
        """Local scene time of a narration word, for actual on-screen actions."""
        take = next(t for t in self.timeline["takes"] if t["id"] == scene)
        hits = [w for w in take["words"] if w["text"].lower().strip(".,!?;") == word.lower()]
        return hits[0]["start"] - self.timeline["scenes"][scene][0] if hits else fallback

    def draw(self, c, t):
        c.clear(color("bg"))
        # Flat, slow parallax and orbiting particles keep diagrams in a living world.
        circle(c, -50, 630, 380, "panel", .35)
        circle(c, 1930, 310, 365, "panel", .4)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+7*math.sin(t*.1+i), y+4*math.cos(t*.13+i), r, "muted", .45)
        name = next((s for s, (a, b) in self.timeline["scenes"].items() if a <= t < b), self.episode["scenes"][-1]["id"])
        scene = next(s for s in self.episode["scenes"] if s["id"] == name)
        a, b = self.timeline["scenes"][name]
        u, p = t-a, clamp((t-a)/(b-a))
        text(c, f"CHAPTER {self.chapter}   /   FILM {self.number:02d}", 105, 79, 25, self.accent, True, "left")
        text(c, self.episode["subtitle"], 1815, 79, 25, "muted", False, "right")
        # Headline slides into its fixed layout; no typewriter reflow.
        text(c, scene["title"], 960, 173+(1-pop(u/.7))*35, 65, "white", True, max_width=1700)
        c.save()
        c.translate(0, (1-pop(u/.7))*45)
        if self.number == 1:
            self.boolean(c, name, u, p)
        elif self.number == 2:
            self.analysis(c, name, u, p)
        else:
            self.index(c, name, u, p)
        c.restore()
        # A separate claim band leaves the lower subtitle zone unobstructed.
        rect(c, 230, 849, 1460, 70, "panel", 35)
        text(c, scene["claim"], 960, 898, 34, self.accent, True, max_width=1390)
        text(c, f"Adapted from Chapter {self.chapter} · Aaron Tay", 105, 945, 20, "muted", align="left")
        for i, s in enumerate(self.episode["scenes"]):
            x = 1652+i*22
            circle(c, x, 937, 5, self.accent if s["id"] == name else "panel2")
        # Short color wipe between narrated scenes, preserving readable hold time.
        if b-t < .3 and scene != self.episode["scenes"][-1]:
            q = smooth((.3-(b-t))/.3)
            rect(c, W-W*q, 230, W*q, 590, self.accent, 0)

    def boolean(self, c, name, t, p):
        if name == "universe":
            circle(c, 550, 540, 208, "blue")
            circle(c, 488, 495, 124, "mint")
            circle(c, 647, 625, 85, "violet")
            # Orbit of paper astronauts around the library planet.
            for k in range(7):
                a = k*math.tau/7+t*.12
                paper(c, 550+math.cos(a)*310, 520+math.sin(a)*190, f"{k+1:02d}", [], t, .28)
            robot(c, 548, 514, t, .95)
            gate(c, 1390, 535, t, True, "QUERY", 1.03)
            flow(c, 950, 535, 1140, 535, t)
            text(c, "The collection", 550, 800, 35)
            text(c, "An admission rule", 1390, 800, 35)
        elif name in ("and", "or", "not"):
            expression = {"and": "delulu AND job", "or": "delulu OR unrealistic", "not": "delulu NOT interview"}[name]
            chip(c, expression, 960, 286, 650, self.accent, 46, 87)
            rows = {"and": [("D1", ["delulu", "job"], True), ("D2", ["job", "interview"], False), ("D4", ["delulu", "job"], True)],
                    "or": [("D1", ["delulu", "job"], True), ("D3", ["unrealistic", "job"], True), ("D4", ["delulu", "job"], True)],
                    "not": [("D1", ["delulu", "interview"], False), ("D2", ["job", "interview"], False), ("D4", ["delulu", "job"], True)]}[name]
            for i, (ident, tags, yes) in enumerate(rows):
                x = 440+i*520
                gate(c, x, 570, t+i, yes, name.upper(), .67)
                # A paper approaches the gate, then settles inside its decision.
                travel = pop((t-.35*i)/1.4)
                paper(c, x-125*(1-travel), 534, ident, tags, t, .62)
                if yes:
                    yy = 420+((t*.19+i*.23) % 1)*260
                    line(c, [(x-84, yy), (x+84, yy)], "mint", 3, .5)
                check(c, x+148, 700, yes, 22)
                text(c, "ELIGIBLE" if yes else "EXCLUDED", x, 792, 31, "mint" if yes else "coral", True)
        elif name == "ranking":
            text(c, "1. Boolean admission", 530, 293, 35, "mint", True)
            text(c, "2. Separate ranking", 1400, 293, 35, "yellow", True)
            rect(c, 180, 342, 700, 450, "panel", 45)
            rect(c, 1030, 342, 700, 450, "panel", 45)
            for i, xx in enumerate((350, 545, 740)):
                paper(c, xx, 518, ("D1", "D3", "D4")[i], [], t, .52)
                line(c, [(xx-75, 685), (xx+75, 685)], "mint", 10)
            flow(c, 905, 530, 1000, 530, t, "yellow")
            for i, x in enumerate((1175, 1385, 1595)):
                height = (110, 200, 72)[i]
                rect(c, x-74, 740-height, 148, height, "yellow" if i == 1 else "blue", 10)
                paper(c, x, 638-height, ("D3", "D1", "D4")[i], [], t, .46)
            text(c, "A set, with no graded order", 530, 775, 28, "muted")
            text(c, "Illustrative ordering", 1400, 775, 28, "muted")
        elif name == "expansion":
            chip(c, "OR", 960, 314, 140, "pink", 44)
            terms = ["delulu", "unrealistic", "irrational", "foolish"]
            for i, term in enumerate(terms):
                x = 360+i*400
                fill = "coral" if i == 3 else "mint"
                flow(c, 960, 367, x, 445, t+i, fill)
                chip(c, term, x, 495, 285, fill, 38)
                flow(c, x, 552, x, 606, t, fill)
                paper(c, x, 714, chr(65+i), [term], t, .4, happy=i != 3)
            text(c, "Each alternative changes admission", 960, 807, 35, "muted")
        elif name == "excluded":
            paper(c, 370, 572, "D4", ["delulu", "job"], t, .85)
            text(c, "Potentially useful", 370, 799, 30, "muted")
            gate(c, 890, 551, t, False, "interview", .9)
            arrow(c, 578, 550, 661, 550, "coral")
            check(c, 897, 530, False, 45)
            robot(c, 1492, 552, t, 1.05, "violet")
            text(c, "RANKING", 1492, 782, 36, "yellow", True)
            line(c, [(1100, 550), (1290, 550)], "muted", 5, .2)
        elif name == "recap":
            pipeline(c, ["Analyse terms", "Boolean admission", "Rank candidates"], 373, 1, t)
            robot(c, 440, 642, t, .75)
            gate(c, 960, 638, t, True, "YES / NO", .6)
            for i, x in enumerate((1340, 1485, 1620)):
                paper(c, x, 644+(i-1)*33, ("D1", "D3", "D4")[i], [], t, .38)
            text(c, "Satisfying a query is evidence — judgement is yours.", 960, 804, 34, "muted")

    def analysis(self, c, name, t, p):
        if name == "raw":
            robot(c, 345, 570, t, 1.15)
            rect(c, 650, 360, 1050, 325, "white", 42)
            polygon(c, [(1570, 360), (1700, 490), (1570, 490)], "blue")
            text(c, "Delulu about jobs!", 1145, 535, 76, "ink", True, max_width=880)
            text(c, "A string of text", 1145, 756, 36, "muted")
        elif name in ("tokens", "case", "filter"):
            text(c, "Delulu about jobs!", 960, 329, 54, "white", True)
            flow(c, 960, 368, 960, 432, t, "yellow")
            lowered = name != "tokens" and (name != "case" or t >= self.spoken_at(name, "lowercase", 3))
            labels = ["delulu" if lowered else "Delulu", "about", "jobs", "!"]
            for i, label in enumerate(labels):
                split = pop((t-.1*i)/1.1)
                x = 960+(420+i*360-960)*split
                inactive = name == "filter" and i in (1, 3) and t >= self.spoken_at(name, "removes", 1.8)
                chip(c, label, x, 533, 270, "panel2" if inactive else "yellow", 53, 110)
                if inactive:
                    line(c, [(x-100, 505), (x+100, 565)], "coral", 9)
                    text(c, "REMOVED", x, 659, 25, "coral", True)
                elif name == "case" and i == 0:
                    text(c, "lowercase", x, 659, 30, "mint")
                else:
                    text(c, "token" if name == "tokens" else "kept", x, 659, 30, "muted")
            robot(c, 1590, 760, t, .34)
            text(c, "Illustrative analysis choices", 940, 792, 32, "muted")
        elif name == "stem":
            chip(c, "jobs", 355, 389, 300, "white", 58, 110)
            chip(c, "job", 1550, 389, 300, "mint", 58, 110)
            polygon(c, [(780, 302), (1140, 302), (1070, 449), (1010, 449), (1010, 496), (910, 496), (910, 449), (850, 449)], "yellow")
            text(c, "STEM", 960, 391, 47, "ink", True)
            flow(c, 545, 389, 743, 389, t, "yellow")
            flow(c, 1177, 389, 1360, 389, t, "mint")
            for i, label in enumerate(("studies", "studying", "studied")):
                chip(c, label, 425, 574+i*83, 300, "blue", 36, 62)
                flow(c, 605, 574+i*83, 1010, 656, t+i, "blue")
            chip(c, "studi", 1340, 656, 340, "pink", 64, 108)
            text(c, "A matching key, not necessarily a word", 1340, 790, 29, "muted", max_width=810)
        elif name == "lemma":
            rect(c, 210, 300, 690, 450, "panel", 40)
            rect(c, 1020, 300, 690, 450, "panel", 40)
            text(c, "STEMMING", 555, 359, 32, "pink", True)
            text(c, "LEMMATISATION", 1365, 359, 32, "yellow", True)
            for x in (555, 1365):
                text(c, "studies · studying · studied", x, 445, 33, max_width=615)
                flow(c, x, 473, x, 525, t, "muted")
            chip(c, "studi", 555, 587, 350, "pink", 64, 108)
            chip(c, "study", 1365, 587, 350, "yellow", 64, 108)
            text(c, "Rule-based matching key", 555, 710, 30, "muted")
            text(c, "better → good (adjective)", 1365, 710, 30, "muted")
            text(c, "Illustrative outputs; algorithms and languages differ.", 960, 803, 31, "muted")
        elif name == "compatibility":
            # Show the successful and unsuccessful cases together, not a misleading
            # transition that appears to change one index between searches.
            for yy, good in ((398, True), (664, False)):
                text(c, "DOCUMENT", 300, yy-72, 26, "muted", True)
                chip(c, "jobs", 300, yy, 200, "blue", 42)
                flow(c, 425, yy, 598, yy, t, "blue")
                chip(c, "job" if good else "jobs", 742, yy, 235, "mint" if good else "coral", 43)
                text(c, "stored term", 742, yy+87, 26, "muted")
                chip(c, "job", 1490, yy, 230, "yellow", 43)
                text(c, "QUERY LOOKUP", 1490, yy-72, 26, "muted", True)
                if good:
                    line(c, [(893, yy), (1330, yy)], "mint", 7)
                    circle(c, 900+((t*.28) % 1)*420, yy, 10, "white")
                    check(c, 1110, yy, True, 30)
                else:
                    line(c, [(893, yy), (1330, yy)], "coral", 5, .5)
                    check(c, 1110, yy, False, 30)
            text(c, "Without another mapping", 1110, 781, 28, "muted")
        elif name == "fields":
            for i, (title, value, label, fill) in enumerate((
                ("TITLE", "jobs → job", "May normalise forms", "mint"),
                ("ABSTRACT", "Delulu → delulu", "May normalise case", "yellow"),
                ("IDENTIFIER", "10.1234/Example", "May preserve exact text", "pink"))):
                x = 390+i*570
                rect(c, x-243, 313, 486, 405, "panel", 38)
                chip(c, title, x, 341, 340, fill, 31, 70)
                text(c, value, x, 497, 42, "white", True, max_width=435)
                text(c, label, x, 605, 28, "muted", max_width=430)
                robot(c, x, 746, t+i, .29, fill)
            text(c, "Field-specific examples, not universal rules", 960, 810, 32, "muted")

    def records(self, c, t, compact=False):
        for i, words in enumerate(RECORDS.values()):
            y = 330+i*118
            if compact:
                rect(c, 130, y-49, 685, 93, "panel", 20)
                docbubble(c, f"D{i+1}", 189, y, "yellow", 34)
                text(c, words, 248, y+11, 26, "white", False, "left", max_width=535)
            else:
                rect(c, 470, y-48, 1230, 94, "panel", 22)
                docbubble(c, f"D{i+1}", 541, y, ("mint", "blue", "pink", "yellow")[i], 35)
                text(c, words, 618, y+13, 35, "white", False, "left", max_width=1040)

    def index(self, c, name, t, p):
        if name == "records":
            self.records(c, t)
            robot(c, 274, 528, t, .85, "coral")
            text(c, "Record → words", 1080, 808, 37, "muted")
        elif name == "invert":
            self.records(c, t, compact=True)
            flow(c, 840, 507, 970, 507, t, "coral")
            for i, (term, ids) in enumerate((("delulu", ["D1", "D4"]), ("interview", ["D1", "D2"]), ("job", ["D1", "D2", "D3", "D4"]))):
                y = 366+i*150
                chip(c, term, 1170, y, 265, "coral", 36)
                flow(c, 1322, y, 1395, y, t, "coral")
                for j, ident in enumerate(ids):
                    docbubble(c, ident, 1462+j*93, y, "blue", 36)
            text(c, "Record → words", 480, 804, 35, "muted")
            text(c, "Term → records", 1440, 804, 35, "coral", True)
        elif name == "postings":
            for i, (term, ids) in enumerate((("delulu", ["D1", "D4"]), ("interview", ["D1", "D2"]), ("job", ["D1", "D2", "D3", "D4"]))):
                postings(c, term, ids, 500, 351+i*167, t, ("mint", "pink", "coral")[i])
            robot(c, 1500, 578, t, .72, "yellow")
            text(c, "Ordered by identifier", 1500, 799, 31, "muted")
        elif name == "intersection":
            postings(c, "delulu", ["D1", "D4"], 470, 352, t, "mint", ("D1",))
            postings(c, "interview", ["D1", "D2"], 470, 521, t, "pink", ("D1",))
            line(c, [(825, 395), (825, 477)], "yellow", 8)
            flow(c, 1260, 438, 1442, 438, t, "yellow")
            docbubble(c, "D1", 1550, 438, "yellow", 88)
            text(c, "SHARED", 1550, 590, 31, "yellow", True)
            chip(c, "AND = INTERSECTION", 960, 740, 680, "yellow", 40, 80)
            robot(c, 355, 741, t, .34, "coral")
        elif name == "sets":
            text(c, "delulu OR interview", 540, 307, 38, "mint", True)
            text(c, "delulu NOT interview", 1430, 307, 38, "coral", True)
            rect(c, 190, 355, 705, 401, "panel", 42)
            rect(c, 1065, 355, 705, 401, "panel", 42)
            for i, ident in enumerate(("D1", "D2", "D4")):
                paper(c, 320+i*218, 514, ident, [], t, .56)
            paper(c, 1420, 514, "D4", ["delulu", "job"], t, .64)
            text(c, "UNION", 540, 708, 35, "mint", True)
            text(c, "SET DIFFERENCE", 1420, 708, 35, "coral", True)
        elif name == "speed":
            # Concrete sorted-list intersection with a moving comparison cursor.
            text(c, "Jump straight to a term's list", 960, 301, 39, "coral", True)
            labels = [("term A", ["D1", "D4", "D7", "D9"]), ("term B", ["D1", "D2", "D7", "D8"])]
            for i, (label, ids) in enumerate(labels):
                postings(c, label, ids, 450, 440+i*181, t, ("mint", "pink")[i])
            # Pointer schedule never moves backwards within one comparison pass.
            stage = min(5, int(p*6))
            indices = [(0, 0), (1, 1), (1, 2), (2, 2), (3, 3), (3, 3)][stage]
            for i, index in enumerate(indices):
                x, y = 805+index*125, 440+i*181
                polygon(c, [(x-18, y-91), (x+18, y-91), (x, y-62)], "yellow")
            robot(c, 1550, 518, t, .66, "coral")
            text(c, "Sorted identifiers", 950, 778, 34, "muted")
            text(c, "Pointers move forwards", 1550, 731, 28, "yellow", True, max_width=505)
        elif name == "rich":
            rect(c, 265, 325, 1390, 372, "panel", 44)
            values = [("RECORD", "D1", "mint"), ("FREQUENCY", "2", "yellow"), ("FIELD", "abstract", "pink"), ("POSITIONS", "4, 19", "coral")]
            for i, (label, value, fill) in enumerate(values):
                x = 455+i*335
                text(c, label, x, 401, 25, fill, True)
                chip(c, value, x, 516, 255, fill, 43, 97)
                text(c, ("which record", "how often", "where", "which offsets")[i], x, 625, 27, "muted")
            text(c, "Illustrative posting: formats vary", 960, 762, 29, "muted")
            text(c, "Full-text search does not guarantee complete-article coverage.", 960, 810, 31, "coral", max_width=1710)
        elif name == "finish":
            pipeline(c, ["Analysed terms", "Posting lists", "Eligible set"], 364, 1, t)
            for i, x in enumerate((355, 546)):
                chip(c, ("delulu", "interview")[i], x, 603+i*101, 245, "coral", 34)
            postings(c, "delulu", ["D1", "D4"], 824, 548, t, "mint")
            postings(c, "interview", ["D1", "D2"], 824, 682, t, "pink")
            paper(c, 1577, 620, "D1", [], t, .58)
            text(c, "Next: how should matches be ranked?", 960, 813, 34, "yellow", True)
