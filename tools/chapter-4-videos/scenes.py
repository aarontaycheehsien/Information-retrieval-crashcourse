"""Original geometric animation for Chapter 4, using the shared drawing primitives."""
from __future__ import annotations

import math
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "chapter-2-videos"))
from visuals import (  # noqa: E402
    Film as BaseFilm, W, color, text, circle, rect, line, polygon, arrow, flow,
    chip, check, robot, paper, gate, docbubble, clamp, pop, smooth,
)

TERMS = ("apple", "orange", "banana")
RECORDS = {"A": ("apple", "orange", "banana"), "B": ("apple", "orange"),
           "C": ("apple",), "D": ("pear", "grape")}
COLORS = {"apple": "mint", "orange": "coral", "banana": "yellow",
          "pear": "blue", "grape": "pink"}
LAB = {"A": "Delulu expectations during a job interview",
       "F": "Why foolish job applicants misread the interview"}


def admitted(minimum):
    return {key for key, values in RECORDS.items() if len(set(values) & set(TERMS)) >= minimum}


def validate_examples(chapter):
    """Guard the examples that carry the films' teaching claims."""
    assert admitted(3) == {"A"}
    assert admitted(2) == {"A", "B"}
    assert admitted(1) == {"A", "B", "C"}
    assert set(("B", "A", "C")[:2]) == {"B", "A"}
    for ident, words in RECORDS.items():
        assert f"{ident} {' '.join(words)}" in chapter, f"Source record changed: {ident}"
    for value in LAB.values():
        assert value in chapter, f"Source lab record changed: {value}"
    query = {"delulu", "job", "interview", "expectations", "foolish"}
    tokens = {k: set(v.lower().split()) for k, v in LAB.items()}
    assert not any(query <= values for values in tokens.values())
    assert all(query & values for values in tokens.values())
    assert "foolish" not in tokens["A"] and "foolish" in tokens["F"]


def fruit(c, term, x, y, scale=1, t=0):
    """Small original fruit symbols: metaphor for indexed terms, not relevance."""
    c.save()
    c.translate(x, y + math.sin(t*1.8+x*.01)*5)
    c.scale(scale, scale)
    if term == "banana":
        polygon(c, [(-52,-22), (-34,13), (0,29), (39,11), (53,-34), (35,-12),
                    (9,1), (-15,-3), (-39,-28)], "yellow")
    elif term == "grape":
        for dx, dy in ((-18,-17),(18,-17),(0,10),(-13,36),(13,36),(0,60)):
            circle(c, dx, dy, 21, "pink")
    else:
        circle(c, -14, 8, 33, COLORS[term])
        circle(c, 17, 8, 33, COLORS[term])
        rect(c, -33, 3, 67, 49, COLORS[term], 26)
        if term == "orange":
            circle(c, 0, 7, 43, "coral")
        line(c, [(0,-26),(7,-52)], "muted", 7)
        polygon(c, [(7,-41),(31,-54),(35,-36),(17,-31)], "mint")
    circle(c, -14, 2, 4, "ink")
    circle(c, 14, 2, 4, "ink")
    line(c, [(-8,17),(0,22),(9,17)], "ink", 3)
    c.restore()


def term_query(c, terms, y, t, width=265):
    gap = width+34
    start = 960-(len(terms)-1)*gap/2
    for i, term in enumerate(terms):
        chip(c, term, start+i*gap, y, width, COLORS.get(term, "coral" if term == "foolish" else "mint"), 36)


def fruit_cards(c, t, minimum=None):
    for i, (ident, terms) in enumerate(RECORDS.items()):
        x = 310+i*435
        rise = (1-pop((t-i*.1)/.9))*45
        c.save()
        c.translate(0, rise)
        rect(c, x-181, 348, 362, 370, "panel", 40)
        docbubble(c, ident, x, 366, "blue", 41)
        for row, term in enumerate(terms):
            yy = 453+row*83
            fruit(c, term, x-114, yy, .42, t)
            chip(c, term, x+23, yy, 229, COLORS[term], 32, 58)
        if minimum is not None:
            yes = ident in admitted(minimum)
            check(c, x, 741, yes, 23)
            text(c, "ADMITTED" if yes else "EXCLUDED", x, 809, 26, "mint" if yes else "coral", True)
        else:
            text(c, f"{len(set(terms)&set(TERMS))} query matches", x, 783, 29, "muted")
        c.restore()


def lab_card(c, ident, x, y, t, scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    rect(c, -320, -178, 640, 356, "panel", 35)
    paper(c, -235, -10, ident, [], t, .43)
    if ident == "A":
        words = [("delulu", "expectations"), ("during a job", "interview")]
        title = "Delulu expectations during a job interview"
    else:
        words = [("foolish", "job"), ("applicants", "interview")]
        title = "Why foolish job applicants misread the interview"
    text(c, "RECORD " + ident, 47, -126, 26, "muted", True)
    for row, pair in enumerate(words):
        for col, word in enumerate(pair):
            chip(c, word, -54+col*197, -46+row*84, 181, "coral" if word == "foolish" else "mint", 25, 60)
    text(c, title, 0, 150, 23, "white", max_width=590)
    c.restore()


def magnet(c, x, y, t, scale=1):
    c.save()
    c.translate(x, y)
    c.rotate(math.sin(t*.8)*5)
    c.scale(scale, scale)
    rect(c, -80, -62, 160, 177, "coral", 69)
    rect(c, -39, -83, 78, 142, "bg", 36)
    rect(c, -80, -74, 42, 49, "white", 7)
    rect(c, 38, -74, 42, 49, "white", 7)
    text(c, "+", -59, -37, 25, "ink", True)
    text(c, "−", 59, -37, 25, "ink", True)
    for i in range(4):
        radius = 110+((t*24+i*31) % 125)
        circle(c, 0, -35, radius, "coral", .2, 3)
    c.restore()


def process_box(c, x, y, heading, sub, fill, width=360):
    rect(c, x-width/2, y-70, width, 140, "panel2", 26)
    text(c, heading, x, y-6, 33, fill, True, max_width=width-25)
    text(c, sub, x, y+41, 26, "muted", max_width=width-25)


class Film(BaseFilm):
    def __init__(self, episode, timeline):
        # Own the chapter frame so this does not depend on changes in other tasks.
        self.episode, self.timeline = episode, timeline
        self.number = int(episode["id"][:2])
        self.accent = episode["accent"]
        self.stars = np.random.default_rng(44).uniform([30, 240, 1], [1890, 820, 3], (54, 3))

    def draw(self, c, t):
        c.clear(color("bg"))
        circle(c, -60, 610, 375, "panel", .3)
        circle(c, 1950, 300, 360, "panel", .35)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+8*math.sin(t*.1+i), y+5*math.cos(t*.13+i), r, "muted", .45)
        name = next((s for s, (a,b) in self.timeline["scenes"].items() if a <= t < b), self.episode["scenes"][-1]["id"])
        scene = next(s for s in self.episode["scenes"] if s["id"] == name)
        a,b = self.timeline["scenes"][name]
        u = t-a
        text(c, f"CHAPTER 4   /   FILM {self.number:02d}", 105, 79, 25, self.accent, True, "left")
        text(c, self.episode["subtitle"], 1815, 79, 25, "muted", align="right")
        text(c, scene["title"], 960, 173+(1-pop(u/.7))*35, 65, "white", True, max_width=1700)
        c.save()
        c.translate(0, (1-pop(u/.7))*45)
        (self.doors, self.trouble, self.histories)[self.number-1](c, name, u)
        c.restore()
        rect(c, 230, 849, 1460, 70, "panel", 35)
        text(c, scene["claim"], 960, 898, 34, self.accent, True, max_width=1390)
        text(c, "Adapted from Chapter 4 · Aaron Tay", 105, 945, 20, "muted", align="left")
        for i,s in enumerate(self.episode["scenes"]):
            circle(c, 1652+i*22, 937, 5, self.accent if s["id"] == name else "panel2")
        if b-t < .3 and scene != self.episode["scenes"][-1]:
            q = smooth((.3-(b-t))/.3)
            rect(c, W-W*q, 230, W*q, 590, self.accent, 0)

    def doors(self, c, name, t):
        if name == "surprise":
            term_query(c, TERMS, 303, t)
            paper(c, 595, 579, "B", ["apple", "orange"], t, .88)
            robot(c, 1355, 556, t, 1.05)
            chip(c, "banana?", 1560, 317, 330, "yellow", 45)
            flow(c, 844, 565, 1075, 565, t, "yellow")
            text(c, "Two matches. Still lexical?", 960, 801, 43, "mint", True)
        elif name in ("cards", "all", "some", "any"):
            if name == "cards":
                term_query(c, TERMS, 278, t, 230)
            else:
                minimum = {"all":3,"some":2,"any":1}[name]
                chip(c, {3:"Require all three",2:"Require at least two",1:"Require any one"}[minimum], 960, 278, 685, "mint", 41)
            fruit_cards(c, t, None if name == "cards" else minimum)
        elif name in ("rank", "boundary"):
            text(c, "ANY-MATCH CANDIDATES", 495, 298, 33, "mint", True)
            for i, ident in enumerate(("A","B","C")):
                paper(c, 270+i*215, 529, ident, [], t, .48)
            text(c, "D never qualified", 480, 749, 31, "muted")
            flow(c, 850, 527, 1020, 527, t, "yellow")
            text(c, "STIPULATED ORDER", 1450, 298, 33, "yellow", True)
            for i, ident in enumerate(("B","A","C")):
                y = 420+i*138
                inside = name == "rank" or i < 2
                rect(c, 1110, y-48, 615, 97, "panel" if inside else "panel2", 25)
                text(c, str(i+1), 1165, y+14, 35, "muted", True)
                docbubble(c, ident, 1265, y, "yellow" if inside else "muted", 33)
                text(c, "competes" if name == "rank" else "retained" if inside else "below boundary", 1485, y+13, 30, "white" if inside else "muted")
            if name == "boundary":
                line(c, [(1100,624),(1740,624)], "coral", 6)
                chip(c, "TOP 2", 1740, 624, 170, "coral", 29, 63)
            text(c, "Illustration, not calculated BM25 scores", 1410, 791, 27, "muted")
        elif name == "controls":
            for i,(title,sub,fill) in enumerate((("ADMISSION","Who may compete?","mint"),("RANKING","How are they ordered?","yellow"),("OUTPUT","How many are kept?","coral"))):
                x = 420+i*540
                rect(c, x-218, 325, 436, 417, "panel", 40)
                text(c, title, x, 388, 35, fill, True)
                if i == 0:
                    gate(c, x, 561, t, True, "ANY", .47)
                elif i == 1:
                    for j,h in enumerate((72,150,111)):
                        rect(c, x-113+j*83, 652-h, 60, h*pop(t/1.6), fill, 10)
                else:
                    circle(c, x, 556, 95, fill)
                    text(c, "k", x, 586, 97, "ink", True)
                text(c, sub, x, 703, 28, "white", max_width=400)
            text(c, "Same terms. Same index. Different controls.", 960, 807, 35, "mint", True)

    def trouble(self, c, name, t):
        if name == "weak":
            term_query(c, ["delulu","job","interview","expectations"], 311, t, 300)
            robot(c, 560, 578, t, 1.0)
            shift = pop((t-self.spoken_at(name,"add",3))/.9)
            chip(c, "foolish", 1500-shift*230, 558, 460, "coral", 65, 123)
            magnet(c, 1270, 719, t, .39)
            text(c, "A weak synonym joins the team", 960, 806, 35, "muted")
        elif name == "records":
            lab_card(c, "A", 490, 515, t, 1.03)
            lab_card(c, "F", 1430, 515, t, 1.03)
            chip(c, "No foolish", 490, 764, 380, "blue", 36)
            chip(c, "No delulu or expectations", 1430, 764, 620, "coral", 33)
        elif name == "closed":
            for i, ident in enumerate(("A","F")):
                x = 400+i*1100
                paper(c, x, 516, ident, [], t, .8)
                check(c, x, 733, False, 29)
                text(c, "Missing foolish" if ident == "A" else "Missing other required terms", x, 811, 31, "coral", max_width=740)
            gate(c, 960, 536, t, False, "ALL FIVE", .85)
            text(c, "No candidate → no downstream rescue", 960, 301, 36, "coral", True)
        elif name == "survive":
            lab_card(c, "A", 442, 529, t, .84)
            lab_card(c, "F", 1480, 529, t, .84)
            gate(c, 960, 520, t, True, "ANY", .63)
            for x in (442,1480):
                check(c, x, 746, True, 28)
            text(c, "Existing evidence survives", 442, 318, 32, "mint")
            text(c, "Another contribution", 1480, 318, 32, "coral")
        elif name == "rare":
            chip(c, "foolish", 410, 299, 390, "coral", 50)
            for i in range(6):
                x = 235+(i%3)*190
                y = 457+(i//3)*174
                rect(c, x-40, y-57, 80, 108, "coral" if i == 5 else "panel2", 17)
                text(c, chr(65+i), x, y+12, 33, "ink" if i == 5 else "muted", True)
                if i == 5:
                    circle(c, x, y-87, 8+3*math.sin(t*2), "yellow")
            text(c, "Only F in the lab collection", 425, 802, 30, "muted")
            flow(c, 840, 533, 1020, 533, t, "coral")
            magnet(c, 1280, 514, t, .95)
            paper(c, 1630-40*math.sin(t*.6), 534, "F", ["foolish"], t, .62)
            text(c, "Extra weight ≠ better answer", 1370, 779, 36, "coral", True, max_width=880)
            text(c, "Diagram of influence; no numerical order asserted", 1280, 821, 25, "muted")
        elif name == "saturation":
            x,y,w,h = 320,690,1270,330
            line(c, [(x,y-h),(x,y),(x+w,y)], "muted", 4)
            points=[]
            for i in range(121):
                n = 20*i/120*pop(t/2)
                factor = n*2.2/(n+1.2)
                points.append((x+n/20*w,y-factor/2.2*h))
            line(c, points, "coral", 9)
            text(c, "Repeated occurrences in one document", 960, 778, 34, "muted")
            text(c, "TF factor", 320, 306, 31, "muted", align="left")
            for n in (0,1,5,10,20):
                text(c, str(n),x+n/20*w,y+43,25,"muted")
            for factor in (0,1,2):
                yy=y-factor/2.2*h
                text(c,str(factor),x-25,yy+9,25,"muted",align="right")
            chip(c, "foolish is still a weak choice", 1170, 279, 720, "yellow", 38, 68)
            text(c, "Average length · k₁ = 1.2 · illustrative factor, not a score", 960, 824, 28, "muted")
        elif name == "remedy":
            term_query(c, ["delulu","job","interview","expectations","foolish"], 352, t, 270)
            x = 960+2*(270+34)
            if t >= self.spoken_at(name,"remove",7):
                line(c, [(x-116,319),(x+116,386)], "white", 7)
            robot(c, 426, 617, t, .83)
            for i,(title,sub,fill) in enumerate((("Required term","Can alter admission","coral"),("Optional term","Can alter scores and candidates","yellow"))):
                process_box(c, 1100, 524+i*192, title, sub, fill, 905)
            text(c, "Test how the term represents your need", 440, 795, 28, "mint", max_width=670)
        elif name == "recap":
            rect(c, 185, 309, 715, 450, "panel", 40)
            rect(c, 1020, 309, 715, 450, "panel", 40)
            text(c, "ALL-TERM AND", 543, 374, 36, "coral", True)
            text(c, "ANY-MATCH BM25", 1377, 374, 36, "yellow", True)
            gate(c, 543, 555, t, False, "foolish", .53)
            magnet(c, 1377, 544, t, .72)
            text(c, "Can exclude useful records", 543, 712, 33, "white", max_width=650)
            text(c, "Can distort the competition", 1377, 712, 33, "white", max_width=650)
            text(c, "The query can fail while the mechanism follows its rules", 960, 811, 34, "muted")

    def histories(self, c, name, t):
        if name == "mystery":
            robot(c, 960, 528, t, 1.10)
            for i,(label,fill) in enumerate((("REMOVED","mint"),("REWRITTEN","pink"),("OPTIONAL","blue"),("OUT OF VIEW","yellow"))):
                x = (430,1490,430,1490)[i]
                y = (357,357,708,708)[i]
                chip(c,label,x,y,470,fill,37,94)
                flow(c, x+(260 if x<960 else -260),y,960+(-170 if x<960 else 170),528,t,fill)
            text(c,"Several histories can coexist",960,815,33,"muted")
        elif name in ("analysis","rewrite"):
            before = ["the","job","interview"] if name == "analysis" else ["delulu","job","expectations"]
            after = ["job","interview"] if name == "analysis" else ["unrealistic","job","expectations"]
            term_query(c, before, 316, t, 350)
            process_box(c,960,500,"ANALYSIS" if name == "analysis" else "TRANSFORMATION",
                        "Illustrative stop-word handling" if name == "analysis" else "Illustrative vocabulary mapping",
                        "mint" if name == "analysis" else "pink",850)
            flow(c,960,363,960,407,t,"yellow")
            flow(c,960,586,960,642,t,"yellow")
            term_query(c,after,714,t,350)
            text(c,"Retrieval receives these terms",960,813,33,"muted")
        elif name == "optional":
            term_query(c,["delulu","job","interview"],300,t,350)
            paper(c,445,556,"X",["job","interview"],t,.82)
            gate(c,960,551,t,True,"ANY",.73)
            check(c,1490,532,True,47)
            text(c,"Candidate admitted",1490,656,39,"mint",True)
            text(c,"Optional delulu may have no posting list",960,812,35,"muted")
        elif name == "hidden":
            rect(c,200,313,1030,415,"panel",38)
            text(c,"VISIBLE TITLE",270,367,25,"muted",True,"left")
            text(c,"Job interview expectations",715,460,52,"white",True,max_width=900)
            line(c,[(257,505),(1172,505)],"muted",3,.5)
            text(c,"INDEXED ABSTRACT",270,563,25,"yellow",True,"left")
            text(c,"We examine delulu expectations.",715,649,47,"yellow",True,max_width=905)
            robot(c,1532,501,t,.88,"blue")
            flow(c,1254,618,1450,618,t,"yellow")
            text(c,"Matched, but absent from the snippet",960,813,37,"yellow",True)
        elif name == "jobs":
            labels=[("ANALYSIS","Prepare strings","mint"),("EXECUTION","Set clause requirements","blue"),
                    ("UNDERSTANDING","Interpret the request","yellow"),("TRANSFORMATION","Change retrieval input","pink")]
            for i,(title,sub,fill) in enumerate(labels):
                x=525+(i%2)*870
                y=414+(i//2)*284
                process_box(c,x,y,title,sub,fill,720)
                chip(c,str(i+1),x-317,y-67,70,fill,32,70)
            text(c,"Interpretation need not change any query word",960,817,34,"muted")
        elif name == "pipeline":
            stages=[("User question","Natural language","white"),("Understanding","Interpret request","yellow"),
                    ("Transformation","Build Boolean query","pink")]
            for i,(title,sub,fill) in enumerate(stages):
                x=400+i*560
                process_box(c,x,383,title,sub,fill,440)
                if i<2:
                    flow(c,x+235,383,x+325,383,t,"yellow")
            stages=[("Results","Present output","coral"),("Lexical retrieval","Boolean / BM25","mint"),
                    ("Analysis + rules","Process and execute","blue")]
            for i,(title,sub,fill) in enumerate(stages):
                x=400+i*560
                process_box(c,x,680,title,sub,fill,440)
                if i>0:
                    flow(c,x-235,680,x-325,680,t,"mint")
            flow(c,1520,475,1520,583,t,"blue")
            text(c,"A possible pipeline, not a mandatory sequence",960,816,31,"muted")
        elif name == "verdict":
            for i,(label,fill) in enumerate((("Processed query","pink"),("Admission rules","mint"),("Indexed fields","yellow"))):
                chip(c,label,410+i*550,316,470,fill,35,88)
            process_box(c,535,583,"CHANGE THE QUERY","Keep lexical matching; map or expand terms","pink",740)
            process_box(c,1385,583,"CHANGE THE REPRESENTATION","Retrieve by proximity in a learnt space","blue",740)
            robot(c,960,437,t,.35)
            text(c,"Part II asks how representations connect vocabulary",960,819,34,"yellow",True)
