#!/usr/bin/env python3
"""The decomposition figures: A = sum of lambda_k u_k u_k^T, drawn in the lecturer's notation.

    decomp-sum      frames: A = lambda_1 u_1 u_1^T + lambda_2 ... + ... + lambda_7 ..., one term per frame
    decomp-orth     u_k^T u_l = 0 for k != l, 1 for k = l (wide rectangle times tall rectangle)
    decomp-square   frames: A^2 as a product of two sums: cross terms die, circles become lambda_k^2
    decomp-power    frames: A^t: circle k scaled by (lambda_k / lambda_1)^t, t = 1, 2, 3, 4, 8, 16
    katz-why        frames: (I - alpha A)^-1: coefficient 1 / (1 - alpha lambda_k) per term

Notation, from lecture-note/figs/spectral-decomposition.jpg: an eigenvalue is a filled
circle (diameter proportional to |value|), an eigenvector u_k is a TALL rectangle, its
transpose a WIDE rectangle, and the pair together stands for the square matrix u_k u_k^T.
Palette: a circle is cool if the value is positive and hot if it is negative; the bars are
neutral (a pale fill, pencil ink outline: only the circles carry sign); words and numbers are Meslo, math is Latin Modern at
FONT_MATH.  Every number is computed from the spectrum of the 7-node graph EIG; none is typed.

The builds are frames (F.emit_frames), one small step each.  Frames of the sum start with
the outlines of all four terms in muted pencil, so every frame spans the canvas and the
picture does not shift when a term is filled in.

The filled circles are drawn in cool!70 / hot!85, not in the node colours: they are values,
not network nodes, and the render gate measures every node-colour disc against the 26-52 px band.
"""

import numpy as np

import figlib as F
from smallgraphs import EIG, EIG_ORDER, spectrum

# --------------------------------------------------------------------------- the numbers
A, _w, _V = spectrum(EIG, EIG_ORDER)
LAM = _w[::-1].copy()                 # descending: lambda_1 > ... > lambda_7
U = _V[:, ::-1].copy()                # column k is u_k
N = len(LAM)
SHOW = [0, 1, 2, N - 1]               # the three first terms and the last

# the facts the figures lean on
assert np.allclose(U @ np.diag(LAM) @ U.T, A), "the sum of terms must be A"
assert np.allclose(U.T @ U, np.eye(N)), "eigenvectors must be orthonormal"
assert np.allclose(U @ np.diag(LAM ** 2) @ U.T, A @ A), "A^2 = sum lambda_k^2 u_k u_k^T"
assert np.allclose([LAM[0], LAM[-1]], [2.884, -2.259], atol=5e-4)
assert LAM[0] > abs(LAM[-1]) > LAM[1] > 0, "lambda_1 must dominate"
assert (LAM[2] > 0) and (LAM[-1] < 0)

# --------------------------------------------------------------------------- style
BLUE = "cool!70"                      # positive eigenvalue / coefficient
GOLD = "hot!85"                       # negative
UFILL = "pale"                        # eigenvector bars: neutral fill, pencil ink outline
UFILL2 = "pale"                       # a second eigenvector: told apart by its label
OUTLINE = "muted"                     # the (implied) square matrix
RED = "hot"

S = 84                                # side of a drawn matrix, bp
BAR = 15                              # thickness of the tall / wide rectangles


def val(v):
    """Two decimals (none from 10 up) in Meslo, with a true minus sign."""
    r = round(v, 2)
    t = ("%.0f" % v) if abs(r) >= 10 else ("%.2f" % v)
    return t.replace("-", "\u2212")


def tx(x, y, s, color="ink", anchor="center"):
    """Meslo for words and numbers; a label with math goes at FONT_MATH."""
    return F.text(x, y, s, color=color, anchor=anchor, size=F.FONT_MATH if "$" in s else F.FONT)


def sgn_color(v):
    return BLUE if v >= 0 else GOLD


def circle(cx, cy, d, color):
    if d < 0.4:
        return ""
    o = f"\\fill[{color}] ({cx:.1f},{cy:.1f}) circle ({d / 2:.2f}bp);\n"
    if d >= 14:
        o += F.sketch_circle(cx, cy, d, color="ink", w=1.5)
    else:                           # a pencil circle this small breaks TikZ's random steps
        o += f"\\draw[ink,line width=1.2bp] ({cx:.1f},{cy:.1f}) circle ({d / 2:.2f}bp);\n"
    return o


def pencil_rect(x0, y0, x1, y1, fill=None, color="ink", w=1.5):
    """A rectangle in pencil (figlib's `pencil` style), seeded by its corners so a rectangle
    drawn in two frames is drawn the same way."""
    o = F._seed(x0, y0, x1, y1)
    if fill:
        o += f"\\fill[{fill}] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});\n"
    o += (f"\\draw[{color},line width={w}bp,pencil] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});\n")
    return o


def bar(x0, y0, x1, y1, fill, color="ink", w=1.6):
    """A rectangle with a pencil ink outline and a neutral fill."""
    return pencil_rect(x0, y0, x1, y1, fill=fill, color=color, w=w)


def matrix(mx, ytop, side=S, colfill=UFILL, rowfill=UFILL, bar_t=BAR, outline=True, only_outline=False,
           colcolor="ink", rowcolor="ink"):
    """u u^T as the lecturer draws it: a tall rectangle at the left edge, a wide one along the top."""
    o = ""
    if outline:
        o += pencil_rect(mx, ytop - side, mx + side, ytop, color=OUTLINE, w=1.6)
    if only_outline:
        return o
    cw = 2.8 if colcolor != "ink" else 1.6
    rw = 2.8 if rowcolor != "ink" else 1.6
    o += bar(mx, ytop - side, mx + bar_t, ytop, colfill, colcolor, cw)
    o += bar(mx + bar_t + 0.55 * bar_t, ytop - bar_t, mx + side, ytop, rowfill, rowcolor, rw)
    return o


def scope(body, opacity):
    return f"\\begin{{scope}}[opacity={opacity}]\n{body}\\end{{scope}}\n"


# One row of the picture: items laid out left to right with fixed gaps.
def place(items, x0, gap=8):
    """items: list of (key, width).  Returns {key: left x}, and the right edge."""
    pos, x = {}, x0
    for key, w in items:
        pos[key] = x
        x += w + gap
    return pos, x - gap


def centred(items, gap=10):
    """Lay the items out and centre the row in the canvas; the row must fit with a margin."""
    pos, right = place(items, 0, gap)
    assert right <= F.FULL_W - 36, f"row is {right}bp wide"
    shift = (F.FULL_W - right) / 2
    return {k: v + shift for k, v in pos.items()}


TG = 10                                         # gap between a term's circle slot and its matrix
COEF_END = -14                                  # a coefficient ends this far left of its matrix, right-aligned against its u label


def term(x, ytop, slot, lam_str, d, color, mlabel, top_label=None, side=S, fade=1.0,
         dy_label=32):
    """One term: circle in a slot of width `slot`, then the matrix; labels beneath."""
    cx, cy = x + slot / 2, ytop - side / 2
    mx = x + slot + TG
    ylab = ytop - side - dy_label
    o = circle(cx, cy, d, color)
    o += matrix(mx, ytop, side)
    if lam_str:                     # right-aligned, ending just before its u u^T label
        o += tx(mx + COEF_END, ylab, lam_str, anchor="east")
    if mlabel:
        o += tx(mx + side / 2, ylab, mlabel)
    if top_label:
        o += top_label(cx, ytop + 30)
    return scope(o, fade) if fade < 1 else o


def uu(k):
    return "$\\mathbf{u}_%s\\mathbf{u}_%s^{\\top}$" % (k, k)


KLAB = {0: "1", 1: "2", 2: "3", N - 1: "7"}

# ONE layout for decomp-sum, decomp-square (last frame) and decomp-power: the left-hand
# side is right-aligned at a fixed x, so the four terms sit in the same columns, with the
# same first circle, on the three consecutive slides.  The "t = ..." band above the row is
# reserved in all three (only decomp-power writes in it).
ROW_SIDE = 72                                  # side of a drawn matrix
ROW_YTOP = 170
ROW_LHS_W = 118
ROW_SLOT = {0: 76, 1: 76, 2: 76, N - 1: 96}
ROW_PLUS = 26
ROW_BOX = (38, 270)                            # the one crop of the row, bp from the canvas top
ROW_H = 300
ROW_ITEMS = [("lhs", ROW_LHS_W), ("t0", ROW_SLOT[0] + TG + ROW_SIDE), ("p1", ROW_PLUS),
             ("t1", ROW_SLOT[1] + TG + ROW_SIDE), ("p2", ROW_PLUS),
             ("t2", ROW_SLOT[2] + TG + ROW_SIDE), ("dots", 126),
             ("t6", ROW_SLOT[N - 1] + TG + ROW_SIDE)]
ROW_POS = centred(ROW_ITEMS)
D1 = 72.0                                      # diameter of the first circle in all three, bp


def row_lhs(pos, s):
    """The left-hand side, right-aligned at the fixed x just before the first circle."""
    return tx(pos["lhs"] + ROW_LHS_W, ROW_YTOP - ROW_SIDE / 2, s, anchor="east")


# --------------------------------------------------------------------------- decomp-sum
D0 = D1 / LAM[0]                               # bp of diameter per unit of |lambda|: lambda_1 is 72 bp


def sum_frame(n_shown, show_top=True):
    """n_shown = 0: 'A =' and four empty outlines; 1..3: terms 1..3; 4: '+ ... +' and the last term."""
    pos, ytop, side = ROW_POS, ROW_YTOP, ROW_SIDE
    ymid = ytop - side / 2
    o = row_lhs(pos, "$A=$")
    for j, k in enumerate(SHOW):
        key = f"t{k if k < 3 else 6}"
        if j >= n_shown:
            # not filled in yet: only the muted outline of the term's square matrix
            o += matrix(pos[key] + ROW_SLOT[k] + TG, ytop, side, only_outline=True)
            continue
        top = (lambda cx, y, k=k: tx(cx, y, "$\\lambda_%s$" % KLAB[k])) if show_top else None
        o += term(pos[key], ytop, ROW_SLOT[k], val(LAM[k]), D0 * abs(LAM[k]),
                  sgn_color(LAM[k]), uu(KLAB[k]), top, side=side)
        if k == 0 and n_shown > 1:
            o += tx(pos["p1"] + ROW_PLUS / 2, ymid, "$+$")
        if k == 1 and n_shown > 2:
            o += tx(pos["p2"] + ROW_PLUS / 2, ymid, "$+$")
        if k == 2 and n_shown > 3:
            o += tx(pos["dots"] + 63, ymid, "$+\\;\\cdots\\;+$")
    return o


def f_sum():
    frames = [sum_frame(n) for n in (0, 1, 2, 3, 4)]
    F.emit_frames("decomp-sum", frames, container="full", h=ROW_H, nodes=False, box=ROW_BOX)


# --------------------------------------------------------------------------- decomp-orth
def f_orth():
    L, T = 210, BAR + 3                       # long side and thickness of the rectangles
    ybot, ymid = 55, 55 + L / 2
    ytop = ybot + L
    panels = [("$k\\neq\\ell$", "$\\mathbf{u}_k^{\\top}$", "$\\mathbf{u}_\\ell$", UFILL, UFILL2,
               "$=0$", RED, 30),
              ("$k=\\ell$", "$\\mathbf{u}_k^{\\top}$", "$\\mathbf{u}_k$", UFILL, UFILL,
               "$=1$", "ink", 560)]
    o = ""
    for head, wl, tl, wfill, tfill, res, rcol, x0 in panels:
        o += tx(x0 + 215, ytop + 36, head)
        # wide rectangle (u_k^T), a dot, a tall rectangle (u_l), the result
        o += bar(x0, ymid - T / 2, x0 + L, ymid + T / 2, wfill)
        o += tx(x0 + L / 2, ymid + T / 2 + 30, wl)
        xd = x0 + L + 34
        o += F.dot(xd, ymid, "ink", 10)
        xt = xd + 34
        o += bar(xt, ybot, xt + T, ytop, tfill)
        o += tx(xt + T / 2, ybot - 28, tl)
        o += tx(xt + T + 70, ymid, res, color=rcol)
    o += F.seg((520, ybot - 40), (520, ytop + 70), color="muted", w=2)
    F.emit("decomp-orth", o, container="full", h=340, nodes=False)


# --------------------------------------------------------------------------- decomp-square
C2 = 9.0                                       # bp of diameter per unit, in this figure only
PS, PSLOT, PBAR = 36, 28, 9                    # pair stage: matrix side, circle slot, bar
GW = 2 * (PSLOT + 6 + PS) + 8                  # width of one product of two terms


def pair(x, ytop, k, l, fade=1.0, tint=False):
    """lambda_k u_k u_k^T  .  lambda_l u_l u_l^T   (two terms side by side)."""
    cy = ytop - PS / 2
    m1 = x + PSLOT + 6
    c2 = m1 + PS + 8
    m2 = c2 + PSLOT + 6
    o = circle(x + PSLOT / 2, cy, C2 * abs(LAM[k]), sgn_color(LAM[k]))
    o += circle(c2 + PSLOT / 2, cy, C2 * abs(LAM[l]), sgn_color(LAM[l]))
    # the pair that gets multiplied: u_k^T (wide bar of the left matrix) against u_l (tall bar of the
    # right one) -- marked by a hot outline, never a hot fill (hot would read as "negative")
    o += matrix(m1, ytop, PS, bar_t=PBAR, rowcolor="hot" if tint else "ink")
    o += matrix(m2, ytop, PS, bar_t=PBAR, colcolor="hot" if tint else "ink")
    return scope(o, fade) if fade < 1 else o


def square_pairs_frame(stage):
    """stage 0: the expanded product; 1: the middle contacts light up; 2: cross terms fade."""
    ytop = 175 - 38 + PS / 2          # same centre line as the final frame
    items = [("lhs", 84)] + sum(([(f"g{i}", GW), (f"p{i}", 36)] for i in range(4)), []) + \
            [("dots", 40)]
    pos = centred(items, gap=6)
    ymid = ytop - PS / 2
    o = tx(pos["lhs"] + 42, ymid, "$A^2=$")
    combos = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for i, (k, l) in enumerate(combos):
        same = k == l
        fade = 0.18 if (stage >= 2 and not same) else 1.0
        o += pair(pos[f"g{i}"], ytop, k, l, fade, tint=stage >= 1)
        if stage >= 1:
            o += tx(pos[f"g{i}"] + GW / 2, ytop - PS - 30, "$=1$" if same else "$=0$",
                        color=RED)
        o += tx(pos[f"p{i}"] + 18, ymid, "$+$")
    o += tx(pos["dots"] + 20, ymid, "$\\cdots$")
    return o


def square_final_frame():
    pos, ytop, side = ROW_POS, ROW_YTOP, ROW_SIDE
    ymid = ytop - side / 2
    c2 = D1 / LAM[0] ** 2                      # lambda_1^2 gets the same 72 bp circle as in the other two
    o = row_lhs(pos, "$A^2=$")
    for k in SHOW:
        top = lambda cx, y, k=k: tx(cx, y, "$\\lambda_%s^2$" % KLAB[k])
        o += term(pos[f"t{k if k < 3 else 6}"], ytop, ROW_SLOT[k], val(LAM[k] ** 2),
                  c2 * LAM[k] ** 2, BLUE, uu(KLAB[k]), top, side=side)
    o += tx(pos["p1"] + ROW_PLUS / 2, ymid, "$+$") + tx(pos["p2"] + ROW_PLUS / 2, ymid, "$+$")
    o += tx(pos["dots"] + 63, ymid, "$+\\;\\cdots\\;+$")
    return o


def f_square():
    # facts: cross terms vanish, the diagonal ones are lambda_k^2 > 0
    assert abs(U[:, 0] @ U[:, 1]) < 1e-9 and abs(U[:, 0] @ U[:, 0] - 1) < 1e-9
    assert all(LAM[k] ** 2 > 0 for k in range(N))
    frames = [square_pairs_frame(0), square_pairs_frame(1), square_pairs_frame(2),
              square_final_frame()]
    F.emit_frames("decomp-square", frames, container="full", h=ROW_H, nodes=False, box=ROW_BOX)


# --------------------------------------------------------------------------- decomp-power
TS = [1, 2, 3, 4, 8, 16]      # t = 3 shows the last term flip back to hot


def power_frame(t):
    pos, ytop, side = ROW_POS, ROW_YTOP, ROW_SIDE
    ymid = ytop - side / 2
    # The circles are divided by lambda_1^t, so the left side says so: "A^t =" with
    # normalised circles would be a false equation.
    o = row_lhs(pos, "$A^t/\\lambda_1^t=$")
    for k in SHOW:
        r = (LAM[k] / LAM[0]) ** t
        o += term(pos[f"t{k if k < 3 else 6}"], ytop, ROW_SLOT[k], val(r), D1 * abs(r),
                  sgn_color(r), uu(KLAB[k]), side=side)
    o += tx(pos["p1"] + ROW_PLUS / 2, ymid, "$+$") + tx(pos["p2"] + ROW_PLUS / 2, ymid, "$+$")
    o += tx(pos["dots"] + 63, ymid, "$+\\;\\cdots\\;+$")
    o += tx(20, ytop + 60, "$t=%d$" % t, anchor="west")
    return o


def f_power():
    # facts: by t = 16 only the first circle is visible
    assert all(abs(LAM[k] / LAM[0]) ** 16 < 0.021 for k in range(1, N))
    assert LAM[-1] / LAM[0] < 0 and (LAM[-1] / LAM[0]) ** 1 < 0
    frames = [power_frame(t) for t in TS]
    F.emit_frames("decomp-power", frames, container="full", h=ROW_H, nodes=False, box=ROW_BOX)


# --------------------------------------------------------------------------- katz-why
KC = 13.0                                      # bp of diameter per sqrt(|coefficient|)
KSLOT = {0: 136, 1: 76, 2: 76, N - 1: 96}
LMAX = "\\lambda_{\\max}"
KSTEPS = [(0.0, "$\\alpha=0$"), (0.5, "$\\alpha=0.5/%s$" % LMAX), (0.8, "$\\alpha=0.8/%s$" % LMAX),
          (0.95, "$\\alpha=0.95/%s$" % LMAX), (0.99, "$\\alpha=0.99/%s$" % LMAX),
          (1.1, "$\\alpha=1.1/%s$" % LMAX)]


def coef(frac, k):
    return 1.0 / (1.0 - frac / LAM[0] * LAM[k])


KSIDE = 72                                    # matrix side: the 130 bp circle and "+ ... +" must fit


def katz_frame(frac, alabel):
    ytop = 190
    items = [("lhs", 30), ("t0", KSLOT[0] + TG + KSIDE), ("p1", 36), ("t1", KSLOT[1] + TG + KSIDE),
             ("p2", 36), ("t2", KSLOT[2] + TG + KSIDE), ("dots", 126), ("t6", KSLOT[N - 1] + TG + KSIDE)]
    pos = centred(items)
    ymid = ytop - KSIDE / 2
    o = tx(pos["lhs"] + 15, ymid, "$=$")
    for k in SHOW:
        c = coef(frac, k)
        d = KC * np.sqrt(abs(c))                # area ~ |coefficient|: 1, 2, 5, 20, 100 read as growing
        top = None
        if c < 0:
            top = lambda cx, y: tx(cx, y, "negative", color=RED)
        # labels sit below the largest possible circle (130 bp), at one height in every frame
        o += term(pos[f"t{k if k < 3 else 6}"], ytop, KSLOT[k], val(c), d, sgn_color(c),
                  uu(KLAB[k]), top, dy_label=56, side=KSIDE)
    o += tx(pos["p1"] + 18, ymid, "$+$") + tx(pos["p2"] + 18, ymid, "$+$")
    o += tx(pos["dots"] + 63, ymid, "$+\\;\\cdots\\;+$")
    o += tx(20, ytop + 84, "$(I-\\alpha A)^{-1}$", anchor="west")
    o += tx(F.FULL_W - 20, ytop + 84, alabel, color=RED, anchor="east")
    return o


def f_katz():
    # facts: the first coefficient 1, 2, 5, 20, 100, then -10 past 1/lambda_1
    got = [coef(f, 0) for f, _ in KSTEPS]
    assert np.allclose(got, [1, 2, 5, 20, 100, -10]), got
    assert all(coef(f, 0) > 0 for f, _ in KSTEPS[:-1]) and coef(1.1, 0) < 0
    assert all(coef(f, k) > 0 for f, _ in KSTEPS for k in range(1, N)), "only term 1 flips"
    frames = [katz_frame(f, lab) for f, lab in KSTEPS]
    F.emit_frames("katz-why", frames, container="full", h=330, nodes=False)


FIGURES = [
    ("decomp-sum", f_sum),
    ("decomp-orth", f_orth),
    ("decomp-square", f_square),
    ("decomp-power", f_power),
    ("katz-why", f_katz),
]
