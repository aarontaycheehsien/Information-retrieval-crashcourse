"""Original motion graphics for Chapter 7, with calculated teaching examples."""
from __future__ import annotations

import math
import numpy as np
import skia

from visuals import (Film as BaseFilm, W, H, arrow, chip, circle, clamp, color,
                     flow, font, line, paint, paper, polygon, pop, rect, robot,
                     smooth, text)

QUERY = (1.0, 0.0)
CANDIDATES = {"A": (.9, .3), "B": (1.0, 1.0)}
POINTS = {"A": (1, 0), "B": (0, 2), "C": (2, 2),
          "D": (1, 3), "E": (3, 4), "F": (5, 1)}
EXAMINED = ("A", "B", "D", "F")


def dot(a, b):
    return sum(x*y for x, y in zip(a, b))


def unit(a):
    length = math.sqrt(dot(a, a))
    if not length:
        raise ValueError("A zero vector has no cosine direction")
    return tuple(x/length for x in a)


def cosine(a, b):
    return dot(unit(a), unit(b))


def nearest(ids, k=3):
    return sorted(ids, key=lambda key: math.hypot(*POINTS[key]))[:k]


def validate_examples():
    assert cosine(QUERY, CANDIDATES["A"]) > cosine(QUERY, CANDIDATES["B"])
    assert dot(QUERY, CANDIDATES["A"]) < dot(QUERY, CANDIDATES["B"])
    for v in CANDIDATES.values():
        assert math.isclose(dot(unit(QUERY), unit(v)), cosine(QUERY, v))
    assert [cosine(QUERY, v) for v in ((2, 0), (0, 2), (-2, 0))] == [1, 0, -1]
    assert math.isclose(cosine(QUERY, (.9, .3)), cosine(QUERY, (1.8, .6)))
    assert nearest(POINTS) == ["A", "B", "C"]
    assert nearest(EXAMINED) == ["A", "B", "D"]
    assert math.hypot(*POINTS["C"]) < math.hypot(*POINTS["D"])
    assert all(math.isclose(math.hypot(*POINTS[key]), expected) for key, expected
               in zip(POINTS, (1, 2, math.sqrt(8), math.sqrt(10), 5, math.sqrt(26))))
    assert len(EXAMINED) == 4 and len(POINTS) == 6


def wrap(c, value, x, y, size=32, fill="white", bold=False, width=540):
    rows, current = [], ""
    for word in value.split():
        candidate = (current+" "+word).strip()
        if current and font(size, bold).measureText(candidate) > width:
            rows.append(current)
            current = word
        else:
            current = candidate
    if current:
        rows.append(current)
    for i, row in enumerate(rows):
        text(c, row, x, y+i*size*1.25, size, fill, bold)


def card(c, x, y, title, subtitle="", fill="mint", width=480, height=180):
    rect(c, x-width/2, y-height/2, width, height, "panel", 30)
    rect(c, x-width/2, y-height/2, 10, height, fill, 5)
    wrap(c, title, x, y-14 if subtitle else y+8, 33, fill, True, width-50)
    if subtitle:
        wrap(c, subtitle, x, y+height/2-28, 25, "muted", False, width-50)


def orbit(c, x, y, r, t, fill="mint", count=8):
    circle(c, x, y, r, fill, .13, 3)
    for i in range(count):
        a = t*.17+i*math.tau/count
        circle(c, x+math.cos(a)*r, y+math.sin(a)*r, 6, fill, .5)


def bars(c, x, y, values, fill="mint", size=52):
    for i, value in enumerate(values):
        xx = x+i*(size+10)
        rect(c, xx, y, size, size, "panel2", 10)
        rect(c, xx+5, y+size-5-(size-10)*abs(value), size-10,
             (size-10)*abs(value), fill, 5)


def vector_plot(c, x, y, scale=220, normalised=False, stretch=1, label=True):
    line(c, [(x-70, y), (x+scale*1.4, y)], "muted", 3, .3)
    line(c, [(x, y+55), (x, y-scale*1.4)], "muted", 3, .3)
    circle(c, x, y, 7, "white")
    for key, v in CANDIDATES.items():
        vv = unit(v) if normalised else v
        if key == "B" and not normalised:
            vv = tuple(a*stretch for a in vv)
        xx, yy = x+vv[0]*scale, y-vv[1]*scale
        arrow(c, x, y, xx, yy, "mint" if key == "A" else "coral", 9)
        if label:
            text(c, key, xx+23, yy-9, 36, "mint" if key == "A" else "coral", True)
    arrow(c, x, y, x+scale, y, "yellow", 9)
    text(c, "Q", x+scale+32, y+15, 35, "yellow", True)


def nearest_plot(c, x, y, title, selected, t, fill, animate=True):
    """Chapter distances, rotated toy positions; Euclidean distance from Q=(0,0)."""
    width = 735
    rect(c, x, y, width, 500, "panel", 30)
    text(c, title, x+width/2, y+47, 31, fill, True)
    origin_x, origin_y, scale = x+110, y+378, 67
    for i in range(6):
        line(c, [(origin_x+i*scale, origin_y), (origin_x+i*scale, origin_y-5*scale)], "muted", 1, .13)
        line(c, [(origin_x, origin_y-i*scale), (origin_x+5*scale, origin_y-i*scale)], "muted", 1, .13)
        text(c, str(i), origin_x+i*scale, origin_y+34, 20, "muted")
        if i:
            text(c, str(i), origin_x-33, origin_y-i*scale+8, 20, "muted")
    circle(c, origin_x, origin_y, 12, "yellow")
    text(c, "Q", origin_x-32, origin_y+8, 28, "yellow", True)
    count = len(selected) if not animate else min(len(selected), int(t/1.15)+1)
    visited = set(selected[:count])
    returned = nearest(selected) if count == len(selected) else []
    for key, (xx, yy) in POINTS.items():
        px, py = origin_x+xx*scale, origin_y-yy*scale
        circle(c, px, py, 13, fill, 1 if key in visited else .55, 0 if key in visited else 3)
        if key in returned:
            circle(c, px, py, 23, "yellow", .95, 3)
        text(c, key, px+24, py+9, 27, fill if key in visited else "muted", True)
        if key == "C" and key not in selected:
            text(c, "missed", px+27, py+35, 21, "coral", True)
    result = ", ".join(nearest(selected))
    text(c, f"{len(selected)} examined → {result}", x+width/2, y+465, 29, fill, True)


class Film(BaseFilm):
    def __init__(self, episode, timeline):
        self.episode, self.timeline = episode, timeline
        self.number, self.accent = int(episode["id"][:2]), episode["accent"]
        self.stars = np.random.default_rng(77).uniform([50, 250, 1], [1870, 820, 3], (55, 3))

    def draw(self, c, t):
        c.clear(color("bg"))
        circle(c, -80, 520, 370, "panel", .36)
        circle(c, 1955, 380, 345, "panel", .42)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+5*math.sin(t*.12+i), y+4*math.cos(t*.1+i), r, "muted", .42)
        name = next((key for key, (a, b) in self.timeline["scenes"].items() if a <= t < b), self.episode["scenes"][-1]["id"])
        scene = next(s for s in self.episode["scenes"] if s["id"] == name)
        a, b = self.timeline["scenes"][name]
        local, p = t-a, clamp((t-a)/(b-a))
        text(c, f"CHAPTER 7   /   FILM {self.number:02d}", 105, 79, 25, self.accent, True, "left")
        text(c, self.episode["subtitle"], 1815, 79, 24, "muted", align="right", max_width=1230)
        text(c, scene["title"], 960, 174+(1-pop(local/.7))*30, 63, "white", True, max_width=1710)
        c.save()
        c.translate(0, (1-pop(local/.7))*40)
        (self.similarity, self.constellation, self.semantics)[self.number-1](c, name, local, p)
        c.restore()
        rect(c, 195, 849, 1530, 70, "panel", 35)
        text(c, scene["claim"], 960, 897, 33, self.accent, True, max_width=1450)
        text(c, "Adapted from Chapter 7 · Aaron Tay", 105, 945, 20, "muted", align="left")
        for i, s in enumerate(self.episode["scenes"]):
            circle(c, 1652+i*22, 937, 5, self.accent if s["id"] == name else "panel2")
        if b-t < .3 and scene != self.episode["scenes"][-1]:
            q = smooth((.3-(b-t))/.3)
            rect(c, W-W*q, 230, W*q, 590, self.accent, 0)

    def similarity(self, c, name, t, p):
        if name == "arrows":
            orbit(c, 575, 516, 207, t, "blue")
            robot(c, 575, 516, t, .9, "yellow")
            for i in range(6):
                a = i*math.tau/6+t*.08
                paper(c, 575+math.cos(a)*305, 516+math.sin(a)*213, str(i+1), [], t, .25, "blue")
            flow(c, 960, 510, 1100, 510, t)
            vector_plot(c, 1240, 668, 248)
            text(c, "Stored passage vectors", 575, 798, 34, "blue", True)
            text(c, "A new query joins the map", 1425, 798, 34, "mint", True)
        elif name == "direction":
            vector_plot(c, 515, 657, 260, stretch=1+.25*math.sin(t*.65))
            c.drawArc(skia.Rect.MakeLTRB(433, 575, 597, 739), -45, 45, False, paint("coral", .8, 4))
            c.drawArc(skia.Rect.MakeLTRB(468, 610, 562, 704), -18.435, 18.435, False, paint("mint", .9, 4))
            text(c, "Angle, not length", 655, 794, 39, "mint", True)
            card(c, 1370, 402, "A: cosine = "+f"{cosine(QUERY,CANDIDATES['A']):.3f}", "Smaller angle", "mint", 590)
            card(c, 1370, 650, "B: cosine = "+f"{cosine(QUERY,CANDIDATES['B']):.3f}", "Stretching B preserves this score", "coral", 590)
        elif name == "landmarks":
            for i, (label, endpoint, score, fill) in enumerate((("SAME", (180, 0), "1", "mint"), ("RIGHT ANGLE", (0, -180), "0", "blue"), ("OPPOSITE", (-180, 0), "−1", "coral"))):
                x, y = 425+i*535, 553
                circle(c, x, y, 205, fill, .1)
                arrow(c, x, y, x+165, y, "yellow", 7)
                arrow(c, x, y, x+endpoint[0], y+endpoint[1], fill, 10)
                circle(c, x, y, 8, "white")
                text(c, label, x, 293, 28, fill, True)
                text(c, score, x, 789, 68, fill, True)
        elif name == "multiply":
            chip(c, "Q = (1, 0)", 960, 301, 460, "yellow", 43)
            for i, (key, v) in enumerate(CANDIDATES.items()):
                x = 530+i*860
                rect(c, x-330, 401, 660, 342, "panel", 32)
                text(c, f"{key} = ({v[0]:g}, {v[1]:g})", x, 462, 39, "mint" if i == 0 else "coral", True)
                text(c, f"1 × {v[0]:g}  +  0 × {v[1]:g}", x, 557, 49, "white", True)
                text(c, f"= {dot(QUERY,v):g}", x, 673, 77, "mint" if i == 0 else "coral", True)
            text(c, "Matching coordinates are multiplied, then added", 960, 805, 32, "muted")
        elif name == "reversal":
            vector_plot(c, 357, 645, 245)
            text(c, "Toy vectors stay fixed", 520, 793, 30, "muted")
            for i, (title, metric, fill) in enumerate((("COSINE", cosine, "mint"), ("DOT PRODUCT", dot, "coral"))):
                x = 1030+i*520
                rect(c, x-225, 278, 450, 490, "panel", 30)
                text(c, title, x, 343, 33, fill, True)
                order = sorted(CANDIDATES, key=lambda key: metric(QUERY,CANDIDATES[key]), reverse=True)
                flip = pop((t-self.spoken_at(name,"flip",1))/1.2) if i else 1
                for j, key in enumerate(order):
                    initial_row = ("A","B").index(key)
                    row = initial_row+(j-initial_row)*flip
                    yy = 462+row*150
                    chip(c, key, x-90, yy, 100, "mint" if key == "A" else "coral", 40)
                    text(c, f"{metric(QUERY,CANDIDATES[key]):.3f}", x+70, yy+17, 45, "white", True)
                text(c, order[0]+" wins" if flip >= 1 else "Ranking changes...", x, 736, 29, fill, True)
        elif name == "normalise":
            vector_plot(c, 435, 645, 260, normalised=True)
            circle(c, 435, 645, 260, "blue", .2, 3)
            text(c, "Every arrow has length 1", 587, 797, 32, "blue", True)
            rect(c, 1010, 317, 670, 406, "panel", 32)
            text(c, "DOT PRODUCT = COSINE", 1345, 388, 36, "mint", True)
            for i, (key, v) in enumerate(CANDIDATES.items()):
                text(c, f"{key}   {dot(unit(QUERY),unit(v)):.3f} = {cosine(QUERY,v):.3f}", 1345, 497+i*106, 47, "mint" if key == "A" else "coral", True)
            text(c, "Match the model's training setup", 1345, 794, 34, "yellow", True)
        elif name == "dimensions":
            for i, (label, count, fill) in enumerate((("[x, y]", 2, "blue"), ("[x, y, z]", 3, "mint"), ("[x1, ... , xn]", 8, "pink"))):
                x = 410+i*550
                circle(c, x, 520, 157, fill, .13)
                for j in range(count):
                    a = -.2-j*.38
                    arrow(c, x-80, 580, x+math.cos(a)*115, 510+math.sin(a)*143, fill, 5)
                text(c, label, x, 746, 44, fill, True)
                if i < 2:
                    flow(c, x+197, 505, x+350, 505, t, fill)
            text(c, "Anonymous coordinates · Not a measured model projection", 960, 814, 30, "muted")
        elif name == "meaning":
            orbit(c, 595, 515, 205, t)
            text(c, "+0.95", 595, 551, 111, "mint", True)
            robot(c, 595, 735, t, .37, "yellow")
            card(c, 1360, 396, "Which model and rule?", "Scores belong to their representation", "blue", 700)
            card(c, 1360, 662, "Useful for this task?", "Relevance needs judgement and evaluation", "yellow", 700)
        else:
            raise ValueError(name)

    def constellation(self, c, name, t, p):
        if name == "warehouse":
            for row in range(3):
                for col in range(7):
                    xx, yy = 262+col*136, 337+row*150
                    rect(c, xx-55, yy-50, 112, 107, "panel2", 18)
                    paper(c, xx, yy, str(row*7+col+1), [], t+col, .21, "mint")
                line(c, [(176, 404+row*150), (1183, 404+row*150)], "blue", 8)
            robot(c, 1535, 489, t, .9, "yellow")
            chip(c, "QUERY", 1535, 724, 365, "yellow", 39)
            flow(c, 1411, 525, 1244, 525, t, "yellow")
            text(c, "Vectors prepared before the question", 700, 809, 36, "mint", True)
        elif name == "postings":
            rect(c, 180, 272, 730, 489, "panel", 30)
            rect(c, 1010, 272, 730, 489, "panel", 30)
            text(c, "LEXICAL", 545, 333, 35, "blue", True)
            chip(c, "job", 378, 485, 235, "blue", 43)
            flow(c, 512, 485, 602, 485, t, "blue")
            for i in range(3):
                chip(c, f"D{i+1}", 740, 397+i*90, 160, "blue", 29, 65)
            text(c, "Term → posting list", 545, 710, 32, "blue", True)
            text(c, "DENSE", 1375, 333, 35, "yellow", True)
            bars(c, 1110, 441, (.4,.8,.3,.6), "yellow", 57)
            flow(c, 1390, 470, 1495, 470, t, "yellow")
            for i in range(6):
                a = i*math.tau/6+t*.08
                circle(c, 1617+math.cos(a)*74, 477+math.sin(a)*115, 13, "mint")
            text(c, "Vector → neighbour search", 1375, 710, 32, "yellow", True)
            text(c, "No term-to-document pointer for an unnamed dense dimension", 960, 811, 30, "muted")
        elif name in ("exhaustive", "approximate"):
            nearest_plot(c, 160, 282, "EXHAUSTIVE", tuple(POINTS), t, "mint", name == "exhaustive")
            nearest_plot(c, 1025, 282, "ILLUSTRATIVE APPROXIMATE RUN", EXAMINED, t, "coral", name == "approximate")
            text(c, "Euclidean distance from Q = (0, 0) · Rings mark returned results", 960, 821, 28, "muted")
        elif name == "graph":
            positions = ((300, 455), (615, 315), (914, 428), (1208, 306), (1580, 448), (1360, 701), (911, 689), (514, 709))
            edges = ((0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,0),(1,7),(2,6),(0,2),(3,5))
            for aa, bb in edges:
                line(c, [positions[aa],positions[bb]], "blue", 4, .5)
            for i,(x,y) in enumerate(positions):
                circle(c,x,y,34,"panel2")
                circle(c,x,y,18,"mint")
            # Separate long-range upper layer and local lower layer, schematically.
            for x in (300,914,1580):
                line(c, [(x,262),(x,positions[(0,2,4)[(300,914,1580).index(x)]][1]-45)], "yellow", 3, .25)
                circle(c,x,262,18,"yellow")
            line(c, [(300,262),(914,262),(1580,262)], "yellow", 5, .65)
            route = (0,2,6,5)
            at = (t*.45) % (len(route)-1)
            idx, u = int(at), at-int(at)
            start,end = positions[route[idx]],positions[route[idx+1]]
            circle(c,start[0]+(end[0]-start[0])*u,start[1]+(end[1]-start[1])*u,13,"yellow")
            text(c, "Upper-layer links and local neighbour links", 960, 791, 35, "yellow", True)
            text(c, "Schematic navigation · Not a measured HNSW run", 960, 829, 26, "muted")
        elif name == "controls":
            for i,(title,number,fill) in enumerate((("POINTS EXAMINED",6,"mint"),("POINTS EXAMINED",4,"coral"))):
                x = 535+i*850
                circle(c,x,467,170,fill,.13)
                text(c,str(number),x,515,135,fill,True)
                text(c,title,x,280,29,fill,True)
                flow(c,x,647,x,681,t,fill)
                chip(c,"RETURN 3",x,736,420,"yellow",45,103)
            text(c,"Exact toy run",535,631,30,"mint")
            text(c,"Approximate toy run",1385,631,30,"coral")
        elif name == "boundaries":
            items = (("1", "CANDIDATES", "Who may compete?", "blue"), ("2", "SCORE", "What comparison rule?", "mint"),
                     ("3", "EXECUTION", "Exact or approximate?", "pink"), ("4", "OUTPUT", "How many leaders?", "yellow"))
            for i,(num,title,sub,fill) in enumerate(items):
                x = 285+i*450
                rect(c,x-190,332,380,389,"panel",34)
                circle(c,x,398,35,fill)
                text(c,num,x,411,35,"ink",True)
                text(c,title,x,506,30,fill,True)
                wrap(c,sub,x,581,31,width=315)
                if i<3:
                    flow(c,x+199,510,x+246,510,t,fill)
            text(c,"k belongs to the output decision",960,806,39,"yellow",True)
        elif name == "nearest":
            circle(c,560,510,210,"blue",.1)
            robot(c,560,510,t,.82,"yellow")
            text(c,"THE QUESTION",560,789,32,"yellow",True)
            for i,(x,y,ident) in enumerate(((1230,363,"A"),(1610,584,"B"),(1290,711,"C"))):
                line(c,[(560,510),(x,y)],"muted",3,.2)
                paper(c,x,y,ident,[],t,.35,"coral")
            circle(c,1230,363,84,"yellow",.8,4)
            text(c,"A is nearest...",1440,290,38,"yellow",True)
            text(c,"...even if all three are unsuitable",1405,813,31,"coral",True)
        else:
            raise ValueError(name)

    def semantics(self, c, name, t, p):
        if name == "goal":
            chip(c,"SEMANTIC",960,315,570,"coral",64,117)
            text(c,"Match by meaning",960,433,45,"white",True)
            for i,(label,fill) in enumerate((("EXPANSION","blue"),("DENSE VECTORS","mint"),("RERANKING","yellow"))):
                x=400+i*560
                flow(c,960,464,x,567,t,fill)
                robot(c,x,662,t,.57,fill)
                text(c,label,x,798,32,fill,True)
        elif name == "routes":
            for i,(label,route,fill) in enumerate((("1 · EXPAND","Add terms → lexical match","blue"),
                                                  ("2 · ENCODE","Compare learned vectors","mint"),
                                                  ("3 · RERANK","Shortlist → richer comparison","yellow"))):
                yy=336+i*175
                chip(c,label,408,yy,360,fill,31)
                flow(c,608,yy,781,yy,t+i,fill)
                card(c,1263,yy,route,"",fill,835,125)
            text(c,"heart attack treatment  ↔  myocardial infarction therapy",960,814,32,"coral",True)
        elif name == "bridge":
            card(c,483,437,"Am I being delulu about getting this job?","Query","blue",660,242)
            card(c,1437,437,"How to recognise unrealistic expectations during a job search","Passage","mint",700,242)
            flow(c,861,437,1059,437,t,"yellow")
            for x,fill in ((430,"blue"),(1170,"mint")):
                bars(c,x,644,(.6,.4,.7,.3),fill,61)
            text(c,"Possible vocabulary bridge; not measured model output",960,805,31,"muted")
        elif name == "bottleneck":
            for i,(label,fill) in enumerate((("Topic","blue"),("Entity CMP-104","mint"),("NOT effective","coral"),("Qualification","pink"))):
                yy=323+i*128
                chip(c,label,380,yy,410,fill,34)
                flow(c,611,yy,843,505,t+i,fill)
            polygon(c,[(875,301),(1186,448),(1186,562),(875,707)],"panel2")
            text(c,"POOL",1020,520,40,"white",True)
            flow(c,1215,505,1386,505,t,"yellow")
            orbit(c,1540,505,129,t,"yellow",6)
            circle(c,1540,505,46,"yellow")
            text(c,"One point",1540,724,39,"yellow",True)
            text(c,"Invented identifier; no actual embedding is measured",960,818,29,"muted")
        elif name == "threshold":
            rect(c,214,291,1492,459,"panel",34)
            text(c,"The same threshold, two possible outcomes",960,352,37,"coral",True)
            for i,(x,label,fill) in enumerate(((520,"QUERY A","blue"),(1400,"QUERY B","mint"))):
                text(c,label,x,424,28,fill,True)
                line(c,[(x-260,566),(x+260,566)],"yellow",4,.8)
                text(c,"threshold",x+262,600,23,"yellow",align="right")
                count=6 if i==0 else 24
                for j in range(count):
                    xx=x-245+(j%8)*67
                    yy=640+(j//8)*24 if i==0 else 535-(j//8)*31
                    circle(c,xx,yy,9,fill,.85)
                text(c,"0 returned" if i==0 else "Many returned",x,708,40,fill,True)
            text(c,"Illustrative score distributions; not comparable relevance probabilities",960,814,28,"muted")
        elif name == "budgets":
            for i,(count,label,fill) in enumerate(((30,"CANDIDATES","blue"),(5,"ANSWER WRITER","mint"),(3,"ON SCREEN","coral"))):
                x=410+i*550
                circle(c,x,467,148,fill,.14)
                text(c,str(count),x,506,114,fill,True)
                text(c,label,x,706,31,fill,True)
                if i<2:
                    flow(c,x+178,469,x+369,469,t,fill)
            text(c,"Invented budgets · Each handoff can discard useful material",960,811,32,"yellow",True)
        elif name == "puzzle":
            rect(c,190,270,1540,233,"panel",30)
            rect(c,190,550,1540,233,"panel",30)
            text(c,"SEMANTIC SCHOLAR · DOCUMENTED 2025 SNAPSHOT",960,321,30,"blue",True)
            text(c,"OPENALEX ALICE · DOCUMENTED 2026 SNAPSHOT",960,602,30,"mint",True)
            for row,(first,second,fill) in enumerate((("Lexical candidates","LightGBM reranking","blue"),("Query embedding","Cosine retrieval","mint"))):
                yy=414+row*280
                chip(c,first,552,yy,600,fill,34)
                flow(c,875,yy,1044,yy,t,fill)
                chip(c,second,1380,yy,600,fill,34)
            text(c,"Chapter's dated accounts; these do not diagnose an individual query",960,824,27,"muted")
        elif name == "questions":
            items=(("1","What does each vector stand for?","blue"),("2","Which model and comparison rule?","mint"),
                   ("3","Exact or approximate search?","yellow"),("4","Where does each result list stop?","coral"))
            for i,(num,title,fill) in enumerate(items):
                yy=318+i*128
                circle(c,319,yy,32,fill)
                text(c,num,319,yy+12,31,"ink",True)
                text(c,title,397,yy+14,43,"white",True,"left",1310)
            text(c,"Read Chapter 7 · Explore the Vector Similarity Lab",960,813,31,"muted")
        else:
            raise ValueError(name)
