#!/usr/bin/env python3
"""Parts 4-6: modularity from the balls-and-strings game, Louvain, and the SBM.

The worksheet graph -- two triangles joined by one friendship -- runs through this whole
stretch. It is the graph the room computes Q on by hand, so every quantity it carries is
a small integer and the answer is an exact fraction: m = 7, observed 6/7, expected 1/2,
Q = 5/14. Reusing it means the algebra on slide 49 is about a picture the room already
has in its hands.
"""

from fractions import Fraction

import networkx as nx
import numpy as np

import verify_numbers as V
from figlib import Axes, FONT, disc, dot, emit, polyline, seg, text
from kfig import (
    CHI, COFF, arrow, bag, cell_grid, number_line, ring_positions, small, string,
)

FIGURES = []


def fig(name, container="full", h=380, hmod=""):
    def deco(fn):
        FIGURES.append((name, lambda: emit(name, fn(), container=container, h=h, hmod=hmod)))
        return fn
    return deco


# The worksheet: two triangles joined by one friendship.  Positions once, used by six
# figures, so the room never has to re-find the same six people.
WS_POS = {1: (120, 300), 2: (120, 116), 3: (300, 208),
          4: (780, 208), 5: (960, 300), 6: (960, 116)}
WS_E = [(1, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 6), (3, 4)]
WS_LEFT, WS_RIGHT = {1, 2, 3}, {4, 5, 6}


def _ws(**kw):
    kw.setdefault("what", "worksheet")
    kw.setdefault("fill", {n: (CHI if n in WS_LEFT else COFF) for n in WS_POS})
    return small(dict(WS_POS), list(WS_E), **kw)


# =========================================================================== Part 4
@fig("chance-idea", h=360)
def _chance():
    """Two networks, the same two friendships crossing -- only one of them surprising."""
    def block(x0, dense):
        p = {0: (x0, 296), 1: (x0 + 150, 296), 2: (x0 + 75, 202), 3: (x0, 108),
             4: (x0 + 150, 108), 5: (x0 + 300, 296), 6: (x0 + 450, 296),
             7: (x0 + 375, 202), 8: (x0 + 300, 108), 9: (x0 + 450, 108)}
        e = [(0, 2), (1, 2), (2, 3), (2, 4), (5, 7), (6, 7), (7, 8), (7, 9),
             (2, 7), (4, 8)]
        if dense:
            e += [(0, 1), (3, 4), (0, 3), (5, 6), (8, 9), (6, 9)]
        return p, e
    out = ""
    cuts = []
    for x0, dense in ((30, True), (550, False)):
        p, e = block(x0, dense)
        cuts.append(sum(1 for a, b in e if (a < 5) != (b < 5)))
        out += small(p, e, node=34, what=f"chance-idea-{x0}",
                     heavy=[(2, 7), (4, 8)], heavy_color="black",
                     fill={n: (CHI if n < 5 else COFF) for n in p})
    assert cuts[0] == cuts[1] == 2, cuts
    return out


@fig("observed", h=340)
def _observed():
    """Pull a string; how often do the two ends match?"""
    g = nx.Graph(WS_E)
    match = [e for e in WS_E if (e[0] in WS_LEFT) == (e[1] in WS_LEFT)]
    assert len(match) == 6 and g.number_of_edges() == 7
    out = ""
    for i, (a, b) in enumerate(WS_E):
        x = 90 + i * 138
        same = (a in WS_LEFT) == (b in WS_LEFT)
        ca = CHI if a in WS_LEFT else COFF
        cb = CHI if b in WS_LEFT else COFF
        out += string((x - 44, 268), (x + 44, 268),
                      color="accenttwo" if same else "annot", w=4.6 if same else 2.6)
        out += disc(x - 44, 268, fill="accent" if ca == CHI else "accenttwo", size=40)
        out += disc(x + 44, 268, fill="accent" if cb == CHI else "accenttwo", size=40)
        out += text(x, 150, "match" if same else "no", color="accenttwo" if same else "annot",
                    anchor="north", size=FONT)
    out += text(540, 78, f"{len(match)} of {g.number_of_edges()} strings match",
                color="black", anchor="north", size=44)
    return out


@fig("bag-2m", h=360)
def _bag():
    """Cut every string and the bag holds two balls per friendship.

    A member with three friends puts three balls in, which is the whole reason a degree
    shows up in the null model at all.
    """
    g = nx.Graph(WS_E)
    m = g.number_of_edges()
    donors = {n: g.degree(n) for n in WS_POS}
    assert sum(donors.values()) == 2 * m == 14
    pos = {n: (x * 0.36 + 30, y * 0.74 + 62) for n, (x, y) in WS_POS.items()}
    out = small(pos, list(WS_E), what="bag-2m", node=32,
                fill={n: (CHI if n in WS_LEFT else COFF) for n in pos})
    out += arrow((420, 200), (516, 200), color="annot", w=4.0)
    out += bag(800, 190, 460, 300)
    rng = np.random.default_rng(11)
    slots = [(600 + (i % 5) * 100 + rng.uniform(-10, 10),
              100 + (i // 5) * 86 + rng.uniform(-8, 8)) for i in range(14)]
    order = [n for n in sorted(WS_POS) for _ in range(donors[n])]
    for (x, y), n in zip(slots, order):
        out += disc(x, y, fill=CHI if n in WS_LEFT else COFF, size=42)
    return out


@fig("expected", h=360)
def _expected():
    """Draw two balls out of the bag; how often do those match?"""
    g = nx.Graph(WS_E)
    m = g.number_of_edges()
    dl = sum(g.degree(n) for n in WS_LEFT)
    dr = sum(g.degree(n) for n in WS_RIGHT)
    assert dl + dr == 2 * m and dl == dr == 7
    out = bag(300, 200, 400, 300)
    rng = np.random.default_rng(4)
    xs = rng.uniform(140, 460, 14)
    ys = rng.uniform(90, 268, 14)
    for i, (x, y) in enumerate(zip(sorted(xs), ys)):
        out += disc(x, y, fill="accent" if i < dl else "accenttwo", size=40)
    out += arrow((520, 200), (640, 200), color="annot", w=4.0)
    out += disc(730, 244, fill="accent", size=52)
    out += disc(730, 152, fill="accenttwo", size=52)
    out += text(880, 200, f"{dl} of {2 * m}\\\\each colour", color="black",
                anchor="center", size=FONT)
    return out


@fig("modularity-gap", h=280)
def _gap():
    """Observed minus expected, on one axis, with the gap named."""
    g = nx.Graph(WS_E)
    m = g.number_of_edges()
    obs = Fraction(sum(1 for a, b in WS_E if (a in WS_LEFT) == (b in WS_LEFT)), m)
    exp = sum(Fraction(sum(g.degree(n) for n in c), 2 * m) ** 2
              for c in (WS_LEFT, WS_RIGHT))
    q = obs - exp
    assert q == Fraction(5, 14), q
    out = number_line(140, 980, 150, 0.0, 1.0,
                      [(float(exp), "by chance", "annot", "down"),
                       (float(obs), "actually", "accent", "up")])
    x0 = 140 + float(exp) * 840
    x1 = 140 + float(obs) * 840
    out += seg((x0, 218), (x1, 218), color="accenttwo", w=6.0)
    out += text((x0 + x1) / 2, 234, f"Q = {q.numerator}/{q.denominator}",
                color="accenttwo", anchor="south", size=44)
    return out


@fig("modularity-matrix", h=250)
def _matrix():
    """One pair of members: what the network did, against what chance would have done."""
    g = nx.Graph(WS_E)
    m = g.number_of_edges()
    i, j = 1, 2
    assert g.has_edge(i, j)
    ki, kj = g.degree(i), g.degree(j)
    cell = 33
    order = [1, 2, 3, 4, 5, 6]
    filled = {(r, c) for r, a in enumerate(order) for c, b in enumerate(order)
              if g.has_edge(a, b)}
    out = cell_grid(130, 236, 6, cell, filled, fill_color="accent")
    out += text(130 + 3 * cell, 34, "who is joined to whom", color="annot",
                anchor="north", size=FONT)
    out += arrow((400, 138), (496, 138), color="annot", w=4.0)
    out += text(780, 184, "this pair: 1", color="accent", anchor="center", size=44)
    out += text(780, 92, f"by chance: {ki}x{kj}/{2 * m}", color="annot",
                anchor="center", size=44)
    return out


@fig("configuration-model", h=340)
def _config():
    """Rewire every friendship at random and keep every count -- that is the baseline."""
    g = nx.Graph(WS_E)
    alt = [(1, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 6), (3, 4)]
    h = nx.Graph(alt)
    h.add_nodes_from(g)
    assert sorted(d for _, d in g.degree()) == sorted(d for _, d in h.degree()), \
        "the rewiring must preserve every degree -- that is the whole null model"
    left = {n: (x * 0.44 + 24, y * 0.80 + 40) for n, (x, y) in WS_POS.items()}
    right = {n: (x * 0.44 + 610, y * 0.80 + 40) for n, (x, y) in WS_POS.items()}
    out = small(left, list(WS_E), node=34, what="config-before",
                fill={n: "accent" for n in left})
    out += small(right, alt, node=34, what="config-after", planar=False,
                 fill={n: "annot" for n in right})
    out += arrow((490, 206), (586, 206), color="annot", w=4.0)
    return out


@fig("worksheet-q", h=360)
def _wsq():
    """The graph the room scores by hand.  It carries no score.

    Asserted, not trusted: nothing in this figure is a value of Q. It sits on the
    activity slide and the answer is the slide after it.
    """
    g = nx.Graph(WS_E)
    body = _ws(labels={n: str(g.degree(n)) for n in WS_POS})
    for token in ("5/14", "0.357", "Q ="):
        assert token not in body, f"{token!r} leaks the answer onto the question slide"
    return body


@fig("worksheet-q-answer", h=360)
def _wsqa():
    """Five fourteenths -- and what the two rival groupings score."""
    w = V.worksheet_Q()
    assert w["right"] == Fraction(5, 14) and w["one_group"] == 0.0
    out = _ws()
    out += text(540, 336, f"{w['right'].numerator}/{w['right'].denominator}",
                color="accenttwo", anchor="north", size=56)
    out += text(540, 92, "one big group: 0", color="annot", anchor="north", size=FONT)
    return out


@fig("q-picks-k", h=360)
def _qk():
    """Q compares groupings that do not even have the same number of groups."""
    g = nx.Graph()
    blocks = [list(range(0, 4)), list(range(4, 8)), list(range(8, 12))]
    for b in blocks:
        g.add_edges_from([(b[0], b[1]), (b[0], b[2]), (b[1], b[2]), (b[1], b[3]),
                          (b[2], b[3])])
    g.add_edges_from([(3, 4), (7, 8)])
    best = {}
    for k in range(1, 6):
        cand = []
        if k == 1:
            cand = [[list(g)]]
        elif k == 2:
            cand = [[blocks[0], blocks[1] + blocks[2]], [blocks[0] + blocks[1], blocks[2]]]
        elif k == 3:
            cand = [blocks]
        elif k == 4:
            cand = [[blocks[0][:2], blocks[0][2:], blocks[1], blocks[2]]]
        else:
            cand = [[blocks[0][:2], blocks[0][2:], blocks[1][:2], blocks[1][2:], blocks[2]]]
        best[k] = max(V.unweighted_Q(g, c) for c in cand)
    peak = max(best, key=best.get)
    assert peak == 3, (peak, best)
    pos = {}
    for bi, b in enumerate(blocks):
        cx = 150 + bi * 200
        for ni, n in enumerate(b):
            pos[n] = (cx + [-64, 0, 0, 64][ni], [206, 300, 112, 206][ni])
    cols = ["accent", "accenttwo", "accentthree"]
    out = small(pos, list(g.edges()), node=32, what="q-picks-k",
                fill={n: cols[n // 4] for n in pos})
    ax = Axes((690, 116, 1010, 296), (1, 5), (0, max(best.values()) * 1.25),
              xlabel="number of groups", xticks=[1, 2, 3, 4, 5],
              yticks=[0, round(max(best.values()), 2)])
    out += ax.frame()
    for k, q in best.items():
        out += dot(*ax.P(k, q), color="accenttwo" if k == peak else "annot", d=17)
    return out


# =========================================================================== Part 5
@fig("bell-growth", h=330)
def _bell():
    """Every way of grouping n people -- there is no searching this."""
    f = V.facts()
    ns = list(range(2, 35))
    ys = [V.bell(n) for n in ns]
    assert ys[-1] == f["bell"][34]
    ax = Axes((196, 116, 1016, 286), (2, 34), (1, 1e29), ylog=True,
              xlabel="people", xticks=[2, 10, 20, 34],
              yticks=[1, 1e7, 1e14, 1e21, 1e28])
    out = ax.frame()
    out += ax.line(ns, ys, color="accent", w=4.4)
    out += dot(*ax.P(34, ys[-1]), color="accenttwo", d=18)
    return out


@fig("leiden-fix", h=340)
def _leiden():
    """Louvain can hand back a group that is not joined up inside."""
    p = {0: (60, 290), 1: (60, 120), 2: (210, 205), 3: (420, 290), 4: (420, 120),
         5: (620, 205), 6: (830, 290), 7: (830, 120), 8: (990, 205)}
    e = [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5),
         (5, 6), (5, 7), (6, 7), (6, 8), (7, 8)]
    group = {0, 1, 2, 6, 7, 8}
    g = nx.Graph(e)
    assert not nx.is_connected(g.subgraph(group)), \
        "the drawn group must genuinely fall into two pieces"
    return small(p, e, node=36, what="leiden-fix",
                 fill={n: ("accenttwo" if n in group else "annot") for n in p})


@fig("four-answers", h=360)
def _four():
    """Five methods, five different things meant by the word 'community'."""
    p = ring_positions(6, 540, 200, 116, 92, start=90)
    e = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3)]
    out = small(p, e, node=34, what="four-answers", planar=False,
                fill={n: "accent" for n in p})
    spokes = [((150, 330), "cheap to cut"), ((150, 70), "more than chance"),
              ((930, 330), "traps a walker"), ((930, 70), "generates it")]
    for (x, y), lab in spokes:
        sx = 400 if x < 540 else 680
        out += arrow((sx, 200 + (60 if y > 200 else -60)),
                     (x + (110 if x < 540 else -110), y), color="annot", w=3.4)
        out += text(x, y, lab, color="accenttwo",
                    anchor="center", size=FONT)
    return out


# =========================================================================== Part 6
def _sbm_graph(n_per=5, p_in=0.85, p_out=0.12, seed=2):
    rng = np.random.default_rng(seed)
    n = 2 * n_per
    e = []
    for a in range(n):
        for b in range(a + 1, n):
            same = (a < n_per) == (b < n_per)
            if rng.random() < (p_in if same else p_out):
                e.append((a, b))
    return e


@fig("sbm-flip", h=340)
def _flip():
    """Groups first, then the odds, then the network -- the arrow runs the other way."""
    out = ""
    for i, (cx, col) in enumerate(((110, "accent"), (110, "accenttwo"))):
        for j in range(3):
            out += disc(cx + j * 62, 268 - i * 132, fill=col, size=44)
    out += arrow((320, 200), (410, 200), color="annot", w=4.0)
    out += cell_grid(456, 262, 2, 62, {(0, 0), (1, 1)}, fill_color="accentthree")
    out += arrow((640, 200), (730, 200), color="annot", w=4.0)
    p = ring_positions(6, 900, 200, 128, 104, start=90)
    e = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 2)]
    out += small(p, e, node=34, what="sbm-flip", planar=False,
                 fill={n: ("accent" if n < 3 else "accenttwo") for n in p})
    return out


def _sorted_matrix(e, n, order):
    idx = {v: i for i, v in enumerate(order)}
    return {(idx[a], idx[b]) for a, b in e} | {(idx[b], idx[a]) for a, b in e}


def _sbm_ring(e, coloured=True, node=32, cx=270, cy=196, rx=230, ry=150):
    """The ten members on an ellipse, group by group.

    An ellipse is strictly convex, so no chord can pass through a disc -- which is what
    two rows of five did, every edge that skipped a neighbour running straight over it.
    """
    pos = ring_positions(10, cx, cy, rx, ry, start=108)
    fill = ({n: (CHI if n < 5 else COFF) for n in pos} if coloured
            else {n: "annot" for n in pos})
    return small(pos, e, node=node, what="sbm-ring", planar=False, fill=fill)


@fig("sbm-blocks", h=380)
def _blocks():
    """Sort the members by group and the picture arranges itself into blocks."""
    e = _sbm_graph()
    filled = _sorted_matrix(e, 10, list(range(10)))
    inside = sum(1 for a, b in e if (a < 5) == (b < 5))
    assert inside > len(e) - inside, "the diagonal blocks must be the dense ones"
    cell = 33
    out = _sbm_ring(e)
    out += cell_grid(636, 362, 10, cell, filled, fill_color="accent")
    out += cell_grid(636, 362, 10, cell, set(), empty="none",
                     diag=[(0, 5, "accenttwo"), (5, 10, "accenttwo")])
    return out


@fig("block-matrix", h=340)
def _blockmat():
    """One small matrix is the entire model."""
    cell = 120
    out = cell_grid(420, 300, 2, cell, {(0, 0), (1, 1)}, fill_color="accentthree")
    out += text(420 + cell / 2, 300 - cell / 2, "high", color="black",
                anchor="center", size=44)
    out += text(420 + cell * 1.5, 300 - cell * 1.5, "high", color="black",
                anchor="center", size=44)
    out += text(420 + cell * 1.5, 300 - cell / 2, "low", color="annot",
                anchor="center", size=44)
    out += text(420 + cell / 2, 300 - cell * 1.5, "low", color="annot",
                anchor="center", size=44)
    out += text(140, 240, "same\\\\group", color="accent", anchor="center", size=FONT)
    out += text(940, 240, "different\\\\group", color="accenttwo", anchor="center",
                size=FONT)
    return out


@fig("sbm-three-cases", h=380)
def _three():
    """Inside more likely, outside more likely, no difference at all."""
    cases = [("inside more likely", 0.90, 0.08, {(0, 0), (1, 1)}),
             ("outside more likely", 0.08, 0.90, {(0, 1), (1, 0)}),
             ("no difference", 0.45, 0.45, {(0, 0), (0, 1), (1, 0), (1, 1)})]
    out = ""
    for i, (lab, pin, pout, hot) in enumerate(cases):
        x0 = 40 + i * 350
        out += cell_grid(x0 + 98, 364, 2, 52, hot, fill_color="accentthree")
        out += text(x0 + 150, 250, lab, color="accenttwo", anchor="north", size=FONT)
        e = _sbm_graph(4, pin, pout, seed=7 + i)
        # Eight members on an ellipse, first group then second, so no chord can run over
        # a disc; two rows of four put every skipping edge straight through a neighbour.
        p = ring_positions(8, x0 + 150, 92, 138, 66, start=112)
        inside = sum(1 for a, b in e if (a < 4) == (b < 4))
        outside = len(e) - inside
        assert (inside > outside) == (pin > pout), (lab, inside, outside)
        out += small(p, e, node=28, what=f"sbm-case-{i}", planar=False,
                     fill={k: ("accent" if k < 4 else "accenttwo") for k in p})
    return out


@fig("sbm-pattern", h=340)
def _pattern():
    """Two groups whose members share no friendship at all -- and are still groups."""
    top = list(range(4))
    bot = list(range(4, 8))
    p = {**{n: (126 + n * 276, 300) for n in top},
         **{n: (126 + (n - 4) * 276, 110) for n in bot}}
    e = [(a, b) for a in top for b in bot if (a + b) % 3 != 2]
    g = nx.Graph(e)
    assert g.subgraph(top).number_of_edges() == 0
    assert g.subgraph(bot).number_of_edges() == 0
    return small(p, e, node=36, what="sbm-pattern", planar=False,
                 fill={n: ("accent" if n in top else "accenttwo") for n in p})


@fig("sbm-inference", h=330)
def _inference():
    """Pick the grouping that makes the network you actually saw most likely."""
    e = _sbm_graph(4, 0.9, 0.1, seed=5)
    g = nx.Graph(e)
    g.add_nodes_from(range(8))
    truth = [0] * 4 + [1] * 4
    cands = [truth, [0, 0, 0, 1, 1, 1, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1],
             [0] * 8, [0, 0, 1, 1, 0, 0, 1, 1]]
    scores = [_loglik(g, c) for c in cands]
    assert int(np.argmax(scores)) == 0, scores
    lo, hi = min(scores), max(scores)
    out = number_line(150, 970, 176, lo - 1.5, hi + 1.5,
                      [(hi, "the right grouping", "accenttwo", "up")],
                      fmt="{:.0f}")
    for s in scores[1:]:
        out += dot(150 + (s - (lo - 1.5)) / ((hi + 1.5) - (lo - 1.5)) * 820, 176,
                   color="annot", d=16)
    out += dot(150 + (hi - (lo - 1.5)) / ((hi + 1.5) - (lo - 1.5)) * 820, 176,
               color="accenttwo", d=20)
    out += text(560, 92, "how likely this network is, under each guess",
                color="black", anchor="north", size=FONT)
    return out


def _loglik(g, c):
    """Log-probability of the observed network under a block model with assignment c."""
    n = len(c)
    tot = 0.0
    groups = sorted(set(c))
    for a in groups:
        for b in groups:
            if b < a:
                continue
            pairs = [(i, j) for i in range(n) for j in range(i + 1, n)
                     if {c[i], c[j]} == {a, b}]
            if not pairs:
                continue
            k = sum(1 for i, j in pairs if g.has_edge(i, j))
            p = min(max(k / len(pairs), 1e-6), 1 - 1e-6)
            tot += k * np.log(p) + (len(pairs) - k) * np.log(1 - p)
    return tot


@fig("sbm-shuffled", h=380)
def _shuffled():
    """The same network, in the order you happened to receive it."""
    e = _sbm_graph()
    rng = np.random.default_rng(9)
    order = [int(v) for v in rng.permutation(10)]
    assert sorted(order) == list(range(10)) and order != list(range(10))
    filled = _sorted_matrix(e, 10, order)
    ref = _sorted_matrix(e, 10, list(range(10)))
    assert len(filled) == len(ref), "shuffling must not add or lose a single friendship"
    out = _sbm_ring(e, coloured=False)
    out += cell_grid(636, 362, 10, 33, filled, fill_color="accent")
    return out


@fig("sbm-assortative", h=360)
def _assort():
    """The ordinary case, at full size: a high diagonal and the groups you expect.

    Deliberately its own file rather than a crop of `sbm-three-cases`. That figure is a
    comparison of three matrices; this slide is about one of them, and m01 shipped a
    figure reused across two slides that explained it differently.
    """
    e = _sbm_graph(5, 0.85, 0.08, seed=12)
    inside = sum(1 for a, b in e if (a < 5) == (b < 5))
    assert inside > 2 * (len(e) - inside), "the diagonal has to dominate here"
    out = _sbm_ring(e, node=34, cx=286, cy=184, rx=250, ry=142)
    out += cell_grid(716, 300, 2, 104, {(0, 0), (1, 1)}, fill_color="accentthree")
    out += text(716 + 52, 300 - 52, "high", color="black", anchor="center", size=44)
    out += text(716 + 156, 300 - 156, "high", color="black", anchor="center", size=44)
    out += text(716 + 156, 300 - 52, "low", color="annot", anchor="center", size=44)
    out += text(716 + 52, 300 - 156, "low", color="annot", anchor="center", size=44)
    return out
