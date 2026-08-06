#!/usr/bin/env python3
"""Parts 1-3: the club, the patterns that fail, and Zachary's cut.

Every club figure calls `kfig.karate()`, which reads one cached layout and takes only
colours. There is no way from here to move a disc, which is the point: fourteen slides
show this network and the room should be reading the change, not relearning the picture.

**No club figure carries in-figure text.** A full-width figure may be 380px tall, the
layout plus its discs already needs 350, and a 36pt line does not fit in the 30 that are
left. Numbers therefore live in the deck's figcaption -- which is also where
FIGURE_GUIDE says prose belongs.
"""

from fractions import Fraction

import networkx as nx
import numpy as np

import verify_numbers as V
from figlib import Axes, FONT, disc, dot, emit, seg, text
from kfig import CHI, COFF, club, karate, ring_positions, small, split_fill

FIGURES = []


def fig(name, container="full", h=380, hmod=""):
    def deco(fn):
        FIGURES.append((name, lambda: emit(name, fn(), container=container, h=h, hmod=hmod)))
        return fn
    return deco


# =========================================================================== Part 1
@fig("timeline-1970", h=250, hmod="tight")
def _timeline():
    """Three dates, in order, on one line. Nothing else happens on that slide."""
    y = 132
    stops = [(180, "1970", "Zachary starts\\\\watching"),
             (540, "1972", "the club\\\\splits"),
             (900, "1977", "the paper")]
    out = seg((92, y), (988, y), color="black", w=2.6)
    for x, year, what in stops:
        out += dot(x, y, color="accenttwo", d=20)
        out += text(x, y + 20, year, color="accenttwo", anchor="south", size=44)
        out += text(x, y - 22, what, color="black", anchor="north", size=FONT)
    xs = [s[0] for s in stops]
    assert xs == sorted(xs), "the three dates must read left to right in date order"
    return out


@fig("the-dispute", h=380)
def _dispute():
    """Two leaders, one disagreement, thirty-two people in between."""
    out = ""
    for x, col, who, want in ((168, "accent", "Mr. Hi", "raise\\\\the dues"),
                              (912, "accenttwo", "John A.", "keep them\\\\as they are")):
        out += disc(x, 246, fill=col, size=52)
        out += text(x, 302, who, color=col, anchor="south", size=44)
        out += text(x, 186, want, color="black", anchor="north", size=FONT)
    for i in range(32):
        r, c = divmod(i, 8)
        out += disc(352 + c * 54, 306 - r * 62, fill="annot", size=28)
    for i in range(9):                       # the crack running down the middle
        y0, y1 = 62 + i * 32, 62 + (i + 1) * 32
        out += seg((540 + (-9 if i % 2 else 9), y0), (540 + (9 if i % 2 else -9), y1),
                   color="annot", w=3.0)
    return out


@fig("karate-plain", h=380)
def _plain():
    """Thirty-four people, seventy-eight friendships, and no colour at all yet."""
    pos, edges = club()
    assert len(pos) == 34 and len(edges) == 78
    return karate()


@fig("karate-three-guesses", h=380)
def _guesses():
    """Three lines a room actually draws -- and not one of them is the answer.

    Asserted here rather than trusted: the three lines cut the club three *different*
    ways, and none of them reproduces the recorded split. This figure sits on the
    activity slide, one slide before the answer, so leaking it would be an N4 failure
    the render could not show.
    """
    pos, _ = club()
    hi, _ = V.factions()
    # Full height, and three dash patterns the room can tell apart. The first version
    # ran them from y=44 to y=346 in a drawing whose ink spans 26..368, so each line
    # stopped short at both ends and read as a stray mark rather than a cut.
    lines = [(520.0, 0.00, "on 20bp off 12bp"),
             (452.0, 0.62, "on 8bp off 9bp"),
             (612.0, -0.52, "on 34bp off 12bp on 6bp off 12bp")]
    parts = []
    out = ""
    for x0, slope, dash in lines:
        pts = [(x0 + slope * (y - 190), y) for y in (34, 190, 354)]
        out += (f"\\draw[line width=3.8bp,draw=annot,dash pattern={dash}] "
                + " -- ".join(f"({x:.1f},{y:.1f})" for x, y in pts) + ";\n")
        parts.append(frozenset(n for n, (px, py) in pos.items()
                               if px < x0 + slope * (py - 190)))
    assert len({parts[i] for i in range(3)}) == 3, "the three guesses must differ"
    for p in parts:
        assert p != hi and p != frozenset(range(34)) - hi, (
            "a guess reproduces the recorded split -- this figure is on the question "
            "slide and must not contain the answer")
    return karate() + out


@fig("karate-split", h=380)
def _split():
    """What actually happened: seventeen against seventeen."""
    hi, of = V.factions()
    assert len(hi) == len(of) == 17
    return karate(fill=split_fill(hi))


@fig("karate-crossing", h=380)
def _crossing():
    """The eleven friendships the split tore, and nothing else drawn heavily."""
    hi, _ = V.factions()
    _, edges = club()
    cross = [e for e in edges if (e[0] in hi) != (e[1] in hi)]
    inside = [e for e in edges if (e[0] in hi) == (e[1] in hi)]
    assert len(cross) == 11 and len(cross) + len(inside) == 78
    return karate(fill=split_fill(hi), heavy=cross, heavy_color="black",
                  faint=inside)


@fig("why-groups", h=214, hmod="stack")
def _why():
    """Four groups, four different reasons -- one drawing, not four panels.

    Built to the `stack` cap of 190bp rather than the usual 380. The slide it sits on
    carries a four-item build as well, and a 259bp figure plus four rows plus a title
    runs past the pagination row in either order. The type does not shrink; the drawing
    does.
    """
    labels = ["same kind", "same job", "same rank", "same channel"]
    pos, edges = {}, []
    for g in range(4):
        cx = 148 + g * 262
        base = g * 4
        pos.update({base: (cx, 178), base + 1: (cx - 76, 134),
                    base + 2: (cx + 76, 134), base + 3: (cx, 90)})
        edges += [(base, base + 1), (base, base + 2), (base + 1, base + 3),
                  (base + 2, base + 3), (base + 1, base + 2)]
        if g:
            edges.append((base - 2, base + 1))          # one link to the group before
    body = small(pos, edges, node=32, fill={n: "accent" for n in pos}, what="why-groups")
    for g, lab in enumerate(labels):
        body += text(148 + g * 262, 62, lab, color="accenttwo", anchor="north", size=FONT)
    return body


@fig("ground-truth-or-not", h=340)
def _gt():
    """One network with a recorded answer; the same network without one.

    Both halves draw the *same* ten-node graph -- asserted, because the slide's claim is
    that the two differ in exactly one respect, whether anyone wrote the answer down.
    """
    shape = [(0, 300), (150, 300), (75, 206), (0, 112), (150, 112),
             (300, 300), (450, 300), (375, 206), (300, 112), (450, 112)]
    e = [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4),
         (5, 6), (5, 7), (6, 7), (7, 8), (7, 9), (8, 9), (1, 5)]
    out = ""
    for x0, coloured in ((40, True), (560, False)):
        p = {i: (x0 + dx, dy) for i, (dx, dy) in enumerate(shape)}
        f = ({n: (CHI if n < 5 else COFF) for n in p} if coloured
             else {n: "annot" for n in p})
        out += small(p, e, fill=f, what="ground-truth-or-not", node=36)
    out += text(560 + 225, 176, "?", color="accenttwo", anchor="center", size=90)
    return out


# =========================================================================== Part 2
@fig("clique-def", container="col", h=330)
def _clique():
    """Everyone knows everyone -- and one missing handshake ends it.

    Drawn as a square with both diagonals, which costs exactly one crossing. K4 has a
    planar drawing (one node inside the triangle) but it reads as a hierarchy rather
    than as four equals, and the point of the slide is that nobody is special.
    """
    def sq(x0):
        return {0: (x0, 246), 1: (x0 + 168, 246), 2: (x0, 96), 3: (x0 + 168, 96)}
    out = ""
    p = sq(46)
    e = [(0, 1), (0, 2), (1, 3), (2, 3), (0, 3), (1, 2)]
    out += small(p, e, fill={n: "accent" for n in p}, what="clique-def-left",
                 planar=False)
    out += text(46 + 84, 42, "a clique", color="accenttwo", anchor="north", size=FONT)
    p = sq(323)
    out += small(p, e[:-1], fill={n: "annot" for n in p}, dashes=[(1, 2)],
                 what="clique-def-right", planar=False, edges_all=e)
    out += text(323 + 84, 42, "not a clique", color="annot", anchor="north", size=FONT)
    return out


@fig("karate-max-clique", h=380)
def _maxclique():
    """The largest all-knows-all group in a 34-person club is five people."""
    f = V.facts()
    c = f["max_cliques"][0]
    g = V.karate()
    assert all(g.has_edge(a, b) for i, a in enumerate(c) for b in c[i + 1:])
    assert len(c) == 5 and V.MR_HI in c
    return karate(fill={n: CHI for n in c}, rings=c)


@fig("k-plex", container="col", h=350)
def _kplex():
    """Each member may be missing at most k of the others -- here k = 1."""
    p = {0: (30, 262), 1: (268, 300), 2: (506, 262), 3: (410, 120), 4: (126, 120)}
    missing = [(0, 2), (1, 3)]
    present = [(a, b) for a in range(5) for b in range(a + 1, 5)
               if (a, b) not in missing]
    g = nx.Graph(present)
    g.add_nodes_from(p)
    for n in p:
        assert len(p) - 1 - g.degree(n) <= 1, f"node {n} misses more than 1"
    out = small(p, present, fill={n: "accent" for n in p}, dashes=missing,
                what="k-plex", planar=False, edges_all=present + missing)
    out += text(268, 66, "dashed = missing", color="annot", anchor="north", size=FONT)
    return out


@fig("rho-dense", container="col", h=330)
def _dense():
    """Half the friendships that could exist, and we call it a group anyway."""
    p = ring_positions(6, 268, 196, 248, 104, start=90)
    e = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 0), (0, 2), (3, 5)]
    poss = 6 * 5 // 2
    assert abs(len(e) / poss - 8 / 15) < 1e-9
    out = small(p, e, fill={n: "accent" for n in p}, what="rho-dense", planar=False)
    out += text(268, 48, f"{len(e)} of {poss} possible", color="accenttwo",
                anchor="north", size=FONT)
    return out


@fig("n-clique", container="col", h=330)
def _nclique():
    """Nobody is more than two steps from anybody -- that is the whole requirement."""
    p = {0: (30, 196), 1: (176, 292), 2: (176, 100), 3: (360, 292), 4: (360, 100),
         5: (506, 196)}
    e = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 5), (1, 2), (3, 4)]
    g = nx.Graph(e)
    assert nx.diameter(g) == 3, nx.diameter(g)
    out = small(p, e, fill={n: "accent" for n in p}, heavy=[(0, 1), (1, 3)],
                what="n-clique")
    out += text(268, 44, "two steps, end to end", color="accenttwo",
                anchor="north", size=FONT)
    return out


@fig("k-truss", container="col", h=330)
def _ktruss():
    """Every friendship has to sit inside a triangle, not just exist."""
    p = {0: (30, 282), 1: (232, 196), 2: (30, 110), 3: (506, 282), 4: (506, 110)}
    e = [(0, 1), (1, 2), (0, 2), (1, 3), (1, 4), (3, 4)]
    g = nx.Graph(e)
    for a, b in e:
        assert len(set(g[a]) & set(g[b])) >= 1, f"edge {(a, b)} lies in no triangle"
    out = small(p, e, fill={n: "accent" for n in p}, heavy=[(1, 3), (1, 4), (3, 4)],
                what="k-truss")
    out += text(268, 54, "every link in a triangle", color="accenttwo",
                anchor="north", size=FONT)
    return out


@fig("patterns-overlap", h=356)
def _overlap():
    """Three definitions, three different groups, and two people in none of them.

    Drawn on eleven people rather than on the club. The claim is that the groups OVERLAP
    and leave members out, and thirty-four intermingled discs cannot show that -- the
    first version rendered as one ringed set of six and no visible overlap at all.
    """
    p = {0: (128, 288), 1: (128, 128), 2: (272, 208), 3: (416, 288), 4: (416, 128),
         5: (560, 208), 6: (704, 288), 7: (704, 128), 8: (848, 208),
         9: (980, 300), 10: (980, 116)}
    e = [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4), (3, 5), (4, 5),
         (5, 6), (5, 7), (6, 7), (6, 8), (7, 8), (8, 9), (9, 10)]
    A, B, C = {0, 1, 2}, {2, 3, 4, 5}, {5, 6, 7, 8}
    assert A & B and B & C and not (A & C), "the groups must overlap in a chain"
    assert set(p) - (A | B | C) == {9, 10}, "two people must belong to none of them"
    out = ""
    for grp, col in ((A, "accent"), (B, "accenttwo"), (C, "accentthree")):
        xs = [p[n][0] for n in grp]
        ys = [p[n][1] for n in grp]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        rx = (max(xs) - min(xs)) / 2 + 42
        ry = (max(ys) - min(ys)) / 2 + 42
        out += (f"\\draw[line width=4.6bp,draw={col},dash pattern=on 12bp off 9bp] "
                f"({cx:.1f},{cy:.1f}) ellipse ({rx:.1f}bp and {ry:.1f}bp);\n")
    out += small(p, e, node=34, what="patterns-overlap",
                 fill={n: ("annot" if n in (9, 10) else "accent") for n in p})
    return out


# =========================================================================== Part 3
# The nine-member club that carries every piece of cut arithmetic. Each half is a group
# of four who all know each other, drawn as a triangle with the fourth member inside --
# the only planar drawing of four mutual friends, and the reason the two members who
# carry the bridges (3 and 4, 5 and 6) sit on the outside where their edges can leave.
SMALL_POS = {9: (46, 214), 1: (150, 214), 2: (250, 214), 3: (340, 320), 4: (340, 108),
             5: (760, 108), 6: (760, 320), 8: (856, 214), 7: (960, 214)}
SMALL_E = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4),
           (5, 6), (5, 7), (5, 8), (6, 7), (6, 8), (7, 8), (4, 5), (3, 6), (1, 9)]
SMALL_LEFT = {1, 2, 3, 4, 9}


def _small_club(pos=None, **kw):
    kw.setdefault("what", "small club")
    return small(dict(pos or SMALL_POS), list(SMALL_E), **kw)


@fig("cut-idea", h=380)
def _cutidea():
    """Stop looking for the groups. Look at what runs between them."""
    out = _small_club(fill={n: (CHI if n in SMALL_LEFT else COFF) for n in SMALL_POS})
    out += ("\\draw[line width=3.6bp,draw=annot,dash pattern=on 13bp off 10bp] "
            "(550,52) -- (550,376);\n")
    return out


@fig("cut-def", h=380)
def _cutdef():
    """Cut(V1, V2) counts the friendships that cross -- here, two of them."""
    cross = [e for e in SMALL_E if (e[0] in SMALL_LEFT) != (e[1] in SMALL_LEFT)]
    assert len(cross) == V.cut_size(V.small_club(), SMALL_LEFT) == 2
    out = _small_club(what="cut-def", heavy=cross,
                      fill={n: (CHI if n in SMALL_LEFT else COFF) for n in SMALL_POS})
    out += text(550, 62, "cut = 2", color="accenttwo", anchor="north", size=44)
    return out


def _pentagon(nodes, cx, cy, r, facing, start=None):
    """Five mutual friends on a circle, rotated to bring `facing` nearest the other five.

    A clique of five has no crossing-free drawing, but it must still not run an edge
    through somebody else's disc -- which is exactly what happened when the bridge left
    from whichever node the default angle happened to put at the back.

    `start` is the angle the facing member sits at. It defaults to the horizontal pair
    (the two cliques side by side); pass 270 and 90 when they are stacked instead, or
    the two rings come out aligned and their nearest members end up 6bp apart.
    """
    i = nodes.index(facing)
    if start is None:
        start = 180.0 if cx > 540 else 0.0
    return ring_positions(5, cx, cy, r, r, start=start, order=nodes[i:] + nodes[:i])


@fig("two-cliques", h=380)
def _twocliques():
    """The demo network: two complete groups of five, joined by one friendship."""
    g = V.two_cliques()
    assert g.number_of_edges() == 21
    bridge = [e for e in g.edges() if (e[0] < 5) != (e[1] < 5)]
    assert len(bridge) == 1
    a, b = bridge[0]
    pos = {**_pentagon(list(range(5)), 214, 196, 152, a),
           **_pentagon(list(range(5, 10)), 866, 196, 152, b)}
    return small(pos, list(g.edges()), what="two-cliques", planar=False,
                 fill={n: (CHI if n < 5 else COFF) for n in pos})


@fig("karate-trivial-cut", h=380)
def _trivial():
    """The cheapest cut in the club costs one friendship, and finds nothing."""
    f = V.facts()
    leaf = f["degree_one_nodes"][0]
    _, edges = club()
    its = [e for e in edges if leaf in e]
    assert len(its) == 1
    return karate(fill={leaf: COFF}, heavy=its, heavy_color="accenttwo", rings=[leaf])


@fig("ratio-cut", h=380)
def _ratiocut():
    """Both candidate cuts on one drawing, each carrying its own score.

    Two shrunken copies would put 30bp discs 37bp apart; one drawing with two dashed
    lines says the same thing at full size, and puts the two numbers where the room can
    compare them without moving its eyes off the network.
    """
    sc = V.facts()["small_club"]
    assert sc["trivial_ratio"] > sc["natural_ratio"], "the balanced split must win"
    out = _small_club(fill={n: "accent" for n in SMALL_POS})
    for x, col, val in ((98, "annot", sc["trivial_ratio"]),
                        (550, "accenttwo", sc["natural_ratio"])):
        out += (f"\\draw[line width=3.6bp,draw={col},dash pattern=on 13bp off 10bp] "
                f"({x},104) -- ({x},366);\n")
        out += text(x, 88, f"{val.numerator}/{val.denominator}", color=col,
                    anchor="north", size=44)
    return out


@fig("normalizer-curve", h=330)
def _normalizer():
    """The normalizer is biggest at the halfway point, which is where it sends you."""
    n = 34
    xs = list(range(1, n))
    ys = [k * (n - k) for k in xs]
    ax = Axes((196, 116, 1016, 250), (1, n - 1), (0, max(ys) * 1.10),
              xlabel="members on the smaller side", yticks=[0, max(ys)],
              yfmt=lambda v: "0" if v == 0 else "biggest")
    out = ax.frame()
    out += ax.line(xs, ys, color="accent", w=4.0)
    peak = xs[int(np.argmax(ys))]
    assert peak in (n // 2, n // 2 - 1), peak
    px, py = ax.P(peak, max(ys))
    out += dot(px, py, color="accenttwo", d=17)
    out += text(px, py + 18, "equal halves", color="accenttwo", anchor="south", size=FONT)
    return out


@fig("norm-cut", h=380)
def _normcut():
    """Balance by the friendships inside each side, not by the head count."""
    sc = V.facts()["small_club"]
    g = V.small_club()
    e1 = g.subgraph(SMALL_LEFT).number_of_edges()
    e2 = g.subgraph(set(g) - SMALL_LEFT).number_of_edges()
    assert (e1, e2) == (7, 6), (e1, e2)
    # Fraction reduces, so 2/42 arrives as 1/21 -- compare the value, not the spelling.
    assert sc["natural_ncut"] == Fraction(V.cut_size(g, SMALL_LEFT), e1 * e2)
    cross = [e for e in SMALL_E if (e[0] in SMALL_LEFT) != (e[1] in SMALL_LEFT)]
    out = _small_club(what="norm-cut", heavy=cross,
                      fill={n: (CHI if n in SMALL_LEFT else COFF) for n in SMALL_POS})
    out += text(216, 48, f"{e1} inside", color="accent", anchor="north", size=44)
    out += text(866, 48, f"{e2} inside", color="accenttwo", anchor="north", size=44)
    return out


@fig("k-way-cut", h=380)
def _kway():
    """Three groups: each one's escaping friendships, divided by its own size."""
    pos, e = {}, []
    for g, cx in enumerate((190, 540, 890)):
        b = g * 4
        pos.update({b: (cx, 300), b + 1: (cx - 96, 200), b + 2: (cx + 96, 200),
                    b + 3: (cx, 100)})
        e += [(b, b + 1), (b, b + 2), (b + 1, b + 3), (b + 2, b + 3), (b + 1, b + 2)]
    e += [(2, 5), (6, 9)]
    cols = ["accent", "accenttwo", "accentthree"]
    out = small(pos, e, what="k-way-cut",
                fill={n: cols[n // 4] for n in pos}, heavy=[(2, 5), (6, 9)],
                heavy_color="black")
    for g, cx in enumerate((190, 540, 890)):
        esc = sum(1 for a, b in e if (a // 4 == g) != (b // 4 == g))
        out += text(cx, 58, f"{esc} out of 4", color="annot", anchor="north", size=FONT)
    return out


@fig("karate-mincut", h=380)
def _mincut():
    """Zachary's own method, on Zachary's own club: thirty-three out of thirty-four."""
    f = V.facts()
    S, _ = V.zachary_min_cut()
    assert f["mincut_agree"] == 33
    fill = {n: (CHI if n in S else COFF) for n in range(34)}
    return karate(fill=fill, rings=[V.NODE9], ring_color="accentthree")


@fig("karate-node9-ring", h=380)
def _node9ring():
    """One member, circled, not named."""
    return karate(rings=[V.NODE9], ring_color="accenttwo")
