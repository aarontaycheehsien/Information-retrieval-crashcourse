"""Original flat-vector production studio, using the earlier film's visual language."""
from __future__ import annotations

import math
from pathlib import Path
import numpy as np
import skia
from visuals import (arrow, check, chip, circle, clamp, color, flow, line,
                     paper, polygon, pop, rect, robot, smooth, text)
from scenes import Film as ChapterFilm, archive, box, lens, wrap

HERE = Path(__file__).resolve().parent


def monitor(c, x, y, width=470, height=270, fill='blue'):
    rect(c, x-width/2-12, y-height/2-12, width+24, height+24, fill, 28)
    rect(c, x-width/2, y-height/2, width, height, 'ink', 20)
    line(c, [(x, y+height/2), (x, y+height/2+45)], fill, 16)
    rect(c, x-85, y+height/2+35, 170, 20, fill, 9)


def waveform(c, x, y, width, height, t, fill='mint', quiet=False):
    points = []
    for i in range(120):
        phase = i*.46-t*3
        envelope = .3+.7*math.sin(i*.07+t*.6)**2
        gain = .22 if quiet else 1
        points.append((x+width*i/119, y+math.sin(phase)*envelope*height*gain))
    line(c, points, fill, 5)


class Film(ChapterFilm):
    SCENES = {'setup', 'read', 'story', 'art', 'clock', 'music', 'review', 'deliver'}

    def __init__(self, episode, timeline):
        super().__init__(episode, timeline)
        self.poster_data = [skia.Data.MakeWithCopy((HERE / 'assets' / f'film-{i}.jpg').read_bytes()) for i in (1, 2, 3)]
        self.posters = [skia.Image.MakeFromEncoded(data) for data in self.poster_data]

    def thumbnail(self, c, number, x, y, width=390):
        height = width*9/16
        rect(c, x-width/2-8, y-height/2-8, width+16, height+16, ['mint', 'pink', 'yellow'][number-1], 18)
        c.drawImageRect(self.posters[number-1], skia.Rect.MakeXYWH(x-width/2, y-height/2, width, height))

    def draw(self, c, t):
        c.clear(color('bg'))
        circle(c, -70, 570, 370, 'panel', .6)
        circle(c, 1990, 435, 390, 'panel2', .38)
        for i, (x, y, r) in enumerate(self.stars):
            circle(c, x+8*math.sin(t*.1+i), y+5*math.cos(t*.14+i), r, 'muted', .5)
        name = next((s for s, (a, b) in self.timeline['scenes'].items() if a <= t < b), self.episode['scenes'][-1]['id'])
        scene = next(s for s in self.episode['scenes'] if s['id'] == name)
        a, b = self.timeline['scenes'][name]
        u = t-a
        text(c, 'BEHIND THE ANIMATION', 105, 79, 25, 'mint', True, 'left')
        text(c, 'CODEX · 6.1 SOL · EXTRA HIGH', 1815, 79, 24, 'muted', align='right')
        text(c, scene['title'], 960, 174+(1-pop(u/.7))*25, 62, 'white', True, max_width=1700)
        c.save()
        c.translate(0, (1-pop(u/.7))*35)
        getattr(self, name)(c, u)
        c.restore()
        rect(c, 155, 843, 1610, 78, 'panel', 36)
        text(c, scene['claim'], 960, 892, 31, 'mint', True, max_width=1530)
        text(c, 'Aaron Tay’s Chapter 1 adaptation · Original artwork · CC BY 4.0', 105, 947, 20, 'muted', align='left')
        for i, s in enumerate(self.episode['scenes']):
            circle(c, 1630+22*i, 939, 5, 'mint' if s['id'] == name else 'panel2')
        if b-t < .28 and scene != self.episode['scenes'][-1]:
            q = smooth((.28-(b-t))/.28)
            rect(c, 1920-1920*q, 235, 1920*q, 580, 'mint', 0)

    def setup(self, c, t):
        robot(c, 960, 493, t, 1.14)
        for x, y, title, sub, fill in [(380, 348, 'READ', 'Understand the chapter', 'blue'),
                (1540, 348, 'ADAPT', 'Make a teaching story', 'pink'),
                (380, 655, 'WRITE & RUN', 'Code plus media tools', 'yellow'),
                (1540, 655, 'CHECK', 'Inspect the real result', 'mint')]:
            box(c, x, y, title, sub, fill, 440, 133)
            flow(c, 620 if x < 960 else 1300, y, 780 if x < 960 else 1140, 464 if y < 500 else 572, t, fill)
        chip(c, 'GPT-6.1 SOL', 762, 752, 350, 'blue', 33, 67)
        chip(c, 'EXTRA HIGH EFFORT', 1230, 752, 540, 'pink', 32, 67)

    def read(self, c, t):
        archive(c, 334, 485, t, .85)
        chip(c, 'CHAPTER 1', 334, 747, 365, 'blue', 35, 72)
        flow(c, 555, 483, 700, 483, t)
        for i, (title, fill) in enumerate([('THE EVIDENCE', 'mint'), ('RELEVANCE', 'pink'), ('THREE PUZZLES', 'yellow')], 1):
            x = 820+(i-1)*386
            self.thumbnail(c, i, x, 476, 330)
            text(c, title, x, 669, 29, fill, True)
        box(c, 1198, 755, 'KEEP THE EVIDENCE LIMITS', 'Dates, quantities, and open questions', 'mint', 1040, 114)

    def story(self, c, t):
        for x, title, subtitle, fill in [(388, 'WHAT WE SAY', 'Narration and teaching point', 'blue'),
                 (960, 'WHAT WE SHOW', 'A scene with a clear visual job', 'pink'),
                 (1532, 'WHERE IT COMES FROM', 'An anchor back to the chapter', 'yellow')]:
            rect(c, x-244, 332, 488, 360, 'panel2', 40)
            text(c, title, x, 394, 30, fill, True, max_width=440)
            if x == 388:
                for i in range(5):
                    rect(c, x-156, 449+i*35, 312-(i%2)*80, 15, fill, 7)
            elif x == 960:
                paper(c, x, 526, 'P', ['one idea'], t, .43, fill)
            else:
                for yy in (462, 538):
                    rect(c, x-67, yy, 134, 75, fill, 38, stroke=11)
                line(c, [(x, 504), (x, 572)], 'white', 8)
            wrap(c, subtitle, x, 754, 470, 28, fill)
        flow(c, 640, 530, 701, 530, t, 'mint')
        flow(c, 1211, 530, 1270, 530, t, 'mint')
        text(c, 'Editable storyboard · 15 scenes across the earlier three films', 960, 293, 28, 'muted')

    def art(self, c, t):
        monitor(c, 1240, 516, 710, 360, 'pink')
        robot(c, 1240, 500, t, .95)
        for i, fill in enumerate(['blue', 'mint', 'yellow', 'coral', 'pink', 'violet']):
            circle(c, 1105+i*54, 679, 15, fill)
        circle(c, 310, 385, 67, 'mint')
        rect(c, 456, 327, 126, 116, 'yellow', 30)
        polygon(c, [(354, 540), (280, 666), (428, 666)], 'pink')
        paper(c, 524, 582, 'P', [], t, .32, 'blue')
        flow(c, 655, 512, 847, 512, t)
        chip(c, 'PYTHON + SKIA', 1240, 779, 620, 'blue', 34, 63)
        text(c, 'Shapes', 415, 756, 33, 'white', True)
        circle(c, 1627, 463, 73, 'mint', .17)
        circle(c, 1627, 463, 73, 'mint', 1, 5)
        a = t*.65
        line(c, [(1627, 463), (1627+math.cos(a)*49, 463+math.sin(a)*49)], 'mint', 6)
        text(c, 'Time', 1627, 586, 30, 'mint', True)

    def clock(self, c, t):
        chip(c, 'EARLIER FILMS: 47 CACHED TAKES', 960, 286, 1080, 'blue', 32, 64)
        waveform(c, 229, 418, 1462, 53, t)
        line(c, [(225, 558), (1695, 558)], 'muted', 4)
        for i, (word, fill) in enumerate([('word', 'blue'), ('timings', 'pink'), ('selection', 'yellow'), ('five', 'mint')]):
            x = 392+i*370
            chip(c, word, x, 558, 292, fill, 34, 66)
            line(c, [(x, 475), (x, 520)], fill, 4)
        for i in range(5):
            paper(c, 717+i*126, 728, str(i+1), [], t, .28*pop((t-self.at('clock', 'five', 20))/.6), 'mint')
        text(c, 'Caption cues and picture reveals share the speech clock', 960, 816, 28, 'muted')

    def music(self, c, t):
        chip(c, 'VOICE', 329, 358, 295, 'mint', 33, 68)
        waveform(c, 543, 358, 1120, 70, t, 'mint')
        chip(c, 'MUSIC', 329, 545, 295, 'pink', 33, 68)
        waveform(c, 543, 545, 1120, 70, t*.7, 'pink', quiet=True)
        box(c, 573, 742, 'LOCALLY SYNTHESIZED', 'Simple tones become a quiet score', 'pink', 695, 132)
        box(c, 1380, 742, 'MEASURE THE SOUND', '−16 LUFS target · peaks below −1 dBTP', 'mint', 720, 132)
        text(c, 'Schematic waveforms · music is reduced beneath narration', 960, 633, 26, 'muted')

    def review(self, c, t):
        text(c, 'A revision from the earlier production', 960, 286, 30, 'muted')
        for x, label, fill, moving in [(490, 'INSPECT THE DIAGRAM', 'blue', False),
                                     (1410, 'SHOW THE BOUNDARY', 'mint', True)]:
            monitor(c, x, 520, 680, 326, fill)
            circle(c, x-169, 520, 106, 'blue', .15)
            circle(c, x+174, 520, 83, 'pink', .15)
            for j in range(12):
                a = j*2.4
                ox, oy = x-169+math.cos(a)*(30+j*5), 520+math.sin(a)*(30+j*5)
                tx, ty = x+132+(j%4)*28, 486+(j//4)*29
                q = smooth((t*.24-j*.025)%1) if moving else 0
                circle(c, ox+(tx-ox)*q, oy+(ty-oy)*q, 6, 'pink' if moving else 'blue')
            circle(c, x-192, 572, 11, 'yellow')
            text(c, label, x, 771, 29, fill, True)
        flow(c, 838, 523, 1048, 523, t, 'yellow')
        lens(c, 961, 408, 48, t, 'yellow')

    def deliver(self, c, t):
        for i, (label, fill) in enumerate([('DECODE', 'blue'), ('CAPTIONS', 'pink'), ('AUDIO', 'yellow'), ('PLAY & SEEK', 'mint')]):
            x = 327+i*424
            check(c, x, 337, True, 25)
            text(c, label, x, 407, 31, fill, True)
        rect(c, 222, 498, 450, 257, 'blue', 35)
        text(c, 'EDITABLE SOURCE', 447, 556, 29, 'ink', True)
        for i in range(4):
            rect(c, 289, 596+i*30, 302-(i%2)*58, 13, 'ink', 6, alpha=.6)
        robot(c, 955, 590, t, .78)
        flow(c, 697, 605, 808, 605, t)
        flow(c, 1104, 605, 1245, 605, t, 'yellow')
        rect(c, 1284, 498, 440, 257, 'yellow', 35)
        polygon(c, [(1457, 556), (1457, 650), (1551, 603)], 'ink')
        text(c, 'PLAYABLE VIDEO', 1504, 716, 28, 'ink', True)
        text(c, 'Read → build → inspect → deliver', 960, 807, 34, 'white', True)
