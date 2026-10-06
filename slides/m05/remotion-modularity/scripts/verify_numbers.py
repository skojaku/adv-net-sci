#!/usr/bin/env python3
"""Recomputes with networkx (not with make_data.py's own code) every number that a slide quotes, from src/data/data.ts.
A number on a slide that no script computed is a bug. Run:  python3 scripts/verify_numbers.py   (exit code 1 if anything fails)
"""
import json
import re
import sys
from math import comb
from pathlib import Path

import networkx as nx

HERE = Path(__file__).resolve().parent.parent
src = (HERE / 'src' / 'data' / 'data.ts').read_text()


def get(name):
    m = re.search(r'export const %s(?::[^=]+)? = (.*?);(?: //.*)?\n' % name, src, re.S)
    return json.loads(m.group(1))


bad = []


def check(label, got, want, tol=5e-5):
    ok = abs(got - want) <= tol if isinstance(want, (int, float)) else got == want
    print(('ok   ' if ok else 'FAIL ') + label, got, want)
    if not ok:
        bad.append(label)


def Q(g, lab, weight=None):
    comms = {}
    for v, l in enumerate(lab):
        comms.setdefault(l, set()).add(v)
    return nx.community.modularity(g, list(comms.values()), weight=weight)


E = get('KARATE_EDGES')
REAL = get('KARATE_REAL')
G = nx.Graph()
G.add_edges_from(E)
n, M = G.number_of_nodes(), G.number_of_edges()
check('34 nodes', n, 34)
check('78 edges', M, 78)

inside = sum(REAL[u] == REAL[v] for u, v in E)
check('inside', inside, get('INSIDE'))
check('between', M - inside, get('BETWEEN'))
check('inside fraction', inside / M, get('FRAC_INSIDE'), 5e-4)
deg = dict(G.degree())
dg = [sum(deg[v] for v in range(n) if REAL[v] == g) for g in (0, 1)]
check('expected fraction (81/156)^2 + (75/156)^2', sum((d / (2 * M)) ** 2 for d in dg), get('EXPECTED_FRAC'), 5e-4)
check('Q two factions', Q(G, REAL), get('Q_REAL'))
check('Q one group', Q(G, [0] * n), get('Q_ONE'))
check('Q all alone', Q(G, list(range(n))), get('Q_SINGLES'))
check('Q = inside fraction - expected fraction', inside / M - sum((d / (2 * M)) ** 2 for d in dg), get('Q_REAL'))
check('k_0 * k_33 / 2M', deg[0] * deg[33] / (2 * M), get('PAIR_0_33'))
check('degree list', [deg[v] for v in range(n)], get('DEG'))

# S03: the orange nodes flip one at a time
lab = list(REAL)
ins = [inside]
for v in get('FLIP_ORDER'):
    assert lab[v] == 1
    lab[v] = 0
    ins.append(sum(lab[a] == lab[b] for a, b in E))
check('flip path', ins, get('FLIP_INSIDE'))
check('everyone in one group: 78 of 78', ins[-1], 78)

# Bell number
bell = [1]
row = [1]
for _ in range(34):
    new = [row[-1]]
    for x in row:
        new.append(new[-1] + x)
    row = new
check('Bell(34)', '%.1e' % row[0], get('BELL_34'))

# local moving: replay the moves, Q after each, each move raises Q
lab = list(range(n))
prev = Q(G, lab)
for v, old, new, q in get('MOVES'):
    assert lab[v] == old, (v, old, lab[v])
    lab[v] = new
    cur = Q(G, lab)
    assert cur > prev, ('move does not raise Q', v, prev, cur)
    assert abs(cur - q) < 5e-5, (v, cur, q)
    prev = cur
STUCK = get('STUCK')
groups = {}
for v, l in enumerate(lab):
    groups.setdefault(l, []).append(v)
mine = {}
for v, l in enumerate(STUCK):
    mine.setdefault(l, []).append(v)
check('replayed moves end in the STUCK partition', sorted(map(sorted, groups.values())), sorted(map(sorted, mine.values())))
check('Q after 36 moves', Q(G, STUCK), get('Q_STUCK'))
check('5 groups', len(set(STUCK)), 5)
# nothing raises Q by moving one node
q0 = Q(G, STUCK)
best = max(Q(G, [c if i == v else x for i, x in enumerate(STUCK)]) - q0 for v in range(n) for c in set(STUCK) - {STUCK[v]})
check('no single move raises Q (best change < 0)', best < 0, True)
a, b = get('MERGE_PAIR')
check('merge two groups', Q(G, [a if x == b else x for x in STUCK]), get('Q_MERGED'))
v, a2, qv = get('MOVE_NODE')
check('one node of the merging group moves', Q(G, [a2 if i == v else x for i, x in enumerate(STUCK)]), qv)
check('that move lowers Q', qv < q0, True)

# aggregation keeps Q
W = get('AGG_W')
Gagg = nx.Graph()
for i in range(5):
    for j in range(i, 5):
        if W[i][j]:
            # a self-loop of weight w/2 per direction: networkx counts a self-loop weight once in the sum but twice in the degree
            Gagg.add_edge(i, j, weight=W[i][j] / 2 if i == j else W[i][j])
check('aggregate: Q of the supernodes alone = Q before', Q(Gagg, list(range(5)), weight='weight'), q0)
check('group sizes', [len(mine[g]) for g in range(5)], get('AGG_SIZE'))
check('sum of W = 2M', sum(map(sum, W)), 2 * M)

FINAL = get('FINAL')
check('final Q', Q(G, FINAL), get('Q_FINAL'))
check('4 groups', len(set(FINAL)), 4)
check('the 4-group partition is the best that networkx Louvain finds (0.4198)', max(Q(G, [next(i for i, c in enumerate(cs) if v in c) for v in range(n)]) for cs in [nx.community.louvain_communities(G, seed=s) for s in range(20)]), get('Q_FINAL'))

# the toy
TE = get('TOY_EDGES')
T = nx.Graph()
T.add_edges_from(TE)
check('toy degrees', [T.degree(v) for v in range(6)], get('TOY_DEG'))
check('toy degrees are 3,1,1,3,2,2', get('TOY_DEG'), [3, 1, 1, 3, 2, 2])
check('toy: 6 edges', T.number_of_edges(), 6)
check('toy Q (groups {0,1,2} and {3,4,5})', Q(T, get('TOY_LAB')), get('TOY_Q'))
check('toy: nodes 1 and 5 (3 x 2) / 2M', T.degree(0) * T.degree(4) / 12, get('TOY_E04'))
check('toy: nodes 1 and 2 (3 x 1) / 2M', T.degree(0) * T.degree(1) / 12, get('TOY_E01'))
check('toy: edges inside the groups', sum(get('TOY_LAB')[a] == get('TOY_LAB')[b] for a, b in TE), get('TOY_ORIG_INSIDE'))
sn = get('TOY_STUB_NODE')
pairs = get('TOY_STUB_PAIRS')
check('stub list has the degrees', [sn.count(v) for v in range(6)], get('TOY_DEG'))
check('rewired = the pairs of stubs', sorted(tuple(sorted((sn[a], sn[b]))) for a, b in pairs), sorted(tuple(e) for e in get('TOY_REWIRED')))
R = nx.Graph()
R.add_edges_from(get('TOY_REWIRED'))
check('rewired: same degrees', [R.degree(v) for v in range(6)], get('TOY_DEG'))
check('rewired: 6 edges, no repeated edge', R.number_of_edges(), 6)
check('rewired: edges inside the two groups', sum(get('TOY_LAB')[a] == get('TOY_LAB')[b] for a, b in get('TOY_REWIRED')), get('TOY_REWIRED_INSIDE'))

# the constructed bridge example
B = nx.Graph()
B.add_edges_from(get('BR_EDGES'))
qs = [Q(B, get(k)) for k in ('BR_S0', 'BR_S1', 'BR_S2')]
for k, q, w in zip(('S0', 'S1', 'S2'), qs, get('BR_Q')):
    check('bridge example ' + k, q, w)
check('Q rises S0 < S1 < S2', qs[0] < qs[1] < qs[2], True)
S1 = get('BR_S1')
C = [v for v in range(10) if S1[v] == 0]
check('after the bridge leaves, group C is in two pieces', nx.number_connected_components(B.subgraph(C)), 2)

print('\nFAILED: ' + ', '.join(bad) if bad else '\nall numbers check out')
sys.exit(1 if bad else 0)
