"""The seven scenes of "Pick a Card", keyed to spoken word timings."""
from __future__ import annotations

import math
from types import SimpleNamespace

import numpy as np
import skia

from draw import (BLUE_LINE, CREAM, CRIMSON, CRIMSON_DARK, GOLD, GOLD_LIGHT, H, INK, MUTED, PAPER,
                  RESULTS, SMOKE, W, back_image, back_out, blueprint_image, clamp, draw_card, draw_image, ease_in,
                  ease_io, ease_out, fade, felt_image, font, footnote, header, lerp, magnifier, measure, offscreen,
                  paint, play_glyph, prog, result_face, rgba, rrect, sparkle, spotlight, spring, stamp, text,
                  topic_face, wand, wrap)

VPAD = 24
TOPICS = [("Boolean", "venn"), ("BM25", "bars"), ("Embeddings", "dots"),
          ("Reranking", "swap"), ("Hybrid search", "merge"), ("Evaluation", "check")]


def keys(tl) -> SimpleNamespace:
    a, s, e = tl.at, tl.start, tl.end
    k = SimpleNamespace()
    k.end = tl.duration
    k.scenes = tl.scenes
    # pick
    k.pick, k.any, k.got, k.top = a("pick", "Pick"), a("pick", "Any"), s("gotone"), a("ontop", "top")
    k.worry, k.most, k.ontop_end = a("ontop", "Don't"), a("ontop", "most"), e("ontop")
    # force
    k.magicians, k.force, k.feel, k.made = s("force"), a("force", "force"), a("force", "You"), a("force", "made")
    k.allday, k.better, k.thani, k.allday_end = s("allday"), a("allday", "better"), a("allday", "than"), e("allday")
    # trick one
    k.t1, k.take, k.add, k.shaz = s("t1a"), a("t1a", "Take"), a("t1a", "add"), a("t1a", "Shazamblix")
    k.anywhere = a("t1a", "Anywhere")
    k.boolean, k.vanish, k.t1b_end = a("t1b", "Boolean"), a("t1b", "vanish"), e("t1b")
    k.yet, k.here = s("t1c"), a("t1c", "here")
    # trick two
    k.t2, k.about, k.million, k.results = s("t2a"), a("t2a", "About"), a("t2a", "million"), a("t2a", "results")
    k.tryit, k.thousand, k.stops, k.where = a("t2a", "try"), s("t2b"), a("t2b", "stops"), a("t2b", "So")
    # trick three
    k.t3, k.ask, k.sentence, k.thirteen = s("t3a"), a("t3a", "Ask"), a("t3a", "sentence"), a("t3a", "thirteen")
    k.keywords, k.thirtyfive, k.same, k.very = a("t3b", "keywords"), a("t3b", "thirty-five"), s("t3c"), a("t3c", "Very")
    # reveal
    k.real_line, k.real, k.chapter = s("real"), a("real", "real"), a("real", "chapter")
    k.secrets, k.secret_word, k.tools = s("secrets"), a("secrets", "secrets"), a("secrets", "search")
    k.book, k.free = s("book"), a("book", "free")
    k.topics = [a("book", w) for w in ("Boolean", "BM25", "embeddings", "reranking", "hybrid")] + [a("table", "test")]
    k.under = a("table", "under")
    # end
    k.title_words = [(w, a("title", w)) for w in ("How", "Search", "Decides", "What", "You", "See")]
    k.textbook, k.by, k.aaron = a("title", "A"), a("author", "by"), a("author", "Aaron")
    k.oh, k.you, k.pick_word, k.either_end = s("oh"), s("either"), a("either", "pick"), e("either")
    k.zoom_back = k.either_end + 0.55
    return k


# ---------------------------------------------------------------------------
class Film:
    def __init__(self, tl, script):
        self.k = keys(tl)
        self.script = script
        self.felt = felt_image()
        self.blue = blueprint_image()
        self.back = back_image()
        self.faces = [result_face(i + 1, *RESULTS[i]) for i in range(len(RESULTS))]
        self.topic_faces = [topic_face(*tp) for tp in TOPICS]
        self.cover = self._cover()
        rng = np.random.default_rng(42)
        self.smoke = [(rng.uniform(0, 2 * math.pi), rng.uniform(80, 420), rng.uniform(60, 150), rng.uniform(0, 0.25),
                       rng.uniform(1.0, 1.7)) for _ in range(54)]
        self.fountain = [(rng.uniform(0, 1.15), rng.uniform(-640, 640), rng.uniform(-1180, -700), rng.uniform(-720, 720),
                          int(rng.integers(0, len(RESULTS))), rng.random() < 0.55) for _ in range(130)]
        self.pile_jitter = [(rng.uniform(-14, 14), rng.uniform(-10, 10), rng.uniform(-7, 7)) for _ in range(64)]
        self.burst_dirs = rng.uniform(0, 2 * math.pi, 64)
        self.end_still = offscreen(W, H, lambda c: self.end_card(c, self.k.end + 10, static=True))
        self.video_face = self._video_card()

    # ------------------------------------------------------------------
    def frame(self, c: skia.Canvas, t: float) -> None:
        k = self.k
        sc = k.scenes
        if t < sc["reveal"][1] and t < k.under - 0.05:
            c.drawImage(self.felt, 0, 0)
            spotlight(c, W / 2, H * 0.55, 900, self.lamp(t))
        if t < sc["force"][0] + 0.6:
            self.scene_pick(c, t)
        if sc["force"][0] - 0.3 <= t < sc["trick1"][0] + 0.6:
            self.scene_force(c, t)
        if sc["trick1"][0] - 0.2 <= t < sc["trick2"][0] + 0.5:
            self.scene_trick1(c, t)
        if sc["trick2"][0] - 0.2 <= t < sc["trick3"][0] + 0.5:
            self.scene_trick2(c, t)
        if sc["trick3"][0] - 0.2 <= t < sc["reveal"][0] + 0.5:
            self.scene_trick3(c, t)
        if sc["reveal"][0] - 0.2 <= t < k.under + 1.3:
            self.scene_reveal(c, t)
        if t >= k.under + 1.3:
            self.scene_end(c, t)
        if t < 0.35:
            c.drawRect(skia.Rect(0, 0, W, H), paint((0, 0, 0), 1))
        elif t < 0.75:
            c.drawRect(skia.Rect(0, 0, W, H), paint((0, 0, 0), 1 - self.lamp(t)))

    def lamp(self, t: float) -> float:
        if t < 0.35:
            return 0.0
        if t < 0.75:
            p = prog(t, 0.35, 0.75)
            flicker = 0.55 + 0.45 * math.sin(t * 90) ** 2
            return clamp(p * flicker * 1.3)
        return 1.0

    # ------------------------------------------------------------------
    # 1. Pick a card
    FAN_ORDER = [6, 4, 2, 1, 3, 5, 7]  # ranks from left to right; rank 1 sits on top in the middle

    def fan_pose(self, slot: int, p: float, pivot=(W / 2, 1480), radius=880, step=10.0):
        ang = step * slot * p
        x = pivot[0] + radius * math.sin(math.radians(ang))
        y = pivot[1] - radius * math.cos(math.radians(ang))
        return x, y, ang

    def scene_pick(self, c, t):
        k = self.k
        out = fade(t, 0, 0.01, k.magicians - 0.25, k.magicians + 0.25)  # cards gather into the deck
        gather = ease_io(prog(t, k.magicians - 0.25, k.magicians + 0.3))
        ranks = sorted(range(7), key=lambda i: -self.FAN_ORDER[i])  # draw low ranks first
        lift_p = back_out(prog(t, k.top - 0.2, k.top + 0.35))
        settle = 1 - ease_io(prog(t, k.magicians - 0.4, k.magicians))
        dim = 0.42 * prog(t, k.top - 0.2, k.top + 0.3) * settle
        deck_xy = (W / 2, 640)
        for idx in ranks:
            rank = self.FAN_ORDER[idx]
            slot = idx - 3
            order = abs(slot)
            p = ease_out(prog(t, k.pick + 0.02 * order, k.pick + 0.62 + 0.02 * order))
            x, y, ang = self.fan_pose(slot, p)
            x, y = lerp(x, deck_xy[0], gather), lerp(y, deck_xy[1], gather)
            ang = lerp(ang, 0, gather)
            flip = ease_io(prog(t, k.got - 0.15 + 0.07 * order, k.got + 0.25 + 0.07 * order))
            flip = flip * (1 - ease_io(prog(t, k.magicians - 0.25, k.magicians + 0.1))) if rank != 1 else flip
            bob = math.sin(t * 2.2 + slot) * 3 * prog(t, k.pick + 0.7, k.pick + 1.2)
            lift = bob
            glow = 0.0
            rot = ang
            if rank == 1:
                c.drawRect(skia.Rect(0, 0, W, H), paint((0, 0, 0), dim))
                lift += 78 * lift_p * settle
                glow = clamp(lift_p) * settle
                wig = prog(t, k.worry, k.worry + 0.9)
                rot += 4.5 * math.sin(wig * math.pi * 4) * (1 - wig)
            sc = 1.12 + 0.1 * clamp(lift_p) * settle
            if rank != 1 and gather > 0:
                sc = lerp(sc, 1.12, gather)
            draw_card(c, self.faces[rank - 1], self.back, x, y, rot, sc, face_up=flip, lift=lift, glow=glow, a=out if rank != 1 else 1)
        # copy
        a1 = fade(t, k.pick - 0.1, k.pick + 0.35, k.magicians - 0.4, k.magicians)
        text(c, "Pick a card.", W / 2, 170 - 10 * (1 - ease_out(prog(t, k.pick - 0.1, k.pick + 0.4))), font("italic", 86), CREAM, a1, shadow=8)
        a2 = fade(t, k.any - 0.05, k.any + 0.3, k.magicians - 0.4, k.magicians)
        text(c, "Any card.", W / 2, 236, font("italic", 46), GOLD_LIGHT, a2, shadow=5)
        # handwritten aside
        an = fade(t, k.most - 0.15, k.most + 0.25, k.magicians - 0.4, k.magicians)
        if an > 0:
            draw_p = prog(t, k.most - 0.15, k.most + 0.7)
            self.hand_note(c, "rank #1 gets seen first", 1250, 405, draw_p, an, arrow_to=(1050, 470))

    def hand_note(self, c, s, x, y, p, a, arrow_to=None, color=GOLD_LIGHT, size=40):
        f = font("hand", size)
        wdt = measure(s, f)
        c.save()
        c.clipRect(skia.Rect(x - 10, y - size * 1.4, x - 10 + (wdt + 20) * clamp(p * 1.3), y + size))
        text(c, s, x, y, f, color, a, align="l", shadow=4)
        c.restore()
        if arrow_to:
            ap = clamp(p * 1.3 - 0.3)
            if ap > 0:
                sx, sy = x + size * 0.4, y - size * 1.0
                ex, ey = arrow_to
                mx, my = (sx + ex) / 2, min(sy, ey) - 40
                path = skia.Path()
                path.moveTo(sx, sy)
                path.quadTo(mx, my, lerp(sx, ex, ap), lerp(sy, ey, ap))
                c.drawPath(path, paint(color, a, stroke=3.2, cap_round=True))
                if ap >= 1:
                    ang = math.atan2(ey - my, ex - mx)
                    for d in (-0.5, 0.5):
                        c.drawLine(ex, ey, ex - 20 * math.cos(ang + d), ey - 20 * math.sin(ang + d), paint(color, a, stroke=3.2, cap_round=True))

    # ------------------------------------------------------------------
    # 2. The force
    def scene_force(self, c, t):
        k = self.k
        leave = ease_in(prog(t, k.allday - 0.35, k.allday + 0.25))
        a_title = fade(t, k.force - 0.12, k.force + 0.15) * (1 - leave)
        if a_title > 0:
            pop = spring(prog(t, k.force - 0.12, k.force + 0.6), 0.25)
            c.save()
            c.translate(W / 2, 330)
            c.scale(lerp(1.35, 1, pop), lerp(1.35, 1, pop))
            text(c, "THE FORCE", 0, 0, font("black", 150), GOLD, a_title, tracking=10, shadow=10)
            c.restore()
        a_def = fade(t, k.feel - 0.1, k.feel + 0.4) * (1 - leave)
        text(c, "force, n. — a choice that feels free, but was made for you.", W / 2, 412, font("italic", 42), CREAM, a_def, shadow=5)
        # deck at centre, then the ribbon spread where every card is #1
        n = 13
        sp = ease_out(prog(t, k.made - 0.15, k.made + 0.75))
        gone = prog(t, k.allday - 0.45, k.allday + 0.35)
        deck_a = fade(t, k.magicians - 0.2, k.magicians + 0.25)
        for i in range(n):
            x = lerp(W / 2, 330 + i * (1590 - 330) / (n - 1), sp)
            y = lerp(640, 740 - 26 * math.sin(math.pi * i / (n - 1)), sp)
            rot = lerp(0, (i - n / 2) * 1.4, sp)
            gx = ease_in(clamp(gone * 1.6 - i * 0.045)) * -1500
            face = ease_io(prog(t, k.made + 0.15 + i * 0.03, k.made + 0.45 + i * 0.03))
            draw_card(c, self.faces[0], self.back, x + gx, y, rot, lerp(1.12, 1.0, sp), face_up=max(face, 1.0 if i == n - 1 else 0.0), a=deck_a)
        an = fade(t, k.made + 0.7, k.made + 1.0, k.allday - 0.45, k.allday - 0.1)
        if an > 0:
            self.hand_note(c, "every card is #1", 1270, 540, prog(t, k.made + 0.7, k.made + 1.4), an)
        # playbill
        pin = back_out(prog(t, k.allday - 0.15, k.allday + 0.55), 1.1)
        pout = ease_in(prog(t, k.t1 - 0.55, k.t1 - 0.05))
        if pin > 0 and pout < 1:
            self.playbill(c, W / 2, lerp(1500, 585, pin) - 1300 * pout, 1 - pout)
        # the wand droops at "than I do"
        wa = fade(t, k.better - 0.5, k.better - 0.1, k.t1 - 0.5, k.t1 - 0.1)
        if wa > 0:
            droop = ease_io(prog(t, k.thani, k.thani + 0.7))
            ang = lerp(-28, -64, droop) + 3 * math.sin(droop * math.pi * 3) * (1 - droop)
            hx, hy = 1871 + 300 * (1 - ease_out(prog(t, k.better - 0.5, k.better))), 603
            wand(c, hx - 420 * math.cos(math.radians(ang)), hy - 420 * math.sin(math.radians(ang)), ang, wa)

    def playbill(self, c, x, y, a):
        w, h = 1000, 600
        c.save()
        c.translate(x, y)
        c.rotate(-1.2)
        c.drawRRect(rrect(-w / 2 + 10, -h / 2 + 18, w / 2 + 10, h / 2 + 18, 6), paint((0, 0, 0), 0.5 * a, blur=16))
        c.drawRRect(rrect(-w / 2, -h / 2, w / 2, h / 2, 6), paint(PAPER, a))
        c.drawRRect(rrect(-w / 2 + 16, -h / 2 + 16, w / 2 - 16, h / 2 - 16, 4), paint(CRIMSON, a, stroke=3))
        c.drawRRect(rrect(-w / 2 + 24, -h / 2 + 24, w / 2 - 24, h / 2 - 24, 3), paint(CRIMSON, a, stroke=1.2))
        text(c, "YOUR SEARCH ENGINE PRESENTS", 0, -h / 2 + 82, font("caps", 24), INK, a, tracking=5)
        text(c, "THREE ASTONISHING TRICKS", 0, -h / 2 + 194, font("playbill", 108), CRIMSON, a, tracking=2)
        text(c, "performed nightly — and daily — for researchers everywhere", 0, -h / 2 + 250, font("italic", 32), INK, a)
        c.drawLine(-300, -h / 2 + 284, 300, -h / 2 + 284, paint(INK, 0.5 * a, stroke=1.5))
        items = [("Nº 1", "The Impossible Word"), ("Nº 2", "The Bottomless Deck"), ("Nº 3", "The Shrinking Question")]
        for i, (num, name) in enumerate(items):
            yy = -h / 2 + 356 + i * 70
            text(c, num, -250, yy, font("caps", 26), CRIMSON, a, align="l", tracking=3)
            text(c, name, -150, yy, font("bodoni_b", 46), INK, a, align="l")
        for sx in (-410, 410):
            sparkle(c, sx, -h / 2 + 74, 13, a, CRIMSON)
        c.restore()

    # ------------------------------------------------------------------
    # 3. Trick one: the impossible word
    QUERY = "open access citation advantage"
    NONSENSE = " shazamblix"

    def scene_trick1(self, c, t):
        k = self.k
        a = fade(t, k.t1 - 0.3, k.t1 + 0.05, k.t2 - 0.75, k.t2 - 0.35)
        header(c, "TRICK  Nº 1", "The Impossible Word", a)
        if a <= 0:
            return
        # search box
        bp = ease_out(prog(t, k.take - 0.35, k.take + 0.15))
        bx, by, bw, bh = W / 2, 312 - 30 * (1 - bp), 1120, 96
        c.drawRRect(rrect(bx - bw / 2 + 6, by - bh / 2 + 12, bx + bw / 2 + 6, by + bh / 2 + 12, 48), paint((0, 0, 0), 0.4 * a * bp, blur=14))
        c.drawRRect(rrect(bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2, 48), paint(CREAM, a * bp))
        magnifier(c, bx - bw / 2 + 58, by, 40, MUTED, a * bp, width=4.5)
        typed = int(len(self.QUERY) * prog(t, k.take + 0.2, k.take + 1.35))
        q = self.QUERY[:typed]
        f = font("mono", 40)
        x0 = bx - bw / 2 + 104
        text(c, q, x0, by + 14, f, INK, a * bp, align="l")
        nonsense_n = int(len(self.NONSENSE) * prog(t, k.shaz - 0.05, k.shaz + 0.4))
        xn = x0 + f.measureText(q)
        if nonsense_n:
            text(c, self.NONSENSE[:nonsense_n], xn, by + 14, f, CRIMSON, a, align="l")
            wspan = f.measureText(self.NONSENSE)
            sp = prog(t, k.shaz + 0.3, k.shaz + 1.1)
            if 0 < sp < 1:
                for j in range(6):
                    ang = j * math.pi / 3 + 0.4
                    r = 40 + 70 * ease_out(sp)
                    sparkle(c, xn + wspan / 2 + math.cos(ang) * r * 1.8, by + math.sin(ang) * r, 14 * (1 - sp), a)
            caret_x = xn + f.measureText(self.NONSENSE[:nonsense_n])
        else:
            caret_x = xn
        if (t * 2) % 1 < 0.6 and t < k.t1b_end:
            c.drawRect(skia.Rect(caret_x + 3, by - 22, caret_x + 6, by + 22), paint(INK, a * bp))
        an = fade(t, k.shaz + 0.45, k.shaz + 0.7, k.boolean - 0.2, k.boolean + 0.1)
        if an > 0:
            self.hand_note(c, "appears in no paper, anywhere", xn + 40, by + 104, prog(t, k.shaz + 0.45, k.shaz + 1.1), an, arrow_to=(xn + 120, by + 40))
        # rule placard
        rp = ease_out(prog(t, k.boolean - 0.1, k.boolean + 0.35))
        if rp > 0:
            py = 448
            pl, pr = W / 2 - 640, W / 2 + 640
            c.drawRRect(rrect(pl, py - 40, pr, py + 40, 10), paint((10, 30, 24), 0.8 * a * rp))
            c.drawRRect(rrect(pl, py - 40, pr, py + 40, 10), paint(GOLD, a * rp, stroke=2))
            text(c, "BOOLEAN LOGIC:  EVERY WORD MUST MATCH", pl + 32, py + 9, font("caps", 23), GOLD_LIGHT, a * rp, align="l", tracking=2)
            ep = prog(t, k.vanish - 0.1, k.vanish + 0.25)
            c.drawLine(pr - 330, py - 26, pr - 330, py + 26, paint(GOLD, 0.6 * a * ep, stroke=1.5))
            text(c, "expected:", pr - 150, py + 10, font("italic", 34), CREAM, a * ep, align="r")
            zx = pr - 82
            text(c, "0", zx, py + 22, font("black", 64), CRIMSON if t > k.here else GOLD_LIGHT, a * ep)
            strike = ease_out(prog(t, k.here + 0.1, k.here + 0.4))
            if strike > 0:
                c.drawLine(zx - 36, py + 22, lerp(zx - 36, zx + 38, strike), lerp(py + 22, py - 28, strike), paint(CRIMSON, a, stroke=7, cap_round=True))
            if t > k.here + 0.4:
                self.hand_note(c, "still millions", pr - 250, py + 92, prog(t, k.here + 0.4, k.here + 1.0), a, size=36)
        # results row
        poof = k.t1b_end + 1.5  # wand tap during the drum roll
        row_y = 760
        for i in range(5):
            dp = ease_out(prog(t, k.take + 1.25 + i * 0.09, k.take + 1.75 + i * 0.09))
            if dp <= 0:
                continue
            tx = W / 2 + (i - 2) * 222
            x = lerp(W / 2, tx, dp)
            y = lerp(300, row_y, dp)
            hop = 34 * math.sin(math.pi * prog(t, k.here + i * 0.07, k.here + 0.35 + i * 0.07))
            shake = 0.0
            if k.vanish - 0.1 < t < poof:
                shake = 1.6 * math.sin(t * 40 + i) * prog(t, k.vanish, poof)
            draw_card(c, self.faces[i], self.back, x, y - hop, (i - 2) * 2.5 + shake, 0.98, face_up=prog(t, k.take + 1.6 + i * 0.09, k.take + 1.95 + i * 0.09), a=a)
        la = fade(t, k.take + 1.7, k.take + 2.0) * a
        text(c, "RESULTS", W / 2, 572, font("caps", 20), CREAM, 0.7 * la, tracking=6)
        # the wand, the drum roll, the poof
        wa = fade(t, k.t1b_end + 0.1, k.t1b_end + 0.5, k.here + 0.2, k.here + 0.6)
        if wa > 0:
            reach = ease_io(prog(t, k.t1b_end + 0.2, poof - 0.08))
            tap = math.sin(math.pi * prog(t, poof - 0.12, poof + 0.12)) * 26
            retreat = ease_in(prog(t, k.here, k.here + 0.6))
            wand(c, lerp(1900, 1250, reach) + 700 * retreat, lerp(640, 640, reach) + tap, -20, wa)
        self.poof(c, t, poof, W / 2, row_y)
        footnote(c, "A real observation in an academic search tool — Chapter 1, Puzzle 1", fade(t, k.here + 0.3, k.here + 0.8) * a)

    def poof(self, c, t, t0, cx, cy):
        age = t - t0
        if age < 0 or age > 2.2:
            return
        if age < 0.25:
            fl = 1 - age / 0.25
            g = skia.GradientShader.MakeRadial((cx, cy), 700, [rgba((255, 250, 235), 0.85 * fl), rgba((255, 250, 235), 0)])
            c.drawCircle(cx, cy, 700, skia.Paint(Shader=g))
        for ang, dist, r0, delay, life in self.smoke:
            a_ = age - delay * 0.4
            if a_ < 0 or a_ > life:
                continue
            p = a_ / life
            d = dist * ease_out(min(1, a_ / 0.6)) * 1.25
            x = cx + math.cos(ang) * d * 1.5
            y = cy + math.sin(ang) * d * 0.75 - 60 * p
            r = r0 * (0.6 + 1.3 * ease_out(p))
            alpha = (1 - p) ** 1.6 * 0.75 * min(1, a_ / 0.08)
            c.drawCircle(x, y, r, paint(SMOKE, alpha, blur=r * 0.35))

    # ------------------------------------------------------------------
    # 4. Trick two: the bottomless deck
    def scene_trick2(self, c, t):
        k = self.k
        a = fade(t, k.t2 - 0.3, k.t2 + 0.05, k.t3 - 0.75, k.t3 - 0.35)
        header(c, "TRICK  Nº 2", "The Bottomless Deck", a)
        if a <= 0:
            return
        bx, by = 600, 650
        bp = ease_out(prog(t, k.t2 - 0.2, k.t2 + 0.5))
        glow = fade(t, k.where - 0.1, k.where + 0.6)
        self.tunnel(c, bx, by + 40 * (1 - bp), a * bp, t, glow)
        # reported count
        cp = ease_io(prog(t, k.about + 0.15, k.results + 0.1))
        n = int(9_400_000 * cp)
        ca = a * fade(t, k.about - 0.1, k.about + 0.2)
        text(c, f"{n:,}", 1330, 340, font("black", 104), GOLD, ca, shadow=8)
        text(c, "results reported", 1330, 400, font("italic", 38), CREAM, ca)
        # dealing until the hard stop at "A thousand"
        start, stop = k.tryit, k.thousand - 0.16
        N = 44
        pile_x, pile_y = 1330, 720
        dealt = 0
        for i in range(N):
            ti = start + (stop - start) * (i / (N - 1)) ** 0.62
            if t < ti:
                break
            dealt = i + 1
        page = 0 if dealt == 0 else int(round(1 + 99 * ((dealt - 1) / (N - 1))))
        base = max(0, dealt - 7)
        for i in range(base, dealt):
            ti = start + (stop - start) * (i / (N - 1)) ** 0.62
            fl = clamp((t - ti) / 0.28)
            jx, jy, jr = self.pile_jitter[i]
            x = lerp(bx, pile_x + jx, ease_out(fl))
            y = lerp(by, pile_y + jy, ease_out(fl)) - 120 * math.sin(math.pi * fl)
            sc = lerp(0.25, 1.0, ease_out(fl))
            draw_card(c, self.faces[i % 7], self.back, x, y, jr * fl, sc, face_up=fl, a=a)
        if dealt:
            ga = a * fade(t, start, start + 0.2)
            text(c, f"page {page}  ·  {page * 10:,} seen", pile_x, 930, font("italic", 38), CREAM, ga * (1 - prog(t, stop, stop + 0.1)))
        sp = prog(t, stop, stop + 0.3)
        if sp > 0:
            stamp(c, "THE END", pile_x, pile_y - 10, sp, rot=-9, size=70)
            text(c, "1,000 shown", pile_x, 930, font("black", 54), GOLD_LIGHT, a * prog(t, stop, stop + 0.15))
        # the rest
        qa = a * fade(t, k.where - 0.1, k.where + 0.4)
        if qa > 0:
            text(c, "9,399,000", bx, 268, font("black", 64), CREAM, qa, shadow=6)
            text(c, "never shown", bx, 312, font("italic", 36), GOLD_LIGHT, qa)
            for j in range(3):
                ph = (t - k.where) * 0.6 + j / 3
                ph %= 1
                text(c, "?", bx + (j - 1) * 70, by - 40 - 220 * ph, font("black", 54 + 30 * ph), GOLD_LIGHT, qa * math.sin(math.pi * ph))
        footnote(c, "A real observation: a reported count far larger than the list you can view — Chapter 1, Puzzle 2", fade(t, k.where + 0.2, k.where + 0.7) * a)

    def tunnel(self, c, x, y, a, t, glow):
        w, h = 360, 470
        c.drawRRect(rrect(x - w / 2 + 10, y - h / 2 + 22, x + w / 2 + 10, y + h / 2 + 22, 14), paint((0, 0, 0), 0.55 * a, blur=18))
        c.save()
        c.clipRRect(rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 12), doAntiAlias=True)
        c.drawRect(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), paint((4, 4, 6), a))
        vx, vy = x + 10, y - 20
        drift = (t * 0.35) % 1
        for i in range(34, -1, -1):
            d = (i + drift)
            s = 0.86 ** d
            cx, cy = lerp(vx, x, s), lerp(vy, y, s)
            ww, hh = w * s * 0.94, h * s * 0.94
            shade = 0.85 * s ** 0.6
            col = CREAM if i % 2 == 0 else (200, 186, 160)
            c.drawRRect(rrect(cx - ww / 2, cy - hh / 2, cx + ww / 2, cy + hh / 2, 12 * s), paint(col, a * shade, stroke=max(0.8, 5 * s)))
        if glow > 0:
            g = skia.GradientShader.MakeRadial((vx, vy), 260, [rgba(GOLD_LIGHT, 0.55 * glow * a), rgba(GOLD, 0)])
            c.drawRect(skia.Rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), skia.Paint(Shader=g, BlendMode=skia.BlendMode.kPlus))
        c.restore()
        c.drawRRect(rrect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, 12), paint(CRIMSON, a, stroke=16))
        c.drawRRect(rrect(x - w / 2 - 8, y - h / 2 - 8, x + w / 2 + 8, y + h / 2 + 8, 16), paint(GOLD, a, stroke=2.5))
        text(c, "THE DECK", x, y + h / 2 + 52, font("caps", 22), GOLD, a * 0.85, tracking=6)

    # ------------------------------------------------------------------
    # 5. Trick three: the shrinking question
    def scene_trick3(self, c, t):
        k = self.k
        a = fade(t, k.t3 - 0.3, k.t3 + 0.05, k.real_line - 0.75, k.real_line - 0.35)
        header(c, "TRICK  Nº 3", "The Shrinking Question", a)
        if a <= 0:
            return
        hx = (620, 1300)
        hy = 640
        for i, x in enumerate(hx):
            hp = back_out(prog(t, k.t3 - 0.1 + i * 0.12, k.t3 + 0.45 + i * 0.12), 1.2)
            pop = 0.0
            if i == 0:
                pop = math.sin(math.pi * prog(t, k.thirteen - 0.05, k.thirteen + 0.25)) * 0.06
            else:
                pop = math.sin(math.pi * prog(t, k.thirtyfive - 0.05, k.thirtyfive + 0.3)) * 0.1
            self.hat_back(c, x, hy + 60 * (1 - hp), a * clamp(hp), 0.84 * (1 + pop))
        # left: the full sentence
        self.slip(c, t, "Is there an open access citation advantage?", font("georgia_i", 27), hx[0], hy, k.ask + 0.15, k.sentence + 0.45, a)
        self.slip(c, t, "open access citation advantage", font("mono", 28), hx[1], hy, k.keywords - 0.05, k.keywords + 0.75, a)
        # thirteen: a modest little fan rises
        rp = back_out(prog(t, k.thirteen - 0.05, k.thirteen + 0.4))
        c.save()
        c.clipRect(skia.Rect(0, 0, W, hy + 4))
        for j in range(3):
            if rp <= 0:
                break
            draw_card(c, self.faces[j], self.back, hx[0] + (j - 1) * 46 * rp, hy - 30 - 112 * rp, (j - 1) * 12 * rp, 0.55, face_up=1, a=a, shadow=0.6)
        c.restore()
        # fountain
        f0 = k.thirtyfive - 0.08
        for (dt, vx, vy, spin, face, up) in self.fountain:
            age = t - (f0 + dt)
            if age <= 0:
                continue
            x = hx[1] + vx * age
            y = hy - 30 + vy * age + 0.5 * 2600 * age * age
            if y > H + 120 or abs(x - W / 2) > W:
                continue
            draw_card(c, self.faces[face] if up else None, self.back, x, y, spin * age, 0.34, face_up=1.0 if up else 0.0, a=a, shadow=0.0)
        for i, x in enumerate(hx):
            hp = back_out(prog(t, k.t3 - 0.1 + i * 0.12, k.t3 + 0.45 + i * 0.12), 1.2)
            self.hat_front(c, x, hy + 60 * (1 - hp), a * clamp(hp), 0.84)
        # counts
        ca = a * fade(t, k.thirteen - 0.05, k.thirteen + 0.2)
        text(c, "13", hx[0], 330, font("black", 128), GOLD, ca, shadow=8)
        text(c, "results", hx[0], 384, font("italic", 38), CREAM, ca)
        cp = ease_out(prog(t, k.thirtyfive, k.thirtyfive + 0.95))
        ca2 = a * fade(t, k.thirtyfive - 0.05, k.thirtyfive + 0.2)
        text(c, f"≈{int(35300 * cp):,}", hx[1], 330, font("black", 128), GOLD, ca2, shadow=8)
        text(c, "results", hx[1], 384, font("italic", 38), CREAM, ca2)
        # labels under the hats and the comparison
        la = a * fade(t, k.sentence + 0.4, k.sentence + 0.7)
        text(c, "A FULL SENTENCE", hx[0], 932, font("caps", 22), GOLD, la, tracking=5)
        lb = a * fade(t, k.keywords + 0.6, k.keywords + 0.9)
        text(c, "JUST THE KEYWORDS", hx[1], 932, font("caps", 22), GOLD, lb, tracking=5)
        sa = a * fade(t, k.same - 0.1, k.same + 0.25)
        if sa > 0:
            yb = 950
            path = skia.Path()
            path.moveTo(hx[0], yb)
            path.lineTo(hx[0], yb + 22)
            path.lineTo(hx[1], yb + 22)
            path.lineTo(hx[1], yb)
            c.drawPath(path, paint(CREAM, 0.7 * sa, stroke=2.5))
            text(c, "same question", W / 2, yb + 58, font("italic", 34), CREAM, sa)
        va = a * fade(t, k.very - 0.1, k.very + 0.25)
        if va > 0:
            pop = spring(prog(t, k.very - 0.1, k.very + 0.6), 0.3)
            c.save()
            c.translate(W / 2, 600)
            c.scale(lerp(1.4, 1, pop), lerp(1.4, 1, pop))
            text(c, "2,700×", 0, 0, font("black", 66), CRIMSON, va)
            text(c, "the results", 0, 40, font("italic", 30), CREAM, va)
            c.restore()
        footnote(c, "Observed August 2026 in an academic search tool — Chapter 1, Puzzle 3", fade(t, k.same, k.same + 0.5) * a)

    def slip(self, c, t, s, f, hx, hy, t0, t1, a):
        if t < t0 - 0.4 or t > t1 + 0.05:
            return
        appear = ease_out(prog(t, t0 - 0.4, t0))
        p = ease_in(prog(t, t0, t1))
        w = f.measureText(s) + 56
        x = hx + math.sin(p * 9) * 30 * (1 - p)
        y = lerp(470, hy - 20, p)
        sc = lerp(1, 0.4, ease_in(prog(p, 0.7, 1)))
        al = a * appear * (1 - prog(p, 0.85, 1))
        c.save()
        c.translate(x, y - 30 * (1 - appear))
        c.rotate(math.sin(p * 7) * 8 * (1 - p) - 2)
        c.scale(sc, sc)
        c.drawRect(skia.Rect(-w / 2 + 6, -34 + 10, w / 2 + 6, 34 + 10), paint((0, 0, 0), 0.35 * al, blur=10))
        c.drawRect(skia.Rect(-w / 2, -34, w / 2, 34), paint(PAPER, al))
        text(c, s, 0, 10, f, INK, al)
        c.restore()

    def hat_back(self, c, x, y, a, s=1.0):
        if a <= 0:
            return
        c.save()
        c.translate(x, y)
        c.scale(s, s)
        # shadow, crown (upside down: brim on top, crown hanging below)
        c.drawOval(skia.Rect(-210, 230, 230, 300), paint((0, 0, 0), 0.5 * a, blur=18))
        path = skia.Path()
        path.moveTo(-128, 0)
        path.lineTo(-112, 250)
        path.quadTo(0, 285, 112, 250)
        path.lineTo(128, 0)
        path.close()
        g = skia.GradientShader.MakeLinear([(-130, 0), (130, 0)], [rgba((18, 18, 22), a), rgba((58, 58, 66), a), rgba((14, 14, 18), a)], [0, 0.35, 1])
        c.drawPath(path, skia.Paint(AntiAlias=True, Shader=g))
        band = skia.Path()
        band.moveTo(-127, 18)
        band.lineTo(-124, 62)
        band.quadTo(0, 80, 124, 62)
        band.lineTo(127, 18)
        band.quadTo(0, 36, -127, 18)
        c.drawPath(band, paint(CRIMSON, a))
        # brim and opening
        c.drawOval(skia.Rect(-190, -46, 190, 46), paint((22, 22, 26), a))
        c.drawOval(skia.Rect(-190, -46, 190, 46), paint((90, 90, 100), 0.6 * a, stroke=2))
        c.drawOval(skia.Rect(-128, -26, 128, 26), paint((2, 2, 4), a))
        c.restore()

    def hat_front(self, c, x, y, a, s=1.0):
        if a <= 0:
            return
        c.save()
        c.translate(x, y)
        c.scale(s, s)
        # front lip of the brim hides what drops into the hat
        path = skia.Path()
        path.moveTo(-190, 0)
        path.quadTo(-190, 46, 0, 46)
        path.quadTo(190, 46, 190, 0)
        path.quadTo(128, 22, 0, 26)
        path.quadTo(-128, 22, -190, 0)
        c.drawPath(path, paint((24, 24, 28), a))
        c.restore()

    # ------------------------------------------------------------------
    # 6. The reveal: real, secret, the book, under the table
    def scene_reveal(self, c, t):
        k = self.k
        pe = ease_io(prog(t, k.under - 0.05, k.under + 1.25))
        if pe > 0:
            c.drawImage(self.blue, 0, 0)
            self.pipeline(c, 1.0)
            c.save()
            c.translate(0, -pe * (H + 140))
            c.rotate(-1.8 * math.sin(math.pi * pe))
            c.drawImage(self.felt, 0, 0)
            spotlight(c, W / 2, H * 0.55, 900, 1)
        self.reveal_objects(c, t)
        if pe > 0:
            # rolled edge of the cloth
            ea = clamp(pe * 6)
            g = skia.GradientShader.MakeLinear([(0, H - 40), (0, H + 50)], [rgba((40, 110, 84), ea), rgba((96, 160, 128), ea), rgba((24, 74, 56), ea)], [0, 0.5, 1])
            c.drawRect(skia.Rect(-60, H - 30, W + 60, H + 50), skia.Paint(AntiAlias=True, Shader=g))
            c.drawRect(skia.Rect(-60, H + 50, W + 60, H + 160), paint((0, 0, 0), 0.45, blur=30))
            c.restore()

    def reveal_objects(self, c, t):
        k = self.k
        # three placards stamped REAL
        out = ease_in(prog(t, k.secrets - 0.35, k.secrets + 0.15))
        if t < k.secrets + 0.3:
            names = [("Nº 1", "The Impossible Word"), ("Nº 2", "The Bottomless Deck"), ("Nº 3", "The Shrinking Question")]
            for i, (num, name) in enumerate(names):
                p = back_out(prog(t, k.real_line - 0.35 + i * 0.1, k.real_line + 0.2 + i * 0.1), 1.2)
                if p <= 0:
                    continue
                x = 480 + i * 480
                y = lerp(1250, 560, p) + out * 900
                self.placard(c, x, y, num, name, i, clamp(p))
                stamp(c, "REAL", x + 92, y + 66, prog(t, k.real + i * 0.2 - 0.05, k.real + i * 0.2 + 0.2), rot=-14 + i * 5, size=44)
            ra = fade(t, k.chapter - 0.15, k.chapter + 0.2) * (1 - out)
            if ra > 0:
                c.drawRRect(rrect(W / 2 - 360, 812, W / 2 + 360, 872, 30), paint(GOLD, 0.92 * ra))
                text(c, "All three: Chapter 1, “The retrieval problem”", W / 2, 853, font("italic", 34), INK, ra)
        # secrets: a sealed envelope and a black box
        gone = ease_in(prog(t, k.book - 0.3, k.book + 0.2))
        ep = back_out(prog(t, k.secrets + 0.05, k.secrets + 0.6), 1.1)
        if ep > 0 and gone < 1:
            self.envelope(c, 640, lerp(1300, 600, ep) - gone * 1100, clamp(ep), t)
            stamp(c, "SECRET", 640, lerp(1300, 600, ep) - gone * 1100 + 110, prog(t, k.secret_word - 0.05, k.secret_word + 0.2), rot=-8)
        bp = back_out(prog(t, k.tools - 0.1, k.tools + 0.45), 1.1)
        if bp > 0 and gone < 1:
            self.black_box(c, 1290, lerp(1300, 620, bp) - gone * 1100, clamp(bp), t)
        # the book and the topic cards
        bk = back_out(prog(t, k.book - 0.05, k.book + 0.55), 1.15)
        if bk > 0:
            bx, by = 560, 590
            c.save()
            c.translate(bx, by)
            c.rotate(lerp(-14, -3, bk))
            c.scale(lerp(0.6, 1, bk), lerp(0.6, 1, bk))
            c.drawRRect(rrect(-200 + 14, -280 + 22, 200 + 14, 280 + 22, 8), paint((0, 0, 0), 0.55 * bk, blur=20))
            glow = fade(t, k.free - 0.1, k.free + 0.2, k.free + 0.8, k.free + 1.6)
            if glow > 0:
                c.drawRRect(rrect(-214, -294, 214, 294, 16), paint(GOLD_LIGHT, 0.7 * glow, blur=30))
            draw_image(c, self.cover, 0, 0, 400, 560, clamp(bk))
            c.restore()
            fp = prog(t, k.free - 0.05, k.free + 0.25)
            if fp > 0:
                c.save()
                c.translate(bx + 175, by - 255)
                sc = lerp(1.8, 1, ease_out(fp))
                c.scale(sc, sc)
                c.rotate(12)
                c.drawCircle(0, 0, 62, paint(GOLD, clamp(fp * 3)))
                c.drawCircle(0, 0, 54, paint(CRIMSON_DARK, clamp(fp * 3), stroke=2))
                text(c, "FREE", 0, 12, font("black", 34), CRIMSON_DARK, clamp(fp * 3), tracking=2)
                c.restore()
        for i, tt in enumerate(k.topics):
            p = ease_out(prog(t, tt - 0.12, tt + 0.33))
            if p <= 0:
                continue
            col, row = i % 3, i // 3
            tx, ty = 1110 + col * 250, 430 + row * 340
            x = lerp(620, tx, p)
            y = lerp(560, ty, p) - 90 * math.sin(math.pi * p)
            draw_card(c, self.topic_faces[i], self.back, x, y, lerp(-30, (col - 1) * 3, p), 0.92, face_up=ease_io(prog(t, tt, tt + 0.35)))

    def placard(self, c, x, y, num, name, kind, a):
        w, h = 400, 250
        c.save()
        c.translate(x, y)
        c.drawRRect(rrect(-w / 2 + 8, -h / 2 + 14, w / 2 + 8, h / 2 + 14, 12), paint((0, 0, 0), 0.45 * a, blur=12))
        c.drawRRect(rrect(-w / 2, -h / 2, w / 2, h / 2, 12), paint(CREAM, a))
        c.drawRRect(rrect(-w / 2 + 8, -h / 2 + 8, w / 2 - 8, h / 2 - 8, 8), paint(CRIMSON, 0.5 * a, stroke=1.6))
        text(c, num, 0, -h / 2 + 46, font("caps", 20), CRIMSON, a, tracking=4)
        text(c, name, 0, -h / 2 + 92, font("bodoni_b", 32), INK, a)
        ix = -78
        if kind == 0:
            c.drawRRect(rrect(ix - 92, 30, ix + 92, 72, 21), paint(INK, 0.5 * a, stroke=2))
            text(c, "… shazamblix", ix - 74, 58, font("mono", 20), CRIMSON, a, align="l")
        elif kind == 1:
            for j in range(6):
                s = 0.78 ** j
                c.drawRect(skia.Rect(ix - 46 * s, 54 - 40 * s, ix + 46 * s, 54 + 40 * s), paint(INK, a * (1 - j * 0.12), stroke=2))
        else:
            c.drawOval(skia.Rect(ix - 62, 18, ix + 62, 38), paint(INK, a))
            c.drawRect(skia.Rect(ix - 40, 28, ix + 40, 92), paint(INK, a))
        c.restore()

    def envelope(self, c, x, y, a, t):
        w, h = 470, 300
        c.save()
        c.translate(x, y)
        c.rotate(-4)
        c.drawRect(skia.Rect(-w / 2 + 10, -h / 2 + 18, w / 2 + 10, h / 2 + 18), paint((0, 0, 0), 0.45 * a, blur=14))
        c.drawRect(skia.Rect(-w / 2, -h / 2, w / 2, h / 2), paint(PAPER, a))
        flap = skia.Path()
        flap.moveTo(-w / 2, -h / 2)
        flap.lineTo(0, 30)
        flap.lineTo(w / 2, -h / 2)
        c.drawPath(flap, paint(MUTED, 0.7 * a, stroke=2))
        c.drawLine(-w / 2, h / 2, -40, 0, paint(MUTED, 0.35 * a, stroke=1.5))
        c.drawLine(w / 2, h / 2, 40, 0, paint(MUTED, 0.35 * a, stroke=1.5))
        c.drawCircle(0, 30, 44, paint(CRIMSON, a))
        c.drawCircle(0, 30, 34, paint(CRIMSON_DARK, a, stroke=3))
        magnifier(c, 3, 33, 36, GOLD_LIGHT, a, width=4)
        text(c, "how the trick is done", 0, -h / 2 - 26, font("hand", 38), GOLD_LIGHT, a, shadow=4)
        c.restore()

    def black_box(self, c, x, y, a, t):
        s = 300
        d = 70
        c.save()
        c.translate(x, y)
        c.drawOval(skia.Rect(-s / 2 - 20, s / 2 - 20, s / 2 + d + 40, s / 2 + 40), paint((0, 0, 0), 0.55 * a, blur=18))
        top = skia.Path()
        top.moveTo(-s / 2, -s / 2)
        top.lineTo(-s / 2 + d, -s / 2 - d * 0.7)
        top.lineTo(s / 2 + d, -s / 2 - d * 0.7)
        top.lineTo(s / 2, -s / 2)
        top.close()
        c.drawPath(top, paint((52, 52, 58), a))
        side = skia.Path()
        side.moveTo(s / 2, -s / 2)
        side.lineTo(s / 2 + d, -s / 2 - d * 0.7)
        side.lineTo(s / 2 + d, s / 2 - d * 0.7)
        side.lineTo(s / 2, s / 2)
        side.close()
        c.drawPath(side, paint((8, 8, 10), a))
        g = skia.GradientShader.MakeLinear([(-s / 2, -s / 2), (s / 2, s / 2)], [rgba((40, 40, 46), a), rgba((14, 14, 16), a)])
        c.drawRect(skia.Rect(-s / 2, -s / 2, s / 2, s / 2), skia.Paint(AntiAlias=True, Shader=g))
        # padlock
        c.drawRRect(rrect(-38, -6, 38, 56, 8), paint(GOLD, a))
        shackle = skia.Path()
        shackle.moveTo(-24, -6)
        shackle.lineTo(-24, -30)
        shackle.quadTo(-24, -54, 0, -54)
        shackle.quadTo(24, -54, 24, -30)
        shackle.lineTo(24, -6)
        c.drawPath(shackle, paint(GOLD, a, stroke=9))
        c.drawCircle(0, 20, 8, paint((40, 30, 10), a))
        c.drawRect(skia.Rect(-3, 22, 3, 40), paint((40, 30, 10), a))
        text(c, "how the tool ranks", 30, -s / 2 - d * 0.7 - 30, font("hand", 38), GOLD_LIGHT, a, shadow=4)
        for j in range(3):
            ph = ((t - self.k.tools) * 0.5 + j / 3) % 1
            text(c, "?", s / 2 + 70 + j * 26, -40 - 160 * ph, font("black", 40 + 20 * ph), GOLD_LIGHT, a * math.sin(math.pi * ph))
        c.restore()

    def pipeline(self, c, a):
        stages = ["QUERY", "INDEX", "CANDIDATES", "RANKING", "RERANKING", "RESULTS"]
        f = font("caps", 20)
        widths = [measure(s, f, 3) + 52 for s in stages]
        gap = 54
        total = sum(widths) + gap * (len(stages) - 1)
        x = W / 2 - total / 2
        y = 560
        lp = paint(BLUE_LINE, 0.9 * a, stroke=2.2)
        centers = []
        for s, w in zip(stages, widths):
            c.drawRRect(rrect(x, y - 38, x + w, y + 38, 6), lp)
            text(c, s, x + w / 2, y + 8, f, (210, 230, 255), a, tracking=3)
            centers.append((x, x + w))
            x += w + gap
        for (a0, a1), (b0, b1) in zip(centers, centers[1:]):
            c.drawLine(a1 + 8, y, b0 - 8, y, lp)
            c.drawLine(b0 - 8, y, b0 - 20, y - 8, lp)
            c.drawLine(b0 - 8, y, b0 - 20, y + 8, lp)
        # evaluation loop
        x0, x1 = (centers[0][0] + centers[0][1]) / 2, (centers[-1][0] + centers[-1][1]) / 2
        path = skia.Path()
        path.moveTo(x1, y + 40)
        path.cubicTo(x1, y + 170, x0, y + 170, x0, y + 40)
        dash = skia.Paint(AntiAlias=True, Color=rgba(GOLD_LIGHT, 0.9 * a), Style=skia.Paint.kStroke_Style, StrokeWidth=2.2,
                          PathEffect=skia.DashPathEffect.Make([12, 8], 0))
        c.drawPath(path, dash)
        text(c, "TEST IT YOURSELF", W / 2, y + 160, font("caps", 20), GOLD_LIGHT, a, tracking=4)
        text(c, "THE MACHINERY UNDER THE TABLE", W / 2, y - 120, font("caps", 22), (210, 230, 255), 0.8 * a, tracking=7)

    def _cover(self) -> skia.Image:
        w, h = 800, 1120

        def draw(c):
            c.drawRRect(rrect(0, 0, w, h, 14), paint((22, 30, 40)))
            g = skia.GradientShader.MakeLinear([(0, 0), (60, 0)], [rgba((0, 0, 0), 0.55), rgba((0, 0, 0), 0)])
            c.drawRect(skia.Rect(0, 0, 60, h), skia.Paint(Shader=g))
            c.drawRect(skia.Rect(46, 46, w - 46, h - 46), paint(GOLD, 1, stroke=4))
            c.drawRect(skia.Rect(60, 60, w - 60, h - 60), paint(GOLD, 0.6, stroke=1.5))
            text(c, "AARON TAY", w / 2, 160, font("caps", 34), GOLD, tracking=10)
            y = 300
            for line in ("How Search", "Decides", "What You See"):
                text(c, line, w / 2, y, font("black", 96), CREAM)
                y += 112
            # emblem: a card with a magnifier
            c.save()
            c.translate(w / 2, 790)
            c.rotate(-8)
            c.drawRRect(rrect(-90, -126, 90, 126, 12), paint(CREAM))
            c.drawRRect(rrect(-80, -116, 80, 116, 8), paint(CRIMSON, 1, stroke=2.5))
            magnifier(c, 6, 6, 110, CRIMSON, width=12)
            c.restore()
            sub = "A librarian’s guide to Boolean search, BM25, embeddings, reranking, and the retrieval pipelines behind hybrid and agentic search"
            f = font("italic", 30)
            y = 980
            for line in wrap(sub, f, w - 180):
                text(c, line, w / 2, y, f, (220, 210, 190))
                y += 36
        return offscreen(w, h, draw)

    # ------------------------------------------------------------------
    # 7. End card and the last trick
    def end_card(self, c, t, static=False):
        k = self.k
        c.drawImage(self.blue, 0, 0)
        dim = 0.0 if static else lerp(1.0, 0.0, ease_io(prog(t, k.title_words[0][1] - 0.2, k.title_words[0][1] + 0.5)))
        self.pipeline(c, 0.16 + 0.84 * dim)
        g = skia.GradientShader.MakeRadial((W / 2, 520), 900, [rgba((8, 18, 38), 0.82), rgba((8, 18, 38), 0.35)])
        veil = 1.0 if static else ease_io(prog(t, k.title_words[0][1] - 0.2, k.title_words[0][1] + 0.5))
        p = skia.Paint(Shader=g)
        p.setAlphaf(veil)
        c.drawRect(skia.Rect(0, 0, W, H), p)
        f = font("black", 124)
        lines = [k.title_words[:3], k.title_words[3:]]
        ys = [440, 580]
        for line, y in zip(lines, ys):
            words = [w for w, _ in line]
            total = sum(f.measureText(w) for w in words) + f.measureText(" ") * (len(words) - 1)
            x = W / 2 - total / 2
            for w, tw in line:
                pp = 1.0 if static else ease_out(prog(t, tw - 0.06, tw + 0.32))
                text(c, w, x, y + 22 * (1 - pp), f, CREAM, pp, align="l", shadow=10)
                x += f.measureText(w + " ")
        ra = 1.0 if static else ease_out(prog(t, k.title_words[-1][1], k.title_words[-1][1] + 0.5))
        c.drawLine(W / 2 - 260 * ra, 636, W / 2 + 260 * ra, 636, paint(GOLD, 0.9 * ra, stroke=2))
        fi = font("italic", 54)
        part1, part2 = "A free textbook", " by Aaron Tay"
        total = fi.measureText(part1 + part2)
        x = W / 2 - total / 2
        a1 = 1.0 if static else ease_out(prog(t, k.textbook - 0.05, k.textbook + 0.35))
        a2 = 1.0 if static else ease_out(prog(t, k.by - 0.05, k.by + 0.35))
        text(c, part1, x, 718, fi, GOLD_LIGHT, a1, align="l", shadow=5)
        text(c, part2, x + fi.measureText(part1), 718, fi, GOLD_LIGHT, a2, align="l", shadow=5)
        ua = 1.0 if static else ease_out(prog(t, k.aaron + 0.45, k.aaron + 0.9))
        url = self.script["display_url"]
        fu = font("mono", 30)
        uw = fu.measureText(url) + 70
        c.drawRRect(rrect(W / 2 - uw / 2, 780, W / 2 + uw / 2, 842, 31), paint(GOLD, 0.95 * ua, stroke=2))
        text(c, url, W / 2, 821, fu, CREAM, ua)
        fc = font("caps", 20)
        left, right = "READ IT FREE ONLINE", "CC BY 4.0"
        wl, wr = measure(left, fc, 5), measure(right, fc, 5)
        x0 = W / 2 - (wl + wr + 60) / 2
        text(c, left, x0, 902, fc, GOLD, 0.85 * ua, align="l", tracking=5)
        c.drawCircle(x0 + wl + 30, 895, 3.5, paint(GOLD, 0.85 * ua))
        text(c, right, x0 + wl + 60, 902, fc, GOLD, 0.85 * ua, align="l", tracking=5)

    def _video_card(self) -> skia.Image:
        """The end card itself as a 16:9 playing card face."""
        w, pad = 960, VPAD
        h = round((w - 2 * pad) * 9 / 16) + 2 * pad

        def draw(c):
            c.drawRRect(rrect(0, 0, w, h, 26), paint(CREAM))
            draw_image(c, self.end_still, w / 2, h / 2, w - 2 * pad, h - 2 * pad)
            c.drawRRect(rrect(pad - 1, pad - 1, w - pad + 1, h - pad + 1, 4), paint(CRIMSON, 0.9, stroke=3))
            c.drawRRect(rrect(pad + 14, pad + 14, pad + 98, pad + 70, 10), paint(CREAM))
            text(c, "1", pad + 42, pad + 59, font("bodoni_b", 44), CRIMSON)
            play_glyph(c, pad + 76, pad + 42, 30, CRIMSON)
        return offscreen(w, h, draw)

    def scene_end(self, c, t):
        k = self.k
        shrink = ease_io(prog(t, k.oh - 0.05, k.oh + 0.75))
        grow = ease_io(prog(t, k.zoom_back, k.zoom_back + 0.95))
        m = shrink * (1 - grow)  # 0 = full-screen end card, 1 = a card on the table
        if m <= 0.001:
            self.end_card(c, t)
            if t > k.zoom_back:
                c.drawImage(self.end_still, 0, 0)
            return
        # table returns underneath
        c.drawImage(self.felt, 0, 0)
        spotlight(c, W / 2, H * 0.55, 900, 1)
        others = [(-3, 6), (-2, 4), (-1, 2), (1, 3), (2, 5), (3, 7)]
        oa = fade(t, k.oh + 0.2, k.oh + 0.6) * (1 - grow)
        for slot, _ in sorted(others, key=lambda s: -abs(s[0])):
            x, y, ang = self.fan_pose(slot, 1.0, pivot=(W / 2, 1600), radius=1000, step=9.0)
            c.save()
            c.translate(x, y + 40)
            c.rotate(ang)
            c.rotate(90)
            draw_card(c, None, self.back, 0, 0, 0, 1.25, face_up=0, a=oa)
            c.restore()
        # our card
        vw, vh = self.video_face.width(), self.video_face.height()
        cw, ch = 480, 480 * vh / vw
        tx, ty = W / 2, 600 - 50 * ease_out(prog(t, k.oh + 0.5, k.oh + 0.9)) * (1 - grow)
        x = lerp(W / 2, tx, m)
        y = lerp(H / 2, ty, m)
        wcur = lerp(W * vw / (vw - 2 * VPAD), cw, m)
        hcur = lerp(H * vh / (vh - 2 * VPAD), ch, m)
        glow = fade(t, k.pick_word - 0.1, k.pick_word + 0.2, k.zoom_back - 0.2, k.zoom_back + 0.2)
        if m > 0.05:
            c.drawRRect(rrect(x - wcur / 2 + 10, y - hcur / 2 + 16, x + wcur / 2 + 10, y + hcur / 2 + 16, 14), paint((0, 0, 0), 0.5 * m, blur=14))
        if glow > 0:
            c.drawRRect(rrect(x - wcur / 2 - 8, y - hcur / 2 - 8, x + wcur / 2 + 8, y + hcur / 2 + 8, 22), paint(GOLD_LIGHT, 0.8 * glow, blur=26))
        draw_image(c, self.video_face, x, y, wcur, hcur)
        # sparkles on "pick"
        sp = prog(t, k.pick_word, k.pick_word + 0.9)
        if 0 < sp < 1:
            for j, ang in enumerate(self.burst_dirs[:12]):
                r = 140 + 200 * ease_out(sp) + j * 6
                sparkle(c, x + math.cos(ang) * r, y + math.sin(ang) * r * 0.6, 18 * (1 - sp), 1 - sp)
        wa = fade(t, k.you - 0.4, k.you - 0.05, k.zoom_back - 0.3, k.zoom_back)
        if wa > 0:
            tap = math.sin(math.pi * prog(t, k.pick_word - 0.1, k.pick_word + 0.15)) * 22
            wand(c, x + 200 + tap * 0.6, y - 40 + tap, -32, wa)
        qa = fade(t, k.oh - 0.05, k.oh + 0.3, k.zoom_back - 0.25, k.zoom_back + 0.1)
        text(c, "Oh, and this video?", W / 2, 190, font("italic", 64), CREAM, qa * (1 - prog(t, k.you - 0.2, k.you)), shadow=6)
        ya = fade(t, k.you - 0.1, k.you + 0.25, k.zoom_back - 0.25, k.zoom_back + 0.1)
        text(c, "You didn’t pick it either.", W / 2, 190, font("italic", 72), GOLD_LIGHT, ya, shadow=8)
