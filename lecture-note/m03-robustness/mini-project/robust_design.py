"""Break a network, and build one that does not break easily.

The attack side of M03, and the machinery the group mini-project runs on. The
mini-project itself is the other half, in ``vaccination.py``: the same removals
with the opposite intention. This file holds the R-index, the attacks, and the
network generators, and ``vaccination.py`` imports all three.

A network is attacked three times, each attack sequential: rank the survivors,
remove the top one, recompute the ranking, repeat. The attacks are random
failure (averaged), degree, and betweenness, and a network scores the *minimum*
of the three R-indices, since a network that holds up under two of them and
falls to the third has fallen.

:func:`design_network` answers the other direction: given n nodes and m edges,
build the network that survives longest. It starts from a randomised
near-regular graph and hill-climbs with degree-preserving double edge swaps,
keeping a swap only when it raises the minimum, which is the method of
Schneider et al. (2011, PNAS 108:3838).

Definitions follow the lecture note. After k nodes have been removed,
connectivity is

    y_k = (size of the largest connected component) / n

with n the size of the *original* network, and

    R = (1 / n) * sum_{k=1}^{n-1} y_k.

R = 0.5 is the unreachable ceiling (only the complete graph approaches it),
R near 0 means the network shattered on the first removal.

Command line
------------
    python robust_design.py design --nodes 100 --edges 200 --out edges.csv
    python robust_design.py score  --edges edges.csv
    python robust_design.py grade  --module a_team/design.py
    python robust_design.py selftest

Everything is standard library only, which is what makes the betweenness
attack the expensive part: 0.16 s per run at n = 100 and 20 s at n = 500,
against milliseconds for the other two. Scoring one submission at both sizes
therefore takes under a minute, but a hill climb that includes betweenness in
its objective is only affordable below n = 150 (see BETWEENNESS_IN_LOOP_UP_TO).

Scores measured here, m = 2n, score being the minimum of the three attacks:

                                     n = 100   n = 500
    ten hubs                            0.06      0.06
    preferential attachment             0.13      0.09
    Erdos-Renyi                         0.19      0.18
    circulant ring, offsets 1 and 2     0.10      0.03
    random 4-regular                    0.26      0.26
    this designer                       0.28      0.26

Two things to read off it. Almost all of the score is bought by the degree
sequence: anything with hubs is finished, and a random regular graph is already
within a few percent of the best we can do. And the hill climb only pays where
the betweenness attack is inside its objective, which at n = 500 it cannot
afford to be within the 60 seconds a call is allowed, so at that size what
comes out is within noise of its own starting point.
The betweenness attack is the one that binds in every row.

NOTE FOR THE INSTRUCTOR: this file is a worked solution and it lives in a
public repository. Move it out of the student-facing tree before the session
if the teams are meant to arrive without one.
"""

from __future__ import annotations

import argparse
import heapq
import importlib.util
import random
import sys
import time
from typing import Callable, Dict, Iterable, List, Sequence, Set, Tuple

Edge = Tuple[int, int]
Adjacency = List[Set[int]]

# ---------------------------------------------------------------------------
# Graph plumbing
# ---------------------------------------------------------------------------


def undirected(u: int, v: int) -> Edge:
    """An edge as an ordered pair, so that (u, v) and (v, u) are one edge."""
    return (u, v) if u < v else (v, u)


def adjacency(n: int, edges: Iterable[Edge]) -> Adjacency:
    adj: Adjacency = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    return adj


def edge_list(adj: Adjacency) -> List[Edge]:
    return sorted({undirected(u, v) for u, nbrs in enumerate(adj) for v in nbrs})


def components(adj: Adjacency, alive: Sequence[bool] | None = None) -> List[List[int]]:
    """Connected components, optionally restricted to the alive nodes."""
    n = len(adj)
    seen = [False] * n
    out: List[List[int]] = []
    for start in range(n):
        if seen[start] or (alive is not None and not alive[start]):
            continue
        seen[start] = True
        stack, comp = [start], [start]
        while stack:
            v = stack.pop()
            for w in adj[v]:
                if seen[w] or (alive is not None and not alive[w]):
                    continue
                seen[w] = True
                stack.append(w)
                comp.append(w)
        out.append(comp)
    return out


def is_connected(adj: Adjacency) -> bool:
    return len(components(adj)) == 1


# ---------------------------------------------------------------------------
# The R-index
# ---------------------------------------------------------------------------


def robustness_profile(adj: Adjacency, order: Sequence[int]) -> List[float]:
    """Connectivity y_k for k = 1 .. n-1 under the given removal order.

    Computed backwards. Removing nodes one at a time and recomputing the
    largest component each time costs O(n * m); adding them back in reverse
    order and merging with a union-find costs O(m * alpha(n)) in total, and
    the largest component can only grow as nodes come back, so a running
    maximum is all the bookkeeping needed.
    """
    n = len(adj)
    if sorted(order) != list(range(n)):
        raise ValueError("a removal order must be a permutation of all n nodes")

    parent = list(range(n))
    size = [1] * n
    present = [False] * n

    def find(x: int) -> int:
        root = x
        while parent[root] != root:
            root = parent[root]
        while parent[x] != root:  # path compression
            parent[x], x = root, parent[x]
        return root

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]

    largest = 0
    profile = [0.0] * n  # profile[k] = y_k; entry 0 is never reported
    for k in range(n - 1, 0, -1):
        v = order[k]
        present[v] = True
        for w in adj[v]:
            if present[w]:
                union(v, w)
        largest = max(largest, size[find(v)])
        profile[k] = largest / n
    return profile[1:]


def r_index(adj: Adjacency, order: Sequence[int]) -> float:
    """Area under the robustness profile: R = (1/n) * sum_k y_k."""
    return sum(robustness_profile(adj, order)) / len(adj)


# ---------------------------------------------------------------------------
# Attacks. Each returns a removal order: a permutation of all n nodes.
# ---------------------------------------------------------------------------


def attack_random(adj: Adjacency, rng: random.Random) -> List[int]:
    """Accidental failure: nodes fall in an order that ignores the network."""
    order = list(range(len(adj)))
    rng.shuffle(order)
    return order


def attack_degree_static(adj: Adjacency, rng: random.Random) -> List[int]:
    """Hubs first, ranked once on the intact network."""
    order = list(range(len(adj)))
    rng.shuffle(order)  # random tie-break
    order.sort(key=lambda v: len(adj[v]), reverse=True)
    return order


def _adaptive(adj: Adjacency, rng: random.Random, score: Callable[[Adjacency, List[bool]], List[float]]) -> List[int]:
    """Remove the top-scoring node, rescore what is left, repeat."""
    n = len(adj)
    alive = [True] * n
    order: List[int] = []
    for _ in range(n):
        values = score(adj, alive)
        best, best_value = -1, float("-inf")
        for v in range(n):
            if not alive[v]:
                continue
            value = values[v] + rng.random() * 1e-9  # random tie-break
            if value > best_value:
                best, best_value = v, value
        alive[best] = False
        order.append(best)
    return order


def attack_degree_adaptive(adj: Adjacency, rng: random.Random) -> List[int]:
    """Hubs first, with every degree recomputed after every removal.

    A lazy heap rather than a rescan of all n nodes per step: at n = 500 the
    rescan costs about a tenth of a second per attack, which is the difference
    between a design run of minutes and one of hours.
    """
    n = len(adj)
    degree = [len(adj[v]) for v in range(n)]
    tie = [rng.random() for _ in range(n)]  # tie-break, drawn once per run
    alive = [True] * n
    heap = [(-degree[v], tie[v], v) for v in range(n)]
    heapq.heapify(heap)

    order: List[int] = []
    while len(order) < n:
        neg_degree, _, v = heapq.heappop(heap)
        if not alive[v] or -neg_degree != degree[v]:
            continue  # a stale entry, superseded by a later push
        alive[v] = False
        order.append(v)
        for w in adj[v]:
            if alive[w]:
                degree[w] -= 1
                heapq.heappush(heap, (-degree[w], tie[w], w))
    return order


def _betweenness(adj: Adjacency, alive: Sequence[bool]) -> List[float]:
    """Brandes' algorithm on the subgraph induced by the alive nodes."""
    n = len(adj)
    cb = [0.0] * n
    for s in range(n):
        if not alive[s]:
            continue
        stack: List[int] = []
        preds: List[List[int]] = [[] for _ in range(n)]
        sigma = [0.0] * n
        dist = [-1] * n
        sigma[s], dist[s] = 1.0, 0
        queue = [s]
        head = 0
        while head < len(queue):
            v = queue[head]
            head += 1
            stack.append(v)
            for w in adj[v]:
                if not alive[w]:
                    continue
                if dist[w] < 0:
                    dist[w] = dist[v] + 1
                    queue.append(w)
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    preds[w].append(v)
        delta = [0.0] * n
        while stack:
            w = stack.pop()
            for v in preds[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1.0 + delta[w])
            if w != s:
                cb[w] += delta[w]
    return cb


def attack_betweenness_adaptive(adj: Adjacency, rng: random.Random) -> List[int]:
    """Bridges first: take the node carrying the most shortest paths, recompute."""
    return _adaptive(adj, rng, lambda a, alive: _betweenness(a, alive))


def attack_greedy_lcc(adj: Adjacency, rng: random.Random, candidates: int = 15) -> List[int]:
    """One-step lookahead: of the top-degree survivors, take whichever removal
    leaves the smallest largest component. Slower than the degree attack and
    strictly nastier on networks that were tuned against the degree attack."""
    n = len(adj)
    alive = [True] * n
    order: List[int] = []
    for _ in range(n):
        live = [v for v in range(n) if alive[v]]
        ranked = sorted(live, key=lambda v: (sum(1 for w in adj[v] if alive[w]), rng.random()), reverse=True)
        best, best_lcc = ranked[0], None
        for v in ranked[:candidates]:
            alive[v] = False
            lcc = max((len(c) for c in components(adj, alive)), default=0)
            alive[v] = True
            if best_lcc is None or lcc < best_lcc:
                best, best_lcc = v, lcc
        alive[best] = False
        order.append(best)
    return order


ATTACKS: Dict[str, Callable[[Adjacency, random.Random], List[int]]] = {
    "random": attack_random,
    "degree_static": attack_degree_static,
    "degree_adaptive": attack_degree_adaptive,
    "betweenness_adaptive": attack_betweenness_adaptive,
    "greedy_lcc": attack_greedy_lcc,
}

# The three attacks a submission is graded on. Each runs sequentially: remove
# the top-ranked survivor, recompute the ranking on what is left, repeat. The
# score is the *minimum* of the three R-indices, so a network has to hold up
# under all three at once.
GRADED_ATTACKS = ("random", "degree_adaptive", "betweenness_adaptive")

# What the hill climb optimises against, cheapest attack first so that a
# proposal already sunk by a cheap attack never pays for a dear one. The
# betweenness attack is the dear one: about 1.3 s per evaluation at n = 200
# and 20 s at n = 500, against a millisecond for the other two. Below the
# cut-off it is worth it (at n = 100 it lifted the final score from 0.26 to
# 0.28), above it the climb would take hours, so it is scored only at the end.
BETWEENNESS_IN_LOOP_UP_TO = 150


def loop_ensemble(n: int) -> Tuple[str, ...]:
    if n <= BETWEENNESS_IN_LOOP_UP_TO:
        return ("random", "degree_adaptive", "betweenness_adaptive")
    return ("random", "degree_adaptive")


def score_network(
    adj: Adjacency,
    attacks: Sequence[str] = GRADED_ATTACKS,
    random_repeats: int = 10,
    seed: int = 0,
) -> Dict[str, float]:
    """R-index under each attack, plus ``score``, the minimum of them.

    Random failure is averaged over ``random_repeats`` orders. The other two
    are deterministic up to tie-breaks, so they are run once.
    """
    out: Dict[str, float] = {}
    for name in attacks:
        attack = ATTACKS[name]
        repeats = random_repeats if name == "random" else 1
        total = 0.0
        for rep in range(repeats):
            rng = random.Random(f"{seed}:{name}:{rep}")
            total += r_index(adj, attack(adj, rng))
        out[name] = total / repeats
    out["score"] = min(out.values())
    return out


# ---------------------------------------------------------------------------
# Construction
# ---------------------------------------------------------------------------


def circulant(n: int, m: int) -> List[Edge]:
    """A near-regular connected starting graph on exactly n nodes and m edges.

    Ring of offset 1, then offset 2, and so on, stopping partway through the
    last offset so that the edge count lands exactly on m.
    """
    if n < 3:
        raise ValueError("need at least 3 nodes")
    if not (n - 1 <= m <= n * (n - 1) // 2):
        raise ValueError(f"m must be between n-1 and n(n-1)/2 for n = {n}")

    edges: List[Edge] = []
    if m == n - 1:  # a tree is the only option: a path
        return [undirected(i, i + 1) for i in range(n - 1)]

    offset = 1
    while len(edges) < m:
        ring = sorted({undirected(i, (i + offset) % n) for i in range(n)})
        room = m - len(edges)
        if len(ring) <= room:
            edges.extend(ring)
        else:  # take an evenly spaced subset of this offset's ring
            step = len(ring) / room
            edges.extend(ring[int(i * step)] for i in range(room))
        offset += 1
    return edges


def _swap(adj: Adjacency, a: int, b: int, c: int, d: int) -> bool:
    """Replace edges (a,b) and (c,d) by (a,c) and (b,d). Degrees are preserved.
    Returns False and changes nothing if the result would not be simple."""
    if len({a, b, c, d}) != 4:
        return False
    if c in adj[a] or d in adj[b]:
        return False
    adj[a].discard(b)
    adj[b].discard(a)
    adj[c].discard(d)
    adj[d].discard(c)
    adj[a].add(c)
    adj[c].add(a)
    adj[b].add(d)
    adj[d].add(b)
    return True


def _random_edge(edges: List[Edge], rng: random.Random) -> Edge:
    u, v = edges[rng.randrange(len(edges))]
    return (u, v) if rng.random() < 0.5 else (v, u)


def randomize(adj: Adjacency, steps: int, rng: random.Random) -> None:
    """Degree-preserving randomisation by double edge swaps, in place."""
    for _ in range(steps):
        edges = edge_list(adj)
        a, b = _random_edge(edges, rng)
        c, d = _random_edge(edges, rng)
        _swap(adj, a, b, c, d)


def repair_connectivity(adj: Adjacency, rng: random.Random, tries: int = 1000) -> bool:
    """Merge components with degree-preserving swaps. True if connected after."""
    for _ in range(tries):
        comps = components(adj)
        if len(comps) == 1:
            return True
        comps.sort(key=len, reverse=True)
        big, small = set(comps[0]), set(comps[1])
        inside_big = [e for e in edge_list(adj) if e[0] in big and e[1] in big]
        inside_small = [e for e in edge_list(adj) if e[0] in small and e[1] in small]
        if not inside_big or not inside_small:
            return False  # nothing to rewire, e.g. an isolated node
        a, b = _random_edge(inside_big, rng)
        c, d = _random_edge(inside_small, rng)
        _swap(adj, a, b, c, d)
    return len(components(adj)) == 1


def _objective(
    adj: Adjacency,
    attacks: Sequence[str],
    seed: int,
    floor: float,
    repeats: int = 2,
) -> Tuple[float, float]:
    """(worst-case R, mean R) over the ensemble.

    Each attack is run ``repeats`` times with different tie-breaks. Without
    that, the climb happily tunes the network against one particular ordering
    of equal-degree nodes and the gain evaporates on the next draw.

    The mean is the objective's own tie-break. A minimax landscape on a sparse
    graph is mostly plateau, since one swap usually leaves the worst attack
    exactly where it was; ranking the plateau by the mean lets the climb keep
    walking instead of stalling on the first flat patch. Evaluation is
    abandoned as soon as the running worst case falls below ``floor``, the
    incumbent, because such a proposal is rejected whatever the rest of the
    ensemble would have said.
    """
    worst, total, count = float("inf"), 0.0, 0
    for name in attacks:
        for rep in range(repeats):
            rng = random.Random(f"{seed}:{name}:{rep}")
            value = r_index(adj, ATTACKS[name](adj, rng))
            worst = min(worst, value)
            total += value
            count += 1
            if worst < floor:
                return worst, float("-inf")
    return worst, total / count


def design_network(
    n: int,
    m: int,
    iterations: int = 600,
    attacks: Sequence[str] | None = None,
    seed: int = 0,
    verbose: bool = False,
    budget_seconds: float = 55.0,
) -> List[Edge]:
    """Return the edges of a connected simple graph on n nodes and m edges,
    hill-climbed so that the minimum of its R-indices over ``attacks`` is high.

    ``attacks`` defaults to :func:`loop_ensemble` for this n. The climb stops
    at ``iterations`` proposals or ``budget_seconds`` of wall clock, whichever
    comes first, because the mini-project gives one call 60 seconds and a
    reference answer that breaks its own rule is not a reference answer.

    Two things do the work, and they are worth very different amounts. The
    near-regular starting point denies the degree attack the hubs it feeds on,
    and that is most of the score. The swaps then buy a few more percent: they
    pull the graph towards the layered "onion" of Schneider et al., in which a
    node's neighbours have degrees close to its own.
    """
    attacks = tuple(attacks) if attacks is not None else loop_ensemble(n)
    rng = random.Random(seed)
    adj = adjacency(n, circulant(n, m))
    randomize(adj, steps=10 * m, rng=rng)
    if not repair_connectivity(adj, rng):
        raise RuntimeError("could not build a connected starting graph")

    best = _objective(adj, attacks, seed, floor=float("-inf"))
    if verbose:
        print(f"start:  score = {best[0]:.4f} (against {', '.join(attacks)})", file=sys.stderr)

    accepted = 0
    started = time.time()
    report_every = max(1, iterations // 4)
    for step in range(iterations):
        if time.time() - started > budget_seconds:
            if verbose:
                print(f"stopped at step {step} on the time budget", file=sys.stderr)
            break
        edges = edge_list(adj)
        a, b = _random_edge(edges, rng)
        c, d = _random_edge(edges, rng)
        if not _swap(adj, a, b, c, d):
            continue
        candidate = _objective(adj, attacks, seed, floor=best[0])
        if candidate > best and is_connected(adj):
            best = candidate
            accepted += 1
        else:
            restored = _swap(adj, a, c, b, d)  # put the two edges back
            assert restored, "failed to undo a swap"
        if verbose and (step + 1) % report_every == 0:
            print(
                f"step {step + 1:5d}: score = {best[0]:.4f} "
                f"(mean {best[1]:.4f}, {accepted} swaps kept)",
                file=sys.stderr,
            )
    return edge_list(adj)


def build_network(n: int, m: int) -> List[Edge]:
    """The interface a submission has to provide: nodes and an edge budget in,
    an edge list out. This one is the reference answer."""
    return design_network(n, m)


# ---------------------------------------------------------------------------
# Submission handling
# ---------------------------------------------------------------------------


def read_edges(path: str) -> Tuple[int, List[Edge]]:
    """Read a two-column edge list (CSV, optional header). Nodes are relabelled
    to 0 .. n-1 in order of first appearance."""
    pairs: List[Tuple[str, str]] = []
    with open(path) as handle:
        for line in handle:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.replace("\t", ",").replace(" ", ",").split(",") if p.strip()]
            if len(parts) < 2:
                raise ValueError(f"cannot read two node names from: {line!r}")
            pairs.append((parts[0], parts[1]))
    header_words = {"source", "target", "node", "node1", "node2", "from", "to", "u", "v", "id"}
    if pairs and {pairs[0][0].lower(), pairs[0][1].lower()} <= header_words:
        pairs = pairs[1:]  # a header line, not an edge between two nodes named "source" and "target"

    labels: Dict[str, int] = {}
    edges: List[Edge] = []
    for u, v in pairs:
        for name in (u, v):
            labels.setdefault(name, len(labels))
        edges.append(undirected(labels[u], labels[v]))
    return len(labels), edges


def write_edges(path: str, edges: Sequence[Edge]) -> None:
    with open(path, "w") as handle:
        handle.write("source,target\n")
        for u, v in edges:
            handle.write(f"{u},{v}\n")


def validate(n: int, edges: Sequence[Edge], expect_nodes: int | None = None, expect_edges: int | None = None) -> List[str]:
    """House rules for a submitted network. Returns the list of violations."""
    problems: List[str] = []
    if any(u == v for u, v in edges):
        problems.append("self-loops are not allowed")
    if len(set(edges)) != len(edges):
        problems.append("repeated edges are not allowed")
    if expect_nodes is not None and n != expect_nodes:
        problems.append(f"expected {expect_nodes} nodes, found {n}")
    if expect_edges is not None and len(edges) != expect_edges:
        problems.append(f"expected {expect_edges} edges, found {len(edges)}")
    if not is_connected(adjacency(n, edges)):
        problems.append("the network is not connected")
    return problems


# ---------------------------------------------------------------------------
# Self-test
# ---------------------------------------------------------------------------


def selftest() -> None:
    n = 20

    complete = [undirected(i, j) for i in range(n) for j in range(i + 1, n)]
    got = r_index(adjacency(n, complete), list(range(n)))
    want = (n - 1) / (2 * n)  # every removal costs exactly one node
    assert abs(got - want) < 1e-12, (got, want)

    star = [undirected(0, i) for i in range(1, n)]
    adj = adjacency(n, star)
    got = r_index(adj, attack_degree_static(adj, random.Random(0)))
    want = (n - 1) / n**2  # the hub goes first, nothing is ever connected again
    assert abs(got - want) < 1e-12, (got, want)

    ring = adjacency(n, [undirected(i, (i + 1) % n) for i in range(n)])
    assert r_index(ring, list(range(n))) > r_index(adj, list(range(n)))

    adj = adjacency(n, circulant(n, 40))
    profile = robustness_profile(adj, attack_degree_adaptive(adj, random.Random(0)))
    assert len(profile) == n - 1
    assert all(profile[i] >= profile[i + 1] for i in range(len(profile) - 1)), "profile must be non-increasing"

    for m in (n - 1, n, 2 * n, 3 * n + 7, n * (n - 1) // 2):
        edges = circulant(n, m)
        assert len(edges) == m and len(set(edges)) == m, m
        assert is_connected(adjacency(n, edges)), m

    edges = circulant(n, 40)
    adj = adjacency(n, edges)
    before = sorted(len(a) for a in adj)
    randomize(adj, 200, random.Random(1))
    assert sorted(len(a) for a in adj) == before, "swaps must preserve the degree sequence"
    assert len(edge_list(adj)) == 40

    assert validate(n, edges, expect_nodes=n, expect_edges=40) == []
    assert validate(n, edges + [edges[0]], expect_edges=40) != []

    scores = score_network(adjacency(n, edges), seed=0)
    assert set(scores) == set(GRADED_ATTACKS) | {"score"}
    assert scores["score"] == min(scores[name] for name in GRADED_ATTACKS)

    built = build_network(30, 60)  # the interface a submission must provide
    assert validate(30, built, expect_nodes=30, expect_edges=60) == []

    print("selftest: all checks passed")


# ---------------------------------------------------------------------------
# Command line
# ---------------------------------------------------------------------------


def _report(adj: Adjacency, seed: int, extra: Sequence[str] = ()) -> Dict[str, float]:
    scores = score_network(adj, attacks=tuple(GRADED_ATTACKS) + tuple(extra), seed=seed)
    width = max(len(k) for k in scores)
    for name, value in scores.items():
        marker = "  <- the minimum of the three, which is the score" if name == "score" else ""
        print(f"  {name:<{width}}  R = {value:.4f}{marker}")
    return scores


def _load_builder(path: str) -> Callable[[int, int], List[Edge]]:
    """Import ``build_network`` from a submitted file."""
    spec = importlib.util.spec_from_file_location("submission", path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot import {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    builder = getattr(module, "build_network", None)
    if builder is None:
        raise ValueError(f"{path} defines no build_network(n, m)")
    return builder


def grade(builder: Callable[[int, int], List[Edge]], sizes: Sequence[int], ratio: int, seed: int) -> float:
    """Run a builder over the contest sizes. Returns the mean of the per-size
    scores, and prints one line per size. An invalid network scores zero."""
    total = 0.0
    for n in sizes:
        m = ratio * n
        started = time.time()
        edges = [undirected(int(u), int(v)) for u, v in builder(n, m)]
        problems = validate(n, edges, expect_nodes=n, expect_edges=m)
        if problems:
            print(f"n = {n:4d}  m = {m:5d}  rejected: {'; '.join(problems)}")
            continue
        scores = score_network(adjacency(n, edges), seed=seed)
        total += scores["score"]
        print(
            f"n = {n:4d}  m = {m:5d}  "
            + "  ".join(f"{name}={scores[name]:.4f}" for name in GRADED_ATTACKS)
            + f"  score={scores['score']:.4f}  ({time.time() - started:.0f}s)"
        )
    mean = total / len(sizes)
    print(f"mean score over {len(sizes)} sizes: {mean:.4f}")
    return mean


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)

    build = sub.add_parser("design", help="build a robust network and score it")
    build.add_argument("--nodes", type=int, default=100)
    build.add_argument("--edges", type=int, default=200)
    build.add_argument("--iterations", type=int, default=600)
    build.add_argument("--seed", type=int, default=0)
    build.add_argument(
        "--fast",
        action="store_true",
        help="leave the betweenness attack out of the climb whatever the size: "
        "much quicker, and the network that comes out is easier to break",
    )
    build.add_argument("--out", default="edges.csv")
    build.add_argument("--quiet", action="store_true")

    check = sub.add_parser("score", help="score an edge list from a file")
    check.add_argument("--edges", required=True)
    check.add_argument("--seed", type=int, default=0)
    check.add_argument("--expect-nodes", type=int, default=None)
    check.add_argument("--expect-edges", type=int, default=None)

    run = sub.add_parser("grade", help="run a submitted build_network(n, m) over the contest sizes")
    run.add_argument("--module", required=True, help="path to a file defining build_network(n, m)")
    run.add_argument("--sizes", default="100,500")
    run.add_argument("--ratio", type=int, default=2, help="edges per node, so m = ratio * n")
    run.add_argument("--seed", type=int, default=0)

    sub.add_parser("selftest", help="check the R-index code against known cases")

    args = parser.parse_args(argv)

    if args.command == "selftest":
        selftest()
        return 0

    if args.command == "design":
        edges = design_network(
            args.nodes,
            args.edges,
            iterations=args.iterations,
            attacks=("random", "degree_adaptive") if args.fast else None,
            seed=args.seed,
            verbose=not args.quiet,
        )
        write_edges(args.out, edges)
        print(f"{args.nodes} nodes, {len(edges)} edges written to {args.out}")
        _report(adjacency(args.nodes, edges), args.seed)
        return 0

    if args.command == "grade":
        sizes = [int(part) for part in args.sizes.split(",")]
        grade(_load_builder(args.module), sizes, args.ratio, args.seed)
        return 0

    n, edges = read_edges(args.edges)
    problems = validate(n, edges, args.expect_nodes, args.expect_edges)
    if problems:
        for problem in problems:
            print(f"rejected: {problem}")
        return 1
    print(f"{n} nodes, {len(edges)} edges")
    _report(adjacency(n, edges), args.seed)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
