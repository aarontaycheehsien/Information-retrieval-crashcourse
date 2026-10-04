"""Original geometric motion graphics and calculated Chapter 10 examples."""
from __future__ import annotations

import math
import numpy as np

from visuals import (arrow, chip, circle, clamp, color, flow, font, line,
                     paper, polygon, pop, rect, robot, smooth, text)

LEXICAL, DENSE = ("A", "B", "C"), ("C", "A", "D")
FILLS = {"A": "mint", "B": "yellow", "C": "blue", "D": "pink", "E": "coral"}


def rrf(lists, constant=60, weights=None):
    """Fuse distinct identities; absent records have no contribution."""
    assert constant >= 0
    weights = [1] * len(lists) if weights is None else weights
    assert len(weights) == len(lists) and all(w >= 0 for w in weights)
    result = {}
    for ranking, weight in zip(lists, weights):
        assert len(ranking) == len(set(ranking)), "Deduplicate each supplied ranking"
        for rank, record in enumerate(ranking, 1):
            result[record] = result.get(record, 0) + weight / (constant + rank)
    return result


def order(scores):
    return sorted(scores, key=lambda d: (-scores[d], d))


def validate_examples():
    scores = rrf((LEXICAL, DENSE))
    assert order(scores) == ["A", "C", "B", "D"]
    assert [f"{scores[d]:.5f}" for d in order(scores)] == ["0.03252", "0.03227", "0.01613", "0.01587"]
    assert math.isclose(scores["A"], 1/61 + 1/62)
    assert math.isclose(scores["C"], 1/63 + 1/61)
    assert len(scores) == 4 and set(order(scores)[:2]) == {"A", "C"}
    assert "E" not in rrf((LEXICAL, DENSE))
    assert order(rrf((LEXICAL, DENSE), weights=(1, 2))) == ["C", "A", "D", "B"]
    assert 1/2 / (1/4) > 1/61 / (1/63)
    assert set(rrf((LEXICAL[:1], DENSE[:1]))) == {"A", "C"}


def wrapped(c, value, x, y, size=31, fill="white", width=480, bold=False):
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


def orbit(c, x, y, r, t, fill="mint", count=8):
    circle(c, x, y, r, fill, .16, 3)
    for i in range(count):
        a = t*.2 + i*math.tau/count
        circle(c, x+math.cos(a)*r, y+math.sin(a)*r, 6, fill, .65)


def card(c, d, x, y, t, scale=1, label=None):
    """Compact record with stable identity across all result lists."""
    c.save()
    c.translate(x, y+math.sin(t*1.7+ord(d[0]))*3)
    c.scale(scale, scale)
    rect(c, -75, -44, 150, 88, FILLS.get(d, "mint"), 18)
    polygon(c, [(48, -44), (75, -17), (48, -17)], "white", .6)
    text(c, d, 0, 18, 49, "ink", True)
    if label:
        text(c, label, 0, 80, 23, "muted")
    c.restore()


def ranked_list(c, x, y, records, title, t, width=390, fill="blue", cutoff=None):
    rect(c, x-width/2, y-70, width, 115+len(records)*95, "panel", 28)
    text(c, title, x, y-22, 27, fill, True)
    for i, d in enumerate(records):
        yy = y+46+i*95
        if cutoff is not None and i >= cutoff:
            c.saveLayerAlpha(None, 55)
        text(c, f"#{i+1}", x-125, yy+12, 27, "muted", True)
        card(c, d, x+30, yy, t, .79)
        if cutoff is not None and i >= cutoff:
            c.restore()
    if cutoff is not None:
        yy = y+cutoff*95-3
        line(c, [(x-width/2-12, yy), (x+width/2+12, yy)], "coral", 5)


def box(c, x, y, title, sub="", fill="mint", width=370, height=150):
    rect(c, x-width/2, y-height/2, width, height, "panel2", 28)
    text(c, title, x, y-5 if sub else y+13, 32, fill, True, max_width=width-25)
    if sub:
        wrapped(c, sub, x, y+37, 24, "muted", width-30)


def scout(c, x, y, t, kind, scale=1):
    fill = "blue" if kind == "LEXICAL" else "mint"
    orbit(c, x, y, 139*scale, t, fill, 6)
    robot(c, x, y, t, scale*.77, fill)
    if kind == "LEXICAL":
        circle(c, x+100*scale, y-75*scale, 36*scale, "yellow", .9, 9*scale)
        line(c, [(x+125*scale, y-50*scale), (x+156*scale, y-18*scale)], "yellow", 12*scale)
    else:
        for i in range(3):
            circle(c, x+110*scale, y-65*scale, (19+15*i)*scale, "pink", .8-i*.2, 4*scale)


def mini_pipeline(c, y, labels, t, fills=None):
    fills = fills or ["mint"] * len(labels)
    positions = np.linspace(300, 1620, len(labels))
    width = min(360, 1150/len(labels))
    for i, (x, label, fill) in enumerate(zip(positions, labels, fills)):
        box(c, x, y, label, fill=fill, width=width, height=125)
        if i < len(labels)-1:
            flow(c, x+width/2+12, y, positions[i+1]-width/2-12, y, t, fill)


class Film:
    SCENES = {
        1: {"scouts", "identifier", "paraphrase", "complement", "stages", "parallel", "cascade", "questions"},
        2: {"lists", "scales", "formula", "record-a", "totals", "constant", "gaps", "boundary"},
        3: {"decisions", "blend", "route", "agency", "depths", "weights", "variants", "evaluate"},
    }

    def __init__(self, episode, timeline):
        self.episode, self.timeline = episode, timeline
        self.number = int(episode["id"][:2])
        self.accent = episode["accent"]
        self.stars = np.random.default_rng(1010).uniform([20, 230, 1], [1900, 820, 3], (55, 3))

    def at(self, scene, word, fallback=1):
        take = next((v for v in self.timeline.get("takes", []) if v["id"] == scene), None)
        if take:
            hits = [w for w in take["words"] if w["text"].lower().strip(".,!?;:'") == word.lower()]
            if hits:
                return hits[0]["start"] - self.timeline["scenes"][scene][0]
        return fallback

    def draw(self, c, t):
        c.clear(color("bg"))
        circle(c, -40, 630, 365, "panel", .4)
        circle(c, 1920, 330, 320, "panel2", .28)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+8*math.sin(t*.09+i), y+5*math.cos(t*.12+i), r, "muted", .45)
        name = next((s for s, (a, b) in self.timeline["scenes"].items() if a <= t < b), self.episode["scenes"][-1]["id"])
        scene = next(s for s in self.episode["scenes"] if s["id"] == name)
        a, b = self.timeline["scenes"][name]
        u, p = t-a, clamp((t-a)/(b-a))
        text(c, f"CHAPTER 10   /   FILM {self.number:02d}", 105, 79, 25, self.accent, True, "left")
        text(c, self.episode["subtitle"], 1815, 79, 25, "muted", align="right")
        text(c, scene["title"], 960, 173+(1-pop(u/.7))*30, 64, "white", True, max_width=1700)
        c.save()
        c.translate(0, (1-pop(u/.7))*40)
        (self.hybrid, self.fusion, self.routing)[self.number-1](c, name, u, p)
        c.restore()
        rect(c, 200, 849, 1520, 70, "panel", 35)
        text(c, scene["claim"], 960, 897, 34, self.accent, True, max_width=1440)
        text(c, "Adapted from Chapter 10 · Aaron Tay", 105, 945, 20, "muted", align="left")
        for i, s in enumerate(self.episode["scenes"]):
            circle(c, 1652+i*22, 937, 5, self.accent if s["id"] == name else "panel2")
        if b-t < .28 and scene != self.episode["scenes"][-1]:
            q = smooth((.28-(b-t))/.28)
            rect(c, 1920-1920*q, 230, 1920*q, 590, self.accent, 0)

    def hybrid(self, c, name, t, p):
        if name == "scouts":
            circle(c, 960, 494, 160, "violet")
            circle(c, 915, 450, 96, "blue")
            circle(c, 1040, 540, 62, "mint")
            orbit(c, 960, 495, 232, t, "pink", 11)
            for i in range(5):
                a = i*math.tau/5+t*.1
                paper(c, 960+math.cos(a)*240, 494+math.sin(a)*190, chr(65+i), [], t, .25)
            scout(c, 400, 510, t, "LEXICAL")
            scout(c, 1530, 510, t, "DENSE")
            text(c, "INDEXED WORDS", 400, 751, 31, "blue", True)
            text(c, "LEARNT COORDINATES", 1530, 751, 31, "mint", True)
            text(c, "THE COLLECTION", 960, 784, 26, "muted", True)
        elif name == "identifier":
            chip(c, "Need: ZX-41", 960, 300, 510, "yellow", 42)
            scout(c, 460, 493, t, "LEXICAL", .85)
            scout(c, 1430, 493, t, "DENSE", .85)
            for x, tag, fill in ((370, "ZX-41", "blue"), (1330, "ZX-41", "mint"), (1570, "ZX-14", "pink")):
                flow(c, 460 if x < 800 else 1430, 635, x, 683, t, fill)
                chip(c, tag, x, 735, 204, fill, 34, 67)
            text(c, "Analysed term evidence", 460, 796, 29, "blue")
            text(c, "A possible blurred distinction", 1430, 796, 29, "muted")
        elif name == "paraphrase":
            box(c, 430, 378, "QUERY", "delulu about a job", "yellow", 480)
            box(c, 1490, 378, "PASSAGE", "unrealistic employment expectations", "mint", 510)
            scout(c, 670, 616, t, "LEXICAL", .67)
            scout(c, 1250, 616, t, "DENSE", .67)
            flow(c, 675, 378, 905, 378, t, "mint")
            flow(c, 1015, 378, 1215, 378, t, "mint")
            orbit(c, 960, 378, 54, t, "mint", 5)
            text(c, "BRIDGE", 960, 390, 24, "mint", True)
            text(c, "No distinctive slang match", 670, 790, 29, "blue")
            text(c, "Possible learnt connection", 1250, 790, 29, "mint")
        elif name == "complement":
            ranked_list(c, 365, 334, LEXICAL, "LEXICAL", t, 330, "blue")
            ranked_list(c, 1515, 334, DENSE, "DENSE", t, 330, "mint")
            for i, d in enumerate(("A", "B", "C", "D")):
                card(c, d, 755+(i%2)*320, 460+(i//2)*154, t)
            flow(c, 547, 515, 650, 515, t, "blue")
            flow(c, 1335, 515, 1200, 515, t, "mint")
            text(c, "4 UNIQUE CANDIDATES", 960, 325, 30, "yellow", True)
            text(c, "Identity first. Then order.", 960, 766, 34, "muted")
        elif name == "stages":
            mini_pipeline(c, 380, ["BM25", "CANDIDATES", "RERANKER"], t, ["blue", "yellow", "pink"])
            text(c, "ONE CANDIDATE-GENERATION ROUTE", 960, 517, 32, "blue", True)
            rect(c, 360, 580, 1200, 172, "panel", 36)
            text(c, "A SINGLE SCORING STAGE", 960, 624, 29, "mint", True)
            text(c, "Lexical evidence + dense evidence → blended score", 960, 693, 33)
            text(c, "Hybrid can also happen within one stage", 960, 808, 29, "muted")
        elif name in ("parallel", "cascade"):
            box(c, 280, 510, "QUERY", fill="yellow", width=230)
            for y, label, fill in ((360, "LEXICAL", "blue"), (655, "DENSE", "mint")):
                flow(c, 406, 510, 558, y, t, fill)
                box(c, 730, y, label, "candidate list", fill, 310)
                flow(c, 900, y, 1048, 510, t, fill)
            box(c, 1200, 510, "FUSION", "one ranking", "yellow", 270)
            if name == "cascade":
                flow(c, 1350, 510, 1460, 510, t, "pink")
                box(c, 1620, 510, "RERANKER", "fused shortlist", "pink", 280)
                card(c, "E", 1580, 747, t, .57)
                text(c, "Missed by both routes", 1570, 811, 26, "coral")
            else:
                flow(c, 1350, 510, 1460, 510, t, "yellow")
                for i, d in enumerate(("A", "C", "B", "D")):
                    card(c, d, 1600, 332+i*113, t, .74)
            text(c, "MULTIPLE ROUTES", 735, 807, 28, "mint", True)
        elif name == "questions":
            scout(c, 355, 504, t, "LEXICAL", .9)
            scout(c, 1560, 504, t, "DENSE", .9)
            for i, value in enumerate(("Which routes ran?", "How deep were the lists?", "How were duplicates handled?", "Which combination rule?")):
                box(c, 960, 315+i*128, value, fill=("blue", "mint", "yellow", "pink")[i], width=650, height=103)

    def fusion(self, c, name, t, p):
        scores = rrf((LEXICAL, DENSE))
        if name == "lists":
            ranked_list(c, 470, 344, LEXICAL, "LEXICAL RANKING", t, 470, "blue")
            ranked_list(c, 1450, 344, DENSE, "DENSE RANKING", t, 470, "mint")
            orbit(c, 960, 535, 126, t, "yellow")
            robot(c, 960, 535, t, .73, "yellow")
            text(c, "Same letter = same record", 960, 791, 34, "muted")
        elif name == "scales":
            for x, label, nums, fill in ((470, "TOY BM25 SCORES", (18.6, 12.1, 8.4), "blue"), (1450, "TOY SIMILARITIES", (.86, .81, .72), "mint")):
                rect(c, x-295, 275, 590, 466, "panel", 32)
                text(c, label, x, 325, 28, fill, True)
                for i, n in enumerate(nums):
                    y = 403+i*105
                    rect(c, x-209, y-20, 290*(n/max(nums)), 47, fill, 14)
                    text(c, f"{n:g}", x+183, y+15, 32, fill, True)
            text(c, "+ ?", 960, 540, 80, "coral", True)
            text(c, "Unlike scales need a combination decision", 960, 806, 32, "muted")
        elif name == "formula":
            text(c, "RRF(d) = Σ  1 / (c + rank)", 960, 385, 73, "yellow", True)
            for x, title, sub, fill in ((415, "POSITION", "Rank starts at 1", "blue"), (960, "CONSTANT c", "Here: 60", "yellow"), (1505, "ABSENT", "Adds zero", "coral")):
                box(c, x, 604, title, sub, fill, 440, 176)
            text(c, "Sum across supplied lists containing d", 960, 475, 33, "muted")
            text(c, "The constant is not a result count", 960, 794, 30, "yellow")
        elif name == "record-a":
            card(c, "A", 960, 305, t, 1.12)
            for x, title, fraction, fill in ((460, "LEXICAL #1", "1 / 61", "blue"), (1460, "DENSE #2", "1 / 62", "mint")):
                text(c, title, x, 411, 30, fill, True)
                text(c, fraction, x, 512, 69, fill, True)
            text(c, "+", 960, 510, 72, "yellow", True)
            reveal = pop((t-self.at(name, "Together", 8))/.8)
            flow(c, 480, 562, 810, 680, t, "blue")
            flow(c, 1440, 562, 1110, 680, t, "mint")
            c.saveLayerAlpha(None, int(reveal*255))
            box(c, 960, 710, "0.03252", "rounded RRF total", "yellow", 440, 153)
            c.restore()
        elif name in ("totals", "weights"):
            self.score_table(c, t, weighted=name == "weights")
        elif name == "constant":
            for x, constant, fill in ((480, 1, "blue"), (1435, 60, "yellow")):
                rect(c, x-340, 275, 680, 490, "panel", 35)
                text(c, f"c = {constant}", x, 336, 44, fill, True)
                for i, rank in enumerate((1, 2, 3)):
                    value = 1/(constant+rank)
                    y = 438+i*97
                    text(c, f"#{rank}", x-245, y+8, 28, "muted", True)
                    rect(c, x-178, y-24, 309*value/(1/(constant+1)), 47, fill, 12)
                    text(c, f"{value:.5f}", x+216, y+9, 27, fill, True)
                text(c, f"#1 / #3 = {(constant+3)/(constant+1):.3f}", x, 729, 31, fill, True)
            text(c, "Bars are scaled separately; compare ratios", 960, 816, 28, "muted")
        elif name == "gaps":
            for x, values, label, fill in ((490, (10.0, 9.9), "SMALL GAP", "blue"), (1430, (100.0, 1.0), "LARGE GAP", "pink")):
                rect(c, x-338, 275, 676, 430, "panel", 34)
                text(c, label, x, 330, 32, fill, True)
                for i, value in enumerate(values):
                    y = 445+i*125
                    text(c, f"#{i+1}", x-255, y+10, 28, "muted")
                    rect(c, x-193, y-22, max(7, 322*value/values[0]), 48, fill, 12)
                    text(c, f"{value:g}", x+229, y+14, 30, fill, True)
                text(c, "Toy raw scores", x, 667, 25, "muted")
            text(c, "Both become: #1 adds 1/61 · #2 adds 1/62", 960, 790, 35, "yellow", True)
        elif name == "boundary":
            ranked_list(c, 420, 320, (*LEXICAL, "E"), "LEXICAL", t, 390, "blue", 3)
            ranked_list(c, 1500, 320, (*DENSE, "E"), "DENSE", t, 390, "mint", 3)
            box(c, 960, 416, "SUPPLIED UNION", "A, B, C, D", "yellow", 500)
            card(c, "E", 960, 639, t, .8)
            text(c, "No contribution", 960, 741, 36, "coral", True)
            text(c, "Depth 3 per route; E is below both cutoffs", 960, 813, 27, "muted")

    def score_table(self, c, t, weighted=False):
        weights = (1, 2) if weighted else (1, 1)
        scores = rrf((LEXICAL, DENSE), weights=weights)
        ranked_list(c, 285, 366, LEXICAL, "LEXICAL × 1", t, 310, "blue")
        ranked_list(c, 1635, 366, DENSE, f"DENSE × {weights[1]}", t, 310, "mint")
        rect(c, 495, 267, 930, 530, "panel", 30)
        for x, label in ((575, "RECORD"), (815, "LEXICAL"), (1065, "DENSE"), (1300, "TOTAL")):
            text(c, label, x, 315, 22, "muted", True)
        for i, d in enumerate(order(scores)):
            y = 390+i*117
            card(c, d, 575, y, t, .59)
            lr = LEXICAL.index(d)+1 if d in LEXICAL else None
            dr = DENSE.index(d)+1 if d in DENSE else None
            text(c, f"1/{60+lr}" if lr else "0", 815, y+13, 34, "blue", True)
            text(c, f"{weights[1]}/{60+dr}" if dr else "0", 1065, y+13, 34, "mint", True)
            rect(c, 1188, y-31, 213, 68, FILLS[d], 17)
            text(c, f"{scores[d]:.5f}", 1295, y+13, 32, "ink", True)
        text(c, "Calculated weighted example" if weighted else "Chapter 10 worked example · c = 60", 960, 827, 27, "muted")

    def routing(self, c, name, t, p):
        if name == "decisions":
            for x, title, fill in ((520, "CHOOSE PATHS", "pink"), (1400, "COMBINE LISTS", "yellow")):
                orbit(c, x, 475, 176, t, fill)
                robot(c, x, 475, t, .9, fill)
                chip(c, title, x, 733, 515, fill, 35)
            flow(c, 764, 492, 1156, 492, t, "mint")
            text(c, "ROUTING", 520, 300, 35, "pink", True)
            text(c, "FUSION", 1400, 300, 35, "yellow", True)
        elif name in ("blend", "route"):
            box(c, 300, 500, "QUESTION", fill="yellow", width=250)
            for y, kind, fill in ((338, "LEXICAL", "blue"), (665, "DENSE", "mint")):
                active = name == "blend" or int(t/5)%3 in ((0, 2) if kind == "LEXICAL" else (1, 2))
                c.saveLayerAlpha(None, 255 if active else 50)
                flow(c, 680 if name == "route" else 445, 500, 830, y, t, fill)
                box(c, 1020, y, kind, "supplied list", fill, 340)
                flow(c, 1205, y, 1445, 500, t, fill)
                c.restore()
            if name == "route":
                flow(c, 442, 500, 497, 500, t, "pink")
                box(c, 590, 500, "ROUTER", fill="pink", width=200)
                text(c, ("LEXICAL ONLY", "DENSE ONLY", "BOTH ROUTES")[int(t/5)%3], 590, 745, 27, "pink", True)
            both = name == "blend" or int(t/5)%3 == 2
            box(c, 1620, 500, "FUSION" if both else "ONE LIST", "combine" if both else "no fusion needed", "yellow", 270)
            text(c, "Prescribed routes run together" if name == "blend" else "Illustrative choices; no real router measured", 960, 811, 28, "muted")
        elif name == "agency":
            for i, (title, fill) in enumerate((("RULE", "blue"), ("CLASSIFIER", "mint"), ("MODEL", "pink"))):
                x = 385+i*575
                box(c, x, 364, title, "can choose a route", fill, 425)
                flow(c, x, 457, 960, 570, t+i, fill)
            box(c, 960, 674, "ROUTING DECISION", "Separate from choosing subsequent actions", "yellow", 790, 177)
        elif name == "depths":
            ranked_list(c, 270, 344, LEXICAL, "INPUT: 3", t, 290, "blue")
            ranked_list(c, 650, 344, DENSE, "INPUT: 3", t, 290, "mint")
            flow(c, 814, 510, 944, 510, t, "yellow")
            ranked_list(c, 1195, 306, ("A", "C", "B", "D"), "4 UNIQUE", t, 360, "yellow", 2)
            box(c, 1640, 445, "OUTPUT: 2", "Show A and C", "pink", 320)
            text(c, "B and D reached fusion", 1640, 651, 28, "yellow")
            text(c, "They were not shown", 1640, 701, 28, "muted")
            text(c, "Input cutoff ≠ output cutoff ≠ constant c", 960, 815, 32, "pink", True)
        elif name == "weights":
            self.score_table(c, t, weighted=True)
        elif name == "variants":
            for i, (title, fill) in enumerate((("QUERY VARIANT 1", "blue"), ("QUERY VARIANT 2", "mint"), ("QUERY VARIANT 3", "pink"))):
                x = 390+i*570
                box(c, x, 320, title, fill=fill, width=425, height=110)
                flow(c, x, 388, x, 453, t, fill)
                box(c, x, 519, "SAME RETRIEVER", "a ranked list", fill, 425, 120)
                flow(c, x, 591, 960, 696, t+i, fill)
            box(c, 960, 748, "RECIPROCAL RANK FUSION", fill="yellow", width=655, height=96)
        elif name == "evaluate":
            labels = ("LEXICAL", "DENSE", "COMBINED")
            for i, label in enumerate(labels):
                x = 400+i*560
                fill = ("blue", "mint", "yellow")[i]
                box(c, x, 337, label, fill=fill, width=420, height=108)
                for j, d in enumerate(("A", "C", "E")):
                    card(c, d, x-119, 467+j*101, t, .48)
                    text(c, "Judge usefulness", x+65, 477+j*101, 25, "muted")
            text(c, "Same queries · stated depths · local judgements", 960, 808, 34, "pink", True)
