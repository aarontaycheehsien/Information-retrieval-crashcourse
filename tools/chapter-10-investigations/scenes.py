"""Original Chapter 10 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter10_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import LEXICAL, DENSE, C, rrf, fused_order as ranking, check_examples
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
        text(c, f"CHAPTER 10   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 10 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Chapter 10 teaching illustration · Candidate routes, fusion and later ranking are separate choices"):
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
        text(c,label,x+w/2,y+h*.43,min(66,int(w*.37)),color,a,True,align="center")
        for j in range(3):line(c,x+w*.16,y+h*(.61+j*.12),x+w*.82,y+h*(.61+j*.12),RULE,a,1)

    def lists(self,c,p=1):
        for j,(title,labels,color) in enumerate([('LEXICAL',LEXICAL,BLUE),('DENSE',DENSE,TEAL)]):
            x=170+j*850
            text(c,title,x,285,30,color,bold=True)
            for i,label in enumerate(labels):
                self.record(c,x+i*230,350,155,220,label,color,1 if j==0 else .3+.7*p)
                text(c,f'#{i+1}',x+i*230+78,625,28,MUTED,align='center')

    def hybrid_hook(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,310,770,345,'BM25 CANDIDATE RETRIEVAL',['Searches the collection','Supplies a shortlist','One candidate-generation route'],BLUE)
        panel(c,1000,310,770,345,'NEURAL MODEL RERANKING',['Receives the supplied candidates','Changes their order','No second route into the collection'],TEAL,.2+.8*p)
        arrow(c,930,480,990,480,TEAL,p)
        text(c,'Count candidate routes, then follow the stages.',960,815,42,INK,p,True,align='center',width=1700)
        self.note(c,'The chapter’s operational definition · A later model does not automatically make retrieval hybrid')

    def complementary_evidence(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,300,770,390,'LEXICAL CLUE: A RARE IDENTIFIER',['AX-317A safety study','Analysed terms may preserve the identifier','Term analysis and indexed text matter','Boolean conditions can add explicit control'],BLUE)
        panel(c,1000,300,770,390,'DENSE CLUE: DIFFERENT WORDING',['heart attack treatment','↔ myocardial infarction therapy','A possible training-dependent bridge','The intended match is not guaranteed'],TEAL,.2+.8*p)
        self.note(c,'Original illustrative strings, not model runs · Complementary blind spots motivate combining routes')

    def parallel_candidates(self,c,t,s):
        p=self.r(t,s)
        self.lists(c,p)
        text(c,'4 distinct supplied identities: { A, B, C, D }',960,790,43,INK,p,True,align='center',width=1700)
        self.note(c,'Two supplied lists, not an AND condition · Set membership here does not specify the fused ranking')

    def sequential_case(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('RETRIEVE',['BM25 candidate generation','One route into the collection'],BLUE),('RERANK',['Cross-encoder second pass','Reorders supplied candidates'],TEAL),('DISPLAY',['Show the leading records','Another output boundary'],RED)]):
            x=130+i*570
            panel(c,x,330,520,350,title,body,color,1 if i==0 else .3+.7*p)
            if i<2:arrow(c,x+532,505,x+558,505,color,p)
        text(c,'Multi-stage · One candidate-generation route',960,815,43,INK,p,True,align='center',width=1700)
        self.note(c,'Vendor labels vary · Inspect which components supply candidates and which only process them')

    def single_stage_blend(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,285,680,230,'LEXICAL CANDIDATE EVIDENCE',['Lexical candidate-generation scores'],BLUE)
        panel(c,150,590,680,230,'DENSE CANDIDATE EVIDENCE',['Dense candidate-generation scores'],TEAL)
        arrow(c,865,420,1020,535,BLUE,.3+.7*p,stroke=3)
        arrow(c,865,690,1020,575,TEAL,.3+.7*p,stroke=3)
        panel(c,1070,335,700,395,'ONE SCORING STAGE',['Blend the evidence in one stage','Produce one ranking','No separate reranking cascade required'],RED,.2+.8*p)
        self.note(c,'The chapter’s single-stage counterexample · Multiple retrieval routes and sequential stages are different properties')

    def both_arrangements(self,c,t,s):
        p=self.r(t,s)
        panel(c,130,295,520,205,'LEXICAL ROUTE',['Supplies one candidate list'],BLUE)
        panel(c,130,585,520,205,'DENSE ROUTE',['Supplies another candidate list'],TEAL)
        panel(c,700,350,520,365,'FUSE',['Reconcile record identities','Combine rank or score evidence','Produce a merged shortlist'],TEAL,.3+.7*p)
        panel(c,1270,350,520,365,'RERANK',['A richer later comparison','Receives fused survivors','Still bounded by the pool'],RED,.3+.7*p)
        arrow(c,660,405,690,470,BLUE,p);arrow(c,660,690,690,600,TEAL,p);arrow(c,1230,535,1260,535,RED,p)
        self.note(c,'Both hybrid and multi-stage · A later scorer cannot inspect a record omitted by every earlier route')

    def routing_choice(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('LEXICAL',['Run only the lexical route','No list combination in this run'],BLUE),('DENSE',['Run only the vector route','No list combination in this run'],TEAL),('BOTH',['Run both candidate routes','Their lists still require fusion'],RED)]):
            panel(c,130+i*570,330,520,350,title,body,color)
        text(c,'Routing chooses the path or paths for this query.',960,815,42,INK,p,True,align='center',width=1700)
        self.note(c,'A blend combines prescribed paths · A product may have multiple retrievers without using both on every query')

    def architecture_questions(self,c,t,s):
        self.four(c,[('ROUTES THAT RAN',['Which methods supplied candidates?','What evidence did each preserve?'],BLUE),('INPUT BOUNDARIES',['How deep were the supplied lists?','Which record identities overlap?'],TEAL),('COMBINATION RULE',['RRF, normalised scores, another rule?','Any explicit route weights?'],RED),('LATER OPERATIONS',['Reranking, display, answer context?','Evaluate the actual search task'],BLUE)],self.r(t,s))
        self.note(c,'Hybrid is an architecture claim, not a quality guarantee · Next: follow four records through RRF')

    def fusion_hook(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,310,770,350,'RAW RETRIEVAL SCORES',['Scales can have different meanings','Numbers are not automatically comparable','A score-based blend needs justification'],BLUE)
        panel(c,1000,310,770,350,'RANK POSITIONS',['First, second, third, …','RRF combines these positions','Raw score gaps are discarded'],TEAL,.2+.8*p)
        text(c,'Can one shared rule combine positions instead?',960,815,41,INK,p,True,align='center',width=1700)
        self.note(c,'RRF avoids a shared raw-score scale · It does not make the fused score a relevance probability')

    def input_lists(self,c,t,s):
        self.lists(c,self.r(t,s))
        text(c,'Same letter → same record identity',960,790,43,INK,self.r(t,s),True,align='center',width=1700)
        self.note(c,'Positions start at 1 · An absent supplied-list occurrence contributes zero from that list')

    def fusion_formula(self,c,t,s):
        p=self.r(t,s)
        text(c,'RRF(d) = Σ 1 / (c + rank of d)',960,350,60,TEAL,bold=True,align='center',width=1700)
        for i,(rank,fraction) in enumerate([(1,'1/61'),(2,'1/62'),(3,'1/63')]):
            x=140+i*570
            panel(c,x,455,500,280,f'RANK {rank} · c = 60',[fraction,'One supplied-list contribution'],BLUE,.3+.7*p)
        self.note(c,'Unsupervised fusion rule · c softens position advantages; the baseline 60 can be tuned for another task')

    def record_a(self,c,t,s):
        self.plot(c,'rrf-a')
        self.note(c,'A: lexical #1 + dense #2 · 1/61 + 1/62 = 0.03252 (rounded)')

    def record_c(self,c,t,s):
        self.plot(c,'rrf-c')
        self.note(c,'C: lexical #3 + dense #1 · 1/63 + 1/61 = 0.03227 (rounded)')

    def single_route_records(self,c,t,s):
        self.plot(c,'rrf-singletons')
        self.note(c,'B: lexical #2 only · D: dense #3 only · One contribution does not imply unimportance')

    def fused_order(self,c,t,s):
        p=self.r(t,s)
        for i,name in enumerate(ranking()):
            x=160+i*430
            self.record(c,x,330,310,330,name,TEAL if name in ('A','C') else GOLD)
            text(c,f'{float(rrf()[name]):.5f}',x+155,745,43,INK,.3+.7*p,True,align='center',width=380)
        self.note(c,'6 input occurrences → 4 distinct records → A, C, B, D · This is fusion, not a new relevance model')

    def three_depths(self,c,t,s):
        p=self.r(t,s)
        for i,(title,value,body,color) in enumerate([('INPUT DEPTH','3','records per route',BLUE),('FUSION CONSTANT','60','inside each denominator',TEAL),('SUPPLIED IDENTITIES','4','before a display cutoff',RED)]):
            x=130+i*570
            rect(c,x,320,520,400,PAPER)
            text(c,title,x+260,385,29,color,bold=True,align='center',width=470)
            text(c,value,x+260,545,106,color,bold=True,align='center')
            text(c,body,x+260,645,29,MUTED,align='center',width=470)
        text(c,'Showing only the top 2 would be a later output boundary.',960,825,37,INK,p,True,align='center',width=1700)
        self.note(c,'c is not top-k · Input cutoffs change supplied evidence; output cutoffs hide already fused records')
    def score_gap_hook(self,c,t,s):
        self.plot(c,'score-gaps')
        self.note(c,'Ranks retain order and identity · The raw first–second score gap is not an RRF input')

    def constant_effect(self,c,t,s):
        self.plot(c,'constant-effect')
        self.note(c,'c = 0 is a declared mathematical comparison · c = 60 is the chapter’s baseline, not a result count')

    def input_cutoff(self,c,t,s):
        self.plot(c,'cutoff-effect')
        self.note(c,'An input cutoff and an output cutoff act at different points in the pipeline')

    def route_weights(self,c,t,s):
        self.plot(c,'weighted-fusion')
        self.note(c,'Weights (lexical, dense) change from (1, 1) to (1, 2) · A declared extension, not a recommended setting')

    def blend_and_route(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,285,770,435,'WEB OF SCIENCE SMART SEARCH',['NLP parser structures the question','Boolean keyword path','Semantic-vector path','Document search can blend both'],BLUE)
        panel(c,1000,285,770,435,'SCOPUS AI',['Choose routes for this question','Lexical, vector, or both','A one-route run combines nothing','Both routes still need a fusion rule'],TEAL,.2+.8*p)
        text(c,'Parsing changes a query. Routing chooses paths. Fusion combines lists.',960,825,34,INK,p,True,align='center',width=1700)
        self.note(c,'Pinned chapter documentation accounts · No fresh product test or claim that the products use the same fusion rule')

    def routing_explanation(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,310,770,360,'BLEND: PRESCRIBED SOURCES',['Which fixed paths contribute?','How are their outputs combined?','The explanation has a fixed shape'],BLUE)
        panel(c,1000,310,770,360,'ROUTE: QUERY-TIME SELECTION',['Which paths ran for this query?','What chose them and what did they supply?','Expose selection before explaining a result'],TEAL,.2+.8*p)
        text(c,'A rule, classifier or model can route; routing alone does not establish agency.',960,825,32,INK,p,True,align='center',width=1700)
        self.note(c,'Knowing a fusion formula does not identify the candidate-generation architecture')

    def query_variant_fusion(self,c,t,s):
        p=self.r(t,s)
        text(c,'SCOPUS AI · 2024 RAG FUSION ACCOUNT',960,270,31,BLUE,bold=True,align='center',width=1700)
        for j in range(3):
            x=160+j*570
            panel(c,x,330,490,275,f'GENERATED VARIANT {j+1}',['Vector retrieval for this variant','A separate ranked result list'],BLUE)
            arrow(c,x+245,620,960,710,TEAL,.3+.7*p,stroke=2)
        pill(c,'RRF → merged top results → summary with references',390,775,TEAL,.3+.7*p,size=29)
        self.note(c,'Multiple variants of one question · This account does not establish lexical-plus-dense retrieval for each query')

    def fusion_evaluation(self,c,t,s):
        self.four(c,[('CANDIDATE SOURCES',['Which routes ran and what did they search?','What input depths and record identities?'],BLUE),('FUSION SETTINGS',['Constant, list weights, combination rule','Which score information was discarded?'],TEAL),('LATER BOUNDARIES',['Output cutoff and any reranker','What evidence reached the answer writer?'],RED),('COMPARE ON REAL TASKS',['RRF baseline versus individual routes','Chapter 11: query interpretation and routing'],BLUE)],self.r(t,s))
        self.note(c,'Representative-query evaluation is needed · A hybrid architecture alone is not a quality guarantee')

    def poster(self,c):
        c.clear(skia.Color(*CREAM))
        text(c,'HOW SEARCH DECIDES WHAT YOU SEE',130,130,27,MUTED,bold=True)
        text(c,f"CHAPTER 10 · FILM {self.script['episode_number']:02d}",130,220,30,self.accent,bold=True)
        titles={1:['Two models do not','make a hybrid.'],2:['How two lists','become one.'],3:['What the fused ranking','cannot tell you.']}
        rows(c,titles[self.script['episode_number']],130,405,86,INK,bold=True,step=132,width=1190)
        text(c,self.script['subtitle'],130,750,31,MUTED,width=1130)
        for i,label in enumerate(('A','C','B','D')):
            x=1450+(i%2)*155;y=350+(i//2)*210
            self.record(c,x,y,112,165,label,self.accent)
        text(c,'Original animated investigation · Narrated and captioned',130,890,26,self.accent)
        text(c,'Adapted from Aaron Tay · CC BY 4.0',130,1000,23,MUTED)
