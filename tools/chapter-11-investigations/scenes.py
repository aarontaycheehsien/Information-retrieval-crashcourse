"""Original Chapter 11 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter11_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import GENERATED_TEXT, STRUCTURED_QUERY, check_examples
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
        text(c, f"CHAPTER 11   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 11 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Chapter 11 teaching illustration · Identify the input object, its receiver and the operation that changed it"):
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

    def object_hook(self,c,t,s):
        self.four(c,[('A QUESTION',['“Is there an open-access citation advantage?”','A text input to a retrieval pipeline'],BLUE),('A KNOWN PAPER',['A seed that stands for the need','Text similarity, graph relationships or both'],TEAL),('A CITATION',['A relationship to follow','An edge in a citation graph'],RED),('A RESEARCH BRIEF',['Goal, criteria, sources and stopping','Instructions addressed to a controller'],BLUE)],self.r(t,s))
        self.note(c,'Same information need · Different objects address different mechanisms, rather than different phrasing styles')

    def text_and_structure(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,305,770,390,'FREE TEXT STRING',['Keywords, phrases or prose','May be analysed, encoded or rewritten','Lexical, dense or hybrid retrieval','The box alone does not reveal the path'],BLUE)
        panel(c,1000,305,770,390,'CONTROLLED / STRUCTURED',['Subject headings and annotations','Named fields, filters and proximity','Supported Boolean conditions','Depends on the target database syntax'],TEAL,.2+.8*p)
        text(c,'A MeSH heading is more than a formal keyword.',960,815,42,INK,p,True,align='center',width=1700)
        self.note(c,'Text and structured conditions can coexist · Supported syntax and annotation coverage must be checked')

    def records_and_links(self,c,t,s):
        p=self.r(t,s)
        for j,title in enumerate(['DIRECT CITATION','BIBLIOGRAPHIC COUPLING','CO-CITATION']):
            x=130+j*570
            rect(c,x,300,520,470,PAPER)
            text(c,title,x+260,365,28,BLUE,bold=True,align='center',width=470)
            points=[('A',140,460),('R',380,650)] if j==0 else [('A',110,460),('B',410,460),('R',260,650)] if j==1 else [('C',260,460),('A',110,650),('B',410,650)]
            pairs=[(0,1)] if j==0 else [(0,2),(1,2)] if j==1 else [(0,1),(0,2)]
            for a,b in pairs:
                _,ax,ay=points[a];_,bx,by=points[b]
                arrow(c,x+ax,ay+25,x+bx,by-25,TEAL,.3+.7*p,stroke=3)
            for label,xx,yy in points:
                circle(c,x+xx,yy,25,BLUE)
                text(c,label,x+xx,yy+9,25,PAPER,bold=True,align='center')
            text(c,['Follow an explicit edge','Share a reference','Are cited together'][j],x+260,735,26,MUTED,align='center',width=470)
        self.note(c,'Arrows run from citing to cited paper · Seed input may use text, citation relations or both; it does not imply embeddings')

    def feedback_and_monitoring(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,305,770,390,'RELEVANCE JUDGEMENTS',['Accepted or rejected records','Help construct a later retrieval input','PRF instead assumes top records relevant','Screening feedback has a different boundary'],BLUE)
        panel(c,1000,305,770,390,'BROWSE / MONITORING TARGET',['Journal, author, subject or collection','Saved searches and continuing alerts','Recognise a useful paper when it appears','The target is more than a wording choice'],TEAL,.2+.8*p)
        self.note(c,'These objects may cooperate with text queries, seeds, citation links and structured conditions')

    def predicates_and_briefs(self,c,t,s):
        self.four(c,[('PROGRAMMATIC PREDICATE',['API attributes, ranges and identifier lists','Sorting and pagination can be explicit'],BLUE),('TASK BRIEF',['Scope, criteria, sources, output and stopping','Not all of this is input every retriever obeys'],TEAL),('THE SUBJECT OF A STUDY',['A study about open access','may itself be paywalled'],RED),('FILTER THE INTENDED PROPERTY',['The chapter uses publication year here','OA status would change the question'],BLUE)],self.r(t,s))
        self.note(c,'API requests can also carry text · A filter on the retrieved paper is not a filter on what the paper studies')

    def objects_cooperate(self,c,t,s):
        self.plot(c,'review-audit')
        self.note(c,'Text → seeds → citation links → feedback → repeatable procedure · Search can develop through berrypicking')

    def phrase_for_receiver(self,c,t,s):
        self.plot(c,'receiving-components')
        self.note(c,'Detailed instructions require suitable training · Form depends on the receiving component')

    def known_record_tests(self,c,t,s):
        self.four(c,[('VARY THE TEXT INPUT',['Short terms, a question, known-item title','Use known relevant records for comparison'],BLUE),('INSPECT STRUCTURED INPUTS',['Fields, controlled terms and Boolean logic','Validate syntax in the target database'],TEAL),('CHECK GENERATED TERMS',['Generated strategies can contain invalid','MeSH terms or omitted concepts'],RED),('ASK BEFORE REPHRASING',['What object represents the need?','Which mechanism actually receives it?'],BLUE)],self.r(t,s))
        self.note(c,'These are evaluation suggestions, not new model tests · Longer or more polished text is not a quality guarantee')

    def understanding_hook(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('UNDERSTAND',['Interpret the request','May leave retrieval input unchanged'],BLUE),('TRANSFORM',['Create changed or additional inputs','A field, filter, rewrite or representation'],TEAL),('CONTROL',['Choose routes or another search','Decide where retrieval inputs go'],RED)]):
            panel(c,130+i*570,330,520,350,title,body,color,1 if i==0 else .3+.7*p)
        text(c,'Recognising a date does not establish the later operations.',960,815,38,INK,p,True,align='center',width=1700)
        self.note(c,'Interpretation can trigger transformation, control or both · The operations need not occupy one fixed stage')

    def visible_boolean(self,c,t,s):
        self.plot(c,'visible-boolean')
        self.note(c,'Source example: fruit topics, 2020–2024, University of California affiliation · Inspect the generated AND relationships')

    def primo_distinction(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,285,770,440,'PRIMO VE NDE NATURAL LANGUAGE SEARCH',['GPT-4.1 Mini identifies fields and filters','Basic Boolean + six OR-connected permutations','Advanced Search receives the expression','The generated query is inspectable and editable'],BLUE)
        panel(c,1000,285,770,440,'PRIMO RESEARCH ASSISTANT',['A distinct documented workflow','Question → Boolean variations → CDI','Candidate retrieval precedes embedding reranking','Do not transfer architecture between features'],TEAL,.2+.8*p)
        self.note(c,'Pinned source accounts · Six OR-connected permutations do not establish six independent retrieval calls')

    def retrieval_feedback(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('INITIAL RETRIEVAL',['Produce an initial ranking','It may contain off-topic records'],BLUE),('CONSTRUCT LATER INPUT',['Explicit: searcher judgements','PRF: assume top results relevant'],TEAL),('SEARCH AGAIN',['A later retrieval pass','May add new candidates'],RED)]):
            x=130+i*570
            panel(c,x,330,520,350,title,body,color,1 if i==0 else .3+.7*p)
            if i<2:arrow(c,x+532,505,x+558,505,color,p)
        text(c,'An unverified top-result assumption can reinforce an early mistake.',960,815,35,INK,p,True,align='center',width=1700)
        self.note(c,'Schematic feedback sequence, not a measured PRF run · Inspect the initial ranking used to build the later query')

    def screening_boundary(self,c,t,s):
        self.plot(c,'feedback-boundaries')
        self.note(c,'Reprioritising a screening queue does not inherently search the collection again or enlarge the candidate pool')

    def fixed_feedback_loop(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,305,770,385,'CONTENTS CAN ADAPT',['Pass 1 returns a particular ranking','Selected terms depend on those results','The second query can change accordingly'],TEAL)
        panel(c,1000,305,770,385,'THE SEQUENCE CAN STAY FIXED',['Designer prescribes two passes every time','Search → select terms → search again','Retrieval-dependent does not imply agentic'],BLUE,.2+.8*p)
        text(c,'Who chooses the next action is a separate question.',960,815,42,INK,p,True,align='center',width=1700)
        self.note(c,'PRF includes a retrieval-to-transformation loop · Chapter 12 examines control while a search is running')

    def representation_boundary(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,305,770,385,'LLM REWRITE',['Alternative language or structured expression','Text that another component can receive','The generated syntax can be inspected'],BLUE)
        panel(c,1000,305,770,385,'SPLADE-STYLE REPRESENTATION',['Predicted weights in vocabulary dimensions','Absent input terms may become active','The active weighted terms can be inspected'],TEAL,.2+.8*p)
        text(c,'The form of the retrieval input is the distinction.',960,815,43,INK,p,True,align='center',width=1700)
        self.note(c,'Both can be handed between components · No model outputs or weights are being measured here')

    def transformation_record(self,c,t,s):
        self.four(c,[('ORIGINAL REQUEST',['What did the searcher supply?','Which constraints were interpreted?'],BLUE),('TRANSFORMED INPUT',['Correction, mapping, expansion or decomposition','What text, expression or weights resulted?'],TEAL),('SELECTED ROUTE',['Which component received which input?','Which retrieval paths actually ran?'],RED),('LATER PASS',['Which earlier results informed a new query?','Retain that ranking and the feedback decision'],BLUE)],self.r(t,s))
        self.note(c,'These operations can coexist in a prescribed workflow · The interface label does not expose the procedure')
    def imagined_hook(self,c,t,s):
        import textwrap
        p=self.r(t,s)
        pill(c,'ILLUSTRATIVE GENERATED TEXT · NO IDENTIFIED STUDY',200,265,RED,size=26)
        rect(c,160,335,1600,330,PAPER)
        quote=textwrap.wrap(GENERATED_TEXT,width=74)
        rows(c,quote,215,420,34,INK,step=66,width=1490,serif=True)
        text(c,'A retrieval aid can be useful without being evidence.',960,805,44,RED,p,True,align='center',width=1700)
        self.note(c,'Source hypothetical wording · It describes neither an identified study nor an established finding')

    def query2doc_path(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,285,650,225,'ORIGINAL QUESTION',['Does open access increase citations?'],BLUE)
        panel(c,150,595,650,225,'GENERATED LANGUAGE',['A pseudo-document supplies vocabulary'],TEAL)
        arrow(c,830,410,960,520,BLUE,p,stroke=3)
        arrow(c,830,705,960,575,TEAL,p,stroke=3)
        panel(c,1010,330,760,395,'EXPANDED QUERY',['Original wording + generated language','BM25 is one possible receiving retriever','Dense retrieval is also possible'],RED,.2+.8*p)
        self.note(c,'Query2doc uses generated language to expand the query · This diagram follows the lexical route, not a measured search')

    def hyde_path(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('GENERATE',['A hypothetical relevant document','An imagined retrieval aid'],BLUE),('ENCODE',['Dense-encode that generated text','Use the resulting vector as a pivot'],TEAL),('RETRIEVE',['Compare with stored document vectors','Read and assess real indexed sources'],RED)]):
            x=130+i*570
            panel(c,x,330,520,350,title,body,color,1 if i==0 else .3+.7*p)
            if i<2:arrow(c,x+532,505,x+558,505,color,p)
        text(c,'The generated document’s vector guides the search.',960,815,42,INK,p,True,align='center',width=1700)
        self.note(c,'HyDE = Hypothetical Document Embeddings · The generated document is neither a verified source nor a final answer')

    def unsupported_assumptions(self,c,t,s):
        self.four(c,[('GENERATED DETAILS',['Compare open and subscription articles','Account for discipline and publication year'],BLUE),('POSSIBLE RETRIEVAL EFFECT',['Steer vocabulary or study design','Import assumptions the searcher did not choose'],TEAL),('NOT ESTABLISHED',['That an identified study used these methods','That any generated detail is true'],RED),('RECORD AND ASSESS',['Retain the exact generated retrieval aid','Read and evaluate actual retrieved sources'],BLUE)],self.r(t,s))
        self.note(c,'Real indexed results do not retroactively validate invented text')

    def product_arrangements(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('EBSCOHOST / EDS',['AI parses keyword and noun phrases','Established search engine receives them','Public page does not identify','the parser as an LLM'],BLUE),('WOS SMART SEARCH',['Structured query parsing','Boolean keyword and vector document paths','Interpretation and retrieval','are different operations'],TEAL),('PRIMO VE NDE',['GPT-4.1 Mini interpretation','Generative Boolean construction','Advanced Search receives the expression','Inspect and edit the generated query'],RED)]):
            panel(c,130+i*570,295,520,430,title,body,color,1 if i==0 else .3+.7*p)
        self.note(c,'Pinned source documentation accounts · Shared AI-assisted interface language does not identify a common architecture')

    def partial_constraints(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,305,770,395,'PRIMO VE NDE NATURAL LANGUAGE SEARCH',['Recognises a defined list of fields and facets','Documented failures in author detection','Cases of unintended OR relationships','Inspect the expression that was generated'],BLUE)
        panel(c,1000,305,770,395,'WEB OF SCIENCE RESEARCH ASSISTANT',['Some institution, geography and date patterns','Other supported document-request patterns','Complex field-tagged Boolean queries','are listed as unsupported in its guidance'],TEAL,.2+.8*p)
        text(c,'A supported pattern is not the full advanced-search language.',960,815,37,INK,p,True,align='center',width=1700)
        self.note(c,'Keep Research Assistant distinct from Smart Search · No new product test or complete support inventory is claimed')

    def inferred_or_manual(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,300,770,405,'PRIMO RESEARCH ASSISTANT · AUTOMATIC',['Limited supported refinements','Availability, books or journal articles','Peer-reviewed material','Supported date ranges'],BLUE)
        panel(c,1000,300,770,405,'USER CHANGES A REFINEMENT',['That field switches to manual handling','It is no longer automatically inferred','Test ambiguous and unsupported limits','Check whether the generated filter is visible'],TEAL,.2+.8*p)
        self.note(c,'A filter inferred from the question and a filter selected explicitly need separate checks')

    def search_record(self,c,t,s):
        self.four(c,[('SEARCHER INPUT',['Original question, seed, relationship or brief','The actual need and constraints'],BLUE),('RETRIEVAL INPUTS',['Generated text and structured expressions','Inferred and manually selected filters'],TEAL),('EXECUTED PROCEDURE',['Chosen routes and retrieval passes','Intermediate results used for feedback'],RED),('NEXT ACTION',['Who chose what happened next?','Chapter 12 examines control during search'],BLUE)],self.r(t,s))
        self.note(c,'Understanding interprets · Transformation changes inputs · Control chooses their use · Preserve what actually happened')

    def poster(self,c):
        c.clear(skia.Color(*CREAM))
        text(c,'HOW SEARCH DECIDES WHAT YOU SEE',130,130,27,MUTED,bold=True)
        text(c,f"CHAPTER 11 · FILM {self.script['episode_number']:02d}",130,220,30,self.accent,bold=True)
        titles={1:['What if your query','is a paper?'],2:['Who changed','your question?'],3:['The paper that','never existed.']}
        rows(c,titles[self.script['episode_number']],130,405,88,INK,bold=True,step=132,width=1190)
        text(c,self.script['subtitle'],130,750,31,MUTED,width=1130)
        for i,label in enumerate(('Q','?','↗')):
            self.record(c,1450+i*75,340+i*135,180,230,label,self.accent)
        text(c,'Original animated investigation · Narrated and captioned',130,890,26,self.accent)
        text(c,'Adapted from Aaron Tay · CC BY 4.0',130,1000,23,MUTED)
