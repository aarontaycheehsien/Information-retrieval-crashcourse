"""Original Chapter 7 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter7_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import QUERY, VECTORS, scores, ANN_POINTS, APPROX_EXAMINED, nearest, check_examples
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
        text(c, f"CHAPTER 7   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 7 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Chapter 7 teaching example · Training labels depend on the stated information need"):
        text(c, message, 960, 900, 21, MUTED, align="center", width=1700)

    def plot(self, c, name, a=1):
        if name not in self.images:
            data = skia.Data.MakeWithCopy((self.plot_directory/(name+".png")).read_bytes())
            self.images[name] = skia.Image.MakeFromEncoded(data)
            assert self.images[name] is not None
        paint = skia.Paint()
        paint.setAlphaf(a)
        c.drawImageRect(self.images[name], skia.Rect.MakeXYWH(170, 255, 1580, 632), paint=paint)

    def winner_hook(self, c, t, s):
        p = self.r(t, s)
        pill(c, "SAME QUERY · SAME A, B, C", 690, 270, BLUE)
        panel(c, 150, 365, 770, 340, "COSINE SIMILARITY", ["A comes first", "Directional alignment"], TEAL)
        panel(c, 1000, 365, 770, 340, "UNNORMALISED DOT PRODUCT", ["B comes first", "Direction and length"], RED, .2+.8*p)
        text(c, "The comparison rule changed.", 960, 825, 46, INK, p, True, align="center")
        self.note(c, "A numerical ordering is not a new relevance judgement · Declared toy vectors follow")

    def precompute(self, c, t, s):
        p = self.r(t, s)
        text(c, "PASSAGE VECTORS PREPARED EARLIER", 160, 295, 28, BLUE, bold=True)
        for i in range(24):
            tiny(c, 180+(i%6)*105, 350+(i//6)*95, 72, 75, color=BLUE)
        panel(c, 1100, 310, 650, 240, "ENCODE THE NEW QUERY", ["An independent representation", "Shared or distinct encoder weights"], TEAL, .2+.8*p)
        arrow(c, 930, 530, 1045, 530, TEAL, p)
        panel(c, 1100, 620, 650, 180, "COMPARE STORED VECTORS", ["Flat search or a neighbour index"], RED, .2+.8*p)
        self.note(c, "Conventional bi-encoder retrieval · Passage encoding does not depend on the incoming query")

    def cosine_direction(self, c, t, s):
        p = self.r(t, s)
        for i, (title, score) in enumerate([("SAME DIRECTION", "1"), ("RIGHT ANGLE", "0"), ("OPPOSITE", "−1")]):
            x=130+i*570
            rect(c, x, 315, 520, 400, PAPER)
            text(c, title, x+260, 375, 28, BLUE, bold=True, align="center", width=470)
            ox, oy=x+250, 550
            arrow(c, ox, oy, ox+155, oy, BLUE, stroke=4)
            dx,dy=(155,0) if i==0 else (0,-125) if i==1 else (-145,0)
            arrow(c, ox, oy, ox+dx, oy+dy, TEAL, .3+.7*p, stroke=4)
            text(c, score, x+260, 665, 51, TEAL, p, True, align="center")
        text(c, "Direction matters. Positive stretching leaves cosine unchanged.", 960, 825, 35, INK, p, True, align="center", width=1710)
        self.note(c, "Cosine landmarks · Values are mathematical comparisons, not percentages of relevance")

    def dot_product(self, c, t, s):
        self.plot(c, "comparison-rules")
        self.note(c, "Dot product multiplies matching coordinates and adds · Length can change the winner")

    def normalisation(self, c, t, s):
        self.plot(c, "unit-rules")
        self.note(c, "Production normalisation and comparison should match training; a model may have learnt to use magnitude")

    def dimensions(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body) in enumerate([("TWO", ["[x, y]", "A drawable toy"]),
                                           ("THREE", ["[x, y, z]", "One more coordinate"]),
                                           ("MANY", ["[x₁, x₂, …, xₙ]", "Hundreds or thousands"])]):
            panel(c, 130+i*570, 330, 520, 310, title, body, BLUE)
        text(c, "q · d = q₁d₁ + q₂d₂ + … + qₙdₙ", 960, 765, 46, TEAL, p, True, align="center", width=1700)
        self.note(c, "Anonymous coordinates, not named concepts · The same comparison extends across matching dimensions")

    def score_limits(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 315, 770, 355, "NUMERICAL SIGNAL", ["A model and comparison rule", "Preprocessing and normalisation", "Scores in that particular setup"], BLUE)
        panel(c, 1000, 315, 770, 355, "TASK JUDGEMENT", ["The reader's information need", "Context and inclusion criteria", "Evaluate actual returned material"], RED, .2+.8*p)
        text(c, "A high similarity score does not settle usefulness.", 960, 820, 40, INK, p, True, align="center")
        self.note(c, "Scores from different models or searches need not be comparable")

    def visited_hook(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 315, 770, 350, "SEARCH ONE", ["Examines all 6 points", "Returns 3 leaders", "A, B, C"], BLUE)
        panel(c, 1000, 315, 770, 350, "SEARCH TWO", ["Examines 4 selected points", "Returns 3 leaders", "A, B, D"], RED, .2+.8*p)
        text(c, "Same requested count. Different work and guarantees.", 960, 820, 38, INK, p, True, align="center", width=1710)
        self.note(c, "Source teaching example · A visible count does not reveal how a search ran")

    def two_indexes(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 310, 770, 370, "TERM → DOCUMENT POINTERS", ["Analyse the query terms", "Jump to matching posting lists", "No need to reread the whole collection"], BLUE)
        panel(c, 1000, 310, 770, 370, "QUERY VECTOR → COMPARISONS", ["No posting list for a meaning", "Flat search compares every vector", "An ANN index searches selected areas"], TEAL, .2+.8*p)
        text(c, "Flat-search work grows with collection size and dimensions.", 960, 825, 34, INK, p, True, align="center", width=1710)
        self.note(c, "Indexing routes can coexist in a product · No measured response time or speedup is claimed")

    def exact_search(self, c, t, s):
        self.plot(c, "neighbours-exact")
        self.note(c, "Euclidean distance toy, not cosine · All six points are examined; the nearest three are A, B, C")

    def approx_search(self, c, t, s):
        self.plot(c, "neighbours-approximate")
        self.note(c, "Stipulated examined set A, B, D, F · Possible ANN miss, not a simulation of HNSW")

    def graph_navigation(self, c, t, s):
        p = self.r(t, s)
        layers=[(310, [280, 1080]), (500, [280, 680, 1080, 1480]), (735, [280, 480, 680, 880, 1080, 1280, 1480, 1680])]
        for j,(y,xs) in enumerate(layers):
            text(c, ["UPPER", "MIDDLE", "LOWER"][j], 130, y+8, 23, MUTED, bold=True)
            for a,b in zip(xs,xs[1:]):
                line(c, a, y, b, y, RULE, stroke=3)
            for x in xs:
                circle(c, x, y, 20, BLUE)
        for x in (280,1080):
            line(c, x, 330, x, 480, RULE, stroke=2)
        for x in (280,680,1080,1480):
            line(c, x, 520, x, 715, RULE, stroke=2)
        route=[(280,310),(1080,310),(1080,500),(1480,500),(1480,735)]
        u=clamp((t-self.at(s,0))/max(1,self.tl['scenes'][s['id']][1]-self.at(s,0)-2))*4
        index=min(3,int(u)); f=clamp(u-index)
        a,b=route[index],route[index+1]
        circle(c, lerp(a[0],b[0],f), lerp(a[1],b[1],f), 13, RED, .4+.6*p)
        self.note(c, "Schematic multi-layer navigation · No real links, measured path or HNSW algorithm trace is represented")

    def four_controls(self, c, t, s):
        p = self.r(t, s)
        for i,(title,body,color) in enumerate([
            ("1 · WHO MAY COMPETE?", ["Admission rules and filters"], BLUE),
            ("2 · WHAT SCORES THEM?", ["Lexical evidence or vector comparison"], TEAL),
            ("3 · HOW IS SEARCH RUN?", ["Exact comparison or approximate navigation"], RED),
            ("4 · HOW MANY LEADERS?", ["The requested output boundary k"], BLUE)]):
            panel(c, 150+(i%2)*850, 270+(i//2)*255, 770, 215, title, body, color)
        text(c, "Our two runs: 6 or 4 examined; both request k = 3.", 960, 820, 36, INK, p, True, align="center")
        self.note(c, "Top-k outputs can be lexical, dense or hybrid, and exact or approximate")

    def best_available(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 310, 770, 355, "LEXICAL CANDIDATE FLOOR", ["Strict Boolean requires its conditions", "Direct BM25 normally needs", "at least one analysed-term match"], BLUE)
        panel(c, 1000, 310, 770, 355, "DENSE CANDIDATE SPACE", ["Every stored vector can receive a score", "Filters may narrow the collection", "Even unrelated records have an order"], TEAL, .2+.8*p)
        pill(c, "Nearest means best available under the rule", 535, 780, RED, p, size=27)
        self.note(c, "Metadata, lexical evidence and vector retrieval can coexist · Judge returned material against the need")

    def semantic_hook(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 315, 770, 360, "WHAT THE LABEL CLAIMS", ["Match by meaning", "A semantic goal or capability", "A natural-language box accepts questions"], TEAL)
        panel(c, 1000, 315, 770, 360, "WHAT STILL NEEDS EVIDENCE", ["Which stage forms candidates?", "Where do representations enter?", "What does a later ranker compare?"], BLUE, .2+.8*p)
        text(c, "A semantic goal can be pursued through several mechanisms.", 960, 820, 35, INK, p, True, align="center", width=1710)
        self.note(c, "Semantic, dense, vector and embedding describe different properties")

    def three_routes(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 245, 1620, 145, "A WORDING GAP", ["Query: heart attack treatment    |    Document: myocardial infarction therapy"], BLUE)
        for i,(title,body,color) in enumerate([
            ("EXPAND → MATCH", ["Add the alternate expressions", "Lexical matches become possible", "Terms provide candidate evidence"], BLUE),
            ("DENSE VECTORS", ["Encode both original texts", "Use a trained comparison", "Overlap need not be required"], TEAL),
            ("RETRIEVE → RERANK", ["Expansion supplies the bridge", "Lexical retrieval admits the text", "A reranker compares the shortlist"], RED)]):
            panel(c, 130+i*570, 460, 520, 340, title, body, color, 1 if i<2 else .2+.8*p)
        self.note(c, "Possible routes, not guaranteed matches · A reranker cannot recover a document excluded upstream")

    def bridge_bottleneck(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 305, 770, 395, "THE VOCABULARY BRIDGE", ["A delulu question", "↓ suitably trained representation", "A passage on unrealistic expectations", "Important expressions can differ"], TEAL)
        panel(c, 1000, 305, 770, 395, "THE SINGLE-VECTOR BOTTLENECK", ["Compress before seeing the query", "Broad similarity may dominate", "Exact code · rare name · negation", "Shorter chunks still pool information"], RED, .2+.8*p)
        text(c, "Similar meaning still needs to serve the reader's task.", 960, 825, 37, INK, p, True, align="center", width=1710)
        self.note(c, "Vocabulary bridging depends on suitable training · No model output or retrieval benchmark is shown")

    def range_threshold(self, c, t, s):
        p = self.r(t, s)
        pill(c, "SAME FIXED SIMILARITY THRESHOLD", 600, 265, BLUE)
        panel(c, 150, 375, 770, 310, "ONE QUERY", ["No vectors above the cutoff", "Output: nothing"], RED)
        panel(c, 1000, 375, 770, 310, "ANOTHER QUERY", ["Many vectors above the cutoff", "Output: a very large set"], TEAL, .2+.8*p)
        text(c, "A fixed k controls output size; threshold usefulness needs calibration.", 960, 825, 32, INK, p, True, align="center", width=1710)
        self.note(c, "Possible yields, not measured query distributions · Scores vary across models, queries and collections")

    def stage_budgets(self, c, t, s):
        p = self.r(t, s)
        pill(c, "INVENTED TEACHING BUDGETS", 675, 270, RED)
        for i,(title,count,body,color) in enumerate([
            ("RETRIEVE", "40", "candidates retained", BLUE),
            ("TO THE WRITER", "8", "source records passed on", TEAL),
            ("DISPLAY", "3", "citations shown", RED)]):
            x=130+i*570
            rect(c, x, 360, 520, 360, PAPER)
            text(c, title, x+260, 420, 27, color, bold=True, align="center", width=470)
            text(c, count, x+260, 560, 105, color, bold=True, align="center")
            text(c, body, x+260, 650, 27, MUTED, align="center", width=470)
            if i<2:
                arrow(c, x+535, 540, x+558, 540, color, p)
        text(c, "The visible count does not reveal how many competed or were examined.", 960, 825, 32, INK, p, True, align="center", width=1710)
        self.note(c, "Illustration only · A documented display cap also does not establish an exhaustively scored global top-k")

    def opening_puzzle(self, c, t, s):
        p = self.r(t, s)
        text(c, "SEMANTIC SCHOLAR · CHAPTER OBSERVATION · AUGUST 2026", 960, 280, 27, BLUE, bold=True, align="center", width=1710)
        for x,number,title,words,color in [
            (150,"13","NATURAL-LANGUAGE QUESTION",["Is there an open access", "citation advantage"],RED),
            (1000,"≈35,300","SHORTER KEYWORD QUERY",["open access citation advantage"],TEAL)]:
            rect(c, x, 340, 770, 370, PAPER)
            text(c, title, x+385, 400, 27, color, bold=True, align="center", width=700)
            text(c, number, x+385, 535, 86, color, bold=True, align="center", width=700)
            rows(c, words, x+385, 615, 27, INK, step=45, align="center", width=700)
        text(c, "Counts and inspected results describe the example; the precise mechanism stays open.", 960, 825, 30, INK, p, True, align="center", width=1710)
        self.note(c, "Reported counts and the author's quality assessment from the pinned chapter · No current-service test")

    def documented_routes(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 250, 1620, 255, "SEMANTIC SCHOLAR · DOCUMENTED MAIN RELEVANCE SEARCH · 2025", ["Query → Elasticsearch keyword candidates → up to 1,000 → LightGBM reranking", "Does not establish the later interface's precise query processing"], BLUE)
        panel(c, 150, 565, 1620, 280, "OPENALEX ALICE · DOCUMENTED SEMANTIC REQUEST · 2026", ["Query → GTE Large EN embedding → stored work vectors → cosine nearest works", "1,024 dimensions · April account: 413 million embeddings", "Semantic, exact and lexical modes are alternatives; not automatically hybrid"], TEAL, .2+.8*p)
        self.note(c, "Dated documentation accounts in the pinned source · Product names do not reveal candidate retrieval")

    def pipeline_questions(self, c, t, s):
        p = self.r(t, s)
        for i,(title,body,color) in enumerate([
            ("CANDIDATES", ["Which indexed text unit?", "What filters and admission?", "Lexical, vector or combined?"], BLUE),
            ("COMPARISON", ["Which representation and rule?", "How was the model trained?", "What can scores establish?"], TEAL),
            ("BOUNDARIES", ["Exact or approximate search?", "Where do later stages narrow?", "Does it serve the real task?"], RED)]):
            panel(c, 130+i*570, 330, 520, 390, title, body, color)
        text(c, "Locate the mechanism and test usefulness at the relevant stage.", 960, 825, 35, INK, p, True, align="center", width=1710)
        self.note(c, "Chapter 8 examines representations and whether an indexed unit is a document, record or passage")

    def poster(self, c):
        c.clear(skia.Color(*CREAM))
        text(c, "HOW SEARCH DECIDES WHAT YOU SEE", 130, 130, 27, MUTED, bold=True)
        text(c, f"CHAPTER 7 · FILM {self.script['episode_number']:02d}", 130, 220, 30, self.accent, bold=True)
        titles={1:["Same vectors,", "different winner."], 2:["The neighbour", "you never visited."], 3:["Where does", "meaning enter?"]}
        rows(c, titles[self.script['episode_number']], 130, 405, 91, INK, bold=True, step=132, width=1190)
        text(c, self.script["subtitle"], 130, 750, 31, MUTED, width=1130)
        origin=(1440,680)
        for x,y,label,color in [(1730,630,"A",TEAL),(1670,370,"B",RED),(1400,470,"C",BLUE)]:
            arrow(c, *origin, x, y, color, .75, stroke=4)
            circle(c, x, y, 13, color)
            text(c, label, x+18, y-10, 25, color, bold=True)
        text(c, "Original animated investigation · Narrated and captioned", 130, 890, 26, self.accent)
        text(c, "Adapted from Aaron Tay · CC BY 4.0", 130, 1000, 23, MUTED)
