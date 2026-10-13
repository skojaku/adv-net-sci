#!/usr/bin/env python3
"""Module 06, eigenvectors, localization and Katz: the figures of `figs_eigen` (v3 style).

    cd slides/m06/figures && python3 -c "import figlib as F, figs_eigen as M; F.run(M.FIGURES)"

Every number printed here is computed from `smallgraphs` (the 7-node graph `EIG`, the clique
ring, `W5`); nothing is typed.  Style: figlib's palette.  A score is `F.shade(v)` (near-paper to
saturated cool, v = score / largest score), a sign is cool (positive) or hot (negative), hot also
marks the one node the slide is about, routes and flows are brush strokes, labels are MesloLGS NF
(its Greek letters and x included, so no math mode is needed).

Figures (all `col` unless noted):

* EIG group, one box: `eigen-inherit` frames (the scores of A's neighbours arrive one at a
  time as a running sum, then A's score, then the rest) and `eig-pf` (= its last frame).
* `eigen-equation`: A c = lambda c as hand-drawn boxes.
* Panels, `full`, one crop: `eig-all-q` and `eig-all` (= eig-all-q + the highlight).
* Ring group, one box: `ring-4444` and the `ring-local` frames (frame 0 = ring-4444).
* `katz-floor`, `walks-discount` frames.

`eig-centrality` is no longer built (the deck uses `eig-pf`).
"""

import itertools
import math

import networkx as nx
import numpy as np

import figlib as F
import smallgraphs as S
from figlib import FONT

W_COL, W_FULL = F.COL_W, F.FULL_W

# --------------------------------------------------------------------------- the 7-node graph
NAMES = S.EIG_ORDER
EDGES = [(a, b) for a, b in S.EIG.edges()]
DEG = dict(S.EIG.degree)
A_MAT, EVALS, EVECS = S.spectrum(S.EIG, NAMES)           # eigh: ascending eigenvalues
LAM1 = float(EVALS[-1])
U1 = EVECS[:, -1]                                         # unit length, all positive
V1 = dict(zip(NAMES, U1 / U1.max()))                      # largest entry is 1.00 (smallgraphs.EIG_v)

_xs = [p[0] for p in S.EIG_XY.values()]
_ys = [p[1] for p in S.EIG_XY.values()]
GX, GY = (min(_xs) + max(_xs)) / 2, (min(_ys) + max(_ys)) / 2
GW, GH = max(_xs) - min(_xs), max(_ys) - min(_ys)       # 3.3 x 2.9 grid units


def eig_layout(sx, cx, cy, sy=None):
    """The 7-node layout scaled by sx (and sy) around the point (cx, cy), y up."""
    sy = sy or sx
    return {k: (cx + sx * (x - GX), cy + sy * (y - GY)) for k, (x, y) in S.EIG_XY.items()}


# --------------------------------------------------------------------------- drawing helpers
def edges_body(edges, pos, w=F.EDGE_W):
    return "".join(F.seg(pos[a], pos[b], w=w) for a, b in edges)


def est_w(s, size=FONT):
    """Width in bp of a string in MesloLGS NF (monospaced, 0.6 em per character)."""
    return 0.6 * size * len(s)


def num(x, d=2):
    """A signed number with a real minus sign (Meslo has U+2212)."""
    s = f"{abs(x):.{d}f}"
    return f"−{s}" if x < -0.5 * 10 ** -d else s


def assert_discs_clear(pos, size, gap=6, what=""):
    for a, b in itertools.combinations(pos, 2):
        d = math.dist(pos[a], pos[b])
        assert d >= size + gap, f"{what}: discs {a},{b} are {d:.0f}bp apart (need {size + gap})"


def check_graph_planar(pos, edges, what, r=None):
    x = F.crossings(list(edges), pos)
    assert not x, f"{what}: edge crossings in a planar graph: {x[:3]}"
    bad = F.clearance_bad(list(edges), pos, r=r or F.NODE / 2 + 3)
    assert not bad, f"{what}: an edge passes through a disc it does not end at: {bad[:3]}"


def head(p, q, color="hot", size=F.NODE, gap=3.0, L=16.0, half=8.5, tip_at=None):
    """An arrowhead pointing from p toward q, its tip just outside q's disc (radius size/2)."""
    p, q = np.array(p, float), np.array(q, float)
    d = q - p
    d = d / np.linalg.norm(d)
    tip = q - d * (size / 2 + gap) if tip_at is None else np.array(tip_at, float)
    base = tip - d * L
    n = np.array([-d[1], d[0]])
    a, b = base + n * half, base - n * half
    return (f"\\fill[{color},opacity=0.92] ({tip[0]:.1f},{tip[1]:.1f}) -- "
            f"({a[0]:.1f},{a[1]:.1f}) -- ({b[0]:.1f},{b[1]:.1f}) -- cycle;\n")


def flow(p, q, color="hot", w=11.0, size=F.NODE):
    """A brush stroke from node p to node q with an arrowhead at q (draw before the discs)."""
    return F.brush([p, q], color=color, w=w) + head(p, q, color=color, size=size)


def frame_path(x0, y0, x1, y1, over=16.0):
    """A hand-drawn frame as one open path that starts mid-left, goes round and overshoots its
    start (draw it with F.brush; TikZ's `pencil` decoration fails on some rectangles)."""
    ym = (y0 + y1) / 2
    return [(x0, ym), (x0, y1), (x1, y1), (x1, y0), (x0, y0), (x0, ym + over)]


def place_values(strings, pos, edges, bounds, disc=F.NODE, gap=7, fixed=None):
    """Put each printed number next to its disc, nearest free spot first.

    Boxes are sized from the glyphs (Meslo, 0.6 em per character).  Checked against every
    disc, every edge, every other number and the canvas bounds.
    """
    r = disc / 2
    boxes, out = {}, {}
    fixed = fixed or {}
    for n, (fx, fy) in fixed.items():                      # hand-placed numbers keep their spot
        w = est_w(strings[n]) + 2
        boxes[n] = (fx - w / 2, fy - 15, fx + w / 2, fy + 15)
    order = sorted((n for n in strings if n not in fixed), key=lambda n: -est_w(strings[n]))

    def cand(n):
        w, h = est_w(strings[n]) + 2, 30
        x0, y0 = pos[n]
        res = []
        for ang in range(0, 360, 15):
            c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            for d in np.arange(r, r + 90, 1.0):
                bx, by = x0 + c * d, y0 + s_ * d
                b = (bx - w / 2, by - h / 2, bx + w / 2, by + h / 2)
                if not F.box_hits_disc(b, x0, y0, r=r + gap):
                    res.append((d + (0 if ang % 90 == 0 else 8), b))
                    break
        return sorted(res, key=lambda t: t[0])

    def ok(n, b):
        if not (bounds[0] <= b[0] and b[2] <= bounds[2] and bounds[1] <= b[1] and b[3] <= bounds[3]):
            return False
        if any(F.box_hits_disc(b, *p, r=r + 3) for m, p in pos.items() if m != n):
            return False
        if any(F.boxes_overlap(b, o) for o in boxes.values()):
            return False
        return not any(F.box_hits_segment(b, pos[a], pos[c], pad=3) for a, c in edges)

    def solve(i):
        if i == len(order):
            return True
        n = order[i]
        for d, b in cand(n):
            if ok(n, b):
                boxes[n] = b
                if solve(i + 1):
                    return True
                del boxes[n]
        return False

    if not solve(0):
        raise SystemExit("value labels: no collision-free placement; move a node or widen the canvas")
    return {n: ((b[0] + b[2]) / 2, (b[1] + b[3]) / 2) for n, b in boxes.items()}


# =========================================================================== eigen-inherit / eig-pf
INH_SX, INH_SY = 122, 58
INH_CY = 232
INH_H = 400
# the crop shared by eigen-inherit and eig-pf (bp from the canvas top)
INH_BOX = (20, 396)


def inherit_geometry():
    pos = eig_layout(INH_SX, W_COL / 2, INH_CY, sy=INH_SY)
    check_graph_planar(pos, EDGES, "eigen-inherit")
    assert_discs_clear(pos, F.NODE, gap=10, what="eigen-inherit")
    strings = {n: f"{V1[n]:.2f}" for n in NAMES}
    # A's own value sits directly left of A, in the wedge between the B-A and A-D edges
    wA = est_w(strings["A"]) + 2
    best = None
    for dy in range(0, -31, -2):
        for dx in range(int(F.NODE / 2 + 8 + wA / 2), 140):
            ax, ay = pos["A"][0] - dx, pos["A"][1] + dy
            wb = (ax - wA / 2, ay - 15, ax + wA / 2, ay + 15)
            if any(F.box_hits_segment(wb, pos[a], pos[b], pad=4) for a, b in EDGES):
                continue
            if any(F.box_hits_disc(wb, *p, r=F.NODE / 2 + 5) for m, p in pos.items()):
                continue
            c = math.hypot(dx, dy)
            if best is None or c < best[0]:
                best = (c, ax, ay)
            break
    assert best is not None, "no place for A's value left of A"
    fixed = {"A": (best[1], best[2])}
    at = place_values(strings, pos, EDGES, bounds=(6, 88, W_COL - 6, INH_H - 6), fixed=fixed)
    return pos, strings, at


def fig_eigen_inherit():
    """The score of A is the sum of its neighbours' scores, divided by lambda.

    Frame 0 is the bare graph with A in hot.  Then B, D, F, G arrive one at a time (shaded by
    its score, the value beside it, a brush into A, a running sum underneath), then A's own
    score closes the identity, then the two nodes that are not A's neighbours, then the clean
    picture (= eig-pf).
    """
    pos, strings, at = inherit_geometry()
    nbrs = sorted(S.EIG["A"])
    assert nbrs == ["B", "D", "F", "G"], nbrs
    terms = [strings[m] for m in nbrs]
    assert terms == ["0.64", "0.58", "0.81", "0.85"], terms
    total = sum(float(t) for t in terms)
    lam = f"{LAM1:.2f}"
    assert f"{total:.2f}" == lam == "2.88" and strings["A"] == "1.00", (total, lam)
    assert abs(float(lam) * float(strings["A"]) - total) < 1e-9
    x0 = (W_COL - est_w(" + ".join(terms))) / 2

    def frame(shown=(), a_done=False, flows=(), nsum=0, clean=False):
        # the clean frame keeps the identity "0.64 + ... = 2.88 x 1.00" in ink (A not hot)
        body = edges_body(EDGES, pos)
        for m in flows:
            body += flow(pos[m], pos["A"])
        for n in NAMES:
            if clean:
                fill = F.shade(V1[n])
            elif n == "A":
                fill = "hot"
            elif n in shown:
                fill = F.shade(V1[n])
            else:
                fill = "white"
            body += F.disc(*pos[n], n, fill=fill)
        for n in NAMES:
            visible = clean or n in shown or (n == "A" and a_done)
            if visible:
                body += F.text(*at[n], strings[n], color="ink")
        if nsum:
            body += F.text(x0, 68, " + ".join(terms[:nsum]), anchor="west")
        if a_done:
            body += F.text(x0, 30, f"= {lam} × {strings['A']}", anchor="west")
        return body

    frames = [frame()]
    for k in range(1, 5):
        frames.append(frame(shown=nbrs[:k], flows=nbrs[:k], nsum=k))
    full = dict(shown=nbrs, flows=nbrs, nsum=4)
    frames.append(frame(a_done=True, **full))                       # the identity closes
    frames.append(frame(shown=nbrs + ["E"], flows=nbrs, nsum=4, a_done=True))
    frames.append(frame(shown=nbrs + ["E", "C"], flows=nbrs, nsum=4, a_done=True))
    frames.append(frame(clean=True, nsum=4, a_done=True))            # = eig-pf
    F.emit_frames("eigen-inherit", frames, container="col", h=INH_H, box=INH_BOX)
    return frames[-1]


def fig_eig_pf():
    """The Perron-Frobenius eigenvector, largest entry set to 1: eigenvector centrality.

    The body is exactly the last frame of eigen-inherit (same canvas, same box).
    """
    assert all(v > 0 for v in V1.values()) and abs(max(V1.values()) - 1) < 1e-12
    assert max(V1, key=V1.get) == "A" and V1["B"] > V1["D"] and DEG["B"] < DEG["D"]
    pos, strings, at = inherit_geometry()
    terms = [strings[m] for m in sorted(S.EIG["A"])]
    lam = f"{LAM1:.2f}"
    x0 = (W_COL - est_w(" + ".join(terms))) / 2
    body = edges_body(EDGES, pos)
    for n in NAMES:
        body += F.disc(*pos[n], n, fill=F.shade(V1[n]))
    for n in NAMES:
        body += F.text(*at[n], strings[n], color="ink")
    body += F.text(x0, 68, " + ".join(terms), anchor="west")
    body += F.text(x0, 30, f"= {lam} × {strings['A']}", anchor="west")
    F.emit("eig-pf", body, container="col", h=INH_H, box=INH_BOX)


# =========================================================================== eigen-equation
def fig_eigen_equation():
    """A c = lambda c: A a 7 x 7 box, c a column of seven cells shaded by its entry."""
    n = len(NAMES)
    assert A_MAT.shape == (n, n) and n == 7
    assert np.abs(A_MAT @ U1 - LAM1 * U1).max() < 1e-9, "the drawn vector must be the eigenvector"
    vals = [V1[c] for c in NAMES]

    cell, cw = 28.0, 56.0
    ay0, ay1 = 70.0, 70.0 + n * cell
    ax0 = 49.0
    ax1 = ax0 + n * cell
    c1x = ax1 + 24
    eqx = c1x + cw + 38
    lamx = eqx + 56
    c2x = lamx + 36

    def box(x0, y0, x1, y1, fill=None, w=2.8, seed=0):
        o = ""
        if fill:
            o += f"\\fill[{fill}] ({x0},{y0}) rectangle ({x1},{y1});\n"
        o += F._seed(x0, y0, x1, y1, seed)
        o += f"\\draw[ink,line width={w}bp,pencil,opacity=0.95] ({x0},{y0}) rectangle ({x1},{y1});\n"
        return o

    def column(x):
        o = ""
        for i in range(n):
            y = ay1 - (i + 1) * cell
            o += f"\\fill[{F.shade(vals[i])}] ({x},{y:.2f}) rectangle ({x + cw},{y + cell:.2f});\n"
        for i in range(1, n):
            y = ay1 - i * cell
            o += f"\\draw[ink,line width=1.2bp,opacity=0.35] ({x},{y:.2f}) -- ({x + cw},{y:.2f});\n"
        return o + box(x, ay0, x + cw, ay1, w=2.6, seed=3)

    body = box(ax0, ay0, ax1, ay1, fill="faint", seed=1)
    body += column(c1x) + column(c2x)
    mid = (ay0 + ay1) / 2
    body += F.text((ax0 + ax1) / 2, mid, "A", size=52)
    body += F.text((ax0 + ax1) / 2, ay0 - 30, "7 × 7", color="muted")
    for x in (c1x, c2x):
        body += F.text(x + cw / 2, ay0 - 30, "c", color="hot")
    body += F.text(eqx, mid, "=", size=52)
    body += F.text(lamx, mid, "λ", color="ink", size=52)
    F.emit("eigen-equation", body, container="col", h=300)


# =========================================================================== eig-all
ALL_S = 31
ALL_PITCH = (W_FULL - 16) / 7
ALL_PW, ALL_PH = ALL_PITCH - 6, 138
ALL_DISC = 30


def _rows(labels, gap=10):
    """Give every (x, width) label the first row where it overlaps nothing placed there."""
    rows = []
    out = []
    for x, w in labels:
        r = 0
        while True:
            if r == len(rows):
                rows.append([])
            if all(x + w / 2 + gap <= x0 - w0 / 2 or x - w / 2 - gap >= x0 + w0 / 2 for x0, w0 in rows[r]):
                rows[r].append((x, w))
                out.append(r)
                break
            r += 1
    return out


def fig_eig_all():
    """Seven eigenvectors of the 7-node graph: sign by hue (cool +, hot -), size by saturation.

    eig-all-q is the question (every panel alike); eig-all adds a cool frame around the
    lambda-max panel and "all positive".  One crop for both.
    """
    order = list(range(7))                                  # ascending eigenvalue
    allpos = [k for k in order if np.all(EVECS[:, k] > 1e-9)]
    assert allpos == [6], f"exactly one all-positive eigenvector, the largest: {allpos}"
    for k in order[:-1]:
        v = EVECS[:, k]
        assert v.min() < -1e-9 < 1e-9 < v.max(), f"eigenvector {k} must have both signs"
    assert np.min(np.diff(EVALS)) > 0.12

    y_line = 135
    y_pb = y_line + 98                                      # bottom of every panel
    y_gc = y_pb + ALL_PH / 2                                # graph centre
    lam_lo, lam_hi = float(EVALS[0]), float(EVALS[-1])
    x_lo, x_hi = 72, W_FULL - 76
    X = lambda lam: x_lo + (lam - lam_lo) / (lam_hi - lam_lo) * (x_hi - x_lo)
    cx = [8 + ALL_PITCH * (i + 0.5) for i in order]
    arrow_opt = "-{Latex[length=12bp,width=13bp]}"

    # eigenvalue labels sit below the axis; a label that would collide with its neighbour goes
    # ABOVE its own dot instead (no leader), and its arrow starts above the label
    items = [(X(EVALS[i]), est_w(num(EVALS[i]))) for i in order]
    zero = (X(0.0), est_w("0"))
    rows = _rows(items + [zero])
    assert max(rows) <= 1, "three rows of eigenvalue labels do not fit"
    above = [i for i in order if rows[i] == 1]
    assert above == [3], above                               # -0.43 only
    below = [(items[i]) for i in order if i not in above] + [zero]
    assert max(_rows(below)) == 0, "the remaining labels do not fit on one row"
    lab_x = {i: X(EVALS[i]) + (14 if i in above else 0) for i in order}
    arrow_from = {i: (X(EVALS[i]), y_line + 10) if i not in above else (lab_x[i], y_line + 52)
                  for i in order}
    arrow_to = {i: (cx[i], y_pb - 5) for i in order}
    for i in above:                                         # the neighbour's arrow stays vertical
        arrow_to[i - 1] = (X(EVALS[i - 1]) + 6, y_pb - 5)

    body = F.seg((36, y_line), (W_FULL - 36, y_line), color="muted", w=2.4)
    for i in order:
        (fx, fy), (tx, ty) = arrow_from[i], arrow_to[i]
        body += f"\\draw[muted,line width=2.2bp,{arrow_opt}] ({fx:.1f},{fy:.1f}) -- ({tx:.1f},{ty:.1f});\n"
    row_y = y_line - 38
    for i in order:
        body += F.dot(X(EVALS[i]), y_line, color="ink", d=13)
        body += F.text(lab_x[i], y_line + 32 if i in above else row_y, num(EVALS[i]))
    body += F.seg((X(0), y_line - 7), (X(0), y_line + 7), color="muted", w=2.4)
    body += F.text(X(0), row_y, "0", color="muted")
    # the above-label must clear the two neighbouring arrows and the zero tick
    for i in above:
        w = est_w(num(EVALS[i])) / 2
        assert lab_x[i] - w > arrow_to[i - 1][0] + 4 and lab_x[i] + w < X(0) + 40

    # the seven panels
    base = eig_layout(ALL_S, 0, 0)
    pos0 = {k: (v[0], v[1]) for k, v in base.items()}
    assert_discs_clear(pos0, ALL_DISC + 4, what="eig-all")
    bad = F.clearance_bad(EDGES, pos0, r=ALL_DISC / 2 + 4)
    assert not bad, f"eig-all: edge through a disc {bad}"
    assert not F.crossings(EDGES, pos0)
    gw = GW * ALL_S + ALL_DISC + 2
    assert gw <= ALL_PW - 8, f"graph is {gw:.0f}bp wide in a {ALL_PW:.0f}bp panel"
    for i in order:
        x0, x1 = cx[i] - ALL_PW / 2, cx[i] + ALL_PW / 2
        body += F.brush(frame_path(x0, y_pb, x1, y_pb + ALL_PH), color="muted", w=3.0,
                        opacity=0.8, strands=3, seed=i)
        v = EVECS[:, i]
        strength = np.abs(v) / np.abs(v).max()
        pos = {k: (cx[i] + p[0], y_gc + p[1]) for k, p in pos0.items()}
        body += edges_body(EDGES, pos, w=2.0)
        for j, c in enumerate(NAMES):
            body += F.disc(*pos[c], "", fill=F.shade(strength[j], hi="cool" if v[j] > 0 else "hot"),
                           size=ALL_DISC)
    body_q = body

    # the answer: the lambda-max panel is framed, its arrow and dot are cool, and it says so
    k = 6
    x0, x1 = cx[k] - ALL_PW / 2 - 4, cx[k] + ALL_PW / 2 + 4
    y0, y1 = y_pb - 4, y_pb + ALL_PH + 4
    hl = F.brush(frame_path(x0, y0, x1, y1), color="cool", w=7.0, opacity=0.95, strands=5, seed=k)
    hl += (f"\\draw[cool,line width=3.6bp,{arrow_opt}] ({X(EVALS[k]):.1f},{y_line + 10}) -- "
           f"({cx[k]:.1f},{y_pb - 5});\n")
    hl += F.dot(X(EVALS[k]), y_line, color="cool", d=17)
    hl += F.text(W_FULL - 10, y1 + 26, "all positive", color="cool", anchor="east")
    F.emit_group([("eig-all-q", body_q), ("eig-all", body_q + hl)], container="full", h=480, hmod="tall")


# =========================================================================== the ring of cliques
RING_DISC = 28
RING_R = 76                                                # every clique sits on a circle of this radius
RING_RX, RING_RY = 172, 104
RING_OX, RING_OY = 252, 200
RING_H = 400
RING_BOX = (22, 378)                                       # bp from the canvas top, one crop


def ring_layout(sizes, Rx, Ry, radius):
    """Positions for clique_ring(sizes): four cliques on an ellipse, counter-clockwise from the top.

    Node 0 of a clique (the port that takes the ring edge from the previous clique) and node 1
    (the port that sends it to the next) sit at FIXED positions, 90 degrees apart on the clique's
    circle and facing the two neighbours.  A 4-clique is the square through the two ports.
    Node j >= 2 is spread evenly over the remaining 270 degrees of the circle, so growing a
    clique adds one node to the far side and moves nothing else but the spacing of the far arc.
    """
    k = len(sizes)
    cen = [(Rx * math.cos(math.radians(90 + 90 * i)), Ry * math.sin(math.radians(90 + 90 * i)))
           for i in range(k)]
    pos, off = {}, 0
    for i, K in enumerate(sizes):
        c = np.array(cen[i])
        dp = np.array(cen[(i - 1) % k]) - c
        dn = np.array(cen[(i + 1) % k]) - c
        dp, dn = dp / np.linalg.norm(dp), dn / np.linalg.norm(dn)
        beta = math.atan2(*(dp + dn)[::-1])
        sgn = 1 if (dn[0] * dp[1] - dn[1] * dp[0]) > 0 else -1
        r = radius(i, K)
        ang = {0: beta + sgn * math.pi / 4, 1: beta - sgn * math.pi / 4}
        step = 1.5 * math.pi / (K - 1)
        for j in range(2, K):
            ang[j] = ang[1] - sgn * (j - 1) * step
        for j in range(K):
            pos[off + j] = (float(c[0] + r * math.cos(ang[j])), float(c[1] + r * math.sin(ang[j])))
        off += K
    return pos


def ring_vec(sizes):
    G = S.clique_ring(sizes)
    A = nx.to_numpy_array(G, nodelist=sorted(G))
    w, V = np.linalg.eigh(A)
    v = np.abs(V[:, -1])
    return G, v / v.max()


def ring_pos(sizes):
    pl = ring_layout(sizes, RING_RX, RING_RY, lambda i, K: RING_R)
    return {n: (RING_OX + p[0], RING_OY + p[1]) for n, p in pl.items()}


def ring_body(sizes, shaded):
    """The ring: white discs (the question) or discs shaded by the eigenvector (the answer)."""
    G, v = ring_vec(sizes)
    pos = ring_pos(sizes)
    assert_discs_clear(pos, RING_DISC, gap=8, what=f"ring {sizes}")
    edges = list(G.edges())
    bad = F.clearance_bad(edges, pos, r=RING_DISC / 2 + 2)
    assert not bad, f"ring {sizes}: an edge passes through a disc {bad[:3]}"
    # the only crossings allowed are the two diagonals inside one clique
    cl = {n: next(i for i, (lo, hi) in enumerate(_spans(sizes)) if lo <= n < hi) for n in G}
    x = [(e, f) for e, f in F.crossings(edges, pos) if not (cl[e[0]] == cl[e[1]] == cl[f[0]] == cl[f[1]])]
    assert not x, f"ring {sizes}: crossings outside a clique {x[:3]}"
    body = edges_body(edges, pos, w=2.2)
    for n in sorted(G):
        body += F.disc(*pos[n], "", fill=F.shade(v[n]) if shaded else "white", size=RING_DISC)
    return body, pos, v


def _spans(sizes):
    out, off = [], 0
    for s_ in sizes:
        out.append((off, off + s_))
        off += s_
    return out


def fig_ring_4444():
    sizes = (4, 4, 4, 4)
    body, pos, v = ring_body(sizes, shaded=False)           # the question must not show the score
    for k in range(4):                                       # the four cliques carry equal score
        assert abs(sum(v[4 * k:4 * k + 4]) / sum(v) - 0.25) < 1e-9
    F.emit("ring-4444", body, container="col", h=RING_H, box=RING_BOX)


def fig_ring_local():
    """Frame 0 = ring-4444.  Then the last clique grows one node at a time (a square, pentagon,
    hexagon, heptagon, octagon around a fixed centre, the two ports fixed), discs shaded by the
    leading eigenvector, with the share of the score that sits in the last clique.  The share is
    in ink at K = 4 (the baseline) and hot from K = 5."""
    shares = {}
    frames = [ring_body((4, 4, 4, 4), shaded=False)[0]]
    cx, cy = RING_OX, RING_OY
    for K in (4, 5, 6, 7, 8):
        sizes = S.RING_SIZES[K]
        share, lam = S.eig_share(sizes)
        shares[K] = F.pct(share)
        body, pos, v = ring_body(sizes, shaded=True)
        l1 = f"K = {K}: {shares[K]}"
        w1 = est_w(l1.replace("\\", "")) + 6
        w2 = est_w("of the score") + 6
        for box in ((cx - w1 / 2, cy + 1, cx + w1 / 2, cy + 31), (cx - w2 / 2, cy - 29, cx + w2 / 2, cy - 3)):
            assert not any(F.box_hits_disc(box, *p, r=RING_DISC / 2 + 4) for p in pos.values()), \
                f"ring-local K={K}: the share label touches a disc"
            assert not any(F.box_hits_segment(box, pos[a], pos[b], pad=2)
                           for a, b in S.clique_ring(sizes).edges()), f"ring-local K={K}: label on an edge"
        pc = shares[K] if K == 4 else f"\\textcolor{{hot}}{{{shares[K]}}}"
        body += F.text(cx, cy + 16, f"K = {K}: {pc}")
        body += F.text(cx, cy - 16, "of the score", color="muted")
        frames.append(body)
    assert [shares[K] for K in (4, 5, 6, 7, 8)] == ["25\\%", "68\\%", "85\\%", "91\\%", "94\\%"], shares
    F.emit_frames("ring-local", frames, container="col", h=RING_H, box=RING_BOX)


# =========================================================================== katz-floor
# katz-floor uses the EIG layout of eigen-inherit / eig-pf, so the room recognises the network


def fig_katz_floor():
    """Every node gets a baseline beta; the focal node A also gets alpha from each neighbour."""
    pos = inherit_geometry()[0]
    check_graph_planar(pos, EDGES, "katz-floor")
    focus = "A"
    nb = sorted(S.EIG[focus])
    body = edges_body(EDGES, pos)
    for m in nb:
        body += flow(pos[m], pos[focus], color="hot", w=10)
    for n in NAMES:
        body += F.disc(*pos[n], "β", fill="hot" if n == focus else "white")
    # an alpha beside each arrow, on the side that has nothing else
    for m in nb:
        a, b = np.array(pos[m]), np.array(pos[focus])
        mid, d = (a + b) / 2, (b - a) / np.linalg.norm(b - a)
        nrm = np.array([-d[1], d[0]])
        best = None
        for sgn in (1, -1):
            p = mid + sgn * 26 * nrm
            box = (p[0] - 13, p[1] - 17, p[0] + 13, p[1] + 17)
            if any(F.box_hits_disc(box, *q, r=F.NODE / 2) for q in pos.values()):
                continue
            if any(F.box_hits_segment(box, pos[x], pos[y], pad=2) for x, y in EDGES):
                continue
            best = p
            break
        assert best is not None, f"katz-floor: no clear place for the alpha on {m}->{focus}"
        body += F.text(best[0], best[1], "α", color="hot")
    F.emit("katz-floor", body, container="col", h=INH_H)


# =========================================================================== walks-discount
def walks_from(G, u, k):
    """Every walk of length k from u, by depth-first search (a walk may revisit nodes and edges)."""
    out = [(u,)]
    for _ in range(k):
        out = [w + (v,) for w in out for v in sorted(G[w[-1]])]
    return out


WD_COLS = {2: "gold", 3: "cool"}


def _bow(p, q, off):
    """A quadratic curve from p to q bowed sideways by `off` bp (negative: the other side)."""
    p, q = np.array(p, float), np.array(q, float)
    d = (q - p) / np.linalg.norm(q - p)
    n = np.array([-d[1], d[0]])
    c = (p + q) / 2 + n * 2 * off
    return [tuple((1 - t) ** 2 * p + 2 * t * (1 - t) * c + t ** 2 * q) for t in np.linspace(0, 1, 14)], c


def fig_walks_discount():
    """Walks from u to v in W5 (the pair of slide 8), drawn in w5-blank's layout: none of length
    1, two of length 2 (gold), one of length 3 (cool).  Each legend entry (arrows = alpha^k)
    appears with the first walk of that length."""
    import figs_defs as D                                   # only for W5's coordinates and crop
    G, u, v = S.W5, "u", "v"
    counts = S.walk_counts(G, S.W5_ORDER, u, v, kmax=4)           # [0, 2, 1, 11]
    ends = {k: [w for w in walks_from(G, u, k) if w[-1] == v] for k in (1, 2, 3, 4)}
    assert [len(ends[k]) for k in (1, 2, 3, 4)] == counts == [0, 2, 1, 11], counts
    assert sorted(ends[2]) == [("u", "n2", "v"), ("u", "n3", "v")]
    assert ends[3] == [("u", "n0", "n2", "v")]
    for k in (2, 3):
        for w in ends[k]:
            assert w[0] == u and w[-1] == v and len(w) == k + 1
            assert all(G.has_edge(a, b) for a, b in zip(w, w[1:])), f"{w} is not a walk in W5"
    drawn = [(2, ends[2][0]), (2, ends[2][1]), (3, ends[3][0])]
    P = dict(D.W5_POS)
    check_graph_planar(P, list(G.edges()), "walks-discount")
    # the one edge two drawn walks share (n2-v) is bowed for the longer walk
    shared = {frozenset(p) for w in ends[2] for p in zip(w, w[1:])} & \
             {frozenset(p) for p in zip(ends[3][0], ends[3][0][1:])}
    assert shared == {frozenset(("n2", "v"))}, shared

    sup = {2: "²", 3: "³", 4: "⁴"}
    sum_line = " + ".join((str(c) if c > 1 else "") + "α" + sup[k + 1]
                          for k, c in enumerate(counts) if c) + " + ⋯"
    assert sum_line == "2α² + α³ + 11α⁴ + ⋯", sum_line
    seg_len = 26
    lx = 236
    rows = {2: 206, 3: 162}                                       # legend rows, inside the graph

    def hop_routes(k, w):
        """The brush points and arrowheads of one walk, hop by hop."""
        out = ""
        for a, b in zip(w, w[1:]):
            if k == 3 and (a, b) == ("n2", "v"):
                pts, c = _bow(P[a], P[b], -20)
                out += F.brush(pts, color=WD_COLS[k], w=11)
                out += head(c, P[b], color=WD_COLS[k])
            else:
                out += F.brush([P[a], P[b]], color=WD_COLS[k], w=11)
                out += head(P[a], P[b], color=WD_COLS[k])
        return out

    def legend(k):
        ly, o = rows[k], ""
        for j in range(k):
            a, b = (lx + j * seg_len, ly), (lx + (j + 1) * seg_len - 8, ly)
            o += F.brush([a, b], color=WD_COLS[k], w=9)
            o += head(a, b, color=WD_COLS[k], tip_at=(b[0] + 5, ly), L=12, half=6.5)
        return o + F.text(lx + k * seg_len + 4, ly, f"= \u03b1{sup[k]}", color="muted", anchor="west")

    def frame(n_drawn, total=False):
        body = edges_body(list(G.edges()), P)
        for k, w in drawn[:n_drawn]:
            body += hop_routes(k, w)
        for n in S.W5_ORDER:
            body += F.disc(*P[n], {"u": "u", "v": "v"}.get(n, ""), fill="white")
        for k in (2, 3):
            if any(kk == k for kk, _ in drawn[:n_drawn]):
                body += legend(k)
        if total:
            body += F.text(P["v"][0], 28, sum_line)
        return body

    assert est_w(sum_line) < W_COL - 20
    frames = [frame(0), frame(1), frame(2), frame(3), frame(3, True)]
    assert frames[0] == D._w5_scene()                              # frame 0 = w5-blank's body
    F.emit_frames("walks-discount", frames, container="col", h=D.W5_H, box=D.W5_BOX)


FIGURES = [
    ("eigen-inherit", fig_eigen_inherit),
    ("eig-pf", fig_eig_pf),
    ("eigen-equation", fig_eigen_equation),
    ("eig-all", fig_eig_all),
    ("ring-4444", fig_ring_4444),
    ("ring-local", fig_ring_local),
    ("katz-floor", fig_katz_floor),
    ("walks-discount", fig_walks_discount),
]
