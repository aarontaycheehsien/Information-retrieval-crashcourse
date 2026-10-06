"""Original vector characters and animated, source-grounded Chapter 8 diagrams."""
from __future__ import annotations

import math

from visuals import (Film as BaseFilm, arrow, chip, circle, clamp, color, flow,
                     font, line, paint, paper, polygon, pop, rect, robot, smooth, text)

VOCAB = ("attack", "cancer", "heart", "interview", "job", "tips", "treatment")
DOCS = {"D1": "heart attack treatment", "D2": "job interview tips", "D3": "cancer treatment"}
BINARY = {k: tuple(int(term in value.split()) for term in VOCAB) for k, value in DOCS.items()}
QUERY = tuple(int(term in ("heart", "treatment")) for term in VOCAB)
DENSE = (.14, -.37, .81, .05, -.21, .63, -.12, .28)
HITS = (("A", 2), ("A", 7), ("B", 3), ("A", 9))


def validate_examples():
    assert tuple(sorted({t for d in DOCS.values() for t in d.split()})) == VOCAB
    assert BINARY == {"D1": (1, 0, 1, 0, 0, 0, 1), "D2": (0, 0, 0, 1, 1, 1, 0), "D3": (0, 1, 0, 0, 0, 0, 1)}
    scores = {k: sum(a*b for a, b in zip(v, QUERY)) for k, v in BINARY.items()}
    assert scores == {"D1": 2, "D2": 0, "D3": 1}
    assert {k for k, v in BINARY.items() if all(a for a, b in zip(v, QUERY) if b)} == {"D1"}
    assert {k for k, v in scores.items() if v} == {"D1", "D3"}
    assert sum("heart" in d.split() for d in DOCS.values()) == 1
    assert sum("treatment" in d.split() for d in DOCS.values()) == 2
    score = lambda tf: tf*2.2/(tf+1.2)
    assert score(2)-score(1) > score(10)-score(9) > 0
    assert len(HITS) == 4 and len({k for k, _ in HITS}) == 2
    assert len(DENSE) == 8 and DENSE[2] == .81


def wrapped(c, value, x, y, size=31, fill="white", width=460, bold=False):
    rows, current = [], ""
    for word in value.split():
        candidate = (current + " " + word).strip()
        if current and font(size, bold).measureText(candidate) > width:
            rows.append(current)
            current = word
        else:
            current = candidate
    rows.append(current)
    for i, row in enumerate(rows):
        text(c, row, x, y+size*1.32*i, size, fill, bold)


def label(c, value, x, y, fill="mint", size=31):
    text(c, value, x, y, size, fill, True)


def panel(c, x, y, width=440, height=360, fill="panel"):
    rect(c, x-width/2, y-height/2, width, height, fill, 32)


def little_vector(c, x, y, values, t, fill="mint", width=540, numbers=False):
    step = width/len(values)
    for i, v in enumerate(values):
        xx = x-width/2+i*step
        rect(c, xx, y-38, step-8, 76, "panel2", 12)
        if v:
            h = 15+37*min(abs(v), 1)*pop(t/.7)
            rect(c, xx+6, y+28-h, step-20, h, fill if v > 0 else "pink", 6)
        if numbers:
            text(c, f"{v:g}", xx+(step-8)/2, y+84, 29, "white", True)


def neural(c, x, y, t, fill="yellow", scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    panel(c, 0, 0, 260, 235, "panel2")
    for j, count in enumerate((3, 4, 3)):
        for i in range(count):
            xx, yy = -82+j*82, (i-(count-1)/2)*49
            if j < 2:
                for k in range(4 if j == 0 else 3):
                    y2 = (k-((4 if j == 0 else 3)-1)/2)*49
                    line(c, [(xx+12, yy), (xx+70, y2)], "blue", 2, .23)
            circle(c, xx, yy, 12, fill, .5+.5*math.sin(t*1.4+i+j)**2)
    c.restore()


def sheet(c, x, y, title, t, fill="white", scale=1, highlights=()):
    c.save()
    c.translate(x, y+math.sin(t*1.4)*5)
    c.scale(scale, scale)
    rect(c, -145, -205, 290, 410, fill, 24)
    polygon(c, [(95, -205), (145, -155), (95, -155)], "blue")
    text(c, title, 0, -147, 31, "ink", True)
    for i in range(8):
        rect(c, -112, -113+i*37, 212 if i%3 else 160, 14, "coral" if i in highlights else "blue", 7)
    c.restore()


def grouped(c, x, y, title, passages, fill="mint"):
    panel(c, x, y, 410, 285)
    label(c, title, x, y-69, fill, 36)
    wrapped(c, "Matching passages", x, y-16, 27, "muted")
    for i, number in enumerate(passages):
        chip(c, str(number), x+(i-(len(passages)-1)/2)*88, y+55, 68, fill, 30, 63)


class Film(BaseFilm):
    def draw(self, c, t):
        # Own title and credit layout also works with the older shared renderer.
        c.clear(color("bg"))
        circle(c, -60, 620, 370, "panel", .5)
        circle(c, 1920, 380, 350, "panel", .45)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+8*math.sin(t*.1+i), y+5*math.cos(t*.13+i), r, "muted", .45)
        name = next((s for s, (a, b) in self.timeline["scenes"].items() if a <= t < b), self.episode["scenes"][-1]["id"])
        scene = next(s for s in self.episode["scenes"] if s["id"] == name)
        a, b = self.timeline["scenes"][name]
        u, p = t-a, clamp((t-a)/(b-a))
        text(c, f"CHAPTER 8   /   FILM {self.number:02d}", 105, 79, 25, self.accent, True, "left")
        text(c, self.episode["subtitle"], 1815, 79, 25, "muted", align="right")
        text(c, scene["title"], 960, 173+(1-pop(u/.7))*35, 61, "white", True, max_width=1700)
        c.save()
        c.translate(0, (1-pop(u/.7))*38)
        (self.lexical, self.sparse, self.units)[self.number-1](c, name, u, p)
        c.restore()
        rect(c, 160, 849, 1600, 70, "panel", 35)
        text(c, scene["claim"], 960, 895, 32, self.accent, True, max_width=1510)
        text(c, "Adapted from Chapter 8 · Aaron Tay", 105, 945, 20, "muted", align="left")
        for i, s in enumerate(self.episode["scenes"]):
            circle(c, 1652+i*22, 937, 5, self.accent if s["id"] == name else "panel2")
        if b-t < .3 and scene != self.episode["scenes"][-1]:
            q = smooth((.3-(b-t))/.3)
            rect(c, 1920-1920*q, 230, 1920*q, 590, self.accent, 0)

    def lexical(self, c, name, t, p):
        if name == "numbers":
            circle(c, 495, 507, 176, "blue")
            circle(c, 448, 455, 105, "mint")
            robot(c, 495, 516, t, .92)
            for i, term in enumerate(("heart", "job", "cancer")):
                a = t*.18+i*math.tau/3
                chip(c, term, 495+math.cos(a)*275, 505+math.sin(a)*188, 170, "yellow", 30, 58)
            flow(c, 850, 505, 1020, 505, t)
            little_vector(c, 1390, 500, BINARY["D1"], t, numbers=True, width=590)
            label(c, "WORDS HAVE COORDINATES TOO", 1375, 345, "mint", 33)
            wrapped(c, "A numerical object. Its meaning depends on the coordinate system.", 1390, 690, width=680)
        elif name in ("vocabulary", "binary"):
            if name == "vocabulary":
                for i, (ident, value) in enumerate(DOCS.items()):
                    paper(c, 410+i*550, 437, ident, [], t, .48)
                    label(c, value, 410+i*550, 580, ("mint", "yellow", "coral")[i], 32)
                for i, term in enumerate(VOCAB):
                    x = 357+i*201
                    chip(c, term, x, 700, 187, "blue", 28, 65)
                    text(c, str(i+1), x, 786, 28, "muted")
            else:
                for i, term in enumerate(VOCAB):
                    text(c, term, 580+i*174, 322, 29, "blue", True)
                for j, (ident, values) in enumerate(BINARY.items()):
                    y = 408+j*145
                    chip(c, ident, 250, y, 145, ("mint", "yellow", "coral")[j], 35)
                    for i, value in enumerate(values):
                        x = 580+i*174
                        rect(c, x-72, y-47, 144, 95, "mint" if value else "panel2", 18)
                        text(c, str(value), x, y+19, 47, "ink" if value else "muted", True)
                text(c, "Only active term–weight pairs need storage", 960, 800, 33, "mint")
        elif name == "rules":
            chip(c, "heart treatment", 960, 296, 460, "blue", 38)
            for x, title, result, detail, fill in (
                (425, "COUNT OVERLAP", "D1: 2   D3: 1   D2: 0", "A graded score", "mint"),
                (960, "HEART AND TREATMENT", "D1", "Both terms required", "yellow"),
                (1495, "HEART OR TREATMENT", "D1 + D3", "Either term required", "coral")):
                panel(c, x, 548, 485, 350)
                label(c, title, x, 431, fill, 27)
                text(c, result, x, 555, 37, "white", True)
                text(c, detail, x, 641, 28, "muted")
            robot(c, 960, 770, t, .28)
        elif name == "frequency":
            paper(c, 375, 500, "D1", ["heart", "attack"], t, .65)
            for i in range(3):
                chip(c, "treatment", 750, 389+i*116, 242, "mint", 32)
            flow(c, 925, 510, 1060, 510, t)
            reveal = pop((t-self.spoken_at(name, "three", 3))/.8)
            values = (1, 0, 1, 0, 0, 0, 1+2*reveal)
            for i, value in enumerate(values):
                x = 1160+i*85
                rect(c, x-35, 425, 70, 150, "panel2", 12)
                if value:
                    rect(c, x-27, 568-value*43, 54, value*43, "yellow", 7)
                text(c, str(round(value)), x, 625, 34, "white", True)
            text(c, "Same coordinates, different values", 960, 769, 38, "mint", True)
        elif name == "rarity":
            for y, term, count, fill in ((430, "heart", 1, "mint"), (630, "treatment", 2, "yellow")):
                chip(c, term, 360, y, 245, fill, 35)
                for j in range(3):
                    circle(c, 655+j*100, y, 28, fill if j < count else "panel2")
                text(c, f"In {count} of 3 documents", 752, y+79, 28, "muted")
                flow(c, 970, y, 1100, y, t, fill)
                w = math.log(3/count)/math.log(3)*470
                rect(c, 1150, y-34, 470, 68, "panel2", 16)
                rect(c, 1150, y-34, w*pop(t/.8), 68, fill, 16)
                text(c, "Higher IDF" if count == 1 else "Lower IDF", 1390, y+79, 31, fill, True)
            text(c, "Bar proportions illustrate IDF = log(N / DF)", 960, 800, 28, "muted")
        elif name == "bm25":
            label(c, "REPETITION HAS DIMINISHING RETURNS", 720, 303, "mint", 31)
            arrow(c, 310, 707, 1150, 707, "muted", 4)
            arrow(c, 310, 707, 310, 362, "muted", 4)
            pts = [(310+i*80, 707-(i*2.2/(i+1.2))*142) for i in range(101) if i <= 10]
            line(c, pts, "mint", 7)
            tf = 1+(t*.48)%9
            circle(c, 310+tf*80, 707-(tf*2.2/(tf+1.2))*142, 12, "yellow")
            for tf in (1, 5, 10):
                text(c, str(tf), 310+tf*80, 750, 25, "muted")
            text(c, "Term frequency", 730, 796, 29)
            panel(c, 1490, 531, 390, 370)
            robot(c, 1490, 491, t, .55, "yellow")
            wrapped(c, "Length adjusts the term contribution", 1490, 644, 30, "yellow", 350, True)
            text(c, "Toy curve: k1=1.2; average length; IDF omitted", 729, 344, 24, "muted")
        elif name == "recap":
            for i, (title, description, fill) in enumerate((
                ("BINARY", "Is the term present?", "blue"), ("TF", "How often?", "mint"),
                ("TF–IDF", "How distinctive?", "yellow"), ("BM25", "Saturation and length", "coral"))):
                x = 345+i*410
                panel(c, x, 520, 375, 395)
                label(c, title, x, 397, fill, 38)
                little_vector(c, x, 514, BINARY["D1"], t+i, fill, 310)
                wrapped(c, description, x, 642, 29, width=325)
            label(c, "attack · cancer · heart · interview · job · tips · treatment", 960, 794, "mint", 29)

    def sparse(self, c, name, t, p):
        if name == "questions":
            robot(c, 960, 535, t, 1.05, "yellow")
            for i, (title, detail, fill) in enumerate((
                ("NUMERICAL OBJECT", "Is it a vector?", "mint"), ("SHAPE", "Sparse or dense?", "blue"),
                ("PROVENANCE", "Specified or learnt?", "yellow"), ("EVIDENCE", "What do dimensions preserve?", "coral"))):
                x, y = (445 if i%2 == 0 else 1475), (367 if i < 2 else 684)
                panel(c, x, y, 485, 225)
                label(c, title, x, y-33, fill, 28)
                wrapped(c, detail, x, y+33, 32, width=450)
        elif name == "density":
            for x, title, fill in ((515, "SPARSE", "mint"), (1405, "DENSE", "yellow")):
                panel(c, x, 515, 790, 405)
                label(c, title, x, 371, fill, 39)
                for i in range(32):
                    xx, yy = x-317+(i%8)*90, 432+(i//8)*55
                    active = i in (2, 9, 30) if x == 515 else True
                    rect(c, xx, yy, 73, 38, fill if active else "panel2", 8, alpha=.9 if active else 1)
                    if active:
                        circle(c, xx+36, yy+19, 5+3*math.sin(t+i)**2, "ink")
                text(c, "Few active coordinates" if x == 515 else "Mostly active coordinates", x, 764, 33, fill, True)
            text(c, "Illustrations of shape, not measured embeddings", 960, 810, 25, "muted")
        elif name == "latent":
            panel(c, 445, 530, 560, 400)
            label(c, "VOCABULARY COORDINATES", 445, 387, "mint", 27)
            for i, term in enumerate(("open", "access", "citation")):
                chip(c, term, 445, 461+i*88, 240, "mint", 31, 62)
            label(c, "LATENT COORDINATES", 1315, 387, "yellow", 31)
            little_vector(c, 1315, 507, DENSE, t, "yellow", 745, True)
            for i in range(8):
                text(c, str(i+1), 942.5+(i+.5)*745/8-4, 440, 26, "muted")
            wrapped(c, "Coordinate 3 = 0.81 ≠ citation", 1315, 675, 33, "yellow", 760, True)
            text(c, "Toy coordinates; meaning is distributed", 1315, 758, 28, "muted")
        elif name == "metadata":
            sheet(c, 347, 536, "ARTICLE", t, scale=.7)
            flow(c, 505, 537, 675, 537, t)
            for i, (term, value) in enumerate(zip(("year", "pages", "references", "citations"), (2026, 14, 32, 87))):
                x = 830+i*254
                panel(c, x, 528, 222, 295)
                label(c, term, x, 454, "blue", 27)
                text(c, str(value), x, 565, 53, "yellow", True)
                circle(c, x, 629, 8, "mint")
            label(c, "All active. Explicit bibliographic facts.", 1145, 755, "yellow", 35)
        elif name == "learned":
            for x, title, fill in ((510, "BM25", "blue"), (1410, "SPLADE", "yellow")):
                panel(c, x, 523, 725, 440)
                label(c, title, x, 365, fill, 39)
                if x == 510:
                    chip(c, "counts + statistics", x, 478, 465, fill, 31, 85)
                else:
                    neural(c, x, 475, t, fill, .7)
                little_vector(c, x, 640, (1, 0, .6, 0, 0, .4, 0), t, fill, 555)
                text(c, "Specified formula" if x == 510 else "Learnt mapping + sparsity", x, 786, 32, fill, True)
        elif name == "expansion":
            chip(c, "heart attack", 350, 510, 355, "blue", 41, 98)
            flow(c, 558, 510, 720, 510, t, "blue")
            neural(c, 916, 508, t, "yellow")
            flow(c, 1066, 510, 1202, 510, t, "yellow")
            reveal = pop((t-self.spoken_at(name, "myocardial", 5))/.8)
            for i, (term, value, fill) in enumerate((
                ("heart", 1.8, "blue"), ("attack", 1.4, "blue"),
                ("myocardial", .9, "mint"), ("infarction", .7, "mint"))):
                y = 332+i*125
                chip(c, term, 1490, y, 318, fill, 32, 63)
                rect(c, 1300, y+46, 380, 14, "panel2", 7)
                rect(c, 1300, y+46, value/1.8*380*(1 if i < 2 else reveal), 14, fill, 7)
                text(c, f"{value:.1f}", 1740, y+11, 32, fill, True)
            text(c, "SCHEMATIC WHOLE-WORD LABELS AND WEIGHTS", 940, 801, 26, "muted", True)
        elif name == "map":
            arrow(c, 310, 733, 1710, 733, "muted", 5)
            arrow(c, 310, 733, 310, 291, "muted", 5)
            label(c, "SPARSE", 286, 697, "blue", 27)
            label(c, "DENSE", 286, 358, "yellow", 27)
            label(c, "SPECIFIED RULE", 702, 804, "blue", 28)
            label(c, "LEARNT MAPPING", 1375, 804, "yellow", 28)
            line(c, [(1050, 330), (1050, 720)], "panel2", 3)
            line(c, [(400, 500), (1670, 500)], "panel2", 3)
            chip(c, "BM25", 702, 631, 340, "blue", 38, 92)
            chip(c, "SPLADE", 1375, 631, 340, "mint", 38, 92)
            chip(c, "Dense bi-encoder", 1375, 391, 460, "yellow", 34, 92)
            text(c, "Axes are independent", 702, 406, 28, "muted")
        elif name == "comparison":
            for i, (title, detail, fill) in enumerate((
                ("REPRESENTATION", "Supplies evidence", "blue"),
                ("COMPARISON", "Supplies a score", "yellow"),
                ("RETRIEVAL RULE", "Uses the score", "mint"))):
                x = 390+i*570
                panel(c, x, 513, 455, 320)
                label(c, title, x, 424, fill, 29)
                robot(c, x, 512, t+i, .37, fill)
                text(c, detail, x, 627, 31)
                if i < 2:
                    flow(c, x+246, 512, x+319, 512, t, fill)
            chip(c, "Dot product or cosine ≠ a guarantee of semantics", 960, 776, 1120, "yellow", 33, 70)

    def units(self, c, name, t, p):
        if name == "paper":
            sheet(c, 455, 520, "ONE PAPER", t, scale=.95)
            flow(c, 650, 521, 830, 521, t, "coral")
            for i, (title, detail, fill) in enumerate((
                ("ABSTRACT", "One unit", "blue"), ("SECTIONS", "Ten units", "yellow"),
                ("PASSAGES", "Fifty units", "coral"))):
                x = 1030+i*280
                panel(c, x, 500, 246, 330)
                label(c, title, x, 398, fill, 28)
                paper(c, x, 505, str((1, 10, 50)[i]), [], t+i, .32)
                text(c, detail, x, 735, 29, fill)
        elif name == "cut":
            for i, (title, count, fill) in enumerate((("1 ABSTRACT", 1, "blue"), ("10 SECTIONS", 10, "yellow"), ("50 PASSAGES", 50, "coral"))):
                x = 405+i*550
                panel(c, x, 528, 465, 420)
                label(c, title, x, 383, fill, 34)
                if count == 1:
                    sheet(c, x, 540, "ABSTRACT", t, scale=.52)
                else:
                    cols = 2 if count == 10 else 5
                    rows = count//cols
                    w = 155 if count == 10 else 68
                    h = 38 if count == 10 else 20
                    for j in range(count):
                        xx = x-(cols*(w+8)-8)/2+(j%cols)*(w+8)
                        yy = 443+(j//cols)*(h+8)
                        rect(c, xx, yy, w, h, fill, 6, alpha=.6+.3*math.sin(t*.5+j)**2)
                text(c, "Same twenty-page source article", x, 801, 27, "muted")
        elif name == "vectors":
            label(c, "50 PASSAGES", 455, 332, "coral", 35)
            label(c, "50 POOLED VECTORS", 1400, 332, "yellow", 35)
            for j in range(5):
                y = 410+j*73
                chip(c, f"Passage {j+1}", 455, y, 335, "coral", 29, 55)
                flow(c, 659, y, 880, y, t+j, "coral")
                little_vector(c, 1400, y, (.14, -.37, .81, .05, -.21, .63), t+j, "yellow", 675)
            text(c, "…", 455, 810, 32)
            text(c, "… independently searchable", 1400, 810, 31, "yellow")
        elif name == "boundary":
            for x, title in ((530, "FIXED WINDOWS"), (1390, "OVERLAPPING WINDOWS")):
                panel(c, x, 528, 700, 440)
                label(c, title, x, 373, "coral" if x == 530 else "mint", 31)
                for j in range(3):
                    y = 432+j*95
                    rect(c, x-271, y, 542, 70, ("blue", "yellow", "coral")[j], 15, alpha=.83)
                    text(c, ("Finding", "Qualification", "Population")[j], x, y+44, 31, "ink", True)
                if x == 1390:
                    rect(c, x-292, 458, 584, 131, "mint", 20, stroke=5)
                    rect(c, x-281, 553, 562, 131, "mint", 20, stroke=5)
                else:
                    line(c, [(x-292, 514), (x+292, 514)], "white", 4)
                    circle(c, x-292, 514, 12, "coral")
            text(c, "What is represented together?", 960, 806, 33, "coral", True)
        elif name == "group":
            for j, (source, passage) in enumerate(HITS):
                y = 334+j*119
                fill = "coral" if source == "A" else "blue"
                chip(c, f"{source} · passage {passage}", 420, y, 375, fill, 32, 75)
                target_y = 410 if source == "A" else 680
                line(c, [(638, y), (840, y), (995, target_y)], fill, 4, .55)
                k = (t*.24+j*.18)%1
                circle(c, 638+(995-638)*k, y+(target_y-y)*k, 7, fill)
            grouped(c, 1300, 410, "PAPER A", (2, 7, 9), "coral")
            grouped(c, 1300, 706, "PAPER B", (3,), "blue")
        elif name == "indexed":
            sheet(c, 444, 528, "FULL ARTICLE", t, scale=.87, highlights=(5,))
            label(c, "Results-only finding", 444, 795, "coral", 31)
            flow(c, 635, 448, 905, 448, t, "blue")
            panel(c, 1260, 448, 605, 220)
            label(c, "ABSTRACT INDEX", 1260, 405, "blue", 33)
            text(c, "Finding absent from indexed text", 1260, 493, 29, "muted")
            line(c, [(660, 671), (898, 671)], "coral", 5)
            line(c, [(806, 650), (846, 690)], "coral", 6)
            line(c, [(806, 690), (846, 650)], "coral", 6)
            panel(c, 1260, 686, 605, 164)
            label(c, "No direct match at this stage", 1260, 696, "coral", 32)
        elif name == "context":
            for i, (title, detail, fill) in enumerate((
                ("INDEXED", "Searchable text", "blue"), ("RETRIEVED", "A matching unit", "coral"),
                ("LATER FETCH", "Parent or neighbours", "yellow"), ("CONTEXT", "Text for the answer", "mint"))):
                x = 338+i*413
                panel(c, x, 512, 350, 385)
                label(c, title, x, 388, fill, 30)
                sheet(c, x, 505, str(i+1), t+i, fill, .37)
                wrapped(c, detail, x, 664, 28, width=315)
                if i < 3:
                    flow(c, x+185, 509, x+224, 509, t, fill)
            label(c, "Later context can contain more than the indexed unit", 960, 810, "mint", 31)
        elif name == "audit":
            for i, (title, detail, fill) in enumerate((
                ("SOURCE TEXT", "What text was indexed?", "blue"), ("UNIT SIZE", "How finely was it cut?", "coral"),
                ("REPRESENTATION", "What does each vector preserve?", "yellow"), ("RESULT + CONTEXT", "How grouped or expanded?", "mint"))):
                x, y = (470 if i%2 == 0 else 1450), (393 if i < 2 else 680)
                panel(c, x, y, 700, 230)
                label(c, title, x, y-45, fill, 33)
                wrapped(c, detail, x, y+35, 33, width=660)
            robot(c, 960, 537, t, .67, "coral")
