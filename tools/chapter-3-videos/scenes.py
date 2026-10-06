"""Calculated BM25 examples and original animated Chapter 3 diagrams."""
from __future__ import annotations

import math
import re

from visuals import (Film as BaseFilm, RECORDS, C, arrow, check, chip, circle, clamp,
                     color, docbubble, flow, gate, line, paint, paper, pipeline,
                     polygon, pop, rect, robot, text)


def idf(n, df):
    """Common positive-IDF variant; not every BM25 implementation uses this form."""
    return math.log1p((n-df+.5)/(df+.5))


def factor(tf, length=100, average=100, k1=1.2, b=.75):
    return 0.0 if tf == 0 else tf*(k1+1)/(tf+k1*(1-b+b*length/average))


def contributions():
    # Explicit analyser: lowercase; retain all whitespace-separated words.
    tokens = {key: re.findall(r"[a-z]+", value.lower()) for key, value in RECORDS.items()}
    average = sum(map(len, tokens.values()))/len(tokens)
    dfs = {term: sum(term in value for value in tokens.values()) for term in ("delulu", "job")}
    scores = {key: {term: idf(len(tokens), dfs[term])*factor(value.count(term), len(value), average)
                    for term in dfs} for key, value in tokens.items()}
    return tokens, average, dfs, scores


def validate_math():
    # Compare to the chapter's independently stated worked values, not only the
    # rendering code: average-length TF factors at k1=1.2 are 1, 1.375, ~2.08.
    assert math.isclose(factor(1), 1)
    assert math.isclose(factor(2), 1.375)
    assert abs(factor(20)-2.08) < .005
    assert math.isclose(factor(1, 40, b=0), factor(1, 400, b=0))
    assert all(math.isclose(factor(tf, k1=0), 1) for tf in (1, 2, 20))
    assert idf(10, 2) > idf(10, 9) > 0
    tokens, average, dfs, scores = contributions()
    assert [len(v) for v in tokens.values()] == [4, 4, 3, 5]
    assert average == 4 and dfs == {"delulu": 2, "job": 4}
    eligible = {key for key, v in tokens.items() if "delulu" in v and "job" in v}
    assert eligible == {"D1", "D4"}
    assert round(sum(scores["D1"].values()), 2) == .80
    assert round(sum(scores["D4"].values()), 2) == .72
    order = sorted(scores, key=lambda key: sum(scores[key].values()), reverse=True)
    assert order == ["D1", "D4", "D3", "D2"]


def bar(c, x, baseline, width, height, fill, value=None):
    if height > 0:
        rect(c, x-width/2, baseline-height, width, height, fill, 14)
    if value is not None:
        text(c, value, x, baseline-height-22, 39, fill, True)


def curve(c, x, y, width, height, t, k1=1.2, fill="yellow", reveal=1, show_axes=True):
    """Linear axes: tf 0..20, frequency factor 0..3.2 (all curves share scale)."""
    if show_axes:
        line(c, [(x, y-height), (x, y), (x+width, y)], "muted", 4)
        for v in (0, 5, 10, 15, 20):
            xx = x+v/20*width
            line(c, [(xx, y), (xx, y+12)], "muted", 3)
            text(c, str(v), xx, y+49, 26, "muted")
        for v in (0, 1, 2, 3):
            yy = y-v/3.2*height
            line(c, [(x-10, yy), (x, yy)], "muted", 3)
            text(c, str(v), x-27, yy+9, 25, "muted", align="right")
        text(c, "Occurrences in this document", x+width/2, y+102, 31, "muted")
        text(c, "TF factor", x, y-height-27, 29, "muted", align="left")
    points = []
    end = max(.04, reveal*20)
    for i in range(201):
        tf = end*i/200
        points.append((x+tf/20*width, y-factor(tf, k1=k1)/3.2*height))
    line(c, points, fill, 8)
    return lambda tf: (x+tf/20*width, y-factor(tf, k1=k1)/3.2*height)


def list_scores(c, scores, x, y, t, selected=(), large=True):
    ordered = sorted(scores, key=lambda key: sum(scores[key].values()), reverse=True)
    spacing = 125 if large else 91
    for rank, ident in enumerate(ordered):
        yy = y+rank*spacing
        if selected and ident not in selected:
            continue
        rect(c, x-245, yy-44, 490, 87, "panel", 21)
        text(c, str(rank+1), x-194, yy+13, 33, "muted", True)
        docbubble(c, ident, x-104, yy, "mint" if ident in ("D1", "D4") else "blue", 33)
        text(c, f"{sum(scores[ident].values()):.2f}", x+138, yy+14, 39, "yellow", True)


class Film(BaseFilm):
    def __init__(self, episode, timeline):
        super().__init__(episode, timeline)
        self.tokens, self.average, self.dfs, self.scores = contributions()

    # The base engine draws the common chapter frame, character language,
    # transitions and captions. Its three scene dispatch hooks are reused here.
    def boolean(self, c, name, t, p):
        self.weighted(c, name, t, p)

    def analysis(self, c, name, t, p):
        self.saturation(c, name, t, p)

    def index(self, c, name, t, p):
        self.ranking(c, name, t, p)

    def weighted(self, c, name, t, p):
        if name == "race":
            text(c, "All passed the Boolean gate", 600, 294, 36, "mint", True)
            for i, x in enumerate((330, 600, 870)):
                paper(c, x, 538, ("A", "B", "C")[i], [], t, .76)
                line(c, [(x-105, 723), (x+105, 723)], "mint", 9)
            flow(c, 1050, 524, 1205, 524, t)
            rect(c, 1300, 352, 385, 380, "panel", 45)
            robot(c, 1492, 492, t, .68, "yellow")
            text(c, "Who comes first?", 1492, 677, 35, "yellow", True)
            text(c, "Same eligibility, different evidence", 960, 809, 33, "muted")
        elif name == "match":
            chip(c, "QUERY: delulu + job", 960, 294, 600, "mint", 40, 86)
            rect(c, 240, 379, 1440, 300, "panel", 40)
            text(c, "Document: unrealistic job expectations", 960, 453, 43, "white", True)
            for i, term in enumerate(("delulu", "job")):
                x = 585+i*750
                chip(c, term, x, 554, 250, "pink" if i == 0 else "mint", 44)
                check(c, x+200, 554, i == 1, 28)
                text(c, "Zero from this term" if i == 0 else "A matching contribution", x, 739, 34, "muted")
        elif name == "rare":
            for row, term in enumerate(("delulu", "job")):
                yy = 410+row*250
                chip(c, term, 294, yy, 250, "mint" if row == 0 else "blue", 40)
                for i in range(10):
                    x = 610+i*111
                    has = i < (2 if row == 0 else 9)
                    rect(c, x-34, yy-48, 68, 92, "mint" if row == 0 and has else "blue" if has else "panel2", 14)
                    for z in range(3):
                        line(c, [(x-16, yy-18+z*19), (x+16, yy-18+z*19)], "ink" if has else "muted", 4)
                    if has:
                        circle(c, x, yy-67, 7+2*math.sin(t*1.5+i), "yellow")
                text(c, f"{2 if row == 0 else 9} of 10 records", 1060, yy+113, 34, "muted")
        elif name == "idf":
            paper(c, 435, 525, "X", ["delulu", "delulu", "delulu"], t, .85)
            text(c, "Many occurrences", 435, 782, 35, "muted")
            flow(c, 667, 530, 878, 530, t, "mint")
            circle(c, 1190, 514, 158, "mint")
            text(c, "1", 1190, 551, 108, "ink", True)
            text(c, "One document for the DF count", 1240, 760, 38, "mint", True, max_width=860)
            text(c, "Document frequency counts records, not repetitions.", 960, 814, 31, "muted")
        elif name == "add":
            vals = [idf(10, 2), idf(10, 9)]
            for i, (term, val) in enumerate(zip(("delulu", "job"), vals)):
                x = 470+i*630
                chip(c, term, x, 290, 330, ("mint", "blue")[i], 44)
                h = val/1.5*320
                bar(c, x, 716, 250, h*pop(t/1.1), ("mint", "blue")[i], f"{val:.2f}")
            text(c, "+", 786, 521, 76, "white", True)
            arrow(c, 1290, 523, 1380, 523, "yellow")
            circle(c, 1588, 524, 123, "yellow")
            text(c, f"{sum(vals):.2f}", 1588, 548, 72, "ink", True)
            text(c, "Average length · tf = 1 per term · positive IDF", 960, 805, 31, "muted")
        elif name == "zero":
            chip(c, "delulu + job", 466, 332, 420, "mint", 42)
            paper(c, 466, 593, "X", ["unrealistic", "expectations"], t, .79)
            check(c, 847, 564, False, 44)
            flow(c, 1050, 564, 1190, 564, t, "coral")
            circle(c, 1430, 563, 143, "coral")
            text(c, "0", 1430, 611, 125, "ink", True)
            text(c, "Matching-term contribution", 1430, 783, 35, "muted", max_width=715)
        elif name == "meaning":
            rect(c, 190, 315, 650, 412, "panel", 42)
            rect(c, 1080, 315, 650, 412, "panel", 42)
            text(c, "BM25 SCORE", 515, 385, 34, "mint", True)
            text(c, "1.63", 515, 589, 129, "mint", True)
            text(c, "Lexical evidence", 515, 680, 32, "muted")
            text(c, "RELEVANCE", 1405, 385, 34, "yellow", True)
            robot(c, 1405, 539, t, .62)
            text(c, "Does it answer your question?", 1405, 680, 30, "muted", max_width=590)
            text(c, "≠", 960, 564, 100, "coral", True)
            text(c, "Scores are not probabilities of relevance.", 960, 806, 36, "yellow", True)
        elif name == "four":
            labels = [("MATCH", "Did it occur?", "mint"), ("RARITY", "In how many records?", "blue"),
                      ("REPETITION", "How often here?", "yellow"), ("LENGTH", "In how much text?", "pink")]
            for i, (title, sub, fill) in enumerate(labels):
                x = 335+i*416
                rect(c, x-181, 330, 362, 358, "panel", 35)
                chip(c, str(i+1), x, 424, 94, fill, 47, 94)
                text(c, title, x, 561, 30, fill, True)
                text(c, sub, x, 637, 27, "muted", max_width=328)
            text(c, "Next: the curve behind repeated words", 960, 799, 35, "yellow", True)

    def saturation(self, c, name, t, p):
        if name == "repeat":
            paper(c, 445, 532, "A", ["delulu"], t, .89)
            paper(c, 1420, 532, "B", ["delulu", "delulu", "delulu"], t, .89)
            chip(c, "1 occurrence", 445, 752, 390, "mint", 37)
            chip(c, "20 occurrences", 1420, 752, 390, "yellow", 37)
            text(c, "20× credit?", 960, 440, 49, "white", True)
            text(c, "No.", 960, 576, 93, "coral", True)
        elif name == "curve":
            at = curve(c, 300, 686, 1260, 343, t, reveal=pop(t/3))
            limit_y = 686-2.2/3.2*343
            line(c, [(300, limit_y), (1560, limit_y)], "pink", 3, .6)
            text(c, "Limit: 2.2", 1576, limit_y-18, 29, "pink", align="left")
            for tf, label in ((1, "1.00"), (2, "1.375"), (20, "2.075")):
                xx, yy = at(tf)
                circle(c, xx, yy, 11, "mint")
            text(c, "k₁ = 1.2 · document length = collection average", 960, 284, 31, "muted")
        elif name == "compare":
            for i, tf in enumerate((1, 2, 20)):
                x = 455+i*505
                val = factor(tf)
                bar(c, x, 696, 242, val/2.2*310*pop(t/1.5), ("mint", "blue", "yellow")[i], f"{val:.3f}")
                chip(c, f"tf = {tf}", x, 750, 270, ("mint", "blue", "yellow")[i], 36, 64)
            text(c, "At average length, k₁ = 1.2", 960, 293, 35, "muted")
            text(c, "Factor × IDF = this term's contribution", 960, 822, 32, "white", True)
        elif name == "kone":
            at = curve(c, 260, 676, 1160, 335, t, k1=.5, fill="blue")
            curve(c, 260, 676, 1160, 335, t, k1=1.2, fill="yellow", show_axes=False)
            curve(c, 260, 676, 1160, 335, t, k1=2, fill="pink", show_axes=False)
            # At k1=0, positive tf has constant factor 1. The tf=0 case is 0.
            line(c, [(318, 676-335/3.2), (1420, 676-335/3.2)], "mint", 5)
            for i, (label, fill) in enumerate((("k₁ = 2", "pink"), ("k₁ = 1.2", "yellow"), ("k₁ = 0.5", "blue"), ("k₁ = 0", "mint"))):
                chip(c, label, 1630, 351+i*102, 265, fill, 31, 70)
            text(c, "Compare curves at average document length", 960, 284, 32, "muted")
        elif name == "length":
            for i, length in enumerate((40, 400)):
                x = 465+i*975
                rect(c, x-204, 356, 408, 265 if i == 0 else 408, "white", 28)
                text(c, "delulu", x, 423, 39, "ink", True)
                for j in range(5 if i == 0 else 11):
                    yy = 458+j*23
                    line(c, [(x-147, yy), (x+145-((j*53)%90), yy)], "muted", 6)
                chip(c, f"{length} analysed terms", x, 797, 455, "mint" if i == 0 else "yellow", 32, 69)
            chip(c, "tf = 1", 960, 484, 244, "pink", 47, 91)
            text(c, "Average length: 100 terms", 960, 654, 29, "muted", max_width=500)
        elif name == "bee":
            # Explicitly labelled animated switch; arithmetic and captions agree.
            switch = self.spoken_at(name, "With", 7)
            b = .75 if t >= switch else 0
            chip(c, f"b = {b:g}", 960, 297, 280, "yellow", 43, 80)
            for i, length in enumerate((40, 400)):
                x = 520+i*885
                val = factor(1, length, 100, b=b)
                bar(c, x, 673, 277, val/1.4*269, ("mint", "blue")[i], f"{val:.3f}")
                text(c, f"{length} analysed terms", x, 743, 37, "muted")
            text(c, "tf = 1 · average length = 100 · k₁ = 1.2", 960, 809, 30, "muted")
        elif name == "judgement":
            paper(c, 419, 535, "SHORT", ["delulu"], t, .79)
            flow(c, 678, 538, 848, 538, t, "yellow")
            robot(c, 1123, 525, t, 1.02, "violet")
            text(c, "Useful?", 1536, 495, 53, "white", True)
            text(c, "Right population?", 1490, 579, 35, "muted")
            text(c, "Right question?", 1490, 653, 35, "muted")
            text(c, "A stronger contribution is still only lexical evidence.", 960, 806, 34, "yellow", True)
        elif name == "recap":
            labels = [("IDF", "Collection rarity", "mint"), ("k₁", "Term saturation", "yellow"), ("b", "Length normalisation", "pink")]
            for i, (title, sub, fill) in enumerate(labels):
                x = 434+i*524
                circle(c, x, 482, 125, fill)
                text(c, title, x, 517, 93, "ink", True)
                text(c, sub, x, 689, 34, "muted", max_width=490)
            text(c, "Next: one index, separate decisions", 960, 809, 37, "yellow", True)

    def ranking(self, c, name, t, p):
        if name == "same":
            for i, (ident, value) in enumerate(RECORDS.items()):
                yy = 330+i*114
                rect(c, 145, yy-45, 915, 88, "panel", 23)
                docbubble(c, ident, 213, yy, "mint", 33)
                text(c, value, 278, yy+12, 30, "white", align="left", max_width=733)
            flow(c, 1100, 510, 1225, 510, t, "coral")
            robot(c, 1480, 500, t, .88, "coral")
            text(c, "INVERTED INDEX", 1480, 736, 32, "coral", True)
            text(c, "Illustrative analyser: lowercase; keep all words", 960, 810, 31, "muted")
        elif name == "gate":
            chip(c, "delulu AND job", 960, 287, 600, "mint", 45, 87)
            for i, ident in enumerate(RECORDS):
                x = 355+i*403
                yes = ident in ("D1", "D4")
                gate(c, x, 565, t+i, yes, "AND", .54)
                paper(c, x, 537, ident, ["delulu", "job"] if yes else ["job"], t, .52)
                text(c, "ELIGIBLE" if yes else "EXCLUDED", x, 786, 31, "mint" if yes else "coral", True)
        elif name == "evidence":
            heads = ["RECORD", "delulu tf", "job tf", "LENGTH"]
            xs = [470, 828, 1186, 1544]
            for x, label in zip(xs, heads):
                text(c, label, x, 334, 30, "coral", True)
            for row, ident in enumerate(("D1", "D4")):
                yy = 445+row*160
                rect(c, 236, yy-58, 1448, 119, "panel", 25)
                values = [ident, "1", "1", str(len(self.tokens[ident]))]
                for x, value in zip(xs, values):
                    text(c, value, x, yy+20, 55, "white", True)
            text(c, "N = 4 · df(delulu) = 2 · df(job) = 4", 960, 753, 35, "mint", True)
            text(c, f"Average length = {self.average:g} analysed terms", 960, 812, 32, "muted")
        elif name == "scores":
            for i, ident in enumerate(("D1", "D4")):
                yy = 430+i*247
                docbubble(c, ident, 286, yy, "coral", 53)
                x = 438
                for term, fill in (("delulu", "mint"), ("job", "blue")):
                    value = self.scores[ident][term]
                    width = value*1050
                    rect(c, x, yy-55, width*pop(t/1.2), 110, fill, 15)
                    text(c, f"{value:.4f}", x+width/2, yy+15, 36, "ink", True, max_width=width-18)
                    x += width+7
                text(c, f"≈ {sum(self.scores[ident].values()):.2f}", 1555, yy+21, 63, "yellow", True)
            chip(c, "delulu", 660, 300, 270, "mint", 34, 64)
            chip(c, "job", 1030, 300, 230, "blue", 34, 64)
            text(c, "k₁ = 1.2 · b = 0.75 · positive IDF", 960, 785, 30, "muted")
            text(c, "Totals are rounded from full-precision contributions", 960, 825, 25, "muted")
        elif name == "topk":
            list_scores(c, {key:self.scores[key] for key in ("D1", "D4")}, 510, 412, t)
            # Show both boundaries simultaneously; top-k does not change scores.
            for i, k in enumerate((1, 2)):
                x = 1140+i*453
                chip(c, f"TOP {k}", x, 320, 306, "coral" if k == 1 else "mint", 37)
                for j, ident in enumerate(("D1", "D4")[:k]):
                    paper(c, x, 492+j*209, ident, [], t, .49)
            text(c, "Same scores; different output sizes", 960, 813, 34, "yellow", True)
        elif name == "direct":
            chip(c, "Any analysed query term can match", 598, 309, 874, "mint", 39, 80)
            for i, ident in enumerate(RECORDS):
                x = 296+i*226
                paper(c, x, 570, ident, ["delulu", "job"] if ident in ("D1", "D4") else ["job"], t, .46)
            flow(c, 1070, 545, 1204, 545, t, "coral")
            list_scores(c, self.scores, 1537, 363, t, large=False)
            text(c, "Illustrative direct BM25 ranking", 960, 811, 33, "muted")
        elif name == "fast":
            chip(c, "Current cutoff: 0.80", 960, 292, 575, "yellow", 40, 78)
            for i, (bound, word, fill) in enumerate(((.40, "SKIP SAFELY", "blue"), (.90, "INSPECT", "mint"))):
                x = 526+i*869
                rect(c, x-272, 367, 544, 342, "panel", 42)
                for j in range(5):
                    rect(c, x-202+j*85, 412, 65, 132, fill, 11)
                text(c, f"Valid upper bound: {bound:.2f}", x, 610, 34, "white", True, max_width=505)
                chip(c, word, x, 731, 407, fill, 35, 78)
            text(c, "Illustration: a bound proves whether a block can compete", 960, 814, 31, "muted")
        elif name == "finish":
            pipeline(c, ["Eligibility", "BM25 score", "Top-k boundary"], 370, 1, t)
            for i, (title, fill) in enumerate((("Field weights", "mint"), ("Phrase boosts", "blue"), ("Other signals", "pink"), ("Later reranking", "yellow"))):
                x = 325+i*420
                chip(c, title, x, 587, 365, fill, 30, 88)
            robot(c, 962, 742, t, .29, "coral")
            text(c, "A relevance label does not reveal the whole pipeline.", 960, 817, 33, "muted")
