#!/usr/bin/env python3
"""Parts 7-9: the three ways modularity lies, how you would ever know, and the close.

The resolution-limit pair is the lecturer's own demo data, not something constructed for
the slide: `two-cliques.json` and `two-cliques-big-clique.json` contain the *same* two
five-cliques, and the only difference between them is a forty-node community somewhere
else in the network. The figures assert that identity node for node, because the whole
argument is that nothing about the cliques changed.
"""

from fractions import Fraction

import networkx as nx
import numpy as np

import verify_numbers as V
from figlib import Axes, FONT, disc, dot, emit, seg, text
from kfig import (
    CHI, COFF, arrow, blob, cell_grid, club, dot_strip, karate, number_line, relax,
    ring_positions, small, split_fill,
)
from figs_story import _pentagon

FIGURES = []


def fig(name, container="full", h=380, hmod=""):
    def deco(fn):
        FIGURES.append((name, lambda: emit(name, fn(), container=container, h=h, hmod=hmod)))
        return fn
    return deco


# =========================================================================== Part 7
def _two_clique_pos(cx_left=214, cx_right=866, cy=196, r=152):
    g = V.two_cliques()
    a, b = [e for e in g.edges() if (e[0] < 5) != (e[1] < 5)][0]
    return {**_pentagon(list(range(5)), cx_left, cy, r, a),
            **_pentagon(list(range(5, 10)), cx_right, cy, r, b)}, g


@fig("two-cliques-split", h=380)
def _tcsplit():
    """Left alone, modularity keeps them apart -- and it is right to."""
    f = V.facts()["tc"]
    assert f["Q_split"] > f["Q_merged"]
    pos, g = _two_clique_pos()
    out = small(pos, list(g.edges()), what="two-cliques-split", planar=False,
                fill={n: (CHI if n < 5 else COFF) for n in pos})
    out += ("\\draw[line width=3.6bp,draw=annot,dash pattern=on 13bp off 10bp] "
            "(540,26) -- (540,366);\n")
    return out


def _assert_same_cliques():
    """The two demo networks must contain the same pair of five-cliques.

    Not the same edge list: the small network joins them at (0,6) and the big one at
    (0,5), which relabels one endpoint and nothing else. What the argument actually
    needs -- and what is checked here -- is that both cliques are complete on the same
    members in both networks, and that exactly one friendship joins them in each.
    """
    for g, name in ((V.two_cliques(), "two-cliques"),
                    (V.two_cliques_big(), "two-cliques-big-clique")):
        for c in (V.CLIQUE_A, V.CLIQUE_B):
            assert g.subgraph(c).number_of_edges() == 10, \
                f"{name}: {sorted(c)} is not complete"
        joins = [e for e in g.edges()
                 if {e[0] in V.CLIQUE_A, e[1] in V.CLIQUE_A} == {True, False}
                 and max(e) < 10]
        assert len(joins) == 1, f"{name}: {len(joins)} friendships join the two cliques"


def _clique_pair(cx, cy_top, cy_bot, r):
    """The two cliques stacked, each rotated so its bridge member faces the other."""
    g = V.two_cliques_big()
    a, b = [e for e in g.edges() if (e[0] < 5) != (e[1] < 5) and max(e) < 10][0]
    return {**_pentagon(list(range(5)), cx, cy_top, r, a, start=270),
            **_pentagon(list(range(5, 10)), cx, cy_bot, r, b, start=90)}


@fig("big-clique-net", h=380)
def _bignet():
    """The same two cliques, and a forty-person community with nothing to do with them."""
    _assert_same_cliques()
    g = V.two_cliques_big()
    pos = _clique_pair(180, 276, 112, 72)
    e = [tuple(x) for x in g.edges() if max(x) < 10]
    out = small(pos, e, node=32, what="big-clique-net", planar=False,
                fill={n: (CHI if n < 5 else COFF) for n in pos})
    out += blob(740, 194, 300, 150)
    out += text(740, 196, "forty more", color="black", anchor="center", size=44)
    link = [x for x in g.edges() if (min(x) < 10) != (max(x) < 10)]
    assert len(link) == 1, link
    out += seg(pos[min(link[0])], (446, 220), color="black", w=2.6)
    return out


@fig("resolution-limit", h=380)
def _reslimit():
    """Before and after: nothing about the cliques changed, and the answer did."""
    f = V.facts()
    _assert_same_cliques()
    assert f["tcb"]["Q_merged"] > f["tcb"]["Q_split"], "in company they must merge"
    assert f["tc"]["Q_split"] > f["tc"]["Q_merged"], "alone they must stay apart"
    g = V.two_cliques()
    out = ""
    left = _clique_pair(120, 282, 116, 68)
    out += small(left, list(g.edges()), node=28, what="reslimit-before",
                 planar=False, fill={n: (CHI if n < 5 else COFF) for n in left})
    out += text(120, 40, "two groups", color="accenttwo", anchor="north", size=FONT)
    right = {n: (x + 420, y) for n, (x, y) in left.items()}
    out += small(right, list(g.edges()), node=28, what="reslimit-after",
                 planar=False, fill={n: "accentthree" for n in right})
    out += blob(884, 200, 162, 146)
    out += text(884, 200, "forty", color="black", anchor="center", size=44)
    out += seg((584, 224), (722, 212), color="black", w=2.6)
    out += text(540, 40, "one group", color="accenttwo", anchor="north", size=FONT)
    return out


@fig("sqrt2m", h=330)
def _sqrt():
    """The threshold is set by the whole network's size, not by the group's."""
    f = V.facts()
    tc, tcb = f["tc"], f["tcb"]
    ms = list(range(10, 700, 4))
    ax = Axes((186, 116, 1010, 288), (0, 700), (0, 30),
              xlabel="friendships in the whole network",
              xticks=[0, 200, 400, 600], yticks=[0, 10, 20, 30])
    out = ax.frame()
    out += ax.line(ms, [np.sqrt(2 * m) for m in ms], color="accent", w=4.2)
    for m, lab, col in ((tc["M"], "kept apart", "accent"),
                        (tcb["M"], "absorbed", "accenttwo")):
        x, y = ax.P(m, tc["clique_internal"])
        out += dot(x, y, color=col, d=18)
        out += text(x, y + 20, lab, color=col, anchor="south", size=FONT)
    assert tc["clique_internal"] > tc["sqrt2m"] and tcb["clique_internal"] < tcb["sqrt2m"]
    return out


@fig("non-local", h=340)
def _nonlocal():
    """Two identical groups, two different fates, decided somewhere else entirely."""
    out = ""
    for x0, crowd in ((40, 0), (560, 26)):
        g0 = V.two_cliques()
        a, b = [e for e in g0.edges() if (e[0] < 5) != (e[1] < 5)][0]
        pos = {**_pentagon(list(range(5)), x0 + 110, 252, 60, a, start=270),
               **_pentagon(list(range(5, 10)), x0 + 110, 96, 60, b, start=90)}
        out += small(pos, list(g0.edges()), node=28, what=f"non-local-{x0}", planar=False,
                     fill={n: (CHI if n < 5 else COFF) for n in pos})
        rng = np.random.default_rng(x0)
        for i in range(crowd):
            out += disc(x0 + 252 + (i % 6) * 42 + rng.uniform(-5, 5),
                        62 + (i // 6) * 56 + rng.uniform(-5, 5), fill="annot", size=26)
    return out


@fig("degeneracy", h=330)
def _degen():
    """Many different answers, all scoring within a hair of each other."""
    f = V.facts()
    rng = np.random.default_rng(2)
    xs = np.linspace(0, 1, 400)
    ys = (0.30 + 0.10 * np.sin(xs * 22) ** 2 + 0.015 * rng.normal(0, 1, 400).cumsum() / 10)
    ys = np.clip(ys, 0.18, 0.44)
    ax = Axes((196, 116, 1010, 286), (0, 1), (0.15, 0.47),
              xlabel="one grouping after another", xticks=[],
              yticks=[0.2, 0.3, 0.4])
    out = ax.frame()
    out += ax.line(list(xs), list(ys), color="accent", w=3.4)
    for x, q, lab, col in ((0.29, f["louvain_Q"], "best", "accenttwo"),
                           (0.71, f["degenerate_alt_Q"], "next", "annot")):
        px, py = ax.P(x, q)
        out += dot(px, py, color=col, d=17)
        out += text(px, py + 18, lab, color=col, anchor="south", size=FONT)
    assert f["louvain_Q"] - f["degenerate_alt_Q"] < 0.006
    return out


@fig("random-net", h=380)
def _rnd():
    """Forty people wired together at random. No groups were put in."""
    g = V.random_net()
    assert g.number_of_edges() == 41
    pos = relax(_spring(g, 1040, 330, seed=5), list(g.edges()), node=30,
                box=(26, 46, 1054, 350))
    return small(pos, list(g.edges()), node=30, what="random-net", planar=False,
                 fill={n: "annot" for n in pos}, edge_w=2.2)


def _spring(g, w, h, seed=0, margin=26, node=30):
    p0 = nx.spring_layout(g, seed=seed, iterations=600, k=1.5)
    P = np.array([p0[n] for n in sorted(g)], float)
    P -= P.min(0)
    P /= np.maximum(P.max(0), 1e-9)
    P = P * np.array([w - 2 * margin, h - 2 * margin]) + margin
    return {n: (float(P[i, 0]) + (1080 - w) / 2, float(P[i, 1]) + 26)
            for i, n in enumerate(sorted(g))}


@fig("random-q-dots", h=300)
def _rqdots():
    """Two hundred random networks the size of the club, every one of them scoring well."""
    f = V.facts()
    er = _er_scores()
    assert min(er) > 0.3 and abs(np.mean(er) - f["er_mean"]) < 1e-9
    lo, hi = 0.24, 0.46
    out = number_line(150, 970, 132, lo, hi,
                      [(0.3, "the rule of thumb", "annot", "down"),
                       (f["Q_true"], "the real split", "accenttwo", "down")],
                      fmt="{:.2f}")
    out += dot_strip(150, 970, 208, er, lo, hi, color="accent", d=11, jitter=17, seed=6)
    out += text(560, 268, "two hundred random networks, same size as the club",
                color="black", anchor="north", size=FONT)
    return out


def _er_scores():
    from networkx.algorithms.community import louvain_communities
    return [max(V.unweighted_Q(h, louvain_communities(h, seed=t)) for t in range(5))
            for h in (nx.gnm_random_graph(34, 78, seed=s) for s in range(200))]


# =========================================================================== Part 8
@fig("three-partitions", h=380)
def _three():
    """The same club, three methods, three different answers."""
    f = V.facts()
    hi, _ = V.factions()
    S, _ = V.zachary_min_cut()
    L4 = f["louvain_parts"]
    assert {frozenset(hi), frozenset(S)} != {frozenset(hi)}, "the answers must differ"
    cols = ["accent", "accenttwo", "accentthree", "annot"]
    return karate(fill={n: cols[next(i for i, c in enumerate(L4) if n in c)]
                        for n in range(34)})


@fig("conductance-def", container="col", h=340)
def _conddef():
    """The friendships that escape, over everything the group is attached to."""
    p = {0: (60, 292), 1: (60, 118), 2: (208, 205), 3: (360, 292), 4: (360, 118),
         5: (500, 205)}
    e = [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5)]
    grp = {0, 1, 2}
    g = nx.Graph(e)
    esc = sum(1 for a, b in e if (a in grp) != (b in grp))
    vol = sum(g.degree(n) for n in grp)
    assert (esc, vol) == (2, 8), (esc, vol)
    out = small(p, e, node=36, what="conductance-def",
                heavy=[x for x in e if (x[0] in grp) != (x[1] in grp)],
                fill={n: (CHI if n in grp else "annot") for n in p})
    out += text(268, 62, f"{esc} escape, {vol} ends in all", color="accenttwo",
                anchor="north", size=FONT)
    return out


@fig("conductance-karate", h=380)
def _condk():
    """The split that happened, scored without any answer key at all."""
    f = V.facts()
    hi, _ = V.factions()
    _, edges = club()
    cross = [e for e in edges if (e[0] in hi) != (e[1] in hi)]
    assert f["cond_true"] == Fraction(11, 75)
    return karate(fill=split_fill(hi), heavy=cross, heavy_color="black")


@fig("scores-disagree", h=300)
def _disagree():
    """One score puts the real split first; the other puts Louvain first."""
    f = V.facts()
    worst_louvain = max(float(c) for c in f["cond_louvain"])
    assert float(f["cond_true"]) < min(float(c) for c in f["cond_louvain"])
    assert f["louvain_Q"] > f["Q_true"]
    out = number_line(150, 560, 236, 0.0, 0.5,
                      [(float(f["cond_true"]), "the real split", "accenttwo", "up"),
                       (worst_louvain, "Louvain", "annot", "up")], fmt="{:.1f}")
    out += text(355, 122, "conductance: lower is better", color="black",
                anchor="north", size=FONT)
    out += number_line(620, 1010, 236, 0.0, 0.5,
                       [(f["Q_true"], "the real split", "accenttwo", "up"),
                        (f["louvain_Q"], "Louvain", "annot", "up")], fmt="{:.1f}")
    out += text(815, 122, "modularity: higher is better", color="black",
                anchor="north", size=FONT)
    return out


# start=0 puts two members at the horizontal extremes; at 90 the widest
# points of the ellipse carry nobody and the drawing loses 10% of its span.
SIX = ring_positions(6, 540, 190, 424, 122, start=0)


@fig("pairs-15", h=360)
def _pairs():
    """Six people make fifteen pairs, and every score below counts those pairs."""
    n = 6
    pairs = [(a, b) for a in range(n) for b in range(a + 1, n)]
    assert len(pairs) == 15
    return small(SIX, pairs, node=38, what="pairs-15", planar=False,
                 fill={k: "annot" for k in SIX}, edge_w=1.8)


@fig("mutual-information", h=340)
def _mi():
    """Knowing where somebody landed tells you something about where they belonged."""
    s = V.worksheet_scores()
    out = ""
    for row, (y, lab, col) in enumerate(((296, "what really happened", "accenttwo"),
                                         (104, "what the method said", "accent"))):
        labels = V.WORKSHEET_TRUTH if row == 0 else V.WORKSHEET_FOUND
        for i, g in enumerate(labels):
            out += disc(118 + i * 169, y, size=48,
                        fill=(col if g == 0 else "annot"))
        out += text(96, y, lab, color=col, anchor="east", size=FONT) if False else ""
    for i in range(6):
        out += seg((118 + i * 169, 268), (118 + i * 169, 132), color="annot", w=2.6)
    out += text(540, 44, f"they agree about five of the six", color="black",
                anchor="north", size=FONT)
    assert abs(s["I"] - 0.3183) < 5e-5
    return out


@fig("nmi-formula", h=300)
def _nmiform():
    """Divide what they share by how much there was to know."""
    s = V.worksheet_scores()
    total = (s["H_true"] + s["H_found"]) / 2
    share = s["I"] / total
    assert abs(2 * s["I"] / (s["H_true"] + s["H_found"]) - s["nmi"]) < 1e-12
    x0, x1, y = 116, 1004, 210
    out = seg((x0, y), (x1, y), color="annot", w=26)
    out += seg((x0, y), (x0 + (x1 - x0) * share, y), color="accenttwo", w=26)
    out += text(x0 + (x1 - x0) * share / 2, y - 30, "shared", color="accenttwo",
                anchor="north", size=FONT)
    out += text((x0 + x1) / 2, y + 26, "everything there was to know", color="annot",
                anchor="south", size=FONT)
    return out


def _six_row(labels, y, cols, size=48, x0=118, dx=169):
    out = ""
    for i, g in enumerate(labels):
        out += disc(x0 + i * dx, y, size=size, fill=cols[g])
    return out


@fig("worksheet-nmi", h=320)
def _wsnmi():
    """Six people, one of them put in the wrong group. No score on this slide."""
    out = _six_row(V.WORKSHEET_TRUTH, 268, {0: "accenttwo", 1: "annot"})
    out += _six_row(V.WORKSHEET_FOUND, 108, {0: "accent", 1: "annot"})
    for i in range(6):
        out += seg((118 + i * 169, 240), (118 + i * 169, 136), color="annot", w=2.2)
    for token in ("0.47", "0.32", "10/15", "NMI"):
        assert token not in out, f"{token!r} leaks the answer onto the question slide"
    return out


@fig("worksheet-nmi-answer", h=340)
def _wsnmia():
    """What the two scores say about that one misplaced person."""
    s = V.worksheet_scores()
    assert abs(s["nmi"] - 0.4787) < 5e-5 and s["rand"] == Fraction(2, 3)
    out = _six_row(V.WORKSHEET_TRUTH, 288, {0: "accenttwo", 1: "annot"})
    out += _six_row(V.WORKSHEET_FOUND, 158, {0: "accent", 1: "annot"})
    for i in range(6):
        out += seg((118 + i * 169, 260), (118 + i * 169, 186), color="annot", w=2.2)
    out += text(370, 74, f"{s['nmi']:.2f}", color="accenttwo", anchor="north", size=56)
    out += text(370, 118, "shared", color="annot", anchor="north", size=FONT)
    out += text(760, 74, f"{s['rand'].numerator * 5}/15", color="accent",
                anchor="north", size=56)
    out += text(760, 118, "pairs agreeing", color="annot", anchor="north", size=FONT)
    return out


@fig("ari", h=300)
def _ari():
    """Take away what coin-flipping would have scored and very little is left."""
    s = V.worksheet_scores()
    assert float(s["rand"]) > s["ari"]
    out = number_line(160, 960, 190, 0.0, 1.0,
                      [(float(s["rand"]), "counting pairs", "annot", "up"),
                       (s["ari"], "after chance is removed", "accenttwo", "down")])
    return out


@fig("nmi-vs-ari", h=300)
def _nmiari():
    """One is generous where the other is strict, so both get reported."""
    s = V.worksheet_scores()
    out = number_line(160, 960, 190, 0.0, 1.0,
                      [(s["nmi"], "one score", "accent", "up"),
                       (s["ari"], "the other", "accenttwo", "down")])
    out += text(560, 268, "same partition, same answer key", color="black",
                anchor="north", size=FONT)
    return out


@fig("best-vs-real", h=380)
def _bestreal():
    """The highest-scoring answer, and the one that actually happened."""
    f = V.facts()
    assert f["louvain_Q"] > f["Q_true"]
    L4 = f["louvain_parts"]
    cols = ["accent", "accenttwo", "accentthree", "annot"]
    return karate(fill={n: cols[next(i for i, c in enumerate(L4) if n in c)]
                        for n in range(34)},
                  rings=[])


@fig("nmi-comparison", h=300)
def _nmicomp():
    """The higher score is the worse answer, measured against what happened."""
    f = V.facts()
    assert f["louvain_nmi"] < f["mincut_nmi"]
    out = number_line(160, 960, 190, 0.0, 1.0,
                      [(f["mincut_nmi"], "Zachary's cut, 1977", "accenttwo", "up"),
                       (f["louvain_nmi"], "the highest-scoring grouping", "annot",
                        "down")])
    out += text(560, 274, "how well each matches what really happened",
                color="black", anchor="north", size=FONT)
    return out


@fig("node9", h=380)
def _node9():
    """One member the structure could not have got right."""
    S, _ = V.zachary_min_cut()
    hi, _ = V.factions()
    assert (V.NODE9 in S) != (V.NODE9 in hi), "node 9 must be the disagreement"
    fill = {n: (CHI if n in hi else COFF) for n in range(34)}
    return karate(fill=fill, rings=[V.NODE9], ring_color="accentthree")


@fig("no-free-lunch", h=340)
def _nofree():
    """Three methods, three answers, and no umpire anywhere in the picture."""
    p = ring_positions(6, 540, 234, 128, 84, start=90)
    e = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 3)]
    out = small(p, e, node=32, what="no-free-lunch", planar=False,
                fill={n: "annot" for n in p})
    for x, lab, col in ((150, "two groups", "accent"), (540, "three", "accenttwo"),
                        (930, "one", "accentthree")):
        out += text(x, 96, lab, color=col if col != "accentthree" else "annot",
                    anchor="north", size=FONT)
        out += arrow((x + (170 if x < 540 else -170 if x > 540 else 0),
                      160 if x != 540 else 150),
                     (x + (60 if x < 540 else -60 if x > 540 else 0), 118),
                     color="annot", w=3.0)
    return out


# =========================================================================== Part 9
@fig("applications", h=340)
def _apps():
    """One network, four fields that have already asked this exact question."""
    labels = ["who talks to whom", "which proteins work together",
              "which networks route to which", "which papers cite which"]
    out = ""
    pos, e = {}, []
    for g in range(4):
        cx = 148 + g * 262
        b = g * 4
        pos.update({b: (cx, 292), b + 1: (cx - 74, 218), b + 2: (cx + 74, 218),
                    b + 3: (cx, 144)})
        e += [(b, b + 1), (b, b + 2), (b + 1, b + 3), (b + 2, b + 3), (b + 1, b + 2)]
        if g:
            e.append((b - 2, b + 1))
    cols = ["accent", "accenttwo", "accent", "accenttwo"]
    out += small(pos, e, node=34, what="applications",
                 fill={n: cols[n // 4] for n in pos})
    for g, lab in enumerate(labels):
        out += text(148 + g * 262, 116, lab.replace(" ", "\\\\", 2), color="annot",
                    anchor="north", size=FONT)
    return out


@fig("recap", h=340)
def _recap():
    """Four moves, in the order the module made them."""
    steps = [("the club", "split in two"), ("cut it", "33 of 34"),
             ("more than chance", "Q picks K"), ("is it real?", "three lies")]
    out = ""
    for i, (top, bot) in enumerate(steps):
        x = 150 + i * 260
        out += disc(x, 232, fill="accent" if i % 2 == 0 else "accenttwo", size=88)
        out += text(x, 292, top, color="black", anchor="south", size=FONT)
        out += text(x, 166, bot, color="annot", anchor="north", size=FONT)
        if i:
            out += arrow((x - 216, 232), (x - 62, 232), color="annot", w=3.4)
    return out


@fig("m06-teaser", h=380)
def _teaser():
    """The club broke cleanly because it had exactly two people holding it together."""
    f = V.facts()
    hi, _ = V.factions()
    assert (f["deg_mr_hi"], f["deg_john_a"]) == (16, 17)
    return karate(fill=split_fill(hi), big=[V.MR_HI, V.JOHN_A])
