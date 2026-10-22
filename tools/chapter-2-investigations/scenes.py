"""Original Chapter 2 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter2_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import RECORDS, SELECTED_POSTINGS, POSTINGS, POINTER_LEFT, POINTER_RIGHT, combine, intersection_trace, check_examples


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
        text(c, f"CHAPTER 2   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 2 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Four-record teaching collection · Analysis choices are illustrative"):
        text(c, message, 960, 900, 21, MUTED, align="center", width=1700)

    def four_records(self, c, admitted=(), y=365, phase=1):
        details = [["Delulu job interview", "expectations"], ["Job interview", "preparation guide"],
                   ["Unrealistic job", "expectations"], ["Delulu about my", "dream job"]]
        for i, ident in enumerate(RECORDS):
            x = 130+i*435
            keep = ident in admitted
            a = 1 if keep else 1-.7*phase
            card(c, x, y, ident, 350, 280, TEAL if keep else MUTED, a, detail=details[i])
            pill(c, "PASS" if keep else "OUT", x+105, y+320, TEAL if keep else RED, phase)

    def set_row(self, c, label, ids, x, y, color=BLUE, width=730):
        text(c, label, x, y, 30, color, bold=True, width=width)
        for i, ident in enumerate(ids):
            rect(c, x+i*140, y+35, 115, 82, PAPER)
            text(c, str(ident), x+57+i*140, y+89, 29, color, bold=True, align="center")

    def prediction(self, c, t, s):
        p = self.r(t, s)
        episode = self.script["episode_number"]
        if episode == 1:
            panel(c, 160, 330, 700, 380, "THE EXISTING RULE", ["delulu OR unrealistic", "A record meets it—or does not", "Eligibility is a hard decision"], BLUE)
            arrow(c, 900, 520, 1060, 520, BLUE, p)
            panel(c, 1100, 330, 660, 380, "ADD ONE OR ALTERNATIVE", ["... OR foolish", "Another route into the set", "More than a score change"], RED, .15+.85*p)
            text(c, "A query edit can change membership.", 960, 830, 41, INK, p, True, align="center")
            self.note(c, "The usefulness of a proposed alternative depends on the information need")
        elif episode == 2:
            card(c, 200, 340, "RECORD TEXT", 590, 360, BLUE, detail=["jobs"])
            card(c, 1130, 340, "YOUR QUERY", 590, 360, TEAL, detail=["job"])
            arrow(c, 830, 520, 1090, 520, TEAL, p)
            pill(c, "Compatible analysed terms can meet", 645, 775, TEAL, p)
            self.note(c, "Different visible forms can match lexically; this does not establish dense retrieval")
        else:
            for i in range(36):
                tiny(c, 170+(i%9)*53, 320+(i//9)*85, 40, 58, color=MUTED)
            arrow(c, 710, 510, 930, 510, RED, p)
            panel(c, 990, 340, 760, 350, "START WITH THE TERM", ["Find its dictionary entry", "Follow its posting list", "No need to reread every document"], RED, .15+.85*p)
            text(c, "A term → document map", 960, 825, 45, INK, p, True, align="center")
            self.note(c, "Schematic mechanism; no collection size, response time or measured speedup is depicted")

    def and_gate(self, c, t, s):
        p = self.r(t, s, 0, "pass")
        pill(c, "delulu AND job", 700, 260, BLUE, size=30)
        self.four_records(c, combine("delulu", "AND", "job"), phase=p)
        text(c, "Keep the shared identifiers: D1, D4", 960, 840, 36, BLUE, self.r(t, s), True, align="center")
        self.note(c, "Fixed D1–D4 collection; lowercasing and indexed fields held constant")

    def or_gate(self, c, t, s):
        p = self.r(t, s, 0, "eligible")
        pill(c, "delulu OR unrealistic", 630, 260, BLUE, size=30)
        self.four_records(c, combine("delulu", "OR", "unrealistic"), phase=p)
        text(c, "Either condition—or both", 960, 840, 39, BLUE, self.r(t, s), True, align="center")
        self.note(c, "An OR alternative can widen eligibility; extra membership does not establish usefulness")

    def not_gate(self, c, t, s):
        p = self.r(t, s, 0, "remains")
        pill(c, "delulu NOT interview", 640, 260, RED, size=30)
        self.four_records(c, combine("delulu", "NOT", "interview"), phase=p)
        text(c, "Start with {D1, D4}; remove the overlap; keep D4.", 960, 840, 33, RED, self.r(t, s), True, align="center", width=1710)
        self.note(c, "NOT can also remove useful records; eligibility follows the expressed rule")

    def expansion(self, c, t, s):
        p = self.r(t, s)
        panel(c, 130, 290, 1660, 190, "THE CHAPTER'S EXPANSION", ["delulu OR unrealistic OR irrational OR foolish"], BLUE)
        card(c, 290, 550, "EXTRA RECORD E", 580, 280, GOLD, detail=["Foolish decisions in a garden", "Contains the added alternative"])
        arrow(c, 920, 680, 1080, 680, GOLD, p)
        panel(c, 1120, 550, 590, 280, "ELIGIBLE VIA foolish", ["Even without the other alternatives", "Ranking cannot undo admission"], RED, p)
        self.note(c, "Record E is an invented addition; foolish is stipulated to be a poor alternative for this need")

    def compulsory(self, c, t, s):
        p = self.r(t, s)
        panel(c, 160, 320, 680, 410, "delulu", ["D1 and D4 are eligible", "D4 has no interview term"], BLUE)
        arrow(c, 880, 520, 1050, 520, RED)
        panel(c, 1090, 320, 680, 410, "delulu AND interview", ["Only D1 is eligible", "D4 is outside this set", "Ranking cannot reintroduce it"], RED)
        text(c, "A new search can change the rule; reordering cannot.", 960, 835, 34, INK, p, True, align="center", width=1720)
        self.note(c, "D4's usefulness is conditional on the purpose; no relevance benchmark is asserted")

    def order(self, c, t, s):
        p = self.r(t, s)
        panel(c, 160, 330, 680, 390, "BOOLEAN ADMISSION", ["Which records satisfy the rule?", "An eligible set", "No graded relevance score"], BLUE)
        arrow(c, 890, 520, 1040, 520, TEAL)
        panel(c, 1090, 330, 680, 390, "RANKING", ["Which eligible record comes first?", "Requires another method", "Usefulness still needs judgement"], TEAL)
        text(c, "First ask what terms and fields were actually matched.", 960, 835, 34, INK, p, True, align="center", width=1730)
        self.note(c, "A yes/no Boolean decision can follow nontrivial text analysis and database-specific rules")

    def tokens(self, c, t, s):
        p = self.r(t, s, 0, "four")
        text(c, "Delulu about jobs!", 960, 330, 65, INK, bold=True, align="center")
        for i, token in enumerate(["Delulu", "about", "jobs", "!"]):
            x = 200+i*420
            rect(c, x, 490, 320, 170, PAPER, p)
            text(c, token, x+160, 593, 45, TEAL, p, True, align="center")
            circle(c, x+160, 420, 6, TEAL, p)
            line(c, x+160, 440, x+160, 480, TEAL, p)
        text(c, "Tokenisation chooses the processing units.", 960, 810, 39, TEAL, self.r(t, s), True, align="center")
        self.note(c, "Illustrative tokenizer: punctuation is one token; other analysers may choose different boundaries")

    def analysis(self, c, t, s):
        case = self.r(t, s, 0, "lowercases")
        remove = self.r(t, s, 0, "removal")
        stem = self.r(t, s, 0, "stemming")
        data = [("RAW TEXT", "Delulu about jobs!", 1), ("TOKENS", "Delulu  ·  about  ·  jobs  ·  !", 1),
                ("CASE NORMALISATION", "delulu  ·  about  ·  jobs  ·  !", case),
                ("OPTIONAL REMOVAL", "delulu  ·  jobs", remove), ("OPTIONAL STEMMING", "delulu  ·  job", stem)]
        for i, (label, value, p) in enumerate(data):
            y = 270+i*110
            text(c, label, 160, y+48, 26, RED if i >= 3 else BLUE, bold=True, width=480)
            rect(c, 690, y, 1030, 85, PAPER, .2+.8*p)
            text(c, value, 740, y+55, 33, TEAL if i == 4 else INK, p, bold=i == 4, width=930)
        self.note(c, "Separate analysis operations; this sequence is an example, not a universal database recipe")

    def morphology(self, c, t, s):
        p = self.r(t, s)
        text(c, "studies     studying     studied", 960, 300, 45, INK, bold=True, align="center")
        panel(c, 150, 410, 690, 380, "STEMMING", ["Rules / heuristics", "studi", "A matching key; not necessarily a word"], BLUE)
        panel(c, 1090, 410, 680, 380, "LEMMATISATION", ["Vocabulary + morphology", "study", "Grammar matters: better → good"], TEAL, .3+.7*p)
        arrow(c, 750, 325, 500, 390, BLUE)
        arrow(c, 1170, 325, 1420, 390, TEAL)
        self.note(c, "Illustrative outputs; algorithms, languages, grammatical interpretations and field analysers differ")

    def risks(self, c, t, s):
        p = self.r(t, s)
        for x, title, body, col in [(140, "USEFUL CONVERGENCE", ["Related grammatical forms", "Share an indexed term", "More matches become possible"], TEAL),
                                    (710, "OVER-STEMMING", ["Unrelated forms collapse", "Potential precision loss", "A shared key can mislead"], RED),
                                    (1280, "UNDER-STEMMING", ["Related forms stay apart", "Potential missed matches", "A useful link is absent"], BLUE)]:
            panel(c, x, 340, 500, 390, title, body, col)
        text(c, "Grammatical normalisation does not guarantee meaning.", 960, 835, 33, INK, p, True, align="center", width=1730)
        self.note(c, "No product-specific stemmer or measured precision/recall effect is inferred")

    def compatibility(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 290, 680, 420, "DOCUMENT SIDE", ["Visible text: jobs", "Stored term: job", "If changed: stored term jobs"], BLUE)
        panel(c, 1090, 290, 680, 420, "QUERY SIDE", ["Typed text: job", "Lookup term: job", "Still looks up only job"], TEAL)
        text(c, "job = job", 960, 490, 38, TEAL, 1-p, True, align="center")
        text(c, "jobs ≠ job", 960, 615, 33, RED, p, True, align="center")
        text(c, "Without another mapping, the incompatible lookup misses.", 960, 825, 34, RED, p, True, align="center", width=1740)
        self.note(c, "Compatible analysis need not mean identical operations on both sides")

    def truncation(self, c, t, s):
        p = self.r(t, s)
        panel(c, 150, 330, 680, 410, "USER-ENTERED TRUNCATION", ["librar*", "Platform-specific expansion", "Depends on indexed forms"], BLUE)
        text(c, "≠", 960, 555, 90, RED, bold=True, align="center")
        panel(c, 1090, 330, 680, 410, "AUTOMATIC ANALYSIS", ["Optional stemming / lemmatisation", "Dictionary lookup keys", "Fields may use different analysers"], TEAL)
        text(c, "Inspect analysis and expansion before the Boolean operator.", 960, 835, 32, INK, p, True, align="center", width=1720)
        self.note(c, "An exact code or identifier field may deliberately preserve the original value")

    def records(self, c, t, s):
        p = self.r(t, s)
        panel(c, 130, 295, 880, 520, "DOCUMENT FIRST: RECORD → WORDS", [f"{k}   {v}" for k, v in RECORDS.items()], BLUE)
        arrow(c, 1040, 540, 1175, 540, RED, p)
        panel(c, 1210, 355, 580, 400, "TERM FIRST", [term+" → "+", ".join(ids) for term, ids in SELECTED_POSTINGS.items()], RED, .2+.8*p)
        self.note(c, "Exact D1–D4 texts from Chapter 2; selected analysed terms use word boundaries and lowercasing")

    def postings(self, c, t, s):
        p = self.r(t, s)
        self.set_row(c, "delulu", POSTINGS["delulu"], 170, 310, BLUE)
        self.set_row(c, "interview", POSTINGS["interview"], 170, 510, TEAL)
        self.set_row(c, "job", POSTINGS["job"], 170, 710, MUTED)
        arrow(c, 860, 480, 1080, 480, RED, p)
        panel(c, 1120, 350, 650, 400, "delulu AND interview", ["Shared identifier: D1", "Intersect the two lists", "No text rereading required"], RED, .2+.8*p)
        self.note(c, "Selected posting lists only; other dictionary terms are omitted")

    def sets(self, c, t, s):
        p = self.r(t, s)
        for i, operator in enumerate(["AND", "OR", "NOT"]):
            x = 140+i*570
            result = ", ".join(combine("delulu", operator, "interview"))
            panel(c, x, 345, 500, 390, operator, ["delulu", f"{operator} interview", "→  "+result], [BLUE, TEAL, RED][i])
        text(c, "Same lists. Different set operations.", 960, 835, 40, INK, p, True, align="center")
        self.note(c, "All three results independently calculated from the unchanged D1–D4 collection")

    def speed(self, c, t, s):
        start = self.at(s, 0, "Ordered")
        steps, result = intersection_trace()
        index = min(len(steps)-1, max(0, int((t-start)/1.3)))
        step = steps[index]
        complete = t > start+len(steps)*1.3
        text(c, "SELECTIVE ACCESS: go straight to the needed lists", 960, 290, 30, BLUE, bold=True, align="center", width=1710)
        for label, ids, y, active in [("LIST A", POINTER_LEFT, 390, step["i"]), ("LIST B", POINTER_RIGHT, 590, step["j"])]:
            text(c, label, 180, y+48, 29, MUTED, bold=True)
            for j, ident in enumerate(ids):
                x = 560+j*220
                rect(c, x, y, 165, 100, TEAL if j == active and not complete else PAPER)
                text(c, str(ident), x+82, y+66, 38, PAPER if j == active and not complete else INK, bold=True, align="center")
            if not complete:
                arrow(c, 642+active*220, y-55, 642+active*220, y-10, TEAL)
        kept = result if complete else step["kept_before"]
        label = "Intersection: "+(", ".join(map(str, kept)) if kept else "nothing retained yet")
        text(c, label, 960, 785, 35, RED, bold=True, align="center")
        text(c, "Sorted access advances forwards; it does not revisit earlier identifiers.", 960, 845, 28, INK, self.r(t, s), True, align="center", width=1740)
        self.note(c, "Additional illustrative lists, separate from D1–D4 · No timing benchmark or universal speed promise")

    def rich(self, c, t, s):
        p = self.r(t, s)
        text(c, "D1: Delulu job interview expectations", 960, 300, 39, INK, bold=True, align="center", width=1700)
        for i, (title, value, col) in enumerate([("IDENTIFIER", "D1", BLUE), ("FREQUENCY", "1", TEAL), ("FIELD", "title (example)", GOLD), ("POSITION", "2 (one-based)", RED)]):
            x = 140+i*435
            panel(c, x, 410, 380, 280, title, [value], col)
        text(c, "Scoring · field weighting · phrases · proximity · highlighting", 960, 815, 32, INK, p, True, align="center", width=1730)
        self.note(c, "Illustrative richer posting: D1's text is assumed to be a title; real posting formats vary")

    def fts(self, c, t, s):
        p = self.r(t, s)
        panel(c, 140, 315, 740, 435, "FULL-TEXT SEARCH: A CAPABILITY", ["Search natural-language text fields", "Titles + abstracts can qualify", "Passages or OCR can qualify", "No single query or ranking rule"], BLUE)
        panel(c, 1040, 315, 740, 435, "PUBLICATION COVERAGE: A QUESTION", ["Which parts were indexed?", "What is the searchable unit?", "Which terms survived analysis?", "How are matches admitted and ranked?"], RED, .3+.7*p)
        text(c, "Complete source possession does not guarantee complete searchable coverage.", 960, 837, 28, INK, p, True, align="center", width=1740)
        self.note(c, "A terminology distinction; no named product's coverage or architecture is inferred")

    def closing(self, c, t, s):
        p = self.r(t, s)
        labels = [["Raw", "text"], ["Tokens /", "analysis"], ["Indexed", "terms"], ["Posting", "lists"], ["Eligible", "set"]]
        for i, label in enumerate(labels):
            x = 105+i*346
            rect(c, x, 360, 290, 205, PAPER)
            rows(c, label, x+145, 440, 29, [MUTED, BLUE, TEAL, GOLD, RED][i], align="center", bold=True, width=260)
            if i < 4:
                arrow(c, x+303, 460, x+333, 460, RULE)
        rows(c, ["The set is eligible. Its order needs a scoring rule.", "Next: Chapter 3 — ranking lexical evidence."], 960, 740, 37, INK, p, align="center", bold=True, step=80, width=1740)
        self.note(c, "Boolean admission, ranking order and human usefulness are different decisions")

    def poster(self, c):
        c.clear(skia.Color(*CREAM))
        text(c, "CHAPTER 2 · BOOLEAN ADMISSION AND THE INVERTED INDEX", 130, 120, 29, self.accent, bold=True, width=1640)
        line(c, 130, 155, 1790, 155, self.accent, stroke=3)
        titles = {1: ["The word that", "opened", "the gate."], 2: ["The word", "you never", "searched."],
                  3: ["Search without", "rereading", "the papers."]}
        rows(c, titles[self.script["episode_number"]], 130, 360, 98, INK, bold=True, step=125, width=1160)
        for i in range(3):
            card(c, 1390+i*22, 340+i*100, ["?", "D1", "D4"][i], 290, 340, [self.accent, MUTED, GOLD][i], angle=(i-1)*6)
        text(c, self.script["subtitle"], 130, 850, 35, self.accent, width=1150)
        text(c, "Adapted from Aaron Tay · How Search Decides What You See", 130, 981, 26, MUTED)
        text(c, f"FILM {self.script['episode_number']:02d}", 1790, 981, 28, self.accent, bold=True, align="right")
