"""Original colorful search cosmos: paper astronauts, machines, gates and lenses."""
from __future__ import annotations

import math
import numpy as np
import skia
from visuals import (arrow, check, chip, circle, clamp, color, flow, font, gate,
                     line, paper, polygon, pop, rect, robot, smooth, text)


def wrap(c, value, x, y, width=460, size=28, fill='muted', bold=False):
    rows, current = [], ''
    for word in value.split():
        candidate = (current + ' ' + word).strip()
        if current and font(size, bold).measureText(candidate) > width:
            rows.append(current)
            current = word
        else:
            current = candidate
    if current:
        rows.append(current)
    for i, row in enumerate(rows):
        text(c, row, x, y + i * size * 1.25, size, fill, bold)


def box(c, x, y, title, subtitle='', fill='mint', width=380, height=130):
    rect(c, x-width/2, y-height/2, width, height, 'panel2', 28)
    text(c, title, x, y-7 if subtitle else y+12, 33, fill, True, max_width=width-30)
    if subtitle:
        wrap(c, subtitle, x, y+33, width-30, 25)


def orbit(c, x, y, radius, t, fill='mint'):
    circle(c, x, y, radius, fill, .22, 3)
    for i in range(5):
        a = t*.19 + i*math.tau/5
        circle(c, x+math.cos(a)*radius, y+math.sin(a)*radius, 6, fill)


def archive(c, x, y, t, scale=1):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    circle(c, 0, 0, 180, 'violet')
    circle(c, -58, -42, 116, 'blue', .18)
    for i in range(4):
        xx = -111 + 68*i
        rect(c, xx, -95, 43, 174, ['mint', 'yellow', 'pink', 'coral'][i], 12)
        line(c, [(xx+10, -64), (xx+33, -64)], 'ink', 5)
        line(c, [(xx+10, 48), (xx+33, 48)], 'ink', 5)
    c.save()
    c.rotate(-18)
    c.scale(1, .36)
    circle(c, 0, 0, 248, 'mint', .65, 14)
    c.restore()
    orbit(c, 0, 0, 236, t, 'mint')
    c.restore()


def answer(c, x, y, t, scale=1, count=5):
    c.save()
    c.translate(x, y)
    c.scale(scale, scale)
    rect(c, -185, -135, 370, 270, 'white', 32)
    for i in range(count):
        yy = -86 + 39*i
        circle(c, -135, yy, 14, 'blue')
        text(c, str(i+1), -135, yy+6, 17, 'ink', True)
        rect(c, -102, yy-6, 220 - (i%2)*55, 12, 'panel2', 6)
    polygon(c, [(83, 130), (139, 178), (142, 130)], 'white')
    c.restore()


def lens(c, x, y, r, t, fill='pink'):
    circle(c, x, y, r, fill, .12)
    circle(c, x, y, r, fill, 1, 12)
    line(c, [(x+r*.74, y+r*.74), (x+r*1.2, y+r*1.2)], fill, 27)
    circle(c, x-r*.25, y-r*.32, r*.14, 'white', .35+.06*math.sin(t))


class Film:
    SCENES = {1: {'opening', 'machines', 'primo', 'sets', 'missing', 'map', 'matrix'},
              2: {'need', 'match', 'lenses'},
              3: {'puzzle1', 'puzzle2', 'puzzle3', 'test', 'closing'}}

    def __init__(self, episode, timeline):
        self.episode, self.timeline = episode, timeline
        self.number, self.accent = int(episode['id'][:2]), episode['accent']
        self.stars = np.random.default_rng(101).uniform([20, 245, 1], [1900, 812, 3], (55, 3))

    def at(self, scene, word, fallback=5):
        for take in self.timeline.get('takes', []):
            if take.get('scene') != scene:
                continue
            hits = [w for w in take['words'] if w['text'].lower().strip('.,!?;:\'') == word.lower()]
            if hits:
                return hits[0]['start'] - self.timeline['scenes'][scene][0]
        return fallback

    def draw(self, c, t):
        c.clear(color('bg'))
        circle(c, -70, 570, 370, 'panel', .6)
        circle(c, 1990, 435, 390, 'panel2', .38)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+8*math.sin(t*.1+i), y+5*math.cos(t*.14+i), r, 'muted', .5)
        name = next((s for s, (a, b) in self.timeline['scenes'].items() if a <= t < b), self.episode['scenes'][-1]['id'])
        scene = next(s for s in self.episode['scenes'] if s['id'] == name)
        a, b = self.timeline['scenes'][name]
        u, p = t-a, clamp((t-a)/(b-a))
        text(c, f'CHAPTER 1   /   FILM {self.number:02d}', 105, 79, 25, self.accent, True, 'left')
        text(c, self.episode['subtitle'], 1815, 79, 24, 'muted', align='right', max_width=1190)
        text(c, scene['title'], 960, 174+(1-pop(u/.7))*25, 62, 'white', True, max_width=1700)
        c.save()
        c.translate(0, (1-pop(u/.7))*35)
        (self.evidence, self.relevance, self.puzzles)[self.number-1](c, name, u, p)
        c.restore()
        rect(c, 155, 843, 1610, 78, 'panel', 36)
        text(c, scene['claim'], 960, 892, 31, self.accent, True, max_width=1530)
        text(c, 'Aaron Tay · How Search Decides What You See · CC BY 4.0', 105, 947, 20, 'muted', align='left')
        for i, s in enumerate(self.episode['scenes']):
            circle(c, 1652+22*i, 939, 5, self.accent if s['id'] == name else 'panel2')
        if b-t < .28 and scene != self.episode['scenes'][-1]:
            q = smooth((.28-(b-t))/.28)
            rect(c, 1920-1920*q, 235, 1920*q, 580, self.accent, 0)

    def evidence(self, c, name, t, p):
        if name == 'opening':
            box(c, 960, 296, 'Is there an open access citation advantage?', 'The question enters a search system', 'mint', 1310, 113)
            archive(c, 402, 580, t, .92)
            robot(c, 952, 566, t, 1.15)
            flow(c, 650, 570, 760, 570, t)
            flow(c, 1138, 570, 1280, 570, t, 'yellow')
            answer(c, 1530, 552, t, .96)
            if t > self.at(name, 'five', 8):
                chip(c, '5 REAL PAPERS', 1515, 766, 380, 'blue', 31, 65)
            if t > self.at(name, 'why', 17):
                chip(c, 'WHY THESE FIVE?', 960, 750, 470, 'yellow', 37)
        elif name == 'machines':
            archive(c, 278, 545, t, .62)
            flow(c, 445, 545, 575, 545, t)
            rect(c, 603, 337, 365, 365, 'mint', 95)
            robot(c, 786, 507, t, .8, 'blue')
            text(c, 'RETRIEVAL', 786, 653, 38, 'ink', True)
            flow(c, 982, 545, 1120, 545, t, 'yellow')
            rect(c, 1140, 337, 365, 365, 'pink', 95)
            answer(c, 1323, 493, t, .63)
            text(c, 'GENERATION', 1323, 653, 38, 'ink', True)
            wrap(c, 'Select and order records', 786, 762, 370, 29, 'mint')
            wrap(c, 'Turn supplied records into prose', 1323, 762, 430, 29, 'pink')
            if t > self.at(name, 'first', 11):
                lens(c, 786, 507, 220, t, 'yellow')
        elif name == 'primo':
            chip(c, 'PRIMO · DOCUMENTED SEPTEMBER 2026', 960, 288, 970, 'blue', 28, 64)
            items = [('Rewrite', 'Boolean variants joined by OR', 'mint'),
                     ('Retrieve', 'CDI · up to 30 candidates', 'blue'),
                     ('Rerank', 'Embeddings · select 5 sources', 'pink'),
                     ('Write', 'Overview from 5 abstracts', 'yellow')]
            triggers = [0, self.at(name, 'thirty', 12), self.at(name, 'embedding', 17), self.at(name, 'overview', 24)]
            for i, (label, sub, fill) in enumerate(items):
                x = 300 + i*440
                box(c, x, 433, label.upper(), sub, fill, 388, 143)
                if i < 3:
                    flow(c, x+201, 430, x+235, 430, t, fill)
                if t >= triggers[i]:
                    if i == 0:
                        robot(c, x, 650, t, .61)
                        chip(c, 'LLM', x, 774, 140, 'mint', 24, 44)
                    elif i == 1:
                        for j in range(30):
                            circle(c, x-100+(j%6)*40, 578+(j//6)*35, 12, 'blue')
                        text(c, 'UP TO 30', x, 784, 26, 'blue', True)
                    elif i == 2:
                        for j in range(5):
                            paper(c, x-116+j*58, 653+math.sin(t+j)*8, str(j+1), [], t, .17, 'pink')
                        text(c, '5 SOURCES', x, 784, 26, 'pink', True)
                    else:
                        answer(c, x, 652, t, .56)
                        text(c, 'ABSTRACT-BASED', x, 784, 25, 'yellow', True)
        elif name == 'sets':
            for x, r, title, fill in [(390, 214, 'INDEX', 'blue'), (985, 151, 'CANDIDATES', 'pink'), (1570, 108, 'SUPPLIED', 'mint')]:
                circle(c, x, 520, r, fill, .12)
                circle(c, x, 520, r, fill, .6, 3)
                text(c, title, x, 286, 31, fill, True)
            flow(c, 639, 520, 797, 520, t, 'pink')
            flow(c, 1160, 520, 1431, 520, t, 'mint')
            for j in range(65):
                a = j*2.4
                r = 25+172*math.sqrt((j+.5)/65)
                xx, yy = 390+math.cos(a)*r, 520+math.sin(a)*r
                circle(c, xx, yy, 6, 'blue', .45 if j < 30 else .8)
            rerank = smooth((t-self.at(name, 'reranking', 9))/.9)
            for j in range(30):
                a = j*2.4
                r = 25+172*math.sqrt((j+.5)/65)
                old_x, old_y = 390+math.cos(a)*r, 520+math.sin(a)*r
                reordered = (j*7) % 30
                tx = 905+((j%6)*(1-rerank)+(reordered%6)*rerank)*32
                ty = 450+((j//6)*(1-rerank)+(reordered//6)*rerank)*32
                move = smooth((t-self.at(name, 'moves', 4)-j*.025)/1.5)
                circle(c, old_x+(tx-old_x)*move, old_y+(ty-old_y)*move, 8, 'pink')
            selection = pop((t-self.at(name, 'selection', 9))/1.0)
            for j in range(5):
                paper(c, 1500+(j%3)*65, 485+(j//3)*90, str(j+1), [], t, .20*selection, 'mint')
            if t > self.at(name, 'gold', 18):
                circle(c, 314, 650, 13, 'yellow')
                line(c, [(314, 669), (314, 687)], 'yellow', 3)
                paper(c, 314, 716, 'P', [], t, .36, 'yellow')
                wrap(c, 'Relevant paper P never entered the candidates', 570, 734, 375, 25, 'yellow')
                check(c, 812, 720, False, 17)
            if t > self.at(name, 'round', 31):
                wrap(c, 'Reordering this pool cannot recover P. Another retrieval round could add it.', 1270, 737, 720, 28, 'muted')
        elif name == 'missing':
            text(c, 'A missing citation has several possible causes', 960, 287, 31, 'muted')
            labels = [('INDEX', 'Outside the collection', 'blue'), ('QUERY', 'Not reached by this expression', 'mint'),
                      ('TOP 30', 'Outside the candidate boundary', 'pink'), ('TOP 5', 'Not selected after reranking', 'coral'),
                      ('WRITER', 'Supplied, then omitted', 'yellow')]
            for i, (label, subtitle, fill) in enumerate(labels):
                x = 288 + i*335
                box(c, x, 575, label, '', fill, 292, 90)
                wrap(c, subtitle, x, 661, 277, 27)
                if i < 4:
                    flow(c, x+151, 575, x+183, 575, t, fill)
                circle(c, x, 450, 63, fill, .12)
                check(c, x, 450, False, 19)
            paper(c, 285+1340*((t*.05)%1), 374, 'P', [], t, .29, 'yellow')
            chip(c, 'INSPECT THE WORKING SET', 960, 778, 800, 'mint', 34, 66)
        elif name == 'map':
            box(c, 960, 289, 'CONTROLLER', 'Chooses and sequences actions', 'yellow', 1230, 97)
            stages = [('QUERY', 'transformation', 'mint'), ('ANALYSIS', 'execution rules', 'blue'),
                      ('RETRIEVAL', 'first-stage candidates', 'pink'), ('FUSION', 'combine candidate lists', 'coral'),
                      ('RERANKING', 'compare a shortlist', 'violet'), ('PRESENTATION', 'what the reader sees', 'yellow')]
            for i, (label, sub, fill) in enumerate(stages):
                x, y = 420+(i%3)*540, 455+(i//3)*226
                box(c, x, y, label, sub, fill, 475, 137)
                circle(c, x-197, y-45, 15, fill)
                text(c, str(i+1), x-197, y-39, 17, 'ink', True)
                if i in (0, 1, 3, 4):
                    flow(c, x+245, y, x+286, y, t, fill)
            arrow(c, 1747, 455, 1747, 568, 'pink', 5)
            line(c, [(1747, 568), (161, 568), (161, 681)], 'pink', 4, .55)
            arrow(c, 161, 681, 170, 681, 'pink', 5)
            text(c, 'A general map: stages are optional. Primo has no fusion step.', 960, 802, 28, 'muted')
        elif name == 'matrix':
            arrow(c, 285, 740, 1690, 740, 'mint', 6)
            arrow(c, 285, 740, 285, 301, 'pink', 6)
            text(c, 'RETRIEVAL ITERATION', 150, 533, 23, 'pink', True)
            for x, y, title, sub, fill in [(650, 416, 'ITERATIVE SEARCH', 'Repeated retrieval · ranked records', 'blue'),
                    (1300, 416, 'DEEP RESEARCH', 'Repeated retrieval · written answer', 'pink'),
                    (650, 640, 'QUICK SEARCH', 'Single pass · ranked records', 'mint'),
                    (1300, 640, 'QUICK ANSWER', 'Single pass · written answer', 'yellow')]:
                box(c, x, y, title, sub, fill, 585, 170)
                if 'SEARCH' in title:
                    for j in range(3):
                        rect(c, x-64, y-56+j*9, 128-j*15, 4, fill, 2)
                else:
                    circle(c, x, y-54, 15, fill)
            text(c, 'Ranked records', 650, 785, 28, 'mint')
            text(c, 'Written answer / report', 1300, 785, 28, 'mint')
            chip(c, 'AGENCY: WHO CHOOSES THE NEXT ACTION?', 990, 269, 1170, 'yellow', 28, 52)

    def relevance(self, c, name, t, p):
        if name == 'need':
            robot(c, 390, 516, t, 1.2)
            chip(c, 'AI academic libraries', 1100, 339, 1050, 'blue', 40)
            flow(c, 570, 532, 680, 532, t, 'pink')
            rect(c, 750, 437, 880, 325, 'panel2', 46)
            text(c, 'THE INFORMATION NEED', 1190, 492, 31, 'pink', True)
            requirements = [('Empirical studies', 'empirical'), ('Since 2024', 'twenty'),
                            ('Academic libraries implementing generative AI', 'implementing'),
                            ('Services for research support', 'support')]
            for i, (value, word) in enumerate(requirements):
                if t > self.at(name, word, 8+i*2):
                    circle(c, 807, 544+i*54, 8, 'mint')
                    text(c, value, 838, 553+i*54, 29, 'white', align='left', max_width=720)
            text(c, 'Typed expression', 1100, 405, 25, 'blue')
            text(c, 'The fuller purpose behind it', 1190, 806, 28, 'pink')
        elif name == 'match':
            # Two genuinely overlapping sets; neither circle contains the other.
            circle(c, 776, 505, 230, 'blue', .24)
            circle(c, 1128, 505, 230, 'pink', .24)
            circle(c, 776, 505, 230, 'blue', .8, 4)
            circle(c, 1128, 505, 230, 'pink', .8, 4)
            text(c, 'MATCHES THE QUERY', 670, 279, 28, 'blue', True)
            text(c, 'HELPS WITH THE NEED', 1250, 279, 28, 'pink', True)
            paper(c, 660, 513, 'A', ['AI', 'academic', 'libraries'], t, .51, 'blue')
            paper(c, 1250, 513, 'B', ['LLMs', 'consultation', 'university'], t, .51, 'pink')
            circle(c, 952, 493, 18, 'mint')
            text(c, 'both', 952, 546, 22, 'mint')
            wrap(c, 'Opinion piece · 2019', 610, 727, 480, 31, 'blue', True)
            wrap(c, 'Implementation study', 1300, 727, 530, 31, 'pink', True)
            text(c, 'Exact words can match while the need fails', 610, 779, 26, 'muted', max_width=590)
            text(c, 'Different words can express the same need', 1300, 779, 26, 'muted', max_width=590)
        elif name == 'lenses':
            paper(c, 960, 520, 'P', ['one paper'], t, .69, 'white')
            items = [(410, 390, 'COMPUTED MATCH', 'What does the system score?', 'blue'),
                     (1510, 390, 'TOPICAL SUITABILITY', 'Is it about this subject?', 'mint'),
                     (410, 690, 'WHAT SOMEONE LEARNS', 'Does it teach this reader?', 'pink'),
                     (1510, 690, 'USEFUL FOR A TASK', 'Does it meet the requirements?', 'yellow')]
            for x, y, title, sub, fill in items:
                lens(c, x, y-35, 75, t, fill)
                text(c, title, x, y+80, 27, fill, True)
                text(c, sub, x, y+119, 24, 'muted', max_width=490)
                flow(c, 535 if x < 960 else 1385, y-15, 820 if x < 960 else 1100, 500 if y < 500 else 580, t, fill)
            text(c, 'Related perspectives · no fixed ladder', 960, 272, 31, 'muted')

    def puzzles(self, c, name, t, p):
        if name == 'puzzle1':
            chip(c, 'open access citation advantage', 960, 288, 1110, 'blue', 34, 65)
            chip(c, 'AND xqzblorp', 450, 393, 590, 'coral', 37, 70)
            gate(c, 450, 645, t, False, 'STRICT AND', .59)
            text(c, 'If impossible word is required: 0 results', 450, 810, 26, 'coral', max_width=680)
            flow(c, 730, 565, 985, 565, t, 'yellow')
            for i in range(3):
                paper(c, 1150+i*235, 569, str(i+1), ['useful-looking'], t, .49, 'mint')
            text(c, 'scite example: useful-looking papers remain', 1400, 793, 28, 'mint', max_width=760)
            text(c, 'CHAPTER OBSERVATION · MECHANISM LEFT OPEN', 1370, 381, 24, 'muted')
        elif name == 'puzzle2':
            archive(c, 474, 534, t, 1.0)
            text(c, '≈9.4 MILLION', 470, 306, 55, 'blue', True)
            text(c, 'REPORTED RESULTS', 470, 354, 28, 'blue', True)
            lens(c, 1333, 531, 176, t, 'yellow')
            for j in range(5):
                rect(c, 1213, 438+j*39, 240, 23, 'mint', 8)
            text(c, '1,000', 1333, 305, 64, 'yellow', True)
            text(c, 'VIEWABLE RECORDS', 1333, 354, 28, 'yellow', True)
            flow(c, 740, 528, 1070, 528, t, 'yellow')
            text(c, 'COUNTS ARE SEPARATE · ILLUSTRATION IS NOT TO SCALE', 960, 758, 23, 'muted')
            text(c, 'A display limit does not reveal which records were scored or ranked', 960, 805, 28, 'muted')
        elif name == 'puzzle3':
            text(c, 'SEMANTIC SCHOLAR · CHAPTER OBSERVATION · AUGUST 2026', 960, 282, 25, 'muted')
            for i, (label, query, n, fill) in enumerate([
                ('FULL QUESTION', 'Is there an open access citation advantage', 13, 'coral'),
                ('SHORT KEYWORD QUERY', 'open access citation advantage', 35300, 'mint')]):
                y = 382+i*216
                text(c, label, 196, y, 28, fill, True, 'left')
                text(c, query, 196, y+44, 29, 'white', align='left')
                width = math.log10(n+1)*250
                rect(c, 196, y+67, width*pop(t/1.4), 66, fill, 16)
                text(c, '13' if n == 13 else '≈35,300', 223+width, y+113, 38, fill, True, 'left')
            text(c, 'Bar length: log₁₀(count + 1) · approximately 2,715-fold difference', 960, 805, 26, 'muted')
        elif name == 'test':
            answer(c, 420, 477, t, .91)
            paper(c, 420, 723, 'P?', [], t, .32, 'yellow')
            box(c, 1100, 339, 'DID P ENTER THE WORKING SET?', '', 'yellow', 1070, 92)
            line(c, [(1100, 396), (1100, 468), (879, 468), (879, 516)], 'mint', 5)
            line(c, [(1100, 468), (1490, 468), (1490, 516)], 'coral', 5)
            box(c, 879, 585, 'YES', 'Inspect selection and generation', 'mint', 412, 140)
            box(c, 1490, 585, 'NO', 'Trace query, index, boundaries and reranking', 'coral', 540, 140)
            text(c, 'A new direct search tests availability', 1168, 751, 31, 'blue', True)
            text(c, 'It does not locate the loss in the original run', 1168, 803, 27, 'muted')
        elif name == 'closing':
            robot(c, 957, 530, t, 1.15)
            for i, (x, title, sub, fill) in enumerate([(340, 'WHAT WAS SUPPLIED?', 'The writer’s evidence', 'pink'),
                    (1580, 'WHAT WAS SELECTED?', 'The shortlist and cut-offs', 'yellow'),
                    (340, 'WHAT WAS SEARCHED?', 'The query and the index', 'mint')]):
                y = 384 if i < 2 else 655
                box(c, x, y, title, sub, fill, 565, 147)
                flow(c, 639 if x < 960 else 1280, y, 790 if x < 960 else 1130, 480 if y < 500 else 583, t, fill)
            box(c, 1575, 681, 'NEXT: WORDS AS CONDITIONS', 'Chapter 2 · Boolean admission', 'blue', 570, 137)
            text(c, 'Follow the evidence backwards', 960, 800, 37, 'white', True)
