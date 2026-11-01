#!/usr/bin/env python3
"""Module 07, worker C: the plots.

    degree-share      scatter, degree against the share of visits (karate club, 20,000 steps)
    lam-curves-q/-a   |lambda_k|^t against t for the twelve eigenvalues; the answer marks lambda_2
    mix-1/2/3         distance to pi against t (one curve per start, the worst start in black), then epsilon, then t_mix
    gap-gauge         lambda_2 on a gauge with the relaxation time of five networks
    eigvec2           the second eigenvector of P, one dot per node
    comm-curve        probability of being in community 1 against the steps

Every number comes from smallgraphs.py or is computed here and asserted. `summary` is built last by the lead.
"""

import numpy as np

import figlib as F
import smallgraphs as G

# a 756 px figure (70 % of the slide width) for the slide with the explanation beside it; theme cap 480 px
F.DESIGN["wide"] = F.CONTAINER["wide"] = 756
F.FIG_H["w"] = 480

# the walks behind degree-share
DS_SEED, DS_STEPS = 0, 20000

BLUE, RED = "cool", "hot"
FAINTLINE = "muted!55"


# --------------------------------------------------------------------------- a collision gate for every drawn text box
def _vis(line):
    """Visible characters of a label: TeX commands count as one glyph, braces and ^ _ $ none."""
    import re
    line = re.sub(r"\\[a-zA-Z]+", "x", line)
    return len(re.sub(r"[{}$^_\\]", "", line))


def text_box(x, y, s, anchor, size, pad=2):
    lines = s.split("\\\\")
    k = 0.5 if "$" in s else (0.52 if size == F.FONT_HAND else 0.6)
    w = max(_vis(l) for l in lines) * k * size + 2 * pad
    h = 1.1 * size * len(lines) + 2 * pad
    ax = {"center": 0.0, "west": 0.5, "east": -0.5, "north": 0.0, "south": 0.0}[anchor]
    ay = {"center": 0.0, "west": 0.0, "east": 0.0, "north": -0.5, "south": 0.5}[anchor]
    cx, cy = x + ax * w, y + ay * h
    return (cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)


class Gate:
    """Every text box and every curve of a figure: fail if a text box meets a curve, a dot or another box."""

    def __init__(self, name):
        self.name, self.boxes, self.lines, self.dots = name, [], [], []

    def text(self, x, y, s, anchor="center", size=F.FONT, color="ink", rot=None, hand=False, own=""):
        self.boxes.append((s, text_box(x, y, s, anchor, size), own))
        return F.text(x, y, s, color=color, anchor=anchor, size=size, rot=rot, hand=hand)

    def box(self, s, b, own=""):
        self.boxes.append((s, b, own))

    def line(self, pts, tag=""):
        self.lines.append((tag, [tuple(p) for p in pts]))

    def dot(self, x, y, r=7, tag=""):
        self.dots.append((tag, x, y, r))

    def check(self):
        bad = []
        for i, (s, b, own) in enumerate(self.boxes):
            for s2, b2, _ in self.boxes[i + 1:]:
                if F.boxes_overlap(b, b2):
                    bad.append(f"text {s!r} meets text {s2!r}")
            for tag, pts in self.lines:
                if tag and tag == own:
                    continue
                if any(F.box_hits_segment(b, p, q, pad=3) for p, q in zip(pts, pts[1:])):
                    bad.append(f"text {s!r} meets curve {tag!r}")
            for tag, x, y, r in self.dots:
                if tag and tag == own:
                    continue
                if not (b[2] < x - r or x + r < b[0] or b[3] < y - r or y + r < b[1]):
                    bad.append(f"text {s!r} meets dot {tag!r}")
        assert not bad, f"{self.name}: " + "; ".join(bad[:6]) + " -- shorten the note or move it, never shrink the type"


def arrow(p, q, color="muted", w=1.6, bend=0):
    path = (f"({p[0]:.1f},{p[1]:.1f}) to[bend left={bend}] ({q[0]:.1f},{q[1]:.1f})" if bend
            else f"({p[0]:.1f},{p[1]:.1f}) -- ({q[0]:.1f},{q[1]:.1f})")
    return f"\\draw[{color},line width={w}bp,line cap=round,-{{Stealth[length=9bp,width=7bp]}}] {path};\n"


def dashed(p, q, color="muted", w=1.8):
    return f"\\draw[{color},line width={w}bp,{F.DASH}] ({p[0]:.1f},{p[1]:.1f}) -- ({q[0]:.1f},{q[1]:.1f});\n"


def frame(ax, ticks_x=None, ticks_y=None):
    """The two spines and the ticks, no axis titles (they are placed by hand)."""
    ax.xticks = ticks_x if ticks_x is not None else ax.xticks
    ax.yticks = ticks_y if ticks_y is not None else ax.yticks
    return ax.frame()


def tick_boxes(ax, gate):
    """Register the tick labels so a note cannot land on them."""
    for v in ax.xticks:
        if ax.xlim[0] <= v <= ax.xlim[1]:
            gate.box(ax.xfmt(v), text_box(ax.X(v), ax.y0 - 17, ax.xfmt(v), "north", ax.size))
    for v in ax.yticks:
        if ax.ylim[0] <= v <= ax.ylim[1]:
            gate.box(ax.yfmt(v), text_box(ax.x0 - 17, ax.Y(v), ax.yfmt(v), "east", ax.size, pad=(-3 if ax.ylog else 2)))


# --------------------------------------------------------------------------- degree-share
def f_degree_share():
    rng = np.random.default_rng(DS_SEED)
    share = G.visit_share(G.PK, 0, DS_STEPS, rng)
    deg = G.AK.sum(axis=1)
    assert abs(share.sum() - 1) < 1e-9 and deg[33] == 17 and deg[11] == 1
    r33, r11 = deg[33] / share[33], deg[11] / share[11]
    assert abs(r33 - 156) / 156 < 0.25 and abs(r11 - 156) / 156 < 0.40, (r33, r11)
    assert np.corrcoef(deg, share)[0, 1] > 0.99

    ax = F.Axes((130, 62, 930, 252), (0, 18), (0, 0.13), xticks=[0, 5, 10, 15], yticks=[0, 0.05, 0.1],
                yfmt=lambda v: f"{v:g}")
    g = Gate("degree-share")
    o = frame(ax)
    tick_boxes(ax, g)
    # the law: y = x / 2m
    xs = np.array([0, 18])
    line = [ax.P(x, x / 156) for x in xs]
    o += F.polyline(line, color="muted", w=2.2, dash=F.DASH)
    g.line(line, "law")
    for d, s in zip(deg, share):
        o += F.dot(*ax.P(d, s), color=BLUE, d=12)
        g.dot(*ax.P(d, s), r=7, tag=f"d{int(d)}")
    # the two nodes of the sheet
    for node, tag in ((33, "d17"), (11, "d1")):
        p = ax.P(deg[node], share[node])
        o += F.ring(*p, size=12, grow=14, color="hot", w=2.8)
    p33, p11 = ax.P(17, share[33]), ax.P(1, share[11])
    s33 = f"17 ÷ {share[33]:.3f} = {r33:.0f}"
    s11 = f"1 ÷ {share[11]:.4f} = {r11:.0f}"
    # 156 is what the law says; the walk gives a nearby number, so write what the walk gave
    ay = ax.y1 + 8
    o += g.text(p33[0] - 40, ay, s33, anchor="east", color="hot")
    o += arrow((p33[0] - 34, ay - 8), (p33[0] - 12, p33[1] + 8), color="hot")
    by = ax.Y(0.0125)
    o += g.text(p11[0] + 150, by, s11, anchor="west", color="hot")
    o += arrow((p11[0] + 146, by + 4), (p11[0] + 12, p11[1] - 2), color="hot")
    # axis names, by hand: the plot is short
    o += g.text(ax.x0 + 14, ax.y1 + 22, "share of visits", anchor="west", color="muted")
    o += g.text(ax.x1 + 14, ax.y0, "degree", anchor="west", color="muted")
    g.check()
    F.emit("degree-share", o, container="full", h=330, hmod="tight", nodes=False)


# --------------------------------------------------------------------------- lam-curves
LAMS = G.LAM12
TMAX = 40


def _lam_axes():
    return F.Axes((92, 78, 480, 330), (0, TMAX), (0, 1), xticks=[0, 10, 20, 30, 40], yticks=[0, 0.5, 1],
                  yfmt=lambda v: f"{v:g}")


def _curve(ax, lam):
    ts = np.arange(0, TMAX + 1)
    ys = np.abs(lam) ** ts
    ys[0] = 1.0
    return [ax.P(t, y) for t, y in zip(ts, ys)]


def _lam_base(answer):
    ax = _lam_axes()
    g = Gate("lam-curves")
    o = frame(ax)
    tick_boxes(ax, g)
    curves = {}
    for k, lam in enumerate(LAMS):
        c = _curve(ax, lam)
        curves[k] = c
        if k in (0, 1):
            continue
        o += F.polyline(c, color=FAINTLINE, w=2.4)
        g.line(c, f"l{k}")
    o += F.polyline(curves[1], color=RED if answer else FAINTLINE, w=5.0 if answer else 2.6)
    g.line(curves[1], "l1")
    o += F.polyline(curves[0], color=BLUE, w=5.0)
    g.line(curves[0], "l0")
    # axis names
    o += g.text(ax.x0 + 6, ax.y1 + 34, "$|\\lambda|^{t}$", anchor="west", size=F.FONT_MATH)
    o += g.text(ax.x1 + 30, ax.y0, "$t$", anchor="west", size=F.FONT_MATH)
    return ax, g, o, curves


def f_lam_q():
    ax, g, o, curves = _lam_base(False)
    o += g.text(ax.X(31), ax.Y(1) - 34, "$\\lambda_1$", size=F.FONT_MATH, color="cool")
    # label the slow curve and the bundle that drops fast
    c = curves[1]
    o += g.text(ax.X(26), ax.Y(0.889 ** 26) + 40, "$\\lambda_2$", size=F.FONT_MATH)
    o += g.text(ax.X(4.5), ax.Y(0.13), "rest", anchor="west", color="muted")
    g.check()
    F.emit("lam-curves-q", o, container="col", h=400, hmod="tall", nodes=False)


def f_lam_a():
    ax, g, o, curves = _lam_base(True)
    o += g.text(ax.X(31), ax.Y(1) - 34, "$\\lambda_1$", size=F.FONT_MATH, color="cool")
    assert abs(LAMS[1] - 0.889) < 5e-4
    vals = {5: 0.553, 10: 0.306, 40: 0.0}
    for t in (5, 10, 40):
        v = abs(LAMS[1]) ** t
        assert abs(v - {5: 0.55, 10: 0.31, 40: 0.01}[t]) < 0.006, (t, v)
        o += F.dot(*ax.P(t, v), color=RED, d=16)
    o += g.text(ax.X(5) + 22, ax.Y(0.553) + 28, "0.55", anchor="west", color="hot", own="l1")
    o += g.text(ax.X(10) + 22, ax.Y(0.306) + 28, "0.31", anchor="west", color="hot", own="l1")
    o += g.text(ax.X(40) - 6, ax.Y(0.009) + 44, "0.01", anchor="east", color="hot", own="l1")
    o += g.text(ax.X(19), ax.Y(0.66), "$\\lambda_2 = 0.89$", anchor="west", size=F.FONT_MATH, color="hot")
    g.check()
    F.emit("lam-curves-a", o, container="col", h=400, hmod="tall", nodes=False)


# --------------------------------------------------------------------------- mix-1..3
MT = 30
TS = list(range(0, MT + 1))
DIST = G.dist_by_start(G.P12, G.PI12, TS)
WORST = DIST.max(axis=0)
TMIX = G.TMIX12
assert WORST[TMIX] <= G.EPS < WORST[TMIX - 1], (WORST[TMIX - 1], WORST[TMIX])
assert np.isclose(G.worst_dist(G.P12, G.PI12, TS)[TMIX], WORST[TMIX])
# the late tail follows lambda_2^t
assert abs(WORST[30] / WORST[20] - G.LAM12[1] ** 10) < 0.03


# semilog: after t = 2 every start is a straight line of slope ln(lambda_2); the start only moves the line
_late = np.log(WORST[15:31])
_fit = np.polyfit(np.arange(15, 31), _late, 1)
assert abs(_fit[0] - np.log(G.LAM12[1])) < 0.002, _fit                      # the slope is ln(lambda_2)
assert np.abs(np.exp(np.polyval(_fit, np.arange(15, 31))) / WORST[15:31] - 1).max() < 0.03   # a straight line within 3 %
REF = lambda t: np.exp(np.polyval(_fit, t))                                  # the reference line


# the start nodes fall into classes by the number of friends: 4 and 5 friends give the highest, almost identical lines,
# the bridge ends (6 friends) the lowest
_DEG = G.A12.sum(axis=1).astype(int)
_CLASS_END = {k: DIST[[i for i in range(12) if _DEG[i] == k][0], 30] for k in (4, 5, 6)}
assert _CLASS_END[6] < _CLASS_END[4] < _CLASS_END[5] and _CLASS_END[5] / _CLASS_END[6] > 1.3, _CLASS_END
assert abs(_CLASS_END[5] / _CLASS_END[4] - 1) < 0.03          # 4 and 5 friends: one line at this scale
assert all(np.isclose(DIST[i], DIST[j]).all() for i in range(12) for j in range(12) if _DEG[i] == _DEG[j])


def _mix_axes():
    return F.Axes((110, 118, 800, 350), (0, MT), (0.01, 2), ylog=True, xticks=[0, 10, 20, 30],
                  yticks=[0.01, 0.1, 1, 2], yfmt=lambda v: f"{v:g}")


def _mix_base(g):
    ax = _mix_axes()
    o = frame(ax)
    tick_boxes(ax, g)
    seen = set()
    for i in range(12):
        key = tuple(np.round(DIST[i], 6))
        if key in seen:                      # twelve starts, three distinct curves: draw each once
            continue
        seen.add(key)
        pts = [ax.P(t, d) for t, d in zip(TS, DIST[i])]
        o += F.polyline(pts, color="muted!70", w=2.6)
        g.line(pts, "start")
    # the straight line of slope ln(lambda_2) through the late part of the worst curve, extended back to t = 0
    rpts = [ax.P(t, REF(t)) for t in np.linspace(0, MT, 31)]
    o += F.polyline(rpts, color="hot", w=2.6, dash=F.DASH)
    g.line(rpts, "ref")
    pts = [ax.P(t, d) for t, d in zip(TS, WORST)]
    o += F.polyline(pts, color="ink", w=5.0)
    g.line(pts, "worst")
    # the classes, labelled at their right end by the number of friends of the start node
    yu, yl = ax.Y(_CLASS_END[5]), ax.Y(_CLASS_END[6])
    o += F.seg((ax.x1 + 8, yu), (ax.x1 + 20, yu + 24), color="muted", w=1.6, sketch=False)
    o += g.text(ax.x1 + 24, yu + 34, "4 or 5 friends", anchor="west", size=F.FONT, color="muted")
    o += F.seg((ax.x1 + 8, yl), (ax.x1 + 20, yl - 24), color="muted", w=1.6, sketch=False)
    o += g.text(ax.x1 + 24, yl - 34, "6 friends", anchor="west", size=F.FONT, color="muted")
    o += g.text(ax.x1 + 40, ax.y0 - 40, "$t$", anchor="west", size=F.FONT_MATH)
    o += g.text(ax.x1 - 8, ax.Y(0.235), "distance to $\\pi$", anchor="east", size=F.FONT_MATH)
    return ax, o


def _mix_notes(ax, g):
    o = ""
    # where you start matters at first (the curves leave the straight line before t = 2)
    tx, ty = ax.X(8.0), ax.Y(1.25)
    o += g.text(tx, ty, "where you start\\\\matters at first", anchor="west", size=F.FONT_HAND, hand=True, color="muted")
    o += arrow((tx - 10, ty - 8), (ax.X(1.5), ax.Y(1.12)))
    # lambda_2 dominates the tail: a straight line on this axis
    lx, ly = ax.X(8.6), ax.Y(0.0215)
    o += g.text(lx, ly, "$\\lambda_2$ dominates:\\\\a straight line", anchor="west", size=F.FONT_MATH, color="muted")
    return o


def _mix_eps(ax, g):
    y = ax.Y(G.EPS)
    o = dashed((ax.x0, y), (ax.x1 + 24, y), color="ink", w=2.0)
    # the usual choice: total variation 1/4 is 1/2 in the 1-norm of the lecture note
    o += g.text(ax.x1 + 34, y, "$\\epsilon = 1/2$", anchor="west", size=F.FONT_MATH, color="ink")
    o += g.text(ax.x1 - 8, ax.Y(1.15), "the usual\\\\choice", anchor="east", size=F.FONT_HAND, hand=True, color="muted")
    return o, y


def _mix_final(ax, g, y):
    p = ax.P(TMIX, WORST[TMIX])
    o = F.dot(*p, color=RED, d=22)
    o += f"\\draw[hot,line width=3bp,line cap=round] ({p[0]:.1f},{p[1]:.1f}) -- ({p[0]:.1f},{ax.y0 - 78:.1f});\n"
    o += g.text(p[0], ax.y0 - 84, "mixing time", anchor="north", color="hot")
    return o


def f_mix():
    frames = []
    for build in (1, 2, 3):
        g = Gate(f"mix-{build}")
        ax, o = _mix_base(g)
        o += _mix_notes(ax, g)
        if build >= 2:
            e, y = _mix_eps(ax, g)
            o += e
        if build >= 3:
            o += _mix_final(ax, g, y)
        g.check()
        frames.append(o)
    names = ["mix-1", "mix-2", "mix-3"]
    F.emit_group(list(zip(names, frames)), container="full", h=430, hmod="", nodes=False, prefix=False)


# --------------------------------------------------------------------------- relax-curve
def f_relax_curve():
    lam = G.LAM12[1]
    tau = 1 / (1 - lam)
    assert abs(tau - 9.0) < 0.05 and abs(lam ** tau - 1 / np.e) < 0.03, (tau, lam ** tau)
    ax = F.Axes((140, 110, 1000, 250), (0, 30), (0, 1), xticks=[0, 10, 20, 30], yticks=[0, 1],
                yfmt=lambda v: f"{v:g}")
    g = Gate("relax-curve")
    o = frame(ax)
    tick_boxes(ax, g)
    tt = np.linspace(0, 30, 181)
    pts = [ax.P(t, lam ** t) for t in tt]
    o += F.polyline(pts, color=BLUE, w=4.4)
    g.line(pts, "curve")
    ye = ax.Y(1 / np.e)
    o += dashed((ax.x0, ye), (ax.X(tau), ye), color="muted", w=1.8)
    o += g.text(ax.x0 - 22, ye, "$1/e$", anchor="east", size=F.FONT_MATH, color="muted")
    p = ax.P(tau, lam ** tau)
    o += dashed((p[0], p[1] - 12), (p[0], ax.y0), color="hot", w=2.4)
    o += F.dot(*p, color=RED, d=22)
    g.dot(*p, r=11, tag="tau")
    o += g.text(p[0], ax.y0 - 66, "$\\tau = 9$", anchor="north", size=F.FONT_MATH, color="hot")
    o += g.text(ax.x1 + 40, ax.y0, "$t$", anchor="west", size=F.FONT_MATH)
    ax_, ay_ = ax.X(14), ax.Y(0.80)
    o += g.text(ax_, ay_, "the slowest term shrinks\\\\by a factor of e", anchor="west", size=F.FONT_HAND, hand=True, color="muted")
    o += arrow((ax_ - 10, ay_ - 8), (p[0] + 22, p[1] + 20), bend=18)
    g.check()
    F.emit("relax-curve", o, container="full", h=330, hmod="tight", nodes=False)


# --------------------------------------------------------------------------- tau-vs-mix
def f_tau_vs_mix():
    rows = G.tau_table()
    want = {"10-clique": (0.9, 1, 2), "karate club": (7.6, 10, 27), "two communities": (9.0, 7, 27),
            "two cliques + bridge": (13.8, 10, 41)}
    for n, tau, t1, t2 in rows:
        w0 = want[n]
        assert abs(tau - w0[0]) < 0.06 and (t1, t2) == w0[1:], (n, tau, t1, t2)
        assert t1 <= t2, n
    g = Gate("tau-vs-mix")
    cols = [470.0, 725.0, 950.0]
    top, pitch = 222.0, 42.0
    o = ""
    heads = [("relaxation time", "$\\tau$"), ("mixing time", "$\\epsilon = 1/2$"), ("mixing time", "$\\epsilon = 0.05$")]
    for c, (h1, h2) in zip(cols, heads):
        col = "hot" if c == cols[-1] else "ink"
        o += g.text(c, top + 52, h1, anchor="south", color=col)
        o += g.text(c, top + 2, h2, anchor="south", size=F.FONT_MATH, color=col)
    yrule = top - 12
    o += F.seg((30, yrule), (1050, yrule), color="ink", w=2.4, sketch=False)
    SZ = F.FONT + 4
    for i, (n, tau, t1, t2) in enumerate(rows):
        y = yrule - 38 - i * pitch
        o += g.text(30, y, n, anchor="west", size=F.FONT)
        o += g.text(cols[0], y, f"{tau:.1f}", size=SZ)
        o += g.text(cols[1], y, f"{t1}", size=SZ)
        o += g.text(cols[2], y, f"{t2}", size=SZ, color="hot")
    yb = yrule - 38 - (len(rows) - 1) * pitch - 28
    o += F.seg((30, yb), (1050, yb), color="muted", w=1.6, sketch=False)
    g.check()
    F.emit("tau-vs-mix", o, container="full", h=340, hmod="tight", nodes=False)


# --------------------------------------------------------------------------- gap-gauge
def f_gap_gauge():
    rows = G.spectral_gap_table()
    names = {"10-clique": "10-clique", "karate club": "karate club", "two communities": "two\\\\communities",
             "two 5-cliques + bridge": "two cliques\\\\+ bridge", "ring of 1,000": "ring of\\\\1,000"}
    taus = {"10-clique": "0.9", "karate club": "7.6", "two communities": "9", "two 5-cliques + bridge": "14",
            "ring of 1,000": "51,000"}
    for n, l, t in rows:
        want = {"10-clique": 0.9, "karate club": 7.6, "two communities": 9.0, "two 5-cliques + bridge": 14, "ring of 1,000": 50660}[n]
        assert abs(t - want) / want < 0.04, (n, t)
    gaps = {n: 1 - l for n, l, _t in rows}
    assert abs(gaps["10-clique"] - 1.11) < 0.01 and abs(gaps["karate club"] - 0.132) < 0.001
    assert abs(gaps["two communities"] - 0.111) < 0.001 and abs(gaps["two 5-cliques + bridge"] - 0.073) < 0.001
    assert abs(gaps["ring of 1,000"] - 2e-5) < 1e-6
    # a LOG axis of the gap 1 - lambda_2, large on the left; the ring (2e-5) is off the right end, past a break
    GX0, GX1, GY = 130.0, 930.0, 118.0
    hi, lo = 2.0, 0.07
    X = lambda v: GX0 + (np.log10(hi) - np.log10(v)) / (np.log10(hi) - np.log10(lo)) * (GX1 - GX0)
    g = Gate("gap-gauge")
    o = F.seg((GX0, GY), (GX1, GY), color="ink", w=3.0, sketch=False)
    for v, s_ in ((1, "1"), (0.1, "0.1")):
        o += F.seg((X(v), GY - 10), (X(v), GY + 10), color="ink", w=2.2, sketch=False)
        o += g.text(X(v), GY - 22, s_, anchor="north")
    o += g.text(GX0 - 24, GY, "gap\\\\$1-\\lambda_2$", anchor="east", size=F.FONT_MATH)
    # the break: two short slashes, then the ring's marker
    for dx in (0, 14):
        o += F.seg((GX1 + 24 + dx, GY - 14), (GX1 + 34 + dx, GY + 14), color="ink", w=2.4, sketch=False)
    RX = GX1 + 74
    xs = {n: (X(gaps[n]) if n != "ring of 1,000" else RX) for n, _l, _t in rows}
    xs_sorted = sorted(xs.values())
    assert min(b - a for a, b in zip(xs_sorted[:-1], xs_sorted[1:-1])) >= 40, xs      # on-scale markers at least 40 px apart
    assert RX - xs_sorted[-2] >= 40
    cx = [135.0, 325.0, 535.0, 765.0, 985.0]
    ly = 240.0
    for (n, l, t), c in zip(rows, cx):
        m = (xs[n], GY)
        o += F.seg((c, ly - 66), (m[0], m[1] + 12), color="muted", w=1.6, sketch=False)
        o += F.dot(m[0], m[1], color=BLUE if n != "ring of 1,000" else RED, d=20)
        o += g.text(c, ly, names[n], anchor="south", color="ink")
        o += g.text(c, ly - 8, f"$\\tau = {taus[n]}$", anchor="north", size=F.FONT_MATH)
    g.check()
    F.emit("gap-gauge", o, container="full", h=330, hmod="tight", nodes=False)


# --------------------------------------------------------------------------- eigvec2
def f_eigvec2():
    w, R, L = G.eigsystem(G.A12)
    r2 = R[:, 1] / np.abs(R[:, 1]).max()
    if r2[0] < 0:
        r2 = -r2
    assert np.all(r2[:6] > 0.5) and np.all(r2[6:] < -0.5)
    ax = F.Axes((96, 112, 690, 364), (-0.6, 11.6), (-1.25, 1.25), xticks=list(range(12)), yticks=[-1, 0, 1],
                yfmt=lambda v: f"{v:g}")
    g = Gate("eigvec2")
    o = frame(ax)
    tick_boxes(ax, g)
    o += dashed((ax.x0, ax.Y(0)), (ax.x1, ax.Y(0)), color="ink", w=2.0)
    for n in range(12):
        col = BLUE if n < 6 else RED
        p = ax.P(n, r2[n])
        o += F.dot(*p, color=col, d=26)
        g.dot(*p, r=13, tag=f"n{n}")
        if n in (2, 5, 8, 11):
            assert abs(abs(r2[n]) - 0.74) < 0.01
            o += F.ring(*p, size=26, grow=14, color="ink", w=2.2)
    o += g.text(ax.x0 + 6, ax.y1 + 34, "second eigenvector", anchor="west", color="muted")
    o += g.text(ax.x1, ax.y0 - 92, "node", anchor="east", color="muted")
    ax_, ay_ = ax.X(6.3), ax.Y(0.80)
    o += g.text(ax_, ay_, "the sign gives\\\\the community", anchor="west", size=F.FONT_HAND, hand=True, color="muted")
    g.check()
    F.emit("eigvec2", o, container="wide", h=470, hmod="w", nodes=False)


# --------------------------------------------------------------------------- comm-curve
def f_comm_curve():
    ts = [0, 1, 2, 3, 5, 10, 20, 40]
    want = [1, 1, 0.92, 0.88, 0.80, 0.67, 0.55, 0.505]
    got = [np.linalg.matrix_power(G.P12, t)[0, :6].sum() for t in ts]
    assert np.allclose(got, want, atol=0.006)
    theory = lambda t: 0.5 + 0.5 * G.LAM12[1] ** t
    assert all(abs(g_ - theory(t)) < 0.06 for g_, t in zip(got, ts) if t >= 3)
    ax = F.Axes((120, 62, 920, 232), (0, 40), (0.5, 1.0), xticks=[0, 10, 20, 30, 40], yticks=[0.5, 0.75, 1],
                yfmt=lambda v: f"{v:g}")
    g = Gate("comm-curve")
    o = frame(ax)
    tick_boxes(ax, g)
    o += dashed((ax.x0, ax.Y(0.5)), (ax.x1, ax.Y(0.5)), color="muted", w=1.6)
    tt = np.linspace(0, 40, 161)
    th = [ax.P(t, theory(t)) for t in tt]
    o += F.polyline(th, color=RED, w=3.0, dash=F.DASH)
    g.line(th, "theory")
    full = [ax.P(t, np.linalg.matrix_power(G.P12, int(t))[0, :6].sum()) for t in range(0, 41)]
    o += F.polyline(full, color=BLUE, w=3.6)
    g.line(full, "walk")
    for t, v in zip(ts, got):
        o += F.dot(*ax.P(t, v), color=BLUE, d=16)
        g.dot(*ax.P(t, v), r=9, tag="walk")
    o += g.text(ax.x0 + 6, ax.y1 + 30, "probability of being in community 1", anchor="west", color="muted")
    o += g.text(ax.x1 + 34, ax.y0, "steps", anchor="west", color="muted")
    cx, cy = ax.X(12), ax.Y(0.90)
    o += g.text(cx, cy, "the other eleven\\\\circles are gone", anchor="west", size=F.FONT_HAND, hand=True, color="muted")
    o += arrow((cx - 8, cy), (ax.X(3.4) + 12, ax.Y(0.88) + 4), bend=10)
    fx, fy = ax.X(28), ax.Y(0.72)
    o += g.text(fx, fy, "$0.5 + 0.5 \\times 0.889^{t}$", anchor="west", size=F.FONT_MATH, color="hot")
    o += arrow((fx + 90, fy - 26), (ax.X(33), ax.Y(theory(33)) + 8), color="hot")
    g.check()
    F.emit("comm-curve", o, container="full", h=300, hmod="tight", nodes=False)


FIGURES = [("degree-share", f_degree_share), ("lam-curves-q", f_lam_q), ("lam-curves-a", f_lam_a),
           ("mix", f_mix), ("relax-curve", f_relax_curve), ("tau-vs-mix", f_tau_vs_mix), ("gap-gauge", f_gap_gauge),
           ("eigvec2", f_eigvec2), ("comm-curve", f_comm_curve)]

if __name__ == "__main__":
    F.run(FIGURES)
