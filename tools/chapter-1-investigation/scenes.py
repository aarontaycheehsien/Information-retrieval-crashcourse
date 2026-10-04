"""Original tabletop investigation: physical cards, evidence trails and reveals."""
from __future__ import annotations

from functools import lru_cache
import math
import os
from pathlib import Path
import re
from types import SimpleNamespace

import skia

W, H = 1920, 1080
CREAM = (238, 233, 224)
PAPER = (250, 248, 243)
INK = (37, 39, 40)
MUTED = (110, 107, 99)
RED = (180, 62, 48)
GOLD = (218, 163, 48)
TEAL = (42, 110, 105)
BLUE = (52, 87, 119)
RULE = (204, 196, 182)
FONT_DIR = Path(os.environ.get("CHAPTER_FONT_DIR", "C:/Windows/Fonts"))


def clamp(x):
    return min(1., max(0., x))


def ease(x):
    x = clamp(x)
    return x*x*(3-2*x)


def mix(a, b, p):
    return a+(b-a)*p


def paint(rgb, alpha=1., stroke=None):
    p = skia.Paint(AntiAlias=True, Color=skia.Color(*rgb, round(clamp(alpha)*255)))
    if stroke is not None:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
    return p


@lru_cache(maxsize=None)
def font(size, bold=False, mono=False):
    name = "consola.ttf" if mono else "segoeuib.ttf" if bold else "segoeui.ttf"
    path = FONT_DIR / name
    assert path.is_file(), f"Missing local font: {path}"
    f = skia.Font(skia.Typeface.MakeFromFile(str(path)), size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def text(c, s, x, y, size=34, rgb=INK, alpha=1, bold=False, mono=False, align="left", width=None):
    if alpha <= .002:
        return
    f = font(size, bold, mono)
    if width is not None and f.measureText(s)>width:
        f = font(size*width/f.measureText(s), bold, mono)
    w = f.measureText(s)
    start = x-w/2 if align=="center" else x-w if align=="right" else x
    assert -1 <= start and start+w <= W+1, f"Text outside frame: {s}"
    assert 0 <= y-f.getSize() and y <= H, f"Text outside frame vertically: {s}"
    c.drawString(s, start, y, f, paint(rgb, alpha))


def lines(c, rows, x, y, size=34, rgb=INK, alpha=1, step=None, **kwargs):
    for i, row in enumerate(rows):
        text(c, row, x, y+i*(step or size*1.35), size, rgb, alpha, **kwargs)


def rect(c, x, y, w, h, rgb=PAPER, alpha=1, radius=8, stroke=None):
    c.drawRoundRect(skia.Rect.MakeXYWH(x,y,w,h),radius,radius,paint(rgb,alpha,stroke))


def line(c, x, y, xx, yy, rgb=RULE, alpha=1, stroke=2):
    c.drawLine(x,y,xx,yy,paint(rgb,alpha,stroke))


def arrow(c, x, y, xx, yy, rgb=RED, alpha=1, stroke=3):
    line(c,x,y,xx,yy,rgb,alpha,stroke)
    angle=math.atan2(yy-y,xx-x)
    for delta in [-.5,.5]:
        line(c,xx,yy,xx-16*math.cos(angle+delta),yy-16*math.sin(angle+delta),rgb,alpha,stroke)


def pill(c, label, x, y, color=RED, alpha=1, size=23):
    w = font(size,True).measureText(label)+32
    rect(c,x,y,w,44,color,alpha,4)
    text(c,label,x+16,y+31,size,PAPER,alpha,True)


def card(c, x, y, w=172, h=220, number=None, color=INK, alpha=1, angle=0, rows=None):
    c.save()
    c.rotate(angle,x+w/2,y+h/2)
    rect(c,x+8,y+10,w,h,INK,.12*alpha,5)
    rect(c,x,y,w,h,PAPER,alpha,5)
    rect(c,x,y,w,7,color,alpha,1)
    rect(c,x,y,w,h,RULE,alpha,5,1)
    if number is not None:
        text(c,str(number),x+16,y+42,min(28,w*.23),color,alpha,True)
    for i in range(4):
        line(c,x+w*.12,y+h*(.43+i*.1),x+w*(.84 if i%2==0 else .66),y+h*(.43+i*.1),RULE,alpha,max(1,w*.015))
    if rows:
        rect(c,x+12,y+65,w-24,h-80,PAPER,alpha,0)
        lines(c,rows,x+22,y+104,27,INK,alpha,step=39,width=w-44)
    c.restore()


def normalize(s):
    return re.sub(r"[^\w]","",s).lower()


class Film:
    def __init__(self,timeline,script):
        self.timeline,self.script=timeline,script
        self.takes={tk["id"]:tk for tk in timeline["takes"]}
        self.by_scene={s["id"]:s for s in script["scenes"]}
        self.order=list(self.by_scene)
        self.count_grid=None
        import sys
        voice=sys.modules.get("chapter_voice")
        if voice is None:
            import importlib.util
            spec=importlib.util.spec_from_file_location("investigation_caption_voice",Path(__file__).parents[1]/"pick-a-card"/"narrate.py")
            voice=importlib.util.module_from_spec(spec)
            sys.modules[spec.name]=voice
            spec.loader.exec_module(voice)
        cues=voice.captions(SimpleNamespace(takes=[SimpleNamespace(**tk) for tk in timeline["takes"]]))
        self.captions=[(cue["start"],cue["end"],cue["text"]) for cue in cues]

    def at(self,line_id,word=None,nth=0):
        tk=self.takes[line_id]
        if word is None:
            return tk["start"]
        found=[w for w in tk["words"] if normalize(w["text"])==normalize(word)]
        assert len(found)>nth, f"Missing reveal word {word} in {line_id}"
        return found[nth]["start"]

    def reveal(self,t,line_id,word=None,duration=.6,nth=0):
        return ease((t-self.at(line_id,word,nth))/duration)

    def header(self,c,scene,t):
        idx=self.order.index(scene)
        text(c,"HOW SEARCH DECIDES WHAT YOU SEE",100,64,22,MUTED,bold=True)
        text(c,f"CHAPTER 1   /   {idx+1:02d}",1820,64,22,RED,bold=True,align="right")
        line(c,100,88,1820,88)
        text(c,self.by_scene[scene]["title"],100,161,52,INK,bold=True,width=1700)
        start,end=self.timeline["scenes"][scene]
        rect(c,100,1064,1720,4,RULE,radius=0)
        rect(c,100,1064,1720*clamp(t/self.timeline["duration"]),4,RED,radius=0)
        text(c,"Aaron Tay · Chapter 1 · CC BY 4.0",100,1042,20,MUTED)
        text(c,"Original animated thought experiments",1820,1042,20,MUTED,align="right")

    def caption(self,c,t):
        for start,end,caption in self.captions:
            if start<=t<end:
                f=font(30)
                w=min(1710,f.measureText(caption)+64)
                rect(c,(W-w)/2,949,w,56,INK,.95,5)
                text(c,caption,960,988,30,PAPER,align="center",width=1650)
                break

    def frame(self,c,t):
        c.clear(skia.Color(*CREAM))
        # Quiet ruled tabletop; the art is intentionally tangible and uncluttered.
        for y in range(225,930,70):
            line(c,60,y,1860,y,RULE,.16,1)
        scene=next((s for s in self.order if self.timeline["scenes"][s][0]<=t<self.timeline["scenes"][s][1]),self.order[-1])
        self.header(c,scene,t)
        c.save()
        start,end=self.timeline["scenes"][scene]
        zoom=1+.022*ease((t-start)/(end-start))
        c.translate(960,560)
        c.scale(zoom,zoom)
        c.translate(-960,-560)
        getattr(self,scene)(c,t)
        c.restore()
        self.caption(c,t)
        start,end=self.timeline["scenes"][scene]
        fade=max(1-ease((t-start)/.25),ease((t-end+.2)/.2))
        if fade>0:
            rect(c,0,180,W,750,CREAM,fade,radius=0)

    def hook(self,c,t):
        p=self.reveal(t,"h2","sixth")
        for i in range(5):
            x=220+i*255
            card(c,x,350,195,270,i+1,TEAL,angle=(-2,1,-1,2,0)[i])
            pill(c,"REAL",x+30,650,TEAL)
        card(c,1470,mix(590,310,p),235,310,"?",GOLD,alpha=p,angle=-4)
        lines(c,["LANDMARK", "STUDY"],1588,mix(725,445,p),33,INK,p,bold=True,align="center")
        text(c,"ACCURATE CITATIONS",100,264,27,TEAL,bold=True)
        text(c,"COMPLETE EVIDENCE?",100,854,62,RED,self.reveal(t,"h3","incomplete"),True)
        text(c,"Illustrative records; no fabricated study titles",100,906,22,MUTED)

    def experiment(self,c,t):
        moving=self.reveal(t,"e1","thirty",2.1)
        rerank=self.reveal(t,"e2","order",2.0)
        select=self.reveal(t,"e2","five",1.0)
        rescue=self.reveal(t,"e4","No")
        labels=[("INDEX",100,430), ("30 CANDIDATES",660,570),("5 FOR THE WRITER",1370,450)]
        for label,x,w in labels:
            text(c,label,x,267,27,INK,bold=True)
            rect(c,x-15,300,w,440,RULE,radius=6,stroke=2)
        for i in range(60):
            x=110+(i%10)*38; y=327+(i//10)*63
            card(c,x,y,29,44,None,GOLD if i==47 else BLUE,alpha=.3 if i<30 else .7)
        for i in range(30):
            origin=(110+(i%10)*38,327+(i//10)*63)
            before=(675+(i%10)*51,330+(i//10)*119)
            after=(675+((i*7)%30%10)*51,330+(((i*7)%30)//10)*119)
            x=mix(origin[0],mix(before[0],after[0],rerank),moving)
            y=mix(origin[1],mix(before[1],after[1],rerank),moving)
            chosen=(i*7)%30<5
            if chosen:
                rank=(i*7)%30
                x=mix(x,1390+rank*75,select); y=mix(y,470,select)
            card(c,x,y,mix(29,43,moving),mix(44,65,moving),i+1,TEAL if chosen else BLUE)
        card(c,340,810,75,100,"48",GOLD)
        text(c,"THE LANDMARK NEVER ENTERED",460,866,30,RED,self.reveal(t,"e3","gold"),True)
        text(c,"A better order cannot add a missing candidate.",100,785,37,RED,rescue,True)
        text(c,"One round · illustrative index · exactly 30 distinct candidates · faint copies remain",100,927,21,MUTED)

    def pipeline(self,c,t):
        text(c,"PRIMO RESEARCH ASSISTANT",100,260,26,RED,bold=True)
        text(c,"Documentation checked September 2026 in Chapter 1",100,303,25,MUTED)
        steps=[("p2","converts","01","Question → OR variants","LLM writes the query",BLUE),
               ("p2","thirty","02","CDI → up to 30","First-stage retrieval",BLUE),
               ("p3","five","03","Rerank → 5 sources","Embedding comparison",TEAL),
               ("p3","overview","04","Abstracts → overview","LLM writes the answer",RED)]
        for i,(take,word,num,label,sub,col) in enumerate(steps):
            p=self.reveal(t,take,word)
            x=100+i*440
            rect(c,x,395,390,255,PAPER,p,8)
            text(c,num,x+24,451,35,col,p,True)
            text(c,label,x+24,533,31,INK,p,True,width=340)
            text(c,sub,x+24,589,25,MUTED,p,width=340)
            if i<3:
                arrow(c,x+402,518,x+430,518,col,p)
        text(c,"EVIDENCE SELECTION",100,726,35,BLUE,self.reveal(t,"p4","Retrieval"),True)
        line(c,100,752,1350,752,BLUE,self.reveal(t,"p4","Retrieval"),4)
        text(c,"WRITING",1420,726,35,RED,self.reveal(t,"p4","Generation"),True)
        lines(c,["An LLM can work on either side.","Naming the model does not locate the mechanism."],100,843,33,INK,self.reveal(t,"p4","either"))

    def diagnosis(self,c,t):
        text(c,"WHERE COULD THE PAPER DISAPPEAR?",100,272,28,RED,bold=True)
        labels=["Index coverage","Query expression","Top-30 boundary","Selection to five","Writer omission"]
        starts=[self.at("d2","index"),self.at("d2","query"),self.at("d2","thirty"),self.at("d2","five"),self.at("d3","writer")]
        for i,(label,start) in enumerate(zip(labels,starts)):
            p=ease((t-start)/.6)
            x=100+i*348
            rect(c,x,362,312,206,PAPER,p)
            c.drawCircle(x+46,409,20,paint(RED,p,3))
            text(c,"?",x+46,419,27,RED,p,True,align="center")
            text(c,label,x+23,505,29,INK,p,True,width=270)
            if i<4: arrow(c,x+319,462,x+343,462,RED,p)
        rect(c,100,654,1720,240,INK,self.reveal(t,"d3","Inspect"))
        lines(c,["FIRST: INSPECT THE SUPPLIED WORKING SET", "Was the paper given to the writer?", "A new direct search tests availability, not the original path."],136,712,34,PAPER,self.reveal(t,"d3","Inspect"),step=65)

    def need(self,c,t):
        rect(c,100,302,720,167,PAPER)
        text(c,"WHAT YOU TYPED",130,346,24,MUTED,bold=True)
        text(c,"AI academic libraries",130,422,52,INK,bold=True,width=650)
        arrow(c,850,390,1015,390,RED)
        text(c,"WHAT YOU NEED",1070,278,27,RED,bold=True)
        items=[("empirical","Empirical studies"),("four","Published since 2024"),("academic","Academic libraries"),("implementing","Implementing generative AI"),("support","Services for research support")]
        for i,(word,label) in enumerate(items):
            p=self.reveal(t,"n2",word)
            rect(c,1050,304+i*94,740,76,PAPER,p)
            text(c,label,1080,355+i*94,34,INK,p,bold=True)
        lines(c,["The system observes", "your representation.", "The fuller purpose is yours."],100,654,43,RED,self.reveal(t,"n3","representation"),bold=True,step=65)

    def contrast(self,c,t):
        text(c,"QUERY:  AI academic libraries",100,257,31,MUTED,bold=True)
        if t>=self.at("c3"):
            c.drawCircle(770,567,246,paint(RED,.10))
            c.drawCircle(770,567,246,paint(RED,1,4))
            c.drawCircle(1160,567,246,paint(TEAL,.10))
            c.drawCircle(1160,567,246,paint(TEAL,1,4))
            text(c,"MATCHES QUERY",585,303,35,RED,bold=True)
            text(c,"MEETS NEED",1070,303,35,TEAL,bold=True)
            card(c,610,504,98,134,"A",RED)
            card(c,1230,504,98,134,"B",TEAL)
            text(c,"Neither set contains the other.",960,868,44,INK,bold=True,align="center")
            text(c,"A match supplies evidence about relevance; usefulness requires judgement.",100,920,26,MUTED)
            return
        card(c,180,319,675,443,"A",RED,angle=-1)
        card(c,1030,319,675,443,"B",TEAL,angle=1)
        rect(c,195,399,635,328,PAPER)
        rect(c,1050,399,635,328,PAPER)
        lines(c,["AI · academic · libraries", "Opinion piece", "2019", "3 exact query-word matches"],226,453,35,INK,step=68,bold=True,width=570)
        p=self.reveal(t,"c2")
        lines(c,["Large language models", "Research consultation", "University library", "Implementation study · 2025"],1080,453,35,INK,p,step=68,bold=True,width=570)
        p=self.reveal(t,"c2","need")
        pill(c,"MATCHES WORDS; FAILS REQUIREMENTS",180,817,RED,p,23)
        pill(c,"MAY MEET THE NEED",1030,817,TEAL,p,23)
        text(c,"Illustrative records; B's design and context still require human assessment",100,917,22,MUTED)

    def lenses(self,c,t):
        entries=[("computed","System / algorithmic","Computed match",BLUE),
                 ("topical","Topical","About the subject",TEAL),
                 ("learns","Cognitive","What someone learns",GOLD),
                 ("task","Situational","Usefulness for this task",RED)]
        for i,(word,label,sub,col) in enumerate(entries):
            p=self.reveal(t,"l1",word)
            x=100+(i%2)*880; y=305+(i//2)*229
            rect(c,x,y,840,197,PAPER,p)
            c.drawCircle(x+75,y+80,42,paint(col,p,4))
            text(c,str(i+1),x+75,y+95,43,col,p,True,align="center")
            text(c,label,x+145,y+78,35,INK,p,True)
            text(c,sub,x+145,y+140,31,MUTED,p)
        text(c,"RELEVANT TO SOMEONE, FOR SOMETHING.",100,867,49,RED,self.reveal(t,"l3","Relevant"),True,width=1720)
        text(c,"Four perspectives, not a fixed ladder",100,920,25,MUTED)

    def impossible(self,c,t):
        text(c,"MAKE A PREDICTION",100,265,28,RED,bold=True)
        rect(c,100,319,1720,121,PAPER)
        text(c,"open access citation advantage  AND  xqzblorp",132,398,44,INK,mono=True,width=1640)
        lines(c,["STRICT AND + ABSENT TERM", "Expected result:"],100,538,32,MUTED,step=55,bold=True)
        text(c,"0",100,785,190,RED,self.reveal(t,"i1","empty"),True)
        p=self.reveal(t,"i2","scite")
        rect(c,830,490,990,319,INK,p)
        lines(c,["CHAPTER'S SCITE OBSERVATION", "Useful-looking papers remain.", "Which terms were actually required?"],875,549,34,PAPER,p,step=90,bold=True,width=890)
        text(c,"An observation challenges an assumption; it does not identify an architecture.",100,901,31,RED,self.reveal(t,"i2","No"),True,width=1720)
        text(c,"xqzblorp is an illustrative invented string; this video does not rerun the search",100,931,21,MUTED)

    def window(self,c,t):
        text(c,"GOOGLE SCHOLAR · CHAPTER'S RECORDED EXAMPLE",100,257,25,RED,bold=True)
        # Exactly 9,400 equal marks; one mark denotes the 1,000-result display cap.
        if self.count_grid is None:
            surface=skia.Surface(1012,528)
            canvas=surface.getCanvas()
            canvas.clear(skia.ColorTRANSPARENT)
            for i in range(9400):
                x=2+(i%100)*10.1; y=1+(i//100)*5.6
                rect(canvas,x,y,7.4,3.9,RED if i==0 else BLUE,.95 if i==0 else .45,radius=0)
            self.count_grid=surface.makeImageSnapshot()
        c.drawImage(self.count_grid,100,334)
        line(c,101,335,1170,455,RED,stroke=2)
        rect(c,1140,342,680,430,PAPER)
        text(c,"9,400,000",1175,432,73,INK,self.reveal(t,"w1","million"),True,width=610)
        text(c,"reported matches",1175,479,28,MUTED)
        text(c,"1,000",1175,593,85,RED,self.reveal(t,"w1","thousand"),True)
        text(c,"viewable records",1175,638,28,MUTED)
        text(c,"≈ 0.0106% viewable",1175,735,37,RED,self.reveal(t,"w2"),True,width=610)
        text(c,"Each equal mark = 1,000 reported matches; 9,400 marks in total",100,898,25,MUTED)
        text(c,"Reported count ≠ proof that every match was individually scored or ranked",100,934,26,INK,self.reveal(t,"w3","alone"),True,width=1720)

    def question(self,c,t):
        text(c,"SEMANTIC SCHOLAR · OBSERVED AUGUST 2026 IN CHAPTER 1",100,256,25,RED,bold=True)
        text(c,"Is there an open access citation advantage",100,343,36,INK,bold=True)
        text(c,"13",1680,352,74,RED,self.reveal(t,"q1","thirteen"),True,align="right")
        p=self.reveal(t,"q2","Remove")
        text(c,"open access citation advantage",100,473,36,INK,p,True)
        text(c,"≈ 35,300",1680,493,74,TEAL,self.reveal(t,"q2","hundred"),True,align="right")
        # Explicit logarithmic scale: bars never imply a false linear ratio.
        lengths=[math.log10(13+1)/math.log10(35300+1),1]
        for i,(fraction,col) in enumerate(zip(lengths,[RED,TEAL])):
            y=581+i*94
            rect(c,100,y,1540*fraction,42,col,self.reveal(t,"q1" if i==0 else "q2","thirteen" if i==0 else "hundred"),radius=2)
        text(c,"Bar length: log10(count + 1)",100,758,24,MUTED)
        text(c,"≈ 2,715× AS MANY RESULTS",100,849,53,RED,self.reveal(t,"q2","counts"),True)
        text(c,"Same need · different query expression · mechanism remains open",100,920,28,INK,self.reveal(t,"q3"),True)

    def map(self,c,t):
        p=self.reveal(t,"m3","controller")
        rect(c,100,258,1720,73,INK,p)
        text(c,"CONTROLLER: CHOOSES AND SEQUENCES ACTIONS",960,307,30,PAPER,p,True,align="center")
        stages=[("transformation",["Query", "transformation"],"Rewrites the expression"),
                ("analysis",["Analysis +", "execution rules"],"Sets eligibility"),
                ("retrieval",["First-stage", "retrieval"],"Finds candidates"),
                ("fusion",["Fusion"],"Combines lists"),
                ("reranking",["Reranking"],"Reorders a shortlist"),
                ("presentation",["Presentation"],"Shows the result")]
        for i,(word,label,sub) in enumerate(stages):
            p=self.reveal(t,"m1",word)
            x=100+(i%3)*590;y=392+(i//3)*224
            rect(c,x,y,540,190,PAPER,p)
            text(c,f"{i+1:02d}",x+22,y+47,28,RED,p,True)
            lines(c,label,x+90,y+51,32,INK,p,step=39,bold=True,width=420)
            text(c,sub,x+22,y+156,25,MUTED,p,width=490)
        text(c,"A map of possible stages; no product must use all six",100,918,30,RED,self.reveal(t,"m2","every"),True)

    def matrix(self,c,t):
        cells=[(140,540,"QUICK SEARCH",BLUE),(960,540,"QUICK ANSWER",RED),
               (140,300,"ITERATIVE SEARCH",TEAL),(960,300,"DEEP RESEARCH",GOLD)]
        for x,y,label,col in cells:
            rect(c,x,y,700,205,PAPER)
            rect(c,x,y,7,205,col)
            text(c,label,x+34,y+67,37,col,bold=True,width=630)
            if y==540:
                text(c,"One retrieval pass",x+34,y+130,30,MUTED)
            else:
                text(c,"Repeated retrieval rounds",x+34,y+130,30,MUTED)
        arrow(c,100,775,1730,775,INK)
        text(c,"Ranked records",140,832,28,INK,bold=True)
        text(c,"Written answer / report",960,832,28,INK,bold=True)
        text(c,"↑ More retrieval",140,265,27,RED,bold=True)
        pill(c,"AGENCY: WHO CHOOSES THE NEXT ACTION?",140,880,INK,self.reveal(t,"x3"),26)

    def payoff(self,c,t):
        for i in range(5):
            card(c,130+i*142,329,107,148,i+1,TEAL,angle=(i%3-1)*2)
        card(c,875,300,143,199,"?",GOLD,angle=-4)
        text(c,"REAL ≠ COMPLETE",1140,429,64,RED,bold=True,width=660)
        labels=[("supplied","What was supplied?"),("selected","What was selected?"),("searched","What was searched?"),("need","Does it meet your need?")]
        for i,(word,label) in enumerate(labels):
            p=self.reveal(t,"f1",word) if word!="need" else self.reveal(t,"f1","searched")
            y=548+i*77
            c.drawCircle(140,y-11,11,paint(RED,p))
            text(c,label,177,y,42,INK,p,True)
        p=self.reveal(t,"f2")
        rect(c,1110,545,710,340,INK,p)
        lines(c,["THE RETRIEVAL", "PROBLEM", "Next: words as admission rules"],1145,620,43,PAPER,p,step=78,bold=True,width=640)
        text(c,"Adapted from Aaron Tay · How Search Decides What You See · CC BY 4.0",100,930,23,MUTED)

    def poster(self,c):
        c.clear(skia.Color(*CREAM))
        text(c,"HOW SEARCH DECIDES WHAT YOU SEE · CHAPTER 1",100,97,26,RED,bold=True)
        lines(c,["The paper", "your AI", "never saw."],100,303,130,INK,step=152,bold=True)
        for i in range(5):
            card(c,1070+(i%3)*220,320+(i//3)*270,170,230,i+1,TEAL,angle=(i-2)*3)
        card(c,1500,616,215,289,"?",GOLD,angle=-7)
        text(c,"Five real citations. One invisible problem.",100,865,46,RED,bold=True,width=1230)
        text(c,"An original experiment-led science explainer · Adapted from Aaron Tay · CC BY 4.0",100,1003,25,MUTED)
