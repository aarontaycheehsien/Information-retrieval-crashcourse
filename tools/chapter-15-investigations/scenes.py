"""Original Chapter 15 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter15_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import check_examples, ORIGINAL_INPUT, TRANSFORMED_QUERY, RATIONALE, CANDIDATE_RANK, CANDIDATE_COUNT, FINAL_RANK, DISPLAY_K, VENDOR_GROUPS
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
        text(c, f"CHAPTER 15   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 15 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Chapter 15 teaching illustration · Source-grounded teaching illustration · Separate observed evidence, vendor documentation and unknowns"):
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

    def same_question_hook(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,300,770,405,'THE QUESTION IS SAVED',['The original words can be identical','A later run starts with the same text','Did it perform the same search?'],BLUE)
        panel(c,1000,300,770,405,'WHAT ELSE COULD HAVE CHANGED?',['Generated inputs, filters and routes','Coverage, indexing and model versions','Ranking configuration and control'],TEAL,.2+.8*p)
        text(c,'Preserve enough to rerun or compare the actual procedure.',960,820,39,INK,p,True,align='center',width=1700)
        self.note(c,'Conditional reproducibility · Possible changes, not an observed before/after test · No method freezes a live database forever')

    def four_record_areas(self,c,t,s):
        self.plot(c,'recording-layers')
        self.note(c,'Document what the system actually searched · Internal versions and candidate budgets may require vendor disclosure')

    def lexical_repeatability(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,295,770,425,'STRICT BOOLEAN',['Same records, indexing and analyser','Same query interpretation and conditions','Record query, platform, fields and limits','Also vocabulary version, date and count'],BLUE)
        panel(c,1000,295,770,425,'RANKED LEXICAL / BM25',['Add analysis, rewriting and field weights','Ranking configuration, sort and depth','New records change rarity and length statistics','Same formula does not freeze the ranking'],TEAL,.2+.8*p)
        text(c,'An unchanged query can meet a changed indexed system.',960,825,39,INK,p,True,align='center',width=1700)
        self.note(c,'Source reporting conditions · Eligibility and ranking are separate repeatability questions')

    def dense_repeatability(self,c,t,s):
        self.four(c,[('FIXED REPRESENTATION',['Encoder, tokeniser and embedded content','Indexed units, chunking and stored vectors'],BLUE),('FIXED COMPARISON',['Similarity function and exact procedure','Filters, depth or threshold'],TEAL),('APPROXIMATE SEARCH',['Construction and ANN settings matter','Candidates near a boundary can change'],RED),('SEPARATE THE SOURCE OF VARIATION',['Dense retrieval is not inherently random','Query generation is a different component'],BLUE)],self.r(t,s))
        self.note(c,'With the listed fixed conditions, dense scores can be repeatable · Do not treat every pipeline variation as randomness in a vector')

    def token_level_records(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,295,770,425,'LEARNT SPARSE',['Generated terms and weights where exposed','Model, tokeniser, index and scoring versions','Retrieval depth','Typed words alone omit model expansions'],BLUE)
        panel(c,1000,295,770,425,'LATE INTERACTION',['Query/document token alignments','Model, indexed units and compression version','Similarity, MaxSim, pruning / ANN and depth','Alignments do not make vectors portable'],TEAL,.2+.8*p)
        text(c,'Save the inspectable evidence with its component settings.',960,825,39,INK,p,True,align='center',width=1700)
        self.note(c,'Table 15.2 reference summary · Visible terms and alignments expose useful layers, not a complete model decision')

    def rewriting_variation(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('SAVE THE GENERATED INPUT',['Exact Boolean, expansions or subqueries','Hypothetical text and inferred filters','Route actually used'],BLUE),('SAVE THE GENERATION SETTINGS',['Prompt / template and parser version','Model version and sampling settings','Seed if exposed'],TEAL),('ASK WHAT A RERUN DOES',['Reuse the saved transformation?','Or generate a new transformation?','Temperature zero is not a system guarantee'],RED)]):
            panel(c,130+i*570,305,520,405,title,body,color,1 if i==0 else .25+.75*p)
        text(c,'Identical output needs an actual tested system guarantee.',960,820,38,INK,p,True,align='center',width=1700)
        self.note(c,'Sampling may vary deliberately; updates and infrastructure can also affect outputs · This does not mean every LLM call must vary')

    def control_trace(self,c,t,s):
        self.four(c,[('FIXED WORKFLOW',['Record the prescribed rules and sequence','Preserve result-dependent generated inputs'],BLUE),('ADAPTIVE WORKFLOW',['Record the branch actually selected','And the rule or policy choosing it'],TEAL),('AGENTIC WORKFLOW',['Record tools, sources, queries and observations','Order, limits, stopping and final identifiers'],RED),('THE RECORD NEEDED',['Actions taken and results returned','Narrated reasoning is not a replacement'],BLUE)],self.r(t,s))
        self.note(c,'Controller model, instructions and permitted action menu belong with the run · Two runs can legitimately take different paths')

    def record_today(self,c,t,s):
        self.four(c,[('CAPTURE TODAY',['Input, product/mode and search date','Visible transformation, filters and limitations'],BLUE),('SAVE THE OUTPUT',['Count and retrieved identifiers','Raw export where possible'],TEAL),('KEEP EVIDENCE STATUS',['Observed, vendor-documented or unknown','Request unavailable versions and traces institutionally'],RED),('COMPARE LATER',['Retain strategy, platform, dates and limits','A saved record does not explain every result'],BLUE)],self.r(t,s))
        self.note(c,'Source aligns this with PRISMA-S reporting while recognising replication limits · Documentation and explanation need separate questions')

    def rationale_hook(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,295,770,425,'GENERATED RATIONALE',['“This paper closely addresses your question','about open access and citations.”','A plausible description of topical fit','Does it establish why P is at rank 3?'],BLUE)
        panel(c,1000,295,770,425,'MOCK RECORDED PATH',['Lexical candidate: rank 18 of 100','Reranked: rank 3','Display: first 10','Internal reranker details: not disclosed'],TEAL,.2+.8*p)
        text(c,'A plausible account does not fill an undisclosed scoring gap.',960,825,37,INK,p,True,align='center',width=1700)
        self.note(c,'Figure 15.1 · All paper details, inputs and ranks are hypothetical · No product trace or search run obtained for this film')

    def three_qualities(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('TRANSPARENCY',['Information about a system is exposed','A broad ranking description may qualify','But may explain little about one record'],BLUE),('INTERPRETABILITY',['Trace inclusion, exclusion and position','Follow actual evidence and stages','A rerunnable search can remain opaque'],TEAL),('UNDERSTANDABILITY',['An accurate, usable mental model','No need to inspect every weight','A detailed score view can still confuse'],RED)]):
            panel(c,130+i*570,305,520,405,title,body,color,1 if i==0 else .25+.75*p)
        text(c,'Related properties. Separate evidence for each.',960,820,42,INK,p,True,align='center',width=1700)
        self.note(c,'Source definitions · Documentation, interpretation and an understandable account are not interchangeable')

    def mock_inputs(self,c,t,s):
        p=self.r(t,s)
        text(c,'ORIGINAL INPUT',960,270,27,BLUE,bold=True,align='center')
        text(c,ORIGINAL_INPUT,960,335,43,INK,bold=True,align='center',width=1700)
        text(c,'TRANSFORMED QUERY ACTUALLY SENT',960,455,27,TEAL,p,True,align='center')
        text(c,TRANSFORMED_QUERY,960,535,52,TEAL,p,True,align='center',width=1700)
        panel(c,240,620,1440,220,'LEXICAL RETRIEVAL OVER INDEXED ABSTRACTS',['Mock evidence: P’s abstract contains “open access” and “citations”.'],BLUE,.2+.8*p)
        self.note(c,'Exact source mock expression · Recorded inputs do not by themselves prove preservation of the searcher’s full intended need')

    def mock_rank_path(self,c,t,s):
        self.plot(c,'mock-record-trace')
        self.note(c,'A real trace must derive from executed input, index, candidate and scoring paths · Generated interpretation cannot fill missing facts')

    def backward_inspection(self,c,t,s):
        p=self.r(t,s)
        text(c,'START AT DISPLAYED P · INSPECT TOWARDS THE ORIGINAL INPUT',960,260,26,BLUE,bold=True,align='center',width=1700)
        items=[('FUSION AND DISPLAY',['Deduplication, labels and snippets','What changed the visible result?'],BLUE),('SCORING AND RERANKING',['Which stage and cutoff?','Why this recorded position?'],TEAL),('MATCHED EVIDENCE',['What did the system match?','What can it faithfully expose?'],RED),('CANDIDATE SOURCE',['Which retriever and route?','Which indexed unit supplied P?'],BLUE),('TRANSFORMED QUERY',['What was actually sent onward?','Which constraints and expansions?'],TEAL),('ORIGINAL INPUT',['What did the searcher enter?','Fields, limits and filters'],RED)]
        for i,(title,body,color) in enumerate(items):
            x=140+(i%3)*570;y=300+(i//3)*280
            panel(c,x,y,500,200,title,body,color,1 if i<3 else .2+.8*p)
            if i%3<2:arrow(c,x+510,y+100,x+558,y+100,color,1 if i<3 else p)
        line(c,1795,400,1830,400,RED,p,2);line(c,1830,400,1830,540,RED,p,2)
        line(c,1830,540,390,540,RED,p,2);arrow(c,390,540,390,575,RED,p,2)
        self.note(c,'Figure 15.2 inspection order, not execution order · Where the recorded trail stops is itself useful evidence about disclosure')

    def stage_limits(self,c,t,s):
        self.plot(c,'inspection-limits')
        self.note(c,'A highlighted term, citation count, rationale or attractive snippet is not by itself proof of the cause of a final position')

    def alignment_and_agency(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,295,770,425,'SPARSE TERMS / TOKEN ALIGNMENTS',['Useful inspectable contributions','One layer of contextual model computation','Inspect candidates, fusion and reranking too','Visible pieces are not the complete decision'],BLUE)
        panel(c,1000,295,770,425,'AGENTIC ACTIONS / OBSERVATIONS',['Which tool, query, route and source?','What returned, and what happened next?','What stopping point and criterion?','Narrated reasoning does not prove causation'],TEAL,.2+.8*p)
        text(c,'Label a helpful post-hoc account as interpretation.',960,825,41,INK,p,True,align='center',width=1700)
        self.note(c,'A faithful trail is derived from actual execution evidence · The source’s mock trace illustrates the requirement without testing a product')

    def evidence_status(self,c,t,s):
        self.plot(c,'evidence-status')
        self.note(c,'A reproducible search can remain opaque · An understandable explanation still needs saved inputs, versions and outputs to support rerunning')
    def licensing_hook(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,295,770,425,'THE LABEL ON THE QUERY BOX',['Semantic · Natural language · AI search','Does that identify the retrieval design?','What can the searcher actually start from?','Ask before comparing the interface'],BLUE)
        panel(c,1000,295,770,425,'STARTING POINTS TO INVESTIGATE',['Text, controlled fields and seed records','Citation links, judgements and API predicates','Agentic task brief plus generated queries','Can the brief and actual queries be exported?'],TEAL,.2+.8*p)
        text(c,'Nineteen source questions. Six groups. Answers to verify.',960,825,39,INK,p,True,align='center',width=1700)
        self.note(c,'Questions for procurement and local evaluation · No vendor answers, architecture claims or product comparisons invented')

    def vendor_control(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,295,770,425,'Q1 · INFER, CHANGE AND DECIDE',['Recognise fields, filters or intent','Transform inputs and select routes','Construct a query from previous results','Inspect/export transformations and feedback'],BLUE)
        panel(c,1000,295,770,425,'Q2 · WHO CONTROLS THE TRAJECTORY?',['Fixed sequence, enumerated branches,','or model-planned sequence from observations?','Which tools, sources and iteration limits?','Can the actual actions and stop be inspected?'],TEAL,.2+.8*p)
        text(c,'A model choosing a predefined branch can still be adaptive.',960,825,38,INK,p,True,align='center',width=1700)
        self.note(c,'Vendor group 1 · Distinguish interpretation, transformation and control · Ask for the mechanism and evidence')

    def vendor_architecture(self,c,t,s):
        self.four(c,[('Q3–4 · COMPONENTS AND MODEL ROLE',['Which routes, sequence and candidate cutoffs?','What job does the named neural model perform?'],BLUE),('Q5 · INDEXED UNIT',['Titles, abstracts, passages or full articles?','Later full-text fetching is a separate question'],TEAL),('Q6 · ASSEMBLING PASSAGES',['How do multiple matches from one paper combine?','Combined scores, best passage or repeated results?'],RED),('Q7 · HYBRID COMBINATION',['Where do lists fuse and reranking follow?','Can component sets, influence and limits be inspected?'],BLUE)],self.r(t,s))
        self.note(c,'Vendor group 2 · An abstract index cannot match full-text-only evidence at that retrieval stage, regardless of later fetching')

    def vendor_exactness(self,c,t,s):
        self.four(c,[('Q8 · EXACT LEXICAL ROUTE',['Identifiers, chemicals, genes and quoted phrases','Can expansion change an exact-identity task?'],BLUE),('Q9 · ANALYSIS AND TOKENISATION',['Case, punctuation, hyphens and compatible analysis','Model input units and unfamiliar-string tests'],TEAL),('Q10 · FAILURE TESTS',['Negation, exclusions and contradictory claims','Near-duplicate names and exact identifiers'],RED),('Q11 · RELEVANCE TRAINING',['Which query–record relationships were rewarded?','Adaptation to local disciplines and document types'],BLUE)],self.r(t,s))
        self.note(c,'Vendor group 3 · Attractive paraphrase demonstrations do not settle exactness, composition or training transfer')

    def vendor_audit(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('Q12 · INSPECT RESULTS',['Trace actual routes, inputs and constraints','Matched evidence, ranking and display','Distinguish trace from post-hoc account'],BLUE),('Q13 · DOCUMENT AND RERUN',['Export exact transformations and routes','Versions, dates, cutoffs and identifiers','Reuse the saved input or regenerate it?'],TEAL),('Q14 · DISCLOSE CHANGES',['Model, index and ranking updates','Notice when saved results may change','Identify the version behind a past run'],RED)]):
            panel(c,130+i*570,305,520,405,title,body,color,1 if i==0 else .25+.75*p)
        text(c,'Make later comparison possible without promising frozen results.',960,820,37,INK,p,True,align='center',width=1700)
        self.note(c,'Vendor group 4 · Auditability and repeatability require saved evidence, disclosed changes and inspectable operations')

    def vendor_continuity(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,295,770,425,'Q15 · COST AND LIMITS',['Per seat, query or token?','Rate, iteration and budget limits?','Refusal, truncation or a shallower search?','Agentic pricing and per-query consumption?'],BLUE)
        panel(c,1000,295,770,425,'Q16 · MODE RETIREMENT',['What notice before withdrawal?','Can searches, sets and traces be exported?','Which mode produced the saved run?','Explicit continuity and change arrangements?'],TEAL,.2+.8*p)
        text(c,'A licensed mode can change. Preserve what can be compared.',960,825,39,INK,p,True,align='center',width=1700)
        self.note(c,'Vendor group 5 · Source mentions renamed/distinct modes as reasons to ask · No new retirement event or pricing test claimed')

    def vendor_evaluation(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('Q17 · WHOSE EVALUATION?',['Local disciplines and vocabulary','Languages and document types','Known relevant records'],BLUE),('Q18 · WHICH FAILURES?',['Include known difficult searches','Go beyond successful demonstrations','Retain examples for investigation'],TEAL),('Q19 · ACROSS AN UPDATE?',['Rerun local tests after a change','Compare against the saved baseline','Inspect per-query regressions'],RED)]):
            panel(c,130+i*570,305,520,405,title,body,color,1 if i==0 else .25+.75*p)
        text(c,'Require the ability to test behaviour against local needs.',960,820,40,INK,p,True,align='center',width=1700)
        self.note(c,'Vendor group 6 · Connect procurement to Chapter 14’s local comparison protocol · No vendor benchmark performed here')

    def professional_requirements(self,c,t,s):
        self.four(c,[('RECORD',['Establish what was actually searched','Preserve enough to rerun or compare it later'],BLUE),('INSPECT',['Follow the executed path to a result','Keep interpretation and unknowns visible'],TEAL),('TEST LOCALLY',['Use the institution’s collections and questions','Compare changes against saved evidence'],RED),('REQUIRE IN ADVANCE',['Ask, record evidence, verify and follow up','Companion question sheet leaves answers blank'],BLUE)],self.r(t,s))
        self.note(c,'The course closes with visibility, documentation and control · Useful accountability does not require access to every model weight')

    def poster(self,c):
        c.clear(skia.Color(*CREAM))
        text(c,'HOW SEARCH DECIDES WHAT YOU SEE',130,130,27,MUTED,bold=True)
        text(c,f"CHAPTER 15 · FILM {self.script['episode_number']:02d}",130,220,30,self.accent,bold=True)
        titles={1:['Same question.','Same search?'],2:['Why is this','paper here?'],3:['What are you','actually licensing?']}
        rows(c,titles[self.script['episode_number']],130,405,88,INK,bold=True,step=132,width=1190)
        text(c,self.script['subtitle'],130,750,31,MUTED,width=1130)
        for i,label in enumerate(('Q','P','?')):
            self.record(c,1450+i*75,340+i*135,180,230,label,self.accent)
        text(c,'Original animated investigation · Narrated and captioned',130,890,26,self.accent)
        text(c,'Adapted from Aaron Tay · CC BY 4.0',130,1000,23,MUTED)
