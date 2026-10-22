"""Original Chapter 12 experiments, drawn with the established paper-and-ink primitives."""
from __future__ import annotations

import importlib.util
import math
from pathlib import Path
import re
import sys

import skia

ART_PATH = Path(__file__).parents[1]/"pre-chapter-1-investigations"/"scenes.py"
spec = importlib.util.spec_from_file_location("chapter12_paper_art", ART_PATH)
art = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = art
spec.loader.exec_module(art)
W, H = art.W, art.H
CREAM, PAPER, INK, MUTED, RULE = art.CREAM, art.PAPER, art.INK, art.MUTED, art.RULE
RED, BLUE, TEAL, GOLD = art.RED, art.BLUE, art.TEAL, art.GOLD
text, rows, rect, line, arrow = art.text, art.rows, art.rect, art.line, art.arrow
circle, pill, card, panel = art.circle, art.pill, art.card, art.panel
ease, clamp, lerp, font = art.ease, art.clamp, art.lerp, art.font

from facts import TOY_RELATED, TOY_REFERENCES, AUTISM_VARIANTS, AUTISM_BROADENING, AUTISM_DATABASES, uncited_candidates, check_examples
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
        text(c, f"CHAPTER 12   /   FILM {self.script['episode_number']:02d}", 1820, 63, 21, self.accent, bold=True, align="right")
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
        text(c, "Adapted from Aaron Tay · Chapter 12 · CC BY 4.0", 100, 1042, 19, MUTED)
        text(c, "Original illustrations · Synthetic narration", 1820, 1042, 19, MUTED, align="right")
        rect(c, 100, 1064, 1720, 4, RULE, radius=0)
        rect(c, 100, 1064, 1720*clamp(t/self.tl["duration"]), 4, self.accent, radius=0)

    def note(self, c, message="Chapter 12 teaching illustration · Control selects a sequence within available actions, sources and limits"):
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

    def control_hook(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('SEARCH ONCE',['Produce an initial ranking','The returned evidence can vary'],BLUE),('CHANGE THE QUERY',['Use top-result terms','The second query can vary too'],TEAL),('SEARCH AGAIN',['The next action was prescribed','A fixed two-pass sequence'],RED)]):
            x=130+i*570
            panel(c,x,330,520,350,title,body,color,1 if i==0 else .3+.7*p)
            if i<2:arrow(c,x+532,505,x+558,505,color,p)
        text(c,'Result-dependent content can live inside fixed control.',960,815,41,INK,p,True,align='center',width=1700)
        self.note(c,'Two-pass PRF example · Changing query content does not establish who selected the next action')

    def three_controls(self,c,t,s):
        self.plot(c,'control-arrangements')
        self.note(c,'The tools can be predefined in all three cases · Ask how the sequence of actions is selected')

    def harness_and_brief(self,c,t,s):
        self.four(c,[('TASK BRIEF',['Scope, criteria, sources and coverage','Stopping conditions and required record'],BLUE),('CALLABLE ACTIONS',['Search, fetch references, filter, rerank','The operations a controller may invoke'],TEAL),('HARNESS LIMITS',['Reachable sources, authentication, budgets','Allowed rounds and other constraints'],RED),('CONTROL WITHIN THOSE LIMITS',['Choose among available operations','Reasoning cannot supply an absent tool'],BLUE)],self.r(t,s))
        self.note(c,'A tool here means a specific callable operation, not the entire product a library licenses')

    def output_separate(self,c,t,s):
        self.plot(c,'output-patterns')
        self.note(c,'Agentic RAG chooses retrieval actions towards generation · Agentic search can end with records and no generated prose')

    def retrieval_axes(self,c,t,s):
        self.plot(c,'independent-properties')
        self.note(c,'Choosing when to run BM25, ANN or a reranker does not change that component’s underlying scoring or comparison rule')

    def mode_evidence(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('ASTA FIND PAPER',['Semi-rigid predefined flow','Model decisions at key points','Described near adaptive control'],BLUE),('UNDERMIND ORIGINAL',['Original deep-search mode','Predefined adaptive structure','Model choices within its layout'],TEAL),('UNDERMIND PROJECTS',['A different mode from the same vendor','Account describes dynamic tool chaining','Assess this mode’s actual arrangement'],RED)]):
            panel(c,130+i*570,310,520,390,title,body,color,1 if i==0 else .3+.7*p)
        self.note(c,'Chapter’s April 2026 comparison · Dated reference points along a continuum, not new tests or a vendor league table')

    def documentation_gate(self,c,t,s):
        self.four(c,[('THE APRIL 2026 LABEL',['Web of Science Research Assistant','A post used “fully agentic”'],BLUE),('THE DESCRIBED OPERATION',['Automatically choose among task routes','Compatible with adaptive control'],TEAL),('WHAT THE POST DOES NOT SETTLE',['Can it compose a novel action sequence?','Document that uncertainty'],RED),('A CONCRETE USER CONTROL',['Review and approve strategy before retrieval','Executed query returned in Advanced Search syntax'],BLUE)],self.r(t,s))
        self.note(c,'Source documentation account · Prior strategy approval is distinct from stopping an ongoing search')

    def choose_for_task(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,305,770,390,'KNOWN PROCEDURE',['A sound fixed or adaptive workflow','Often a better cost/reproducibility bargain','Record the prescribed steps and branches'],BLUE)
        panel(c,1000,305,770,390,'UNANTICIPATED SEQUENCE',['Agentic control can attempt a new sequence','Within available actions and sources','More latency, tokens and path variation'],TEAL,.2+.8*p)
        text(c,'Choose the control arrangement for the actual task.',960,815,42,INK,p,True,align='center',width=1700)
        self.note(c,'Qualitative trade-off from the chapter, not a timing benchmark · More agency is not automatically better')

    def uncited_hook(self,c,t,s):
        p=self.r(t,s)
        for x,title,color in [(140,'RELATED CANDIDATES',BLUE),(745,'ALREADY CITED',RED),(1350,'SET DIFFERENCE',TEAL)]:
            text(c,title,x+215,305,27,color,bold=True,align='center',width=460)
        for i,label in enumerate(TOY_RELATED):
            self.record(c,170+(i%2)*215,355+(i//2)*190,165,160,label,BLUE)
        for i,label in enumerate(TOY_REFERENCES):
            self.record(c,795,355+i*190,220,160,label,RED)
        for i,label in enumerate(uncited_candidates()):
            self.record(c,1400,355+i*190,220,160,label,TEAL,p)
        text(c,'−',675,535,65,RED,bold=True,align='center')
        arrow(c,1160,510,1290,510,TEAL,p)
        text(c,'B and D still need relevance, timing and identity checks.',960,815,36,INK,p,True,align='center',width=1650)
        self.note(c,'Invented identity example · Set difference yields candidates to check, not verified citation omissions')

    def dated_probe(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('ASTA',['Looked up the target article','Stopped at that step','The requested comparison was absent'],BLUE),('CONSENSUS',['Returned already cited papers','Despite four subagents','More parallel work did not ensure comparison'],RED),('SCISPACE',['Extracted references and compared','Most suggestions were uncited','Metadata failures; completion unclear'],TEAL)]):
            panel(c,130+i*570,310,520,395,title,body,color,1 if i==0 else .3+.7*p)
        text(c,'One task type · Source access also affected the outcome',960,805,35,INK,p,True,align='center',width=1650)
        self.note(c,'Author’s December 2025 probe · Not new tests, a general product ranking or an isolated diagnosis of failure')

    def available_menu(self,c,t,s):
        self.four(c,[('EXECUTED TRACE',['The actions actually taken','Intermediate results and observations'],BLUE),('AVAILABLE MENU',['The operations that could have been called','Including options never chosen'],TEAL),('REACHABLE SOURCES',['Full text, metadata and references','Access can constrain the possible sequence'],RED),('MCP DESCRIBES OPERATIONS',['Callable purpose, inputs and outputs','Retrieval algorithms remain separate'],BLUE)],self.r(t,s))
        self.note(c,'A trace is evidence of one executed path · It does not establish every available action')

    def endpoint_boundaries(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,290,770,430,'WILEY AI GATEWAY',['Relevant full-text chunks','Paper metadata','A specific exposed service','Within authentication and entitlements'],BLUE)
        panel(c,1000,290,770,430,'SCITE TOOLS / SEARCH API',['Documented operations and filters','Web-interface ranking parity undocumented','Assistant not offered through MCP','Do not infer every product feature is exposed'],TEAL,.2+.8*p)
        text(c,'The controller selects calls; the service defines their boundary.',960,820,36,INK,p,True,align='center',width=1700)
        self.note(c,'Pinned documentation accounts · Scite guidance checked October 2026 · An endpoint does not bypass a subscription')

    def reinforced_omission(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('ROUND 1',['Open access and citations','Overall differences appear','Selection-bias methods absent'],BLUE),('ROUND 2',['Follow returned terms and references','More papers on the same aspect','The missing methods stay unseen'],TEAL),('ROUND 3',['Continue from the observed results','Budget is reached','Coverage has not been established'],RED)]):
            x=130+i*570
            panel(c,x,315,520,390,title,body,color,1 if i==0 else .3+.7*p)
            if i<2:arrow(c,x+532,510,x+558,510,color,p)
        text(c,'An early omission can influence the next search.',960,815,42,INK,p,True,align='center',width=1700)
        self.note(c,'Chapter’s hypothetical trajectory · Recorded actions and observations, not private model reasoning')

    def repairing_the_gap(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,300,770,400,'AN ALTERNATIVE SECOND ACTION',['Open access + citation advantage','Explicitly add selection-bias methods','A brief, librarian or controller can prompt it'],BLUE)
        panel(c,1000,300,770,400,'SUPPOSE NEW METHODS PAPERS RETURN',['New candidates enter the cumulative pool','Later actions can use the new evidence','Neither the action nor success is guaranteed'],TEAL,.2+.8*p)
        arrow(c,930,505,990,505,TEAL,p)
        text(c,'Different possible trajectories can expose different aspects.',960,815,38,INK,p,True,align='center',width=1700)
        self.note(c,'Hypothetical alternative · Citation searching does not always remain trapped in one aspect')

    def stopping_boundary(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('PROCEDURE ENDS',['The prescribed steps are complete','A designed endpoint','Record what those steps covered'],BLUE),('HARNESS OR USER STOPS',['Round limit or budget reached','Or the user interrupts','Record the imposed boundary'],TEAL),('MODEL DECIDES ENOUGH',['Observed evidence seems sufficient','Applies a relevance criterion','Unseen evidence remains unknown'],RED)]):
            panel(c,130+i*570,300,520,410,title,body,color,1 if i==0 else .3+.7*p)
        text(c,'Record the stopping condition. It does not prove completeness.',960,815,38,INK,p,True,align='center',width=1700)
        self.note(c,'A strategy approval before retrieval is a separate control · Two runs can follow different paths and stop differently')

    def trace_and_cost(self,c,t,s):
        self.plot(c,'loop-boundaries')
        self.note(c,'More rounds add latency and tokens · Assess recovered evidence and unexamined gaps, not just report fluency')

    def zero_hook(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,310,770,390,'DATABASE FOR AUTISM RESEARCH',['Catalogue query: autism','Returned database records: zero','What observation should guide the next move?'],BLUE)
        panel(c,1000,310,770,390,'LOOK FOR SUBJECT COVERAGE',['Broaden to psychology, medicine,','education and disability','A database need not be named after the topic'],TEAL,.15+.85*p)
        arrow(c,930,505,990,505,TEAL,p)
        text(c,'The failed query can inform another action.',960,815,42,INK,p,True,align='center',width=1700)
        self.note(c,'Selected source example · A database for a subject need not have that subject in its name')

    def selected_demonstration(self,c,t,s):
        p=self.r(t,s)
        for i,(title,body,color) in enumerate([('2023 LOGS',['Database queries with zero results','The original failures','Not a sample of all searching'],BLUE),('SELECTED REPLAYS',['A chosen set of examples','Request a database for each topic','Library Primo index through MCP'],TEAL),('JUNE 2026 DEMONSTRATION',['Newer models try the older queries','Exploratory failure recovery','No measured general success rate'],RED)]):
            x=130+i*570
            panel(c,x,310,520,400,title,body,color,1 if i==0 else .3+.7*p)
            if i<2:arrow(c,x+532,510,x+558,510,color,p)
        text(c,'Selection and elapsed time limit the comparison.',960,815,40,INK,p,True,align='center',width=1700)
        self.note(c,'Selected rather than sampled · No controlled benchmark or evidence of superiority over human searchers')

    def one_shot_synonyms(self,c,t,s):
        p=self.r(t,s)
        text(c,'ONE GENERATED OR EXPRESSION · SAME INDEX',960,265,28,BLUE,bold=True,align='center')
        for i,label in enumerate(AUTISM_VARIANTS):
            x=160+(i%2)*845;y=305+(i//2)*125
            rect(c,x,y,760,95,PAPER,1,5)
            text(c,label,x+380,y+58,29,INK,bold=True,align='center',width=700)
            if i%2==0:text(c,'OR',965,y+58,22,MUTED,bold=True,align='center')
        rect(c,500,730,920,100,PAPER,.2+.8*p,6)
        text(c,'Reported result: still zero',960,793,40,RED,p,True,align='center',width=860)
        self.note(c,'Source’s six terms from single-pass Natural Language Search · One OR expression, not six independent calls')

    def broader_subjects(self,c,t,s):
        p=self.r(t,s)
        text(c,'BROADER SUBJECT AREAS',550,290,28,BLUE,bold=True,align='center')
        for i,label in enumerate(AUTISM_BROADENING):
            rect(c,190,325+i*115,720,85,PAPER,1,5)
            text(c,label,550,380+i*115,34,BLUE,bold=True,align='center',width=650)
        arrow(c,930,525,1020,525,TEAL,p)
        text(c,'REPORTED DATABASE NAMES',1435,290,28,TEAL,p,True,align='center',width=730)
        for i,label in enumerate(AUTISM_DATABASES):
            rect(c,1070,370+i*140,730,100,PAPER,p,5)
            text(c,label,1435,434+i*140,34,TEAL,p,True,align='center',width=670)
        self.note(c,'Selected example in the chapter · No fresh catalogue query was run for this film')

    def other_recoveries(self,c,t,s):
        self.four(c,[('COST OF LIVING',['Inflation, household expenditure, consumer prices','Then search for economics databases'],BLUE),('ROLEX WATCHES',['Luxury goods','Reported names: Statista and Passport'],TEAL),('STATIS',['Resolve the typo to Statista','A selected recovery example'],RED),('REFINITUV',['Reached the name LSEG','Rebrand postdated the original query'],BLUE)],self.r(t,s))
        self.note(c,'Selected source cases · Newer knowledge and other setup changes complicate attribution to the loop alone')

    def limits_of_comparison(self,c,t,s):
        self.plot(c,'catalogue-comparison')
        self.note(c,'Holdings CSV and a smaller model also worked for selected cases · These comparisons do not isolate one cause')

    def local_knowledge(self,c,t,s):
        p=self.r(t,s)
        panel(c,150,295,770,430,'PUBLIC SUBJECT KNOWLEDGE',['Familiar database names and disciplines','Useful broader concepts','Less help for obscure or new resources','Cannot establish local current access'],BLUE)
        panel(c,1000,295,770,430,'AUTHORITATIVE LIBRARY INFORMATION',['Current coverage and field quirks','Embargo dates and institutional entitlements','Newly licensed databases','Specific variables, companies and years'],TEAL,.2+.8*p)
        text(c,'A recovered name still needs local verification.',960,820,40,INK,p,True,align='center',width=1700)
        self.note(c,'Recovery changes the process · It does not make current coverage or licensing safe to infer from public-web knowledge')

    def recovery_evaluation(self,c,t,s):
        self.four(c,[('FAILED QUERY',['Preserve the exact input','Record the zero-result observation'],BLUE),('NEXT ACTION',['Record the reformulation or new operation','Who selected it, and within which limits?'],TEAL),('RETURNED EVIDENCE',['Inspect the actual records','Verify current local coverage and access'],RED),('STOPPING AND DIAGNOSIS',['Record why the process ended','Where did this particular search go wrong?'],BLUE)],self.r(t,s))
        self.note(c,'Useful retries can be fixed, adaptive or agentic · Evaluate the whole process for the actual task')

    def poster(self,c):
        c.clear(skia.Color(*CREAM))
        text(c,'HOW SEARCH DECIDES WHAT YOU SEE',130,130,27,MUTED,bold=True)
        text(c,f"CHAPTER 12 · FILM {self.script['episode_number']:02d}",130,220,30,self.accent,bold=True)
        titles={1:['Who chooses','the next search?'],2:['The blind spot that','survives the loop.'],3:['When zero results','become a clue.']}
        rows(c,titles[self.script['episode_number']],130,405,88,INK,bold=True,step=132,width=1190)
        text(c,self.script['subtitle'],130,750,31,MUTED,width=1130)
        for i,label in enumerate(('Q','0','↗')):
            self.record(c,1450+i*75,340+i*135,180,230,label,self.accent)
        text(c,'Original animated investigation · Narrated and captioned',130,890,26,self.accent)
        text(c,'Adapted from Aaron Tay · CC BY 4.0',130,1000,23,MUTED)
