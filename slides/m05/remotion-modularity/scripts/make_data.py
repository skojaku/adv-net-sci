#!/usr/bin/env python3
"""Writes src/data/data.ts: every number and every random choice that the modularity deck shows.

Run:  python3 scripts/make_data.py
The slides never compute or draw anything random: they read this file. scripts/verify_numbers.py
recomputes the quoted numbers with networkx (an independent check).

The karate club (positions, edges, the two real factions) is the one of the Module 05 deck
(slides/m05/remotion/src/data/data.ts), read from there so that the two decks show the same drawing.
"""
import itertools
import json
import math
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
M05 = HERE.parent / 'remotion' / 'src' / 'data' / 'data.ts'
OUT = HERE / 'src' / 'data' / 'data.ts'

src = M05.read_text()


def arr(name):
    m = re.search(r'export const %s = (\[.*?\])(?: as|;)' % name, src, re.S)
    return json.loads(m.group(1))


POS = arr('KARATE_POS')
EDGES = arr('KARATE_EDGES')
REAL = arr('KARATE_REAL')  # 0 = Mr. Hi, 1 = Officer
N = len(POS)
M = len(EDGES)


def graph(n, edges):
    adj = [dict() for _ in range(n)]
    for u, v in edges:
        adj[u][v] = adj[u].get(v, 0) + 1
        adj[v][u] = adj[v].get(u, 0) + 1
    return adj


ADJ = graph(N, EDGES)
K = [sum(a.values()) for a in ADJ]
TWO_M = 2 * M
assert sum(K) == TWO_M


def modularity(lab, adj):
    """Q of a labelling of a weighted graph; adj[i][i] is a self-loop, which counts twice in the degree."""
    tot = sum(sum(a.values()) for a in adj)
    kk = [sum(a.values()) for a in adj]
    inside = sum(w for i in range(len(adj)) for j, w in adj[i].items() if lab[i] == lab[j])
    deg = {}
    for i, l in enumerate(lab):
        deg[l] = deg.get(l, 0) + kk[i]
    return inside / tot - sum((d / tot) ** 2 for d in deg.values())


def local_move(adj, lab, order, log):
    """Louvain's first phase: visit the nodes in `order` over and over; a node takes the label of the neighbouring group that raises Q the most, if any."""
    tot = sum(sum(a.values()) for a in adj)
    kk = [sum(a.values()) for a in adj]
    deg = {}
    for i, l in enumerate(lab):
        deg[l] = deg.get(l, 0) + kk[i]
    moved = True
    while moved:
        moved = False
        for v in order:
            old = lab[v]
            w = {}
            for u, x in adj[v].items():
                if u != v:
                    w[lab[u]] = w.get(lab[u], 0) + x
            deg[old] -= kk[v]

            def gain(c):
                return w.get(c, 0) - kk[v] * deg.get(c, 0) / tot

            best, bg = old, gain(old)
            for c in sorted(w):
                if gain(c) > bg + 1e-12:
                    best, bg = c, gain(c)
            deg[best] = deg.get(best, 0) + kk[v]
            if best != old:
                lab[v] = best
                moved = True
                log.append([v, old, best, round(modularity(lab, adj), 4)])


def aggregate(adj, lab):
    ids = sorted(set(lab))
    idx = {l: i for i, l in enumerate(ids)}
    new = [dict() for _ in ids]
    for i in range(len(adj)):
        for j, w in adj[i].items():
            a, b = idx[lab[i]], idx[lab[j]]
            new[a][b] = new[a].get(b, 0) + w
    return new, ids


def groups_of(lab):
    g = {}
    for i, l in enumerate(lab):
        g.setdefault(l, []).append(i)
    return g


def renumber(lab):
    """labels 0, 1, 2 ... in the order the groups are first met (node 0 is in group 0)"""
    seen = {}
    return [seen.setdefault(l, len(seen)) for l in lab]


data = {}

# ---- the club, two real factions ----
inside = sum(REAL[u] == REAL[v] for u, v in EDGES)
deg_group = [sum(K[i] for i in range(N) if REAL[i] == g) for g in (0, 1)]
data['INSIDE'] = inside
data['BETWEEN'] = M - inside
data['FRAC_INSIDE'] = round(inside / M, 4)
data['EXPECTED_FRAC'] = round(sum((d / TWO_M) ** 2 for d in deg_group), 4)
data['Q_REAL'] = round(modularity(REAL, ADJ), 4)
data['Q_ONE'] = round(modularity([0] * N, ADJ), 4)
data['Q_SINGLES'] = round(modularity(list(range(N)), ADJ), 4)
assert abs(data['FRAC_INSIDE'] - data['EXPECTED_FRAC'] - data['Q_REAL']) < 1e-3
data['DEG'] = K
data['TWO_M'] = TWO_M
data['PAIR_0_33'] = round(K[0] * K[33] / TWO_M, 4)  # more than one edge expected: not a probability
data['BELL_34'] = None  # filled below as a string

# ---- S03: the orange nodes join the blue group one at a time; the fraction of edges inside after each flip
lab = list(REAL)
flip_order, flip_inside = [], [inside]
while any(l == 1 for l in lab):
    best = None
    for v in range(N):
        if lab[v] != 1:
            continue
        trial = list(lab)
        trial[v] = 0
        ins = sum(trial[a] == trial[b] for a, b in EDGES)
        if best is None or ins > best[0]:
            best = (ins, v)
    lab[best[1]] = 0
    flip_order.append(best[1])
    flip_inside.append(best[0])
assert flip_inside[-1] == M
data['FLIP_ORDER'] = flip_order
data['FLIP_INSIDE'] = flip_inside


def bell(n):
    row = [1]
    for _ in range(n):
        new = [row[-1]]
        for x in row:
            new.append(new[-1] + x)
        row = new
    return row[0]


b34 = bell(34)
data['BELL_34'] = '%.1e' % b34  # 2.1e+28

# ---- S16 to S20: Louvain on the club, with one fixed visiting order ----
rng = random.Random(256)
order = list(range(N))
rng.shuffle(order)
lab0 = list(range(N))
log0 = []
local_move(ADJ, lab0, order, log0)
g0 = groups_of(lab0)
assert len(g0) == 5, len(g0)
q_stuck = round(modularity(lab0, ADJ), 4)
LAB0 = renumber(lab0)  # the stuck partition, groups 0..4
G0 = groups_of(LAB0)
data['ORDER'] = order
data['MOVES'] = log0  # [node, from label, to label, Q after]; labels are node numbers (each node starts with its own)
data['Q_STUCK'] = q_stuck
data['STUCK'] = LAB0

# no single move raises Q (that is what "stuck" means); the largest change is below 0
tot = TWO_M
best_single = None
for v in range(N):
    for c in set(LAB0) - {LAB0[v]}:
        trial = list(LAB0)
        trial[v] = c
        dq = modularity(trial, ADJ) - modularity(LAB0, ADJ)
        if best_single is None or dq > best_single[0]:
            best_single = (dq, v, c)
assert best_single[0] < 0, best_single

# merging two whole groups: which pair raises Q the most
best_merge = None
for a, b in itertools.combinations(sorted(set(LAB0)), 2):
    trial = [a if x == b else x for x in LAB0]
    dq = modularity(trial, ADJ) - modularity(LAB0, ADJ)
    if best_merge is None or dq > best_merge[0]:
        best_merge = (dq, a, b)
assert best_merge[0] > 0
data['MERGE_PAIR'] = [best_merge[1], best_merge[2]]
data['Q_MERGED'] = round(modularity([best_merge[1] if x == best_merge[2] else x for x in LAB0], ADJ), 4)
# the single move to show: a node of the group `b` moving into the group `a`, the least bad one
a, b = best_merge[1], best_merge[2]
best_node = None
for v in G0[b]:
    trial = list(LAB0)
    trial[v] = a
    dq = modularity(trial, ADJ) - q_stuck
    if best_node is None or dq > best_node[0]:
        best_node = (dq, v)
data['MOVE_NODE'] = [best_node[1], a, round(modularity([a if i == best_node[1] else x for i, x in enumerate(LAB0)], ADJ), 4)]
assert data['MOVE_NODE'][2] < q_stuck

# aggregation: 5 supernodes, weights = number of edge ends (a group's own edges are a self-loop counted twice)
agg, ids = aggregate(ADJ, LAB0)
assert ids == sorted(set(LAB0))
data['AGG_SIZE'] = [len(G0[g]) for g in range(5)]
data['AGG_W'] = [[agg[i].get(j, 0) for j in range(5)] for i in range(5)]  # W[i][i] = 2 x (edges inside group i)
assert sum(sum(r) for r in data['AGG_W']) == TWO_M
data['Q_AGG_SINGLES'] = round(modularity(list(range(5)), agg), 4)
assert data['Q_AGG_SINGLES'] == q_stuck

# the second level: the same local moving on the five supernodes
lab1 = list(range(5))
log1 = []
local_move(agg, lab1, list(range(5)), log1)
final = renumber([lab1[LAB0[v]] for v in range(N)])
data['L1_MOVES'] = log1  # [supernode, from, to, Q after]
data['L1'] = lab1
data['FINAL'] = final
data['Q_FINAL'] = round(modularity(final, ADJ), 4)
data['N_FINAL'] = len(set(final))
agg2, _ = aggregate(agg, lab1)
lab2 = list(range(len(agg2)))
log2 = []
local_move(agg2, lab2, list(range(len(agg2))), log2)
assert not log2  # a third level changes nothing: Louvain stops
data['L2_MOVES'] = log2
data['LEVEL_Q'] = [data['Q_SINGLES'], q_stuck, data['Q_FINAL']]

# ---- the toy (S05 to S11): a star joined to a triangle; degrees 3, 1, 1, 3, 2, 2 ----
# Lecturer: with (nearly) equal degrees the matrix of expected edges teaches nothing, so the degrees differ: two hubs (3), two leaves (1), two nodes of degree 2.
# node 0 is the hub of the star {0,1,2}; node 3 joins the triangle {3,4,5}; one edge between the groups (0-3)
TOY_POS = [[0.3, 0.5], [0.02, 0.14], [0.02, 0.86], [0.64, 0.5], [0.94, 0.14], [0.94, 0.86]]
TOY_EDGES = [[0, 1], [0, 2], [0, 3], [3, 4], [3, 5], [4, 5]]
toy_adj = graph(6, TOY_EDGES)
toy_k = [sum(a.values()) for a in toy_adj]
assert toy_k == [3, 1, 1, 3, 2, 2] and sum(toy_k) == 12
TOY_LAB = [0, 0, 0, 1, 1, 1]
data['TOY_POS'] = TOY_POS
data['TOY_EDGES'] = TOY_EDGES
data['TOY_DEG'] = toy_k
data['TOY_LAB'] = TOY_LAB
data['TOY_Q'] = round(modularity(TOY_LAB, toy_adj), 4)
data['TOY_E04'] = round(toy_k[0] * toy_k[4] / 12, 4)  # node 1 (hub) and node 5: 3 x 2 / 12 = 0.50 (S06, S07, S10)
data['TOY_E01'] = round(toy_k[0] * toy_k[1] / 12, 4)  # node 1 (hub) and node 2 (leaf): 3 x 1 / 12 = 0.25, and they are joined (S11)

# S05: the 12 stubs (node of each stub) and one random reconnection that is a simple, connected graph that shares 1 or 2 edges with the original
stubs = [v for v in range(6) for _ in range(toy_k[v])]
orig = {tuple(sorted(e)) for e in TOY_EDGES}
for seed in range(100000):
    r = random.Random(seed)
    idx = list(range(12))
    r.shuffle(idx)
    pairs = [(idx[2 * i], idx[2 * i + 1]) for i in range(6)]
    e = [tuple(sorted((stubs[a], stubs[b]))) for a, b in pairs]
    if any(a == b for a, b in e) or len(set(e)) < 6:
        continue
    if len(set(e) & orig) > 3:
        continue
    ins = sum(1 for a, b in e if TOY_LAB[a] == TOY_LAB[b])
    if ins != 3:  # the expected number of edges inside by chance is 6 x 0.514 = 3.1: a typical outcome
        continue
    g = graph(6, e)
    seen, st = {0}, [0]
    while st:
        u = st.pop()
        for v in g[u]:
            if v not in seen:
                seen.add(v)
                st.append(v)
    if len(seen) == 6:
        break
else:
    raise SystemExit('no rewiring found')
data['TOY_STUB_NODE'] = stubs
data['TOY_STUB_PAIRS'] = [list(p) for p in pairs]  # pairs of stub indices
data['TOY_REWIRED'] = [list(x) for x in e]
data['TOY_ORIG_INSIDE'] = sum(1 for a, b in TOY_EDGES if TOY_LAB[a] == TOY_LAB[b])
data['TOY_REWIRED_INSIDE'] = sum(1 for a, b in e if TOY_LAB[a] == TOY_LAB[b])

# ---- S21: a community whose two parts share no edge ----
BR_POS = [[0.05, 0.25], [0.05, 0.75], [0.25, 0.5], [0.62, 0.5], [0.82, 0.25], [0.82, 0.75], [0.43, 0.5]]
# nodes 0,1,2 and 3,4,5 are two triangles; node 6 is the bridge between them; D = triangle 7,8,9 attached to 6 on the right
BR_POS = [[0.0, 0.2], [0.0, 0.8], [0.2, 0.5], [0.6, 0.5], [0.8, 0.2], [0.8, 0.8], [0.4, 0.5]]
BR_EDGES = [[0, 1], [0, 2], [1, 2], [3, 4], [3, 5], [4, 5], [6, 2], [6, 3]]
# the third group D hangs off the bridge: nodes 7, 8, 9
BR_POS += [[1.05, 0.5], [1.3, 0.25], [1.3, 0.75]]
BR_EDGES += [[7, 8], [7, 9], [8, 9], [6, 7], [6, 8], [6, 9]]
# the bridge goes to the 3 edges on the right: in the picture it is drawn from the middle
br_adj = graph(10, BR_EDGES)
S0 = [0, 0, 0, 0, 0, 0, 0, 1, 1, 1]  # community C = {0..6}, community D = {7,8,9}
S1 = [0, 0, 0, 0, 0, 0, 1, 1, 1, 1]  # the bridge joins D: C = {0..5} is in two pieces
S2 = [0, 0, 0, 1, 1, 1, 2, 2, 2, 2]  # the pieces split (Leiden refines before it aggregates)
br_q = [round(modularity(s, br_adj), 4) for s in (S0, S1, S2)]
assert br_q[0] < br_q[1] < br_q[2], br_q
data['BR_POS'] = [[round(x / 1.3, 4), y] for x, y in BR_POS]
data['BR_EDGES'] = BR_EDGES
data['BR_S0'], data['BR_S1'], data['BR_S2'] = S0, S1, S2
data['BR_Q'] = br_q

# ---- write ----


def ts(name, value):
    if isinstance(value, str):
        return 'export const %s = %s;\n' % (name, json.dumps(value))
    typ = 'number'
    v = value
    depth = 0
    while isinstance(v, list):
        depth += 1
        v = v[0] if v else 0
    if isinstance(v, float) or isinstance(v, int):
        typ = 'number' + '[]' * depth if depth else 'number'
    return 'export const %s: %s = %s;\n' % (name, typ, json.dumps(value))


lines = ['// GENERATED by scripts/make_data.py. Do not edit: run the script again.\n']
lines += ['export const KARATE_POS: number[][] = %s;\n' % json.dumps(POS)]
lines += ['export const KARATE_EDGES: number[][] = %s;\n' % json.dumps(EDGES)]
lines += ['export const KARATE_REAL: number[] = %s; // 0 = Mr. Hi, 1 = Officer\n' % json.dumps(REAL)]
for k, v in data.items():
    lines.append(ts(k, v))
OUT.write_text(''.join(lines))
print('wrote', OUT.relative_to(HERE))
for k in ['INSIDE', 'BETWEEN', 'FRAC_INSIDE', 'EXPECTED_FRAC', 'Q_REAL', 'Q_ONE', 'Q_SINGLES', 'PAIR_0_33', 'BELL_34', 'Q_STUCK', 'MERGE_PAIR', 'Q_MERGED', 'MOVE_NODE', 'AGG_SIZE', 'Q_FINAL', 'N_FINAL', 'LEVEL_Q', 'TOY_Q', 'TOY_E04', 'TOY_E01', 'TOY_REWIRED', 'TOY_ORIG_INSIDE', 'TOY_REWIRED_INSIDE', 'BR_Q']:
    print(' ', k, data[k])
print('  moves level 0:', len(log0), ' level 1:', log1)
print('  flip inside:', flip_inside)
print('  stuck groups:', {g: v for g, v in G0.items()})
