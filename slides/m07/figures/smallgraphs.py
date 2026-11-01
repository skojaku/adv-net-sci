#!/usr/bin/env python3
"""Every graph and every number the Module 07 (random walks) deck quotes.

    python3 figures/smallgraphs.py        # prints the numbers; exits non-zero if one is wrong

One module, so a figure and a slide cannot disagree about a graph or a value.  A figure
imports from here and never types a number.  Row-vector convention, as in the lecture
note:  P_ij = A_ij / k_i,  x(t+1) = x(t) P,  x(t) = x(0) P^t,  pi_i = k_i / 2m.

Layouts are in grid units (y up); a figure module scales them.
"""

import sys

import networkx as nx
import numpy as np


# --------------------------------------------------------------------------- core maths
def adj(G, order=None):
    order = list(order if order is not None else sorted(G.nodes()))
    return nx.to_numpy_array(G, nodelist=order, weight=None)


def trans(A):
    """P = D^-1 A (row i = the odds of leaving i; every row sums to 1)."""
    return A / A.sum(axis=1, keepdims=True)


def stationary(A):
    k = A.sum(axis=1)
    return k / k.sum()


def spectrum(P):
    """Eigenvalues of P, descending, real (P is similar to a symmetric matrix)."""
    w = np.linalg.eigvals(P)
    assert np.allclose(w.imag, 0, atol=1e-9)
    return np.sort(w.real)[::-1]


def eigsystem(A):
    """lam (descending), R (right eigenvectors, columns), L (left eigenvectors, columns), each
    scaled so that L[:,k] . R[:,k] = 1.  Right vector k is the left vector k rescaled by degree."""
    P = trans(A)
    k = A.sum(axis=1)
    S = np.diag(k ** 0.5) @ P @ np.diag(k ** -0.5)       # symmetric, same eigenvalues as P
    S = (S + S.T) / 2
    w, V = np.linalg.eigh(S)
    o = np.argsort(-w)
    w, V = w[o], V[:, o]
    R = np.diag(k ** -0.5) @ V                           # P R = R diag(w)
    L = np.diag(k ** 0.5) @ V                            # L^T P = diag(w) L^T
    return w, R, L


def dist1(x, pi):
    """The distance of the lecture note: the 1-norm."""
    return np.abs(x - pi).sum(axis=-1)


def worst_dist(P, pi, ts):
    """max over the starting node of || e_i P^t - pi ||_1, for each t in ts."""
    out, Pt, t0 = [], np.eye(len(P)), 0
    for t in ts:
        Pt = Pt @ np.linalg.matrix_power(P, t - t0)
        t0 = t
        out.append(dist1(Pt, pi).max())
    return np.array(out)


def dist_by_start(P, pi, ts):
    """array [start, t] of || e_i P^t - pi ||_1."""
    out, Pt, t0 = [], np.eye(len(P)), 0
    for t in ts:
        Pt = Pt @ np.linalg.matrix_power(P, t - t0)
        t0 = t
        out.append(dist1(Pt, pi))
    return np.array(out).T


def mixing_time(P, pi, eps, tmax=100000):
    t, Pt = 0, np.eye(len(P))
    while dist1(Pt, pi).max() > eps:
        Pt = Pt @ P
        t += 1
        assert t < tmax
    return t


def walk(P, start, steps, rng):
    """one path of `steps` moves; returns the visited nodes (steps + 1 of them)."""
    n = len(P)
    cum = np.cumsum(P, axis=1)
    path = [start]
    u = rng.random(steps)
    for r in u:
        path.append(int(np.searchsorted(cum[path[-1]], r)))
    return np.array(path)


def visit_share(P, start, steps, rng):
    path = walk(P, start, steps, rng)
    return np.bincount(path, minlength=len(P)) / len(path)


# --------------------------------------------------------------------------- the 12-node "two communities" network
# Nodes 0-5 (community 1) and 6-11 (community 2): two 6-cliques, each missing one edge (0-3, 7-10),
# joined by two bridges 2-8 and 5-11.  30 edges.  This is the motif of the whole lecture and of Part 3.
def two_communities():
    G = nx.Graph()
    for c in (range(0, 6), range(6, 12)):
        G.add_edges_from((a, b) for a in c for b in c if a < b)
    G.remove_edges_from([(0, 3), (7, 10)])
    G.add_edges_from([(2, 8), (5, 11)])
    return G


TWO12 = two_communities()
A12 = adj(TWO12, range(12))
P12 = trans(A12)
PI12 = stationary(A12)
LAM12 = spectrum(P12)
COMM12 = np.array([0] * 6 + [1] * 6)               # 0 = community 1 (cool), 1 = community 2 (hot)

# grid layout (y up): two flat-top hexagons, community 1 on the left and community 2 on the right. The removed
# edges 0-3 and 7-10 are long diagonals, the bridge ends 2, 5 (left) and 8, 11 (right) face each other, so the
# bridges 2-8 and 5-11 are two parallel horizontal lines that touch no other node.
def _hexagon(cx, order):
    import math
    return {n: (round(cx + 1.7 * math.cos(math.radians(a)), 2), round(2.0 + 1.7 * math.sin(math.radians(a)), 2))
            for n, a in order.items()}


TWO12_XY = {**_hexagon(1.5, {2: 60, 1: 120, 0: 180, 4: 240, 5: 300, 3: 0}),
            **_hexagon(7.5, {6: 60, 8: 120, 10: 180, 11: 240, 9: 300, 7: 0})}
# (the layout is a first draft: a figure may move nodes, but the graph is TWO12)


# --------------------------------------------------------------------------- the karate club
KARATE = nx.karate_club_graph()
AK = adj(KARATE, range(34))
PK = trans(AK)
PIK = stationary(AK)
LAMK = spectrum(PK)


# --------------------------------------------------------------------------- the 4-node diamond (Pen & Paper Part 2)
# degrees 2, 2, 3, 3: nodes 0 and 1 are not joined to each other; node 2 and 3 are joined to everything.
DIAMOND = nx.Graph([(0, 2), (0, 3), (1, 2), (1, 3), (2, 3)])
AD = adj(DIAMOND, range(4))
PD = trans(AD)
PID = stationary(AD)
LAMD = spectrum(PD)
DIAMOND_XY = {0: (0.0, 1.6), 1: (3.0, 1.6), 2: (1.5, 3.0), 3: (1.5, 0.2)}
# the sheet's initial distribution and its eigen-expansion (left eigenvectors psi, unnormalised as on the sheet)
PSI = np.array([[0.2, 0.2, 0.3, 0.3], [-1, 1, 0, 0], [0, 0, -1, 1], [1, 1, -1, -1]], dtype=float)
LAM_PSI = np.array([1.0, 0.0, -1 / 3, -2 / 3])
X0D = PSI[0] - 0.5 * PSI[1] + 0.0 * PSI[2] + 0.3 * PSI[3]      # = (0.5, 0.5, 0, 0) ... see check()


# --------------------------------------------------------------------------- cliques (mixing-time questions)
CLIQUE10 = nx.complete_graph(10)
AC10 = adj(CLIQUE10, range(10))
PC10 = trans(AC10)
PIC10 = stationary(AC10)
LAMC10 = spectrum(PC10)


def two_cliques():
    G = nx.Graph()
    for c in (range(0, 5), range(5, 10)):
        G.add_edges_from((a, b) for a in c for b in c if a < b)
    G.add_edge(4, 5)
    return G


TWOC = two_cliques()
ATC = adj(TWOC, range(10))
PTC = trans(ATC)
PITC = stationary(ATC)
LAMTC = spectrum(PTC)


# --------------------------------------------------------------------------- the 7-node rule picture and the averaging picture
# A walker on a node with four neighbours (the rule), and the "no eigenvalue above 1" frames.
RULE = nx.Graph([(0, 1), (0, 2), (0, 3), (0, 4), (1, 2), (3, 4), (4, 5), (5, 6), (2, 6)])
RULE_XY = {0: (3.0, 2.0), 1: (1.6, 3.4), 2: (1.0, 1.6), 3: (4.4, 3.2), 4: (4.5, 0.8), 5: (3.0, -0.3), 6: (1.2, -0.2)}
AVG_VALUES = [9, 2, 4, 3, 7, 1, 5]           # frame 1: the largest is 9 (node 0)


def spectral_gap_table():
    """(name, lambda2, tau) for the gauge slide."""
    rows = [("10-clique", LAMC10[1]), ("karate club", LAMK[1]), ("two communities", LAM12[1]),
            ("two 5-cliques + bridge", LAMTC[1])]
    out = [(n, l, 1 / (1 - l)) for n, l in rows]
    # a ring of 1,000 nodes: lambda2 = cos(2 pi / 1000)
    l = float(np.cos(2 * np.pi / 1000))
    out.append(("ring of 1,000", l, 1 / (1 - l)))
    return out


# --------------------------------------------------------------------------- the distance threshold
EPS = 0.25          # "close enough": ||x(t) - pi||_1 <= EPS, for every starting node
TMIX12, TMIXK, TMIXC10, TMIXTC = 13, 15, 1, 20      # mixing times at EPS (asserted in check)


# --------------------------------------------------------------------------- the numbers the slides state
def check():
    # transition matrices: every row sums to 1, pi P = pi, detailed balance
    for P, pi in ((P12, PI12), (PK, PIK), (PD, PID), (PC10, PIC10), (PTC, PITC)):
        assert np.allclose(P.sum(axis=1), 1)
        assert np.allclose(pi @ P, pi) and np.isclose(pi.sum(), 1)
        assert np.allclose(pi[:, None] * P, (pi[:, None] * P).T), "detailed balance"
    # the largest eigenvalue is 1 and no eigenvalue exceeds it
    for lam in (LAM12, LAMK, LAMD, LAMC10, LAMTC):
        assert np.isclose(lam[0], 1) and np.all(np.abs(lam) <= 1 + 1e-9)

    # --- the 12-node network
    assert TWO12.number_of_edges() == 30 and A12.sum() == 60
    assert list(A12.sum(axis=1).astype(int)) == [4, 5, 6, 4, 5, 6, 5, 4, 6, 5, 4, 6]
    assert np.allclose(LAM12, [1, 0.889, 0, 0, 0, -0.088, -0.2, -0.2, -0.266, -0.333, -0.379, -0.423], atol=6e-4)
    tau12 = 1 / (1 - LAM12[1])
    assert abs(tau12 - 9.0) < 0.05, tau12
    # community probability from node 0: 1, 1, .92, .88, .80, .67, .55, .505 at t = 0, 1, 2, 3, 5, 10, 20, 40
    ts = [0, 1, 2, 3, 5, 10, 20, 40]
    got = [np.linalg.matrix_power(P12, t)[0, :6].sum() for t in ts]
    assert np.allclose(got, [1, 1, 0.92, 0.88, 0.80, 0.67, 0.55, 0.505], atol=0.006), np.round(got, 3)
    # the second eigenvector separates the communities by sign
    w, R, L = eigsystem(A12)
    r2 = R[:, 1] / np.abs(R[:, 1]).max()
    if r2[0] < 0:
        r2 = -r2
    assert np.all(r2[:6] > 0.5) and np.all(r2[6:] < -0.5), np.round(r2, 2)
    assert np.allclose(np.abs(r2)[[2, 5, 8, 11]], 0.74, atol=0.01)       # the bridge ends sit closest to 0
    assert np.allclose(np.abs(r2)[[0, 1, 3, 4, 6, 7, 9, 10]], [.98, 1, .98, 1, 1, .98, 1, .98], atol=0.01)

    # --- karate club
    assert KARATE.number_of_nodes() == 34 and KARATE.number_of_edges() == 78 and AK.sum() == 156
    assert abs(LAMK[1] - 0.868) < 0.001 and abs(1 / (1 - LAMK[1]) - 7.6) < 0.1
    # k / share = 2m for every node at stationarity
    assert np.allclose(AK.sum(axis=1) / PIK, 156)

    # --- the diamond
    assert sorted(AD.sum(axis=1)) == [2, 2, 3, 3]
    assert np.allclose(LAMD, [1, 0, -1 / 3, -2 / 3], atol=1e-9)
    for k in range(4):                                   # PSI rows are left eigenvectors of PD
        assert np.allclose(PSI[k] @ PD, LAM_PSI[k] * PSI[k]), k
    x1 = X0D @ PD
    x2 = x1 @ PD
    assert np.allclose(x1, [0, 0, .5, .5]) and np.allclose(x2, [1 / 3, 1 / 3, 1 / 6, 1 / 6]), (x1, x2)
    assert np.allclose(X0D, [1, 0, 0, 0])                 # the sheet starts the walker on node 0
    # the expansion at t = 2:  pi - 0.5 * 0^2 psi_2 + 0 + 0.3 (-2/3)^2 psi_4
    xt = lambda t: PSI[0] - 0.5 * LAM_PSI[1] ** t * PSI[1] + 0.3 * LAM_PSI[3] ** t * PSI[3]
    assert np.allclose(xt(2), x2) and np.allclose(xt(1), x1)

    # --- cliques
    assert CLIQUE10.number_of_edges() == 45 and abs(LAMC10[1] + 1 / 9) < 1e-9
    assert TWOC.number_of_edges() == 21 and abs(LAMTC[1] - 0.927) < 0.001
    assert abs(1 / (1 - LAMTC[1]) - 13.7) < 0.1 and 1 / (1 - LAMC10[1]) < 1
    # mixing times at EPS: the clique takes 1 step, the bridged cliques 20 ("about 20 times longer")
    assert [mixing_time(P, pi, EPS) for P, pi in ((P12, PI12), (PK, PIK), (PC10, PIC10), (PTC, PITC))] == \
        [TMIX12, TMIXK, TMIXC10, TMIXTC]
    return True


def main():
    check()
    print("two12 degrees", list(A12.sum(axis=1).astype(int)))
    print("two12 lambda", np.round(LAM12, 3), " tau", round(1 / (1 - LAM12[1]), 2))
    print("karate lambda2", round(LAMK[1], 3), " tau", round(1 / (1 - LAMK[1]), 2))
    print("diamond x0", X0D, " lambda", np.round(LAMD, 3))
    print("clique10 lambda2", round(LAMC10[1], 3), " two 5-cliques lambda2", round(LAMTC[1], 3))
    for e in (0.5,):
        print("t_mix (eps 0.5) two12", mixing_time(P12, PI12, e), " karate", mixing_time(PK, PIK, e),
              " clique10", mixing_time(PC10, PIC10, e), " two5", mixing_time(PTC, PITC, e))
    for r in spectral_gap_table():
        print("gap", r[0], round(r[1], 5), round(r[2], 1))
    print("OK")


if __name__ == "__main__":
    main()
