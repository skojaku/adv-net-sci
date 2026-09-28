#!/usr/bin/env python3
"""The worked histogram example that Part Five opens with.

Twenty degrees, small enough to count on the slide, carried through five figures:
a frequency table, bars of width one, bars of unequal width, the area fix, and the
running total.  The sixth figure in the sequence is `ccdf-def` in `figs_tail.py`,
which cuts the SAME twenty degrees from the top -- so the example that teaches how a
distribution is drawn is the example the CCDF is then defined on, and the room never
has to re-learn a data set.

`TOY` is `figs_tail.CCDF_DEMO`; the import is one-way so the two files cannot drift.
"""

import numpy as np

from figlib import (Axes, emit, fill_poly, rect, seg, text)
from figs_tail import CCDF_DEMO as TOY

H = 380

COUNT = "accent"          # the quantity every panel is counting
FIX = "accenttwo"         # what THIS figure is about

# k = 1..7 with counts 7, 5, 3, 2, 1, 1, 1.  Written out so the drawing and the table
# cannot disagree, and asserted against the degree list itself.
KS = tuple(range(1, max(TOY) + 1))
CNT = tuple(TOY.count(k) for k in KS)
assert sum(CNT) == len(TOY) == 20, (CNT, len(TOY))
assert CNT == (7, 5, 3, 2, 1, 1, 1), CNT

# The three unequal bins the "area, not height" pair is built on: [1,1], [2,3], [4,7].
BINS = ((1, 1), (2, 3), (4, 7))
BIN_W = tuple(hi - lo + 1 for lo, hi in BINS)
BIN_N = tuple(sum(c for k, c in zip(KS, CNT) if lo <= k <= hi) for lo, hi in BINS)
assert BIN_W == (1, 2, 4) and BIN_N == (7, 8, 5) and sum(BIN_N) == 20, (BIN_W, BIN_N)
# Height as a count makes the four-degree-wide bin look like the one-degree-wide one;
# height as a density does not.  If that ever stops being true the pair has no point.
assert BIN_N[2] / BIN_N[0] > 0.6, BIN_N
assert (BIN_N[2] / BIN_W[2]) / (BIN_N[0] / BIN_W[0]) < 0.25, BIN_N


def bar(ax, lo, hi, h, color=COUNT, opacity=0.30, what=None):
    """One histogram bar spanning [lo, hi] in data units, filled and outlined."""
    x0, x1 = ax.X(lo), ax.X(hi)
    y0, y1 = ax.Y(0), ax.Y(h)
    pts = ((x0, y0), (x1, y0), (x1, y1), (x0, y1))
    o = fill_poly(pts, color=color, opacity=opacity, record=False)
    o += rect(x0, y0, x1, y1, color=color, w=2.6, what=what or "a bar")
    return o


def _count_axes(box, ymax=8, yticks=(0, 2, 4, 6, 8)):
    return Axes(box, (0.5, 7.5), (0, ymax),
                xticks=list(KS), yticks=list(yticks))


# --------------------------------------------------------------- 1. the raw material
def fig_hist_degrees():
    """Twenty degrees, and the count of how often each one occurs.

    The reference deck opens its histogram lesson on a frequency table alone.  Here the
    table is not given: the degree list is, and the table is what the room produces from
    it, so the first thing on the board is the raw data rather than a summary of it.
    """
    ks = sorted(TOY, reverse=True)
    assert len(ks) == 20

    b = text(58, 302, "degree of\\\\each node", color="annot", anchor="west")
    x0, pitch = 300, 38.0
    for i, k in enumerate(ks):
        b += text(x0 + i * pitch, 302, str(k), anchor="center")

    # The arrow says the table is derived, not a second data set.
    b += seg((540, 258), (540, 212), color=FIX, w=3.0, arrow="-{Latex[length=10bp]}")
    b += text(556, 235, "count them", color=FIX, anchor="west")

    # Two rows, laid out on the same pitch the bars will use, so the table reads onto
    # the x axis of the next figure without being re-sorted.
    tx, tp = 330, 92.0
    row_k, row_n = 148, 82
    b += text(tx - 118, row_k, "degree $k$", color="annot", anchor="east")
    b += text(tx - 118, row_n, "nodes", color="annot", anchor="east")
    b += seg((tx - 108, row_k + 34), (tx + 6 * tp + 46, row_k + 34), color="annot", w=2.2)
    b += seg((tx - 108, row_k - 26), (tx + 6 * tp + 46, row_k - 26), color="annot", w=2.2)
    for i, (k, c) in enumerate(zip(KS, CNT)):
        b += text(tx + i * tp, row_k, str(k), anchor="center")
        b += text(tx + i * tp, row_n, str(c), color=COUNT, anchor="center")
    emit("hist-degrees", b, container="full", h=H)


# --------------------------------------------------------------- 2. bars of width one
def fig_hist_bars():
    """One bar per degree, and the bars touch.

    A gap between two bars would say there is something between k = 3 and k = 4, and on
    a degree axis there is not.  That is the whole content of the reference deck's "No
    gaps!" slide, and it is the reason a histogram is not a bar chart.
    """
    ax = _count_axes((250, 120, 1000, 330))
    b = ax.frame()
    b += text((ax.x0 + ax.x1) / 2, ax.y0 - 66, "degree $k$", anchor="north")
    b += text(ax.x0 - 108, (ax.y0 + ax.y1) / 2, "nodes", rot=90)
    for k, c in zip(KS, CNT):
        b += bar(ax, k - 0.5, k + 0.5, c, what=f"the k={k} bar")

    # The one edge the point is about, marked where it happens.
    # The arrow lands ON the shared edge. Drawn as a free-floating tick above the bars
    # it read as an annotation about the empty space, which is the opposite of the point.
    xe = ax.X(3.5)
    b += seg((xe, ax.Y(5.2)), (xe, ax.Y(2.3)), color=FIX, w=3.4,
             arrow="-{Latex[length=11bp]}")
    b += text(xe + 18, ax.Y(5.4), "no gap here", color=FIX, anchor="west")
    b += text(ax.x1, 372, f"{sum(CNT)} nodes in {len(KS)} bins of width 1",
              color="annot", anchor="north east")
    emit("hist-bars", b, container="full", h=H)


# --------------------------------------------------------------- 3. unequal bins
def fig_hist_rebin():
    """The same twenty nodes in three bins, drawn the obvious and wrong way.

    Nothing about the data changed; only the bin edges did.  Drawn with the count as the
    height the four-degree bin stands nearly as tall as the one-degree bin, which reads
    as "k = 4...7 is about as common as k = 1" -- and it is not.
    """
    ax = _count_axes((250, 120, 1000, 300), ymax=10, yticks=(0, 5, 10))
    b = ax.frame()
    b += text((ax.x0 + ax.x1) / 2, ax.y0 - 66, "degree $k$", anchor="north")
    b += text(ax.x0 - 108, (ax.y0 + ax.y1) / 2, "nodes", rot=90)
    # The count goes INSIDE its bar: "height = count" is the reading the next figure
    # breaks, so the drawing has to say that is what the height is.
    for (lo, hi), n, w in zip(BINS, BIN_N, BIN_W):
        b += bar(ax, lo - 0.5, hi + 0.5, n, what=f"the {lo}-{hi} bar")
        b += text((ax.X(lo - 0.5) + ax.X(hi + 0.5)) / 2, ax.Y(n / 2), str(n),
                  color=COUNT, anchor="center", record=False)
    b += text(ax.x1, 372, "same 20 nodes; bin widths 1, 2, 4", color=FIX,
              anchor="north east")
    emit("hist-rebin", b, container="full", h=H)


# --------------------------------------------------------------- 4. area, not height
def fig_hist_area():
    """Divide each count by its bin width and the bar's AREA carries the count.

    Two panels, same bins, same twenty nodes: on the left the height is the count and
    the widest bin is inflated by its own width; on the right the height is the count
    per unit of k, and what you read off the drawing is area.
    """
    left = Axes((180, 140, 520, 300), (0.5, 7.5), (0, 8),
                xticks=[1, 4, 7], yticks=[0, 4, 8])
    right = Axes((700, 140, 1040, 300), (0.5, 7.5), (0, 8),
                 xticks=[1, 4, 7], yticks=[0, 4, 8])
    assert (left.x1 - left.x0) == (right.x1 - right.x0)
    assert left.ylim == right.ylim

    b = left.frame() + right.frame()
    for ax, heights, col in ((left, BIN_N, COUNT),
                             (right, [n / w for n, w in zip(BIN_N, BIN_W)], FIX)):
        for (lo, hi), h in zip(BINS, heights):
            b += bar(ax, lo - 0.5, hi + 0.5, h, color=col, what="a bar")
        b += text((ax.x0 + ax.x1) / 2, ax.y0 - 62, "degree $k$", anchor="north")

    b += text(left.x0 - 96, (left.y0 + left.y1) / 2, "nodes", rot=90)
    b += text(right.x0 - 96, (right.y0 + right.y1) / 2, "nodes per $k$", rot=90)
    b += text((left.x0 + left.x1) / 2, 372, "height $=$ count", anchor="north")
    b += text((right.x0 + right.x1) / 2, 372, "height $=$ count $\\div$ width",
              color=FIX, anchor="north")

    # Every bar on the right encloses the count it came from; that is the claim, so it
    # is asserted rather than described.
    for (lo, hi), n, w in zip(BINS, BIN_N, BIN_W):
        assert abs((n / w) * w - n) < 1e-9
    emit("hist-area", b, container="full", h=H)


# --------------------------------------------------------------- 5. the running total
def fig_hist_cumulative():
    """Count upward instead of within: each bar is everybody at this degree or below.

    The last bar is all twenty nodes by construction, which is what makes the right
    panel readable as a fraction -- and a fraction of nodes below k is one subtraction
    away from the fraction above it, which is the CCDF the next figure cuts.
    """
    run = np.cumsum(CNT)
    assert run[-1] == 20 and list(run) == [7, 12, 15, 17, 18, 19, 20], list(run)

    left = Axes((180, 140, 520, 300), (0.5, 7.5), (0, 8), xticks=[1, 4, 7],
                yticks=[0, 4, 8])
    # The right panel is drawn in counts and labelled as a share: twenty nodes IS one,
    # and that identity is the whole reason a cumulative count can be read as a CDF.
    right = Axes((680, 140, 1020, 300), (0.5, 7.5), (0, 20), xticks=[1, 4, 7],
                 yticks=[0, 10, 20],
                 yfmt=lambda v: {0: "0", 10: "0.5", 20: "1"}[int(v)])
    b = left.frame() + right.frame()
    for k, c in zip(KS, CNT):
        b += bar(left, k - 0.5, k + 0.5, c, what="a bar")
    for k, c in zip(KS, run):
        b += bar(right, k - 0.5, k + 0.5, int(c), color=FIX, what="a bar")

    for ax in (left, right):
        b += text((ax.x0 + ax.x1) / 2, ax.y0 - 62, "degree $k$", anchor="north")
    b += text(left.x0 - 96, (left.y0 + left.y1) / 2, "nodes", rot=90)
    b += text(right.x0 - 112, (right.y0 + right.y1) / 2, "$P(k' \\le k)$", rot=90)
    b += text((left.x0 + left.x1) / 2, 372, "counted at $k$", anchor="north")
    b += text((right.x0 + right.x1) / 2, 372, "counted at $k$ or below",
              color=FIX, anchor="north")

    emit("hist-cumulative", b, container="full", h=H)


FIGURES = [
    ("hist-degrees", fig_hist_degrees),
    ("hist-bars", fig_hist_bars),
    ("hist-rebin", fig_hist_rebin),
    ("hist-area", fig_hist_area),
    ("hist-cumulative", fig_hist_cumulative),
]
