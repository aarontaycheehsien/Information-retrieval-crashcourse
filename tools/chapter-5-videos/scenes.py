"""Original geometric motion graphics for Chapter 5; all coordinates are illustrative."""
from __future__ import annotations

import math

import skia

from visuals import (Film as BaseFilm, arrow, check, chip, circle, clamp, color,
                     flow, line, paint, paper, polygon, pop, rect, robot, smooth, text)


def label(c, value, x, y, size=32, fill="muted"):
    text(c, value, x, y, size, fill, max_width=1600)


def capsule(c, value, x, y, fill="blue", w=300, h=70, size=32):
    chip(c, value, x, y, w, fill, size, h)


def vector(c, x, y, values, fill="mint", width=280):
    """Anonymous illustrative dimensions, with a true zero baseline."""
    rect(c, x-width/2-18, y-108, width+36, 215, "panel2", 22)
    line(c, [(x-width/2, y), (x+width/2, y)], "muted", 2)
    gap = width/len(values)
    for i, v in enumerate(values):
        xx = x-width/2+gap*(i+.5)
        hh = abs(v)*80
        rect(c, xx-gap*.32, y-hh if v > 0 else y, gap*.64, hh, fill, 5)
    label(c, "illustrative vector", x, y+145, 25)


def map_grid(c, x, y, w, h):
    rect(c, x, y, w, h, "panel", 34)
    for i in range(1, 7):
        line(c, [(x+i*w/7, y+25), (x+i*w/7, y+h-25)], "panel2", 2)
    for i in range(1, 5):
        line(c, [(x+25, y+i*h/5), (x+w-25, y+i*h/5)], "panel2", 2)


def dot(c, value, x, y, t, fill="mint", r=25):
    circle(c, x, y, r+11+4*math.sin(t*2), fill, .12)
    circle(c, x, y, r, fill)
    circle(c, x-7, y-7, 5, "white", .7)
    label(c, value, x, y+64, 30, fill)


def sentence(c, y, hidden=None, future=None, small=False):
    words = ["The", "patient", "received", "heart", "treatment", "after", "the", "attack"]
    for i, word in enumerate(words):
        x = 274+i*196
        fill = "coral" if i == hidden else "panel2" if future is not None and i >= future else "blue"
        capsule(c, "?" if i == hidden else "…" if future is not None and i >= future else word,
                x, y, fill, 174, 78, 30 if not small else 25)


def river(c, x, y, t, scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    circle(c, 0, 0, 175, "mint")
    polygon(c, [(-140, -40), (-5, -20), (60, 35), (160, 25), (145, 85),
                (25, 92), (-45, 30), (-150, 20)], "blue")
    for i in range(3):
        xx = -85+((t*24+i*60) % 150)
        line(c, [(xx, 4), (xx+25, 13)], "white", 4, .65)
    for xx, yy in [(-80, -80), (90, -50), (-70, 90)]:
        line(c, [(xx, yy), (xx, yy-35)], "ink", 7)
        polygon(c, [(xx-25, yy-15), (xx, yy-65), (xx+25, yy-15)], "panel")
    c.restore()


def finance(c, x, y, t, scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    circle(c, 0, 0, 175, "violet")
    polygon(c, [(-120, -70), (0, -130), (120, -70)], "yellow")
    for xx in (-78, 0, 78):
        rect(c, xx-17, -55, 34, 150, "white", 8)
    rect(c, -127, 90, 254, 26, "yellow", 5)
    capsule(c, "$", 0, -87, "yellow", 48, 42, 29)
    circle(c, 132, 96+math.sin(t*2)*10, 30, "yellow")
    text(c, "$", 132, 108+math.sin(t*2)*10, 30, "ink", True)
    c.restore()


class Film(BaseFilm):
    def draw(self, c, t):
        # Own chapter frame keeps compatibility with the original Chapter 2 engine.
        c.clear(color("bg"))
        circle(c, -130, 680, 450, "panel", .35)
        circle(c, 2020, 370, 400, "panel", .4)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+8*math.sin(t*.12+i), y+5*math.cos(t*.1+i), r, "muted", .45)
        name = next((s for s, (a, b) in self.timeline["scenes"].items() if a <= t < b),
                    self.episode["scenes"][-1]["id"])
        scene = next(s for s in self.episode["scenes"] if s["id"] == name)
        a, b = self.timeline["scenes"][name]
        u, p = t-a, clamp((t-a)/(b-a))
        text(c, f"CHAPTER 5   /   FILM {self.number:02d}", 105, 79, 25, self.accent, True, "left")
        text(c, self.episode["subtitle"], 1815, 79, 25, "muted", align="right")
        text(c, scene["title"], 960, 173+(1-pop(u/.7))*35, 65, "white", True, max_width=1700)
        c.save()
        c.translate(0, (1-pop(u/.7))*45)
        (self.geometry, self.context, self.training)[self.number-1](c, name, u, p)
        c.restore()
        rect(c, 190, 849, 1540, 70, "panel", 35)
        text(c, scene["claim"], 960, 897, 32, self.accent, True, max_width=1470)
        text(c, "Adapted from Chapter 5 · Aaron Tay", 105, 945, 20, "muted", align="left")
        for i, s in enumerate(self.episode["scenes"]):
            circle(c, 1652+i*22, 937, 5, self.accent if s["id"] == name else "panel2")
        if b-t < .3 and scene != self.episode["scenes"][-1]:
            q = smooth((.3-(b-t))/.3)
            rect(c, 1920-1920*q, 230, 1920*q, 590, self.accent, 0)

    def geometry(self, c, name, t, p):
        if name == "islands":
            for x, fill, words in [(485, "mint", ["delulu", "job", "expectations"]),
                                   (1435, "pink", ["unrealistic", "career", "hopes"])]:
                circle(c, x, 530, 195, fill)
                polygon(c, [(x-140, 550), (x, 330), (x+155, 550)], "panel")
                paper(c, x, 540, "TEXT", words, t, .67)
            q = pop((t-self.spoken_at(name, "Embeddings", 8))/2)
            if q > 0:
                line(c, [(710, 565), (710+q*500, 565)], "yellow", 17)
                for i in range(5):
                    if q*500 > i*100:
                        circle(c, 750+i*100, 565, 9, "white")
            robot(c, 960, 440, t, .6)
            label(c, "No shared words in this example", 960, 787, 35)
        elif name == "numbers":
            paper(c, 380, 550, "QUERY", ["delulu", "job", "expectations"], t, .76)
            flow(c, 580, 540, 790, 540, t)
            robot(c, 960, 540, t, 1.15)
            flow(c, 1120, 540, 1315, 540, t)
            vector(c, 1520, 520, [.8, -.35, .55, .9, -.65, .2], "mint", 310)
            label(c, "Text", 380, 780, 38, "white")
            label(c, "Encoder", 960, 780, 38, "yellow")
            label(c, "Ordered numbers", 1520, 780, 38, "mint")
        elif name == "routes":
            for y, fill, values in [(400, "yellow", ["Counts + lengths", "Specified formula", "Scores"]),
                                    (660, "mint", ["Text + tokens", "Learnt parameters", "Vector"])]:
                for i, value in enumerate(values):
                    x = 470+i*490
                    capsule(c, value, x, y, fill if i != 1 else "blue", 385, 105, 32)
                    if i < 2:
                        flow(c, x+210, y, x+280, y, t, fill)
                label(c, "BM25" if y == 400 else "Neural encoder", 175, y+13, 26, fill)
            label(c, "Both compute outputs", 960, 803, 40, "white")
        elif name == "targets":
            sentence(c, 360, hidden=3)
            for i in (1, 2, 4, 5):
                flow(c, 274+i*196, 420, 960, 545, t, "blue")
            robot(c, 960, 600, t, .65)
            capsule(c, "heart", 1470, 600, "mint", 260)
            flow(c, 1080, 600, 1310, 600, t)
            label(c, "Compare prediction with the original word", 960, 787, 36)
        elif name == "word2vec":
            for x, fill, title in [(510, "mint", "CBOW"), (1410, "pink", "SKIP-GRAM")]:
                rect(c, x-360, 260, 720, 530, "panel", 34)
                text(c, title, x, 325, 39, fill, True)
                context_y, word_y = (420, 630) if x == 510 else (630, 420)
                for i, word in enumerate(("river", "the", "near")):
                    xx = x-210+i*210
                    capsule(c, word, xx, context_y, "blue", 175)
                    if x == 510:
                        flow(c, xx, context_y+48, x, word_y-48, t, fill)
                    else:
                        flow(c, x, word_y+48, xx, context_y-48, t, fill)
                capsule(c, "bank", x, word_y, fill, 230)
                label(c, "Context → word" if x == 510 else "Word → context", x, 755, 33, fill)
        elif name == "analogy":
            map_grid(c, 230, 265, 1460, 535)
            man, woman, king, queen = (440, 610), (790, 425), (1040, 630), (1390, 445)
            q = pop((t-self.spoken_at(name, "subtracts", 3))/2.5)
            for aa, bb in [(man, woman), (king, queen)]:
                arrow(c, aa[0], aa[1], aa[0]+q*(bb[0]-aa[0]), aa[1]+q*(bb[1]-aa[1]), "yellow")
            for word, pos, fill in [("man", man, "blue"), ("woman", woman, "pink"),
                                    ("king", king, "mint"), ("queen", queen, "coral")]:
                dot(c, word, *pos, t, fill)
            label(c, "SCHEMATIC · anonymous axes · no trained vectors plotted", 960, 785, 25)
        elif name == "shadow":
            # A rotating wireframe casts a flattened view; not a numerical PCA claim.
            pts = []
            for x, y, z in [(-1,-1,-1),(1,-1,-1),(1,1,-1),(-1,1,-1),
                             (-1,-1,1),(1,-1,1),(1,1,1),(-1,1,1)]:
                a = t*.16
                xx, zz = x*math.cos(a)+z*math.sin(a), -x*math.sin(a)+z*math.cos(a)
                pts.append((500+xx*125+zz*45, 530+y*130+zz*30))
            for aa, bb in [(0,1),(1,2),(2,3),(3,0),(4,5),(5,6),(6,7),(7,4),(0,4),(1,5),(2,6),(3,7)]:
                line(c, [pts[aa], pts[bb]], "mint", 5)
            flow(c, 770, 530, 1000, 530, t, "yellow")
            map_grid(c, 1100, 300, 610, 400)
            for i, (a, b) in enumerate([("France", "Paris"), ("Japan", "Tokyo"), ("Italy", "Rome")]):
                x, y = 1190+i*160, 590-i*70
                dot(c, a, x, y, t, "blue", 12)
                arrow(c, x+10, y-20, x+70, y-120, "yellow", 4)
                dot(c, b, x+75, y-140, t, "pink", 12)
            label(c, "High-dimensional relationships", 500, 770, 32)
            label(c, "Illustrative 2D view", 1400, 770, 32)
        elif name == "compass":
            circle(c, 580, 540, 205, "panel2")
            circle(c, 580, 540, 170, "mint", .8, 5)
            a = -.7+.12*math.sin(t)
            polygon(c, [(580+145*math.sin(a), 540-145*math.cos(a)),
                        (555, 550), (580, 575), (605, 550)], "yellow")
            label(c, "Training target", 580, 795, 40, "mint")
            for i, (value, fill) in enumerate([("Co-occurrence", "blue"), ("Linguistic regularity", "pink"),
                                              ("Relevance? Check the task.", "coral")]):
                capsule(c, value, 1350, 375+i*165, fill, 650, 100, 35)

    def context(self, c, name, t, p):
        if name in ("bank", "static", "context"):
            river(c, 430, 520, t)
            finance(c, 1490, 520, t)
            label(c, "the river bank", 430, 760, 37, "mint")
            label(c, "the bank refused the loan", 1490, 760, 37, "pink")
            if name == "bank":
                robot(c, 960, 550, t, .95)
                capsule(c, "bank", 960, 310, "yellow", 270)
                flow(c, 740, 520, 625, 520, t, "mint")
                flow(c, 1180, 520, 1295, 520, t, "pink")
            elif name == "static":
                vector(c, 960, 540, [.8, -.4, .55, .2, -.5], "yellow", 300)
                label(c, "SAME STORED VECTOR", 960, 310, 35, "yellow")
                flow(c, 630, 520, 760, 520, t, "mint")
                flow(c, 1290, 520, 1160, 520, t, "pink")
            else:
                q = pop((t-self.spoken_at(name, "River", 5))/2)
                x1, x2 = 960-200*q, 960+200*q
                dot(c, "bank | river", x1, 440, t, "mint", 23)
                dot(c, "bank | loan", x2, 605, t, "pink", 23)
                flow(c, 605, 450, x1-40, 440, t, "mint")
                flow(c, 1310, 605, x2+40, 605, t, "pink")
                label(c, "Computed for each occurrence", 960, 300, 35, "white")
        elif name == "attention":
            words = ["the", "river", "bank", "was", "quiet"]
            for i in range(5):
                for j in range(i+1, 5):
                    x1, x2 = 350+i*300, 350+j*300
                    path = skia.Path()
                    path.moveTo(x1, 510)
                    path.quadTo((x1+x2)/2, 265-(j-i)*15, x2, 510)
                    c.drawPath(path, paint("mint" if i == 2 or j == 2 else "blue", .6, 5))
            for i, word in enumerate(words):
                capsule(c, word, 350+i*300, 550, "yellow" if i == 2 else "blue", 240, 94, 40)
                circle(c, 350+i*300, 685+math.sin(t*2+i)*12, 24, "mint")
            label(c, "Token representations can use sequence context", 960, 790, 38)
        elif name == "units":
            capsule(c, "river bank", 960, 300, "white", 620, 90, 43)
            rect(c, 180, 400, 700, 380, "panel", 32)
            rect(c, 1040, 400, 700, 380, "panel", 32)
            text(c, "LEXICAL ANALYSER", 530, 465, 35, "mint", True)
            text(c, "TOY MODEL TOKENIZER", 1390, 465, 35, "pink", True)
            capsule(c, "river", 380, 590, "mint", 240)
            capsule(c, "bank", 680, 590, "mint", 240)
            for i, word in enumerate(["r", "i", "v", "e", "r"]):
                capsule(c, word, 1170+i*105, 590, "pink", 85, 65, 32)
            label(c, "Indexed terms", 530, 725, 35, "mint")
            label(c, "Illustration only: character split", 1390, 725, 29, "pink")
        elif name == "pooling":
            for i, word in enumerate(["river", "bank", "quiet"]):
                x = 360+i*310
                capsule(c, word, x, 330, "blue", 240)
                vector(c, x, 520, [.5+i*.1, -.3, .8-i*.2, .2], "blue", 215)
                flow(c, x+130, 520, 1220, 520, t)
            rect(c, 1220, 380, 140, 280, "mint", 30)
            text(c, "POOL", 1290, 535, 29, "ink", True)
            flow(c, 1375, 520, 1455, 520, t)
            vector(c, 1620, 520, [.6, -.3, .6, .2], "mint", 225)
            label(c, "Contextual token vectors", 665, 785, 35, "blue")
            label(c, "One text vector", 1580, 785, 35, "mint")
        elif name == "comparison":
            for y, value, fill in [(390, "delulu job expectations", "blue"),
                                    (655, "unrealistic career hopes", "pink")]:
                capsule(c, value, 490, y, fill, 660, 98, 38)
                flow(c, 850, y, 970, y, t, fill)
                vector(c, 1150, y, [.65, -.25, .7 if y == 390 else .5, .3], fill, 250)
            flow(c, 1330, 410, 1470, 490, t, "blue")
            flow(c, 1330, 640, 1470, 560, t, "pink")
            circle(c, 1610, 525, 105, "yellow")
            text(c, "SCORE", 1610, 537, 36, "ink", True)
            label(c, "A model-dependent comparison", 1610, 785, 28)
        elif name == "useful":
            robot(c, 485, 550, t, 1.2)
            capsule(c, "Context", 485, 320, "blue", 430, 100, 43)
            flow(c, 750, 525, 1170, 525, t, "yellow")
            circle(c, 1450, 525, 145, "coral")
            text(c, "PURPOSE", 1450, 539, 44, "ink", True)
            label(c, "Available information", 485, 790, 40, "blue")
            label(c, "Chosen by training", 1450, 790, 40, "coral")

    def training(self, c, name, t, p):
        if name in ("blank", "cbow", "masked", "next"):
            if name == "blank":
                sentence(c, 370)
                sentence(c, 650, hidden=4)
                flow(c, 960, 430, 960, 575, t, "yellow")
                label(c, "The original token supplies the target", 960, 800, 36, "yellow")
            else:
                hidden = {"cbow": 3, "masked": 4, "next": 5}[name]
                sentence(c, 390, hidden=hidden, future=5 if name == "next" else None)
                indices = [1, 2, 4, 5] if name == "cbow" else [0,1,2,3,5,6,7] if name == "masked" else [0,1,2,3,4]
                for i in indices:
                    flow(c, 274+i*196, 445, 960, 560, t, "blue")
                robot(c, 960, 620, t, .67)
                value = {"cbow": "heart", "masked": "treatment", "next": "after"}[name]
                capsule(c, value, 1470, 620, "mint", 280, 82, 39)
                flow(c, 1095, 620, 1290, 620, t, "mint")
                label(c, "Local context window" if name == "cbow" else "Both sides visible" if name == "masked" else "Only preceding tokens visible",
                      960, 802, 35, "yellow")
        elif name == "mismatch":
            for x, title, subtitle, fill, yes in [(480, "FILL A BLANK", "Language pretraining", "blue", True),
                                                (1440, "RANK AN ANSWER", "Different task", "coral", False)]:
                rect(c, x-355, 300, 710, 475, "panel", 36)
                text(c, title, x, 375, 42, fill, True)
                robot(c, x, 555, t, .8, fill)
                check(c, x+210, 555, yes, 31)
                label(c, subtitle, x, 730, 36, fill)
            label(c, "Pretraining success alone does not establish retrieval quality", 960, 817, 29)
        elif name == "domain":
            for i, (value, subtitle, fill) in enumerate([("BioBERT", "Continued biomedical pretraining", "mint"),
                                                       ("BiomedBERT", "Biomedical text + vocabulary", "blue"),
                                                       ("SciBERT", "Scientific text + vocabulary", "pink")]):
                x = 395+i*565
                rect(c, x-225, 295, 450, 490, "panel", 32)
                for j in range(5):
                    rect(c, x-160+j*65, 425+15*math.sin(t+j), 52, 180, fill, 8)
                text(c, value, x, 375, 42, fill, True)
                text(c, subtitle, x, 702, 27, "white", max_width=405)
                label(c, "Language background", x, 752, 28, fill)
        elif name == "retrieval":
            map_grid(c, 180, 290, 1130, 495)
            q = pop((t-self.spoken_at(name, "closer", 16))/2)
            dot(c, "Question", 420, 520, t, "yellow")
            dot(c, "Useful passage", 1070-430*q, 385+105*q, t, "mint")
            dot(c, "Distractor", 1040, 670, t, "coral")
            if q > 0:
                arrow(c, 1005, 416, 640, 490, "mint", 5)
            for i, word in enumerate(["Human", "Behaviour", "Weak / synthetic", "Self-supervised"]):
                capsule(c, word, 1540, 365+i*113, "blue" if i % 2 else "pink", 405, 74, 31)
            label(c, "ILLUSTRATIVE TRAINING MOVEMENT", 745, 770, 25)
        elif name == "questions":
            for y, num, value, fill in [(380, "1", "Was it trained for retrieval?", "mint"),
                                        (575, "2", "Where is it in the pipeline?", "yellow")]:
                circle(c, 330, y, 57, fill)
                text(c, num, 330, y+19, 55, "ink", True)
                text(c, value, 1080, y+15, 55, "white", True, max_width=1180)
            for i, value in enumerate(["Interpret query", "Retrieve candidates", "Rerank shortlist"]):
                capsule(c, value, 415+i*545, 770, "blue", 460, 75, 31)
