#!/usr/bin/env python3
"""Parts 7-8: the four awkward questions, and the straight line that proves nothing.

Eleven figures, slides 075-090 of `m04-node-degree.md`.  Each carries the single claim
of its slide:

    individual-vs-average   five of the eight sit below, two above, one exactly on it
    mean-vs-median          which average you compare against moves the answer 9 points
    vanishing               Var(k) = 0 is the only escape, and it costs all structure
    directed                in and out are two degrees, and an arrow's far end tilts both
    assortativity           one degree sequence, three wirings, three values of r
    assortativity-real      four measured r, social positive, the rest negative
    lognormal-trap          straight to R^2 = 0.99 over 2.3 decades, and not a power law
    scale-free-debate       1999 the claim, 2011 the doubt, 2019 the audit
    consequences            the second moment is what the earlier modules used
    recap                   the five things
    m05-teaser              two clumps

Every number is computed from `verify_numbers`; the quoted figures are checked against
the verbatim sentences that module keeps from the papers, so a typo here fails the build
rather than the review.
"""

import math

import networkx as nx
import numpy as np

from figlib import (EDGE_W, NODE, SMALLNODE, Axes, assert_planar_drawing,
                    clearance_bad, crossings, disc, dot, emit, polyline, pct, seg, text)
from feld import ABOVE, BELOW, EQUAL, degree, friend_mean
from verify_numbers import (LITERATURE, ccdf, ccdf_fit, condmat, internet_as,
                            lognormal_degrees, moments, net_stats, yeast_ppi)

# --------------------------------------------------------------------------- quoted
# Nothing here is computable from the data we hold, so each is pinned to the sentence
# verify_numbers.LITERATURE keeps verbatim from the paper. Mistype one and the import
# fails; the alternative is a number that only a reviewer with the PDF open can check.
FB_BELOW_MEAN = 0.927        # Ugander et al. 2011, arXiv:1111.4503
FB_BELOW_MEDIAN = 0.836
FB_R = 0.226
for _quote in ("92.7%", "83.6%", "721 million", "r = 0.226",
               "gamma = 3", "substantial curvature",
               # Broido & Clauset 2019, Nat. Commun. 10:1017, abstract. The corpus was
               # printed as "927" on the strength of how widely it is quoted; the
               # abstract says "nearly 1000" and LITERATURE now records that 927 could
               # not be verified. This is the slide that teaches the room not to trust
               # an eyeballed claim, so it is the last one that may carry a remembered
               # number.
               "nearly 1000 network data sets", "only 4% exhibiting"):
    assert _quote in LITERATURE, f"{_quote!r} is not in verify_numbers.LITERATURE"

BC_NETWORKS, BC_STRONG = "nearly 1000", 0.04


def _dec(x, places):
    """Round half UP in decimal -- 0.9857... must print 0.99, and a float rounds 0.575
    to 57 because it is really 57.49999999999999."""
    from decimal import ROUND_HALF_UP, Decimal
    return str(Decimal(repr(float(x))).quantize(Decimal("1." + "0" * places),
                                                rounding=ROUND_HALF_UP))


def _signed(x, places=3):
    if abs(x) < 0.5 * 10 ** -places:
        return "$" + _dec(0, places) + "$"
    return ("$+" if x > 0 else "$-") + _dec(abs(x), places) + "$"


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

    ccdf() is O(distinct x n); the power-law sample has tens of thousands of distinct
    degrees. Asserted equal to ccdf() on the real array before either is drawn.
    """
    k, c = np.unique(np.asarray(d), return_counts=True)
    return k, 1.0 - np.cumsum(c) / c.sum()


def _tail_sketch(x0, y0, x1, y1, color="accent"):
    """A log-log CCDF as a pictogram: two spines and one straight descent."""
    o = seg((x0, y0), (x0, y1), color="annot", w=2.4)
    o += seg((x0, y0), (x1, y0), color="annot", w=2.4)
    o += polyline([(x0 + 14, y1 - 12), (x1 - 12, y0 + 14)], color=color, w=5.0)
    return o


# ===========================================================================
# slide 076 -- the eight girls, sorted.  Facebook moved to its own slide (C-6/D-1):
# one slide was teaching the hub reversal on eight girls and mean-vs-median on
# 721 million users at the same time.
# ===========================================================================
def fig_individual_vs_average():
    assert (len(BELOW), len(ABOVE), len(EQUAL)) == (5, 2, 1), "the Feld split moved"
    assert len(BELOW) + len(ABOVE) + len(EQUAL) == 8

    # "5 have fewer" never said fewer than WHAT. The header says it once, for all three
    # groups, rather than three times in three row labels.
    #
    # And the discs used to carry only her own k, which CONTRADICTED the grouping the
    # figure is built on: two girls printing 2 sat in different groups and two printing
    # 3 sat under "fewer", because the quantity that decides the group -- her friends'
    # average -- was nowhere on the drawing. Both numbers are on it now.
    b = text(540, 330, "each girl against her friends' average", anchor="south")
    groups = [(BELOW, f"{len(BELOW)} have fewer", "accenttwo", 280),
              (ABOVE, f"{len(ABOVE)} have more", "accent", 720),
              (EQUAL, f"{len(EQUAL)} the same", "annot", 960)]
    for girls, lab, fill, cx in groups:
        x0 = cx - 60 * (len(girls) - 1)
        for i, g in enumerate(girls):
            k, fm = degree(g), friend_mean(g)
            rel = (fm > k) - (fm < k)
            assert rel == {"accenttwo": 1, "accent": -1, "annot": 0}[fill], \
                f"{g} is drawn in the {fill} group but {k} vs {fm} says otherwise"
            b += disc(x0 + 120 * i, 240, str(k), fill=fill)
            # bare number, not "vs 4.0": the line under the row already says what the
            # second number is, and the two words cost 60bp of pitch per disc
            b += text(x0 + 120 * i, 200, f"${_dec(fm, 1)}$", color="annot",
                      anchor="north")
        b += text(cx, 146, lab, color=fill, anchor="north")
    b += text(540, 72, "her $k$ in the disc, her friends' average below it",
              color="annot", anchor="north")
    emit("individual-vs-average", b, container="full", h=400)


# ===========================================================================
# slide 076b -- which average you compare against, on Facebook's own numbers
# ===========================================================================
def fig_mean_vs_median():
    lo, hi, x0, x1, ay = 80, 100, 150, 1030, 190

    def X(v):
        return x0 + (v - lo) / (hi - lo) * (x1 - x0)

    gap = FB_BELOW_MEAN - FB_BELOW_MEDIAN
    assert 0 < gap < 0.1

    b = seg((x0, ay), (x1, ay), color="annot", w=2.6)
    for v in (80, 85, 90, 95, 100):
        b += seg((X(v), ay), (X(v), ay - 9), color="annot", w=2.6)
        b += text(X(v), ay - 17, f"{v}", color="annot", anchor="north")
    for share, tail in ((FB_BELOW_MEDIAN, "friends' median"),
                        (FB_BELOW_MEAN, "friends' mean")):
        x = X(share * 100)
        b += seg((x, ay + 14), (x, ay + 44), color="annot", w=2.2)
        b += text(x, 324, pct(share, 1), color="accenttwo", anchor="south")
        b += text(x, 280, "are below their", anchor="south")
        b += text(x, 236, tail, anchor="south")
        b += dot(x, ay, color="accenttwo", d=SMALLNODE)
    # the gap between the two is the point of the slide, so it is drawn, not left to
    # the reader's arithmetic
    xa, xb = X(FB_BELOW_MEDIAN * 100), X(FB_BELOW_MEAN * 100)
    b += polyline([(xa, 140), (xa, 128), (xb, 128), (xb, 140)], color="annot", w=2.2)
    b += text((xa + xb) / 2, 118, f"{_dec(gap * 100, 1)} points apart",
              color="annot", anchor="north")
    b += text(590, 74, "\\% of Facebook's 721 million users",
              color="annot", anchor="north")
    emit("mean-vs-median", b, container="full", h=400)


# ===========================================================================
# slide 078 -- the only escape is a graph with no structure left
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

    pos_lat = {i: ((140 if i % 2 == 0 else 56) * math.cos(math.radians(45 * i)),
                   (88 if i % 2 == 0 else 36) * math.sin(math.radians(45 * i)))
               for i in range(8)}

    b = ""
    panels = [("ring", ring6, _ring(6, 140, 88), 180),
              ("complete graph", k5, _ring(5, 140, 88, phase=18), 540),
              ("ring lattice", lat, pos_lat, 900)]
    for title, g, pos, cx in panels:
        ks = {g.degree(n) for n in g.nodes()}
        assert len(ks) == 1, f"{title} is not regular: degrees {sorted(ks)}"
        assert moments(g)["var"] == 0, f"{title}: Var(k) is not exactly 0"
        p = _centre(pos, cx, 205)
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
        b += text(cx, 340, title, anchor="south")
    # Once, centred, for the row. It was set under each panel and again in the body --
    # the same three characters four times on one slide.
    b += text(540, 72, "Var$(k) = 0$ in all three", color="accenttwo", anchor="north")
    emit("vanishing", b, container="full", h=420)


# ===========================================================================
# slide 080 -- in and out are two degrees, and an arrow's far end tilts both
# ===========================================================================
# Eight arcs. C is the account four others watch and that watches only one; the
# underlying undirected graph is planar and drawn so.
ARCS = [("A", "C"), ("B", "C"), ("D", "C"), ("E", "C"), ("C", "F"),
        ("A", "B"), ("D", "A"), ("E", "B")]
DIR_POS = {"A": (-207, 56), "B": (-207, -56), "D": (-54, 78), "E": (-54, -78),
           "C": (99, 0), "F": (234, 0)}


def fig_directed():
    kin = {n: 0 for n in DIR_POS}
    kout = {n: 0 for n in DIR_POS}
    for a, c in ARCS:
        kout[a] += 1
        kin[c] += 1
    M, N = len(ARCS), len(DIR_POS)
    assert sum(kin.values()) == sum(kout.values()) == M

    def at_arrow_end(k):
        """Mean degree of the account you reach by walking a random arrow.

        Sum k^2 / sum k -- the same edge-end sampling the module has done since Part
        Three, now on a directed graph. THIS is what "tilt" means; the figure used to
        assert it in words (an arrow-conservation line the slide never used) instead
        of comparing a node to the nodes at the other end of its arrows.
        """
        return sum(v * v for v in k.values()) / sum(k.values())

    b = ""
    panels = [("in-degree (followers)", kin, "an arrow's head", 279),
              ("out-degree (following)", kout, "an arrow's tail", 801)]
    for title, counts, phrase, cx in panels:
        mean = M / N
        end = at_arrow_end(counts)
        assert end > mean, f"{title}: the far end does not tilt up ({end} vs {mean})"
        p = _centre(DIR_POS, cx, 205)
        assert_planar_drawing([tuple(e) for e in ARCS], p, "directed")
        for a, c in ARCS:
            b += _arrow(p[a], p[c])
        for n, xy in p.items():
            b += disc(xy[0], xy[1], str(counts[n]), fill="accent")
        b += text(cx, 322, title, anchor="south")
        b += text(cx, 94, f"an account at random: ${_dec(mean, 1)}$", anchor="north")
        b += text(cx, 38, f"{phrase}: ${_dec(end, 1)}$", color="accenttwo",
                  anchor="north")
    emit("directed", b, container="full", h=420)


# ===========================================================================
# slide 082 -- one degree sequence, three wirings
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
# Laid out shallow. r is a fourth row of type now, so each graph has to live in about
# 160bp of height or the 380bp cap binds and every label in the figure shrinks.
LAYOUTS = {
    # the K4 core {0,1,2,3} as a triangle with 3 inside it, the two 2-chains folded UP
    # beside the apex rather than hanging below it
    "hubs together": {0: (-70, -45), 1: (70, -45), 2: (0, 55), 3: (0, -12),
                      4: (-145, 10), 6: (-145, 72), 5: (145, 10), 7: (145, 72)},
    # hub 0 left, hub 5 right, two disjoint paths between them, leaves on both
    "hubs apart": {0: (-85, 0), 1: (-142, 35), 2: (0, 68), 3: (-142, -35),
                   4: (0, -68), 5: (85, 0), 6: (142, 40), 7: (142, -40)},
    # the 4-cycle 0-2-1-3 with its diagonal, a triangle on 0, a leaf on 1, a tail on 3
    "hubs indifferent": {0: (-50, 0), 1: (50, 0), 2: (0, 58), 3: (0, -58),
                         4: (-105, 42), 5: (112, 40), 6: (75, -58), 7: (148, -58)},
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
        p = _centre(LAYOUTS[name], cx, 200)
        assert_planar_drawing(WIRINGS[name], p, name)
        hubs = [n for n in g.nodes() if g.degree(n) == max(seq)]
        assert len(hubs) == 2
        b += _graph(WIRINGS[name], p,
                    {n: "accenttwo" if n in hubs else "accent" for n in g.nodes()},
                    labels={n: g.degree(n) for n in g.nodes()})
        b += text(cx, 320, name, anchor="south")
        # r was invisible here while the next slide plotted four of them, so those dots
        # encoded a quantity the deck had never named. Computed from the drawn graph.
        b += text(cx, 96, "$r = " + _signed(rs[name], 2)[1:-1] + "$",
                  color="accenttwo", anchor="north")
    b += text(540, 50, "all three: $k = " + ",".join(str(k) for k in seq) + "$",
              anchor="north")
    emit("assortativity", b, container="full", h=420)


# ===========================================================================
# slide 083 -- four measured r on one axis
# ===========================================================================
def fig_assortativity_real():
    rows = [("Facebook", FB_R),
            ("cond-mat", float(nx.degree_assortativity_coefficient(condmat()))),
            ("Internet AS", float(nx.degree_assortativity_coefficient(internet_as()))),
            ("yeast proteins", float(nx.degree_assortativity_coefficient(yeast_ppi())))]
    assert [n for n, r in rows if r > 0] == ["Facebook", "cond-mat"]
    assert [n for n, r in rows if r < 0] == ["Internet AS", "yeast proteins"]
    assert rows == sorted(rows, key=lambda t: -t[1]), "rows must run downward in r"

    # The window is +-0.30, not the full +-1: Internet AS and yeast differ by 0.028, and
    # over the full range their 28bp discs would overlap and the row order would be
    # unreadable. So the quantity is named, the ticks give the scale, and a note carries
    # the range this window is a zoom of.
    lo, hi, ax0, ax1, ay = -0.30, 0.30, 340, 900, 135

    def X(v):
        return ax0 + (v - lo) / (hi - lo) * (ax1 - ax0)

    # The caveat now sits in the axis title, under the axis it qualifies. Set at the
    # top left it was ~470bp from that axis and read after the dots, so Facebook's
    # +0.226 looked near-maximal on a scale whose real ends are +-1.
    b = seg((X(0), ay), (X(0), 358), color="annot", w=2.4)
    b += seg((ax0, ay), (ax1, ay), color="annot", w=2.4)
    for v in (-0.2, 0.0, 0.2):
        b += seg((X(v), ay), (X(v), ay - 9), color="annot", w=2.4)
        b += text(X(v), ay - 25, _signed(v, 1), color="annot", anchor="north")
    b += text(620, 53, "assortativity $r$: this axis spans $\\pm0.3$ of a $\\pm1$ scale",
              anchor="north")
    for (name, r), y in zip(rows, (344, 284, 224, 164)):
        assert lo < r < hi, f"{name}: r = {r} is off the axis"
        col = "accent" if r > 0 else "accenttwo"
        b += text(300, y, name, anchor="east")
        b += polyline([(316, y), (X(r) - 17, y)], color="annot", w=1.8,
                      dash="dash pattern=on 3bp off 7bp")
        b += dot(X(r), y, color=col, d=SMALLNODE)
        b += text(930, y, _signed(r), color=col, anchor="west")
    emit("assortativity-real", b, container="full", h=430)


# ===========================================================================
# slide 086 -- straight to R^2 = 0.99, and not a power law at all
# ===========================================================================
KLO, KHI = 5, 1000          # the drawn range IS the fitted range, so one span is quoted


def _minimax_powerlaw(ks, surv):
    """The straight line lying closest to these points, in the max-gap sense.

    The slide's claim is that you cannot tell the two apart, so the power law drawn is
    the strongest version of that claim. For a fixed exponent the best intercept centres
    the residuals, so the Chebyshev line is one scan over the exponent; a least-squares
    line answers a different question.
    """
    sel = (ks >= KLO) & (ks <= KHI) & (surv > 0)
    x, y = np.log10(ks[sel]), np.log10(surv[sel])
    best = None
    for alpha in np.linspace(0.7, 1.5, 1601):
        res = y + alpha * x
        err = (res.max() - res.min()) / 2
        if best is None or err < best[0]:
            best = (float(err), float(alpha), float((res.max() + res.min()) / 2))
    return best


def _powerlaw_sample(alpha, xmin, n=300000, seed=11):
    """A Pareto(alpha) sample floored to integers -- a genuine discrete power law."""
    u = np.random.default_rng(seed).random(n)
    d = np.floor(xmin * u ** (-1.0 / alpha)).astype(int)
    return d[d >= 1]


def fig_lognormal_trap():
    ln = lognormal_degrees()
    ks_ln, su_ln = ccdf(ln)
    assert np.allclose(_ccdf_fast(ln)[1], su_ln), "the fast CCDF disagrees with ccdf()"

    # C-3. The deck said "three decades". Over a true three decades this log-normal fits
    # to R^2 = 0.983 and -- worse for the slide -- the closest power law then stands
    # 0.41 decades off it at k = 6, so the figure would show two curves the room CAN
    # tell apart, which is the opposite of the point. The honest span is the drawn one,
    # and it is printed on the figure rather than left to the prose.
    decades = math.log10(KHI / KLO)
    slope, _, r2, npts = ccdf_fit(ks_ln, su_ln, KLO, KHI)
    assert r2 > 0.98, f"the log-normal must look straight; R^2 = {r2:.4f}"
    assert 2.2 < decades < 2.4 and slope < 0

    err, alpha, logc = _minimax_powerlaw(ks_ln, su_ln)
    pl = _powerlaw_sample(alpha, 10 ** (logc / alpha))
    ks_pl, su_pl = _ccdf_fast(pl)
    _, _, r2_pl, _ = ccdf_fit(ks_pl, su_pl, KLO, KHI)
    assert r2_pl > 0.99, r2_pl

    # "indistinguishable" is the claim, so measure it on the two sampled curves
    grid = np.unique(np.round(np.logspace(math.log10(KLO), math.log10(KHI), 60)).astype(int))
    gap = max(abs(math.log10(float((pl > k).mean()) / float((ln > k).mean()))) for k in grid)
    assert gap < 0.16, f"the two CCDFs are {gap:.2f} decades apart -- not on top of each other"

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
    # Lifted clear of the x spine: the R^2 line sat 8bp above y0 = 140, which the
    # collision gate reads as the axis crossing the label, and 8bp is tight on the
    # render too. 56bp apart rather than 42 so the two lines' boxes do not touch.
    b += text(200, 236, "a log-normal", color="accenttwo", anchor="west")
    b += text(200, 180, f"$R^2 = {_dec(r2, 2)}$ across ${_dec(decades, 1)}$ decades",
              color="accenttwo", anchor="west")
    emit("lognormal-trap", b, container="full", h=400)


# ===========================================================================
# slide 087 -- the claim, the doubt, the audit
# ===========================================================================
def fig_scale_free_debate():
    b = seg((60, 230), (1005, 230), color="annot", w=3.0)
    b += seg((1005, 230), (1030, 230), color="annot", w=3.0,
             arrow="-{Stealth[length=16bp,width=12bp]}")
    # The 2019 dot carried no content, and the slide's title promises a statistical
    # test that nothing on the drawing named. Each dot now says what its year
    # contributed, and 2019 names the test.
    # "Barabási" in UTF-8, not "Barab\'{a}si": figlib's collision boxes are sized from
    # len(the source string), so five characters of TeX escape for one glyph inflated
    # this label's modelled width by 29% and it was rejected for overlapping a label
    # the render puts 108bp away. Measured, not argued -- see the note to the lead.
    marks = [(180, "1999", "Barabási \\& Albert", "the claim",
              ["$\\gamma = 3$"]),
             (520, "2011", "Ugander et al.", "the doubt", ["curvature"]),
             (850, "2019", "Broido \\& Clauset", "the audit",
              ["likelihood-ratio tests", f"{pct(BC_STRONG)} of {BC_NETWORKS} networks"])]
    for x, year, who, role, what in marks:
        b += dot(x, 230, color="accent", d=SMALLNODE)
        b += text(x, 285, year, anchor="south", size=48)
        b += text(x, 195, who, anchor="north")
        b += text(x, 143, role, color="annot", anchor="north")
        for i, line in enumerate(what):
            b += text(x, 91 - 56 * i, line, anchor="north")
    emit("scale-free-debate", b, container="full", h=380)


# ===========================================================================
# slide 088 -- everything earlier came out of the second moment
# ===========================================================================
def fig_consequences():
    s = net_stats(condmat())
    kappa = s["k2"] / s["k1"]
    fc = 1 - 1 / (kappa - 1)                 # Molloy-Reed, the Module 03 threshold
    lam = s["k1"] / s["k2"]                  # the spreading threshold
    assert 0.9 < fc < 1.0 and 0.03 < lam < 0.06, (fc, lam)

    b = _tail_sketch(40, 150, 280, 300)
    # Both numbers below are cond-mat's, last drawn 32 slides earlier, and the figure
    # named neither the network nor the fact that the third result is still to come.
    b += text(160, 120, "cond-mat's tail", color="annot", anchor="north")
    # The flow runs ALONG one arrow with the quantity labelled above it, rather than
    # arrows terminating at a floating <k^2>. Collision boxes are sized from source
    # length, so `$\langle k^2\rangle$` models as 408bp around an 85bp glyph and
    # swallows any arrow that reaches it -- an arrow pointing at a label is not
    # currently drawable. Running the arrow past the label instead keeps the relation
    # visible and keeps the label clear of it.
    b += _arrow((300, 196), (612, 196), color="annot", gap_tail=0, gap_head=0)
    b += text(450, 290, "$\\langle k^2\\rangle$", color="accenttwo")
    results = [(330, "Module 03: robustness", f"$f_c = {_dec(fc, 2)}$"),
               (222, "Module 02: distance", "shorter paths"),
               (114, "spreading: still to come",
                f"$\\langle k\\rangle/\\langle k^2\\rangle = {_dec(lam, 3)}$")]
    for y, head, val in results:
        b += _arrow((676, 196), (716, y - 22), color="annot", gap_tail=0, gap_head=0)
        b += text(742, y, head, anchor="west")
        b += text(742, y - 56, val, color="accenttwo", anchor="west")
    emit("consequences", b, container="full", h=440)


# ===========================================================================
# slide 089 -- the module on one page
# ===========================================================================
def fig_recap():
    from verify_numbers import FELD_EDGES
    m = moments(nx.Graph([tuple(e) for e in FELD_EDGES]))
    k1, gap, friend = float(m["k1"]), float(m["gap"]), float(m["friend"])
    assert k1 + gap == friend

    b = ""
    # Act one, in slide 076's key: 5 below, 2 above, 1 exactly equal. Drawn 5 red +
    # 3 gray, it taught three ties against the key the deck had just given the room.
    fills = ["accenttwo"] * len(BELOW) + ["accent"] * len(ABOVE) + ["annot"] * len(EQUAL)
    assert len(fills) == 8
    for i, fill in enumerate(fills):
        b += disc(108 - 63 + 42 * (i % 4), 292 if i < 4 else 240,
                  fill=fill, size=SMALLNODE)

    # Act two: 2.5 of your own, plus the gap the variance buys. All gray -- accent-2
    # means "her friends have more" in panel one and must not mean a second thing here.
    x0, x1 = 224, 424
    xm = x0 + (k1 / friend) * (x1 - x0)
    b += polyline([(x0, 266), (x1, 266)], color="annot", w=8.0)
    for x in (x0, xm, x1):
        b += seg((x, 250), (x, 282), color="annot", w=2.4)

    # Act three: the tail we measured.  Act five: the same picture, not to be trusted.
    b += _tail_sketch(465, 190, 615, 330)
    b += _tail_sketch(897, 190, 1047, 330)
    b += polyline([(911, 314), (1040, 203)], color="accenttwo", w=5.0,
                  dash="dash pattern=on 10bp off 8bp")
    b += text(972, 332, "?", color="annot", anchor="south", size=48)

    # Act four: Part Seven, which the recap dropped entirely. Two hubs touching, two
    # leaves each -- symmetric, so it reads as "the hubs are adjacent" rather than as
    # the four-node path an earlier diagonal placement produced.
    #
    # Hubs in accent-2, exactly as `assortativity.png` draws the same two degree-4 hubs
    # on slide 088. Drawn in accent they reproduced, inside this panel, the very defect
    # panel one is guarded against two lines above: a recap that recolours what the
    # deck just taught.
    hub = [(756 - 30, 286), (756 + 30, 286)]
    leaf = [(660, 328), (660, 244), (852, 328), (852, 244)]
    b += seg(hub[0], hub[1])
    for i, p in enumerate(leaf):
        b += seg(hub[0] if i < 2 else hub[1], p)
    for p in leaf:
        b += disc(p[0], p[1], fill="accent", size=SMALLNODE)
    for p in hub:
        b += disc(p[0], p[1], fill="accenttwo", size=SMALLNODE)

    # Five panels in 1080bp leaves 216bp of pitch, and the collision boxes are sized
    # from source-string length, so each pair of neighbouring captions has a character
    # budget. These are the shortest wordings that still name their act; the numbers
    # they used to carry in full ("2.5 + 0.5 = 3.0", the exponent) are in the deck's
    # figcaption, which is where the lead ruled they should go when a drawing cannot
    # hold its annotations at 36pt.
    # Panel three carries no second line: its neighbour holds the identity, which has
    # to stay whole -- "2.5 + 0.5" without the "= 3.0" is a fragment, not an identity --
    # and the pictogram plus "one tail" says panel three's act without help.
    for cx, head, val in (
            (108, "the girls", f"{len(BELOW)} of 8"),
            (324, "identity",
             f"${_dec(k1, 1)}+{_dec(gap, 1)}={_dec(friend, 1)}$"),
            (540, "one tail", None),
            (756, "one wiring", "$r \\neq 0$"),
            (972, "one doubt", "$R^2=0.99$")):
        b += text(cx, 152, head, anchor="north")
        if val:
            b += text(cx, 106, val, color="annot", anchor="north")
    emit("recap", b, container="full", h=400)


# ===========================================================================
# slide 090 -- two clumps, unlabelled
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
    ("mean-vs-median", fig_mean_vs_median),
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
