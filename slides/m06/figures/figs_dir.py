#!/usr/bin/env python3
"""Directed-network figures of Module 06: HITS and PageRank, five small drawings.

Pages are rounded boxes with a single letter.  Arrowheads stop at the box border
(every arrow is drawn between named TikZ nodes, so the border does the clipping).
The four PageRank figures put the five pages A-E at the SAME positions (asserted),
so a student sees one web change from slide to slide, not five webs.

Every number printed comes from smallgraphs.compute(); the facts the slides rest on
(hub, authority, the tie, the winners) are asserted before anything is drawn.
"""

from fractions import Fraction

import figlib as F
import smallgraphs as S

A1, A2, GY = "accent", "accenttwo", "annot"
ARROW = "-{Stealth[length=12bp,width=9.5bp]}"
BOX = 42.0                                   # page box side, bp (area-equal disc ~47 bp)
HALF = BOX / 2
CHIP_PAD = 3.0
FS = f"\\fontsize{{{F.FONT}}}{{{int(F.FONT * 1.15)}}}\\selectfont"
GRAY_W = 2.4

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
LOOP_DY = 9.0                                      # the solid return enters A this far below centre

# The six HITS pages: the square A, D, B, E with A -> C -> F -> E hung on its left side.
HITS_XY = {"A": (225.0, 292.0), "D": (485.0, 292.0), "B": (485.0, 110.0), "E": (225.0, 110.0),
           "C": (52.0, 252.0), "F": (52.0, 150.0)}


def anchors(xy):
    """Invisible boxes first, so every arrow can be clipped to a border."""
    return "".join(
        f"\\node[rectangle,minimum width={BOX}bp,minimum height={BOX}bp,inner sep=0pt] "
        f"({n}) at ({x:.1f},{y:.1f}) {{}};\n" for n, (x, y) in xy.items())


def _mix(t):
    """White-ish -> full accent; t in [0, 1] (accent!10 up to accent)."""
    t = 0.10 + 0.90 * max(0.0, min(1.0, float(t)))
    base = tuple(int(F.ACCENT[i:i + 2], 16) for i in (0, 2, 4))
    return "".join(f"{int(round(255 + (c - 255) * t)):02X}" for c in base)


def pages(xy, shade=None, marks=(), mark_color=A2):
    """The page boxes.  shade = {page: t in [0,1]} fills white -> accent."""
    out = ""
    for n, (x, y) in xy.items():
        fill, tc = "white", "black"
        if shade is not None:
            t = shade[n]
            out += f"\\definecolor{{sh{n}}}{{HTML}}{{{_mix(t)}}}\n"
            fill, tc = f"sh{n}", ("white" if t > 0.55 else "black")
        out += (f"\\node[rectangle,rounded corners=8bp,draw=black,line width=1.8bp,"
                f"fill={fill},text={tc},minimum width={BOX}bp,minimum height={BOX}bp,"
                f"inner sep=0pt,font={FS}] at ({x:.1f},{y:.1f}) {{{n}}};\n")
    for n in marks:
        x, y = xy[n]
        out += (f"\\draw[line width=5bp,draw={mark_color},rounded corners=8bp] "
                f"({x - HALF:.1f},{y - HALF:.1f}) rectangle ({x + HALF:.1f},{y + HALF:.1f});\n")
    return out


def box_of(xy, n, grow=0.0):
    x, y = xy[n]
    return (x - HALF - grow, y - HALF - grow, x + HALF + grow, y + HALF + grow)


def edge(a, b, color="black", w=F.EDGE_W, dash="", bend=None, extra=""):
    o = [f"line width={w}bp", f"draw={color}", ARROW]
    if dash:
        o.append(dash)
    if extra:
        o.append(extra)
    if bend:
        return f"\\draw[{','.join(o)}] ({a}) to[bend {bend}] ({b});\n"
    return f"\\draw[{','.join(o)}] ({a}) -- ({b});\n"


def pr_links(edges, loop=True, color="black"):
    """The PageRank links.  E -> A is the long return along the bottom."""
    out = ""
    for a, b in edges:
        if (a, b) == ("E", "A"):
            ex, ey = PR_XY["E"]
            ax, ay = PR_XY["A"]
            out += (f"\\draw[line width={F.EDGE_W}bp,draw={color},{ARROW},rounded corners=16bp] "
                    f"(E.south) -- ({ex:.1f},{PR_LOOP_Y}) -- ({PR_LOOP_X},{PR_LOOP_Y}) -- "
                    f"({PR_LOOP_X},{ay - LOOP_DY:.1f}) -- ({ax - HALF:.1f},{ay - LOOP_DY:.1f});\n")
        else:
            out += edge(a, b, color=color)
    return out


def txt(x, y, s, color="black", anchor="center", fill=None):
    o = [f"font={FS}", f"text={color}", f"anchor={anchor}", "align=center"]
    if fill:
        o += [f"fill={fill}", f"inner sep={CHIP_PAD}bp"]
    return f"\\node[{','.join(o)}] at ({x:.1f},{y:.1f}) {{{s}}};\n"


def text_box(x, y, s, anchor="center", w_per_char=0.45):
    """A measured-ish box for a plain label: Latin Modern text is ~0.45 em a character."""
    w = w_per_char * F.FONT * len(s) + 2 * CHIP_PAD
    h = 0.95 * F.FONT
    ax = {"center": 0, "west": 0.5, "east": -0.5}[anchor]
    cx = x + ax * w
    return (cx - w / 2, y - h / 2, cx + w / 2, y + h / 2)


def hits_seg(b, p, q, pad=3):
    return F.box_hits_segment(b, p, q, pad=pad)


# --------------------------------------------------------------------------- score labels
# Where each page's score goes: above B, C, E; below A and D.
SCORE_AT = {"A": (4, -72), "B": (0, 46), "C": (16, 46), "E": (0, 46), "D": (0, -46)}


def score_labels(xy, vals, fmt, winners=(), at=SCORE_AT):
    out, boxes = "", {}
    for n, v in vals.items():
        dx, dy = at[n]
        x, y = xy[n][0] + dx, xy[n][1] + dy
        s = fmt(n, v)
        out += txt(x, y, s, color=(A2 if n in winners else "black"))
        boxes[n] = text_box(x, y, s)
    return out, boxes


def check_clear(xy, edges, label_boxes, what, loop=True, extra_segments=()):
    """No score label touches a page box, an arrow or another label."""
    segs = []
    for a, b in edges:
        if (a, b) == ("E", "A"):
            ex, ey = xy["E"]
            ax, ay = xy["A"]
            segs += [((ex, ey - HALF), (ex, PR_LOOP_Y)), ((ex, PR_LOOP_Y), (PR_LOOP_X, PR_LOOP_Y)),
                     ((PR_LOOP_X, PR_LOOP_Y), (PR_LOOP_X, ay - LOOP_DY)),
                     ((PR_LOOP_X, ay - LOOP_DY), (ax - HALF, ay - LOOP_DY))]
        else:
            segs.append((xy[a], xy[b]))
    segs += list(extra_segments)
    for n, lb in label_boxes.items():
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
    # the E -> A return runs below every page and clear of D's score label
    assert PR_LOOP_Y + F.EDGE_W < min(y for _, y in xy.values()) - HALF - 2, f"{what}: return line hits a page"


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
    body += pages(xy, marks=("A", "E"))
    ax, ay = xy["A"]
    ex, ey = xy["E"]
    ta = f"hub {_h['A']:.1f}"
    te = f"authority {_a['E']:.1f}"
    ya, ye = ay + 46, ey - 46
    body += txt(ax, ya, ta, color=A2)
    body += txt(ex, ye, te, color=A2)
    # the tags must clear every page and arrow
    for lb, nm in ((text_box(ax, ya, ta), "hub"), (text_box(ex, ye, te), "authority")):
        assert 4 <= lb[0] and lb[2] <= F.COL_W - 4, f"hits-graph: tag {nm!r} runs off the canvas {lb}"
        for m in xy:
            assert not F.boxes_overlap(lb, box_of(xy, m, 2)), f"tag {nm!r} sits on page {m}"
        for a, b in edges:
            assert not hits_seg(lb, xy[a], xy[b]), f"tag {nm!r} sits on arrow {a}->{b}"
    F.emit("hits-graph", body, container="col", h=372)


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
            ax, _ = xy["A"]
            cx, cy = (ex + PR_LOOP_X) / 2 + 40, PR_LOOP_Y
        else:
            t = t_over.get((a, b), t_default)
            (x0, y0), (x1, y1) = xy[a], xy[b]
            cx, cy = x0 + t * (x1 - x0), y0 + t * (y1 - y0)
        out += txt(cx, cy, s, fill="white")
        boxes.append(text_box(cx, cy, s))
    return out, boxes


def fig_pr_split(answer=False):
    name = "pr-split-answer" if answer else "pr-split"
    xy = PR_XY
    assert_same_positions(name, xy)
    edges = S.PR_EDGES
    assert_planar(xy, edges, name)
    body = anchors(xy) + pr_links(edges)
    # chips: nearer the destination on the fan from A so the three do not crowd A
    chips, cboxes = share_chips(xy, edges, t_default=0.5,
                                t_over={("A", "B"): 0.54, ("A", "D"): 0.54, ("A", "C"): 0.5})
    # no chip may sit on a page or another chip
    for i, cb in enumerate(cboxes):
        for m in xy:
            assert not F.boxes_overlap(cb, box_of(xy, m)), f"{name}: a share chip sits on page {m}"
        for cb2 in cboxes[i + 1:]:
            assert not F.boxes_overlap(cb, cb2), f"{name}: two share chips overlap"
    body += chips
    if answer:
        shade = {n: float(N["PR_plain"][n]) / max(N["PR_plain"].values()) for n in xy}
        tie = [n for n in xy if FRAC[n] == Fraction(3, 11)]
        assert sorted(tie) == ["A", "C", "E"]
        body += pages(xy, shade=shade, marks=tie)
        sl, lb = score_labels(xy, FRAC, lambda n, v: frac(v), winners=tie)
        check_clear(xy, edges, lb, name)
        body += sl
        # a score label must not sit under a share chip either
        for n, b in lb.items():
            for cb in cboxes:
                assert not F.boxes_overlap(b, cb), f"{name}: score {n} overlaps a share chip"
    else:
        body += pages(xy)
    F.emit(name, body, container="col", h=372)


# --------------------------------------------------------------------------- teleport / ppr
def fig_pr_teleport():
    name = "pr-teleport"
    xy = PR_XY
    assert_same_positions(name, xy)
    edges = S.PR_EDGES
    assert_planar(xy, edges, name)
    sc = N["PR"]
    assert abs(sum(sc.values()) - 1) < 1e-9
    assert [dec(sc[k]) for k in "CEABD"] == ["0.276", "0.265", "0.255", "0.102", "0.102"]
    shade = {n: float(sc[n]) / max(sc.values()) for n in xy}
    body = anchors(xy) + pr_links(edges) + pages(xy, shade=shade, marks=["C"])
    sl, lb = score_labels(xy, sc, lambda n, v: dec(v), winners=["C"])
    check_clear(xy, edges, lb, name)
    F.emit(name, body + sl, container="col", h=372)


# Dashed teleport arrows back to A.  Each one is the twin of a solid link, so each is
# bent away from it, into the free space beside it.
PPR_BEND = {"B": "right=34", "C": "right=26", "D": "right=18"}


def fig_ppr():
    name = "ppr"
    xy = PR_XY
    assert_same_positions(name, xy)
    edges = S.PR_EDGES
    assert_planar(xy, edges, name)
    sc = N["PPR_A"]
    assert abs(sum(sc.values()) - 1) < 1e-9
    assert dec(sc["A"]) == "0.335"
    shade = {n: float(sc[n]) / max(sc.values()) for n in xy}
    body = anchors(xy) + pr_links(edges)
    ex, ey = xy["E"]
    ax, ay = xy["A"]
    tele = ""
    for src in "BCD":
        tele += edge(src, "A", color=GY, w=GRAY_W, dash=F.DASH, bend=PPR_BEND[src])
    # E -> A teleport: a second return, outside the solid one
    ylo, xlo = PR_LOOP_Y - 18.0, PR_LOOP_X - 18.0
    tele += (f"\\draw[line width={GRAY_W}bp,draw={GY},{F.DASH},{ARROW},rounded corners=16bp] "
             f"({ex + 12:.1f},{ey - HALF:.1f}) -- ({ex + 12:.1f},{ylo}) -- ({xlo},{ylo}) -- "
             f"({xlo},{ay + LOOP_DY:.1f}) -- ({ax - HALF:.1f},{ay + LOOP_DY:.1f});\n")
    body += tele + pages(xy, shade=shade, marks=["A"])
    sl, lb = score_labels(xy, sc, lambda n, v: dec(v), winners=["A"])
    body += sl
    F.emit(name, body, container="col", h=372)


# --------------------------------------------------------------------------- pr-leak
def fig_pr_leak():
    xy = PR_XY
    assert_same_positions("pr-leak", xy)
    edges = S.PR_DEAD
    assert ("E", "A") not in edges and not [e for e in edges if e[0] == "E"], "E must be a dead end"
    assert_planar(xy, edges, "pr-leak")
    tr = N["PR_leak_trace"][:5]
    top = max(float(c.max()) for c in tr)
    order = S.PR_ORDER
    frames = []
    for k, c in enumerate(tr):
        vals = {n: float(c[i]) for i, n in enumerate(order)}
        shade = {n: v / top for n, v in vals.items()}
        total = sum(vals.values())
        assert abs(total - LEAK_TOTALS[k]) < 1e-9
        body = anchors(xy) + pr_links(edges) + pages(xy, shade=shade)
        ex, ey = xy["E"]
        body += txt(F.COL_W - 14, ey - 46, "dead end", color=GY, anchor="east")
        body += txt(xy["D"][0], 48, f"total {total:.2f}", color=A2)
        frames.append(body)
    # tag and counter must clear every page and arrow
    tb = text_box(F.COL_W - 14, xy["E"][1] - 46, "dead end", anchor="east")
    cb = text_box(xy["D"][0], 48, "total 0.00")
    for lb, nm in ((tb, "dead end"), (cb, "total")):
        for m in xy:
            assert not F.boxes_overlap(lb, box_of(xy, m, 2)), f"pr-leak: {nm!r} sits on page {m}"
        for a, b in edges:
            assert not hits_seg(lb, xy[a], xy[b]), f"pr-leak: {nm!r} sits on arrow {a}->{b}"
    F.emit_gif("pr-leak", frames, container="col", h=372, ms=1100, hold=4)


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
