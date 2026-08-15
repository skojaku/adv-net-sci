#!/usr/bin/env python3
"""Every number the Module 05 deck claims, computed from data before the spec is written.

Two arithmetic errors reached m01 slides through unverified specs, so nothing goes into
review/DECK_SPEC.md or onto a slide that has not printed here first.  The figure modules
import from here rather than re-typing any value, so the deck, the spec and the figures
cannot drift apart.

    python3 figures/verify_numbers.py      # print the verified table, run every assertion

THE TRAP THIS FILE EXISTS FOR
-----------------------------
`nx.karate_club_graph()` ships **edge weights** (Zachary's interaction counts), and
`nx.community.modularity` defaults to `weight="weight"`.  So the obvious call returns the
*weighted* modularity: 0.3914 for the real split, 0.4449 for Louvain's best.  The deck
teaches unweighted modularity -- A_ij is 0 or 1 -- and those numbers are 0.3582 and
0.4198.  plan.md carried the weighted pair; this module computes both and asserts the
gap, so the substitution cannot happen again silently.

Data: `nx.karate_club_graph()` (Zachary 1977) and the three demo networks the lecturer
already uses in class, read from
`lecture-note/assets/vis/community-detection/*.json`.
"""

import itertools
import json
import math
import statistics
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

import networkx as nx
from networkx.algorithms.community import louvain_communities

HERE = Path(__file__).resolve().parent
VIS = HERE.parents[2] / "lecture-note" / "assets" / "vis" / "community-detection"


# =========================================================================== primitives
def unweighted_Q(g, parts):
    """Modularity with A_ij in {0,1} -- the quantity the deck defines.

    Q = sum_c [ L_c/m - (d_c/2m)^2 ].  Never call nx's version on the karate club: it
    reads the `weight` attribute by default and answers a different question.
    """
    m = g.number_of_edges()
    return sum(g.subgraph(c).number_of_edges() / m
               - (sum(d for _, d in g.degree(c)) / (2 * m)) ** 2 for c in parts)


def cut_size(g, S):
    S = set(S)
    return sum(1 for u, v in g.edges() if (u in S) != (v in S))


def ratio_cut(g, S):
    S = set(S)
    return F(cut_size(g, S), len(S) * (g.number_of_nodes() - len(S)))


def normalized_cut(g, S):
    S = set(S)
    T = set(g) - S
    e1 = g.subgraph(S).number_of_edges()
    e2 = g.subgraph(T).number_of_edges()
    return None if e1 * e2 == 0 else F(cut_size(g, S), e1 * e2)


def conductance(g, S):
    S = set(S)
    vol = sum(d for _, d in g.degree(S))
    return F(cut_size(g, S), min(vol, 2 * g.number_of_edges() - vol))


def entropy(lab):
    n = len(lab)
    return -sum(v / n * math.log(v / n) for v in Counter(lab).values())


def mutual_information(a, b):
    n = len(a)
    ca, cb = Counter(a), Counter(b)
    return sum(v / n * math.log((v / n) / ((ca[x] / n) * (cb[y] / n)))
               for (x, y), v in Counter(zip(a, b)).items())


def nmi(a, b):
    return 2 * mutual_information(a, b) / (entropy(a) + entropy(b))


def rand_index(a, b):
    n = len(a)
    agree = sum((a[i] == a[j]) == (b[i] == b[j])
                for i, j in itertools.combinations(range(n), 2))
    return F(agree, n * (n - 1) // 2)


def ari(a, b):
    n = len(a)
    ch = lambda x: x * (x - 1) // 2                                       # noqa: E731
    sij = sum(ch(v) for v in Counter(zip(a, b)).values())
    sa = sum(ch(v) for v in Counter(a).values())
    sb = sum(ch(v) for v in Counter(b).values())
    exp = sa * sb / ch(n)
    return (sij - exp) / ((sa + sb) / 2 - exp)


def labels(parts, n):
    return [next(i for i, c in enumerate(parts) if x in c) for x in range(n)]


def bell(n):
    """Ways to partition n labelled items into any number of groups (Bell triangle).

    The tempting slide line is "more ways than atoms in the universe". B(34) is
    2.1e28 and the observable universe holds ~1e80 atoms, so the comparison is false
    and the deck does not make it.
    """
    row = [1]
    for _ in range(n):
        nxt = [row[-1]]
        for x in row:
            nxt.append(nxt[-1] + x)
        row = nxt
    return row[0]


def best_louvain(g, seeds=200):
    """The best partition Louvain reaches, and every distinct one it produced."""
    seen = {}
    for s in range(seeds):
        c = [sorted(x) for x in louvain_communities(g, seed=s)]
        seen[tuple(sorted(tuple(x) for x in c))] = unweighted_Q(g, c)
    ranked = sorted(seen.items(), key=lambda kv: -kv[1])
    return [list(x) for x in ranked[0][0]], ranked[0][1], ranked


# =========================================================================== the club
# Zachary, Wayne W. 1977. "An Information Flow Model for Conflict and Fission in Small
# Groups." Journal of Anthropological Research 33(4): 452-473.  Observed 1970-1972.
ZACHARY_CITE = ("Zachary 1977, Journal of Anthropological Research 33(4): 452-473; "
                "observed 1970-1972")


@lru_cache(maxsize=None)
def karate():
    return nx.karate_club_graph()


@lru_cache(maxsize=None)
def factions():
    """(Mr. Hi's club, the officers' club) as node sets, from the recorded outcome."""
    g = karate()
    hi = frozenset(n for n, d in g.nodes(data=True) if d["club"] == "Mr. Hi")
    return hi, frozenset(g) - hi


# The one person the structure gets wrong.  0-indexed 8 is Zachary's node 9.
NODE9 = 8
NODE9_STORY = ("a weak supporter of the officers who joined Mr. Hi's club anyway: he was "
               "three weeks from his black-belt test and would have lost his rank")

MR_HI, JOHN_A = 0, 33            # 0-indexed; Zachary's nodes 1 and 34


@lru_cache(maxsize=None)
def zachary_min_cut():
    """Reproduce Zachary's own answer: the weighted min cut between the two leaders."""
    g = karate()
    _, (S, T) = nx.minimum_cut(g, MR_HI, JOHN_A, capacity="weight")
    return frozenset(S), frozenset(T)


# =========================================================================== demo nets
def _load(name):
    d = json.loads((VIS / name).read_text())
    g = nx.Graph()
    g.add_nodes_from(range(d["n_nodes"]))
    g.add_edges_from((l["source"], l["target"]) for l in d["links"])
    return g


@lru_cache(maxsize=None)
def two_cliques():
    """Two 5-cliques joined by one edge -- the live demo the lecturer already runs."""
    return _load("two-cliques.json")


@lru_cache(maxsize=None)
def two_cliques_big():
    """The same two 5-cliques, plus a 40-node community.  Nothing else changed."""
    return _load("two-cliques-big-clique.json")


@lru_cache(maxsize=None)
def random_net():
    return _load("random-net.json")


CLIQUE_A, CLIQUE_B = frozenset(range(5)), frozenset(range(5, 10))
BIG_BLOCK = frozenset(range(10, 50))


# =========================================================================== worksheets
# Part 4: compute Q by hand.  Two triangles joined by one edge; every quantity is a
# small integer and the answer is an exact fraction.
WORKSHEET_Q_EDGES = [(1, 2), (1, 3), (2, 3), (4, 5), (4, 6), (5, 6), (3, 4)]


@lru_cache(maxsize=None)
def worksheet_Q():
    g = nx.Graph(WORKSHEET_Q_EDGES)
    right = unweighted_Q(g, [[1, 2, 3], [4, 5, 6]])
    return {"g": g, "m": g.number_of_edges(),
            "right": F(right).limit_denominator(10 ** 6),
            "one_group": unweighted_Q(g, [[1, 2, 3, 4, 5, 6]]),
            "crossed": F(unweighted_Q(g, [[1, 2, 4], [3, 5, 6]])).limit_denominator(10 ** 6)}


# Part 8: compute NMI and ARI by hand.  Six people, one of them placed wrongly.
WORKSHEET_TRUTH = [0, 0, 0, 1, 1, 1]
WORKSHEET_FOUND = [0, 0, 0, 0, 1, 1]


@lru_cache(maxsize=None)
def worksheet_scores():
    t, f = WORKSHEET_TRUTH, WORKSHEET_FOUND
    return {"H_true": entropy(t), "H_found": entropy(f), "I": mutual_information(t, f),
            "nmi": nmi(t, f), "rand": rand_index(t, f), "ari": ari(t, f),
            "contingency": dict(Counter(zip(t, f)))}


# =========================================================================== the table
def facts():
    """Every claim the deck makes, computed. Assertions guard the ones that could rot."""
    g = karate()
    m = g.number_of_edges()
    hi, of = factions()
    out = {}

    out["N"], out["M"] = g.number_of_nodes(), m
    assert (out["N"], out["M"]) == (34, 78)

    out["split"] = (len(hi), len(of))
    assert out["split"] == (17, 17), "the recorded split is 17 against 17"

    out["deg_mr_hi"], out["deg_john_a"] = g.degree(MR_HI), g.degree(JOHN_A)
    assert (out["deg_mr_hi"], out["deg_john_a"]) == (16, 17)

    out["internal_hi"] = g.subgraph(hi).number_of_edges()
    out["internal_of"] = g.subgraph(of).number_of_edges()
    out["cut_true"] = cut_size(g, hi)
    assert out["internal_hi"] + out["internal_of"] + out["cut_true"] == m
    assert (out["internal_hi"], out["internal_of"], out["cut_true"]) == (35, 32, 11)

    # Part 2 -- pattern matching
    cliques = [sorted(c) for c in nx.find_cliques(g)]
    top = max(len(c) for c in cliques)
    out["max_clique_size"] = top
    out["max_cliques"] = [c for c in cliques if len(c) == top]
    assert out["max_clique_size"] == 5 and len(out["max_cliques"]) == 2
    assert all(MR_HI in c for c in out["max_cliques"]), "both maximum cliques hold Mr. Hi"
    assert JOHN_A not in set().union(*out["max_cliques"])

    core = nx.core_number(g)
    out["max_core_k"] = max(core.values())
    out["max_core_nodes"] = sorted(n for n, v in core.items() if v == out["max_core_k"])
    assert out["max_core_k"] == 4 and len(out["max_core_nodes"]) == 10
    out["core_sizes"] = {k: sum(1 for v in core.values() if v >= k) for k in range(1, 5)}

    # Part 3 -- cuts
    out["degree_one_nodes"] = sorted(n for n, d in g.degree() if d == 1)
    assert out["degree_one_nodes"] == [11], "node 12 (1-indexed) is the club's only leaf"
    S, T = zachary_min_cut()
    out["mincut_agree"] = sum(1 for n in g if (n in S) == (n in hi))
    out["mincut_wrong"] = sorted(S ^ hi)
    assert out["mincut_agree"] == 33 and out["mincut_wrong"] == [NODE9], (
        "Zachary's min cut must reproduce his paper: 33 of 34, missing only node 9")
    lab_true = [0 if n in hi else 1 for n in range(34)]
    lab_cut = [0 if n in S else 1 for n in range(34)]
    out["mincut_nmi"], out["mincut_ari"] = nmi(lab_true, lab_cut), ari(lab_true, lab_cut)

    # Part 3 -- the small club used for the cut arithmetic
    sc = small_club()
    out["small_club"] = {
        "N": sc.number_of_nodes(), "M": sc.number_of_edges(),
        "trivial_cut": cut_size(sc, [9]), "trivial_ratio": ratio_cut(sc, [9]),
        "trivial_ncut": normalized_cut(sc, [9]),
        "natural_cut": cut_size(sc, SMALL_LEFT), "natural_ratio": ratio_cut(sc, SMALL_LEFT),
        "natural_ncut": normalized_cut(sc, SMALL_LEFT),
        "crossed_ratio": ratio_cut(sc, [1, 2, 5, 6]),
    }
    assert out["small_club"]["trivial_ratio"] > out["small_club"]["natural_ratio"], (
        "the ratio-cut demo only works if the balanced split beats peeling the leaf")
    assert out["small_club"]["trivial_ncut"] is None, (
        "the lone node must have no internal edges -- that is the normalized-cut point")

    # Part 4 -- modularity, and the weighted/unweighted trap
    out["Q_true"] = unweighted_Q(g, [hi, of])
    out["Q_true_weighted"] = nx.community.modularity(g, [hi, of])
    assert abs(out["Q_true"] - 0.3582) < 5e-5, out["Q_true"]
    assert abs(out["Q_true_weighted"] - 0.3914) < 5e-5, (
        "the weighted value plan.md quoted; kept only so the gap stays visible")

    out["worksheet_Q"] = worksheet_Q()
    assert out["worksheet_Q"]["right"] == F(5, 14)
    assert out["worksheet_Q"]["one_group"] == 0.0

    # Part 5 / 7 -- Louvain, degeneracy
    L4, QL4, ranked = best_louvain(g)
    out["louvain_parts"] = L4
    out["louvain_Q"] = QL4
    out["louvain_sizes"] = sorted(len(c) for c in L4)
    assert abs(QL4 - 0.4198) < 5e-5 and len(L4) == 4, (QL4, len(L4))
    assert QL4 > out["Q_true"], "the deck's closing line needs the optimum to beat reality"
    lab_L4 = labels(L4, 34)
    out["louvain_nmi"], out["louvain_ari"] = nmi(lab_true, lab_L4), ari(lab_true, lab_L4)
    assert out["louvain_nmi"] < out["mincut_nmi"], (
        "the point of the ending: the higher-scoring partition matches reality less well")

    out["bell"] = {n: bell(n) for n in (5, 10, 20, 34)}
    assert 2e28 < out["bell"][34] < 2.2e28, "the Part 5 slide states 2e28"

    out["distinct_partitions"] = len({k for k, _ in ranked})
    alt = next((list(k), q) for k, q in ranked if abs(q - QL4) > 1e-9 and QL4 - q < 0.006)
    out["degenerate_alt_Q"] = alt[1]
    out["degenerate_alt"] = [sorted(c) for c in alt[0]]
    ga = {n: i for i, c in enumerate(L4) for n in c}
    gb = {n: i for i, c in enumerate(out["degenerate_alt"]) for n in c}
    out["degenerate_moved"] = sorted(
        n for n in range(34)
        if sorted(x for x in range(34) if ga[x] == ga[n]) != sorted(
            x for x in range(34) if gb[x] == gb[n]))
    out["degenerate_pairs"] = sum(
        1 for u, v in itertools.combinations(range(34), 2)
        if (ga[u] == ga[v]) != (gb[u] == gb[v]))

    # Part 7 -- the resolution limit, on the lecturer's own demo networks
    small, big = two_cliques(), two_cliques_big()
    out["tc"] = {
        "N": small.number_of_nodes(), "M": small.number_of_edges(),
        "sqrt2m": math.sqrt(2 * small.number_of_edges()),
        "clique_internal": small.subgraph(CLIQUE_A).number_of_edges(),
        "Q_split": unweighted_Q(small, [CLIQUE_A, CLIQUE_B]),
        "Q_merged": unweighted_Q(small, [set(small)]),
    }
    out["tcb"] = {
        "N": big.number_of_nodes(), "M": big.number_of_edges(),
        "sqrt2m": math.sqrt(2 * big.number_of_edges()),
        "clique_internal": big.subgraph(CLIQUE_A).number_of_edges(),
        "block_internal": big.subgraph(BIG_BLOCK).number_of_edges(),
        "Q_split": unweighted_Q(big, [CLIQUE_A, CLIQUE_B, BIG_BLOCK]),
        "Q_merged": unweighted_Q(big, [CLIQUE_A | CLIQUE_B, BIG_BLOCK]),
    }
    assert out["tc"]["clique_internal"] == out["tcb"]["clique_internal"] == 10, (
        "the two demos must contain the SAME cliques -- that is the whole argument")
    assert out["tc"]["Q_split"] > out["tc"]["Q_merged"], "alone, the cliques stay apart"
    assert out["tcb"]["Q_merged"] > out["tcb"]["Q_split"], "in company, they are merged"
    assert out["tc"]["clique_internal"] > out["tc"]["sqrt2m"], "10 > sqrt(42): kept"
    assert out["tcb"]["clique_internal"] < out["tcb"]["sqrt2m"], "10 < sqrt(548): absorbed"
    out["karate_sqrt2m"] = math.sqrt(2 * m)
    assert min(out["internal_hi"], out["internal_of"]) > out["karate_sqrt2m"], (
        "the club's own factions sit safely above the threshold; do not claim otherwise")

    # Part 7 -- structure where there is none
    rnd = random_net()
    _, out["random_Q"], _ = best_louvain(rnd, seeds=120)
    out["random_N"], out["random_M"] = rnd.number_of_nodes(), rnd.number_of_edges()
    assert out["random_Q"] > out["tc"]["Q_split"], (
        "the demo's punchline: the random net outscores the two-clique net")

    er = [max(unweighted_Q(h, louvain_communities(h, seed=t)) for t in range(5))
          for h in (nx.gnm_random_graph(34, 78, seed=s) for s in range(200))]
    out["er_mean"], out["er_max"] = statistics.mean(er), max(er)
    out["er_above_03"] = sum(q > 0.3 for q in er) / len(er)
    assert out["er_above_03"] == 1.0, "every random twin of the club clears the 0.3 rule"
    assert out["er_mean"] > out["Q_true"] - 0.01, (
        "the killer comparison: a random graph of the same size scores what the real "
        "split scores")

    # Part 8 -- evaluation
    out["cond_true"] = conductance(g, hi)
    out["cond_louvain"] = [conductance(g, c) for c in L4]
    assert all(c > out["cond_true"] for c in out["cond_louvain"]), (
        "conductance ranks the real split above every Louvain community -- the slide "
        "where the two scores disagree")
    out["worksheet_scores"] = worksheet_scores()
    ws = out["worksheet_scores"]
    assert ws["rand"] == F(2, 3) and abs(ws["ari"] - 0.3243) < 5e-5
    assert ws["rand"] > ws["ari"], "Rand flatters; ARI corrects it"
    return out


# The small club used for the cut arithmetic in Part 3: two 4-cliques joined by two
# edges, with one leaf hanging off.  Small enough to draw planar and to follow by hand.
SMALL_EDGES = [(1, 2), (1, 3), (1, 4), (2, 3), (2, 4), (3, 4),
               (5, 6), (5, 7), (5, 8), (6, 7), (6, 8), (7, 8),
               (4, 5), (3, 6), (1, 9)]
SMALL_LEFT = [1, 2, 3, 4, 9]


@lru_cache(maxsize=None)
def small_club():
    return nx.Graph(SMALL_EDGES)


# =========================================================================== report
def main():
    f = facts()
    p = print
    p("=== The club ===================================================== " + ZACHARY_CITE)
    p(f"  nodes {f['N']}   edges {f['M']}   split {f['split'][0]} vs {f['split'][1]}")
    p(f"  Mr. Hi degree {f['deg_mr_hi']}   John A. degree {f['deg_john_a']}")
    p(f"  internal edges {f['internal_hi']} / {f['internal_of']}, crossing {f['cut_true']}")
    p("=== Part 2  pattern matching =====================================")
    p(f"  largest clique {f['max_clique_size']} nodes, {len(f['max_cliques'])} of them: "
      f"{f['max_cliques']}")
    p(f"  deepest core {f['max_core_k']}-core, {len(f['max_core_nodes'])} nodes: "
      f"{f['max_core_nodes']}")
    p(f"  core sizes by k: {f['core_sizes']}")
    p("=== Part 3  cuts =================================================")
    sc = f["small_club"]
    p(f"  small club: {sc['N']} nodes, {sc['M']} edges")
    p(f"    peel the leaf : cut {sc['trivial_cut']}  ratio {sc['trivial_ratio']} "
      f"= {float(sc['trivial_ratio']):.4f}  ncut {sc['trivial_ncut']} (undefined)")
    p(f"    natural split : cut {sc['natural_cut']}  ratio {sc['natural_ratio']} "
      f"= {float(sc['natural_ratio']):.4f}  ncut {sc['natural_ncut']} "
      f"= {float(sc['natural_ncut']):.4f}")
    p(f"    across cliques: ratio {sc['crossed_ratio']} = {float(sc['crossed_ratio']):.4f}")
    p(f"  only leaf in the club: node {f['degree_one_nodes'][0]} (1-indexed 12)")
    p(f"  Zachary's min cut agrees with the outcome on {f['mincut_agree']}/34; "
      f"wrong only on 0-indexed {f['mincut_wrong']} = node 9")
    p(f"    NMI {f['mincut_nmi']:.4f}   ARI {f['mincut_ari']:.4f}")
    p("=== Part 4  modularity ===========================================")
    p(f"  Q(real split)  unweighted {f['Q_true']:.4f}   "
      f"[weighted {f['Q_true_weighted']:.4f} <- what nx returns by default; NOT the deck's]")
    w = f["worksheet_Q"]
    p(f"  worksheet: m={w['m']}  Q(two triangles) = {w['right']} = {float(w['right']):.4f}"
      f"   Q(all one) = {w['one_group']:.1f}   Q(crossed) = {w['crossed']}")
    p("=== Part 5 / 7  Louvain and degeneracy ===========================")
    p(f"  best Q {f['louvain_Q']:.4f} with {len(f['louvain_parts'])} communities, "
      f"sizes {f['louvain_sizes']}")
    p(f"    vs the real split: NMI {f['louvain_nmi']:.4f}  ARI {f['louvain_ari']:.4f}")
    p("  ways to partition n people: "
      + ", ".join(f"B({n})={v:.3g}" for n, v in f["bell"].items()))
    p(f"  {f['distinct_partitions']} distinct partitions from 200 Louvain runs")
    p(f"  runner-up Q {f['degenerate_alt_Q']:.4f} (gap "
      f"{f['louvain_Q'] - f['degenerate_alt_Q']:.4f}), moves nodes "
      f"{f['degenerate_moved']}, {f['degenerate_pairs']} pairs disagree")
    p("=== Part 7  three ways it lies ===================================")
    tc, tcb = f["tc"], f["tcb"]
    p(f"  two cliques alone: m {tc['M']}, sqrt(2m) {tc['sqrt2m']:.2f}, "
      f"clique has {tc['clique_internal']} internal edges "
      f"-> Q(split) {tc['Q_split']:.4f} > Q(merged) {tc['Q_merged']:.4f}   KEPT APART")
    p(f"  plus a 40-node block: m {tcb['M']}, sqrt(2m) {tcb['sqrt2m']:.2f}, "
      f"the SAME {tcb['clique_internal']} internal edges "
      f"-> Q(merged) {tcb['Q_merged']:.4f} > Q(split) {tcb['Q_split']:.4f}   MERGED")
    p(f"  karate sqrt(2m) = {f['karate_sqrt2m']:.2f}; its factions hold "
      f"{f['internal_hi']} and {f['internal_of']} internal edges (safe)")
    p(f"  random net ({f['random_N']} nodes, {f['random_M']} edges): Q {f['random_Q']:.4f} "
      f"> the two-clique network's {tc['Q_split']:.4f}")
    p(f"  200 random graphs with the club's own 34 nodes and 78 edges: mean Q "
      f"{f['er_mean']:.4f}, best {f['er_max']:.4f}, above 0.3: {f['er_above_03']:.0%}")
    p("=== Part 8  evaluation ===========================================")
    p(f"  conductance of the real split {f['cond_true']} = {float(f['cond_true']):.4f}")
    p("  conductance of Louvain's four: "
      + ", ".join(f"{float(c):.3f}" for c in f["cond_louvain"]))
    s = f["worksheet_scores"]
    p(f"  worksheet: I {s['I']:.4f}  H {s['H_true']:.4f}/{s['H_found']:.4f}  "
      f"NMI {s['nmi']:.4f}  Rand {s['rand']} = {float(s['rand']):.4f}  ARI {s['ari']:.4f}")
    p("\nall assertions passed")


if __name__ == "__main__":
    main()
