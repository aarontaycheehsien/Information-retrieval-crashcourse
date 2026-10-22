"""Original Chapter 9 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter9_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import QUERY_TOKENS, DOCUMENT_TOKENS, SIMILARITIES, ASPECTS, SHORTLIST, RERANKED, EXCLUDED, INDEPENDENT_SELECTION, DIVERSE_SELECTION, check_examples
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
        text(c, f"CHAPTER 9   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 9 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Chapter 9 teaching illustration · A later stage works within the evidence it receives"):
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

    def shortlist_hook(self,c,t,s):
        p=self.r(t,s)
        text(c,'FIRST-STAGE SHORTLIST',170,285,28,BLUE,bold=True)
        text(c,'RERANKED ORDER',170,595,28,TEAL,bold=True)
        for j,labels in enumerate([SHORTLIST,RERANKED]):
            for i,label in enumerate(labels):tiny(c,190+i*270,330+j*310,160,185,label,BLUE if j==0 else TEAL,1 if j==0 else p)
        panel(c,1170,350,580,380,'X · OUTSIDE THE POOL',['Stipulated useful paper','Not supplied to this reranker','Cannot appear in its ordering'],RED,.3+.7*p)
        self.note(c,'Invented cards · Reranking changes order inside the pool; it cannot add an excluded record')

    def broad_then_deep(self,c,t,s):
        p=self.r(t,s)
        for j,(title,body,color) in enumerate([('COLLECTION',['Fast indexed retrieval','Retain potential candidates'],BLUE),('SHORTLIST',['Richer comparisons','More work per survivor'],TEAL),('DISPLAY / ANSWER',['Only surviving evidence','Another boundary may follow'],RED)]):
            x=130+j*570
            panel(c,x,330,520,350,title,body,color,1 if j==0 else .3+.7*p)
            if j<2:arrow(c,x+532,505,x+558,505,color,p)
        text(c,'Retrieve broadly first. Compare carefully later.',960,805,43,INK,p,True,align='center',width=1700)
        self.note(c,'Stage division improves affordability · Recall of the candidate pool still limits later decisions')

    def joint_encoding(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,285,770,425,'BI-ENCODER: INDEPENDENT',['Query → pooled query vector','Passage → stored passage vector','Compare after separate compression','Passage encoding can be precomputed'],BLUE)
        panel(c,1000,285,770,425,'CROSS-ENCODER: JOINT',['[ Query + one candidate ]','Attention across their tokens','One query-dependent ranking score','Pair encoding must happen for this query'],TEAL,.2+.8*p)
        text(c,'Interaction moves inside the encoding step.',960,815,42,INK,p,True,align='center',width=1700)
        self.note(c,'Arrangement and training task both matter · Joint attention is not an infallibility guarantee')

    def delulu_example(self,c,t,s):
        p=self.r(t,s)
        text(c,'“Am I being delulu about getting this job?”',960,280,38,BLUE,bold=True,align='center',width=1700)
        panel(c,150,365,770,340,'INTENDED MATCH FOR THIS NEED',['How to recognise unrealistic','expectations during a job search'],TEAL,.3+.7*p)
        panel(c,1000,365,770,340,'HARD NEGATIVE IN THE EXAMPLE',['Ten signs that you performed well','in your job interview'],RED)
        text(c,'Shared topic and advice format can hide the decisive intent.',960,815,37,INK,p,True,align='center',width=1700)
        self.note(c,'Source teaching example · No model run or measured ranking score is claimed')

    def pair_cost(self,c,t,s):
        p=self.r(t,s)
        text(c,'100 CANDIDATES',960,280,34,BLUE,bold=True,align='center')
        for i in range(100):
            x=180+(i%10)*78;y=340+(i//10)*39
            tiny(c,x,y,46,28,color=BLUE)
        arrow(c,1050,510,1150,510,TEAL,p,stroke=4)
        text(c,'≈100',1450,470,107,TEAL,p,True,align='center')
        rows(c,['query–candidate evaluations','Batching can organise the work'],1450,565,29,INK,p,step=55,align='center',width=620)
        self.note(c,'Source order-of-work example, not measured latency · Truncation and training still constrain the score')

    def llm_modes(self,c,t,s):
        self.plot(c,'reranking-modes')
        self.note(c,'Explicit criteria can include population, study design and whether the passage answers the question')

    def judgement_limits(self,c,t,s):
        self.four(c,[('POINTWISE',['Separate scores may need calibration','No direct candidate comparison'],BLUE),('PAIRWISE',['Many comparisons may be needed','Preferences can be inconsistent'],TEAL),('LISTWISE',['Context limits and input order','Windows or partial lists may be needed'],RED),('WHOLE PIPELINE',['Prompt, model version and sampling','A fluent rationale is not validation'],BLUE)],self.r(t,s))
        self.note(c,'Richer instructions do not recover a record absent from the candidate pool')

    def documented_boundary(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,285,1620,240,'SEMANTIC SCHOLAR · DOCUMENTED MAIN RELEVANCE ACCOUNT · 2025',['Elasticsearch keyword retrieval over titles, abstracts and author names','Up to 1,000 candidates → LightGBM reranking'],BLUE)
        panel(c,150,590,1620,230,'MACHINE-LEARNT RANKING INSIDE A LEXICAL CANDIDATE BOUNDARY',['Ranker signals include title matches, citations and recency','This account does not establish dense retrieval or an LLM reranker'],TEAL,.2+.8*p)
        self.note(c,'Pinned source documentation snapshot · No fresh service test or explanation of later interface counts')

    def token_hook(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,310,770,345,'ONE POOLED PASSAGE VECTOR',['A compact representation','Some local details can be blurred','[ · · · · ]'],BLUE)
        panel(c,1000,310,770,345,'RETAIN TOKEN-VECTOR SETS',['Independent document encoding','More local matching evidence','[ · · ]  [ · · ]  [ · · ]  …'],TEAL,.2+.8*p)
        text(c,'Store the token representations before the query arrives.',960,815,38,INK,p,True,align='center',width=1700)
        self.note(c,'ColBERT-style late interaction · Contextual token vectors, not bags of exact word counts')

    def token_sets(self,c,t,s):
        p=self.r(t,s)
        text(c,'QUERY TOKEN VECTORS',180,285,28,BLUE,bold=True)
        text(c,'DOCUMENT TOKEN VECTORS',1120,285,28,TEAL,bold=True)
        for i,label in enumerate(QUERY_TOKENS):
            x,y=250,410+i*210
            pill(c,label,x,y,BLUE,size=30)
            for j,doc in enumerate(DOCUMENT_TOKENS):
                line(c,570,y+20,1110,355+j*125,TEAL,.15+.25*p,stroke=2)
        for j,label in enumerate(DOCUMENT_TOKENS):pill(c,label,1140,335+j*125,TEAL,size=30)
        self.note(c,'Compare after independent encoding · Can serve retrieval or reranking depending on implementation')

    def maxsim_score(self,c,t,s):
        self.plot(c,'maxsim-table')
        self.plot(c,'maxsim',self.r(t,s,word='Keep'))
        self.note(c,'Source-exact invented values · MaxSim sums one maximum per query-token row')

    def alignment_limits(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,285,770,385,'SCORE COMPOSITION',['citation → citation: 0.90','benefit → advantage: 0.80','The same document token may win','for more than one query token'],TEAL)
        panel(c,1000,285,770,385,'WHAT REMAINS LATENT',['Why were those similarities learnt?','How were contextual vectors formed?','Alignment is scoring evidence','It is not end-to-end transparency'],RED,.2+.8*p)
        text(c,'You can inspect the contributions without explaining the whole model.',960,815,34,INK,p,True,align='center',width=1700)
        self.note(c,'Whole-word labels simplify the source illustration · Real models use their own tokenisers')

    def storage_tradeoff(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,310,770,360,'SIMPLIFIED 100-TOKEN PASSAGE',['One pooled vector: 1 vector','One retained vector per token: 100','Same dimensions assumed for the count'],BLUE)
        panel(c,1000,310,770,360,'STORAGE IS AN INFRASTRUCTURE CHOICE',['Token retention increases the footprint','Compression changes the byte budget','ColBERTv2 reports 6–10× reduction','relative to earlier late-interaction systems'],TEAL,.2+.8*p)
        self.note(c,'Toy vector count, not measured bytes · Source-attributed compression result is not a universal guarantee')

    def three_arrangements(self,c,t,s):
        self.plot(c,'encoding-arrangements')
        self.note(c,'A pretrained encoder name does not identify its arrangement, training task or pipeline position')

    def neural_sparse(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,285,770,410,'LEARNT SPARSE ROUTE',['Predict active vocabulary weights','Typed terms + learnt expansions','Inverted-index machinery can serve it','Active-coordinate overlap still matters'],BLUE)
        panel(c,1000,285,770,410,'ELICIT · JUNE 2024 ACCOUNT',['SPLADE-suggested query terms','Regular full-text retrieval','Development work, not confirmed rollout','Extra terms can increase posting work'],TEAL,.2+.8*p)
        text(c,'Familiar indexing infrastructure does not imply equal query cost.',960,815,35,INK,p,True,align='center',width=1700)
        self.note(c,'Pinned source account · No current-service test, deployment confirmation or latency benchmark')

    def inspection_questions(self,c,t,s):
        self.four(c,[('SPLADE',['Inspectable weighted vocabulary terms','Training-dependent expansion'],BLUE),('COLBERT',['Inspectable token alignments','Latent contextual representations'],TEAL),('NEURAL IR',['An umbrella across representations','and pipeline stages'],RED),('EVALUATE THE ARRANGEMENT',['Candidate source, comparison, training','Transfer to the actual search task'],BLUE)],self.r(t,s))
        self.note(c,'Limited public deployment documentation does not establish absence · Inspectable is not fully transparent')
    def list_hook(self,c,t,s):
        p=self.r(t,s)
        for i,label in enumerate(('A','B','C')):
            panel(c,130+i*570,310,520,315,f'PAPER {label}',['Strong individual match','Same overall-advantage aspect'],BLUE)
        text(c,'What could another useful aspect add to the list?',960,795,43,TEAL,p,True,align='center',width=1700)
        self.note(c,'Exploratory objective · Relevance to the query and marginal usefulness to a set are different questions')

    def aspect_example(self,c,t,s):
        self.plot(c,'aspect-coverage')
        self.note(c,'Schematic source pool and stipulated selections · Shared aspects do not make A, B and C duplicates')

    def distinct_objectives(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('DIVERSIFICATION',['An objective for the selected set','What does this candidate add?'],TEAL),('RERANKING',['A position in the pipeline','A second pass over candidates'],BLUE),('DEDUPLICATION',['A rule for equivalent records','Remove records judged the same'],RED)]):
            panel(c,130+i*570,320,520,340,title,body,color)
        text(c,'Topical difference alone establishes neither fairness nor balanced evidence.',960,815,34,INK,p,True,align='center',width=1700)
        self.note(c,'Define difference for the actual task: topic, method, geography, viewpoint or another property')

    def review_boundary(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,305,770,370,'EXPLORATORY SEARCH',['Less redundant aspects may help','A useful set for orientation','Evaluate the chosen diversity objective'],TEAL)
        panel(c,1000,305,770,370,'HIGH-RECALL REVIEW',['Similar studies remain distinct evidence','Every relevant study may be needed','A display cut-off can hide near-neighbours'],RED,.2+.8*p)
        text(c,'Diversification cannot retrieve records outside its pool.',960,815,40,INK,p,True,align='center',width=1700)
        self.note(c,'Broader-looking coverage is not an exhaustive evidence account')

    def product_budgets(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,280,770,440,'PUBMED BEST MATCH · PUBLISHED ACCOUNT',['BM25 first-stage ordering','Top 500 → LambdaMART reranking','Below 500: list continues','The tail is not discarded at that boundary'],BLUE)
        panel(c,1000,280,770,440,'PRIMO RESEARCH ASSISTANT · DOCUMENTED',['CDI candidate retrieval and ranking','Up to 30 → embedding reranking','5 selected abstracts → generation','Another source boundary limits the answer'],TEAL,.2+.8*p)
        text(c,'Candidate budgets describe processing, not relevance.',960,825,39,INK,p,True,align='center',width=1700)
        self.note(c,'Pinned source accounts, not new service tests · The products handle their tails differently')

    def primo_chain(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('1 · TRANSFORM',['LLM writes Boolean variations','Connected with OR','Supported auto-refinements'],BLUE),('2 · RETRIEVE + RANK',['CDI largely lexical retrieval','Term, field, phrase and proximity','Static ranking signals also apply'],TEAL),('3 · RERANK',['Up to 30 leading candidates','Reorder using embeddings','The pool is already bounded'],RED)]):
            x=130+i*570
            panel(c,x,320,520,390,title,body,color,1 if i==0 else .3+.7*p)
            if i<2:arrow(c,x+532,510,x+558,510,color,p)
        self.note(c,'Teaching decomposition of documented stages · An embedding reranker does not establish dense first-stage retrieval')

    def abstract_boundary(self,c,t,s):
        p=self.r(t,s)
        text(c,'PRIMO · DOCUMENTED WORKING SET FOR GENERATION',960,275,29,BLUE,bold=True,align='center',width=1700)
        for i in range(5):
            x=210+i*310
            tiny(c,x,355,230,300,f'Abstract {i+1}',TEAL)
        text(c,'5 abstracts ≠ 5 complete papers',960,775,53,RED,p,True,align='center',width=1700)
        self.note(c,'A detail only in full text was not supplied in this documented abstract-based context')

    def pipeline_questions(self,c,t,s):
        self.four(c,[('CANDIDATE ROUTE',['What searched the full collection?','What records could enter the pool?'],BLUE),('SECOND COMPARISON',['Which model and ranking task?','How many candidates and what text?'],TEAL),('SELECTED EVIDENCE',['Independent scores or useful coverage?','Which display and context boundaries?'],RED),('COMPLETE-PIPELINE EVALUATION',['Learning to rank can use lexical features','Chapter 10: combining or routing routes'],BLUE)],self.r(t,s))
        self.note(c,'A more detailed second pass inherits the candidate and evidence boundaries of earlier stages')

    def poster(self,c):
        c.clear(skia.Color(*CREAM))
        text(c,'HOW SEARCH DECIDES WHAT YOU SEE',130,130,27,MUTED,bold=True)
        text(c,f"CHAPTER 9 · FILM {self.script['episode_number']:02d}",130,220,30,self.accent,bold=True)
        titles={1:['The paper the','reranker never saw.'],2:['One vector,','or many clues?'],3:['The best next result','may rank lower.']}
        rows(c,titles[self.script['episode_number']],130,405,87,INK,bold=True,step=132,width=1190)
        text(c,self.script['subtitle'],130,750,31,MUTED,width=1130)
        for i in range(5):
            x=1450+(i%2)*155;y=340+(i//2)*150
            tiny(c,x,y,112,130,chr(65+i),self.accent)
        text(c,'Original animated investigation · Narrated and captioned',130,890,26,self.accent)
        text(c,'Adapted from Aaron Tay · CC BY 4.0',130,1000,23,MUTED)
