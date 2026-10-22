"""Original Chapter 3 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter3_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import RECORDS, TOKENS, LENGTHS, AVERAGE_LENGTH, DOCUMENT_FREQUENCIES, idf, factor, contributions, totals, ranking, check_examples
from plots import verify_plots



def tiny(c, x, y, w, h, label=None, color=BLUE, a=1):
    rect(c, x+3, y+4, w, h, INK, .09*a, 2)
    rect(c, x, y, w, h, PAPER, a, 2)
    rect(c, x, y, w, 3, color, a, 1)
    if label is not None and w >= 40:
        text(c, str(label), x+w/2, y+25, 18, color, a, True, align="center")
    for i in range(3):
        line(c, x+w*.15, y+h*(.5+i*.15), x+w*.8, y+h*(.5+i*.15), RULE, a, 1)


class Film(art.Film):
    def __init__(self, timeline, script):
        super().__init__(timeline, script)
        check_examples()
        verify_plots(timeline["plot_directory"], timeline["plot_manifest_sha256"])
        self.plot_directory = Path(timeline["plot_directory"])
        self.images = {}

    def at(self, scene, n=0, word=None):
        take = self.takes[f"{scene['id']}_{n}"]
        if word is None:
            return take["start"]
        normal = lambda s: re.sub(r"[^\w]", "", s).casefold()
        hits = [w for w in take["words"] if normal(w["text"]) == normal(word)]
        assert hits, f"Reveal word {word!r} not spoken in {scene['id']}_{n}"
        return hits[0]["start"]

    def r(self, t, scene, n=1, word=None, duration=.8):
        return ease((t-self.at(scene, n, word))/duration)

    def frame(self, c, t):
        c.clear(skia.Color(*CREAM))
        scene = next((s for s in self.scenes if self.tl["scenes"][s["id"]][0] <= t < self.tl["scenes"][s["id"]][1]), self.scenes[-1])
        start, end = self.tl["scenes"][scene["id"]]
        for y in range(230, 930, 70):
            line(c, 60, y, 1860, y, RULE, .14, 1)
        text(c, "HOW SEARCH DECIDES WHAT YOU SEE", 100, 63, 21, MUTED, bold=True)
        text(c, f"CHAPTER 3   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
        line(c, 100, 87, 1820, 87)
        text(c, scene["title"], 100, 165, 49, INK, bold=True, width=1700)
        c.save()
        zoom = 1+.016*ease((t-start)/(end-start))
        c.translate(960, 550); c.scale(zoom, zoom); c.translate(-960, -550)
        getattr(self, scene["visual"])(c, t, scene)
        c.restore()
        fade = max(1-ease((t-start)/.25), ease((t-end+.2)/.2))
        if fade:
            rect(c, 0, 200, W, 730, CREAM, fade, 0)
        for cue in self.captions:
            if cue["start"] <= t < cue["end"]:
                w = min(1710, font(30).measureText(cue["text"])+62)
                rect(c, (W-w)/2, 950, w, 56, INK, .96, 5)
                text(c, cue["text"], 960, 989, 30, PAPER, align="center", width=1650)
                break
        text(c, "Adapted from Aaron Tay · Chapter 3 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Illustrative single-field BM25 · Positive-IDF variant · Scores are not probabilities"):
        text(c, message, 960, 900, 21, MUTED, align="center", width=1700)

    def plot(self, c, name):
        if name not in self.images:
            data = skia.Data.MakeWithCopy((self.plot_directory/(name+".png")).read_bytes())
            self.images[name] = skia.Image.MakeFromEncoded(data)
            assert self.images[name] is not None
        c.drawImageRect(self.images[name], skia.Rect.MakeXYWH(170, 255, 1580, 632))

    def prediction(self, c, t, s):
        p = self.r(t, s)
        episode = self.script["episode_number"]
        if episode == 1:
            for i in range(3):
                card(c, 200+i*350, 350, chr(65+i), 260, 300, BLUE, angle=(i-1)*2)
                pill(c, "ELIGIBLE", 250+i*350, 715, TEAL)
            arrow(c, 1230, 510, 1370, 510, BLUE, p)
            panel(c, 1410, 350, 360, 350, "RANKING", ["Graded scores", "Which comes first?"], RED, .2+.8*p)
            text(c, "An ordering does not identify its scoring method.", 960, 835, 34, INK, p, True, align="center", width=1720)
            self.note(c, "A–C are schematic records; ranked retrieval can use lexical, vector or combined signals")
        elif episode == 2:
            for x, label, count, color in [(210, "DOCUMENT A", 1, BLUE), (1110, "DOCUMENT B", 20, TEAL)]:
                card(c, x, 330, label, 600, 390, color, detail=[f"{count} occurrence"+("s" if count != 1 else ""), "Same document length", "Same term and collection rarity"])
            text(c, "20 × the occurrences ≠ 20 × the contribution", 960, 835, 37, RED, p, True, align="center", width=1730)
            self.note(c, "Hold the other inputs fixed; isolate term-frequency saturation")
        else:
            panel(c, 150, 320, 680, 420, "THE SAME INVERTED INDEX", ["Terms → posting lists", "Within-document term frequencies", "Collection document frequencies", "Document lengths"], BLUE)
            arrow(c, 880, 525, 1050, 525, RED, p)
            panel(c, 1100, 350, 650, 360, "A GRADED SCORING RULE", ["Read the lexical evidence", "Add weighted contributions", "Order candidates by score"], RED, .2+.8*p)
            text(c, "The map can support both admission and scoring.", 960, 835, 35, INK, p, True, align="center", width=1720)
            self.note(c, "A simplified single-field index; real posting formats and pipeline configurations vary")

    def match(self, c, t, s):
        p = self.r(t, s)
        pill(c, "QUERY: delulu + job", 690, 245, BLUE, size=29)
        panel(c, 170, 345, 1580, 190, "DOCUMENT TEXT", ["unrealistic job expectations"], BLUE)
        panel(c, 180, 620, 680, 230, "delulu: ABSENT", ["Zero contribution from this term"], RED)
        panel(c, 1050, 620, 680, 230, "job: MATCHED", ["A term contribution is available"], TEAL)
        self.note(c, "Compare analysed terms; absent delulu does not make the whole document's score zero")

    def rarity(self, c, t, s):
        p = self.r(t, s)
        for row, (term, count, color) in enumerate([("delulu", 2, TEAL), ("job", 9, BLUE)]):
            y = 365+row*255
            text(c, term, 160, y+45, 39, color, bold=True)
            for i in range(10):
                x = 500+i*122
                tiny(c, x, y-20, 80, 110, color=color if i < count else MUTED, a=1 if i < count else .22)
            text(c, f"In {count} of 10 documents", 1110, y+155, 31, color, bold=True, align="center")
        text(c, "Rarer matching terms usually get higher IDF.", 960, 850, 37, INK, p, True, align="center", width=1730)
        self.note(c, "The chapter's illustrative ten-document counts; discrimination is not guaranteed usefulness")

    def frequency(self, c, t, s):
        p = self.r(t, s)
        card(c, 210, 300, "ONE DOCUMENT", 640, 500, BLUE)
        rect(c, 230, 390, 600, 380, PAPER)
        for i in range(20):
            text(c, "delulu", 260+(i%4)*140, 430+(i//4)*60, 25, BLUE)
        panel(c, 1080, 340, 680, 390, "TWO DIFFERENT COUNTS", ["Within this document: tf = 20", "Documents represented here: df = 1", "Twenty repetitions ≠ twenty documents"], TEAL)
        text(c, "Rarity and repetition answer different questions.", 960, 850, 34, INK, p, True, align="center", width=1730)
        self.note(c, "A separate counting illustration; the ten-document example's df values remain unchanged")

    def addition(self, c, t, s):
        p = self.r(t, s)
        formula = "IDF = ln(1 + (N − df + 0.5) / (df + 0.5))"
        text(c, formula, 960, 280, 32, BLUE, bold=True, align="center", width=1700)
        values = [("delulu", 2, TEAL), ("job", 9, BLUE)]
        for x, (term, df, color) in zip([170, 1080], values):
            panel(c, x, 360, 670, 335, term, [f"df = {df} of N = 10", f"IDF ≈ {idf(10,df):.3f}", "One occurrence, average length: factor 1"], color)
        text(c, "+", 960, 550, 80, MUTED, bold=True, align="center")
        total = idf(10,2)+idf(10,9)
        text(c, f"Total ≈ {total:.3f}  (about {total:.2f})", 960, 800, 45, INK, p, True, align="center")
        self.note(c, "One labeled positive-IDF version; production implementations and related variants can differ")

    def limits(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 330, 680, 400, "NO SHARED QUERY TERM", ["Query: delulu + job", "Text: unrealistic expectations", "No expansion → no term contribution"], RED)
        panel(c, 1090, 330, 680, 400, "A HIGH SCORE STILL NEEDS JUDGEMENT", ["Does it address this population?", "Does it answer this task?", "The score is not a probability"], TEAL, .2+.8*p)
        rows(c, ["Match · rarity · repetition · length", "Next: why repetition stops earning equal-sized votes"], 960, 805, 33, INK, p, align="center", bold=True, step=55, width=1740)
        self.note(c, "A plain lexical score cannot bridge every vocabulary gap; expansion could change the matching terms")

    def curve(self, c, t, s):
        self.plot(c, "saturation")
        for x, value, cue in [(210, "1 → 1.000", "occurrence"), (730, "2 → 1.375", "give"), (1250, "20 → 2.075", "Twenty")]:
            pill(c, value, x, 215, TEAL, self.r(t,s,0,cue), size=24)
        self.note(c, "Linear axes · k₁ = 1.2 · average document length · Factor × IDF = term contribution")

    def kone(self, c, t, s):
        self.plot(c, "k1-curves")
        pill(c, "k₁ = 0: positive tf → 1; absent term → 0", 880, 215, BLUE, self.r(t,s), size=22)
        self.note(c, "Same linear scales as the preceding plot; these are frequency factors, not probabilities")

    def length(self, c, t, s):
        p = self.r(t,s)
        for x, length, color in [(180,40,TEAL), (1080,400,BLUE)]:
            card(c, x, 340, f"{length} ANALYSED TERMS", 660, 380, color, detail=["delulu occurs once", "Same term, same rarity", "Collection average: 100 terms"])
        text(c, "With normalisation, frequency is read in its length context.", 960, 835, 33, INK, p, True, align="center", width=1740)
        self.note(c, "Card sizes are schematic; counts are explicit · k₁ = 1.2, b = 0.75, one occurrence")

    def bee(self, c, t, s):
        self.plot(c, "length-normalisation")
        pill(c, "b = 0 turns off the length effect", 915, 215, BLUE, self.r(t,s), size=23)
        self.note(c, "Frequency, term rarity and average length held fixed; turning off length does not turn off scoring")

    def recap(self, c, t, s):
        p = self.r(t,s)
        for x, title, body, color in [(140,"IDF",["Collection rarity", "In how many documents?", "Weight a matching term"],BLUE),
                                      (710,"k₁",["Term-frequency saturation", "How repetition contributes", "At zero: positive tf is binary"],TEAL),
                                      (1280,"b",["Length normalisation", "Strength of the length effect", "At zero: length is disabled"],RED)]:
            panel(c,x,345,500,390,title,body,color)
        text(c, "Typical defaults: k₁ = 1.2, b = 0.75 · not a quality certificate",960,835,32,INK,p,True,align="center",width=1740)
        self.note(c, "Settings are configurable; structured-field and other BM25 variants can differ")

    def evidence(self, c, t, s):
        p = self.r(t,s)
        panel(c,130,285,1010,515,"CHAPTER 2'S D1–D4", [f"{key}   {value}   (length {LENGTHS[key]})" for key,value in RECORDS.items()], BLUE)
        panel(c,1220,335,570,400,"SCORING EVIDENCE",["Average length = 4", "df(delulu) = 2", "df(job) = 4", "AND admits D1 and D4"], TEAL)
        self.note(c,"Explicit toy analyser: lowercase, retain all words · No production system was measured")

    def scores(self, c, t, s):
        p = self.r(t,s)
        data = contributions()
        text(c,"SAME QUERY-TERM COUNTS · DIFFERENT LENGTHS",960,270,28,BLUE,bold=True,align="center")
        for i,key in enumerate(["D1","D4"]):
            y=345+i*235
            rect(c,160,y,1600,185,PAPER)
            text(c,f"{key} · length {LENGTHS[key]}",200,y+68,33,BLUE,bold=True)
            text(c,f"delulu: {data[key]['delulu']:.3f}",670,y+65,30,TEAL,bold=True)
            text(c,f"job: {data[key]['job']:.3f}",1070,y+65,30,BLUE,bold=True)
            text(c,f"Total ≈ {totals()[key]:.2f}",1535,y+123,43,RED,bold=True,align="center",width=400)
        text(c,"Sum full-precision contributions; round only for display.",960,855,32,INK,p,True,align="center",width=1740)
        self.note(c,"N = 4 · average length = 4 · k₁ = 1.2 · b = 0.75 · positive IDF")

    def boundaries(self, c, t, s):
        p = self.r(t,s)
        panel(c,140,320,700,435,"STRICT AND: SAME SCORES", [f"D1 ≈ {totals()['D1']:.2f}", f"D4 ≈ {totals()['D4']:.2f}", "Top-1: D1", "Top-2: D1 and D4"],BLUE)
        panel(c,1080,320,700,435,"DIRECT UNION: ANY MATCHING TERM", [f"{i+1}   {key} ≈ {totals()[key]:.2f}" for i,key in enumerate(ranking())],RED,.2+.8*p)
        text(c,"Eligibility → scoring → output boundary",960,840,39,INK,p,True,align="center")
        self.note(c,"Top-k changes how many are retained; changing the admission rule changes who may compete")

    def products(self, c, t, s):
        p = self.r(t,s)
        text(c,"Relevance / Best Match names an ordering—not a formula.",960,265,33,INK,bold=True,align="center",width=1740)
        for x,title,body,color in [(140,"PUBMED",["Published BM25 first stage", "Top 500 → LambdaMART", "Later reranking matters"],TEAL),
                                   (710,"SCOPUS",["Term frequency + IDF", "Fields, positions, proximity", "Does not establish plain BM25"],BLUE),
                                   (1280,"PRIMO CDI",["Lexical + phrase evidence", "Field and static signals", "Does not establish plain BM25"],RED)]:
            panel(c,x,345,500,390,title,body,color)
        text(c,"Lucene / Elasticsearch / Solr / OpenSearch: BM25 text similarity; final pipelines can differ.",960,835,26,INK,p,True,align="center",width=1740)
        self.note(c,"The chapter's cited accounts; no current product behavior was retested for these films")

    def pruning(self, c, t, s):
        p = self.r(t,s)
        pill(c,"FULL CURRENT TOP-k · CUTOFF = 5",600,260,BLUE,size=27)
        panel(c,160,370,680,380,"BLOCK A: VALID UPPER BOUND 3",["Every possible score ≤ 3", "Cannot beat the cutoff of 5", "Safe to skip under this rule"],TEAL,p)
        panel(c,1080,370,680,380,"BLOCK B: VALID UPPER BOUND 7",["Could exceed the cutoff", "Needs inspection", "Does not guarantee a winner"],RED,p)
        text(c,"Efficiency changes the work; safe bounds preserve the result.",960,840,32,INK,p,True,align="center",width=1740)
        self.note(c,"Separate hypothetical numbers; assumed valid bounds and a full current top-k · No speedup measured")

    def closing(self, c, t, s):
        p=self.r(t,s)
        for x,title,body,color in [(140,"ADMISSION",["Which records become candidates?", "Strict AND or any-term matching?"],BLUE),
                                   (710,"SCORING",["What evidence sets the score?", "Which settings and extra signals?"],TEAL),
                                   (1280,"OUTPUT BOUNDARY",["Complete order or top-k?", "What is retained for later stages?"],RED)]:
            panel(c,x,340,500,370,title,body,color)
        rows(c,["A lexical baseline, not every relevance sort.", "Next: Chapter 4 — optional and unmatched query terms."],960,795,34,INK,p,align="center",bold=True,step=60,width=1740)
        self.note(c,"Hardware, index design, query mix and accuracy settings affect performance; no universal latency claim")

    def poster(self, c):
        c.clear(skia.Color(*CREAM))
        text(c,"CHAPTER 3 · BM25 AND RANKED LEXICAL RETRIEVAL",130,120,29,self.accent,bold=True,width=1640)
        line(c,130,155,1790,155,self.accent,stroke=3)
        titles={1:["Which word", "deserves", "more weight?"],2:["Twenty mentions.", "Twice", "the credit?"],3:["Same index.", "Three different", "controls."]}
        rows(c,titles[self.script['episode_number']],130,360,96,INK,bold=True,step=125,width=1160)
        for i in range(3):
            card(c,1390+i*22,340+i*100,["?","D1","D4"][i],290,340,[self.accent,MUTED,GOLD][i],angle=(i-1)*6)
        text(c,self.script['subtitle'],130,850,35,self.accent,width=1150)
        text(c,"Adapted from Aaron Tay · How Search Decides What You See",130,981,26,MUTED)
        text(c,f"FILM {self.script['episode_number']:02d}",1790,981,28,self.accent,bold=True,align="right")
