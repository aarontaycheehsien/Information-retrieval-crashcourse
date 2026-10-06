"""Original vector animation for Chapter 11; all retrieval examples are schematic."""
from __future__ import annotations

import math
import numpy as np

from visuals import (arrow, chip, circle, clamp, color, flow, font, line,
                     paper, polygon, pop, rect, robot, smooth, text)

DOORS = (
    ("TEXT", "words / prose", "blue"),
    ("STRUCTURE", "headings / fields", "mint"),
    ("CITATION", "follow a relation", "yellow"),
    ("SEED PAPER", "query by example", "pink"),
    ("JUDGEMENT", "retrieval feedback", "coral"),
    ("BROWSE / ALERT", "follow a collection", "violet"),
    ("API PREDICATE", "filters / identifiers", "blue"),
    ("TASK BRIEF", "instruct a controller", "mint"),
)
# Citation arrows always run from a citing paper to its reference.
REFERENCES = {"A": {"C", "D"}, "B": {"C"}, "C": set(), "D": {"C"}, "E": {"A", "B"}}
STUDIES = (
    {"id": "A", "year": 2021, "topic": "citation advantage", "oa": False},
    {"id": "B", "year": 2023, "topic": "citation advantage", "oa": True},
    {"id": "C", "year": 2018, "topic": "citation advantage", "oa": True},
)


def citation_neighbours(seed, forward=False):
    return {d for d, refs in REFERENCES.items() if seed in refs} if forward else REFERENCES[seed]


def scoped_studies(require_oa=False):
    return {d["id"] for d in STUDIES if 2020 <= d["year"] <= 2024 and (not require_oa or d["oa"])}


def validate_examples():
    assert len(DOORS) == 8
    assert citation_neighbours("A") == {"C", "D"}
    assert citation_neighbours("A", forward=True) == {"E"}
    assert REFERENCES["A"] & REFERENCES["B"] == {"C"}  # Bibliographic coupling.
    assert {"A", "B"}.issubset(REFERENCES["E"])  # Co-cited by E.
    assert scoped_studies() == {"A", "B"}
    assert scoped_studies(require_oa=True) == {"B"}  # An unnecessary filter excludes A.


def wrapped(c, value, x, y, size=30, fill="white", width=470, bold=False):
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


def box(c, x, y, title, sub="", fill="mint", width=380, height=145):
    rect(c, x-width/2, y-height/2, width, height, "panel2", 28)
    text(c, title, x, y-12 if sub else y+12, 32, fill, True, max_width=width-34)
    if sub:
        wrapped(c, sub, x, y+30, 27, "muted", width-36)


def orbit(c, x, y, r, t, fill="mint", count=9):
    circle(c, x, y, r, fill, .2, 3)
    for i in range(count):
        a = t*.22+i*math.tau/count
        circle(c, x+r*math.cos(a), y+r*math.sin(a), 6, fill, .75)


def record(c, d, x, y, t, fill="mint", scale=1):
    c.save()
    c.translate(x, y+math.sin(t*1.8+x*.007)*4)
    c.scale(scale, scale)
    rect(c, -55, -65, 110, 130, fill, 16)
    polygon(c, [(24, -65), (55, -34), (24, -34)], "white", .6)
    text(c, d, 0, 0, 38, "ink", True)
    for i in range(2):
        rect(c, -29, 22+i*15, 58, 5, "ink", 2, .45)
    c.restore()


def parchment(c, x, y, t, imagined=True, scale=1):
    c.save()
    c.translate(x, y+math.sin(t*1.2)*7)
    c.rotate(math.sin(t*.7)*2)
    c.scale(scale, scale)
    rect(c, -143, -183, 286, 366, "pink" if imagined else "mint", 26)
    polygon(c, [(79, -183), (143, -119), (79, -119)], "white", .75)
    circle(c, 0, -84, 41, "ink")
    text(c, "?" if imagined else "A", 0, -69, 47, "pink" if imagined else "mint", True)
    for i, w in enumerate((193, 166, 193, 137, 180)):
        rect(c, -96, -7+i*29, w, 10, "ink", 5, .45)
    c.restore()


def icon(c, kind, x, y, t, fill="mint", scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    if kind in (0, 1, 6, 7):
        rect(c, -56, -48, 112, 96, fill, 16)
        if kind == 6:
            text(c, "{ }", 0, 16, 48, "ink", True)
        elif kind == 0:
            text(c, "Aa", 0, 14, 44, "ink", True)
        else:
            for i in range(3):
                rect(c, -32, -26+i*24, 64, 8, "ink", 4)
                if kind == 7:
                    circle(c, -41, -22+i*24, 4, "ink")
    elif kind == 2:
        for a, b in (((-46, 28), (0, -32)), ((0, -32), (46, 28))):
            flow(c, *a, *b, t, fill)
        for xx, yy in ((-46, 28), (0, -32), (46, 28)):
            circle(c, xx, yy, 15, fill)
    elif kind == 3:
        record(c, "A", 0, 0, t, fill, .75)
    elif kind == 4:
        circle(c, 0, 0, 49, fill)
        line(c, [(-26, 0), (-6, 23), (29, -23)], "ink", 10)
    elif kind == 5:
        rect(c, -58, -43, 116, 87, fill, 14)
        for i in range(3):
            rect(c, -35+i*29, -28, 20, 54, "ink", 4)
        circle(c, 51, -41, 18, "coral")
    c.restore()


def door(c, i, x, y, t, scale=1):
    label, sub, fill = DOORS[i]
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    rect(c, -154, -100, 308, 204, "panel", 32)
    rect(c, -63, -75, 126, 128, fill, 60, stroke=7)
    icon(c, i, 0, -15, t, fill, .56)
    text(c, label, 0, 84, 25, fill, True)
    text(c, sub, 0, 126, 24, "muted")
    c.restore()


def pipeline(c, labels, y, t, fills=None, width=None):
    fills = fills or ["mint"]*len(labels)
    positions = np.linspace(310, 1610, len(labels))
    w = width or min(375, 1120/len(labels))
    for i, (x, value, fill) in enumerate(zip(positions, labels, fills)):
        box(c, x, y, value, fill=fill, width=w, height=123)
        if i+1 < len(labels):
            flow(c, x+w/2+12, y, positions[i+1]-w/2-12, y, t, fill)


class Film:
    SCENES = {
        1: {"doors", "text-structure", "graph-seed", "judgements", "browse-api", "brief", "receiver", "cooperate"},
        2: {"roles", "interpret", "expand", "alternatives", "paths", "feedback-loop", "feedback-risk", "representation"},
        3: {"imagined", "query2doc", "hyde", "assumptions", "translator", "products", "limits", "audit"},
    }

    def __init__(self, episode, timeline):
        self.episode, self.timeline = episode, timeline
        self.number = int(episode["id"][:2])
        self.accent = episode["accent"]
        self.stars = np.random.default_rng(1111).uniform([20, 230, 1], [1900, 820, 3], (58, 3))

    def at(self, scene, word, fallback):
        take = next((v for v in self.timeline.get("takes", []) if v["id"] == scene), None)
        if take:
            hit = next((w for w in take["words"] if w["text"].lower().strip(".,!?;:'") == word.lower()), None)
            if hit:
                return hit["start"]-self.timeline["scenes"][scene][0]
        return fallback

    def draw(self, c, t):
        c.clear(color("bg"))
        circle(c, -35, 660, 365, "panel", .6)
        circle(c, 1955, 380, 345, "panel2", .35)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+8*math.sin(t*.12+i), y+5*math.cos(t*.09+i), r, "muted", .5)
        name = next((s for s, (a, b) in self.timeline["scenes"].items() if a <= t < b), self.episode["scenes"][-1]["id"])
        scene = next(s for s in self.episode["scenes"] if s["id"] == name)
        a, b = self.timeline["scenes"][name]
        u, p = t-a, clamp((t-a)/(b-a))
        text(c, f"CHAPTER 11   /   FILM {self.number:02d}", 105, 79, 25, self.accent, True, "left")
        text(c, self.episode["subtitle"], 1815, 79, 25, "muted", align="right")
        text(c, scene["title"], 960, 173+(1-pop(u/.7))*30, 62, "white", True, max_width=1700)
        c.save()
        c.translate(0, (1-pop(u/.8))*40)
        (self.objects, self.transformations, self.generated)[self.number-1](c, name, u, p)
        c.restore()
        rect(c, 200, 849, 1520, 70, "panel", 35)
        text(c, scene["claim"], 960, 897, 33, self.accent, True, max_width=1440)
        text(c, "Adapted from Chapter 11 · Aaron Tay", 105, 945, 20, "muted", align="left")
        for i, s in enumerate(self.episode["scenes"]):
            circle(c, 1652+i*22, 937, 5, self.accent if s["id"] == name else "panel2")
        if b-t < .28 and scene != self.episode["scenes"][-1]:
            q = smooth((.28-(b-t))/.28)
            rect(c, 1920-1920*q, 230, 1920*q, 590, self.accent, 0)

    def objects(self, c, name, t, p):
        if name == "doors":
            text(c, "Does open access increase citations?", 960, 261, 37, "yellow", True)
            for i in range(8):
                c.saveLayerAlpha(None, int(255*pop((t-.16*i)/.8)))
                door(c, i, 280+(i%4)*455, 388+(i//4)*290, t, .95)
                c.restore()
        elif name == "text-structure":
            for x, k in ((480, 0), (1440, 1)):
                icon(c, k, x, 354, t, DOORS[k][2], 1.15)
            box(c, 480, 534, "FREE TEXT", "open access citation advantage", "blue", 650, 145)
            box(c, 1440, 534, "STRUCTURED EXPRESSION", "subject heading + fields + logic", "mint", 650, 145)
            flow(c, 480, 624, 480, 690, t, "blue")
            flow(c, 1440, 624, 1440, 690, t, "mint")
            text(c, "Lexical / dense / hybrid?", 480, 761, 33, "blue", True)
            text(c, "Annotations and database structure", 1440, 761, 30, "mint", True)
        elif name == "graph-seed":
            text(c, "CITATION RELATION", 475, 282, 31, "yellow", True)
            pts = {"A": (470, 490), "C": (250, 675), "D": (665, 675), "E": (470, 330)}
            for d in ("C", "D"):
                flow(c, pts["A"][0], pts["A"][1]+60, pts[d][0], pts[d][1]-65, t, "yellow")
            flow(c, 470, 394, 470, 422, t, "yellow")
            for d, (x, y) in pts.items():
                record(c, d, x, y, t, "yellow" if d == "A" else "blue", .7)
            text(c, "Arrows: citing paper → reference", 475, 801, 27, "muted")
            text(c, "SEED DOCUMENT", 1420, 282, 31, "pink", True)
            parchment(c, 1300, 467, t, False, .73)
            for i in range(3):
                record(c, chr(66+i), 1660, 360+i*119, t, "pink", .57)
                flow(c, 1417, 450+i*20, 1613, 360+i*119, t+i, "pink")
            box(c, 1430, 727, "PubMed Similar Articles", "Weighted title, abstract and MeSH words", "mint", 700, 132)
        elif name == "judgements":
            for x, title, sub, fill, kind in ((480, "EXPLICIT FEEDBACK", "Searcher accepts / rejects records", "mint", 4), (1440, "PSEUDO-RELEVANCE", "Top-ranked = assumed useful", "coral", 3)):
                icon(c, kind, x, 370, t, fill, 1.3)
                box(c, x, 559, title, sub, fill, 710, 170)
                flow(c, x, 664, x, 721, t, fill)
                text(c, "Construct another retrieval input", x, 787, 30, fill, True)
        elif name == "browse-api":
            icon(c, 5, 430, 357, t, "violet", 1.4)
            box(c, 430, 536, "BROWSE / MONITOR", "Journal · author · subject · alert", "pink", 595, 160)
            box(c, 1370, 348, "API PREDICATE", "Publication years: 2020–2024", "blue", 730, 135)
            for i, d in enumerate(STUDIES[:2]):
                x = 1190+i*350
                record(c, d["id"], x, 566, t, "mint" if d["oa"] else "yellow", .8)
                text(c, str(d["year"]), x, 671, 30, "white", True)
                text(c, "Open access" if d["oa"] else "Paywalled", x, 721, 30, "muted")
            text(c, "Both studies fit the topic and year range", 1370, 800, 28, "mint", True)
            text(c, "Schematic records", 430, 779, 25, "muted")
        elif name == "brief":
            robot(c, 410, 498, t, 1.15, "mint")
            orbit(c, 410, 498, 200, t, "pink")
            text(c, "CONTROLLER", 410, 787, 33, "mint", True)
            labels = ("Goal and scope", "Inclusion / exclusion", "Sources and coverage", "Limits and stopping", "Required search record")
            for i, value in enumerate(labels):
                box(c, 1280, 308+i*109, value, fill=("yellow", "blue", "pink", "coral", "mint")[i], width=740, height=85)
            flow(c, 883, 526, 646, 526, t, "mint")
        elif name == "receiver":
            rows = (("LEXICAL / BOOLEAN", "Concepts, variants, fields, tested operators", "blue"), ("DENSE RETRIEVER", "Description suited to training and domain", "mint"), ("QUERY TRANSLATOR", "Context → inspectable retrieval inputs", "pink"), ("CONTROLLER", "Scope, sources, coverage, stopping, record", "yellow"))
            for i, (title, sub, fill) in enumerate(rows):
                y = 305+i*140
                box(c, 440, y, title, fill=fill, width=575, height=100)
                flow(c, 745, y, 900, y, t+i, fill)
                box(c, 1335, y, sub, fill=fill, width=805, height=100)
        elif name == "cooperate":
            circle(c, 960, 522, 154, "violet")
            robot(c, 960, 524, t, .75, "yellow")
            for i in range(8):
                a = -math.pi/2+i*math.tau/8
                x, y = 960+math.cos(a)*650, 505+math.sin(a)*185
                icon(c, i, x, y, t, DOORS[i][2], .7)
                text(c, DOORS[i][0], x, y+74, 23, DOORS[i][2], True)
                if i in (0, 2, 3, 4):
                    flow(c, x+(960-x)*.15, y+(520-y)*.15, x+(960-x)*.62, y+(520-y)*.62, t+i, DOORS[i][2])
            text(c, "The need evolves as the searcher learns", 960, 820, 30, "mint", True)

    def transformations(self, c, name, t, p):
        if name == "roles":
            for i, (title, sub, fill) in enumerate((("UNDERSTAND", "Interpret the request", "blue"), ("TRANSFORM", "Create retrieval inputs", "yellow"), ("CONTROL", "Choose paths and passes", "pink"))):
                x = 405+i*555
                orbit(c, x, 427, 143, t+i, fill)
                robot(c, x, 428, t+i, .68, fill)
                box(c, x, 673, title, sub, fill, 470, 165)
        elif name == "interpret":
            box(c, 960, 319, "ORIGINAL REQUEST", "Citation-advantage studies from 2020 to 2024", "yellow", 1290, 135)
            pipeline(c, ["RECOGNISE DATES", "BUILD A CONDITION", "EXECUTE FIELD"], 547, t, ["blue", "yellow", "mint"], 410)
            for x, value, fill in ((310, "understanding", "blue"), (960, "transformation", "yellow"), (1610, "supported receiver", "mint")):
                text(c, value, x, 699, 28, fill)
            text(c, "Publication year: 2020–2024", 960, 791, 40, "mint", True)
        elif name == "expand":
            rows = (("CORRECT", "autsim", "autism", "coral"), ("MAP", "user term", "controlled heading", "blue"), ("EXPAND", "open access", "open access + variants", "mint"))
            for i, (label, old, new, fill) in enumerate(rows):
                y = 340+i*173
                text(c, label, 275, y+10, 31, fill, True)
                box(c, 740, y, old, fill=fill, width=450, height=108)
                flow(c, 985, y, 1160, y, t+i, fill)
                box(c, 1485, y, new, fill=fill, width=600, height=108)
            text(c, "Inspect replacements, headings, and additions", 960, 805, 29, "muted")
        elif name == "alternatives":
            box(c, 960, 319, "THE NEED", "Does open access increase citations?", "yellow", 1120, 127)
            for x, title, sub, fill in ((475, "ONE RELATIONSHIP", "open access ↔ citation advantage", "mint"), (1445, "TWO LOOSE TOPICS", "anything about access / anything about citations", "coral")):
                flow(c, 960, 400, x, 479, t, fill)
                box(c, x, 586, title, sub, fill, 780, 166)
            text(c, "Decomposition needs to preserve the relationship", 960, 792, 32, "yellow", True)
        elif name == "paths":
            for i, fill in enumerate(("blue", "mint", "pink")):
                y = 324+i*196
                box(c, 340, y, f"QUERY VARIANT {i+1}", fill=fill, width=380, height=113)
                flow(c, 545, y, 685, y, t+i, fill)
                box(c, 960, y, "SAME RETRIEVER", "ranked list", fill, 490, 130)
                flow(c, 1221, y, 1458, 519, t+i, fill)
            box(c, 1630, 520, "FUSION", "combine lists", "yellow", 310)
            text(c, "Three rewrites need not mean three retrieval methods", 960, 813, 29, "muted")
        elif name == "feedback-loop":
            pipeline(c, ["INITIAL QUERY", "FIRST RETRIEVAL", "TOP RECORDS"], 356, t, ["blue", "mint", "yellow"], 385)
            for i in range(3):
                record(c, chr(65+i), 1490+i*114, 550, t, "yellow", .6)
            flow(c, 1610, 431, 1610, 470, t, "yellow")
            flow(c, 1490, 550, 1210, 637, t, "pink")
            box(c, 960, 672, "SELECT TERMS → LATER INPUT", "Top records are assumed relevant", "pink", 650, 152)
            flow(c, 616, 672, 516, 672, t, "pink")
            box(c, 310, 672, "LATER RETRIEVAL", fill="mint", width=380, height=135)
            text(c, "Another retrieval pass may add candidates", 960, 811, 29, "mint", True)
        elif name == "feedback-risk":
            for x, fill, label in ((470, "pink", "RETRIEVAL FEEDBACK"), (1450, "blue", "SCREENING FEEDBACK")):
                rect(c, x-360, 294, 720, 416, "panel", 36)
                text(c, label, x, 352, 29, fill, True)
                for i in range(3):
                    record(c, chr(65+i), x-165+i*165, 498, t, fill, .6)
                if x < 900:
                    record(c, "D", x+264, 654, t, "mint", .49)
                    flow(c, x+20, 620, x+216, 650, t, "mint")
                    text(c, "New retrieval may add D", x-67, 658, 28, "mint", True)
                else:
                    text(c, "Reprioritise the existing pool", x, 658, 29, "blue", True)
            text(c, "Bad initial evidence can steer the next retrieval off topic", 960, 799, 31, "coral", True)
        elif name == "representation":
            box(c, 960, 299, "ORIGINAL INPUT", "open access citation advantage", "yellow", 1080, 123)
            for x, fill in ((480, "mint"), (1440, "pink")):
                flow(c, 960, 380, x, 438, t, fill)
            box(c, 480, 520, "SPLADE", "weighted vocabulary coordinates", "mint", 740, 142)
            box(c, 1440, 520, "LLM REWRITE", "text / structured expression", "pink", 740, 142)
            for i, (label, val) in enumerate((("access", .9), ("citations", .75), ("publishing", .4))):
                y = 663+i*53
                text(c, label, 270, y, 26, "muted", align="right")
                rect(c, 305, y-24, 350*val*(.9+.1*math.sin(t)), 28, "mint", 8)
            wrapped(c, "How does open-access publishing relate to citation counts?", 1440, 686, 32, "pink", 620)
            text(c, "Illustrative weights", 490, 825, 23, "muted")

    def generated(self, c, name, t, p):
        if name == "imagined":
            robot(c, 380, 530, t, .95, "pink")
            orbit(c, 380, 530, 180, t, "pink")
            flow(c, 596, 530, 779, 530, t, "pink")
            parchment(c, 960, 495, t, True, 1)
            for i in range(3):
                record(c, chr(65+i), 1530+(i%2)*156, 411+(i//2)*210, t, "mint", .8)
            flow(c, 1136, 530, 1399, 530, t, "mint")
            text(c, "HYPOTHETICAL", 960, 756, 35, "pink", True)
            text(c, "REAL INDEXED RECORDS", 1580, 790, 27, "mint", True)
        elif name in ("query2doc", "hyde"):
            self.generated_route(c, name, t)
        elif name == "assumptions":
            parchment(c, 465, 505, t, True, .98)
            chip(c, "Only physics?", 465, 735, 514, "coral", 38)
            box(c, 1220, 343, "INVENTED DETAIL", "Can steer vocabulary or vector similarity", "coral", 930, 158)
            flow(c, 674, 539, 1090, 539, t, "coral")
            for i in range(3):
                record(c, chr(65+i), 1190+i*215, 584, t, "mint", .8)
            text(c, "Read and assess the retrieved sources", 1310, 752, 34, "mint", True)
            text(c, "The generated detail remains unverified", 1310, 812, 28, "coral")
        elif name == "translator":
            box(c, 430, 324, "NATURAL-LANGUAGE INPUT", "topic + publication years", "pink", 640, 140)
            flow(c, 778, 324, 998, 324, t, "pink")
            box(c, 1430, 324, "STRUCTURED EXPRESSION", "topic conditions + year field", "blue", 740, 140)
            flow(c, 1430, 422, 1430, 464, t, "pink")
            for x, label, fill in ((1120, "BOOLEAN PATH", "blue"), (1640, "VECTOR PATH", "mint")):
                flow(c, 1430, 477, x, 542, t, fill)
                box(c, x, 620, label, fill=fill, width=440, height=115)
            box(c, 480, 610, "Web of Science Smart Search", "Documents Boolean conversion and blended search", "yellow", 710, 180)
            text(c, "Schematic arrangement · official documentation", 960, 824, 26, "muted")
        elif name == "products":
            for x, title, sub, fill in ((490, "EBSCO AI-Assisted Search", "Keyword and noun phrases", "blue"), (1430, "Primo NDE Natural Language Search", "Generated Boolean alternatives", "pink")):
                box(c, x, 339, title, sub, fill, 810, 175)
                flow(c, x, 451, x, 542, t, fill)
                box(c, x, 632, "ESTABLISHED ENGINE" if x < 900 else "ADVANCED SEARCH", "usual ranking and search functions" if x < 900 else "inspect and edit the generated query", fill, 810, 170)
            text(c, "Different products can share an interface label", 960, 809, 32, "yellow", True)
        elif name == "limits":
            for i, (label, fill) in enumerate((("DATE", "mint"), ("TYPE", "blue"), ("LANGUAGE", "pink"), ("AVAILABILITY", "yellow"))):
                chip(c, label, 350+i*410, 330, 335, fill, 30)
            box(c, 475, 568, "SUPPORTED CONSTRAINTS", "Inspect which fields and filters were inferred", "mint", 790, 194)
            box(c, 1445, 568, "CHECK THE LOGIC", "Author detection? AND intended, OR generated?", "coral", 790, 194)
            text(c, "Inferred from the request ≠ explicitly selected by the user", 960, 795, 31, "yellow", True)
        elif name == "audit":
            robot(c, 395, 502, t, 1.04, "yellow")
            orbit(c, 395, 502, 184, t, "mint")
            for i, (label, fill) in enumerate((("Original request and scope", "blue"), ("Every transformed / generated input", "pink"), ("Selected retrieval paths", "mint"), ("Intermediate feedback records", "coral"), ("Coverage and stopping trace", "yellow"))):
                box(c, 1270, 295+i*109, label, fill=fill, width=880, height=87)
            text(c, "Who chooses the next action? → Chapter 12", 960, 825, 30, "mint", True)

    def generated_route(self, c, name, t):
        hyde = name == "hyde"
        parchment(c, 375, 480, t, True, .86)
        text(c, "GENERATED PASSAGE", 375, 740, 29, "pink", True)
        box(c, 960, 384, "DENSE ENCODER" if hyde else "ORIGINAL QUERY", "encode the imagined document" if hyde else "+ generated language", "mint" if hyde else "yellow", 550, 165)
        flow(c, 526, 459, 660, 384, t, "pink")
        flow(c, 960, 486, 960, 550, t, "mint" if hyde else "yellow")
        if hyde:
            box(c, 960, 642, "VECTOR SEARCH", "nearest real document vectors", "mint", 550, 148)
            for i in range(5):
                a = t*.25+i*math.tau/5
                circle(c, 1540+math.cos(a)*156, 430+math.sin(a)*111, 13, "mint")
            circle(c, 1540, 430, 22, "pink")
            text(c, "VECTOR SPACE", 1540, 280, 28, "mint", True)
        else:
            box(c, 960, 642, "LEXICAL RETRIEVER", "BM25 route shown; dense also possible", "blue", 550, 148)
            for i, term in enumerate(("open access", "citations", "publication year")):
                chip(c, term, 1540, 331+i*104, 425, "blue", 31, 73)
        flow(c, 1260, 642, 1406, 642, t, "mint")
        for i in range(3):
            record(c, chr(65+i), 1460+i*140, 674, t, "mint", .63)
        text(c, "REAL RECORDS", 1600, 797, 29, "mint", True)
