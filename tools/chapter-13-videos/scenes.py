"""Original vector detective stories for Chapter 13, drawn with Skia."""
from __future__ import annotations

from collections import Counter
import math
import numpy as np
from visuals import (arrow, check, chip, circle, clamp, color, flow, font, line,
                     paper, polygon, pop, rect, robot, text)

TOKEN_PIECES = ("ri", "##zz", "##lord")
IDENTIFIERS = ("DELULU-427", "DELULU-428")
DIRECTION_PAIR = ("A causes B", "B causes A")


def boundary(covered, eligible, candidate, displayed):
    """Return the earliest established boundary; unknown is not exclusion."""
    for observed, label in ((covered, "coverage"), (eligible, "filter"),
                            (candidate, "candidate"), (displayed, "display")):
        if observed is None:
            return "unknown"
        if not observed:
            return label
    return "visible"


def exact_matches(query, records):
    # Schematic keyword-field identity comparison, not a text analyser.
    return [value for value in records if value == query]


def bag(value):
    return Counter(value.lower().split())


def validate_examples():
    assert boundary(False, None, None, None) == "coverage"
    assert boundary(True, False, None, None) == "filter"
    assert boundary(True, True, False, None) == "candidate"
    assert boundary(True, True, True, False) == "display"
    assert boundary(True, True, None, False) == "unknown"
    assert exact_matches(IDENTIFIERS[0], IDENTIFIERS) == [IDENTIFIERS[0]]
    assert bag(DIRECTION_PAIR[0]) == bag(DIRECTION_PAIR[1])
    assert "".join(part.removeprefix("##") for part in TOKEN_PIECES) == "rizzlord"


def wrap(c, value, x, y, width=480, size=29, fill="muted", bold=False):
    rows, current = [], ""
    for word in value.split():
        trial = (current + " " + word).strip()
        if current and font(size, bold).measureText(trial) > width:
            rows.append(current)
            current = word
        else:
            current = trial
    if current:
        rows.append(current)
    for i, row in enumerate(rows):
        text(c, row, x, y+i*size*1.3, size, fill, bold)


def box(c, x, y, title, subtitle="", fill="mint", width=420, height=160):
    rect(c, x-width/2, y-height/2, width, height, "panel2", 28)
    text(c, title, x, y-8 if subtitle else y+12, 34, fill, True, max_width=width-36)
    if subtitle:
        wrap(c, subtitle, x, y+36, width-42, 26)


def card(c, ident, x, y, t, fill="mint", scale=1):
    c.save()
    c.translate(x, y+math.sin(t*1.7+x*.01)*5)
    c.rotate(2*math.sin(t*.8+x*.01))
    c.scale(scale, scale)
    rect(c, -64, -83, 128, 166, fill, 16)
    polygon(c, [(28, -83), (64, -47), (28, -47)], "white", .65)
    text(c, ident, 0, 17, 48, "ink", True)
    for i in range(2):
        line(c, [(-34, 40+i*16), (34, 40+i*16)], "ink", 4, .4)
    c.restore()


def lens(c, x, y, t, scale=1, fill="mint"):
    c.save()
    c.translate(x, y+math.sin(t*1.7)*5)
    c.rotate(4*math.sin(t*.6))
    c.scale(scale, scale)
    line(c, [(50, 60), (134, 154)], fill, 30)
    circle(c, 0, 0, 108, fill, .13)
    circle(c, 0, 0, 108, fill, 1, 12)
    line(c, [(-63, -43), (-40, -65), (-16, -74)], "white", 9, .7)
    c.restore()


def boundary_lane(c, t, active, candidate=True):
    labels = ("COLLECTION", "ELIGIBLE", "CANDIDATES", "DISPLAY")
    for i, label in enumerate(labels):
        x = 330+i*420
        box(c, x, 710, label, fill="mint" if i != active else "coral", width=320, height=94)
        if i < 3:
            flow(c, x+170, 710, x+250, 710, t, "muted")
        if i == active:
            circle(c, x, 710, 182, "coral", .22, 3)


def relation(c, x, y, reverse, t, fill="mint", label="causes"):
    chip(c, "A", x-230, y, 120, "blue", 47, 104)
    chip(c, "B", x+230, y, 120, "pink", 47, 104)
    if reverse:
        flow(c, x+155, y, x-155, y, t, fill)
    else:
        flow(c, x-155, y, x+155, y, t, fill)
    text(c, label, x, y-40, 31, fill, True)


class Film:
    SCENES = {
        1: {"missing", "coverage", "filter", "candidate", "display", "split", "bridge", "remedy"},
        2: {"layers", "index", "tokens", "identity", "shift", "sites", "compare", "fallback"},
        3: {"direction", "negation", "binding", "interaction", "lenses", "preserve", "test", "audit"},
    }

    def __init__(self, episode, timeline):
        self.episode, self.timeline = episode, timeline
        self.number = int(episode["id"][:2])
        self.accent = episode["accent"]
        self.stars = np.random.default_rng(1313).uniform([25, 240, 1], [1895, 818, 3], (65, 3))

    def at(self, scene, word, fallback=5):
        take = next((v for v in self.timeline.get("takes", []) if v["id"] == scene), None)
        if take:
            hits = [w for w in take["words"] if w["text"].lower().strip(".,!?;:'") == word.lower()]
            if hits:
                return hits[0]["start"]-self.timeline["scenes"][scene][0]
        return fallback

    def draw(self, c, t):
        c.clear(color("bg"))
        circle(c, -80, 610, 350, "panel", .6)
        circle(c, 1990, 420, 360, "panel2", .32)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+8*math.sin(t*.13+i), y+5*math.cos(t*.1+i), r, "muted", .45)
        name = next((s for s, (a, b) in self.timeline["scenes"].items() if a <= t < b), self.episode["scenes"][-1]["id"])
        scene = next(s for s in self.episode["scenes"] if s["id"] == name)
        a, b = self.timeline["scenes"][name]
        u, p = t-a, clamp((t-a)/(b-a))
        text(c, f"CHAPTER 13   /   FILM {self.number:02d}", 105, 78, 25, self.accent, True, "left")
        text(c, scene["title"], 105, 150, 49, "white", True, "left", 1710)
        text(c, scene["claim"], 105, 204, 30, "muted", False, "left", 1710)
        c.save()
        c.translate(0, (1-pop(u/.8))*28)
        (self.boundaries, self.vocabulary, self.logic)[self.number-1](c, name, u, p)
        c.restore()
        rect(c, 105, 856, 1710, 5, "panel2", 3)
        rect(c, 105, 856, 1710*p, 5, self.accent, 3)
        text(c, "HOW SEARCH DECIDES WHAT YOU SEE  ·  AARON TAY  ·  ORIGINAL ANIMATION  ·  CC BY 4.0", 105, 898, 20, "muted", False, "left")

    def boundaries(self, c, name, t, p):
        if name == "missing":
            robot(c, 370, 510, t, 1.2)
            lens(c, 600, 440, t, .65)
            for i in range(5):
                x = 895+i*180
                if i == 2:
                    rect(c, x-64, 365, 128, 166, "mint", 16, .8, 4)
                    text(c, "?", x, 475, 72, "mint", True)
                else:
                    card(c, chr(65+i), x, 448, t, "blue", .85)
            text(c, "KNOWN RELEVANT P: MISSING", 1280, 652, 36, "coral", True)
            wrap(c, "The result screen does not reveal the cause.", 1280, 740, 850, 33)
        elif name == "coverage":
            circle(c, 670, 475, 190, "blue", .18)
            circle(c, 670, 475, 190, "blue", .8, 4)
            for i in range(4):
                a = t*.18+i*math.tau/4
                card(c, chr(65+i), 670+math.cos(a)*130, 475+math.sin(a)*110, t, "blue", .52)
            card(c, "P", 1330, 460, t, "coral", 1.15)
            lens(c, 1430, 410, t, .5, "coral")
            text(c, "SEARCHABLE COLLECTION", 670, 265, 29, "blue", True)
            text(c, "OUTSIDE / NOT YET INDEXED", 1340, 642, 29, "coral", True)
            boundary_lane(c, t, 0)
        elif name == "filter":
            card(c, "P", 485+90*math.sin(t*.3)**2, 450, t, "blue", 1.1)
            flow(c, 660, 445, 855, 445, t, "blue")
            rect(c, 865, 285, 170, 335, "coral", 24, .16)
            for i in range(5):
                line(c, [(875+i*37, 298), (875+i*37, 608)], "coral", 10)
            chip(c, "DATE LIMIT", 950, 304, 290, "coral", 32)
            check(c, 1260, 448, False, 39)
            text(c, "Indexed ≠ eligible", 1540, 467, 38, "white", True, max_width=465)
            boundary_lane(c, t, 1)
        elif name == "candidate":
            card(c, "P", 410, 443, t, "coral", 1.03)
            rect(c, 700, 290, 670, 320, "panel", 35)
            text(c, "SHORTLIST", 1040, 325, 29, "mint", True)
            for i in range(3):
                card(c, chr(65+i), 840+i*200, 448, t, "mint", .8)
            flow(c, 1390, 448, 1500, 448, t)
            box(c, 1650, 445, "RERANK", "receives A, B, C", width=295)
            text(c, "P is absent before reranking begins", 960, 629, 32, "coral", True)
            boundary_lane(c, t, 2)
        elif name == "display":
            labels = ("A", "B", "C", "P")
            rect(c, 1110, 286, 540, 335, "panel2", 24)
            text(c, "DISPLAYED", 1380, 328, 30, "mint", True)
            for i, ident in enumerate(labels):
                y = 332+i*112
                chip(c, str(i+1), 425, y, 70, "blue", 29, 64)
                box(c, 730, y, ident, fill="coral" if ident == "P" else "mint", width=420, height=78)
                if i < 3:
                    card(c, ident, 1230+i*150, 465, t, "mint", .65)
            line(c, [(365, 620), (985, 620)], "coral", 5)
            text(c, "DISPLAY CUTOFF", 1380, 666, 29, "coral", True)
            text(c, "Retrieved, but below the visible boundary", 960, 802, 31, "muted")
        elif name == "split":
            rect(c, 190, 287, 570, 460, "panel2", 28)
            text(c, "WHOLE DOCUMENT", 475, 340, 30, "blue", True)
            box(c, 475, 452, "Intervention", fill="blue", width=445, height=98)
            box(c, 475, 630, "Outcome", fill="pink", width=445, height=98)
            line(c, [(225, 542), (725, 542)], "muted", 3)
            flow(c, 790, 458, 1000, 383, t, "blue")
            flow(c, 790, 630, 1000, 677, t, "pink")
            box(c, 1380, 380, "PASSAGE 1", "intervention evidence", "blue", 630, 170)
            box(c, 1380, 680, "PASSAGE 2", "outcome evidence", "pink", 630, 170)
            text(c, "What evidence is available together?", 1380, 541, 32, "yellow", True, max_width=610)
        elif name == "bridge":
            box(c, 470, 413, "QUERY", "heart attack recovery", "blue", 600, 175)
            box(c, 1450, 413, "RELEVANT TITLE", "Rehabilitation after myocardial infarction", "pink", 670, 175)
            flow(c, 800, 413, 1080, 413, t, "muted")
            lens(c, 960, 580, t, .6)
            text(c, "Related concepts · different lexical forms", 960, 757, 36, "mint", True)
        elif name == "remedy":
            chip(c, "heart attack", 520, 407, 430, "blue", 37)
            chip(c, "OR", 960, 407, 150, "yellow", 42)
            chip(c, "myocardial infarction", 1400, 407, 580, "pink", 34)
            for i, (label, subtitle) in enumerate((("EXPAND", "synonyms / controlled terms"),
                                                  ("ADD A ROUTE", "dense / hybrid, if useful"),
                                                  ("TEST", "known relevant record"))):
                box(c, 390+i*570, 656, label, subtitle, "mint", 490, 175)
            text(c, "BM25 ranks term evidence; the bridge comes from elsewhere.", 960, 812, 29, "muted")

    def vocabulary(self, c, name, t, p):
        if name == "layers":
            for i, (label, subtitle, fill) in enumerate((("INDEX", "Is there a posting list?", "blue"),
                  ("TOKENISER", "Can the string be encoded?", "pink"),
                  ("REPRESENTATION", "Is it useful for retrieval?", "mint"))):
                x = 420+i*540
                circle(c, x, 440, 132, fill, .16)
                lens(c, x, 405, t+i, .6, fill)
                box(c, x, 663, label, subtitle, fill, 470, 170)
            text(c, "Name the vocabulary. Then inspect the next layer.", 960, 815, 32, "yellow", True)
        elif name == "index":
            chip(c, "DELULU-427", 415, 370, 470, "yellow", 40)
            flow(c, 675, 370, 835, 370, t)
            box(c, 1190, 370, "KEYWORD FIELD", "complete identifier", "mint", 610, 170)
            chip(c, "delulu", 1080, 590, 275, "blue", 36)
            chip(c, "427", 1410, 590, 230, "blue", 36)
            text(c, "TEXT ANALYSIS: MAY SPLIT", 1245, 697, 29, "blue", True)
            wrap(c, "Illustrative analysis paths: inspect the actual field and analyser.", 960, 788, 1460, 30)
        elif name == "tokens":
            chip(c, "rizzlord", 960, 346, 540, "yellow", 55, 100)
            for i, piece in enumerate(TOKEN_PIECES):
                x = 550+i*410
                reveal = pop((t-self.at(name, "splits", 2)-i*.2)/.65)
                if reveal > 0:
                    flow(c, 960, 406, x, 515, t-i, "muted")
                    c.save()
                    c.translate(x, 587)
                    c.scale(reveal, reveal)
                    chip(c, piece, 0, 0, 300, "blue", 49, 115)
                    c.restore()
            text(c, "BERT tokeniser example from Appendix B", 960, 735, 30, "muted")
            text(c, "KNOWN PIECES ≠ USEFUL RETRIEVAL MEANING", 960, 814, 33, "coral", True)
        elif name == "identity":
            text(c, "EXACT IDENTITY REQUIRED", 960, 302, 30, "yellow", True)
            for i, ident in enumerate(IDENTIFIERS):
                x = 500+i*920
                box(c, x, 447, ident, "schematic comparison", "mint" if i == 0 else "coral", 730, 200)
                check(c, x, 637, i == 0, 36)
            lens(c, 970, 440, t, .45)
            text(c, "427 ≠ 428", 960, 747, 43, "yellow", True)
            text(c, "Lexical identity and learned similarity answer different questions.", 960, 812, 29, "muted")
        elif name == "shift":
            for x, fill, label in ((480, "blue", "TRAINING"), (1440, "pink", "DEPLOYMENT")):
                circle(c, x, 461, 174, fill, .25)
                circle(c, x-44, 417, 73, "white", .1)
                robot(c, x, 470, t, .9, fill)
                chip(c, label, x, 704, 440, fill, 35)
            flow(c, 730, 467, 1190, 467, t, "yellow")
            text(c, "Does the learned relevance relationship travel?", 960, 806, 34, "white", True)
        elif name == "sites":
            values = (("QUERY SHIFT", "style / length / intent", "blue"),
                      ("CORPUS SHIFT", "discipline / language / genre", "pink"),
                      ("TASK SHIFT", "one answer / all eligible studies", "mint"))
            for i, (label, subtitle, fill) in enumerate(values):
                x = 420+i*540
                box(c, x, 650, label, subtitle, fill, 485, 175)
                if i == 0:
                    for j, width in enumerate((170, 260, 345)):
                        rect(c, x-180, 331+j*61, width, 28, fill, 13)
                elif i == 1:
                    for j in range(3):
                        card(c, chr(65+j), x-125+j*125, 412, t, fill, .6)
                else:
                    card(c, "A", x-100, 408, t, fill, .68)
                    for j in range(4):
                        circle(c, x+60+j%2*57, 375+j//2*63, 20, fill)
            text(c, "Familiar words can still belong to a different retrieval task.", 960, 817, 31, "muted")
        elif name == "compare":
            text(c, "HYPOTHETICAL PATTERN · NO MODEL MEASURED", 960, 300, 27, "yellow", True)
            for i, (label, width, fill) in enumerate((("Familiar setting", 820, "blue"),
                                                   ("Local target task", 340, "pink"))):
                y = 435+i*170
                text(c, label, 280, y+14, 34, "white", True, "left", 410)
                rect(c, 750, y-37, 860, 76, "panel2", 18)
                rect(c, 750, y-37, width*pop(t/2), 76, fill, 18)
            text(c, "Compare a local query set and consistent relevance judgements.", 960, 802, 31, "mint", True)
        elif name == "fallback":
            rows = (("LEXICAL LOSS", "inspect fields and both analysis paths", "blue"),
                    ("IDENTITY / REPRESENTATION", "keep exact matching; test meaning", "yellow"),
                    ("SUSPECTED TRANSFER", "local evaluation before adaptation", "pink"))
            for i, (label, subtitle, fill) in enumerate(rows):
                y = 353+i*170
                box(c, 550, y, label, fill=fill, width=710, height=110)
                flow(c, 930, y, 1030, y, t-i, fill)
                box(c, 1420, y, subtitle, fill=fill, width=715, height=110)
            text(c, "Keep useful lexical or hybrid fallbacks; test the suspected mechanism.", 960, 818, 29, "muted")

    def logic(self, c, name, t, p):
        if name == "direction":
            text(c, "REQUIRED", 450, 306, 31, "mint", True)
            text(c, "OPPOSED PASSAGE", 1450, 306, 31, "coral", True)
            relation(c, 450, 443, False, t)
            relation(c, 1450, 443, True, t, "coral")
            for i, word in enumerate(("A", "causes", "B")):
                chip(c, word, 645+i*315, 672, 230, "yellow", 37)
            text(c, "Same bag of words · different direction", 960, 804, 35, "white", True)
        elif name == "negation":
            for i, label in enumerate(("does increase risk", "does NOT increase risk")):
                y = 401+i*247
                rect(c, 280, y-82, 1360, 164, "panel2", 30)
                text(c, label, 960, y+17, 55, "coral" if i == 0 else "mint", True)
            text(c, "A decisive local difference can disappear in an overall score.", 960, 818, 30, "muted")
        elif name == "binding":
            box(c, 485, 427, "CO-OCCURRENCE", "A occurs here. B occurs elsewhere.", "blue", 710, 270)
            box(c, 1430, 427, "REQUIRED RELATION", "A participates with B in this claim.", "mint", 710, 270)
            relation(c, 1430, 660, False, t, "mint", "required relation")
            chip(c, "A", 350, 660, 125, "blue", 45)
            chip(c, "B", 650, 660, 125, "pink", 45)
            text(c, "Phrase / proximity controls help with local order, but do not guarantee logic.", 960, 818, 28, "yellow")
        elif name == "interaction":
            chip(c, "QUERY", 365, 338, 330, "blue", 35)
            chip(c, "CANDIDATE", 365, 642, 330, "pink", 35)
            flow(c, 550, 338, 770, 438, t, "blue")
            flow(c, 550, 642, 770, 540, t, "pink")
            box(c, 1040, 487, "CROSS-ENCODER", "reads query and candidate jointly", "mint", 500, 330)
            for i in range(5):
                circle(c, 890+i*76, 365+8*math.sin(t+i), 11, "blue")
                circle(c, 890+i*76, 430+8*math.cos(t+i), 11, "pink")
                line(c, [(890+i*76, 378), (1194-i*76, 416)], "mint", 2, .35)
            flow(c, 1310, 487, 1450, 487, t)
            box(c, 1640, 485, "TEST LOGIC", "no guarantee", "yellow", 325, 180)
            text(c, "Neither reranking nor late interaction rescues an absent first-stage record.", 960, 808, 28, "muted")
        elif name == "lenses":
            for i, (label, sub, fill) in enumerate((("MISMATCH", "query ↔ record language", "blue"),
                       ("OOV", "a named vocabulary", "yellow"),
                       ("OOD", "training ↔ deployment", "pink"),
                       ("COMPOSITION", "logic / relations survive?", "mint"))):
                x, y = 550+(i%2)*825, 393+(i//2)*288
                lens(c, x-233, y-6, t+i, .46, fill)
                box(c, x+55, y, label, sub, fill, 500, 174)
            text(c, "Different kinds of evidence. More than one can apply.", 960, 818, 32, "white", True)
        elif name == "preserve":
            rows = (("STRICT BOOLEAN", "explicit logic over analysed terms", "blue"),
                    ("BM25", "rare matching lexical evidence", "yellow"),
                    ("SINGLE-VECTOR DENSE", "overall learned similarity", "pink"))
            for i, (label, subtitle, fill) in enumerate(rows):
                y = 365+i*166
                box(c, 545, y, label, fill=fill, width=710, height=114)
                flow(c, 930, y, 1030, y, t-i, fill)
                box(c, 1420, y, subtitle, fill=fill, width=715, height=114)
            text(c, "Reference patterns, not an exhaustive list. None preserves everything.", 960, 818, 29, "muted")
        elif name == "test":
            for i, (label, subtitle) in enumerate((("FIX THE REQUIREMENT", "known record / controlled contrast"),
                    ("CHANGE ONE MECHANISM", "intervention suggested by evidence"),
                    ("COMPARE RETRIEVAL", "same relevance requirement"))):
                x = 400+i*565
                box(c, x, 470, label, subtitle, "mint", 505, 250)
                if i < 2:
                    flow(c, x+268, 470, x+292, 470, t-i)
            robot(c, 310, 731, t, .58)
            text(c, "More visible records need not mean better relevance.", 1070, 754, 35, "yellow", True, max_width=1250)
        elif name == "audit":
            robot(c, 382, 496, t, 1.2)
            lens(c, 535, 399, t, .5)
            labels = ("Could it be searched?", "Where did it disappear?", "What did the test change?", "What remains unknown?")
            for i, label in enumerate(labels):
                y = 321+i*126
                rect(c, 790, y-48, 885, 93, "panel2", 20)
                check(c, 845, y, True, 17)
                text(c, label, 910, y+12, 32, "white", True, "left", 715)
            text(c, "HYPOTHESIS → COMPARISON → EVIDENCE TRAIL", 960, 816, 33, "mint", True)
