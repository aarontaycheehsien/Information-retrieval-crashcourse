"""Original Chapter 14 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter14_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import check_examples, BEFORE, AFTER, RELEVANT, LOCAL_ROWS, precision_at, recall_at, reciprocal_rank, average_precision, row_mean
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
        text(c, f"CHAPTER 14   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 14 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Chapter 14 teaching illustration · Controlled source illustrations · Metrics depend on the stated relevance judgements and evaluation protocol"):
        text(c, message, 960, 900, 21, MUTED, align="center", width=1700)

    def plot(self, c, name, a=1):
        if name not in self.images:
            data = skia.Data.MakeWithCopy((self.plot_directory/(name+".png")).read_bytes())
            self.images[name] = skia.Image.MakeFromEncoded(data)
            assert self.images[name] is not None
        paint = skia.Paint()
        paint.setAlphaf(a)
        c.drawImageRect(self.images[name], skia.Rect.MakeXYWH(170, 255, 1580, 632), paint=paint)

    def four(self,c,items,p=1):
        for i,(title,body,color) in enumerate(items):
            x=140+(i%2)*850;y=270+(i//2)*295
            panel(c,x,y,790,255,title,body,color,1 if i<2 else .2+.8*p)

    def record(self,c,x,y,w,h,label,color=BLUE,a=1):
        rect(c,x+3,y+4,w,h,INK,.09*a,2)
        rect(c,x,y,w,h,PAPER,a,2)
        rect(c,x,y,w,3,color,a,1)
        text(c,label,x+w/2,y+h*.43,min(66,int(w*.37)),color,a,True,align='center',width=w-20)
        for j in range(3):line(c,x+w*.16,y+h*(.61+j*.12),x+w*.82,y+h*(.61+j*.12),RULE,a,1)

    def tiles(self,c,ranking,x,y,step=169,w=148,h=145,a=1):
        for i,label in enumerate(ranking):
            color=TEAL if label in RELEVANT else MUTED
            xx=x+i*step
            rect(c,xx+2,y+3,w,h,INK,.08*a,3)
            rect(c,xx,y,w,h,PAPER,a,3)
            rect(c,xx,y,w,4,color,a,1)
            text(c,label,xx+w/2,y+h*.48,min(48,int(w*.50)),color,a,True,align='center')
            text(c,'R' if label in RELEVANT else 'N',xx+w/2,y+h*.82,min(23,int(w*.27)),color,a,True,align='center')

    def both_hook(self,c,t,s):
        p=self.r(t,s)
        text(c,'BEFORE · FIRST TEN',140,275,29,BLUE,bold=True)
        self.tiles(c,BEFORE[:10],140,305)
        text(c,'Precision@10 = 2/10 = 0.2     Recall@10 = 2/10 = 0.2',960,505,32,BLUE,bold=True,align='center',width=1700)
        text(c,'AFTER · FIRST TEN',140,575,29,TEAL,p,True)
        self.tiles(c,AFTER[:10],140,605,a=p)
        text(c,'Precision@10 = 6/10 = 0.6     Recall@10 = 6/10 = 0.6',960,805,32,TEAL,p,True,align='center',width=1700)
        self.note(c,'Figure 14.1 · R = judged relevant; N = judged non-relevant · Complete relevance set A–J stipulated; same 20 candidates')

    def relevance_perspectives(self,c,t,s):
        self.four(c,[('SYSTEM / ALGORITHMIC',['The system estimates fit to an input','A score is not experienced usefulness'],BLUE),('TOPICAL',['Is the paper about the subject?','It can still have the wrong population or method'],TEAL),('COGNITIVE / PERTINENCE',['Does it inform this reader?','What they already know matters'],RED),('SITUATIONAL / USEFULNESS',['Does it help this person do this task?','Criteria and stage of work can change the verdict'],BLUE)],self.r(t,s))
        self.note(c,'Four source perspectives are a teaching simplification, not a complete taxonomy · Relevance is relational and can change over time')

    def judgement_protocol(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,295,770,415,'MAKE THE CRITERIA EXPLICIT',['Whose need and task?','Topical or detailed inclusion criteria?','Binary or graded relevance?','Who judged, and under what instructions?'],BLUE)
        panel(c,1000,295,770,415,'THEN APPLY THE SAME JUDGEMENTS',['Compare systems against the same labels','Scores inherit those operational criteria','Topical relevance alone may admit','the wrong population, date or method'],TEAL,.2+.8*p)
        text(c,'The formula cannot choose the right relevance criteria for you.',960,820,37,INK,p,True,align='center',width=1700)
        self.note(c,'A metric measures agreement with recorded judgements · A model score is evidence, not the judgement itself')

    def two_denominators(self,c,t,s):
        self.plot(c,'denominators')
        self.note(c,'Numerically equal is not conceptually identical · Ten displayed papers and ten total relevant papers are different denominators')

    def fixed_pool(self,c,t,s):
        p=self.r(t,s)
        for x,title,ranking,a in [(150,'BEFORE',BEFORE,1),(1000,'AFTER',AFTER,.2+.8*p)]:
            text(c,title,x+385,280,31,BLUE if x==150 else TEAL,a,True,align='center')
            self.tiles(c,ranking[:10],x+15,325,step=75,w=66,h=100,a=a)
            line(c,x+10,475,x+760,475,RED,a,2)
            text(c,'DISPLAY STOPS AFTER RANK 10',x+385,510,23,RED,a,True,align='center',width=730)
            self.tiles(c,ranking[10:],x+15,555,step=75,w=66,h=100,a=a)
            text(c,'Pool recall: 10/10 = 1.0',x+385,750,38,TEAL,a,True,align='center',width=730)
        text(c,'All 20 identities remain. Only their order changes.',960,835,36,INK,p,True,align='center',width=1700)
        self.note(c,'Full controlled source rankings · Whole-pool recall is fixed; precision@10 and recall@10 can both improve')

    def fresh_retrieval(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('FIXED OUTPUT',['Reorder the existing candidates','Cannot recover an excluded identity','A ceiling for downstream-only processing'],BLUE),('FRESH ROUTE OR ROUND',['Issue another retrieval','May add relevant records others missed','A new cumulative candidate set'],TEAL),('CHECK THE CONTRIBUTION',['Duplicates add no relevant identity','Irrelevant additions do not raise recall','Displayed cutoffs still matter'],RED)]):
            panel(c,130+i*570,305,520,405,title,body,color,1 if i==0 else .25+.75*p)
        text(c,'Find where candidate generation ends.',960,820,43,INK,p,True,align='center',width=1700)
        self.note(c,'A boundary, not a fixed position in a pipeline drawing · A later retrieval round starts a new candidate set')

    def unknown_denominator(self,c,t,s):
        self.four(c,[('PRECISION',['Judge the records that came back','Relevant returned ÷ returned'],BLUE),('ABSOLUTE RECALL',['Need the collection’s complete relevant total','Usually unknown in a live database'],RED),('RELATIVE COMPARISON',['Judge the relevant union found by strategies','Its denominator is that discovered union'],TEAL),('KNOWN-SEED RECOVERY',['Check recovery of known relevant records','Useful regression evidence, not absolute recall'],BLUE)],self.r(t,s))
        self.note(c,'Where did the denominator come from? · A larger result count does not establish the collection’s total relevant evidence')

    def task_and_practice(self,c,t,s):
        self.four(c,[('TASK PRIORITIES',['Ready reference often values precision','Evidence reviews lean heavily on recall'],BLUE),('AUGUST 2026 PRACTICE NOTE',['Structured database searching as formal core','Other routes supplement evidence synthesis'],TEAL),('NO INHERENT BOOLEAN RECALL CLAIM',['Missing synonyms and incomplete coverage matter','Inspect admission conditions and operators'],RED),('BOUNDARIES AFFECT RANKED METHODS',['BM25 and dense can both expose only top k','Evaluate sensitivity of the complete workflow'],BLUE)],self.r(t,s))
        self.note(c,'Dated methodological account from the source · Current practice is distinct from an inherent advantage of a retrieval method')

    def first_hit_hook(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,300,770,405,'BEFORE RERANKING',['First relevant paper: A at rank 1','Relevant records in first ten: 2','Reciprocal rank: 1/1 = 1'],BLUE)
        panel(c,1000,300,770,405,'AFTER RERANKING',['First relevant paper: A at rank 1','Relevant records in first ten: 6','Reciprocal rank: 1/1 = 1'],TEAL,.2+.8*p)
        text(c,'The first hit stayed first. Everything after it is ignored.',960,820,39,INK,p,True,align='center',width=1700)
        self.note(c,'Source rankings, computed single-query reciprocal rank · MRR averages reciprocal ranks across queries')

    def depth_choice(self,c,t,s):
        self.four(c,[('EVALUATION DEPTH k',['Where the metric stops counting','Precision@10 judges the first ten'],BLUE),('WITHIN THAT DEPTH',['Rank 1 and rank 10 count equally for P@10','Rank 11 adds nothing to that first-page score'],TEAL),('FIRST-STAGE CANDIDATE LIMIT',['How many candidates the retriever supplies','Need not equal the evaluation depth'],RED),('RERANKER BUDGET',['How many candidates are compared later','State this separately too'],BLUE)],self.r(t,s))
        self.note(c,'Different boundaries answer different questions · Compare both systems at the same evaluation depth')

    def reciprocal_goal(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,300,770,400,'THE FIRST ANSWER ARRIVES EARLY',['Single query: RR = 1 / first relevant rank','Across queries: MRR = mean of those RRs','A fit for a known paper, citation or lookup'],BLUE)
        panel(c,1000,300,770,400,'WHAT THE MEASURE DOES NOT SEE',['Additional relevant records after the first','Broad coverage of a useful evidence set','The source example has RR = 1 in both runs'],TEAL,.2+.8*p)
        text(c,'An unchanged score can hide a task-relevant improvement.',960,820,38,INK,p,True,align='center',width=1700)
        self.note(c,'One declared query supplies RR, not a multiquery MRR comparison · No new retrieval run')

    def average_precision_goal(self,c,t,s):
        self.plot(c,'single-query-scores')
        self.note(c,'AP averages precision at relevant ranks using the judged-relevant total · MAP averages query-level AP scores')

    def graded_goal(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,295,770,425,'nDCG’S GOAL',['Use relevance grades','Discount contributions lower in the ranking','Normalise against an ideal ordering','at the stated evaluation depth'],BLUE)
        panel(c,1000,295,770,425,'WHAT THE PROTOCOL MUST SUPPLY',['Defensible graded judgements','Explicit gain and discount convention','The source example is only binary','No grades or nDCG values invented here'],TEAL,.2+.8*p)
        text(c,'Highly graded records can still repeat the same aspect.',960,825,39,INK,p,True,align='center',width=1700)
        self.note(c,'Metric-goal illustration · No graded ranking computed · Ranking quality does not by itself establish diverse coverage')

    def metric_choice(self,c,t,s):
        self.plot(c,'ranking-goals')
        self.note(c,'Which benefit does the metric reward, and which failure can it hide? · Every one needs relevance judgements')

    def benchmark_controls(self,c,t,s):
        self.plot(c,'benchmark-controls')
        self.note(c,'Cranfield offline comparisons fix collection, queries and judgements · BEIR findings are conditional on their topics and assessors')

    def judgement_pooling(self,c,t,s):
        self.four(c,[('BUILD A JUDGEMENT POOL',['Union top results from multiple systems','Assess that deduplicated union'],BLUE),('DESCRIBED SCORING CONVENTION',['Unjudged records treated as non-relevant','A convenience for incomplete assessment'],RED),('THE LIMIT',['Unjudged need not mean irrelevant','Novel useful records can receive no credit'],TEAL),('TRANSFER TO A LIBRARY',['Ask whether topics, criteria and pool fit','A leaderboard is evidence about its benchmark'],BLUE)],self.r(t,s))
        self.note(c,'Judgement pooling is distinct from vector pooling · Protocol can disadvantage approaches unlike those contributing to the pool')
    def average_hook(self,c,t,s):
        p=self.r(t,s)
        for x,label,value,color in [(200,'EQUAL ROW MEAN · BEFORE','0.30',BLUE),(1040,'EQUAL ROW MEAN · AFTER','0.33',TEAL)]:
            rect(c,x,310,680,300,PAPER,1,6)
            text(c,label,x+340,380,28,color,bold=True,align='center',width=620)
            text(c,value,x+340,530,106,color,bold=True,align='center')
        arrow(c,925,465,995,465,TEAL)
        text(c,'Identifier row: precision@10 falls from 0.30 to 0.10',960,745,42,RED,p,True,align='center',width=1700)
        text(c,'A two-thirds relative loss can disappear inside that mean.',960,825,36,INK,p,True,align='center',width=1700)
        self.note(c,'Hypothetical Table 14.3 update · Three equally weighted displayed rows; one row averages two queries · After mean rounded')

    def source_rows(self,c,t,s):
        self.plot(c,'local-regression')
        self.note(c,'Identifier: hypothetical expansion drops SLC6A4 · Composition row averages two separately judged opposite-meaning queries')

    def local_queries(self,c,t,s):
        self.four(c,[('A PRACTICAL START',['30–50 queries from real library work','Not an exhaustive research test collection'],BLUE),('WHERE THEY COME FROM',['Enquiries, loan requests and consultations','Training, disciplines, languages and document types'],TEAL),('KNOWN DIFFICULT CASES',['Include searches already known to go badly','Demonstration-friendly examples are insufficient'],RED),('TIME AND JUDGEMENTS',['Rerunning can be quick; construction takes longer','Record task criteria, known items and defensible grades'],BLUE)],self.r(t,s))
        self.note(c,'Source guidance for a local baseline · An afternoon rerun is not a claim that creating and judging the set takes an afternoon')

    def fixed_depth_judging(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('CAPTURE AT FIXED DEPTH',['For example, ten or twenty','Use the same depth for both runs','Record shorter lists and denominators'],BLUE),('POOL AND DEDUPLICATE',['Union the two captured sets','Judge every pooled identity','Use the same written criteria'],TEAL),('COMPARE THE OUTCOMES',['Ideally hide which run supplied a record','Compute precision at that depth','Report known-seed recovery separately'],RED)]):
            panel(c,130+i*570,305,520,405,title,body,color,1 if i==0 else .25+.75*p)
        text(c,'Changing the judging protocol changes the comparison.',960,820,40,INK,p,True,align='center',width=1700)
        self.note(c,'Fixed depth and common criteria make a local rerun comparable · Missing judgements are not a system improvement')

    def deliberate_probes(self,c,t,s):
        self.four(c,[('EXACT IDENTIFIER',['Gene, chemical string or product code','Does a suitable lexical route survive?'],BLUE),('FULL-TEXT-ONLY PHRASE',['A phrase in a paper the library holds','Probe indexed units and coverage'],TEAL),('VOCABULARY MISMATCH',['Known relevant item shares almost no words','Probe the intended semantic bridge'],RED),('OPPOSITE MEANING',['Near-identical queries, reversed meaning','Judge each query separately for composition'],BLUE)],self.r(t,s))
        self.note(c,'Four source-recommended probes · Diagnostic evidence to investigate, not a promise that one metric identifies the cause')

    def variation_and_scope(self,c,t,s):
        self.four(c,[('PER-QUERY DIFFERENCES',['Inspect sharp gains and losses','Break down discipline, language and document type'],BLUE),('ORDINARY VARIATION',['Small changes can sit inside run-to-run variation','Further evidence may be needed'],RED),('THE VENDOR’S COMPARISON',['Which queries, collection, assessors and depth?','Which metric, grades and baseline?'],TEAL),('THE LOCAL COMPARISON',['Does the gain survive your hard queries?','Narrow scope is intentional; state its limits'],BLUE)],self.r(t,s))
        self.note(c,'A mean absorbs differences between queries · Measurement reports performance under stated criteria, not the internal cause')

    def answer_layer(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('RETRIEVAL QUALITY',['Did the right evidence reach the shortlist?','What was missed or ranked below the limit?','Judge the records for the actual task'],BLUE),('ANSWER FAITHFULNESS',['Does prose reflect the retrieved material?','A fluent summary can still use wrong sources','Faithfulness is a separate question'],TEAL),('CLAIM SUPPORT',['Can each claim trace to a source?','Does that source contain the claimed support?','Groundedness cannot expose every omission'],RED)]):
            panel(c,130+i*570,305,520,405,title,body,color,1 if i==0 else .25+.75*p)
        text(c,'A faithful summary of the wrong ten documents is still wrong.',960,820,37,INK,p,True,align='center',width=1700)
        self.note(c,'Answer evaluation inherits the shortlist · It complements retrieval evaluation and does not replace it')

    def rerun_and_record(self,c,t,s):
        self.four(c,[('SAVE THE BASELINE',['Queries, criteria, depth, judgements and captures','Keep the comparison explicit'],BLUE),('RERUN WHEN THINGS CHANGE',['Model or index update, migration or renewal','Use the same evaluation protocol'],TEAL),('INVESTIGATE REGRESSIONS',['Compare the rows; inspect the lost records','Chapter 13 supplies diagnostic hypotheses'],RED),('WHAT MEASUREMENT CANNOT DO',['Explain internal causes by itself','Make an undocumented search repeatable next year'],BLUE)],self.r(t,s))
        self.note(c,'Chapter 15 turns to what must be recorded, inspected and required · A local baseline earns its value by being rerun')

    def poster(self,c):
        c.clear(skia.Color(*CREAM))
        text(c,'HOW SEARCH DECIDES WHAT YOU SEE',130,130,27,MUTED,bold=True)
        text(c,f"CHAPTER 14 · FILM {self.script['episode_number']:02d}",130,220,30,self.accent,bold=True)
        titles={1:['Can both scores','improve?'],2:['The number that','ignores the rest.'],3:['The average went up.','The search got worse.']}
        rows(c,titles[self.script['episode_number']],130,405,88,INK,bold=True,step=132,width=1190)
        text(c,self.script['subtitle'],130,750,31,MUTED,width=1130)
        for i,label in enumerate(('R','÷','?')):
            self.record(c,1450+i*75,340+i*135,180,230,label,self.accent)
        text(c,'Original animated investigation · Narrated and captioned',130,890,26,self.accent)
        text(c,'Adapted from Aaron Tay · CC BY 4.0',130,1000,23,MUTED)
