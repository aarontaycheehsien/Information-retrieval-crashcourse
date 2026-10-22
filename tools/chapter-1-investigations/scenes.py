"""Original Chapter 1 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter1_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

CANDIDATES = tuple(range(30))
RERANKED_POSITIONS = tuple((i*7) % 30 for i in CANDIDATES)
GRID_COLUMNS, GRID_ROWS = 94, 100
REPORTED_MATCHES, DISPLAY_CAP = 9_400_000, 1_000
QUESTION_RESULTS, KEYWORD_RESULTS = 13, 35_300


def check_examples():
    assert len(CANDIDATES) == 30
    assert set(RERANKED_POSITIONS) == set(CANDIDATES), "Reranking must preserve membership"
    assert sum(p < 5 for p in RERANKED_POSITIONS) == 5
    assert 47 not in CANDIDATES, "The illustrative gold paper stays outside this round"
    assert GRID_COLUMNS*GRID_ROWS*DISPLAY_CAP == REPORTED_MATCHES
    assert QUESTION_RESULTS == 13 and KEYWORD_RESULTS == 35_300
    assert math.log10(QUESTION_RESULTS+1) < math.log10(KEYWORD_RESULTS+1)


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
        self.count_picture = None

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
        text(c, f"CHAPTER 1   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 1 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Schematic teaching illustration · No measured product scores or proportions"):
        text(c, message, 960, 900, 21, MUTED, align="center", width=1700)

    def opening(self, c, t, s):
        p = self.r(t, s, 0, "sixth")
        for i in range(5):
            card(c, 160+i*250, 360, str(i+1), 190, 265, TEAL, angle=(i%3-1)*2)
            pill(c, "ACCURATE", 157+i*250, 695, TEAL)
        card(c, 1470, lerp(590, 330, p), "P", 235, 310, GOLD, p, angle=-4)
        text(c, "LANDMARK", 1590, 490, 29, GOLD, p, True, align="center")
        text(c, "Which decision excluded it?", 960, 830, 43, RED, self.r(t, s), True, align="center")
        self.note(c, "Invented paper identities; no real study is claimed to have been omitted")

    def pipeline(self, c, t, s):
        p = self.r(t, s)
        labels = [("QUERY", ["LLM conversion", "Boolean variants + OR"], BLUE),
                  ("RETRIEVAL", ["Central Discovery Index", "Up to 30 results"], BLUE),
                  ("RERANKING", ["Embedding-based", "Identify five sources"], TEAL),
                  ("WORKING SET", ["Five sources", "Abstracts supplied"], TEAL),
                  ("OVERVIEW", ["GPT-4.1 Mini", "Inline citations"], RED)]
        for i, (title, body, col) in enumerate(labels):
            x = 110+i*347
            panel(c, x, 370, 305, 315, title, body, col, 1 if i < 2 else .18+.82*p)
            if i < 4:
                arrow(c, x+314, 520, x+335, 520, col)
        text(c, "Evidence selection precedes answer writing.", 960, 805, 38, INK, p, True, align="center")
        self.note(c, "Primo Research Assistant · Documentation checked by September 2026 · Not a new behavioral test")

    def coverage(self, c, t, s):
        p = self.r(t, s)
        rect(c, 170, 290, 1200, 555, PAPER)
        rect(c, 170, 290, 1200, 555, RULE, stroke=2)
        text(c, "WIDER LIBRARY DISCOVERY", 220, 355, 32, BLUE, bold=True)
        rect(c, 390, 420, 830, 310, CREAM)
        rect(c, 390, 420, 830, 310, TEAL, stroke=3)
        text(c, "ASSISTANT'S SEARCHABLE SCOPE", 805, 485, 29, TEAL, bold=True, align="center", width=750)
        rows(c, ["CDI metadata and abstracts", "Subject to content exclusions"], 805, 570, 29, INK, align="center")
        card(c, 215, 505, "A", 135, 180, GOLD, p)
        rows(c, ["Discoverable", "does not guarantee", "assistant-searchable."], 1600, 470, 31, GOLD, p, bold=True, align="center", width=430)
        self.note(c, "Content scope: October 2026 documentation check · Nested areas are not measured proportions")

    def candidates(self, c, t, s):
        move = self.r(t, s, 0, "Thirty", 2.1)
        rank = self.r(t, s, 0, "order", 1.8)
        select = self.r(t, s, 0, "five", 1.0)
        gold = self.r(t, s, 0, "gold")
        for label, x, width in [("INDEX", 100, 430), ("30 CANDIDATES", 650, 545), ("5 FOR THE WRITER", 1360, 450)]:
            text(c, label, x, 270, 25, BLUE, bold=True, width=width)
            rect(c, x-14, 300, width, 490, RULE, stroke=2)
        for i in range(60):
            tiny(c, 105+(i%10)*38, 330+(i//10)*66, 27, 43,
                 color=GOLD if i == 47 else BLUE, a=.35 if i < 30 else .75)
        for i, position in enumerate(RERANKED_POSITIONS):
            ox, oy = 105+(i%10)*38, 330+(i//10)*66
            x = lerp(ox, lerp(665+(i%6)*83, 665+(position%6)*83, rank), move)
            y = lerp(oy, lerp(330+(i//6)*88, 330+(position//6)*88, rank), move)
            chosen = position < 5
            tiny(c, x, y, 62, 73, i+1, TEAL if chosen else BLUE)
            if chosen:
                tiny(c, 1370+position*78, 465, 63, 100, i+1, TEAL, select)
        pill(c, "P stays outside this round", 95, 825, GOLD, gold)
        text(c, "Reordering cannot add a member.", 1230, 845, 30, RED, self.r(t, s), True, align="center", width=1120)
        self.note(c, "Illustration: exactly 30 candidates in one round; original records remain in the index")

    def losses(self, c, t, s):
        p = self.r(t, s)
        for x, title, body, col in [(140, "A  OUTSIDE SCOPE", ["Not assistant-searchable", "Needs coverage evidence", "Wider discovery is insufficient"], GOLD),
                                    (710, "B  CANDIDATE, NOT SUPPLIED", ["Entered the 30", "Missed the five-source set", "Needs intermediate traces"], BLUE),
                                    (1280, "C  SUPPLIED, NOT CITED", ["Reached the working set", "Absent from the overview", "Compare sources and citations"], RED)]:
            panel(c, x, 330, 500, 385, title, body, col)
        text(c, "If the trace is hidden, keep the loss point open.", 960, 825, 35, INK, p, True, align="center", width=1710)
        self.note(c, "Three stipulated cases; a missing citation alone establishes none of them")

    def stages(self, c, t, s):
        p = self.r(t, s)
        rect(c, 110, 270, 1700, 90, INK)
        text(c, "CONTROLLER — chooses and sequences actions", 960, 329, 31, PAPER, bold=True, align="center")
        labels = [["Query", "transformation"], ["Analysis &", "execution"], ["First-stage", "retrieval"],
                  ["Fusion", "candidate lists"], ["Reranking", "a shortlist"], ["Presentation", "what is shown"]]
        for i, label in enumerate(labels):
            x = 110+i*290
            a = 1-.55*p if i == 3 else 1
            line(c, x+125, 360, x+125, 430, RULE)
            rect(c, x, 430, 250, 180, PAPER, a)
            rows(c, label, x+125, 495, 27, BLUE, a, align="center", bold=True, width=220)
            if i < 5:
                arrow(c, x+261, 520, x+280, 520, BLUE)
        rows(c, ["Primo: no separate fusion stage documented", "Scopus AI: historical 2024 variants + vector retrieval + fusion"], 960, 740, 31, RED, p, align="center", step=66, width=1700)
        self.note(c, "A general map of possible stages; presence and control require product-specific evidence")

    def rag(self, c, t, s):
        p = self.r(t, s)
        panel(c, 130, 390, 490, 340, "SUPPLIED EVIDENCE", ["Selected sources", "Limited working set"], TEAL)
        arrow(c, 650, 560, 770, 560, TEAL)
        panel(c, 800, 390, 350, 340, "WRITER", ["Language model", "Conditioned on evidence"], BLUE)
        arrow(c, 1180, 560, 1300, 560, RED)
        panel(c, 1330, 390, 460, 340, "GENERATED ANSWER", ["May omit a source", "May invent a citation", "May draw on parameters"], RED, .2+.8*p)
        pill(c, "Parameters / other learned knowledge", 665, 265, BLUE, p)
        arrow(c, 975, 310, 975, 370, BLUE, p)
        text(c, "Inspect what the writer actually received.", 960, 825, 39, INK, p, True, align="center")
        self.note(c, "RAG constrains supplied evidence; it does not guarantee grounded claims")

    def match(self, c, t, s):
        p = self.r(t, s)
        card(c, 240, 320, "STUDY", 500, 440, TEAL, detail=["Right service", "Right setting", "Right publication dates", "Empirical evidence"])
        arrow(c, 790, 535, 990, 535, TEAL)
        panel(c, 1050, 370, 660, 340, "A USEFUL MATCH", ["It meets the search conditions.", "Does it help with the task?"], TEAL)
        text(c, "Relevant to someone, for something.", 960, 845, 40, INK, p, True, align="center")
        self.note(c, "Hypothetical study from the chapter; matching does not settle usefulness")

    def need(self, c, t, s):
        p = self.r(t, s)
        labels = [["Information", "need"], ["Query /", "representation"], ["Retrieval", "signals"], ["Retrieved", "records"], ["Human", "judgement"]]
        for i, label in enumerate(labels):
            x = 105+i*346
            rect(c, x, 365, 290, 205, PAPER)
            rows(c, label, x+145, 445, 28, TEAL if i in (0, 4) else BLUE, align="center", bold=True, width=260)
            if i < 4:
                arrow(c, x+303, 465, x+333, 465, RULE)
        line(c, 451, 625, 1489, 625, BLUE, p, 3)
        text(c, "What the system works with directly", 970, 690, 31, BLUE, p, True, align="center")
        arrow(c, 1635, 730, 595, 730, TEAL, p)
        text(c, "Detailed purpose and feedback can improve the estimate.", 960, 820, 32, INK, p, True, align="center", width=1700)
        self.note(c, "Queries, filters and task briefs can express substantial detail about the information need")

    def strategy(self, c, t, s):
        p = self.r(t, s)
        groups = [("generative AI", "large language models"), ("academic library", "university library"), ("research support", "research consultation")]
        for i, alternatives in enumerate(groups):
            x = 135+i*570
            panel(c, x, 350, 500, 340, "ALTERNATIVES", [alternatives[0], "OR", alternatives[1]], [TEAL, BLUE, RED][i])
        pill(c, "Publication date: 2024 onwards", 650, 775, TEAL, p)
        self.note(c, "Hypothetical strategy for empirical studies of generative-AI research support in academic libraries")

    def purposes(self, c, t, s):
        p = self.r(t, s)
        card(c, 805, 275, "SAME STUDY", 310, 290, TEAL, detail=["Short demonstration", "Positive reactions"])
        arrow(c, 805, 475, 640, 590, TEAL)
        arrow(c, 1115, 475, 1280, 590, RED, p)
        panel(c, 150, 590, 650, 270, "INTRODUCTORY WORKSHOP", ["A concrete service example", "How participants responded"], TEAL)
        panel(c, 1120, 590, 650, 270, "SERVICE-ADOPTION DECISION", ["Accuracy? Workload? Real use?", "Reactions alone are insufficient"], RED, p)
        self.note(c, "Invented study · The match stays fixed; its contribution changes with the purpose")

    def followup(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body, col) in enumerate([("SEARCH AGAIN", ["Accuracy evaluations", "Workload and real-world use"], TEAL),
                                                ("ASSESS THE STUDIES", ["Methods and conditions", "What the findings establish"], BLUE),
                                                ("REFINE THE QUESTION", ["Use the evidence judgement", "Guide another search"], RED)]):
            x = 140+i*570
            panel(c, x, 330, 500, 340, title, body, col)
            if i < 2:
                arrow(c, x+514, 500, x+556, 500, col)
        arrow(c, 1530, 735, 390, 735, TEAL, p)
        text(c, "Compulsory terms can miss unexpected wording or full-text-only details.", 960, 830, 29, RED, p, True, align="center", width=1730)
        self.note(c, "Searching brings evidence forward; judgement can guide the next search")

    def screening(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 340, 680, 400, "RETRIEVAL", ["Dependable searchable concepts", "A broader potentially relevant set", "Do not force every criterion in"], TEAL)
        arrow(c, 870, 535, 1050, 535, TEAL, p)
        panel(c, 1090, 340, 680, 400, "SCREENING", ["Read what retrieval cannot encode", "Assess eligibility criteria", "Inspect inconsistent or full-text detail"], BLUE, .2+.8*p)
        text(c, "A deliberate division of work.", 960, 835, 42, INK, p, True, align="center")
        self.note(c, "Search-resistant concepts may be poorly indexed or inconsistently described; no recall claim is made")

    def lenses(self, c, t, s):
        p = self.r(t, s)
        items = [(150, 280, "ESTIMATED MATCH", ["A system's score or rule"], BLUE),
                 (1040, 280, "TOPICAL SUITABILITY", ["Does it address the topic?"], TEAL),
                 (150, 570, "CONTRIBUTION TO UNDERSTANDING", ["What does the reader learn?"], GOLD),
                 (1040, 570, "USEFULNESS FOR A TASK", ["Does it help accomplish the purpose?"], RED)]
        for x, y, title, body, col in items:
            panel(c, x, y, 720, 225, title, body, col)
        text(c, "A high score cannot change what a study measured.", 960, 855, 32, INK, p, True, align="center", width=1720)
        self.note(c, "Related perspectives, with no fixed hierarchy; Chapter 14 develops their evaluation uses")

    def impossible(self, c, t, s):
        p = self.r(t, s)
        panel(c, 160, 300, 1580, 200, "QUESTION + AN INVENTED TOKEN", ["Is there an open access citation advantage?  xqzblorp"], BLUE)
        panel(c, 180, 600, 680, 230, "STRICT-AND PREDICTION", ["No occurrence of a required term → no matches"], BLUE)
        panel(c, 1040, 600, 680, 230, "CHAPTER'S scite OBSERVATION", ["Useful-looking results remain"], RED, p)
        self.note(c, "Observed behavior attributed to the chapter screenshot · On-screen token is schematic")

    def count_grid(self):
        if self.count_picture is None:
            recorder = skia.PictureRecorder()
            canvas = recorder.beginRecording(skia.Rect.MakeWH(W, H))
            for i in range(GRID_COLUMNS*GRID_ROWS):
                rect(canvas, 100+(i%GRID_COLUMNS)*15, 310+(i//GRID_COLUMNS)*5, 11, 3, RULE, radius=0)
            self.count_picture = recorder.finishRecordingAsPicture()
        return self.count_picture

    def window(self, c, t, s):
        p = self.r(t, s)
        c.drawPicture(self.count_grid())
        rect(c, 100, 310, 11, 3, RED, radius=0)
        rect(c, 96, 305, 19, 13, RED, radius=1, stroke=2)
        arrow(c, 125, 260, 106, 299, RED)
        text(c, "ONE MARK = 1,000", 165, 268, 26, RED, bold=True)
        rows(c, ["≈9.4 million", "reported matches"], 1660, 430, 30, BLUE, align="center", bold=True, width=300)
        rows(c, ["1,000", "display cap"], 1660, 610, 35, RED, p, align="center", bold=True, width=300)
        text(c, "Reported count ≠ fully scored or ranked set", 960, 853, 35, INK, p, True, align="center")
        self.note(c, "9,400 equal marks · Google Scholar example in Chapter 1 · Display cap from Google help")

    def question(self, c, t, s):
        p = self.r(t, s)
        chart_x, chart_width = 610, 1080
        scale = lambda count: math.log10(count+1)/math.log10(100_000+1)*chart_width
        for i, (label, count, col) in enumerate([("Full question", QUESTION_RESULTS, BLUE), ("Unquoted keywords", KEYWORD_RESULTS, RED)]):
            y = 385+i*205
            text(c, label, 150, y-15, 24, col, bold=True, width=420)
            query = ["Is there an open access", "citation advantage?"] if i == 0 else ["open access", "citation advantage"]
            rows(c, query, 150, y+37, 25, INK, width=420)
            rect(c, chart_x, y, scale(count), 72, col)
            text(c, "13" if i == 0 else "≈35,300", chart_x+scale(count)+18, y+49, 29, col, bold=True, width=210)
        for count, label in [(0, "0"), (10, "10"), (100, "100"), (1000, "1k"), (10_000, "10k"), (100_000, "100k")]:
            x = chart_x+scale(count)
            line(c, x, 710, x, 724, MUTED)
            text(c, label, x, 760, 22, MUTED, align="center")
        text(c, "LOGARITHMIC BAR LENGTHS: log10(count + 1)", 1150, 815, 25, MUTED, bold=True, align="center")
        text(c, "Quality assessment also used inspected leading results and known literature.", 960, 855, 26, INK, p, True, align="center", width=1740)
        self.note(c, "Semantic Scholar · Author's August 2026 comparison · Counts alone do not establish search quality")

    def limits(self, c, t, s):
        p = self.r(t, s)
        for x, title, body, col in [(140, "01  ADMISSION", ["Which terms were required?", "Why did results remain?", "Revisited in Chapter 4"], BLUE),
                                    (710, "02  RANKING / DISPLAY", ["Which fraction was shown?", "What does the total establish?", "Revisited in Chapter 4"], GOLD),
                                    (1280, "03  QUERY INTERPRETATION", ["How was the question handled?", "What does a label establish?", "Part II, especially Chapter 7"], RED)]:
            panel(c, x, 335, 500, 390, title, body, col)
        text(c, "Visible behavior leaves mechanisms open.", 960, 830, 40, INK, p, True, align="center")
        self.note(c, "Source observations are retained as dated illustrations; no live product searches were rerun")

    def axes(self, c, t, s):
        p = self.r(t, s)
        for x, y, title, col in [(430, 310, "ITERATIVE SEARCH", BLUE), (1020, 310, "DEEP RESEARCH", TEAL),
                                  (430, 570, "QUICK SEARCH", GOLD), (1020, 570, "QUICK ANSWER", RED)]:
            rect(c, x, y, 540, 220, PAPER)
            text(c, title, x+270, y+120, 29, col, bold=True, align="center", width=490)
        arrow(c, 390, 810, 1610, 810, INK)
        arrow(c, 390, 810, 390, 270, INK)
        rows(c, ["Repeated", "retrieval"], 240, 395, 28, MUTED, align="center")
        rows(c, ["Single /", "limited pass"], 240, 675, 28, MUTED, align="center")
        text(c, "Ranked records", 700, 853, 26, MUTED, align="center")
        text(c, "Written answer / report", 1290, 853, 26, MUTED, align="center")
        pill(c, "Agency is a separate question: who chooses the next action?", 440, 225, TEAL, p)
        self.note(c, "Conceptual quadrants, not current product placements · Neither axis records agency")

    def llms(self, c, t, s):
        p = self.r(t, s)
        rect(c, 140, 300, 1110, 470, PAPER)
        text(c, "INSIDE RETRIEVAL", 695, 365, 30, BLUE, bold=True, align="center")
        for i, label in enumerate(["Write a query", "Invent search text", "Rerank candidates", "Control the loop"]):
            x, y = 185+(i%2)*525, 420+(i//2)*160
            rect(c, x, y, 470, 115, CREAM)
            text(c, label, x+235, y+70, 29, BLUE, bold=True, align="center", width=440)
        panel(c, 1370, 380, 420, 310, "GENERATION", ["Write the answer", "A separate role"], RED)
        text(c, "Uses an LLM does not locate a component.", 960, 845, 38, INK, p, True, align="center", width=1720)
        self.note(c, "Ask which decision the model makes, what evidence it receives and what is inspectable")

    def closing(self, c, t, s):
        p = self.r(t, s)
        for i, (title, body) in enumerate([("SEARCHABLE?", "Check scope"), ("CANDIDATE?", "Inspect retrieval"),
                                            ("SUPPLIED?", "Inspect selection"), ("CITED?", "Inspect the answer")]):
            x = 150+i*435
            panel(c, x, 350, 380, 310, title, [body], [GOLD, BLUE, TEAL, RED][i])
            if i < 3:
                arrow(c, x+393, 500, x+422, 500, RULE)
        rows(c, ["Then judge usefulness against the information need.", "Next: Chapter 2 — words as admission rules."], 960, 770, 35, INK, p, align="center", bold=True, step=70, width=1720)
        self.note(c, "Each diagnostic question needs different evidence; a new direct search does not reconstruct an earlier run")

    def poster(self, c):
        c.clear(skia.Color(*CREAM))
        text(c, "CHAPTER 1 · THE RETRIEVAL PROBLEM", 130, 120, 30, self.accent, bold=True)
        line(c, 130, 155, 1790, 155, self.accent, stroke=3)
        titles = {1: ["The paper", "your AI", "never saw."], 2: ["A match", "is not", "a verdict."],
                  3: ["Three clues", "in a", "search box."]}
        rows(c, titles[self.script["episode_number"]], 130, 360, 100, INK, bold=True, step=125, width=1140)
        for i in range(3):
            card(c, 1390+i*22, 340+i*100, ["?", "A", "P"][i], 290, 340, [self.accent, MUTED, GOLD][i], angle=(i-1)*6)
        text(c, self.script["subtitle"], 130, 850, 36, self.accent, width=1150)
        text(c, "Adapted from Aaron Tay · How Search Decides What You See", 130, 981, 26, MUTED)
        text(c, f"FILM {self.script['episode_number']:02d}", 1790, 981, 28, self.accent, bold=True, align="right")
