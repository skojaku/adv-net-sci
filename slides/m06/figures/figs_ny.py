#!/usr/bin/env python3
"""The New York State highway maps of Module 06 (all `col`, 537 bp wide, ONE canvas and ONE
crop box, so switching slides changes only the dots and the labels).

Data: `data/ny_network.json` (289 interchanges, 433 road segments, built by `make_ny.py`).
Projection: equirectangular, longitude scaled by cos(42.5 deg).  One scale for every map.

Style (the lecturer's): muted road lines and state outline, every interchange a small dot
from near-paper (low) to saturated cool (high) by `F.shade`, a darker dot is ALWAYS the more
central one, the winner a hot disc, MesloLGS NF labels, and a hot brush underline under the
one label that is the point of the slide.

    degree        shade 0 / 0.55 / 1 for degree 1 / 3 / 4+ (only four values exist)
    closeness     min-max of the value
    eccentricity  min-max of 1 / eccentricity  (the smaller the worst-case drive, the darker)
    betweenness   value / maximum
    eigenvector   value / maximum

Eccentricity is the one measure where *smaller* is better. It is shaded by 1/e so that the
slide's rule "darker = more central" holds on every map.
"""

import json
import math

import numpy as np

import figlib as F
from figlib import text


NY = json.loads((F.OUT / "data" / "ny_network.json").read_text())
NODES, EDGES, CITIES = NY["nodes"], NY["edges"], NY["cities"]
N = len(NODES)
assert (N, len(EDGES)) == (289, 433), (N, len(EDGES))
assert all(n["id"] == i for i, n in enumerate(NODES))

# --------------------------------------------------------------------------- projection
SCALE = 72.0                        # bp per degree of latitude
X0, Y0 = 6.0, 30.0                  # lower-left of the state's bounding box on the canvas
CANVAS_H = 400
DY = 22.0                           # Y0 grew from 8 to 30 (room for the 60 km circle); hand-placed names move with the map
_ring_pts = [p for ring in NY["outline"] for p in ring]
LON0, LAT0 = min(p[0] for p in _ring_pts), min(p[1] for p in _ring_pts)
KX = math.cos(math.radians(42.5)) * SCALE


def P(lon, lat):
    return (X0 + (lon - LON0) * KX, Y0 + (lat - LAT0) * SCALE)


XY = [P(n["lon"], n["lat"]) for n in NODES]
MAP_W = max(p[0] for p in XY)
assert max(p[0] for p in map(lambda q: P(*q), _ring_pts)) < F.COL_W - 90

# --------------------------------------------------------------------------- facts
CITY_ID = dict(CITIES)
assert len(CITY_ID) == 8


def argbest(key, sign=1):
    vals = [sign * n[key] for n in NODES]
    best = max(vals)
    ties = [i for i, v in enumerate(vals) if abs(v - best) < 1e-12 * max(1, abs(best))]
    assert len(ties) == 1, f"{key}: tie between {ties}"
    return ties[0]


WIN = {"closeness": argbest("closeness"), "harmonic": argbest("harmonic"),
       "eccentricity": argbest("eccentricity", -1), "betweenness": argbest("betweenness"),
       "eigenvector": argbest("eigenvector")}
EXPECT = {                                  # measure -> (refs, nearest place)
    "closeness": ({"NY 17", "US 209"}, "Middletown"),
    "harmonic": ({"I 95", "HR", "I 295"}, "New York City"),
    "eccentricity": ({"NY 17", "NY 8", "NY 10"}, "Binghamton"),
    "betweenness": ({"NY 17", "NY 52"}, "Monticello"),
    "eigenvector": ({"CI", "I 495"}, "Hempstead"),
}
for m, (refs, near) in EXPECT.items():
    n = NODES[WIN[m]]
    assert set(n["refs"]) == refs and n["near"] == near, f"{m}: winner is {n['refs']} near {n['near']}"
assert round(NODES[WIN["eccentricity"]]["eccentricity"], 1) == 472.7
_btw8 = sorted(CITY_ID, key=lambda c: -NODES[CITY_ID[c]]["betweenness"])
assert _btw8[0] == "Binghamton", _btw8
from collections import Counter                      # noqa: E402
assert Counter(n["degree"] for n in NODES) == {3: 201, 4: 57, 1: 30, 5: 1}

# --------------------------------------------------------------------------- shading
def _norm(vals, lo=None):
    lo = min(vals) if lo is None else lo
    hi = max(vals)
    return [(v - lo) / (hi - lo) for v in vals]


SHADE = {
    "degree": [{1: 0.0, 3: 0.55, 4: 1.0, 5: 1.0}[n["degree"]] for n in NODES],
    "closeness": _norm([n["closeness"] for n in NODES]),
    "eccentricity": _norm([1 / n["eccentricity"] for n in NODES]),
    "betweenness": _norm([n["betweenness"] for n in NODES], lo=0.0),
    "eigenvector": _norm([n["eigenvector"] for n in NODES], lo=0.0),
}

ROAD = "muted"
ROAD_W = 1.6
ROAD_OP = 0.8
WIN_D = 22.0


def _dot(x, y, t):
    """One interchange: fill by value, a thin ink rim so the faintest still reads."""
    d = 7.0 + 4.0 * t
    return ("\\filldraw[fill=%s,draw=ink!60,line width=0.7bp] (%.1f,%.1f) circle (%sbp);\n"
            % (F.shade(t), x, y, d / 2))


# --------------------------------------------------------------------------- drawing
def outline(zoom=None):
    o = ""
    for ring in NY["outline"]:
        pts = [P(*p) for p in ring]
        if zoom:
            pts = [zoom(p) for p in pts]
        o += ("\\draw[line width=1.8bp,draw=muted,line join=round] %s -- cycle;\n"
              % " -- ".join("(%.1f,%.1f)" % p for p in pts))
    return o


def roads(xy=None):
    xy = xy or (lambda i: XY[i])
    return "".join(F.seg(xy(e["u"]), xy(e["v"]), color=ROAD, w=ROAD_W, opacity=ROAD_OP) for e in EDGES)


def base():
    """State outline and the road segments, behind everything."""
    return outline() + roads()


def shaded_dots(shade):
    """All 289 interchanges, light ones first so the dark ones sit on top."""
    return "".join(_dot(*XY[i], shade[i]) for i in sorted(range(N), key=lambda i: shade[i]))


def plain_dots(t=0.12):
    return "".join(_dot(x, y, t) for x, y in XY)


def winner(i, d=WIN_D, xy=None):
    x, y = (xy or XY)[i] if xy is None else xy
    return F.disc(x, y, "", fill="hot", size=d)


def ul(x0, x1, y, color="hot"):
    """A hand-drawn brush underline: a translucent body and five thin strands with their own
    opacity, wobble and trimmed ends, drawn as plain polylines. (figlib.brush runs TikZ's
    random-steps decoration, which fails with "Dimension too large" for some lengths.)"""
    rng = np.random.default_rng(int(x0 * 7 + x1 * 3 + y) % (2 ** 32))
    n = max(int((x1 - x0) // 6), 3)
    xs = np.linspace(x0, x1, n + 1)
    rise = lambda x: 1.5 * (x - x0) / (x1 - x0)

    def line(off, t0, t1, w, op):
        pts = " -- ".join("(%.1f,%.1f)" % (xs[i], y + rise(xs[i]) + off + rng.normal(0, 0.28))
                          for i in range(t0, t1 + 1))
        return ("\\draw[%s,line width=%.2fbp,line cap=round,line join=round,opacity=%.2f] %s;\n"
                % (color, w, op, pts))
    o = line(0.0, 1, n - 1, 3.6, 0.35)
    for k in range(5):
        off = (k - 2) * 1.0
        o += line(off, int(rng.integers(0, 2)), n - int(rng.integers(0, 2)),
                  float(rng.uniform(0.9, 1.7)), float(rng.uniform(0.5, 0.95)))
    return o


class Labels:
    """Names in blank regions with leader lines, MesloLGS NF.

    Asserts that labels clear each other, the canvas and the city dots, and that no leader
    crosses another label. Meslo is monospaced: 0.61 em per character.
    """
    CW = F.CHAR_W

    def __init__(self, name):
        self.name, self.boxes, self.out, self.leaders, self.lines, self.ul = name, [], "", "", [], ""
        self.dy = DY

    def box(self, s, x, y, anchor, cw=None):
        w = (cw or self.CW) * F.FONT * len(s) + 6
        h = 0.95 * F.FONT + 2
        ax = {"center": 0.0, "west": 0.5, "east": -0.5}[anchor]
        return (x + ax * w - w / 2, y - h / 2, x + ax * w + w / 2, y + h / 2)

    def add(self, s, x, y, anchor="center", color="ink", to=None, r=0.0, halo=True, avoid=(),
            rel=True, underline=False, grow=0.0):
        if rel:
            y += self.dy
        b = self.box(s, x, y, anchor)
        assert 2 <= b[0] and b[2] <= F.COL_W - 2 and 2 <= b[1] and b[3] <= CANVAS_H - 2, \
            f"{self.name}: label {s!r} runs off the canvas {tuple(round(v) for v in b)}"
        for k, o in self.boxes:
            assert not F.boxes_overlap(b, o), f"{self.name}: labels {s!r} and {k!r} overlap"
        for px, py in avoid:
            assert not F.box_hits_disc(b, px, py, 11), f"{self.name}: label {s!r} covers a city dot"
        self.boxes.append((s, b))
        if to is not None:
            x0, y0, x1, y1 = b
            dx = max(x0 - to[0], 0, to[0] - x1)
            dy = max(y0 - to[1], 0, to[1] - y1)
            if dx > 0 and (dx >= dy or dx >= 8):
                sx, sy = (x0 + 2 if to[0] < x0 else x1 - 2), min(max(to[1], y0 + 8), y1 - 8)
            else:
                sy, sx = (y0 + 2 if to[1] < y0 else y1 - 2), min(max(to[0], x0 + 8), x1 - 8)
            L = math.hypot(to[0] - sx, to[1] - sy)
            ex, ey = to[0] - (to[0] - sx) / L * r, to[1] - (to[1] - sy) / L * r
            self.lines.append((s, (sx, sy), (ex, ey)))
            self.leaders += F.seg((sx, sy), (ex, ey), color="muted", w=2.2)
        if halo:                                  # a white plate and two rings of white copies: no road shows through
            self.out += ("\\fill[white,rounded corners=3bp] (%.1f,%.1f) rectangle (%.1f,%.1f);\n"
                         % (b[0] + 1, b[1] + 3 - grow, b[2] - 1 + grow, b[3] - 3 + grow))
            for r_ in (2.4, 4.8):
                for k in range(8):
                    a_ = k * math.pi / 4
                    self.out += text(x + r_ * math.cos(a_), y + r_ * math.sin(a_), s, color="white",
                                     anchor=anchor)
        self.out += text(x, y, s, color=color, anchor=anchor)
        if underline:
            self.ul += ul(b[0] + 5, b[2] - 5, y - 20)

    def nyc(self, spots=((262, 74, "east"), (322, 17.5, "center"))):
        """A muted "NYC" on every map, in the first of `spots` (absolute canvas bp) that is free."""
        for x, y, anc in spots:
            b = self.box("NYC", x, y, anc)
            if b[1] < 2 or any(F.boxes_overlap(b, o) for _, o in self.boxes):
                continue
            self.add("NYC", x, y, anchor=anc, color="muted", rel=False)
            return
        raise AssertionError(f"{self.name}: no free place for the NYC label")

    def body(self):
        for s, p, q in self.lines:
            for k, o in self.boxes:
                assert k == s or not F.box_hits_segment(o, p, q, pad=0), \
                    f"{self.name}: the leader of {s!r} crosses the label {k!r}"
        return self.leaders + self.out + self.ul


KEY_X, KEY_Y = 10.0, 342.0                    # top-left, between the map's top edge (y 358) and Lake Ontario's shore (y 270): bare on every map
KEY_STEP = 32.0


def shade_key(L, body, title, hi, lo):
    """A muted title and the two ends of the shade scale, in the style of ny-degree's key (the same
    swatches, ink labels on a muted name), in the free corner above Lake Erie.  Asserts that nothing
    of the map (a road, a dot, a label) is under it, by rendering the map without it, and that the
    two rows do not touch each other."""
    x0 = KEY_X + 8

    def ink(x, y, word):                          # the ink of a word set at (x, y), anchor west, + 1 bp
        return (x - 1, y - 15, x + F.CHAR_W * F.FONT * len(word) + 1, y + 16)

    o = F.text(KEY_X, KEY_Y, title, color="muted", anchor="west")
    boxes = [ink(KEY_X, KEY_Y, title)]
    assert KEY_Y + 15 <= 358, "the key must not rise above the map: the group crop would grow"
    for k, (word, v) in enumerate(((hi, 1.0), (lo, 0.0))):
        y = KEY_Y - 28 - k * KEY_STEP
        o += ("\\filldraw[fill=%s,draw=ink!60,line width=0.9bp] (%d,%d) circle (8bp);\n" % (F.shade(v), x0, y))
        o += F.text(x0 + 20, y, word, anchor="west")
        boxes.append(ink(x0 + 20, y, word))
        boxes.append((x0 - 9, y - 9, x0 + 9, y + 9))
    # rows 32 bp apart (ink is 29 bp tall at most): the lines clear each other; the pixel test below keeps them off the shore
    assert KEY_STEP >= 32
    for bx in boxes:
        assert 2 <= bx[0] and bx[2] <= F.COL_W - 2 and 2 <= bx[1] and bx[3] <= CANVAS_H - 2, (title, bx)
    a = np.asarray(F.render(body, F.COL_W, CANVAS_H).convert("L"))
    for bx in boxes:                                  # every part of the key on bare paper
        r0, r1 = int(F.PXBP * (CANVAS_H - bx[3])), int(F.PXBP * (CANVAS_H - bx[1]))
        c0, c1 = int(F.PXBP * bx[0]), int(F.PXBP * bx[2])
        assert (a[r0:r1, c0:c1] > 245).all(), f"{title}: something is drawn under the key"
        assert not any(F.boxes_overlap(bx, bl) for _, bl in L.boxes), f"{title}: a label is under the key"
    return o


# --------------------------------------------------------------------------- the 3x inset
ZOOM = 3.0
INS_W = 156.0                                   # frame, bp
INS_X0, INS_Y0 = 377.0, 150.0                   # lower-left of the inset frame
REG_C = (322.0, 64.0)                           # centre of the NYC area on the map (map bp)
REG_H = INS_W / ZOOM / 2                        # half the side of the region the inset shows
INS_C = (INS_X0 + INS_W / 2, INS_Y0 + INS_W / 2)


def Z(p):
    """Map position -> inset position."""
    return (INS_C[0] + ZOOM * (p[0] - REG_C[0]), INS_C[1] + ZOOM * (p[1] - REG_C[1]))


def inset(shade=None, winners=()):
    """A framed 3x view of the NYC area (lower right): the same dots, the same shading."""
    fx0, fy0, fx1, fy1 = INS_X0, INS_Y0, INS_X0 + INS_W, INS_Y0 + INS_W
    o = ("\\draw[line width=1.8bp,draw=muted] (%.1f,%.1f) rectangle (%.1f,%.1f);\n"
         % (REG_C[0] - REG_H, REG_C[1] - REG_H, REG_C[0] + REG_H, REG_C[1] + REG_H))
    o += "\\begin{scope}\n\\clip (%.1f,%.1f) rectangle (%.1f,%.1f);\n" % (fx0, fy0, fx1, fy1)
    o += "\\fill[white] (%.1f,%.1f) rectangle (%.1f,%.1f);\n" % (fx0, fy0, fx1, fy1)
    o += outline(zoom=lambda p: Z(p))
    zxy = lambda i: Z(XY[i])
    o += roads(zxy)
    inside = [i for i in range(N)
              if fx0 - 8 <= Z(XY[i])[0] <= fx1 + 8 and fy0 - 8 <= Z(XY[i])[1] <= fy1 + 8]
    for i in sorted(inside, key=lambda i: shade[i] if shade else 0):
        o += _dot(*Z(XY[i]), shade[i] if shade else 0.12)
    for i, d in winners:
        x, y = Z(XY[i])
        assert fx0 + d / 2 < x < fx1 - d / 2 and fy0 + d / 2 < y < fy1 - d / 2, f"winner {i} not in the inset"
        o += F.disc(x, y, "", fill="hot", size=d)
    o += "\\end{scope}\n"
    o += ("\\draw[line width=2bp,draw=muted] (%.1f,%.1f) rectangle (%.1f,%.1f);\n" % (fx0, fy0, fx1, fy1))
    o += F.seg((REG_C[0] + REG_H, REG_C[1] + REG_H), (fx0, fy0), color="muted", w=1.4)   # box -> inset
    return o


# 60 km around Manhattan, drawn with the map's own projection (1 deg lat = 111.2 km)
MANHATTAN = P(-73.9712, 40.7831)
R60 = (60 / 111.2 * SCALE, 60 / (111.2 * math.cos(math.radians(40.7831))) * KX)   # (y, x) radii, bp


def circle60():
    return ("\\draw[line width=2bp,draw=muted,%s] (%.1f,%.1f) ellipse (%.2fbp and %.2fbp);\n"
            % (F.DASH, MANHATTAN[0], MANHATTAN[1], R60[1], R60[0]))


def _city(c):
    return XY[CITY_ID[c]]


# --------------------------------------------------------------------------- the figures
def b_overview():
    L = Labels("ny-overview")
    b = base() + plain_dots()
    for c in CITY_ID:
        b += F.disc(*_city(c), "", fill="cool", size=20)
    dots = [_city(c) for c in CITY_ID]
    spec = {                                  # name: (anchor, x, y, leader?)  y is map-relative
        "Watertown": ("east", _city("Watertown")[0] - 6, _city("Watertown")[1] + 52 - DY, True),
        "Buffalo": ("west", 8, 140, True),
        "Rochester": ("center", 90, 262, True),     # ends 20 bp short of the Watertown pin (was 14)
        "Syracuse": ("center", 198, 230, True),
        "Utica": ("west", 290, 214, True),
        "Albany": ("west", 346, 166, False),
        "Binghamton": ("center", 130, 70, True),
        "NYC": ("center", 398, 100, True),
    }
    for c, (anc, x, y, lead) in spec.items():
        key = "New York City" if c == "NYC" else c
        # Buffalo's plate is taller: the lake-shore roads and dots under its baseline show past a plain one
        L.add(c, x, y, anchor=anc, to=_city(key) if lead else None, r=12, avoid=dots,
              grow=6.0 if c == "Buffalo" else 0.0)
    # Rochester's name keeps 18 bp of white between its last letter and the Watertown pin
    rb = L.box("Rochester", 90, 262 + DY, "center")
    wx, wy = _city("Watertown")
    assert wx - 10 - rb[2] >= 18, (wx - 10 - rb[2])
    return b + L.body()


def b_degree():
    b = base() + shaded_dots(SHADE["degree"])
    L = Labels("ny-degree")
    L.add("degree", 372, 330, anchor="west", halo=False, rel=False, color="muted")
    for k, (s, t) in enumerate((("4+", 1.0), ("3", 0.55), ("1", 0.0))):
        y = 290 - k * 42
        b += ("\\filldraw[fill=%s,draw=ink!60,line width=0.9bp] (380,%d) circle (8bp);\n" % (F.shade(t), y))
        L.add(s, 400, y, anchor="west", halo=False, rel=False)
    L.nyc()
    return b + L.body()


def _single(name, measure, labels, key=None):
    L = Labels(name)
    i = WIN[measure]
    b = base() + shaded_dots(SHADE[measure]) + winner(i)
    labels(L, i)
    if key:
        return b + shade_key(L, b + L.body(), *key) + L.body()
    return b + L.body()


def _share60():
    """Share of the interchanges inside the 60 km circle around Manhattan."""
    inside = sum(1 for x, y in XY
                 if ((x - MANHATTAN[0]) / R60[1]) ** 2 + ((y - MANHATTAN[1]) / R60[0]) ** 2 <= 1)
    return inside / N


SHARE60 = _share60()
assert round(100 * SHARE60) == 31, SHARE60            # the slide says 31%


def b_closeness():
    L = Labels("ny-closeness")
    i = WIN["closeness"]
    b = base() + circle60() + shaded_dots(SHADE["closeness"]) + winner(i)
    L.add("Middletown", 100, 78, color="hot", to=XY[i], r=13, underline=True)
    ang = math.radians(225)
    L.add("31\\%", MANHATTAN[0] + R60[1] * math.cos(ang) - 14, MANHATTAN[1] + R60[0] * math.sin(ang) + 3,
          anchor="east", color="muted", rel=False)
    L.nyc()
    return b + shade_key(L, b + L.body(), "closeness", "high", "low") + L.body()


def b_eccentricity():
    def lab(L, i):
        L.add("Binghamton", 105, 80, color="muted", to=_city("Binghamton"), r=3)
        L.add("473 km", 160, 8, color="hot", to=XY[i], r=13, underline=True)
        L.nyc(spots=((322, 17.5, "center"),))        # the leader of "473 km" passes the usual spot
    # dark = the smaller worst case (the shade is 1 / eccentricity)
    return _single("ny-eccentricity", "eccentricity", lab, key=("worst case", "smaller", "larger"))


def b_betweenness():
    """The slide asks which CITY most trips pass through: Binghamton (of the eight cities, the
    most), hot with its brush underline.  Monticello, the busiest interchange of all, is named in
    muted ink and keeps its dark shade; ny-five (slide 128) still points at it."""
    L = Labels("ny-betweenness")
    assert _btw8[0] == "Binghamton"
    ib, im = CITY_ID["Binghamton"], WIN["betweenness"]
    b = base() + shaded_dots(SHADE["betweenness"]) + winner(ib)
    L.add("Binghamton", 105, 80, color="hot", to=_city("Binghamton"), r=15, underline=True)
    L.add("Monticello", 150, 8, color="muted", to=XY[im], r=8)
    L.nyc(spots=((322, 17.5, "center"),))
    return b + shade_key(L, b + L.body(), "betweenness", "high", "low") + L.body()


def b_eigenvector():
    L = Labels("ny-eigenvector")
    i = WIN["eigenvector"]
    sh = SHADE["eigenvector"]
    b = base() + circle60() + shaded_dots(sh) + winner(i)
    b += inset(sh, [(i, WIN_D)])
    ang = math.radians(225)
    L.add("60 km", MANHATTAN[0] + R60[1] * math.cos(ang) - 14, MANHATTAN[1] + R60[0] * math.sin(ang) + 3,
          anchor="east", color="muted", rel=False)
    L.nyc()
    zx, zy = Z(XY[i])
    L.add("Hempstead", 533, INS_Y0 - 28, anchor="east", color="hot", to=(zx, zy), r=13, rel=False,
          underline=True)
    return b + shade_key(L, b + L.body(), "eigenvector", "high", "low") + L.body()


def b_five():
    L = Labels("ny-five")
    b = base() + plain_dots(0.12)
    for m in ("eccentricity", "betweenness", "closeness", "eigenvector", "harmonic"):
        b += winner(WIN[m], d=12.0)
    b += inset(None, [(WIN["harmonic"], 14.0), (WIN["eigenvector"], 14.0)])
    spec = {                                   # measure: (x, y), map-relative
        "eccentricity": ("west", 10, 84),
        "betweenness": ("center", 120, 38),
        "closeness": ("center", 205, 0),
    }
    for m, (anc, x, y) in spec.items():
        L.add(m, x, y, anchor=anc, color="hot", to=XY[WIN[m]], r=9)
    zh, ze = Z(XY[WIN["harmonic"]]), Z(XY[WIN["eigenvector"]])
    L.add("harmonic", 533, INS_Y0 + INS_W + 28, anchor="east", color="hot", to=zh, r=10, rel=False)
    # in the white strip under Long Island, away from the Hudson-valley roads
    L.add("eigenvector", 533, 19, anchor="east", color="hot", to=ze, r=10, rel=False)
    L.nyc(spots=((410, 115, "center"),))     # on the box-to-inset leader's side
    return b + L.body()


NAMES = [("ny-overview", b_overview), ("ny-degree", b_degree), ("ny-closeness", b_closeness),
         ("ny-eccentricity", b_eccentricity), ("ny-betweenness", b_betweenness),
         ("ny-eigenvector", b_eigenvector), ("ny-five", b_five)]


def fig_ny():
    """All seven maps on one canvas and one crop (a map is dots and labels on one base)."""
    F.emit_group([(n, fn()) for n, fn in NAMES], container="col", h=CANVAS_H, nodes=False,
                 prefix=False)


FIGURES = [("ny-maps", fig_ny)]
