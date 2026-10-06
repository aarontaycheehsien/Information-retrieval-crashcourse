"""Original flat cosmic illustrations, character animation and seven scene layouts."""
from __future__ import annotations

from functools import lru_cache
import math
import os
from pathlib import Path
import random

import skia

W, H = 1920, 1080
NAVY = (19, 18, 58)
PANEL = (39, 35, 85)
PURPLE = (124, 89, 229)
LILAC = (190, 171, 255)
TEAL = (86, 224, 204)
BLUE = (78, 169, 246)
YELLOW = (255, 204, 93)
CORAL = (255, 125, 122)
WHITE = (252, 246, 224)
MUTED = (191, 187, 222)
FONT_DIR = Path(os.environ.get("CHAPTER_FONT_DIR", "C:/Windows/Fonts"))


def clamp(v):
    return min(1., max(0., v))


def ease(v):
    v = clamp(v)
    return v*v*(3-2*v)


def paint(color, alpha=1, stroke=None):
    p = skia.Paint(AntiAlias=True, Color=skia.Color(*color, round(clamp(alpha)*255)))
    if stroke is not None:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        p.setStrokeCap(skia.Paint.kRound_Cap)
        p.setStrokeJoin(skia.Paint.kRound_Join)
    return p


@lru_cache(maxsize=160)
def font(size, bold=False):
    path = FONT_DIR / ("segoeuib.ttf" if bold else "segoeui.ttf")
    assert path.is_file(), f"Missing local font: {path}"
    f = skia.Font(skia.Typeface.MakeFromFile(str(path)), size)
    f.setSubpixel(True)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    return f


def text(c, value, x, y, size=34, color=WHITE, bold=False, align="left", width=None, alpha=1):
    f = font(size, bold)
    actual = f.measureText(value)
    assert width is None or actual <= width, f"Copy too wide: {value} ({actual:.0f} > {width})"
    if align == "center":
        x -= actual/2
    if align == "right":
        x -= actual
    c.drawString(value, x, y, f, paint(color, alpha))


def rows(c, values, x, y, size=72, color=WHITE, bold=True, leading=None, width=None):
    for i,value in enumerate(values):
        text(c,value,x,y+i*(leading or size*1.15),size,color,bold,width=width)


def rect(c,x,y,w,h,color=PANEL,radius=18,alpha=1,stroke=None):
    c.drawRoundRect(skia.Rect.MakeXYWH(x,y,w,h),radius,radius,paint(color,alpha,stroke))


def circle(c,x,y,r,color,alpha=1,stroke=None):
    c.drawCircle(x,y,r,paint(color,alpha,stroke))


def line(c,x,y,xx,yy,color=MUTED,stroke=4,alpha=1):
    c.drawLine(x,y,xx,yy,paint(color,alpha,stroke))


def poly(c,points,color,alpha=1,stroke=None,close=True):
    p = skia.Path()
    p.moveTo(*points[0])
    for point in points[1:]:
        p.lineTo(*point)
    if close:
        p.close()
    c.drawPath(p,paint(color,alpha,stroke))


def arrow(c,x,y,xx,yy,color=TEAL,stroke=6):
    line(c,x,y,xx,yy,color,stroke)
    a = math.atan2(yy-y,xx-x)
    for d in [-.6,.6]:
        line(c,xx,yy,xx-20*math.cos(a+d),yy-20*math.sin(a+d),color,stroke)


def star(c,x,y,r=8,color=YELLOW,alpha=1):
    poly(c,[(x,y-r),(x+r*.3,y-r*.3),(x+r,y),(x+r*.3,y+r*.3),
            (x,y+r),(x-r*.3,y+r*.3),(x-r,y),(x-r*.3,y-r*.3)],color,alpha)


def check(c,x,y,color=TEAL,scale=1):
    poly(c,[(x-10*scale,y),(x-2*scale,y+8*scale),(x+15*scale,y-12*scale)],color,stroke=5*scale,close=False)


def pill(c,label,x,y,color=TEAL,size=28):
    w = font(size,True).measureText(label)+44
    rect(c,x,y,w,size+30,color,30)
    text(c,label,x+22,y+size+7,size,NAVY,True)
    return w


def document(c,x,y,scale=1,color=WHITE,angle=0,marked=False):
    c.save()
    c.translate(x,y)
    c.rotate(angle)
    c.scale(scale,scale)
    rect(c,-44,-59,88,118,color,9)
    poly(c,[(15,-59),(44,-30),(15,-30)],NAVY,.2)
    rect(c,-26,-33,31,8,NAVY,4,.65)
    for i,w in enumerate([49,42,48,31]):
        rect(c,-26,-8+i*15,w,5,NAVY,2,.28)
    if marked:
        circle(c,27,40,15,PURPLE)
        check(c,26,42,WHITE,.65)
    c.restore()


def magnifier(c,x,y,r=46,color=TEAL):
    circle(c,x,y,r,color,stroke=12)
    line(c,x+r*.7,y+r*.7,x+r*1.55,y+r*1.55,color,14)
    line(c,x-r*.4,y-r*.3,x-r*.13,y-r*.48,WHITE,6,.65)


def robot(c,x,y,t,scale=1,excited=False):
    """An original floating library robot with spectacles and an open book."""
    c.save()
    c.translate(x,y+math.sin(t*1.7)*10*scale)
    c.scale(scale,scale)
    circle(c,0,95,110,PURPLE,.13)
    poly(c,[(-49,76),(-26,129),(0,148),(26,129),(49,76)],TEAL,.8)
    rect(c,-88,-32,176,132,PURPLE,60)
    rect(c,-101,-118,202,134,LILAC,48)
    rect(c,-83,-100,166,96,NAVY,32)
    for ex in [-39,39]:
        circle(c,ex,-54,33,TEAL,stroke=5)
        blink = .1 if t % 4.8 < .13 else 1
        rect(c,ex-7,-62,14,22*blink,WHITE,7)
    line(c,-6,-55,6,-55,TEAL,5)
    line(c,0,-118,0,-148,LILAC,6)
    circle(c,0,-156,13,YELLOW)
    line(c,-79,26,-123,70,LILAC,18)
    line(c,79,26,123,70,LILAC,18)
    poly(c,[(-98,48),(-8,68),(0,126),(-97,105)],YELLOW)
    poly(c,[(98,48),(8,68),(0,126),(97,105)],WHITE)
    line(c,0,72,0,126,NAVY,4)
    for j in range(3):
        line(c,21,80+j*11,72,69+j*11,PURPLE,4)
    if excited:
        star(c,-140,-132,15,TEAL)
        star(c,137,-95,11,YELLOW)
    c.restore()


def cover(c,x,y,scale=1,angle=0):
    c.save()
    c.translate(x,y)
    c.rotate(angle)
    c.scale(scale,scale)
    rect(c,16,22,400,558,NAVY,10,.45)
    rect(c,10,5,395,546,WHITE,8)
    rect(c,0,0,392,540,PURPLE,10)
    rect(c,0,0,22,540,(89,61,190),8)
    rect(c,27,28,339,484,NAVY,4)
    text(c,"A LIBRARIAN'S GUIDE",48,65,19,TEAL,True,width=300)
    rows(c,["How Search","Decides What","You See"],48,125,43,WHITE,leading=52,width=302)
    circle(c,207,350,96,PURPLE)
    c.drawOval(skia.Rect.MakeXYWH(69,303,276,91),paint(TEAL,stroke=4))
    c.save()
    c.translate(207,348)
    c.rotate(-18)
    document(c,0,0,.65,WHITE,marked=True)
    c.restore()
    circle(c,79,320,12,YELLOW)
    circle(c,337,371,9,CORAL)
    star(c,274,289,11,YELLOW)
    star(c,142,398,7,TEAL)
    text(c,"AARON TAY",48,479,24,WHITE,True)
    text(c,"FREE ONLINE TEXTBOOK",48,506,16,MUTED,True)
    c.restore()


def topic_icon(c,kind,x,y,t,color=TEAL,scale=1):
    c.save()
    c.translate(x,y)
    c.scale(scale,scale)
    if kind == "boolean":
        circle(c,-25,0,48,BLUE,.7)
        circle(c,25,0,48,TEAL,.7)
        # The intersection is highlighted while the two sets remain visible.
        c.save()
        p = skia.Path()
        p.addCircle(-25,0,48)
        c.clipPath(p,doAntiAlias=True)
        circle(c,25,0,48,YELLOW)
        c.restore()
    elif kind == "bm25":
        for i,height in enumerate([35,64,95,52]):
            rect(c,-68+i*38,50-height*(.85+.15*math.sin(t+i)),25,height*(.85+.15*math.sin(t+i)),[BLUE,TEAL,YELLOW,PURPLE][i],6)
        line(c,-75,57,85,57,MUTED,3)
    elif kind == "embedding":
        points = [(-58,-32),(-18,-59),(9,10),(66,-20),(44,57),(-53,46)]
        for a,b in [(0,1),(0,2),(1,3),(2,3),(2,4),(4,5),(0,5)]:
            line(c,*points[a],*points[b],color,3,.45)
        for i,(xx,yy) in enumerate(points):
            circle(c,xx,yy+math.sin(t+i)*5,10,[TEAL,YELLOW,BLUE][i%3])
    elif kind == "hybrid":
        arrow(c,-75,-47,-9,-8,BLUE,8)
        arrow(c,-75,47,-9,8,YELLOW,8)
        arrow(c,17,0,84,0,TEAL,8)
        circle(c,0,0,22,PURPLE)
    elif kind == "rerank":
        for i,w in enumerate([97,75,54]):
            rect(c,-52,-49+i*43,w,27,[TEAL,BLUE,LILAC][i],7)
            circle(c,-70,-35+i*43,8,YELLOW)
        arrow(c,75,48,75,-48,YELLOW,6)
    elif kind == "agent":
        c.drawArc(skia.Rect.MakeXYWH(-62,-62,124,124),-75,295,False,paint(TEAL,stroke=8))
        poly(c,[(57,-38),(56,-8),(32,-24)],TEAL)
        circle(c,0,0,24,PURPLE)
        for xx in [-8,8]:
            circle(c,xx,-2,4,WHITE)
    elif kind == "teach":
        rect(c,-101,-71,202,124,TEAL,10)
        rect(c,-88,-59,176,99,NAVY,6)
        topic_icon(c,"boolean",0,-10,t,scale=.48)
        line(c,-49,56,-67,88,LILAC,7)
        line(c,49,56,67,88,LILAC,7)
        circle(c,91,-63,15,YELLOW)
    elif kind == "investigate":
        document(c,-17,-5,1.1,WHITE,-7)
        magnifier(c,29,-6,40,TEAL)
    elif kind in ["vendor","evaluation"]:
        rect(c,-75,-87,150,174,WHITE,10)
        rect(c,-31,-97,62,22,PURPLE,8)
        for i in range(3):
            rect(c,-53,-49+i*45,23,23,TEAL,4)
            check(c,-43,-38+i*45,NAVY,.65)
            rect(c,-16,-42+i*45,61-i*8,7,PURPLE,3)
    elif kind == "workshop":
        poly(c,[(-90,-64),(-10,-45),(0,80),(-90,60)],YELLOW)
        poly(c,[(90,-64),(10,-45),(0,80),(90,60)],WHITE)
        for j in range(4):
            line(c,25,-22+j*20,67,-31+j*20,PURPLE,5)
        star(c,-125,-66,13,TEAL)
    c.restore()


class Film:
    def __init__(self,timeline,script):
        self.timeline = timeline
        self.script = script
        self.scene_ids = [s["id"] for s in script["scenes"]]
        self.takes = {t["id"]:t for t in timeline["takes"]}
        rng = random.Random(739)
        self.stars = [(rng.randrange(1920),rng.randrange(1080),rng.uniform(1,3),rng.random()*6.28) for _ in range(135)]
        self.paper_orbits = [(rng.uniform(1100,1690),rng.uniform(245,775),rng.uniform(.25,.47),rng.uniform(-25,25),rng.random()*6.28) for _ in range(17)]

    def at(self,line_id,word):
        normalized = lambda v: ''.join(ch for ch in v.lower() if ch.isalnum())
        hits = [w for w in self.takes[line_id]["words"] if normalized(w["text"]) == normalized(word)]
        assert hits, f"Missing timing word: {word}"
        return hits[0]["start"]

    def background(self,c,t):
        shader = skia.GradientShader.MakeLinear([(0,0),(1920,1080)],
            [skia.Color(*NAVY),skia.Color(33,24,76)])
        c.drawPaint(skia.Paint(Shader=shader))
        circle(c,1910,120,345,PURPLE,.11)
        circle(c,-130,890,370,BLUE,.065)
        c.drawOval(skia.Rect.MakeXYWH(-390,450,940,480),paint(BLUE,.11,2))
        for x,y,r,phase in self.stars:
            circle(c,(x+t*1.7)%W,y+math.sin(t*.18+phase)*3,r,WHITE,.18+.19*(1+math.sin(t*.5+phase))/2)
        star(c,1730,140,11,TEAL,.6)
        star(c,79,448,9,YELLOW,.5)

    def heading(self,c,eyebrow,headline,sub=None):
        text(c,eyebrow,130,176,23,TEAL,True)
        text(c,headline,130,265,66,WHITE,True,width=1660)
        if sub:
            text(c,sub,130,321,30,MUTED,width=1620)

    def universe(self,c,t,start,end):
        local = t-start
        text(c,"FOR LIBRARIANS",130,224,24,TEAL,True)
        rows(c,["A universe", "of research."],130,335,87,leading=99,width=790)
        if t >= self.at("u1","paper"):
            text(c,"One paper missing.",130,576,59,YELLOW,True,width=790,alpha=ease((t-self.at("u1","paper"))/.45))
        text(c,"What did your search miss?",130,665,37,MUTED,width=790)
        circle(c,1410,482,263,PURPLE,.23)
        c.drawOval(skia.Rect.MakeXYWH(1100,257,645,470),paint(LILAC,.3,3))
        for i,(x,y,s,a,phase) in enumerate(self.paper_orbits):
            document(c,x+math.sin(t*.4+phase)*25,y+math.cos(t*.5+phase)*14,s,[WHITE,LILAC,TEAL][i%3],a+math.sin(t+phase)*4)
        glow = .8+.15*math.sin(t*3)
        circle(c,1700,710,59,YELLOW,.12*glow)
        document(c,1700,710,.72,YELLOW,12)
        star(c,1745,666,13,YELLOW)
        # A result panel passes over only a few papers, leaving the gold one outside.
        rect(c,1140,323,492,276,NAVY,28)
        rect(c,1140,323,492,276,LILAC,28,stroke=3)
        rect(c,1171,352,427,55,WHITE,18)
        text(c,"Search the research",1193,388,25,PANEL,width=334)
        magnifier(c,1570,378,12,PURPLE)
        for i in range(3):
            circle(c,1208,446+i*54,10,[TEAL,BLUE,LILAC][i])
            rect(c,1235,438+i*54,288-i*49,12,[TEAL,BLUE,LILAC][i],5)
            rect(c,1235,458+i*54,218-i*18,5,MUTED,3,.4)
        robot(c,1260,731,t,1.07)
        if t >= self.takes["u2"]["start"]:
            pill(c,"MISSING EVIDENCE MATTERS",130,760,YELLOW,24)

    def pipeline(self,c,t,start,end):
        self.heading(c,"BEHIND THE SEARCH BOX","Look inside the pipeline.","Each stage shapes the evidence you see.")
        centers = [310,735,1160,1585]
        names = ["Collection","Retrieve","Rank","Present"]
        colors = [LILAC,BLUE,TEAL,YELLOW]
        for i,(x,name,color) in enumerate(zip(centers,names,colors)):
            if i:
                arrow(c,centers[i-1]+114,564,x-114,564,PURPLE,7)
            circle(c,x,564,105,color,.13)
            circle(c,x,564,105,color,stroke=3)
            if i == 0:
                for j in range(3):
                    document(c,x-32+j*31,562+(j%2)*16,.48,[WHITE,LILAC,WHITE][j],-10+j*9)
            elif i == 1:
                magnifier(c,x-12,555,40,BLUE)
            elif i == 2:
                topic_icon(c,"rerank",x,562,t)
            else:
                rect(c,x-67,521,134,87,YELLOW,12)
                for j in range(3):
                    rect(c,x-48,541+j*20,94-j*16,7,NAVY,3,.7)
            text(c,name,x,739,33,WHITE,True,align="center")
        flow = ((t-start)*.16)%1
        for j in range(6):
            p = (flow+j/6)%1
            x = 310+p*(1585-310)
            circle(c,x,414+math.sin(p*math.pi)*-30,7,TEAL,.8)
        if t >= self.at("p1","ranked"):
            a = ease((t-self.at("p1","ranked"))/.7)
            arrow(c,761,650,859,809,CORAL,5)
            document(c,913,821,.44,YELLOW,13)
            text(c,"Evidence can drop out along the way.",990,834,30,MUTED,width=720,alpha=a)
        text(c,"Understanding the pipeline helps you ask better questions.",130,942,34,TEAL,width=1650)

    def book(self,c,t,start,end):
        scale = 1.1+.02*math.sin((t-start)*.5)
        c.save()
        c.translate(384,548)
        c.rotate(-6+math.sin(t*.4)*1.5)
        cover(c,-196*scale,-270*scale,scale)
        c.restore()
        circle(c,598,247,60,TEAL,.12)
        star(c,605,254,28,YELLOW)
        star(c,121,244,16,TEAL)
        text(c,"MEET YOUR NEW SEARCH COMPANION",770,216,23,TEAL,True,width=1000)
        rows(c,["How Search", "Decides What", "You See"],770,322,80,leading=92,width=1020)
        text(c,"Aaron Tay",773,647,35,MUTED)
        pill(c,"FREE ONLINE TEXTBOOK",770,697,TEAL,27)
        text(c,"Written for librarians.",770,836,45,WHITE,True,width=1030)
        if t >= self.takes["b2"]["start"]:
            text(c,"Start with Boolean. No mathematics required.",770,903,30,MUTED,width=1050)

    def map(self,c,t,start,end):
        self.heading(c,"A MAP OF THE MACHINERY","Connect the moving parts.")
        topics = [("Boolean search","boolean",BLUE,"Boolean"), ("BM25","bm25",YELLOW,"B"),
                  ("Embeddings","embedding",TEAL,"embeddings"),("Hybrid search","hybrid",CORAL,"hybrid"),
                  ("Reranking","rerank",LILAC,"reranking"),("Agentic search","agent",TEAL,"agentic")]
        for i,(label,kind,color,word) in enumerate(topics):
            x = 400+(i%3)*560
            y = 471+(i//3)*339
            reveal = ease((t-self.at("m1",word)+.15)/.5)
            c.saveLayerAlpha(skia.Rect.MakeWH(W,H),round((.22+.78*reveal)*255))
            rect(c,x-221,y-139,442,269,PANEL,28)
            circle(c,x,y-30,91,color,.1)
            topic_icon(c,kind,x,y-33,t,color)
            text(c,label,x,y+99,34,WHITE,True,align="center")
            if reveal > .7:
                circle(c,x+182,y-103,7,color)
            c.restore()
        # The full grid is a conceptual map, not a claim that every tool uses all six.
        text(c,"Understand the methods. Follow the evidence.",960,998,31,TEAL,align="center",width=1660)

    def practice(self,c,t,start,end):
        self.heading(c,"FOR THE WORK YOU ALREADY DO","Turn understanding into action.")
        cards = [("Teach search","Clearer lessons","teach",BLUE,"Build"),
                 ("Investigate gaps","Trace missing evidence","investigate",YELLOW,"Investigate"),
                 ("Question claims","Sharper vendor questions","vendor",TEAL,"vendor")]
        for i,(label,sub,icon,color,word) in enumerate(cards):
            x = 385+i*565
            reveal = ease((t-self.at("r1",word)+.1)/.55)
            c.save()
            c.translate(0,(1-reveal)*18)
            rect(c,x-233,382,466,397,PANEL,28)
            rect(c,x-233,382,466,8,color,4)
            topic_icon(c,icon,x,540,t,color,1.2)
            text(c,label,x,696,36,WHITE,True,align="center")
            text(c,sub,x,744,26,MUTED,align="center")
            c.restore()
        if t >= self.takes["r2"]["start"]:
            rect(c,290,848,1340,99,PURPLE,22)
            text(c,"EVIDENCE SYNTHESIS",330,890,21,TEAL,True)
            text(c,"Look beyond a convincing answer.",330,931,33,WHITE,True)
            document(c,1514,898,.43,YELLOW,8)

    def labs(self,c,t,start,end):
        self.heading(c,"LEARN BY TRYING","Put the ideas to work.","Interactive companions for your next search, review or workshop.")
        kinds = [("Interactive labs","bm25",BLUE),("Evaluation kit","evaluation",TEAL),("Teaching notes","workshop",YELLOW)]
        for i,(label,icon,color) in enumerate(kinds):
            x = 393+i*563
            rect(c,x-232,405,464,374,PANEL,26)
            rect(c,x-207,428,414,49,NAVY,10)
            for j in range(3):
                circle(c,x-183+j*20,452,5,[CORAL,YELLOW,TEAL][j])
            topic_icon(c,icon,x,588,t,color,1.2)
            if i == 0:
                line(c,x-101,711,x+100,711,MUTED,5)
                circle(c,x-54+math.sin(t*1.3)*44,711,12,BLUE)
            text(c,label,x,756,31,WHITE,True,align="center")
        pill(c,"PLUS: A VENDOR QUESTIONNAIRE",130,857,TEAL,25)
        text(c,"Try it. Compare it. Teach it.",130,975,42,WHITE,True,width=1600)
        robot(c,1721,907,t,.38,True)

    def cta(self,c,t,start,end):
        circle(c,374,506,299,PURPLE,.18)
        cover(c,175,218,1.07,-4)
        robot(c,588,835,t,.61,True)
        star(c,630,240,22,YELLOW)
        text(c,"YOUR NEXT SEARCH STARTS HERE",755,218,24,TEAL,True,width=1030)
        rows(c,["How Search", "Decides What You See"],755,320,66,leading=79,width=1040)
        text(c,"A librarian’s guide · Aaron Tay",755,474,33,MUTED,width=1030)
        rect(c,755,522,435,93,TEAL,47)
        text(c,"READ FREE",808,584,39,NAVY,True)
        arrow(c,1102,569,1143+math.sin(t*2)*5,569,NAVY,5)
        text(c,"Start with ‘Read This First’",755,695,36,WHITE,True,width=1040)
        text(c,"A 45-minute guided route",755,748,30,MUTED,width=1040)
        rows(c,["aarontaycheehsien.github.io/", "Information-retrieval-crashcourse/"],755,850,31,TEAL,False,leading=45,width=1040)
        text(c,"Understand the search behind the answer.",755,982,32,YELLOW,True,width=1050)

    def scene(self,c,index,t):
        name = self.scene_ids[index]
        start,end = self.timeline["scenes"][name]
        getattr(self,name)(c,t,start,end)

    def frame(self,c,t):
        self.background(c,t)
        index = max(i for i,name in enumerate(self.scene_ids) if self.timeline["scenes"][name][0] <= t)
        start,_ = self.timeline["scenes"][self.scene_ids[index]]
        mix = ease((t-start)/.55) if index else ease(t/.5)
        if index and mix < 1:
            c.saveLayerAlpha(skia.Rect.MakeWH(W,H),round((1-mix)*255))
            self.scene(c,index-1,t)
            c.restore()
        c.saveLayerAlpha(skia.Rect.MakeWH(W,H),round(mix*255))
        self.scene(c,index,t)
        c.restore()
        text(c,"HOW SEARCH DECIDES WHAT YOU SEE",130,1044,17,MUTED,True)
        text(c,f"{index+1:02d} / 07",1790,1044,18,MUTED,align="right")
        rect(c,0,1075,W*clamp(t/self.timeline["duration"]),5,TEAL,0)

    def poster(self,c):
        self.background(c,5)
        self.cta(c,self.timeline["duration"]-2,*self.timeline["scenes"]["cta"])
