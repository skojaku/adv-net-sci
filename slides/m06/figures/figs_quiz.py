#!/usr/bin/env python3
"""The quiz figures of Module 06: closeness, harmonic, eccentricity, betweenness, and the cut.

    quiz-close / quiz-close-answer    CA | CB     (full)
    quiz-harm  / quiz-harm-answer     CA | HD     (full)
    quiz-ecc   / quiz-ecc-answer      EA | EB     (full)
    quiz-btw   / quiz-btw-answer      DB | SQ     (full)
    cut-blank / cut-closeness         CA_CUT      (col)

A question figure carries the two graphs, the edges and a letter in every disc, and nothing
else.  The answer figure is the question figure's TikZ followed by marks and values: the
builder asserts that the answer body *starts with* the question body, so the geometry cannot
differ.  The pair is also cropped to one common box, so the graphs do not move when the slide
changes from the question to the answer.

Every value is read from `smallgraphs` (dsum, harmonic, eccentricity, betweenness) and
printed as a fraction when it is one.  Winners are asserted with the facts of
`smallgraphs.check()`.
"""

from fractions import Fraction

import numpy as np

import figlib as F
import smallgraphs as S

# --------------------------------------------------------------------------- constants
CW = F.FULL_W                     # 1080
HALF = (20.0, 520.0), (560.0, 1060.0)
CANVAS_H = 460                    # tall enough for every pair; the pair is cropped to its ink
CY = CANVAS_H / 2
BOUNDS = (4.0, 4.0, CW - 4.0, CANVAS_H - 4.0)
OWN = 4.0                         # a label's own disc must be this much nearer than any other
CLEAR = 24.0                      # margins beyond this are equally good
GAP = -4.0                        # figlib.label_box pads its boxes by 6 on every side; -4 leaves 2 bp of that

RED, GRAY_C = "accenttwo", "annot"


# Where a value may sit, best first: directly above or below its disc (the least ambiguous),
# then the diagonals, then the sides, then the same again one step further out.
def _sides():
    """Candidate positions of a label relative to its disc: (anchor, dx, dy), nearest first.

    At each distance r: straight above and below, the four diagonals, the left and right
    sides, and the above/below positions shifted so that the label's far edge sits over the
    disc's centre (they let a wide label sit beside a neighbour without crowding it).
    """
    out = []
    for r in (24, 28, 34, 42, 54, 68):
        c = round(r / 2 ** 0.5 * 0.9)
        out += [("south", 0, r), ("north", 0, -r),
                ("south west", c, c), ("north west", c, -c), ("south east", -c, c), ("north east", -c, -c),
                ("west", r, 0), ("east", -r, 0),
                ("south east", 8, r), ("south west", -8, r), ("north east", 8, -r), ("north west", -8, -r)]
    return out


SIDES = _sides()
F.SIDES = SIDES            # figlib.place_labels reads this module-level list


# CA with the hub E moved 0.4 units left (and its four leaves with it): the gap E-F grows from 1.4
# to 1.8 units, so that a value such as "27/4" beside E is not mistaken for F's.  Still a hub with
# four leaves, a bridge, a cluster with a tail; the total width is unchanged.
CA_XY = S.CA_XY        # the spacing fix now lives in smallgraphs, shared with harmonic-def
assert set(CA_XY) == set(S.CA_XY)

# HD with the star's arms 1.2 long instead of 1.0, for the same reason: the hub N's value must
# fit between two neighbours and still read as N's.
HD_XY = S.HD_XY
assert set(HD_XY) == set(S.HD_XY)


def frac(x):
    """27/4, 19/2, 4 -- never a decimal."""
    x = Fraction(x)
    return str(x.numerator) if x.denominator == 1 else f"{x.numerator}/{x.denominator}"


# --------------------------------------------------------------------------- geometry
def scale_for(*xys):
    """One scale for every graph on a slide: the widest graph fills its half."""
    span = max(max(x for x, _ in xy.values()) - min(x for x, _ in xy.values()) for xy in xys)
    return (HALF[0][1] - HALF[0][0] - F.NODE) / span


def place(xy, s, x_lo, x_hi):
    """Grid units -> bp, scaled by s and centred in [x_lo, x_hi] and on the canvas's mid-line."""
    xs = [p[0] for p in xy.values()]
    ys = [p[1] for p in xy.values()]
    gx, gy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    cx = (x_lo + x_hi) / 2
    return {n: (round(cx + (x - gx) * s, 2), round(CY + (y - gy) * s, 2)) for n, (x, y) in xy.items()}


def edge_list(G):
    return sorted(tuple(sorted(e)) for e in G.edges)


def layout_pair(GL, XYL, GR, XYR):
    s = scale_for(XYL, XYR)
    pos = {}
    pl, pr = place(XYL, s, *HALF[0]), place(XYR, s, *HALF[1])
    assert not set(pl) & set(pr), "the two graphs on a slide must not share a letter"
    pos.update(pl)
    pos.update(pr)
    edges = edge_list(GL) + edge_list(GR)
    F.assert_planar_drawing(edge_list(GL), pl, "left graph")
    F.assert_planar_drawing(edge_list(GR), pr, "right graph")
    return pos, edges, s


def base_body(pos, edges, edge_extra=""):
    """Edges, then discs with their letters.  Nothing else: this is the question."""
    out = "".join(F.seg(pos[a], pos[b]) for a, b in edges)
    out += edge_extra
    out += "".join(F.disc(x, y, n) for n, (x, y) in sorted(pos.items()))
    return out


# --------------------------------------------------------------------------- labels
def _margin(box, n, pos):
    """How much nearer the label's own disc is than any other (negative if another is nearer)."""
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    own = np.hypot(cx - pos[n][0], cy - pos[n][1])
    return min(np.hypot(cx - p[0], cy - p[1]) for m, p in pos.items() if m != n) - own


def place_owned(names, pos, edges, blockers=(), bounds=BOUNDS):
    """figlib.place_labels plus one more rule: a value must read as belonging to its own disc.

    Same collision tests as figlib (other labels, every disc, every edge, blockers, canvas),
    same backtracking.  A candidate side is rejected when another disc is within OWN bp of being
    as close to the label's centre as its own, and the surviving sides are tried best-margin
    first (margins above CLEAR count as equal, so a tidy nearby spot beats a distant one).
    """
    order = sorted(names, key=lambda n: -len(names[n]))
    chosen, boxes = {}, {}

    def candidates(n):
        out = []
        for i, side in enumerate(SIDES):
            anc, dx, dy = side
            b = F.label_box(pos[n][0] + dx, pos[n][1] + dy, names[n], anc)
            b = (b[0] - GAP, b[1] - GAP, b[2] + GAP, b[3] + GAP)
            if not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
                continue
            if any(F.box_hits_disc(b, x, y) for x, y in pos.values()):
                continue
            if any(F.boxes_overlap(b, o) for o in list(boxes.values()) + list(blockers)):
                continue
            if any(F.box_hits_segment(b, pos[u], pos[v]) for u, v in edges):
                continue
            m = _margin(b, n, pos)
            if m > OWN:
                out.append((-min(m, CLEAR), i, side, b))
        return sorted(out, key=lambda c: c[:2])

    def solve(i):
        if i == len(order):
            return True
        n = order[i]
        for _, _, side, b in candidates(n):
            chosen[n], boxes[n] = side, b
            if solve(i + 1):
                return True
            del chosen[n], boxes[n]
        return False

    assert solve(0), "no collision-free, unambiguous placement of the values; move a node"
    return chosen, boxes


def _seg_hits_box(p, q, b):
    return F.box_hits_segment(b, p, q, pad=0)


def place_tag(n, s, pos, edges, taken, bounds=BOUNDS):
    """A gray tag too wide to sit beside its disc: put it in free space, joined by a gray leader.

    The nearest free spot within reach, tried on 24 directions and growing radii.  The box
    must clear every disc, every edge and every other label; the leader (disc border to box)
    must cross no edge and touch no other disc.
    """
    cx, cy = pos[n]
    for r in range(70, 190, 6):
        for k in range(24):
            a = 2 * np.pi * k / 24
            x, y = cx + r * np.cos(a), cy + r * np.sin(a)
            b = F.label_box(x, y, s, "center")
            b = (b[0] + 4, b[1] + 4, b[2] - 4, b[3] - 4)           # the box without its padding
            if not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
                continue
            if any(F.box_hits_disc(b, px, py, F.NODE / 2 + 6) for px, py in pos.values()):
                continue
            if any(F.boxes_overlap(b, o) for o in taken):
                continue
            if any(F.box_hits_segment(b, pos[u], pos[v], pad=6) for u, v in edges):
                continue
            # leader: from the disc border towards the box, stopped at the box
            d = np.array([x - cx, y - cy]); d /= np.linalg.norm(d)
            p0 = np.array([cx, cy]) + d * (F.NODE / 2 + 3)
            q = p0.copy()
            for _ in range(400):
                if b[0] - 3 <= q[0] <= b[2] + 3 and b[1] - 3 <= q[1] <= b[3] + 3:
                    break
                q = q + d
            else:
                continue
            if any(F._seg_cross(tuple(p0), tuple(q), pos[u], pos[v]) for u, v in edges):
                continue
            if any(F.box_hits_segment(o, tuple(p0), tuple(q), pad=2) for o in taken):
                continue
            if any(m != n and _dist_seg_pt(p0, q, np.array(pm)) < F.NODE / 2 + 3 for m, pm in pos.items()):
                continue
            ink = F.seg(tuple(p0), tuple(q), color=GRAY_C, w=2.2)
            ink += F.text(x, y, s, color=GRAY_C)
            return ink, b
    raise AssertionError(f"no free spot for the tag {s!r} of {n}")


def _dist_seg_pt(p, q, c):
    d = q - p
    t = max(0.0, min(1.0, float((c - p) @ d) / float(d @ d)))
    return float(np.linalg.norm(p + t * d - c))


def solve_labels(texts, pos, edges, blockers=(), bounds=BOUNDS):
    """texts: node -> (sizing string, tikz string, colour).  Returns the TikZ and the label boxes.

    The sizing string is plain (what figlib.label_box measures); the TikZ string may carry
    colour commands.
    """
    chosen, boxes = place_owned({n: v[0] for n, v in texts.items()}, pos, edges, blockers, bounds)
    out = ""
    for n, (anc, dx, dy) in chosen.items():
        _, tikz, col = texts[n]
        out += F.text(pos[n][0] + dx, pos[n][1] + dy, tikz, color=col, anchor=anc)
    return out, boxes


# --------------------------------------------------------------------------- pair emitter
def emit_pair(nameq, bodyq, namea, bodya, container="full", h=CANVAS_H):
    """Render a question and its answer and crop both to ONE box.

    figlib.emit crops each figure to its own ink, which would move the graphs by a few bp
    between the question slide and the answer slide.  Here both images are cropped to the
    union of their ink, and figlib's gates are run on the cropped images.
    """
    import numpy as _np
    names = [nameq, namea]
    if F._only and not any(k in n for n in names for k in F._only):
        return
    try:
        assert bodya.startswith(bodyq), f"{namea}: the answer must be the question plus marks and values"
        W = F.DESIGN[container]
        ims = [F.render(b, W, h) for b in (bodyq, bodya)]
        lo, hi = 10 ** 9, -1
        for im in ims:
            ys, _x = _np.where(_np.array(im.convert("L")) < 200)
            lo, hi = min(lo, ys.min()), max(hi, ys.max())
        pad = int(F.PAD * F.PXBP)
        lo, hi = max(0, lo - pad), min(ims[0].size[1], hi + pad)
        for name, im in zip(names, ims):
            im = im.crop((0, lo, im.size[0], hi))
            F.crop_and_check(name, im, container, "")          # the gates, on the shared crop
            fw, fh = im.size
            node_px, x_px = F.NODE, F.FONT * F.calibrate()
            a = _np.array(im.convert("L"))
            span = (_np.ptp(_np.where(a < 200)[1]) + 1) / fw
            im.save(F.OUT / f"{name}.png")
            F._built.append(name)
            print(f"  {name}.png  {fw // 4}x{fh // 4}bp  node {node_px:.0f}px  x-h {x_px:.1f}px  "
                  f"ink {span:.0%}  [{container}]")
    except (AssertionError, SystemExit) as e:
        F._failures.append((nameq, str(e)))
        print(f"  FAIL {nameq}/{namea}: {e}")


# --------------------------------------------------------------------------- the four quizzes
def quiz(slug, GL, XYL, GR, XYR, values, winners, extra_tags=None, who_labelled=None):
    """values: node -> display string; winners: nodes to mark; extra_tags: node -> gray tag."""
    pos, edges, s = layout_pair(GL, XYL, GR, XYR)
    q = base_body(pos, edges)
    texts = {}
    for n, v in values.items():
        assert n in pos
        texts[n] = (v, v, RED if n in winners else "black")
    lab, boxes = solve_labels(texts, pos, edges)
    for n, tag in (extra_tags or {}).items():
        t_ink, tb = place_tag(n, tag, pos, edges, list(boxes.values()))
        lab += t_ink
        boxes[n + "#tag"] = tb
    marks = "".join(F.mark(*pos[n]) for n in sorted(winners))
    a = q + marks + lab
    emit_pair(f"quiz-{slug}", q, f"quiz-{slug}-answer", a)
    return pos


# ---- closeness
def quiz_close():
    sumL, sumR = S.dsum(S.CA), S.dsum(S.CB)
    # the facts of smallgraphs.check()
    assert S.argbest(sumL, min) == (["F"], 19)
    assert sumL["E"] == sumL["G"] == 20
    assert dict(S.CA.degree)["E"] == 5 and dict(S.CA.degree)["F"] == 2
    assert S.argbest(sumR, min) == (["P"], 16) and sumR["N"] == 18
    assert dict(S.CB.degree)["N"] == 4 and dict(S.CB.degree)["P"] == 3
    values = {n: str(sumL[n]) for n in "EFG"} | {n: str(sumR[n]) for n in "NP"}
    quiz("close", S.CA, CA_XY, S.CB, S.CB_XY, values, winners={"F", "P"})


# ---- harmonic
def quiz_harm():
    hL, hR = S.harmonic(S.CA), S.harmonic(S.HD)
    assert S.argbest(hL) == (["E"], Fraction(27, 4))
    assert hL["G"] == Fraction(19, 3) and hL["F"] == Fraction(35, 6)
    assert S.argbest(hR) == (["N"], Fraction(4)) and hR["T"] == Fraction(11, 3)
    values = {n: frac(hL[n]) for n in "EGF"} | {n: frac(hR[n]) for n in "NT"}
    assert values == {"E": "27/4", "G": "19/3", "F": "35/6", "N": "4", "T": "11/3"}
    quiz("harm", S.CA, CA_XY, S.HD, HD_XY, values, winners={"E", "N"})


# ---- eccentricity
def quiz_ecc():
    sL, sR = S.dsum(S.EA), S.dsum(S.EB)
    eL, eR = S.eccentricity(S.EA), S.eccentricity(S.EB)
    assert S.argbest(sL, min) == (["E"], 10) and S.argbest(eL, min) == (["F"], 2)
    assert eL["E"] == 3
    assert S.argbest(sR, min) == (["K"], 11) and S.argbest(eR, min) == (["L"], 2)
    assert sR["L"] == 12 and eR["K"] == 3 and dict(S.EB.degree)["L"] == 2
    values = {n: str(e) for n, e in (eL | eR).items()}
    quiz("ecc", S.EA, S.EA_XY, S.EB, S.EB_XY, values, winners={"F", "L"},
         extra_tags={"E": "closeness", "K": "closeness"})


# ---- betweenness
def quiz_btw():
    bL, bR = S.betweenness(S.DB), S.betweenness(S.SQ)
    assert S.argbest(bL) == (["E", "G"], 30) and bL["F"] == 25
    assert S.argbest(bR) == (["O"], Fraction(19, 2)) and bR["M"] == 9
    assert dict(S.SQ.degree)["O"] == dict(S.SQ.degree)["M"] == 3
    values = {n: frac(bL[n]) for n in "EFG"} | {n: frac(bR[n]) for n in "MO"}
    assert values == {"E": "30", "F": "25", "G": "30", "M": "9", "O": "19/2"}
    quiz("btw", S.DB, S.DB_XY, S.SQ, S.SQ_XY, values, winners={"E", "G", "O"})


# --------------------------------------------------------------------------- the cut
def cut_figures():
    G = S.CA_CUT
    c = S.closeness(G)
    assert set(c.values()) == {0}, "after the cut every closeness is 0"
    assert not S.nx.is_connected(G)
    W = F.COL_W
    xy = CA_XY
    s = (W - F.NODE - 2 * 30) / (max(x for x, _ in xy.values()) - min(x for x, _ in xy.values()))
    xs = [p[0] for p in xy.values()]
    ys = [p[1] for p in xy.values()]
    gx, gy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    h = 380
    pos = {n: (round(W / 2 + (x - gx) * s, 2), round(h / 2 + (y - gy) * s, 2)) for n, (x, y) in xy.items()}
    edges = edge_list(G)
    F.assert_planar_drawing(edges, pos, "cut graph")
    # The closed road E-F: dashed gray, crossed out in accent-2 (the one thing the slide is about).
    p, q = np.array(pos["E"]), np.array(pos["F"])
    m = (p + q) / 2
    r = 11
    closed = F.seg(pos["E"], pos["F"], color=GRAY_C, w=F.EDGE_W, dash=F.DASH)
    closed += F.seg((m[0] - r, m[1] - r), (m[0] + r, m[1] + r), color=RED, w=5)
    closed += F.seg((m[0] - r, m[1] + r), (m[0] + r, m[1] - r), color=RED, w=5)
    blocker = (m[0] - r - 4, m[1] - r - 4, m[0] + r + 4, m[1] + r + 4)
    body = base_body(pos, edges, edge_extra=closed)

    zeros = {n: ("0", "0", "black") for n in pos}
    names = {n: v[0] for n, v in zeros.items()}
    chosen, boxes = place_owned(names, pos, edges + [("E", "F")], blockers=[blocker],
                                bounds=(4.0, 4.0, W - 4.0, h - 4.0))
    lab = ""
    for n, (anc, dx, dy) in chosen.items():
        lab += F.text(pos[n][0] + dx, pos[n][1] + dy, "0", anchor=anc)
    emit_pair("cut-blank", body, "cut-closeness", body + lab, container="col", h=h)


FIGURES = [
    ("quiz-close", quiz_close),
    ("quiz-harm", quiz_harm),
    ("quiz-ecc", quiz_ecc),
    ("quiz-btw", quiz_btw),
    ("cut", cut_figures),
]
