"""Original Chapter 13 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter13_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import check_examples, ID_RECORDS, exact_identifier_hits, RELATION_PAIR, NEGATION_PAIR, BERT_PIECES
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
        text(c, f"CHAPTER 13   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 13 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Chapter 13 teaching illustration · A missing result supplies a symptom; test the suspected boundary and lost evidence"):
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

    def missing_hook(self,c,t,s):
        self.four(c,[('P OUTSIDE THE COLLECTION',['The source was not covered','Or indexing has not caught up'],BLUE),('P EXCLUDED BY A FILTER',['The record exists in the collection','An applied limit blocks eligibility'],RED),('P ABSENT FROM THE CANDIDATE POOL',['Eligible, but not supplied by retrieval','Later stages never receive this paper'],TEAL),('P RETRIEVED BUT NOT DISPLAYED',['The record reached the candidate pool','Later ranking or a display limit hides it'],BLUE)],self.r(t,s))
        self.note(c,'Four alternative paths for the same hypothetical paper · The result screen alone does not identify the cause')

    def eligibility_first(self,c,t,s):
        self.four(c,[('COLLECTION COVERAGE',['Was this source searchable?','Check the database and indexed coverage'],BLUE),('INDEXING LAG',['Had this record entered the index?','A publication date is not an indexing date'],TEAL),('APPLIED LIMITS',['Date, format or access condition','Inspect visible filters and metadata'],RED),('UNKNOWN INTERNAL DETAILS',['Seek documentation or a saved trace','Unavailable evidence is not proof of exclusion'],BLUE)],self.r(t,s))
        self.note(c,'A record outside coverage or eligibility cannot be recovered through that unchanged boundary by vocabulary expansion')

    def pool_or_display(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,290,770,420,'ELIGIBLE → ABSENT FROM THE POOL',['Query and indexed evidence','Retrieval method and candidate cutoff','Later reranker never receives P','Investigate the first-stage boundary'],BLUE)
        panel(c,1000,290,770,420,'IN THE POOL → BELOW DISPLAY LIMIT',['P was matched and supplied','Later ranking, selection or presentation','Investigate the later boundary','Check filter and cutoff order too'],TEAL,.2+.8*p)
        text(c,'A missing result does not reveal internal candidate membership.',960,820,37,INK,p,True,align='center',width=1700)
        self.note(c,'Alternative hypothetical cases · A failed lookup alone does not identify the stage that excluded P')

    def units_and_excerpts(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('WHOLE DOCUMENT',['The complete claim is present','Its parts may span indexed units','Presence in the document is one fact'],BLUE),('PASSAGE INDEX',['One unit carries only part of the claim','Another carries the remaining evidence','Neither may rank strongly enough'],TEAL),('VISIBLE EXCERPT',['Only a selected view of the record','A term may match another field or version','Check what was actually indexed'],RED)]):
            panel(c,130+i*570,305,520,405,title,body,color,1 if i==0 else .3+.7*p)
        text(c,'Indexed units, indexed fields and displayed excerpts can differ.',960,820,36,INK,p,True,align='center',width=1700)
        self.note(c,'Diagnostic possibilities from the chapter · These drawings do not establish any particular product’s indexing or matching')

    def four_lenses(self,c,t,s):
        self.plot(c,'diagnostic-lenses')
        self.note(c,'Different kinds of claim · A query–record relation, a component vocabulary, training transfer, or a lost relationship')

    def heart_bridge(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,290,770,395,'QUERY',['heart attack recovery','The searcher’s lexical forms','Neither expression is necessarily OOV'],BLUE)
        panel(c,1000,290,770,395,'KNOWN RELEVANT TITLE',['Rehabilitation after myocardial infarction','Related concept, different terminology','Evidence for vocabulary mismatch'],TEAL,.2+.8*p)
        arrow(c,930,495,990,495,TEAL,p)
        text(c,'Synonyms · Controlled vocabulary · Explicit OR · Citation searching',960,815,34,INK,p,True,align='center',width=1700)
        self.note(c,'Source text example · No retrieval or clinical claim is being tested in this illustration')

    def retrieval_bridges(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,295,770,420,'BM25 + LEXICAL ANALYSIS',['Partial lexical overlap can contribute','Analysis may connect morphological variants','The scoring rule does not itself supply','heart attack = myocardial infarction'],BLUE)
        panel(c,1000,295,770,420,'SUITABLY TRAINED DENSE RETRIEVAL',['May connect complete representations','Can bridge without exact lexical overlap','A response to an old retrieval problem','No guarantee for every paraphrase'],TEAL,.2+.8*p)
        text(c,'Check the suspected bridge against known relevant records.',960,820,39,INK,p,True,align='center',width=1700)
        self.note(c,'Remedies to test · Expansion performed elsewhere should not be attributed to BM25’s scoring formula')

    def diagnostic_record(self,c,t,s):
        self.four(c,[('OBSERVATION',['Original query and known relevant record','What was actually visible?'],BLUE),('BOUNDARY EVIDENCE',['Coverage, limits, indexed units and trace','Which facts are documented or unknown?'],TEAL),('HYPOTHESIS',['What evidence might have been lost?','More than one explanation may apply'],RED),('TESTED INTERVENTION',['Choose a remedy for the suspected cause','Check whether the expected record is recovered'],BLUE)],self.r(t,s))
        self.note(c,'A result screen supplies symptoms, not causes · Preserve the distinction between observation and inference')

    def encodable_hook(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('VISIBLE STRING',['An identifier is printed in a record','That does not identify the indexed field','Eligibility still needs checking'],BLUE),('ENCODABLE STRING',['The model can represent its pieces','That answers a tokenisation question','Not every retrieval question'],TEAL),('USEFUL RETRIEVAL EVIDENCE',['Was lexical evidence preserved?','Was a useful representation learnt?','Those questions remain open'],RED)]):
            panel(c,130+i*570,310,520,400,title,body,color,1 if i==0 else .25+.75*p)
        text(c,'Out of whose vocabulary?',960,815,48,INK,p,True,align='center',width=1700)
        self.note(c,'Hypothetical diagnostic setup · Encoding a string is not proof that a retriever can use it well')

    def three_questions(self,c,t,s):
        self.plot(c,'vocabulary-layers')
        self.note(c,'Inspect lexical index analysis separately from model tokenisation and learnt retrieval representation')

    def word_and_subword(self,c,t,s):
        p=self.r(t,s)
        text(c,'rizzlord',960,335,70,INK,bold=True,align='center')
        text(c,'Source-reported BERT pieces',960,415,29,MUTED,align='center')
        for i,label in enumerate(BERT_PIECES):
            x=330+i*440
            rect(c,x,490,380,155,PAPER,1 if i==0 else .25+.75*p,6)
            text(c,label,x+190,588,56,TEAL,1 if i==0 else p,True,align='center',width=340)
            if i<2:text(c,'+',x+410,585,34,MUTED,p,align='center')
        text(c,'Not the reader’s neat “rizz” + “lord” decomposition',960,800,38,INK,p,True,align='center',width=1700)
        self.note(c,'Tokenisation reported in the chapter’s Appendix B · No new tokenizer run · Other models may split the same string differently')

    def bytes_are_not_meaning(self,c,t,s):
        self.four(c,[('WORD-LEVEL VOCABULARY',['A complete word entry may be missing','Name the vocabulary before saying OOV'],BLUE),('SUBWORD VOCABULARY',['Known pieces may encode a new string','Piece boundaries need not match a reader’s'],TEAL),('BYTE / CHARACTER COVERAGE',['Pure byte model: valid UTF-8 input','Character model: inventory or fallback matters'],RED),('LEARNT RETRIEVAL REPRESENTATION',['Form can be encodable but poorly useful','Test retrieval, not only encoding coverage'],BLUE)],self.r(t,s))
        self.note(c,'Tokenisable does not establish understanding or useful retrieval · Keep literal OOV separate from a representation gap')

    def exact_identity(self,c,t,s):
        p=self.r(t,s)
        text(c,'QUERY · DELULU-427',960,290,39,BLUE,bold=True,align='center')
        hits=exact_identifier_hits()
        for i,(label,value) in enumerate(ID_RECORDS):
            x=170+i*430;color=TEAL if label in hits else RED
            self.record(c,x,365,310,235,label,color)
            text(c,value,x+155,665,30,INK,bold=True,align='center',width=390)
            text(c,'EXACT MATCH' if label in hits else 'DIFFERENT ID',x+155,730,23,color,p,True,align='center',width=390)
        text(c,'Literal equality selects D1, D2 and D3.',960,825,39,INK,p,True,align='center',width=1700)
        self.note(c,'Invented keyword-field records · Calculation of exact identity only; not a BM25 run or a claim about an ordinary text analyser')

    def pooled_identity(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,300,770,405,'A DECISIVE LOCAL DIFFERENCE',['DELULU-427','DELULU-428','Exact identity determines relevance'],BLUE)
        panel(c,1000,300,770,405,'ONE POOLED REPRESENTATION',['Model tokens can encode both strings','Pooling may blur related strings or concepts','Better training can mitigate the weakness'],TEAL,.2+.8*p)
        text(c,'Representable does not mean reliably distinguishable.',960,815,41,INK,p,True,align='center',width=1700)
        self.note(c,'Teaching contrast · No vectors, similarity scores or model ranking measured · Dense retrieval does not always fail on identifiers')

    def preserve_a_route(self,c,t,s):
        self.four(c,[('IDENTITY-SENSITIVE INPUTS',['Genes, chemicals and article identifiers','Dataset titles, model names and personal names'],BLUE),('PRESERVE A LEXICAL ROUTE',['Use an appropriate field and matching path','Check query and document analysis agree'],TEAL),('A POSSIBLE VOCABULARY REPAIR',['Synonym or controlled term for some absence','Keyword field for complete exact identity'],RED),('OTHER FAILURES STILL NEED EVIDENCE',['Training transfer is a different question','So are negation, direction and relation binding'],BLUE)],self.r(t,s))
        self.note(c,'Choose the remedy for the component that lost evidence · No single representation preserves everything')

    def layered_evidence(self,c,t,s):
        self.four(c,[('KNOWN RELEVANT RECORD',['Establish eligibility and indexed evidence','Keep a neighbouring-string contrast'],BLUE),('LEXICAL LAYER',['Literal input, field and analysis','An indexed term is not a model token'],TEAL),('MODEL LAYER',['Tokenisation and learnt representation','Mark undisclosed details unknown'],RED),('RETRIEVAL OUTCOME',['Test which records actually return','Several diagnostic hypotheses can coexist'],BLUE)],self.r(t,s))
        self.note(c,'Encoding gives evidence about one layer · It does not identify a complete cause of retrieval failure')
    def relation_hook(self,c,t,s):
        p=self.r(t,s)
        for x,title,labels,color,a in [(150,'REQUIRED DIRECTION',('A','B'),BLUE,1),(1000,'REVERSED DIRECTION',('B','A'),RED,.2+.8*p)]:
            rect(c,x,300,770,400,PAPER,a,6)
            text(c,title,x+385,365,29,color,a,True,align='center',width=690)
            for j,label in enumerate(labels):
                circle(c,x+180+j*410,505,72,color,a)
                text(c,label,x+180+j*410,524,57,PAPER,a,True,align='center')
            arrow(c,x+270,505,x+500,505,color,a)
            text(c,'causes',x+385,470,26,MUTED,a,align='center')
            text(c,'Term inventory: A · causes · B',x+385,645,27,INK,a,True,align='center',width=690)
        text(c,'Same term counts. Different causal direction.',960,815,43,INK,p,True,align='center',width=1700)
        self.note(c,'Controlled text contrast · Equal term counts verified; no retrieval scores or model behaviour predicted')

    def shift_sites(self,c,t,s):
        self.plot(c,'distribution-shifts')
        self.note(c,'OOD is a training–deployment relationship · Vocabulary familiarity alone neither proves nor rules it out')

    def training_relevance(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,300,770,400,'WHAT TRAINING REWARDED',['Positive pairs, negatives and labels','An operational meaning of relevance','Example: find one answer-bearing passage'],BLUE)
        panel(c,1000,300,770,400,'WHAT DEPLOYMENT REQUIRES',['All studies meeting review criteria','A particular known item','Or a useful citation relationship'],TEAL,.2+.8*p)
        arrow(c,930,505,990,505,TEAL,p)
        text(c,'Will the rewarded relationship transfer to this task?',960,815,42,INK,p,True,align='center',width=1700)
        self.note(c,'Examples of different relevance purposes · Task shift can overlap with terminology and representation problems')

    def local_comparison(self,c,t,s):
        self.four(c,[('LOCAL DIAGNOSTIC EVIDENCE',['Compare a set of queries and relevance judgements','Look for systematic differences by setting'],BLUE),('TRAINING UNCERTAINTY',['Undisclosed training data limits conclusions','One poor result cannot prove OOD'],RED),('THE CITED BEIR FINDING',['BM25 was a robust zero-shot baseline','Some costlier neural/reranking methods won on average'],TEAL),('THE LIMIT OF THAT FINDING',['Evidence about those benchmark tasks','Not a law about every lexical or dense retriever'],BLUE)],self.r(t,s))
        self.note(c,'Source research summary · No new benchmark run · Compare locally before adapting, retraining or replacing a model')

    def logic_and_proximity(self,c,t,s):
        p=self.r(t,s)
        text(c,NEGATION_PAIR[0],960,300,39,BLUE,bold=True,align='center',width=1700)
        text(c,NEGATION_PAIR[1],960,375,39,RED,p,True,align='center',width=1700)
        panel(c,150,460,770,340,'BOOLEAN TERM LOGIC',['Explicit inclusion and exclusion','Ordinary AND does not bind a proposition','Excluding a word ≠ interpreting negation scope'],BLUE)
        panel(c,1000,460,770,340,'PHRASES, POSITIONS AND PROXIMITY',['Preserve adjacency and local order','Useful controls to test','Adjacency alone does not solve causality'],TEAL,.2+.8*p)
        self.note(c,'Controlled statements, not model scores · Direction, negation and relation binding need targeted checks')

    def interaction_limits(self,c,t,s):
        self.four(c,[('CROSS-ENCODER',['Reads query and candidate jointly','Strongest architectural opportunity for relations'],BLUE),('LATE INTERACTION',['Preserves more token-level evidence','Query and document still encoded separately'],TEAL),('THE CITED NEVIR RESULT',['Cross-encoders strongest; late interaction next','Most systems at or below a random baseline'],RED),('TWO LIMITS TO KEEP VISIBLE',['Neither architecture guarantees correct logic','A reranker cannot rescue an absent candidate'],BLUE)],self.r(t,s))
        self.note(c,'Source summary of NevIR (Weller et al., 2024) · No new model ranking or guarantee of logical reasoning')

    def preservation_patterns(self,c,t,s):
        self.plot(c,'first-stage-preservation')
        self.note(c,'Transformation changes inputs · Control chooses operations · Rerankers compare shortlists · A pipeline may combine methods')

    def hypothesis_to_test(self,c,t,s):
        self.plot(c,'remedy-tests')
        self.note(c,'Diagnosis supplies hypotheses · Chapter 14 asks how to compare retrieval and define better for the actual task')

    def poster(self,c):
        c.clear(skia.Color(*CREAM))
        text(c,'HOW SEARCH DECIDES WHAT YOU SEE',130,130,27,MUTED,bold=True)
        text(c,f"CHAPTER 13 · FILM {self.script['episode_number']:02d}",130,220,30,self.accent,bold=True)
        titles={1:['Where did','the paper go?'],2:['It can spell it.','Can it find it?'],3:['Every word','was there.']}
        rows(c,titles[self.script['episode_number']],130,405,88,INK,bold=True,step=132,width=1190)
        text(c,self.script['subtitle'],130,750,31,MUTED,width=1130)
        for i,label in enumerate(('P','?','↗')):
            self.record(c,1450+i*75,340+i*135,180,230,label,self.accent)
        text(c,'Original animated investigation · Narrated and captioned',130,890,26,self.accent)
        text(c,'Adapted from Aaron Tay · CC BY 4.0',130,1000,23,MUTED)
