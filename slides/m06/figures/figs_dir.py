#!/usr/bin/env python3
"""Directed-network figures of Module 06: HITS and the PageRank group.

hits-graph (col): six pages, the best hub hot, the best authority cool.

The PageRank group (col): pr-split, pr-split-answer, pr-leak (frames), pr-teleport, ppr.
All five share ONE canvas (537 x 372 bp), ONE crop box (PR_BOX) and the same five node
positions (PR_XY), so the web does not move between those five slides: only arrows,
shares, fills and values change.  Pages are discs with a pencil outline and a Meslo
letter; arrowheads stop at the disc border (arrows are drawn between named anchor nodes).
A winner is a hot disc with its value in hot and a hot underline; the other pages are
shaded cool by value.

Every number printed comes from smallgraphs.compute(); the facts the slides rest on
(hub, authority, the tie, the winners) are asserted before anything is drawn.
"""

from fractions import Fraction

import figlib as F
import smallgraphs as S

ARROW = "-{Stealth[length=12bp,width=9.5bp]}"
BOX = float(F.NODE)                          # a page is a disc of NODE bp
HALF = BOX / 2
GAP = 1.5                                    # arrowheads stop this far from the disc outline
CHIP_PAD = 2.0
CANVAS_H = 372
PR_BOX = (2, 362)                            # the one crop of the PageRank group, bp from the canvas top
CHAR = 0.61 * F.FONT                         # width of a Meslo character at FONT, bp

N = S.compute()
S.check(N)


# --------------------------------------------------------------------------- facts
def _top(d):
    return max(d, key=d.get)


_h, _a = N["HITS"]
assert _top(_h) == "A" and abs(_h["A"] - 1.0) < 1e-9, "hub is A"
assert _top(_a) == "E" and abs(_a["E"] - 1.0) < 1e-9, "authority is E"
_p = N["PR_plain"]
assert abs(_p["A"] - _p["C"]) < 1e-9 and abs(_p["C"] - _p["E"]) < 1e-9, "three-way tie"
assert min(_p["A"], _p["C"], _p["E"]) > max(_p["B"], _p["D"]) + 0.1, "B, D are below the tie"
assert _top(N["PR"]) == "C", "C is top with teleportation"
assert _top(N["PPR_A"]) == "A", "A is top with teleport to A"
FRAC = {k: Fraction(float(v)).limit_denominator(100) for k, v in _p.items()}
assert FRAC["A"] == FRAC["C"] == FRAC["E"] == Fraction(3, 11)
assert FRAC["B"] == FRAC["D"] == Fraction(1, 11)

LEAK_TOTALS = [float(c.sum()) for c in N["PR_leak_trace"][:5]]
assert [round(t, 2) for t in LEAK_TOTALS] == [1.00, 0.80, 0.60, 0.13, 0.00], LEAK_TOTALS


def frac(f):
    return f"{f.numerator}/{f.denominator}"


def dec(x, d=3):
    return f"{float(x):.{d}f}"




# --------------------------------------------------------------------------- geometry
# The five PageRank pages.  A sends to B, C, D; B and D send to C; C sends to E; E
# sends back to A by a loop under the whole drawing.  Planar, no arrow crosses another.
PR_XY = {"A": (72.0, 205.0), "B": (212.0, 292.0), "D": (212.0, 118.0),
         "C": (352.0, 205.0), "E": (480.0, 205.0)}
PR_LOOP_Y = 26.0                                   # the E -> A return runs along this line
PR_LOOP_X = 28.0                                   # ... and up this one, into A's west side
LOOP_DY = 9.0                                      # the return enters A this far below centre
LOOP_END_X = lambda ax: ax - (HALF + GAP) * 0.9    # a point on A's west border, LOOP_DY below centre
CROSS_AT = 340.0

# The six HITS pages: the square A, D, B, E with A -> C -> F -> E hung on its left side.
HITS_XY = {"A": (225.0, 292.0), "D": (485.0, 292.0), "B": (485.0, 110.0), "E": (225.0, 110.0),
           "C": (52.0, 252.0), "F": (52.0, 150.0)}


def anchors(xy):
    """Invisible discs first, so every arrow can be clipped to a border."""
    return "".join(
        f"\\node[circle,minimum size={BOX}bp,inner sep=0pt,outer sep={GAP}bp] "
        f"({n}) at ({x:.1f},{y:.1f}) {{}};\n" for n, (x, y) in xy.items())


def pages(xy, fills=None):
    """The page discs.  fills = {page: fill}; the default page is white."""
    fills = fills or {}
    return "".join(F.disc(x, y, n, fill=fills.get(n, "white")) for n, (x, y) in xy.items())


def box_of(xy, n, grow=0.0):
    x, y = xy[n]
    return (x - HALF - grow, y - HALF - grow, x + HALF + grow, y + HALF + grow)


def edge(a, b, color="ink", w=F.EDGE_W, dash="", bend=None):
    o = [f"line width={w}bp", f"draw={color}", ARROW]
    if dash:
        o.append(dash)
    if bend:
        return f"\\draw[{','.join(o)}] ({a}) to[bend {bend}] ({b});\n"
    return f"\\draw[{','.join(o)}] ({a}) -- ({b});\n"


def return_path(color="ink", dash=""):
    """E -> A: down from E, along the bottom, up the left side, into A's west border."""
    ex, ey = PR_XY["E"]
    ax, ay = PR_XY["A"]
    o = [f"line width={F.EDGE_W}bp", f"draw={color}", ARROW, "rounded corners=16bp"]
    if dash:
        o.append(dash)
    return (f"\\draw[{','.join(o)}] (E.south) -- ({ex:.1f},{PR_LOOP_Y}) -- ({PR_LOOP_X},{PR_LOOP_Y}) -- "
            f"({PR_LOOP_X},{ay - LOOP_DY:.1f}) -- ({LOOP_END_X(ax):.1f},{ay - LOOP_DY:.1f});\n")


def return_segments():
    ex, ey = PR_XY["E"]
    ax, ay = PR_XY["A"]
    return [((ex, ey - HALF), (ex, PR_LOOP_Y)), ((ex, PR_LOOP_Y), (PR_LOOP_X, PR_LOOP_Y)),
            ((PR_LOOP_X, PR_LOOP_Y), (PR_LOOP_X, ay - LOOP_DY)),
            ((PR_LOOP_X, ay - LOOP_DY), (ax - HALF, ay - LOOP_DY))]


def pr_links(edges):
    out = ""
    for a, b in edges:
        out += return_path() if (a, b) == ("E", "A") else edge(a, b)
    return out


def tbox(x, y, s, anchor="center"):
    """A box for a plain Meslo label (monospaced, so the width is exact)."""
    w = CHAR * len(s) + 2 * CHIP_PAD
    h = 0.95 * F.FONT
    ax = {"center": 0, "west": 0.5, "east": -0.5}[anchor]
    cx = x + ax * w
    return (cx - w / 2, y - h / 2, cx + w / 2, y + h / 2)


def hits_seg(b, p, q, pad=3):
    return F.box_hits_segment(b, p, q, pad=pad)


def chip(x, y, s):
    """A share on an arrow: Meslo on a paper-white chip that interrupts the line."""
    return (f"\\node[font=\\fontsize{{{F.FONT}}}{{{int(F.FONT * 1.15)}}}\\selectfont,text=ink,"
            f"fill=white,inner sep={CHIP_PAD}bp] at ({x:.1f},{y:.1f}) {{{s}}};\n")


# --------------------------------------------------------------------------- score labels
# Where each page's score goes: above B, C, E; below A and D.
SCORE_AT = {"A": (14, -76), "B": (0, 54), "C": (4, 54), "E": (0, 54), "D": (0, -54)}


def score_labels(xy, vals, fmt, winners=(), at=SCORE_AT):
    """Values in ink, the winners' in hot with a hot underline."""
    out, boxes = "", {}
    for n, v in vals.items():
        dx, dy = at[n]
        x, y = xy[n][0] + dx, xy[n][1] + dy
        s = fmt(n, v)
        hot = n in winners
        out += F.text(x, y, s, color="hot" if hot else "ink")
        if hot:
            w = CHAR * len(s)
            out += F.underline(x - w / 2, x + w / 2, y - 18, color="hot")
        boxes[n] = tbox(x, y, s)
    return out, boxes


def check_clear(xy, edges, label_boxes, what, extra_segments=()):
    """No score label touches a page, an arrow or another label."""
    segs = []
    for a, b in edges:
        segs += return_segments() if (a, b) == ("E", "A") else [(xy[a], xy[b])]
    segs += list(extra_segments)
    for n, lb in label_boxes.items():
        assert 4 <= lb[0] and lb[2] <= F.COL_W - 4, f"{what}: label {n} runs off the canvas {lb}"
        for m in xy:
            assert not F.boxes_overlap(lb, box_of(xy, m, 2)), f"{what}: label {n} sits on page {m}"
        for p, q in segs:
            assert not hits_seg(lb, p, q), f"{what}: label {n} sits on an arrow {p}-{q}"
    ks = list(label_boxes)
    for i in range(len(ks)):
        for j in range(i + 1, len(ks)):
            assert not F.boxes_overlap(label_boxes[ks[i]], label_boxes[ks[j]]), \
                f"{what}: labels {ks[i]} and {ks[j]} overlap"


def assert_same_positions(name, xy):
    assert xy is PR_XY or xy == PR_XY, f"{name}: the five pages must sit where every other PageRank figure puts them"


def assert_planar(xy, edges, what):
    straight = [e for e in edges if e != ("E", "A")]
    x = F.crossings(straight, xy)
    assert not x, f"{what}: arrows cross: {x}"
    c = F.clearance_bad(straight, xy, r=HALF * 1.5)
    assert not c, f"{what}: an arrow passes through a page: {c}"
    assert PR_LOOP_Y + F.EDGE_W < min(y for _, y in xy.values()) - HALF - 2, f"{what}: return line hits a page"


def values_fill(vals, winners=()):
    """Winners hot; every other page shaded cool by its share of the largest value."""
    top = max(float(v) for v in vals.values())
    return {n: ("hot" if n in winners else F.shade(float(v) / top)) for n, v in vals.items()}


# --------------------------------------------------------------------------- hits-graph
def fig_hits_graph():
    xy = HITS_XY
    assert set(xy) == set(S.HITS_ORDER)
    edges = S.HITS_EDGES
    assert F.crossings(edges, xy) == [], "hits-graph: arrows cross"
    assert F.clearance_bad(edges, xy, r=HALF * 1.5) == [], "hits-graph: an arrow passes through a page"
    body = anchors(xy)
    for a, b in edges:
        body += edge(a, b)
    body += pages(xy, fills={"A": "hot", "E": "cool"})
    ax, ay = xy["A"]
    ex, ey = xy["E"]
    ta = f"hub {_h['A']:.1f}"
    te = f"authority {_a['E']:.1f}"
    ya, ye = ay + 54, ey - 54
    for (x, y, s, col) in ((ax, ya, ta, "hot"), (ex, ye, te, "cool")):
        lb = tbox(x, y, s)
        assert 4 <= lb[0] and lb[2] <= F.COL_W - 4, f"hits-graph: tag {s!r} runs off the canvas {lb}"
        for m in xy:
            assert not F.boxes_overlap(lb, box_of(xy, m, 2)), f"tag {s!r} sits on page {m}"
        for a, b in edges:
            assert not hits_seg(lb, xy[a], xy[b]), f"tag {s!r} sits on arrow {a}->{b}"
        w = CHAR * len(s)
        body += F.text(x, y, s, color=col) + F.underline(x - w / 2, x + w / 2, y - 18, color=col)
    F.emit("hits-graph", body, container="col", h=CANVAS_H)


# --------------------------------------------------------------------------- shares
def share_chips(xy, edges, t_default=0.5, t_over=None):
    """The vote each arrow carries, in a white chip ON the arrow (1/3 from A, 1 from the rest)."""
    t_over = t_over or {}
    out, boxes = "", []
    outdeg = {}
    for a, _ in edges:
        outdeg[a] = outdeg.get(a, 0) + 1
    for a, b in edges:
        s = "1" if outdeg[a] == 1 else f"1/{outdeg[a]}"
        if a == "A":
            assert s == "1/3"
        else:
            assert s == "1", f"{a} sends {outdeg[a]} links"
        if (a, b) == ("E", "A"):
            ex, _ = xy["E"]
            cx, cy = (ex + PR_LOOP_X) / 2 + 40, PR_LOOP_Y
        else:
            t = t_over.get((a, b), t_default)
            (x0, y0), (x1, y1) = xy[a], xy[b]
            cx, cy = x0 + t * (x1 - x0), y0 + t * (y1 - y0)
        out += chip(cx, cy, s)
        boxes.append(tbox(cx, cy, s))
    return out, boxes


def fig_pr_split(answer=False):
    name = "pr-split-answer" if answer else "pr-split"
    xy = PR_XY
    assert_same_positions(name, xy)
    edges = S.PR_EDGES
    assert_planar(xy, edges, name)
    body = anchors(xy) + pr_links(edges)
    chips, cboxes = share_chips(xy, edges, t_default=0.5,
                                t_over={("A", "B"): 0.45, ("A", "D"): 0.45, ("A", "C"): 0.5})
    for i, cb in enumerate(cboxes):
        for m in xy:
            assert not F.boxes_overlap(cb, box_of(xy, m)), f"{name}: a share chip sits on page {m}"
        for cb2 in cboxes[i + 1:]:
            assert not F.boxes_overlap(cb, cb2), f"{name}: two share chips overlap"
    body += chips
    if answer:
        tie = [n for n in xy if FRAC[n] == Fraction(3, 11)]
        assert sorted(tie) == ["A", "C", "E"]
        body += pages(xy, fills=values_fill(N["PR_plain"], winners=tie))
        sl, lb = score_labels(xy, FRAC, lambda n, v: frac(v), winners=tie)
        check_clear(xy, edges, lb, name)
        body += sl
        for n, b in lb.items():
            for cb in cboxes:
                assert not F.boxes_overlap(b, cb), f"{name}: score {n} overlaps a share chip"
    else:
        body += pages(xy)
    F.emit(name, body, container="col", h=CANVAS_H, box=PR_BOX)


# --------------------------------------------------------------------------- teleport / ppr
def fig_pr_teleport():
    name = "pr-teleport"
    xy = PR_XY
    assert_same_positions(name, xy)
    edges = S.PR_DEAD
    assert ("E", "A") not in edges and not [e for e in edges if e[0] == "E"], "E must be a dead end"
    assert_planar(xy, edges, name)
    assert abs(float(S.PR_R) - 0.15) < 1e-12
    sc = N["PR_dead"]
    assert abs(sum(sc.values()) - 1) < 1e-9
    assert _top(sc) == "E"
    assert [dec(sc[k]) for k in "ECBDA"] == ["0.359", "0.316", "0.117", "0.117", "0.091"]
    body = anchors(xy) + pr_links(edges) + pages(xy, fills=values_fill(sc, winners=["E"]))
    sl, lb = score_labels(xy, sc, lambda n, v: dec(v), winners=["E"])
    check_clear(xy, edges, lb, name)
    tot_r = f"r = {float(S.PR_R):.2f}"
    tot_t = f"total {sum(float(v) for v in sc.values()):.2f}"
    assert tot_t == "total 1.00"
    tx, ty = F.COL_W - 14, 84
    for s_, y_ in ((tot_r, ty + 18), (tot_t, ty - 18)):
        tb = tbox(tx, y_, s_, anchor="east")
        assert tb[0] >= 4, f"{name}: {s_!r} runs off the canvas"
        for m in xy:
            assert not F.boxes_overlap(tb, box_of(xy, m, 2)), f"{name}: {s_!r} sits on page {m}"
        for a_, b_ in edges:
            assert not hits_seg(tb, xy[a_], xy[b_]), f"{name}: {s_!r} sits on arrow {a_}->{b_}"
        for n_, bb_ in lb.items():
            assert not F.boxes_overlap(tb, bb_), f"{name}: {s_!r} overlaps the score of {n_}"
        body += F.text(tx, y_, s_, color="muted", anchor="east")
    F.emit(name, body + sl, container="col", h=CANVAS_H, box=PR_BOX)


# Dashed teleport arrows back to A.  Each one is the twin of a solid link, so each is
# bent away from it, into the free space beside it.
PPR_BEND = {"B": "right=34", "C": "right=26", "D": "right=18"}


def fig_ppr():
    name = "ppr"
    xy = PR_XY
    assert_same_positions(name, xy)
    edges = S.PR_DEAD
    assert ("E", "A") not in edges and not [e for e in edges if e[0] == "E"], "E must be a dead end"
    assert_planar(xy, edges, name)
    sc = N["PPR_A_dead"]
    assert abs(sum(sc.values()) - 1) < 1e-9
    assert dec(sc["A"]) == "0.335"
    assert all(abs(sc[k] - N["PPR_A"][k]) < 1e-9 for k in sc)
    body = anchors(xy) + pr_links(edges)
    tele = ""
    for src in "BCD":
        tele += edge(src, "A", color="muted", dash=F.DASH, bend=PPR_BEND[src])
    # E -> A jump: E has no link out, so the jump takes the free return along the bottom
    tele += return_path(color="muted", dash=F.DASH)
    body += tele + pages(xy, fills=values_fill(sc, winners=["A"]))
    sl, lb = score_labels(xy, sc, lambda n, v: dec(v), winners=["A"])
    body += sl
    F.emit(name, body, container="col", h=CANVAS_H, box=PR_BOX)


# --------------------------------------------------------------------------- pr-leak
def removed_link():
    """The link E -> A that was cut: muted, dashed, with a hot cross on it."""
    out = return_path(color="muted", dash=F.DASH)
    cx, cy, d = CROSS_AT, PR_LOOP_Y, 8.0
    for sgn in (1, -1):
        out += (f"\\draw[line width=3.4bp,draw=hot,line cap=round] "
                f"({cx - d:.1f},{cy - sgn * d:.1f}) -- ({cx + d:.1f},{cy + sgn * d:.1f});\n")
    return out


def fig_pr_leak():
    xy = PR_XY
    assert_same_positions("pr-leak", xy)
    edges = S.PR_DEAD
    assert ("E", "A") not in edges and not [e for e in edges if e[0] == "E"], "E must be a dead end"
    assert_planar(xy, edges, "pr-leak")
    tr = N["PR_leak_trace"][:5]
    top = max(float(c.max()) for c in tr)
    order = S.PR_ORDER
    tot_xy = (xy["D"][0] + 40, 66)
    frames = []
    for k, c in enumerate(tr):
        vals = {n: float(c[i]) for i, n in enumerate(order)}
        fills = {n: F.shade(v / top) for n, v in vals.items()}
        total = sum(vals.values())
        assert abs(total - LEAK_TOTALS[k]) < 1e-9
        body = anchors(xy) + pr_links(edges) + removed_link() + pages(xy, fills=fills)
        body += F.text(F.COL_W - 14, xy["E"][1] + 54, "dead end", color="muted", anchor="east")
        body += F.text(*tot_xy, f"total {total:.2f}", color="hot")
        frames.append(body)
    tb = tbox(F.COL_W - 14, xy["E"][1] + 54, "dead end", anchor="east")
    cb = tbox(*tot_xy, "total 0.00")
    for lb, nm in ((tb, "dead end"), (cb, "total")):
        for m in xy:
            assert not F.boxes_overlap(lb, box_of(xy, m, 2)), f"pr-leak: {nm!r} sits on page {m}"
        for a, b in edges:
            assert not hits_seg(lb, xy[a], xy[b]), f"pr-leak: {nm!r} sits on arrow {a}->{b}"
        for p, q in return_segments():
            assert not hits_seg(lb, p, q), f"pr-leak: {nm!r} sits on the removed link"
    F.emit_frames("pr-leak", frames, container="col", h=CANVAS_H, box=PR_BOX)


FIGURES = [
    ("hits-graph", fig_hits_graph),
    ("pr-split", lambda: fig_pr_split(False)),
    ("pr-split-answer", lambda: fig_pr_split(True)),
    ("pr-leak", fig_pr_leak),
    ("pr-teleport", fig_pr_teleport),
    ("ppr", fig_ppr),
]

if __name__ == "__main__":
    F.run(FIGURES)
