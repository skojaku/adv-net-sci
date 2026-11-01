#!/usr/bin/env python3
"""Worker B: the matrix pictures of the M07 deck, all on the 12-node two-communities network.

    P-def                  the network and P as a heat map (rows "from", columns "to")
    xP-1 .. xP-3           a wide bar x times P = a wide bar; three cases, one canvas
    xPt                    x(0) times P, P, ..., P = x(t)
    Pt-slider              frames t = 1..40 of the heat map of P^t (stepped by the scrubber)
    Pt-40                  P^40 as a table of numbers on coloured cells
    Pt-zoom                a 3 x 3 patch of P^5 enlarged
    P-decomp               P = sum of lambda_k phi_k psi_k^T (terms 1, 2, 12)
    Pt-circles-1 .. -3     the same canvas, circle areas = |lambda_k|^t for t = 1, 5, 40
    P1-eq-1                P times a column of ones = the same column

Every number is computed from smallgraphs.py. Notation as in M06 (figs_decomp.py): circle = eigenvalue
(area proportional to |value|), column (tall bar) = right eigenvector, row (wide bar) = left eigenvector, square = matrix.

Colour of every heat map (round 2): low values blue, high values red, through a pale yellow; see GRAD / fill_of.
"""

import sys

import numpy as np

import figlib as F
from smallgraphs import (A12, COMM12, LAM12, P12, PI12, TWO12, TWO12_XY, eigsystem, check)

# figlib caps a figure's height by its `hmod`; the deck's L-b layout allows 480 px (420 under a take line)
F.FIG_H["l"] = 480
F.FIG_H["lt"] = 420

check()
N = 12
VMAX = 0.3                                   # the one colour scale of every heat map: 0 blue ... 0.3 and above red
GAMMA = 0.5                                  # square-root stretch: .07 (t = 40) stays clearly apart from 0 and from .25
# blue (0) - light blue - pale yellow - orange - red (max); the lecturer, 2026-10-31: "small = blue, large = red"
GRAD = [(0.0, (57, 89, 166)), (0.22, (140, 170, 225)), (0.42, (238, 240, 235)), (0.58, (250, 226, 140)), (0.78, (232, 148, 88)), (1.0, (177, 68, 52))]
BLUE, GOLD, PALEFILL = "cool!70", "hot!85", "pale"


# --------------------------------------------------------------------------- the numbers the figures state
def Pt(t):
    return np.linalg.matrix_power(P12, t)


assert np.allclose(Pt(40), np.tile(PI12, (N, 1)), atol=0.01), "P^40 has the same row everywhere"
assert round(LAM12[1] ** 5, 2) == 0.56 and round(LAM12[1] ** 10, 2) == 0.31 and round(LAM12[1] ** 40, 2) == 0.01  # the brief said 0.55 for t = 5; the value is 0.555
assert np.allclose(P12.sum(axis=1), 1) and np.allclose(P12 @ np.ones(N), np.ones(N))


# --------------------------------------------------------------------------- small helpers
def num(v):
    """Two decimals, leading zero dropped: .07"""
    s = "%.2f" % v
    return s[1:] if s.startswith("0.") else s


def rgb_of(v, vmax=VMAX):
    u = min(max(v / vmax, 0.0), 1.0) ** GAMMA
    for (a, ca), (b, cb) in zip(GRAD, GRAD[1:]):
        if u <= b:
            f = (u - a) / (b - a)
            return tuple(int(round(ca[k] + f * (cb[k] - ca[k]))) for k in range(3))
    return GRAD[-1][1]


def fill_of(v, vmax=VMAX):
    r, g, b = rgb_of(v, vmax)
    return "fill={rgb,255:red,%d;green,%d;blue,%d}" % (r, g, b)


def ink_on(v, vmax=VMAX):
    """a number written on the cell: white on the dark blue and the dark red, ink on the light middle"""
    r, g, b = rgb_of(v, vmax)
    return "white" if 0.2126 * r + 0.7152 * g + 0.0722 * b < 125 else "ink"


def key(x0, ytop, hgt, ticks=(0, 0.15, 0.3), w=18):
    """a vertical colour key: 0 at the bottom (blue), VMAX at the top (red); the ticks read right of the strip"""
    n = 48
    o = ""
    for i in range(n):
        v = (i + .5) / n * VMAX
        y0 = ytop - hgt + i * hgt / n
        o += f"\\fill[{fill_of(v)}] ({x0:.1f},{y0:.1f}) rectangle ({x0 + w:.1f},{y0 + hgt / n + .4:.1f});\n"
    o += rect(x0, ytop - hgt, x0 + w, ytop, w=1.8)
    for tv in ticks:
        y = ytop - hgt + tv / VMAX * hgt
        o += F.text(x0 + w + 8, y, (("0" if tv == 0 else ("%g" % tv).lstrip("0")) + ("+" if tv == VMAX else "")), anchor="west", size=F.FONT)
    return o


def rect(x0, y0, x1, y1, fill=None, color="ink", w=1.6):
    return F._seed(x0, y0, x1, y1) + (f"\\fill[{fill}] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});\n" if fill else "") + \
        (f"\\draw[{color},line width={w}bp,pencil] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});\n" if color else "")


def heat(x0, ytop, M, c, vmax=VMAX, numbers=False, split=True, outline="ink"):
    """An n x n matrix of cells c bp wide; the fill is blue (0) to red (vmax). A dashed line marks the
    boundary of the two communities (after node 5)."""
    n = len(M)
    o = ""
    for i in range(n):
        for j in range(n):
            xl, yt = x0 + j * c, ytop - i * c
            o += f"\\fill[{fill_of(M[i][j], vmax)}] ({xl:.1f},{yt - c:.1f}) rectangle ({xl + c:.1f},{yt:.1f});\n"
    for k in range(1, n):                       # thin white separators between cells
        o += f"\\draw[white,line width=0.6bp] ({x0 + k * c:.1f},{ytop - n * c:.1f}) -- ({x0 + k * c:.1f},{ytop:.1f});\n"
        o += f"\\draw[white,line width=0.6bp] ({x0:.1f},{ytop - k * c:.1f}) -- ({x0 + n * c:.1f},{ytop - k * c:.1f});\n"
    if numbers:
        for i in range(n):
            for j in range(n):
                o += F.text(x0 + (j + .5) * c, ytop - (i + .5) * c, num(M[i][j]), size=F.FONT, color=ink_on(M[i][j]))
    if split:
        h = 6
        o += f"\\draw[muted,line width=1.6bp,dash pattern=on 6bp off 5bp] ({x0 + h * c:.1f},{ytop - n * c:.1f}) -- ({x0 + h * c:.1f},{ytop:.1f});\n"
        o += f"\\draw[muted,line width=1.6bp,dash pattern=on 6bp off 5bp] ({x0:.1f},{ytop - h * c:.1f}) -- ({x0 + n * c:.1f},{ytop - h * c:.1f});\n"
    o += rect(x0, ytop - n * c, x0 + n * c, ytop, color=outline, w=2.0)
    return o


def wide(x0, yc, vec, c, vmax=VMAX, split=True):
    """A wide bar (a row vector): len(vec) cells of width c, centred on height yc."""
    n = len(vec)
    o = ""
    for j, v in enumerate(vec):
        o += f"\\fill[{fill_of(v, vmax)}] ({x0 + j * c:.1f},{yc - c / 2:.1f}) rectangle ({x0 + (j + 1) * c:.1f},{yc + c / 2:.1f});\n"
    for k in range(1, n):
        o += f"\\draw[white,line width=0.6bp] ({x0 + k * c:.1f},{yc - c / 2:.1f}) -- ({x0 + k * c:.1f},{yc + c / 2:.1f});\n"
    if split:
        o += f"\\draw[muted,line width=1.6bp,dash pattern=on 6bp off 5bp] ({x0 + 6 * c:.1f},{yc - c / 2:.1f}) -- ({x0 + 6 * c:.1f},{yc + c / 2:.1f});\n"
    o += rect(x0, yc - c / 2, x0 + n * c, yc + c / 2, w=2.0)
    return o


def tall(x0, ytop, vec, c, vmax=1.0, numbers=None, fill_mode="blue"):
    n = len(vec)
    o = ""
    for i, v in enumerate(vec):
        o += f"\\fill[{fill_of(v, vmax)}] ({x0:.1f},{ytop - (i + 1) * c:.1f}) rectangle ({x0 + c:.1f},{ytop - i * c:.1f});\n"
    for k in range(1, n):
        o += f"\\draw[white,line width=0.6bp] ({x0:.1f},{ytop - k * c:.1f}) -- ({x0 + c:.1f},{ytop - k * c:.1f});\n"
    if numbers:
        for i in range(n):
            o += F.text(x0 + c / 2, ytop - (i + .5) * c, numbers, size=F.FONT, color=ink_on(vec[i], vmax))
    o += rect(x0, ytop - n * c, x0 + c, ytop, w=2.0)
    return o


def net(ox, oy, w, vals=None, vmax=1.0, size=F.NODE, label=True, ring_nodes=(), edge_w=2.0):
    """The 12-node network inside a box of width w whose lower-left corner of the ink is (ox, oy).
    Fill: community colours, or `vals` (0..vmax) as a shade of blue. Returns (tikz, {node: (x, y)})."""
    xs = [p[0] for p in TWO12_XY.values()]
    ys = [p[1] for p in TWO12_XY.values()]
    sc = w / (max(xs) - min(xs))
    pos = {n: (ox + (x - min(xs)) * sc, oy + (y - min(ys)) * sc) for n, (x, y) in TWO12_XY.items()}
    o = ""
    for a, b in TWO12.edges():
        o += F.seg(pos[a], pos[b], color="muted", w=edge_w)
    for n, (x, y) in pos.items():
        if vals is not None:
            f = F.shade(vals[n] / vmax)
        else:
            f = "cool!38!white" if COMM12[n] == 0 else "hot!38!white"
        show = label if not isinstance(label, (set, list, tuple)) else (n in label)
        o += F.disc(x, y, str(n) if show else "", fill=f, size=size)
    for n in ring_nodes:
        o += F.ring(*pos[n], size=size, color="hot", w=3.0, grow=10)
    return o, pos


def op(x, y, s):
    return F.text(x, y, s, size=F.FONT_MATH + 4)


def mtext(x, y, s, size=F.FONT_MATH, color="ink", anchor="center"):
    return F.text(x, y, s, size=size, color=color, anchor=anchor)


def hot_rows(x0, ytop, rows, n, c, w=3.0):
    """a black frame round the rows under discussion: red would vanish on the red cells of the new scale"""
    return "".join(rect(x0 - 1, ytop - (i + 1) * c, x0 + n * c + 1, ytop - i * c, color="ink", w=w) for i in rows)


# --------------------------------------------------------------------------- P-def
PD_C = 28                                          # cell side, bp
PD_X0, PD_YTOP = 600, 392


def f_Pdef():
    o = ""
    # network, left
    no, pos = net(34, 218, 460)
    o += no
    # the matrix, right
    o += heat(PD_X0, PD_YTOP, P12, PD_C)
    o += key(PD_X0 + N * PD_C + 32, PD_YTOP, N * PD_C)
    # "to" over the columns, "from" beside the rows, and the two blocks
    cxm = PD_X0 + N * PD_C / 2
    o += F.text(cxm, PD_YTOP + 56, "to", size=F.FONT)
    o += F.text(PD_X0 - 34, PD_YTOP - N * PD_C / 2, "from", size=F.FONT, rot=90)
    o += F.text(PD_X0 + 3 * PD_C, PD_YTOP + 22, "0-5", color="muted", size=F.FONT)
    o += F.text(PD_X0 + 9 * PD_C, PD_YTOP + 22, "6-11", color="muted", size=F.FONT)
    # one row highlighted, with its note
    r = 8
    o += hot_rows(PD_X0, PD_YTOP, [r], N, PD_C, w=3.4)
    yr = PD_YTOP - (r + .5) * PD_C
    c, _ = F.callout("row 8: the odds of leaving\\\\node 8. They sum to 1", (235, 122), (PD_X0 - 8, yr), anchor="center",
                     bend=-12, gap=8)
    o += c
    F.emit("P-def", o, container="full", h=470, hmod="l", nodes=True)


# --------------------------------------------------------------------------- xP-1..3
XC = 20                                            # cell side of the pictogram
XP_X = 100                                         # left of the x bar
XP_P = 420                                         # left of P
XP_R = 740                                         # left of the result
XP_YTOP = 290
XP_YC = XP_YTOP - N * XC / 2

X_CASES = {
    1: np.eye(N)[0],
    2: np.eye(N)[1],
    3: np.array([0.5, 0, 0, 0.3, 0, 0, 0, 0, 0.2, 0, 0, 0]),
}
for _x in X_CASES.values():
    assert abs(_x.sum() - 1) < 1e-12


def wnum(v):
    return "1" if v >= 1 else ("%.1f" % v)[1:]


def f_xP(case):
    x = X_CASES[case]
    y = x @ P12
    assert np.allclose(y, sum(x[i] * P12[i] for i in range(N)))
    nz = [i for i in range(N) if x[i] > 0]
    o = wide(XP_X, XP_YC, x, XC)
    o += op(XP_X + N * XC + 40, XP_YC, "$\\times$")
    o += heat(XP_P, XP_YTOP, P12, XC)
    o += hot_rows(XP_P, XP_YTOP, nz, N, XC, w=3.0)
    o += op(XP_P + N * XC + 40, XP_YC, "$=$")
    o += wide(XP_R, XP_YC, y, XC)
    o += mtext(XP_X + N * XC / 2, XP_YTOP + 34, "$x$")
    o += mtext(XP_P + N * XC / 2, XP_YTOP + 34, "$P$")
    o += mtext(XP_R + N * XC / 2, XP_YTOP + 34, "$xP$")
    for i in nz:     # the weight above each non-zero cell of x, the node number beside the row of P it picks
        o += rect(XP_X + i * XC, XP_YC - XC / 2, XP_X + (i + 1) * XC, XP_YC + XC / 2, color="ink", w=3.0)
        o += F.text(XP_X + (i + .5) * XC, XP_YC + XC / 2 + 24, wnum(x[i]), color="hot", size=F.FONT)
        o += F.text(XP_X + (i + .5) * XC, XP_YC - XC / 2 - 22, str(i), color="muted", size=F.FONT)
        o += F.text(XP_P - 14, XP_YTOP - (i + .5) * XC, str(i), color="hot", anchor="east", size=F.FONT)
    return o


def f_xP_all():
    F.emit_group([(f"xP-{k}", f_xP(k)) for k in (1, 2, 3)], container="full", h=380, hmod="tight", nodes=False,
                 box=None, prefix=False)


# --------------------------------------------------------------------------- xPt
def f_xPt():
    c = 12
    side = N * c
    x0 = np.eye(N)[0]
    t = 3
    xt = x0 @ Pt(t)
    ytop = 250
    yc = ytop - side / 2
    gap = 46
    xs = [26]
    o = ""
    o += wide(xs[0], yc, x0, c)
    xp = xs[0] + side
    ppos = []
    cur = xp
    for k in range(3):
        if k == 2:
            o += mtext(cur + gap / 2 + 8, yc, "$\\cdots$")
            cur += gap + 22
        o += op(cur + gap / 2, yc, "$\\times$")
        cur += gap
        ppos.append(cur)
        o += heat(cur, ytop, P12, c)
        cur += side
    o += op(cur + gap / 2 - 4, yc, "$=$")
    cur += gap - 8
    o += wide(cur, yc, xt, c)
    o += mtext(xs[0] + side / 2, ytop + 34, "$x(0)$")
    for p in ppos:
        o += mtext(p + side / 2, ytop + 34, "$P$")
    o += mtext(cur + side / 2, ytop + 34, "$x(t)$")
    # brace under the three squares: "t times"
    b0, b1, by = ppos[0], ppos[2] + side, ytop - side - 14
    o += (f"\\draw[hot,line width=2.6bp] ({b0:.1f},{by + 8:.1f}) -- ({b0:.1f},{by:.1f}) -- ({b1:.1f},{by:.1f}) -- ({b1:.1f},{by + 8:.1f});\n")
    o += mtext((b0 + b1) / 2, by - 34, "$t$ times", color="hot")
    F.emit("xPt", o, container="full", h=330, hmod="", nodes=False)


# --------------------------------------------------------------------------- Pt-slider
SL_C = 30
SL_X0, SL_YTOP = 150, 396
SL_NOTE = {1: "stays in its\\\\community", 5: "starting to leak", 40: "every row is\\\\the same"}


def slider_frame(t):
    o = heat(SL_X0, SL_YTOP, Pt(t), SL_C)
    o += F.text(SL_X0 + N * SL_C / 2, SL_YTOP + 44, "to", size=F.FONT)
    o += F.text(SL_X0 - 34, SL_YTOP - N * SL_C / 2, "from", size=F.FONT, rot=90)
    o += key(SL_X0 + N * SL_C + 30, SL_YTOP, N * SL_C)
    o += F.text(840, SL_YTOP - 120, "$t=%d$" % t, size=96)
    if t in SL_NOTE:
        o += F.text(840, SL_YTOP - 250, SL_NOTE[t], color="muted", size=F.FONT)
    return o


def f_slider():
    ts = [1, 40] if "--test" in sys.argv else range(1, 41)
    frames = [slider_frame(t) for t in ts]
    F.emit_frames("Pt-slider", frames, container="full", h=480, hmod="l", nodes=False, box=None)


# --------------------------------------------------------------------------- Pt-40
def f_Pt40():
    M = Pt(40)
    assert np.allclose(np.round(M, 2), np.round(np.tile(PI12, (N, 1)), 2)), "every row is pi to 2 decimals"
    c, rp = 58, 30
    x0, ytop = 186, 372
    o = ""
    for i in range(N):
        for j in range(N):
            xl, yt = x0 + j * c, ytop - i * rp
            o += f"\\fill[{fill_of(M[i][j])}] ({xl:.1f},{yt - rp:.1f}) rectangle ({xl + c:.1f},{yt:.1f});\n"
    for k in range(1, N):
        o += f"\\draw[white,line width=0.8bp] ({x0 + k * c:.1f},{ytop - N * rp:.1f}) -- ({x0 + k * c:.1f},{ytop:.1f});\n"
        o += f"\\draw[white,line width=0.8bp] ({x0:.1f},{ytop - k * rp:.1f}) -- ({x0 + N * c:.1f},{ytop - k * rp:.1f});\n"
    for i in range(N):
        for j in range(N):
            o += F.text(x0 + (j + .5) * c, ytop - (i + .5) * rp, num(M[i][j]), size=F.FONT, color=ink_on(M[i][j]))
        o += F.text(x0 - 12, ytop - (i + .5) * rp, "start %d" % i, color="muted", anchor="east", size=F.FONT)
    for j in range(N):
        o += F.text(x0 + (j + .5) * c, ytop + 22, str(j), color="muted", size=F.FONT)
    o += rect(x0, ytop - N * rp, x0 + N * c, ytop, w=2.0)
    # the bracket at the right: the same row in every row
    bx = x0 + N * c + 14
    o += (f"\\draw[hot,line width=3bp] ({bx:.1f},{ytop:.1f}) -- ({bx + 12:.1f},{ytop:.1f}) -- ({bx + 12:.1f},{ytop - N * rp:.1f}) -- ({bx:.1f},{ytop - N * rp:.1f});\n")
    o += mtext(bx + 48, ytop - N * rp / 2, "$\\pi$", size=62, color="hot")
    o += key(bx + 88, ytop, N * rp)
    F.emit("Pt-40", o, container="full", h=420, hmod="lt", nodes=False)


# --------------------------------------------------------------------------- Pt-zoom
def f_zoom():
    t, z, c = 5, 3, 22
    M = Pt(t)
    x0, ytop = 70, 440
    o = heat(x0, ytop, M, c)
    o += mtext(x0 + N * c / 2, ytop + 36, "$P^{5}$")
    bx1, by0 = x0 + z * c, ytop - z * c
    o += rect(x0, by0, bx1, ytop, color="ink", w=3.4)
    big = 90
    X0, YT = 500, 440
    for i in range(z):
        for j in range(z):
            xl, yt = X0 + j * big, YT - i * big
            o += f"\\fill[{fill_of(M[i][j])}] ({xl:.1f},{yt - big:.1f}) rectangle ({xl + big:.1f},{yt:.1f});\n"
            o += F.text(xl + big / 2, yt - big / 2, num(M[i][j]), size=F.FONT, color=ink_on(M[i][j]))
    for k in range(1, z):
        o += f"\\draw[white,line width=0.8bp] ({X0 + k * big:.1f},{YT - z * big:.1f}) -- ({X0 + k * big:.1f},{YT:.1f});\n"
        o += f"\\draw[white,line width=0.8bp] ({X0:.1f},{YT - k * big:.1f}) -- ({X0 + z * big:.1f},{YT - k * big:.1f});\n"
    o += rect(X0, YT - z * big, X0 + z * big, YT, color="ink", w=3.4)
    o += f"\\draw[hot,line width=1.8bp,dash pattern=on 7bp off 6bp] ({bx1:.1f},{ytop:.1f}) -- ({X0 - 4:.1f},{YT:.1f});\n"
    o += f"\\draw[hot,line width=1.8bp,dash pattern=on 7bp off 6bp] ({bx1:.1f},{by0:.1f}) -- ({X0 - 4:.1f},{YT - z * big:.1f});\n"
    ex, ey = X0 + 2.5 * big, YT - .5 * big
    o += F.sketch_circle(ex, ey, big * .9, color="ink", w=3.0)
    a, _ = F.aside("start at 0,\\\\at 2 after\\\\5 steps", (930, YT - 150), (ex + 42, ey - 22), anchor="center", bend=25, gap=8)
    o += a
    o += F.text(X0 + z * big / 2, YT - z * big - 36, "row: where it starts", color="muted", size=F.FONT)
    o += F.text(X0 + z * big / 2, YT - z * big - 76, "column: where it is", color="muted", size=F.FONT)
    F.emit("Pt-zoom", o, container="full", h=520, hmod="l", nodes=False)


# --------------------------------------------------------------------------- the decomposition row (P-decomp and Pt-circles)
SIDE = 100
TG = 10
BAR = 0.15
K = [0, 1, N - 1]                                   # the terms drawn: 1, 2 and 12
VFILL = {0: "cool!55", 1: "gold!70", N - 1: "pale"}
KLAB = {0: "1", 1: "2", N - 1: "12"}
ROW_H, ROW_YTOP = 340, 196
SLOT = {0: 100, 1: 100, N - 1: 110}
LHS_W, PLUS, DOTS = 118, 30, 126
ITEMS = [("lhs", LHS_W), ("t0", SLOT[0] + TG + SIDE), ("p1", PLUS), ("t1", SLOT[1] + TG + SIDE), ("dots", DOTS),
         ("t11", SLOT[N - 1] + TG + SIDE)]


def _layout():
    pos, x = {}, 0
    for k, w in ITEMS:
        pos[k] = x
        x += w + 8
    right = x - 8
    assert right <= F.FULL_W - 36, right
    sh = (F.FULL_W - right) / 2
    return {k: v + sh for k, v in pos.items()}


POS = _layout()
KEY = {0: "t0", 1: "t1", N - 1: "t11"}
YMID = ROW_YTOP - SIDE / 2
D1 = 96.0
BOX = (ROW_H - 300, ROW_H - 30)


def dcircle(cx, cy, d, color):
    if d < 0.4:
        return ""
    o = f"\\fill[{color}] ({cx:.1f},{cy:.1f}) circle ({d / 2:.2f}bp);\n"
    o += F.sketch_circle(cx, cy, d, color="ink", w=1.5) if d >= 14 else \
        f"\\draw[ink,line width=1.2bp] ({cx:.1f},{cy:.1f}) circle ({d / 2:.2f}bp);\n"
    return o


def dmatrix(mx, ytop, side, k):
    bt = BAR * side
    o = rect(mx, ytop - side, mx + side, ytop, color="muted", w=1.6)
    o += rect(mx, ytop - side, mx + bt, ytop, VFILL[k], "ink", 1.6)                 # tall bar: phi_k
    o += rect(mx + 1.55 * bt, ytop - bt, mx + side, ytop, VFILL[k], "ink", 1.6)     # wide bar: psi_k^T
    return o


def dterm(k, d, color, lam_s, top=None):
    x = POS[KEY[k]]
    cx, cy = x + SLOT[k] / 2, YMID
    mx = x + SLOT[k] + TG
    ylab = ROW_YTOP - SIDE - 34
    o = dcircle(cx, cy, d, color)
    o += dmatrix(mx, ROW_YTOP, SIDE, k)
    o += mtext(mx - 14, ylab, lam_s, anchor="east")
    o += mtext(mx + SIDE / 2, ylab, "$\\phi_{%s}\\psi_{%s}^{\\top}$" % (KLAB[k], KLAB[k]))
    if top:
        o += top(cx, ROW_YTOP + 30)
    return o


def sgn(v):
    return BLUE if v >= 0 else GOLD


def sval(v):
    r = round(v, 2)
    t = "%.2f" % v
    return t.replace("-", "−")


def decomp_row(lhs, vals, diam, top=True):
    """vals: the three numbers printed under the terms; diam: circle diameters."""
    o = mtext(POS["lhs"] + LHS_W, YMID, lhs, anchor="east")
    for k, v, d, lam in zip(K, vals, diam, [LAM12[i] for i in K]):
        o += dterm(k, d, sgn(lam), sval(v), top=(lambda cx, y, k=k: mtext(cx, y, "$\\lambda_{%s}$" % KLAB[k])) if top else None)
    o += mtext(POS["p1"] + PLUS / 2, YMID, "$+$")
    o += mtext(POS["dots"] + DOTS / 2, YMID, "$+\\;\\cdots\\;+$")
    return o


D0 = D1 / LAM12[0]


def f_decomp():
    o = decomp_row("$P=$", [LAM12[i] for i in K], [D0 * abs(LAM12[i]) for i in K])
    a, _ = F.aside("column and row are\\\\different vectors for P", (POS["t1"] + 120, ROW_YTOP + 98), (POS["t1"] + SLOT[1] + TG + 60, ROW_YTOP - 8),
                   anchor="center", bend=25, gap=8)
    o += a
    F.emit("P-decomp", o, container="full", h=ROW_H, hmod="tight", nodes=False, box=None)


CIRC_T = {1: "one step", 5: "$\\lambda_2^{5}=0.56$", 40: "only the circle at 1 is left"}


def circ_frame(t):
    pw = [abs(LAM12[i]) ** t for i in K]                     # area proportional to |lambda|^t
    o = decomp_row("$P^{%d}=$" % t, [LAM12[i] ** t for i in K], [D1 * np.sqrt(p) for p in pw], top=False)
    # the one note of the step, straight above the circle it is about
    s = CIRC_T[t]
    k, cx = (1, POS["t1"] + SLOT[1] / 2) if "$" in s else (0, POS["t0"] + SLOT[0] / 2)
    r = D1 * np.sqrt(pw[k]) / 2
    if "$" in s:
        c, _ = F.callout(s, (cx, ROW_YTOP + 70), (cx, YMID + r), anchor="center", size=F.FONT_MATH, gap=8)
    else:
        c, _ = F.callout(s, (cx + 30, ROW_YTOP + 70), (cx, YMID + r), anchor="center", gap=8)
    return o + c


def f_circles():
    F.emit_group([(f"Pt-circles-{k}", circ_frame(t)) for k, t in enumerate((1, 5, 40), 1)], container="full", h=ROW_H,
                 hmod="tight", nodes=False, box=None, prefix=False)


# --------------------------------------------------------------------------- P1-eq-1
def f_P1():
    c = 28
    x0, ytop = 92, 388
    o = heat(x0, ytop, P12, c)
    ones = np.ones(N)
    bx1 = x0 + N * c + 86
    o += op(x0 + N * c + 40, ytop - N * c / 2, "$\\times$")
    o += tall(bx1, ytop, ones, c, vmax=1.0, numbers="1")
    o += op(bx1 + c + 40, ytop - N * c / 2, "$=$")
    bx2 = bx1 + c + 80
    o += tall(bx2, ytop, ones, c, vmax=1.0, numbers="1")
    o += mtext(x0 + N * c / 2, ytop + 36, "$P$")
    o += mtext(bx1 + c / 2, ytop + 36, "$\\mathbf{1}$")
    o += mtext(bx2 + c / 2, ytop + 36, "$\\mathbf{1}$")
    r = 3
    o += hot_rows(x0, ytop, [r], N, c, w=3.4)
    o += rect(bx2 - 1, ytop - (r + 1) * c, bx2 + c + 1, ytop - r * c, color="ink", w=3.4)
    yr = ytop - (r + .5) * c
    o += f"\\draw[hot,line width=1.8bp,dash pattern=on 7bp off 6bp] ({x0 + N * c + 2:.1f},{yr:.1f}) -- ({bx2 - 4:.1f},{yr:.1f});\n"
    cc, _ = F.callout("this row sums to 1", (x0 + 120, ytop - N * c - 30), (x0 + 40, ytop - (r + 1) * c - 4), anchor="center", bend=0, gap=6) if False else ("", None)
    # the big equation and its comment, at the right
    ex = 830
    o += mtext(ex, ytop - 50, "$P\\,\\mathbf{x}=\\mathbf{x}$", size=62)
    a, _ = F.aside("a vector that P\\\\does not change", (ex, ytop - 170), (ex, ytop - 92), anchor="center", bend=0, gap=6)
    o += a
    o += mtext(ex, ytop - 270, "$P\\,\\mathbf{1}=\\mathbf{1}$", size=62, color="hot")
    F.emit("P1-eq-1", o, container="full", h=480, hmod="l", nodes=False)


FIGURES = [("P-def", f_Pdef), ("xP", f_xP_all), ("xPt", f_xPt), ("Pt-slider", f_slider), ("Pt-40", f_Pt40),
           ("Pt-zoom", f_zoom), ("P-decomp", f_decomp), ("Pt-circles", f_circles), ("P1-eq-1", f_P1)]

if __name__ == "__main__":
    F.run(FIGURES)
