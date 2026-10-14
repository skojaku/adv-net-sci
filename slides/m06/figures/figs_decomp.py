#!/usr/bin/env python3
"""The decomposition figures: A = sum of lambda_k u_k u_k^T, drawn in the lecturer's notation.

    decomp-sum      static: A = lambda_1 u_1 u_1^T + lambda_2 u_2 u_2^T + ... + lambda_7 u_7 u_7^T
    decomp-orth     u_k^T u_l = 0 for k != l (two colours), 1 for k = l (one colour)
    decomp-square   frames: A^2 = (sum)(sum); different colours meet: 0; same colour: 1; the result
    decomp-power    frames: A^t / lambda_1^t: circle k scaled by (lambda_k / lambda_1)^t, t = 1, 2, 4, 16
    katz-why        frames: an alpha gauge, the function 1/(1 - alpha x) with the eigenvalues on it,
                    and (I - alpha A)^-1 as the sum with coefficient 1 / (1 - alpha lambda_k)

Notation, from lecture-note/figs/spectral-decomposition.jpg: an eigenvalue is a filled
circle (diameter proportional to |value|), an eigenvector u_k is a TALL rectangle, its
transpose a WIDE rectangle, and the pair together stands for the square matrix u_k u_k^T.
Palette: a circle is cool if the value is positive and hot if it is negative. The bars are
coloured by WHICH eigenvector they are (the lecturer, 2026-10-13): u_1 blue, u_2 gold, u_7 pale.
Same colour meeting same colour is u_k^T u_k = 1; two colours meeting is u_k^T u_l = 0, so the
eye can see which products survive. Words and numbers are Meslo, math is Latin Modern at
FONT_MATH.  Every number is computed from the spectrum of the 7-node graph EIG; none is typed.

The builds are frames (F.emit_frames), one small step each, every step with a grey callout.
Three terms (1, 2 and 7) instead of four, so the drawn matrices can be large.

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
SHOW = [0, 1, N - 1]                  # the first two terms and the last

# the facts the figures lean on
assert np.allclose(U @ np.diag(LAM) @ U.T, A), "the sum of terms must be A"
assert np.allclose(U.T @ U, np.eye(N)), "eigenvectors must be orthonormal"
assert np.allclose(U @ np.diag(LAM ** 2) @ U.T, A @ A), "A^2 = sum lambda_k^2 u_k u_k^T"
assert np.allclose([LAM[0], LAM[-1]], [2.884, -2.259], atol=5e-4)
assert LAM[0] > abs(LAM[-1]) > LAM[1] > 0, "lambda_1 must dominate"
assert (LAM[2] > 0) and (LAM[-1] < 0)

# --------------------------------------------------------------------------- style
BLUE = "cool!70"                      # positive eigenvalue / coefficient
GOLD = "hot!85"                       # negative (the name is historical: it is the hot orange)
OUTLINE = "muted"                     # the (implied) square matrix
RED = "hot"

# Which eigenvector a bar is: u_1 blue, u_2 gold, u_7 (and any other) pale.
VFILL = {0: "cool!55", 1: "gold!70", N - 1: "pale"}
VNAME = {0: "blue", 1: "gold", N - 1: "grey"}
KLAB = {0: "1", 1: "2", N - 1: "7"}
KEY = {0: "t0", 1: "t1", N - 1: "t6"}

BAR_FRAC = 0.15                       # bar thickness as a share of the matrix side


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


def matrix(mx, ytop, side, k, colw=1.6, roww=1.6, only_outline=False):
    """u_k u_k^T as the lecturer draws it: a tall bar (u_k) at the left edge and a wide bar
    (u_k^T) along the top, both in u_k's colour, inside the muted outline of the square."""
    bar_t = BAR_FRAC * side
    o = pencil_rect(mx, ytop - side, mx + side, ytop, color=OUTLINE, w=1.6)
    if only_outline:
        return o
    o += pencil_rect(mx, ytop - side, mx + bar_t, ytop, VFILL[k], "ink", colw)
    o += pencil_rect(mx + 1.55 * bar_t, ytop - bar_t, mx + side, ytop, VFILL[k], "ink", roww)
    return o


def row_bar_top(mx, ytop, side):
    """Top centre of a matrix's wide bar (u^T) and of its tall bar (u)."""
    bar_t = BAR_FRAC * side
    return (mx + (1.55 * bar_t + side) / 2, ytop), (mx + bar_t / 2, ytop)


def scope(body, opacity):
    return f"\\begin{{scope}}[opacity={opacity}]\n{body}\\end{{scope}}\n"


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
COEF_END = -14                                  # a coefficient ends this far left of its matrix


def term(x, ytop, slot, k, lam_str, d, color, top_label=None, side=100, dy_label=34):
    """One term: circle in a slot of width `slot`, then u_k u_k^T; labels beneath."""
    cx, cy = x + slot / 2, ytop - side / 2
    mx = x + slot + TG
    ylab = ytop - side - dy_label
    o = circle(cx, cy, d, color)
    o += matrix(mx, ytop, side, k)
    if lam_str:                     # right-aligned, ending just before its u u^T label
        o += tx(mx + COEF_END, ylab, lam_str, anchor="east")
    o += tx(mx + side / 2, ylab, uu(KLAB[k]))
    if top_label:
        o += top_label(cx, ytop + 30)
    return o


def uu(k):
    return "$\\mathbf{u}_%s\\mathbf{u}_%s^{\\top}$" % (k, k)


# ONE layout for decomp-sum, decomp-square (last frame) and decomp-power: the left-hand
# side is right-aligned at a fixed x, so the three terms sit in the same columns, with the
# same first circle, on consecutive slides. A callout band above the row is reserved in all.
ROW_H = 340
ROW_SIDE = 100                                 # side of a drawn matrix
ROW_YTOP = 196
ROW_LHS_W = 118
ROW_SLOT = {0: 100, 1: 100, N - 1: 110}
ROW_PLUS = 30
ROW_DOTS = 126
ROW_BOX = (ROW_H - 300, ROW_H - 30)            # the one crop of the row, bp from the canvas top
ROW_ITEMS = [("lhs", ROW_LHS_W), ("t0", ROW_SLOT[0] + TG + ROW_SIDE), ("p1", ROW_PLUS),
             ("t1", ROW_SLOT[1] + TG + ROW_SIDE), ("dots", ROW_DOTS),
             ("t6", ROW_SLOT[N - 1] + TG + ROW_SIDE)]
ROW_POS = centred(ROW_ITEMS)
D1 = 96.0                                      # diameter of the first circle in all three, bp
YMID = ROW_YTOP - ROW_SIDE / 2


def row_lhs(s):
    """The left-hand side, right-aligned at the fixed x just before the first circle."""
    return tx(ROW_POS["lhs"] + ROW_LHS_W, YMID, s, anchor="east")


def row_ops():
    """The '+' after term 1 and the '+ ... +' before the last term."""
    return (tx(ROW_POS["p1"] + ROW_PLUS / 2, YMID, "$+$")
            + tx(ROW_POS["dots"] + ROW_DOTS / 2, YMID, "$+\\;\\cdots\\;+$"))


BAND_Y = 272                                   # the callout band, above the row


def co(text, at, target, anchor="west", gap=8.0, bend=0, tip=None):
    """A muted callout in the band above the row; the box is asserted inside the band and canvas."""
    assert "$" not in text, "callouts are plain Meslo text"
    o, b = F.callout(text, at, target, anchor=anchor, bend=bend, gap=gap, size=F.FONT, tip=tip)
    assert 6 <= b[0] and b[2] <= F.FULL_W - 6, f"callout {text!r} runs off the canvas {b}"
    assert b[1] >= ROW_YTOP + 44 and b[3] <= ROW_H - ROW_BOX[0] - 2, f"callout {text!r} leaves its band {b}"
    return o


def circle_xy(k):
    """Centre of the circle of term k in the shared row."""
    return ROW_POS[KEY[k]] + ROW_SLOT[k] / 2, YMID


def row(coefs, diam, top=None):
    """The three terms of the shared row: coefficient strings, circle diameters, colours from
    the signs, optional labels above the circles."""
    o = ""
    for k in SHOW:
        o += term(ROW_POS[KEY[k]], ROW_YTOP, ROW_SLOT[k], k, coefs[k], diam[k],
                  sgn_color(float(coefs[k].replace("\u2212", "-"))),
                  (lambda cx, y, k=k: top(cx, y, k)) if top else None, side=ROW_SIDE)
    return o + row_ops()


# --------------------------------------------------------------------------- decomp-sum
D0 = D1 / LAM[0]                               # bp of diameter per unit of |lambda|


def f_sum():
    """Static: the sum, three terms."""
    import shutil
    shutil.rmtree(F.FRAMES / "decomp-sum", ignore_errors=True)
    o = row_lhs("$A=$")
    o += row({k: val(LAM[k]) for k in SHOW}, {k: D0 * abs(LAM[k]) for k in SHOW},
             top=lambda cx, y, k: tx(cx, y, "$\\lambda_%s$" % KLAB[k]))
    F.emit("decomp-sum", o, container="full", h=ROW_H, nodes=False, box=ROW_BOX)


# --------------------------------------------------------------------------- decomp-orth
def f_orth():
    """u_k^T u_l: blue against gold is 0, blue against blue is 1."""
    L, T = 210, 18                             # long side and thickness of the bars
    ybot, ymid = 55, 55 + L / 2
    ytop = ybot + L
    panels = [("$k\\neq\\ell$", "$\\mathbf{u}_k^{\\top}$", "$\\mathbf{u}_\\ell$", VFILL[0], VFILL[1],
               "$=0$", RED, 30),
              ("$k=\\ell$", "$\\mathbf{u}_k^{\\top}$", "$\\mathbf{u}_k$", VFILL[0], VFILL[0],
               "$=1$", "ink", 560)]
    o = ""
    for head, wl, tl, wfill, tfill, res, rcol, x0 in panels:
        o += tx(x0 + 215, ytop + 36, head)
        o += pencil_rect(x0, ymid - T / 2, x0 + L, ymid + T / 2, wfill, "ink", 1.6)
        o += tx(x0 + L / 2, ymid + T / 2 + 30, wl)
        xd = x0 + L + 34
        o += F.dot(xd, ymid, "ink", 10)
        xt = xd + 34
        o += pencil_rect(xt, ybot, xt + T, ytop, tfill, "ink", 1.6)
        o += tx(xt + T / 2, ybot - 28, tl)
        o += tx(xt + T + 70, ymid, res, color=rcol)
    o += F.seg((520, ybot - 40), (520, ytop + 70), color="muted", w=2)
    F.emit("decomp-orth", o, container="full", h=340, nodes=False)


# --------------------------------------------------------------------------- decomp-square
# Frames 00-02: A^2 = ( l1 u1u1' + l2 u2u2' + ... ) ( l1 u1u1' + l2 u2u2' + ... ), two factors
# on the row's centre line. Frame 01: u_1^T (blue) of the left factor meets u_2 (gold) of the
# right one: 0. Frame 02: u_1^T meets u_1 (blue, blue): 1. Frame 03: the result, on the row.
FSIDE, FSLOT, FD1 = 60, 62, 58.0               # factor stage: matrix side, circle slot, lambda_1 circle
FPAREN, FPLUS, FDOTS = 26, 28, 84
FTOP = YMID + FSIDE / 2


def _factor_items(tag):
    return [(f"{tag}(", FPAREN), (f"{tag}0", FSLOT + TG + FSIDE), (f"{tag}p", FPLUS),
            (f"{tag}1", FSLOT + TG + FSIDE), (f"{tag}dots", FDOTS), (f"{tag})", FPAREN)]


FPOS = centred([("lhs", 84)] + _factor_items("L") + _factor_items("R"), gap=6)


def _paren(x, s):
    strut = "\\rule[-40bp]{0pt}{80bp}"
    body = f"\\left({strut}\\right." if s == "(" else f"\\left.{strut}\\right)"
    return F.text(x, YMID, f"${body}$", size=F.FONT_MATH)


def factor(tag, wide=None, tall=None):
    """One factor ( l1 u1u1' + l2 u2u2' + ... ). `wide` / `tall`: the index k whose wide bar
    (u_k^T) / tall bar (u_k) gets a heavy outline, the pair being multiplied."""
    o = _paren(FPOS[f"{tag}("] + FPAREN / 2, "(")
    for j, k in enumerate((0, 1)):
        x = FPOS[f"{tag}{j}"]
        o += circle(x + FSLOT / 2, YMID, FD1 * abs(LAM[k]) / LAM[0], sgn_color(LAM[k]))
        o += matrix(x + FSLOT + TG, FTOP, FSIDE, k,
                    colw=3.2 if tall == k else 1.6, roww=3.2 if wide == k else 1.6)
    o += tx(FPOS[f"{tag}p"] + FPLUS / 2, YMID, "$+$")
    o += tx(FPOS[f"{tag}dots"] + 6, YMID, "$+\\;\\cdots$", anchor="west")
    o += _paren(FPOS[f"{tag})"] + FPAREN / 2, ")")
    return o


def factors_frame(meet=None):
    """meet = (k, l): u_k^T of the left factor against u_l of the right factor, joined by an arc
    and named in the band."""
    o = tx(FPOS["lhs"] + 42, YMID, "$A^2=$")
    if meet is None:
        return o + factor("L") + factor("R")
    k, l = meet
    o += factor("L", wide=k) + factor("R", tall=l)
    p, _ = row_bar_top(FPOS[f"L{k}"] + FSLOT + TG, FTOP, FSIDE)
    _, q = row_bar_top(FPOS[f"R{l}"] + FSLOT + TG, FTOP, FSIDE)
    h = 64
    o += (f"\\draw[muted,line width=1.8bp,line cap=round,{{Stealth[length=9bp,width=7bp]}}-"
          f"{{Stealth[length=9bp,width=7bp]}}] ({p[0]:.1f},{p[1] + 6:.1f}) .. controls "
          f"({p[0]:.1f},{p[1] + h:.1f}) and ({q[0]:.1f},{q[1] + h:.1f}) .. ({q[0]:.1f},{q[1] + 6:.1f});\n")
    dot = U[:, k] @ U[:, l]
    want = 1 if k == l else 0
    assert abs(dot - want) < 1e-9, (k, l, dot)
    sub = {0: "\u2081", 1: "\u2082"}
    text = (f"u{sub[k]}\u1d40u{sub[l]} = {want}: " +
            ("same colour" if k == l else "different colours vanish"))
    mx = (p[0] + q[0]) / 2
    b = F.label_box(mx, BAND_Y, text, "center", pad=2)
    assert 6 <= b[0] and b[2] <= F.FULL_W - 6, f"{text!r} runs off the canvas"
    assert b[1] >= FTOP + 0.75 * h + 4, f"{text!r} sits on its arc"
    o += F.text(mx, BAND_Y, text, color="muted")
    return o


def square_final_frame():
    c2 = D1 / LAM[0] ** 2                      # lambda_1^2 gets the same circle as lambda_1 in the sum
    o = row_lhs("$A^2=$")
    o += row({k: val(LAM[k] ** 2) for k in SHOW}, {k: c2 * LAM[k] ** 2 for k in SHOW},
             top=lambda cx, y, k: tx(cx, y, "$\\lambda_%s^2$" % KLAB[k]))
    cx, cy = circle_xy(0)
    o += co("each eigenvalue squared, same colours", (20, BAND_Y), (cx, cy), gap=D1 / 2 + 8,
            tip=(110, BAND_Y - 18))
    return o


def f_square():
    # facts: cross terms vanish, the diagonal ones are lambda_k^2 > 0
    assert abs(U[:, 0] @ U[:, 1]) < 1e-9 and abs(U[:, 0] @ U[:, 0] - 1) < 1e-9
    assert all(LAM[k] ** 2 > 0 for k in range(N))
    frames = [factors_frame(), factors_frame((0, 1)), factors_frame((0, 0)), square_final_frame()]
    F.emit_frames("decomp-square", frames, container="full", h=ROW_H, nodes=False, box=ROW_BOX)


# --------------------------------------------------------------------------- decomp-power
TS = [1, 2, 4, 16]            # t = 2: the last term turns positive


def _r(k, t):
    return (LAM[k] / LAM[0]) ** t


def _note1():
    assert all(abs(_r(k, 1)) > 0.05 for k in range(N)), "t = 1: every term still shows"
    # what a circle is: its eigenvalue over the largest one (1.00 for the first, 0.46, ..., -0.78)
    assert abs(_r(0, 1) - 1) < 1e-12
    cx, cy = circle_xy(0)
    return co("circles: \u03bbk / \u03bb1", (20, BAND_Y), (cx, cy), gap=D1 / 2 + 8,
              tip=(130, BAND_Y - 18))


def _note2():
    assert _r(N - 1, 1) < 0 < _r(N - 1, 2), "the negative term turns positive at t = 2"
    cx, cy = circle_xy(N - 1)
    return co("t = 2: the negative term turns positive", (cx + 140, BAND_Y), (cx, cy),
              anchor="east", gap=D1 * abs(_r(N - 1, 2)) / 2 + 8)


def _note4():
    assert abs(_r(1, 4)) < 0.05, "t = 4: term 2 has faded"
    cx, cy = circle_xy(1)
    return co("t = 4: the small terms fade", (20, BAND_Y), (cx, cy), gap=10, tip=(cx - 24, BAND_Y - 18))


def _note16():
    assert all(abs(_r(k, 16)) < 0.021 for k in range(1, N)), "t = 16: only the first is left"
    cx, cy = circle_xy(0)
    return co("t = 16: only the first is left", (20, BAND_Y), (cx, cy), gap=D1 / 2 + 8,
              tip=(130, BAND_Y - 18))


POWER_NOTE = {1: _note1, 2: _note2, 4: _note4, 16: _note16}


def power_frame(t):
    # The circles are divided by lambda_1^t, so the left side says so: "A^t =" with
    # normalised circles would be a false equation.
    o = row_lhs("$A^t/\\lambda_1^t=$")
    o += row({k: val(_r(k, t)) for k in SHOW}, {k: D1 * abs(_r(k, t)) for k in SHOW})
    return o + POWER_NOTE[t]()


def f_power():
    assert all(abs(LAM[k] / LAM[0]) ** 16 < 0.021 for k in range(1, N))
    assert LAM[-1] / LAM[0] < 0
    frames = [power_frame(t) for t in TS]
    F.emit_frames("decomp-power", frames, container="full", h=ROW_H, nodes=False, box=ROW_BOX)


# --------------------------------------------------------------------------- katz-why
# One canvas, three parts. Top left: a gauge for alpha (0 to 1.2/lambda_max, the tick at
# 1/lambda_max, the part past it shaded as the danger zone). Top right: the function
# 1/(1 - alpha x), the eigenvalues as dots on it, the wall x = 1/alpha drawn when it is in
# view. Bottom: (I - alpha A)^-1 as the three-term sum, circle k sized by 1/(1 - alpha lambda_k).
KH = 380
KSIDE = 92
KYTOP = 150
KYMID = KYTOP - KSIDE / 2
KSLOT = {0: 86, 1: 64, N - 1: 64}
KC = 17.0                                      # bp of diameter per sqrt(|coefficient|)
KLHS = 196
KITEMS = [("lhs", KLHS), ("t0", KSLOT[0] + TG + KSIDE), ("p1", 30),
          ("t1", KSLOT[1] + TG + KSIDE), ("dots", 120), ("t6", KSLOT[N - 1] + TG + KSIDE)]
KPOS, _KRIGHT = place(KITEMS, 30, 10)             # left-aligned: the slide number sits at the bottom right
assert _KRIGHT <= F.FULL_W - 90
KFRACS = [0.5, 0.8, 0.95, 1.1]                 # alpha * lambda_max on the four slides

# the plot: x in [XLO, XHI], y in [YLO, YHI], drawn in the box (PX0, PY0)-(PX1, PY1)
XLO, XHI, YLO, YHI = -2.6, 4.2, -3.0, 6.0
PX0, PX1, PY0, PY1 = 548.0, 1040.0, 190.0, 340.0


def px(x):
    return PX0 + (x - XLO) / (XHI - XLO) * (PX1 - PX0)


def py(y):
    return PY0 + (y - YLO) / (YHI - YLO) * (PY1 - PY0)


# the gauge
GX0, GX1, GY = 70.0, 470.0, 310.0
GMAX = 1.2                                     # alpha * lambda_max at the right end


def gx(frac):
    return GX0 + frac / GMAX * (GX1 - GX0)


def coef(frac, k):
    return 1.0 / (1.0 - frac / LAM[0] * LAM[k])


def gauge(frac):
    o = tx(24, GY, "$\\alpha$", anchor="west")
    # the track, the safe part filled up to the knob, the danger zone past 1/lambda_max
    o += f"\\fill[hot!18] ({gx(1):.1f},{GY - 7:.1f}) rectangle ({GX1:.1f},{GY + 7:.1f});\n"
    o += f"\\fill[cool!45] ({GX0:.1f},{GY - 7:.1f}) rectangle ({gx(min(frac, 1.0)):.1f},{GY + 7:.1f});\n"
    if frac > 1:
        o += f"\\fill[hot!55] ({gx(1):.1f},{GY - 7:.1f}) rectangle ({gx(frac):.1f},{GY + 7:.1f});\n"
    o += pencil_rect(GX0, GY - 7, GX1, GY + 7, None, "ink", 1.6)
    o += F.seg((gx(1), GY - 16), (gx(1), GY + 16), color="ink", w=2.4, sketch=False)
    o += tx(GX0, GY - 36, "0")
    o += tx(gx(1), GY - 38, "$1/\\lambda_{\\max}$")
    # the knob and its value
    o += F.disc(gx(frac), GY, "", fill="white", size=26)
    lab = "%.2g" % frac if frac != 1.1 else "1.1"
    o += tx(gx(frac), GY + 28, f"{lab}/\u03bbmax", color="hot" if frac > 1 else "ink")
    return o


def curve(frac):
    """1/(1 - a x) on [XLO, XHI], clipped to the plot box, split at the wall x = 1/a."""
    a = frac / LAM[0]
    wall = 1.0 / a
    xs = np.linspace(XLO, XHI, 900)
    # the branch past the wall is drawn only once alpha is past 1/lambda_max, where it carries lambda_1's
    # negative weight; before that its only visible piece is a stray arc at the floor of the plot
    pieces = [xs[xs < wall - 1e-3]] + ([xs[xs > wall + 1e-3]] if frac > 1 else [])
    o = f"\\begin{{scope}}\\clip ({PX0:.1f},{PY0:.1f}) rectangle ({PX1:.1f},{PY1:.1f});\n"
    for p in pieces:
        if len(p) < 2:
            continue
        ys = np.clip(1.0 / (1.0 - a * p), YLO - 2, YHI + 2)
        pts = " -- ".join(f"({px(x):.1f},{py(y):.1f})" for x, y in zip(p, ys))
        o += f"\\draw[ink,line width=2.6bp,line join=round,line cap=round] {pts};\n"
    o += "\\end{scope}\n"
    return o, wall


def plot(frac):
    a = frac / LAM[0]
    o = ""
    # axes: x axis at y = 0, a faint line at y = 1 (the weight of every term at alpha = 0)
    o += F.seg((px(XLO), py(0)), (px(XHI) + 14, py(0)), color="muted", w=1.8, sketch=False,
               arrow="-{Stealth[length=8bp,width=6bp]}")
    o += F.seg((px(0), py(YLO)), (px(0), py(YHI) + 8), color="muted", w=1.8, sketch=False,
               arrow="-{Stealth[length=8bp,width=6bp]}")
    o += f"\\draw[muted,line width=1.2bp,dash pattern=on 4bp off 4bp] ({px(XLO):.1f},{py(1):.1f}) -- ({px(XHI):.1f},{py(1):.1f});\n"
    o += tx(px(XHI) + 8, py(1), "1", color="muted", anchor="west")
    o += tx(px(XHI) + 22, py(0) - 26, "$x$", color="muted")
    # the eigenvalue ticks, and lambda_1 named
    for k in range(N):
        o += F.seg((px(LAM[k]), py(0) - 6), (px(LAM[k]), py(0) + 6), color="muted", w=2.0, sketch=False)
    c, wall = curve(frac)
    o += c
    if wall <= XHI:
        o += (f"\\draw[hot,line width=1.8bp,dash pattern=on 6bp off 5bp] ({px(wall):.1f},{py(YLO):.1f}) -- "
              f"({px(wall):.1f},{py(YHI):.1f});\n")
        o += tx(px(wall) + 6, py(YHI) - 14, "$1/\\alpha$", color="hot", anchor="west")
    # lambda_1 named on a white ground, so the wall passes behind the label
    o += tx(px(LAM[0]), py(0) - 30, "$\\lambda_1$").replace("align=center]", "align=center,fill=white,inner sep=1.5bp]")
    # the dots: the value of every eigenvalue on the curve; off the plot, an arrow at the edge
    for k in range(N):
        v = coef(frac, k)
        col = sgn_color(v) if k in SHOW else "pale"
        if YLO <= v <= YHI:
            o += F.dot(px(LAM[k]), py(v), col, 15 if k in SHOW else 10)
            o += f"\\draw[ink,line width=1.2bp] ({px(LAM[k]):.1f},{py(v):.1f}) circle (7.5bp);\n" if k in SHOW else ""
        else:
            edge = YHI if v > 0 else YLO
            sgn = 1 if v > 0 else -1
            # the value is printed under the circle in the row; here only where it went (up off
            # the plot, or down under the lambda_1 label and out of the plot's floor)
            y0, y1 = ((py(YHI) - 34, py(YHI) + 4) if v > 0 else (PY0 + 1, PY0 - 22))
            o += (f"\\draw[{col},line width=4bp,-{{Stealth[length=13bp,width=12bp]}}] "
                  f"({px(LAM[k]):.1f},{y0:.1f}) -- ({px(LAM[k]):.1f},{y1:.1f});\n")
    o += tx(PX0 + 6, PY1 - 2, "$1/(1-\\alpha x)$", anchor="west")
    return o, wall


def katz_frame(frac, note):
    o = gauge(frac)
    p, wall = plot(frac)
    o += p
    # the row: (I - alpha A)^-1 = sum of three terms
    o += tx(KPOS["lhs"] + KLHS, KYMID, "$(I-\\alpha A)^{-1}=$", anchor="east")
    for k in SHOW:
        c = coef(frac, k)
        o += term(KPOS[KEY[k]], KYTOP, KSLOT[k], k, val(c), KC * np.sqrt(abs(c)), sgn_color(c),
                  side=KSIDE, dy_label=30)
    o += tx(KPOS["p1"] + 15, KYMID, "$+$") + tx(KPOS["dots"] + 8, KYMID, "$+\\;\\cdots\\;+$", anchor="west")
    # the note, left, under the gauge
    text, target, gap, bend = note(frac, wall)
    co_, b = F.callout(text, (20, 230), target, anchor="west", gap=gap, size=F.FONT, bend=bend)
    assert 6 <= b[0] and b[2] <= PX0 - 8, f"callout {text!r} runs into the plot {b}"
    assert b[1] > KYTOP + 8 and b[3] < GY - 58, f"callout {text!r} leaves its band {b}"
    return o + co_


def _n05(frac, wall):
    c = [coef(frac, k) for k in range(N)]
    assert max(c) / min(c) < 3 and wall > XHI, "alpha = 0.5: weights comparable, wall out of view"
    cx = KPOS["t0"] + KSLOT[0] / 2
    return "small \u03b1: weights comparable", (cx, KYMID), KC * np.sqrt(coef(frac, 0)) / 2 + 8, 0


def _n08(frac, wall):
    assert XLO < wall < XHI and wall > LAM[0], "alpha = 0.8: the wall is in view, right of lambda_1"
    assert 4 < coef(frac, 0) < YHI, "alpha = 0.8: lambda_1's weight 5, still on the plot"
    cx = KPOS["t0"] + KSLOT[0] / 2
    return "\u03bb\u2081 near 1/\u03b1: weight 5", (cx, KYMID), KC * np.sqrt(coef(frac, 0)) / 2 + 8, 0


def _n095(frac, wall):
    assert LAM[0] < wall < LAM[0] + 0.25 and coef(frac, 0) > YHI
    cx = KPOS["t0"] + KSLOT[0] / 2
    return "\u03bb\u2081 nearer 1/\u03b1: weight 20", (cx, KYMID), KC * np.sqrt(coef(frac, 0)) / 2 + 8, 0


def _n11(frac, wall):
    assert wall < LAM[0] and coef(frac, 0) < YLO
    cx = KPOS["t0"] + KSLOT[0] / 2
    return "past 1/\u03b1: weight \u221210", (cx, KYMID), KC * np.sqrt(-coef(frac, 0)) / 2 + 8, 0


KNOTES = {0.5: _n05, 0.8: _n08, 0.95: _n095, 1.1: _n11}


def f_katz():
    # facts: the first coefficient 2, 5, 20, then -10 past 1/lambda_1; only term 1 flips
    got = [coef(f, 0) for f in KFRACS]
    assert np.allclose(got, [2, 5, 20, -10]), got
    assert all(coef(f, k) > 0 for f in KFRACS for k in range(1, N)), "only term 1 flips"
    frames = [katz_frame(f, KNOTES[f]) for f in KFRACS]
    F.emit_frames("katz-why", frames, container="full", h=KH, nodes=False)


FIGURES = [
    ("decomp-sum", f_sum),
    ("decomp-orth", f_orth),
    ("decomp-square", f_square),
    ("decomp-power", f_power),
    ("katz-why", f_katz),
]
