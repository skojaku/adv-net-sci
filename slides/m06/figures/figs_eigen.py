#!/usr/bin/env python3
"""Module 06, eigenvectors, power iteration, localization and Katz: the figures of `figs_eigen`.

    cd slides/m06/figures && python3 -c "import figlib, figs_eigen as m; figlib.run(m.FIGURES)"

Every number printed here is computed from `smallgraphs` (the 7-node graph `EIG`, the clique
ring, `W5`); nothing is typed.  Colour language (DECK_SPEC "Visual language"):

* a score is a sequential ramp `accent!10` -> `accent` (value / largest value),
* a sign is blue (positive) or gold (negative) and its strength is the shade,
* accent-2 red marks the one thing the slide is about.

Discs that carry a score get a thin black outline: a near-white disc would otherwise read
as a hole in the drawing.
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
UNIT1 = dict(zip(NAMES, U1))                              # unit length (the u_1 of the decomposition)

_xs = [p[0] for p in S.EIG_XY.values()]
_ys = [p[1] for p in S.EIG_XY.values()]
GX, GY = (min(_xs) + max(_xs)) / 2, (min(_ys) + max(_ys)) / 2
GW, GH = max(_xs) - min(_xs), max(_ys) - min(_ys)       # 3.3 x 2.9 grid units


def eig_layout(sx, cx, cy, sy=None):
    """The 7-node layout scaled by sx (and sy) around the point (cx, cy), y up."""
    sy = sy or sx
    return {k: (cx + sx * (x - GX), cy + sy * (y - GY)) for k, (x, y) in S.EIG_XY.items()}


# --------------------------------------------------------------------------- drawing helpers
def ramp(v):
    """Percent of accent for a score fraction v in [0, 1]: accent!10 ... accent."""
    return int(round(10 + 90 * max(0.0, min(1.0, float(v)))))


def ink_on(p):
    """Letter colour on accent!p: white only where it beats black (p >= 85)."""
    return "white" if p >= 85 else "black"


def nd(x, y, label="", fill="accent", size=F.NODE, name=None, outline=True, txt=None, ow=1.8):
    """A disc.  `minimum size` is the diameter; the outline adds half its width outside."""
    nm = f"({name})" if name else ""
    opt = ["disc", f"fill={fill}", f"minimum size={size}bp"]
    if outline:
        opt += ["draw=black", f"line width={ow}bp"]
    if txt:
        opt.append(f"text={txt}")
    return f"\\node[{','.join(opt)}] {nm} at ({x:.2f},{y:.2f}) {{{label}}};\n"


def edges_body(edges, pos, w=F.EDGE_W, color="black"):
    return "".join(F.seg(pos[a], pos[b], color=color, w=w) for a, b in edges)


def arrow(a, b, color="accenttwo", w=5.0, head=(15, 18)):
    """An arrow between two named nodes: it starts and stops at the disc borders."""
    return (f"\\draw[line width={w:.1f}bp,draw={color},"
            f"-{{Latex[length={head[0]}bp,width={head[1]}bp]}}] ({a}) -- ({b});\n")


def score_graph(pos, vals, letters=True, size=F.NODE, ew=F.EDGE_W):
    """The 7-node graph with every disc shaded by vals[node] (a fraction of the largest)."""
    body = edges_body(EDGES, pos, w=ew)
    for n in NAMES:
        p = ramp(vals[n])
        body += nd(*pos[n], label=n if letters else "", fill=f"accent!{p}", size=size,
                   name=n, txt=ink_on(p))
    return body


def tex_num(x, d=2):
    s = f"{abs(x):.{d}f}"
    return f"$-{s}$" if x < -0.5 * 10 ** -d else s


def est_w(s, size=FONT):
    """A generous width in bp for a printed number (digits 0.5 em, point 0.28 em, minus 0.78 em)."""
    em = 0.0
    for ch in s.replace("$", ""):
        em += {"-": 0.78, ".": 0.28}.get(ch, 0.5)
    return em * size


def assert_discs_clear(pos, size, gap=6, what=""):
    for a, b in itertools.combinations(pos, 2):
        d = math.dist(pos[a], pos[b])
        assert d >= size + gap, f"{what}: discs {a},{b} are {d:.0f}bp apart (need {size + gap})"


def check_graph_planar(pos, edges, what, r=None):
    x = F.crossings(list(edges), pos)
    assert not x, f"{what}: edge crossings in a planar graph: {x[:3]}"
    bad = F.clearance_bad(list(edges), pos, r=r or F.NODE / 2 + 3)
    assert not bad, f"{what}: an edge passes through a disc it does not end at: {bad[:3]}"


# =========================================================================== eigen-inherit
INH_SX, INH_SY = 118, 100
INH_H = 400


def fig_eigen_inherit():
    """Node A's score is the sum of its neighbours' scores, then the same for B."""
    pos = eig_layout(INH_SX, W_COL / 2, 205, sy=INH_SY)
    check_graph_planar(pos, EDGES, "eigen-inherit")
    nbrs = {n: sorted(S.EIG[n]) for n in NAMES}
    assert nbrs["A"] == ["B", "D", "F", "G"] and nbrs["B"] == ["A", "G"], nbrs

    def frame(focus=None, into=(), shaded=False):
        if shaded:
            body = score_graph(pos, V1, size=F.NODE)
        else:
            body = edges_body(EDGES, pos)
            for n in NAMES:
                body += nd(*pos[n], label=n, name=n, outline=False)
        if focus:
            for m in into:
                assert S.EIG.has_edge(m, focus)
                body += arrow(m, focus)
            body += F.mark(*pos[focus], size=F.NODE)
        return body

    frames = [frame("A", nbrs["A"]),                      # first frame: the claim
              frame()]
    frames += [frame("A", nbrs["A"][:k]) for k in range(1, 5)]
    frames += [frame("B", nbrs["B"][:k]) for k in range(1, 3)]
    frames += [frame(shaded=True)]                         # last frame: the eigenvector shading
    F.emit_gif("eigen-inherit", frames, container="col", h=INH_H,
               durations=[1200, 700] + [800] * 4 + [800, 1100] + [1400], hold=4)


# =========================================================================== eigen-equation
def fig_eigen_equation():
    """A c = lambda c on the 7-node graph: A a 7 x 7 block, c a shaded column of seven cells."""
    n = len(NAMES)
    assert A_MAT.shape == (n, n) and n == 7
    assert np.abs(A_MAT @ U1 - LAM1 * U1).max() < 1e-9, "the drawn vector must be the eigenvector"
    lam = f"{LAM1:.2f}"
    assert lam == "2.88", lam
    vals = [V1[c] for c in NAMES]

    ox = 255                                  # shifts the whole composition to the page centre
    bx0, bx1, by0, by1 = ox, ox + 190, 70, 260
    body = (f"\\fill[accent!14] ({bx0},{by0}) rectangle ({bx1},{by1});\n"
            f"\\draw[line width=3bp,draw=black] ({bx0},{by0}) rectangle ({bx1},{by1});\n")

    def column(x, w=34.0):
        out, cell = "", (by1 - by0) / n
        for i in range(n):
            y = by0 + (n - 1 - i) * cell
            out += (f"\\fill[accent!{ramp(vals[i])}] ({x},{y:.2f}) rectangle ({x + w},{y + cell:.2f});\n")
        out += (f"\\draw[line width=2.4bp,draw=black] ({x},{by0}) rectangle "
                f"({x + w},{by1});\n")
        return out

    mid = (by0 + by1) / 2
    cx1, cx2 = bx1 + 60, bx1 + 60 + 34 + 240
    body += column(cx1) + column(cx2)
    body += F.text((bx0 + bx1) / 2, mid + 24, "$A$", size=46)
    body += F.text((bx0 + bx1) / 2, mid - 34, f"${n} \\times {n}$")
    body += F.text((cx1 + 34 + cx2) / 2 - 62, mid, "$=$", size=46)
    body += F.text((cx1 + 34 + cx2) / 2 + 40, mid, "$\\lambda$", color="accenttwo", size=46)
    body += F.text(W_FULL / 2, 330, "$A\\,\\mathbf{c} = \\lambda\\,\\mathbf{c}$", size=46)
    body += F.text(W_FULL / 2, 22,
                   f"$\\lambda = {lam}$: the same seven numbers, each {lam} times bigger",
                   color="accenttwo")
    F.emit("eigen-equation", body, container="full", h=400, hmod="")


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
    """Seven eigenvectors of the 7-node graph, nodes coloured by sign and strength."""
    order = list(range(7))                                  # ascending eigenvalue
    allpos = [k for k in order if np.all(EVECS[:, k] > 1e-9)]
    assert allpos == [6], f"exactly one all-positive eigenvector, the largest: {allpos}"
    for k in order[:-1]:
        v = EVECS[:, k]
        assert v.min() < -1e-9 < 1e-9 < v.max(), f"eigenvector {k} must have both signs"
    assert np.min(np.diff(EVALS)) > 0.12

    # vertical layout (y up): value labels, number line, arrows, copies, "all positive"
    y_line = 135
    y_pb = y_line + 88                                      # bottom of every copy's panel
    y_gc = y_pb + ALL_PH / 2                                # graph centre
    lam_lo, lam_hi = float(EVALS[0]), float(EVALS[-1])
    x_lo, x_hi = 72, W_FULL - 76
    X = lambda lam: x_lo + (lam - lam_lo) / (lam_hi - lam_lo) * (x_hi - x_lo)

    body = F.seg((36, y_line), (W_FULL - 36, y_line), color="annot", w=2.4)
    cx = [8 + ALL_PITCH * (i + 0.5) for i in order]
    # dots and arrows
    for i in order:
        hot = i == 6
        col = "accenttwo" if hot else "annot"
        body += (f"\\draw[line width={3.4 if hot else 2.2}bp,draw={col},"
                 f"-{{Latex[length=13bp,width=14bp]}}] ({X(EVALS[i]):.1f},{y_line + 9}) -- "
                 f"({cx[i]:.1f},{y_pb - 5});\n")
    # value labels: two rows where the dots are too close for one
    items = [(X(EVALS[i]), est_w(tex_num(EVALS[i]))) for i in order]
    zero = (X(0.0), est_w("0"))
    rows = _rows(items + [zero])
    row_y = {0: y_line - 38, 1: y_line - 38 - 46}
    assert max(rows) <= 1, "three rows of eigenvalue labels do not fit"
    for i in order:
        hot = i == 6
        body += F.dot(X(EVALS[i]), y_line, color="accenttwo" if hot else "black", d=14 if hot else 12)
        body += F.text(X(EVALS[i]), row_y[rows[i]], tex_num(EVALS[i]),
                       color="accenttwo" if hot else "black")
        if rows[i] == 1:                                    # a short leader to the second row
            body += F.seg((X(EVALS[i]), y_line - 9), (X(EVALS[i]), row_y[1] + 25), color="annot", w=1.6)
    body += F.seg((X(0), y_line - 7), (X(0), y_line + 7), color="annot", w=2.4)
    body += F.text(X(0), row_y[rows[-1]], "0", color="annot")
    if rows[-1] == 1:
        body += F.seg((X(0), y_line - 7), (X(0), row_y[1] + 25), color="annot", w=1.6)

    # the seven copies
    base = eig_layout(ALL_S, 0, 0)
    pos0 = {k: (v[0], v[1]) for k, v in base.items()}
    assert_discs_clear({k: (v[0], v[1]) for k, v in pos0.items()}, ALL_DISC + 4, what="eig-all")
    bad = F.clearance_bad(EDGES, pos0, r=ALL_DISC / 2 + 4)
    assert not bad, f"eig-all: edge through a disc {bad}"
    assert not F.crossings(EDGES, pos0)
    gw = GW * ALL_S + ALL_DISC + 2
    assert gw <= ALL_PW - 8, f"graph is {gw:.0f}bp wide in a {ALL_PW:.0f}bp panel"
    for i in order:
        hot = i == 6
        x0, x1 = cx[i] - ALL_PW / 2, cx[i] + ALL_PW / 2
        if hot:
            body += (f"\\draw[line width=4.5bp,draw=accenttwo,rounded corners=6bp] "
                     f"({x0:.1f},{y_pb}) rectangle ({x1:.1f},{y_pb + ALL_PH});\n")
        else:
            body += (f"\\draw[line width=1.6bp,draw=annot!45,rounded corners=6bp] "
                     f"({x0:.1f},{y_pb}) rectangle ({x1:.1f},{y_pb + ALL_PH});\n")
        v = EVECS[:, i]
        strength = np.abs(v) / np.abs(v).max()
        pos = {k: (cx[i] + p[0], y_gc + p[1]) for k, p in pos0.items()}
        body += edges_body(EDGES, pos, w=2.0)
        for j, c in enumerate(NAMES):
            p = ramp(strength[j])
            col = "accent" if v[j] > 0 else "accentthree"
            body += nd(*pos[c], fill=f"{col}!{p}", size=ALL_DISC, outline=True, ow=1.6)
    body += F.text(W_FULL - 10, y_pb + ALL_PH + 26, "all positive", color="accenttwo", anchor="east")
    F.emit("eig-all", body, container="full", h=480, hmod="tall")


# =========================================================================== value graphs
def place_values(strings, pos, edges, bounds, disc=F.NODE, gap=7):
    """Put each printed number next to its disc, nearest free spot first.

    Boxes are sized from the glyphs (digits 0.5 em) rather than from `label_box`, which
    models a four-character number as 91 bp and leaves no room on a seven-node graph.
    Checked against every disc, every edge, every other number and the canvas.
    """
    r = disc / 2
    boxes, out = {}, {}
    order = sorted(strings, key=lambda n: -est_w(strings[n]))

    def cand(n):
        w, h = est_w(strings[n]) + 4, 30
        x0, y0 = pos[n]
        res = []
        for ang in range(0, 360, 15):
            c, s_ = math.cos(math.radians(ang)), math.sin(math.radians(ang))
            for d in np.arange(r, r + 90, 1.0):
                bx, by = x0 + c * d, y0 + s_ * d
                b = (bx - w / 2, by - h / 2, bx + w / 2, by + h / 2)
                if not F.box_hits_disc(b, x0, y0, r=r + gap):
                    res.append((d, b))
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


def value_graph(name, vals, strings, sx, sy, letters=True, h=400):
    """The 7-node graph, discs shaded by `vals` (fractions of the largest), `strings` printed."""
    pos = eig_layout(sx, W_COL / 2, h / 2, sy=sy)
    check_graph_planar(pos, EDGES, name)
    at = place_values(strings, pos, EDGES, bounds=(6, 6, W_COL - 6, h - 6))
    body = score_graph(pos, vals, letters=letters)
    for n in NAMES:
        body += F.text(at[n][0], at[n][1], strings[n])
    return body, pos


def fig_eig_pf():
    """The Perron-Frobenius eigenvector: every entry positive, every entry printed (unit length)."""
    assert all(v > 0 for v in UNIT1.values())
    assert abs(sum(v * v for v in UNIT1.values()) - 1) < 1e-9
    strings = {n: f"{UNIT1[n]:.2f}" for n in NAMES}
    body, _ = value_graph("eig-pf", V1, strings, 114, 78)
    F.emit("eig-pf", body, container="col", h=400)


def fig_eig_centrality():
    """Eigenvector centrality of the 7-node graph: the largest entry is 1."""
    assert max(V1, key=V1.get) == "A" and abs(V1["A"] - 1) < 1e-12
    assert V1["B"] > V1["D"] and DEG["B"] < DEG["D"]
    strings = {n: f"{V1[n]:.2f}" for n in NAMES}
    body, _ = value_graph("eig-centrality", V1, strings, 114, 78)
    F.emit("eig-centrality", body, container="col", h=400)


def fig_power_step1():
    """Step one of the power iteration is the degree: A times the all-ones vector."""
    ones = A_MAT @ np.ones(len(NAMES))
    assert all(ones[i] == DEG[c] for i, c in enumerate(NAMES))
    dmax = max(DEG.values())
    vals = {c: DEG[c] / dmax for c in NAMES}
    strings = {c: str(DEG[c]) for c in NAMES}
    body, _ = value_graph("power-step1", vals, strings, 112, 90)
    F.emit("power-step1", body, container="col", h=400)


# =========================================================================== the ring of cliques
RING_DISC = 30
RING_R = {4: 42, 5: 47, 6: 53, 7: 59, 8: 65}              # radius of the last clique by size


def ring_layout(sizes, Rx, Ry, radius):
    """Positions for clique_ring(sizes): four cliques on an ellipse, counter-clockwise from the top.

    Node 0 of a clique faces the previous clique and node 1 the next one, so the two ring
    edges leave on the sides that point at the neighbours.  A 4-clique is a triangle with
    its fourth node in the middle (planar); larger cliques are regular polygons.
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
        ang = {}
        if K == 4:
            ang = {0: beta + sgn * math.pi / 3, 1: beta - sgn * math.pi / 3, 2: beta + math.pi}
            pts = {j: c + r * np.array([math.cos(a), math.sin(a)]) for j, a in ang.items()}
            pts[3] = c.copy()
        else:
            ang[0] = beta + sgn * math.pi / K
            ang[1] = beta - sgn * math.pi / K
            for j in range(2, K):
                ang[j] = beta - sgn * (math.pi / K + (j - 1) * 2 * math.pi / K)
            pts = {j: c + r * np.array([math.cos(a), math.sin(a)]) for j, a in ang.items()}
        for j in range(K):
            pos[off + j] = (float(pts[j][0]), float(pts[j][1]))
        off += K
    return pos


def ring_vec(sizes):
    G = S.clique_ring(sizes)
    A = nx.to_numpy_array(G, nodelist=sorted(G))
    w, V = np.linalg.eigh(A)
    v = np.abs(V[:, -1])
    return G, v / v.max()


def ring_body(sizes, Rx, Ry, ox, oy, radius):
    G, v = ring_vec(sizes)
    pl = ring_layout(sizes, Rx, Ry, radius)
    pos = {n: (ox + p[0], oy + p[1]) for n, p in pl.items()}
    assert_discs_clear(pos, RING_DISC, gap=8, what=f"ring {sizes}")
    edges = list(G.edges())
    if all(s == 4 for s in sizes):
        check_graph_planar(pos, edges, f"ring {sizes}", r=RING_DISC / 2 + 4)
    else:
        bad = F.clearance_bad(edges, pos, r=RING_DISC / 2 + 2)
        assert not bad, f"ring {sizes}: an edge passes through a disc {bad[:3]}"
    body = edges_body(edges, pos, w=2.2)
    for n in sorted(G):
        body += nd(*pos[n], fill=f"accent!{ramp(v[n])}", size=RING_DISC, outline=True, ow=1.8)
    return body, pos, v


def fig_ring_4444():
    sizes = (4, 4, 4, 4)
    body, pos, v = ring_body(sizes, 190, 105, W_COL / 2, 200, lambda i, K: RING_R[4])
    for k in range(4):                         # the four cliques carry equal mass: 25% each
        assert abs(sum(v[4 * k:4 * k + 4] ** 2) / sum(v ** 2) - 0.25) < 1e-9
    F.emit("ring-4444", body, container="col", h=400)


def fig_ring_local():
    shares = []
    frames = []
    for K in (4, 5, 6, 7, 8):
        sizes = S.RING_SIZES[K]
        share, lam = S.eig_share(sizes)
        shares.append(share)
        body, pos, v = ring_body(sizes, 395, 105, W_FULL / 2, 200,
                                 lambda i, KK, K=K: RING_R[KK] if i == 3 else RING_R[4])
        txt = (f"$K={K}$: \\textcolor{{accenttwo}}{{{F.pct(share)}}} in the last clique")
        body += F.text(W_FULL / 2, 200, txt)
        # the text box must clear every disc
        w = est_w(f"K={K}: {F.pct(share)} in the last clique", FONT) * 0.80
        box = (W_FULL / 2 - w / 2, 200 - 24, W_FULL / 2 + w / 2, 200 + 24)
        assert not any(F.box_hits_disc(box, *p, r=RING_DISC / 2) for p in pos.values()), \
            f"ring-local K={K}: the share text touches a disc"
        frames.append(body)
    got = [F.pct(s) for s in shares]
    assert got == ["25\\%", "89\\%", "97\\%", "99\\%", "99\\%"], got
    # first frame = the claim (K = 8), then the growth 4 -> 8; the last frame is K = 8, held
    F.emit_gif("ring-local", [frames[-1]] + frames, container="full", h=400,
               durations=[1000, 1100, 900, 900, 900, 1500], hold=4)


# =========================================================================== katz-floor
def fig_katz_floor():
    """Every node gets a baseline beta; the focal node also gets alpha from each neighbour."""
    pos = eig_layout(INH_SX, W_COL / 2, 205, sy=INH_SY)
    check_graph_planar(pos, EDGES, "katz-floor")
    focus = "A"
    nb = sorted(S.EIG[focus])
    body = edges_body(EDGES, pos)
    for n in NAMES:
        body += nd(*pos[n], label="$\\beta$", name=n, outline=False)
    for m in nb:
        body += arrow(m, focus)
    # an alpha beside each arrow, on the side that has nothing else
    obst = [(p, F.NODE / 2 + 6) for p in pos.values()]
    for m in nb:
        a, b = np.array(pos[m]), np.array(pos[focus])
        mid, d = (a + b) / 2, (b - a) / np.linalg.norm(b - a)
        nrm = np.array([-d[1], d[0]])
        best = None
        for sgn in (1, -1):
            p = mid + sgn * 24 * nrm
            box = (p[0] - 13, p[1] - 13, p[0] + 13, p[1] + 13)
            if any(F.box_hits_disc(box, *q, r=F.NODE / 2) for q in pos.values()):
                continue
            if any(F.box_hits_segment(box, pos[x], pos[y], pad=2) for x, y in EDGES):
                continue
            best = p
            break
        assert best is not None, f"katz-floor: no clear place for the alpha on {m}->{focus}"
        body += F.text(best[0], best[1], "$\\alpha$", color="accenttwo")
    F.emit("katz-floor", body, container="col", h=400)


# =========================================================================== walks-discount
def walks_from(G, u, k):
    """Every walk of length k from u, by depth-first search (a walk may revisit nodes and edges)."""
    out = [(u,)]
    for _ in range(k):
        out = [w + (v,) for w in out for v in sorted(G[w[-1]])]
    return out


WD_SX, WD_SY = 150, 118
WD_COLS = {2: "accent", 3: "accent!50"}              # fainter = longer


def arrow_to(a, b, color, w=6.0, bend=0):
    """An arrow between two named discs, 3 bp short of each border so the head never merges
    into a disc of the same hue.  `bend` (degrees, negative = to the right) bows the arrow."""
    path = f"to[bend left={bend}]" if bend else "--"
    return (f"\\draw[line width={w}bp,draw={color},shorten >=3bp,shorten <=3bp,"
            f"-{{Latex[length=15bp,width=18bp]}}] ({a}) {path} ({b});\n")


def fig_walks_discount():
    """Walks from u to v in W5 (the pair of slide 10): none of length 1, two of length 2, one of 3."""
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
    P = {n: (45 + WD_SX * x, 100 + WD_SY * (y + 0.9)) for n, (x, y) in S.W5_XY.items()}
    check_graph_planar(P, list(G.edges()), "walks-discount")
    # the one edge two drawn walks share (n2-v) is bowed for the longer walk
    shared = {frozenset(p) for w in ends[2] for p in zip(w, w[1:])} & \
             {frozenset(p) for p in zip(ends[3][0], ends[3][0][1:])}
    assert shared == {frozenset(("n2", "v"))}, shared

    sum_line = ("$" + "+".join(
        f"{c}\\alpha" + (f"^{k + 1}" if k else "") for k, c in enumerate(counts)) + "+\\cdots$")
    sum_line = sum_line.replace("+", " + ")
    lx, seg_len = 300, 36

    def frame(n_drawn, total=False):
        body = edges_body(list(G.edges()), P)
        for n in S.W5_ORDER:
            body += nd(*P[n], label={"u": "u", "v": "v"}.get(n, ""), name=n, outline=False)
        for k, w in drawn[:n_drawn]:
            for a, b in zip(w, w[1:]):
                bend = -22 if (k == 3 and (a, b) == ("n2", "v")) else 0
                body += arrow_to(a, b, WD_COLS[k], bend=bend)
        rows = {2: 300, 3: 220}
        for k in (2, 3):
            if any(kk == k for kk, _ in drawn[:n_drawn]):
                ly = rows[k]
                for j in range(k):
                    body += (f"\\draw[line width=6bp,draw={WD_COLS[k]},-{{Latex[length=15bp,"
                             f"width=18bp]}}] ({lx + j * seg_len},{ly}) -- ({lx + (j + 1) * seg_len - 3},{ly});\n")
                body += F.text(lx + k * seg_len + 14, ly, f"$\\alpha^{k}$", anchor="west")
        if total:
            body += F.text(W_COL / 2, 28, sum_line)
        return body

    frames = [frame(3, True), frame(0), frame(1), frame(2), frame(3, True)]
    # the sum line must fit under the graph
    assert est_w(sum_line.replace("$", "").replace("\\alpha", "a").replace("\\cdots", "...")) < W_COL - 20
    F.emit_gif("walks-discount", frames, container="col", h=400,
               durations=[1500, 700, 1200, 1200, 1800], hold=4)


FIGURES = [
    ("eigen-inherit", fig_eigen_inherit),
    ("eigen-equation", fig_eigen_equation),
    ("eig-all", fig_eig_all),
    ("eig-pf", fig_eig_pf),
    ("power-step1", fig_power_step1),
    ("ring-4444", fig_ring_4444),
    ("ring-local", fig_ring_local),
    ("katz-floor", fig_katz_floor),
    ("walks-discount", fig_walks_discount),
    ("eig-centrality", fig_eig_centrality),
]
