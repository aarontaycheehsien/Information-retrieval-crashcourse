"""Original geometric animation for Chapter 15's cosmic search observatory."""
from __future__ import annotations

import math
import numpy as np
from visuals import (arrow, chip, circle, clamp, color, flow, font, line,
                     paper, polygon, pop, rect, robot, smooth, text)

MOCK_TRACE = {
    'original': 'Does open access increase citations?',
    'transformed': '"open access" AND citation*',
    'unit': 'indexed abstracts', 'route': 'lexical retrieval',
    'candidate_rank': 18, 'candidate_count': 100,
    'final_rank': 3, 'display_cutoff': 10,
    'reranker_details': None,
}
QUESTION_GROUPS = ((1, 2), (3, 4, 5, 6, 7), (8, 9, 10, 11),
                   (12, 13, 14), (15, 16), (17, 18, 19))


def validate_examples():
    assert [q for group in QUESTION_GROUPS for q in group] == list(range(1, 20))
    assert 1 <= MOCK_TRACE['candidate_rank'] <= MOCK_TRACE['candidate_count']
    assert MOCK_TRACE['final_rank'] <= MOCK_TRACE['display_cutoff']
    assert MOCK_TRACE['candidate_rank'] > MOCK_TRACE['display_cutoff']
    assert MOCK_TRACE['reranker_details'] is None


def wrap(c, value, x, y, width=450, size=28, fill='muted', bold=False):
    rows, current = [], ''
    for word in value.split():
        trial = (current+' '+word).strip()
        if current and font(size, bold).measureText(trial) > width:
            rows.append(current)
            current = word
        else:
            current = trial
    if current:
        rows.append(current)
    for i, row in enumerate(rows):
        text(c, row, x, y+i*size*1.24, size, fill, bold)


def box(c, x, y, title, subtitle='', fill='mint', width=380, height=140):
    rect(c, x-width/2, y-height/2, width, height, 'panel2', 26)
    text(c, title, x, y-8 if subtitle else y+12, 34, fill, True, max_width=width-36)
    if subtitle:
        wrap(c, subtitle, x, y+33, width-36, 26)


def orbit(c, x, y, radius, t, fill='mint'):
    circle(c, x, y, radius, fill, .3, 3)
    for i in range(5):
        a = t*.2+i*math.tau/5
        circle(c, x+math.cos(a)*radius, y+math.sin(a)*radius, 6, fill)


def banner(c, value, y=794, fill='muted'):
    text(c, value, 960, y, 27, fill, max_width=1650)


def record(c, x, y, ident, fill='white', scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    rect(c, -49, -65, 98, 130, fill, 17)
    polygon(c, [(20, -65), (49, -36), (20, -36)], 'blue', .7)
    text(c, ident, 0, -20, 30, 'ink', True)
    for yy in [0, 15, 30]:
        line(c, [(-27, yy), (27 if yy != 30 else 8, yy)], 'ink', 5, .35)
    for xx in [-12, 12]:
        circle(c, xx, 48, 4, 'ink')
    c.restore()


def recorder(c, x, y, t, scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    rect(c, -165, -115, 330, 230, 'coral', 38)
    rect(c, -142, -92, 284, 153, 'ink', 22)
    for i in range(6):
        height = 22+28*(1+math.sin(t*2+i*.8))
        rect(c, -108+i*41, 30-height, 22, height, 'mint', 8)
    text(c, 'RUN RECORD', 0, 94, 22, 'ink', True)
    circle(c, -119, -75, 7, 'yellow', .5+.5*math.sin(t*3)**2)
    c.restore()


def lens(c, x, y, radius, t, fill='pink'):
    circle(c, x, y, radius, fill, .15)
    circle(c, x, y, radius, fill, 1, 13)
    line(c, [(x+radius*.72, y+radius*.72), (x+radius*1.23, y+radius*1.23)], fill, 30)
    circle(c, x-radius*.3, y-radius*.36, radius*.14, 'white', .32+.08*math.sin(t))


def evidence(c, x, y, value, category, width=580):
    fill = {'OBSERVED': 'mint', 'DOCUMENTED': 'blue', 'UNKNOWN': 'coral'}[category]
    rect(c, x-width/2, y-38, width, 76, 'panel', 16)
    chip(c, category, x-width/2+94, y, 163, fill, 19, 43)
    text(c, value, x-width/2+194, y+9, 25, 'white', align='left', max_width=width-212)


class Film:
    SCENES = {
        1: {'library', 'moving', 'areas', 'rewrite', 'controller', 'settings', 'snapshot', 'compare'},
        2: {'qualities', 'rationale', 'input', 'rank', 'backwards', 'layers', 'observations', 'mental'},
        3: {'inputs', 'architecture', 'exactness', 'training', 'audit', 'continuity', 'evaluation', 'require'},
    }

    def __init__(self, episode, timeline):
        self.episode, self.timeline = episode, timeline
        self.number, self.accent = int(episode['id'][:2]), episode['accent']
        self.stars = np.random.default_rng(1515).uniform([20, 246, 1], [1900, 813, 3], (50, 3))

    def at(self, scene, word, fallback=5):
        take = next((v for v in self.timeline.get('takes', []) if v['id'] == scene), None)
        if take:
            hits = [w for w in take['words'] if w['text'].lower().strip('.,!?;:\'') == word.lower()]
            if hits:
                return hits[0]['start']-self.timeline['scenes'][scene][0]
        return fallback

    def draw(self, c, t):
        c.clear(color('bg'))
        circle(c, -70, 570, 370, 'panel', .6)
        circle(c, 1990, 435, 390, 'panel2', .38)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+8*math.sin(t*.1+i), y+5*math.cos(t*.14+i), r, 'muted', .45)
        name = next((s for s, (a, b) in self.timeline['scenes'].items() if a <= t < b), self.episode['scenes'][-1]['id'])
        scene = next(s for s in self.episode['scenes'] if s['id'] == name)
        a, b = self.timeline['scenes'][name]
        u, p = t-a, clamp((t-a)/(b-a))
        text(c, f'CHAPTER 15   /   FILM {self.number:02d}', 105, 79, 25, self.accent, True, 'left')
        text(c, self.episode['subtitle'], 1815, 79, 24, 'muted', align='right', max_width=1190)
        text(c, scene['title'], 960, 176+(1-pop(u/.7))*25, 60, 'white', True, max_width=1710)
        c.save()
        c.translate(0, (1-pop(u/.7))*35)
        (self.documentation, self.inspection, self.procurement)[self.number-1](c, name, u, p)
        c.restore()
        rect(c, 155, 843, 1610, 78, 'panel', 36)
        text(c, scene['claim'], 960, 892, 31, self.accent, True, max_width=1530)
        text(c, 'Adapted from Chapter 15 · Aaron Tay', 105, 947, 20, 'muted', align='left')
        for i, s in enumerate(self.episode['scenes']):
            circle(c, 1652+22*i, 939, 5, self.accent if s['id'] == name else 'panel2')
        if b-t < .28 and scene != self.episode['scenes'][-1]:
            q = smooth((.28-(b-t))/.28)
            rect(c, 1920-1920*q, 235, 1920*q, 580, self.accent, 0)

    def documentation(self, c, name, t, p):
        if name == 'library':
            orbit(c, 960, 515, 215, t)
            robot(c, 960, 528, t, 1.05, 'yellow')
            for i, (x, title, sub, fill) in enumerate([(345, 'TRANSFORM', 'what was searched?', 'mint'),
                    (1575, 'RETRIEVE', 'which candidates?', 'blue'),
                    (345, 'ORDER', 'fusion and reranking', 'pink'), (1575, 'PRESENT', 'what reached the reader?', 'yellow')]):
                y = 350 if i < 2 else 661
                box(c, x, y, title, sub, fill, 440, 130)
                flow(c, 590 if x < 960 else 1330, y, 790 if x < 960 else 1130, 488 if i < 2 else 578, t, fill)
            recorder(c, 960, 745, t, .42)
        elif name == 'moving':
            chip(c, 'SAME INPUT', 960, 288, 420, 'mint', 31)
            for x, label, fill, ids in [(525, 'SAVED RUN', 'blue', 'ABCP'), (1395, 'LATER RUN', 'pink', 'CAPD')]:
                orbit(c, x, 489, 150, t, fill)
                for i, ident in enumerate(ids):
                    aa = i*math.tau/4+t*.1
                    record(c, x+math.cos(aa)*128, 489+math.sin(aa)*94, ident, fill, .66)
                text(c, label, x, 700, 31, fill, True)
            flow(c, 760, 495, 1150, 495, t, 'yellow')
            box(c, 960, 727, 'CONDITIONS CAN CHANGE', 'records • index • model • ranking', 'yellow', 620, 120)
            banner(c, 'Schematic results illustrate change; they do not measure a product', 818)
        elif name == 'areas':
            recorder(c, 960, 530, t, .86)
            for i, (x, y, title, sub, fill) in enumerate([(390, 352, '01  INTERPRETATION', 'inputs, rewrites, filters', 'mint'),
                    (1530, 352, '02  CANDIDATES', 'index, fields, units, cut-offs', 'blue'),
                    (390, 690, '03  ORDERING', 'ranking, fusion, component lists', 'pink'),
                    (1530, 690, '04  CONTROL', 'rules, route, actual trajectory', 'yellow')]):
                box(c, x, y, title, sub, fill, 520, 155)
                flow(c, 675 if x < 960 else 1245, y, 815 if x < 960 else 1105, 463 if y < 500 else 597, t, fill)
        elif name == 'rewrite':
            box(c, 455, 348, 'ORIGINAL QUESTION', 'Does open access increase citations?', 'blue', 650, 155)
            robot(c, 960, 474, t, .88, 'yellow')
            flow(c, 815, 348, 900, 375, t, 'blue')
            flow(c, 1040, 491, 1220, 535, t, 'mint')
            box(c, 1430, 566, 'ACTUAL RETRIEVAL INPUT', MOCK_TRACE['transformed'], 'mint', 680, 160)
            recorder(c, 447, 640, t, .63)
            flow(c, 1080, 600, 666, 640, t, 'mint')
            text(c, 'SAVE THE EXACT TRANSFORMATION', 447, 781, 28, 'mint', True)
            banner(c, 'Illustrative rewrite from the chapter: reuse the saved input, or generate a new one?', 818)
        elif name == 'controller':
            for i, (x, title, fill) in enumerate([(390, 'FIXED', 'blue'), (960, 'ADAPTIVE', 'mint'), (1530, 'AGENTIC', 'pink')]):
                rect(c, x-240, 305, 480, 403, 'panel', 33)
                text(c, title, x, 359, 35, fill, True)
                if i == 0:
                    for j in range(3):
                        circle(c, x-145+j*145, 475, 35, fill)
                        text(c, str(j+1), x-145+j*145, 486, 25, 'ink', True)
                        if j < 2:
                            flow(c, x-100+j*145, 475, x-45+j*145, 475, t, fill)
                    wrap(c, 'Planned sequence and configuration', x, 621, 380, 27)
                elif i == 1:
                    circle(c, x-135, 495, 32, fill)
                    for j, yy in enumerate([437, 552]):
                        flow(c, x-94, 495, x+60, yy, t, fill if j == 0 else 'muted')
                        circle(c, x+100, yy, 32, fill if j == 0 else 'panel2')
                    wrap(c, 'Chosen branch and selection rule', x, 621, 380, 27)
                else:
                    for j, (xx, yy) in enumerate([(x-100, 460), (x+115, 468), (x, 568)]):
                        circle(c, xx, yy, 32, fill)
                        text(c, str(j+1), xx, yy+9, 23, 'ink', True)
                    flow(c, x-59, 460, x+ 70, 468, t, fill)
                    flow(c, x+ 90, 500, x+28, 540, t, fill)
                    arrow(c, x-30, 550, x-84, 492, 'yellow', 4)
                    wrap(c, 'Actions, observations, limits, stop', x, 648, 405, 27)
            banner(c, 'A classifier or model choosing a predefined branch does not itself make the workflow agentic')
        elif name == 'settings':
            robot(c, 960, 517, t, .9, 'yellow')
            orbit(c, 960, 515, 193, t, 'mint')
            labels = [('ANALYSIS', 'query and index', 'mint'), ('INDEXED UNITS', 'fields and chunking', 'blue'),
                      ('MODEL', 'encoder and tokeniser', 'pink'), ('SCORING', 'weights and similarity', 'yellow'),
                      ('PROCEDURE', 'exact / ANN settings', 'coral'), ('BOUNDARIES', 'k and thresholds', 'violet')]
            for i, (title, sub, fill) in enumerate(labels):
                xx = 385 if i < 3 else 1535
                yy = 323+(i%3)*184
                box(c, xx, yy, title, sub, fill, 485, 130)
                flow(c, 650 if xx < 960 else 1270, yy, 805 if xx < 960 else 1115, 515, t, fill)
            banner(c, 'Repeatability depends on the complete retrieval configuration')
        elif name == 'snapshot':
            rect(c, 175, 280, 800, 503, 'panel2', 35)
            text(c, 'SEARCH LOG', 575, 343, 36, 'mint', True)
            fields = ['Input and visible transformation', 'Product, mode, date, filters', 'Count and result identifiers', 'Raw export and observed limitations']
            for i, value in enumerate(fields):
                yy = 418+i*88
                circle(c, 239, yy-10, 8, 'mint')
                text(c, value, 270, yy, 28, 'white', align='left', max_width=655)
            evidence(c, 1370, 380, 'P displayed at rank 3', 'OBSERVED', 680)
            evidence(c, 1370, 509, 'Method described by vendor', 'DOCUMENTED', 680)
            evidence(c, 1370, 638, 'Internal model version', 'UNKNOWN', 680)
            banner(c, 'These category examples are schematic; an unknown setting is not a recorded fact')
        elif name == 'compare':
            for x, title, fill, ids in [(495, 'BASELINE', 'mint', 'ABPC'), (1425, 'LATER RUN', 'pink', 'BPDA')]:
                box(c, x, 326, title, 'saved inputs + exported identifiers', fill, 670, 125)
                for i, ident in enumerate(ids):
                    record(c, x-210+i*140, 527+7*math.sin(t+i), ident, fill, .82)
                text(c, 'VERSION / DATE / CONFIGURATION', x, 664, 24, 'muted')
            lens(c, 960, 536, 79, t, 'yellow')
            box(c, 960, 739, 'COMPARE RECORDS AND RANKS', 'Changed inputs? Changed system? Both?', 'yellow', 790, 125)

    def inspection(self, c, name, t, p):
        if name == 'qualities':
            for i, (x, title, sub, fill) in enumerate([(390, 'TRANSPARENCY', 'What is exposed?', 'blue'),
                    (960, 'INTERPRETABILITY', 'Why this result?', 'pink'),
                    (1530, 'UNDERSTANDABILITY', 'Can I form a useful mental model?', 'yellow')]):
                orbit(c, x, 443, 125, t, fill)
                if i == 0:
                    recorder(c, x, 443, t, .53)
                elif i == 1:
                    record(c, x, 432, 'P', 'white', .8)
                    lens(c, x+33, 447, 67, t, fill)
                else:
                    robot(c, x, 451, t, .64, fill)
                box(c, x, 684, title, sub, fill, 490, 163)
            banner(c, 'One quality does not automatically supply the other two', 818)
        elif name == 'rationale':
            rect(c, 150, 295, 1010, 389, 'panel2', 40)
            text(c, 'GENERATED RATIONALE', 655, 355, 27, 'pink', True)
            wrap(c, '“This paper closely addresses your question about open access and citations.”', 655, 443, 840, 42, 'white', True)
            polygon(c, [(1040, 665), (1160, 705), (1110, 624)], 'panel2')
            paper(c, 1500, 514, 'PAPER P', ['open access', 'citations'], t, .9)
            chip(c, 'RANK 3', 1500, 719, 310, 'pink', 32)
            banner(c, 'HYPOTHETICAL FIGURE 15.1 · Plausible relevance description; no executed stage established')
        elif name == 'input':
            box(c, 960, 326, 'ORIGINAL INPUT', MOCK_TRACE['original'], 'blue', 1100, 132)
            flow(c, 960, 409, 960, 450, t, 'mint')
            box(c, 960, 518, 'TRANSFORMED QUERY', MOCK_TRACE['transformed'], 'mint', 1100, 125)
            for x, title, sub, fill in [(485, 'ROUTE', 'lexical retrieval over indexed abstracts', 'blue'),
                    (1435, 'MATCHED EVIDENCE', 'P contains “open access” and “citations”', 'pink')]:
                flow(c, 775 if x < 960 else 1145, 592, x, 642, t, fill)
                box(c, x, 717, title, sub, fill, 730, 140)
            banner(c, 'Mock facts are a trace only if supplied by the executed search', 820)
        elif name == 'rank':
            q = smooth((t-self.at(name, 'moved', 9))/1.7)
            box(c, 460, 360, 'CANDIDATE RANK', '18 of 100 supplied candidates', 'blue', 660, 140)
            box(c, 1470, 360, 'AFTER RERANKING', 'rank 3 • first 10 displayed', 'pink', 660, 140)
            flow(c, 840, 360, 1090, 360, t, 'yellow')
            text(c, 'DISPLAYED TOP 10', 960, 499, 28, 'muted', True)
            rect(c, 240, 530, 1450, 201, 'panel', 30)
            for i in range(10):
                x = 330+i*140
                text(c, str(i+1), x, 561, 23, 'muted')
                if i != MOCK_TRACE['final_rank']-1:
                    record(c, x, 635, chr(65+i), 'panel2', .63)
            record(c, 460+(610-460)*q, 513+(635-513)*q, 'P', 'pink', .86)
            evidence(c, 960, 788, 'Reranker internal scoring', 'UNKNOWN', 800)
        elif name == 'backwards':
            stages = [('DISPLAY', 'fusion, deduplication, labels'), ('ORDERING', 'scores, reranker, cut-off'),
                      ('EVIDENCE', 'what actually matched?'), ('CANDIDATE SOURCE', 'retriever, unit, route'),
                      ('TRANSFORMED INPUT', 'what was actually sent?'), ('ORIGINAL INPUT', 'what the user entered')]
            coords = [(420, 373), (960, 373), (1500, 373), (1500, 670), (960, 670), (420, 670)]
            active = min(5, int(p*6))
            for i, ((title, sub), (x, y)) in enumerate(zip(stages, coords)):
                box(c, x, y, title, sub, 'pink' if i <= active else 'muted', 465, 155)
                circle(c, x-202, y-54, 17, 'pink' if i <= active else 'panel')
                text(c, str(i+1), x-202, y-48, 16, 'ink', True)
                if i < 5:
                    xx, yy = coords[i+1]
                    if yy == y:
                        sign = 1 if xx > x else -1
                        flow(c, x+sign*242, y, xx-sign*242, yy, t, 'pink')
                    else:
                        flow(c, x, y+ 90, xx, yy- 90, t, 'pink')
            banner(c, 'FIGURE 15.2 · Backwards inspection of recorded stages, not system execution order', 809)
        elif name == 'layers':
            labels = [('BOOLEAN', 'eligibility conditions', 'not relevance', 'mint'),
                      ('LEXICAL', 'score contributions', 'not a probability', 'blue'),
                      ('DENSE', 'unit and similarity', 'not every latent cause', 'pink'),
                      ('ALIGNMENTS', 'an inspectable layer', 'not the whole decision', 'yellow'),
                      ('DISPLAY', 'highlight and snippet', 'not ranking proof', 'coral')]
            for i, (title, sub, limit, fill) in enumerate(labels):
                x = 300+i*330
                rect(c, x-150, 305, 300, 441, 'panel', 29)
                text(c, title, x, 362, 28, fill, True)
                record(c, x, 481, 'P', fill, .75)
                if i in [2, 3]:
                    orbit(c, x, 481, 84, t, fill)
                wrap(c, sub, x, 604, 258, 26, 'white')
                wrap(c, limit, x, 686, 258, 23, 'muted')
            banner(c, 'Read what each exposed layer can show together with what it cannot establish')
        elif name == 'observations':
            labels = [('ACTION 1', 'query source A', 'blue'), ('OBSERVATION', 'returned records', 'mint'),
                      ('ACTION 2', 'query source B', 'pink'), ('STOP', 'record the decision', 'yellow')]
            for i, (title, sub, fill) in enumerate(labels):
                x = 330+i*420
                circle(c, x, 430, 74, fill, .13)
                circle(c, x, 430, 74, fill, 1, 5)
                if i == 1:
                    record(c, x, 430, 'P', fill, .68)
                else:
                    text(c, '1' if i == 0 else '2' if i == 2 else '■', x, 449, 50, fill, True)
                if i < 3:
                    flow(c, x+ 90, 430, x+330, 430, t, fill)
                box(c, x, 621, title, sub, fill, 350, 126)
            box(c, 960, 758, 'ACTUAL CALLS + RETURNED OBSERVATIONS', 'Keep narrated reasoning labelled as interpretation', 'pink', 1200, 110)
        elif name == 'mental':
            robot(c, 483, 495, t, 1.1, 'yellow')
            lens(c, 483, 490, 185, t)
            for i, (title, sub, fill) in enumerate([('SAVE', 'inputs, versions, outputs', 'mint'),
                    ('TRACE', 'admission, scoring, ordering', 'pink'), ('ACT', 'diagnose, compare, test', 'yellow')]):
                box(c, 1290, 333+i*190, title, sub, fill, 790, 140)
            banner(c, 'An accurate mental model and an actionable trail can leave model internals unknown', 817)

    def groups(self, c, active, t):
        titles = ['CONTROL', 'ARCHITECTURE', 'EXACTNESS', 'AUDITABILITY', 'CONTINUITY', 'EVALUATION']
        for i, title in enumerate(titles):
            x = 275+i*275
            fill = 'yellow' if i == active else 'panel2'
            rect(c, x-259/2, 782-51/2, 259, 51, fill, 20)
            text(c, f'{i+1}  {title}', x, 789, 19, 'ink' if i == active else 'muted', True)
            if i == active:
                circle(c, x, 822, 4+2*math.sin(t)**2, 'yellow')

    def procurement(self, c, name, t, p):
        if name == 'inputs':
            robot(c, 960, 471, t, .78, 'yellow')
            orbit(c, 960, 466, 153, t, 'yellow')
            for i, (label, sub) in enumerate([('TEXT', 'question or task brief'), ('FIELDS', 'controlled search'), ('SEED RECORD', 'start with a paper'),
                                              ('CITATIONS', 'follow links'), ('JUDGEMENTS', 'recorded feedback'), ('API', 'structured predicates')]):
                x, y = (385 if i < 3 else 1535), 305+(i%3)*145
                box(c, x, y, label, sub, 'yellow' if i%2 == 0 else 'blue', 465, 112)
                flow(c, 650 if x < 960 else 1270, y, 820 if x < 960 else 1100, 467, t, 'yellow')
            text(c, 'Inspect interpretations, export transformed inputs, record routes and limits', 960, 717, 26, 'muted')
            self.groups(c, 0, t)
        elif name == 'architecture':
            for i, (x, title, sub, fill) in enumerate([(360, 'LEXICAL', 'indexed abstracts', 'mint'),
                    (360, 'DENSE', 'embedded passages', 'blue'), (950, 'FUSION', 'component lists + cut-offs', 'yellow'),
                    (1530, 'RERANK', 'merged candidates', 'pink')]):
                y = 334 if i == 0 else 547 if i == 1 else 440
                box(c, x, y, title, sub, fill, 440, 131)
                if i < 2:
                    flow(c, x+240, y, 705, 440, t, fill)
                elif i == 2:
                    flow(c, x+240, y, 1287, y, t, fill)
            for i in range(5):
                record(c, 255+i* 80, 686+4*math.sin(t+i), f'P{i+1}', 'blue', .43)
            flow(c, 656, 686, 815, 686, t, 'yellow')
            box(c, 1120, 670, 'ONE PAPER, MANY CHUNKS?', 'assemble • retain best • show duplicates?', 'yellow', 780, 100)
            text(c, 'Illustrative architecture • ask what the product actually indexes and how each model is used', 960, 747, 24, 'muted')
            self.groups(c, 1, t)
        elif name == 'exactness':
            for x, title, ident, fill in [(485, 'EXACT REQUIREMENT', 'GENE-17', 'mint'), (1435, 'NEAR-DUPLICATE NAME', 'GENE-71', 'coral')]:
                box(c, x, 338, title, '', fill, 740, 115)
                record(c, x, 496, 'ID', fill, .7)
                chip(c, ident, x, 630, 410, fill, 46)
            lens(c, 960, 498, 87, t, 'yellow')
            text(c, 'Also test punctuation, hyphens, exact phrases, negation, and exclusions', 960, 720, 28, 'muted')
            self.groups(c, 2, t)
        elif name == 'training':
            for i, (title, fill) in enumerate([('WEB QUERIES', 'mint'), ('Q–A PAIRS', 'blue'), ('CITATION LINKS', 'pink'), ('SCHOLARLY JUDGEMENTS', 'yellow')]):
                x = 320+i*425
                chip(c, title, x, 325, 380, fill, 27, 72)
                for j in range(3):
                    yy = 400+((t*40+j* 60)%125)
                    circle(c, x+25*math.sin(t+j), yy, 8, fill)
                flow(c, x, 537, 960+(i-1.5)*65, 572, t, fill)
            robot(c, 960, 620, t, .7, 'yellow')
            text(c, 'Different training signals teach different behaviours', 960, 733, 30, 'white', True)
            self.groups(c, 2, t)
        elif name == 'audit':
            recorder(c, 440, 470, t, .97)
            chip(c, 'EXPORT THE RUN', 440, 696, 460, 'mint', 30)
            for i, (title, sub, fill) in enumerate([('EXECUTION TRACE', 'actual route, evidence, ordering', 'pink'),
                    ('SAVED INPUTS', 'reuse, or generate again?', 'mint'), ('CHANGE RECORD', 'model, index, ranking, date', 'yellow')]):
                box(c, 1310, 309+i*170, title, sub, fill, 830, 126)
            flow(c, 646, 472, 855, 472, t, 'mint')
            self.groups(c, 3, t)
        elif name == 'continuity':
            rect(c, 195, 300, 680, 419, 'panel', 34)
            text(c, 'WHEN THE BUDGET ENDS', 535, 363, 32, 'yellow', True)
            rect(c, 310, 415, 440, 103, 'yellow', 14, 1, 6)
            rect(c, 754, 443, 18, 46, 'yellow', 5)
            remaining = .15+.65*(1-p)
            rect(c, 325, 430, 410*remaining, 73, 'yellow', 8)
            text(c, 'REFUSE? TRUNCATE? SEARCH LESS?', 535, 595, 25, 'white', True)
            text(c, 'Expose per-query use and limits', 535, 658, 28, 'muted')
            rect(c, 1035, 300, 680, 419, 'panel', 34)
            text(c, 'WHEN A MODE IS RETIRED', 1375, 363, 32, 'pink', True)
            recorder(c, 1280, 507, t, .61)
            record(c, 1570, 504, 'P', 'mint', .81)
            flow(c, 1400, 507, 1510, 507, t, 'mint')
            text(c, 'NOTICE + EXPORT BEFORE WITHDRAWAL', 1375, 655, 26, 'white', True)
            self.groups(c, 4, t)
        elif name == 'evaluation':
            labels = [('IDENTIFIERS', 'mint'), ('LANGUAGES', 'blue'), ('DOCUMENT TYPES', 'pink'), ('KNOWN FAILURES', 'yellow')]
            text(c, 'LOCAL TEST SET', 420, 301, 28, 'yellow', True)
            for i, (label, fill) in enumerate(labels):
                chip(c, label, 420, 387+i* 80, 470, fill, 27, 61)
            recorder(c, 960, 505, t, .72)
            flow(c, 698, 495, 799, 495, t, 'yellow')
            flow(c, 1106, 495, 1211, 495, t, 'yellow')
            box(c, 1510, 372, 'BEFORE', 'saved baseline and judgements', 'mint', 530, 128)
            box(c, 1510, 575, 'AFTER UPDATE', 'compare each query and the average', 'pink', 530, 140)
            text(c, 'Schematic protocol • no benchmark result or product score is claimed', 960, 720, 27, 'muted')
            self.groups(c, 5, t)
        elif name == 'require':
            for i, (x, title, sub, fill) in enumerate([(390, 'VISIBILITY', 'establish what was searched', 'mint'),
                    (960, 'DOCUMENTATION', 'rerun or compare later', 'pink'), (1530, 'CONTROL', 'test against local needs', 'yellow')]):
                orbit(c, x, 428, 112, t, fill)
                if i == 0:
                    lens(c, x-14, 409, 58, t, fill)
                elif i == 1:
                    recorder(c, x, 420, t, .51)
                else:
                    robot(c, x, 437, t, .61, fill)
                box(c, x, 647, title, sub, fill, 490, 142)
            banner(c, '19 questions • answers • evidence • library verification • follow-up', 800, 'yellow')
