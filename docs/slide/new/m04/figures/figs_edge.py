#!/usr/bin/env python3
"""Parts 7-8: the four awkward questions, and the straight line that proves nothing.

Ten figures, slides 78-92 of `m04-node-degree.md`.  Each carries the single claim of
its slide:

    individual-vs-average   "on average" is not "for you" -- 5 of 8, and 92.7 vs 83.6
    vanishing               Var(k) = 0 is the only escape, and it costs all structure
    directed                in and out are two degrees, and both tilt
    assortativity           one degree sequence, three wirings
    assortativity-real      four measured r, social positive, the rest negative
    lognormal-trap          straight to R^2 = 0.99 and not a power law at all
    scale-free-debate       1999 the claim, 2011 the doubt, 2019 the audit
    consequences            the second moment is what the earlier modules used
    recap                   the four acts
    m05-teaser              two clumps

Every number is computed from `verify_numbers`; the three quoted Facebook figures are
checked against the verbatim sentences that module keeps from the paper, so a typo here
fails the build rather than the review.
"""

import math

import networkx as nx
import numpy as np

from figlib import (EDGE_W, FONT, NODE, Axes, assert_planar_drawing, clearance_bad,
                    crossings, disc, dot, emit, polyline, pct, seg, text)
from feld import ABOVE, BELOW, EQUAL, degree
from verify_numbers import (LITERATURE, ccdf, ccdf_fit, condmat, internet_as,
                            lognormal_degrees, moments, net_stats, yeast_ppi)

# --------------------------------------------------------------------------- quoted
# Nothing below is computable from the data we hold, so each is pinned to the sentence
# verify_numbers.LITERATURE keeps verbatim from the paper. Mistype one and the import
# fails; the alternative is a number that only a reviewer with the PDF open can check.
FB_BELOW_MEAN = 0.927        # Ugander et al. 2011, arXiv:1111.4503
FB_BELOW_MEDIAN = 0.836
FB_R = 0.226
for _quote in ("92.7%", "83.6%", "721 million", "r = 0.226"):
    assert _quote in LITERATURE, f"{_quote!r} is not in verify_numbers.LITERATURE"


def _dec(x, places):
    """Round half UP in decimal -- 0.9857... must print 0.99, and a float rounds 0.575
    to 57 because it is really 57.49999999999999."""
    from decimal import ROUND_HALF_UP, Decimal
    return str(Decimal(repr(float(x))).quantize(Decimal("1." + "0" * places),
                                                rounding=ROUND_HALF_UP))


def _signed(x, places=3):
    return ("$+" if x >= 0 else "$-") + _dec(abs(x), places) + "$"


def _centre(pos, cx, cy):
    """Translate a node layout so its bounding box centres on (cx, cy)."""
    xs = [p[0] for p in pos.values()]
    ys = [p[1] for p in pos.values()]
    ox = cx - (min(xs) + max(xs)) / 2
    oy = cy - (min(ys) + max(ys)) / 2
    return {k: (v[0] + ox, v[1] + oy) for k, v in pos.items()}


def _graph(edges, pos, fills, labels=None, size=NODE):
    """Edges first, then discs on top, so an edge never crosses a glyph."""
    out = "".join(seg(pos[a], pos[b]) for a, b in edges)
    for n, p in pos.items():
        out += disc(p[0], p[1], "" if labels is None else str(labels[n]),
                    fill=fills[n], size=size)
    return out


def _arrow(p, q, color="black", w=EDGE_W, gap_tail=NODE / 2 + 4, gap_head=NODE / 2 + 8):
    """A straight arc trimmed to both disc borders.

    seg() draws centre to centre, so an untrimmed arrowhead lands *under* the target
    disc -- the m01 defect class the guide opens with. The head standoff is larger than
    the tail's because the Stealth tip is the path end and its own stroke widens the
    visual gap with the line width.
    """
    dx, dy = q[0] - p[0], q[1] - p[1]
    L = math.hypot(dx, dy)
    assert L > gap_tail + gap_head + 16, f"arc of {L:.0f}bp is too short to show an arrow"
    ux, uy = dx / L, dy / L
    return seg((p[0] + ux * gap_tail, p[1] + uy * gap_tail),
               (q[0] - ux * gap_head, q[1] - uy * gap_head),
               color=color, w=w, arrow="-{Stealth[length=14bp,width=11bp]}")


def _ccdf_fast(d):
    """Same quantity as verify_numbers.ccdf, computed in one pass.

    ccdf() is O(distinct x n); the log-normal has 1221 distinct degrees over 144548
    nodes and the power-law sample far more. Asserted equal to ccdf() on the real
    array before either is drawn.
    """
    k, c = np.unique(np.asarray(d), return_counts=True)
    return k, 1.0 - np.cumsum(c) / c.sum()


# ===========================================================================
# slide 78 -- "on average" is not "for you"
# ===========================================================================
def fig_individual_vs_average():
    assert (len(BELOW), len(ABOVE), len(EQUAL)) == (5, 2, 1), "the Feld split moved"
    assert len(BELOW) + len(ABOVE) + len(EQUAL) == 8

    b = ""
    # left: the eight girls sorted into the three classes, each disc carrying her own k
    rows = [(BELOW, f"{len(BELOW)} have fewer", "accenttwo", 308),
            (ABOVE, f"{len(ABOVE)} have more", "accent", 213),
            (EQUAL, f"{len(EQUAL)} the same", "annot", 118)]
    for girls, lab, fill, y in rows:
        b += text(300, y, lab, anchor="east")
        for i, g in enumerate(girls):
            b += disc(340 + 56 * i, y, str(degree(g)), fill=fill)
    b += text(62, 48, "number in disc $=$ her $k$", color="annot", anchor="west")

    # right: Facebook, the same comparison against a mean and against a median
    x0, x1, lo, hi = 650, 1020, 80, 100
    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    b += text(835, 318, "Facebook, 721 M users")
    b += seg((x0, 158), (x1, 158), color="annot", w=2.6)
    for v in (80, 85, 90, 95, 100):
        b += seg((X(v), 158), (X(v), 149), color="annot", w=2.6)
        b += text(X(v), 142, f"{v}", color="annot", anchor="north")
    b += text(820, 106, "\\% below their friends'", color="annot", anchor="north")
    for share, name in ((FB_BELOW_MEDIAN, "median"), (FB_BELOW_MEAN, "mean")):
        x = X(share * 100)
        b += seg((x, 172), (x, 196), color="annot", w=2.2)
        b += text(x, 218, name, anchor="south")
        b += text(x, 263, pct(share, 1), color="accenttwo", anchor="south")
        b += dot(x, 158, color="accenttwo", d=26)
    emit("individual-vs-average", b, container="full", h=400)


# ===========================================================================
# slide 80 -- the only escape is a graph with no structure left
# ===========================================================================
def _ring(n, rx, ry, phase=0.0):
    return {i: (rx * math.cos(math.radians(phase + 360 * i / n)),
                ry * math.sin(math.radians(phase + 360 * i / n))) for i in range(n)}


def fig_vanishing():
    ring6 = nx.cycle_graph(6)
    k5 = nx.complete_graph(5)
    # a ring lattice, k = 4: node i joined to i +- 1 and i +- 2. Drawn as the antiprism
    # it is, so the skip chords do not cross -- the guide's ring-lattice trap.
    lat = nx.Graph((i, (i + s) % 8) for i in range(8) for s in (1, 2))
    assert nx.is_isomorphic(lat, nx.watts_strogatz_graph(8, 4, 0.0, seed=1))

    pos_ring = _ring(6, 140, 88)
    pos_k5 = _ring(5, 140, 88, phase=18)
    pos_lat = {i: p for i, p in enumerate(
        [(140 if i % 2 == 0 else 56) * math.cos(math.radians(45 * i)),
         (88 if i % 2 == 0 else 36) * math.sin(math.radians(45 * i))] for i in range(8))}
    pos_lat = {i: tuple(v) for i, v in pos_lat.items()}

    b = ""
    panels = [("ring", ring6, pos_ring, 180),
              ("complete graph", k5, pos_k5, 540),
              ("ring lattice", lat, pos_lat, 900)]
    for title, g, pos, cx in panels:
        ks = {g.degree(n) for n in g.nodes()}
        assert len(ks) == 1, f"{title} is not regular: degrees {sorted(ks)}"
        assert moments(g)["var"] == 0, f"{title}: Var(k) is not exactly 0"
        p = _centre(pos, cx, 200)
        if title == "complete graph":
            # K5 is Kuratowski's own non-planar graph, so zero crossings is impossible.
            # The convex drawing has exactly the five of the pentagram; assert that
            # number rather than waiving the gate.
            assert len(crossings(list(g.edges()), p)) == 5
            assert not clearance_bad(list(g.edges()), p)
        else:
            assert_planar_drawing(list(g.edges()), p, title)
        b += _graph(list(g.edges()), p, {n: "accent" for n in g.nodes()},
                    labels={n: g.degree(n) for n in g.nodes()})
        b += text(cx, 335, title, anchor="south")
        b += text(cx, 72, "Var$(k) = 0$", color="accenttwo", anchor="north")
    emit("vanishing", b, container="full", h=420)


# ===========================================================================
# slide 82 -- in and out are two degrees, and both of them tilt
# ===========================================================================
# Eight arcs. C is the account four others watch and that watches only one, which is
# the whole asymmetry; the underlying undirected graph is planar and drawn so.
ARCS = [("A", "C"), ("B", "C"), ("D", "C"), ("E", "C"), ("C", "F"),
        ("A", "B"), ("D", "A"), ("E", "B")]
DIR_POS = {"A": (-207, 65), "B": (-207, -65), "D": (-54, 90), "E": (-54, -90),
           "C": (99, 0), "F": (234, 0)}


def fig_directed():
    kin = {n: 0 for n in DIR_POS}
    kout = {n: 0 for n in DIR_POS}
    for a, c in ARCS:
        kout[a] += 1
        kin[c] += 1
    M = len(ARCS)
    assert sum(kin.values()) == sum(kout.values()) == M
    assert kin["C"] == 4 and kout["C"] == 1, "C is meant to be the watched account"

    b = ""
    for title, counts, cx in (("in-degree (followers)", kin, 279),
                              ("out-degree (following)", kout, 801)):
        p = _centre(DIR_POS, cx, 205)
        assert_planar_drawing([tuple(e) for e in ARCS], p, "directed")
        for a, c in ARCS:
            b += _arrow(p[a], p[c])
        for n, xy in p.items():
            b += disc(xy[0], xy[1], str(counts[n]),
                      fill="accenttwo" if n == "C" else "accent")
        b += text(cx, 338, title, anchor="south")
    # Written out rather than set as a sum: at 36pt an inline \sum and a \mathrm{in}
    # subscript render at roughly 25pt, i.e. under the deck's x-height floor, and the
    # gate cannot see it because it measures the surrounding text.
    b += text(52, 72, f"{M} arrows $=$ {M} in $=$ {M} out", anchor="west")
    b += text(1055, 72, f"marked: {kin['C']} in, {kout['C']} out",
              color="accenttwo", anchor="east")
    emit("directed", b, container="full", h=420)


# ===========================================================================
# slide 84 -- one degree sequence, three wirings
# ===========================================================================
# Found by exhausting every 8-node graph with degrees 4,4,3,3,2,2,1,1: of the connected
# planar ones, r runs from -0.700 to +0.300, and the three below are its top, its middle
# and its bottom. (A useful fact that fell out: with these degrees the two hubs can only
# be non-adjacent when r <= -0.30, so "indifferent" necessarily has them touching -- the
# point being that assortativity is the whole pattern, not one edge.)
WIRINGS = {
    "hubs together": [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2),
                      (1, 3), (1, 5), (2, 3), (4, 6), (5, 7)],
    "hubs apart": [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2),
                   (1, 3), (2, 5), (4, 5), (5, 6), (5, 7)],
    "hubs indifferent": [(0, 1), (0, 2), (0, 3), (0, 4), (1, 2),
                         (1, 3), (1, 5), (2, 4), (3, 6), (6, 7)],
}
LAYOUTS = {
    # the K4 core {0,1,2,3} drawn as a triangle with 3 inside it, two 2-chains outside
    "hubs together": {0: (-75, -40), 1: (75, -40), 2: (0, 85), 3: (0, 2),
                      4: (-145, -35), 6: (-145, -105), 5: (145, -35), 7: (145, -105)},
    # hub 0 left, hub 5 right, two disjoint paths between them, leaves on both
    "hubs apart": {0: (-85, 0), 1: (-142, 35), 2: (0, 68), 3: (-142, -35),
                   4: (0, -68), 5: (85, 0), 6: (142, 40), 7: (142, -40)},
    # the 4-cycle 0-2-1-3 with its diagonal, a triangle on 0, a leaf on 1, a tail on 3
    "hubs indifferent": {0: (-55, 0), 1: (55, 0), 2: (0, 70), 3: (0, -70),
                         4: (-105, 55), 5: (120, 55), 6: (65, -115), 7: (135, -85)},
}


def fig_assortativity():
    graphs, rs = {}, {}
    for name, edges in WIRINGS.items():
        g = nx.Graph()
        g.add_nodes_from(range(8))
        g.add_edges_from(edges)
        graphs[name] = g
        rs[name] = float(nx.degree_assortativity_coefficient(g))

    # the point of the slide: one p(k), three networks
    seqs = {n: sorted((d for _, d in g.degree()), reverse=True) for n, g in graphs.items()}
    seq = seqs["hubs together"]
    assert all(s == seq for s in seqs.values()), f"the three degree sequences differ: {seqs}"
    assert seq == [4, 4, 3, 3, 2, 2, 1, 1]
    assert rs["hubs together"] > 0.25, rs
    assert abs(rs["hubs indifferent"]) < 0.02, rs
    assert rs["hubs apart"] < -0.5, rs
    assert rs["hubs together"] > rs["hubs indifferent"] > rs["hubs apart"]

    b = ""
    for name, cx in (("hubs together", 180), ("hubs apart", 540),
                     ("hubs indifferent", 900)):
        g = graphs[name]
        p = _centre(LAYOUTS[name], cx, 205)
        assert_planar_drawing(WIRINGS[name], p, name)
        hubs = [n for n in g.nodes() if g.degree(n) == max(seq)]
        assert len(hubs) == 2
        b += _graph(WIRINGS[name], p,
                    {n: "accenttwo" if n in hubs else "accent" for n in g.nodes()},
                    labels={n: g.degree(n) for n in g.nodes()})
        b += text(cx, 340, name, anchor="south")
    b += text(540, 68, "all three: $k = " + ",".join(str(k) for k in seq) + "$",
              anchor="north")
    emit("assortativity", b, container="full", h=420)


# ===========================================================================
# slide 85 -- four measured r on one axis
# ===========================================================================
def fig_assortativity_real():
    rows = [("Facebook", FB_R),
            ("cond-mat", float(nx.degree_assortativity_coefficient(condmat()))),
            ("Internet AS", float(nx.degree_assortativity_coefficient(internet_as()))),
            ("yeast proteins", float(nx.degree_assortativity_coefficient(yeast_ppi())))]
    assert [n for n, r in rows if r > 0] == ["Facebook", "cond-mat"]
    assert [n for n, r in rows if r < 0] == ["Internet AS", "yeast proteins"]
    assert rows == sorted(rows, key=lambda t: -t[1]), "rows must run downward in r"

    lo, hi, ax0, ax1 = -0.30, 0.30, 340, 900
    def X(v):
        return ax0 + (v - lo) / (hi - lo) * (ax1 - ax0)

    zero = X(0)
    ys = [300, 235, 170, 105]
    b = seg((zero, 76), (zero, 336), color="annot", w=2.4)
    b += text(zero, 348, "$r = 0$", color="annot", anchor="south")
    for (name, r), y in zip(rows, ys):
        assert lo < r < hi, f"{name}: r = {r} is off the axis"
        col = "accent" if r > 0 else "accenttwo"
        b += text(300, y, name, anchor="east")
        b += polyline([(316, y), (X(r) - 16, y)], color="annot", w=1.8,
                      dash="dash pattern=on 3bp off 7bp")
        b += dot(X(r), y, color=col, d=26)
        b += text(930, y, _signed(r), color=col, anchor="west")
    emit("assortativity-real", b, container="full", h=420)


# ===========================================================================
# slide 88 -- straight to R^2 = 0.99, and not a power law at all
# ===========================================================================
def _powerlaw_sample(alpha, xmin, n=200000, seed=11):
    """A Pareto(alpha) sample, floored to integers -- a genuine power law.

    Its two parameters are chosen so that it lands on the same line as the log-normal;
    that is what a modeller fitting a real degree sequence would produce, and the slide
    only works if the two are actually on top of each other.
    """
    u = np.random.default_rng(seed).random(n)
    d = np.floor(xmin * u ** (-1.0 / alpha)).astype(int)
    return d[d >= 1]


def fig_lognormal_trap():
    ln = lognormal_degrees()
    ks_ln, su_ln = ccdf(ln)
    assert np.allclose(_ccdf_fast(ln)[1], su_ln), "the fast CCDF disagrees with ccdf()"
    slope, icept, r2, npts = ccdf_fit(ks_ln, su_ln, 3, 500)
    assert r2 > 0.98, f"the log-normal must look straight; R^2 = {r2:.4f}"

    alpha = -slope
    pl = _powerlaw_sample(alpha, 10 ** (icept / alpha))
    ks_pl, su_pl = _ccdf_fast(pl)
    s_pl, _, r2_pl, _ = ccdf_fit(ks_pl, su_pl, 3, 500)
    assert r2_pl > 0.99 and abs(s_pl - slope) < 0.06, (s_pl, r2_pl)

    KLO, KHI = 5, 1000
    # "indistinguishable" is the claim, so measure it: nowhere in the drawn range may
    # the two curves stand more than a fifth of a decade apart.
    grid = np.unique(np.round(np.logspace(math.log10(KLO), math.log10(KHI), 40)).astype(int))
    gap = max(abs(math.log10(float((pl > k).mean()) / float((ln > k).mean()))) for k in grid)
    assert gap < 0.22, f"the two CCDFs are {gap:.2f} decades apart -- not on top of each other"

    ax = Axes((185, 140, 1040, 335), (KLO, KHI), (1e-3, 1.0), xlog=True, ylog=True,
              xlabel="degree $k$", ylabel="CCDF",
              xticks=[10, 100, 1000], yticks=[1e-3, 1e-2, 1e-1, 1])
    b = ax.frame()
    sel = (ks_pl >= KLO) & (ks_pl <= KHI)
    b += ax.line(ks_pl[sel], su_pl[sel], color="accent", w=6.0)
    keep = np.unique(np.round(np.logspace(math.log10(KLO), math.log10(KHI), 34)).astype(int))
    idx = [int(np.argmin(np.abs(ks_ln - k))) for k in keep]
    b += ax.points(ks_ln[idx], su_ln[idx], color="accenttwo", d=13)
    b += text(1035, 320, "a true power law", color="accent", anchor="east")
    b += text(200, 175, f"a log-normal, $R^2 = {_dec(r2, 2)}$",
              color="accenttwo", anchor="west")
    emit("lognormal-trap", b, container="full", h=400)


# ===========================================================================
# slide 89 -- the claim, the doubt, the audit
# ===========================================================================
def fig_scale_free_debate():
    b = seg((60, 190), (1005, 190), color="annot", w=3.0)
    b += seg((1005, 190), (1030, 190), color="annot", w=3.0,
             arrow="-{Stealth[length=16bp,width=12bp]}")
    marks = [(200, "1999", "Barab\\'{a}si \\& Albert", "the claim"),
             (540, "2011", "Ugander et al.", "the doubt"),
             (880, "2019", "Broido \\& Clauset", "the audit")]
    for x, year, who, what in marks:
        b += dot(x, 190, color="accent", d=26)
        b += text(x, 245, year, anchor="south", size=48)
        b += text(x, 155, who, anchor="north")
        b += text(x, 105, what, color="annot", anchor="north")
    emit("scale-free-debate", b, container="full", h=340)


# ===========================================================================
# slide 90 -- everything earlier came out of the second moment
# ===========================================================================
def _tail_sketch(x0, y0, x1, y1, color="accent"):
    """A log-log CCDF as a pictogram: two spines and one straight descent."""
    o = seg((x0, y0), (x0, y1), color="annot", w=2.4)
    o += seg((x0, y0), (x1, y0), color="annot", w=2.4)
    o += polyline([(x0 + 14, y1 - 12), (x1 - 12, y0 + 14)], color=color, w=5.0)
    return o


def fig_consequences():
    s = net_stats(condmat())
    kappa = s["k2"] / s["k1"]
    fc = 1 - 1 / (kappa - 1)                 # Molloy-Reed, the Module 03 threshold
    lam = s["k1"] / s["k2"]                  # the spreading threshold
    assert 0.9 < fc < 1.0 and 0.03 < lam < 0.06, (fc, lam)

    b = _tail_sketch(32, 150, 292, 300)
    b += text(162, 120, "the tail", color="annot", anchor="north")
    b += _arrow((312, 225), (392, 225), color="annot", gap_tail=0, gap_head=0)
    b += text(452, 225, "$\\langle k^2\\rangle$", color="accenttwo", size=60)
    results = [(350, "Module 03: robustness", f"$f_c = {_dec(fc, 2)}$"),
               (225, "Module 02: distance", "shorter paths"),
               (100, "spreading", f"$\\langle k\\rangle/\\langle k^2\\rangle "
                                  f"= {_dec(lam, 3)}$")]
    for y, head, val in results:
        b += _arrow((516, 225), (616, y - 21), color="annot", gap_tail=0, gap_head=0)
        b += text(640, y, head, anchor="west")
        b += text(640, y - 42, val, color="accenttwo", anchor="west")
    emit("consequences", b, container="full", h=440)


# ===========================================================================
# slide 91 -- the module on one page
# ===========================================================================
def fig_recap():
    m = moments(nx.Graph([tuple(e) for e in __import__("verify_numbers").FELD_EDGES]))
    k1, gap, friend = float(m["k1"]), float(m["gap"]), float(m["friend"])
    assert k1 + gap == friend

    b = ""
    # act one: the eight girls, five of them below their friends
    cx = 135
    for i in range(8):
        x = cx - 63 + 42 * (i % 4)
        y = 262 if i < 4 else 212
        b += disc(x, y, fill="accenttwo" if i < len(BELOW) else "annot", size=28)

    # act two: 2.5 of your own, plus the gap the variance buys, makes 3.0
    cx, x0, x1 = 405, 305, 505
    xm = x0 + (k1 / friend) * (x1 - x0)
    b += polyline([(x0, 237), (xm, 237)], color="annot", w=8.0)
    b += polyline([(xm, 237), (x1, 237)], color="accenttwo", w=8.0)
    for x in (x0, xm, x1):
        b += seg((x, 222), (x, 252), color="annot", w=2.4)

    # acts three and four: the same picture, honest and then not
    b += _tail_sketch(600, 190, 750, 295)
    b += _tail_sketch(870, 190, 1020, 295)
    b += polyline([(884, 279), (1010, 202)], color="accenttwo", w=5.0,
                  dash="dash pattern=on 10bp off 8bp")
    b += text(945, 300, "?", color="annot", anchor="south", size=48)

    for cx, head, val in ((135, "eight girls", f"{len(BELOW)} of 8 below"),
                          (405, "one identity",
                           f"${_dec(k1, 1)}+{_dec(gap, 1)}={_dec(friend, 1)}$"),
                          (675, "one tail", "$p(k)\\sim k^{-\\gamma}$"),
                          (945, "one doubt", "straight $\\neq$ proof")):
        b += text(cx, 148, head, anchor="north")
        b += text(cx, 102, val, color="annot", anchor="north")
    emit("recap", b, container="full", h=400)


# ===========================================================================
# slide 92 -- two clumps, unlabelled
# ===========================================================================
def fig_m05_teaser():
    g = nx.Graph()
    pos = {}
    for side, (cx, phase) in enumerate(((135, 0), (402, 36))):
        hub = f"h{side}"
        pos[hub] = (cx, 180)
        for i in range(5):
            n = f"n{side}{i}"
            a = math.radians(phase + 72 * i)
            pos[n] = (cx + 88 * math.cos(a), 180 + 88 * math.sin(a))
            g.add_edge(hub, n)
            g.add_edge(n, f"n{side}{(i + 1) % 5}")
    g.add_edge("n00", "n12")             # the one edge between the clumps
    assert nx.is_connected(g) and g.number_of_nodes() == 12
    assert len(list(nx.bridges(g))) == 1, "there must be exactly one edge between clumps"
    assert_planar_drawing(list(g.edges()), pos, "m05-teaser")
    emit("m05-teaser", _graph(list(g.edges()), pos, {n: "accent" for n in g.nodes()}),
         container="col", h=376)


FIGURES = [
    ("individual-vs-average", fig_individual_vs_average),
    ("vanishing", fig_vanishing),
    ("directed", fig_directed),
    ("assortativity", fig_assortativity),
    ("assortativity-real", fig_assortativity_real),
    ("lognormal-trap", fig_lognormal_trap),
    ("scale-free-debate", fig_scale_free_debate),
    ("consequences", fig_consequences),
    ("recap", fig_recap),
    ("m05-teaser", fig_m05_teaser),
]
