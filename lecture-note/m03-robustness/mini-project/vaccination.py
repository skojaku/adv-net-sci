"""Spend a fixed number of vaccines on a network, and see who is left exposed.

Reference implementation for the M03 group mini-project (see
``mini-project.md`` one directory up), and the same problem as
``robust_design.py`` read backwards. The
attacker removes nodes to shatter a network; the public health officer removes
nodes, by making them immune, to shatter the network the disease travels on.
One picks removals to make the R-index small, the other picks removals to make
the outbreak small, and it is the same choice.

The model is site percolation, which is the fully transmissible limit of SIR:
a vaccinated person never catches it and never passes it on, and everybody
reachable from the first case through unvaccinated people does catch it. So
after the vaccines are given out, the residual network splits into components,
and the outbreak is whichever component the first case lands in. Two numbers
follow, both in units of the whole population:

    expected outbreak  = sum over residual components of s^2 / N^2
                         (the first case is uniform over all N people, so a
                         vaccinated person starting it means no outbreak)
    worst outbreak     = largest residual component / N

The first is what you optimise. The second is what you promise a minister.

This limit is deliberately pessimistic: every contact transmits. A disease
that spreads with probability p < 1 needs bond percolation on top, and the
ranking of strategies is not guaranteed to survive that change. Say so before
anyone quotes a number from here.

The interface a submission provides
-----------------------------------
    def vaccinate(edges, n, budget) -> list[int]:
        '''Up to `budget` people to vaccinate, in the order you would give the
        shots.'''

What the plans are worth
------------------------
Expected outbreak, as a fraction of the population, on n = 500 people with
1000 contacts and 100 vaccines, which is the mini-project's own setting. Lower
is better, and 1.00 is what happens if nobody is vaccinated.

    plan                        even contacts   random contacts   hub-heavy
    vaccinate at random                 0.638             0.583       0.606
    a random contact of a
      random person                     0.637             0.533       0.274
    most contacts, ranked once          0.637             0.487       0.006
    most contacts, recomputed           0.624             0.411       0.005
    smallest outbreak left behind       0.596             0.339       0.004
    most shortest paths,
      recomputed                        0.471             0.262       0.004

Three things worth saying out loud to a class. Vaccinating at random is
hopeless everywhere, and it is what you get if you simply open a clinic.
Knowing who the hubs are is worth almost everything in the hub-heavy
population and almost nothing in the even one, which is the robust-yet-fragile
paradox arriving from the other side. And the acquaintance rule, which asks
nobody to know the network at all, recovers a good part of that advantage
where it matters: 0.27 against 0.61, from a rule you could run with a
clipboard.

The budget decides which of those lessons the numbers will teach. At 50
vaccines only the hub-heavy column moves at all (0.80 at random, 0.36 by
degree, 0.11 by betweenness). At 150 the hub-heavy column is finished by every
targeted rule alike, all of them at 0.002, and the interesting contrast has
moved to the even one (0.48 at random against 0.17 by betweenness).

No single rule wins everywhere: cutting bridges is worth most where contacts
are spread evenly, chasing hubs is worth most where they are not. A rule that
switched between the two partway through a campaign ought to beat both, and
finding one is a good thing to hand a class that finishes early.

Command line
------------
    python vaccination.py compare --nodes 500 --budget 50
    python vaccination.py grade --module a_team/plan.py --nodes 500 --budget 50
    python vaccination.py selftest
"""

from __future__ import annotations

import argparse
import importlib.util
import pathlib
import random
import sys
from typing import Callable, Dict, List, Sequence, Tuple

# robust_design.py is the sibling file, and it already holds the graph
# plumbing, the betweenness routine and the generators.
_HERE = pathlib.Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from robust_design import (  # noqa: E402
    Adjacency,
    Edge,
    adjacency,
    circulant,
    components,
    edge_list,
    randomize,
    read_edges,
    repair_connectivity,
    undirected,
    _betweenness,
)

Strategy = Callable[[Adjacency, int, random.Random], List[int]]


# ---------------------------------------------------------------------------
# What an outbreak costs
# ---------------------------------------------------------------------------


def outbreak_sizes(adj: Adjacency, vaccinated: Sequence[int]) -> Tuple[float, float]:
    """(expected outbreak, worst outbreak), both as fractions of the population."""
    n = len(adj)
    alive = [True] * n
    for v in vaccinated:
        alive[v] = False
    sizes = [len(c) for c in components(adj, alive)]
    return sum(s * s for s in sizes) / (n * n), (max(sizes) / n if sizes else 0.0)


def outbreak_curve(adj: Adjacency, order: Sequence[int], budget: int) -> List[float]:
    """Expected outbreak after 0, 1, ..., budget vaccines given in ``order``.

    Computed backwards, as in the R-index: vaccinate the whole budget, then
    put people back one at a time and merge with a union-find, which keeps the
    sum of squared component sizes to hand at every step. One pass over the
    edges instead of one component scan per vaccine.
    """
    n = len(adj)
    budget = min(budget, len(order))
    parent = list(range(n))
    size = [1] * n
    present = [False] * n

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:
            parent[x], x = root, parent[x]
        return root

    sum_sq = 0

    def union(a: int, b: int) -> None:
        nonlocal sum_sq
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        sum_sq += 2 * size[ra] * size[rb]  # (a+b)^2 - a^2 - b^2
        parent[rb] = ra
        size[ra] += size[rb]

    vaccinated = set(order[:budget])
    for v in range(n):  # everybody who never gets a vaccine is there from the start
        if v in vaccinated:
            continue
        present[v] = True
        sum_sq += 1
        for w in adj[v]:
            if present[w]:
                union(v, w)

    curve = [0.0] * (budget + 1)
    curve[budget] = sum_sq / (n * n)
    for k in range(budget - 1, -1, -1):
        v = order[k]  # the person who, with k vaccines, does not get one
        present[v] = True
        sum_sq += 1
        for w in adj[v]:
            if present[w]:
                union(v, w)
        curve[k] = sum_sq / (n * n)
    return curve


def evaluate(adj: Adjacency, order: Sequence[int], budget: int) -> Dict[str, float]:
    """How much of the population a vaccination plan protects."""
    curve = outbreak_curve(adj, order, budget)
    expected, worst = outbreak_sizes(adj, order[:budget])
    return {
        "expected_outbreak": expected,
        "worst_outbreak": worst,
        "protected": 1.0 - expected,
        # Area under the outbreak curve: rewards a plan that is already doing
        # something useful halfway through the campaign, not only at the end.
        "mean_outbreak": sum(curve) / len(curve),
    }


# ---------------------------------------------------------------------------
# Who gets the shot, and in what order
# ---------------------------------------------------------------------------


def by_random(adj: Adjacency, budget: int, rng: random.Random) -> List[int]:
    """Vaccinate whoever turns up. The baseline every other plan has to beat."""
    order = list(range(len(adj)))
    rng.shuffle(order)
    return order[:budget]


def by_degree(adj: Adjacency, budget: int, rng: random.Random) -> List[int]:
    """The most connected people, ranked once on the intact network."""
    order = list(range(len(adj)))
    rng.shuffle(order)
    order.sort(key=lambda v: len(adj[v]), reverse=True)
    return order[:budget]


def by_degree_adaptive(adj: Adjacency, budget: int, rng: random.Random) -> List[int]:
    """The most connected person *left*, recomputed after every shot."""
    n = len(adj)
    alive = [True] * n
    degree = [len(adj[v]) for v in range(n)]
    chosen: List[int] = []
    for _ in range(min(budget, n)):
        best, best_key = -1, (-1, 0.0)
        for v in range(n):
            if not alive[v]:
                continue
            key = (degree[v], rng.random())
            if key > best_key:
                best, best_key = v, key
        alive[best] = False
        chosen.append(best)
        for w in adj[best]:
            if alive[w]:
                degree[w] -= 1
    return chosen


def by_acquaintance(adj: Adjacency, budget: int, rng: random.Random) -> List[int]:
    """Cohen, Havlin and ben-Avraham (2003): pick a person at random, vaccinate
    one of their contacts at random.

    Nobody has to know the network. It works because the person at the far end
    of a randomly chosen edge has the biased degree kappa, not the average
    degree, which is the same fact that makes hubs dangerous in the first place.
    """
    n = len(adj)
    vaccinated: set[int] = set()
    chosen: List[int] = []
    attempts = 0
    while len(chosen) < min(budget, n) and attempts < 100 * n:
        attempts += 1
        v = rng.randrange(n)
        if not adj[v]:
            continue
        w = rng.choice(sorted(adj[v]))
        if w in vaccinated:
            continue
        vaccinated.add(w)
        chosen.append(w)
    return chosen


def by_betweenness(adj: Adjacency, budget: int, rng: random.Random) -> List[int]:
    """The people on the most shortest paths, recomputed after every shot."""
    n = len(adj)
    alive = [True] * n
    chosen: List[int] = []
    for _ in range(min(budget, n)):
        values = _betweenness(adj, alive)
        best, best_key = -1, (float("-inf"), 0.0)
        for v in range(n):
            if not alive[v]:
                continue
            key = (values[v], rng.random())
            if key > best_key:
                best, best_key = v, key
        alive[best] = False
        chosen.append(best)
    return chosen


def removal_pieces(adj: Adjacency, alive: Sequence[bool]) -> Tuple[List[List[int]], List[int]]:
    """For every living node, the sizes of the pieces its removal would leave.

    One iterative Tarjan pass. A node that is not a cut vertex leaves a single
    piece of size c-1, where c is its component. A cut vertex leaves one piece
    per child subtree that cannot reach above it, plus whatever is left of the
    component. Also returns each node's component size.
    """
    n = len(adj)
    disc = [-1] * n
    low = [0] * n
    sub = [1] * n
    parent = [-1] * n
    cut_pieces: List[List[int]] = [[] for _ in range(n)]
    comp_size = [0] * n
    timer = 0

    for start in range(n):
        if not alive[start] or disc[start] != -1:
            continue
        disc[start] = low[start] = timer
        timer += 1
        visited = [start]
        stack: List[Tuple[int, object]] = [(start, iter(adj[start]))]
        while stack:
            v, it = stack[-1]
            descended = False
            for w in it:  # the iterator keeps its place across re-entries
                if not alive[w] or w == parent[v]:
                    continue
                if disc[w] == -1:
                    parent[w] = v
                    disc[w] = low[w] = timer
                    timer += 1
                    visited.append(w)
                    stack.append((w, iter(adj[w])))
                    descended = True
                    break
                low[v] = min(low[v], disc[w])
            if descended:
                continue
            stack.pop()
            if stack:
                u = stack[-1][0]
                low[u] = min(low[u], low[v])
                sub[u] += sub[v]
                if low[v] >= disc[u]:
                    cut_pieces[u].append(sub[v])
        size = len(visited)
        for v in visited:
            comp_size[v] = size

    pieces: List[List[int]] = [[] for _ in range(n)]
    for v in range(n):
        if not alive[v]:
            continue
        rest = comp_size[v] - 1 - sum(cut_pieces[v])
        pieces[v] = list(cut_pieces[v]) + ([rest] if rest > 0 else [])
    return pieces, comp_size


def by_fragmentation(adj: Adjacency, budget: int, rng: random.Random) -> List[int]:
    """The reference plan: at every step vaccinate whoever leaves the smallest
    expected outbreak behind.

    The damage a single vaccination does is exact and cheap, because a node's
    removal only breaks up its own component and Tarjan hands over the pieces
    for every node in one pass. Early on nobody is a cut vertex, every
    candidate leaves one piece of size c-1, and the rule falls back on degree.
    Once the network is brittle it stops chasing hubs and starts cutting
    bridges, which is the part a degree ranking cannot do.
    """
    n = len(adj)
    alive = [True] * n
    chosen: List[int] = []
    for _ in range(min(budget, n)):
        pieces, comp_size = removal_pieces(adj, alive)
        best, best_key = -1, None
        for v in range(n):
            if not alive[v]:
                continue
            # change in sum of squared component sizes, which is the change in
            # the expected outbreak up to the factor N^2
            delta = sum(p * p for p in pieces[v]) - comp_size[v] ** 2
            degree = sum(1 for w in adj[v] if alive[w])
            key = (delta, -degree, rng.random())
            if best_key is None or key < best_key:
                best, best_key = v, key
        alive[best] = False
        chosen.append(best)
    return chosen


STRATEGIES: Dict[str, Strategy] = {
    "random": by_random,
    "degree": by_degree,
    "degree_adaptive": by_degree_adaptive,
    "acquaintance": by_acquaintance,
    "betweenness": by_betweenness,
    "fragmentation": by_fragmentation,
}


def by_portfolio(
    adj: Adjacency,
    budget: int,
    rng: random.Random,
    candidates: Sequence[str] = ("degree_adaptive", "betweenness", "fragmentation"),
) -> List[int]:
    """Draw up several plans, score each one, and give out the shots for the
    best of them.

    No single rule wins on every network: cutting bridges is worth most where
    contacts are spread evenly, and chasing hubs is worth most where they are
    not. Nothing forces a choice in advance, because the network and the budget
    are both known before the first shot is given, and a plan can be scored
    without anybody being vaccinated. This is the honest way to use
    :func:`evaluate`, and it is also the trap: the score it optimises is the
    percolation limit, not a disease.
    """
    best_order: List[int] = []
    best_score = float("inf")
    for name in candidates:
        order = STRATEGIES[name](adj, budget, rng)
        score = evaluate(adj, order, budget)["expected_outbreak"]
        if score < best_score:
            best_order, best_score = order, score
    return best_order


STRATEGIES["portfolio"] = by_portfolio


def vaccinate(edges: Sequence[Edge], n: int, budget: int) -> List[int]:
    """The interface a submission has to provide. This one is the reference."""
    return by_portfolio(adjacency(n, edges), budget, random.Random(0))


# ---------------------------------------------------------------------------
# Networks to practise on
# ---------------------------------------------------------------------------


def example_networks(n: int, m: int, seed: int = 0) -> Dict[str, Adjacency]:
    """Three populations with the same number of people and the same number of
    contacts, differing only in how those contacts are spread."""
    rng = random.Random(seed)

    regular = adjacency(n, circulant(n, m))
    randomize(regular, 10 * m, rng)
    repair_connectivity(regular, rng)

    er_edges: set[Edge] = set()
    while len(er_edges) < m:
        u, v = rng.randrange(n), rng.randrange(n)
        if u != v:
            er_edges.add(undirected(u, v))
    er = adjacency(n, er_edges)
    repair_connectivity(er, rng)

    k = max(1, round(m / n))
    seed_n = k + 1
    ba_edges = {undirected(i, j) for i in range(seed_n) for j in range(i + 1, seed_n)}
    repeated = [v for e in ba_edges for v in e]
    for new in range(seed_n, n):
        targets: set[int] = set()
        while len(targets) < k:
            targets.add(repeated[rng.randrange(len(repeated))])
        for t in targets:
            ba_edges.add(undirected(new, t))
            repeated += [new, t]
    ba_list = sorted(ba_edges)
    while len(ba_list) > m:
        ba_list.pop(rng.randrange(len(ba_list)))
    ba = adjacency(n, ba_list)
    repair_connectivity(ba, rng)

    return {"even contacts": regular, "random contacts": er, "hub-heavy": ba}


def compare(n: int, m: int, budget: int, seed: int = 0) -> None:
    """Every strategy on every example network, one line each."""
    for label, adj in example_networks(n, m, seed).items():
        print(f"{label}  (n = {n}, m = {len(edge_list(adj))}, vaccines = {budget})")
        for name, strategy in STRATEGIES.items():
            rng = random.Random(f"{seed}:{name}")
            repeats = 10 if name in ("random", "acquaintance") else 1
            totals = {"expected_outbreak": 0.0, "worst_outbreak": 0.0, "mean_outbreak": 0.0}
            for rep in range(repeats):
                order = strategy(adj, budget, random.Random(f"{seed}:{name}:{rep}"))
                scores = evaluate(adj, order, budget)
                for key in totals:
                    totals[key] += scores[key] / repeats
            print(
                f"  {name:<16} expected {totals['expected_outbreak']:.3f}"
                f"   worst {totals['worst_outbreak']:.3f}"
                f"   over the campaign {totals['mean_outbreak']:.3f}"
            )
        print()


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def selftest() -> None:
    # A star: one vaccine on the hub protects everybody but the first case.
    n = 10
    star = adjacency(n, [undirected(0, i) for i in range(1, n)])
    expected, worst = outbreak_sizes(star, [])
    assert abs(expected - 1.0) < 1e-12 and abs(worst - 1.0) < 1e-12
    expected, worst = outbreak_sizes(star, [0])
    assert abs(expected - 9 / 100) < 1e-12, expected  # nine components of size 1
    assert abs(worst - 0.1) < 1e-12

    # A path cut in the middle leaves two halves.
    path = adjacency(n, [undirected(i, i + 1) for i in range(n - 1)])
    expected, _ = outbreak_sizes(path, [5])
    assert abs(expected - (25 + 16) / 100) < 1e-12, expected

    # The curve must agree with the direct computation at every budget.
    rng = random.Random(0)
    adj = adjacency(40, circulant(40, 80))
    randomize(adj, 400, rng)
    order = by_fragmentation(adj, 12, random.Random(1))
    curve = outbreak_curve(adj, order, 12)
    for k in range(13):
        direct, _ = outbreak_sizes(adj, order[:k])
        assert abs(curve[k] - direct) < 1e-12, (k, curve[k], direct)

    # Tarjan's pieces must match brute force, on graphs that are not connected.
    for trial in range(30):
        n = 25
        adj = adjacency(n, circulant(n, 35))
        randomize(adj, 100, random.Random(trial))
        alive = [random.Random(trial + 1000).random() > 0.2 for _ in range(n)]
        pieces, comp_size = removal_pieces(adj, alive)
        for v in range(n):
            if not alive[v]:
                continue
            alive[v] = False
            brute = sorted(len(c) for c in components(adj, alive))
            alive[v] = True
            here = {x for c in components(adj, alive) if v in c for x in c}
            assert comp_size[v] == len(here), (trial, v)
            # v's own component, broken into the pieces Tarjan claims, plus
            # the components v was never part of, must be the brute-force answer
            others = [len(c) for c in components(adj, alive) if v not in c]
            assert sorted(others + pieces[v]) == brute, (trial, v, pieces[v], others, brute)

    # Every strategy returns distinct, valid, budgeted choices.
    adj = adjacency(60, circulant(60, 120))
    randomize(adj, 600, random.Random(2))
    for name, strategy in STRATEGIES.items():
        chosen = strategy(adj, 15, random.Random(3))
        assert len(chosen) == len(set(chosen)) <= 15, name
        assert all(0 <= v < 60 for v in chosen), name

    # And the reference beats vaccinating at random, on the network where it
    # matters most.
    ba = example_networks(200, 400, seed=1)["hub-heavy"]
    smart = evaluate(ba, vaccinate(edge_list(ba), 200, 20), 20)
    blind = evaluate(ba, by_random(ba, 20, random.Random(4)), 20)
    assert smart["expected_outbreak"] < blind["expected_outbreak"], (smart, blind)

    print("selftest: all checks passed")


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------


def _load_plan(path: str) -> Callable[[Sequence[Edge], int, int], List[int]]:
    spec = importlib.util.spec_from_file_location("submission", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    plan = getattr(module, "vaccinate", None)
    if plan is None:
        raise ValueError(f"{path} defines no vaccinate(edges, n, budget)")
    return plan


def grade(plan: Callable[[Sequence[Edge], int, int], List[int]], n: int, m: int, budget: int, seed: int) -> float:
    """Run a submitted plan on the example networks. Returns the mean expected
    outbreak, which is the thing to minimise."""
    total = 0.0
    networks = example_networks(n, m, seed)
    for label, adj in networks.items():
        edges = edge_list(adj)
        chosen = [int(v) for v in plan(edges, n, budget)]
        if len(chosen) > budget:
            print(f"{label:<16} rejected: {len(chosen)} vaccines used, budget is {budget}")
            total += 1.0
            continue
        if len(set(chosen)) != len(chosen) or any(not 0 <= v < n for v in chosen):
            print(f"{label:<16} rejected: repeated or out-of-range person")
            total += 1.0
            continue
        scores = evaluate(adj, chosen, budget)
        total += scores["expected_outbreak"]
        print(
            f"{label:<16} expected {scores['expected_outbreak']:.3f}"
            f"   worst {scores['worst_outbreak']:.3f}"
            f"   over the campaign {scores['mean_outbreak']:.3f}"
        )
    mean = total / len(networks)
    print(f"mean expected outbreak: {mean:.3f}")
    return mean


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    show = sub.add_parser("compare", help="every strategy on the example networks")
    show.add_argument("--nodes", type=int, default=500)
    show.add_argument("--edges", type=int, default=None, help="default is 2 * nodes")
    show.add_argument("--budget", type=int, default=None, help="default is a fifth of the nodes")
    show.add_argument("--seed", type=int, default=0)

    run = sub.add_parser("grade", help="run a submitted vaccinate(edges, n, budget)")
    run.add_argument("--module", required=True)
    run.add_argument("--nodes", type=int, default=500)
    run.add_argument("--edges", type=int, default=None)
    run.add_argument("--budget", type=int, default=None)
    run.add_argument("--seed", type=int, default=0)

    one = sub.add_parser("score", help="score the reference plan on an edge list from a file")
    one.add_argument("--edges", required=True)
    one.add_argument("--budget", type=int, required=True)

    sub.add_parser("selftest", help="check the outbreak code against known cases")

    args = parser.parse_args(argv)

    if args.command == "selftest":
        selftest()
        return 0

    if args.command == "score":
        n, edges = read_edges(args.edges)
        adj = adjacency(n, edges)
        chosen = vaccinate(edges, n, args.budget)
        scores = evaluate(adj, chosen, args.budget)
        print(f"{n} people, {len(edges)} contacts, {len(chosen)} vaccines")
        for key, value in scores.items():
            print(f"  {key:<18} {value:.4f}")
        return 0

    m = args.edges if args.edges is not None else 2 * args.nodes
    budget = args.budget if args.budget is not None else max(1, args.nodes // 5)

    if args.command == "compare":
        compare(args.nodes, m, budget, args.seed)
        return 0

    grade(_load_plan(args.module), args.nodes, m, budget, args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
