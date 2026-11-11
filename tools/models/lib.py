"""ia_industries model generator v2 (0.3.0): 2 px per model unit, model scale, seats/mounts, custom animations, z-fight check."""
import json, uuid, base64, io, math
from PIL import Image
import oldlib
from oldlib import hsh, sh, P, PROPS

D = 2                       # texture pixels per model unit (0.5.0: 2 again, like the stock warship, but with painted-in texture detail)
FACES = ['north', 'south', 'east', 'west', 'up', 'down']
PROPS['blade2w'] = (2, .10, .21, .06); PROPS['blade2wb'] = (2, .10, .21, .06, math.pi / 2); PROPS['fan3'] = (3, .10, .30, .38); PROPS['paddle6'] = (6, .07, .16, .0)
# straight helicopter blades (like the cargo copter's prop2), sized for bigger rotors
PROPS['heli4'] = (4, .03, .075, 0.0); PROPS['heli2'] = (2, .022, .05, 0.0); PROPS['heli2b'] = (2, .022, .05, 0.0, math.pi / 2); PROPS['heli3'] = (3, .025, .06, 0.0); PROPS['heli3b'] = (3, .025, .06, 0.0, math.pi / 3)
FLAT = set(PROPS) | {'cog', 'net', 'flag'}
PERFACE = ('engine', 'wheel', 'vault', 'tank', 'dash', 'crate')
GREY = [(170, 170, 164), (146, 146, 141), (124, 124, 120), (100, 100, 98), (76, 76, 76)]
COP = [(250, 176, 132), (232, 142, 104), (206, 112, 80), (170, 86, 62), (128, 62, 48)]
BR = P['brass']
SPR = [(118, 86, 50), (104, 75, 44), (90, 64, 38), (72, 51, 30), (56, 40, 24)]       # spruce
DSP = [(104, 74, 44), (90, 63, 37), (76, 53, 31), (60, 42, 25), (46, 32, 20)]         # dark spruce (warship hull)


def andes(x, y, seed):
    k = hsh(x // 2, y // 2, seed) % 12
    c = GREY[1] if k < 6 else GREY[0] if k < 8 else GREY[2]
    return sh(c, 4) if hsh(x, y, seed, 5) % 11 == 0 else c


def frame(x, y, w, h, seed, t=3):
    """andesite casing border, t px thick, bevelled; returns None inside."""
    e = min(x, y, w - 1 - x, h - 1 - y)
    if e >= t: return None
    c = andes(x, y, seed)
    if e == 0: c = GREY[0] if (x == 0 or y == 0) and x != w - 1 and y != h - 1 else GREY[4]
    elif e == t - 1: c = GREY[3] if (x == t - 1 or y == t - 1) else GREY[1]
    cx, cy = min(x, w - 1 - x), min(y, h - 1 - y)
    if t >= 3 and cx == 1 and cy == 1: c = (58, 58, 60)                              # corner bolt
    return c


def planks(a, b, seed, pal=SPR, rh=6):
    row, r = b // rh, b % rh
    Lb = 20 + hsh(row, seed) % 14; off = hsh(row, seed, 3) % Lb; seg = (a + off) // Lb; k = (a + off) % Lb
    tone = (hsh(row, seg, seed) % 5 - 2) * 4
    c = sh(pal[1], tone)
    if r == 0: c = sh(pal[0], tone)
    elif r == rh - 1: c = sh(pal[4], tone // 2)
    elif r == rh - 2: c = sh(pal[2], tone)
    if k == 0 and r != rh - 1: c = sh(pal[3], tone // 2)
    elif k in (2, Lb - 2) and r in (1, rh - 3): c = pal[4]                           # nails beside each joint
    elif hsh(a // 5, b, seed) % 7 == 0 and 0 < r < rh - 2: c = sh(pal[2], tone)     # grain
    elif hsh(a // 3, b, seed, 7) % 19 == 0 and 0 < r < rh - 1: c = sh(pal[0], tone + 5)
    return c


def boards(a, b, seed, pal=DSP, bw=4):
    """vertical boards across the panel length"""
    col, r = a // bw, a % bw
    tone = (hsh(col, seed) % 5 - 2) * 3
    c = sh(pal[1], tone)
    if r == 0: c = sh(pal[0], tone)
    elif r == bw - 1: c = pal[4]
    elif hsh(col, b // 7, seed) % 5 == 0: c = sh(pal[2], tone)
    if hsh(col, b // 9, seed, 3) % 13 == 0 and r == 1: c = pal[3]
    return c


def fan(x, y, w, h, ring):
    e = min(x, y, w - 1 - x, h - 1 - y); cx, cy = (w - 1) / 2, (h - 1) / 2; dx, dy = x - cx, y - cy
    r = math.hypot(dx, dy); R = min(cx, cy) - 3; ang = math.atan2(dy, dx)
    if e < 3:
        c = ring[1] if e == 1 else ring[4] if e == 0 else ring[3]
        if e == 1 and min(x, w - 1 - x) == 1 and min(y, h - 1 - y) == 1: c = ring[0]
        return c
    c = (30, 30, 34)
    if r <= R:
        c = (44, 44, 48)
        if math.cos(ang * 8 + r * 0.12) > 0.25 and r > R * 0.22: c = (112, 112, 116) if math.cos(ang * 8 + r * 0.12) > 0.7 else (84, 84, 88)
        if abs(r - R) < 1.0: c = (140, 140, 142)
        if r <= R * 0.22: c = (150, 150, 152) if r > R * 0.1 else (70, 70, 74)
    return c


def paint_v2(mat, w, h, face):
    """0.3.0 painters (2 px per unit); still used for dash / crate / preview player"""
    if mat in FLAT or mat in ('chest', 'vault', 'wheel', 'latch'):
        if mat in FLAT: return oldlib.paint(mat, w, h, face)
        im = oldlib.paint(mat, max(1, (w + 1) // 2), max(1, (h + 1) // 2), face).resize((2 * ((w + 1) // 2), 2 * ((h + 1) // 2)), Image.NEAREST).crop((0, 0, w, h))
        px = im.load()
        for y in range(h):
            for x in range(w):
                c = px[x, y]
                if c[3] and hsh(x, y, w) % 5 == 0: px[x, y] = sh(c[:3], -7 if (x + y) % 2 else 6) + (255,)
        return im
    im = Image.new('RGBA', (w, h)); px = im.load(); horiz = w >= h; seed = hsh(w, h, len(mat), ord(mat[0]))
    for y in range(h):
        for x in range(w):
            a, b = (x, y) if horiz else (y, x); L, W_ = (w, h) if horiz else (h, w)
            e = min(x, y, w - 1 - x, h - 1 - y); m = min(w, h)
            if mat == 'wood':
                c = planks(a, b, seed)
                if L >= 20:
                    if a < 3 or a >= L - 3:
                        c = andes(x, y, seed)
                        if a in (0, L - 1): c = GREY[4]
                        if a in (2, L - 3): c = GREY[0] if a == 2 else GREY[3]
                        if b % 8 == 3 and a in (1, L - 2): c = (58, 58, 60)
                    elif a in (3, L - 4): c = SPR[4]
            elif mat == 'casing':
                c = frame(x, y, w, h, seed, 3 if m > 8 else m)
                if c is None:
                    c = planks(a, b, seed, rh=5)
                    if e == 3: c = SPR[4]
                    elif e == 4 and (x == 4 or y == 4): c = sh(c, -10)
            elif mat == 'hullw':
                n = max(1, round(L / 32)); pl = L / n; pa = a - int(a // pl * pl + 1e-6); pn = int(round(pl))
                if m <= 6:
                    c = andes(x, y, seed)
                    if b == 0: c = GREY[0]
                    if b == W_ - 1: c = GREY[4]
                else:
                    c = frame(pa if horiz else b, b if horiz else pa, pn if horiz else W_, W_ if horiz else pn, seed, 3)
                    if c is None:
                        pe = min(pa, pn - 1 - pa, b, W_ - 1 - b)
                        c = boards(x, y, seed)
                        if pe == 3: c = DSP[4]
                        elif pe == 4 and b == 4: c = sh(c, -8)
            elif mat == 'panel':
                eo = e
                if m <= 4: c = BR[1] if b == 0 else BR[3] if b == W_ - 1 else BR[2]
                elif eo < 2: c = (BR[0] if eo == 1 else BR[1]) if (x <= 1 or y <= 1) and x < w - 2 and y < h - 2 else (BR[2] if eo == 1 else BR[3])
                else:
                    n = max(1, round(L / 24)); pl = (L - 4) / n; pa = (a - 2) - int((a - 2) // pl * pl + 1e-6); pn = int(round(pl)); bb = b - 2; Wn = W_ - 4
                    pe = min(pa, pn - 1 - pa, bb, Wn - 1 - bb)
                    t = bb / max(1, Wn - 1); g = int(20 - 16 * t)
                    c = (36 + g, 40 + g, 48 + g)
                    if pe == 0: c = (20, 22, 28)
                    elif pe == 1: c = (78, 84, 96) if (bb == 1 or pa == 1) else (30, 32, 40)
                    elif (pa - bb) % 11 == 0 and pe > 2 and bb < Wn * 0.6: c = (60 + g, 66 + g, 78 + g)        # gloss streak
                    if m >= 12 and pe == 3 and min(pa, pn - 1 - pa) == 3 and min(bb, Wn - 1 - bb) == 3: c = (128, 136, 148)   # rivets
            elif mat == 'engine':                                               # copper casing engine (cargo)
                if face == 'south': c = fan(x, y, w, h, COP)
                else:
                    c = COP[1] if hsh(x // 2, y // 2, seed) % 6 else COP[0]
                    if e == 0: c = COP[4]
                    elif e == 1: c = COP[0] if (x == 1 or y == 1) else COP[3]
                    elif e == 4 and m >= 14: c = COP[3] if (x == 4 or y == 4) else COP[0]
                    elif e == 5 and m >= 14: c = COP[2]
                    cx, cy = min(x, w - 1 - x), min(y, h - 1 - y)
                    if m >= 14 and cx == 2 and cy == 2: c = COP[4]
                    if face in ('east', 'west') and m >= 16 and e >= 7:          # vent slats
                        c = (92, 92, 96) if x % 3 == 0 else (64, 64, 68) if x % 3 == 1 else (44, 44, 48)
                        if e == 7: c = COP[4]
            elif mat == 'tank':                                                 # copper fluid tank (warship class), axis along z
                if face == 'south': c = fan(x, y, w, h, COP)
                elif face == 'north':
                    c = COP[1]
                    if e == 0: c = COP[4]
                    elif e == 1: c = COP[0] if (x == 1 or y == 1) else COP[3]
                    elif m >= 16 and e == 5: c = COP[3] if (x == 5 or y == 5) else COP[0]
                    cx, cy = min(x, w - 1 - x), min(y, h - 1 - y)
                    if m >= 16 and cx == 7 and cy == 7: c = COP[4]
                    r = math.hypot(x - (w - 1) / 2, y - (h - 1) / 2)
                    if m >= 16 and r < 3: c = COP[4] if r > 1.8 else GREY[1]
                else:
                    al, ac, AL, AC = (x, y, w, h) if face in ('east', 'west') else (y, x, h, w)
                    t = ac / max(1, AC - 1); k = abs(t - 0.3)
                    c = COP[0] if k < 0.08 else COP[1] if k < 0.26 else COP[2] if k < 0.48 else COP[3]
                    if ac in (0, AC - 1): c = COP[4]
                    m16 = al % 16
                    if m16 in (0, 1): c = COP[3] if m16 == 0 else (COP[0] if k < 0.26 else COP[1])
                    if m16 == 15: c = COP[4] if k > 0.26 else COP[3]
                    if m16 == 1 and ac % 5 == 2: c = COP[4]                      # rivets on the hoops
                    if al in (0, AL - 1): c = COP[4]
            elif mat in ('sail', 'sailc'):
                clean = mat == 'sailc'; ps = 40 if clean else 32
                rim = [(196, 196, 192), (168, 168, 164)] if clean else [P['tan'][1], P['tan'][2]]
                if m <= 4:
                    c = rim[0] if b == 0 else rim[1]
                    if a % ps == 0: c = sh(rim[1], -20)
                else:
                    n = max(1, round(L / ps)); pl = L / n; pa = a - int(a // pl * pl + 1e-6); pn = int(round(pl))
                    n2 = max(1, round(W_ / ps)); ql = W_ / n2; qb = b - int(b // ql * ql + 1e-6); qn = int(round(ql))
                    pe = min(pa, pn - 1 - pa, qb, qn - 1 - qb); eo = min(a, L - 1 - a, b, W_ - 1 - b)
                    c = (236, 236, 231) if clean else (240, 240, 235)
                    if hsh(x // 3, y // 3, seed) % 7 == 0: c = sh(c, -6)
                    if eo < 2: c = rim[0] if eo == 1 else rim[1]
                    elif pe == 0: c = (206, 206, 201) if clean else (214, 198, 164)
                    elif pe == 1: c = (248, 248, 245)
                    elif pe == 2: c = (222, 222, 216)
                    if pe <= 1 and eo >= 2 and m >= 14:                           # stitch pairs across the seams
                        s_along = pa if min(qb, qn - 1 - qb) <= 1 else qb; sn = pn if min(qb, qn - 1 - qb) <= 1 else qn
                        if s_along in (7, 10, sn - 8, sn - 11): c = (128, 124, 116)
            elif mat == 'window':
                c = frame(x, y, w, h, seed, 2 if m > 6 else m)
                if c is None:
                    c = (184, 214, 232)
                    if e == 2: c = (128, 168, 192)
                    elif e == 3: c = (214, 234, 244) if (x == 3 or y == 3) else (168, 200, 220)
                    elif (x - y) % 13 in (0, 1) and e > 4: c = (224, 240, 248)
                    elif (x - y) % 13 == 5 and e > 5: c = (204, 228, 240)
            elif mat in ('rod', 'brassrod', 'gun', 'girder'):
                pal = {'rod': [GREY[0], GREY[2], GREY[4], GREY[3]], 'brassrod': [BR[0], BR[1], BR[3], BR[2]],
                       'gun': [(84, 84, 90), (54, 54, 60), (30, 30, 34), (40, 40, 44)], 'girder': [(116, 118, 126), (80, 82, 90), (46, 48, 54), (60, 62, 68)]}[mat]
                c = pal[1]
                if b == 0: c = pal[0]
                elif b == W_ - 1: c = pal[2]
                elif b == 1 and W_ > 3: c = sh(pal[1], 12)
                if mat == 'girder' and W_ >= 8 and 1 < b < W_ - 2:
                    k = (a + b) % 12; k2 = (a - b) % 12
                    if k == 0 or k2 == 0: c = pal[0]
                    elif k == 1 or k2 == 1: c = pal[2]
                    else: c = pal[3]
                per = 16 if mat != 'gun' else 10
                if a % per == per - 1: c = pal[2]
                elif a % per == 0 and W_ > 2: c = pal[0] if b < W_ - 1 else pal[2]
                if mat == 'gun' and a >= L - 4: c = pal[2] if a < L - 1 else (16, 16, 18)
            elif mat == 'seat':
                c = (104, 66, 48) if hsh(x // 2, y // 2, seed) % 5 else (96, 60, 44)
                if e == 0: c = (66, 42, 32)
                elif e == 1: c = (126, 84, 62) if (x == 1 or y == 1) else (80, 50, 38)
                elif e == 2 and (x + y) % 3 == 0: c = (150, 110, 84)              # stitching
                elif m >= 10 and x % 6 == 3 and y % 6 == 3: c = (70, 44, 34)      # tufts
            elif mat == 'dash':                                                 # dashboard: dials face the pilot (north)
                c = frame(x, y, w, h, seed, 2)
                if c is None:
                    c = (52, 40, 30) if y % 4 else (44, 34, 26)
                    if face == 'north' and h >= 8:
                        n = max(1, w // 12); cw = w / n; i = int(x // cw); cxp = (i + 0.5) * cw - 0.5; r = math.hypot(x - cxp, y - (h - 1) / 2); R = min(cw, h) / 2 - 2.5
                        if r <= R + 1: c = BR[2] if r > R else (226, 226, 220)
                        if r <= R and (i % 3 == 0 and abs(x - cxp) < 0.6 and y <= (h - 1) / 2 or i % 3 == 1 and abs((x - cxp) - ((h - 1) / 2 - y)) < 0.8 and x >= cxp or i % 3 == 2 and abs(y - (h - 1) / 2) < 0.6 and x <= cxp): c = (168, 44, 40)
                        if r < 0.8: c = (40, 40, 44)
            elif mat == 'crate':                                                # small strapped crate (cargo detail)
                c = planks(a, b, seed, pal=[(170, 132, 80), (152, 116, 68), (134, 100, 58), (108, 80, 46), (80, 58, 34)], rh=5)
                if e == 0: c = (72, 52, 30)
                elif e == 1: c = (186, 148, 92) if (x == 1 or y == 1) else (110, 82, 48)
                if m >= 10 and (abs(x - y) <= 1 or abs(x - (h - 1 - y)) <= 1) and e > 1 and face not in ('up', 'down'): c = (120, 90, 52)
            elif mat in ('skin', 'shirt', 'pants'):
                c = {'skin': (198, 150, 118), 'shirt': (60, 150, 160), 'pants': (60, 62, 130)}[mat]
                if e == 0: c = sh(c, -30)
            else: c = (255, 0, 255)
            px[x, y] = c + (255,)
    return im


CONT = ('rod', 'brassrod', 'gun', 'girder', 'hullw', 'panel', 'net', 'flag', 'lantern', 'rope')


def paint1(mat, w, h, face):
    """1 px per unit. Long parts get one continuous texture (no repeated block-sized panels or bands)."""
    if mat in ('dash', 'crate', 'skin', 'shirt', 'pants'): return paint_v2(mat, w, h, face)
    if mat not in CONT: return oldlib.paint(mat, w, h, face)
    im = Image.new('RGBA', (w, h)); px = im.load(); horiz = w >= h; seed = hsh(w, h, len(mat), ord(mat[0]))
    for y in range(h):
        for x in range(w):
            a, b = (x, y) if horiz else (y, x); L, W_ = (w, h) if horiz else (h, w)
            e = min(x, y, w - 1 - x, h - 1 - y); m = min(w, h)
            if mat in ('rod', 'brassrod', 'gun'):
                pal = {'rod': [GREY[0], GREY[2], GREY[4]], 'brassrod': [BR[0], BR[1], BR[3]], 'gun': [(84, 84, 90), (54, 54, 60), (30, 30, 34)]}[mat]
                c = pal[1]
                if b == 0 and W_ > 1: c = pal[0]
                if b == W_ - 1 and W_ > 1: c = pal[2]
                if W_ == 1: c = pal[1] if hsh(a // 5, seed) % 3 else pal[0]
                if mat == 'gun' and L >= 6 and a >= L - 2: c = pal[2] if a == L - 2 else (16, 16, 18)
            elif mat == 'girder':
                c = (62, 64, 72)
                if b == 0: c = (116, 118, 126)
                elif b == W_ - 1: c = (44, 46, 52)
                elif W_ >= 4:
                    per = 2 * (W_ - 2); k = a % per; d = min(abs(k - (b - 1)), abs((per - k) - (b - 1)))
                    c = (104, 106, 114) if d == 0 else (46, 48, 54) if d == 1 else (66, 68, 76)
                if a in (0, L - 1): c = (44, 46, 52)
            elif mat == 'hullw':
                if m <= 3:
                    c = (126, 126, 122) if b == 0 else (104, 104, 101) if b < W_ - 1 else (80, 80, 78)
                    if hsh(a // 3, seed) % 5 == 0 and 0 < b < W_ - 1: c = (112, 112, 108)
                elif e < 2:
                    c = (132, 132, 128) if e == 1 else (98, 98, 96)
                    if e == 0 and (y == h - 1 or x == w - 1): c = (78, 78, 77)
                    if e == 1 and min(x, w - 1 - x) == 1 and min(y, h - 1 - y) == 1: c = (70, 70, 70)
                    if e == 1 and hsh(x // 2, y // 2, seed) % 6 == 0: c = (122, 122, 118)
                else:
                    col = x // 3; r = x % 3; tone = (hsh(col, seed) % 5 - 2) * 3
                    c = sh(DSP[1], tone) if r == 1 else sh(DSP[0], tone) if r == 0 else DSP[3]
                    if r != 2 and hsh(col, y // 5, seed) % 4 == 0: c = sh(DSP[2], tone)
                    if e == 2: c = DSP[3]
            elif mat == 'panel':
                if m <= 2: c = BR[1] if b == 0 else BR[3]
                elif e == 0: c = BR[1] if (y == 0 or x == 0) else BR[3]
                elif e == 1 and m >= 6: c = BR[0] if (y == 1 or x == 1) else BR[2]
                else:
                    t = b / max(1, W_ - 1); g = int(22 - 18 * t); ei = e - (2 if m >= 6 else 1)
                    c = (34 + g, 38 + g, 46 + g)
                    if ei == 0: c = (24, 26, 32)
                    elif (x - y) % 9 == 0 and b < W_ * 0.55: c = (64 + g, 70 + g, 82 + g)
                    cx2, cy2 = min(x, w - 1 - x), min(y, h - 1 - y)
                    if m >= 8 and cx2 == 3 and cy2 == 3: c = (120, 128, 140)
            elif mat == 'net':
                c = (0, 0, 0, 0)
                if (x + y) % 4 == 0 or (x - y) % 4 == 0: c = (196, 172, 118) if (x + y) % 4 == 0 else (168, 144, 96)
                if e == 0: c = (150, 126, 82)
            elif mat == 'flag':
                c = (176, 58, 50)
                if e == 0: c = (128, 40, 36)
                elif abs(y - (h - 1) / 2) < 0.6: c = (236, 226, 204)
                if x >= w - 2 and abs(y - (h - 1) / 2) < (x - (w - 3)) * 0.9: c = (0, 0, 0, 0)        # swallow tail
            elif mat == 'lantern':
                c = (255, 220, 130)
                if e == 0: c = BR[2] if (x + y) % 2 == 0 or m < 3 else BR[1]
                elif e == 1 and m >= 4: c = (255, 240, 178)
            elif mat == 'rope':
                c = (176, 150, 100) if (a + b) % 3 else (140, 116, 74)
                if b == W_ - 1: c = (118, 96, 60)
            px[x, y] = c if len(c) == 4 else c + (255,)
    return im


import numpy as np
WEATHER = {'sail': (13, 5, 16), 'sailc': (13, 5, 16), 'wood': (16, 8, 12), 'casing': (16, 8, 12), 'hullw': (16, 8, 12), 'crate': (14, 7, 8), 'rod': (18, 8, 0), 'girder': (18, 8, 0), 'gun': (12, 6, 0),
           'engine': (20, 8, 12), 'tank': (20, 8, 12), 'panel': (10, 4, 8), 'window': (5, 2, 0), 'chest': (12, 6, 8), 'vault': (16, 6, 10), 'wheel': (8, 4, 0), 'seat': (10, 5, 6), 'brassrod': (14, 6, 0),
           'dash': (6, 3, 0), 'rope': (8, 4, 0), 'latch': (6, 3, 0), 'lantern': (0, 0, 0)}
# patches of a second colour: (colour, how much of the surface, blend strength)
PATINA = {'engine': ((86, 158, 138), 0.30, 0.42), 'tank': ((86, 158, 138), 0.30, 0.42), 'rod': ((122, 86, 60), 0.26, 0.38), 'girder': ((122, 86, 60), 0.26, 0.40), 'gun': ((110, 80, 60), 0.18, 0.30),
          'brassrod': ((96, 130, 104), 0.22, 0.34), 'panel': ((120, 96, 60), 0.16, 0.26), 'vault': ((122, 86, 60), 0.24, 0.36), 'sail': ((176, 150, 104), 0.30, 0.34), 'sailc': ((168, 152, 120), 0.30, 0.34),
          'wood': ((52, 40, 30), 0.26, 0.34), 'casing': ((70, 66, 58), 0.24, 0.30), 'hullw': ((40, 32, 26), 0.26, 0.34), 'crate': ((70, 52, 34), 0.22, 0.30), 'chest': ((70, 50, 26), 0.18, 0.26)}


def _vnoise(w, h, scale, rng):
    g = rng.uniform(-1, 1, (max(2, h // scale + 2), max(2, w // scale + 2))).astype('float32')
    im = Image.fromarray(g, 'F').resize((w, h), Image.BICUBIC)
    return np.clip(np.asarray(im), -1, 1)


def weather(im, mat, seed, face='north', rs=1):
    """weathering in the manner of the stock warship texture: mottled blotches, stains and patina, dark rims, drip streaks, creased canvas."""
    w, h = im.size; blotch, grain, vig = WEATHER.get(mat, (12, 6, 8))
    rng = np.random.default_rng(seed & 0x7fffffff)
    a = np.asarray(im).astype('float32'); rgb = a[..., :3].copy(); alpha = a[..., 3:4]
    big = _vnoise(w, h, max(2, 9 // rs), rng); mid = _vnoise(w, h, max(2, 4 // rs), rng)
    d = blotch * big + 0.6 * blotch * mid + grain * rng.uniform(-1, 1, (h, w)).astype('float32')
    yy, xx = np.mgrid[0:h, 0:w]
    if vig and min(w, h) >= 8:
        e = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)).astype('float32')
        d -= vig * np.clip(1 - e / (6.0 / rs), 0, 1) ** 1.5
    if mat in PATINA and w * h >= 24:                                           # stains / rust / verdigris patches
        col, cover, strength = PATINA[mat]
        n = 0.65 * _vnoise(w, h, max(2, 6 // rs), rng) + 0.35 * _vnoise(w, h, max(2, 3 // rs), rng)
        thr = np.quantile(n, 1 - cover) if w * h >= 64 else 0.3
        k = np.clip((n - thr) / 0.18, 0, 1)[..., None] * strength
        rgb = rgb * (1 - k) + np.array(col, 'float32') * k
        d -= 6 * k[..., 0]
    if face in ('north', 'south', 'east', 'west') and h >= 10 and mat not in ('window', 'dash', 'seat', 'lantern'):   # drip streaks down the sides
        s = np.zeros((h, w), 'float32')
        for _ in range(max(1, w // 7)):
            x0 = int(rng.integers(0, w)); L = int(rng.integers(h // 3, h)); y0 = int(rng.integers(0, max(1, h - L)))
            fade = np.linspace(1, 0, L) ** 0.7
            s[y0:y0 + L, x0] = np.maximum(s[y0:y0 + L, x0], fade)
            if x0 + 1 < w: s[y0:y0 + L, x0 + 1] = np.maximum(s[y0:y0 + L, x0 + 1], fade * 0.4)
        d -= (10 if mat in ('sail', 'sailc') else 15) * s
        d -= 8 * np.clip((yy - (h - 5 // rs)) / (5.0 / rs), 0, 1)                             # grime gathering at the lower edge
    if mat in ('sail', 'sailc') and min(w, h) >= 10:                            # creases
        v = np.zeros((h, w), 'float32')
        for _ in range(max(2, w * h // 220)):
            x, y = rng.uniform(1, w - 1), rng.uniform(1, h - 1); ang = rng.uniform(0, 6.283)
            for _ in range(int(rng.integers(10 // rs, 34 // rs + 1))):
                xi, yi = int(x), int(y)
                if not (0 <= xi < w and 0 <= yi < h): break
                v[yi, xi] = 1.0
                if xi + 1 < w: v[yi, xi + 1] = max(v[yi, xi + 1], 0.4)
                ang += rng.uniform(-0.55, 0.55); x += math.cos(ang); y += math.sin(ang)
        d -= 22 * v
    out = np.clip(rgb + d[..., None] * np.array([1.0, 0.96, 0.9], 'float32'), 0, 255)
    return Image.fromarray(np.concatenate([out, alpha], -1).astype('uint8'), 'RGBA')


def paint(mat, w, h, face):
    """w, h in texture pixels (D per unit): the 1 px design scaled up softly, then weathered."""
    if mat in ('skin', 'shirt', 'pants'): return paint_v2(mat, w, h, face)
    seed = hsh(w, h, len(mat), ord(mat[0]), ord(face[0]))
    if D == 1: return paint1(mat, w, h, face)
    if mat in PROPS:
        return weather(oldlib.paint(mat, w, h, face), 'sail', seed) if False else oldlib.paint(mat, w, h, face)
    base = paint1(mat, max(1, (w + 1) // 2), max(1, (h + 1) // 2), face); size = (2 * base.width, 2 * base.height)
    near = base.resize(size, Image.NEAREST)
    if mat in FLAT or mat == 'lantern': return near.crop((0, 0, w, h))
    # 1.0.0: weather at the vanilla 1 px/unit grid and enlarge with NEAREST, so stains/grain are chunky 2x2 pixels (no fine, high-res noise)
    lo = weather(base, mat, seed, face, rs=2)
    return lo.resize(size, Image.NEAREST).crop((0, 0, w, h))


def rotm(rot):
    rx, ry, rz = [math.radians(v) for v in rot]
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    X = [[1, 0, 0], [0, cx, -sx], [0, sx, cx]]; Y = [[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]]; Z = [[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]]
    mul = lambda A, B: [[sum(A[i][k] * B[k][j] for k in range(3)) for j in range(3)] for i in range(3)]
    return mul(Z, mul(Y, X))


class Model:
    def __init__(s, name, TW=512, scale=1.0):
        s.name = name; s.C = []; s.TW = TW; s.gorig = {}; s.gdef = {}; s.anim = {}; s.scale = scale
        s.seats = []; s.mounts = []; s.preview = []; s.meta = {}

    def cube(s, name, f, t, mat, group='body', rot=None, origin=None):
        s.C.append(dict(name=name, f=list(map(float, f)), t=list(map(float, t)), mat=mat, group=group, rot=rot, origin=origin))

    def mir(s, name, f, t, mat, group='body', g2=None):
        s.cube(name, f, t, mat, group); s.cube(name, [-t[0], f[1], f[2]], [-f[0], t[1], t[2]], mat, g2 or group)

    def rcube(s, name, f, t, mat, rot, origin, group='body'): s.cube(name, f, t, mat, group, rot=list(rot), origin=list(origin))

    def rmir(s, name, f, t, mat, rot, origin, group='body'):
        s.rcube(name, f, t, mat, rot, origin, group)
        s.rcube(name, [-t[0], f[1], f[2]], [-f[0], t[1], t[2]], mat, [rot[0], -rot[1], -rot[2]], [-origin[0], origin[1], origin[2]], group)

    def chest(s, x0, y0, z0, front):
        s.cube('chest', [x0, y0, z0], [x0 + 14, y0 + 14, z0 + 14], 'chest', 'cargo')
        if front == 'e': s.cube('latch', [x0 + 14, y0 + 7, z0 + 6], [x0 + 15, y0 + 11, z0 + 8], 'latch', 'cargo')
        if front == 'w': s.cube('latch', [x0 - 1, y0 + 7, z0 + 6], [x0, y0 + 11, z0 + 8], 'latch', 'cargo')

    def seat(s, x, ytop, z, w=6):
        """seat cushion whose top is at ytop; registers a passenger position (order = boarding order)."""
        s.cube('seat', [x - w / 2, ytop - 2, z - 3], [x + w / 2, ytop, z + 3], 'seat')
        s.cube('seat_back', [x - w / 2, ytop, z - 4], [x + w / 2, ytop + 7, z - 3], 'seat')
        s.seats.append((x, ytop, z))

    def player(s, x, ytop, z):
        """preview-only sitting player (sizes in world pixels / scale)."""
        k = 1.0 / s.scale; q = lambda *v: [a * k for a in v]
        def box(mat, x0, y0, z0, x1, y1, z1):
            a = q(x0, y0, z0); b = q(x1, y1, z1)
            s.preview.append(dict(name='player', f=[x + a[0], ytop + a[1], z + a[2]], t=[x + b[0], ytop + b[1], z + b[2]], mat=mat, group='body', rot=None, origin=None))
        box('pants', -3.75, -0.2, -1.9, 3.75, 3.5, 10); box('shirt', -3.75, 1.6, -1.9, 3.75, 12.9, 1.9)
        box('shirt', -7.5, 1.6, -1.9, -3.75, 12.9, 1.9); box('shirt', 3.75, 1.6, -1.9, 7.5, 12.9, 1.9); box('skin', -3.75, 12.9, -3.75, 3.75, 20.4, 3.75)

    def build(s):
        C = s.C; TW = s.TW; S = s.scale
        for (x, y, z) in s.seats: s.player(x, y, z)
        ALL = C + s.preview

        def fsize(c, f):
            dx, dy, dz = [c['t'][i] - c['f'][i] for i in range(3)]
            return {'north': (dx, dy), 'south': (dx, dy), 'east': (dz, dy), 'west': (dz, dy), 'up': (dx, dz), 'down': (dx, dz)}[f]
        rects = []; uniq = {}
        for ci, c in enumerate(ALL):
            c['uv'] = {}
            flat_axis = [i for i in range(3) if c['t'][i] == c['f'][i]]
            for f in FACES:
                w, h = fsize(c, f)
                if w <= 0 or h <= 0: continue
                W, H = max(1, math.ceil(w * D)), max(1, math.ceil(h * D))
                fk = f if c['mat'] in PERFACE else ('ud' if f in ('up', 'down') else 's')
                key = (c['mat'], W, H, fk); rects.append((key, ci, f)); uniq[key] = (W, H)

        def pack(TH):
            pos = {}; x = y = rowh = 0
            for key, (W, H) in sorted(uniq.items(), key=lambda kv: (-kv[1][1], -kv[1][0])):
                if W > TW: raise SystemExit('%s: face %s wider than texture' % (s.name, key))
                if x + W > TW: x = 0; y += rowh + 1; rowh = 0
                if y + H > TH: return None
                pos[key] = (x, y); x += W + 1; rowh = max(rowh, H)
            return pos
        TH = 64
        while not (pos := pack(TH)): TH *= 2
        tex = Image.new('RGBA', (TW, TH), (0, 0, 0, 0))
        for key, (x, y) in pos.items():
            W, H = uniq[key]; fk = key[3]; tex.paste(paint(key[0], W, H, 'up' if fk == 'ud' else 'north' if fk == 's' else fk), (x, y))
        for key, ci, f in rects:
            x, y = pos[key]; W, H = uniq[key]; c = ALL[ci]; c['uv'][f] = [x, y, x + W, y + H]
            d = [c['t'][i] - c['f'][i] for i in range(3)]
            if d[1] == 0 and f == 'down': c['uv'][f] = [x, y + H, x + W, y]
            if d[2] == 0 and f == 'north': c['uv'][f] = [x + W, y, x, y + H]
            if d[0] == 0 and f == 'west': c['uv'][f] = [x + W, y, x, y + H]
        # the published texture must not contain the preview-only player colours
        pub = tex.copy()
        for key, (x, y) in pos.items():
            if key[0] in ('skin', 'shirt', 'pants'): pub.paste((0, 0, 0, 0), (x, y, x + uniq[key][0], y + uniq[key][1]))
        pub.save(s.name + '.png')
        b64 = lambda im: 'data:image/png;base64,' + base64.b64encode((lambda b: (im.save(b, 'PNG'), b.getvalue())[1])(io.BytesIO())).decode()
        gdef = s.gdef
        sv = lambda v: [round(a * S, 4) for a in v]

        def gchain(g):
            out = []
            while g:
                d = gdef.get(g, {})
                if d.get('rotation'): out.append((d['rotation'], d.get('origin') or s.gorig.get(g, [0, 0, 0])))
                g = d.get('parent')
            return out
        els = []; groups = {}; nodes = {}; roots = []

        def node(g):
            if g in nodes: return nodes[g]
            d = gdef.get(g, {})
            n = dict(name=g, origin=sv(d.get('origin') or s.gorig.get(g, [0, 0, 0])), color=0, uuid=str(uuid.uuid4()), export=True, mirror_uv=False, isOpen=False, locked=False, visibility=True, autouv=0, children=[])
            if d.get('rotation'): n['rotation'] = d['rotation']
            nodes[g] = n
            p = d.get('parent')
            if p: node(p)['children'].append(n)
            else: roots.append(n)
            return n
        scene = []
        for c in ALL:
            sc = dict(c); ch = gchain(c['group']); sc['chain'] = ([(c['rot'], c['origin'] or [(c['f'][i] + c['t'][i]) / 2 for i in range(3)])] if c['rot'] else []) + ch
            scene.append(sc)
            if c in s.preview: continue
            u = str(uuid.uuid4())
            faces = {f: ({'uv': c['uv'][f], 'texture': 0} if f in c['uv'] else {'uv': [0, 0, 0, 0], 'texture': None}) for f in FACES}
            org = c['origin'] or [(c['f'][i] + c['t'][i]) / 2 for i in range(3)]
            e = dict(name=c['name'], box_uv=False, rescale=False, locked=False, render_order='default', allow_mirror_modeling=True, **{'from': sv(c['f']), 'to': sv(c['t'])}, autouv=0, color=0, origin=sv(org), faces=faces, type='cube', uuid=u)
            if c['rot']: e['rotation'] = c['rot']
            els.append(e); groups.setdefault(c['group'], []).append(u); node(c['group'])['children'].append(u)
        anims = {}; pi = 0

        def addanim(g, dp):
            full = {k: '0' for k in 'xyz'}; full.update(dp)
            anims[nodes[g]['uuid']] = dict(name=g, type='bone', keyframes=[dict(channel='rotation', data_points=[full], uuid=str(uuid.uuid4()), time=0, color=-1, interpolation='linear', bezier_linked=True, bezier_left_time=[-0.1] * 3, bezier_left_value=[0] * 3, bezier_right_time=[0.1] * 3, bezier_right_value=[0] * 3)])
        for g in s.anim: node(g)
        for g in sorted(nodes):
            if g in s.anim: addanim(g, s.anim[g]); continue
            if not g.startswith('propell'): continue
            c0 = [c for c in C if c['group'] == g and any(c['t'][i] == c['f'][i] for i in range(3)) and c['mat'] != 'cog']
            if not c0: continue
            ax = 'y' if c0[0]['t'][1] == c0[0]['f'][1] else 'z' if c0[0]['t'][2] == c0[0]['f'][2] else 'x'
            sp = (100 if ax == 'y' else 150) * (1 if pi % 2 == 0 else -1); pi += 1
            addanim(g, {ax: 'variable.engine_rotation * %d' % sp})
        animations = [dict(uuid=str(uuid.uuid4()), name='animation', loop='loop', override=False, length=0, snapping=24, selected=False, anim_time_update='', blend_weight='', start_delay='', loop_delay='', animators=anims)] if anims else []
        bb = dict(meta=dict(format_version='4.9', model_format='free', box_uv=False), name=s.name, model_identifier='', visible_box=[1, 1, 0], variable_placeholders='', variable_placeholder_buttons=[], timeline_setups=[], unhandled_root_fields={},
                  resolution=dict(width=TW, height=TH), elements=els, outliner=roots,
                  textures=[dict(path='', name=s.name + '.png', folder='', namespace='', id='0', width=TW, height=TH, uv_width=TW, uv_height=TH, particle=False, layers_enabled=False, sync_to_project='', render_mode='default', render_sides='auto', frame_time=1, frame_order_type='loop', frame_order='', frame_interpolate=False, visible=True, internal=True, saved=True, uuid=str(uuid.uuid4()), source=b64(pub))], animations=animations)
        json.dump(bb, open(s.name + '.bbmodel', 'w'))
        json.dump(dict(cubes=scene, tw=TW, th=TH, tex=b64(tex), scale=S), open(s.name + '.scene.json', 'w'))
        # game data derived from the model (blocks)
        k = S / 16.0
        meta = dict(s.meta); meta['scale'] = S
        meta['seats'] = [dict(x=round(x * k, 4), y=round(y * k, 4), z=round(z * k, 4)) for (x, y, z) in s.seats]
        meta['mounts'] = [{t: [dict({'x': round(p[0] * k, 4), 'y': round(p[1] * k, 4), 'z': round(p[2] * k, 4)}, **(p[3] if len(p) > 3 else {})) for p in pts] for t, pts in slot.items()} for slot in s.mounts]
        ext = [[min(c['f'][i] for c in C), max(c['t'][i] for c in C)] for i in range(3)]
        meta['extent_blocks'] = [[round(v * k, 2) for v in e2] for e2 in ext]
        json.dump(meta, open(s.name + '.meta.json', 'w'), indent=1)
        zf = zfight(scene)
        print(s.name, 'cubes', len(C), 'tex', TW, TH, 'anim', len(anims), 'seats', len(s.seats), 'zfight', len(zf))
        for z in zf: print('   ZFIGHT', z)


def zfight(scene):
    """coplanar faces looking the same way whose areas overlap -> flicker in game."""
    faces = []
    for ci, c in enumerate(scene):
        if c['mat'] in ('skin', 'shirt', 'pants'): continue
        x0, y0, z0 = c['f']; x1, y1, z1 = c['t']
        Q = {'north': ([[x1, y1, z0], [x0, y1, z0], [x0, y0, z0], [x1, y0, z0]], [0, 0, -1]), 'south': ([[x0, y1, z1], [x1, y1, z1], [x1, y0, z1], [x0, y0, z1]], [0, 0, 1]),
             'east': ([[x1, y1, z1], [x1, y1, z0], [x1, y0, z0], [x1, y0, z1]], [1, 0, 0]), 'west': ([[x0, y1, z0], [x0, y1, z1], [x0, y0, z1], [x0, y0, z0]], [-1, 0, 0]),
             'up': ([[x0, y1, z0], [x1, y1, z0], [x1, y1, z1], [x0, y1, z1]], [0, 1, 0]), 'down': ([[x0, y0, z1], [x1, y0, z1], [x1, y0, z0], [x0, y0, z0]], [0, -1, 0])}
        for f, (pts, n) in Q.items():
            if f not in c['uv']: continue
            for rot, org in c['chain']:
                M = rotm(rot)
                pts = [[org[i] + sum(M[i][j] * (p[j] - org[j]) for j in range(3)) for i in range(3)] for p in pts]
                n = [sum(M[i][j] * n[j] for j in range(3)) for i in range(3)]
            faces.append((ci, c['name'], f, pts, n, c['group']))
    out = []

    def clip(poly, a, b):                                                      # keep the left side of a->b (2D)
        res = []
        for i in range(len(poly)):
            p, q = poly[i], poly[(i + 1) % len(poly)]
            sp = (b[0] - a[0]) * (p[1] - a[1]) - (b[1] - a[1]) * (p[0] - a[0]); sq = (b[0] - a[0]) * (q[1] - a[1]) - (b[1] - a[1]) * (q[0] - a[0])
            if sp >= 0: res.append(p)
            if (sp >= 0) != (sq >= 0) and sp != sq:
                t = sp / (sp - sq); res.append((p[0] + t * (q[0] - p[0]), p[1] + t * (q[1] - p[1])))
        return res

    def area(poly): return abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1] for i in range(len(poly)))) / 2 if len(poly) > 2 else 0
    for i in range(len(faces)):
        ci, n1, f1, p1, na, g1 = faces[i]
        for j in range(i + 1, len(faces)):
            cj, n2, f2, p2, nb, g2 = faces[j]
            if ci == cj: continue
            dot = sum(na[k] * nb[k] for k in range(3))
            if dot < 0.9995: continue
            if abs(sum(na[k] * (p2[0][k] - p1[0][k]) for k in range(3))) > 0.02: continue
            ax = max(range(3), key=lambda k: abs(na[k])); ii = [k for k in range(3) if k != ax]
            a2 = [(p[ii[0]], p[ii[1]]) for p in p1]; b2 = [(p[ii[0]], p[ii[1]]) for p in p2]
            if sum(a2[k][0] * a2[(k + 1) % 4][1] - a2[(k + 1) % 4][0] * a2[k][1] for k in range(4)) < 0: a2 = a2[::-1]
            poly = b2
            for k in range(4): poly = clip(poly, a2[k], a2[(k + 1) % 4]) if poly else poly
            ar = area(poly)
            if ar > 0.3: out.append('%s.%s x %s.%s area %.1f' % (n1, f1, n2, f2, ar))
    return out
