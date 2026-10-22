"""Original Chapter 4 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter4_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import FRUIT_RECORDS, FRUIT_QUERY, ILLUSTRATIVE_ORDER, eligible, check_examples


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
        text(c, f"CHAPTER 4   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 4 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Teaching examples from the pinned Chapter 4 · Indexed terms determine matches"):
        text(c, message, 960, 900, 21, MUTED, align="center", width=1700)

    def fruit_cards(self, c, admitted=("A", "B", "C", "D"), y=360, p=1):
        for i, (ident, terms) in enumerate(FRUIT_RECORDS.items()):
            x = 130+i*435
            keep = ident in admitted
            alpha = 1 if keep else 1-.7*p
            detail = [term for term in ("apple", "orange", "banana", "pear", "grape") if term in terms]
            card(c, x, y, ident, 350, 310, BLUE if keep else MUTED, alpha, detail=detail)

    def doors_prediction(self, c, t, s):
        p = self.r(t, s)
        panel(c, 140, 320, 720, 350, "TYPED QUERY", ["apple", "orange", "banana"], BLUE)
        arrow(c, 900, 500, 1030, 500, BLUE, p)
        panel(c, 1080, 320, 700, 350, "RETURNED RECORD", ["apple", "orange", "No banana"], TEAL, .2+.8*p)
        text(c, "Which terms were compulsory?", 960, 810, 48, INK, p, True, align="center")
        self.note(c, "A record lacking a typed word does not identify the retrieval architecture")

    def fruit_records(self, c, t, s):
        pill(c, "apple  orange  banana", 720, 260, BLUE, size=27)
        self.fruit_cards(c)
        p = self.r(t, s)
        text(c, "One collection. Change only admission.", 960, 820, 43, INK, p, True, align="center")
        self.note(c, "Cards show term presence; frequencies and full document lengths are not supplied")

    def three_rules(self, c, t, s):
        for i, ident in enumerate(FRUIT_RECORDS):
            text(c, ident, 1040+i*205, 300, 40, BLUE, bold=True, align="center")
        rules = [("ALL THREE", 3), ("AT LEAST TWO", 2), ("ANY ONE", 1)]
        for j, (label, minimum) in enumerate(rules):
            p = ease((t-self.at(s, 0)-j*6)/1.2)
            y = 350+j*155
            rect(c, 140, y, 1640, 130, PAPER, .8)
            text(c, label, 180, y+55, 32, BLUE, bold=True)
            ids = eligible(FRUIT_RECORDS, FRUIT_QUERY, minimum)
            text(c, "Admit "+", ".join(ids), 180, y+99, 25, MUTED, p)
            for i, ident in enumerate(FRUIT_RECORDS):
                keep = ident in ids
                circle(c, 1040+i*205, y+65, 36, TEAL if keep else RULE, p)
                text(c, "YES" if keep else "—", 1040+i*205, y+74, 23, PAPER if keep else MUTED, p, True, align="center")
        self.note(c, "All three rules are lexical · Any-match eligibility is the posting-list union (OR)")

    def stipulated_order(self, c, t, s):
        p = self.r(t, s, 0, "Suppose", 2)
        pill(c, "ANY-MATCH: A, B, C QUALIFY", 665, 260, BLUE)
        for i, ident in enumerate(("A", "B", "C")):
            target = ILLUSTRATIVE_ORDER.index(ident)
            x = lerp(240+i*560, 240+target*560, p)
            card(c, x, 390, ident, 310, 265, BLUE)
        text(c, "Suppose the scorer orders them B, A, C", 960, 765, 40, BLUE, p, True, align="center")
        text(c, "Rarity + term frequency + length can affect scores", 960, 830, 30, MUTED, self.r(t, s), align="center")
        self.note(c, "Stipulated order from Figure 4.1 · These presence-only cards cannot determine BM25 scores")

    def output_boundary(self, c, t, s):
        p = self.r(t, s, 0, "C", 1.2)
        text(c, "STIPULATED RANKING", 200, 290, 28, BLUE, bold=True)
        for i, ident in enumerate(ILLUSTRATIVE_ORDER):
            x = 230+i*560
            card(c, x, 360, ident, 310, 270, BLUE, 1 if i<2 else 1-.65*p)
            text(c, str(i+1), x+155, 690, 35, BLUE, bold=True, align="center")
        line(c, 1280, 330, 1280, 745, RED, p, 4)
        pill(c, "TOP 2", 1120, 280, RED, p)
        panel(c, 180, 755, 750, 100, "C: eligible, below boundary", [], GOLD, p)
        panel(c, 990, 755, 750, 100, "D: never eligible", [], MUTED, p)
        self.note(c, "Absence from the final output can have different causes")

    def reported_count(self, c, t, s):
        p = self.r(t, s)
        rect(c, 150, 300, 770, 360, PAPER)
        rect(c, 1000, 300, 770, 360, PAPER)
        text(c, "ABOUT 9.4 MILLION", 535, 445, 58, BLUE, bold=True, align="center", width=710)
        text(c, "reported matches", 535, 535, 33, MUTED, align="center")
        text(c, "1,000", 1385, 445, 87, RED, bold=True, align="center")
        text(c, "documented display limit", 1385, 535, 32, MUTED, align="center", width=710)
        rows(c, ["Count, ordering and viewable set are separate.", "A display cap does not establish a global top-k computation."], 960, 755, 31, INK, p, step=60, align="center", width=1700)
        self.note(c, "Google Scholar evidence reported in the pinned chapter · No current-service test is claimed")

    def three_controls(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body, color) in enumerate([
            ("1 · ADMISSION", ["Who may compete?", "All / some / any terms"], BLUE),
            ("2 · RANKING", ["How are they ordered?", "Weights and other signals"], TEAL),
            ("3 · OUTPUT", ["How many are retained?", "Top-k or display boundary"], RED)]):
            panel(c, 130+i*570, 350, 520, 350, title, body, color, .3+.7*p)
        text(c, "A result screen leaves several controls hidden.", 960, 820, 39, INK, p, True, align="center", width=1700)
        self.note(c, "Non-Boolean behavior can remain lexical · The interface alone cannot identify the pipeline")

    def weak_prediction(self, c, t, s):
        p = self.r(t, s)
        panel(c, 160, 270, 1600, 185, "ORIGINAL QUERY", ["delulu  job  interview  expectations"], BLUE)
        pill(c, "+ foolish", 825, 495, RED, size=32)
        panel(c, 160, 600, 750, 230, "COMPULSORY", ["Can change who enters", "A missing term can exclude"], RED, .2+.8*p)
        panel(c, 1010, 600, 750, 230, "OPTIONAL EVIDENCE", ["Can change competition", "A poor term can add weight"], GOLD, .2+.8*p)
        self.note(c, "The quality of a proposed synonym depends on the searcher's information need")

    def pair(self, c, y=290):
        for i, (ident, title, details) in enumerate([
            ("A", ["Delulu expectations", "during a job interview"], ["Original four terms", "No foolish"]),
            ("F", ["Why foolish job applicants", "misread the interview"], ["foolish, job, interview", "No delulu or expectations"])]):
            x = 150+i*860
            card(c, x, y, ident, 760, 370, BLUE if i==0 else RED, detail=title)
            rows(c, details, x+35, y+275, 27, MUTED, step=45, width=690)

    def lab_pair(self, c, t, s):
        self.pair(c, 320)
        text(c, "Term matches are evidence, not a relevance verdict.", 960, 815, 37, INK, self.r(t, s), True, align="center", width=1710)
        self.note(c, "A and F are original six-record Evidence Lab examples, linked from Chapter 4")

    def compulsory_failure(self, c, t, s):
        p = self.r(t, s)
        pill(c, "ALL FIVE TERMS REQUIRED", 715, 260, RED)
        self.pair(c, 355)
        for i, label in enumerate(("A OUT: lacks foolish", "F OUT: lacks delulu + expectations")):
            pill(c, label, 240+i*810, 765, RED, p, size=24)
        self.note(c, "A met the original four-term AND · No ranking can recover A from this unchanged eligible set")

    def optional_failure(self, c, t, s):
        p = self.r(t, s)
        text(c, "ANY MATCH IS SUFFICIENT", 960, 290, 35, BLUE, bold=True, align="center")
        items = [("A", ["delulu", "job", "interview", "expectations"], BLUE),
                 ("F", ["job", "interview"], RED)]
        for j, (ident, labels, color) in enumerate(items):
            y=365+j*205
            rect(c, 150, y, 1620, 165, PAPER)
            text(c, ident, 205, y+95, 56, color, bold=True)
            for i, label in enumerate(labels):
                pill(c, label, 350+i*285, y+60, color, size=23)
            if ident=="F":
                pill(c, "+ foolish", 920, y+60, RED, p, size=23)
        text(c, "A remains eligible. F gains another scoring term.", 960, 830, 37, INK, p, True, align="center", width=1700)
        self.note(c, "Each chip indicates a match, not equal numerical weight · No A/F score or ranking is asserted")

    def rarity_quality(self, c, t, s):
        p = self.r(t, s)
        for i, ident in enumerate("ABCDEF"):
            x=145+i*280
            card(c, x, 340, ident, 230, 240, RED if ident=="F" else MUTED, detail=["foolish"] if ident=="F" else ["—"])
        text(c, "Only F contains foolish: df = 1 of 6", 960, 680, 41, RED, bold=True, align="center")
        panel(c, 220, 745, 1480, 105, "High rarity weight does not establish a good synonym.", [], BLUE, p)
        self.note(c, "Document frequency checked against all six pinned lab records · Usefulness depends on the need")

    def saturation_limit(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 310, 770, 390, "SATURATION ADDRESSES", ["More repeats of the same term", "inside one document", "Diminishing added credit"], BLUE)
        panel(c, 1000, 310, 770, 390, "THE QUERY PROBLEM", ["Is foolish a good substitute?", "A question about the concept", "Saturation cannot decide it"], RED, .25+.75*p)
        text(c, "A weighting rule cannot repair a poor expression of the need.", 960, 820, 36, INK, p, True, align="center", width=1700)
        self.note(c, "Conceptual comparison · No measured score, benchmark or numerical ranking is shown")

    def inspect_expansion(self, c, t, s):
        p = self.r(t, s)
        panel(c, 140, 300, 790, 430, "WITH / WITHOUT THE TERM", ["Hold the collection fixed", "Compare who enters or disappears", "Inspect new scoring evidence", "Judge against the information need"], BLUE)
        panel(c, 1000, 300, 780, 430, "WHAT JOB DOES IT DO?", ["A compulsory condition?", "An alternative inside a group?", "Optional scoring evidence?", "Inspect the proposed expansion"], RED, .25+.75*p)
        text(c, "Correct execution can still serve a poor query.", 960, 825, 40, INK, p, True, align="center")
        self.note(c, "Comparison is a proposed investigation, not a new relevance experiment performed for these films")

    def missing_prediction(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 300, 760, 350, "YOU TYPE", ["delulu", "job interview"], TEAL)
        panel(c, 1010, 300, 760, 350, "VISIBLE TITLE", ["Job interview", "expectations"], BLUE)
        text(c, "Where did delulu go?", 960, 760, 57, TEAL, bold=True, align="center")
        text(c, "One visible absence. Four possible histories.", 960, 840, 34, INK, p, align="center")
        self.note(c, "Illustrative screen · A title alone cannot diagnose a search product's architecture")

    def query_history(self, c, t, s, before, after, operation, color):
        p = self.r(t, s)
        panel(c, 180, 300, 1560, 150, "TYPED INPUT", [before], BLUE)
        arrow(c, 960, 475, 960, 570, color, p)
        pill(c, operation, 1130, 490, color, p, size=24)
        panel(c, 180, 610, 1560, 180, "RETRIEVAL RECEIVES", [after], color, .2+.8*p)

    def analysis_history(self, c, t, s):
        self.query_history(c, t, s, "the job interview", "job interview", "Optional stop-word rule", TEAL)
        self.note(c, "Illustrative analysis choice · Stop lists and other analysis rules depend on the system")

    def rewrite_history(self, c, t, s):
        self.query_history(c, t, s, "delulu job expectations", "unrealistic job expectations", "Explicit reformulation", RED)
        self.note(c, "Possible rewrite, not a diagnosis of any named product · Inspect the processed query")

    def optional_history(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 300, 760, 390, "RETRIEVAL INPUT", ["delulu  job  interview", "delulu is optional", "It may have no postings at all"], TEAL)
        panel(c, 1010, 300, 760, 390, "THIS RECORD", ["job + interview match", "Any match: may enter", "Required unmatched term: fails"], BLUE, .25+.75*p)
        text(c, "Retained in the query does not mean required.", 960, 820, 40, INK, p, True, align="center")
        self.note(c, "With strict AND, any compulsory term with no postings makes the whole eligible set empty")

    def hidden_history(self, c, t, s):
        p = self.r(t, s)
        panel(c, 170, 275, 1580, 180, "VISIBLE TITLE", ["Job interview expectations"], BLUE)
        panel(c, 170, 530, 1580, 270, "INDEXED ABSTRACT", ["We examine delulu expectations.", "The term matched; the title did not show it."], TEAL, .15+.85*p)
        self.note(c, "Inspect indexed fields, versions and other searchable evidence before inferring an absent match")

    def four_jobs(self, c, t, s):
        p = self.r(t, s)
        labels = [("ANALYSIS", ["Prepare strings for matching", "Tokens, normalisation, stemming"], BLUE),
                  ("EXECUTION RULES", ["Choose the required conditions", "Required / optional / minimum"], RED),
                  ("UNDERSTANDING", ["Interpret entities, dates or intent", "Can leave all words unchanged"], TEAL),
                  ("TRANSFORMATION", ["Change the retrieval input", "Correct, expand or restructure"], GOLD)]
        for i, (title, body, color) in enumerate(labels):
            panel(c, 140+(i%2)*860, 270+(i//2)*285, 780, 245, title, body, color, 1 if i<2 else .25+.75*p)
        self.note(c, "Understanding alone does not remove a word; it matters when its interpretation causes a change")

    def natural_language(self, c, t, s):
        p = self.r(t, s)
        panel(c, 130, 285, 510, 340, "QUESTION", ["What explains", "unrealistic expectations", "in job interviews?"], BLUE)
        panel(c, 705, 285, 510, 340, "POSSIBLE REWRITE", ["(delulu OR unrealistic)", "AND job AND interview", "Parser or language model"], TEAL, .25+.75*p)
        panel(c, 1280, 285, 510, 340, "LEXICAL RETRIEVAL", ["Inverted index", "Boolean admission", "BM25 ranking"], RED, .25+.75*p)
        arrow(c, 650, 450, 692, 450, TEAL, p)
        arrow(c, 1225, 450, 1267, 450, RED, p)
        text(c, "Two routes across a vocabulary gap", 960, 725, 35, INK, bold=True, align="center")
        pill(c, "Change the query; keep lexical matching", 200, 780, TEAL, p, size=23)
        pill(c, "Change the representation", 1120, 780, BLUE, p, size=23)
        self.note(c, "Illustrative transformation · Natural-language input does not identify the retrieval method")

    def evidence_questions(self, c, t, s):
        p = self.r(t, s)
        labels = ["Analysis removed it", "Rewriting changed it", "It was optional", "It matched out of view"]
        for i, label in enumerate(labels):
            panel(c, 130+i*435, 300, 390, 210, f"HISTORY {i+1}", [label], TEAL)
        for i, (title, body) in enumerate([
            ("PROCESSED QUERY", ["What reached retrieval?", "Which transformations?"]),
            ("ADMISSION RULES", ["What was required?", "What could be optional?"]),
            ("INDEXED EVIDENCE", ["Which fields and versions?", "What pipeline is documented?"])]):
            panel(c, 130+i*570, 590, 520, 250, title, body, BLUE, .25+.75*p)
        self.note(c, "Part I separates lexical retrieval from strict all-term conjunction · Part II investigates representations")

    def poster(self, c):
        c.clear(skia.Color(*CREAM))
        text(c, "HOW SEARCH DECIDES WHAT YOU SEE", 130, 130, 27, MUTED, bold=True)
        text(c, f"CHAPTER 4 · FILM {self.script['episode_number']:02d}", 130, 220, 30, self.accent, bold=True)
        titles = {1: ["Three doors,", "one index."], 2: ["One bad word,", "two failures."], 3: ["Four lives of", "a missing word."]}
        rows(c, titles[self.script['episode_number']], 130, 405, 98, INK, bold=True, step=132, width=1190)
        text(c, self.script["subtitle"], 130, 750, 32, MUTED, width=1130)
        for i, ident in enumerate(("A", "B", "C")):
            card(c, 1410+i*25, 315+i*115, ident, 285, 335, self.accent, angle=(i-1)*3)
        text(c, "Original animated investigation · Narrated and captioned", 130, 890, 26, self.accent)
        text(c, "Adapted from Aaron Tay · CC BY 4.0", 130, 1000, 23, MUTED)
