#!/usr/bin/env python3
"""Module 06, power iteration from random starts: the figures of `figs_power` (v3 style).

    cd slides/m06/figures && python3 make_figures.py power-starts

The stage before this slide ("Power iteration", lecture-note/assets/anim/power-step.js) starts
from x_0 = 1 and plots one line per node: x = iteration t, y = that node's score. This figure
starts the same iteration from four random vectors and plots the same lines in four small
panels, so the room sees every run end on the same seven scores. Three runs end on +c; one ends
on -c, the same eigenvector with its sign flipped (A c = lambda c holds for -c too).

`power-starts` (col, `fig tall`), frames:

    00   panels 1-3 drawn (runs that end positive), panel 4 an empty frame
    01   panel 4 drawn (the run that ends all negative), with a grey note and arrow

Every number is computed here: x_0 is uniform in [-1, 1] from a fixed seed, x_{t+1} = A x_t divided
by its entry of largest absolute value (the vector keeps its sign), A = smallgraphs.EIG in
EIG_ORDER. The seeds are asserted: three runs end at +c (A at +1.00), one at -c (A at -1.00), and
c is the eigenvector of the largest eigenvalue scaled so its largest entry is 1.
"""

import numpy as np

import figlib as F
import smallgraphs as S
from figlib import FONT

NAMES = S.EIG_ORDER
A_MAT, EVALS, EVECS = S.spectrum(S.EIG, NAMES)
U1 = EVECS[:, -1]
C = U1 / U1[np.argmax(np.abs(U1))]                 # the eigenvector, largest entry 1 (all positive)

T_MAX = 20                                         # iterations drawn
SEEDS = [9, 13, 14, 29]                            # three end at +c, the last at -c
SIGNS = [+1, +1, +1, -1]


def run_from(seed, steps):
    """x_0 uniform in [-1, 1]; each step is A x divided by the entry of largest |value|."""
    x = np.random.default_rng(seed).uniform(-1, 1, len(NAMES))
    out = [x.copy()]
    for _ in range(steps):
        x = A_MAT @ x
        x = x / np.max(np.abs(x))
        out.append(x.copy())
    return np.array(out)                           # (steps + 1, 7)


RUNS = [run_from(s, T_MAX) for s in SEEDS]


def check():
    for seed, sign, tr in zip(SEEDS, SIGNS, RUNS):
        assert np.all(np.abs(tr[0]) <= 1)
        assert np.isclose(np.abs(tr[1:]).max(axis=1), 1).all()
        # what is drawn (t = 20) is already on the eigenvector to within a line width
        assert np.abs(tr[-1] - sign * C).max() < 0.01, (seed, np.abs(tr[-1] - sign * C).max())
        # and the iteration really converges: 120 steps agree to 1e-6
        far = run_from(seed, 120)[-1]
        assert np.abs(far - sign * C).max() < 1e-6, (seed, np.abs(far - sign * C).max())
        assert np.sign(far[0]) == sign and abs(far[0]) > 1 - 1e-6        # A is at +1.00 or -1.00
    assert [int(np.sign(r[-1][0])) for r in RUNS] == SIGNS
    assert SIGNS.count(-1) == 1
    # why: the sign is the sign of x_0's component along u_1
    for seed, sign in zip(SEEDS, SIGNS):
        x0 = np.random.default_rng(seed).uniform(-1, 1, len(NAMES))
        assert np.sign(x0 @ U1) * np.sign(U1[0]) == sign
    return True


# --------------------------------------------------------------------------- geometry (bp, y up)
PLOT_H = 104
YLIM = 1.15                                        # the spines sit a little outside +-1
ROW_TOP = [398, 398 - PLOT_H - 72]                 # top of the plot of row 1, row 2
COL_X = [98, 334]                                  # left of the plot of column 1, column 2
PLOT_W = 172


def X(c, t):
    return COL_X[c] + PLOT_W * t / T_MAX


def Y(r, v):
    return ROW_TOP[r] - PLOT_H * (YLIM - v) / (2 * YLIM)


def panel(r, c, tr, color, label_nodes=()):
    """The axes of one panel and, if tr is given, its seven lines."""
    o = ""
    x0, x1 = COL_X[c], COL_X[c] + PLOT_W
    o += F.seg((x0, Y(r, 0)), (x1, Y(r, 0)), color="pale", w=2.0, sketch=False)      # the zero line
    o += F.seg((x0, Y(r, -YLIM)), (x1, Y(r, -YLIM)), color="muted", w=2.2)
    o += F.seg((x0, Y(r, -YLIM)), (x0, Y(r, YLIM)), color="muted", w=2.2)
    for v in (-1, 0, 1):
        o += F.seg((x0 - 8, Y(r, v)), (x0, Y(r, v)), color="muted", w=2.2, sketch=False)
        if c == 0:
            s = {-1: "$-$1", 0: "0", 1: "1"}[v] if False else {-1: "−1", 0: "0", 1: "1"}[v]
            o += F.text(x0 - 14, Y(r, v), s, color="muted", anchor="east")
    if r == 1:
        for t in (0, 10, 20):
            o += F.seg((X(c, t), Y(r, -YLIM)), (X(c, t), Y(r, -YLIM) - 8), color="muted", w=2.2, sketch=False)
            o += F.text(X(c, t), Y(r, -YLIM) - 14, str(t), color="muted", anchor="north")
    if tr is None:
        return o
    for i in range(len(NAMES)):
        pts = [(X(c, t), Y(r, tr[t][i])) for t in range(T_MAX + 1)]
        o += F.polyline(pts, color=color, w=2.6).replace(
            f"draw={color}", f"draw={color},opacity=0.6,line join=round,line cap=round")
        o += f"\\fill[{color},opacity=0.85] ({pts[-1][0]:.1f},{pts[-1][1]:.1f}) circle (3.2bp);\n"
    for i in label_nodes:
        o += F.text(X(c, T_MAX) + 12, Y(r, tr[-1][i]), NAMES[i], color="ink", anchor="west")
    return o


def axis_titles():
    o = F.text(18, (ROW_TOP[0] + Y(1, -YLIM)) / 2, "score", color="muted", anchor="center", rot=90)
    o += F.text((COL_X[0] + COL_X[1] + PLOT_W) / 2, Y(1, -YLIM) - 56, "iteration t", color="muted",
                anchor="north")
    return o


def start_label(r, c, k, tr, upper=False):
    """A muted "start k" inside panel (r, c), in the half of the panel the lines never reach (from t = 2):
    below the lines for the runs that end positive, above them for the run that ends negative.
    Asserts that no line of the run passes through the word."""
    t0 = 2
    s = f"start {k}"
    x, v = X(c, t0), (0.55 if upper else -0.58)
    y = Y(r, v)
    w = F.CHAR_W * FONT * len(s)
    box = (x - 1, y - 15, x + w + 1, y + 16)
    for t in range(T_MAX):
        for i in range(len(NAMES)):
            p0, p1 = (X(c, t), Y(r, tr[t][i])), (X(c, t + 1), Y(r, tr[t + 1][i]))
            assert not F.box_hits_segment(box, p0, p1, pad=2), f"{s}: a line of the run passes through it"
    return F.text(x, y, s, color="muted", anchor="west"), box


def f_starts():
    check()
    A_IDX, C_IDX = NAMES.index("A"), NAMES.index("C")
    base = axis_titles()
    labs = [start_label(0, 0, 1, RUNS[0]), start_label(0, 1, 2, RUNS[1]),
            start_label(1, 0, 3, RUNS[2]), start_label(1, 1, 4, RUNS[3], upper=True)]
    base += "".join(t for t, _ in labs)
    pos = (panel(0, 0, RUNS[0], "ink", label_nodes=(A_IDX, C_IDX))
           + panel(0, 1, RUNS[1], "ink")
           + panel(1, 0, RUNS[2], "ink"))
    frame0 = base + pos + panel(1, 1, None, "ink")
    # the note sits in the gap between the rows, above panel 4, and points down into its lines
    tr = RUNS[3]
    # the arrow comes down at the right end of the panel, clear of the label "start 4" (which ends at t = 17)
    target = (X(1, 19), Y(1, tr[19][NAMES.index("E")]))
    at = (COL_X[1] + PLOT_W + 18, Y(0, -YLIM) - 12)
    bx = F.label_box(at[0], at[1], "all negative:\\\\flip the sign", "north east", pad=2)
    note, box = F.callout("all negative:\\\\flip the sign", at, target, anchor="north east", gap=10,
                          tip=(target[0], bx[1] - 4))
    assert target[0] > labs[3][1][2] + 12, "the arrow of the note runs through the label of panel 4"
    assert not F.boxes_overlap(box, labs[3][1]), "the note covers the label of panel 4"
    frame1 = base + pos + panel(1, 1, tr, "hot") + note
    F.emit_frames("power-starts", [frame0, frame1], container="col", h=420, hmod="tall", nodes=False)
    d = F.FRAMES / "power-starts"
    if d.is_dir():
        (d / "steps.txt").write_text("the fourth start ends on the same scores with every sign flipped\n")


FIGURES = [("power-starts", f_starts)]
