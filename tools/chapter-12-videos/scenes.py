"""Original flat-vector search voyages for Chapter 12; no borrowed artwork."""
from __future__ import annotations

import math
import numpy as np
from visuals import (arrow, chip, circle, clamp, color, flow, font, line,
                     paper, polygon, pop, rect, robot, smooth, text)

RELATED = frozenset("ABCD")
REFERENCES = frozenset("AC")
ROUNDS = (frozenset(("citation differences",)),
          frozenset(("citation differences", "selection-bias methods")))


def uncited(related, references):
    return sorted(set(related) - set(references))


def cumulative(rounds):
    pool, history = set(), []
    for records in rounds:
        pool.update(records)
        history.append(frozenset(pool))
    return history


def validate_examples():
    assert uncited(RELATED, REFERENCES) == ["B", "D"]
    assert cumulative(ROUNDS)[0] < cumulative(ROUNDS)[1]
    assert cumulative((ROUNDS[0], ROUNDS[0]))[-1] == ROUNDS[0]


def wrap(c, value, x, y, width=470, size=29, fill="muted", bold=False):
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


def box(c, x, y, title, subtitle="", fill="mint", width=350, height=140):
    rect(c, x-width/2, y-height/2, width, height, "panel2", 26)
    text(c, title, x, y-5 if subtitle else y+12, 32, fill, True, max_width=width-30)
    if subtitle:
        wrap(c, subtitle, x, y+36, width-35, 23)


def orbit(c, x, y, radius, t, fill="mint", count=9):
    circle(c, x, y, radius, fill, .2, 3)
    for i in range(count):
        a = t*.2 + i*math.tau/count
        circle(c, x+math.cos(a)*radius, y+math.sin(a)*radius, 6, fill, .7)


def ship(c, x, y, t, scale=1, fill="mint"):
    c.save()
    c.translate(x, y+7*math.sin(t*1.7))
    c.scale(scale, scale)
    # An original round search ship with a robot navigator and pulsing exhaust.
    polygon(c, [(-120, 70), (-155, 70), (-205-18*math.sin(t*8), 126), (-85, 120)], "coral", .8)
    polygon(c, [(120, 70), (155, 70), (205+18*math.sin(t*8), 126), (85, 120)], "yellow", .8)
    circle(c, 0, -25, 113, "blue", .22)
    circle(c, 0, -25, 113, "blue", .7, 7)
    robot(c, 0, -8, t, .65, "yellow")
    rect(c, -178, 56, 356, 70, fill, 35)
    rect(c, -133, 98, 266, 43, "panel2", 22)
    for i in range(5):
        circle(c, -102+51*i, 89, 9, "white", .55+.4*math.sin(t*2+i)**2)
    c.restore()


def planet(c, x, y, t, label="INDEX", fill="blue", radius=110):
    circle(c, x, y, radius, fill)
    circle(c, x-radius*.25, y-radius*.24, radius*.57, "white", .13)
    circle(c, x+radius*.35, y+radius*.35, radius*.32, "ink", .14)
    orbit(c, x, y, radius+25, t, fill, 7)
    text(c, label, x, y+11, 28, "ink", True, max_width=radius*1.65)


def route(c, labels, y, t, fill="mint"):
    xs = np.linspace(280, 1640, len(labels))
    width = min(330, 1150/len(labels))
    for i, (x, label) in enumerate(zip(xs, labels)):
        box(c, x, y, label, fill=fill, width=width, height=120)
        if i < len(xs)-1:
            flow(c, x+width/2+12, y, xs[i+1]-width/2-12, y, t-i, fill)


def record(c, ident, x, y, t, fill="mint", scale=1):
    c.save()
    c.translate(x, y+math.sin(t*1.5+ord(ident[0]))*4)
    c.scale(scale, scale)
    rect(c, -52, -65, 104, 130, fill, 13)
    polygon(c, [(20, -65), (52, -33), (20, -33)], "white", .65)
    text(c, ident, 0, 17, 42, "ink", True)
    c.restore()


class Film:
    SCENES = {
        1: {"cockpit", "brief", "fixed", "adaptive", "agentic", "harness", "outputs", "rag"},
        2: {"engine", "subtract", "menu", "miss", "recover", "stop", "trade", "mcp"},
        3: {"empty", "autism", "synonyms", "broaden", "same", "limits", "library", "audit"},
    }

    def __init__(self, episode, timeline):
        self.episode, self.timeline = episode, timeline
        self.number = int(episode["id"][:2])
        self.accent = episode["accent"]
        self.stars = np.random.default_rng(1212).uniform([25, 235, 1], [1895, 810, 3], (65, 3))

    def at(self, scene, word, fallback=5):
        take = next((v for v in self.timeline.get("takes", []) if v["id"] == scene), None)
        if take:
            hits = [w for w in take["words"] if w["text"].lower().strip(".,!?;:'") == word.lower()]
            if hits:
                return hits[0]["start"]-self.timeline["scenes"][scene][0]
        return fallback

    def draw(self, c, t):
        c.clear(color("bg"))
        circle(c, -70, 630, 350, "panel", .6)
        circle(c, 1990, 360, 360, "panel2", .32)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+9*math.sin(t*.1+i), y+5*math.cos(t*.13+i), r, "muted", .45)
        name = next((s for s, (a, b) in self.timeline["scenes"].items() if a <= t < b), self.episode["scenes"][-1]["id"])
        scene = next(s for s in self.episode["scenes"] if s["id"] == name)
        a, b = self.timeline["scenes"][name]
        u, p = t-a, clamp((t-a)/(b-a))
        text(c, f"CHAPTER 12   /   FILM {self.number:02d}", 105, 79, 25, self.accent, True, "left")
        text(c, self.episode["subtitle"], 1815, 79, 25, "muted", align="right")
        text(c, scene["title"], 960, 173+(1-pop(u/.7))*30, 62, "white", True, max_width=1700)
        c.save()
        c.translate(0, (1-pop(u/.7))*40)
        (self.control, self.risks, self.recovery)[self.number-1](c, name, u, p)
        c.restore()
        rect(c, 200, 849, 1520, 70, "panel", 35)
        text(c, scene["claim"], 960, 897, 33, self.accent, True, max_width=1440)
        text(c, "Adapted from Chapter 12 · Aaron Tay", 105, 945, 20, "muted", align="left")
        for i, s in enumerate(self.episode["scenes"]):
            circle(c, 1652+i*22, 937, 5, self.accent if s["id"] == name else "panel2")
        if b-t < .28 and scene != self.episode["scenes"][-1]:
            q = smooth((.28-(b-t))/.28)
            rect(c, 1920-1920*q, 235, 1920*q, 580, self.accent, 0)

    def control(self, c, name, t, p):
        if name == "cockpit":
            ship(c, 575, 505, t, 1.4)
            planet(c, 1400, 505, t, "RETRIEVAL", "blue", 145)
            flow(c, 890, 525, 1170, 525, t)
            box(c, 570, 752, "NAVIGATOR", "chooses the next action", width=440, height=110)
            box(c, 1400, 752, "ENGINE", "finds and scores records", "blue", 440, 110)
            for i in range(3):
                paper(c, 1300+i*100, 295, chr(65+i), [], t, .21)
        elif name == "brief":
            rect(c, 310, 285, 680, 475, "white", 28)
            chip(c, "TASK BRIEF", 650, 316, 340, "mint", 35)
            for i, label in enumerate(("Scope and relevance criteria", "Sources and coverage", "Limits and stopping conditions", "Required output and search record")):
                circle(c, 362, 403+i*83, 11, "blue")
                text(c, label, 397, 414+i*83, 28, "ink", True, "left", 540)
            ship(c, 1415, 477, t, .9)
            flow(c, 1040, 475, 1170, 475, t)
            box(c, 1415, 732, "QUERIES + TOOL CALLS", fill="blue", width=540, height=100)
        elif name == "fixed":
            route(c, ("SEARCH", "EXPAND", "SEARCH", "MERGE", "RETURN"), 525, t, "blue")
            rect(c, 235, 285, 1450, 100, "panel", 24)
            text(c, "ONE PRESCRIBED SEQUENCE", 960, 350, 38, "blue", True)
            k = (t*.065) % 1
            ship(c, 280+k*1360, 420, t, .25, "blue")
            chip(c, "Result-dependent words", 650, 732, 490, "yellow", 29)
            chip(c, "Predetermined next operation", 1290, 732, 560, "blue", 29)
        elif name == "adaptive":
            box(c, 370, 510, "RESULTS", "inspect the yield", "blue", 330)
            flow(c, 555, 510, 775, 510, t)
            polygon(c, [(960, 365), (1105, 510), (960, 655), (815, 510)], "pink")
            text(c, "PICK", 960, 505, 37, "ink", True)
            text(c, "A BRANCH", 960, 548, 25, "ink", True)
            for i, (label, y) in enumerate((("BROADEN", 320), ("NARROW", 510), ("RETURN", 700))):
                active = int(t/3)%3 == i
                flow(c, 1125, 510, 1365, y, t, "yellow" if active else "panel2")
                box(c, 1550, y, label, fill="yellow" if active else "muted", width=330, height=110)
            text(c, "The chooser may be a rule OR a model", 690, 786, 31, "muted")
        elif name == "agentic":
            nodes = [(350, 335, "SEARCH"), (900, 310, "INSPECT"), (1510, 390, "REFERENCES"),
                     (1510, 705, "OTHER SOURCE"), (840, 700, "REVISE QUERY"), (325, 680, "STOP")]
            for i, (x, y, label) in enumerate(nodes):
                box(c, x, y, label, width=300, height=100, fill="mint")
                if i < 4:
                    xx, yy, _ = nodes[i+1]
                    arrow(c, x+70, y+70, xx-70, yy+70, "mint", 4)
            ship(c, 945+110*math.sin(t*.45), 492+30*math.cos(t*.7), t, .57)
            text(c, "Reusable actions · sequence planned during the run", 960, 811, 31, "muted")
        elif name == "harness":
            rect(c, 250, 270, 1420, 510, "panel", 45)
            rect(c, 250, 270, 1420, 510, "mint", 45, .65, 5)
            ship(c, 650, 475, t, .83)
            for i, label in enumerate(("Permitted tools", "Reachable sources", "Round and token budgets", "User approval gates")):
                box(c, 1290, 340+i*110, label, fill="mint", width=530, height=80)
            text(c, "A HARNESS DEFINES THE AVAILABLE MOVES", 650, 727, 27, "yellow", True, max_width=610)
        elif name == "outputs":
            text(c, "RECORDS", 900, 290, 29, "blue", True)
            text(c, "REPORT / ANSWER", 1450, 290, 29, "pink", True)
            for row, label in enumerate(("FIXED", "AGENTIC")):
                y = 455+250*row
                chip(c, label, 370, y, 300, "blue" if row == 0 else "mint", 33)
                for x in (900, 1450):
                    rect(c, x-225, y-105, 450, 210, "panel2", 24)
                for j in range(3):
                    record(c, chr(65+j), 790+j*110, y, t, "blue", .65)
                rect(c, 1390, y-70, 120, 145, "white", 12)
                for j in range(5):
                    line(c, [(1410, y-45+j*22), (1490, y-45+j*22)], "pink", 7)
            text(c, "Any cell can exist. Output does not establish control.", 960, 816, 29, "muted")
        elif name == "rag":
            route(c, ("CHOOSE ACTION", "RETRIEVE", "GENERATE ANSWER"), 500, t, "mint")
            robot(c, 280, 345, t, .45)
            paper(c, 960, 330, "SOURCE", [], t, .36)
            rect(c, 1590, 267, 100, 150, "white", 12)
            for i in range(5):
                line(c, [(1605, 295+i*23), (1675, 295+i*23)], "pink", 7)
            line(c, [(1640, 580), (1640, 675), (280, 675), (280, 580)], "mint", 4)
            arrow(c, 280, 640, 280, 580, "mint", 4)
            text(c, "Chosen retrieval actions towards a generated response", 960, 750, 32, "muted")

    def risks(self, c, name, t, p):
        if name == "engine":
            for i, (label, subtitle, fill) in enumerate((("HYBRID", "Which signals contribute?", "blue"),
                   ("MULTI-STAGE", "Which sequential operations?", "pink"), ("AGENTIC", "Who chooses the sequence?", "mint"))):
                x = 410+i*550
                orbit(c, x, 480, 140, t, fill)
                if i == 2:
                    robot(c, x, 480, t, .7, fill)
                elif i == 0:
                    circle(c, x-40, 480, 70, "blue", .9)
                    circle(c, x+40, 480, 70, "yellow", .7)
                else:
                    for j in range(3):
                        rect(c, x-78+j*38, 425+j*40, 80, 50, "pink", 10)
                box(c, x, 715, label, subtitle, fill, 465, 140)
        elif name == "subtract":
            cols = ((420, "RELATED CANDIDATES", sorted(RELATED)),
                    (960, "ALREADY CITED", sorted(REFERENCES)),
                    (1500, "UNCITED CANDIDATES", uncited(RELATED, REFERENCES)))
            for x, title, records in cols:
                rect(c, x-220, 305, 440, 405, "panel", 28)
                text(c, title, x, 358, 27, "pink", True, max_width=410)
                for i, ident in enumerate(records):
                    record(c, ident, x-75+150*(i%2), 458+155*(i//2), t, "mint" if ident in "BD" else "blue", .7)
            text(c, "−", 690, 540, 78, "pink", True)
            text(c, "=", 1230, 540, 68, "pink", True)
            text(c, "Schematic sets · no measured papers or relevance scores", 960, 785, 29, "muted")
        elif name == "menu":
            rect(c, 235, 280, 680, 495, "panel", 28)
            text(c, "ACTUAL TRACE", 575, 342, 32, "mint", True)
            for i, label in enumerate(("1 · Search source A", "2 · Inspect candidates", "3 · Reformulate query", "4 · Stop: budget reached")):
                text(c, label, 320, 425+i*85, 30, "white", align="left", max_width=555)
                circle(c, 277, 415+i*85, 8, "mint", .65)
            rect(c, 1030, 280, 650, 495, "panel2", 28)
            text(c, "AVAILABLE MENU?", 1355, 342, 32, "pink", True)
            for i, label in enumerate(("Other databases?", "Extract references?", "Read full text?", "Compare record identities?")):
                box(c, 1355, 410+i*94, label, fill="muted", width=560, height=73)
            text(c, "?", 972, 552, 70, "yellow", True)
        elif name in ("miss", "recover"):
            recovery = name == "recover"
            planet(c, 510, 520, t, "CITATION", "blue", 155)
            text(c, "DIFFERENCES", 510, 565, 26, "ink", True)
            show = recovery and t >= self.at(name, "suppose", 7)
            planet(c, 1390, 520, t, "METHODS", "mint" if show else "panel2", 155)
            text(c, "SELECTION BIAS", 1390, 730, 29, "mint" if show else "muted", True)
            for i in range(3):
                a = i*math.tau/3+t*.15
                record(c, chr(65+i), 510+math.cos(a)*215, 520+math.sin(a)*165, t, "blue", .45)
            if recovery:
                flow(c, 775, 520, 1130, 520, t, "mint" if show else "yellow")
                box(c, 960, 313, "INVESTIGATE THE GAP", "alternative round 2", "mint", 520, 120)
                if show:
                    record(c, "M", 1390, 290, t, "mint", .7)
            else:
                for i in range(3):
                    chip(c, f"ROUND {i+1}", 365+i*160, 290, 145, "blue", 23, 56)
                line(c, [(740, 385), (830, 440), (830, 640), (700, 700)], "blue", 5)
                arrow(c, 710, 704, 665, 675, "blue", 5)
                text(c, "Early evidence can keep steering later actions", 960, 812, 29, "muted")
            text(c, "HYPOTHETICAL TRAJECTORY", 960, 245, 23, "muted", True)
        elif name == "stop":
            for i, (label, detail, fill) in enumerate((("HARNESS LIMIT", "rounds / budget", "yellow"),
                      ("USER INTERRUPTS", "external control", "blue"), ("MODEL STOPS", "evidence judged sufficient", "pink"))):
                x = 400+i*560
                circle(c, x, 485, 110, fill, .2)
                circle(c, x, 485, 110, fill, .8, 8)
                if i == 0:
                    line(c, [(x, 485), (x, 415), (x+55, 485)], fill, 9)
                elif i == 1:
                    rect(c, x-38, 430, 26, 110, fill, 5)
                    rect(c, x+12, 430, 26, 110, fill, 5)
                else:
                    text(c, "?", x, 518, 105, fill, True)
                box(c, x, 706, label, detail, fill, 485, 145)
            text(c, "Record the reason. Coverage still needs evidence.", 960, 299, 37, "white", True)
        elif name == "trade":
            for x, title, fill in ((530, "FIXED / ADAPTIVE", "blue"), (1390, "AGENTIC", "pink")):
                rect(c, x-350, 290, 700, 470, "panel", 30)
                text(c, title, x, 355, 39, fill, True)
                clock = 45 if x == 530 else 85
                circle(c, x-170, 485, clock, fill, .8, 8)
                angle = t*(.8 if x == 530 else .4)
                line(c, [(x-170, 485), (x-170+math.cos(angle)*clock*.65, 485+math.sin(angle)*clock*.65)], fill, 7)
                for i in range(2 if x == 530 else 5):
                    circle(c, x+105+i*15, 515-i*15, 37, "yellow", .7)
                wrap(c, "Known procedures; record inputs and branches" if x == 530 else "Flexible trajectory; keep the actual run trace", x, 645, 610, 32, "white")
            text(c, "Qualitative trade-off · no measured cost or timing values", 960, 807, 27, "muted")
        elif name == "mcp":
            route(c, ("CONTROLLER", "MCP DESCRIPTION", "SEARCH SERVICE"), 440, t, "blue")
            ship(c, 280, 305, t, .34)
            box(c, 960, 675, "INPUTS / OUTPUTS", "callable operations", "mint", 465)
            planet(c, 1640, 680, t, "INDEX", "blue", 86)
            flow(c, 1640, 517, 1640, 572, t, "blue")
            rect(c, 335, 630, 250, 110, "panel2", 23)
            rect(c, 368, 667, 46, 38, "yellow", 8)
            circle(c, 391, 659, 16, "yellow", 1, 6)
            text(c, "ACCESS", 490, 683, 25, "yellow", True)

    def recovery(self, c, name, t, p):
        if name in ("empty", "autism", "synonyms"):
            ship(c, 400, 510, t, .85, "yellow")
            label = "USER REQUEST" if name == "empty" else "DATABASE FOR AUTISM"
            box(c, 1000, 340, label, fill="yellow", width=600, height=110)
            planet(c, 1530, 545, t, "INDEX", "blue", 118)
            flow(c, 600, 515, 1320, 515, t, "yellow")
            box(c, 1000, 707, "0 RESULTS", "observe the failure", "coral", 500, 125)
            if name == "empty":
                text(c, "END?", 960, 540, 53, "coral", True)
            elif name == "autism":
                text(c, "Subject need ≠ database name", 970, 574, 34, "white", True)
                text(c, "REPORTED JUNE 2026 DEMONSTRATION", 960, 252, 23, "muted", True)
            else:
                variants = (("autism", 790, 448), ("autistic disorder", 1150, 448),
                            ("ASD", 750, 550), ("autism spectrum", 1120, 550))
                for label, x, y in variants:
                    chip(c, label, x, y, 300 if len(label)>8 else 200, "pink", 25, 56)
                text(c, "4 of the 6 reported variants shown", 1000, 623, 24, "muted")
        elif name == "broaden":
            chip(c, "AUTISM", 960, 280, 330, "yellow", 36)
            for i, label in enumerate(("Psychology", "Medicine", "Education", "Disability")):
                x = 330+i*420
                flow(c, 960, 335, x, 408, t, "yellow")
                box(c, x, 480, label, fill="yellow", width=330, height=105)
            found = t >= self.at(name, "reports", 7)
            if found:
                for i, label in enumerate(("PsycINFO", "Education Research Complete", "SocINDEX")):
                    box(c, 420+i*540, 690, label, fill="mint", width=475, height=110)
            else:
                text(c, "CHANGE THE CONCEPTUAL LEVEL", 960, 704, 40, "yellow", True)
            text(c, "Reported historical example · current local access must be checked", 960, 802, 26, "muted")
        elif name == "same":
            planet(c, 960, 500, t, "SAME INDEX", "blue", 145)
            box(c, 395, 345, "ONE SHOT", "rewrite → retrieve", "pink", 460, 125)
            box(c, 395, 700, "LOOP", "observe → revise → retry", "mint", 460, 125)
            flow(c, 650, 345, 790, 425, t, "pink")
            flow(c, 650, 700, 790, 580, t, "mint")
            box(c, 1490, 345, "HOLDINGS CSV", "different input arrangement", "yellow", 500, 125)
            box(c, 1490, 700, "SMALLER MODEL", "selected comparisons", "yellow", 500, 125)
            text(c, "Useful retries can be fixed, adaptive, or agentic", 960, 800, 32, "muted")
        elif name == "limits":
            for i, (title, label, fill) in enumerate((("SELECTED", "examples, not a sample", "yellow"),
                       ("2023 → 2026", "older queries, newer models", "blue"), ("EXPLORATORY", "no measured success rate", "pink"))):
                x = 405+i*555
                orbit(c, x, 450, 120, t, fill)
                text(c, "!", x, 480, 105, fill, True)
                box(c, x, 682, title, label, fill, 480, 145)
            text(c, "Comparisons do not isolate a single cause", 960, 270, 40, "white", True)
        elif name == "library":
            rect(c, 660, 285, 600, 475, "panel", 35)
            polygon(c, [(660, 357), (960, 235), (1260, 357)], "yellow")
            for x in (735, 855, 975, 1095):
                rect(c, x, 385, 78, 295, "blue", 14)
            rect(c, 640, 712, 640, 40, "yellow", 10)
            ship(c, 960, 492, t, .7)
            for x, y, label in ((350, 355, "Current holdings"), (350, 590, "Entitlements"),
                               (1570, 355, "Coverage / embargoes"), (1570, 590, "Local field quirks")):
                box(c, x, y, label, fill="mint", width=470, height=120)
            text(c, "MAINTAIN THE LOCAL MAP", 960, 809, 37, "yellow", True)
        elif name == "audit":
            rect(c, 635, 285, 1050, 475, "panel", 32)
            for i, label in enumerate(("Which tools were available?", "Which actions actually ran?", "What evidence may still be missing?", "Why did the run stop?")):
                circle(c, 697, 369+i*105, 17, "yellow")
                text(c, str(i+1), 697, 378+i*105, 25, "ink", True)
                text(c, label, 745, 380+i*105, 33, "white", align="left", max_width=900)
            ship(c, 360, 490, t, .82, "yellow")
            text(c, "Test recovery on your own library tasks", 960, 812, 34, "mint", True)
