#!/usr/bin/env python3
"""Every number the Module 04 deck claims, computed from data before the spec is written.

Two arithmetic errors reached m01 slides *through* unverified specs, so nothing goes into
review/DECK_SPEC.md or onto a slide that has not printed here first.  `make_figures.py`
imports from this module rather than re-typing any value, so the deck, the spec and the
figures cannot drift apart.

    python3 figures/verify_numbers.py          # print the verified table, run every assertion

Data (downloaded into figures/data/, all public):
    ca-CondMat.txt.gz  SNAP, arXiv cond-mat coauthorship  -- the deck's real network
    as20000102.txt.gz  SNAP, Internet autonomous systems  -- technological
    bio-yeast.mtx      Network Repository, S. cerevisiae protein interactions -- biological
    ca-HepTh.txt.gz    SNAP, arXiv hep-th coauthorship    -- kept for reference only
"""

import gzip
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

import networkx as nx
import numpy as np

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"

# =========================================================================== Feld 1991
# Feld, Scott L. 1991. "Why Your Friends Have More Friends than You Do."
# American Journal of Sociology 96(6): 1464-1477.  Figure 1 / Table 1.
FELD_EDGES = [
    ("Betty", "Sue"),
    ("Sue", "Alice"), ("Sue", "Pam"), ("Sue", "Dale"),
    ("Alice", "Jane"), ("Alice", "Pam"), ("Alice", "Dale"),
    ("Jane", "Dale"),
    ("Pam", "Carol"),
    ("Carol", "Tina"),
]
FELD_ORDER = ["Betty", "Sue", "Alice", "Jane", "Pam", "Dale", "Carol", "Tina"]


def feld_graph():
    g = nx.Graph()
    g.add_nodes_from(FELD_ORDER)
    g.add_edges_from(FELD_EDGES)
    return g


def moments(g):
    """Exact (N, M, sum k, sum k^2, <k>, <k^2>, Var, <k^2>/<k>, gap) as Fractions."""
    ks = [g.degree(n) for n in g.nodes()]
    n = len(ks)
    k1 = Fraction(sum(ks), n)
    k2 = Fraction(sum(k * k for k in ks), n)
    var = k2 - k1 * k1
    return {"N": n, "M": g.number_of_edges(), "sum_k": sum(ks),
            "sum_k2": sum(k * k for k in ks), "k1": k1, "k2": k2,
            "var": var, "friend": k2 / k1, "gap": var / k1}


def friend_means(g):
    """node -> (degree, total degree of its friends, that total / degree)."""
    return {v: (g.degree(v), sum(g.degree(u) for u in g.neighbors(v)),
                Fraction(sum(g.degree(u) for u in g.neighbors(v)), g.degree(v))
                if g.degree(v) else None)
            for v in g.nodes()}


def check_feld(verbose=True):
    g, m, fm = feld_graph(), None, None
    m, fm = moments(g), friend_means(g)

    assert m["N"] == 8 and m["M"] == 10
    assert m["sum_k"] == 2 * m["M"] == 20
    assert [g.degree(v) for v in FELD_ORDER] == [1, 4, 4, 2, 3, 3, 2, 1]
    assert [fm[v][1] for v in FELD_ORDER] == [4, 11, 12, 7, 10, 10, 4, 2]
    assert m["sum_k2"] == 60 and m["k2"] == Fraction(15, 2) and m["k1"] == Fraction(5, 2)
    assert m["friend"] == 3 and m["var"] == Fraction(5, 4) and m["gap"] == Fraction(1, 2)
    assert m["k1"] + m["gap"] == m["friend"]
    # every node is counted once per friend, so the friend-degree totals sum to sum k^2
    assert sum(fm[v][1] for v in FELD_ORDER) == m["sum_k2"] == 60
    # Pam's neighbours are Carol, Sue and ALICE -- widely misquoted as Carol, Sue, Dale
    assert sorted(g.neighbors("Pam")) == ["Alice", "Carol", "Sue"]

    below = [v for v in FELD_ORDER if fm[v][2] > g.degree(v)]
    above = [v for v in FELD_ORDER if fm[v][2] < g.degree(v)]
    same = [v for v in FELD_ORDER if fm[v][2] == g.degree(v)]
    assert below == ["Betty", "Jane", "Pam", "Dale", "Tina"]
    assert above == ["Sue", "Alice"] and same == ["Carol"]

    per_person = sum(fm[v][2] for v in FELD_ORDER) / 8      # the OTHER average
    assert abs(float(per_person) - 2.9896) < 1e-4
    assert nx.check_planarity(g)[0]                          # F2: draw it with no crossings

    if verbose:
        print("--- Feld (1991) Figure 1, eight girls ------------------------------------")
        print(f"  N={m['N']}  M={m['M']}  sum k={m['sum_k']}=2M  sum k^2={m['sum_k2']}")
        print(f"  <k>={float(m['k1'])}   <k^2>={float(m['k2'])}   Var={float(m['var'])}")
        print(f"  <k^2>/<k> = {float(m['friend'])} = 60/20 ;  gap = Var/<k> = {float(m['gap'])}")
        print(f"  {float(m['k1'])} + {float(m['gap'])} = {float(m['friend'])}  [theorem checks]")
        print(f"  mean over PEOPLE of each friend-mean = {float(per_person):.4f}  (Feld: 2.99)")
        for v in FELD_ORDER:
            k, tot, mean = fm[v]
            rel = "below" if mean > k else ("above" if mean < k else "same ")
            print(f"    {v:6s} k={k}  friends' degrees sum={tot:2d}  mean={float(mean):.4f}  {rel}")
        print(f"  below {len(below)} / above {len(above)} / same {len(same)}   planar: True")
    return m, fm, float(per_person)


# =========================================================================== toy graphs
def check_toys(verbose=True):
    star, ring, comp = nx.star_graph(3), nx.cycle_graph(6), nx.complete_graph(5)
    ms, mr, mc = moments(star), moments(ring), moments(comp)
    assert ms["k1"] == Fraction(3, 2) and ms["friend"] == 2 and ms["gap"] == Fraction(1, 2)
    assert mr["var"] == 0 and mr["gap"] == 0 and mr["friend"] == mr["k1"] == 2
    assert mc["var"] == 0 and mc["gap"] == 0 and mc["k1"] == 4
    # handshaking lemma: no graph anywhere has an odd number of odd-degree nodes
    assert all(sum(1 for _, d in g.degree() if d % 2) % 2 == 0 for g in nx.graph_atlas_g())
    if verbose:
        print("\n--- worksheet graphs -----------------------------------------------------")
        print(f"  star, 4 nodes: <k>={float(ms['k1'])} <k^2>={float(ms['k2'])} "
              f"Var={float(ms['var'])} gap={float(ms['gap'])} friend={float(ms['friend'])}")
        print(f"  ring, 6 nodes: <k>={float(mr['k1'])} Var=0 gap=0 friend={float(mr['friend'])}")
        print(f"  K5:            <k>={float(mc['k1'])} Var=0 gap=0")
        print("  atlas 0..7 nodes: every graph has an EVEN number of odd-degree nodes")
    return ms, mr, mc


# =========================================================================== real networks
def _load_snap(name):
    g = nx.Graph()
    with gzip.open(DATA / name, "rt") as fh:
        for line in fh:
            if line.startswith("#"):
                continue
            a, b = line.split()[:2]
            if a != b:
                g.add_edge(int(a), int(b))
    return g


def _load_mtx(name):
    g = nx.Graph()
    for line in open(DATA / name):
        if line.startswith("%"):
            continue
        f = line.split()
        if len(f) < 2:
            continue
        try:
            a, b = int(f[0]), int(f[1])
        except ValueError:
            continue
        if a != b:
            g.add_edge(a, b)
    return g


@lru_cache(maxsize=None)
def condmat():
    """The deck's real network: arXiv cond-mat coauthorship (SNAP ca-CondMat).

    Chosen over ca-HepTh and ca-AstroPh, which the plan listed, on a measurement:
    over 10 <= k <= 200 the CCDF of ca-CondMat is straight to R^2 = 0.976, against
    0.920 (HepTh, whose tail stops at k=65) and 0.931 (AstroPh, which has a visible
    shoulder).  Part 5's slide claims "roughly a straight line" and has to be true.
    """
    return _load_snap("ca-CondMat.txt.gz")


@lru_cache(maxsize=None)
def internet_as():
    return _load_snap("as20000102.txt.gz")


@lru_cache(maxsize=None)
def yeast_ppi():
    return _load_mtx("bio-yeast.mtx")


def ccdf(degrees):
    """Empirical CCDF(k) = P(k' > k) at each distinct observed degree."""
    d = np.asarray(list(degrees))
    ks = np.array(sorted(set(d.tolist())))
    return ks, np.array([(d > k).mean() for k in ks])


def ccdf_fit(ks, surv, kmin, kmax):
    """(slope, intercept, R^2, n) of log10 CCDF against log10 k over [kmin, kmax]."""
    sel = (ks >= kmin) & (ks <= kmax) & (surv > 0)
    x, y = np.log10(ks[sel]), np.log10(surv[sel])
    a, b = np.polyfit(x, y, 1)
    resid = y - (a * x + b)
    return float(a), float(b), float(1 - np.var(resid) / np.var(y)), int(sel.sum())


def net_stats(g):
    d = np.array([x for _, x in g.degree()], float)
    k1, k2 = d.mean(), (d ** 2).mean()
    return {"N": g.number_of_nodes(), "M": g.number_of_edges(), "k1": k1, "k2": k2,
            "var": k2 - k1 * k1, "friend": k2 / k1, "gap": (k2 - k1 * k1) / k1,
            "kmax": int(d.max()), "degrees": d.astype(int)}


def paradox_share(g):
    """Fraction of nodes whose friends' MEAN degree strictly exceeds their own."""
    hit = [np.mean([g.degree(u) for u in g.neighbors(v)]) > g.degree(v)
           for v in g.nodes() if g.degree(v) > 0]
    return float(np.mean(hit))


def check_real(verbose=True):
    out = {}
    for label, g in (("cond-mat coauthorship", condmat()),
                     ("Internet AS graph", internet_as()),
                     ("yeast protein interactions", yeast_ppi())):
        s = net_stats(g)
        s["r"] = float(nx.degree_assortativity_coefficient(g))
        ks, su = ccdf(s["degrees"])
        s["ccdf"] = (ks, su)
        s["fit"] = ccdf_fit(ks, su, 10, 200) if s["kmax"] >= 200 else ccdf_fit(ks, su, 5, s["kmax"])
        out[label] = s
        if verbose:
            a, _, r2, n = s["fit"]
            print(f"\n--- {label} ---")
            print(f"  N={s['N']}  M={s['M']}  <k>={s['k1']:.4f}  <k^2>={s['k2']:.2f}  "
                  f"Var={s['var']:.2f}  max k={s['kmax']}")
            print(f"  <k^2>/<k> = {s['friend']:.4f}   gap = Var/<k> = {s['gap']:.4f}")
            print(f"  CCDF slope {a:.3f} over {n} points -> gamma = {1-a:.3f}, R^2 = {r2:.4f}")
            print(f"  degree assortativity r = {s['r']:+.4f}")

    cm = out["cond-mat coauthorship"]
    assert cm["N"] == 23133 and cm["M"] == 93439, (cm["N"], cm["M"])
    assert abs(cm["k1"] - 8.0784) < 1e-3 and abs(cm["friend"] - 22.0581) < 1e-3
    assert cm["fit"][2] > 0.97, "Part 5 claims this tail is roughly straight"
    assert cm["r"] > 0, "Part 7 claims collaboration networks are assortative"
    assert out["Internet AS graph"]["r"] < 0, "Part 7 claims technological networks are not"
    assert out["yeast protein interactions"]["r"] < 0

    if verbose:
        share = paradox_share(condmat())
        print(f"\n  share of cond-mat authors whose coauthors average MORE coauthors: "
              f"{share*100:.1f}%")
    return out


# =========================================================================== models
def ba_graph(n=20000, m=2, seed=7):
    return nx.barabasi_albert_graph(n, m, seed=seed)


def uniform_growth_graph(n=20000, m=2, seed=20260916):
    """Same growth as BA, but each arriving node picks its m targets uniformly."""
    rng = np.random.default_rng(seed)
    g = nx.Graph()
    g.add_edges_from([(0, 1), (1, 2), (0, 2)])
    for new in range(3, n):
        for t in rng.choice(new, size=m, replace=False):
            g.add_edge(new, int(t))
    return g


def check_models(verbose=True):
    ba = ba_graph()
    dba = np.array([x for _, x in ba.degree()])
    ua = uniform_growth_graph()
    dua = np.array([x for _, x in ua.degree()])
    er = nx.gnp_random_graph(20000, 4 / 19999, seed=3)
    der = np.array([x for _, x in er.degree()])
    lat = nx.watts_strogatz_graph(2000, 4, 0.0, seed=1)
    dlat = np.array([x for _, x in lat.degree()])

    assert abs(dba.mean() - 4) < 0.01 and abs(dua.mean() - 4) < 0.01   # same <k>
    assert dba.max() > 5 * dua.max(), "preferential attachment must dominate the tail"
    assert abs(der.var() / der.mean() - 1) < 0.05, "Poisson has Var = <k>"
    assert set(dlat.tolist()) == {4} and dlat.var() == 0

    if verbose:
        print("\n--- model networks -------------------------------------------------------")
        print(f"  BA n=20000 m=2      : <k>={dba.mean():.3f}  max k={dba.max()}   "
              f"(theory gamma = 3)")
        print(f"  uniform growth, m=2 : <k>={dua.mean():.3f}  max k={dua.max()}   "
              f"(exponential tail)")
        print(f"  ER <k>=4            : <k>={der.mean():.3f}  Var={der.var():.3f}  "
              f"max k={der.max()}")
        print(f"  ring lattice, k=4   : every degree {set(dlat.tolist())}  Var={dlat.var():.1f}")
    return dba, dua, der, dlat


# =========================================================================== c26
def lognormal_degrees(n=200000, mu=0.6, sigma=2.2, seed=4):
    """A log-normal is NOT a power law, yet draws a straight CCDF over three decades.

    The plan asked for a *mixture of Poissons* here.  Measured, that construction does
    not land: a mixture over log-uniform means gives CCDF ~ log(kmax/k), which is
    visibly curved (R^2 = 0.92 over the same range; a few discrete components are worse
    still, R^2 = 0.59-0.87).  The log-normal is the counterexample the scale-free
    literature actually uses (Broido & Clauset 2019 test it as the leading alternative)
    and it reaches R^2 = 0.98 -- straight enough that the room will not spot it, which
    is the whole point of the slide.
    """
    rng = np.random.default_rng(seed)
    d = np.round(rng.lognormal(mu, sigma, n)).astype(int)
    return d[d >= 1]


def check_lognormal(verbose=True):
    d = lognormal_degrees()
    ks, su = ccdf(d)
    a, _, r2, n = ccdf_fit(ks, su, 3, 500)
    assert r2 > 0.98, "the fake must look convincingly straight or the slide has no punch"
    if verbose:
        print("\n--- the straight line that is not a power law (c26) ----------------------")
        print(f"  log-normal(mu=0.6, sigma=2.2), {len(d)} nodes: <k>={d.mean():.2f}  "
              f"max k={d.max()}")
        print(f"  CCDF slope {a:.3f} over 3<=k<=500 ({n} points) -> apparent gamma "
              f"{1-a:.3f}, R^2 = {r2:.4f}")
        print("  and it is not a power law at all -- no tail exponent exists")
    return d


# =========================================================================== literature
# Every figure below was read out of the paper's own text, not a secondary source.
LITERATURE = r"""
--- quoted from the sources (each checked against the paper's text) ------------
  Coleman, James S. 1961. The Adolescent Society. New York: Free Press.
      the survey Feld re-analysed; "Marketville" is the school's pseudonym

  Feld, Scott L. 1991. AJS 96(6):1464-1477.
      Figure 1, eight girls : <k> = 2.5,  mean friend degree = 3.0   [recomputed above]
      Marketville, 146 girls: 80 below / 41 above / 25 equal  (= 146)
                              mean degree 2.7, mean friend degree 3.4

  Ugander, Karrer, Backstrom, Marlow 2011.  arXiv:1111.4503   [verified in the PDF]
      "we characterize the entire social network of active members of Facebook in
       May 2011, a network then comprised of 721 million active users"
      "There were 68.7 billion friendship edges ... so the average Facebook user in
       our study had around 190 Facebook friends"
      "The median friend count for global users in our study was 99."
      "The expected number of friends at the end of a randomly chosen edge,
       <k^2>/<k> = 635"
      "we observe that 83.6% of users have less friends than the median friend count
       of their friends"
      "we also note that 92.7% of users have less friends than the average friend
       count of their friends"
      "For the Facebook network, r = 0.226, displaying positive correlations"
      "it is notable that there is substantial curvature exhibited in the distribution
       on a log-log scale. This curvature is somewhat surprising, because empirical
       measurements of networks have often claimed degree distributions to follow
       so-called power-law..."                       <- Part 8 rests on this sentence

  Hodas, Kooti, Lerman 2013 (ICWSM).  arXiv:1304.3480          [verified in the PDF]
      "we confirm that the friendship paradox holds for >98% of Twitter users"
      "The subgraph of such users includes 5.8M users and 193.9M links between them."
      "everyone you follow or who follows you has more friends and followers than you"

  Cohen, Havlin, ben-Avraham 2003. PRL 91:247901.   acquaintance immunization
  Barabasi & Albert 1999. Science 286:509-512.      preferential attachment, gamma = 3
  Broido & Clauset 2019. Nat. Commun. 10:1017.      "Scale-free networks are rare"
"""

if __name__ == "__main__":
    check_feld()
    check_toys()
    check_real()
    check_models()
    check_lognormal()
    print(LITERATURE)
    print("all assertions passed")
