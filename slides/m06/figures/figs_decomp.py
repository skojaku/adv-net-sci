#!/usr/bin/env python3
"""The decomposition figures: A = sum of lambda_k u_k u_k^T, drawn in the lecturer's notation.

    decomp-sum.gif      A = lambda_1 u_1 u_1^T + lambda_2 ... + ... + lambda_7 ..., one term at a time
    decomp-orth         u_k^T u_l = 0 for k != l, 1 for k = l (wide rectangle times tall rectangle)
    decomp-square.gif   A^2 as a product of two sums: cross terms die, circles become lambda_k^2
    decomp-power.gif    A^t: circle k scaled by (lambda_k / lambda_1)^t, t = 1, 2, 4, 8, 16
    katz-why.gif        (I - alpha A)^-1: coefficient 1 / (1 - alpha lambda_k) per term

Notation, from lecture-note/figs/spectral-decomposition.jpg: an eigenvalue is a filled
circle (diameter proportional to |value|), an eigenvector u_k is a TALL rectangle, its
transpose a WIDE rectangle, and the pair together stands for the square matrix u_k u_k^T.
Blue circle = positive, gold circle = negative.  Every number is computed from the
spectrum of the 7-node graph EIG; none is typed.

The filled circles are drawn in accent!65, not in the node blue: they are values, not
network nodes, and the render gate measures every node-blue disc against the 26-52 px band.
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
BLUE = "accent!65"                    # positive eigenvalue / coefficient
GOLD = "accentthree"                  # negative
UFILL = "accent!25"                   # eigenvectors: neutral
UFILL2 = "accent!55"                  # a second, different eigenvector
OUTLINE = "annot!45"                  # the (implied) square matrix
RED = "accenttwo"

S = 84                                # side of a drawn matrix, bp
BAR = 15                              # thickness of the tall / wide rectangles


def val(v):
    """Two decimals, a true minus sign, inside math so the glyphs match the formulas."""
    if abs(round(v, 2)) >= 10:
        return "$%s$" % ("%.0f" % v)
    return "$%s$" % ("%.2f" % v)


def sgn_color(v):
    return BLUE if v >= 0 else GOLD


def circle(cx, cy, d, color):
    if d < 0.4:
        return ""
    return f"\\fill[{color}] ({cx:.1f},{cy:.1f}) circle ({d / 2:.2f}bp);\n"


def matrix(mx, ytop, side=S, colfill=UFILL, rowfill=UFILL, bar=BAR, outline=True):
    """u u^T as the lecturer draws it: a tall rectangle at the left edge, a wide one along the top."""
    o = ""
    if outline:
        o += (f"\\draw[line width=1.6bp,draw={OUTLINE}] ({mx:.1f},{ytop - side:.1f}) "
              f"rectangle ({mx + side:.1f},{ytop:.1f});\n")
    o += f"\\fill[{colfill}] ({mx:.1f},{ytop - side:.1f}) rectangle ({mx + bar:.1f},{ytop:.1f});\n"
    o += (f"\\fill[{rowfill}] ({mx + bar + 0.55 * bar:.1f},{ytop - bar:.1f}) "
          f"rectangle ({mx + side:.1f},{ytop:.1f});\n")
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


def term(x, ytop, slot, lam_str, d, color, mlabel, top_label=None, side=S, fade=1.0,
         cap_break=False, below_circle=None):
    """One term: circle in a slot of width `slot`, then the matrix; labels beneath."""
    cx, cy = x + slot / 2, ytop - side / 2
    mx = x + slot + TG
    ylab = ytop - side - 32
    o = circle(cx, cy, d, color)
    if cap_break:                               # a white band: the drawn circle is capped
        r = d / 2
        o += (f"\\begin{{scope}}\\clip ({cx:.1f},{cy:.1f}) circle ({r:.2f}bp);"
              f"\\draw[white,line width=6bp] ({cx - r:.1f},{cy - 0.35 * r:.1f}) -- "
              f"({cx + r:.1f},{cy + 0.35 * r - 18:.1f});\\end{{scope}}\n")
    o += matrix(mx, ytop, side)
    if lam_str:
        o += F.text(cx, ylab, lam_str)
    if mlabel:
        o += F.text(mx + side / 2, ylab, mlabel)
    if top_label:
        o += top_label(cx, ytop + 30)
    return scope(o, fade) if fade < 1 else o


def uu(k):
    return "$\\mathbf{u}_%s\\mathbf{u}_%s^{\\top}$" % (k, k)


KLAB = {0: "1", 1: "2", 2: "3", N - 1: "7"}


# --------------------------------------------------------------------------- decomp-sum
D0 = 25.0                                      # bp of diameter per unit of |lambda|
SLOT = {0: 76, 1: 76, 2: 76, N - 1: 96}


def sum_frame(n_shown, lhs="$\\mathbf{A}=$", lhs_w=60, show_top=True):
    """n_shown = 0: just 'A ='; 1..3: terms 1..3; 4: '+ ... +' and the last term."""
    ytop = 170
    items = [("lhs", lhs_w), ("t0", SLOT[0] + TG + S), ("p1", 36), ("t1", SLOT[1] + TG + S),
             ("p2", 36), ("t2", SLOT[2] + TG + S), ("dots", 126), ("t6", SLOT[N - 1] + TG + S)]
    pos = centred(items)
    ymid = ytop - S / 2
    o = F.text(pos["lhs"] + lhs_w / 2, ymid, lhs)
    for j, k in enumerate(SHOW):
        if j >= n_shown:
            break
        top = (lambda cx, y, k=k: F.text(cx, y, "$\\lambda_%s$" % KLAB[k])) if show_top else None
        o += term(pos[f"t{k if k < 3 else 6}"], ytop, SLOT[k], val(LAM[k]), D0 * abs(LAM[k]),
                  sgn_color(LAM[k]), uu(KLAB[k]), top)
        if k == 0 and n_shown > 1:
            o += F.text(pos["p1"] + 18, ymid, "$+$")
        if k == 1 and n_shown > 2:
            o += F.text(pos["p2"] + 18, ymid, "$+$")
        if k == 2 and n_shown > 3:
            o += F.text(pos["dots"] + 63, ymid, "$+\\;\\cdots\\;+$")
    return o


def f_sum():
    frames = [sum_frame(n) for n in (0, 1, 2, 3, 4)]
    F.emit_gif("decomp-sum", frames, container="full", h=300, ms=1100, hold=4, nodes=False)


# --------------------------------------------------------------------------- decomp-orth
def f_orth():
    L, T = 210, BAR + 3                       # long side and thickness of the rectangles
    ybot, ymid = 55, 55 + L / 2
    ytop = ybot + L
    panels = [("$k\\neq\\ell$", "$\\mathbf{u}_k^{\\top}$", "$\\mathbf{u}_\\ell$", UFILL, UFILL2,
               "$=0$", RED, 30),
              ("$k=\\ell$", "$\\mathbf{u}_k^{\\top}$", "$\\mathbf{u}_k$", UFILL, UFILL,
               "$=1$", "black", 560)]
    o = ""
    for head, wl, tl, wfill, tfill, res, rcol, x0 in panels:
        o += F.text(x0 + 215, ytop + 36, head)
        # wide rectangle (u_k^T), a dot, a tall rectangle (u_l), the result
        o += f"\\fill[{wfill}] ({x0},{ymid - T / 2:.1f}) rectangle ({x0 + L},{ymid + T / 2:.1f});\n"
        o += F.text(x0 + L / 2, ymid + T / 2 + 30, wl)
        xd = x0 + L + 34
        o += F.dot(xd, ymid, "black", 10)
        xt = xd + 34
        o += f"\\fill[{tfill}] ({xt},{ybot}) rectangle ({xt + T},{ytop});\n"
        o += F.text(xt + T / 2, ybot - 28, tl)
        o += F.text(xt + T + 70, ymid, res, color=rcol)
    o += F.seg((520, ybot - 40), (520, ytop + 70), color="annot!40", w=2)
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
    o += matrix(m1, ytop, PS, bar=PBAR, rowfill=RED + "!45" if tint else UFILL)
    o += matrix(m2, ytop, PS, bar=PBAR, colfill=RED + "!45" if tint else UFILL)
    return scope(o, fade) if fade < 1 else o


def square_pairs_frame(stage):
    """stage 0: the expanded product; 1: the middle contacts light up; 2: cross terms fade."""
    ytop = 175 - 38 + PS / 2          # same centre line as the final frame
    items = [("lhs", 84)] + sum(([(f"g{i}", GW), (f"p{i}", 36)] for i in range(4)), []) + \
            [("dots", 40)]
    pos = centred(items, gap=6)
    ymid = ytop - PS / 2
    o = F.text(pos["lhs"] + 42, ymid, "$\\mathbf{A}^2=$")
    combos = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for i, (k, l) in enumerate(combos):
        same = k == l
        fade = 0.18 if (stage >= 2 and not same) else 1.0
        o += pair(pos[f"g{i}"], ytop, k, l, fade, tint=stage >= 1)
        if stage >= 1:
            o += F.text(pos[f"g{i}"] + GW / 2, ytop - PS - 30, "$=1$" if same else "$=0$",
                        color=RED)
        o += F.text(pos[f"p{i}"] + 18, ymid, "$+$")
    o += F.text(pos["dots"] + 20, ymid, "$\\cdots$")
    return o


def square_final_frame():
    ytop, side = 175, 76
    slot = {0: 80, 1: 72, 2: 72, N - 1: 72}
    items = [("lhs", 84), ("t0", slot[0] + TG + side), ("p1", 36), ("t1", slot[1] + TG + side),
             ("p2", 36), ("t2", slot[2] + TG + side), ("dots", 126),
             ("t6", slot[N - 1] + TG + side)]
    pos = centred(items)
    ymid = ytop - side / 2
    o = F.text(pos["lhs"] + 42, ymid, "$\\mathbf{A}^2=$")
    for k in SHOW:
        o += term(pos[f"t{k if k < 3 else 6}"], ytop, slot[k], val(LAM[k] ** 2),
                  C2 * LAM[k] ** 2, BLUE, uu(KLAB[k]), side=side)
    o += F.text(pos["p1"] + 18, ymid, "$+$") + F.text(pos["p2"] + 18, ymid, "$+$")
    o += F.text(pos["dots"] + 63, ymid, "$+\\;\\cdots\\;+$")
    return o


def f_square():
    # facts: cross terms vanish, the diagonal ones are lambda_k^2 > 0
    assert abs(U[:, 0] @ U[:, 1]) < 1e-9 and abs(U[:, 0] @ U[:, 0] - 1) < 1e-9
    assert all(LAM[k] ** 2 > 0 for k in range(N))
    frames = [square_pairs_frame(0), square_pairs_frame(1), square_pairs_frame(2),
              square_final_frame()]
    F.emit_gif("decomp-square", frames, container="full", h=300, ms=1500, hold=4, nodes=False)


# --------------------------------------------------------------------------- decomp-power
D1 = 72.0                                      # diameter of the first circle, bp
TS = [1, 2, 3, 4, 8, 16]      # t = 3 shows the last term flip back to gold


def power_frame(t):
    ytop = 170
    # The circles are divided by lambda_1^t, so the left side says so: "A^t =" with
    # normalised circles would be a false equation.
    items = [("lhs", 118), ("t0", SLOT[0] + TG + S), ("p1", 26), ("t1", SLOT[1] + TG + S),
             ("p2", 26), ("t2", SLOT[2] + TG + S), ("dots", 96), ("t6", SLOT[N - 1] + TG + S)]
    pos = centred(items)
    ymid = ytop - S / 2
    o = F.text(pos["lhs"] + 59, ymid, "$\\mathbf{A}^t/\\lambda_1^t=$")
    for k in SHOW:
        r = (LAM[k] / LAM[0]) ** t
        o += term(pos[f"t{k if k < 3 else 6}"], ytop, SLOT[k], val(r), D1 * abs(r),
                  sgn_color(r), uu(KLAB[k]))
    o += F.text(pos["p1"] + 13, ymid, "$+$") + F.text(pos["p2"] + 13, ymid, "$+$")
    o += F.text(pos["dots"] + 48, ymid, "$+\\;\\cdots\\;+$")
    o += F.text(20, ytop + 60, "$t=%d$" % t, color=RED, anchor="west")
    return o


def f_power():
    # facts: by t = 16 only the first circle is visible
    assert all(abs(LAM[k] / LAM[0]) ** 16 < 0.021 for k in range(1, N))
    assert LAM[-1] / LAM[0] < 0 and (LAM[-1] / LAM[0]) ** 1 < 0
    frames = [power_frame(t) for t in TS]
    F.emit_gif("decomp-power", frames, container="full", h=300, ms=1500, hold=4, nodes=False)


# --------------------------------------------------------------------------- katz-why
KC = 18.0                                      # bp of diameter per unit of coefficient
KCAP = 100.0
KSLOT = {0: 96, 1: 76, 2: 76, N - 1: 96}
KSTEPS = [(0.0, "$\\alpha=0$"), (0.5, "$\\alpha=0.5/\\lambda_1$"), (0.8, "$\\alpha=0.8/\\lambda_1$"),
          (0.95, "$\\alpha=0.95/\\lambda_1$"), (0.99, "$\\alpha=0.99/\\lambda_1$"),
          (1.1, "$\\alpha=1.1/\\lambda_1$")]


def coef(frac, k):
    return 1.0 / (1.0 - frac / LAM[0] * LAM[k])


def katz_frame(frac, alabel):
    ytop = 170
    items = [("lhs", 30), ("t0", KSLOT[0] + TG + S), ("p1", 36), ("t1", KSLOT[1] + TG + S),
             ("p2", 36), ("t2", KSLOT[2] + TG + S), ("dots", 126), ("t6", KSLOT[N - 1] + TG + S)]
    pos = centred(items)
    ymid = ytop - S / 2
    o = F.text(pos["lhs"] + 15, ymid, "$=$")
    for k in SHOW:
        c = coef(frac, k)
        d = min(KC * abs(c), KCAP)
        capped = KC * abs(c) > KCAP
        top = None
        if c < 0:
            top = lambda cx, y: F.text(cx, y, "negative", color=RED)
        o += term(pos[f"t{k if k < 3 else 6}"], ytop, KSLOT[k], val(c), d, sgn_color(c),
                  uu(KLAB[k]), top, cap_break=capped)
    o += F.text(pos["p1"] + 18, ymid, "$+$") + F.text(pos["p2"] + 18, ymid, "$+$")
    o += F.text(pos["dots"] + 63, ymid, "$+\\;\\cdots\\;+$")
    o += F.text(20, ytop + 84, "$(\\mathbf{I}-\\alpha\\mathbf{A})^{-1}$", anchor="west")
    o += F.text(F.FULL_W - 20, ytop + 84, alabel, color=RED, anchor="east")
    return o


def f_katz():
    # facts: the first coefficient 1, 2, 5, 20, 100, then -10 past 1/lambda_1
    got = [coef(f, 0) for f, _ in KSTEPS]
    assert np.allclose(got, [1, 2, 5, 20, 100, -10]), got
    assert all(coef(f, 0) > 0 for f, _ in KSTEPS[:-1]) and coef(1.1, 0) < 0
    assert all(coef(f, k) > 0 for f, _ in KSTEPS for k in range(1, N)), "only term 1 flips"
    frames = [katz_frame(f, lab) for f, lab in KSTEPS]
    F.emit_gif("katz-why", frames, container="full", h=300, ms=1300, hold=4, nodes=False)


FIGURES = [
    ("decomp-sum", f_sum),
    ("decomp-orth", f_orth),
    ("decomp-square", f_square),
    ("decomp-power", f_power),
    ("katz-why", f_katz),
]
