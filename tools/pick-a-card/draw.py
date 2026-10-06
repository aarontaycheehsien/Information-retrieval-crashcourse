"""Small Skia motion-graphics toolkit: palette, fonts, easing, cards and props."""
from __future__ import annotations

import math
import os
from functools import lru_cache
from pathlib import Path

import numpy as np
import skia

W, H = 1920, 1080
FONT_DIR = Path(os.environ.get("PROMO_FONT_DIR", "C:/Windows/Fonts"))

# Palette ---------------------------------------------------------------
FELT = (18, 70, 54)
FELT_DARK = (6, 30, 23)
CREAM = (247, 239, 222)
PAPER = (236, 225, 200)
INK = (30, 26, 24)
MUTED = (120, 110, 98)
CRIMSON = (178, 34, 46)
CRIMSON_DARK = (112, 18, 28)
GOLD = (218, 176, 96)
GOLD_LIGHT = (246, 216, 150)
BLUEPRINT = (13, 33, 64)
BLUE_LINE = (128, 176, 232)
SMOKE = (226, 226, 220)

FONT_FILES = {
    "black": "BOD_BLAR.TTF",      # Bodoni MT Black
    "bodoni": "BOD_R.TTF",
    "bodoni_b": "BOD_B.TTF",
    "italic": "BOD_I.TTF",
    "caps": "ENGR.TTF",           # Engravers MT
    "playbill": "PLAYBILL.TTF",
    "mono": "consola.ttf",
    "mono_b": "consolab.ttf",
    "ui": "segoeui.ttf",
    "ui_b": "segoeuib.ttf",
    "hand": "Inkfree.ttf",
    "georgia_b": "georgiab.ttf",
    "georgia_i": "georgiai.ttf",
}


def check_fonts() -> None:
    missing = [f for f in FONT_FILES.values() if not (FONT_DIR / f).is_file()]
    if missing:
        raise SystemExit(f"Missing fonts in {FONT_DIR}: {', '.join(missing)} (set PROMO_FONT_DIR)")


@lru_cache(maxsize=None)
def typeface(name: str) -> skia.Typeface:
    return skia.Typeface.MakeFromFile(str(FONT_DIR / FONT_FILES[name]))


@lru_cache(maxsize=None)
def font(name: str, size: float) -> skia.Font:
    f = skia.Font(typeface(name), size)
    f.setEdging(skia.Font.Edging.kAntiAlias)
    f.setSubpixel(True)
    return f


# Easing ----------------------------------------------------------------
def clamp(x: float, a: float = 0.0, b: float = 1.0) -> float:
    return a if x < a else b if x > b else x


def prog(t: float, a: float, b: float) -> float:
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


def ease_out(p: float) -> float:
    return 1 - (1 - p) ** 3


def ease_in(p: float) -> float:
    return p ** 3


def ease_io(p: float) -> float:
    return 4 * p ** 3 if p < 0.5 else 1 - (-2 * p + 2) ** 3 / 2


def back_out(p: float, s: float = 1.6) -> float:
    p -= 1
    return p * p * ((s + 1) * p + s) + 1


def spring(p: float, bounce: float = 0.35) -> float:
    if p <= 0:
        return 0.0
    if p >= 1:
        return 1.0
    return 1 - math.exp(-6 * p) * math.cos(p * math.pi * (2.2 + 4 * bounce))


def lerp(a: float, b: float, p: float) -> float:
    return a + (b - a) * p


def fade(t: float, a: float, b: float, c: float | None = None, d: float | None = None) -> float:
    """1 between fade-in [a,b] and fade-out [c,d]."""
    v = prog(t, a, b)
    if c is not None and d is not None:
        v *= 1 - prog(t, c, d)
    return v


# Paint helpers ---------------------------------------------------------
def rgba(c, a: float = 1.0) -> int:
    return skia.Color(int(c[0]), int(c[1]), int(c[2]), int(round(255 * clamp(a))))


def paint(c=CREAM, a: float = 1.0, stroke: float | None = None, blur: float = 0.0, cap_round: bool = False) -> skia.Paint:
    p = skia.Paint(AntiAlias=True, Color=rgba(c, a))
    if stroke:
        p.setStyle(skia.Paint.kStroke_Style)
        p.setStrokeWidth(stroke)
        if cap_round:
            p.setStrokeCap(skia.Paint.kRound_Cap)
            p.setStrokeJoin(skia.Paint.kRound_Join)
    if blur > 0:
        p.setMaskFilter(skia.MaskFilter.MakeBlur(skia.kNormal_BlurStyle, blur))
    return p


def text(c: skia.Canvas, s: str, x: float, y: float, f: skia.Font, color=CREAM, a: float = 1.0,
         align: str = "c", tracking: float = 0.0, shadow: float = 0.0) -> float:
    """Draw a single line; returns its width. y is the baseline."""
    if a <= 0.002 or not s:
        return 0.0
    if tracking:
        widths = [f.measureText(ch) for ch in s]
        width = sum(widths) + tracking * (len(s) - 1)
    else:
        width = f.measureText(s)
    x0 = x - width / 2 if align == "c" else x - width if align == "r" else x
    if shadow:
        sp = paint((0, 0, 0), 0.55 * a, blur=shadow)
        _draw_run(c, s, x0 + shadow * 0.3, y + shadow * 0.6, f, sp, tracking)
    _draw_run(c, s, x0, y, f, paint(color, a), tracking)
    return width


def _draw_run(c, s, x0, y, f, p, tracking):
    if not tracking:
        c.drawString(s, x0, y, f, p)
        return
    x = x0
    for ch in s:
        c.drawString(ch, x, y, f, p)
        x += f.measureText(ch) + tracking


def measure(s: str, f: skia.Font, tracking: float = 0.0) -> float:
    return f.measureText(s) + tracking * max(0, len(s) - 1)


def wrap(s: str, f: skia.Font, width: float) -> list[str]:
    lines, cur = [], ""
    for word in s.split():
        trial = f"{cur} {word}".strip()
        if f.measureText(trial) <= width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def rrect(x0, y0, x1, y1, r) -> skia.RRect:
    return skia.RRect.MakeRectXY(skia.Rect(x0, y0, x1, y1), r, r)


def offscreen(w: int, h: int, draw_fn) -> skia.Image:
    surface = skia.Surface(w, h)
    with surface as c:
        c.clear(skia.Color4f(0, 0, 0, 0))
        draw_fn(c)
    return surface.makeImageSnapshot().withDefaultMipmaps()


SAMPLING = skia.SamplingOptions(skia.FilterMode.kLinear, skia.MipmapMode.kLinear)


def draw_image(c: skia.Canvas, img: skia.Image, cx: float, cy: float, w: float, h: float, a: float = 1.0) -> None:
    p = skia.Paint(AntiAlias=True)
    p.setAlphaf(clamp(a))
    c.drawImageRect(img, skia.Rect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), SAMPLING, p)


# Background ------------------------------------------------------------
def felt_image(seed: int = 7) -> skia.Image:
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    # low-frequency mottling
    small = rng.normal(0, 1, (18, 32)).astype(np.float32)
    from PIL import Image
    mott = np.asarray(Image.fromarray(small).resize((W, H), Image.BICUBIC), np.float32)
    grain = rng.normal(0, 1, (H, W)).astype(np.float32)
    # woven fibre: faint diagonal ridges
    weave = np.sin((xx + yy) * 1.9) * 0.6 + np.sin((xx - yy) * 1.7) * 0.6
    base = np.array(FELT, np.float32)
    dark = np.array(FELT_DARK, np.float32)
    r = np.sqrt(((xx - W / 2) / (W * 0.62)) ** 2 + ((yy - H * 0.52) / (H * 0.78)) ** 2)
    vig = np.clip(r, 0, 1.25) ** 1.7
    col = base[None, None, :] * (1 - vig[..., None] * 0.78) + dark[None, None, :] * (vig[..., None] * 0.78)
    col += (mott * 5.0 + grain * 3.2 + weave * 1.4)[..., None]
    rgba_arr = np.dstack([np.clip(col, 0, 255).astype(np.uint8)[..., ::-1], np.full((H, W), 255, np.uint8)])
    return skia.Image.fromarray(np.ascontiguousarray(rgba_arr), colorType=skia.kBGRA_8888_ColorType)


def blueprint_image() -> skia.Image:
    def draw(c):
        c.clear(rgba(BLUEPRINT))
        g = skia.GradientShader.MakeRadial((W / 2, H * 0.48), W * 0.75, [rgba((26, 58, 104)), rgba((8, 20, 42))])
        p = skia.Paint(Shader=g)
        c.drawRect(skia.Rect(0, 0, W, H), p)
        for x in range(0, W + 1, 40):
            c.drawLine(x, 0, x, H, paint(BLUE_LINE, 0.16 if x % 200 else 0.3, stroke=1))
        for y in range(0, H + 1, 40):
            c.drawLine(0, y, W, y, paint(BLUE_LINE, 0.16 if y % 200 else 0.3, stroke=1))
    return offscreen(W, H, draw)


def spotlight(c: skia.Canvas, cx: float, cy: float, r: float, a: float, color=(255, 226, 170)) -> None:
    if a <= 0:
        return
    g = skia.GradientShader.MakeRadial((cx, cy), r, [rgba(color, 0.22 * a), rgba(color, 0.08 * a), rgba(color, 0)], [0, 0.45, 1])
    p = skia.Paint(Shader=g, BlendMode=skia.BlendMode.kPlus)
    c.drawCircle(cx, cy, r, p)


# Glyphs ----------------------------------------------------------------
def magnifier(c: skia.Canvas, x: float, y: float, s: float, color=CRIMSON, a: float = 1.0, width: float | None = None) -> None:
    w = width or max(1.5, s * 0.16)
    c.drawCircle(x - s * 0.12, y - s * 0.12, s * 0.36, paint(color, a, stroke=w))
    c.drawLine(x + s * 0.14, y + s * 0.14, x + s * 0.48, y + s * 0.48, paint(color, a, stroke=w * 1.25, cap_round=True))


def play_glyph(c, x, y, s, color=CRIMSON, a=1.0):
    path = skia.Path()
    path.moveTo(x - s * 0.32, y - s * 0.42)
    path.lineTo(x + s * 0.44, y)
    path.lineTo(x - s * 0.32, y + s * 0.42)
    path.close()
    c.drawPath(path, paint(color, a))


def sparkle(c: skia.Canvas, x: float, y: float, s: float, a: float, color=GOLD_LIGHT) -> None:
    if a <= 0 or s <= 0:
        return
    path = skia.Path()
    k = 0.22
    path.moveTo(x, y - s)
    path.quadTo(x + s * k, y - s * k, x + s, y)
    path.quadTo(x + s * k, y + s * k, x, y + s)
    path.quadTo(x - s * k, y + s * k, x - s, y)
    path.quadTo(x - s * k, y - s * k, x, y - s)
    c.drawPath(path, paint(color, a * 0.5, blur=s * 0.35))
    c.drawPath(path, paint(color, a))


# Cards -----------------------------------------------------------------
CW, CH = 230, 322
RES = 2  # pre-render scale for crisp zooms


RESULTS = [
    ("Does open access raise citation counts?", "A. Rivera, K. Osei · 2019"),
    ("Free to read, more often cited?", "M. Lindqvist · 2021"),
    ("Open access and research reach", "J. Park et al. · 2018"),
    ("Self-archiving and citation impact", "S. Haddad · 2020"),
    ("Measuring the open access effect", "T. Nguyen · 2017"),
    ("Who cites openly available papers?", "L. Moreau · 2022"),
    ("Citation patterns in open journals", "R. Adeyemi · 2016"),
]


def _card_base(c, w, h, s):
    c.drawRRect(rrect(0, 0, w, h, 16 * s), paint(CREAM))
    c.drawRRect(rrect(7 * s, 7 * s, w - 7 * s, h - 7 * s, 11 * s), paint(CRIMSON, 0.55, stroke=1.6 * s))


def _corner(c, label, s, w, h, color=CRIMSON, glyph="mag"):
    f = font("bodoni_b", 34 * s)
    for flip in (False, True):
        c.save()
        if flip:
            c.translate(w, h)
            c.rotate(180)
        text(c, label, 26 * s, 46 * s, f, color, align="c")
        if glyph == "mag":
            magnifier(c, 26 * s, 66 * s, 20 * s, color)
        elif glyph == "diamond":
            d = skia.Path()
            d.moveTo(26 * s, 30 * s)
            d.lineTo(36 * s, 46 * s)
            d.lineTo(26 * s, 62 * s)
            d.lineTo(16 * s, 46 * s)
            d.close()
            c.drawPath(d, paint(color))
        elif glyph == "play":
            play_glyph(c, 27 * s, 68 * s, 22 * s, color)
        c.restore()


def result_face(rank: int, title: str, byline: str) -> skia.Image:
    s = RES
    w, h = CW * s, CH * s

    def draw(c):
        _card_base(c, w, h, s)
        _corner(c, str(rank), s, w, h)
        # mini search result
        x0, x1 = 50 * s, w - 50 * s
        f = font("georgia_b", 17.5 * s)
        y = 108 * s
        for line in wrap(title, f, x1 - x0):
            text(c, line, x0, y, f, (26, 52, 120), align="l")
            y += 22 * s
        text(c, byline, x0, y + 4 * s, font("ui", 12.5 * s), (40, 120, 70), align="l")
        y += 26 * s
        for i, frac in enumerate((1.0, 0.92, 0.97, 0.6)):
            c.drawRRect(rrect(x0, y + i * 15 * s, x0 + (x1 - x0) * frac, y + i * 15 * s + 6 * s, 3 * s), paint(MUTED, 0.38))
    return offscreen(w, h, draw)


def back_image() -> skia.Image:
    s = RES
    w, h = CW * s, CH * s

    def draw(c):
        c.drawRRect(rrect(0, 0, w, h, 16 * s), paint(CREAM))
        c.drawRRect(rrect(9 * s, 9 * s, w - 9 * s, h - 9 * s, 10 * s), paint(CRIMSON))
        c.save()
        c.clipRRect(rrect(15 * s, 15 * s, w - 15 * s, h - 15 * s, 7 * s), doAntiAlias=True)
        step = 22 * s
        lp = paint(GOLD, 0.42, stroke=1.4 * s)
        for k in range(-20, 30):
            c.drawLine(k * step, 0, k * step + h, h, lp)
            c.drawLine(k * step, h, k * step + h, 0, lp)
        c.restore()
        c.drawRRect(rrect(15 * s, 15 * s, w - 15 * s, h - 15 * s, 7 * s), paint(GOLD, 0.9, stroke=2 * s))
        c.drawCircle(w / 2, h / 2, 44 * s, paint(CRIMSON_DARK))
        c.drawCircle(w / 2, h / 2, 44 * s, paint(GOLD, 1, stroke=2.5 * s))
        magnifier(c, w / 2 + 3 * s, h / 2 + 3 * s, 46 * s, GOLD_LIGHT, width=5 * s)
    return offscreen(w, h, draw)


def topic_face(label: str, icon: str) -> skia.Image:
    s = RES
    w, h = CW * s, CH * s

    def draw(c):
        _card_base(c, w, h, s)
        _corner(c, "", s, w, h, color=CRIMSON, glyph="diamond")
        cx, cy = w / 2, h * 0.42
        ip = paint(CRIMSON, 1, stroke=4 * s, cap_round=True)
        if icon == "venn":
            c.drawCircle(cx - 22 * s, cy, 34 * s, ip)
            c.drawCircle(cx + 22 * s, cy, 34 * s, ip)
        elif icon == "bars":
            for i, hh in enumerate((30, 62, 44, 80)):
                c.drawRRect(rrect(cx - 54 * s + i * 28 * s, cy + 40 * s - hh * s, cx - 34 * s + i * 28 * s, cy + 40 * s, 3 * s), paint(CRIMSON))
        elif icon == "dots":
            rng = np.random.default_rng(3)
            for _ in range(14):
                dx, dy = rng.normal(0, 26, 2)
                c.drawCircle(cx + dx * s, cy + dy * s, 4.5 * s, paint(CRIMSON, 0.8))
            c.drawLine(cx - 50 * s, cy + 40 * s, cx + 30 * s, cy - 30 * s, ip)
            c.drawCircle(cx + 30 * s, cy - 30 * s, 7 * s, paint(GOLD))
        elif icon == "swap":
            for d, xo in ((-1, -22), (1, 22)):
                c.drawLine(cx + xo * s, cy - 40 * s, cx + xo * s, cy + 40 * s, ip)
                tip = cy - 40 * s if d < 0 else cy + 40 * s
                c.drawLine(cx + xo * s, tip, cx + xo * s - 14 * s, tip - d * 16 * s, ip)
                c.drawLine(cx + xo * s, tip, cx + xo * s + 14 * s, tip - d * 16 * s, ip)
        elif icon == "merge":
            path = skia.Path()
            path.moveTo(cx - 50 * s, cy - 40 * s)
            path.cubicTo(cx - 10 * s, cy - 40 * s, cx - 20 * s, cy, cx + 10 * s, cy)
            path.moveTo(cx - 50 * s, cy + 40 * s)
            path.cubicTo(cx - 10 * s, cy + 40 * s, cx - 20 * s, cy, cx + 10 * s, cy)
            path.moveTo(cx + 10 * s, cy)
            path.lineTo(cx + 52 * s, cy)
            c.drawPath(path, ip)
        elif icon == "check":
            c.drawRRect(rrect(cx - 40 * s, cy - 40 * s, cx + 40 * s, cy + 40 * s, 8 * s), ip)
            path = skia.Path()
            path.moveTo(cx - 20 * s, cy)
            path.lineTo(cx - 4 * s, cy + 18 * s)
            path.lineTo(cx + 24 * s, cy - 20 * s)
            c.drawPath(path, paint(CRIMSON, 1, stroke=7 * s, cap_round=True))
        f = font("black", 30 * s)
        lines = wrap(label, f, w - 50 * s)
        y = h * 0.74 - (len(lines) - 1) * 17 * s
        for line in lines:
            text(c, line, w / 2, y, f, INK)
            y += 34 * s
    return offscreen(w, h, draw)


def draw_card(c: skia.Canvas, face: skia.Image | None, back: skia.Image, x: float, y: float, rot: float = 0.0,
              scale: float = 1.0, face_up: float = 1.0, a: float = 1.0, lift: float = 0.0, glow: float = 0.0,
              shadow: float = 1.0, w: float = CW, h: float = CH) -> None:
    """face_up: 0 shows the back, 1 the face; values between animate a flip."""
    if a <= 0.003 or scale <= 0.001:
        return
    angle = math.pi * (1 - clamp(face_up))
    sx = abs(math.cos(angle))
    showing_face = angle < math.pi / 2 and face is not None
    c.save()
    c.translate(x, y - lift)
    c.rotate(rot)
    c.scale(scale, scale)
    if shadow > 0:
        off = 6 + lift * 0.35
        c.drawRRect(rrect(-w / 2 * sx + off * 0.5, -h / 2 + off, w / 2 * sx + off * 0.5, h / 2 + off, 16),
                    paint((0, 0, 0), 0.42 * a * shadow, blur=7 + lift * 0.12))
    if glow > 0:
        c.drawRRect(rrect(-w / 2 - 6, -h / 2 - 6, w / 2 + 6, h / 2 + 6, 22), paint(GOLD_LIGHT, 0.8 * glow * a, blur=26))
        c.drawRRect(rrect(-w / 2 - 2, -h / 2 - 2, w / 2 + 2, h / 2 + 2, 18), paint(GOLD_LIGHT, 0.9 * glow * a, stroke=3))
    c.scale(max(sx, 0.002), 1)
    draw_image(c, face if showing_face else back, 0, 0, w, h, a)
    c.restore()


def wand(c: skia.Canvas, x: float, y: float, angle: float, a: float = 1.0, length: float = 420) -> None:
    """Magic wand whose white tip sits at (x, y), body extending along angle (degrees)."""
    if a <= 0:
        return
    c.save()
    c.translate(x, y)
    c.rotate(angle)
    c.drawRRect(rrect(8, -9 + 14, length + 8, 9 + 14, 9), paint((0, 0, 0), 0.4 * a, blur=8))
    g = skia.GradientShader.MakeLinear([(0, -9), (0, 9)], [rgba((70, 70, 74), a), rgba((10, 10, 12), a), rgba((40, 40, 44), a)])
    c.drawRRect(rrect(0, -9, length, 9, 9), skia.Paint(AntiAlias=True, Shader=g))
    tip = skia.GradientShader.MakeLinear([(0, -9), (0, 9)], [rgba((255, 255, 255), a), rgba((200, 196, 188), a)])
    c.drawRRect(rrect(0, -9, 64, 9, 9), skia.Paint(AntiAlias=True, Shader=tip))
    c.drawRRect(rrect(length - 64, -9, length, 9, 9), skia.Paint(AntiAlias=True, Shader=tip))
    c.restore()


def header(c: skia.Canvas, kicker: str, title: str, a: float, y: float = 96) -> None:
    if a <= 0:
        return
    dy = (1 - ease_out(a)) * -14
    text(c, kicker, W / 2, y + dy, font("caps", 25), GOLD, a, tracking=6)
    lw = 70
    c.drawLine(W / 2 - measure(kicker, font("caps", 25), 6) / 2 - lw - 24, y - 9 + dy, W / 2 - measure(kicker, font("caps", 25), 6) / 2 - 24, y - 9 + dy, paint(GOLD, 0.6 * a, stroke=1.5))
    c.drawLine(W / 2 + measure(kicker, font("caps", 25), 6) / 2 + 24, y - 9 + dy, W / 2 + measure(kicker, font("caps", 25), 6) / 2 + lw + 24, y - 9 + dy, paint(GOLD, 0.6 * a, stroke=1.5))
    text(c, title, W / 2, y + 74 + dy * 0.5, font("italic", 66), CREAM, a, shadow=6)


def footnote(c: skia.Canvas, s: str, a: float) -> None:
    text(c, s, 64, H - 42, font("ui", 21), CREAM, 0.62 * a, align="l")


def stamp(c: skia.Canvas, label: str, x: float, y: float, p: float, rot: float = -12, color=CRIMSON, size: float = 54) -> None:
    """Rubber stamp landing: p from 0 (above, invisible) to 1 (pressed)."""
    if p <= 0:
        return
    sc = lerp(1.9, 1.0, ease_out(clamp(p * 1.4)))
    a = clamp(p * 3)
    f = font("black", size)
    w = measure(label, f, 4) + 40
    c.save()
    c.translate(x, y)
    c.rotate(rot)
    c.scale(sc, sc)
    c.drawRRect(rrect(-w / 2, -size * 0.78, w / 2, size * 0.42, 8), paint(color, 0.9 * a, stroke=5))
    text(c, label, 0, size * 0.18, f, color, 0.9 * a, tracking=4)
    c.restore()
