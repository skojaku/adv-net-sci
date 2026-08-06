#!/usr/bin/env python3
"""Parts 1-4 of the Module 04 deck: Marketville, counting ends, the exact gap, using it.

Twenty-nine figures.  Every drawing primitive comes from `figlib`, the eight girls'
one shared layout from `feld`, and every printed number from `verify_numbers` -- nothing
here types a value that the data can produce.

Containers are read off the deck's own markup (`m04-node-degree.md`), not off the spec
table: `feld-degrees` and `feld-two-numbers` sit in `cols` columns there, and a figure
authored for 1080bp and dropped into a 537bp column renders at 48% of its intended scale.
"""

import math
from functools import lru_cache

import networkx as nx
import numpy as np

from feld import ABOVE, BELOW, EQUAL, G, LABEL_BAND, M, POS, degree, friend_mean, solve_names
from figlib import (DASH, EDGE_W, FONT, SMALLNODE, Axes, assert_planar_drawing, disc,
                    dot, draw_labels, emit, pct, place_labels, polyline, ring, seg, text)
from verify_numbers import (FELD_EDGES, FELD_ORDER, LITERATURE, MARKETVILLE_ABOVE,
                            MARKETVILLE_BELOW, MARKETVILLE_EQUAL, MARKETVILLE_PK,
                            condmat, immunization_curves, internet_as, moments,
                            net_stats, paradox_share)

FULL_H = 420          # page height for a full-width figure; the crop trims it to the ink
COL_H = 400

ARROW = "-{Stealth[length=13bp,width=9bp]}"


# --------------------------------------------------------------------------- helpers
def rect(x0, y0, x1, y1, draw="black", fill=None, w=2.6, rounded=0):
    o = [f"line width={w}bp"]
    o.append(f"draw={draw}" if draw else "draw=none")
    if fill:
        o.append(f"fill={fill}")
    if rounded:
        o.append(f"rounded corners={rounded}bp")
    return f"\\draw[{','.join(o)}] ({x0:.1f},{y0:.1f}) rectangle ({x1:.1f},{y1:.1f});\n"


def arc(p, q, bulge=70, color="accenttwo", w=3.4, dash=DASH, n=30):
    """A parabolic arc from p to q, bulging left of p->q.  TikZ has no straight-line
    'bend' primitive we can also sample, and the pairing arcs must clear the discs."""
    (px, py), (qx, qy) = p, q
    dx, dy = qx - px, qy - py
    L = math.hypot(dx, dy)
    cx, cy = (px + qx) / 2 - dy / L * 2 * bulge, (py + qy) / 2 + dx / L * 2 * bulge
    pts = [((1 - t) ** 2 * px + 2 * t * (1 - t) * cx + t * t * qx,
            (1 - t) ** 2 * py + 2 * t * (1 - t) * cy + t * t * qy)
           for t in (i / n for i in range(n + 1))]
    return polyline(pts, color=color, w=w, dash=dash)


def cross(x, y, r=20, color="accenttwo", w=5.0):
    return (seg((x - r, y - r), (x + r, y + r), color=color, w=w)
            + seg((x - r, y + r), (x + r, y - r), color=color, w=w))


def tick(x, y, h=26, color="accenttwo", w=5.0):
    return seg((x, y - h / 2), (x, y + h / 2), color=color, w=w)


def bar(x, y, h=60, w=9, color="accent"):
    return rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2, draw=None, fill=color)


def strip(x0, x1, y, share, h=44, fill="accenttwo", back="annot"):
    """A part-of-whole strip: the whole is drawn, the part is filled.  Not a bar chart --
    the scale is the strip itself, so there is nothing to decode against an axis."""
    assert 0 <= share <= 1
    return (rect(x0, y - h / 2, x0 + (x1 - x0) * share, y + h / 2, draw=None, fill=fill)
            + rect(x0, y - h / 2, x1, y + h / 2, draw=back, w=2.4))


def feld_body(pos=None, color="black", w=EDGE_W):
    pos = pos or POS
    return "".join(seg(pos[a], pos[b], color=color, w=w) for a, b in FELD_EDGES)


def feld_scaled(s, cx, cy):
    """The ONE layout, uniformly scaled into a narrower canvas.

    `feld-degrees` and `feld-two-numbers` sit in 537bp `cols` columns, where the 1080bp
    layout would be clipped.  A uniform scale is the same drawing, smaller -- the shape,
    the crossing count and the clearances are all preserved -- so the graph still cannot
    change shape between consecutive slides, which is what one shared layout is for.
    """
    x0 = (min(p[0] for p in POS.values()) + max(p[0] for p in POS.values())) / 2
    y0 = (min(p[1] for p in POS.values()) + max(p[1] for p in POS.values())) / 2
    return {n: (cx + (p[0] - x0) * s, cy + (p[1] - y0) * s) for n, p in POS.items()}


def assert_no_digits(strings, what):
    bad = [s for s in strings if any(c.isdigit() for c in s)]
    assert not bad, (f"{what}: a question-slide figure must not carry its own answer -- "
                     f"these strings hold numbers: {bad}")


def num(x, d=1):
    """A number formatted for the slide, rounded in decimal (see figlib.pct)."""
    from decimal import ROUND_HALF_UP, Decimal
    q = Decimal(repr(float(x))).quantize(Decimal("1" if d == 0 else "0." + "0" * d),
                                         rounding=ROUND_HALF_UP)
    return f"{q}"


# =========================================================================== Part One
def fig_timeline_1961():
    y = 200
    b = seg((60, y), (1020, y), color="annot", w=4.0)
    marks = [(250, "1961", "James Coleman surveys\\\\twelve high schools"),
             (830, "1991", "Scott Feld reopens\\\\one of them")]
    for x, year, who in marks:
        # 34bp, not 24: check_render counts a solid accent disc as a node and measures it
        # on the slide against the 26-52px band -- 24bp came back 23.5px and failed.
        b += dot(x, y, color="accent", d=34)
        b += text(x, y + 30, year, anchor="south", size=46)
        b += text(x, y - 30, who, anchor="north")
    b += text(540, y + 22, "30 years", color="annot", anchor="south")
    for _, year, _ in marks:
        assert year in b
    emit("timeline-1961", b, container="full", h=FULL_H)


def fig_feld_names():
    chosen, _ = solve_names()
    names = {n: n for n in POS}
    assert_no_digits(list(names.values()), "feld-names")
    b = feld_body()
    b += "".join(disc(*POS[n], fill="accent") for n in FELD_ORDER)
    b += draw_labels(names, POS, chosen)
    emit("feld-names", b, container="full", h=FULL_H)


def fig_feld_degrees():
    pos = feld_scaled(0.52, 268.5, 200)
    assert_planar_drawing(FELD_EDGES, pos, "feld-degrees (scaled)")
    drawn = {n: degree(n) for n in FELD_ORDER}
    assert sum(drawn.values()) == 2 * M["M"] == 20, drawn
    assert [drawn[n] for n in FELD_ORDER] == [1, 4, 4, 2, 3, 3, 2, 1]
    b = feld_body(pos)
    b += "".join(disc(*pos[n], str(drawn[n]), fill="accent") for n in FELD_ORDER)
    emit("feld-degrees", b, container="col", h=COL_H)


def fig_feld_worksheet():
    # The answer goes in the empty right-middle void; the solver is told to keep the
    # eight names out of it.  Nothing in this figure may carry a friend-mean value.
    void = [(800, 90, 1070, 250)]
    chosen, _ = solve_names(extra_blockers=void)
    names = {n: n for n in POS}
    b = feld_body()
    b += ring(*POS["Jane"], color="accenttwo", grow=16)
    b += "".join(disc(*POS[n], str(degree(n)), fill="accent") for n in FELD_ORDER)
    b += draw_labels(names, POS, chosen)
    b += seg((830, 108), (1050, 108), color="accenttwo", w=5.0)
    prompt = "her friends'\\\\average"
    b += text(940, 190, prompt, color="accenttwo")
    shown = list(names.values()) + [prompt]
    assert_no_digits(shown, "feld-worksheet")
    for v in POS:
        assert f"{friend_mean(v):.2f}" not in b, "feld-worksheet leaks a friend mean"
    emit("feld-worksheet", b, container="full", h=FULL_H)


def fig_feld_friendmeans():
    """The eight girls with their names, their degrees and their friends' means.

    Chips carry ONE decimal, which is what Feld's own Table 1 prints.  Two decimals plus
    the eight names is the one combination the label solver cannot place inside the
    356bp band: two-line "Betty\\\\4.00", one-line "Betty 4.0", and sixteen labels with
    two-decimal chips all raise.  Rounding to one decimal cannot change the story, and
    the assertion below is what says so rather than a comment claiming it.
    """
    fm = {n: friend_mean(n) for n in FELD_ORDER}
    chip = {n: num(fm[n], 1) for n in FELD_ORDER}
    assert [chip[n] for n in FELD_ORDER] == \
        ["4.0", "2.8", "3.0", "3.5", "3.3", "3.3", "2.0", "2.0"]
    # the below/above/equal reading must survive the rounding
    for n in FELD_ORDER:
        exact = (fm[n] > degree(n)) - (fm[n] < degree(n))
        shown = (float(chip[n]) > degree(n)) - (float(chip[n]) < degree(n))
        assert exact == shown, f"{n}: rounding {fm[n]} to {chip[n]} flips the comparison"

    colour = {}
    for n in FELD_ORDER:
        colour[n] = ("accenttwo" if n in BELOW else "accent" if n in ABOVE else "annot")
    assert sum(v == "accenttwo" for v in colour.values()) == len(BELOW) == 5
    assert sum(v == "accent" for v in colour.values()) == len(ABOVE) == 2
    assert sum(v == "annot" for v in colour.values()) == len(EQUAL) == 1

    # Sixteen labels sharing eight coordinates: the name and the chip are solved as
    # independent labels of the same disc, so each finds its own free side.
    pos2, lab = dict(POS), {}
    for n in FELD_ORDER:
        lab[n] = n
        pos2[n + "#"] = POS[n]
        lab[n + "#"] = chip[n]
    chosen, _ = place_labels(lab, pos2, FELD_EDGES, bounds=LABEL_BAND)

    b = feld_body()
    b += "".join(disc(*POS[n], str(degree(n)), fill=colour[n]) for n in FELD_ORDER)
    for key, (anc, dx, dy) in chosen.items():
        n = key.rstrip("#")
        b += text(POS[n][0] + dx, POS[n][1] + dy, lab[key], anchor=anc,
                  color=colour[n] if key.endswith("#") else "black")
    emit("feld-friendmeans", b, container="full", h=FULL_H)


def fig_feld_two_numbers():
    own, friends = float(M["k1"]), float(M["friend"])
    assert (own, friends) == (2.5, 3.0)
    b = ""
    rows = [(280, num(own, 1), "accent", "each girl", 320),
            (120, num(friends, 1), "accenttwo", "her friends", 280)]
    for y, v, col, lab, lead_x1 in rows:
        b += text(25, y, v, color=col, anchor="west", size=92)
        b += text(512, y, lab, color=col, anchor="east")
        b += seg((195, y), (lead_x1, y), color="annot", w=2.0, dash=DASH)
    emit("feld-two-numbers", b, container="col", h=COL_H)


def fig_marketville_146():
    n = sum(MARKETVILLE_PK.values())
    sum_k = sum(k * c for k, c in MARKETVILLE_PK.items())
    sum_k2 = sum(k * k * c for k, c in MARKETVILLE_PK.items())
    k1, friend = sum_k / n, sum_k2 / sum_k
    assert n == 146 == MARKETVILLE_BELOW + MARKETVILLE_ABOVE + MARKETVILLE_EQUAL
    assert num(k1, 1) == "2.7" and num(friend, 1) == "3.4"

    groups = [(MARKETVILLE_BELOW, "accenttwo", "below"),
              (MARKETVILLE_ABOVE, "accent", "above"),
              (MARKETVILLE_EQUAL, "annot", "equal")]
    # check_render measures discs on the RENDERED SLIDE against a 26-52px band, and 24bp
    # discs came back 23.5px -- under it.  28bp on a 32bp pitch is the smallest that
    # clears the floor and still lets three blocks and two gaps fit the canvas.
    rows, pitch, size, gap = 5, 32, 28, 50
    ncols = [math.ceil(c / rows) for c, _, _ in groups]
    widths = [(n - 1) * pitch + size for n in ncols]
    total = sum(widths) + gap * (len(groups) - 1)
    assert total <= 1060, f"the block is {total}bp wide and would touch the canvas edge"
    b, x, drawn = "", (1080 - total) / 2 + size / 2, 0
    for (count, col, lab), n_, wide in zip(groups, ncols, widths):
        for i in range(count):
            b += disc(x + (i // rows) * pitch, 150 + (i % rows) * pitch,
                      fill=col, size=size)
            drawn += 1
        b += text(x + (n_ - 1) * pitch / 2, 95, f"{count} {lab}", color=col)
        x += wide + gap
    assert drawn == 146
    b += text(540, 330, f"{num(k1,1)} friends each, {num(friend,1)} per friend")
    emit("marketville-146", b, container="full", h=FULL_H)


# =========================================================================== Part Two
def fig_degree_def():
    cx, cy = 268, 215
    leaves = [(cx - 190, cy + 92), (cx + 190, cy + 92),
              (cx - 190, cy - 92), (cx + 190, cy - 92)]
    b = "".join(seg((cx, cy), p) for p in leaves)
    b += "".join(disc(*p, fill="annot") for p in leaves)
    b += disc(cx, cy, fill="accenttwo")
    for i, (lx, ly) in enumerate(leaves, start=1):
        mx, my = (cx + lx) / 2, (cy + ly) / 2
        b += text(mx, my + (26 if ly > cy else -26), str(i), color="accenttwo")
    assert len(leaves) == 4
    b += text(cx, cy - 165, f"degree {len(leaves)}", color="accenttwo")
    emit("degree-def", b, container="col", h=COL_H)


def fig_sum_ends():
    b = feld_body()
    ends = 0
    for a, c in FELD_EDGES:
        for p, q in ((POS[a], POS[c]), (POS[c], POS[a])):
            d = np.array(q, float) - np.array(p, float)
            d /= np.linalg.norm(d)
            m = np.array(p, float) + d * 44
            n_ = np.array([-d[1], d[0]])
            b += seg(tuple(m - n_ * 13), tuple(m + n_ * 13), color="accenttwo", w=5.0)
            ends += 1
    assert ends == 2 * M["M"] == 20
    b += "".join(disc(*POS[n], fill="accent") for n in FELD_ORDER)
    b += text(540, 45, f"{M['M']} lines, {ends} ends", color="accenttwo")
    emit("sum-ends", b, container="full", h=FULL_H)


def fig_mean_degree():
    ends, girls = 2 * M["M"], M["N"]
    assert ends == 20 and girls == 8 and float(M["k1"]) == ends / girls
    b = text(268, 322, f"{ends} ends")
    b += "".join(tick(35 + i * 24, 258, h=34) for i in range(ends))
    b += seg((268, 232), (268, 190), color="annot", w=3.0, arrow=ARROW)
    b += "".join(disc(60 + i * 60, 150, fill="accent") for i in range(girls))
    b += text(268, 100, f"{girls} girls")
    b += text(268, 45, f"{num(float(M['k1']), 1)} each", color="accenttwo", size=56)
    emit("mean-degree", b, container="col", h=COL_H)


def fig_handshake():
    xs = [140, 540, 940]
    pairs = [(0, 1)]
    left = [i for i in range(len(xs)) if not any(i in p for p in pairs)]
    assert len(xs) % 2 == 1 and 2 * len(pairs) + len(left) == len(xs) and len(left) == 1
    b = ""
    for i, j in pairs:
        b += arc((xs[i], 190), (xs[j], 190), bulge=62)
    k = xs[left[0]]
    b += polyline([(k, 190), (k, 250), (k, 268)], color="accenttwo", w=3.4, dash=DASH)
    b += cross(k, 300, r=22)
    b += "".join(disc(x, 170, fill="accent") for x in xs)
    b += text(540, 110, f"{len(xs)} nodes of odd degree", color="annot")
    b += text(940, 350, "no partner", color="accenttwo")
    emit("handshake", b, container="full", h=FULL_H)


def fig_pk_def():
    # Deliberately NOT the eight girls: `feld-pk` two slides later is that figure, and a
    # definition slide sharing its picture with the worked example teaches nothing twice.
    heights = [2, 5, 4, 1]
    total = sum(heights)
    assert total == 12
    b = ""
    for c, hgt in enumerate(heights):
        x = 70 + c * 130
        for r in range(hgt):
            b += disc(x, 140 + r * 48, fill="accent")
        b += text(x, 100, str(c + 1))
    b += text(265, 45, "$k$")
    b += text(25, 236, "nodes", color="annot", rot=90)
    emit("pk-def", b, container="col", h=COL_H)


def fig_feld_pk():
    by_k = {}
    for v in FELD_ORDER:
        by_k.setdefault(degree(v), []).append(v)
    assert sorted(by_k) == [1, 2, 3, 4] and all(len(v) == 2 for v in by_k.values())
    share = f"{len(by_k[1])}/{M['N']}"
    b = ""
    for i, k in enumerate(sorted(by_k)):
        x = 90 + i * 260
        for j, v in enumerate(by_k[k]):
            y = 250 - j * 62
            b += disc(x, y, str(k), fill="accent")
            b += text(x + 30, y, v, anchor="west")
        b += text(x, 140, f"$k = {k}$", color="annot", anchor="north")
    b += text(540, 340, f"$p(k) = {share} = 1/4$ at every $k$", color="accenttwo")
    emit("feld-pk", b, container="full", h=FULL_H)


def fig_rosters():
    lists = {v: sorted(G.neighbors(v)) for v in FELD_ORDER}
    counts = {v: sum(v in lst for lst in lists.values()) for v in FELD_ORDER}
    assert counts == {v: degree(v) for v in FELD_ORDER}
    assert sum(counts.values()) == 20
    hubs = [v for v in FELD_ORDER if degree(v) == max(counts.values())]
    assert hubs == ["Sue", "Alice"]

    # Eight free-standing rosters, not a ruled table.  The header row and the two rules
    # of the first version made this the format the rubric calls the worst one; each list
    # now hangs from its owner's own disc -- the same disc every Feld figure draws --
    # carrying the number of lists she turns up on. That the count and the degree are one
    # number is the point of the slide, so they are one mark.
    b = ""
    for i, v in enumerate(FELD_ORDER):
        x = 85 + i * 130
        b += text(x, 332, v)
        b += disc(x, 282, str(counts[v]), fill="accenttwo" if v in hubs else "accent")
        for j, u in enumerate(lists[v]):
            b += text(x, 222 - j * 45, u,
                      color="accenttwo" if u in hubs else "annot")
    emit("rosters", b, container="full", h=FULL_H)


# ========================================================================= Part Three
def fig_bag_of_hands():
    owners = []
    for v in FELD_ORDER:
        owners += [v] * degree(v)
    assert len(owners) == 2 * M["M"] == 20
    b = rect(45, 62, 492, 338, draw="annot", w=3.4, rounded=20)
    for i, v in enumerate(owners):
        x, y = 90 + (i % 5) * 88, 296 - (i // 5) * 62
        b += disc(x, y, v[0], fill="accenttwo" if v == "Sue" else "accent")
    assert sum(1 for v in owners if v == "Sue") == degree("Sue") == 4
    b += text(150, 372, f"{len(owners)} ends")
    b += text(390, 372, f"{degree('Sue')} are Sue's", color="accenttwo")
    emit("bag-of-hands", b, container="col", h=COL_H)


def fig_qk_formula():
    ends, k = 2 * M["M"], degree("Sue")
    assert (ends, k) == (20, 4)
    b = "".join(bar(35 + i * 24, 155, h=64,
                    color="accenttwo" if i < k else "accent") for i in range(ends))
    x0, x1 = 35 - 6, 35 + (k - 1) * 24 + 6
    b += polyline([(x0, 196), (x0, 206), (x1, 206), (x1, 196)], color="accenttwo", w=3.4)
    b += text((x0 + x1) / 2, 240, "Sue", color="accenttwo")
    b += text(268, 68, f"{k} ends of {ends}", color="accenttwo")
    emit("qk-formula", b, container="col", h=COL_H)


# lmex10 -- the math EXTENSION font -- does not scale with \fontsize in this preamble:
# at 36pt a \sum, \int or \prod still draws at its 10pt natural size, silently, with no
# "not available" line in the log for figlib.render() to catch.  A capital \Sigma comes
# from the letters font, which does scale, so the operator is built from that instead.
SUM_K = r"\mathop{\scalebox{1.35}{$\Sigma$}}\limits_{k}"

_DERIV = [
    r"$\displaystyle \langle k\rangle_{\mathrm{friend}} = " + SUM_K + r" k\,q(k) "
    r"= \frac{\langle k^2\rangle}{\langle k\rangle}$",
    r"$\displaystyle \langle k^2\rangle = \mathrm{Var}(k) + \langle k\rangle^2$",
    r"$\displaystyle \langle k\rangle_{\mathrm{friend}} = \langle k\rangle "
    r"+ \frac{\mathrm{Var}(k)}{\langle k\rangle}$",
]
_GLOSS = ["average over ends", r"rewrite $\langle k^2\rangle$", "the theorem"]
_DERIV_Y = [278, 186, 92]


def _derivation(upto):
    """One figure in three states: the same frame, the same left margin, one line more.

    Each state's body is a prefix of the next, so everything above the added line is
    identical by construction rather than by inspection.
    """
    b = rect(58, 32, 1022, 342, draw="annot", w=2.4, rounded=10)
    for i in range(upto):
        b += text(110, _DERIV_Y[i], str(i + 1), color="annot")
        if i == 2:
            b += (f"\\node[font=\\fontsize{{{FONT}}}{{{int(FONT*1.15)}}}\\selectfont,"
                  f"text=black,anchor=west,align=center] (eqthree) at "
                  f"(178,{_DERIV_Y[i]}) {{{_DERIV[i]}}};\n"
                  f"\\node[draw=accenttwo,line width=3.4bp,rounded corners=8bp,"
                  f"fit=(eqthree),inner sep=13bp] {{}};\n")
        else:
            b += text(178, _DERIV_Y[i], _DERIV[i], anchor="west")
        b += text(680, _DERIV_Y[i], _GLOSS[i], color="annot", anchor="west")
    return b


def fig_derivation_1():
    emit("derivation-1", _derivation(1), container="full", h=FULL_H)


def fig_derivation_2():
    assert _derivation(2).startswith(_derivation(1))
    emit("derivation-2", _derivation(2), container="full", h=FULL_H)


def fig_derivation_3():
    assert _derivation(3).startswith(_derivation(2))
    emit("derivation-3", _derivation(3), container="full", h=FULL_H)


def fig_gap_nonneg():
    zero = 170
    b = seg((30, 200), (zero, 200), color="annot", w=3.0, dash=DASH)
    b += seg((zero, 200), (505, 200), color="accenttwo", w=5.0, arrow=ARROW)
    b += seg((zero, 186), (zero, 214), color="black", w=3.0)
    b += text(zero, 180, "0", anchor="north")
    b += text(190, 105, "all degrees\\\\equal", color="annot")
    b += text(95, 250, "never", color="annot")
    b += text(345, 250, "always here", color="accenttwo")
    b += text(300, 310, r"$\mathrm{Var}(k)/\langle k\rangle$")
    emit("gap-nonneg", b, container="col", h=COL_H)


def fig_feld_check():
    k1, k2, var, gap = (float(M["k1"]), float(M["k2"]), float(M["var"]), float(M["gap"]))
    assert (k1, k2, var, gap) == (2.5, 7.5, 1.25, 0.5)
    assert k1 + gap == float(M["friend"]) == 3.0
    assert M["sum_k2"] == 60 and M["sum_k"] == 20
    assert M["sum_k2"] / M["sum_k"] == 3.0
    ans = num(k1 + gap, 1)

    b = text(200, 342, "the identity", color="annot")
    b += text(880, 342, "the hand count", color="annot")
    for y, l, r in ((278, rf"$\langle k^2\rangle = {num(k2,1)}$",
                     f"{M['sum_k']} ends"),
                    (218, rf"$\mathrm{{Var}}(k) = {num(var,2)}$",
                     f"{M['sum_k2']} friends"),
                    (158, f"${num(k1,1)} + {num(gap,1)}$",
                     f"${M['sum_k2']} \\div {M['sum_k']}$")):
        b += text(200, y, l)
        b += text(880, y, r)
    b += seg((380, 240), (462, 240), color="annot", w=3.0, arrow=ARROW)
    b += seg((700, 240), (618, 240), color="annot", w=3.0, arrow=ARROW)
    b += text(540, 240, ans, color="accenttwo", size=88)
    b += text(540, 150, "friends' average", color="annot")
    emit("feld-check", b, container="full", h=FULL_H)


def fig_two_averages():
    per_end = float(M["friend"])
    per_person = float(np.mean([float(friend_mean(v)) for v in FELD_ORDER]))
    assert per_end == 3.0 and abs(per_person - 2.9896) < 1e-4
    ends, girls = 2 * M["M"], M["N"]

    b = seg((530, 60), (530, 330), color="annot", w=2.0)
    b += text(280, 318, "pick an edge end")
    b += "".join(tick(70 + i * 22, 218, h=40) for i in range(ends))
    b += text(280, 90, num(per_end, 2), color="accenttwo", size=88)
    b += text(790, 318, "pick a person")
    b += "".join(disc(600 + i * 54, 218, fill="accent") for i in range(girls))
    b += text(790, 90, num(per_person, 2), color="accent", size=88)
    emit("two-averages", b, container="full", h=FULL_H)


_STAR = nx.star_graph(3)
_RING = nx.cycle_graph(6)
_STAR_POS = {0: (250, 230), 1: (110, 150), 2: (110, 310), 3: (392, 230)}
_RING_POS = {i: (790 + 190 * math.cos(math.radians(a)), 230 + 95 * math.sin(math.radians(a)))
             for i, a in enumerate(range(0, 360, 60))}


def _star_ring_body():
    assert_planar_drawing(list(_STAR.edges()), _STAR_POS, "worksheet star")
    assert_planar_drawing(list(_RING.edges()), _RING_POS, "worksheet ring")
    b = "".join(seg(_STAR_POS[a], _STAR_POS[c]) for a, c in _STAR.edges())
    b += "".join(seg(_RING_POS[a], _RING_POS[c]) for a, c in _RING.edges())
    return b


def fig_worksheet_star_ring():
    b = _star_ring_body()
    b += "".join(disc(*_STAR_POS[n], fill="accent") for n in _STAR)
    b += "".join(disc(*_RING_POS[n], fill="accent") for n in _RING)
    q = r"$\mathrm{Var}(k)/\langle k\rangle$"
    b += text(250, 78, q)
    b += text(790, 78, q)
    b += seg((150, 32), (350, 32), color="accenttwo", w=5.0)
    b += seg((690, 32), (890, 32), color="accenttwo", w=5.0)
    assert_no_digits([q], "worksheet-star-ring")
    for bad in ("0.5", "0.50", "= 0$", "zero"):
        assert bad not in b, f"worksheet-star-ring leaks the answer ({bad})"
    emit("worksheet-star-ring", b, container="full", h=FULL_H)


def fig_worksheet_answer():
    ms, mr = moments(_STAR), moments(_RING)
    assert float(ms["gap"]) == 0.5 and float(mr["gap"]) == 0.0
    b = _star_ring_body()
    b += "".join(disc(*_STAR_POS[n], str(_STAR.degree(n)), fill="accent") for n in _STAR)
    b += "".join(disc(*_RING_POS[n], str(_RING.degree(n)), fill="accent") for n in _RING)
    q = r"$\mathrm{Var}(k)/\langle k\rangle = "
    b += text(250, 70, q + num(float(ms["gap"]), 1) + "$", color="accenttwo")
    b += text(790, 70, q + num(float(mr["gap"]), 0) + "$", color="accenttwo")
    emit("worksheet-answer", b, container="full", h=FULL_H)


# ========================================================================== Part Four
@lru_cache(maxsize=None)
def _condmat_stats():
    g = condmat()
    return net_stats(g), paradox_share(g)


def fig_coauthor_gap():
    s, share = _condmat_stats()
    assert s["N"] == 23133
    assert num(s["k1"], 1) == "8.1" and num(s["friend"], 1) == "22.1"
    b = text(250, 300, num(s["k1"], 1), color="accent", size=88)
    b += text(830, 300, num(s["friend"], 1), color="accenttwo", size=88)
    b += seg((420, 300), (660, 300), color="annot", w=3.4, arrow=ARROW)
    b += text(250, 228, "each author", color="annot")
    b += text(830, 228, "their coauthors", color="annot")
    x0, x1 = 90, 990
    b += strip(x0, x1, 140, share)
    b += text(x0 + (x1 - x0) * share - 24, 140, pct(share, 1), color="white",
              anchor="east")
    b += text(x0, 68, "below their coauthors' average", color="annot", anchor="west")
    emit("coauthor-gap", b, container="full", h=FULL_H)


def fig_fb_twitter():
    assert "92.7% of users have less friends than the average" in LITERATURE
    assert "83.6% of users have less friends than the median" in LITERATURE
    assert ">98% of Twitter users" in LITERATURE
    rows = [(300, "Facebook mean", 0.927, "92.7"),
            (200, "Facebook median", 0.836, "83.6"),
            (100, "Twitter", 0.98, r"$>$98")]
    x0, x1 = 430, 1030
    b = ""
    for y, lab, share, shown in rows:
        b += text(400, y, lab, anchor="east")
        b += strip(x0, x1, y, share)
        b += text(x0 + (x1 - x0) * share - 24, y, shown + "\\%", color="white",
                  anchor="east")
    assert [f"{r[2]*100:g}" in r[3] or ">" in r[3] for r in rows] == [True] * 3
    emit("fb-twitter", b, container="full", h=FULL_H)


_SB = nx.Graph()
_SB.add_edges_from([("H", i) for i in range(6)] + [(0, 1), (2, 3), (4, 5)])
_SB_POS = {"H": (250, 205)}
_SB_POS.update({i: (250 + 165 * math.cos(math.radians(a)),
                    205 + 90 * math.sin(math.radians(a)))
                for i, a in enumerate(range(0, 360, 60))})


def fig_sampling_bias():
    assert_planar_drawing(list(_SB.edges()), _SB_POS, "sampling-bias")
    n, m = _SB.number_of_nodes(), _SB.number_of_edges()
    kh, ends = _SB.degree("H"), 2 * _SB.number_of_edges()
    factor = kh / (ends / n)
    assert (n, ends, kh) == (7, 18, 6) and abs(factor - 7 / 3) < 1e-9

    b = "".join(seg(_SB_POS[a], _SB_POS[c]) for a, c in _SB.edges())
    b += "".join(disc(*_SB_POS[i], fill="accent") for i in range(6))
    b += disc(*_SB_POS["H"], fill="accenttwo")
    b += text(250, 60, "the hub", color="accenttwo")
    for y, lab, tot, hit in ((320, "pick a person", n, 1), (190, "follow an edge", ends, kh)):
        b += text(790, y, lab)
        pitch = 425 / (tot - 1)
        for i in range(tot):
            b += dot(560 + i * pitch, y - 50, color="accenttwo" if i < hit else "accent")
    b += text(790, 60, f"${num(factor,1)}\\times$ more often", color="accenttwo")
    emit("sampling-bias", b, container="full", h=FULL_H)


_ACQ = {"H": (0, 18), 1: (-118, -58), 2: (-40, 112), 3: (118, -58), 4: (52, 112)}


def fig_acquaintance():
    steps = [(200, "pick anyone", 1), (540, "name a friend", None), (880, "immunise them", 0)]
    b = ""
    for cx, lab, _ in steps:
        for k in (1, 2, 3, 4):
            b += seg((cx + _ACQ["H"][0], 205 + _ACQ["H"][1]),
                     (cx + _ACQ[k][0], 205 + _ACQ[k][1]), w=2.4)
        for k in (1, 2, 3, 4):
            b += disc(cx + _ACQ[k][0], 205 + _ACQ[k][1], fill="accent", size=SMALLNODE)
        b += disc(cx + _ACQ["H"][0], 205 + _ACQ["H"][1], fill="accent", size=SMALLNODE)
        b += text(cx, 68, lab)
    # 1: the random pick.  2: the nomination travelling up the edge.  3: the hub treated.
    b += ring(200 + _ACQ[1][0], 205 + _ACQ[1][1], size=SMALLNODE, grow=14)
    # the nomination travels along the edge itself, stopping at both discs' borders
    p = np.array([540 + _ACQ[1][0], 205 + _ACQ[1][1]], float)
    q = np.array([540 + _ACQ["H"][0], 205 + _ACQ["H"][1]], float)
    u = (q - p) / np.linalg.norm(q - p)
    b += seg(tuple(p + u * (SMALLNODE / 2 + 2)), tuple(q - u * (SMALLNODE / 2 + 8)),
             color="accenttwo", w=4.4, arrow=ARROW)
    b += disc(880, 223, fill="accenttwo", size=SMALLNODE)
    b += ring(880, 223, size=SMALLNODE, grow=14)
    emit("acquaintance", b, container="full", h=FULL_H)


IMM_F = (0.0, 0.02, 0.04, 0.06, 0.08, 0.10)
IMM_SEEDS = tuple(range(1, 13))


@lru_cache(maxsize=None)
def _imm():
    """Twelve realisations, averaged.

    One realisation of `random` is noisy enough to run UPWARDS as more nodes are
    immunised (0.947 at f = 0.02 against 0.953 at f = 0.04 on the module's default
    seed), which is a visible lie on a monotone process.  Averaging removes it and
    the curves come out monotone, which is asserted below.
    """
    g = internet_as()
    runs = [immunization_curves(g, list(IMM_F), seed=s) for s in IMM_SEEDS]
    out = {k: [float(np.mean([r[k][i] for r in runs])) for i in range(len(IMM_F))]
           for k in ("random", "acquaintance", "degree")}
    for k, v in out.items():
        assert v[0] == 1.0, k
        assert all(a >= b - 1e-12 for a, b in zip(v, v[1:])), f"{k} is not monotone: {v}"
    return out


def fig_immunization_curves():
    c = _imm()
    at10 = {k: v[-1] for k, v in c.items()}
    assert IMM_F[-1] == 0.10
    assert at10["random"] > at10["acquaintance"] > at10["degree"]

    ax = Axes((124, 132, 310, 312), (0, 0.10), (0.001, 1), ylog=True,
              xticks=[0, 0.05, 0.10], yticks=[0.001, 0.01, 0.1, 1],
              xfmt=lambda v: f"{v:g}", yfmt=lambda v: pct(v, 1 if v < 0.01 else 0),
              xlabel="fraction immunised")
    b = ax.frame()
    series = [("random", "accent", f"random {pct(at10['random'])}"),
              ("acquaintance", "accenttwo", f"named {pct(at10['acquaintance'])}"),
              ("degree", "annot", "targeted")]
    for key, col, lab in series:
        ys = c[key]
        b += ax.line(IMM_F, ys, color=col, w=3.6,
                     dash=DASH if key == "degree" else "")
        b += ax.points(IMM_F, ys, color=col, d=11)
        b += text(318, ax.Y(ys[-1]), lab, color=col, anchor="west")
    emit("immunization-curves", b, container="col", h=COL_H)


FIGURES = [
    ("timeline-1961", fig_timeline_1961),
    ("feld-names", fig_feld_names),
    ("feld-degrees", fig_feld_degrees),
    ("feld-worksheet", fig_feld_worksheet),
    ("feld-friendmeans", fig_feld_friendmeans),
    ("feld-two-numbers", fig_feld_two_numbers),
    ("marketville-146", fig_marketville_146),
    ("degree-def", fig_degree_def),
    ("sum-ends", fig_sum_ends),
    ("mean-degree", fig_mean_degree),
    ("handshake", fig_handshake),
    ("pk-def", fig_pk_def),
    ("feld-pk", fig_feld_pk),
    ("rosters", fig_rosters),
    ("bag-of-hands", fig_bag_of_hands),
    ("qk-formula", fig_qk_formula),
    ("derivation-1", fig_derivation_1),
    ("derivation-2", fig_derivation_2),
    ("derivation-3", fig_derivation_3),
    ("gap-nonneg", fig_gap_nonneg),
    ("feld-check", fig_feld_check),
    ("two-averages", fig_two_averages),
    ("worksheet-star-ring", fig_worksheet_star_ring),
    ("worksheet-answer", fig_worksheet_answer),
    ("coauthor-gap", fig_coauthor_gap),
    ("fb-twitter", fig_fb_twitter),
    ("sampling-bias", fig_sampling_bias),
    ("acquaintance", fig_acquaintance),
    ("immunization-curves", fig_immunization_curves),
]
