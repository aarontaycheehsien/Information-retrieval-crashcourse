"""Original Chapter 6 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter6_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import TOY_TEXT, TOY_VOCABULARY, INITIAL_VECTORS, CONTEXT_VECTORS, token_ids, mean_pool, check_examples
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
        text(c, f"CHAPTER 6   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 6 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Chapter 6 teaching example · Training labels depend on the stated information need"):
        text(c, message, 960, 900, 21, MUTED, align="center", width=1700)

    def plot(self, c, name, a=1):
        if name not in self.images:
            data = skia.Data.MakeWithCopy((self.plot_directory/(name+".png")).read_bytes())
            self.images[name] = skia.Image.MakeFromEncoded(data)
            assert self.images[name] is not None
        paint = skia.Paint()
        paint.setAlphaf(a)
        c.drawImageRect(self.images[name], skia.Rect.MakeXYWH(170, 255, 1580, 632), paint=paint)

    def vector_hook(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body, color) in enumerate([
            ("TOKEN IDs", ["3, 8, 11, 21, 11, 21", "Input lookup keys"], MUTED),
            ("CONTEXTUAL VECTORS", ["One working vector per token", "Information from the sequence"], BLUE),
            ("ONE POOLED VECTOR", ["[1, 1, 2]", "Stored and compared here"], TEAL)]):
            panel(c, 130+i*570, 345, 520, 350, title, body, color, 1 if i<2 else .2+.8*p)
        text(c, "Follow the boundary between working material and search output.", 960, 820, 34, INK, p, True, align="center", width=1720)
        self.note(c, "Conventional single-vector dense retrieval · All displayed numeric values are declared toys")

    def two_units(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 300, 770, 390, "LEXICAL INDEX TERM", ["Text analysis → indexed term", "Term → posting list", "Collection determines the postings"], BLUE)
        panel(c, 1000, 300, 770, 390, "MODEL INPUT TOKEN", ["Tokenizer → vocabulary ID", "ID → encoder working material", "Fixed input vocabulary or byte inventory"], TEAL, .2+.8*p)
        text(c, "Sharing a name does not make the units interchangeable.", 960, 815, 36, INK, p, True, align="center", width=1700)
        self.note(c, "A model input token does not automatically become a searchable term with a posting list")

    def coverage(self, c, t, s):
        p = self.r(t, s)
        text(c, "delulu", 960, 355, 80, BLUE, bold=True, align="center")
        arrow(c, 960, 400, 960, 485, TEAL, p)
        for i, char in enumerate(TOY_TEXT):
            x=205+i*270
            rect(c, x, 530, 160, 125, PAPER, .15+.85*p)
            text(c, char, x+80, 612, 52, TEAL, .15+.85*p, True, align="center")
        text(c, "Input coverage does not establish understanding.", 960, 800, 42, INK, p, True, align="center")
        self.note(c, "Declared toy tokenizer: one character per token · Actual model tokenization depends on its vocabulary")

    def ids(self, c, t, s):
        p = self.r(t, s)
        text(c, "CHARACTER", 145, 285, 23, MUTED, bold=True)
        text(c, "TOY ID", 145, 435, 23, MUTED, bold=True)
        text(c, "INITIAL VECTOR", 145, 590, 23, MUTED, bold=True)
        for i, (char, ident) in enumerate(zip(TOY_TEXT, token_ids())):
            x=460+i*245
            text(c, char, x, 325, 50, BLUE, bold=True, align="center")
            arrow(c, x, 350, x, 400, BLUE, p)
            text(c, str(ident), x, 475, 41, TEAL, p, True, align="center")
            vector=INITIAL_VECTORS[ident]
            for j, value in enumerate(vector):
                rect(c, x-74+j*50, 555, 44, 60, TEAL if value else RULE, .15+.85*p, 2)
                text(c, str(value), x-52+j*50, 597, 25, PAPER if value else MUTED, p, True, align="center")
        rows(c, ["Both l positions use ID 11 and begin with the same lookup vector.", "Context can change the representation for each occurrence."], 960, 760, 32, INK, p, step=60, align="center", width=1700)
        self.note(c, "Declared toy vocabulary and initial vectors · Token IDs are lookup keys, not final search coordinates")

    def context_pool(self, c, t, s):
        p = self.r(t, s)
        text(c, "SUPPLIED CONTEXTUAL VECTORS", 170, 280, 28, BLUE, bold=True)
        for i, (char, vec) in enumerate(zip(TOY_TEXT, CONTEXT_VECTORS)):
            y=320+i*65
            rect(c, 180, y, 650, 53, PAPER)
            text(c, f"{i+1} · {char}           [{vec[0]}, {vec[1]}, {vec[2]}]", 215, y+38, 28, BLUE, bold=True)
        arrow(c, 880, 515, 1105, 515, TEAL, p)
        panel(c, 1175, 350, 570, 300, "ONE TEXT VECTOR", ["Sum: [6, 6, 12]", "Mean: [1, 1, 2]", "Divide each coordinate by 6"], TEAL, .2+.8*p)
        text(c, "Other pooling methods can select a sequence-opening representation.", 960, 815, 32, INK, p, align="center", width=1700)
        self.note(c, "Toy arithmetic from six supplied vectors · No contextual encoder was run to produce these numbers")

    def independent(self, c, t, s):
        p = self.r(t, s)
        for y, title, body, color, label in [(290, "QUERY", "A new question", BLUE, "[q₁, q₂, …]"),
                                             (555, "PASSAGE", "Can be prepared earlier", TEAL, "[d₁, d₂, …]")]:
            panel(c, 150, y, 500, 190, title, [body], color)
            arrow(c, 685, y+95, 755, y+95, color, p)
            panel(c, 790, y, 360, 190, "ENCODER", ["Independent path"], color, .2+.8*p)
            arrow(c, 1190, y+95, 1260, y+95, color, p)
            panel(c, 1300, y, 470, 190, "OUTPUT VECTOR", [label], color, .2+.8*p)
        text(c, "Compare the output vectors · Parameters may be shared or distinct", 960, 830, 32, INK, p, True, align="center", width=1710)
        self.note(c, "Bi-encoder arrangement · Independent passage encoding can happen before a query arrives")

    def stored_boundary(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 290, 770, 360, "ENCODER WORKING MATERIAL", ["Model tokens → IDs → initial vectors", "Contextual token representations", "Pooling combines or selects"], BLUE)
        panel(c, 1000, 290, 770, 360, "STORED AND COMPARED HERE", ["One query or passage vector", "Dimensions are not token IDs", "Training must support useful comparisons"], TEAL, .2+.8*p)
        pill(c, "Late interaction retains multiple token vectors instead", 415, 760, RED, p, size=25)
        self.note(c, "The chapter follows a conventional single-vector design; it does not define every dense retrieval architecture")

    def nearby_hook(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 315, 770, 360, "SOUNDS RELATED", ["Same broad topic", "Important words in common", "Close for some learnt reason"], BLUE)
        panel(c, 1000, 315, 770, 360, "SERVES THIS SEARCH", ["Addresses the stated information need", "Scores above competing passages", "Requires the right training and evidence"], RED, .2+.8*p)
        text(c, "Which relationship did training reward?", 960, 815, 44, INK, p, True, align="center")
        self.note(c, "Pooling a pretrained encoder does not automatically make its separate query and passage vectors useful")

    def stated_need(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 255, 1620, 175, "QUERY", ["Am I being delulu about getting this job?"], BLUE)
        panel(c, 150, 485, 770, 325, "STATED NEED", ["Help me judge whether", "my expectations are unrealistic"], RED)
        panel(c, 1000, 485, 770, 325, "LABELLED POSITIVE", ["How to recognise unrealistic", "expectations during a job search"], TEAL, .2+.8*p)
        self.note(c, "Labels follow the chapter's stipulated need · This is not evidence of a pretrained model understanding slang")

    def easy_negative(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 320, 770, 360, "STATED NEED", ["Judge unrealistic expectations", "about getting a job"], BLUE)
        panel(c, 1000, 320, 770, 360, "EASY NEGATIVE", ["A history of agricultural", "employment", "Broad work theme; a different task"], MUTED, .2+.8*p)
        text(c, "Broad contrasts need not teach the finer distinctions.", 960, 820, 38, INK, p, True, align="center", width=1710)
        self.note(c, "Chapter teaching example · The chosen negative examples change the lesson supplied during training")

    def hard_negative(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 285, 1620, 210, "HARD NEGATIVE FOR THE STATED NEED", ["Ten signs that you performed well in your job interview"], RED)
        panel(c, 150, 570, 770, 250, "OUR STATED NEED", ["Are my expectations unrealistic?", "This is labelled a negative here"], BLUE)
        panel(c, 1000, 570, 770, 250, "A DIFFERENT NEED", ["How well did my interview go?", "The same passage could be useful"], TEAL, .2+.8*p)
        self.note(c, "Positive and negative labels record a task's intended distinction; they are not permanent passage properties")

    def score_comparison(self, c, t, s):
        self.plot(c, "comparison-before")
        self.plot(c, "comparison-after", self.r(t, s, 1, "desired", 1.5))
        self.note(c, "Desired ordering only · Parameters, examples and objectives determine what a real training run learns")

    def sbert_dpr(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 310, 770, 355, "SENTENCE-BERT", ["Adapt BERT for efficient comparison", "Encode sentences independently", "Train the intended relationship"], BLUE)
        panel(c, 1000, 310, 770, 355, "DENSE PASSAGE RETRIEVAL", ["Question and passage encoders", "Train relevant passages to score higher", "Compare independent representations"], TEAL, .2+.8*p)
        text(c, "A model family name alone does not make the transition.", 960, 815, 36, INK, p, True, align="center", width=1700)
        self.note(c, "Influential examples described in Chapter 6 · Pooling and task training both matter")

    def labels_limit(self, c, t, s):
        p = self.r(t, s)
        items = ["Starting model", "Training pairs", "Negative examples", "Loss function", "Optimisation"]
        for i, label in enumerate(items):
            x = 200+(i%3)*570
            y = 320+(i//3)*160
            panel(c, x, y, 490, 110, label, [], BLUE)
        panel(c, 225, 710, 1470, 140, "ASK WHAT THE LABELS REWARD; TEST THE FIT TO YOUR TASK", [], RED, p)
        self.note(c, "High similarity reflects learnt comparisons · It does not establish usefulness for every search")

    def signals_hook(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 310, 770, 365, "RETRIEVER ONE", ["Same architecture", "Training: question–answer pairs", "Reward answer-bearing relationships"], BLUE)
        panel(c, 1000, 310, 770, 365, "RETRIEVER TWO", ["Same architecture", "Training: citation-linked papers", "Reward scholarly relationships"], TEAL, .2+.8*p)
        text(c, "The same machinery can learn a different ranking.", 960, 820, 40, INK, p, True, align="center")
        self.note(c, "The training examples and negatives supply an operational model of relevance")

    def clicks_answers(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body, color) in enumerate([
            ("CLICKS", ["An observed action", "Popularity and position can matter"], RED),
            ("QUESTION + ANSWER", ["Answer-bearing relationship", "Favors useful answering passages"], BLUE),
            ("TITLE + ABSTRACT", ["A document's related text", "May favor topical similarity"], TEAL)]):
            panel(c, 130+i*570, 300, 520, 340, title, body, color)
        text(c, "Human judgements, generated queries and neighbouring passages", 960, 755, 32, INK, p, align="center", width=1710)
        text(c, "can supply other signals—with their own limits.", 960, 815, 32, INK, p, align="center")
        self.note(c, "Training signals are proxies for useful results, not direct observations of relevance itself")

    def citations(self, c, t, s):
        p = self.r(t, s)
        points = [(250, 380), (580, 310), (770, 535), (430, 650), (215, 770)]
        for a, b in [(0, 1), (1, 2), (2, 3), (0, 3), (3, 4)]:
            arrow(c, *points[a], *points[b], TEAL, .6, stroke=3)
        for i, (x, y) in enumerate(points):
            circle(c, x, y, 34, TEAL)
            text(c, chr(65+i), x, y+10, 28, PAPER, bold=True, align="center")
        panel(c, 1000, 315, 770, 430, "SPECTER: PAPER EMBEDDINGS", ["Training from the citation graph", "A scholarly relatedness signal", "Different from a direct answer target", "Evaluate the relationship you need"], TEAL, .2+.8*p)
        self.note(c, "Schematic citation graph, not SPECTER data · A citation does not certify agreement or review eligibility")

    def transfer(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 280, 770, 340, "TRAINING SETTING", ["General web questions", "Particular genres and languages", "Available positives and negatives"], BLUE)
        panel(c, 1000, 280, 770, 340, "DEPLOYMENT SETTING", ["Systematic review?", "Specialist chemistry?", "Another language or query population?"], TEAL, .2+.8*p)
        panel(c, 225, 710, 1470, 140, "A BENCHMARK RESULT DOES NOT GUARANTEE TRANSFER", [], RED, p)
        self.note(c, "Changing examples can change rankings even with the same architecture · Evaluate locally")

    def fine_distinctions(self, c, t, s):
        p = self.r(t, s)
        for i, ident in enumerate(("CMP-104", "CMP-140")):
            panel(c, 150+i*850, 320, 770, 300, "INVENTED IDENTIFIER", [ident], BLUE if i==0 else RED)
        rows(c, ["Exact identifiers · contradictions · specialised senses", "Include the distinctions that carry your real information need."], 960, 740, 34, INK, p, step=70, align="center", width=1710)
        self.note(c, "Teaching identifiers, not chemical facts or a scored model test · No numerical similarity is asserted")

    def diagnosis(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body) in enumerate([
            ("COLLECTION COVERAGE", ["Was the relevant material available?"]),
            ("SEARCHABLE FIELDS", ["Was the necessary evidence indexed?"]),
            ("QUERY PROCESSING", ["What reached the retrieval stage?"]),
            ("CANDIDATE CUT-OFFS", ["What survived for later stages?"])]):
            panel(c, 150+(i%2)*850, 265+(i//2)*245, 770, 205, title, body, BLUE)
        text(c, "Then compare performance across locally judged queries.", 960, 825, 36, INK, p, True, align="center", width=1710)
        self.note(c, "Training mismatch is a hypothesis · Retrieval-training data do not establish whether domain pretraining occurred")

    def three_questions(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body, color) in enumerate([
            ("1 · WHAT IS STORED?", ["What text unit?", "One vector or several?"], BLUE),
            ("2 · WHAT TAUGHT IT?", ["Which positives and negatives?", "What signal and objective?"], RED),
            ("3 · WHAT WORKS HERE?", ["Our task and collection", "Our query population and judgements"], TEAL)]):
            panel(c, 130+i*570, 340, 520, 350, title, body, color, 1 if i<2 else .2+.8*p)
        text(c, "Local evidence tests whether the learnt comparisons serve the need.", 960, 825, 33, INK, p, True, align="center", width=1710)
        self.note(c, "Chapter 7 puts the retrieval encoder to work across a whole collection")

    def poster(self, c):
        c.clear(skia.Color(*CREAM))
        text(c, "HOW SEARCH DECIDES WHAT YOU SEE", 130, 130, 27, MUTED, bold=True)
        text(c, f"CHAPTER 6 · FILM {self.script['episode_number']:02d}", 130, 220, 30, self.accent, bold=True)
        titles = {1: ["The vector we", "actually store."], 2: ["The result that", "almost answers."], 3: ["Whose idea", "of relevance?"]}
        rows(c, titles[self.script['episode_number']], 130, 405, 95, INK, bold=True, step=132, width=1190)
        text(c, self.script["subtitle"], 130, 750, 31, MUTED, width=1130)
        for i in range(6):
            rect(c, 1410, 330+i*45, 125, 28, self.accent, .3+.1*(i%3), 3)
        arrow(c, 1555, 460, 1630, 460, self.accent, stroke=4)
        rect(c, 1660, 350, 110, 220, PAPER, stroke=1)
        for i in range(3):
            rect(c, 1680, 385+i*55, 70, 35, self.accent, .6+i*.15, 2)
        text(c, "Original animated investigation · Narrated and captioned", 130, 890, 26, self.accent)
        text(c, "Adapted from Aaron Tay · CC BY 4.0", 130, 1000, 23, MUTED)
