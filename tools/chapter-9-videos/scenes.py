"""Original flat-vector animation for Chapter 9, with labelled teaching examples."""
from __future__ import annotations

import math
import skia

from visuals import (Film as BaseFilm, arrow, chip, circle, clamp, flow, font,
                     line, paint, paper, pop, rect, robot, text)

POOL = ("B", "A", "F", "D", "E", "C")
RERANKED = ("A", "D", "E", "B", "C", "F")
RELEVANT = frozenset(("A", "D", "E", "G"))
SIMILARITIES = ((.10, .20, .90, .40), (.20, .30, .50, .80))
ASPECTS = {"A": "Overall advantage", "B": "Overall advantage", "C": "Overall advantage",
           "D": "Disciplinary differences", "E": "Selection-bias methods", "F": "Weakly related topic"}


def validate_examples():
    assert set(POOL) == set(RERANKED) and "G" not in POOL
    assert len(RELEVANT.intersection(POOL)) / len(RELEVANT) == .75
    assert len(RELEVANT.intersection(POOL[:3])) == 1
    assert len(RELEVANT.intersection(RERANKED[:3])) == 3
    assert tuple(row.index(max(row)) for row in SIMILARITIES) == (2, 3)
    assert math.isclose(sum(max(row) for row in SIMILARITIES), 1.70)
    assert len(set(ASPECTS[k] for k in ("A", "B", "C"))) == 1
    assert len(set(ASPECTS[k] for k in ("A", "D", "E"))) == 3
    assert len(set(POOL)) == 6  # Sharing an aspect does not make studies duplicates.


def lines(c, value, x, y, size=32, fill="white", bold=False, width=530):
    rows, current = [], ""
    for word in value.split():
        candidate = (current + " " + word).strip()
        if current and font(size, bold).measureText(candidate) > width:
            rows.append(current)
            current = word
        else:
            current = candidate
    if current:
        rows.append(current)
    for i, row in enumerate(rows):
        text(c, row, x, y+i*size*1.3, size, fill, bold)


def box(c, x, y, title, body, fill="mint", w=500, h=210):
    rect(c, x-w/2, y-h/2, w, h, "panel", 28)
    rect(c, x-w/2, y-h/2, w, 9, fill, 4)
    text(c, title, x, y-h/2+55, 29, fill, True, max_width=w-40)
    lines(c, body, x, y-h/2+108, 33, width=w-55)


def engine(c, x, y, t, fill="yellow", scale=1, label="COMPARE"):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    rect(c, -125, -125, 250, 250, "panel2", 40)
    for i in range(3):
        for j in range(3):
            xx, yy = -70+i*70, -70+j*70
            if i < 2:
                line(c, [(xx, yy), (xx+70, yy)], fill, 4, .4)
            if j < 2:
                line(c, [(xx, yy), (xx, yy+70)], fill, 4, .4)
            circle(c, xx, yy, 13+2*math.sin(t+i+j), fill)
    text(c, label, 0, 175, 29, fill, True)
    c.restore()


def lens(c, x, y, t, scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    circle(c, 0, 0, 84, "mint", .16)
    circle(c, 0, 0, 84, "yellow", 1, 13)
    line(c, [(58, 64), (132, 144)], "yellow", 24)
    line(c, [(-40, -30), (20, -30)], "white", 8, .8)
    line(c, [(-40, -6), (43, -6)], "white", 8, .8)
    line(c, [(-40, 20), (5+22*math.sin(t), 20)], "mint", 8)
    c.restore()


def vectors(c, x, y, fill="mint", count=1, t=0):
    for i in range(count):
        yy = y+i*49
        for j, v in enumerate((.35, .8, .5, .65)):
            rect(c, x+j*36, yy, 29, 35, "panel2", 7)
            rect(c, x+j*36+4, yy+29-23*v, 21, 23*v, fill, 4)
        circle(c, x+164, yy+17, 5, fill, .7+.3*math.sin(t+i)**2)


def item(c, ident, x, y, w=430, h=65, label=None, fill=None):
    fill = fill or ("mint" if ident in RELEVANT else "blue")
    rect(c, x-w/2, y-h/2, w, h, "panel2", 15)
    chip(c, ident, x-w/2+34, y, 48, fill, 25, 42)
    text(c, label or ("Relevant" if ident in RELEVANT else "Other candidate"),
         x-w/2+78, y+10, 28, "white", align="left", max_width=w-95)


def ranklist(c, order, x, y, t, title, swapped=None, progress=0, w=430):
    text(c, title, x, y-59, 31, "white", True)
    if swapped is None:
        for i, ident in enumerate(order):
            item(c, ident, x, y+i*75, w)
    else:
        for i, ident in enumerate(order):
            j = swapped.index(ident)
            yy = y+(i+(j-i)*progress)*75
            item(c, ident, x+math.sin(progress*math.pi)*35*(1 if i%2 else -1), yy, w)


def orbit(c, x, y, t, fill="mint", r=170):
    circle(c, x, y, r, fill, .23, 3)
    for i in range(8):
        a = i*math.tau/8+t*.19
        circle(c, x+r*math.cos(a), y+r*math.sin(a), 7, fill, .8)


class Film(BaseFilm):
    def boolean(self, c, name, t, p):
        if name == "universe":
            circle(c, 483, 515, 185, "blue")
            circle(c, 435, 485, 96, "mint")
            circle(c, 565, 587, 67, "violet")
            for i in range(11):
                a = i*math.tau/11+t*.12
                paper(c, 483+280*math.cos(a), 515+190*math.sin(a), str(i+1), [], t, .22)
            robot(c, 483, 535, t, .68)
            flow(c, 825, 520, 1095, 520, t)
            lens(c, 1390, 483, t, 1.5)
            text(c, "Collection-scale search", 483, 796, 36, "blue", True)
            text(c, "Detailed comparison", 1400, 796, 36, "yellow", True)
        elif name == "two-speeds":
            box(c, 398, 410, "FIRST STAGE", "Search indexed collection", "blue", 570)
            box(c, 1460, 410, "SECOND PASS", "Score supplied candidates", "yellow", 570)
            flow(c, 722, 410, 1130, 410, t)
            text(c, "SHORTLIST", 926, 360, 28, "mint", True)
            for i in range(14):
                paper(c, 183+i*34, 640+(i%2)*46, "", [], t, .14, "blue")
            for i, ident in enumerate(("A", "D", "E")):
                paper(c, 1280+i*180, 655, ident, [], t, .4, "mint")
            text(c, "Broad, fast candidate search", 398, 803, 31, "blue")
            text(c, "More work per candidate", 1460, 803, 31, "yellow")
        elif name == "ceiling":
            rect(c, 650, 275, 1000, 500, "panel", 34)
            text(c, "FIXED CANDIDATE POOL", 1150, 336, 32, "mint", True)
            for i, ident in enumerate(POOL):
                paper(c, 830+(i%3)*315, 477+(i//3)*193, ident, [], t, .39,
                      "mint" if ident in RELEVANT else "blue")
            paper(c, 320, 500, "G", [], t, .72, "coral")
            line(c, [(510, 360), (510, 700)], "coral", 8)
            text(c, "Relevant, excluded", 319, 713, 31, "coral", True)
            text(c, "No ordering can create G", 1150, 815, 35, "yellow", True)
        elif name == "precision":
            q = pop((t-self.spoken_at(name, "Afterwards", 9))/2.8)
            ranklist(c, POOL, 440, 355, t, "Before reranking", w=460)
            ranklist(c, POOL, 1430, 355, t, "After reranking", RERANKED, q, 460)
            for x in (440, 1430):
                line(c, [(x-252, 552), (x+252, 552)], "yellow", 4)
                text(c, "Displayed top 3", x, 802, 27, "yellow")
            text(c, "1 / 3", 830, 427, 42, "blue", True)
            flow(c, 923, 415, 1079, 415, t, "yellow")
            text(c, "3 / 3" if q == 1 else "1 / 3", 1118, 427, 42, "mint", True)
            text(c, "Pool recall", 975, 600, 26, "muted")
            text(c, "3 / 4", 975, 660, 49, "coral", True)
            chip(c, "G stays outside", 975, 742, 300, "coral", 27, 55)
        elif name == "triage":
            names = ("COVERAGE", "RETRIEVAL", "BUDGET", "RERANK", "DISPLAY")
            for i, label in enumerate(names):
                x = 238+i*359
                orbit(c, x, 495, t+i, "coral" if i == int(t/3)%5 else "blue", 111)
                paper(c, x, 493, "?", [], t, .42)
                text(c, label, x, 698, 26, "coral" if i == int(t/3)%5 else "white", True)
                if i < 4:
                    flow(c, x+128, 495, x+229, 495, t, "muted")
            text(c, "Trace the missing paper through the stages", 960, 795, 35, "yellow", True)
        elif name == "text-boundary":
            box(c, 501, 454, "SUPPLIED ABSTRACT", "The study investigated an intervention…", "blue", 650, 260)
            box(c, 1440, 454, "FULL TEXT ONLY", "The detail you need is on page 12", "coral", 650, 260)
            lens(c, 493, 675, t, .66)
            line(c, [(925, 320), (925, 744)], "coral", 7, .8)
            text(c, "Compared", 506, 808, 33, "mint", True)
            text(c, "Unavailable to this scorer", 1440, 808, 33, "coral", True)
        elif name == "budgets":
            for i, (label, number, fill) in enumerate((("COLLECTION", "Many", "blue"),
                    ("RERANKER", "100", "yellow"), ("DISPLAY", "10", "mint"))):
                x = 388+i*575
                rect(c, x-193, 307, 386, 379, "panel", 80)
                text(c, label, x, 374, 29, fill, True)
                text(c, number, x, 516, 94, fill, True)
                paper(c, x, 615, "", [], t, .19, fill)
                if i < 2:
                    flow(c, x+209, 495, x+364, 495, t, fill)
            text(c, "Schematic budgets; every selection can omit evidence", 960, 797, 34, "muted")
        elif name == "questions":
            robot(c, 383, 522, t, 1.22, "mint")
            for i, (title, body) in enumerate((("ROUTE", "What supplied the candidates?"),
                    ("BUDGET", "How many reached the reranker?"), ("EVIDENCE", "What text was compared?"),
                    ("BOUNDARY", "How many survived selection?"))):
                y = 320+i*122
                chip(c, title, 803, y, 260, "mint", 26, 62)
                text(c, body, 994, y+11, 32, align="left", max_width=760)

    def analysis(self, c, name, t, p):
        if name == "need":
            box(c, 960, 349, "QUERY", "Am I being delulu about getting this job?", "yellow", 1450, 170)
            box(c, 501, 584, "STATED POSITIVE", "How to recognise unrealistic expectations during a job search", "mint", 690, 250)
            box(c, 1419, 584, "HARD NEGATIVE FOR THIS NEED", "Ten signs that you performed well in your job interview", "coral", 690, 250)
            text(c, "Different search needs could change these labels", 960, 801, 32, "muted")
        elif name == "bi":
            for i, (label, fill) in enumerate((("QUERY", "yellow"), ("PASSAGE", "blue"))):
                y = 362+i*291
                chip(c, label, 290, y, 275, fill, 33)
                flow(c, 456, y, 654, y, t, fill)
                engine(c, 792, y, t, fill, .55, "ENCODE + POOL")
                flow(c, 878, y, 1103, y, t, fill)
                vectors(c, 1172, y-17, fill)
                flow(c, 1377, y, 1538, 510, t, fill)
            circle(c, 1639, 510, 83, "mint")
            text(c, "SIMILARITY", 1639, 520, 25, "ink", True)
            text(c, "Document vectors can be prepared in advance", 960, 803, 34, "mint", True)
        elif name == "cross":
            box(c, 348, 371, "QUERY", "Unrealistic expectations?", "yellow", 450, 165)
            box(c, 348, 640, "CANDIDATE", "Recognise expectations", "blue", 450, 165)
            for y, fill in ((371, "yellow"), (640, "blue")):
                flow(c, 601, y, 779, 504, t, fill)
            rect(c, 825, 295, 520, 437, "panel2", 40)
            text(c, "ONE JOINT INPUT", 1085, 350, 29, "mint", True)
            xs = (925, 1085, 1245)
            for i, x in enumerate(xs):
                chip(c, ("query", "tokens", "?")[i], x, 427, 139, "yellow", 24, 52)
                chip(c, ("passage", "tokens", "…")[i], x, 602, 139, "blue", 24, 52)
                for xx in xs:
                    line(c, [(x, 457), (xx, 572)], "mint", 3, .2+.35*math.sin(t+i)**2)
            flow(c, 1386, 512, 1494, 512, t)
            circle(c, 1632, 512, 90, "mint")
            text(c, "SCORE", 1632, 525, 33, "ink", True)
            text(c, "Query and candidate interact before scoring", 960, 805, 34, "yellow", True)
        elif name == "distinction":
            box(c, 448, 380, "QUESTION TURNS ON", "Are expectations unrealistic?", "yellow", 650, 210)
            box(c, 1467, 380, "COMPETING PASSAGE", "Did the interview go well?", "coral", 650, 210)
            lens(c, 925, 547, t, 1.15)
            for i, title in enumerate(("TRAINING", "TEXT TRUNCATION", "TASK DEFINITION")):
                chip(c, title, 410+i*550, 748, 425, ("blue", "mint", "coral")[i], 27, 70)
            text(c, "Finer comparison is possible; correctness still needs evaluation", 960, 805, 30, "muted")
        elif name == "cost":
            text(c, "PAIR EVALUATIONS", 640, 305, 29, "yellow", True)
            for i, (label, count, width) in enumerate((("10", 10, 70), ("100", 100, 310), ("1 million", 1000000, 930))):
                y = 395+i*131
                text(c, label+" candidates", 136, y+11, 29, align="left")
                rect(c, 434, y-24, width*pop(t/2), 48, "yellow" if i < 2 else "coral", 15)
                text(c, f"≈ {count:,}", 1460, y+11, 33, "yellow" if i < 2 else "coral", True, align="left")
            text(c, "Schematic bars, not a latency benchmark", 960, 754, 28, "muted")
            text(c, "Batching does not make the pair evaluations disappear", 960, 809, 32, "yellow", True)
        elif name == "late":
            for i, (label, fill) in enumerate((("QUERY", "yellow"), ("DOCUMENT", "blue"))):
                y = 390+i*274
                chip(c, label, 242, y, 290, fill, 31)
                flow(c, 415, y, 533, y, t, fill)
                engine(c, 655, y, t, fill, .48, "ENCODE")
                flow(c, 739, y, 889, y, t, fill)
                vectors(c, 949, y-72, fill, 3, t)
                flow(c, 1160, y, 1339, 510, t, fill)
            rect(c, 1390, 382, 366, 265, "panel2", 36)
            lines(c, "Compare retained token vectors", 1573, 457, 35, "mint", True, 310)
            text(c, "Document token vectors can be prepared in advance", 960, 805, 32, "mint", True)
        elif name == "maxsim":
            columns = ("open", "access", "citation", "advantage")
            xs = (584, 800, 1016, 1232)
            for j, value in enumerate(columns):
                text(c, value, xs[j], 348, 30, "blue", True)
            for i, row in enumerate(SIMILARITIES):
                y = 452+i*134
                text(c, ("citation", "benefit")[i], 250, y+16, 36, "yellow", True)
                for j, value in enumerate(row):
                    winner = j == row.index(max(row))
                    active = t > self.spoken_at(name, "Citation" if i == 0 else "benefit", 5+i*3)
                    fill = "mint" if winner and active else "panel2"
                    rect(c, xs[j]-88, y-48, 176, 96, fill, 21)
                    text(c, f"{value:.2f}", xs[j], y+16, 42, "ink" if fill == "mint" else "white", True)
                flow(c, 1350, y, 1430, y, t)
                text(c, f"{max(row):.2f}", 1530, y+16, 49, "mint", True)
            text(c, "Invented contextual similarities", 835, 697, 30, "muted")
            text(c, "0.90 + 0.80 = 1.70", 960, 779, 52, "mint", True)
            text(c, "A document token can win more than one row", 960, 824, 27, "muted")
        elif name == "choice":
            for i, (title, fill, label) in enumerate((("BI-ENCODER", "blue", "One pooled vector"),
                    ("CROSS-ENCODER", "yellow", "Joint pair encoding"), ("LATE INTERACTION", "mint", "Retained token vectors"))):
                x = 397+i*560
                text(c, title, x, 330, 30, fill, True)
                orbit(c, x, 515, t+i, fill, 132)
                if i == 0:
                    vectors(c, x-77, 494, fill)
                elif i == 1:
                    engine(c, x, 515, t, fill, .61, "")
                else:
                    vectors(c, x-77, 445, fill, 3, t)
                text(c, label, x, 734, 30, fill, True)
            text(c, "Same model family, different evidence and costs", 960, 814, 32, "muted")

    def index(self, c, name, t, p):
        if name == "pointwise":
            for i, ident in enumerate(("A", "B", "C")):
                x = 410+i*550
                paper(c, x, 404, ident, [], t, .42, "blue")
                flow(c, x, 488, x, 533, t, "blue")
                robot(c, x, 606, t+i, .57, "coral")
                text(c, "Independent judgement", x, 774, 28, "coral", True)
            text(c, "Explicit relevance instructions apply to each candidate", 960, 282, 31, "muted")
        elif name == "pairwise":
            xs, ys = (960, 550, 1370), (337, 681, 681)
            for i, ident in enumerate(("A", "B", "C")):
                paper(c, xs[i], ys[i], ident, [], t, .38, "coral")
            arrow(c, 827, 380, 635, 570, "yellow")
            arrow(c, 699, 681, 1230, 681, "yellow")
            arrow(c, 1293, 567, 1086, 379, "yellow")
            chip(c, "A preferred to B", 569, 432, 332, "yellow", 27, 56)
            chip(c, "B preferred to C", 960, 757, 332, "yellow", 27, 56)
            chip(c, "C preferred to A", 1360, 432, 332, "yellow", 27, 56)
            text(c, "Invented preference cycle", 960, 824, 28, "muted")
        elif name == "listwise":
            for i, ident in enumerate(POOL):
                paper(c, 278+i*271, 371, ident, [], t, .25, "blue")
            q = (t*.22)%3
            rect(c, 200+int(q)*270, 297, 840, 165, "yellow", 25, .75, 5)
            text(c, "Limited context window", 960, 525, 32, "yellow", True)
            flow(c, 960, 557, 960, 608, t, "coral")
            for i, ident in enumerate(RERANKED):
                paper(c, 278+i*271, 712, ident, [], t, .25, "mint")
            text(c, "Illustrative output; input order can affect judgements", 960, 814, 29, "muted")
        elif name == "explanation":
            robot(c, 390, 519, t, 1.17, "coral")
            box(c, 1223, 406, "GENERATED RATIONALE", "This paper fits the requested method…", "coral", 970, 230)
            lens(c, 905, 659, t, .75)
            box(c, 1417, 677, "JUDGED QUERY SET", "Check the resulting order", "mint", 600, 165)
            text(c, "Fluency is not evidence of ranking accuracy", 960, 815, 34, "yellow", True)
        elif name == "diversity":
            text(c, "RELEVANCE-ONLY SELECTION", 499, 308, 29, "blue", True)
            text(c, "DIVERSIFIED SELECTION", 1416, 308, 29, "mint", True)
            for i, ident in enumerate(("A", "B", "C")):
                item(c, ident, 499, 409+i*98, 660, 82, ASPECTS[ident], "blue")
            for i, ident in enumerate(("A", "D", "E")):
                item(c, ident, 1416, 409+i*98, 660, 82, ASPECTS[ident], "mint")
            item(c, "F", 960, 738, 680, 67, "Weakly related: omitted from both", "coral")
            text(c, "Schematic selections, not a computed ranking", 960, 816, 28, "muted")
        elif name == "high-recall":
            paper(c, 415, 517, "B", [], t, .8, "blue")
            paper(c, 817, 517, "C", [], t, .8, "blue")
            text(c, "Shared aspect", 614, 312, 34, "blue", True)
            text(c, "Distinct studies", 614, 728, 34, "mint", True)
            box(c, 1445, 413, "EXPLORATION", "Show more aspects", "yellow", 615, 190)
            box(c, 1445, 650, "HIGH-RECALL REVIEW", "Find every relevant study", "mint", 615, 190)
            text(c, "Variety does not establish fairness or balanced evidence", 960, 817, 29, "muted")
        elif name == "pipelines":
            text(c, "PUBLISHED PUBMED BEST MATCH", 960, 305, 31, "blue", True)
            text(c, "DOCUMENTED PRIMO RESEARCH ASSISTANT", 960, 553, 31, "coral", True)
            for y, labels, fill in ((404, ("BM25", "500 → LambdaMART", "Results continue"), "blue"),
                    (651, ("CDI retrieval", "Up to 30 → embeddings", "5 abstracts → LLM"), "coral")):
                for i, label in enumerate(labels):
                    x = 384+i*576
                    chip(c, label, x, y, 467, fill, 31, 95)
                    if i < 2:
                        flow(c, x+254, y, x+318, y, t, fill)
            text(c, "Budgets constrain evidence; models perform different jobs", 960, 813, 31, "yellow", True)
        elif name == "neural":
            for i, (title, body, fill) in enumerate((("DENSE", "Pooled coordinates", "blue"),
                    ("LEARNT SPARSE", "Weighted vocabulary", "yellow"),
                    ("LATE INTERACTION", "Token-level vectors", "mint"),
                    ("NEURAL RERANKING", "Score existing candidates", "coral"))):
                x, y = 510+(i%2)*900, 386+(i//2)*260
                box(c, x, y, title, body, fill, 760, 208)
            text(c, "Inspect the route, budget, evidence, and selection", 960, 815, 35, "white", True)
