"""Original, deterministic animation and score for The Missing Paper.

Run --preview first, then --format both. All exports belong in outputs/promo-video.
No downloaded artwork, commercial screenshots, or prerecorded music are used.
"""
from __future__ import annotations

import argparse
from functools import lru_cache
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import sys
import time
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent
STORY = json.loads((HERE / "storyboard.json").read_text(encoding="utf-8"))
INK = "#0c1319"
IVORY = "#f5ead5"
MUTED = "#b4b4a8"
RED = "#e66b5e"
TEAL = "#83d9cc"
EDGE = "#394248"
PAPER = "#e8d9bb"
FPS = STORY["fps"]
DURATION = STORY["duration"]
FORMATS = {"landscape": (1920, 1080), "vertical": (1080, 1920)}
FONT_DIR = Path(os.environ.get("PROMO_FONT_DIR", "C:/Windows/Fonts"))
FONT_FILES = {"serif": "georgia.ttf", "bold": "georgiab.ttf", "italic": "georgiai.ttf", "mono": "consola.ttf", "mono-bold": "consolab.ttf"}


def clamp(x, low=0.0, high=1.0):
    return max(low, min(high, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def lerp(a, b, t):
    return a + (b - a) * t


@lru_cache(maxsize=160)
def font(size, face="serif"):
    return ImageFont.truetype(str(FONT_DIR / FONT_FILES[face]), int(size))


def rgba(color, alpha=255):
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4)) + (int(alpha),)


@lru_cache(maxsize=500)
def text_asset(text, size, face="serif", color=IVORY):
    f = font(size, face)
    box = f.getbbox(text)
    im = Image.new("RGBA", (max(1, int(f.getlength(text)) + 8), size + 18))
    ImageDraw.Draw(im).text((3, 3 - box[1]), text, font=f, fill=color)
    return im


def paste(im, sprite, x, y, opacity=1):
    if opacity <= 0:
        return
    if opacity < 0.999:
        sprite = sprite.copy()
        sprite.putalpha(sprite.getchannel("A").point(lambda a: int(a * opacity)))
    im.alpha_composite(sprite, (int(x), int(y)))


def text(im, value, x, y, size=32, face="serif", color=IVORY, opacity=1, align="left"):
    asset = text_asset(value, size, face, color)
    if align == "center":
        x -= asset.width / 2
    elif align == "right":
        x -= asset.width
    paste(im, asset, x, y, opacity)


def wrap(value, size, width, face="serif"):
    lines = []
    for paragraph in value.split("\n"):
        line = ""
        for word in paragraph.split():
            test = f"{line} {word}".strip()
            if line and font(size, face).getlength(test) > width:
                lines.append(line)
                line = word
            else:
                line = test
        lines.append(line)
    return lines


def copy(im, lines, x, y, size, width, reveal=1, color=IVORY, leading=1.13):
    lines = [part for line in lines for part in wrap(line, size, width)]
    total = sum(len(line) for line in lines)
    remaining = round(total * clamp(reveal))
    for i, line in enumerate(lines):
        # Reveal on the final, fixed line layout: typography never reflows.
        if remaining > 0:
            text(im, line[:remaining], x, y + i * size * leading, size, color=color)
        remaining -= len(line)
    return y + len(lines) * size * leading


def line(im, points, color=RED, width=3, alpha=255):
    layer = Image.new("RGBA", im.size)
    ImageDraw.Draw(layer).line(points, fill=rgba(color, alpha), width=width, joint="curve")
    im.alpha_composite(layer)


def bezier(points, n=64):
    a, b, c, d = points
    out = []
    for i in range(n + 1):
        t = i / n
        out.append(tuple((1-t)**3*a[k] + 3*(1-t)**2*t*b[k] + 3*(1-t)*t*t*c[k] + t**3*d[k] for k in (0, 1)))
    return out


def pin(im, x, y, color=RED, radius=7):
    d = ImageDraw.Draw(im)
    d.ellipse((x-radius+3, y-radius+6, x+radius+3, y+radius+6), fill="#050a0e")
    d.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)
    d.ellipse((x-radius/2, y-radius/2, x, y), fill=IVORY)


def arrow(im, start, end, color=RED, width=4, alpha=255):
    line(im, [start, end], color, width, alpha)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    d = ImageDraw.Draw(im)
    tip = 15
    pts = [end, (end[0]-tip*math.cos(angle-.55), end[1]-tip*math.sin(angle-.55)), (end[0]-tip*math.cos(angle+.55), end[1]-tip*math.sin(angle+.55))]
    d.polygon(pts, fill=rgba(color, alpha))


def stamp_asset(value, size=40, color=RED):
    content = text_asset(value, size, "mono-bold", color)
    im = Image.new("RGBA", (content.width + 38, content.height + 26))
    d = ImageDraw.Draw(im)
    d.rectangle((2, 2, im.width-3, im.height-3), outline=color, width=4)
    d.rectangle((8, 8, im.width-9, im.height-9), outline=color, width=1)
    paste(im, content, 18, 12)
    return im


def stamp(im, value, x, y, size=40, rotation=-8, opacity=1):
    asset = stamp_asset(value, size).rotate(rotation, Image.Resampling.BICUBIC, expand=True)
    paste(im, asset, x-asset.width/2, y-asset.height/2, opacity)


@lru_cache(maxsize=80)
def paper_asset(width, number="07", character=True, muted=False):
    # Supersampled original paper character, including folds and print texture.
    w = int(width)
    h = int(w * 1.32)
    scale = 2
    im = Image.new("RGBA", ((w+30)*scale, (h+30)*scale))
    d = ImageDraw.Draw(im)
    x, y = 12*scale, 10*scale
    fold = int(w * .19) * scale
    ww, hh = w*scale, h*scale
    shape = [(x, y), (x+ww-fold, y), (x+ww, y+fold), (x+ww, y+hh), (x, y+hh)]
    shadow = [(a+8*scale, b+12*scale) for a,b in shape]
    d.polygon(shadow, fill=(0, 0, 0, 100))
    d.polygon(shape, fill=rgba("#a8aa9e" if muted else IVORY))
    d.line(shape + [shape[0]], fill=rgba("#c9b994"), width=scale)
    d.polygon([(x+ww-fold,y), (x+ww-fold,y+fold), (x+ww,y+fold)], fill=rgba("#c7b995"))
    d.text((x+ww*.11, y+hh*.11), f"PAPER {number}", font=font(int(w*.12*scale), "mono-bold"), fill=INK)
    if character:
        for xx in (.34, .67):
            d.ellipse((x+ww*(xx-.035), y+hh*.43, x+ww*(xx+.035), y+hh*.50), fill=INK)
        d.line([(x+ww*.26, y+hh*.39), (x+ww*.43,y+hh*.37)], fill=INK, width=max(2,scale*2))
        d.line([(x+ww*.60, y+hh*.37), (x+ww*.76,y+hh*.40)], fill=INK, width=max(2,scale*2))
        d.arc((x+ww*.40, y+hh*.52, x+ww*.65, y+hh*.60), 185, 345, fill=INK, width=scale*2)
    else:
        for yy in (.38, .44, .50, .56):
            d.line([(x+ww*.12,y+hh*yy),(x+ww*.84,y+hh*yy)], fill=rgba("#a49d8c"), width=scale*2)
    for i in range(3):
        d.line([(x+ww*.12,y+hh*(.72+i*.055)), (x+ww*(.83-i*.055),y+hh*(.72+i*.055))], fill=rgba("#a49d8c"), width=scale)
    d.rectangle((x+ww*.12, y+hh*.91, x+ww*.38, y+hh*.925), fill=RED if number=="07" else INK)
    return im.resize((w+30,h+30), Image.Resampling.LANCZOS)


def paper(im, x, y, width=180, number="07", character=True, angle=0, opacity=1, muted=False):
    asset = paper_asset(int(width), number, character, muted)
    if abs(angle) > .1:
        asset = asset.rotate(round(angle, 1), Image.Resampling.BICUBIC, expand=True)
    paste(im, asset, x-asset.width/2, y-asset.height/2, opacity)


@lru_cache(maxsize=8)
def poster_asset(width):
    w, h = int(width), int(width*1.25)
    im = Image.new("RGBA", (w+50, h+50))
    d = ImageDraw.Draw(im)
    d.rectangle((25,30,w+30,h+35), fill=(0,0,0,110))
    d.polygon([(15,15),(w+14,12),(w+19,h+16),(12,h+20)], fill=PAPER)
    d.rectangle((32,33,w-4,h-1), outline=INK, width=2)
    text(im, "MISSING", w/2+10, 48, int(w*.14), "mono-bold", INK, align="center")
    d.rectangle((w*.20,h*.22,w*.83,h*.76), fill=INK)
    paper(im, w*.51,h*.49, int(w*.34), angle=-3)
    text(im,"ONE RELEVANT PAPER",w/2+10,h*.80,int(w*.045),"mono-bold",INK,align="center")
    text(im,"FILE 001 / LAST SEEN: INDEX",w/2+10,h*.90,int(w*.033),"mono",INK,align="center")
    return im


@lru_cache(maxsize=8)
def cover_asset(width):
    w, h = int(width), int(width*1.3)
    im = Image.new("RGBA", (w+50,h+50))
    d = ImageDraw.Draw(im)
    d.rectangle((28,30,w+30,h+30), fill=(0,0,0,140))
    d.polygon([(16,12),(w+16,12),(w+16,h+15),(16,h+15)],fill=IVORY)
    d.rectangle((16,12,35,h+15),fill="#d5c8a9")
    d.line((50,70,w-15,70),fill=INK,width=2)
    text(im,"ONLINE TEXTBOOK",58,34,int(w*.037),"mono-bold",INK)
    y=100
    for title in ["How Search", "Decides", "What You See"]:
        text(im,title,55,y,int(w*.079),"bold",INK)
        y+=w*.115
    text(im,"Aaron Tay",58,y+14,int(w*.051),"serif",INK)
    # The same thread and paper form the book's original promotional cover.
    pts=bezier([(w*.18,h*.66),(w*.67,h*.44),(w*.30,h*.96),(w*.88,h*.85)])
    line(im,pts,RED,4)
    paper(im,w*.57,h*.73,int(w*.24),angle=-9)
    pin(im,w*.18,h*.66)
    pin(im,w*.88,h*.85)
    text(im,"UNDERSTAND THE PIPELINE",58,h-22,int(w*.032),"mono-bold",INK)
    return im


@lru_cache(maxsize=4)
def backdrop(fmt):
    w,h=FORMATS[fmt]
    rng=np.random.default_rng(STORY["seed"]+(0 if fmt=="landscape" else 1))
    yy,xx=np.mgrid[0:h,0:w]
    vignette=np.clip(1-(((xx-w*.55)/w)**2+((yy-h*.48)/h)**2)*.9,.45,1)
    grain=rng.normal(0,1.25,(h,w))
    pixels=np.empty((h,w,3),dtype=np.uint8)
    for i,c in enumerate((18,25,30)):
        pixels[:,:,i]=np.clip(c*vignette+grain,0,255)
    im=Image.fromarray(pixels).convert("RGBA")
    d=ImageDraw.Draw(im)
    margin=70 if fmt=="landscape" else 48
    d.rectangle((margin,margin,w-margin,h-margin),outline="#293239",width=1)
    # A faint drafting grid makes the later diagram feel latent from frame one.
    for x in range(110,w-60,90):
        for y in range(145,h-70,90):
            d.point((x,y),fill="#3b4245")
    return im


def furniture(im, fmt, t, scene):
    w,h=im.size
    portrait=fmt=="vertical"
    x=86 if portrait else 130
    y=150 if portrait else 115
    text(im,"THE MISSING PAPER",x,y,25,"mono-bold",MUTED)
    text(im,"A RETRIEVAL MYSTERY",w-x,y,21,"mono",MUTED,align="right") if not portrait else None
    line(im,[(x,y+48),(w-x,y+48)],EDGE,1)
    text(im,scene["eyebrow"],x,y+85,26 if portrait else 24,"mono-bold",RED if scene["id"]!="book" else TEAL)
    # Decorative case timing sits outside the social-safe narrative zone.
    footer=h-(130 if portrait else 85)
    text(im,"FILE 001 / PAPER 07",x,footer,22,"mono",MUTED)
    text(im,f"{int(t):02d}:00 / 45:00",w-x,footer,22,"mono",MUTED,align="right")
    line(im,[(x,footer-25),(w-x,footer-25)],EDGE,1)
    line(im,[(x,footer-25),(lerp(x,w-x,t/DURATION),footer-25)],RED if t<30 else TEAL,2)


def dust(im, fmt, t, warm=True):
    w,h=im.size
    d=ImageDraw.Draw(im)
    for i in range(18):
        x=(w*.46+i*117+math.sin(t*.19+i)*18)%(w*.83)+w*.08
        y=(h*.31+i*83-t*(5+i%4))%(h*.61)+h*.15
        r=1 if i%3 else 2
        d.ellipse((x-r,y-r,x+r,y+r),fill=rgba(PAPER if warm else TEAL,25+int(15*(1+math.sin(t+i)))))


def shot_missing(im, fmt, u):
    p=fmt=="vertical"
    x,y,size,width=(86,326,83,910) if p else (130,290,107,850)
    copy(im,STORY["scenes"][0]["copy"],x,y,size,width,reveal=clamp((u-.15)/2.4))
    text(im,STORY["scenes"][0]["note"],x,650 if p else 703,34 if p else 30,"mono",MUTED,opacity=ease((u-2.45)/.45))
    cx,cy,pw=(540,1135,570) if p else (1400,570,480)
    layer=Image.new("RGBA",im.size)
    d=ImageDraw.Draw(layer)
    lampx,lampy=(855,795) if p else (1705,225)
    d.polygon([(lampx-30,lampy),(cx-pw*.65,cy+pw*.68),(cx+pw*.66,cy+pw*.68),(lampx+30,lampy)],fill=(220,199,144,15))
    im.alpha_composite(layer)
    d=ImageDraw.Draw(im)
    d.line([(lampx+60,lampy-145),(lampx+115,lampy-70),(lampx,lampy-15)],fill="#7c827d",width=8)
    d.polygon([(lampx-48,lampy-18),(lampx+23,lampy-47),(lampx+63,lampy+10),(lampx-30,lampy+32)],fill="#81827a")
    d.line((lampx-28,lampy+32,lampx+62,lampy+10),fill=IVORY,width=5)
    angle=-5+math.sin(u*2.2)*2*math.exp(-u*.6)
    asset=poster_asset(pw).rotate(angle,Image.Resampling.BICUBIC,expand=True)
    paste(im,asset,cx-asset.width/2,cy-asset.height/2,ease(u/.35))
    pin(im,cx+4,cy-pw*.60)
    thread=bezier([(cx+4,cy-pw*.60),(cx+pw*.65,cy-pw*.73),(cx+pw*.45,cy+pw*.3),(cx+pw*.7,cy+pw*.5)])
    line(im,thread,RED,3)
    dust(im,fmt,u)
    if u<.18:
        shade=Image.new("RGBA",im.size,(0,0,0,int(160*(1-ease(u/.18)))))
        im.alpha_composite(shade)


@lru_cache(maxsize=4)
def answer_asset(width):
    w,h=int(width),int(width*.79)
    im=Image.new("RGBA",(w+30,h+30))
    d=ImageDraw.Draw(im)
    d.rounded_rectangle((15,20,w+15,h+15),radius=12,fill=(0,0,0,110))
    d.rounded_rectangle((5,5,w+5,h+5),radius=12,fill=IVORY)
    text(im,"RESEARCH ASSISTANT",34,28,int(w*.035),"mono-bold",INK)
    d.line((34,76,w-24,76),fill="#c9bea8",width=2)
    text(im,"Evidence overview",34,107,int(w*.054),"serif",INK)
    for i,length in enumerate((.87,.79,.85,.63)):
        d.rectangle((35,172+i*23,w*length,177+i*23),fill="#b7b1a2")
    text(im,"SOURCES",34,h*.51,int(w*.033),"mono-bold",INK)
    cw=(w-84)/3
    for i in range(3):
        xx=34+i*(cw+8)
        d.rounded_rectangle((xx,h*.60,xx+cw,h*.85),radius=5,outline="#b8ad97",width=2)
        text(im,f"[{i+1:02d}]",xx+13,h*.625,int(w*.04),"mono-bold",INK)
        for yy in range(3):
            d.line((xx+14,h*.71+yy*12,xx+cw-14,h*.71+yy*12),fill="#afa797",width=2)
    return im


def shot_answer(im,fmt,u):
    p=fmt=="vertical"
    x,y,size,width=(86,326,83,910) if p else (130,320,94,870)
    scene=STORY["scenes"][1]
    a=1-ease((u-2.45)/.5)
    overlay=Image.new("RGBA",im.size)
    copy(overlay,scene["copy"],x,y,size,width)
    paste(im,overlay,0,0,a)
    overlay=Image.new("RGBA",im.size)
    copy(overlay,scene["reveal"],x,y,size,width)
    paste(im,overlay,0,0,1-a)
    cx,cy,pw=(540,1040,795) if p else (1380,530,675)
    plate=answer_asset(pw)
    px,py=int(cx-plate.width/2),int(cy-plate.height/2)
    paste(im,plate,px,py)
    for i in range(3):
        if u>.5+i*.6:
            stamp(im,"REAL",px+pw*(.18+i*.31),py+pw*.64,int(pw*.045),rotation=-10+i*6,opacity=ease((u-.5-i*.6)/.2))
    # The lens actually magnifies the source plate beneath it.
    lx=px+pw*(.28+.42*ease(u/4))
    ly=py+pw*(.29+.2*math.sin(u*.6))
    r=100 if p else 80
    box=(int(lx-px-r*.62),int(ly-py-r*.62),int(lx-px+r*.62),int(ly-py+r*.62))
    lens=plate.crop(box).resize((2*r,2*r),Image.Resampling.LANCZOS)
    mask=Image.new("L",lens.size)
    ImageDraw.Draw(mask).ellipse((2,2,2*r-3,2*r-3),fill=255)
    lens.putalpha(mask)
    paste(im,lens,lx-r,ly-r)
    d=ImageDraw.Draw(im)
    d.ellipse((lx-r,ly-r,lx+r,ly+r),outline=INK,width=12)
    d.arc((lx-r+15,ly-r+15,lx+r-15,ly+r-15),200,265,fill="#aaa995",width=4)
    d.line((lx+r*.71,ly+r*.71,lx+r*1.65,ly+r*1.65),fill=INK,width=24)
    # A conspicuous empty evidence slot appears beneath the complete answer.
    sy=1458 if p else 887
    sx=cx-160
    for xx in range(int(sx),int(sx+320),23):
        d.line((xx,sy,xx+12,sy),fill=RED,width=2)
        d.line((xx,sy+58,xx+12,sy+58),fill=RED,width=2)
    text(im,"PAPER 07 / ABSENT",cx,sy+14,28,"mono-bold",RED,opacity=ease((u-3)/.5),align="center")
    line(im,bezier([(cx+pw*.44,cy+pw*.12),(cx+pw*.59,cy+pw*.57),(cx-230,sy+160),(cx,sy+58)]),RED,3)


def stage_icon(im,cx,cy,kind,scale=1):
    d=ImageDraw.Draw(im)
    if kind=="INDEX":
        for i in range(3):
            paper(im,cx+(i-1)*24*scale,cy+(1-i)*6*scale,int(55*scale),str(i+1).zfill(2),False)
    elif kind=="RETRIEVAL":
        d.polygon([(cx-50*scale,cy-35*scale),(cx+50*scale,cy-35*scale),(cx+15*scale,cy+5*scale),(cx+15*scale,cy+37*scale),(cx-15*scale,cy+37*scale),(cx-15*scale,cy+5*scale)],outline=INK,fill="#c9b995",width=2)
    elif kind=="RERANKING":
        for i,ww in enumerate((85,65,43)):
            d.rectangle((cx-45*scale,cy-30*scale+i*26*scale,cx+(ww-45)*scale,cy-17*scale+i*26*scale),fill=INK)
    else:
        d.rounded_rectangle((cx-52*scale,cy-38*scale,cx+52*scale,cy+38*scale),radius=6,outline=INK,width=2)
        for i in range(3):
            d.line((cx-33*scale,cy-21*scale+i*18*scale,cx+33*scale,cy-21*scale+i*18*scale),fill=INK,width=3)


def shot_backwards(im,fmt,u):
    p=fmt=="vertical"
    copy(im,STORY["scenes"][2]["copy"],86 if p else 130,326 if p else 270,83 if p else 94,910 if p else 1550)
    original=im
    im=Image.new("RGBA",im.size)
    names=["INDEX","RETRIEVAL","RERANKING","ANSWER"]
    centers=[(620,805+i*210) for i in range(4)] if p else [(280+i*455,690) for i in range(4)]
    # The evidence-board thread visibly straightens into a pipeline.
    bend=150*(1-ease(u/3.2))
    for i in range(3):
        a,b=centers[i],centers[i+1]
        pts=bezier([a,(a[0]+bend,a[1]+(b[1]-a[1])*.35-bend),(b[0]-bend,b[1]-(b[1]-a[1])*.35+bend),b])
        line(im,pts,RED,4)
        for j in (.18,.83):
            pt=pts[int(j*64)]
            pin(im,*pt,radius=5)
    d=ImageDraw.Draw(im)
    tilew,tileh=(340,155) if p else (280,210)
    for i,(cx,cy) in enumerate(centers):
        # Early corkboard slips become aligned stage cards.
        layer=Image.new("RGBA",(tilew+22,tileh+24))
        dl=ImageDraw.Draw(layer)
        dl.rectangle((9,10,tilew+12,tileh+15),fill=(0,0,0,110))
        dl.rectangle((2,2,tilew+2,tileh+2),fill=IVORY)
        text(layer,names[i],tilew/2,18,27 if p else 26,"mono-bold",INK,align="center")
        stage_icon(layer,tilew/2,tileh*.63,names[i],.7 if p else 1)
        angle=(i%2*2-1)*5*(1-ease(u/3.2))
        layer=layer.rotate(angle,Image.Resampling.BICUBIC,expand=True)
        paste(im,layer,cx-layer.width/2,cy-layer.height/2)
        pin(im,cx,cy-tileh/2+9)
    journey=3*ease((u-.7)/5.5)
    which=min(2,int(journey))
    amount=journey-which
    a,b=centers[3-which],centers[2-which]
    cx,cy=lerp(a[0],b[0],amount),lerp(a[1],b[1],amount)
    d.ellipse((cx-19,cy-19,cx+19,cy+19),outline=RED,width=3)
    d.ellipse((cx-5,cy-5,cx+5,cy+5),fill=RED)
    if p:
        text(im,"TRACE",130,882,30,"mono-bold",RED)
        arrow(im,(205,1340),(205,940),RED)
        text(im,"BACK",130,1380,30,"mono-bold",RED)
    else:
        text(im,"ANSWER  <  RERANKING  <  RETRIEVAL  <  INDEX",960,904,29,"mono",MUTED,align="center")
    zoom=1+.18*(1-ease(u/3.2))
    anchor=(620,1120) if p else (960,700)
    if zoom>1.001:
        im=im.resize((round(im.width*zoom),round(im.height*zoom)),Image.Resampling.BICUBIC)
    paste(original,im,anchor[0]*(1-zoom),anchor[1]*(1-zoom))


def panel(im,box,label):
    d=ImageDraw.Draw(im)
    d.rounded_rectangle(box,radius=12,fill="#172127",outline=EDGE,width=2)
    text(im,label,box[0]+25,box[1]+19,29,"mono-bold",IVORY)
    d.line((box[0]+24,box[1]+68,box[2]-24,box[1]+68),fill=EDGE,width=1)


def shot_candidates(im,fmt,u):
    p=fmt=="vertical"
    copy(im,STORY["scenes"][3]["copy"],86 if p else 130,326 if p else 260,83 if p else 94,910 if p else 1600)
    if p:
        index=(104,772,976,1090)
        shortlist=(104,1230,976,1548)
        home=(275,955)
        starts=[(560+i*135,952) for i in range(3)]
        ends=[(320+i*210,1415) for i in range(3)]
        pw=125
        arrow(im,(740,1115),(740,1197),RED)
        text(im,"RETRIEVE",500,1133,32,"mono",MUTED)
    else:
        index=(130,530,800,930)
        shortlist=(1070,530,1790,930)
        home=(300,758)
        starts=[(540+i*76,750) for i in range(3)]
        ends=[(1220+i*210,760) for i in range(3)]
        pw=138
        arrow(im,(848,730),(1010,730),RED)
        text(im,"RETRIEVE",841,661,27,"mono",MUTED)
    panel(im,index,"INDEX")
    panel(im,shortlist,"CANDIDATE LIST")
    for i in range(3):
        v=ease((u-.6-i*.55)/2.7)
        a,b=starts[i],ends[i]
        px,py=lerp(a[0],b[0],v),lerp(a[1],b[1],v)
        paper(im,px,py,pw,str(i+1).zfill(2),False,angle=math.sin(v*math.pi)*(-6+i*6))
    paper(im,*home,148 if p else 172,angle=-4)
    if u>3.8:
        d=ImageDraw.Draw(im)
        radius=110 if p else 135
        # An investigator's pencil circles the paper that never moved.
        d.arc((home[0]-radius,home[1]-radius-8,home[0]+radius,home[1]+radius+8),20,20+int(345*ease((u-3.8)/1.4)),fill=RED,width=4)
    text(im,"STILL HERE",index[2]-175,index[3]-55,28,"mono-bold",RED,opacity=ease((u-4.2)/.5),align="center")


def shot_rerank(im,fmt,u):
    p=fmt=="vertical"
    x,y,size,width=(86,326,77,908) if p else (130,310,81,850)
    copy(im,STORY["scenes"][4]["copy"],x,y,size,width)
    if p:
        box=(440,848,970,1510)
        home=(235,1210)
        ys=[1018,1190,1362]
        cx=707
        pw=110
        barrier=393
    else:
        box=(1240,332,1800,930)
        home=(1062,692)
        ys=[497,658,819]
        cx=1515
        pw=100
        barrier=1204
    panel(im,box,"RERANKING")
    swap=ease((u-.7)/2.4)
    start=[2,0,1]
    for i in range(3):
        yy=lerp(ys[start[i]],ys[i],swap)
        d=ImageDraw.Draw(im)
        d.rounded_rectangle((cx-175,yy-59,cx+175,yy+65),radius=6,fill=IVORY)
        text(im,f"PAPER {i+1:02d}",cx-122,yy-27,31,"mono-bold",INK)
        for k in range(2):
            d.line((cx-120,yy+20+k*12,cx+107,yy+20+k*12),fill="#aea693",width=2)
        text(im,str(i+1).zfill(2),box[0]+26,ys[i]-18,27,"mono",RED)
    paper(im,home[0]+6*math.sin(u*1.5),home[1],170 if p else 165,angle=-5)
    d=ImageDraw.Draw(im)
    for yy in range(int(box[1]+80),int(box[3]),22):
        d.line((barrier,yy,barrier,yy+10),fill=RED,width=3)
    arrow(im,(home[0]+105,home[1]),(barrier-20,home[1]),RED,width=3)
    text(im,"NEVER RECEIVED",home[0],box[3]+30 if p else 854,27,"mono-bold",RED,align="center")


def open_book(im,cx,cy,width,u):
    d=ImageDraw.Draw(im)
    opening=ease(u/2.3)
    spread=width*(.25+.75*opening)
    hh=width*.52
    left=[(cx-spread/2,cy-hh/2-15),(cx,cy-hh/2+20),(cx,cy+hh/2+40),(cx-spread/2,cy+hh/2)]
    right=[(cx,cy-hh/2+20),(cx+spread/2,cy-hh/2-15),(cx+spread/2,cy+hh/2),(cx,cy+hh/2+40)]
    d.polygon([(x+9,y+17) for x,y in left+right[::-1]],fill=(0,0,0,100))
    d.polygon(left,fill=PAPER)
    d.polygon(right,fill=IVORY)
    for i in range(5):
        yy=cy-hh/2+85+i*22
        d.line((cx-spread/2+26,yy,cx-30,yy+8),fill="#a49e8e",width=2)
        d.line((cx+30,yy+8,cx+spread/2-26,yy),fill="#bbb09a",width=2)
    d.line((cx,cy-hh/2+20,cx,cy+hh/2+40),fill="#a89b7e",width=4)
    # A deliberately graphic librarian's hand turns the page at the corner.
    handx=cx+spread*.46
    handy=cy+hh*.40
    d.polygon([(handx-48,handy+158),(handx-28,handy+15),(handx-49,handy-25),(handx-41,handy-52),(handx-20,handy-47),(handx+2,handy-4),(handx+44,handy+38),(handx+52,handy+158)],fill="#b6b09f")
    d.line((handx-8,handy+18,handx+20,handy+65),fill="#837f74",width=2)
    if opening<.8:
        cover=cover_asset(int(width*.44))
        cover=cover.resize((max(1,int(cover.width*(1-opening))),cover.height),Image.Resampling.LANCZOS)
        paste(im,cover,cx-cover.width*.2,cy-cover.height/2,1-opening)


def shot_book(im,fmt,u):
    p=fmt=="vertical"
    x,y,size,width=(86,326,79,910) if p else (130,310,88,900)
    bottom=copy(im,STORY["scenes"][5]["copy"],x,y,size,width)
    topics=STORY["scenes"][5]["topics"]
    for i in range(3):
        values=" / ".join(topics[i*2:i*2+2])
        text(im,values.upper(),x,bottom+45+i*49,32 if p else 29,"mono",TEAL,opacity=ease((u-1.8-i*.65)/.6))
    cx,cy,bw=(520,1275,750) if p else (1410,722,620)
    open_book(im,cx,cy,bw,u)
    # The pipeline lifts out of the pages, illuminating the same case thread.
    appear=ease((u-1.2)/2)
    nodey=cy-bw*.49-80*appear
    xs=[cx-bw*.36+i*bw*.24 for i in range(4)]
    labels=["QUERY","RETRIEVE","RERANK","RESULT"]
    for i in range(3):
        line(im,[(xs[i],nodey),(xs[i+1],nodey)],TEAL,3,int(255*appear))
    for i,xx in enumerate(xs):
        overlay=Image.new("RGBA",im.size)
        dd=ImageDraw.Draw(overlay)
        dd.ellipse((xx-23,nodey-23,xx+23,nodey+23),fill=INK,outline=TEAL,width=3)
        text(overlay,str(i+1),xx,nodey-13,25,"mono",TEAL,align="center")
        text(overlay,labels[i],xx,nodey-78,24 if p else 21,"mono-bold",TEAL,align="center")
        line(overlay,[(xx,nodey+23),(cx+(xx-cx)*.4,cy)],TEAL,1,90)
        paste(im,overlay,0,0,appear)
    dust(im,fmt,u,False)


def shot_end(im,fmt,u):
    p=fmt=="vertical"
    if p:
        copy(im,["How Search", "Decides", "What You See"],86,324,90,910)
        text(im,STORY["author"],90,684,44,"serif",IVORY)
        text(im,"FREE ONLINE TEXTBOOK",90,776,34,"mono-bold",TEAL)
        cx,cy,pw=540,1211,455
        text(im,"Read free / Link in post",540,1607,43,"mono-bold",IVORY,align="center")
    else:
        copy(im,STORY["scenes"][6]["copy"],130,294,97,1140)
        text(im,STORY["author"],134,564,45,"serif",IVORY)
        text(im,"FREE ONLINE TEXTBOOK",134,674,34,"mono-bold",TEAL)
        text(im,"Read free / Link in post",134,806,38,"mono-bold",IVORY)
        cx,cy,pw=1490,595,460
    flip=ease(u/.45)
    cy+=3*math.sin(u*.7)
    if flip<1:
        asset=poster_asset(pw)
        paste(im,asset,cx-asset.width/2,cy-asset.height/2,1-flip)
    asset=cover_asset(pw)
    angle=-4+math.sin(u*.4)*.7
    asset=asset.rotate(angle,Image.Resampling.BICUBIC,expand=True)
    paste(im,asset,cx-asset.width/2,cy-asset.height/2,flip)
    stamp(im,"CASE REOPENED",cx,cy+pw*.36,31 if p else 32,rotation=-11,opacity=ease((u-.35)/.15))


SHOTS={"missing":shot_missing,"answer":shot_answer,"backwards":shot_backwards,"candidates":shot_candidates,"rerank":shot_rerank,"book":shot_book,"end":shot_end}


def scene_at(t):
    t=min(t,DURATION-1/FPS)
    return next(s for s in STORY["scenes"] if s["start"]<=t<s["end"])


def raw_frame(fmt,t):
    scene=scene_at(t)
    im=backdrop(fmt).copy()
    furniture(im,fmt,t,scene)
    SHOTS[scene["id"]](im,fmt,t-scene["start"])
    return im


def render_frame(fmt,t):
    scene=scene_at(t)
    im=raw_frame(fmt,t)
    # Quick match dissolves preserve the recurring paper/thread between settings.
    # Final card has no incoming dissolve, keeping its full eight-second hold.
    u=t-scene["start"]
    if scene["start"]>0 and scene["id"]!="end" and u<.24:
        old=raw_frame(fmt,scene["start"]-1/FPS)
        im=Image.blend(old,im,ease(u/.24))
    return im.convert("RGB")


def validate_story(check_fonts=True):
    scenes=STORY["scenes"]
    assert scenes[0]["start"]==0 and scenes[-1]["end"]==DURATION
    assert all(a["end"]==b["start"] for a,b in zip(scenes,scenes[1:]))
    assert all(s["end"]>s["start"] and s["id"] in SHOTS for s in scenes)
    if check_fonts:
        assert all((FONT_DIR/f).exists() for f in FONT_FILES.values()), f"Set PROMO_FONT_DIR to a directory containing {FONT_FILES}"
    book=(ROOT/"search-textbook.html").read_text(encoding="utf-8")
    assert f'<h1>{STORY["book_title"]}</h1>' in book
    assert STORY["author"] in book
    assert "reranking changes its order but cannot add an excluded record" in book
    # Essential headlines must fit the actual margins before rendering starts.
    if check_fonts:
        for fmt in FORMATS:
            width=910 if fmt=="vertical" else 1600
            for scene in scenes:
                for item in scene["copy"]:
                    assert all(font(77).getlength(part)<=width for part in wrap(item,77,width))


def ffmpeg_executable():
    override=os.environ.get("PROMO_FFMPEG")
    if override:
        return override
    import imageio_ffmpeg
    return imageio_ffmpeg.get_ffmpeg_exe()


def run_ffmpeg(args,log):
    with log.open("w",encoding="utf-8") as handle:
        result=subprocess.run([ffmpeg_executable(),"-hide_banner","-y",*args],stdout=subprocess.DEVNULL,stderr=handle)
    if result.returncode:
        raise RuntimeError(f"FFmpeg failed; see {log}")


def soundtrack(out):
    sr=48000
    n=sr*DURATION
    mix=np.zeros((n,2),dtype=np.float64)
    music=np.zeros_like(mix)
    effects=np.zeros_like(mix)
    rng=np.random.default_rng(STORY["seed"])

    def add(at,signal,volume=1,pan=0,bus="music"):
        start=round(at*sr)
        sig=signal[:max(0,n-start)]*volume
        if not len(sig):
            return
        mix[start:start+len(sig),0]+=sig*math.sqrt((1-pan)/2)
        mix[start:start+len(sig),1]+=sig*math.sqrt((1+pan)/2)
        stem=music if bus=="music" else effects
        stem[start:start+len(sig),0]+=sig*math.sqrt((1-pan)/2)
        stem[start:start+len(sig),1]+=sig*math.sqrt((1+pan)/2)

    def note(at,hz,duration=1.4,vol=.12,pan=0,soft=False):
        tt=np.arange(round(duration*sr))/sr
        phase=2*np.pi*hz*tt
        sig=np.sin(phase)+.24*np.sin(phase*2)+.085*np.sin(phase*3)
        env=(1-np.exp(-tt*(35 if soft else 140)))*np.exp(-tt*(1.7 if soft else 3.8))
        env*=np.minimum(1,(duration-tt)/.09)
        add(at,sig*env,vol,pan)

    def noise(at,duration,vol=.09,pan=0,kind="paper",bus="effects"):
        count=round(duration*sr)
        tt=np.arange(count)/sr
        nn=rng.normal(0,1,count)
        if kind=="click":
            sig=nn*np.exp(-tt*220)+.6*np.sin(2*np.pi*1400*tt)*np.exp(-tt*140)
        elif kind=="stamp":
            sig=nn*np.exp(-tt*45)*.5+np.sin(2*np.pi*(65*tt+25*(1-np.exp(-tt*20))/20))*np.exp(-tt*17)
        elif kind=="rewind":
            env=np.sin(np.pi*tt/duration)**2
            sig=nn*.12*env+np.sin(2*np.pi*(1400*tt-500*tt**2))*env*.28
        else:
            nn=np.convolve(nn,np.ones(12)/12,mode="same")
            sig=nn*np.sin(np.pi*tt/duration)**2
        add(at,sig,vol,pan,bus)

    # A spare D-minor detective motif becomes a D-major resolution after 30s.
    bass=[73.416,73.416,110.0,65.406]
    for i,at in enumerate(np.arange(.2,37,1.5)):
        note(float(at),bass[i%4],1.35,.12,pan=-.15)
        noise(float(at)+.72,.055,.018,pan=.2,kind="click",bus="music")
    melody=[293.665,349.228,329.628,220.0,261.626,293.665]
    for i,at in enumerate(np.arange(1.0,29.5,3)):
        note(float(at),melody[i%len(melody)],2.25,.057,pan=.2,soft=True)
    for i,at in enumerate((30.3,31.8,33.3,34.8,36.3)):
        note(at,[293.665,369.994,440,587.33,440][i],2.8,.07,pan=.25,soft=True)
    for hz in (146.832,184.997,220.0,293.665):
        note(38.05,hz,6.6,.045,pan=(hz%2-.5)*.3,soft=True)
    noise(.12,.09,.15,kind="click")
    for at in np.arange(.34,2.9,.095):
        noise(float(at),.035,.033,pan=-.25,kind="click")
    for at in (4.58,5.18,5.78):
        noise(at,.26,.17,kind="stamp")
    noise(10.05,1.05,.18,kind="rewind")
    for at in (17.6,18.15,18.7):
        noise(at,.48,.14,pan=.35)
    noise(21.8,.05,.09,kind="click")
    for at in (24.7,25.4,26.1):
        noise(at,.65,.12,pan=-.2)
    noise(30.15,1.15,.18)
    note(32.1,880,.9,.035,pan=.3,soft=True)
    noise(37.42,.4,.3,kind="stamp")
    fade=np.minimum(1,np.arange(n)/(sr*.18))*np.minimum(1,(n-1-np.arange(n))/(sr*.65))
    mix*=fade[:,None]
    music*=fade[:,None]
    effects*=fade[:,None]
    peak=float(np.max(np.abs(mix)))
    assert peak<1, f"Unmastered audio clips at {peak}"
    path=out/"score-original.wav"
    for stem_path,stem in ((path,mix),(out/"music-original.wav",music),(out/"effects-original.wav",effects)):
        with wave.open(str(stem_path),"wb") as wav:
            wav.setnchannels(2)
            wav.setsampwidth(2)
            wav.setframerate(sr)
            wav.writeframes((stem*32767).astype("<i2").tobytes())
    master=out/"soundtrack.wav"
    # Reserve a further decibel for AAC's intersample peak overshoot.
    run_ffmpeg(["-i",str(path),"-af","loudnorm=I=-16:TP=-2:LRA=9","-ar","48000","-c:a","pcm_s16le",str(master)],out/"audio-mastering.log")
    return master,{"sample_rate":sr,"channels":2,"duration":DURATION,"unmastered_peak":peak}


def previews(out,formats):
    times=[2.9,5.8,8.6,15.5,22.8,28.5,35.6,40.5]
    for fmt in formats:
        directory=out/"previews"/fmt
        directory.mkdir(parents=True,exist_ok=True)
        thumbs=[]
        tw,th=(480,270) if fmt=="landscape" else (270,480)
        for t in times:
            frame=render_frame(fmt,t)
            frame.save(directory/f"{t:04.1f}-{scene_at(t)['id']}.jpg",quality=94)
            thumb=frame.resize((tw,th),Image.Resampling.LANCZOS)
            thumbs.append(thumb)
        cols=2 if fmt=="landscape" else 4
        rows=math.ceil(len(thumbs)/cols)
        contact=Image.new("RGB",(cols*(tw+16)+16,rows*(th+45)+16),INK)
        for i,thumb in enumerate(thumbs):
            x=16+(i%cols)*(tw+16)
            y=16+(i//cols)*(th+45)
            contact.paste(thumb,(x,y))
            ImageDraw.Draw(contact).text((x,y+th+7),f"{times[i]:04.1f}s / {scene_at(times[i])['id']}",font=font(18,"mono"),fill=IVORY)
        contact.save(out/f"contact-sheet-{fmt}.jpg",quality=94)
        render_frame(fmt,40.5).save(out/f"poster-{fmt}.jpg",quality=96)


def export_video(out,fmt,audio):
    w,h=FORMATS[fmt]
    target=out/f"missing-paper-{fmt}.mp4"
    log=out/f"encode-{fmt}.log"
    cmd=[ffmpeg_executable(),"-hide_banner","-loglevel","warning","-y","-f","rawvideo","-pix_fmt","rgb24","-s",f"{w}x{h}","-r",str(FPS),"-i","pipe:0","-i",str(audio),"-c:v","libx264","-preset","fast","-crf","20","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-ar","48000","-t",str(DURATION),"-movflags","+faststart",str(target)]
    start=time.monotonic()
    with log.open("w",encoding="utf-8") as handle:
        proc=subprocess.Popen(cmd,stdin=subprocess.PIPE,stderr=handle,stdout=subprocess.DEVNULL)
        try:
            for i in range(FPS*DURATION):
                frame=render_frame(fmt,i/FPS)
                assert frame.size==(w,h)
                proc.stdin.write(frame.tobytes())
                if i%150==0:
                    print(f"{fmt}: {i//FPS:02d}s / {DURATION}s ({time.monotonic()-start:.1f}s elapsed)",flush=True)
            proc.stdin.close()
            code=proc.wait()
        except BaseException:
            proc.kill()
            proc.wait()
            raise
    if code:
        raise RuntimeError(f"Encoding failed: {log}")
    return target


def verification(out,video,fmt):
    # Decode every video/audio packet and preserve machine-readable stream info.
    log=out/f"verify-{fmt}.log"
    run_ffmpeg(["-i",str(video),"-map","0:v:0","-map","0:a:0","-f","null","-"],log)
    metadata=log.read_text(encoding="utf-8")
    w,h=FORMATS[fmt]
    assert f"{w}x{h}" in metadata and "30 fps" in metadata
    assert "Duration: 00:00:45.00" in metadata
    assert "Video: h264" in metadata and "yuv420p" in metadata
    assert "Audio: aac" in metadata and "48000 Hz, stereo" in metadata
    assert "frame= 1350" in metadata or "frame=1350" in metadata.replace(" ","")
    loudness=out/f"loudness-{fmt}.log"
    run_ffmpeg(["-i",str(video),"-vn","-af","loudnorm=I=-16:TP=-1:LRA=9:print_format=json","-f","null","-"],loudness)
    info=loudness.read_text(encoding="utf-8")
    measurement=json.loads(info[info.rfind("{"):info.rfind("}")+1])
    assert float(measurement["input_tp"])<=-1, f"Encoded audio exceeds the -1 dBTP ceiling: {measurement}"
    # MP4 atom order proves progressive download / fast-start playback.
    payload=video.read_bytes()
    cursor=0
    atoms=[]
    while cursor+8<=len(payload):
        size=int.from_bytes(payload[cursor:cursor+4],"big")
        kind=payload[cursor+4:cursor+8].decode("ascii",errors="replace")
        if size==1:
            size=int.from_bytes(payload[cursor+8:cursor+16],"big")
        atoms.append(kind)
        if size<8:
            break
        cursor+=size
    assert atoms.index("moov")<atoms.index("mdat")
    return {"file":video.name,"width":w,"height":h,"fps":FPS,"frames":FPS*DURATION,"duration_seconds":DURATION,"video_codec":"H.264","pixel_format":"yuv420p","audio_codec":"AAC","decode":"passed","fast_start":True,"integrated_lufs":float(measurement["input_i"]),"true_peak_dbtp":float(measurement["input_tp"]),"bytes":len(payload),"sha256":hashlib.sha256(payload).hexdigest()}


def write_sharing_copy(out,narrated=True):
    value=("Every citation was real. One crucial paper was absent.\n\n"
           "The Missing Paper — a 45-second search mystery for librarians.\n\n"
           "How Search Decides What You See, Aaron Tay's free online textbook, "
           "explains the machinery between a question and the papers you actually see: "
           "Boolean search, BM25, embeddings, hybrid search, reranking, and evaluation.\n\n"
           f"Read the textbook: {STORY['book_url']}\n"
           f"Start with Read this first: {STORY['intro_url']}\n\n"
           "Video description: A paper-shaped missing-person poster starts a noir investigation. "
           "Verified citations lead backwards through an evidence board that becomes a search pipeline. "
           "Paper 07 remains in the index as other papers enter the shortlist. Reranking sorts only that shortlist. "
           "A librarian opens the textbook, illuminating the pipeline. The final card reads: "
           "How Search Decides What You See / Aaron Tay / Free online textbook / Read free, link in post.\n\n"
           "All visuals and music were created procedurally for this film. Original promotional cover artwork "
           "represents the online textbook. The search example is illustrative.\n")
    if narrated:
        import narration
        value+=f"Synthetic female narration: Microsoft {narration.config()['voice']}.\n"
    (out/"share-copy.txt").write_text(value,encoding="utf-8")
    viewer='''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>The Missing Paper — video preview</title><style>
*{box-sizing:border-box}body{margin:0;background:#0c1319;color:#f5ead5;font:16px Georgia,serif}
main{max-width:1280px;margin:0 auto;padding:36px 28px}h1{font-size:42px;font-weight:normal;margin:0 0 8px}
p{color:#b4b4a8;line-height:1.6}h2{font:16px Consolas,monospace;color:#83d9cc;margin:0 0 16px}
section{margin:32px 0}video{display:block;width:100%;background:#050a0e;border:1px solid #394248}
.vertical{max-width:420px}a{color:#83d9cc}nav{display:flex;gap:24px;flex-wrap:wrap;margin:18px 0}
</style></head><body><main><h1>The Missing Paper</h1><p>A 45-second retrieval mystery for librarians. Original animation and score. NARRATION_NOTICE</p>
<section><h2>LANDSCAPE / 1920 × 1080</h2><video controls playsinline preload="metadata" poster="poster-landscape.jpg" aria-label="The Missing Paper landscape video"><source src="missing-paper-landscape.mp4" type="video/mp4">CAPTION_TRACK</video></section>
<section class="vertical"><h2>VERTICAL / 1080 × 1920</h2><video controls playsinline preload="metadata" poster="poster-vertical.jpg" aria-label="The Missing Paper vertical video"><source src="missing-paper-vertical.mp4" type="video/mp4">CAPTION_TRACK</video></section>
<nav><a href="missing-paper-landscape.mp4" download>Download landscape</a><a href="missing-paper-vertical.mp4" download>Download vertical</a><a href="share-copy.txt">Sharing caption and reader links</a></nav>
NARRATION_LINKS
<p>Promoting <em>How Search Decides What You See</em> by Aaron Tay — a free online textbook.</p></main></body></html>'''
    viewer=viewer.replace("NARRATION_NOTICE","Warm female investigator narration (synthetic voice)." if narrated else "Music-only edition.")
    viewer=viewer.replace("CAPTION_TRACK",'<track kind="captions" src="narration.vtt" srclang="en" label="English narration">' if narrated else "")
    viewer=viewer.replace("NARRATION_LINKS",'<nav><a href="narration-transcript.txt">Narration transcript</a><a href="narration.srt" download>Download SRT captions</a><a href="missing-paper-landscape-music-only.mp4" download>Landscape music-only original</a><a href="missing-paper-vertical-music-only.mp4" download>Vertical music-only original</a></nav>' if narrated else "")
    (out/"preview.html").write_text(viewer,encoding="utf-8")


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format",choices=["both",*FORMATS],default="both")
    parser.add_argument("--output",type=Path,default=ROOT/"outputs"/"promo-video")
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument("--preview",action="store_true",help="Render storyboard frames and posters without video or audio")
    mode.add_argument("--verify-only",action="store_true",help="Decode and measure existing MP4 exports")
    mode.add_argument("--audio-only",action="store_true",help="Add or rebuild narration on existing videos, preserving every picture packet")
    parser.add_argument("--music-only",action="store_true",help="Render the original edition without narration")
    args=parser.parse_args()
    out=args.output.resolve()
    out.mkdir(parents=True,exist_ok=True)
    formats=list(FORMATS) if args.format=="both" else [args.format]
    if args.audio_only and args.music_only:
        parser.error("--audio-only adds narration; use --music-only with a full render")
    validate_story(check_fonts=not (args.audio_only or args.verify_only))
    if args.verify_only:
        results=[verification(out,out/f"missing-paper-{fmt}.mp4",fmt) for fmt in formats]
        manifest_path=out/"verification.json"
        existing=json.loads(manifest_path.read_text(encoding="utf-8")) if manifest_path.exists() else {}
        if not isinstance(existing,dict):
            existing={}
        previous={item["file"]:item for item in existing.get("exports",[])}
        for item in results:
            previous[item["file"]]={**previous.get(item["file"],{}),**item}
        existing["exports"]=list(previous.values())
        manifest_path.write_text(json.dumps(existing,indent=2),encoding="utf-8")
        print(json.dumps(results,indent=2))
        return
    if args.audio_only:
        for fmt in formats:
            if not (out/f"missing-paper-{fmt}.mp4").is_file():
                parser.error(f"No existing {fmt} video; run a full render first")
    else:
        previews(out,formats)
    if args.preview:
        write_sharing_copy(out,narrated=not args.music_only)
        print(f"Storyboard previews and posters: {out}",flush=True)
        return
    audio,audio_info=soundtrack(out)
    narration_info=None
    if not args.music_only:
        import narration
        narrated_audio,narration_info=narration.mix(out,STORY,run_ffmpeg)
    results=[]
    for fmt in formats:
        video=out/f"missing-paper-{fmt}.mp4" if args.audio_only else export_video(out,fmt,audio)
        if args.music_only:
            results.append(verification(out,video,fmt))
        else:
            results.append(narration.remux(out,fmt,narrated_audio,run_ffmpeg,ffmpeg_executable(),verification))
        print(f"Verified: {video}",flush=True)
    manifest={"title":STORY["title"],"seed":STORY["seed"],"audio":audio_info,"exports":results,"python":sys.version,"fonts":{k:str(FONT_DIR/v) for k,v in FONT_FILES.items()}}
    if narration_info:
        manifest["narration"]=narration_info
    (out/"verification.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    write_sharing_copy(out,narrated=not args.music_only)
    print(f"Complete: {out}",flush=True)


if __name__=="__main__":
    main()
