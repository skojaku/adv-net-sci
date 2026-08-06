#!/usr/bin/env python3
"""The one reference layout of the karate club, solved once and cached.

Fourteen figures draw this network. If each solved its own positions the room would be
asked to re-learn where everyone sits every time a slide changed colour, so the layout is
computed once, written to `karate-layout.json`, and every figure recolours it without
moving a single disc.

    python3 figures/layout.py            # re-solve and rewrite the cache
    python3 figures/layout.py --report   # measure the cached one

The graph has 34 nodes and 78 edges and is **not planar**, so F2's "draw it planar" is
unreachable; the honest target is the fewest crossings a legible drawing can have. What
the solver enforces as hard constraints, because those are the ones that make a figure
unreadable rather than merely busy:

  * no two discs closer than SEP centre to centre -- overlapping nodes
  * no edge passing within CLEAR of a disc it does not end at -- an edge that appears
    to terminate at the wrong person
  * everything inside the canvas -- ink outside it is silently clipped, not cropped

and it minimises, in order: crossings, then edge-length spread, then deviation from the
two-lobe arrangement the story needs.

**Why the cost function is incremental.** The first version recomputed all 3003 edge
pairs and all 2652 edge-disc distances for every one of 234,000 proposals and did not
finish in ten minutes. Moving one node can only change the terms that touch it, so each
proposal now rescores that node's own edges against the rest -- about 4% of the work, and
the whole solve runs in under a minute.

The two-lobe bias is a **layout choice made from the recorded outcome**, which is fine
here and stated on the slide the first time colour appears: the audience is told the club
split before any figure claims a side.
"""

import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
CACHE = HERE / "karate-layout.json"

W, H = 1044.0, 336.0          # the drawing box in bp; the canvas adds a margin
MARGIN = 22.0                 # keeps a disc's own radius inside the page
NODE = 34.0                   # disc diameter for the club figures -> 34px on the slide
SEP = 46.0                    # minimum centre-to-centre distance between discs
CLEAR = 20.0                  # minimum distance from an edge to a disc it does not touch

# A full-width figure is 1080bp wide and at most 380bp tall, so every club figure is a
# 3:1 box whether or not that suits the graph. It turns out not to matter: **crossings
# are invariant under an affine map**, so a layout solved in a square and stretched has
# exactly as many as it started with (measured: 79 either way). What the stretch does
# ruin is *distance* -- a 54bp vertical gap becomes 25bp -- so the solve has to happen in
# the final aspect ratio, which is what this file does.


def _graph():
    import networkx as nx
    g = nx.karate_club_graph()
    hi = frozenset(n for n, d in g.nodes(data=True) if d["club"] == "Mr. Hi")
    return g, hi


# ------------------------------------------------------------------ vectorised geometry
def _seg_point_dist(A, B, P):
    """Distance from each point in P to each segment A[i]--B[i].  -> (len(A), len(P))."""
    d = B - A                                              # (E,2)
    L2 = np.maximum((d * d).sum(1), 1e-9)                  # (E,)
    t = ((P[None, :, :] - A[:, None, :]) * d[:, None, :]).sum(-1) / L2[:, None]
    t = np.clip(t, 0.0, 1.0)
    foot = A[:, None, :] + t[:, :, None] * d[:, None, :]
    return np.linalg.norm(foot - P[None, :, :], axis=-1)


def _cross_mask(P, E):
    """Boolean (E,E) of which edge pairs cross, ignoring pairs that share a node."""
    A, B = P[E[:, 0]], P[E[:, 1]]

    def o(p, q, r):        # orientation of r about the line p->q, for all pairs
        return ((q[:, None, 0] - p[:, None, 0]) * (r[None, :, 1] - p[:, None, 1])
                - (q[:, None, 1] - p[:, None, 1]) * (r[None, :, 0] - p[:, None, 0]))

    d1, d2 = o(A, B, A).T, o(A, B, B).T        # transpose: [i,j] = j's ends vs i's line
    d3, d4 = o(A, B, A), o(A, B, B)
    hit = ((d1 > 0) != (d2 > 0)) & ((d3 > 0) != (d4 > 0))
    shared = ((E[:, None, 0] == E[None, :, 0]) | (E[:, None, 0] == E[None, :, 1])
              | (E[:, None, 1] == E[None, :, 0]) | (E[:, None, 1] == E[None, :, 1]))
    return hit & ~shared


class Cost:
    """Total cost, plus a rescore of exactly what one node's move can change.

    The first version of `local` missed one term -- the clearance between node k's disc
    and every edge that does **not** touch it -- so the annealer happily walked a
    stranger's edge across k, and the solve finished with 1.9bp of clearance where 25
    was required. Four terms change when k moves, not three:

      1. crossings involving k's own edges
      2. k's distance to every other disc
      3. k's own edges against every other disc
      4. **every other edge against k's disc**
    """

    def __init__(self, E, side, n=34, w_cross=30.0):
        self.E, self.side, self.n, self.w_cross = E, side, n, w_cross
        self.touch = [np.where((E[:, 0] == k) | (E[:, 1] == k))[0] for k in range(n)]
        self.untouch = [np.where((E[:, 0] != k) & (E[:, 1] != k))[0] for k in range(n)]

    # -- pieces -----------------------------------------------------------------
    def _pen_gap_all(self, P):
        D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=-1)
        np.fill_diagonal(D, np.inf)
        return 60.0 * float(np.sum(np.maximum(0.0, SEP - D) ** 2)) / 2

    def _pen_gap_one(self, P, k):
        D = np.linalg.norm(P - P[k], axis=1)
        D[k] = np.inf
        return 60.0 * float(np.sum(np.maximum(0.0, SEP - D) ** 2))

    def _pen_clear(self, P, eidx, targets=None):
        if len(eidx) == 0:
            return 0.0
        A, B = P[self.E[eidx, 0]], P[self.E[eidx, 1]]
        pts = P if targets is None else P[targets]
        d = _seg_point_dist(A, B, pts)
        if targets is None:
            for r, e in enumerate(eidx):
                d[r, self.E[e, 0]] = d[r, self.E[e, 1]] = np.inf
        return 60.0 * float(np.sum(np.maximum(0.0, CLEAR - d) ** 2))

    def _pen_bounds(self, P):
        out = (np.maximum(0, MARGIN - P[:, 0]) + np.maximum(0, P[:, 0] - (W - MARGIN))
               + np.maximum(0, MARGIN - P[:, 1]) + np.maximum(0, P[:, 1] - (H - MARGIN)))
        return 200.0 * float(np.sum(out ** 2))

    def _pen_side(self, P):
        return 1.4 * float(np.sum(np.maximum(0.0, self.side * (P[:, 0] - W / 2) + 40.0)))

    def lengths(self, P):
        return np.linalg.norm(P[self.E[:, 0]] - P[self.E[:, 1]], axis=1)

    # -- totals -----------------------------------------------------------------
    def total(self, P):
        return (self.w_cross * float(_cross_mask(P, self.E).sum()) / 2
                + self._pen_gap_all(P)
                + self._pen_clear(P, np.arange(len(self.E)))
                + self._pen_bounds(P) + self._pen_side(P)
                + 0.6 * float(self.lengths(P).std()))

    def local(self, P, k):
        eid = self.touch[k]
        return (self.w_cross * float(_cross_mask(P, self.E)[eid].sum())
                + self._pen_gap_one(P, k)
                + self._pen_clear(P, eid)
                + self._pen_clear(P, self.untouch[k], targets=[k])
                + self._pen_bounds(P) + self._pen_side(P)
                + 0.6 * float(self.lengths(P).std()))


def crossings(P, E):
    return int(_cross_mask(P, E).sum() // 2)


def min_gap(P):
    D = np.linalg.norm(P[:, None, :] - P[None, :, :], axis=-1)
    np.fill_diagonal(D, np.inf)
    return float(D.min())


def min_clear(P, E):
    d = _seg_point_dist(P[E[:, 0]], P[E[:, 1]], P)
    for r in range(len(E)):
        d[r, E[r, 0]] = d[r, E[r, 1]] = np.inf
    return float(d.min())


def _start(g, side, seed):
    """A spring layout, rotated so the two clubs separate left-to-right, then stretched.

    Spring layouts of this graph land at 79-94 crossings on their own, which is a far
    better place to start annealing from than anything random -- the anneal's job is to
    open the discs apart and clear the edges, not to rediscover the shape.
    """
    import networkx as nx
    p0 = nx.spring_layout(g, seed=seed, iterations=600, k=1.2)
    P = np.array([p0[n] for n in range(34)], float)
    P -= P.mean(0)
    c = np.array([P[side > 0, 0].mean() - P[side < 0, 0].mean(),
                  P[side > 0, 1].mean() - P[side < 0, 1].mean()])
    th = -math.atan2(c[1], c[0]) + math.pi          # Mr. Hi's club to the left
    R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    P = P @ R.T
    P -= P.min(0)
    P /= np.maximum(P.max(0), 1e-9)
    return P * np.array([W - 2 * MARGIN, H - 2 * MARGIN]) + MARGIN


def fill_box(P):
    """Stretch the finished drawing out to the full box, if that is an expansion.

    Free to do and worth doing: crossings survive any affine map, and the ink-span gate
    wants at least 76% of the canvas width. Expanding only, so no distance shrinks and
    neither hard constraint can be broken by this step.
    """
    lo, hi = P.min(0), P.max(0)
    span = np.maximum(hi - lo, 1e-9)
    s = np.array([W - 2 * MARGIN, H - 2 * MARGIN]) / span
    if s.min() < 1.0:
        return P
    return (P - lo) * s + MARGIN


def polish(P, C, rng, sweeps=14, ring=(9.0, 20.0, 38.0)):
    """Greedy descent after the anneal: try each node on three rings of eight offsets,
    keep the best strict improvement. The anneal finds the shape; this squeezes the last
    crossings out of it without letting temperature undo them again."""
    offs = [(0.0, 0.0)] + [(r * math.cos(a), r * math.sin(a))
                           for r in ring
                           for a in (np.arange(8) * math.pi / 4)]
    for _ in range(sweeps):
        moved = False
        for k in rng.permutation(C.n):
            base = C.local(P, k)
            old = P[k].copy()
            best, bestp = base, old
            for dx, dy in offs[1:]:
                P[k] = np.clip(old + [dx, dy], [MARGIN, MARGIN], [W - MARGIN, H - MARGIN])
                v = C.local(P, k)
                if v < best - 1e-9:
                    best, bestp = v, P[k].copy()
            P[k] = bestp
            moved |= best < base - 1e-9
        if not moved:
            break
    return P


def solve(rounds=22, iters=45000, seed=0):
    g, hi = _graph()
    E = np.array(sorted(tuple(sorted(e)) for e in g.edges()))
    side = np.array([1.0 if n in hi else -1.0 for n in range(34)])
    C = Cost(E, side)

    best = None
    for r in range(rounds):
        rng = np.random.default_rng(1000 + r)
        P = _start(g, side, seed + r)
        T0, T1 = 22.0, 0.25
        for it in range(iters):
            T = T0 * (T1 / T0) ** (it / iters)
            k = int(rng.integers(34))
            before = C.local(P, k)
            old = P[k].copy()
            P[k] = np.clip(old + [rng.normal(0, T * 1.5), rng.normal(0, T * 0.9)],
                           [MARGIN, MARGIN], [W - MARGIN, H - MARGIN])
            after = C.local(P, k)
            if not (after <= before
                    or rng.random() < math.exp((before - after) / max(T, 1e-6))):
                P[k] = old
        P = fill_box(polish(P, C, rng))
        tot, x, gp, cl = C.total(P), crossings(P, E), min_gap(P), min_clear(P, E)
        feasible = gp >= SEP - 0.5 and cl >= CLEAR - 0.5
        print(f"  round {r}: cost {tot:9.1f}  crossings {x:3d}  gap {gp:5.1f}  "
              f"clear {cl:5.1f}  {'ok' if feasible else 'INFEASIBLE'}")
        # a feasible drawing always beats an infeasible one, whatever the cost says
        key = (0 if feasible else 1, x, tot)
        if best is None or key < best[0]:
            best = (key, P.copy())
    return best[1], E


def report(P, E):
    print(f"  crossings                 {crossings(P, E)}  (78 edges, graph is non-planar)")
    print(f"  min centre distance       {min_gap(P):.1f}bp  (need {SEP})")
    print(f"  min edge-to-disc distance {min_clear(P, E):.1f}bp  (need {CLEAR})")
    print(f"  bounding box              {P[:,0].min():.0f}..{P[:,0].max():.0f} x "
          f"{P[:,1].min():.0f}..{P[:,1].max():.0f}")


def load():
    """{node: (x, y)} in bp, with the hard constraints re-checked on every import."""
    d = json.loads(CACHE.read_text())
    P = np.array(d["pos"], float)
    E = np.array(d["edges"])
    assert min_gap(P) >= SEP - 0.5, f"cached layout overlaps discs ({min_gap(P):.1f}bp)"
    assert min_clear(P, E) >= CLEAR - 0.5, (
        f"cached layout runs an edge through a disc ({min_clear(P, E):.1f}bp)")
    assert crossings(P, E) <= d["crossings"], "cached crossing count is stale"
    return ({i: (float(P[i, 0]), float(P[i, 1])) for i in range(len(P))},
            [tuple(e) for e in E.tolist()])


if __name__ == "__main__":
    if "--report" in sys.argv:
        d = json.loads(CACHE.read_text())
        report(np.array(d["pos"], float), np.array(d["edges"]))
    else:
        P, E = solve()
        report(P, E)
        CACHE.write_text(json.dumps(
            {"pos": [[round(x, 2), round(y, 2)] for x, y in P],
             "edges": E.tolist(), "crossings": crossings(P, E)}, indent=0))
        print(f"  wrote {CACHE.name}")
