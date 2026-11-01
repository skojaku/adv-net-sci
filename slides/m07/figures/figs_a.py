#!/usr/bin/env python3
"""Worker A: the drawn scenes and the small graphs of the M07 deck.

    pearson-walker     L-c    a stick figure on a field, the first steps of a walk
    pearson-answer     L-g    5 paths and 10,000 end points (Pearson 1905)
    fields             L-b    pollen, mosquito, web: three fields, then "and on a network?"
    walk-rule          L-b    the rule: each of 4 edges carries 1/4
    two-comm-q         L-c    two 5-cliques and one edge, the walker in community 1
    two-comm-walk      L-b    the walk coloured by community, and the time strip
    clique-q / -a      L-a    a 10-clique and the distance curve (empty axes / the curve)
    twoclique-q / -a   L-a    the same for two 5-cliques joined by one edge
    no-larger          L-b    one step replaces every number by the average of its neighbours
    detailed-balance   L-a    the flow along one edge is equal in both directions
    tasks-diamond      L-c    the 4-node diamond and the QR placeholder for the Part 3 notebook

Every number comes from smallgraphs.py or is computed here from a seeded walk and asserted.
Community 1 is cool (blue), community 2 is hot (red); a walker is a ring in ink.
"""

import math

import numpy as np

import figlib as F
import smallgraphs as G

# The display caps of the deck's layouts (theme.css): B 480 (420 with a take), A 380 (320 with a
# sub and a take), G 600, C 470.  figlib's own table was written for the m04 container.
F.FIG_H.update({"a": 380, "at": 320, "b": 480, "bt": 420, "g": 600, "c": 470})

ARROW = "-{Stealth[length=10bp,width=8bp]}"
HEAD = "{Stealth[length=10bp,width=8bp]}"
CA, CB = "cool", "hot"                     # community 1 / community 2
FA, FB = "cool!45", "hot!45"               # their node fills


def comm_fill(n):
    return FA if n < 5 else FB


def edges_ink(edges, pos, color="ink", w=F.EDGE_W, opacity=None):
    return "".join(F.seg(pos[a], pos[b], color=color, w=w, opacity=opacity) for a, b in edges)


def discs_ink(pos, fills=None, size=F.NODE, labels=None):
    out = ""
    for n, p in pos.items():
        fill = (fills or {}).get(n, "white")
        out += F.disc(p[0], p[1], str((labels or {}).get(n, "")), fill=fill, size=size)
    return out


def pent(cx, cy, r, first_angle):
    """five points on a circle, the first at first_angle (degrees), counter-clockwise."""
    return [(cx + r * math.cos(math.radians(first_angle + 72 * k)),
             cy + r * math.sin(math.radians(first_angle + 72 * k))) for k in range(5)]


def two_clique_layout(cxa, cxb, cy, r):
    """TWOC: nodes 0-4 on the left pentagon (node 4 faces the right), 5-9 on the right (node 5
    faces the left); the bridge is the edge 4-5."""
    pos = {}
    for k, p in enumerate(pent(cxa, cy, r, 0)):
        pos[[4, 0, 1, 2, 3][k]] = p
    for k, p in enumerate(pent(cxb, cy, r, 180)):
        pos[[5, 6, 7, 8, 9][k]] = p
    return pos


TWOC_EDGES = [tuple(e) for e in G.TWOC.edges()]
assert len(TWOC_EDGES) == 21


def walk_nodes(P, start, steps, seed):
    return G.walk(P, start, steps, np.random.default_rng(seed))


# ============================================================================ pearson-walker
def f_pearson_walker():
    ox, oy = 186.0, 120.0                       # where the walker stands (screen)
    sh, sy = 0.28, 0.5                          # the field is drawn at an angle: shear and squash
    L = 70                                      # one yard, in field units

    def S(u, v):
        return (ox + u + sh * v, oy + sy * v)

    o = ""
    us = list(range(-140, 281, L))
    vs = list(range(-70, 211, L))
    for v in vs:
        o += F.seg(S(us[0], v), S(us[-1], v), color="muted", w=1.7, opacity=0.55)
    for u in us:
        o += F.seg(S(u, vs[0]), S(u, vs[-1]), color="muted", w=1.7, opacity=0.55)
    pts = [(0.0, 0.0)]
    for a in [38, 112, 8, -42, 76]:               # five steps of one yard, random directions
        pts.append((pts[-1][0] + L * math.cos(math.radians(a)), pts[-1][1] + L * math.sin(math.radians(a))))
    assert all(us[0] <= u <= us[-1] and vs[0] <= v <= vs[-1] for u, v in pts)
    sp = [S(u, v) for u, v in pts]
    o += F.polyline(sp, color="hot", w=5.0)
    for p in sp[1:]:
        o += F.dot(p[0], p[1], color="hot", d=13)
    x, y = sp[0]                                  # the stick figure, standing on the start
    o += F.sketch_circle(x, y + 118, 30, color="ink", w=3.2)
    for p, q in [((x, y + 103), (x, y + 50)), ((x, y + 50), (x - 20, y)), ((x, y + 50), (x + 20, y)),
                 ((x, y + 92), (x - 30, y + 62)), ((x, y + 92), (x + 30, y + 62))]:
        o += F.seg(p, q, color="ink", w=4.0)
    mid = ((sp[0][0] + sp[1][0]) / 2, (sp[0][1] + sp[1][1]) / 2)
    t, _ = F.aside("1 yard", at=(mid[0] + 40, mid[1] - 70), target=(mid[0] + 6, mid[1] - 8), anchor="north", bend=-30)
    o += t
    F.emit("pearson-walker", o, container="col", h=420, hmod="c", nodes=False)


# ============================================================================ pearson-answer
def _cloud(xy, side, cx, cy, ss=3):
    """10,000 translucent dots as one transparent PNG (10,000 TikZ fills exceed TeX's memory)."""
    from PIL import Image
    n = int(side * ss)
    r = 1.7 * ss
    k = int(2 * r + 3)
    yy, xx = np.mgrid[0:k, 0:k]
    stamp = (((xx - k / 2) ** 2 + (yy - k / 2) ** 2) <= r * r).astype(np.float32)
    cnt = np.zeros((n, n), dtype=np.float32)
    for x, y in xy:
        px, py = int((x + side / 2) * ss - k / 2), int((side / 2 - y) * ss - k / 2)
        cnt[py:py + k, px:px + k] += stamp
    out = np.zeros((n, n, 4), dtype=np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = 0x39, 0x59, 0xA6
    out[..., 3] = ((1 - 0.70 ** cnt) * 255).astype(np.uint8)
    path = F.OUT / "_cloud.png"
    Image.fromarray(out, "RGBA").save(path)
    return f"\\node at ({cx},{cy}) {{\\pgfimage[width={side}bp]{{{path}}}}};\n"


def f_pearson_answer():
    sc = 7.0                                    # px per yard; both panels the same
    cxl, cxr, cy = 215.0, 800.0, 215.0
    rng = np.random.default_rng(1905)
    o = ""
    # left: 5 walkers of 100 unit steps
    cols = ["cool!70", "hot!70", "deep!60", "tealc", "olivec"]
    for k in range(5):
        a = rng.uniform(0, 2 * np.pi, 100)
        xy = np.vstack([[0, 0], np.cumsum(np.c_[np.cos(a), np.sin(a)], axis=0)]) * sc
        assert np.abs(xy).max() < 190, "a path leaves its panel"
        o += F.polyline([(cxl + x, cy + y) for x, y in xy], color=cols[k], w=3.0)
        o += F.dot(cxl + xy[-1][0], cy + xy[-1][1], color=cols[k], d=10)
    # right: the end points of 10,000 walkers
    a = rng.uniform(0, 2 * np.pi, (10000, 100))
    end = np.c_[np.cos(a).sum(axis=1), np.sin(a).sum(axis=1)]
    rms = float(np.sqrt((end ** 2).sum(axis=1).mean()))
    assert abs(rms - 10) / 10 < 0.03, rms          # the typical distance after 100 unit steps is 10
    keep = (np.abs(end) * sc < 195).all(axis=1)
    assert keep.mean() > 0.995
    o += _cloud(end[keep] * sc, 400, cxr, cy)
    o += (f"\\draw[muted,line width=3bp,dash pattern=on 9bp off 7bp] ({cxr:.1f},{cy:.1f}) circle ({10 * sc:.1f}bp);\n")
    for cx in (cxl, cxr):
        o += F.disc(cx, cy, "", fill="ink", size=14)
    o += F.text(cxl, cy + 215, "5 walkers", anchor="south")
    o += F.text(cxr, cy + 215, "10,000 walkers", anchor="south")
    t, _ = F.aside("typical\\\\distance after\\\\100 steps", at=(600, cy - 70), target=(cxr - 10 * sc * 0.72, cy - 10 * sc * 0.70),
                   anchor="east", bend=-25)
    o += t
    t, _ = F.aside("the start", at=(cxl + 20, cy + 140), target=(cxl + 2, cy + 12), anchor="south", bend=30)
    o += t
    F.emit("pearson-answer", o, container="full", h=520, hmod="g", nodes=False)


# ============================================================================ fields
def f_fields():
    o = ""
    w, gap, top = 240.0, 20.0, 330.0                 # panel width, gap, panel top
    x0 = [8.0 + k * (w + gap) for k in range(3)]
    cap_y = 8.0
    # (1) pollen: the zig-zag trace of one grain
    rng = np.random.default_rng(1827)
    st = rng.normal(size=(70, 2))
    tr = np.cumsum(st, axis=0)
    tr = tr - tr.mean(axis=0)
    tr = tr / np.abs(tr).max(axis=0) * np.array([w / 2 - 14, 112.0])
    cx, cy = x0[0] + w / 2, cap_y + 100 + 130
    pts = [(cx + a, cy + b) for a, b in tr]
    o += F.polyline(pts, color="ink", w=2.4)
    o += F.dot(*pts[0], color="cool", d=14) + F.dot(*pts[-1], color="hot", d=14)
    # (2) a mosquito
    mx, my = x0[1] + w / 2, cap_y + 100 + 130
    o += f"\\fill[faint] ({mx - 12},{my + 8}) ellipse (46bp and 20bp);\n"
    o += f"\\draw[ink,line width=3bp,rotate around={{-12:({mx - 12},{my + 8})}}] ({mx - 12},{my + 8}) ellipse (46bp and 17bp);\n"
    o += f"\\fill[ink] ({mx + 52},{my + 24}) circle (13bp);\n"
    o += F.seg((mx + 62, my + 30), (mx + 112, my + 56), color="ink", w=3.2)          # proboscis
    o += F.seg((mx - 54, my + 4), (mx - 100, my - 6), color="ink", w=3.4)             # tail
    for dx, rot in ((8, 28), (-18, 18)):                                                # wings
        o += (f"\\draw[ink,line width=2.4bp,fill=white,opacity=0.9,rotate around={{{rot}:({mx + dx},{my + 40})}}] "
              f"({mx + dx},{my + 62}) ellipse (14bp and 44bp);\n")
    for dx, e in ((14, 30), (-6, 26), (-26, 22)):                                      # six legs
        o += F.seg((mx + dx, my - 6), (mx + dx + e * 0.5, my - 56), color="ink", w=2.6)
        o += F.seg((mx + dx, my - 6), (mx + dx - e * 0.9, my - 52), color="ink", w=2.6)
    # (3) the web: a small graph with a surfer
    wx, wy = x0[2], cap_y + 100 + 130
    wpos = {0: (wx + 34, wy + 70), 1: (wx + 122, wy + 100), 2: (wx + 206, wy + 38), 3: (wx + 50, wy - 70),
            4: (wx + 140, wy - 28), 5: (wx + 208, wy - 90)}
    wed = [(0, 1), (1, 2), (0, 4), (1, 4), (3, 4), (4, 5), (2, 5), (3, 0)]
    for a, b in wed:
        o += F.seg(wpos[a], wpos[b], color="ink", w=2.6)
    o += discs_ink(wpos, size=F.NODE)
    o += F.ring(*wpos[4], size=F.NODE, color="hot", w=3.4, grow=16)
    # captions
    for k, cap in enumerate(["pollen in\\\\water, 1905", "mosquitoes\\\\and malaria", "the web,\\\\1998"]):
        o += F.text(x0[k] + w / 2, cap_y + 82, cap, anchor="north")
    # the arrow and the aside
    ax = x0[2] + w + 6
    o += F.seg((ax + 8, 240), (ax + 66, 240), color="muted", w=4.2, arrow=ARROW, sketch=False)
    o += F.text(ax + 88, 247, "and on a\\\\network?", color="muted", anchor="west", size=F.FONT_HAND, hand=True)
    F.emit("fields", o, container="full", h=420, hmod="b", nodes=True)


# ============================================================================ walk-rule
RULE_PX = {0: (540, 262), 1: (150, 372), 2: (62, 182), 3: (935, 372), 4: (1018, 182), 5: (790, 34), 6: (290, 34)}


def f_walk_rule():
    pos = RULE_PX
    edges = [tuple(e) for e in G.RULE.edges()]
    F.assert_planar_drawing(edges, pos, "walk-rule")
    o = edges_ink(edges, pos, color="ink", w=2.8)
    o += discs_ink(pos, fills={0: "white"})
    o += F.ring(*pos[0], size=F.NODE, color="ink", w=3.0, grow=22)
    for nb in (1, 2, 3, 4):
        (x0, y0), (x1, y1) = pos[0], pos[nb]
        mx, my = x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.5
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        nx_, ny_ = -dy / L, dx / L
        if ny_ < 0:                                  # put every label on the upper side of its edge
            nx_, ny_ = -nx_, -ny_
        o += f"\\fill[white] ({mx + nx_ * 34 - 36:.1f},{my + ny_ * 34 - 21:.1f}) rectangle ({mx + nx_ * 34 + 36:.1f},{my + ny_ * 34 + 21:.1f});\n"
        o += F.text(mx + nx_ * 34, my + ny_ * 34, "1/4", color="hot", anchor="center")
    t, _ = F.aside("no memory of where\\\\it came from", at=(540, 90), target=(540, pos[0][1] - 40),
                   anchor="south", bend=0)
    o += t
    F.emit("walk-rule", o, container="full", h=450, hmod="b", nodes=True)


# ============================================================================ two-comm-q
def f_two_comm_q():
    pos = two_clique_layout(130, 407, 215, 78)
    o = ""
    for cx, col in ((130, CA), (407, CB)):
        o += (f"\\draw[{col},line width=2.6bp,dash pattern=on 10bp off 7bp,opacity=0.65] "
              f"({cx},215) circle (124bp);\n")
    inner = [e for e in TWOC_EDGES if e != (4, 5)]
    o += edges_ink(inner, pos, color="ink", w=2.2, opacity=0.8)
    o += F.seg(pos[4], pos[5], color="ink", w=F.HEAVY_W)
    o += discs_ink(pos, fills={n: comm_fill(n) for n in pos})
    o += F.ring(*pos[2], size=F.NODE, color="ink", w=3.0, grow=20)
    mid = ((pos[4][0] + pos[5][0]) / 2, 215)
    t, _ = F.aside("one edge", at=(mid[0], 395), target=(mid[0], 222), anchor="south", bend=0, gap=10)
    o += t
    F.emit("two-comm-q", o, container="col", h=480, hmod="c", nodes=True)


# ============================================================================ two-comm-walk
def _find_walk(P, comm, steps=400):
    """A seeded walk from node 0 whose first 60 steps cross once or more and whose mean run
    length (steps per visit to a community) is within 14 to 30."""
    for seed in range(1, 400):
        path = G.walk(P, 0, steps, np.random.default_rng(seed))
        c = comm[path]
        runs = 1 + int((c[1:] != c[:-1]).sum())
        cross = np.flatnonzero(c[:61] != c[0])
        if 19 <= steps / runs <= 23 and len(cross) and 12 <= cross[0] <= 40 and (c[:61] != c[0]).sum() >= 12:
            return seed, path, steps / runs
    raise AssertionError("no seed gives a walk with runs of 19-23 steps")


def f_two_comm_walk():
    comm = np.array([0] * 5 + [1] * 5)
    seed, path, mean_run = _find_walk(G.PTC, comm)
    assert 19 <= mean_run <= 23
    pos = two_clique_layout(120, 390, 215, 88)
    rng = np.random.default_rng(seed)
    jit = {i: (rng.normal(0, 5), rng.normal(0, 5)) for i in range(61)}
    pts = [(pos[n][0] + jit[i][0], pos[n][1] + jit[i][1]) for i, n in enumerate(path[:61])]
    o = ""
    inner = TWOC_EDGES
    o += edges_ink(inner, pos, color="muted", w=2.0, opacity=0.6)
    # runs of one colour along the first 60 steps (a step takes the colour of the node it leaves)
    i = 0
    while i < 60:
        j = i
        while j < 60 and comm[path[j]] == comm[path[i]]:
            j += 1
        o += F.brush(pts[i:j + 1], color=CB if comm[path[i]] else CA, w=8.0, opacity=0.95, strands=5, seed=i)
        i = j
    o += discs_ink(pos, fills={n: "white" for n in pos}, size=F.NODE)
    o += F.ring(*pos[0], size=F.NODE, color="ink", w=3.0, grow=20)
    # the time strip: 400 steps, one cell per step, merged into runs
    sx0, sx1, sy0, sy1 = 580.0, 1060.0, 160.0, 225.0
    cw = (sx1 - sx0) / 400
    c = comm[path[:400]]
    k = 0
    while k < 400:
        m = k
        while m < 400 and c[m] == c[k]:
            m += 1
        o += f"\\fill[{CB if c[k] else CA}] ({sx0 + k * cw:.2f},{sy0}) rectangle ({sx0 + m * cw:.2f},{sy1});\n"
        k = m
    o += f"\\draw[ink,line width=2.4bp] ({sx0},{sy0}) rectangle ({sx1},{sy1});\n"
    o += F.seg((sx0, sy0 - 26), (sx1 + 6, sy0 - 26), color="ink", w=3.0, arrow=ARROW, sketch=False)
    o += F.text(sx1, sy0 - 40, "time", anchor="north east")
    # the longest run gets the aside
    runs, k = [], 0
    while k < 400:
        m = k
        while m < 400 and c[m] == c[k]:
            m += 1
        runs.append((k, m))
        k = m
    a, b = max(runs, key=lambda r: r[1] - r[0])
    tx = sx0 + (a + b) / 2 * cw
    t, _ = F.aside("about 21 steps\\\\per visit", at=(min(tx, sx1 - 170), sy1 + 95),
                   target=(tx, sy1 + 5), anchor="south", bend=0)
    o += t
    F.emit("two-comm-walk", o, container="full", h=430, hmod="b", nodes=True)
    print(f"    two-comm-walk: seed {seed}, mean run {mean_run:.1f} steps, {len(runs)} runs")


# ============================================================================ clique / twoclique pairs
AXBOX = (540.0, 128.0, 1040.0, 292.0)


def _inset_axes(xmax, xticks):
    ax = F.Axes(AXBOX, (0, xmax), (0, 2), xlabel="steps", ylabel="distance", xticks=xticks,
                yticks=[0, 1, 2], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{int(v)}")
    o = ax.frame()
    o += F.seg(ax.P(0, G.EPS), ax.P(xmax, G.EPS), color="muted", w=2.6, dash=F.DASH)
    o += F.text(ax.X(xmax) + 6, ax.Y(G.EPS) + 2, "$\\epsilon$", color="muted", anchor="west", size=F.FONT_MATH)
    return ax, o


def _curve(ax, ts, d, color, label=None):
    o = F.polyline([ax.P(t, v) for t, v in zip(ts, d)], color=color, w=4.2)
    for t, v in zip(ts, d):
        o += F.dot(*ax.P(t, v), color=color, d=11)
    return o


def f_clique():
    pos = {k: (150 + 112 * math.cos(math.radians(90 - 36 * k)), 150 + 112 * math.sin(math.radians(90 - 36 * k)))
           for k in range(10)}
    edges = [tuple(e) for e in G.CLIQUE10.edges()]
    assert len(edges) == 45
    q = edges_ink(edges, pos, color="ink", w=1.6, opacity=0.55)
    q += discs_ink(pos)
    q += F.ring(*pos[0], size=F.NODE, color="ink", w=3.0, grow=18)
    ax, a_ = _inset_axes(4, [0, 1, 2, 3, 4])
    q += a_
    ts = list(range(0, 5))
    d = G.worst_dist(G.PC10, G.PIC10, ts)
    assert d[0] > 1.5 and d[1] <= G.EPS and G.mixing_time(G.PC10, G.PIC10, G.EPS) == 1
    a = q + _curve(ax, ts, d, "hot")
    a += F.seg(ax.P(1, d[1]), ax.P(1, 0), color="hot", w=2.6, dash=F.DASH)
    a += F.ring(*ax.P(1, d[1]), size=F.NODE - 12, color="hot", w=3.0, grow=10)
    F.emit_group([("clique-q", q), ("clique-a", a)], container="full", h=330, hmod="at", nodes=True)


def f_twoclique():
    pos = two_clique_layout(100, 322, 150, 64)
    q = ""
    inner = [e for e in TWOC_EDGES if e != (4, 5)]
    q += edges_ink(inner, pos, color="ink", w=2.0, opacity=0.8)
    q += F.seg(pos[4], pos[5], color="ink", w=F.HEAVY_W)
    q += discs_ink(pos, fills={n: comm_fill(n) for n in pos})
    q += F.ring(*pos[2], size=F.NODE, color="ink", w=3.0, grow=20)
    ax, a_ = _inset_axes(30, [0, 10, 20, 30])
    q += a_
    ts = list(range(0, 31))
    d = G.worst_dist(G.PTC, G.PITC, ts)
    dc = G.worst_dist(G.PC10, G.PIC10, ts)
    tm = G.mixing_time(G.PTC, G.PITC, G.EPS)
    assert tm == 20 and d[tm] <= G.EPS < d[tm - 1]
    a = q
    a += F.polyline([ax.P(t, v) for t, v in zip(ts, dc)], color="muted", w=3.6)
    a += F.text(ax.X(3) + 18, ax.Y(0.8) + 14, "10-clique", color="muted", anchor="west")
    a += F.polyline([ax.P(t, v) for t, v in zip(ts, d)], color="hot", w=4.4)
    a += F.seg(ax.P(tm, d[tm]), ax.P(tm, 0), color="hot", w=2.6, dash=F.DASH)
    a += F.ring(*ax.P(tm, d[tm]), size=F.NODE - 12, color="hot", w=3.0, grow=10)
    F.emit_group([("twoclique-q", q), ("twoclique-a", a)], container="full", h=330, hmod="at", nodes=True)


# ============================================================================ no-larger
NL_VALUES = np.array([1, 4, 9, 6, 5, 5, 7])


def f_no_larger():
    A = G.adj(G.RULE, range(7))
    P = G.trans(A)
    v0 = NL_VALUES.astype(float)
    v1 = P @ v0
    assert np.allclose(v1, np.round(v1)) and v0.max() == 9 and v1.max() < v0.max(), (v0, v1)
    assert v0.argmax() == 2 and (v1 <= v0.max()).all() and (v1 >= v0.min()).all()
    sx = lambda x0: {0: (x0 + 175, 240), 1: (x0 + 55, 390), 2: (x0 + 30, 170), 3: (x0 + 330, 370),
                     4: (x0 + 330, 170), 5: (x0 + 235, 55), 6: (x0 + 105, 55)}
    edges = [tuple(e) for e in G.RULE.edges()]
    o = ""
    for x0, vals in ((20.0, v0), (700.0, v1)):
        pos = sx(x0)
        F.assert_planar_drawing(edges, pos, "no-larger")
        o += edges_ink(edges, pos, color="ink", w=2.4)
        fills = {n: ("hot" if vals[n] == vals.max() else "white") for n in pos}
        o += discs_ink(pos, fills=fills, size=F.NODE, labels={n: int(vals[n]) for n in pos})
        o += F.text(x0 + 190, 445, "largest: %d" % vals.max(), anchor="south", color="hot")
    o += F.seg((420, 240), (680, 240), color="muted", w=4.4, arrow=ARROW, sketch=False)
    o += F.text(550, 270, "one step: every\\\\number becomes the\\\\average of its\\\\neighbours", color="muted", anchor="south")
    F.emit("no-larger", o, container="full", h=520, hmod="b", nodes=True)


# ============================================================================ detailed-balance
def f_detailed_balance():
    # 5 edges in all: i has 3 (one to j, two to others), j has 2 (one to i, one to another); 2m = 10
    k_i, k_j, two_m = 3, 2, 10
    pi_i, pi_j = k_i / two_m, k_j / two_m
    assert math.isclose(pi_i / k_i, pi_j / k_j) and math.isclose(pi_i / k_i, 0.1)
    xi, xj, y = 275.0, 805.0, 210.0
    o = ""
    for dy in (62, -62):
        o += F.seg((xi, y), (xi - 150, y + dy), color="muted", w=2.8)
    o += F.seg((xj, y), (xj + 160, y), color="muted", w=2.8)
    o += F.disc(xi - 150, y + 62, "", fill="pale") + F.disc(xi - 150, y - 62, "", fill="pale")
    o += F.disc(xj + 160, y, "", fill="pale")
    o += F.disc(xi, y, "i", fill="white") + F.disc(xj, y, "j", fill="white")
    o += (f"\\draw[ink,line width=3.4bp,{ARROW}] ({xi + 30},{y + 16}) to[bend left=20] ({xj - 30},{y + 16});\n")
    o += (f"\\draw[ink,line width=3.4bp,{ARROW}] ({xj - 30},{y - 16}) to[bend left=20] ({xi + 30},{y - 16});\n")
    o += F.text((xi + xj) / 2, y + 80, "$\\pi_i\\cdot\\frac{1}{k_i}=0.3\\cdot\\frac{1}{3}=0.1$", size=F.FONT_MATH, anchor="south")
    o += F.text((xi + xj) / 2, y - 80, "$\\pi_j\\cdot\\frac{1}{k_j}=0.2\\cdot\\frac{1}{2}=0.1$", size=F.FONT_MATH, anchor="north")
    o += F.text((xi + xj) / 2, y, "the same flow both ways", color="muted", size=F.FONT_HAND, hand=True)
    F.emit("detailed-balance", o, container="full", h=420, hmod="at", nodes=True)


# ============================================================================ tasks-diamond
def f_tasks_diamond():
    xy = G.DIAMOND_XY
    pos = {n: (40 + 62 * x, 130 + 66 * y) for n, (x, y) in xy.items()}
    edges = [tuple(e) for e in G.DIAMOND.edges()]
    F.assert_planar_drawing(edges, pos, "tasks-diamond")
    o = edges_ink(edges, pos, color="ink", w=2.8)
    o += discs_ink(pos, labels={n: n for n in pos})
    o += F.text(130, 78, "Part 2", anchor="south")
    bx0, by0, bx1, by1 = 312, 110, 527, 330
    o += f"\\draw[muted,line width=3bp,dash pattern=on 12bp off 8bp] ({bx0},{by0}) rectangle ({bx1},{by1});\n"
    o += F.text((bx0 + bx1) / 2, (by0 + by1) / 2 + 6, "QR code\\\\Part 3\\\\notebook", color="muted", anchor="center")
    F.emit("tasks-diamond", o, container="col", h=360, hmod="c", nodes=True)


FIGURES = [
    ("pearson-walker", f_pearson_walker), ("pearson-answer", f_pearson_answer), ("fields", f_fields),
    ("walk-rule", f_walk_rule), ("two-comm-q", f_two_comm_q), ("two-comm-walk", f_two_comm_walk),
    ("clique", f_clique), ("twoclique", f_twoclique), ("no-larger", f_no_larger),
    ("detailed-balance", f_detailed_balance), ("tasks-diamond", f_tasks_diamond),
]

if __name__ == "__main__":
    F.run(FIGURES)
