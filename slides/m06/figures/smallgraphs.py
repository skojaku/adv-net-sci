#!/usr/bin/env python3
"""Every small graph in the Module 06 deck (v2), with its layout and every number a slide quotes.

    python3 figures/smallgraphs.py        # prints every quoted number; exits non-zero if one is wrong

One module, so a figure, an animation and a stage cannot disagree about a graph or a value.
Distances, sums and betweenness are computed exactly (integers and Fractions). The
assertions at the bottom are the numbers the slides state; a figure imports the value
from here and never types it.

Layouts are in grid units (y up). A figure module scales them; the shape is decided here.

Quiz graphs come in pairs, a left and a right graph on one slide, and the right graph's
letters continue from the left graph's so that "E" names one node on the slide.
The pairs were chosen so that the node that looks central is not the answer:

    closeness     left  CA   the degree-5 hub E loses to the degree-2 bridge F (20 vs 19)
                  right CB   the hub N with a triangle loses to P with two long arms (18 vs 16)
    harmonic      left  CA   the same graph, and now the hub E wins (27/4 against F's 35/6)
                  right HD   two pieces: a 5-node star beats the middle of a 7-node path (4 vs 11/3)
    eccentricity  left  EA   a broom: E wins closeness, F wins eccentricity (2 against 3)
                  right EB   a pentagon: K wins closeness, the degree-2 L wins eccentricity
    betweenness   left  DB   a dumbbell: the bridge F (25) loses to both hubs (30)
                  right SQ   a fork and a square: O beats M by one half (9.5 vs 9)
"""

from fractions import Fraction as Fr
import itertools
import math
import sys

import networkx as nx
import numpy as np


# --------------------------------------------------------------------------- helpers
def graph(edges, nodes=None):
    G = nx.Graph()
    if nodes:
        G.add_nodes_from(nodes)
    G.add_edges_from(tuple(e.split("-")) for e in edges)
    return G


def dist(G, u):
    return nx.single_source_shortest_path_length(G, u)


def dsum(G):
    """Sum of distances to every other node; None if some node is unreachable."""
    n = G.number_of_nodes()
    out = {}
    for u in G:
        L = dist(G, u)
        out[u] = sum(L.values()) if len(L) == n else None
    return out


def closeness(G):
    n = G.number_of_nodes()
    return {u: (Fr(n - 1, s) if s else Fr(0)) for u, s in dsum(G).items()}


def harmonic(G):
    """Sum over the other nodes of 1/distance, an unreachable node adding 0 (the lecture note's form)."""
    return {u: sum((Fr(1, d) for v, d in dist(G, u).items() if v != u), Fr(0)) for u in G}


def eccentricity(G):
    n = G.number_of_nodes()
    out = {}
    for u in G:
        L = dist(G, u)
        out[u] = max(L.values()) if len(L) == n else math.inf
    return out


def betweenness(G):
    """Unnormalized, over unordered pairs s<t, exact: sum of sigma_st(i)/sigma_st."""
    nodes = sorted(G)
    b = {u: Fr(0) for u in nodes}
    for s, t in itertools.combinations(nodes, 2):
        if not nx.has_path(G, s, t):
            continue
        paths = list(nx.all_shortest_paths(G, s, t))
        for p in paths:
            for i in p[1:-1]:
                b[i] += Fr(1, len(paths))
    return b


def argbest(d, best=max):
    v = best(x for x in d.values() if x is not None)
    return sorted(k for k, x in d.items() if x == v), v


# --------------------------------------------------------------------------- closeness quiz
# Left: a hub with four leaves (E), a bridge (F), a small cluster (G, H, I, J) with a tail K.
CA = graph(["E-A", "E-B", "E-C", "E-D", "E-F", "F-G",
            "G-H", "G-I", "G-J", "H-I", "I-J", "J-K"])
# The hub E is drawn at the centre of the picture, with long spokes to its leaves, and the
# winner F sits off-centre: picking "the middle of the drawing" must not give the answer.
CA_XY = {"E": (2.6, 2.0), "A": (1.9, 3.5), "B": (0.0, 3.0), "C": (0.0, 1.0), "D": (1.9, 0.5),
         "F": (3.9, 2.0), "G": (5.0, 2.0), "H": (5.6, 2.9), "I": (6.2, 2.0), "J": (5.6, 1.1),
         "K": (6.2, 0.2)}

# Right: N carries a triangle (L, M) and a leaf O; P carries two long arms (Q-R-S, T-U).
CB = graph(["N-L", "N-M", "L-M", "N-O", "N-P", "P-Q", "Q-R", "R-S", "P-T", "T-U"])
CB_XY = {"N": (2.5, 2.0), "L": (1.1, 3.4), "M": (-0.2, 2.3), "O": (1.1, 0.5),
         "P": (3.6, 2.0), "Q": (4.3, 2.9), "R": (5.1, 3.5), "S": (5.9, 3.0),
         "T": (4.3, 1.1), "U": (5.2, 0.6)}

# The same left graph with the road E-F closed: two pieces.
CA_CUT = CA.copy()
CA_CUT.remove_edge("E", "F")

# --------------------------------------------------------------------------- harmonic quiz
# Right: two pieces. A star (centre N, leaves L M O P) and a path of seven (Q ... W).
HD = graph(["N-L", "N-M", "N-O", "N-P", "Q-R", "R-S", "S-T", "T-U", "U-V", "V-W"])
HD_XY = {"N": (1.6, 3.0), "L": (1.6, 4.5), "M": (0.1, 3.0), "O": (3.1, 3.0), "P": (1.6, 1.5),
         **{c: (0.0 + 1.0 * i, 0.3) for i, c in enumerate("QRSTUVW")}}

# --------------------------------------------------------------------------- eccentricity quiz
# Left: a broom. Hub E with leaves A-D and a tail F-G-H.
EA = graph(["E-A", "E-B", "E-C", "E-D", "E-F", "F-G", "G-H"])
# The hub E is drawn at the centre of the picture (long bristles); the eccentricity winner F
# sits off-centre, so "the middle of the drawing" is not the answer.
EA_XY = {"E": (1.3, 2.0), "A": (0.7, 3.6), "B": (-1.2, 3.1), "C": (-1.2, 0.9), "D": (0.7, 0.4),
         "F": (3.3, 2.0), "G": (4.1, 2.0), "H": (4.9, 2.0)}

# Right: a pentagon K-L-M-O-P. K carries leaves I, J; M carries the leaf N.
EB = graph(["K-I", "K-J", "K-L", "K-P", "L-M", "M-N", "M-O", "O-P"])
_pent = {c: (2.6 + 1.25 * math.cos(math.radians(a)), 1.9 + 1.25 * math.sin(math.radians(a)))
         for c, a in zip("KLMOP", (162, 90, 18, -54, -126))}
EB_XY = {**_pent, "I": (0.35, 3.0), "J": (0.15, 1.75), "N": (5.15, 2.85)}

# --------------------------------------------------------------------------- betweenness
# The first example: two triangles joined through D.
BT = graph(["A-B", "B-C", "A-C", "C-D", "D-E", "E-F", "F-G", "E-G"])
BT_XY = {"A": (0.0, 2.6), "B": (0.0, 0.6), "C": (1.3, 1.6), "D": (2.6, 1.6), "E": (3.9, 1.6),
         "F": (5.2, 2.6), "G": (5.2, 0.6)}

# Quiz left: a dumbbell. E with leaves A-D, the bridge F, G with leaves H-K.
DB = graph(["E-A", "E-B", "E-C", "E-D", "E-F", "F-G", "G-H", "G-I", "G-J", "G-K"])
DB_XY = {"E": (1.5, 2.0), "A": (1.5, 3.2), "B": (0.35, 2.6), "C": (0.35, 1.4), "D": (1.5, 0.8),
         "F": (2.9, 2.0), "G": (4.3, 2.0), "H": (4.3, 3.2), "I": (5.45, 2.6), "J": (5.45, 1.4),
         "K": (4.3, 0.8)}

# Quiz right: M forks to two leaves (L, N) and to O; O is a corner of the square O-P-R-Q.
SQ = graph(["L-M", "N-M", "M-O", "O-P", "O-Q", "P-R", "Q-R"])
# M (the loser, 9) is drawn at the centre of the picture; the winner O (19/2) is not.
SQ_XY = {"L": (-1.6, 3.4), "N": (-1.6, 0.6), "M": (1.0, 2.0), "O": (2.0, 2.0), "P": (2.7, 2.7),
         "Q": (2.7, 1.3), "R": (3.4, 2.0)}

# --------------------------------------------------------------------------- two ways to count
# Module 01's five-node graph (make_figures.py graph5, walk-power.js): the room has met it.
# u is node 1, v is node 4 there.
W5 = graph(["n0-u", "n0-n2", "u-n2", "u-n3", "n2-v", "n3-v"])
W5_XY = {"n0": (0.0, 1.0), "u": (1.0, 1.0), "n2": (0.0, 0.0), "n3": (1.0, 0.0), "v": (0.5, -0.9)}
W5_ORDER = ["n0", "u", "n2", "n3", "v"]


def walk_counts(G, order, s, t, kmax=5):
    A = nx.to_numpy_array(G, nodelist=order, dtype=int)
    i, j = order.index(s), order.index(t)
    out, P = [], np.eye(len(order), dtype=int)
    for _ in range(kmax):
        P = P @ A
        out.append(int(P[i, j]))
    return out


# --------------------------------------------------------------------------- eigenvector
# Seven nodes, no symmetry, seven distinct eigenvalues. A is the hub (degree 4); B has
# degree 2 and sits in two triangles with the top nodes; D has degree 3 but one of its
# neighbours is the leaf C. B ends above D: "known by the company you keep".
EIG = graph(["A-B", "A-D", "A-F", "A-G", "B-G", "C-D", "D-E", "E-F", "F-G"])
EIG_ORDER = list("ABCDEFG")
EIG_XY = {"A": (2.0, 1.6), "B": (1.0, 2.9), "G": (2.6, 3.1), "F": (3.6, 1.9), "E": (3.2, 0.4),
          "D": (1.6, 0.2), "C": (0.3, 0.6)}


def spectrum(G, order):
    A = nx.to_numpy_array(G, nodelist=order)
    w, V = np.linalg.eigh(A)
    V = V * np.where(V.sum(0) < 0, -1, 1)          # a sign convention, for drawing only
    return A, w, V


def power_trace(A, steps):
    """x_0 = 1, x_{t+1} = A x_t, each step rescaled so that the largest entry is 1."""
    x = np.ones(len(A))
    out = [x.copy()]
    for _ in range(steps):
        x = A @ x
        x = x / x.max()
        out.append(x.copy())
    return out


# --------------------------------------------------------------------------- eigenvector quiz
# Two candidates per side; only they carry letters. Left: M has three neighbours, two of them
# hubs; X has four, three of them leaves. Right: H has six neighbours, five of them leaves;
# K has three, all in a clique.
EQ_L = graph(["M-H1", "M-H2", "H1-H2", "H1-a", "H1-b", "H1-c", "H2-d", "H2-e", "H2-f",
              "M-X", "X-p", "X-q", "X-r"])
EQ_L_XY = {"H1": (1.6, 2.8), "H2": (1.6, 1.2), "M": (3.0, 2.0), "X": (4.4, 2.0),
           "a": (0.8, 3.5), "b": (0.1, 3.0), "c": (1.6, 3.7), "d": (0.8, 0.5), "e": (0.1, 1.0),
           "f": (1.6, 0.3), "p": (5.1, 2.9), "q": (5.6, 2.0), "r": (5.1, 1.1)}
EQ_R = graph(["H-a", "H-b", "H-c", "H-d", "H-e", "H-K1", "K1-K", "K1-K3", "K1-K4",
              "K-K3", "K-K4", "K3-K4"])
EQ_R_XY = {"H": (1.6, 2.0), "a": (0.6, 3.1), "b": (0.2, 2.0), "c": (0.6, 0.9), "d": (1.6, 3.3),
           "e": (1.6, 0.7), "K1": (3.0, 2.0), "K": (5.0, 3.4), "K4": (5.0, 0.6), "K3": (4.3, 2.0)}
EQ_LABELS = {"left": ["M", "X"], "right": ["H", "K"]}


def katz_q(G, frac=0.5):
    """Katz centrality (beta = 1) at alpha = frac / lambda_max of G, largest entry set to 1."""
    nodes = sorted(G)
    A = nx.to_numpy_array(G, nodelist=nodes)
    lam = np.linalg.eigvalsh(A)[-1]
    c = np.linalg.solve(np.eye(len(A)) - frac / lam * A, np.ones(len(A)))
    return dict(zip(nodes, c / c.max()))


def eigvec(G):
    """Eigenvector centrality with the largest entry set to 1."""
    nodes = sorted(G)
    A = nx.to_numpy_array(G, nodelist=nodes)
    w, V = np.linalg.eigh(A)
    v = np.abs(V[:, -1])
    return dict(zip(nodes, v / v.max()))


# --------------------------------------------------------------------------- clique ring
def clique_ring(sizes):
    """Cliques in a ring; clique k's second node is joined to clique k+1's first node."""
    G, off, ports = nx.Graph(), 0, []
    for s in sizes:
        nodes = list(range(off, off + s))
        G.add_edges_from(itertools.combinations(nodes, 2))
        ports.append((nodes[0], nodes[1]))
        off += s
    for k in range(len(sizes)):
        G.add_edge(ports[k][1], ports[(k + 1) % len(sizes)][0])
    return G


RING_SIZES = {K: (4, 4, 4, K) for K in (4, 5, 6, 7, 8)}
RING_KATZ = (4, 4, 4, 6)                 # the graph under the alpha slider


def eig_share(sizes):
    """Share of the total eigenvector-centrality score (the sum of the leading eigenvector's
    entries) that sits in the last clique. A share of the SQUARED entries would read higher
    (89% instead of 68% at K = 5) and is not what "share of the score" means."""
    G = clique_ring(sizes)
    A = nx.to_numpy_array(G, nodelist=sorted(G))
    w, V = np.linalg.eigh(A)
    v = np.abs(V[:, -1])
    big = range(sum(sizes[:-1]), sum(sizes))
    return float(sum(v[i] for i in big) / v.sum()), float(w[-1])


def katz(A, alpha, beta=1.0):
    return beta * np.linalg.solve(np.eye(len(A)) - alpha * A, np.ones(len(A)))


# --------------------------------------------------------------------------- directed
# HITS: A links out three times, E is linked to three times.
HITS_EDGES = [("A", "C"), ("A", "D"), ("A", "E"), ("B", "D"), ("B", "E"), ("F", "E"), ("C", "F")]
HITS_ORDER = list("ABCDEF")

# PageRank: five pages. A splits its vote three ways; C collects three links and hands
# everything to E; E hands everything back to A.
PR_EDGES = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "C"), ("D", "C"), ("C", "E"), ("E", "A")]
PR_ORDER = list("ABCDE")
PR_DEAD = [e for e in PR_EDGES if e != ("E", "A")]      # E becomes a dead end
PR_R = Fr(15, 100)


def adj_directed(edges, order):
    A = np.zeros((len(order), len(order)))
    for u, v in edges:
        A[order.index(u), order.index(v)] = 1
    return A


def hits(edges, order):
    A = adj_directed(edges, order)
    w, V = np.linalg.eigh(A.T @ A)
    a = np.abs(V[:, -1]); a /= a.max()
    w2, V2 = np.linalg.eigh(A @ A.T)
    h = np.abs(V2[:, -1]); h /= h.max()
    return dict(zip(order, h)), dict(zip(order, a))


def pagerank(edges, order, r=0.15, tele=None, steps=2000, dangling="uniform"):
    """c_i = (1-r) sum_j A_ji c_j / d_out_j + r t_i. A dead end hands its score to t ('uniform')
    or to nobody ('leak', the score drains away)."""
    n = len(order)
    A = adj_directed(edges, order)
    out = A.sum(1)
    t = np.ones(n) / n if tele is None else np.array([1.0 if v == tele else 0.0 for v in order])
    c = np.ones(n) / n
    trace = [c.copy()]
    for _ in range(steps):
        new = np.zeros(n)
        for i in range(n):
            if out[i]:
                new += (1 - r) * c[i] * A[i] / out[i]
            elif dangling == "uniform":
                new += (1 - r) * c[i] * t
        new += r * t * (c.sum() if dangling == "leak" else 1.0)
        c = new
        trace.append(c.copy())
    return dict(zip(order, c)), trace


# =========================================================================== numbers
def compute():
    N = {}
    N["CA_sum"] = dsum(CA)
    N["CB_sum"] = dsum(CB)
    N["CA_harm"] = harmonic(CA)
    N["HD_harm"] = harmonic(HD)
    N["CA_cut_close"] = closeness(CA_CUT)
    N["CA_cut_harm"] = harmonic(CA_CUT)
    N["EA_sum"], N["EA_ecc"] = dsum(EA), eccentricity(EA)
    N["EB_sum"], N["EB_ecc"] = dsum(EB), eccentricity(EB)
    N["BT_btw"] = betweenness(BT)
    N["DB_btw"] = betweenness(DB)
    N["SQ_btw"] = betweenness(SQ)
    N["W5_dist"] = dist(W5, "u")["v"]
    N["W5_walks"] = walk_counts(W5, W5_ORDER, "u", "v")
    A, w, V = spectrum(EIG, EIG_ORDER)
    N["EIG_w"], N["EIG_V"] = w, V
    v = V[:, -1] / V[:, -1].max()
    N["EIG_v"] = dict(zip(EIG_ORDER, v))
    N["EIG_trace"] = power_trace(A, 30)
    N["RING"] = {K: eig_share(s) for K, s in RING_SIZES.items()}
    N["EQ"] = {"left": eigvec(EQ_L), "right": eigvec(EQ_R)}
    N["KQ"] = {"left": katz_q(EQ_L), "right": katz_q(EQ_R)}
    Gk = clique_ring(RING_KATZ)
    Ak = nx.to_numpy_array(Gk, nodelist=sorted(Gk))
    lam = np.linalg.eigvalsh(Ak)[-1]
    N["KATZ_lam"] = lam
    N["HITS"] = hits(HITS_EDGES, HITS_ORDER)
    N["PR_plain"], _ = pagerank(PR_EDGES, PR_ORDER, r=0.0)
    N["PR"], _ = pagerank(PR_EDGES, PR_ORDER, r=float(PR_R))
    N["PR_leak"], N["PR_leak_trace"] = pagerank(PR_DEAD, PR_ORDER, r=0.0, dangling="leak", steps=12)
    N["PR_dead"], _ = pagerank(PR_DEAD, PR_ORDER, r=float(PR_R))
    N["PPR_A"], _ = pagerank(PR_EDGES, PR_ORDER, r=float(PR_R), tele="A")
    # On the dead-end graph a dangling page jumps to the teleport target, which for the
    # personalized walk is A -- exactly what E's lost link did. Same scores.
    N["PPR_A_dead"], _ = pagerank(PR_DEAD, PR_ORDER, r=float(PR_R), tele="A")
    return N


def check(N):
    # --- closeness quiz
    assert argbest(N["CA_sum"], min) == (["F"], 19)
    assert N["CA_sum"]["E"] == N["CA_sum"]["G"] == 20
    assert dict(CA.degree)["E"] == 5 and dict(CA.degree)["F"] == 2
    assert argbest(N["CB_sum"], min) == (["P"], 16) and N["CB_sum"]["N"] == 18
    assert dict(CB.degree)["N"] == 4 and dict(CB.degree)["P"] == 3
    # --- the cut: every closeness is 0, harmonic still ranks
    assert set(N["CA_cut_close"].values()) == {0}
    # --- harmonic quiz
    assert argbest(N["CA_harm"]) == (["E"], Fr(27, 4))
    assert N["CA_harm"]["G"] == Fr(19, 3) and N["CA_harm"]["F"] == Fr(35, 6)
    assert argbest(N["HD_harm"]) == (["N"], Fr(4))
    assert N["HD_harm"]["T"] == Fr(11, 3)
    # --- eccentricity quiz
    assert argbest(N["EA_sum"], min) == (["E"], 10) and argbest(N["EA_ecc"], min) == (["F"], 2)
    assert N["EA_ecc"]["E"] == 3
    assert argbest(N["EB_sum"], min) == (["K"], 11) and argbest(N["EB_ecc"], min) == (["L"], 2)
    assert N["EB_sum"]["L"] == 12 and N["EB_ecc"]["K"] == 3 and dict(EB.degree)["L"] == 2
    # --- betweenness
    assert argbest(N["BT_btw"]) == (["D"], 9) and N["BT_btw"]["C"] == N["BT_btw"]["E"] == 8
    assert argbest(N["DB_btw"]) == (["E", "G"], 30) and N["DB_btw"]["F"] == 25
    assert argbest(N["SQ_btw"]) == (["O"], Fr(19, 2)) and N["SQ_btw"]["M"] == 9
    assert dict(SQ.degree)["O"] == dict(SQ.degree)["M"] == 3
    # --- two ways to count
    assert N["W5_dist"] == 2 and N["W5_walks"][:4] == [0, 2, 1, 11]
    # --- eigenvector
    w = N["EIG_w"]
    assert np.min(np.diff(w)) > 0.12, "eigenvalues must be distinct"
    assert sum(1 for k in range(7) if np.all(N["EIG_V"][:, k] > 0)) == 1, \
        "exactly one eigenvector is all positive"
    assert np.all(N["EIG_V"][:, -1] > 0)
    v = N["EIG_v"]
    assert max(v, key=v.get) == "A"
    assert v["B"] > v["D"] and dict(EIG.degree)["B"] == 2 and dict(EIG.degree)["D"] == 3
    deg1 = N["EIG_trace"][1] * 4                       # step one is degree (scaled by max = 4)
    assert np.allclose(deg1, [dict(EIG.degree)[c] for c in EIG_ORDER])
    assert np.allclose(N["EIG_trace"][-1], list(v.values()), atol=1e-3)
    # --- localization
    assert abs(N["RING"][4][0] - 0.25) < 1e-9
    assert [round(N["RING"][K][0], 2) for K in (5, 6, 7, 8)] == [0.68, 0.85, 0.91, 0.94]
    # --- eigenvector quiz: in both networks the node with fewer neighbours scores higher
    ev = N["EQ"]
    assert ev["left"]["M"] > ev["left"]["X"] and dict(EQ_L.degree)["M"] < dict(EQ_L.degree)["X"]
    assert ev["right"]["K"] > ev["right"]["H"] and dict(EQ_R.degree)["K"] < dict(EQ_R.degree)["H"]
    assert [round(ev[s][n], 2) for s, n in (("left", "M"), ("left", "X"), ("right", "K"), ("right", "H"))] \
        == [0.85, 0.46, 0.85, 0.62]
    # --- Katz quiz (same graphs, alpha = 0.5 / lambda_max): left agrees with the eigenvector
    #     (M above X), right agrees with degree (H above K)
    kq = N["KQ"]
    assert kq["left"]["M"] > kq["left"]["X"] and kq["right"]["H"] > kq["right"]["K"]
    assert [round(kq[s][n], 2) for s, n in (("left", "M"), ("left", "X"), ("right", "H"), ("right", "K"))] \
        == [0.87, 0.81, 1.0, 0.81]
    # --- the quiz drawings: the drawn middle is never the answer
    for xy, middle, winner in ((EA_XY, "E", "F"), (SQ_XY, "M", "O")):
        xs, ys = [p[0] for p in xy.values()], [p[1] for p in xy.values()]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        near = min(xy, key=lambda n: (xy[n][0] - cx) ** 2 + (xy[n][1] - cy) ** 2)
        assert near == middle != winner, (near, middle, winner)
    # --- HITS
    h, a = N["HITS"]
    assert max(h, key=h.get) == "A" and max(a, key=a.get) == "E"
    # --- PageRank
    p = N["PR_plain"]
    assert abs(p["A"] - 3 / 11) < 1e-6 and abs(p["C"] - 3 / 11) < 1e-6 and abs(p["E"] - 3 / 11) < 1e-6
    assert abs(p["B"] - 1 / 11) < 1e-6
    assert max(N["PR"], key=N["PR"].get) == "C"
    assert sum(N["PR_leak"].values()) < 0.2              # the score drains through the dead end
    assert abs(sum(N["PR_dead"].values()) - 1) < 1e-9
    assert max(N["PPR_A"], key=N["PPR_A"].get) == "A"
    assert all(abs(N["PPR_A"][k] - N["PPR_A_dead"][k]) < 1e-9 for k in PR_ORDER)
    assert max(N["PR_dead"], key=N["PR_dead"].get) == "E"


def show(N):
    f = lambda d: ", ".join(f"{k} {x}" for k, x in sorted(d.items(), key=lambda kv: str(kv[0])))
    print("closeness quiz  left  sum of distances:", f(N["CA_sum"]))
    print("                right sum of distances:", f(N["CB_sum"]))
    print("cut             closeness:", set(N["CA_cut_close"].values()), " harmonic:", f(N["CA_cut_harm"]))
    print("harmonic quiz   left :", f(N["CA_harm"]))
    print("                right:", f(N["HD_harm"]))
    print("ecc quiz        left  sum:", f(N["EA_sum"]), "\n                      ecc:", f(N["EA_ecc"]))
    print("                right sum:", f(N["EB_sum"]), "\n                      ecc:", f(N["EB_ecc"]))
    print("betweenness     first:", f(N["BT_btw"]))
    print("                left :", f(N["DB_btw"]))
    print("                right:", f(N["SQ_btw"]))
    print("two ways        d(u,v) =", N["W5_dist"], " walks u->v of length 1..5:", N["W5_walks"])
    print("eigenvalues    ", np.round(N["EIG_w"], 3))
    print("eigvec (max 1) ", {k: round(x, 3) for k, x in N["EIG_v"].items()})
    for t in (0, 1, 2, 3, 5, 10, 30):
        print(f"  power step {t:2d}", np.round(N["EIG_trace"][t], 3))
    for K, (s, lam) in N["RING"].items():
        print(f"ring 4,4,4,{K}: lambda_max {lam:.3f}, share of the eigenvector score in the big clique {s:.3f}")
    print("eigenvector quiz left ", {k: round(v, 2) for k, v in N["EQ"]["left"].items()})
    print("eigenvector quiz right", {k: round(v, 2) for k, v in N["EQ"]["right"].items()})
    print("katz quiz left ", {k: round(v, 2) for k, v in N["KQ"]["left"].items()})
    print("katz quiz right", {k: round(v, 2) for k, v in N["KQ"]["right"].items()})
    print("katz ring", RING_KATZ, "lambda_max", round(N["KATZ_lam"], 4), "1/lambda_max", round(1 / N["KATZ_lam"], 4))
    h, a = N["HITS"]
    print("HITS hub ", {k: round(x, 2) for k, x in h.items()})
    print("HITS auth", {k: round(x, 2) for k, x in a.items()})
    for key in ("PR_plain", "PR", "PR_dead", "PPR_A"):
        print(f"{key:9s}", {k: round(x, 3) for k, x in N[key].items()})
    print("PR_leak total by step", [round(c.sum(), 3) for c in N["PR_leak_trace"]])


if __name__ == "__main__":
    N = compute()
    show(N)
    check(N)
    print("all assertions pass")
