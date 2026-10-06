"""Original flat-vector animation: a cosmic library and its evidence explorers."""
from __future__ import annotations

import math
import numpy as np
from visuals import (arrow, chip, circle, clamp, color, flow, font, line,
                     paper, polygon, pop, rect, robot, smooth, text)


LABELS = ('NEURAL', 'VECTOR', 'EMBEDDING', 'SEMANTIC', 'AGENTIC', 'AI-POWERED')
ROUTES = ('ORIENTATION', 'INSTRUCTION', 'EVIDENCE SYNTHESIS', 'PROCUREMENT', 'CURIOSITY')


def wrap(c, value, x, y, width=460, size=28, fill='muted'):
    rows, current = [], ''
    for word in value.split():
        trial = (current+' '+word).strip()
        if current and font(size).measureText(trial) > width:
            rows.append(current)
            current = word
        else:
            current = trial
    if current:
        rows.append(current)
    for i, row in enumerate(rows):
        text(c, row, x, y+i*size*1.25, size, fill)


def plaque(c, x, y, title, subtitle='', fill='mint', w=450, h=140):
    rect(c, x-w/2, y-h/2, w, h, 'panel2', 28)
    text(c, title, x, y-8 if subtitle else y+12, 33, fill, True, max_width=w-40)
    if subtitle:
        wrap(c, subtitle, x, y+34, w-40, 26)


def orbit(c, x, y, r, t, fill='mint'):
    circle(c, x, y, r, fill, .25, 3)
    for i in range(6):
        angle = t*.18+i*math.tau/6
        circle(c, x+math.cos(angle)*r, y+math.sin(angle)*r, 5, fill)


def book(c, x, y, t, scale=1, fill='blue'):
    c.save()
    c.translate(x, y+6*math.sin(t*1.6))
    c.rotate(3*math.sin(t*.7))
    c.scale(scale, scale)
    polygon(c, [(-142, -108), (-18, -85), (0, -55), (18, -85), (142, -108),
                (142, 103), (20, 128), (0, 107), (-20, 128), (-142, 103)], fill)
    polygon(c, [(-125, -93), (-15, -68), (-15, 105), (-125, 84)], 'white')
    polygon(c, [(125, -93), (15, -68), (15, 105), (125, 84)], 'white')
    line(c, [(0, -58), (0, 102)], 'ink', 6)
    for sign in (-1, 1):
        for i in range(5):
            line(c, [(sign*30, -35+i*26), (sign*102, -51+i*26)], 'ink', 5, .3)
    for xx in (-46, 46):
        circle(c, xx, -1, 8, 'ink')
    line(c, [(-34, 31), (0, 45), (34, 31)], 'ink', 7)
    c.restore()


def telescope(c, x, y, t, fill='yellow', scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    line(c, [(0, 8), (-67, 152)], fill, 15)
    line(c, [(0, 8), (67, 152)], fill, 15)
    line(c, [(0, 8), (0, 155)], fill, 12)
    c.rotate(-18+3*math.sin(t*.6))
    rect(c, -114, -52, 228, 88, fill, 18)
    rect(c, 87, -67, 43, 119, 'white', 16)
    circle(c, 118, -7, 26, 'mint')
    rect(c, -150, -30, 50, 40, 'coral', 9)
    c.restore()


def record(c, x, y, ident, t, fill='white', scale=.6):
    paper(c, x, y, ident, [], t, scale, fill)


class Film:
    SCENES = {
        1: {'questions', 'gate', 'podium', 'syntax', 'labels', 'inside', 'evidence', 'compass'},
        2: {'machines', 'fluency', 'fabrication', 'faithful', 'missing', 'checks', 'library', 'handoff'},
        3: {'audiences', 'principles', 'dated', 'scope', 'start', 'routes', 'specialist', 'launch'},
    }

    def __init__(self, episode, timeline):
        self.episode, self.timeline = episode, timeline
        self.number, self.accent = int(episode['id'][:2]), episode['accent']
        self.stars = np.random.default_rng(20261004).uniform([20, 240, 1], [1900, 820, 3], (60, 3))

    def at(self, scene, word, fallback=5):
        take = next((v for v in self.timeline.get('takes', []) if v['id'] == scene), None)
        if take:
            hits = [w for w in take['words'] if w['text'].lower().strip('.,!?;:\'') == word.lower()]
            if hits:
                return hits[0]['start']-self.timeline['scenes'][scene][0]
        return fallback

    def draw(self, c, t):
        c.clear(color('bg'))
        circle(c, -100, 620, 425, 'panel', .75)
        circle(c, 2000, 425, 420, 'panel2', .45)
        circle(c, 1880, 790, 84, self.accent, .15)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+8*math.sin(t*.1+i), y+6*math.cos(t*.12+i), r, 'muted', .4)
        name = next((s for s, (a, b) in self.timeline['scenes'].items() if a <= t < b), self.episode['scenes'][-1]['id'])
        scene = next(s for s in self.episode['scenes'] if s['id'] == name)
        a, b = self.timeline['scenes'][name]
        u, p = t-a, clamp((t-a)/(b-a))
        text(c, f'PREFACE   /   FILM {self.number:02d}', 105, 79, 25, self.accent, True, 'left')
        text(c, self.episode['subtitle'], 1815, 79, 24, 'muted', align='right', max_width=1190)
        text(c, scene['title'], 960, 177+(1-pop(u/.7))*24, 59, 'white', True, max_width=1700)
        c.save()
        c.translate(0, (1-pop(u/.7))*35)
        (self.box, self.evidence, self.route)[self.number-1](c, name, u, p)
        c.restore()
        rect(c, 155, 843, 1610, 78, 'panel', 36)
        text(c, scene['claim'], 960, 892, 30, self.accent, True, max_width=1520)
        text(c, 'Adapted from the Preface · Aaron Tay', 105, 947, 20, 'muted', align='left')
        for i, s in enumerate(self.episode['scenes']):
            circle(c, 1652+22*i, 939, 5, self.accent if s['id'] == name else 'panel2')
        if b-t < .28 and scene != self.episode['scenes'][-1]:
            q = smooth((.28-(b-t))/.28)
            rect(c, 1920-1920*q, 235, 1920*q, 580, self.accent, 0)

    def box(self, c, name, t, p):
        if name in ('questions', 'compass'):
            book(c, 960, 520, t, 1.22, 'mint')
            orbit(c, 960, 520, 230, t)
            plaque(c, 380, 432, 'WHY ADMITTED?', 'the candidate set', 'mint', 460)
            plaque(c, 1540, 595, 'WHY RANKED HERE?', 'the ordering decision', 'pink', 470)
            flow(c, 635, 432, 728, 478, t, 'mint')
            flow(c, 1190, 563, 1277, 595, t, 'pink')
            robot(c, 490, 712, t, .6)
            text(c, 'ONE RESULT · TWO QUESTIONS', 1080, 777, 31, 'yellow', True)
        elif name == 'gate':
            rect(c, 780, 288, 880, 482, 'panel', 40)
            text(c, 'CANDIDATE ROOM', 1220, 345, 32, 'mint', True)
            rect(c, 740, 372, 80, 340, 'mint', 26)
            circle(c, 780, 414, 16, 'white')
            for i in range(5):
                x = 245+(i-3)*210 if i > 2 else 1000+i*245
                if i == 0:
                    x = 620+380*smooth((t-self.at(name, 'admits', 5))/3)
                record(c, x, 535+25*math.sin(i+t*.3), chr(65+i), t, 'white' if i < 3 else 'coral', .55)
            flow(c, 615, 490, 722, 490, t, 'mint')
            text(c, 'COLLECTION', 390, 748, 30, 'muted', True)
            text(c, 'Selection illustrated; no admission rule assumed', 1180, 802, 27, 'muted')
        elif name == 'podium':
            for i, (ident, fill) in enumerate([('B', 'mint'), ('A', 'pink'), ('C', 'blue')]):
                x, height = 570+i*390, 160-i*42
                y = 706-height
                rect(c, x-150, y, 300, height, fill, 22)
                text(c, str(i+1), x, y+55, 42, 'ink', True)
            # Draw explorers after every pedestal, so crossing records stay visible.
            for i, ident in enumerate('BAC'):
                x, y = 570+i*390, 546+i*42
                q = smooth((t-self.at(name, 'upward', 5))/4)
                if i < 2:
                    initial_x = 960 if i == 0 else 570
                    initial_y = 473 if i == 0 else 431
                    record(c, initial_x+(x-initial_x)*q, initial_y+(y-115-initial_y)*q,
                           ident, t, 'white', .64)
                else:
                    record(c, x, y-115, ident, t, 'white', .64)
            text(c, 'ILLUSTRATIVE ORDER · NO SCORES CALCULATED', 960, 785, 29, 'muted', True)
        elif name == 'syntax':
            telescope(c, 1450, 482, t, scale=1.25)
            book(c, 425, 535, t, 1.1, 'blue')
            flow(c, 650, 540, 1130, 540, t, 'yellow')
            plaque(c, 925, 343, 'FAMILIAR SKILLS', 'Boolean syntax • database searching', 'blue', 650)
            plaque(c, 1000, 742, 'NEW QUESTIONS', 'How does the engine select papers?', 'yellow', 800)
        elif name == 'labels':
            robot(c, 960, 535, t, 1.05)
            for i, label in enumerate(LABELS):
                aa = i*math.tau/6
                x, y = 960+math.cos(aa)*540, 525+math.sin(aa)*205
                y += 10*math.sin(t*.6+i)
                chip(c, label, x, y, 310, ('mint', 'blue', 'pink', 'coral', 'yellow', 'violet')[i], 28, 67)
            text(c, 'SAME BOX. DIFFERENT KINDS OF CLAIM.', 960, 806, 29, 'muted', True)
        elif name == 'inside':
            rect(c, 750, 334, 420, 386, 'mint', 45)
            shift = 90*smooth((t-self.at(name, 'label', 4))/2)
            rect(c, 750-shift, 300-shift, 420, 140, 'blue', 26)
            text(c, 'SEMANTIC', 960-shift, 386-shift, 43, 'ink', True)
            robot(c, 960, 563, t, .72)
            for x, y, title, subtitle, fill in [(360, 435, 'REPRESENTATION', 'how text is encoded', 'pink'),
                    (1560, 435, 'MATCHING', 'how records are compared', 'blue'),
                    (360, 676, 'PIPELINE STAGE', 'where a method is used', 'mint'),
                    (1560, 676, 'CAPABILITY', 'what the product promises', 'yellow')]:
                plaque(c, x, y, title, subtitle, fill, 460)
            text(c, 'THE LABEL DOES NOT SPECIFY THE INTERNAL CHOICES', 960, 806, 27, 'muted', True)
        elif name == 'evidence':
            self.knowledge(c, t)

    def knowledge(self, c, t):
        for i, (title, subtitle, fill) in enumerate([('DECISION', 'Which layer?', 'mint'),
                ('DOCUMENTED', 'What does the vendor say?', 'blue'), ('UNKNOWN', 'What is still undisclosed?', 'coral')]):
            x = 425+i*535
            orbit(c, x, 460, 123, t, fill)
            if i == 2:
                text(c, '?', x, 501, 118, fill, True)
            elif i == 1:
                record(c, x, 458, 'DOC', t, 'white', .61)
            else:
                robot(c, x, 460, t, .63, fill)
            plaque(c, x, 716, title, subtitle, fill, 475)

    def evidence(self, c, name, t, p):
        if name in ('machines', 'handoff'):
            for x, label, fill in [(595, 'SELECT EVIDENCE', 'mint'), (1330, 'WRITE ANSWER', 'pink')]:
                rect(c, x-220, 372, 440, 297, 'panel2', 38)
                robot(c, x, 510, t, .8, fill)
                chip(c, label, x, 710, 460, fill, 28, 66)
            flow(c, 845, 515, 1070, 515, t, 'yellow')
            for i in range(3):
                record(c, 190+i*65, 512+i*53, chr(65+i), t, 'white', .29)
            text(c, 'DIFFERENT JOBS · DIFFERENT FAILURE MODES', 960, 810, 29, 'muted', True)
        elif name == 'fluency':
            self.answer(c, 1130, 504, t)
            for i in range(3):
                record(c, 340+i*180, 473, chr(65+i), t, 'white', .5)
            flow(c, 685, 582, 820, 582, t, 'mint')
            plaque(c, 575, 739, 'AVAILABLE INPUTS', 'The prose does not show the missing ones', 'blue', 780, 100)
        elif name == 'fabrication':
            record(c, 650, 504, 'X', t, 'coral', 1)
            telescope(c, 1260, 463, t, scale=1)
            circle(c, 650, 475, 165, 'coral', .3, 5)
            line(c, [(790, 500), (1090, 460)], 'coral', 5, .7)
            plaque(c, 1000, 748, 'DOES THIS REFERENCE EXIST?', 'Card X is invented for this illustration', 'coral', 1030)
        elif name == 'faithful':
            record(c, 490, 525, 'A', t, 'mint', .94)
            self.answer(c, 1290, 497, t, 'CLAIM TOO STRONG')
            flow(c, 690, 490, 947, 490, t, 'coral')
            chip(c, 'REAL SOURCE', 480, 746, 370, 'mint', 30)
            text(c, 'SUPPORT?', 820, 441, 36, 'coral', True)
            text(c, 'Schematic mismatch; no actual paper is characterized', 960, 807, 26, 'muted')
        elif name == 'missing':
            rect(c, 320, 326, 740, 384, 'panel', 32)
            text(c, 'EVIDENCE RECEIVED', 690, 383, 30, 'mint', True)
            for i in range(3):
                record(c, 475+i*213, 535, chr(65+i), t, 'white', .48)
            orbit(c, 1430, 498, 173, t, 'yellow')
            record(c, 1430, 500, 'P', t, 'yellow', .7)
            chip(c, 'NEVER RECEIVED', 1430, 755, 440, 'coral', 28)
            text(c, 'Hypothetical important paper P; no measured omissions', 960, 807, 26, 'muted')
        elif name == 'checks':
            for i, (label, question, fill) in enumerate([('EXISTENCE', 'Is the reference real?', 'blue'),
                    ('FAITHFUL WRITING', 'Does it support this claim?', 'pink'),
                    ('ADEQUATE RETRIEVAL', 'Was enough evidence available?', 'yellow')]):
                x = 420+i*540
                circle(c, x, 462, 125, fill, .16)
                circle(c, x, 462, 130+9*math.sin(t*.7-i), fill, .3, 3)
                text(c, str(i+1), x, 510, 132, fill, True)
                plaque(c, x, 709, label, question, fill, 490, 150)
        elif name == 'library':
            telescope(c, 960, 523, t, scale=1.2)
            orbit(c, 960, 523, 220, t)
            for x, y, label, fill in [(400, 364, 'LICENSE', 'blue'), (1520, 364, 'CONFIGURE', 'mint'),
                    (400, 711, 'COMPARE', 'pink'), (1520, 711, 'EVALUATE', 'yellow')]:
                chip(c, label, x, y, 360, fill, 31)
                flow(c, x+190 if x < 960 else x-190, y, 775 if x < 960 else 1145, 476 if y < 500 else 634, t, fill)

    def answer(self, c, x, y, t, title='FLUENT ANSWER'):
        rect(c, x-280, y-177, 560, 354, 'white', 33)
        text(c, title, x, y-110, 33, 'ink', True)
        for i in range(5):
            length = 390 if i < 4 else 250
            rect(c, x-207, y-68+i*38, length, 10, 'blue', 5, .65)
        for i in range(3):
            chip(c, chr(65+i), x-132+i*132, y+126, 100, 'mint', 28, 43)
        circle(c, x+258, y-147, 13+2*math.sin(t*2), 'yellow')

    def route(self, c, name, t, p):
        if name == 'audiences':
            for i, (title, subtitle, fill) in enumerate([('INSTRUCTION', 'Teach questions into searches', 'blue'),
                    ('EVIDENCE SYNTHESIS', 'Build and document high recall', 'mint'),
                    ('SYSTEMS & DISCOVERY', 'Configure indexes and integrations', 'pink')]):
                x = 420+i*540
                orbit(c, x, 455, 140, t, fill)
                robot(c, x, 473, t+i, .7, fill)
                plaque(c, x, 718, title, subtitle, fill, 490, 150)
        elif name == 'principles':
            for i, (label, subtitle, fill) in enumerate([('UNDERSTANDING FIRST', 'Enough mechanism to reason with', 'mint'),
                    ('FAMILIAR EXAMPLES', 'Library and academic search', 'blue'),
                    ('PURPOSEFUL FORMULAS', 'Use an equation to carry an argument', 'yellow')]):
                x = 420+i*540
                if i == 0:
                    telescope(c, x, 443, t, fill, .72)
                elif i == 1:
                    book(c, x, 476, t, .8, fill)
                else:
                    orbit(c, x, 475, 118, t, fill)
                    text(c, 'BM25', x, 500, 52, fill, True)
                plaque(c, x, 723, label, subtitle, fill, 490, 150)
        elif name == 'dated':
            rect(c, 360, 315, 475, 367, 'white', 38)
            rect(c, 360, 315, 475, 83, 'coral', 30)
            text(c, 'CHECK THE DATE', 597, 371, 33, 'ink', True)
            text(c, 'DOCUMENTED', 597, 479, 39, 'ink', True)
            text(c, 'AT THE TIME', 597, 545, 38, 'ink', True)
            for i in range(3):
                circle(c, 490+i*110, 620, 13, 'blue')
            flow(c, 880, 505, 1130, 505, t, 'coral')
            telescope(c, 1450, 490, t, scale=1)
            plaque(c, 1270, 753, 'DOCUMENTATION ENDS SOMEWHERE', 'An unknown is not an invitation to guess', 'coral', 900, 115)
        elif name == 'scope':
            rect(c, 555, 675, 810, 47, 'mint', 14)
            robot(c, 960, 543, t, .85)
            for x, y, label, sub, fill in [(350, 365, 'FOLLOW', 'a technical conversation', 'blue'),
                    (1570, 365, 'QUESTION', 'a vendor claim', 'pink'),
                    (350, 704, 'RECOGNIZE', 'a retrieval problem', 'yellow')]:
                plaque(c, x, y, label, sub, fill, 470)
            text(c, 'A FLOOR TO STAND ON', 1130, 792, 34, 'mint', True)
        elif name == 'start':
            book(c, 435, 500, t, 1.13, 'yellow')
            flow(c, 660, 530, 845, 530, t, 'mint')
            plaque(c, 1270, 377, 'START WITH BOOLEAN SEARCH', 'No prior IR knowledge required', 'mint', 810)
            plaque(c, 1270, 566, 'WORDS EXPLAIN THE FORMULAS', 'No calculation required for the main argument', 'blue', 810)
            plaque(c, 1110, 746, 'TRY THE APPLICATION EXERCISES', 'Search a tool you can access; record what happens', 'yellow', 1020, 115)
        elif name == 'routes':
            book(c, 370, 524, t, .92, 'yellow')
            line(c, [(575, 515), (740, 515), (740, 306), (740, 750)], 'muted', 5, .6)
            for i, route in enumerate(ROUTES):
                y = 309+i*107
                flow(c, 745, y, 903, y, t+i*.3, 'mint')
                chip(c, route, 1260, y, 650, ('blue', 'mint', 'pink', 'yellow', 'coral')[i], 29, 72)
        elif name == 'specialist':
            for x, title, detail, appendix, fill in [(520, 'EVIDENCE SYNTHESIS', 'Ch. 2, 11, 13–15', 'APPENDIX F: CORE', 'mint'),
                    (1400, 'PROCUREMENT', 'Distinctions • diagnosis • practice', 'APPENDIX D: MAP', 'blue')]:
                book(c, x, 425, t, .74, fill)
                plaque(c, x, 640, title, detail, fill, 745, 120)
                chip(c, appendix, x, 762, 630, fill, 29, 66)
        elif name == 'launch':
            book(c, 960, 507, t, 1.1, 'yellow')
            orbit(c, 960, 507, 215, t, 'yellow')
            plaque(c, 382, 437, 'WHY ADMITTED?', 'Which candidates were available?', 'mint', 495)
            plaque(c, 1538, 596, 'WHY RANKED HERE?', 'Which decision ordered them?', 'pink', 495)
            flow(c, 960, 751, 960, 801, t, 'yellow')
            text(c, 'NEXT: CHAPTER 1 · THE RETRIEVAL PROBLEM', 960, 813, 27, 'yellow', True)
