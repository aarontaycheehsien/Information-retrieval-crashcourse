"""Original geometric animation for Chapter 14's cosmic evaluation laboratory."""
from __future__ import annotations

import math
import numpy as np
from visuals import (arrow, chip, circle, clamp, color, flow, font, line,
                     paper, polygon, pop, rect, robot, smooth, text)

RELEVANT = frozenset('ABCDEFGHIJ')
BEFORE = list('AKLMBNOPQR') + list('CDEFGHIJST')
AFTER = list('ABKCDLEM FN'.replace(' ', '')) + list('GHIJOPQRST')
AP_A, AP_B = [1, 0, 1, 0, 1], [0, 1, 0, 1, 1]
GRADES_A, GRADES_B = [3, 0, 1], [1, 0, 3]
ROWS_BEFORE, ROWS_AFTER = [.3, .2, .4], [.1, .5, .4]


def precision_at(ranking, relevant, depth):
    """Fixed-depth denominator; examples always contain at least depth records."""
    assert depth > 0 and len(ranking) >= depth
    return sum(v in relevant for v in ranking[:depth]) / depth


def recall(ranking, relevant):
    assert relevant
    return len(set(ranking) & set(relevant)) / len(relevant)


def reciprocal_rank(labels):
    return next((1/i for i, value in enumerate(labels, 1) if value), 0.)


def average_precision(labels, total_relevant):
    assert total_relevant > 0 and sum(labels) <= total_relevant
    hits, gain = 0, 0.
    for rank, value in enumerate(labels, 1):
        if value:
            hits += 1
            gain += hits/rank
    return gain/total_relevant


def dcg(grades):
    return sum((2**grade-1)/math.log2(rank+1) for rank, grade in enumerate(grades, 1))


def ndcg(grades):
    ideal = dcg(sorted(grades, reverse=True))
    return dcg(grades)/ideal if ideal else 0.


def validate_examples():
    assert len(BEFORE) == len(AFTER) == len(set(BEFORE)) == 20
    assert set(BEFORE) == set(AFTER)
    assert precision_at(BEFORE, RELEVANT, 10) == recall(BEFORE[:10], RELEVANT) == .2
    assert precision_at(AFTER, RELEVANT, 10) == recall(AFTER[:10], RELEVANT) == .6
    assert recall(BEFORE, RELEVANT) == recall(AFTER, RELEVANT) == 1
    assert math.isclose(average_precision(AP_A, 3), 34/45)
    assert math.isclose(average_precision(AP_B, 3), 8/15)
    assert round(ndcg(GRADES_A), 3) == .983
    assert round(ndcg(GRADES_B), 3) == .590
    assert round(sum(ROWS_BEFORE)/3, 2) == .30
    assert round(sum(ROWS_AFTER)/3, 2) == .33


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
        text(c, row, x, y+i*size*1.25, size, fill, bold)


def box(c, x, y, title, subtitle='', fill='mint', width=380, height=140):
    rect(c, x-width/2, y-height/2, width, height, 'panel2', 26)
    text(c, title, x, y-7 if subtitle else y+12, 34, fill, True, max_width=width-35)
    if subtitle:
        wrap(c, subtitle, x, y+35, width-35, 25)


def orbit(c, x, y, radius, t, fill='mint'):
    circle(c, x, y, radius, fill, .28, 3)
    for i in range(6):
        a = t*.17+i*math.tau/6
        circle(c, x+math.cos(a)*radius, y+math.sin(a)*radius, 7, fill)


def doc(c, x, y, ident, relevant=True, scale=1, alpha=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    fill = 'yellow' if relevant is None else 'mint' if relevant else 'panel2'
    rect(c, -49, -61, 98, 122, fill, 16, alpha)
    polygon(c, [(22, -61), (49, -34), (22, -34)], 'white', .6*alpha)
    text(c, str(ident), 0, -19, 30, 'ink' if relevant else 'white', True)
    rect(c, -30, -4, 60, 28, 'ink', 12, alpha)
    for offset in [-13, 13]:
        circle(c, offset, 9, 5, 'mint' if relevant else 'muted', alpha)
    text(c, '?' if relevant is None else 'R' if relevant else 'N', 0, 47, 22, 'ink' if relevant is None or relevant else 'muted', True)
    c.restore()


def gauge(c, x, y, value, title, subtitle, fill='mint', radius=105):
    circle(c, x, y, radius, 'panel2', 1, 22)
    pts = [(x+radius*math.cos(-math.pi/2+i*math.tau/100),
            y+radius*math.sin(-math.pi/2+i*math.tau/100)) for i in range(int(100*clamp(value))+1)]
    if len(pts) > 1:
        line(c, pts, fill, 22)
    text(c, f'{value:.0%}', x, y+19, 52, 'white', True)
    text(c, title, x, y+radius+60, 32, fill, True)
    text(c, subtitle, x, y+radius+104, 27, 'muted')


def ranked(c, labels, x, y, t, fill='pink', width=720, identities=None):
    count = len(labels)
    step = width/count
    for i, value in enumerate(labels):
        xx = x+(i+.5)*step
        text(c, str(i+1), xx, y-78, 22, 'muted')
        doc(c, xx, y+4*math.sin(t*1.5+i), identities[i] if identities else chr(65+i), bool(value), min(1, step/115))
        if value:
            circle(c, xx, y+91, 6, fill)


def banner(c, value, y=774, fill='muted'):
    text(c, value, 960, y, 27, fill, max_width=1620)


class Film:
    SCENES = {
        1: {'need', 'lenses', 'fractions', 'depth', 'denominator', 'rerank', 'ceiling', 'fresh'},
        2: {'order', 'pk', 'mrr', 'map', 'ndcg', 'diversity', 'budgets', 'choose'},
        3: {'collection', 'pool', 'transfer', 'local', 'protocol', 'probes', 'average', 'audit'},
    }

    def __init__(self, episode, timeline):
        self.episode, self.timeline = episode, timeline
        self.number, self.accent = int(episode['id'][:2]), episode['accent']
        self.stars = np.random.default_rng(1414).uniform([20, 245, 1], [1900, 815, 3], (48, 3))

    def at(self, scene, word, fallback=5):
        take = next((v for v in self.timeline.get('takes', []) if v['id'] == scene), None)
        if take:
            hits = [w for w in take['words'] if w['text'].lower().strip('.,!?;:\'') == word.lower()]
            if hits:
                return hits[0]['start']-self.timeline['scenes'][scene][0]
        return fallback

    def draw(self, c, t):
        c.clear(color('bg'))
        circle(c, -90, 590, 330, 'panel', .7)
        circle(c, 2010, 450, 375, 'panel2', .35)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+7*math.sin(t*.12+i), y+5*math.cos(t*.11+i), r, 'muted', .5)
        name = next((s for s, (a, b) in self.timeline['scenes'].items() if a <= t < b), self.episode['scenes'][-1]['id'])
        scene = next(s for s in self.episode['scenes'] if s['id'] == name)
        a, b = self.timeline['scenes'][name]
        u, p = t-a, clamp((t-a)/(b-a))
        text(c, f'CHAPTER 14   /   FILM {self.number:02d}', 105, 79, 25, self.accent, True, 'left')
        text(c, self.episode['subtitle'], 1815, 79, 24, 'muted', align='right', max_width=1210)
        text(c, scene['title'], 960, 177+(1-pop(u/.65))*25, 61, 'white', True, max_width=1710)
        c.save()
        c.translate(0, (1-pop(u/.65))*35)
        (self.coverage, self.metrics, self.evaluation)[self.number-1](c, name, u, p)
        c.restore()
        rect(c, 155, 843, 1610, 78, 'panel', 36)
        text(c, scene['claim'], 960, 892, 32, self.accent, True, max_width=1530)
        text(c, 'Adapted from Chapter 14 · Aaron Tay', 105, 947, 20, 'muted', align='left')
        for i, s in enumerate(self.episode['scenes']):
            circle(c, 1652+22*i, 939, 5, self.accent if s['id'] == name else 'panel2')
        if b-t < .28 and scene != self.episode['scenes'][-1]:
            q = smooth((.28-(b-t))/.28)
            rect(c, 1920-1920*q, 235, 1920*q, 580, self.accent, 0)

    def coverage(self, c, name, t, p):
        if name == 'need':
            paper(c, 960, 478, 'ONE PAPER', ['same text'], t, .88)
            for i, (x, title, sub, fill) in enumerate([(340, 'RESEARCHER', 'needs this method', 'mint'),
                    (960, 'BEGINNER', 'needs an overview', 'blue'), (1580, 'REVIEWER', 'applies inclusion criteria', 'coral')]):
                box(c, x, 719, title, sub, fill, 440, 125)
                if i != 1:
                    flow(c, 835 if i == 0 else 1085, 510, x+120 if i == 0 else x-120, 590, t, fill)
            orbit(c, 960, 475, 210, t)
        elif name == 'lenses':
            robot(c, 960, 540, t, 1.1, 'yellow')
            for i, (x, y, title, sub, fill) in enumerate([(440, 373, 'SYSTEM', 'estimated query fit', 'blue'),
                    (1480, 373, 'TOPICAL', 'about the subject?', 'mint'),
                    (440, 680, 'COGNITIVE', 'informative to this reader?', 'pink'),
                    (1480, 680, 'SITUATIONAL', 'useful for this task?', 'yellow')]):
                box(c, x, y, title, sub, fill, 470)
                flow(c, 720 if x < 960 else 1200, y, 870 if x < 960 else 1050, 515, t, fill)
        elif name == 'fractions':
            text(c, 'CONTROLLED FIGURE 14.1 · AFTER RERANKING', 960, 282, 25, 'muted')
            for i, ident in enumerate(AFTER[:10]):
                doc(c, 320+i*143, 378+4*math.sin(t+i), ident, ident in RELEVANT, .75)
            reveal = pop(t/2)
            gauge(c, 555, 582, .6*reveal, 'PRECISION@10', '6 relevant / 10 displayed')
            gauge(c, 1365, 582, .6*reveal, 'RECALL@10', '6 recovered / 10 total relevant', 'blue')
            text(c, 'Ten displayed records ≠ ten relevant records in the collection', 960, 817, 25, 'muted')
        elif name == 'depth':
            k = 5 if p < .28 else 10 if p < .62 else 20
            rect(c, 265, 314, 1390, 330, 'panel', 30)
            for i, ident in enumerate(AFTER):
                x, y = 345+(i%10)*137, 391+(i//10)*160
                doc(c, x, y, ident, ident in RELEVANT, .77, 1 if i < k else .4)
                if i == k-1:
                    circle(c, x, y, 72, 'yellow', 1, 5)
            for x, title, value, fill in [(480, 'DEPTH', str(k), 'yellow'),
                    (960, 'PRECISION', f'{precision_at(AFTER, RELEVANT, k):.0%}', 'mint'),
                    (1440, 'RECALL', f'{recall(AFTER[:k], RELEVANT):.0%}', 'blue')]:
                box(c, x, 733, title, value, fill, 350, 118)
            text(c, 'Same fixed ranking · complete toy collection', 960, 285, 27, 'muted')
        elif name == 'denominator':
            text(c, 'KNOWN SEEDS', 495, 307, 32, 'mint', True)
            for i in range(4):
                doc(c, 300+i*130, 464, str(i+1), True, .85, 1 if i < 3 else .35)
                text(c, 'FOUND' if i < 3 else 'MISSED', 300+i*130, 568, 21, 'mint' if i < 3 else 'coral', True)
            box(c, 495, 678, '3 / 4 = 75%', 'known-seed recovery', 'mint', 520)
            orbit(c, 1390, 482, 160, t, 'blue')
            circle(c, 1390, 482, 124, 'panel2')
            text(c, '?', 1390, 524, 118, 'blue', True)
            box(c, 1390, 710, 'ALL RELEVANT RECORDS', 'unknown in a live database', 'blue', 590, 120)
            banner(c, 'Seeds: some known relevant records · union: relevant records found by compared strategies', 810)
        elif name == 'rerank':
            q = smooth((t-self.at(name, 'After', 10))/2.2)
            text(c, 'SAME CANDIDATE POOL · TEN RELEVANT, TEN NON-RELEVANT', 960, 288, 27, 'muted')
            rect(c, 233, 335, 1454, 158, 'mint', 22, .1)
            for ident in BEFORE:
                ia, ib = BEFORE.index(ident), AFTER.index(ident)
                xa, ya = 315+(ia%10)*143, 407+(ia//10)*181
                xb, yb = 315+(ib%10)*143, 407+(ib//10)*181
                doc(c, xa+(xb-xa)*q, ya+(yb-ya)*q, ident, ident in RELEVANT, .82)
            line(c, [(245, 503), (1675, 503)], 'yellow', 3)
            text(c, 'DISPLAY BOUNDARY: RANK 10', 960, 528, 23, 'yellow', True)
            label = '0.2 → 0.6' if q > .5 else '0.2'
            box(c, 540, 731, 'PRECISION@10 / RECALL@10', label, 'mint', 650, 115)
            box(c, 1410, 731, 'CANDIDATE RECALL', '1.0 throughout', 'blue', 580, 115)
        elif name == 'ceiling':
            rect(c, 270, 300, 960, 440, 'panel', 34)
            text(c, 'FIXED CANDIDATE SET', 750, 356, 30, 'mint', True)
            for i in range(6):
                angle = i*math.tau/6+t*.12
                doc(c, 750+290*math.cos(angle), 525+105*math.sin(angle), chr(65+i), i < 4, .73)
            line(c, [(1280, 287), (1280, 764)], 'coral', 12)
            paper(c, 1565, 493, 'EXCLUDED', ['relevant'], t, .78)
            text(c, 'Cannot rank a record', 1570, 701, 30, 'coral', True)
            text(c, 'that is not a candidate', 1570, 743, 29, 'muted')
        elif name == 'fresh':
            rect(c, 290, 315, 900, 390, 'panel', 34)
            text(c, 'CUMULATIVE POOL', 740, 363, 30, 'mint', True)
            for i in range(4):
                doc(c, 460+i*180, 520, chr(65+i), i < 2, .92)
            box(c, 1510, 350, 'NEW RETRIEVAL', 'query · source · route · round', 'blue', 510)
            flow(c, 1420, 475, 1150, 655, t, 'blue')
            q = smooth(clamp((p-.25)/.25))
            doc(c, 1500-420*q, 550+95*q, 'E', True, .82)
            text(c, 'NEW RELEVANT', 1480, 724, 29, 'mint', True)
            text(c, 'Duplicate A: no gain', 570, 758, 28, 'muted')
            text(c, 'New non-relevant F: no gain', 1000, 758, 28, 'muted')

    def metrics(self, c, name, t, p):
        if name == 'order':
            robot(c, 360, 520, t, 1.18, 'pink')
            for y, labels, title in [(392, [1]+[0]*9, 'USEFUL FIRST'), (643, [0]*9+[1], 'USEFUL TENTH')]:
                text(c, title, 1130, y-106, 28, 'pink', True)
                ranked(c, labels, 570, y, t, width=1130,
                       identities=list('ABCDEFGHIJ') if y == 392 else list('BCDEFGHIJA'))
            banner(c, 'Same set membership · different reader experience', 801)
        elif name == 'pk':
            text(c, 'SCHEMATIC LISTS · TWO RELEVANT HITS IN EACH TOP TEN', 960, 280, 26, 'muted')
            ranked(c, [1,0,0,0,1,0,0,0,0,0], 240, 405, t, width=1180)
            ranked(c, [0,0,0,0,0,0,0,1,0,1], 240, 657, t, width=1180)
            for y in [405, 657]:
                box(c, 1630, y, 'P@10', '2 / 10 = 0.2', 'pink', 350, 140)
            line(c, [(1430, 318), (1430, 747)], 'yellow', 5)
        elif name == 'mrr':
            ranked(c, [0,1,0,0,1], 255, 393, t, width=880)
            ranked(c, [0,0,0,0,1], 255, 622, t, width=880)
            box(c, 1500, 393, 'QUERY 1: RR = 1/2', 'first relevant at rank 2', 'pink', 540)
            box(c, 1500, 622, 'QUERY 2: RR = 1/5', 'first relevant at rank 5', 'pink', 540)
            banner(c, 'MRR = (0.5 + 0.2) / 2 = 0.35 · later hits do not affect reciprocal rank', 800, 'pink')
        elif name == 'map':
            ranked(c, AP_A, 290, 377, t, width=1260)
            for i, frac in [(0, '1 / 1'), (2, '2 / 3'), (4, '3 / 5')]:
                box(c, 416+i*252, 594, 'PRECISION AT HIT', frac, 'pink', 295, 125)
            banner(c, 'AP = (1 + 2/3 + 3/5) / 3 = 0.756', 723, 'pink')
            banner(c, 'Complete toy judgement set: 3 relevant records · MAP averages AP across queries', 790)
        elif name == 'ndcg':
            q = smooth((t-self.at(name, 'third', 16)+4)/2)
            grades = GRADES_A if q < .5 else GRADES_B
            for i, grade in enumerate(grades):
                x = 425+i*535
                rect(c, x-135, 625-90*grade, 270, max(25, 90*grade), 'pink' if grade == 3 else 'blue', 20)
                text(c, f'GRADE {grade}', x, 305, 29, 'pink' if grade == 3 else 'blue', True)
                text(c, f'RANK {i+1}', x, 676, 28, 'muted')
                text(c, f'gain {2**grade-1}', x, 619-90*grade, 26, 'white', True)
            banner(c, f'nDCG@3 = DCG / ideal DCG = {ndcg(grades):.3f}', 750, 'pink')
            banner(c, 'Toy grades · gain = 2^grade − 1 · discount = 1 / log₂(rank + 1)', 803)
        elif name == 'diversity':
            for y, aspects, title in [(409, ['METHODS']*3, 'REPEATED ASPECT'),
                    (675, ['METHODS', 'IMPLEMENTATION', 'LIMITATIONS'], 'ASPECT COVERAGE')]:
                text(c, title, 335, y+8, 29, 'pink', True, max_width=400)
                for i, aspect in enumerate(aspects):
                    box(c, 780+i*390, y, aspect, 'individually useful', ['mint','blue','yellow'][i] if y == 675 else 'mint', 345, 135)
            banner(c, 'Aspect coverage requires additional judgements and a suitable metric', 803)
        elif name == 'budgets':
            for i, (title, value, sub, fill) in enumerate([('RETRIEVER', '100', 'candidate boundary', 'blue'),
                    ('RERANKER', '40', 'inspection budget', 'yellow'), ('EVALUATION', '10', 'judgement depth k', 'pink')]):
                x = 405+i*555
                orbit(c, x, 490, 158, t+i, fill)
                text(c, value, x, 520, 94, fill, True)
                text(c, title, x, 699, 34, fill, True)
                text(c, sub, x, 746, 29, 'muted')
                if i < 2:
                    flow(c, x+195, 490, x+360, 490, t, fill)
            text(c, 'ILLUSTRATIVE SETTINGS · NOT RECOMMENDATIONS', 960, 280, 26, 'muted')
        elif name == 'choose':
            robot(c, 960, 521, t, 1.12, 'pink')
            for x,y,title,sub,fill in [(440,377,'PRECISION@k','useful first page','mint'),
                    (1480,377,'MRR','first correct item','blue'), (440,693,'MAP','many early useful records','pink'),
                    (1480,693,'nDCG','graded usefulness early','yellow')]:
                box(c,x,y,title,sub,fill,480,145)
                flow(c, 720 if x < 960 else 1200, y, 855 if x < 960 else 1065, 520, t, fill)

    def evaluation(self, c, name, t, p):
        if name == 'collection':
            robot(c, 960, 505, t, 1.05, 'yellow')
            for i, (x,title,sub,fill) in enumerate([(370,'DOCUMENTS','fixed collection','blue'),
                    (960,'QUERIES','fixed topics / needs','pink'), (1550,'JUDGEMENTS','fixed relevance criteria','mint')]):
                box(c,x,730,title,sub,fill,470,142)
                flow(c,x,644,x,610,t,fill)
                if i != 1:
                    orbit(c,x,446,120,t,fill)
                    text(c,'FIXED',x,456,38,fill,True)
            text(c,'Compare systems against the same test conditions',960,286,29,'yellow',True)
        elif name == 'pool':
            box(c,380,360,'SYSTEM A','A · B · C','blue',420,130)
            box(c,380,635,'SYSTEM B','B · C · D','pink',420,130)
            for y,fill in [(360,'blue'),(635,'pink')]:
                flow(c,610,y,835,495,t,fill)
            rect(c,865,318,475,410,'panel',30)
            text(c,'JUDGED UNION',1100,366,30,'mint',True)
            for i, ident in enumerate('ABCD'):
                doc(c,995+(i%2)*205,475+(i//2)*160,ident,i%2==0,.75)
            doc(c,1605,493,'E',None,1.12)
            circle(c,1605,493,122,'yellow',1,5)
            text(c,'UNJUDGED',1605,689,31,'yellow',True)
            text(c,'relevance unknown',1605,731,27,'muted')
            banner(c,'Schematic result identities · useful E can receive no credit without a judgement',803)
        elif name == 'transfer':
            for x,title,fill in [(450,'BENCHMARK','blue'),(1450,'YOUR LIBRARY','yellow')]:
                circle(c,x,494,147,fill)
                orbit(c,x,494,176,t,fill)
                text(c,title,x,505,32,'ink',True,max_width=245)
            flow(c,690,494,1200,494,t,'muted')
            chip(c,'TRANSFER?',960,494,330,'pink',32)
            for i,(title,sub,fill) in enumerate([('LANGUAGES','what users search','yellow'),
                    ('COLLECTIONS','what is indexed','blue'), ('TASKS','what counts as useful','mint')]):
                box(c,420+i*540,742,title,sub,fill,450,123)
        elif name == 'local':
            rect(c,350,275,1200,490,'panel',35)
            text(c,'YOUR REUSABLE QUERY SET',960,336,34,'yellow',True)
            for i,(title,sub) in enumerate([('REFERENCE ENQUIRIES','real questions'),('CONSULTATIONS','discipline and task'),
                    ('TRAINING / ILL','language and document type'),('KNOWN FAILURES','deliberate stress tests')]):
                y=412+i*83
                text(c,f'{i+1:02d}',435,y,30,'yellow',True)
                text(c,title,520,y,29,'white',True,'left')
                text(c,sub,1470,y,27,'muted',align='right')
            banner(c,'30–50 is a starting range · construction and judging require time',809,'yellow')
        elif name == 'protocol':
            for i,(title,sub,fill) in enumerate([('CAPTURE','both runs at fixed depth','blue'),
                    ('POOL','deduplicate the union','pink'), ('JUDGE','same written criteria','mint')]):
                x=400+i*560
                box(c,x,423,title,sub,fill,450,160)
                if i<2:
                    flow(c,x+235,423,x+320,423,t,fill)
            box(c,590,686,'PRECISION@k','judge every pooled result','mint',630,155)
            box(c,1350,686,'SEED RECOVERY','report separately','yellow',630,155)
            text(c,'Mask the supplying run when judging, where feasible',960,300,29,'muted')
            banner(c,'Record fewer-than-k returns and the denominator convention',811)
        elif name == 'probes':
            for x,y,title,example,fill in [(460,394,'EXACT IDENTITY','SLC6A4 promoter polymorphism','blue'),
                    (1460,394,'INDEXED UNIT','phrase only in held full text','yellow'),
                    (460,695,'WORD MISMATCH','known item; almost no shared words','mint'),
                    (1460,695,'OPPOSITE MEANINGS','reduces / increases readmission','pink')]:
                box(c,x,y,title,example,fill,730,175)
                circle(c,x-310,y-43,10,fill)
            line(c,[(960,291),(960,784)],'panel2',4)
        elif name == 'average':
            text(c,'HYPOTHETICAL TABLE 14.3 · PRECISION@10',960,279,27,'muted')
            text(c,'BEFORE',1130,340,27,'blue',True)
            text(c,'AFTER',1515,340,27,'yellow',True)
            for i,(label,before,after) in enumerate(zip(['Identifier','Vocabulary mismatch','Composition pair mean'],ROWS_BEFORE,ROWS_AFTER)):
                y=421+i*116
                text(c,label,245,y+8,31,'white',True,'left')
                rect(c,1010,y-32,before*340,43,'blue',14)
                text(c,f'{before:.1f}',1245,y+2,31,'blue',True)
                rect(c,1400,y-32,after*340*pop(t/2),43,'coral' if i==0 else 'yellow',14)
                text(c,f'{after:.1f}',1705,y+2,31,'coral' if i==0 else 'yellow',True)
            box(c,740,751,'EQUALLY WEIGHTED ROW MEAN','0.30 → 0.33','yellow',820,110)
            box(c,1470,751,'IDENTIFIER LOSS','two thirds of precision','coral',530,110)
        elif name == 'audit':
            robot(c,960,508,t,1.07,'yellow')
            for x,y,title,sub,fill in [(440,365,'RECORD','queries · criteria · baseline','blue'),
                    (1480,365,'INSPECT','per-query changes · variation','pink'),
                    (440,690,'RERUN','updates · migration · renewal','mint'),
                    (1480,690,'DIAGNOSE','why retrieval or answers fail','yellow')]:
                box(c,x,y,title,sub,fill,510,145)
                flow(c,725 if x<960 else 1195,y,850 if x<960 else 1070,505,t,fill)
            banner(c,'A faithful generated answer still depends on its retrieved shortlist',809)
