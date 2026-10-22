"""Original Chapter 8 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter8_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import VOCAB, SOURCE_BINARY, EXPANSION, BIBLIOGRAPHIC, MATCHES, groups, check_examples
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
        text(c, f"CHAPTER 8   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 8 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Chapter 8 teaching illustration · Representation, indexed evidence and result display are separate choices"):
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

    def vector_hook(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body) in enumerate([('D1',['heart attack','treatment']),('D2',['job interview','tips']),('D3',['cancer','treatment'])]):
            panel(c,140+i*570,310,500,310,title,body,BLUE)
        text(c,'An ordered list of numbers can already describe each one.',960,800,39,TEAL,p,True,align='center',width=1700)
        self.note(c,'Prediction: what does each coordinate mean? · No neural model is needed for this construction')

    def coordinates(self,c,t,s):
        self.plot(c,'binary-vectors')
        self.note(c,'The order is arbitrary but must be consistent · Sparse storage can omit the zeros')

    def overlap_logic(self,c,t,s):
        p=self.r(t,s)
        pill(c,'QUERY: heart treatment',150,260,BLUE)
        for i,(name,score,color) in enumerate([('D1',2,TEAL),('D3',1,BLUE),('D2',0,MUTED)]):
            y=380+i*135
            text(c,name,180,y+30,36,color,bold=True)
            for j in range(2):
                circle(c,380+j*95,y+15,24,color if j<score else RULE)
            text(c,f'{score} shared terms',620,y+30,32,INK)
        panel(c,1080,335,670,205,'AND: REQUIRE BOTH',['Only D1 is admitted'],TEAL,.2+.8*p)
        panel(c,1080,600,670,205,'OR: REQUIRE EITHER',['D1 and D3 are admitted'],BLUE,.2+.8*p)
        self.note(c,'Same binary presence evidence · Different retrieval rules')

    def term_counts(self,c,t,s):
        self.plot(c,'term-counts')
        self.note(c,'Raw TF records repetition · Binary presence would still put 1 in the treatment coordinate')

    def rarity_weights(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,310,770,350,'heart',['Present in 1 of 3 documents','IDF = ln(3/1) ≈ 1.099','More rarity weight per occurrence'],TEAL)
        panel(c,1000,310,770,350,'treatment',['Present in 2 of 3 documents','IDF = ln(3/2) ≈ 0.405','Less rarity weight per occurrence'],BLUE)
        text(c,'TF–IDF = raw count × ln(N/df)',960,805,46,INK,p,True,align='center',width=1700)
        self.note(c,'Declared TF–IDF variant · Formula choices vary · Coordinates remain vocabulary terms')

    def bm25_weights(self,c,t,s):
        self.plot(c,'lexical-weights')
        self.note(c,'Comparison of representations, not a history of derivation · Both weights remain lexical')

    def inverted_storage(self,c,t,s):
        p=self.r(t,s)
        panel(c,140,285,730,260,'CONCEPTUAL VOCABULARY SPACE',['Millions of possible coordinates','A short document activates few'],BLUE)
        for i in range(42):
            color=BLUE if i in (2,7,18,30) else RULE
            rect(c,165+(i%14)*47,605+(i//14)*48,30,30,color,.25 if color==RULE else 1,2)
        arrow(c,930,520,1020,520,TEAL,p,stroke=4)
        panel(c,1080,300,690,430,'STORE ACTIVE ENTRIES',['(attack, weight)','(heart, weight)','(treatment, weight)','Query terms → posting lists'],TEAL,.2+.8*p)
        self.note(c,'A dot-product-style score does not imply dense storage or nearest-neighbour execution')

    def vector_verdict(self,c,t,s):
        self.four(c,[('COORDINATES',['Vocabulary terms? Latent features?','Recorded fields?'],BLUE),('ACTIVE VALUES',['Mostly zero? Mostly active?','How is sparsity used?'],TEAL),('WEIGHTING RULE',['Counts and collection formulas?','A mapping fitted during training?'],RED),('RETRIEVAL RULE',['Hard admission conditions?','Graded contributions and ranking?'],BLUE)],self.r(t,s))
        self.note(c,'“Uses vectors” names the numerical object · Ask which evidence the representation preserves')

    def dense_hook(self,c,t,s):
        p=self.r(t,s)
        for i,(name,value) in enumerate(BIBLIOGRAPHIC.items()):
            x=140+i*435
            rect(c,x,330,390,340,PAPER)
            text(c,str(value),x+195,490,79,BLUE,bold=True,align='center',width=340)
            text(c,name.upper(),x+195,595,26,TEAL,p,True,align='center',width=340)
        text(c,'Dense: all four coordinates are active.',960,780,40,INK,bold=True,align='center',width=1700)
        self.note(c,'Explicit bibliographic facts · Density alone does not establish semantic text matching')

    def separate_questions(self,c,t,s):
        self.four(c,[('IS IT A VECTOR?',['An ordered list of numbers'],BLUE),('SPARSE OR DENSE?',['Relatively few or mostly active','coordinates'],TEAL),('SPECIFIED OR LEARNT?',['Where did the rule for its','numbers come from?'],RED),('WHAT EVIDENCE?',['Named fields or words?','Distributed latent features?'],BLUE)],self.r(t,s))
        self.note(c,'Shape, provenance and preserved evidence are different questions')

    def latent_coordinates(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,305,770,395,'VOCABULARY-ALIGNED',['heart → named term coordinate','treatment → named term coordinate','Active entries can be listed'],BLUE)
        panel(c,1000,305,770,395,'DISTRIBUTED LATENT FEATURES',['[0.14, −0.37, 0.81, …]','Coordinate 3 is not “citation”','Meaning depends on the representation'],TEAL,.2+.8*p)
        text(c,'Training and task evaluation establish capability.',960,815,40,INK,p,True,align='center',width=1700)
        self.note(c,'Dense values are structural illustrations, not measured outputs from a named model')

    def learned_weights(self,c,t,s):
        p=self.r(t,s)
        panel(c,140,340,500,310,'READ THE TEXT',['heart attack','Transformer language model'],BLUE)
        arrow(c,675,490,770,490,TEAL,p,stroke=4)
        panel(c,815,280,955,440,'PREDICT VOCABULARY WEIGHTS',['Output vocabulary: WordPiece subword units','Absent input terms can receive weight','Training penalty encourages sparsity','Most coordinates stay zero'],TEAL,.2+.8*p)
        self.note(c,'Standard SPLADE vocabulary differs from a BM25 index’s chosen analysed terms')

    def expansion_bridge(self,c,t,s):
        self.plot(c,'sparse-expansion')
        self.note(c,'A query activating myocardial + infarction can share these expanded coordinates · Training-dependent')

    def sparse_execution(self,c,t,s):
        p=self.r(t,s)
        for i in range(140):
            active=i in (2,16,34,58)
            rect(c,160+(i%20)*45,340+(i//20)*55,28,30,TEAL if active else RULE,1 if active else .3,2)
        text(c,'Most vocabulary entries stay zero',610,790,30,BLUE,bold=True,align='center',width=930)
        panel(c,1150,315,620,440,'ACTIVE TERMS → POSTINGS',['Exact terms and expansions','One retrieval route is possible','May also join a hybrid pipeline','Cost depends on active postings'],TEAL,.2+.8*p)
        self.note(c,'Schematic grid, not a measured sparsity rate · Index and query costs depend on the actual implementation')

    def comparison_choice(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,310,770,345,'SPARSE VOCABULARY WEIGHTS',['Dot product or cosine can apply','Named active coordinates','Appropriate comparison still matters'],BLUE)
        panel(c,1000,310,770,345,'DENSE LATENT FEATURES',['Dot product or cosine can apply','Distributed coordinates','Appropriate comparison still matters'],TEAL,.2+.8*p)
        text(c,'Arithmetic does not settle admission or which results are returned.',960,805,36,INK,p,True,align='center',width=1700)
        self.note(c,'Representation, comparison operation and result boundary are separate choices')

    def representation_passport(self,c,t,s):
        self.plot(c,'representation-cases')
        self.note(c,'Meaning-oriented matching is a capability to evaluate against a stated information need')
    def units_hook(self,c,t,s):
        p=self.r(t,s)
        for i,(paper,n) in enumerate(MATCHES):
            x=150+i*430
            panel(c,x,305,380,290,f'{paper} · passage {n}',['One retrieved unit'],BLUE if paper=='A' else TEAL)
        text(c,'4 passage matches → 2 distinct papers',960,770,51,RED,p,True,align='center',width=1700)
        self.note(c,'Source-exact grouping example · A display may show passages or grouped paper results')

    def unit_strategies(self,c,t,s):
        p=self.r(t,s)
        for j,(title,count,color) in enumerate([('1 ABSTRACT',1,BLUE),('10 SECTIONS',10,TEAL),('50 PASSAGES',50,RED)]):
            x=130+j*570
            rect(c,x,280,520,495,PAPER)
            text(c,title,x+260,340,30,color,bold=True,align='center',width=470)
            cols=1 if count==1 else 5 if count==10 else 10
            size=140 if count==1 else 65 if count==10 else 34
            for i in range(count):
                xx=x+260-cols*(size+10)/2+(i%cols)*(size+10)
                yy=400+(i//cols)*(size+16)
                tiny(c,xx,yy,size,size*1.12,color=color,a=1 if j==0 else .35+.65*p)
        self.note(c,'Same illustrative 20-page article · Alternative indexing choices, not measured product settings')

    def independent_units(self,c,t,s):
        p=self.r(t,s)
        for j in range(2):
            for i in range(5):
                x=160+i*333;y=325+j*240
                tiny(c,x,y,105,130,str(j*5+i+1),BLUE)
                arrow(c,x+120,y+67,x+162,y+67,TEAL,p)
                rows(c,['[ · · · ]','vector'],x+185,y+57,24,TEAL,.3+.7*p,step=40,width=120)
        text(c,'50 indexed passages → 50 independently searchable pooled vectors',960,825,35,INK,p,True,align='center',width=1700)
        self.note(c,'Ten units drawn to illustrate the mapping · No single vector automatically captures the whole paper')

    def split_evidence(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('PASSAGE 1',['Participants: adults','Population evidence'],BLUE),('PASSAGE 2',['Numerical outcome','Result evidence'],TEAL),('PASSAGE 3',['A decisive limitation','Interpretive context'],RED)]):
            panel(c,130+i*570,320,520,330,title,body,color)
        text(c,'A question may need relationships across all three.',960,795,41,INK,p,True,align='center',width=1700)
        self.note(c,'Declared illustration · Neither separate vectors nor overlap automatically combine the evidence')

    def indexed_limit(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,300,770,380,'ABSTRACT-ONLY INDEX',['Abstract is searchable','Results-only claim is absent','Paper may match on other evidence'],BLUE)
        panel(c,1000,300,770,380,'FULL-TEXT CHUNK INDEX',['Results passage can be searchable','Local evidence may be reachable','Depends on the actual indexed text'],TEAL,.2+.8*p)
        text(c,'The indexed unit sets the evidence available at that stage.',960,810,38,INK,p,True,align='center',width=1700)
        self.note(c,'The chapter describes Wiley AI Gateway full-text chunks · No fresh service test or performance claim')

    def later_context(self,c,t,s):
        p=self.r(t,s)
        items=[('INDEXED',['Abstract or passage','Evidence initially searchable'],BLUE),('RETRIEVED',['A selected indexed unit','Candidate source for context'],TEAL),('SUPPLIED CONTEXT',['May fetch neighbours or full text','May compress selected units'],RED)]
        for i,(title,body,color) in enumerate(items):
            x=130+i*570
            panel(c,x,330,520,340,title,body,color,1 if i<2 else .2+.8*p)
            if i<2:arrow(c,x+532,500,x+558,500,color,p)
        text(c,'Document the later fetch as its own operation.',960,810,42,INK,p,True,align='center',width=1700)
        self.note(c,'Retrieved unit and generator context may differ · Evidence use in the answer needs its own evaluation')

    def group_matches(self,c,t,s):
        p=self.r(t,s)
        for i,(paper,n) in enumerate(MATCHES):
            y=305+i*125
            pill(c,f'{paper} · passage {n}',220,y,BLUE if paper=='A' else TEAL,size=30)
        arrow(c,770,520,1000,520,RED,p,stroke=4)
        panel(c,1090,290,660,235,'PAPER A',['Passages 2, 7 and 9'],BLUE,.2+.8*p)
        panel(c,1090,580,660,235,'PAPER B',['Passage 3'],TEAL,.2+.8*p)
        self.note(c,'Grouping by source identity specifies neither a paper-score formula nor evidence synthesis')

    def unit_questions(self,c,t,s):
        self.four(c,[('SOURCE DOCUMENT',['The article, report or book','a reader thinks of as one object'],BLUE),('INDEXED UNIT',['Abstract, section, sentence, passage','What text can match at this stage?'],TEAL),('REPRESENTATION',['One pooled vector per unit here','What evidence survives encoding?'],RED),('RESULT AGGREGATION',['Separate passages or paper groups?','Which aggregation and scoring rule?'],BLUE)],self.r(t,s))
        self.note(c,'Then document later context expansion · Chapter 9 examines careful comparison after a shortlist')

    def poster(self,c):
        c.clear(skia.Color(*CREAM))
        text(c,'HOW SEARCH DECIDES WHAT YOU SEE',130,130,27,MUTED,bold=True)
        text(c,f"CHAPTER 8 · FILM {self.script['episode_number']:02d}",130,220,30,self.accent,bold=True)
        titles={1:['The vector hiding','in keyword search.'],2:['Dense does not','mean semantic.'],3:['One paper, fifty','searchable objects.']}
        rows(c,titles[self.script['episode_number']],130,405,88,INK,bold=True,step=132,width=1190)
        text(c,self.script['subtitle'],130,750,31,MUTED,width=1130)
        for j in range(3):
            x=1420+j*85;y=410+j*58
            tiny(c,x,y,160,230,['01','10','50'][j],self.accent)
        text(c,'Original animated investigation · Narrated and captioned',130,890,26,self.accent)
        text(c,'Adapted from Aaron Tay · CC BY 4.0',130,1000,23,MUTED)
