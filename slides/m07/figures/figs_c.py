#!/usr/bin/env python3
"""Module 07, worker C: the plots.

    degree-share      scatter, degree against the share of visits (karate club, 20,000 steps)
    lam-curves-q/-a   |lambda_k|^t against t for the twelve eigenvalues; the answer marks lambda_2
    mix-1/2/3         distance to pi against t (one curve per start, the worst start in black), then epsilon, then t_mix
    gap-gauge         lambda_2 on a gauge with the relaxation time of five networks
    diamond-expansion x(t) on the 4-node diamond at t = 0, 1, 2, 5, 10 and its eigen-expansion
    eigvec2           the second eigenvector of P, one dot per node
    comm-curve        probability of being in community 1 against the steps

Every number comes from smallgraphs.py or is computed here and asserted. `summary` is built last by the lead.
"""

import numpy as np

import figlib as F
import smallgraphs as G

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
            gate.box(ax.yfmt(v), text_box(ax.x0 - 17, ax.Y(v), ax.yfmt(v), "east", ax.size))


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


def _mix_axes():
    return F.Axes((110, 125, 1010, 300), (0, MT), (0, 2), xticks=[0, 10, 20, 30], yticks=[0, 1, 2],
                  yfmt=lambda v: f"{v:g}")


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
        o += F.polyline(pts, color="muted!70", w=2.4)
        g.line(pts, "start")
    pts = [ax.P(t, d) for t, d in zip(TS, WORST)]
    o += F.polyline(pts, color="ink", w=5.0)
    g.line(pts, "worst")
    o += g.text(ax.x0 + 8, ax.y1 + 36, "distance to $\\pi$", anchor="west", size=F.FONT_MATH)
    o += g.text(ax.x1 + 36, ax.y0, "$t$", anchor="west", size=F.FONT_MATH)
    return ax, o


def _mix_notes(ax, g):
    o = ""
    # where you start matters at first
    tx, ty = ax.X(17), ax.Y(1.8)
    o += g.text(tx, ty, "where you start\\\\matters at first", anchor="west", size=F.FONT_HAND, hand=True, color="muted")
    o += arrow((tx - 10, ty - 14), (ax.X(2.5), ax.Y(1.27)))
    # lambda_2 dominates the tail
    lx, ly = ax.X(12), ax.Y(1.0)
    o += g.text(lx, ly, "$\\lambda_2$ dominates", anchor="west", size=F.FONT_MATH, color="muted")
    o += arrow((lx + 100, ly - 30), (lx + 100, ax.Y(WORST[15]) + 14))
    return o


def _mix_eps(ax, g):
    y = ax.Y(G.EPS)
    o = dashed((ax.x0, y), (ax.x1, y), color="ink", w=2.0)
    o += g.text(ax.X(MT), y + 52, "how close is\\\\close enough?", anchor="east", size=F.FONT_HAND, hand=True, color="muted")
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
    GX0, GX1, GY = 130.0, 960.0, 118.0
    lo, hi = -0.2, 1.0
    X = lambda v: GX0 + (v - lo) / (hi - lo) * (GX1 - GX0)
    g = Gate("gap-gauge")
    o = ""
    # track, with the shaded zone past 0.99
    o += F.seg((GX0, GY), (GX1, GY), color="ink", w=3.0, sketch=False)
    o += f"\\fill[hot!35] ({X(0.99):.1f},{GY - 9:.1f}) rectangle ({GX1:.1f},{GY + 9:.1f});\n"
    for v, s in ((-0.2, "−0.2"), (0, "0"), (0.5, "0.5"), (1.0, "1")):
        o += F.seg((X(v), GY - 10), (X(v), GY + 10), color="ink", w=2.2, sketch=False)
        o += g.text(X(v), GY - 22, s, anchor="north")
    o += g.text(GX0 - 84, GY, "$\\lambda_2$", anchor="east", size=F.FONT_MATH)
    # five labels in a row, joined to their marker by a thin line that never crosses another
    cx = [130.0, 330.0, 540.0, 780.0, 975.0]
    ly = 240.0
    for (n, l, t), c in zip(rows, cx):
        m = (X(min(l, 0.9999)), GY)
        o += F.seg((c, ly - 66), (m[0], m[1] + 12), color="muted", w=1.6, sketch=False)
        o += F.dot(m[0], m[1], color=BLUE if n != "ring of 1,000" else RED, d=20)
        o += g.text(c, ly, names[n], anchor="south", color="ink")
        o += g.text(c, ly - 8, f"$\\tau = {taus[n]}$", anchor="north", size=F.FONT_MATH)
    # the ring is past the right end: an arrow says so
    g.check()
    F.emit("gap-gauge", o, container="full", h=330, hmod="tight", nodes=False)


# --------------------------------------------------------------------------- diamond-expansion
def f_diamond_expansion():
    XY = G.DIAMOND_XY
    panel_w = 216.0
    ts = [0, 1, 2, 5, 10]
    X0 = np.array([1.0, 0, 0, 0])
    assert np.allclose(X0, G.X0D)
    xt = lambda t: G.PSI[0] - 0.5 * G.LAM_PSI[1] ** t * G.PSI[1] + 0.3 * G.LAM_PSI[3] ** t * G.PSI[3]
    for t in ts:                          # the expansion is the walk
        assert np.allclose(xt(t) if t else xt(0), X0 @ np.linalg.matrix_power(G.PD, t)), t
    assert np.allclose(xt(2), [1 / 3, 1 / 3, 1 / 6, 1 / 6])
    g = Gate("diamond-expansion")
    o = ""
    sx, sy = 50.0, 36.0
    cy0 = 230.0
    for i, t in enumerate(ts):
        cx = panel_w * (i + 0.5)
        x = X0 @ np.linalg.matrix_power(G.PD, t)
        pos = {n: (cx + (XY[n][0] - 1.5) * sx, cy0 + (XY[n][1] - 1.6) * sy) for n in range(4)}
        for a, b in G.DIAMOND.edges():
            o += F.seg(pos[a], pos[b], color="muted", w=2.4)
        for n in range(4):
            v = float(x[n])
            lab = "1" if abs(v - 1) < 1e-9 else ("0" if abs(v) < 1e-9 else (f"{v:.2f}".rstrip("0") if abs(v * 10 - round(v * 10)) < 1e-9 else f"{v:.2f}").lstrip("0"))
            o += F.disc(pos[n][0], pos[n][1], lab, fill=F.shade(min(1.0, v * 1.8)), size=52)
        o += g.text(cx, cy0 - 94, f"$t = {t}$", size=F.FONT_MATH, color="muted")
    # the expansion
    o += g.text(540, 76, "$x(t) = \\pi - 0.5\\cdot 0^{t}\\,\\psi_2 + 0.3\\,(-\\tfrac{2}{3})^{t}\\,\\psi_4$", size=F.FONT_MATH)
    o += g.text(540, 30, "$t = 2:\\quad x(2) = (\\tfrac13,\\,\\tfrac13,\\,\\tfrac16,\\,\\tfrac16)$", size=F.FONT_MATH, color="hot")
    g.check()
    F.emit("diamond-expansion", o, container="full", h=330, hmod="", nodes=True)


# --------------------------------------------------------------------------- eigvec2
def f_eigvec2():
    w, R, L = G.eigsystem(G.A12)
    r2 = R[:, 1] / np.abs(R[:, 1]).max()
    if r2[0] < 0:
        r2 = -r2
    assert np.all(r2[:6] > 0.5) and np.all(r2[6:] < -0.5)
    ax = F.Axes((100, 78, 985, 330), (-0.6, 11.6), (-1.25, 1.25), xticks=list(range(12)), yticks=[-1, 0, 1],
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
    o += g.text(ax.x1 + 14, ax.y0, "node", anchor="west", color="muted")
    ax_, ay_ = ax.X(7.0), ax.Y(0.80)
    o += g.text(ax_, ay_, "the sign gives\\\\the community", anchor="west", size=F.FONT_HAND, hand=True, color="muted")
    o += arrow((ax_ + 150, ay_ - 52), (ax_ + 150, ax.Y(0) + 12))
    g.check()
    F.emit("eigvec2", o, container="full", h=400, hmod="tall", nodes=False)


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
           ("mix", f_mix), ("gap-gauge", f_gap_gauge), ("diamond-expansion", f_diamond_expansion),
           ("eigvec2", f_eigvec2), ("comm-curve", f_comm_curve)]

if __name__ == "__main__":
    F.run(FIGURES)
