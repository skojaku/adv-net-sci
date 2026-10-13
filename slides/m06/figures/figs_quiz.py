#!/usr/bin/env python3
"""The quiz figures of Module 06 (v3): every question is ONE graph, in the 537 bp `col` container.

    q-close-CB  q-close-CB-ans          closeness, hub N with a triangle against P with two long arms
    q-close-CA  q-close-CA-ans          closeness, hub E against the bridge F          (CA group)
    q-harm-CA-ans                       harmonic on the same CA drawing                 (CA group)
    cut-blank   cut-closeness           CA with the road E-F closed                     (CA group)
    harmonic-def (12 frames)            frame 0 = cut-blank; G's terms, their sum 9/2, the star piece's
                                        scores, the other piece's scores, G hot        (CA group)
    q-harm-HD   q-harm-HD-ans           harmonic on a star and a path of seven
    q-ecc-EA/-ans  q-ecc-EB/-ans        eccentricity: the closeness winner is not the answer
    q-btw-DB/-ans  q-btw-SQ/-ans        betweenness
    q-eig-L  q-eig-L-ans  q-katz-L-ans  eigenvector and Katz on the left graph
    q-eig-R  q-eig-R-ans  q-katz-R-ans  eigenvector and Katz on the right graph

A question carries the edges and a letter in every disc (the eigenvector questions only on the
candidates).  Its answer is the question's TikZ followed by the winner's disc redrawn "hot", the
candidates' values and an underline under the winner's value: `F.emit_group` asserts the prefix, and
crops all of them to one box, so the graph never moves between a question and its answers.

The CA group is drawn on one canvas and cropped to one box; the label slots of the CA group are
solved once, so a value sits in the same place on every slide it appears.

Every number is read from `smallgraphs` and asserted against its facts.
"""

from fractions import Fraction

import networkx as nx
import numpy as np

import figlib as F
import smallgraphs as S

# --------------------------------------------------------------------------- constants
W = F.COL_W                       # 537
CANVAS_H = 420
CY = CANVAS_H / 2
MARGIN = 26                       # a graph's discs keep this far from the canvas edge, left and right
BOUNDS = (10.0, 4.0, W - 10.0, CANVAS_H - 4.0)
OWN = 4.0                         # a value's own disc must be this much nearer than any other
CLEAR = 24.0                      # margins beyond this are equally good
DISC_R = F.NODE / 2
GAP = -2.0                        # figlib.label_box pads by 6 on every side; -2 leaves 4 bp of it
CH = 0.6 * F.FONT                 # MesloLGS NF advance of one character, in bp


def frac(x):
    """27/4, 19/2, 4 -- never a decimal."""
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


def _sides():
    """Where a label may sit relative to its disc: (anchor, dx, dy), nearest first.

    The anchor names the side of the text box that sits at the offset point.  y is up.
    """
    out = []
    for r in (28, 32, 38, 46, 56, 68):
        c = round(r / 2 ** 0.5 * 0.9)
        out += [("south", 0, r), ("north", 0, -r),
                ("south west", c, c), ("north west", c, -c), ("south east", -c, c), ("north east", -c, -c),
                ("west", r, 0), ("east", -r, 0),
                ("south east", 8, r), ("south west", -8, r), ("north east", 8, -r), ("north west", -8, -r)]
    return out


SIDES = _sides()
SIDES_WIDE = SIDES + [(a, dx, dy) for r in (32, 38, 46, 56, 68) for dx in (-40, -32, -24, -16, 16, 24, 32, 40)
                      for a, dy in (("south", r), ("north", -r))]


# --------------------------------------------------------------------------- geometry
def layout(xy, G, smax=None, margin=(MARGIN, MARGIN)):
    """Grid units -> bp: the graph fills the column's width (less the margins) and is centred
    vertically.  margin = (left, right): room kept beside the outermost discs, for values."""
    ml, mr = margin
    xs = [p[0] for p in xy.values()]
    ys = [p[1] for p in xy.values()]
    s = (W - F.NODE - ml - mr) / (max(xs) - min(xs))
    if smax is not None:
        s = min(s, smax)
    x0 = ml + F.NODE / 2 - min(xs) * s
    gy = (min(ys) + max(ys)) / 2
    pos = {n: (round(x0 + x * s, 2), round(CY + (y - gy) * s, 2)) for n, (x, y) in xy.items()}
    assert set(pos) == set(G), "layout and graph must name the same nodes"
    F.assert_planar_drawing(edge_list(G), pos, "quiz graph")
    return pos


def edge_list(G):
    return sorted(tuple(sorted(e)) for e in G.edges)


def question(pos, G, letters=None, dashed=(), extra=""):
    """Edges, then discs with their letters; nothing else.  dashed: edges drawn as closed roads."""
    out = ""
    for a, b in edge_list(G):
        if (a, b) in dashed:
            out += F.seg(pos[a], pos[b], color="muted", w=F.EDGE_W, dash=F.DASH)
        else:
            out += F.seg(pos[a], pos[b])
    for a, b in dashed:
        if not G.has_edge(a, b):
            out += F.seg(pos[a], pos[b], color="muted", w=F.EDGE_W, dash=F.DASH)
    out += extra
    out += "".join(F.disc(x, y, n if letters is None or n in letters else "")
                   for n, (x, y) in sorted(pos.items()))
    return out


# --------------------------------------------------------------------------- label slots
class Spec:
    """One label.  kind: 'val' (a value, ink), 'win' (hot, underlined) or 'lift' (ink, at a winner's
    height, so that the value does not move when it turns hot)."""

    def __init__(self, text, owner, kind="val"):
        self.text, self.owner, self.kind = text, owner, kind

    @property
    def sizing(self):
        return self.text


LIFT = 14     # a winner's value above its disc is lifted this far, so that its underline fits beneath it


def lifted(sp, anc, dy):
    return dy + LIFT if sp.kind in ("win", "lift") and "south" in anc else dy


def solve_slots(specs, pos, edges, blockers=(), bounds=BOUNDS, sides=None, segs=(), fixed=None):
    """Choose a side for every label.  A value must read as belonging to its own disc: no other
    disc may be within OWN bp of being as near to the label as its own.  Same collision tests as figlib.place_labels."""
    for sd in ((SIDES, SIDES_WIDE) if sides is None else (sides,)):
        try:
            return _solve(specs, pos, edges, blockers, bounds, sd, segs, fixed or {})
        except AssertionError:
            pass
    raise AssertionError("no collision-free, unambiguous placement of the values; move a node")


def _solve(specs, pos, edges, blockers, bounds, sides, segs=(), fixed=None):
    rank = {"win": 0, "val": 1}
    order = sorted((k for k in specs if k not in (fixed or {})),
                   key=lambda k: (rank[specs[k].kind], -len(specs[k].sizing)))
    chosen, boxes = {}, {}

    def box_of(k, side):
        sp = specs[k]
        anc, dx, dy = side
        b = F.label_box(pos[sp.owner][0] + dx, pos[sp.owner][1] + lifted(sp, anc, dy), sp.sizing, anc)
        return (b[0] - GAP, b[1] - GAP - (8 if sp.kind == "win" else 0), b[2] + GAP, b[3] + GAP)

    for k, side in (fixed or {}).items():          # hand-chosen slots: checked, then kept
        b = box_of(k, side)
        assert BOUNDS[0] <= b[0] and b[2] <= BOUNDS[2] and BOUNDS[1] <= b[1] and b[3] <= BOUNDS[3], f"slot {k}: out of bounds"
        assert not any(F.box_hits_disc(b, x, y, DISC_R) for x, y in pos.values()), f"slot {k}: hits a disc"
        assert not any(F.box_hits_segment(b, pos[u], pos[v]) for u, v in edges), f"slot {k}: hits an edge"
        assert not any(F.boxes_overlap(b, o) for o in list(boxes.values()) + list(blockers)), f"slot {k}: overlaps a label"
        chosen[k], boxes[k] = side, b

    def candidates(k):
        sp = specs[k]
        n = sp.owner
        out = []
        for i, side in enumerate(sides):
            anc, dx, dy = side
            if sp.kind == "win" and "south" in anc and dy < 34:
                continue                   # the underline sits between the value and the disc
            b = F.label_box(pos[n][0] + dx, pos[n][1] + lifted(sp, anc, dy), sp.sizing, anc)
            b = (b[0] - GAP, b[1] - GAP - (8 if sp.kind == "win" else 0), b[2] + GAP, b[3] + GAP)
            if not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
                continue
            if any(F.box_hits_disc(b, x, y, DISC_R) for x, y in pos.values()):
                continue
            if any(F.boxes_overlap(b, o) for o in list(boxes.values()) + list(blockers)):
                continue
            if any(F.box_hits_segment(b, pos[u], pos[v]) for u, v in edges):
                continue
            if any(F.box_hits_segment(b, p, r, pad=6) for p, r in segs):
                continue
            cx, cy = (b[0] + b[2]) / 2, (b[1] + b[3]) / 2
            own = float(np.hypot(cx - pos[n][0], cy - pos[n][1]))
            m = min(np.hypot(cx - p[0], cy - p[1]) for mm, p in pos.items() if mm != n) - own
            if m > OWN:
                out.append((-min(m, CLEAR), i, side, b))
        return sorted(out, key=lambda c: c[:2])

    steps = [0]

    def solve(i):
        if i == len(order):
            return True
        steps[0] += 1
        assert steps[0] < 20000, f"label search gave up at {order[i]}"
        k = order[i]
        for _, _, side, b in candidates(k):
            chosen[k], boxes[k] = side, b
            if solve(i + 1):
                return True
            del chosen[k], boxes[k]
        return False

    assert solve(0), "no placement"
    return chosen


def _text_x(x, anc, text):
    """The horizontal centre of text placed at x with this anchor."""
    w = CH * len(text)
    return x + (w / 2 if "west" in anc else -w / 2 if "east" in anc else 0)


def draw(spec, side, pos, text=None, color=None):
    """One label in its slot.  A winner's value is hot and underlined.

    The anchor names the side of the text box at the offset point.
    """
    anc, dx, dy = side
    t = spec.text if text is None else text
    x, y = pos[spec.owner][0] + dx, pos[spec.owner][1] + lifted(spec, anc, dy)
    col = color or ("hot" if spec.kind == "win" else "ink")
    out = F.text(x, y, t, color=col, anchor=anc)
    if spec.kind == "win":
        cx = _text_x(x, anc, t)
        uy = y - 40 if "north" in anc else y - LIFT + 3 if "south" in anc else y - 26
        hw = CH * len(t) / 2 + 4
        out += F.underline(cx - hw, cx + hw, uy, color="hot")
    return out


def answer(q, pos, G, values, winners, letters=None, blockers=(), slots=None, level=False):
    """The question's TikZ plus the winner discs, the values and the underlines.

    values: node -> text.  winners: nodes drawn hot.
    """
    # level: the candidates that lose are drawn at a winner's height, so that two answers on one
    # graph (eigenvector, Katz) place the same value in the same spot
    lose = "lift" if level else "val"
    specs = {n: Spec(v, n, "win" if n in winners else lose) for n, v in values.items()}
    chosen = slots if slots is not None else solve_slots(specs, pos, edge_list(G), blockers)
    body = q
    for n in sorted(winners):
        body += F.disc(*pos[n], n if letters is None or n in letters else "", fill="hot")
    for k in sorted(specs):
        body += draw(specs[k], chosen[k], pos)
    return body


def quiz(name, G, xy, values, winners, letters=None, smax=None):
    """Emit  name  and  name-ans  on one crop.  Returns (pos, q, [other items])."""
    pos = layout(xy, G, smax=smax)
    q = question(pos, G, letters=letters)
    a = answer(q, pos, G, values, winners, letters=letters)
    F.emit_group([(name, q), (name + "-ans", a)], container="col", h=CANVAS_H)
    return pos, q


# --------------------------------------------------------------------------- closeness
def _close_facts():
    sumL, sumR = S.dsum(S.CA), S.dsum(S.CB)
    assert S.argbest(sumL, min) == (["F"], 19)
    assert sumL["E"] == sumL["G"] == 20
    assert dict(S.CA.degree)["E"] == 5 and dict(S.CA.degree)["F"] == 2
    assert S.argbest(sumR, min) == (["P"], 16) and sumR["N"] == 18
    assert dict(S.CB.degree)["N"] == 4 and dict(S.CB.degree)["P"] == 3
    return sumL, sumR


def close_CB():
    _, sumR = _close_facts()
    quiz("q-close-CB", S.CB, S.CB_XY, {n: str(sumR[n]) for n in "NP"}, {"P"})


# --------------------------------------------------------------------------- the CA group
CA_POS = layout(S.CA_XY, S.CA)
CA_CUT_EDGE = ("E", "F")
_mid = tuple((np.array(CA_POS["E"]) + np.array(CA_POS["F"])) / 2)
CR = 12                                                     # half-size of the cross on the closed road
CROSS_BLOCK = (_mid[0] - CR - 6, _mid[1] - CR - 6, _mid[0] + CR + 6, _mid[1] + CR + 6)


def _cross():
    m = _mid
    return (F.seg((m[0] - CR, m[1] - CR), (m[0] + CR, m[1] + CR), color="hot", w=5)
            + F.seg((m[0] - CR, m[1] + CR), (m[0] + CR, m[1] - CR), color="hot", w=5))


def union_box(bodies, h=CANVAS_H, container="col"):
    """The (top, bottom) in bp of the crop that holds the ink of every body."""
    lo, hi = 10 ** 9, -1
    for b in bodies:
        a = np.asarray(F.render(b, F.DESIGN[container], h).convert("L"))
        ys, _ = np.where(a < 200)
        lo, hi = min(lo, ys.min()), max(hi, ys.max())
    pad = int(F.PAD * F.PXBP)
    return (max(0, lo - pad) / F.PXBP, min(h * F.PXBP, hi + pad) / F.PXBP)


# Every value sits directly above or directly below its own disc (never beside it, never over an edge).
# The three quiz candidates sit on one line: E's above E, F's below F, G's above G (the block H-I-J-K is
# drawn low and to the right so that G's value has the room).
CA_SLOTS = {"E": ("south", 0, 32), "F": ("north", 0, -28), "G": ("south", 0, 32)}
VSIDES = [(a, 0, d) for r in (28, 32, 38, 46, 56, 64, 72, 80) for a, d in (("south", r), ("north", -r))]


def ca_group():
    sumL, _ = _close_facts()
    hL = S.harmonic(S.CA)
    assert S.argbest(hL) == (["E"], Fraction(27, 4))
    assert hL["G"] == Fraction(19, 3) and hL["F"] == Fraction(35, 6)
    G, Gc = S.CA, S.CA_CUT
    hc = S.harmonic(Gc)
    assert S.argbest(hc) == (["G"], Fraction(9, 2))
    assert set(S.closeness(Gc).values()) == {0}
    L = S.dist(Gc, "G")
    one = [n for n in sorted(L) if L[n] == 1]
    assert one == ["F", "H", "I", "J"] and [n for n in L if L[n] == 2] == ["K"]
    other = [n for n in sorted(Gc) if n not in L]
    assert other == list("ABCDE")

    pos = CA_POS
    edges = edge_list(G)                                    # includes E-F: it is drawn, dashed, on the cut
    q = question(pos, G)
    cut = question(pos, G, dashed=[CA_CUT_EDGE], extra=_cross())

    # one set of slots for the whole group: every node gets a slot for its final harmonic score,
    # and E, F, G (the quiz candidates, the cut's winner) get a slot fit for an underlined value
    final = {n: frac(x) for n, x in hc.items()}
    uses = {n: [final[n]] for n in pos}
    for n in "EFG":
        uses[n] += [str(sumL[n]), frac(hL[n])]
    widest = {n: max(t, key=len) for n, t in uses.items()}
    specs = {n: Spec(widest[n], n, "win" if n in "EFG" else "val") for n in pos}
    slots = solve_slots(specs, pos, edges, blockers=[CROSS_BLOCK], fixed=CA_SLOTS, sides=VSIDES)

    # q-close-CA-ans / q-harm-CA-ans use the same slots
    def ans(values, winners):
        sp = {n: Spec(v, n, "win" if n in winners else "val") for n, v in values.items()}
        body = q
        for n in sorted(winners):
            body += F.disc(*pos[n], n, fill="hot")
        for n in sorted(sp):
            body += draw(sp[n], slots[n], pos)
        return body

    close_ans = ans({n: str(sumL[n]) for n in "EFG"}, {"F"})
    harm_ans = ans({n: frac(hL[n]) for n in "EFG"}, {"E"})

    zeros = "".join(draw(Spec("0", n), slots[n], pos) for n in sorted(pos))
    cut_close = cut + zeros

    def frame(vals, win=None, source=None, lift=()):
        body = cut
        if source:
            body += F.disc(*pos[source], source, fill="cool")
        if win:
            body += F.disc(*pos[win], win, fill="hot")
        for n in sorted(vals):
            kind = "win" if n == win else "lift" if n in lift else "val"
            body += draw(Spec(vals[n], n, kind), slots[n], pos)
        return body

    frames = [cut, frame({}, source="G")]
    v = {}
    for n in one:
        v[n] = "1/1"
        frames.append(frame(v, source="G"))
    v["K"] = "1/2"
    frames.append(frame(v, source="G"))
    v.update({n: "0" for n in other})
    frames.append(frame(v, source="G"))                                   # 07: G's terms
    g = {"G": frac(hc["G"])}
    frames.append(frame({**v, **g}, source="G", lift="G"))                # 08: their sum, in ink
    frames.append(frame(g, source="G", lift="G"))                         # 09: the terms cleared
    star = {n: frac(hc[n]) for n in other}
    frames.append(frame({**g, **star}, source="G", lift="G"))             # 10: the star piece's scores
    rest = {n: frac(hc[n]) for n in "FHIJK"}
    frames.append(frame(final, win="G"))                                  # 11: the other piece, then G wins
    assert len(frames) == 12 and final == {**g, **star, **rest}
    assert frames[0] == cut

    bodies = [q, close_ans, harm_ans, cut, cut_close] + frames[1:]
    box = union_box(bodies)
    F.emit_group([("q-close-CA", q), ("q-close-CA-ans", close_ans), ("q-harm-CA-ans", harm_ans),
                  ("cut-blank", cut), ("cut-closeness", cut_close)],
                 container="col", h=CANVAS_H, box=box, prefix=False)
    F.emit_frames("harmonic-def", frames, container="col", h=CANVAS_H, box=box)


# --------------------------------------------------------------------------- harmonic, HD
def harm_HD():
    hR = S.harmonic(S.HD)
    assert S.argbest(hR) == (["N"], Fraction(4)) and hR["T"] == Fraction(11, 3)
    values = {"N": frac(hR["N"]), "T": frac(hR["T"])}
    assert values == {"N": "4", "T": "11/3"}
    quiz("q-harm-HD", S.HD, S.HD_XY, values, {"N"}, smax=70)


# --------------------------------------------------------------------------- eccentricity
def ecc():
    sL, sR = S.dsum(S.EA), S.dsum(S.EB)
    eL, eR = S.eccentricity(S.EA), S.eccentricity(S.EB)
    assert S.argbest(sL, min) == (["E"], 10) and S.argbest(eL, min) == (["F"], 2)
    assert eL["E"] == 3
    assert S.argbest(sR, min) == (["K"], 11) and S.argbest(eR, min) == (["L"], 2)
    assert sR["L"] == 12 and eR["K"] == 3 and dict(S.EB.degree)["L"] == 2
    quiz("q-ecc-EA", S.EA, S.EA_XY, {"E": str(eL["E"]), "F": str(eL["F"])}, {"F"})
    quiz("q-ecc-EB", S.EB, S.EB_XY, {"K": str(eR["K"]), "L": str(eR["L"])}, {"L"})


# --------------------------------------------------------------------------- betweenness
def btw():
    bL, bR = S.betweenness(S.DB), S.betweenness(S.SQ)
    assert S.argbest(bL) == (["E", "G"], 30) and bL["F"] == 25
    assert S.argbest(bR) == (["O"], Fraction(19, 2)) and bR["M"] == 9
    assert dict(S.SQ.degree)["O"] == dict(S.SQ.degree)["M"] == 3
    values = {n: frac(bL[n]) for n in "EFG"}
    assert values == {"E": "30", "F": "25", "G": "30"}
    quiz("q-btw-DB", S.DB, S.DB_XY, values, {"E", "G"})
    values = {n: frac(bR[n]) for n in "MO"}
    assert values == {"M": "9", "O": "19/2"}
    quiz("q-btw-SQ", S.SQ, S.SQ_XY, values, {"O"})


# --------------------------------------------------------------------------- eigenvector, Katz
def eig():
    NN = S.compute()
    ev, kq = NN["EQ"], NN["KQ"]
    assert ev["left"]["M"] > ev["left"]["X"] and dict(S.EQ_L.degree)["M"] < dict(S.EQ_L.degree)["X"]
    assert ev["right"]["K"] > ev["right"]["H"] and dict(S.EQ_R.degree)["K"] < dict(S.EQ_R.degree)["H"]
    assert kq["left"]["M"] > kq["left"]["X"] and kq["right"]["H"] > kq["right"]["K"]
    assert S.EQ_LABELS == {"left": ["M", "X"], "right": ["H", "K"]}
    for side, G, xy, cand, e_win, k_win in (("L", S.EQ_L, S.EQ_L_XY, "MX", "M", "M"),
                                            ("R", S.EQ_R, S.EQ_R_XY, "HK", "K", "H")):
        key = "left" if side == "L" else "right"
        pos = layout(xy, G, smax=EQ_SMAX[side])
        q = question(pos, G, letters=set(cand))
        ev_v = {n: f"{ev[key][n]:.2f}" for n in cand}
        kq_v = {n: f"{kq[key][n]:.2f}" for n in cand}
        # one set of slots, solved as if every candidate won, so that a value is in the same place on
        # the eigenvector answer and on the Katz answer (slide 70 shows the flip, nothing else moves)
        both = {n: Spec(ev_v[n], n, "win") for n in cand}
        slots = solve_slots(both, pos, edge_list(G))
        a = answer(q, pos, G, ev_v, {e_win}, letters=set(cand), slots=slots, level=True)
        k = answer(q, pos, G, kq_v, {k_win}, letters=set(cand), slots=slots, level=True)
        F.emit_group([(f"q-eig-{side}", q), (f"q-eig-{side}-ans", a), (f"q-katz-{side}-ans", k)],
                     container="col", h=CANVAS_H)


EQ_SMAX = {"L": None, "R": None}


FIGURES = [
    ("q-close-CB", close_CB),
    ("q-CA-group", ca_group),
    ("q-harm-HD", harm_HD),
    ("q-ecc", ecc),
    ("q-btw", btw),
    ("q-eig", eig),
]
