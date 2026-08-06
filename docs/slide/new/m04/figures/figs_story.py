#!/usr/bin/env python3
"""Parts 1-4 of the Module 04 deck: Marketville, counting ends, the exact gap, using it.

Twenty-nine figures.  Every drawing primitive comes from `figlib`, the eight girls'
one shared layout from `feld`, and every printed number from `verify_numbers` -- nothing
here types a value that the data can produce.

Containers are read off the deck's own markup (`m04-node-degree.md`), not off the spec
table: `feld-degrees` and `feld-two-numbers` sit in `cols` columns there, and a figure
authored for 1080bp and dropped into a 537bp column renders at 48% of its intended scale.
"""

import itertools
import math
import re
from functools import lru_cache

import networkx as nx
import numpy as np

from feld import ABOVE, BELOW, EQUAL, G, LABEL_BAND, M, POS, degree, friend_mean, solve_names
from figlib import (ACCENT2, DASH, EDGE_W, FONT, NODE, PXBP, SMALLNODE,
                    TEXT_MIN_PX, Axes,
                    assert_planar_drawing, clearance_bad, disc, dot, draw_labels, emit,
                    pct, place_labels, polyline, rect, render, ring, scene_clear,
                    seg,
                    text)
from verify_numbers import (FELD_EDGES, FELD_ORDER, LITERATURE, MARKETVILLE_ABOVE,
                            MARKETVILLE_BELOW, MARKETVILLE_EQUAL, MARKETVILLE_PK,
                            condmat, immunization_curves, internet_as, moments,
                            net_stats, paradox_share)

FULL_H = 420          # page height for a full-width figure; the crop trims it to the ink
COL_H = 400

ARROW = "-{Stealth[length=13bp,width=9bp]}"


# --------------------------------------------------------------------------- helpers
def cross(x, y, r=20, color="accenttwo", w=5.0):
    return (seg((x - r, y - r), (x + r, y + r), color=color, w=w)
            + seg((x - r, y + r), (x + r, y - r), color=color, w=w))


# ONE edge-end glyph for the whole module (R1 A-6).  Reviewer B measured the same
# object at 8x63px on slide 028 and 4x39px on 034, in a deck that otherwise keeps its
# objects stable.  Every figure that draws an edge end -- sum-ends, mean-degree,
# qk-formula, rosters, two-averages -- draws THIS mark.  Spacing is a per-figure layout
# choice; the mark is not.
END_W, END_H = 6.0, 34


def end_mark(x, y, color="accenttwo"):
    return seg((x, y - END_H / 2), (x, y + END_H / 2), color=color, w=END_W)


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


# --------------------------------------------------------------- the one role table
# R4 A4-1: three rounds addressed this by recolouring one figure at a time, and each
# time the sibling twelve lines below kept the opposite key -- accent-2 meant "above her
# friends' average" on slide 010 and "below" on 012, on the slide built to confirm the
# result at eighteen times the scale.  A role written into one function binds nothing.
# It is declared once here, both figures draw through `role_disc`, and
# `assert_role_consistency` fails the build if any two figures disagree about what a
# colour means.
ABOVE_FRIENDS = "accenttwo"   # her friends average FEWER than she has -- the hubs
BELOW_FRIENDS = None          # hollow: legible as "not red", carrying no second meaning
EQUAL_FRIENDS = "annot"       # exactly equal

_FRIEND_ROLE = {"above": ABOVE_FRIENDS, "below": BELOW_FRIENDS, "equal": EQUAL_FRIENDS}
_ROLE_LOG = {}


def friend_role(rel, what):
    """The single place a below/above/equal group becomes a way of drawing a disc."""
    assert rel in _FRIEND_ROLE, rel
    role = _FRIEND_ROLE[rel]
    seen, first = _ROLE_LOG.setdefault(role, (rel, what))
    assert seen == rel, (
        f"{what} draws '{rel}' the way {first} draws '{seen}' -- one colour, two "
        f"meanings, across two figures. Change the role table, not the call site.")
    return role


def role_disc(x, y, role, label="", size=NODE):
    """A disc in one of the three roles.  Hollow is a white disc with an ink ring, and
    the count rides inside the node: a separate text() would be recorded by the
    collision gate and the edges underneath it are rules."""
    if role is BELOW_FRIENDS:
        return (disc(x, y, label, fill="white", text_col="black", size=size)
                + ring(x, y, size=size, color="black", w=3.0, grow=0))
    return disc(x, y, label, fill=role, size=size)


_DISC_RE = re.compile(r"disc,fill=(\w+),minimum size=[\d.]+bp")


def assert_role_counts(body, expect, what):
    """Count the discs the body actually DRAWS, by role, and check them against the data.

    `friend_role` centralises the table but cannot see a call site that bypasses it,
    which is precisely what happened: `fig_marketville_146` hardcoded the colours and no
    amount of declaring changed that.  This counts fills in the emitted TeX, so it holds
    whatever route drew them -- and it is the check that fails if the 80 "below" girls
    are ever drawn in the 41 "above" colour again.
    """
    fills = {}
    for m in _DISC_RE.finditer(body):
        fills[m.group(1)] = fills.get(m.group(1), 0) + 1
    got = {"above": fills.get(ABOVE_FRIENDS, 0),
           "below": fills.get("white", 0),
           "equal": fills.get(EQUAL_FRIENDS, 0)}
    assert got == expect, (
        f"{what}: the drawing holds {got} where the data says {expect} -- a group is "
        f"being drawn in another group's colour. Fix the role table, not the figure.")



# =========================================================================== Part One
def assert_ink_components(body, w, h, colour, n, what):
    """Render the figure and count connected components of one drawn colour.

    R2 A2-1: `sum-ends.png` printed "20 ends" and rendered THIRTEEN marks -- three of
    Sue's four ticks had fused into a single chevron, and so had Alice's, at exactly the
    two hubs the module is about.  Every gate in the build was green, because they all
    measure what the generator intended rather than what the page shows.  A figure that
    prints a count now has that count checked on the pixels.
    """
    a = np.asarray(render(body, w, h).convert("RGB")).astype(int)
    rgb = np.array([int(colour[i:i + 2], 16) for i in (0, 2, 4)])
    mask = np.abs(a - rgb).sum(axis=2) < 90
    seen = np.zeros(mask.shape, bool)
    H, W = mask.shape
    comps = 0
    for y0, x0 in zip(*np.where(mask)):
        if seen[y0, x0]:
            continue
        comps += 1
        stack = [(y0, x0)]
        seen[y0, x0] = True
        while stack:
            y, x = stack.pop()
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < H and 0 <= nx < W and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
    assert comps == n, (f"{what}: the drawing prints {n} but renders {comps} separate "
                        f"marks -- adjacent ones have fused. Push them further apart; "
                        f"do not shrink them.")


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
    b += text(540, y + 22, "30 years", color="annot", anchor="south", size=40)
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
    """R1 A-9: full width, so the eight-girl graph never changes scale across the build.

    This was a `cols` column, where the shared 830x200bp layout had to be scaled 0.52 to
    fit -- so the edges halved against unchanged 40bp discs on slide 008 and sprang back
    on 010.  The deck now lays 008 out full width (D-2) and the layout is used unscaled,
    which is the assertion below: this figure draws POS itself, not a copy of it.
    """
    assert_planar_drawing(FELD_EDGES, POS, "feld-degrees")
    drawn = {n: degree(n) for n in FELD_ORDER}
    assert sum(drawn.values()) == 2 * M["M"] == 20, drawn
    assert [drawn[n] for n in FELD_ORDER] == [1, 4, 4, 2, 3, 3, 2, 1]
    chosen, _ = solve_names()
    b = feld_body()
    b += "".join(disc(*POS[n], str(drawn[n]), fill="accent") for n in FELD_ORDER)
    b += draw_labels({n: n for n in POS}, POS, chosen)
    emit("feld-degrees", b, container="full", h=FULL_H)


def fig_feld_worksheet():
    # The answer goes in the empty right-middle void; the solver is told to keep the
    # eight names out of it.  Nothing in this figure may carry a friend-mean value.
    void = [(788, 90, 1072, 250)]
    chosen, _ = solve_names(extra_blockers=void)
    names = {n: n for n in POS}
    b = feld_body()
    b += ring(*POS["Jane"], color="accenttwo", grow=16)
    b += "".join(disc(*POS[n], str(degree(n)), fill="accent") for n in FELD_ORDER)
    b += draw_labels(names, POS, chosen)
    b += seg((830, 108), (1050, 108), color="accenttwo", w=5.0)
    # R1 A-11: name Jane in the prompt, so the ring round her disc has a stated reason.
    prompt = "Jane's friends'\\\\average"
    b += text(930, 190, prompt, color="accenttwo")
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

    # R3 A3-1: accent-2 is the node we are counting, or the hub -- the role it carries
    # on 014, 023, 026 and 027.  It used to mark the five girls whose friends have more,
    # which put Sue and Alice, the two hubs, in accent one slide before 023 drew them in
    # accent-2; the deck then had to state the opposite key twice.  Above the line is
    # filled accent-2, below is a hollow disc, and equal stays gray, so this figure
    # spends no colour on a meaning any other figure has taken.
    assert ABOVE == ["Sue", "Alice"], ABOVE
    rel = {n: ("above" if n in ABOVE else "equal" if n in EQUAL else "below")
           for n in FELD_ORDER}
    colour = {n: friend_role(rel[n], "feld-friendmeans") for n in FELD_ORDER}
    assert sum(v == ABOVE_FRIENDS for v in colour.values()) == len(ABOVE) == 2
    assert sum(v is BELOW_FRIENDS for v in colour.values()) == len(BELOW) == 5
    assert sum(v == EQUAL_FRIENDS for v in colour.values()) == len(EQUAL) == 1

    # Sixteen labels sharing eight coordinates: the name and the chip are solved as
    # independent labels of the same disc, so each finds its own free side.
    pos2, lab = dict(POS), {}
    for n in FELD_ORDER:
        lab[n] = n
        pos2[n + "#"] = POS[n]
        lab[n + "#"] = chip[n]
    chosen, _ = place_labels(lab, pos2, FELD_EDGES, bounds=LABEL_BAND)

    b = feld_body()
    for n in FELD_ORDER:
        b += role_disc(*POS[n], colour[n], str(degree(n)))
    for key, (anc, dx, dy) in chosen.items():
        n = key.rstrip("#")
        b += text(POS[n][0] + dx, POS[n][1] + dy, lab[key], anchor=anc,
                  color=(colour[n] or "black") if key.endswith("#") else "black")
    assert_role_counts(b, {"above": len(ABOVE), "below": len(BELOW), "equal": len(EQUAL)},
                       "feld-friendmeans")
    emit("feld-friendmeans", b, container="full", h=FULL_H)


def fig_feld_two_numbers():
    own, friends = float(M["k1"]), float(M["friend"])
    assert (own, friends) == (2.5, 3.0)
    b = ""
    # R3 A3-9: the girls' own mean is ink, not accent. Every other figure in the
    # build spends accent on a role (the hub, the node being counted), and a
    # second encoding of 2.5 as "blue" collided with it. Only the number this
    # slide is about is coloured.
    # The labels name the SAMPLING, not the object. "her friends" was true of both
    # numbers -- the room's 2.99 is the mean of eight per-girl means and Feld's 3.0 is
    # the mean over the twenty friendships -- so it labelled the one thing that does not
    # tell them apart. Same distinction `two-averages.png` draws in Part Three.
    # Labels left-aligned at a common x, so the two leaders are the same length. Hung
    # off the right edge instead, one came out 135bp and the other 20bp and the pair
    # read as a broken rule rather than as two rows of one table.
    rows = [(280, num(own, 1), "black", "per girl"),
            (120, num(friends, 1), "accenttwo", "per friendship")]
    for y, v, col, lab in rows:
        b += text(25, y, v, color=col, anchor="west", size=92)
        b += text(270, y, lab, color="annot", anchor="west")
        b += seg((195, y), (255, y), color="annot", w=2.0, dash=DASH)
    emit("feld-two-numbers", b, container="col", h=COL_H)


def fig_marketville_146():
    n = sum(MARKETVILLE_PK.values())
    sum_k = sum(k * c for k, c in MARKETVILLE_PK.items())
    sum_k2 = sum(k * k * c for k, c in MARKETVILLE_PK.items())
    k1, friend = sum_k / n, sum_k2 / sum_k
    assert n == 146 == MARKETVILLE_BELOW + MARKETVILLE_ABOVE + MARKETVILLE_EQUAL
    assert num(k1, 1) == "2.7" and num(friend, 1) == "3.4"

    # R4 A4-1: this block is the largest single piece of ink in Part One and it used to
    # hardcode the opposite key to slide 010's, so read with 010's legend it said eighty
    # girls were ahead of their friends -- the module's thesis, inverted, on the slide
    # built to confirm it. The roles come from the table now.
    groups = [(MARKETVILLE_ABOVE, friend_role("above", "marketville-146"), "above"),
              (MARKETVILLE_BELOW, friend_role("below", "marketville-146"), "below"),
              (MARKETVILLE_EQUAL, friend_role("equal", "marketville-146"), "equal")]
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
            b += role_disc(x + (i // rows) * pitch, 150 + (i % rows) * pitch,
                           col, size=size)
            drawn += 1
        b += text(x + (n_ - 1) * pitch / 2, 95, f"{count} {lab}",
                  color=col or "black")
        x += wide + gap
    assert drawn == 146
    assert_role_counts(b, {"above": MARKETVILLE_ABOVE, "below": MARKETVILLE_BELOW,
                           "equal": MARKETVILLE_EQUAL}, "marketville-146")
    b += text(540, 330, f"{num(k1,1)} friends each, {num(friend,1)} per friend")
    emit("marketville-146", b, container="full", h=FULL_H)


# =========================================================================== Part Two
# Four rays that no pair leaves collinear through the hub (R1 A-3).  The first version
# put the neighbours on the corners of a rectangle, so both diagonals ran straight
# through the centre and the eye counted TWO lines on the slide whose whole job is
# "four edges attached".  The gap from 180 degrees is asserted, not eyeballed.
# clockwise from the top right, so the edge numbers run 1 2 3 4 the way the
# eye does (R3 A3-11); they used to come out 2 1 3 4.
STAR_ANGLES = (15, 300, 230, 155)


def _rays(cx, cy, rx, ry, angles):
    """Points on an ellipse whose DRAWN direction from the centre is exactly `angles`.

    Placing them at (rx cos a, ry sin a) does not do that: squashing y rotates every
    direction toward the x-axis, and a set 35 degrees clear of collinear in parameter
    space came out 13 degrees clear on the page.
    """
    out = []
    for a in angles:
        t = math.radians(a)
        r = rx * ry / math.hypot(ry * math.cos(t), rx * math.sin(t))
        out.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return out


def assert_not_collinear(hub, leaves, what, floor=15.0):
    worst = 180.0
    for i in range(len(leaves)):
        for j in range(i + 1, len(leaves)):
            u = math.atan2(leaves[i][1] - hub[1], leaves[i][0] - hub[0])
            v = math.atan2(leaves[j][1] - hub[1], leaves[j][0] - hub[0])
            d = math.degrees(abs(u - v)) % 360
            worst = min(worst, abs(180 - min(d, 360 - d)))
    assert worst >= floor, (f"{what}: two edges leave the hub {180 - worst:.0f}deg apart "
                            f"-- they will read as one straight line through it")


def fig_degree_def():
    cx, cy = 268, 205
    leaves = _rays(cx, cy, 240, 115, STAR_ANGLES)
    assert_not_collinear((cx, cy), leaves, "degree-def")
    b = "".join(seg((cx, cy), q) for q in leaves)
    # R2 A2-5: neighbours in accent like every other graph in the deck.  They were
    # annotation gray, which two slides earlier means "her friends average exactly
    # what she has".
    b += "".join(disc(*q, fill="accent") for q in leaves)
    b += disc(cx, cy, fill="accenttwo")
    for i, (lx, ly) in enumerate(leaves, start=1):
        mx, my = (cx + lx) / 2, (cy + ly) / 2
        nx_, ny_ = -(ly - cy), (lx - cx)
        L = math.hypot(nx_, ny_)
        b += text(mx + nx_ / L * 30, my + ny_ / L * 30, str(i), color="accenttwo")
    assert len(leaves) == 4
    b += text(cx, 42, f"degree {len(leaves)}", color="accenttwo")
    emit("degree-def", b, container="col", h=COL_H)


# R3 A3-2: a tick sits at a fixed FRACTION of its edge, not a fixed distance from its
# node.  A constant ~66bp separated cleanly on the 292bp Pam-Carol edge and put both
# ticks of a 150bp edge at 44% and 56% -- 18bp apart at the midpoint, which is the
# standard geometry mark for two lengths being EQUAL, and around Sue the eye counted six
# marks where four ends exist.  The component count could not see it: twenty marks were
# genuinely there.  Position is asserted now as well as quantity.
END_F = 0.28


def _end_marks():
    """One (node, segment) per edge end, with the drawn geometry checked."""
    out = []
    for a, c in FELD_EDGES:
        pa, pc = np.array(POS[a], float), np.array(POS[c], float)
        span = float(np.linalg.norm(pc - pa))
        n_ = np.array([-(pc - pa)[1], (pc - pa)[0]]) / span
        ends = []
        for u, v in ((pa, pc), (pc, pa)):
            m = u + (v - u) * END_F
            ends.append((m - n_ * END_H / 2, m + n_ * END_H / 2, m))
        apart = float(np.linalg.norm(ends[0][2] - ends[1][2]))
        assert apart >= 0.40 * span, (
            f"sum-ends: the two ticks on {a}-{c} are {apart / span:.0%} of the edge "
            f"apart; below 40% they read as one pair at the midpoint, not as two ends")
        assert END_F * span - NODE / 2 > 8, f"sum-ends: the {a}-{c} tick is inside a disc"
        out += [(a, ends[0][:2]), (c, ends[1][:2])]

    def gap(s1, s2):
        t = np.linspace(0, 1, 60)[:, None]
        A, B = s1[0] + (s1[1] - s1[0]) * t, s2[0] + (s2[1] - s2[0]) * t
        return float(np.min(np.linalg.norm(A[:, None] - B[None, :], axis=2)))

    for i in range(len(out)):
        for j in range(i + 1, len(out)):
            d = gap(out[i][1], out[j][1])
            assert d >= 12, (f"sum-ends: a tick at {out[i][0]} and one at {out[j][0]} "
                             f"are {d:.0f}bp apart and will fuse on the page")
    return out


def fig_sum_ends():
    marks = _end_marks()
    b = feld_body()
    for _, (p, q) in marks:
        b += seg(tuple(p), tuple(q), color="accenttwo", w=END_W)
    ends = len(marks)
    assert ends == 2 * M["M"] == 20
    b += "".join(disc(*POS[n], fill="accent") for n in FELD_ORDER)
    # black, not accent-2: the accent-2 ink in this figure is exactly the twenty ticks,
    # which is what makes the component count below a check and not a coincidence.
    b += text(540, 45, f"{M['M']} lines, {ends} ends")
    assert_ink_components(b, 1080, FULL_H, ACCENT2, ends, "sum-ends")
    emit("sum-ends", b, container="full", h=FULL_H)


def fig_mean_degree():
    ends, girls = 2 * M["M"], M["N"]
    assert ends == 20 and girls == 8 and float(M["k1"]) == ends / girls
    b = text(268, 322, f"{ends} ends")
    b += "".join(end_mark(35 + i * 24, 258) for i in range(ends))
    b += seg((268, 232), (268, 190), color="annot", w=3.0, arrow=ARROW)
    b += "".join(disc(60 + i * 60, 150, fill="accent") for i in range(girls))
    b += text(268, 100, f"{girls} girls")
    b += text(268, 45, f"{num(float(M['k1']), 1)} each", color="accenttwo", size=56)
    emit("mean-degree", b, container="col", h=COL_H)


def fig_handshake():
    """Three odd counts, their five ends, and the pairing that runs out (R2 A2-2, A2-3).

    Two rounds of this figure drew only the FAILURE -- a stub with an X -- while the
    body's claim is that odd degrees *pair off*.  The pairing is drawn now: the five
    ends are marks, two gray brackets take them two at a time, and the fifth is left
    with nothing to bracket.  Colour does one job each: accent is a node, accent-2 is an
    end (the same red tick slides 016 and 017 spend two slides establishing), gray is
    annotation, black is the arithmetic.  Nothing red is line-like, so nothing red can
    be read as an edge -- which is what killed both earlier versions.
    """
    want = {"A": 3, "B": 1, "C": 1}
    ends = sum(want.values())
    assert ends % 2 == 1, "the whole point is that the wanted degree sum is odd"
    pairs = ends // 2
    assert 2 * pairs + 1 == ends

    at = {"A": 250.0, "B": 620.0, "C": 960.0}
    stubs = {"A": [210.0, 250.0, 290.0], "B": [620.0], "C": [960.0]}
    assert all(len(v) == want[k] for k, v in stubs.items())
    flat = [x for k in ("A", "B", "C") for x in stubs[k]]
    assert len(flat) == ends

    b = ""
    # the two matched pairs, nested so their brackets cannot cross
    for (x0, x1), y in ((( stubs["A"][1], stubs["C"][0]), 130.0),
                        ((stubs["A"][2], stubs["B"][0]), 175.0)):
        b += polyline([(x0, 223), (x0, y), (x1, y), (x1, 223)], color="annot", w=3.4)
    b += cross(stubs["A"][0], 175, r=20, color="annot", w=4.0)

    # a short gray shelf under each disc, spanning exactly its own ends, so the three
    # under "3" read as that node's three rather than as three loose marks
    for k in ("A", "B", "C"):
        b += seg((min(stubs[k]) - 9, 264), (max(stubs[k]) + 9, 264), color="annot", w=3.0)
    for x in flat:
        b += end_mark(x, 240)
    b += "".join(disc(at[k], 290, str(want[k]), fill="accent") for k in ("A", "B", "C"))

    b += text(stubs["A"][0], 95, "no partner", color="annot")
    b += text(605, 95, f"{pairs} pairs", color="annot")
    total = " + ".join(str(want[k]) for k in ("A", "B", "C"))
    b += text(540, 360, f"${total} = {ends}$ ends")
    assert_ink_components(b, 1080, FULL_H, ACCENT2, ends, "handshake")
    emit("handshake", b, container="full", h=FULL_H)


def fig_pk_def():
    """The definition, on a generic three-degree network (R2 A2-6).

    R1's A-5 fixed a real defect -- the figure counted where the slide defines a
    fraction -- by importing slide 021's content, which left 020 and 021 the same
    picture one slide apart and 021 with nothing to reveal.  So: the fraction and its
    denominator stay, the eight girls go back to 021.  The piles fall away with k, which
    is also the shape 021's flat 2-2-2-2 is then surprising against.
    """
    heights = [3, 2, 1]
    n = sum(heights)
    assert n == 6 and heights == sorted(heights, reverse=True)
    b = ""
    for i, hgt in enumerate(heights):
        x = 70 + i * 198
        for j in range(hgt):
            b += disc(x, 200 + j * 48, fill="accent")
        b += text(x, 150, f"$k={i + 1}$", color="annot")
        b += text(x, 95, f"${hgt}/{n}$", color="accenttwo")
    b += text(268, 40, f"$p(k)$ = fraction of all ${n}$")
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

    # R2 A2-4: the tally column is gone.  It sat at the end of each girl's own line, so
    # it counted the names ON that line -- her degree, already visible -- while the
    # caption claims the other direction, how often her name appears on everyone else's.
    # The two coincide only because the graph is undirected, which the slide never says.
    # The red and blue mark-up carries the point on its own; the eight lines run in two
    # blocks of four because eight full-width lines of running text span 412bp of a
    # 1080bp canvas, and the ink floor is 821bp.
    ones = [v for v in FELD_ORDER if counts[v] == min(counts.values())]
    assert ones == ["Betty", "Tina"]
    role = {v: ("hub" if v in hubs else "one" if v in ones else None)
            for v in FELD_ORDER}

    # Two one-argument macros rather than \textcolor at each name.  figlib's collision
    # gate models a box from the SOURCE string, counting a control word as one glyph and
    # everything inside its braces as text -- so "\textcolor{accenttwo}{Alice}" measured
    # 15 glyphs where the page shows 5, and the modelled box was twice the real one.
    # A macro puts the colour name outside the string the gate sees.
    b = ("\\def\\hub#1{\\textcolor{accenttwo}{#1}}\n"
         "\\def\\one#1{\\textcolor{accent}{#1}}\n")
    for i, v in enumerate(FELD_ORDER):
        x, row = (55, i) if i < 4 else (690, i - 4)
        entries = ", ".join(f"\\{role[u]}{{{u}}}" if role[u] else u for u in lists[v])
        b += text(x, 330 - row * 76, f"{v}: {entries}", anchor="west")
    emit("rosters", b, container="full", h=FULL_H)


# ========================================================================= Part Three
def fig_bag_of_hands():
    """Twenty edge ENDS, drawn with the deck's end glyph (R3 A3-5).

    This slide's single point is that you do not pick a person, you pick one end of one
    edge -- and it drew the ends as the 40px lettered disc that has meant a person on
    every slide since 006.  Red ticks now, the same mark 016, 017 and 027 use, each
    labelled with its owner's initial.  Discs stay for people.
    """
    owners = []
    for v in FELD_ORDER:
        owners += [v] * degree(v)
    assert len(owners) == 2 * M["M"] == 20
    # R4 A4-10: full names, not initials. Round 3 put B/S/A/J/P/D/C/T in the bag and a
    # three-of-eight legend under it; the legend was then dropped rather than completed,
    # leaving nothing on the slide that decodes a letter. Four columns instead of five
    # buys the room to write the name out, which needs no legend at all.
    b = rect(20, 15, 516, 292, color="annot", w=3.4, rounded=20,
             what="the bag")
    for i, v in enumerate(owners):
        x, y = 40 + (i % 4) * 124, 260 - (i // 4) * 55
        b += end_mark(x, y)
        b += text(x + 16, y, v, color="annot", anchor="west")
    b += text(268, 330, f"{len(owners)} ends, and whose they are")
    emit("bag-of-hands", b, container="col", h=COL_H)


def fig_qk_formula():
    """q(k) drawn per DEGREE, because that is what q(k) is (R3 A3-4).

    Eight per-girl rows put "4 of 20 = 0.2" under a formula whose value at k = 4 is
    0.4: two girls sit at degree four and q(k) collects both of them.  One row per
    degree, all that degree's hands in it, and the fraction beside it -- which is now
    q(k) itself and is asserted equal to k*p(k)/<k>.
    """
    from fractions import Fraction
    piles = {}
    for v in FELD_ORDER:
        piles.setdefault(degree(v), []).append(v)
    ends, n = 2 * M["M"], M["N"]
    b, marks = "", 0
    for i, k in enumerate(sorted(piles)):
        hands = k * len(piles[k])
        q = Fraction(hands, ends)
        assert q == Fraction(k) * Fraction(len(piles[k]), n) / M["k1"], (k, q)
        y = 80 + i * 70
        b += text(120, y, f"$k={k}$", color="annot", anchor="east")
        for j in range(hands):
            b += end_mark(146 + j * 26, y)
            marks += 1
        b += text(146 + 8 * 26, y, f"${hands}/{ends}$", color="accenttwo", anchor="west")
    assert marks == ends == 20
    b += text(268, 350, f"$q(k)$: share of the {ends} hands")
    emit("qk-formula", b, container="col", h=COL_H)




# lmex10 -- the math EXTENSION font -- does not scale with \fontsize in this preamble:
# at 36pt a \sum, \int or \prod still draws at its 10pt natural size, silently, with no
# "not available" line in the log for figlib.render() to catch.  A capital \Sigma comes
# from the letters font, which does scale, so the operator is built from that instead.
# R3 A3-3: "friend" is the only mark separating this quantity from a plain <k>, and
# at TeX's script size it landed 12px x-height against a 15px floor. It is set at the
# body size now -- raised, not shrunk -- and `_assert_subscript_height` measures what
# that actually renders rather than trusting the number.
SUB_PT = 36

SUM_K = r"\mathop{\scalebox{1.35}{$\Sigma$}}\limits_{k}"

# Every heavy sub-expression gets a macro, and the equations are written in terms of
# them.  The expansion is identical -- TeX draws exactly what it drew before -- but the
# string figlib's collision gate measures is no longer mostly markup.  `visible()`
# counts a control word as one glyph and everything inside its braces as text, so
# \mathrm{friend} measured "nfriend" and \scalebox{1.35} measured "n1.35": line one
# modelled 1115bp against a rendered 492bp and was flagged against a gloss it clears by
# 58bp.  With the macros the model reads 541bp, which is a fair over-estimate rather
# than a doubling, and the gate can do its job on this figure instead of crying wolf.
_MACROS = (r"\def\dsp{\displaystyle}"
           r"\def\sub#1{\mbox{\fontsize{" + str(SUB_PT) + r"}{" + str(SUB_PT) + r"}"
           r"\selectfont #1}}"
           r"\def\kf{\langle k\rangle_{\sub{friend}}}"
           r"\def\kk{\langle k\rangle}"
           r"\def\ksq{\langle k^2\rangle}"
           r"\def\sk{" + SUM_K + r"}"
           r"\def\vk{\mathrm{Var}(k)}" + "\n")

# R1 A-14 / R2 Major 1: line one used to make three moves at once -- sum, substitute,
# and name a symbol the deck had never written down -- on a build whose whole premise is
# one new idea per line. Four states now: q(k) goes in, then the numerator gets its name.
_DERIV = [
    r"$\dsp \kf = \sk k\,q(k) = \sk k\cdot\frac{k\,p(k)}{\kk}$",
    r"$\dsp \phantom{\kf} = \frac{\ksq}{\kk}$",
    r"$\dsp \ksq = \vk + \kk^2$",
    r"$\dsp \kf = \kk + \frac{\vk}{\kk}$",
]
# "name the numerator" drew to x = 1052 against a frame border at 1040, so the border
# ran through its last letter on three consecutive slides. The collision gate cannot see
# it -- a frame rectangle is not in its blocker set -- so the containment is asserted
# below, against the measured ink rather than against the modelled box.
_GLOSS = [r"substitute $q(k)$", r"name $\ksq$",
          r"rewrite $\ksq$", "the theorem"]
_FRAME = (40, 20, 1040, 356)
_DERIV_Y = [300, 226, 152, 78]
_EQ_X, _GLOSS_X = 150, 760


def _raw_node(x, y, s, size=FONT, anchor="west"):
    """A text node that does NOT enter figlib's collision scene.

    `text()` records every call, so measuring a string by rendering it through `text()`
    left a phantom box at the measuring coordinates and the gate reported the figure
    colliding with its own ruler.  Measurement draws nothing the figure keeps, so it
    must not be recorded.
    """
    return (f"\\node[font=\\fontsize{{{size}}}{{{int(size * 1.15)}}}\\selectfont,"
            f"text=black,anchor={anchor},align=center] at ({x},{y}) {{{s}}};\n")


@lru_cache(maxsize=None)
def _assert_subscript_height():
    """Measure the x-height the derivation's subscript really renders at."""
    glyph = (f"\\mbox{{\\fontsize{{{SUB_PT}}}{{{SUB_PT}}}\\selectfont rnm}}")
    a = np.asarray(render(_raw_node(30, 120, f"${glyph}$"), 400, 240).convert("L"))
    ys, _ = np.where(a < 200)
    px = (ys.max() - ys.min() + 1) / PXBP
    assert px >= TEXT_MIN_PX, (
        f"the derivation's 'friend' subscript renders {px:.1f}px x-height against a "
        f"{TEXT_MIN_PX}px floor -- raise SUB_PT; do not accept the warning")
    return px


@lru_cache(maxsize=None)
def _ink_width(s):
    """The width one text node really occupies, measured off a render.

    The collision gate models a box from the source string, and for these lines the
    model runs 10% UNDER the truth as often as it runs over (line three: 244bp modelled,
    297bp drawn).  A model that can under-estimate cannot be the only check on a column
    that has to clear another column, so the equations are measured.
    """
    body = _MACROS + _raw_node(30, 120, s)
    a = np.asarray(render(body, 1900, 300).convert("L"))
    ys, xs = np.where(a < 200)
    return (xs.max() - xs.min() + 1) / PXBP


def _derivation(upto):
    """One figure in four states: the same frame, the same left margin, one line more.

    Each state's body is a prefix of the next, so everything above the added line is
    identical by construction rather than by inspection.
    """
    _assert_subscript_height()
    b = _MACROS + rect(*_FRAME, color="annot", w=2.4, rounded=10,
                       what="the derivation frame")
    for i in range(upto):
        assert _EQ_X + _ink_width(_DERIV[i]) < _GLOSS_X - 20, (
            f"derivation line {i + 1} is drawn to x="
            f"{_EQ_X + _ink_width(_DERIV[i]):.0f} and the gloss column starts at "
            f"{_GLOSS_X}. Shorten the line or move the column; do not shrink the type.")
        assert _GLOSS_X + _ink_width(_GLOSS[i]) < _FRAME[2] - 12, (
            f"gloss {i + 1} is drawn to x="
            f"{_GLOSS_X + _ink_width(_GLOSS[i]):.0f} and the frame border sits at "
            f"{_FRAME[2]} -- the border will run through its last letter")
        b += text(78, _DERIV_Y[i], str(i + 1), color="annot")
        if i == 3:
            b += (f"\\node[font=\\fontsize{{{FONT}}}{{{int(FONT*1.15)}}}\\selectfont,"
                  f"text=black,anchor=west,align=center] (eqthree) at "
                  f"({_EQ_X},{_DERIV_Y[i]}) {{{_DERIV[i]}}};\n"
                  f"\\node[draw=accenttwo,line width=3.4bp,rounded corners=8bp,"
                  f"fit=(eqthree),inner sep=9bp] {{}};\n")
        else:
            b += text(_EQ_X, _DERIV_Y[i], _DERIV[i], anchor="west")
        b += text(_GLOSS_X, _DERIV_Y[i], _GLOSS[i], color="annot", anchor="west")
    return b


def _emit_derivation(n):
    """Check the prefix property, then draw the state ONCE.

    `_derivation()` records into figlib's collision scene, so building state n-1 to
    compare against it left a second copy of every earlier line in the scene and the
    gate reported each of them overlapping itself.  The scene is reset after the
    comparison so only the emitted body is measured.
    """
    if n > 1:
        assert _derivation(n).startswith(_derivation(n - 1))
    scene_clear()
    emit(f"derivation-{n}", _derivation(n), container="full", h=FULL_H)


def fig_derivation_1():
    _emit_derivation(1)


def fig_derivation_2():
    _emit_derivation(2)


def fig_derivation_3():
    _emit_derivation(3)


def fig_derivation_4():
    _emit_derivation(4)


def fig_gap_nonneg():
    zero = 170
    b = seg((30, 200), (zero, 200), color="annot", w=3.0, dash=DASH)
    b += seg((zero, 200), (505, 200), color="accenttwo", w=5.0, arrow=ARROW)
    b += seg((zero, 186), (zero, 214), color="black", w=3.0)
    # clear of the zero tick, which is a rule and now records itself
    b += text(zero, 178, "0", anchor="north")
    b += text(190, 86, "all degrees\\\\equal", color="annot")
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
    b += "".join(end_mark(70 + i * 22, 218) for i in range(ends))
    b += text(280, 90, num(per_end, 2), color="accenttwo", size=88)
    b += text(790, 318, "pick a person")
    b += "".join(disc(600 + i * 54, 218, fill="accent") for i in range(girls))
    b += text(790, 90, num(per_person, 2), color="accent", size=88)
    emit("two-averages", b, container="full", h=FULL_H)


_STAR = nx.star_graph(3)
_RING = nx.cycle_graph(6)
_STAR_POS = {0: (250, 260), 1: (110, 180), 2: (110, 340), 3: (392, 260)}
_RING_POS = {i: (790 + 190 * math.cos(math.radians(a)), 260 + 95 * math.sin(math.radians(a)))
             for i, a in enumerate(range(0, 360, 60))}


def _star_ring_body():
    assert_planar_drawing(list(_STAR.edges()), _STAR_POS, "worksheet star")
    assert_planar_drawing(list(_RING.edges()), _RING_POS, "worksheet ring")
    b = "".join(seg(_STAR_POS[a], _STAR_POS[c]) for a, c in _STAR.edges())
    b += "".join(seg(_RING_POS[a], _RING_POS[c]) for a, c in _RING.edges())
    return b


_WS_Q = r"$\mathrm{Var}(k)/\langle k\rangle$"
_WS_CX = (250, 790)


def _worksheet(values=None):
    """The question and the answer, drawn on identical ink extents (R3 A3-10).

    They used to differ by 66px: the question carried a blank rule the answer dropped,
    so the two croppings differed and the pair of graphs jumped between the slides. The
    rule stays in both, the prompt keeps its position and its colour, and the answer is
    added beside it -- the acquaintance build holds still across three slides and this
    one should too.
    """
    b = _star_ring_body()
    lab = (lambda n: str(_STAR.degree(n))) if values else (lambda n: "")
    b += "".join(disc(*_STAR_POS[n], lab(n), fill="accent") for n in _STAR)
    lab2 = (lambda n: str(_RING.degree(n))) if values else (lambda n: "")
    b += "".join(disc(*_RING_POS[n], lab2(n), fill="accent") for n in _RING)
    # Both states anchor the prompt at the same LEFT edge and let the answer grow to the
    # right, so the formula does not slide sideways between the two slides. The value is
    # appended inside the same node through a macro rather than a second node: it keeps
    # the two parts on one baseline, and it keeps the colour name out of the string
    # figlib's collision gate measures.
    # R4 A4-9: the answer is written ON the rule the question drew for it, not appended
    # to the prompt. The prompt is the same string in both states, centred at the same
    # x, so nothing about it moves; the rule is in both; and the ink extents are set by
    # the graphs and the rule, so the two states crop identically and cannot jump.
    for i, cx in enumerate(_WS_CX):
        b += text(cx, 110, _WS_Q)
        b += seg((cx - 100, 32), (cx + 100, 32), color="accenttwo", w=5.0)
        if values:
            b += text(cx, 40, f"${values[i]}$", color="accenttwo", anchor="south")
    return b


def fig_worksheet_star_ring():
    b = _worksheet()
    assert_no_digits([_WS_Q], "worksheet-star-ring")
    for bad in ("0.5", "0.50", "= 0$", "zero"):
        assert bad not in b, f"worksheet-star-ring leaks the answer ({bad})"
    emit("worksheet-star-ring", b, container="full", h=FULL_H)


def fig_worksheet_answer():
    ms, mr = moments(_STAR), moments(_RING)
    assert float(ms["gap"]) == 0.5 and float(mr["gap"]) == 0.0
    b = _worksheet((num(float(ms["gap"]), 1), num(float(mr["gap"]), 0)))
    emit("worksheet-answer", b, container="full", h=FULL_H)


# ========================================================================== Part Four
@lru_cache(maxsize=None)
def _condmat_stats():
    g = condmat()
    return net_stats(g), paradox_share(g)


def fig_coauthor_gap():
    """R3 A3-8: the last bar in the deck becomes the objects it was encoding.

    Slide 040's three bars became a hundred discs for exactly this rule and this strip
    was left behind, so 82.8% was the one quantity in the module still drawn as a length
    to be decoded against a scale.  The field is 4 x 25 rather than 040's 10 x 10 so the
    two slides do not read as the same picture twice.
    """
    s_, share = _condmat_stats()
    assert s_["N"] == 23133
    assert num(s_["k1"], 1) == "8.1" and num(s_["friend"], 1) == "22.1"
    hit = round(share * 100)
    assert hit == 83, hit

    b = text(250, 330, num(s_["k1"], 1), color="accent", size=88)
    b += text(830, 330, num(s_["friend"], 1), color="accenttwo", size=88)
    b += seg((420, 330), (660, 330), color="annot", w=3.4, arrow=ARROW)
    b += text(250, 258, "each author", color="annot")
    b += text(830, 258, "their coauthors", color="annot")

    PITCH, MARK, PER_ROW = 38, 26, 25
    field, red = "", 0
    for i in range(100):
        row, col = divmod(i, PER_ROW)
        field += dot(71 + col * PITCH, 205 - row * PITCH, d=MARK,
                     color="accenttwo" if i < hit else "accent")
        red += i < hit
    assert red == hit == field.count("accenttwo"), (red, hit)
    b += field
    b += text(540, 40, f"{pct(share, 1)} below their coauthors' average", color="annot")
    emit("coauthor-gap", b, container="full", h=FULL_H)


def fig_fb_twitter():
    """R1 A-2: one point, and the objects rather than a length.

    This was three bars on a common 0-100 scale measuring 0.925, 0.834 and 0.978 of
    their boxes -- all nearly full, so every bit of information came from the numbers
    printed inside them, which is what FIGURE_GUIDE rules bars out for. And the middle
    bar was the MEDIAN, a distinction this deck does not introduce for another 43
    slides; it lives on "The mean and the median disagree" now, where the room has been
    asked the question first.

    A hundred discs, ninety-three of them red. Nothing to decode against an axis: the
    room counts the seven that are not.
    """
    assert "92.7% of users have less friends than the average" in LITERATURE
    assert ">98% of Twitter users" in LITERATURE
    assert "721 million active users" in LITERATURE

    share = 0.927
    hit = round(share * 100)
    assert hit == 93, hit
    PITCH, MARK, PER_ROW = 36, 28, 10
    x0, ytop = 92, 360
    b = ""
    for i in range(100):
        row, col = divmod(i, PER_ROW)
        b += dot(x0 + col * PITCH, ytop - row * PITCH, d=MARK,
                 color="accenttwo" if i < hit else "accent")
    assert b.count("accenttwo") == hit

    tx = 560
    b += text(tx, 300, f"{pct(share, 1)} of Facebook", color="accenttwo", anchor="west")
    b += text(tx, 246, "have fewer friends than", anchor="west")
    b += text(tx, 192, "their friends average", anchor="west")
    b += text(tx, 122, "721 million people, 2011", color="annot", anchor="west")
    b += text(tx, 62, "on Twitter, over 98\\%", color="annot", anchor="west")
    # The median belongs to the slide that asks about it, not to this one.
    assert "83.6" not in b and "median" not in b
    emit("fb-twitter", b, container="full", h=FULL_H)


_SB = nx.Graph()
_SB.add_edges_from([("H", i) for i in range(6)] + [(0, 1), (2, 3), (4, 5)])
_SB_POS = {"H": (250, 235)}
_SB_POS.update({i: (250 + 165 * math.cos(math.radians(a)),
                    235 + 90 * math.sin(math.radians(a)))
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
    b += text(250, 90, "the hub", color="accenttwo")
    # 28bp marks, not 13: these are objects the room is asked to count and compare, and
    # the floor for a countable disc on the slide is 26px. Eighteen of them will not fit
    # on one row at that size, so the row wraps -- the drawing grows, the mark does not
    # shrink. Both fractions are printed, because "2.3x" cannot be checked otherwise.
    PITCH, MARK, PER_ROW = 36, 28, 9
    for ytop, lab, tot, hit, unit in ((330, "pick a person", n, 1, "one person"),
                                      (176, "follow an edge", ends, kh, "one edge end")):
        b += text(560, ytop, lab, anchor="west")
        for i in range(tot):
            row, col = divmod(i, PER_ROW)
            b += dot(578 + col * PITCH, ytop - 46 - row * PITCH, d=MARK,
                     color="accenttwo" if i < hit else "accent")
        rows = (tot + PER_ROW - 1) // PER_ROW
        b += text(578 + PER_ROW * PITCH + 16, ytop - 46 - (rows - 1) * PITCH / 2,
                  f"${hit}$ of ${tot}$", color="accenttwo", anchor="west")
        b += text(560, ytop - 46 - (rows - 1) * PITCH - 40, unit, color="annot",
                  anchor="north west", size=FONT)
    # under the graph, not under the tally: at the foot of the right column it sat
    # on the "one edge end" unit label and 2bp into the bottom row of dots.
    b += text(250, 40, f"${num(factor,1)}\\times$ more often", color="accenttwo")
    emit("sampling-bias", b, container="full", h=FULL_H)


_ACQ = {"H": (0, 18), 1: (-118, -58), 2: (-40, 112), 3: (118, -58), 4: (52, 112)}


# One step per slide (R1 A-7). The three-panel strip this replaces differed only by a
# small ring moving and an arrow appearing, so the room had to diff three near-identical
# drawings to find the change -- the case F4 reserves for a build. Same graph, same
# positions, one new mark each time; and the discs are NODE now, not SMALLNODE, because
# at 28px they were the smallest graph in the range against 40px everywhere else.
#
# Two marks, and each says what it means on the drawing: an accent-2 RING is the person
# this step is choosing, an accent-2 FILL is a person who has been immunised. Nothing on
# the old figure said either.
ACQ_HUB = (540, 150)

# Seven leaves on a wide ellipse, not four on a rectangle. Two reasons. The hub has to
# LOOK like a hub -- with four leaves the drawing reads as an X with a node dropped on
# the crossing, which is the same defect A-3 fixed on `degree-def` -- and 360/7 is not a
# divisor of 180, so no two edges are collinear through the hub and every one of them
# reads as its own stroke. The ellipse is wide because a round star spans 31% of a
# 1080bp canvas and the floor is 76%.
# Spread over 260 degrees rather than the full circle, so a wedge stays clear straight
# below the hub for the step label. With seven edges radiating in every direction the
# placement solver had nowhere to put "immunised" and -- correctly -- refused, which is
# the layout telling you it is wrong, not the label.
ACQ_ANGLES = [-40 + i * (260 / 6) for i in range(7)]
ACQ_LEAF = {i + 1: (round(540 + 430 * math.cos(math.radians(a))),
                    round(150 + 150 * math.sin(math.radians(a))))
            for i, a in enumerate(ACQ_ANGLES)}
# Tolerance 3 degrees, not 8: at a 430bp radius, 6.7 degrees puts the two far ends 50bp
# apart, which no one reads as one stroke -- and the hub disc sits between them anyway.
# What A-3 was about is EXACT collinearity (measured slopes 0.489 and 0.484).
assert not any(abs(((a - b) % 360) - 180) < 3
               for a in ACQ_ANGLES for b in ACQ_ANGLES), \
    "two leaves are opposite the hub: their edges read as one straight line (cf. A-3)"
ACQ_EDGES = [("H", k) for k in ACQ_LEAF]
ACQ_POS = {"H": ACQ_HUB, **ACQ_LEAF}
ACQ_PICK = 6                      # the leaf the random draw lands on, left of the hub

assert_planar_drawing(ACQ_EDGES, ACQ_POS, "acquaintance star")
assert min(math.dist(a, b) for a, b in itertools.combinations(ACQ_POS.values(), 2)) \
    > NODE + 6, "acquaintance star: two discs are touching"


def _acq_label(at, s, color="accenttwo"):
    """Place a step label clear of every edge and every disc, or fail loudly.

    Hand-placing it put "immunised" straight across the edge running down-left out of the
    hub. The rule the guide states for names applies to notes too: try the sides in
    order, reject anything that hits ink, and say so rather than shrinking the type.
    """
    from figlib import box_hits_disc, box_hits_segment, label_box
    for anc, dx, dy in (("south", 0, 34), ("north", 0, -34), ("west", 34, 0),
                        ("east", -34, 0), ("south west", 26, 26), ("south east", -26, 26),
                        ("north west", 26, -26), ("north east", -26, -26),
                        ("south", 0, 62), ("north", 0, -62)):
        x, y = at[0] + dx, at[1] + dy
        b = label_box(x, y, s, anc)
        if not (6 <= b[0] and b[2] <= 1074 and 6 <= b[1] and b[3] <= 414):
            continue
        if any(box_hits_disc(b, *p) for p in ACQ_POS.values()):
            continue
        if any(box_hits_segment(b, ACQ_POS[a], ACQ_POS[c]) for a, c in ACQ_EDGES):
            continue
        return text(x, y, s, color=color, anchor=anc)
    raise SystemExit(f"acquaintance: nowhere to put {s!r} without hitting an edge or a "
                     f"disc -- move a leaf or shorten the label; do not shrink the type.")


def _acq_base(treated=()):
    b = ""
    for k, p in ACQ_LEAF.items():
        b += seg(ACQ_HUB, p, w=2.6)
    for k, p in ACQ_LEAF.items():
        b += disc(p[0], p[1], fill="accenttwo" if k in treated else "accent", size=NODE)
    b += disc(ACQ_HUB[0], ACQ_HUB[1], fill="accenttwo" if "H" in treated else "accent",
              size=NODE)
    return b


def _acq_arrow():
    """The nomination, drawn along the edge it travels.  Shared by steps two and three."""
    p = np.array(ACQ_LEAF[ACQ_PICK], float)
    q = np.array(ACQ_HUB, float)
    u = (q - p) / np.linalg.norm(q - p)
    return seg(tuple(p + u * (NODE / 2 + 12)), tuple(q - u * (NODE / 2 + 10)),
               color="accenttwo", w=4.4, arrow=ARROW)


def fig_acquaintance_1():
    """Step one: somebody chosen at random, and it is almost never the hub."""
    b = _acq_base()
    b += ring(*ACQ_LEAF[ACQ_PICK], size=NODE, grow=14)
    b += _acq_label(ACQ_LEAF[ACQ_PICK], "picked")
    emit("acquaintance-1", b, container="full", h=FULL_H)


def fig_acquaintance_2():
    """Step two: the nomination travels along the edge, and lands on the hub."""
    b = _acq_base()
    b += ring(*ACQ_LEAF[ACQ_PICK], size=NODE, grow=14)
    b += _acq_label(ACQ_LEAF[ACQ_PICK], "picked")
    b += _acq_arrow()
    emit("acquaintance-2", b, container="full", h=FULL_H)


def fig_acquaintance_3():
    """Step three: the named friend is the one who gets the dose.

    The volunteer keeps her ring. The title of this slide is "vaccinate the friend, not
    the volunteer", so a drawing that has dropped the volunteer cannot make its own
    point -- and reusing the ring for the hub would give one glyph two meanings across a
    three-slide build, which is the defect the marks were labelled to stop.
    """
    b = _acq_base(treated=("H",))
    b += ring(*ACQ_LEAF[ACQ_PICK], size=NODE, grow=14)
    # R3 A3-6: the nomination arrow has to survive into this frame. `_acq_base` redraws
    # every edge as plain black, so step two's mark was being painted over and the slide
    # titled "vaccinate the friend, not the volunteer" no longer showed how the friend
    # was reached. A build that stops accumulating is not a build.
    b += _acq_arrow()
    b += _acq_label(ACQ_LEAF[ACQ_PICK], "picked")
    b += _acq_label(ACQ_HUB, "immunised")
    emit("acquaintance-3", b, container="full", h=FULL_H)


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

    # The axis title is horizontal, above the frame, and carries the scale with it.
    # Rotated it cannot fit: a 537bp column has to hold a 99bp "100\%" tick label, the
    # plot, and a right gutter of curve labels, and `Axes` draws a rotated title 100bp
    # left of the axis -- which put it through the tick labels at x=54..67.  The
    # "log scale" mark had the same problem in the other direction: inside the frame at
    # the top left it sat on the random curve, its first data dot, and the "random 87\%"
    # label.  One line above the plot says both things and touches nothing.
    # x0 = 140, not 170: "nominated" is four glyphs longer than "named" and the
    # gutter label ran off the right edge of a 537bp column. The plot moves left
    # and gives the gutter the room; the type does not move.
    ax = Axes((140, 132, 300, 300), (0, 0.10), (0.001, 1), ylog=True,
              xticks=[0, 0.05, 0.10], yticks=[0.001, 0.01, 0.1, 1],
              xfmt=lambda v: f"{v:g}", yfmt=lambda v: pct(v, 1 if v < 0.01 else 0),
              xlabel="fraction immunised")
    b = ax.frame()
    b += text(250, 348, "component left (log scale)")
    series = [("random", "accent", f"random {pct(at10['random'])}"),
              ("acquaintance", "accenttwo", f"nominated {pct(at10['acquaintance'])}"),
              ("degree", "annot", "targeted")]
    for key, col, lab in series:
        ys = c[key]
        b += ax.line(IMM_F, ys, color=col, w=3.6,
                     dash=DASH if key == "degree" else "")
        b += ax.points(IMM_F, ys, color=col, d=11)
        b += text(308, ax.Y(ys[-1]), lab, color=col, anchor="west")
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
    ("derivation-4", fig_derivation_4),
    ("gap-nonneg", fig_gap_nonneg),
    ("feld-check", fig_feld_check),
    ("two-averages", fig_two_averages),
    ("worksheet-star-ring", fig_worksheet_star_ring),
    ("worksheet-answer", fig_worksheet_answer),
    ("coauthor-gap", fig_coauthor_gap),
    ("fb-twitter", fig_fb_twitter),
    ("sampling-bias", fig_sampling_bias),
    ("acquaintance-1", fig_acquaintance_1),
    ("acquaintance-2", fig_acquaintance_2),
    ("acquaintance-3", fig_acquaintance_3),
    ("immunization-curves", fig_immunization_curves),
]
