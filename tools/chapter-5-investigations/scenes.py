"""Original Chapter 5 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter5_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import POOL_INPUT, SENTENCE, mean_pool, training_tasks, check_examples
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
        text(c, f"CHAPTER 5   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 5 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Illustrative teaching example · Geometry depends on training and requires task evaluation"):
        text(c, message, 960, 900, 21, MUTED, align="center", width=1700)

    def plot(self, c, name, a=1):
        if name not in self.images:
            data = skia.Data.MakeWithCopy((self.plot_directory/(name+".png")).read_bytes())
            self.images[name] = skia.Image.MakeFromEncoded(data)
            assert self.images[name] is not None
        paint = skia.Paint()
        paint.setAlphaf(a)
        c.drawImageRect(self.images[name], skia.Rect.MakeXYWH(170, 255, 1580, 632), paint=paint)

    def map_hook(self, c, t, s):
        p = self.r(t, s)
        panel(c, 140, 295, 720, 420, "A MAP OF WORDS", ["Who chose the locations?", "Who labelled the dimensions?", "What makes a neighbour useful?"], BLUE)
        for x, y, name in [(1150, 415, "word A"), (1440, 350, "word B"), (1340, 610, "word C"), (1650, 580, "word D")]:
            circle(c, x, y, 12, TEAL)
            text(c, name, x+20, y+7, 26, INK)
        arrow(c, 900, 520, 1070, 520, BLUE, p)
        text(c, "Prediction can leave geometry behind.", 960, 820, 43, INK, p, True, align="center")
        self.note(c, "Schematic locations · No trained model or semantic axes are shown")

    def representations(self, c, t, s):
        p = self.r(t, s)
        items = [("REPRESENTATION", ["A form standing for an item", "A label, a structure, a vector…"], BLUE),
                 ("VECTOR", ["An ordered list of numbers", "For example: [2, 4, 1]"], TEAL),
                 ("EMBEDDING", ["A mapping into vector space", "Usually learnt in modern NLP"], RED)]
        for i, (title, body, color) in enumerate(items):
            panel(c, 130+i*570, 345, 520, 340, title, body, color, 1 if i<2 else .2+.8*p)
        text(c, "The output vector is also commonly called an embedding.", 960, 810, 34, INK, p, align="center", width=1720)
        self.note(c, "A vector is one form of representation; it need not come from a learnt mapping")

    def two_routes(self, c, t, s):
        p = self.r(t, s)
        panel(c, 145, 280, 780, 325, "BM25", ["Term counts + lengths + statistics", "Specified weighting formula", "Calculated term weights"], BLUE)
        panel(c, 995, 280, 780, 325, "NEURAL ENCODER", ["Text + tokenisation + parameters", "A mapping fitted during training", "Calculated embedding vector"], TEAL)
        panel(c, 225, 690, 1470, 155, "TRAINING → FIT THE MAPPING     |     INFERENCE → APPLY IT", ["Reproducible outputs can still have hard-to-interpret dimensions."], RED, p)
        self.note(c, "Both routes calculate outputs · The distinction is how the mapping is obtained")

    def self_targets(self, c, t, s):
        p = self.r(t, s)
        panel(c, 160, 290, 1600, 180, "TEXT SUPPLIES THE TARGET", ["The patient received  [?]  treatment after the attack"], BLUE)
        arrow(c, 960, 500, 960, 590, TEAL, p)
        pill(c, "TARGET: heart", 825, 620, TEAL, p, size=31)
        rows(c, ["Hide a word → predict it → compare with the original", "No manual meaning label is needed for this prediction target."], 960, 755, 32, INK, p, step=65, align="center", width=1700)
        self.note(c, "The distributional hypothesis motivates the task; it is not a universal definition of meaning")

    def word2vec_games(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 285, 770, 345, "CBOW", ["Neighbouring words", "↓", "Predict the target word"], BLUE)
        panel(c, 1000, 285, 770, 345, "SKIP-GRAM", ["Target word", "↓", "Predict neighbouring words"], TEAL)
        panel(c, 300, 715, 1320, 135, "AFTER TRAINING: KEEP AND REUSE THE WORD VECTORS", [], RED, p)
        self.note(c, "The prediction machinery trains the representations · Individual dimensions are usually anonymous")

    def analogy(self, c, t, s):
        p = self.r(t, s, 0, "queen", 1.5)
        self.plot(c, "analogy-before")
        self.plot(c, "analogy-after", p)
        self.note(c, "Real nearest-neighbour analogy tests exclude king, man and woman from candidate answers")

    def projection(self, c, t, s):
        self.plot(c, "projection-loss", .15+.85*self.r(t, s))
        self.note(c, "Chapter 5's country/capital example uses PCA · This separate toy example drops one coordinate")

    def geometry_limits(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 315, 770, 355, "WHAT TRAINING REWARDED", ["Predicting word contexts", "Patterns of co-occurrence", "Useful relational regularities can emerge"], BLUE)
        panel(c, 1000, 315, 770, 355, "WHAT SEARCH NEEDS", ["Queries linked to useful passages", "A suitable representation and task", "Evaluation with relevance judgments"], RED, .2+.8*p)
        text(c, "Near according to which learnt relationship?", 960, 810, 41, INK, p, True, align="center")
        self.note(c, "Geometric proximity alone does not certify usefulness for a particular information need")

    def bank_hook(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 310, 770, 330, "OCCURRENCE ONE", ["the river bank"], BLUE)
        panel(c, 1000, 310, 770, 330, "OCCURRENCE TWO", ["the bank refused the loan"], TEAL)
        text(c, "Same letters. Must it be the same vector?", 960, 745, 44, INK, bold=True, align="center")
        text(c, "A contextual representation depends on this sequence.", 960, 830, 32, TEAL, p, align="center")
        self.note(c, "Examples from Chapter 5 · No model output or accuracy measurement is claimed")

    def static_context(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 265, 770, 190, "the river bank", ["Surrounding sequence one"], BLUE)
        panel(c, 1000, 265, 770, 190, "the bank refused the loan", ["Surrounding sequence two"], TEAL)
        for target, color in [(535, BLUE), (1385, TEAL)]:
            x = lerp(960, target, p)
            circle(c, x, 610, 52, color, .7)
            text(c, "bank", x, 621, 25, PAPER, bold=True, align="center")
        text(c, "One stored vector", 960, 520, 31, MUTED, 1-p, align="center")
        text(c, "Two contextual token representations", 960, 755, 42, INK, p, True, align="center")
        self.note(c, "Marker positions are invented · Different vectors alone would not prove correct interpretation")

    def attention(self, c, t, s):
        p = self.r(t, s)
        labels = [(470, "the"), (820, "river"), (1170, "bank")]
        for x, label in labels:
            pill(c, label, x, 315, TEAL, size=32)
            arrow(c, x+45, 385, 960, 560, TEAL, p, stroke=3)
        panel(c, 560, 590, 800, 175, "UPDATE THIS TOKEN REPRESENTATION", ["Combine information from the sequence"], BLUE, .2+.8*p)
        text(c, "The objective determines what that mechanism learns to do.", 960, 840, 33, INK, p, align="center", width=1710)
        self.note(c, "Schematic information flow, not an attention-weight plot · ELMo also produced contextual representations")

    def model_tokens(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 290, 770, 355, "TOY MODEL TOKENIZER", ["Input: jobs", "Declared rule: one character per token"], BLUE)
        for i, char in enumerate("jobs"):
            pill(c, char, 235+i*155, 550, BLUE, size=28)
        panel(c, 1000, 290, 770, 355, "ILLUSTRATIVE LEXICAL ANALYSER", ["Lowercase + stem jobs → job", "Indexed term: job"], TEAL, .2+.8*p)
        text(c, "Different processes create different units.", 960, 805, 43, INK, p, True, align="center")
        self.note(c, "Declared toy character split · No tokenization behavior of BERT or another named model is asserted")

    def pooling(self, c, t, s):
        p = self.r(t, s)
        text(c, "CONTEXTUAL TOKEN VECTORS", 200, 290, 29, BLUE, bold=True)
        for i, vector in enumerate(POOL_INPUT):
            rect(c, 220, 345+i*135, 500, 95, PAPER)
            text(c, f"Token {i+1}    [{vector[0]:g}, {vector[1]:g}]", 260, 405+i*135, 33, BLUE, bold=True)
        arrow(c, 775, 535, 1110, 535, TEAL, p)
        text(c, "MEAN POOLING", 955, 475, 25, TEAL, p, True, align="center")
        pooled = mean_pool()
        panel(c, 1180, 360, 550, 310, "ONE TEXT VECTOR", [f"[{pooled[0]:g}, {pooled[1]:g}]", "Average each coordinate"], TEAL, .2+.8*p)
        text(c, "The pooling choice depends on the model and its training.", 960, 825, 34, INK, p, align="center", width=1710)
        self.note(c, "Invented vectors · Demonstrates arithmetic mean pooling, not a particular BERT retrieval implementation")

    def reproducible(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 310, 770, 370, "HOLD THESE FIXED", ["Model and fitted parameters", "Input and preprocessing", "Inference settings"], BLUE)
        panel(c, 1000, 310, 770, 370, "REPRODUCIBLE OUTPUT", ["Apply the same mapping", "No new training step is implied", "Dimensions can remain hard to interpret"], TEAL, .2+.8*p)
        text(c, "Reproduction and interpretation are separate questions.", 960, 820, 35, INK, p, True, align="center", width=1710)
        self.note(c, "Conceptual inference diagram · No encoder run or numerical model output is represented")

    def context_limits(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body, color) in enumerate([
            ("CONTEXTUALISE", ["Let surrounding tokens", "change each representation"], BLUE),
            ("POOL / SELECT", ["Produce one representation", "for a complete text unit"], TEAL),
            ("TRAIN + EVALUATE", ["Reward useful relationships", "Test actual retrieval behavior"], RED)]):
            panel(c, 130+i*570, 340, 520, 340, title, body, color, 1 if i<2 else .2+.8*p)
        text(c, "What does this vector represent, and what taught it?", 960, 815, 39, INK, p, True, align="center", width=1700)
        self.note(c, "Contextualisation and pooling alone do not establish effective first-stage retrieval")

    def training_hook(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 310, 770, 360, "A LANGUAGE TASK", ["Recover hidden words", "in medical papers", "Use the surrounding context"], BLUE)
        panel(c, 1000, 310, 770, 360, "A RETRIEVAL TASK", ["Compare a separate question", "with candidate passages", "Rank useful answers highly"], RED, .2+.8*p)
        text(c, "What relationship did the training reward?", 960, 815, 43, INK, p, True, align="center")
        self.note(c, "A capable language model still needs a suitable architecture and training for its retrieval role")

    def prediction_task(self, c, t, s, name):
        task = training_tasks()[name]
        target = task["target_position"]
        p = self.r(t, s)
        label = {"cbow": "MODEL INPUT: LOCAL NEIGHBOURS", "masked": "MODEL INPUT: BOTH SIDES", "next_token": "MODEL INPUT: PRECEDING CONTEXT ONLY"}[name]
        text(c, label, 145, 300, 31, BLUE, bold=True)
        for i, word in enumerate(SENTENCE):
            x = 145+i*205
            visible = i in task["visible_positions"]
            active = i == target
            rect(c, x, 355, 185, 130, PAPER if visible or active else RULE, 1 if visible or active else .35)
            text(c, word if visible else "[?]" if active else "hidden", x+92, 430, 26, RED if active else INK if visible else MUTED,
                 bold=active, align="center", width=165)
        line(c, 150, 550, 1770, 550, RULE)
        panel(c, 150, 605, 1060, 205, "TRAINING TARGET · FROM THE ORIGINAL TEXT", ["Used to score the prediction; not supplied at the blank."], TEAL)
        pill(c, SENTENCE[target], 1350, 675, TEAL, p, size=36)
        notes = {"cbow": "Declared two-word window on each side · Skip-gram reverses the prediction direction",
                 "masked": "Word boxes simplify model-token prediction · The target position is hidden from the input",
                 "next_token": "The future remains hidden in the input · The separate target is available only to the training comparison"}
        self.note(c, notes[name])

    def cbow(self, c, t, s):
        self.prediction_task(c, t, s, "cbow")

    def masked(self, c, t, s):
        self.prediction_task(c, t, s, "masked")

    def next_token(self, c, t, s):
        self.prediction_task(c, t, s, "next_token")

    def three_training_jobs(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body, color) in enumerate([
            ("LANGUAGE", ["Broad language patterns", "Text supplies prediction targets"], BLUE),
            ("DOMAIN", ["Specialist text and vocabulary", "Different language experience"], TEAL),
            ("RETRIEVAL", ["Relationships useful for search", "Queries and relevant passages"], RED)]):
            panel(c, 130+i*570, 290, 520, 320, title, body, color)
        panel(c, 200, 700, 1520, 155, "RETRIEVAL SIGNALS CAN COME FROM MANY SOURCES", ["Human judgments · behavior · weak or synthetic labels · self-supervised pairs"], RED, p)
        self.note(c, "The examples and targets shape what is rewarded; transfer to a deployment task must be tested")

    def domain_models(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body) in enumerate([
            ("BioBERT", ["Continue pretraining", "on biomedical literature"]),
            ("BiomedBERT", ["Start with biomedical", "text and vocabulary"]),
            ("SciBERT", ["Pretrain on", "scientific literature"])]):
            panel(c, 130+i*570, 290, 520, 290, title, body, TEAL)
        panel(c, 225, 680, 1470, 175, "RETRIEVAL NEEDS A SUITABLE ARCHITECTURE AND TRAINING", ["Sentence-BERT adapts complete-text representations for useful comparison."], RED, p)
        self.note(c, "Domain pretraining changes language experience; it does not by itself specify which passage to rank")

    def pipeline_roles(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body, color) in enumerate([
            ("QUERY INTERPRETATION", ["Read the request", "Help determine its meaning"], BLUE),
            ("FIRST-STAGE ENCODING", ["Make query / document vectors", "Support candidate retrieval"], TEAL),
            ("RERANKING", ["Compare an existing shortlist", "Change its ordering"], RED)]):
            panel(c, 130+i*570, 335, 520, 350, title, body, color)
        text(c, "“Uses BERT” does not locate the model in the pipeline.", 960, 815, 36, INK, p, True, align="center", width=1710)
        self.note(c, "Alternative roles for a model family · This diagram does not assert that every system uses all three")

    def two_questions(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 300, 770, 390, "1 · WHAT WAS IT TRAINED TO DO?", ["Was it trained for retrieval?", "What targets and relationships?", "Does that transfer to your task?"], BLUE)
        panel(c, 1000, 300, 770, 390, "2 · WHERE IS IT USED?", ["Interpreting a query?", "First-stage retrieval?", "Comparing a shortlist?"], RED, .2+.8*p)
        text(c, "Training shapes the geometry. Evaluation tests its usefulness.", 960, 820, 35, INK, p, True, align="center", width=1710)
        self.note(c, "Chapter 6 examines what one vector represents and how query–document comparisons are trained")

    def poster(self, c):
        c.clear(skia.Color(*CREAM))
        text(c, "HOW SEARCH DECIDES WHAT YOU SEE", 130, 130, 27, MUTED, bold=True)
        text(c, f"CHAPTER 5 · FILM {self.script['episode_number']:02d}", 130, 220, 30, self.accent, bold=True)
        titles = {1: ["The map", "nobody drew."], 2: ["One word,", "two locations."], 3: ["The wrong", "prediction game."]}
        rows(c, titles[self.script['episode_number']], 130, 405, 95, INK, bold=True, step=132, width=1190)
        text(c, self.script["subtitle"], 130, 750, 31, MUTED, width=1130)
        for x1, y1, x2, y2 in [(1410, 620, 1570, 350), (1570, 350, 1740, 520), (1410, 620, 1740, 520)]:
            line(c, x1, y1, x2, y2, self.accent, .35, 3)
        for x, y, label in [(1410, 620, "A"), (1570, 350, "B"), (1740, 520, "C")]:
            circle(c, x, y, 34, self.accent)
            text(c, label, x, y+11, 29, PAPER, bold=True, align="center")
        text(c, "Original animated investigation · Narrated and captioned", 130, 890, 26, self.accent)
        text(c, "Adapted from Aaron Tay · CC BY 4.0", 130, 1000, 23, MUTED)
