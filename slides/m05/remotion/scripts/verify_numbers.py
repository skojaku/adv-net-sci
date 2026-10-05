# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["networkx", "numpy", "scikit-learn", "scipy"]
# ///
"""Every number quoted in DECK_SPEC.md, recomputed and asserted.

    uv run slides/m05/remotion/scripts/verify_numbers.py

The Remotion deck's data generator must reproduce these values; until it exists, this
script is the check on the spec. The Louvain-dependent lines (section 3 and 4) depend on
the networkx version, which is printed at the top.
"""

import math

import networkx as nx
import numpy as np
from sklearn.metrics import adjusted_rand_score as ARI
from sklearn.metrics import normalized_mutual_info_score as NMI
from sklearn.metrics import rand_score as RAND


def Q(g, parts):
    """Unweighted modularity. nx.karate_club_graph() carries edge weights and
    nx.community.modularity() uses them by default, which gives 0.434 / 0.432 / 0.445
    where the deck says 0.407 / 0.402 / 0.420."""
    return nx.community.modularity(g, parts, weight=None)


def near(x, y, tol=5e-4):
    assert abs(x - y) <= tol, (x, y)


def H(lbl):
    _, c = np.unique(lbl, return_counts=True)
    p = c / c.sum()
    return float(-(p * np.log2(p)).sum())


def MI(x, y):
    n = len(x)
    s = 0.0
    for a in set(x):
        for b in set(y):
            pij = sum(1 for i in range(n) if x[i] == a and y[i] == b) / n
            if pij > 0:
                s += pij * math.log2(pij / ((x.count(a) / n) * (y.count(b) / n)))
    return s


print("networkx", nx.__version__)

# ---------------------------------------------------------------- 1. ring of triangles
# triangle i = (3i, 3i+1, 3i+2); one edge joins node 3i+1 to node 3(i+1). m = 4n.
def ring(n):
    g = nx.Graph()
    for i in range(n):
        a, b, c = 3 * i, 3 * i + 1, 3 * i + 2
        g.add_edges_from([(a, b), (b, c), (a, c), (b, 3 * ((i + 1) % n))])
    return g


for n, apart, pairs in [(4, 0.500, 0.375), (8, 0.625, 0.625), (10, 0.650, 0.675), (16, 0.6875, 0.750)]:
    g = ring(n)
    tri = [{3 * i, 3 * i + 1, 3 * i + 2} for i in range(n)]
    duo = [tri[i] | tri[i + 1] for i in range(0, n, 2)]
    near(Q(g, tri), apart)
    near(Q(g, duo), pairs)
    near(Q(g, tri), 0.75 - 1 / n)
    near(Q(g, duo), 0.875 - 2 / n)
    assert g.number_of_edges() == 4 * n
    # a triangle has degrees 3, 3, 2: volume 8. Expected edges between two neighbors:
    assert sum(d for _, d in g.degree([0, 1, 2])) == 8
    near(8 * 8 / (2 * g.number_of_edges()), 8 / n)
print("1 ring: apart 3/4-1/n, pairs 7/8-2/n, tie at n=8, expected edges between neighbors 8/n")

# ---------------------------------------------------------------- 2. eight-node example
t = [0, 0, 0, 0, 1, 1, 1, 1]           # true: nodes 1-4 blue, 5-8 red
f = [0, 0, 0, 0, 0, 1, 1, 1]           # found: A = nodes 1-5, B = nodes 6-8
assert RAND(t, f) * 28 == 21
near(RAND(t, f), 0.75)
near(ARI(t, f), 0.4948)
near(NMI(t, f), 0.5616)
near(H(t), 1.000)
near(H(f), 0.954)
near(MI(t, f), 0.549)
near(H(t) - MI(t, f), 0.451)                                  # H(true | found)
near(2 * MI(t, f) / (H(t) + H(f)), 0.5616)
# pair table: both together 9, true-only 3, found-only 4, both apart 12
pairs = [(i, j) for i in range(8) for j in range(i + 1, 8)]
both = sum(t[i] == t[j] and f[i] == f[j] for i, j in pairs)
t_only = sum(t[i] == t[j] and f[i] != f[j] for i, j in pairs)
f_only = sum(t[i] != t[j] and f[i] == f[j] for i, j in pairs)
apart = sum(t[i] != t[j] and f[i] != f[j] for i, j in pairs)
assert (both, t_only, f_only, apart) == (9, 3, 4, 12)
# expected Rand under shuffling: 12 true-together pairs, 13 found-together pairs
ea = 12 * 13 / 28
e_rand = (28 + 2 * ea - 12 - 13) / 28
near(e_rand, 0.505)
near((0.75 - e_rand) / (1 - e_rand), ARI(t, f))
# the entropy of the picked node's true group, given each found group
near(H([0, 0, 0, 0, 1]), 0.722)                              # inside A: 4 blue, 1 red
# everyone alone
s = list(range(8))
near(RAND(t, s), 16 / 28)
near(NMI(t, s), 0.500)
near(ARI(t, s), 0.000)
print("2 eight nodes: Rand 21/28=0.75, ARI 0.495, NMI 0.562, H 1.000/0.954, I 0.549; singletons 0.571/0.500/0.000")

# ---------------------------------------------------------------- 3. shuffle of 30 dots
x = np.repeat(np.arange(5), 6)
assert 5 * math.comb(6, 2) == 75 and math.comb(30, 2) == 435 and 435 - 75 == 360
rng = np.random.default_rng(0)
R, A, N = [], [], []
for _ in range(2000):
    y = rng.permutation(x)
    R.append(RAND(x, y)); A.append(ARI(x, y)); N.append(NMI(x, y))
near(np.mean(R), 0.714, 2e-3)
near(np.mean(A), 0.000, 5e-3)
near(np.mean(N), 0.215, 3e-3)
ea = 75 * 75 / 435
near((435 + 2 * ea - 150) / 435, 0.7146, 5e-4)               # expected Rand
print("3 shuffle (seed 0, 2000): Rand %.3f  ARI %.3f  NMI %.3f" % (np.mean(R), np.mean(A), np.mean(N)))

# ---------------------------------------------------------------- 4. karate club
w = nx.karate_club_graph()
g = nx.Graph()
g.add_nodes_from(range(34))
g.add_edges_from(w.edges())
assert g.number_of_nodes() == 34 and g.number_of_edges() == 78
real = [0 if w.nodes[v]["club"] == "Mr. Hi" else 1 for v in w]
assert real.count(0) == 17 and real.count(1) == 17
FOUR = [[0, 1, 2, 3, 7, 11, 12, 13, 17, 19, 21], [4, 5, 6, 10, 16],
        [8, 9, 14, 15, 18, 20, 22, 30, 32, 33], [23, 24, 25, 26, 27, 28, 29, 31]]
THREE = [[0, 1, 2, 3, 7, 9, 11, 12, 13, 17, 19, 21], [4, 5, 6, 10, 16],
         [8, 14, 15, 18, 20, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33]]


def lab(parts):
    out = [0] * 34
    for i, p in enumerate(parts):
        for v in p:
            out[v] = i
    return out


near(Q(g, [{v for v in g if real[v] == k} for k in (0, 1)]), 0.358)   # the real split
near(Q(g, [set(p) for p in FOUR]), 0.407)
near(Q(g, [set(p) for p in THREE]), 0.402)
near(NMI(real, lab(FOUR)), 0.586); near(ARI(real, lab(FOUR)), 0.450)
near(NMI(real, lab(THREE)), 0.568); near(ARI(real, lab(THREE)), 0.591)
near(NMI(lab(FOUR), lab(THREE)), 0.768); near(ARI(lab(FOUR), lab(THREE)), 0.626)
# the grids: rows = real split (Mr. Hi, Officer), columns = found groups
grid = lambda P: [[sum(1 for v in grp if real[v] == r) for grp in P] for r in (0, 1)]
assert grid(FOUR) == [[11, 5, 1, 0], [0, 0, 9, 8]]
assert grid(THREE) == [[11, 5, 1], [1, 0, 16]]
# NMI prefers the four-group split, ARI prefers the three-group split
assert NMI(real, lab(FOUR)) > NMI(real, lab(THREE)) and ARI(real, lab(FOUR)) < ARI(real, lab(THREE))

res = {}
for seed in range(400):
    p = nx.community.louvain_communities(g, seed=seed, weight=None)
    key = tuple(sorted(tuple(sorted(c)) for c in p))
    res.setdefault(key, Q(g, p))
qs = sorted(res.values())
assert len(res) == 16, len(res)
near(qs[0], 0.385); near(qs[-1], 0.420)
print("4 karate: real-split Q 0.358; four 0.407 (NMI .586 ARI .450); three 0.402 (NMI .568 ARI .591);"
      " 400 Louvain seeds -> %d splits, Q %.3f to %.3f" % (len(res), qs[0], qs[-1]))

# ---------------------------------------------------------------- 5. noise
rq = []
for sd in range(200):
    r = nx.gnm_random_graph(34, 78, seed=sd)
    rq.append(max(Q(r, nx.community.louvain_communities(r, seed=k)) for k in range(5)))
rq = np.array(rq)
near(rq.mean(), 0.354, 2e-3); near(rq.min(), 0.305, 2e-3); near(rq.max(), 0.402, 2e-3)
assert (rq > 0.3).all() and rq.max() < 0.4198          # all above the rule of thumb, all below the club
r0 = nx.gnm_random_graph(34, 78, seed=0)
p0 = nx.community.louvain_communities(r0, seed=1)
assert len(p0) == 5
near(Q(r0, p0), 0.346)
big = []
for sd in range(100):
    r = nx.gnp_random_graph(100, 0.05, seed=sd)
    big.append(max(Q(r, nx.community.louvain_communities(r, seed=k)) for k in range(3)))
big = np.array(big)
near(big.mean(), 0.417, 2e-3); near(big.min(), 0.362, 2e-3); near(big.max(), 0.471, 2e-3)
sparse = []
for sd in range(200):
    r = nx.gnm_random_graph(40, 41, seed=sd)      # the size of last year's "Random Network Demo"
    sparse.append(max(Q(r, nx.community.louvain_communities(r, seed=k)) for k in range(5)))
sparse = np.array(sparse)
near(sparse.mean(), 0.592, 2e-3); near(sparse.min(), 0.465, 2e-3); near(sparse.max(), 0.681, 2e-3)
print("5 noise: G(34,78) Q mean %.3f (%.3f to %.3f, all > 0.3); seed 0: 5 groups, Q 0.346;"
      " G(100,0.05) mean %.3f (%.3f to %.3f); G(40,41) mean %.3f (%.3f to %.3f)"
      % (rq.mean(), rq.min(), rq.max(), big.mean(), big.min(), big.max(), sparse.mean(), sparse.min(), sparse.max()))

# ---------------------------------------------------------------- 6. SBM, 8 nodes (4 + 4)
# One uniform number per pair, fixed. An edge exists when u < p of the pair's block, so
# turning a probability up or down only adds or removes edges.
sp = [(a, b) for a in range(8) for b in range(a + 1, 8)]
inside = lambda a, b: (a < 4) == (b < 4)
u = np.random.default_rng(901).random(28)


def sample(p_in, p_out):
    return [(a, b) for (a, b), x in zip(sp, u) if x < (p_in if inside(a, b) else p_out)]


def graph(e):
    h = nx.Graph()
    h.add_nodes_from(range(8))
    h.add_edges_from(e)
    return h


TRUTH = [{0, 1, 2, 3}, {4, 5, 6, 7}]
e1, e2, e3 = sample(0.9, 0.1), sample(0.1, 0.9), sample(0.45, 0.45)
assert [len(e1), sum(inside(a, b) for a, b in e1)] == [12, 11]
assert [len(e2), sum(inside(a, b) for a, b in e2)] == [15, 1]
assert [len(e3), sum(inside(a, b) for a, b in e3)] == [12, 6]
near(Q(graph(e1), TRUTH), 0.413); near(Q(graph(e2), TRUTH), -0.436); near(Q(graph(e3), TRUTH), 0.000)
assert u[sp.index((0, 1))] < 0.9 and abs(u[sp.index((0, 1))] - 0.72) < 0.005       # nodes 1,2: edge
assert u[sp.index((0, 5))] >= 0.1 and abs(u[sp.index((0, 5))] - 0.59) < 0.005      # nodes 1,6: no edge


def loglik(h, c):
    tot = 0.0
    gs = sorted(set(c))
    for a in gs:
        for b in gs:
            if b < a:
                continue
            pr = [(i, j) for i in range(8) for j in range(i + 1, 8) if {c[i], c[j]} == {a, b}]
            if not pr:
                continue
            k = sum(1 for i, j in pr if h.has_edge(i, j))
            p = min(max(k / len(pr), 1e-6), 1 - 1e-6)
            tot += k * math.log(p) + (len(pr) - k) * math.log(1 - p)
    return tot


h1 = graph(e1)
cands = {"stripes": [0, 1, 0, 1, 0, 1, 0, 1], "one node moved": [0, 0, 0, 1, 1, 1, 1, 1],
         "two nodes moved": [0, 0, 0, 1, 1, 1, 0, 0], "all together": [0] * 8,
         "true": [0] * 4 + [1] * 4}
want = {"stripes": -17.5, "one node moved": -15.5, "two nodes moved": -18.4, "all together": -19.1, "true": -6.4}
for k, c in cands.items():
    near(loglik(h1, c), want[k], 0.06)
tc = cands["true"]
cnt = lambda lo, hi: sum(1 for a, b in e1 if (a < 4) == lo and (b < 4) == hi)
assert (cnt(True, True), cnt(False, False), len(e1) - cnt(True, True) - cnt(False, False)) == (5, 6, 1)
print("6 SBM seed 901: Q(true) 0.413 / -0.436 / 0.000; block counts 5/6, 6/6, 1/16;"
      " log-likelihoods true -6.4, one moved -15.5, stripes -17.5, two moved -18.4, all -19.1")


# ---------------------------------------------------------------- 7. the SBM score for every K (S29 to S31)
# best log L and a simple Bayesian score (uniform prior on each block probability, integrated out;
# P(K) = 1/8, P(c | K) uniform) over all 4140 groupings of the 8 nodes, by K
from math import lgamma, log, comb, factorial

def _partitions(n):
    def rec(i, m, cur):
        if i == n:
            yield tuple(cur)
            return
        for g in range(m + 1):
            cur.append(g)
            yield from rec(i + 1, max(m, g + 1), cur)
            cur.pop()
    yield from rec(0, 0, [])


_E = set(e1)


def _blocks(c):
    K = max(c) + 1
    m, nn = {}, {}
    for a, b in sp:
        r, s = sorted((c[a], c[b]))
        nn[(r, s)] = nn.get((r, s), 0) + 1
        m[(r, s)] = m.get((r, s), 0) + ((a, b) in _E)
    return m, nn


def _ll(c):
    m, nn = _blocks(c)
    return sum(m[k] * log(m[k] / nn[k]) + (nn[k] - m[k]) * log(1 - m[k] / nn[k]) for k in nn if 0 < m[k] < nn[k])


def _bayes(c):
    m, nn = _blocks(c)
    return sum(lgamma(m[k] + 1) + lgamma(nn[k] - m[k] + 1) - lgamma(nn[k] + 2) for k in nn)


def _s2(n, k):
    return sum((-1) ** (k - j) * comb(k, j) * j ** n for j in range(k + 1)) // factorial(k)


best_ll, best_b = {}, {}
for c in _partitions(8):
    K = max(c) + 1
    best_ll[K] = max(best_ll.get(K, -1e9), _ll(c))
    best_b[K] = max(best_b.get(K, -1e9), _bayes(c) - log(_s2(8, K)) - log(8))
assert len(best_ll) == 8
for K, want in zip(range(1, 9), [-19.121, -6.444, -3.014, -1.386, 0, 0, 0, 0]):
    near(best_ll[K], want, 2e-3)
for K, want in zip(range(1, 9), [-22.677, -18.213, -20.330, -21.850, -22.596, -22.912, -23.094, -21.488]):
    near(best_b[K], want, 2e-3)
assert all(best_ll[K + 1] >= best_ll[K] - 1e-12 for K in range(1, 8))          # log L never decreases with K
assert max(best_b, key=best_b.get) == 2                                          # the Bayesian score peaks at K = 2
print("7 SBM by K: best log L", [round(best_ll[K], 3) for K in range(1, 9)], "never decreases;",
      "Bayesian score peaks at K = 2:", [round(best_b[K], 2) for K in range(1, 9)])

print("\nall assertions passed")
