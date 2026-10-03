"""Original animated diagrams for Chapter 6; toy coordinates are labelled."""
from __future__ import annotations

import math
import skia

from visuals import (Film as BaseFilm, arrow, chip, circle, clamp, color, flow,
                     font, line, paint, paper, pop, rect, robot, text)

TOKEN_VECTORS = ((.2, .6, .8, .1), (.8, .3, .4, .5), (.8, .3, .3, .3))
POOLED = tuple(sum(row[j] for row in TOKEN_VECTORS)/3 for j in range(4))
ANGLES = {"P": (82, 22), "H": (28, 68), "E": (145, 150)}


def validate_examples():
    assert all(math.isclose(a, b) for a, b in zip(POOLED, (.6, .4, .5, .3)))
    before = {k: math.cos(math.radians(v[0])) for k, v in ANGLES.items()}
    after = {k: math.cos(math.radians(v[1])) for k, v in ANGLES.items()}
    assert before["H"] > before["P"] > before["E"]
    assert after["P"] > after["H"] > after["E"]
    assert all(-1 <= s <= 1 for s in (*before.values(), *after.values()))


def lines(c, value, x, y, size=32, fill="white", bold=False, width=540):
    """Word-wrap at measured glyph widths; fixed lines do not reflow in motion."""
    output, current = [], ""
    for word in value.split():
        candidate = (current + " " + word).strip()
        if current and font(size, bold).measureText(candidate) > width:
            output.append(current)
            current = word
        else:
            current = candidate
    if current:
        output.append(current)
    for i, row in enumerate(output):
        text(c, row, x, y+i*size*1.3, size, fill, bold)


def vector(c, x, y, values, fill="mint", size=72, numbers=False):
    for i, value in enumerate(values):
        xx = x+i*(size+9)
        rect(c, xx, y, size, size, "panel2", 12)
        rect(c, xx+6, y+size-6-(size-12)*value, size-12, (size-12)*value, fill, 7)
        if numbers:
            text(c, f"{value:.1f}", xx+size/2, y+size+33, 26, fill, True)


def machine(c, x, y, t, fill="mint", scale=1, label="ENCODER"):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    rect(c, -154, -122, 308, 252, "panel2", 38)
    rect(c, -126, -101, 252, 188, "ink", 26)
    for i, xx in enumerate((-83, 0, 83)):
        for j, yy in enumerate((-65, 0, 65)):
            circle(c, xx, yy, 16, fill, .6+.3*math.sin(t*1.4+i+j)**2)
            if i < 2:
                line(c, [(xx+19, yy), (xx+64, yy)], fill, 3, .45)
            if j < 2:
                line(c, [(xx, yy+19), (xx, yy+46)], "blue", 3, .45)
    for i in range(5):
        circle(c, -84+42*i, 109, 5, fill if (int(t*2)+i)%5 else "white")
    text(c, label, 0, 179, 30, fill, True)
    c.restore()


def passage(c, x, y, title, fill="mint", label="PASSAGE", width=490):
    rect(c, x-width/2, y-110, width, 224, "panel", 30)
    rect(c, x-width/2, y-110, 12, 224, fill, 5)
    text(c, label, x, y-65, 23, fill, True)
    lines(c, title, x, y-10, 32, width=width-55)


def orbit(c, x, y, radius, t, fill="mint", count=8):
    circle(c, x, y, radius, fill, .16, 3)
    for i in range(count):
        a = i*math.tau/count+t*.22
        circle(c, x+math.cos(a)*radius, y+math.sin(a)*radius, 6, fill, .55)


class Film(BaseFilm):
    def boolean(self, c, name, t, p):
        self.factory(c, name, t, p)

    def analysis(self, c, name, t, p):
        self.training(c, name, t, p)

    def index(self, c, name, t, p):
        self.relevance(c, name, t, p)

    def factory(self, c, name, t, p):
        if name == "factory":
            orbit(c, 956, 495, 227, t)
            robot(c, 955, 508, t, 1.02, "mint")
            passage(c, 340, 520, "Am I being delulu about getting this job?", "blue", "QUESTION", 490)
            flow(c, 608, 507, 716, 507, t)
            flow(c, 1200, 507, 1320, 507, t, "yellow")
            vector(c, 1380, 461, (.6, .3, .8, .5), "yellow", 64)
            text(c, "One stored representation", 1517, 661, 31, "yellow", True)
            text(c, "Inside the factory", 960, 785, 35, "mint", True)
        elif name == "two-tokens":
            rect(c, 205, 278, 680, 499, "panel", 34)
            rect(c, 1035, 278, 680, 499, "panel", 34)
            text(c, "LEXICAL INDEX", 545, 335, 30, "blue", True)
            text(c, "MODEL INPUT", 1375, 335, 30, "mint", True)
            chip(c, "job", 380, 453, 190, "blue")
            flow(c, 491, 453, 571, 453, t, "blue")
            for i in range(3):
                chip(c, f"D{i+1}", 700, 397+i*79, 155, "blue", 30, 62)
            text(c, "Posting list", 545, 690, 33, "blue", True)
            for i, value in enumerate(("del", "ulu", "job")):
                chip(c, value, 1200+i*174, 424, 145, "mint", 31, 62)
                flow(c, 1200+i*174, 465, 1375, 528, t+i*.3)
            machine(c, 1375, 591, t, "mint", .46)
            text(c, "Into the encoder", 1375, 729, 31, "mint", True)
        elif name == "pieces":
            chip(c, "delulu", 525, 490, 420, "blue", 69, 133)
            flow(c, 784, 490, 974, 490, t)
            split = self.spoken_at(name, "pieces", 3)
            q = pop((t-split)/1.1)
            for i, part in enumerate(("del", "ulu")):
                chip(c, part, 1208+i*(40+240*q), 490, 238, "mint", 62, 119)
            text(c, "Possible input pieces", 1335, 664, 37, "mint", True)
            text(c, "Coverage does not prove understanding", 960, 789, 38, "yellow", True)
        elif name == "ids":
            for i, (part, ident, values) in enumerate(zip(("del", "ulu", "job"), (17, 42, 9), TOKEN_VECTORS)):
                yy = 347+i*159
                chip(c, part, 352, yy, 230, "blue", 40)
                flow(c, 495, yy, 626, yy, t, "blue")
                chip(c, str(ident), 793, yy, 205, "yellow", 40)
                flow(c, 937, yy, 1065, yy, t, "yellow")
                vector(c, 1175, yy-36, values, "mint", 68)
            for x, title in ((352, "Pieces"), (793, "Toy token IDs"), (1330, "Initial vectors")):
                text(c, title, x, 790, 35, "muted", True)
        elif name == "context":
            terms = ("getting", "this", "job", "unrealistic", "expectations")
            xs = (330, 635, 960, 1285, 1590)
            for i, x in enumerate(xs):
                for j in range(i+1, len(xs)):
                    c.drawArc(skia.Rect.MakeLTRB(x, 306+(j-i)*21, xs[j], 703), 180, 180, False,
                              paint("mint", .15+.2*math.sin(t*.7+i+j)**2, 3))
                chip(c, terms[i], x, 578, 290, "mint" if i == 2 else "blue", 30)
                vector(c, x-100, 656, (.3, .6, .4, .8), "mint" if i == 2 else "blue", 43)
            text(c, "Information from surrounding tokens", 960, 327, 37, "mint", True)
        elif name == "pooling":
            for i, values in enumerate(TOKEN_VECTORS):
                vector(c, 280, 310+i*154, values, ("mint", "blue", "pink")[i], 66, True)
                flow(c, 667, 345+i*154, 943, 498, t+i, "muted")
            circle(c, 1025, 498, 95, "yellow")
            text(c, "MEAN", 1025, 511, 33, "ink", True)
            flow(c, 1128, 498, 1253, 498, t, "yellow")
            vector(c, 1321, 462, POOLED, "yellow", 71, True)
            text(c, "Toy contextual vectors", 440, 788, 32, "muted")
            text(c, "One pooled vector", 1477, 667, 34, "yellow", True)
        elif name == "separate":
            for row, (kind, fill) in enumerate((("QUERY", "blue"), ("PASSAGE", "mint"))):
                yy = 372+row*296
                chip(c, kind, 351, yy, 282, fill, 35)
                flow(c, 522, yy, 681, yy, t, fill)
                machine(c, 838, yy, t, fill, .6)
                flow(c, 956, yy, 1071, yy, t, fill)
                vector(c, 1118, yy-26, (.6, .4, .5, .3), fill, 52)
                flow(c, 1383, yy, 1514, 523, t, fill)
            circle(c, 1608, 523, 93, "yellow")
            text(c, "COMPARE", 1608, 535, 25, "ink", True)
            text(c, "Passages can be encoded in advance", 960, 812, 31, "muted")
        elif name == "handoff":
            for i, (label, sub, fill) in enumerate((("LANGUAGE", "Pretraining", "blue"), ("RETRIEVAL", "Task training", "yellow"), ("COLLECTION", "Indexing", "mint"))):
                x = 405+i*555
                orbit(c, x, 495, 148, t+i, fill, 6)
                robot(c, x, 483, t, .69, fill)
                text(c, label, x, 704, 34, fill, True)
                text(c, sub, x, 754, 29, "muted")
                if i < 2:
                    flow(c, x+188, 490, x+362, 490, t, fill)

    def training(self, c, name, t, p):
        if name == "nearby":
            passage(c, 460, 438, "Predict missing language", "blue", "PRETRAINING", 550)
            passage(c, 1460, 438, "Rank useful passages", "yellow", "RETRIEVAL", 550)
            for i in range(6):
                x = 295+i*70
                circle(c, x, 663+38*math.sin(i+t*.2), 16, "blue")
                xx = 1300+i*63
                circle(c, xx, 656+(i%2)*44, 16, "mint" if i%2 == 0 else "coral")
            robot(c, 960, 537, t, .7, "yellow")
            text(c, "Different tasks teach different comparisons", 960, 790, 35, "yellow", True)
        elif name == "need":
            passage(c, 960, 376, "Am I being delulu about getting this job?", "blue", "QUERY", 1200)
            flow(c, 960, 504, 960, 580, t)
            rect(c, 365, 610, 1190, 145, "yellow", 35)
            lines(c, "Help me judge whether my expectations are unrealistic", 960, 668, 40, "ink", True, 1070)
        elif name in ("positive", "easy", "hard"):
            which = {"positive": ("P", "How to recognise unrealistic expectations during a job search", "mint", "LABELLED POSITIVE"),
                     "easy": ("E", "A history of agricultural employment", "blue", "EASY NEGATIVE"),
                     "hard": ("H", "Ten signs that you performed well in your job interview", "coral", "HARD NEGATIVE")}[name]
            ident, title, fill, label = which
            passage(c, 523, 508, "Am I being delulu about getting this job?", "yellow", "QUERY", 610)
            passage(c, 1415, 508, title, fill, label, 660)
            flow(c, 858, 505, 1065, 505, t, fill)
            paper(c, 1417, 727, ident, [], t, .25, fill)
            text(c, "Stipulated need: unrealistic expectations", 960, 299, 34, "muted")
            if name == "hard":
                text(c, "A different need could make this useful", 960, 800, 33, "yellow", True)
        elif name == "training":
            reveal = self.spoken_at(name, "updates", 2)
            q = pop(clamp((t-reveal)/8))
            x0, y0, r = 690, 510, 218
            circle(c, x0, y0, r, "muted", .26, 2)
            line(c, [(x0-r-20, y0), (x0+r+20, y0)], "muted", 2, .35)
            line(c, [(x0, y0-r-20), (x0, y0+r+20)], "muted", 2, .35)
            circle(c, x0+r, y0, 25, "yellow")
            text(c, "Q", x0+r+50, y0+13, 31, "yellow", True)
            for i, (ident, (start, end)) in enumerate(ANGLES.items()):
                theta = math.radians(start+(end-start)*q)
                x, y = x0+r*math.cos(theta), y0-r*math.sin(theta)
                fill = {"P": "mint", "H": "coral", "E": "blue"}[ident]
                line(c, [(x0, y0), (x, y)], fill, 3, .35)
                circle(c, x, y, 24, fill)
                text(c, ident, x, y+10, 25, "ink", True)
                yy = 364+i*137
                rect(c, 1116, yy-48, 563, 99, "panel", 25)
                text(c, {"P": "Positive", "H": "Hard negative", "E": "Easy negative"}[ident], 1147, yy+10, 32, fill, True, "left")
                text(c, f"{math.cos(theta):+.2f}", 1639, yy+12, 39, fill, True, "right")
            text(c, "Toy unit-circle projection", 690, 790, 30, "muted")
            text(c, "Cosine similarity", 1390, 745, 31, "muted")
        elif name == "examples":
            for i, (title, fill, sub) in enumerate((("SENTENCE-BERT", "mint", "Independent sentence comparison"), ("DPR", "yellow", "Question–passage retrieval"))):
                x = 540+i*850
                orbit(c, x, 478, 164, t, fill)
                machine(c, x, 471, t, fill, .76)
                text(c, title, x, 710, 40, fill, True)
                lines(c, sub, x, 767, 30, "muted", width=660)
        elif name == "limits":
            rect(c, 315, 300, 1290, 390, "panel", 45)
            text(c, "SIMILARITY", 660, 386, 31, "muted", True)
            text(c, "+0.93", 660, 548, 110, "yellow", True)
            robot(c, 1300, 483, t, .69, "mint")
            text(c, "A learned comparison", 960, 750, 44, "mint", True)
            text(c, "Task labels and local judgement still matter", 960, 803, 32, "muted")

    def relevance(self, c, name, t, p):
        if name == "signals":
            labels = ("Judgements", "Clicks", "Answer pairs", "Citations", "Generated queries")
            fills = ("mint", "coral", "yellow", "blue", "pink")
            for i, (label, fill) in enumerate(zip(labels, fills)):
                a = math.radians(190+i*36)
                x, y = 960+math.cos(a)*575, 590+math.sin(a)*300
                chip(c, label, x, y, 310, fill, 30)
                flow(c, x, y+47, 960, 634, t+i, fill)
            robot(c, 960, 676, t, .63, "coral")
            text(c, "What should count as useful?", 960, 802, 36, "coral", True)
        elif name == "clicks":
            for i, (label, width) in enumerate((("FIRST: highly visible", 645), ("SECOND: another option", 330), ("THIRD: relevant?", 180))):
                yy = 362+i*129
                rect(c, 276, yy-48, 950, 101, "panel", 24)
                text(c, label, 308, yy+10, 34, "white", i == 0, "left")
                rect(c, 278, yy+43, width*(.7+.3*pop(t/2)), 9, "coral" if i == 0 else "blue", 4)
            robot(c, 1530, 519, t, .8, "coral")
            text(c, "Position can affect clicks", 960, 800, 37, "coral", True)
        elif name == "answers":
            for i, (first, second, fill) in enumerate((("QUESTION", "ANSWER", "yellow"), ("TITLE", "ABSTRACT", "blue"))):
                yy = 407+i*246
                chip(c, first, 417, yy, 360, fill, 37)
                flow(c, 643, yy, 1198, yy, t, fill)
                chip(c, second, 1460, yy, 410, fill, 37)
                text(c, "Answer-bearing" if i == 0 else "Topically similar", 960, yy+83, 31, "muted")
        elif name == "citations":
            positions = ((455, 423), (832, 346), (1135, 493), (1453, 340), (1560, 663), (918, 723), (446, 691))
            for a, b in ((0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 0), (2, 5), (0, 2)):
                flow(c, *positions[a], *positions[b], t+a, "blue")
            for i, (x, y) in enumerate(positions):
                circle(c, x, y, 49, "panel")
                paper(c, x, y, str(i+1), [], t, .28, "blue")
            text(c, "Citation-linked scholarly relatedness", 960, 800, 35, "blue", True)
        elif name == "domain":
            for i, (label, fill) in enumerate((("WEB QUESTIONS", "yellow"), ("CHEMISTRY", "mint"), ("EVIDENCE REVIEW", "coral"))):
                x = 420+i*540
                circle(c, x, 477, 144, fill, .2)
                robot(c, x, 464, t+i, .72, fill)
                text(c, label, x, 693, 32, fill, True)
            text(c, "Test the fit to your collection and task", 960, 799, 38, "white", True)
        elif name == "detail":
            passage(c, 522, 480, "CMP-104", "mint", "INVENTED IDENTIFIER", 510)
            passage(c, 1398, 480, "CMP-140", "coral", "INVENTED IDENTIFIER", 510)
            circle(c, 960, 479, 93, "yellow")
            text(c, "≠", 960, 500, 78, "ink", True)
            text(c, "Similar strings can refer to different things", 960, 736, 39, "yellow", True)
            text(c, "The example is illustrative; no model scores are measured", 960, 795, 29, "muted")
        elif name == "diagnose":
            items = (("1", "Collection coverage"), ("2", "Searchable fields"), ("3", "Query processing"), ("4", "Candidate cut-offs"))
            for i, (num, title) in enumerate(items):
                x, y = 550+(i%2)*830, 402+(i//2)*207
                rect(c, x-335, y-61, 670, 130, "panel", 30)
                circle(c, x-262, y, 34, "coral")
                text(c, num, x-262, y+13, 34, "ink", True)
                text(c, title, x+23, y+12, 33, "white", True)
            text(c, "Then compare local judged queries", 960, 797, 37, "mint", True)
        elif name == "questions":
            questions = ("What does each vector represent?", "Which training signals taught similarity?", "Does it retrieve what our task needs?")
            for i, value in enumerate(questions):
                y = 355+i*150
                circle(c, 309, y, 36, ("mint", "yellow", "coral")[i])
                text(c, str(i+1), 309, y+13, 35, "ink", True)
                text(c, value, 389, y+14, 42, "white", True, "left", 1360)
            text(c, "Read Chapter 6 · Then explore collection-scale retrieval", 960, 797, 31, "muted")
