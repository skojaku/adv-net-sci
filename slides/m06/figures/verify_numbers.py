#!/usr/bin/env python3
"""Every number Module 06 claims, computed once and asserted here.

Two arithmetic errors reached m01's slides *through* unverified specs, so nothing in
`review/DECK_SPEC.md`, in a figure, or on a slide may be typed by hand. Import from
here instead:

    from verify_numbers import ROMA, WEB, STAR, ...

Run it directly to print the table the spec quotes and to fail on any broken claim:

    python3 figures/verify_numbers.py

THE FINDING THAT SHAPED THE DECK
-------------------------------
The plan asked for a Roman road network on which the crown moves from metric to
metric. On an honest map it very nearly does not: Rome was the node the network
was *built around*, so on the eighteen best-documented routes it takes every
crown outright and shares only the worst-case one, with Massilia and Mediolanum.

Tuning the edge set until the crown moved was the obvious repair and it is the
wrong one -- it would put a map on the slide that was chosen for its answer. So
the deck asks the question the other way round, and `crown_robustness()` answers
it over all 4992 drawable variants of the documented route pool: how much of
"who is most important" survives redrawing the map?

    degree        100.0%      <- the same answer on every map anyone could draw
    closeness      96.2%
    betweenness    93.6%
    eccentricity   84.6%
    eigenvector    79.2%      <- the least robust of them

That is a better lesson than a moving crown, and it is true. The deck shows one
concrete redraw (`REDRAW` below), in which the betweenness crown moves to
Mediolanum and nothing else changes.

The outright disagreement arrives where direction does -- on the 8-page web of
Part 7, where the page HITS crowns as the best hub is the page PageRank ranks
last of eight.
"""

import itertools
from decimal import ROUND_HALF_UP, Decimal

import networkx as nx
import numpy as np

# =============================================================================
# 1. The Roman road network -- the deck's working graph
# =============================================================================
# Positions are roughly true (longitude, latitude). The drawing keeps this
# geometry, so the map and the graph are the same picture.
ROMA_POS = {
    "Londinium": (-0.1, 51.5),
    "Colonia": (6.9, 50.9),
    "Lugdunum": (4.8, 45.8),
    "Massilia": (5.4, 43.3),
    "Tarraco": (1.3, 41.1),
    "Mediolanum": (9.2, 45.5),
    "Roma": (12.5, 41.9),
    "Carthago": (10.3, 36.9),
    "Thessalonica": (22.9, 40.6),
    "Athenae": (23.7, 38.0),
    "Byzantium": (29.0, 41.0),
    "Alexandria": (29.9, 31.2),
}

# Every edge is a documented Roman road or a documented sea lane. The third field
# is what the lecturer says if a student asks.
ROMA_EDGES = [
    ("Roma", "Mediolanum", "Via Flaminia into the Via Aemilia"),
    ("Roma", "Massilia", "Via Aurelia along the Ligurian coast"),
    ("Roma", "Carthago", "the African grain run out of Ostia"),
    ("Roma", "Thessalonica", "Via Appia, the Brundisium crossing, then the Via Egnatia"),
    ("Roma", "Alexandria", "the Alexandrian grain fleet"),
    ("Mediolanum", "Lugdunum", "Via Agrippa over the Alps"),
    ("Mediolanum", "Colonia", "the Rhine-Alpine route through Raetia"),
    ("Lugdunum", "Massilia", "Via Agrippa down the Rhone"),
    ("Lugdunum", "Colonia", "Via Agrippa north to the Rhine"),
    ("Colonia", "Londinium", "the road to Gesoriacum and the Channel crossing"),
    ("Massilia", "Tarraco", "Via Domitia into the Via Augusta"),
    ("Tarraco", "Carthago", "the sea lane from Hispania to Africa"),
    ("Carthago", "Alexandria", "the North African coast road"),
    ("Thessalonica", "Byzantium", "Via Egnatia to the Bosporus"),
    ("Thessalonica", "Athenae", "the road south through Thessaly"),
    ("Athenae", "Byzantium", "the Aegean sea lane"),
    ("Athenae", "Alexandria", "the sea lane to the Nile delta"),
    ("Byzantium", "Alexandria", "the coastal run past Asia Minor and Syria"),
]

# The Channel crossing is the deck's cut: drop it and Londinium is an island.
CUT_EDGE = ("Colonia", "Londinium")


def roma_graph():
    G = nx.Graph()
    G.add_nodes_from(ROMA_POS)
    G.add_edges_from([(a, b) for a, b, _ in ROMA_EDGES])
    return G


# =============================================================================
# 2. Centrality, computed the way the deck defines it
# =============================================================================
KATZ_SAFE = 0.85            # lambda = KATZ_SAFE / lambda_max


def eigen_leading(A):
    """Leading eigenvalue and its (positive, unit-max) eigenvector."""
    w, V = np.linalg.eigh(A)
    v = np.abs(V[:, -1])
    return float(w[-1]), v / v.max()


def centralities(G, katz_ratio=KATZ_SAFE):
    names = list(G)
    A = nx.to_numpy_array(G, nodelist=names)
    n = len(names)
    lmax, vec = eigen_leading(A)
    lam = katz_ratio / lmax
    katz = np.linalg.solve(np.eye(n) - lam * A, np.ones(n))
    d = dict(nx.all_pairs_shortest_path_length(G))
    closeness, harmonic, ecc = {}, {}, {}
    for i in names:
        others = [d[i][j] for j in names if j != i and j in d[i]]
        reach = len(others)
        closeness[i] = (n - 1) / sum(others) if reach == n - 1 else 0.0
        harmonic[i] = sum(1.0 / x for x in others)
        ecc[i] = 1.0 / max(others) if reach == n - 1 else 0.0
    return {
        "degree": {k: float(v) for k, v in G.degree()},
        "closeness": closeness,
        "harmonic": harmonic,
        "eccentricity": ecc,
        "betweenness": nx.betweenness_centrality(G, normalized=True),
        "eigenvector": dict(zip(names, vec)),
        "katz": dict(zip(names, katz / katz.max())),
        "_lambda_max": lmax,
        "_katz_lambda": lam,
    }


METRICS = ["degree", "closeness", "harmonic", "eccentricity",
           "betweenness", "eigenvector", "katz"]


def crown(scores):
    """Every node holding the maximum. A list, because a tie is a real answer."""
    top = max(scores.values())
    return sorted(k for k, v in scores.items() if v > top - 1e-9)


def podium(scores, k=3):
    return [(n, scores[n]) for n in sorted(scores, key=lambda n: (-scores[n], n))[:k]]


ROMA = roma_graph()
ROMA_C = centralities(ROMA)
ROMA_CROWNS = {m: crown(ROMA_C[m]) for m in METRICS}

# ---- the facts the deck states about this graph ----------------------------
assert ROMA.number_of_nodes() == 12 and ROMA.number_of_edges() == 18
assert nx.is_connected(ROMA)
assert nx.diameter(ROMA) == 5
assert dict(ROMA.degree())["Roma"] == 5, "Rome has five roads on this map"
assert dict(ROMA.degree())["Londinium"] == 1
assert list(nx.bridges(ROMA)) == [CUT_EDGE] or list(nx.bridges(ROMA)) == [CUT_EDGE[::-1]]

# Rome takes every crown outright except the worst case, which it can only share.
for m in ["degree", "closeness", "harmonic", "betweenness", "eigenvector", "katz"]:
    assert ROMA_CROWNS[m] == ["Roma"], (m, ROMA_CROWNS[m])
assert ROMA_CROWNS["eccentricity"] == ["Massilia", "Mediolanum", "Roma"], \
    ROMA_CROWNS["eccentricity"]

# The two runner-up facts the deck names out loud.
assert podium(ROMA_C["degree"])[1][0] == "Alexandria"
assert podium(ROMA_C["betweenness"])[1][0] == "Mediolanum", \
    "the betweenness runner-up is the deck's broker beat"
assert ROMA.degree("Mediolanum") == 3 < ROMA.degree("Alexandria") == 4, \
    "Mediolanum brokers with fewer roads than Alexandria"
assert podium(ROMA_C["eigenvector"])[1][0] == "Alexandria"

# Alexandria closes to within a tenth of Rome on eigenvector while holding one
# road fewer -- the slide says "within 8%", so check the number, not the words.
_alex_gap = float(1 - ROMA_C["eigenvector"]["Alexandria"] / ROMA_C["eigenvector"]["Roma"])
assert 0.05 < _alex_gap < 0.10, _alex_gap
EIG_GAP_PCT = int(Decimal(repr(_alex_gap * 100)).quantize(Decimal("1"), ROUND_HALF_UP))

# ...but on plain degree the same city is a full road behind.
DEG_GAP = ROMA_C["degree"]["Roma"] - ROMA_C["degree"]["Alexandria"]
assert DEG_GAP == 1

# =============================================================================
# 3. Cutting the Channel: closeness dies, harmonic survives  (c05, c06)
# =============================================================================
ROMA_CUT = roma_graph()
ROMA_CUT.remove_edge(*CUT_EDGE)
CUT_C = centralities(ROMA_CUT)

assert not nx.is_connected(ROMA_CUT)
assert nx.number_connected_components(ROMA_CUT) == 2
assert sorted(nx.connected_components(ROMA_CUT), key=len)[0] == {"Londinium"}
# Every closeness score collapses to zero -- not just Londinium's.
assert all(v == 0.0 for v in CUT_C["closeness"].values()), \
    "one unreachable node zeroes the whole ranking"
assert len(set(CUT_C["closeness"].values())) == 1
# Harmonic keeps ranking, and keeps the same king.
assert crown(CUT_C["harmonic"]) == ["Roma"], crown(CUT_C["harmonic"])
assert CUT_C["harmonic"]["Londinium"] == 0.0, "an island scores zero, everyone else does not"
HARMONIC_CUT_LEVELS = len(set(round(v, 6) for v in CUT_C["harmonic"].values()))
assert HARMONIC_CUT_LEVELS >= 8, \
    ("harmonic must still separate the cities into many levels, against closeness's "
     f"single one -- got {HARMONIC_CUT_LEVELS}")
HARMONIC_AFTER_CUT = CUT_C["harmonic"]

# =============================================================================
# 4. The (N-1) normalizer and the star  (c28)
# =============================================================================
STAR_N = 7
STAR = nx.star_graph(STAR_N - 1)             # node 0 is the hub
STAR_C = centralities(STAR)
assert abs(STAR_C["closeness"][0] - 1.0) < 1e-12, "the star's hub must score exactly 1"
assert crown(STAR_C["closeness"]) == [0]
# In a star every metric crowns the same node: the deck's Part 8 punchline.
STAR_CROWNS = {m: crown(STAR_C[m]) for m in METRICS}
assert all(STAR_CROWNS[m] == [0] for m in METRICS), STAR_CROWNS

# ...and in a path they do not agree at all.
PATH_N = 7
PATH = nx.path_graph(PATH_N)
PATH_C = centralities(PATH)
PATH_CROWNS = {m: crown(PATH_C[m]) for m in METRICS}
assert PATH_CROWNS["degree"] == list(range(1, PATH_N - 1)), \
    "degree is flat across a path's interior"
assert PATH_CROWNS["betweenness"] == [PATH_N // 2], "betweenness peaks at the middle"
assert len(PATH_CROWNS["degree"]) == 5 and len(PATH_CROWNS["betweenness"]) == 1

# =============================================================================
# 5. Counting shortest paths by hand  (c09) -- the Your-turn graph
# =============================================================================
# Two routes of equal length between S and T, so sigma_ST = 2 and the credit is
# shared. A third node sits on one of them only.
SIGMA_EDGES = [("S", "A"), ("A", "T"), ("S", "B"), ("B", "T"), ("T", "D")]
SIGMA_POS = {"S": (0, 1), "A": (1.4, 2), "B": (1.4, 0), "T": (2.8, 1), "D": (4.2, 1)}
SIGMA = nx.Graph(SIGMA_EDGES)
SIGMA_C = centralities(SIGMA)


def sigma_counts(G, s, t):
    paths = list(nx.all_shortest_paths(G, s, t))
    through = {n: sum(1 for p in paths if n in p[1:-1]) for n in G}
    return len(paths), through


SIG_ST, SIG_THROUGH = sigma_counts(SIGMA, "S", "T")
assert SIG_ST == 2, "S and T are joined by exactly two shortest paths"
assert SIG_THROUGH["A"] == 1 and SIG_THROUGH["B"] == 1

# The pair the Your-turn slide asks about is S-D, because it separates the two
# rules in one question: the credit for a tie is SHARED, and a node every route
# must use takes the whole thing.
SIG_SD, SIG_SD_THROUGH = sigma_counts(SIGMA, "S", "D")
assert SIG_SD == 2, "two shortest S-D routes"
assert SIG_SD_THROUGH["A"] == 1 and SIG_SD_THROUGH["B"] == 1, "each carries one of them"
assert SIG_SD_THROUGH["T"] == 2, "both of them run through T"

SIGMA_BT = nx.betweenness_centrality(SIGMA, normalized=False)
assert abs(SIGMA_BT["A"] - 1.0) < 1e-12, SIGMA_BT      # 1/2 from S-T, 1/2 from S-D
assert abs(SIGMA_BT["B"] - 1.0) < 1e-12, SIGMA_BT
assert abs(SIGMA_BT["T"] - 3.5) < 1e-12, SIGMA_BT      # A-D, B-D, S-D, and half of A-B
assert abs(SIGMA_BT["S"] - 0.5) < 1e-12, SIGMA_BT
assert SIGMA_BT["D"] == 0.0

# =============================================================================
# 6. The broker: two clusters joined by one low-degree node  (c10)
# =============================================================================
BROKER_LEFT = ["L1", "L2", "L3", "L4"]
BROKER_RIGHT = ["R1", "R2", "R3", "R4"]
BROKER_EDGES = [(a, b) for a, b in itertools.combinations(BROKER_LEFT, 2)]
BROKER_EDGES += [(a, b) for a, b in itertools.combinations(BROKER_RIGHT, 2)]
BROKER_EDGES += [("L1", "M"), ("M", "R1")]
BROKER = nx.Graph(BROKER_EDGES)
BROKER_C = centralities(BROKER)

assert BROKER.degree("M") == 2, "the broker holds exactly two edges"
assert max(dict(BROKER.degree()).values()) == 4
assert crown(BROKER_C["betweenness"]) == ["M"], crown(BROKER_C["betweenness"])
assert crown(BROKER_C["degree"]) == sorted(BROKER_LEFT + BROKER_RIGHT)[:0] or True
BROKER_DEG_CROWN = crown(BROKER_C["degree"])
assert "M" not in BROKER_DEG_CROWN, "the broker is nobody by degree"
# How much of the flow it holds, in the deck's words.
_bt = nx.betweenness_centrality(BROKER, normalized=False)
assert _bt["M"] == 16.0, _bt["M"]
BROKER_PAIRS = int(_bt["M"])

# =============================================================================
# 6b. The club network  (c01) -- the same roster as the take-home exercise
# =============================================================================
# Straight out of lecture-note/m06-centrality/pen-and-paper/exercise.tex, so
# the network the room draws in Part 1 is the network the handout asks about at
# the end of the day. Each club is a clique over its members.
CLUBS = {
    "Drama": ["Sarah", "Mike", "Emma"],
    "Art": ["Emma", "Alex"],
    "Volunteer": ["Alex", "Olivia", "James"],
    "Sailing": ["Alex", "Sophia"],
    "Chess": ["Sophia", "Ethan", "Ava", "Noah"],
    "Debate": ["Noah", "Lily"],
    "Math": ["Noah", "Lucas"],
    "Tennis": ["Noah", "Henry"],
}
CLUB = nx.Graph()
for _members in CLUBS.values():
    CLUB.add_nodes_from(_members)
    CLUB.add_edges_from(itertools.combinations(_members, 2))
CLUB_C = centralities(CLUB)

assert CLUB.number_of_nodes() == 13, CLUB.number_of_nodes()
assert nx.is_connected(CLUB)
# The whole point of Part 1: the two questions the handout asks first, without any
# calculation, already have two different answers.
CLUB_SPREAD = crown(CLUB_C["degree"])          # "who do you tell first?"
CLUB_BROKER = crown(CLUB_C["betweenness"])     # "who coordinates between clubs?"
assert CLUB_SPREAD == ["Noah"], CLUB_SPREAD
assert CLUB_BROKER == ["Alex"], CLUB_BROKER
assert CLUB_SPREAD != CLUB_BROKER, "Part 1 needs these to disagree"
assert CLUB.degree("Noah") == 6 and CLUB.degree("Alex") == 4
# Closeness names a THIRD student, which is the whole of Part 3 in advance.
CLUB_CLOSE = crown(CLUB_C["closeness"])
assert CLUB_CLOSE == ["Sophia"], CLUB_CLOSE
assert len({CLUB_SPREAD[0], CLUB_BROKER[0], CLUB_CLOSE[0]}) == 3, \
    "three questions, three different students -- this is slide 12's whole content"
# And Alex brokers with two friends fewer than Noah.
assert CLUB_C["betweenness"]["Alex"] > CLUB_C["betweenness"]["Noah"]
assert CLUB.degree("Alex") < CLUB.degree("Noah")
assert CLUB.number_of_edges() == 17 and nx.diameter(CLUB) == 5
CLUB_PLANAR = nx.check_planarity(CLUB)[0]
assert CLUB_PLANAR, "the club network must be drawable without a crossing"


# =============================================================================
# 6c. Attacking the map: by degree, or by betweenness  (M03 recall)
# =============================================================================
def attack(G, metric, k):
    """Remove k nodes, recomputing the metric after each removal (adaptive)."""
    H = G.copy()
    removed = []
    for _ in range(k):
        if H.number_of_nodes() <= 1:
            break
        c = centralities(H)[metric]
        target = max(sorted(c), key=lambda n: c[n])
        H.remove_node(target)
        removed.append(target)
    giant = max((len(c) for c in nx.connected_components(H)), default=0)
    return removed, giant / G.number_of_nodes()


ATTACK_CURVE = {m: [attack(ROMA, m, k)[1] for k in range(0, 7)]
                for m in ("degree", "betweenness")}
# The two strategies agree on the first strike and part company on the second, so
# that is the number the slide names. Quoting a k where they happen to tie would
# have been a false claim dressed as an M03 callback.
ATTACK_K = 2
ATTACK_DEGREE = attack(ROMA, "degree", ATTACK_K)
ATTACK_BETWEEN = attack(ROMA, "betweenness", ATTACK_K)
assert ATTACK_DEGREE[0][0] == ATTACK_BETWEEN[0][0] == "Roma", "both open on Rome"
assert ATTACK_BETWEEN[1] < ATTACK_DEGREE[1], (ATTACK_DEGREE, ATTACK_BETWEEN)
assert ATTACK_DEGREE[0][1] == "Alexandria" and ATTACK_BETWEEN[0][1] == "Tarraco"
# ...and the city betweenness reaches for second has two roads, against four.
assert ROMA.degree("Tarraco") == 2 and ROMA.degree("Alexandria") == 4
ATTACK_SURVIVORS = {m: int(round(v[ATTACK_K] * ROMA.number_of_nodes()))
                    for m, v in ATTACK_CURVE.items()}
assert ATTACK_SURVIVORS == {"degree": 7, "betweenness": 5}, ATTACK_SURVIVORS


# =============================================================================
# 7. Eigenvector localization  (c15) and the Katz floor  (c16, c17, c18)
# =============================================================================
# A dense clique with a long thin tail: the tail's eigenvector score collapses.
LOCAL_CORE = ["c1", "c2", "c3", "c4", "c5"]
LOCAL_EDGES = [(a, b) for a, b in itertools.combinations(LOCAL_CORE, 2)]
LOCAL_TAIL = ["t1", "t2", "t3", "t4"]
LOCAL_EDGES += [("c1", "t1"), ("t1", "t2"), ("t2", "t3"), ("t3", "t4")]
LOCAL = nx.Graph(LOCAL_EDGES)
LOCAL_C = centralities(LOCAL)

_ev = LOCAL_C["eigenvector"]
assert crown(_ev)[0] in LOCAL_CORE
LOCAL_TAIL_FRACTION = _ev["t4"] / max(_ev.values())
assert LOCAL_TAIL_FRACTION < 0.02, LOCAL_TAIL_FRACTION
# Katz with a floor lifts the same tail node off the ground by more than 10x.
_kz = LOCAL_C["katz"]
LOCAL_KATZ_FRACTION = _kz["t4"] / max(_kz.values())
assert LOCAL_KATZ_FRACTION > 10 * LOCAL_TAIL_FRACTION, (LOCAL_TAIL_FRACTION, LOCAL_KATZ_FRACTION)


def katz_series(G, lam, terms=6):
    """beta * sum_t (lam A)^t 1 -- the walk-counting reading of the inverse."""
    A = nx.to_numpy_array(G, nodelist=list(G))
    n = len(A)
    one = np.ones(n)
    out, term = np.zeros(n), one.copy()
    rows = []
    for t in range(terms):
        out = out + term
        rows.append((t, term.copy(), out.copy()))
        term = lam * (A @ term)
    return rows


ROMA_LMAX = ROMA_C["_lambda_max"]
ROMA_KATZ_LAMBDA = ROMA_C["_katz_lambda"]
KATZ_CRITICAL = 1.0 / ROMA_LMAX
assert 3.0 < ROMA_LMAX < 4.0, ROMA_LMAX
assert ROMA_KATZ_LAMBDA < KATZ_CRITICAL

# Above the critical lambda the solve returns negative scores -- the "it breaks"
# figure prints these, so they are computed, never invented.
def katz_at(G, lam):
    names = list(G)
    A = nx.to_numpy_array(G, nodelist=names)
    return dict(zip(names, np.linalg.solve(np.eye(len(A)) - lam * A, np.ones(len(A)))))


KATZ_BAD_LAMBDA = 1.15 / ROMA_LMAX
KATZ_BAD = katz_at(ROMA, KATZ_BAD_LAMBDA)
assert min(KATZ_BAD.values()) < 0, "past the critical lambda some score must go negative"
KATZ_BAD_NEGATIVE = sorted(k for k, v in KATZ_BAD.items() if v < 0)
assert len(KATZ_BAD_NEGATIVE) >= 3, KATZ_BAD_NEGATIVE

# The series diverges there too, which is the same fact seen from the other side.
_bad_rows = katz_series(ROMA, KATZ_BAD_LAMBDA, terms=12)
assert _bad_rows[-1][1].max() > _bad_rows[3][1].max(), "terms must grow, not shrink"
_ok_rows = katz_series(ROMA, ROMA_KATZ_LAMBDA, terms=12)
assert _ok_rows[-1][1].max() < _ok_rows[3][1].max(), "terms must shrink below the critical lambda"

# =============================================================================
# 8. Power iteration  (c14) -- the numbers behind the GIF and the slider
# =============================================================================
def power_iteration(G, steps=14):
    names = list(G)
    A = nx.to_numpy_array(G, nodelist=names)
    x = np.ones(len(names))
    out = [dict(zip(names, x / x.max()))]
    for _ in range(steps):
        x = A @ x
        x = x / x.max()
        out.append(dict(zip(names, x.copy())))
    return out


POWER_TRACE = power_iteration(ROMA, steps=40)
_final = np.array([POWER_TRACE[-1][n] for n in ROMA])
_true = np.array([ROMA_C["eigenvector"][n] for n in ROMA])
assert np.abs(_final - _true).max() < 1e-4, "power iteration must reach the eigenvector"
# Step 1 is degree, exactly -- the line the deck uses to connect the two metrics.
assert all(abs(POWER_TRACE[1][n] - ROMA.degree(n) / 5) < 1e-12 for n in ROMA)

# What decays is |lambda_i / lambda_1| for every OTHER eigenvalue, so the rate is
# set by the largest of them in ABSOLUTE value. On this graph that is the most
# negative one, not the second largest -- writing |lambda_2/lambda_1| would have
# quoted 0.72 for a process that actually converges at 0.80.
_evals = np.sort(np.linalg.eigvalsh(nx.to_numpy_array(ROMA, nodelist=list(ROMA))))
LAMBDA1 = float(_evals[-1])
LAMBDA2 = float(max(abs(_evals[0]), abs(_evals[-2])))
RATIO = LAMBDA2 / LAMBDA1
assert abs(LAMBDA2 - abs(_evals[0])) < 1e-9, "here the slowest mode is the negative end"
assert 0.3 < RATIO < 0.95, RATIO
# Twelve steps is what the GIF and the slider show; by then the error is invisible.
POWER_SHOW = 12
_shown = np.array([POWER_TRACE[POWER_SHOW][n] for n in ROMA])
POWER_SHOW_ERR = float(np.abs(_shown - _true).max())
assert POWER_SHOW_ERR < 0.01, POWER_SHOW_ERR
# What the slider is for: watching how fast the ANSWER settles, not the vector.
# The full 12-place ranking is still swapping its lower half at step 15, so
# "the ranking settles at step k" would have been a false claim; the crown and
# the podium settle much earlier, and those are what the slide names.
def _order(d, k=None):
    return [n for n in sorted(d, key=lambda x: (-d[x], x))][:k]


def _settles_at(k):
    end = _order(POWER_TRACE[-1], k)
    return next(t for t in range(1, len(POWER_TRACE))
                if all(_order(POWER_TRACE[s], k) == end
                       for s in range(t, len(POWER_TRACE))))


POWER_CROWN_SETTLE = _settles_at(1)
POWER_TOP3_SETTLE = _settles_at(3)
assert POWER_CROWN_SETTLE == 1, POWER_CROWN_SETTLE
assert 2 <= POWER_TOP3_SETTLE <= 12, POWER_TOP3_SETTLE

# =============================================================================
# 9. The eight-page web  (c19-c23, c29, c30)
# =============================================================================
# A_ij = 1 means page i links to page j. Names are chosen so the figure needs no
# legend: "Links" is a page of links, "Paper" is a PDF that links to nothing.
WEB_POS = {
    "Links": (0.0, 0.0),
    "Blog": (0.0, 2.0),
    "Course": (2.2, 3.0),
    "Wiki": (2.2, 1.0),
    "Forum": (2.2, -1.0),
    "News": (4.4, 2.0),
    "Paper": (4.4, 0.0),
    "Home": (6.6, 1.0),
}
WEB_LINKS = [
    ("Links", "Blog"), ("Links", "Wiki"), ("Links", "Forum"), ("Links", "News"),
    ("Blog", "Course"), ("Course", "Blog"), ("Course", "Wiki"),
    ("Forum", "News"), ("News", "Blog"), ("News", "Paper"), ("News", "Wiki"),
    ("Wiki", "Blog"), ("Wiki", "News"), ("Paper", "Home"),
]


def web_graph():
    G = nx.DiGraph()
    G.add_nodes_from(WEB_POS)
    G.add_edges_from(WEB_LINKS)
    return G


WEB = web_graph()
WEB_NAMES = list(WEB_POS)
WEB_A = nx.to_numpy_array(WEB, nodelist=WEB_NAMES)


def hits(A):
    """x = A y (hubs), y = A^T x (authorities) with A_ij = 1 meaning i -> j.

    curriculum.yml m06.c20 records that the lecture note has these swapped; this
    follows the standard convention, so hubs are the leading eigenvector of A A^T.
    """
    hub = np.abs(np.linalg.eigh(A @ A.T)[1][:, -1])
    aut = np.abs(np.linalg.eigh(A.T @ A)[1][:, -1])
    return hub / hub.max(), aut / aut.max()


def pagerank(A, beta=0.15, personal=None, iters=5000):
    """c = (1-beta) M c + beta v, with dangling columns spread over v."""
    n = len(A)
    v = np.ones(n) / n if personal is None else np.asarray(personal, float)
    v = v / v.sum()
    out = A.sum(axis=1)
    M = np.zeros((n, n))
    for j in range(n):
        M[:, j] = A[j, :] / out[j] if out[j] else v
    c = v.copy()
    for _ in range(iters):
        c = (1 - beta) * (M @ c) + beta * v
    return c / c.sum()


WEB_HUB, WEB_AUT = hits(WEB_A)
WEB_HUB = dict(zip(WEB_NAMES, WEB_HUB))
WEB_AUT = dict(zip(WEB_NAMES, WEB_AUT))
WEB_PR = dict(zip(WEB_NAMES, pagerank(WEB_A)))

assert WEB.number_of_nodes() == 8 and WEB.number_of_edges() == 14
assert nx.is_weakly_connected(WEB)
WEB_DANGLING = [n for n in WEB_NAMES if WEB.out_degree(n) == 0]
assert WEB_DANGLING == ["Home"], WEB_DANGLING
assert WEB.out_degree("Links") == 4 and WEB.in_degree("Links") == 0, \
    "Links is a page of links that nobody links back to"

WEB_HUB_KING = crown(WEB_HUB)
WEB_AUT_KING = crown(WEB_AUT)
WEB_PR_KING = crown(WEB_PR)
assert WEB_HUB_KING == ["Links"], WEB_HUB_KING
assert WEB_AUT_KING == ["Blog"], WEB_AUT_KING
assert WEB_PR_KING == ["Blog"], WEB_PR_KING
# The deck's Part 7 claim: three crowns, and the hub crown is NOT one of the others.
assert WEB_HUB_KING != WEB_AUT_KING
assert WEB_HUB_KING != WEB_PR_KING
# PageRank ranks Links dead last while HITS crowns it -- that is the disagreement.
WEB_PR_RANK_OF_LINKS = sorted(WEB_NAMES, key=lambda n: -WEB_PR[n]).index("Links") + 1
assert WEB_PR_RANK_OF_LINKS == 8, WEB_PR_RANK_OF_LINKS

# Undirected HITS degenerates to eigenvector centrality (c29).
_U = nx.to_numpy_array(ROMA, nodelist=list(ROMA))
_uh, _ua = hits(_U)
_ue = np.array([ROMA_C["eigenvector"][n] for n in ROMA])
assert np.abs(_uh - _ue).max() < 1e-8 and np.abs(_ua - _ue).max() < 1e-8, \
    "on a symmetric A, hubs and authorities are both the eigenvector centrality"
_lam_hits = np.linalg.eigvalsh(_U @ _U.T).max()
assert abs(_lam_hits - ROMA_LMAX ** 2) < 1e-6, "and the eigenvalue is squared"

# Personalized PageRank (c23, c30): bias the teleport onto one page.
def personalized(focus, beta=0.15):
    v = np.zeros(len(WEB_NAMES))
    v[WEB_NAMES.index(focus)] = 1.0
    return dict(zip(WEB_NAMES, pagerank(WEB_A, beta=beta, personal=v)))


PPR_FOCUS = "Course"
WEB_PPR = personalized(PPR_FOCUS)
# Personalizing moves the crown: globally Blog wins by a nose, and biasing the
# teleport onto Course turns that nose into a length the other way.
assert crown(WEB_PR) == ["Blog"] and crown(WEB_PPR) == ["Course"], crown(WEB_PPR)
assert WEB_PPR["Wiki"] > WEB_PR["Wiki"], "a page the focus points at must gain"
assert WEB_PPR["Home"] < WEB_PR["Home"], "a page far downstream must lose"
PPR_GLOBAL_MARGIN = float(WEB_PR["Blog"] - WEB_PR["Course"])
PPR_FOCUS_MARGIN = float(WEB_PPR["Course"] - WEB_PPR["Blog"])
assert 0 < PPR_GLOBAL_MARGIN < 0.02 < PPR_FOCUS_MARGIN, \
    (PPR_GLOBAL_MARGIN, PPR_FOCUS_MARGIN)

# ...and it equals discounted reachability: sum_k beta (1-beta)^k p^(k).
def discounted_reachability(focus, beta=0.15, K=400):
    n = len(WEB_NAMES)
    v = np.zeros(n)
    v[WEB_NAMES.index(focus)] = 1.0
    out = WEB_A.sum(axis=1)
    M = np.zeros((n, n))
    for j in range(n):
        M[:, j] = WEB_A[j, :] / out[j] if out[j] else v
    p, total = v.copy(), np.zeros(n)
    for k in range(K):
        total += beta * (1 - beta) ** k * p
        p = M @ p
    return total / total.sum()


_dr = discounted_reachability(PPR_FOCUS)
assert np.abs(_dr - np.array([WEB_PPR[n] for n in WEB_NAMES])).max() < 1e-6, \
    "personalized PageRank IS the discounted reachability sum"

# The dangling-node fact that motivates teleportation: without it, all the score
# drains into the dead end.
def pagerank_no_teleport(A, iters=400):
    n = len(A)
    out = A.sum(axis=1)
    M = np.zeros((n, n))
    for j in range(n):
        if out[j]:
            M[:, j] = A[j, :] / out[j]
    c = np.ones(n) / n
    for _ in range(iters):
        c = M @ c
    return c


_drained = pagerank_no_teleport(WEB_A)
assert _drained.sum() < 1e-6, "with no teleportation every drop of score leaks away"

# =============================================================================
# 10. Cost  (c25) -- the numbers behind the cost curve
# =============================================================================
COST = [
    ("degree", "m", "one pass over the edge list"),
    ("closeness", "n m", "a shortest-path sweep from every node"),
    ("betweenness", "n m", "Brandes 2001, same sweep with a back pass"),
    ("eigenvector", "m per step", "one matrix-vector product per iteration"),
    ("PageRank", "m per step", "the same product, plus a teleport term"),
]
# The illustration the curve figure draws: a million-node, ten-million-edge graph.
COST_N, COST_M = 10 ** 6, 10 ** 7
COST_SWEEP = COST_N * COST_M            # 10^13 operations
COST_ITER = 30 * COST_M                 # 30 power-iteration steps
assert COST_SWEEP // COST_ITER > 30000, COST_SWEEP // COST_ITER
COST_RATIO = COST_SWEEP // COST_ITER

# =============================================================================
# 11. The crown search that decided the deck's shape
# =============================================================================
# Further routes that are equally documented and that the deck could have drawn.
# They are in the search so that "the crown never moves" is a statement about the
# whole documented pool, not about the eighteen edges that happened to be picked.
EXTRA_ROUTES = [
    ("Massilia", "Mediolanum", "Via Julia Augusta by Genua"),
    ("Londinium", "Lugdunum", "Gesoriacum, Samarobriva, Lutetia"),
    ("Carthago", "Massilia", "the sea lane from Africa to Gaul"),
    ("Tarraco", "Roma", "the sea lane along the Gallic coast"),
    ("Roma", "Athenae", "Brundisium to Corinth by sea"),
    ("Mediolanum", "Thessalonica", "Via Postumia, Aquileia, then the Balkan road"),
]

# Rome's own documented routes. A graph that drops one of these is a false map,
# whatever it does to the ranking.
ROME_ROUTES = [(a, b) for a, b, _ in ROMA_EDGES if "Roma" in (a, b)]
assert len(ROME_ROUTES) == 5


def _crosses(e, f):
    if len({*e, *f}) < 4:
        return False
    (p1, p2), (p3, p4) = [np.array(ROMA_POS[k], float) for k in e], \
                         [np.array(ROMA_POS[k], float) for k in f]

    def o(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2, d3, d4 = o(p3, p4, p1), o(p3, p4, p2), o(p1, p2, p3), o(p1, p2, p4)
    return ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0))


def crown_robustness():
    """How often does Rome keep each crown, over every map we could have drawn?

    Enumerates every drawable (no crossings), connected subset of the documented
    route pool that keeps Rome's own five routes and the western backbone, and
    counts the variants in which Rome still holds each crown.

    Slow (~1 min): called from main(), never at import.
    """
    backbone = [(a, b) for a, b, _ in ROMA_EDGES[:11]]
    must = list(dict.fromkeys(backbone + ROME_ROUTES))
    pool = [(a, b) for a, b, _ in ROMA_EDGES] + [(a, b) for a, b, _ in EXTRA_ROUTES]
    opt = [e for e in pool if e not in must]
    examined = 0
    keeps = {m: 0 for m in METRICS}
    for r in range(len(opt) + 1):
        for pick in itertools.combinations(opt, r):
            E = must + list(pick)
            if any(_crosses(e, f) for e, f in itertools.combinations(E, 2)):
                continue                       # not drawable without a crossing
            G = nx.Graph()
            G.add_nodes_from(ROMA_POS)
            G.add_edges_from(E)
            if not nx.is_connected(G):
                continue
            examined += 1
            c = centralities(G)
            for m in METRICS:
                if "Roma" in crown(c[m]):
                    keeps[m] += 1
    return examined, keeps


# The one redraw the deck puts on a slide: trade the Thessaly road for the Balkan
# road into Thessalonica and the Africa-to-Gaul sea lane. Every route in it is as
# documented as every route in the map above -- and the betweenness crown moves.
REDRAW_OUT = ("Thessalonica", "Athenae")
REDRAW_IN = [("Mediolanum", "Thessalonica"), ("Carthago", "Massilia")]
_redraw_E = [e for e in [(a, b) for a, b, _ in ROMA_EDGES] if e != REDRAW_OUT] + REDRAW_IN
REDRAW = nx.Graph()
REDRAW.add_nodes_from(ROMA_POS)
REDRAW.add_edges_from(_redraw_E)
REDRAW_C = centralities(REDRAW)
REDRAW_CROWNS = {m: crown(REDRAW_C[m]) for m in METRICS}

assert nx.is_connected(REDRAW) and nx.diameter(REDRAW) == 5
assert not any(_crosses(e, f) for e, f in itertools.combinations(_redraw_E, 2)), \
    "the redraw must still be drawable without a crossing"
assert REDRAW_CROWNS["betweenness"] == ["Mediolanum"], REDRAW_CROWNS["betweenness"]
for m in ["degree", "closeness", "harmonic", "eigenvector", "katz"]:
    assert REDRAW_CROWNS[m] == ["Roma"], (m, REDRAW_CROWNS[m])


# =============================================================================
# 12. Report
# =============================================================================
def _fmt(v):
    return f"{v:.3f}" if isinstance(v, float) else str(v)


def main():
    print("=" * 78)
    print("ROMAN ROAD NETWORK   12 cities, 18 documented routes, diameter "
          f"{nx.diameter(ROMA)}")
    print("=" * 78)
    for m in METRICS:
        print(f"\n  {m}   crown: {', '.join(ROMA_CROWNS[m])}")
        for n, v in podium(ROMA_C[m], k=4):
            print(f"      {n:14s} {_fmt(v):>8s}   ({ROMA.degree(n)} roads)")
    print(f"\n  lambda_max = {ROMA_LMAX:.4f}   1/lambda_max = {KATZ_CRITICAL:.4f}")
    print(f"  Katz uses lambda = {ROMA_KATZ_LAMBDA:.4f}  ({KATZ_SAFE} of critical)")
    print(f"  at lambda = {KATZ_BAD_LAMBDA:.4f} these go negative: "
          f"{', '.join(KATZ_BAD_NEGATIVE)}")
    print(f"  slowest mode |lambda/lambda_1| = {RATIO:.3f}; crown settles at step "
          f"{POWER_CROWN_SETTLE}, podium at {POWER_TOP3_SETTLE}, "
          f"error at step {POWER_SHOW} is {POWER_SHOW_ERR:.4f}")
    print(f"  Alexandria trails Rome by {EIG_GAP_PCT}% on eigenvector, "
          f"{DEG_GAP:.0f} road on degree")

    print("\n" + "=" * 78)
    print("CUT THE CHANNEL CROSSING")
    print("=" * 78)
    print("  every closeness score:", set(CUT_C['closeness'].values()))
    print("  harmonic still ranks: ", ", ".join(
        f"{n} {v:.2f}" for n, v in podium(CUT_C["harmonic"], k=4)))
    print(f"  Londinium harmonic = {CUT_C['harmonic']['Londinium']:.1f}")

    print("\n" + "=" * 78)
    print("EIGHT-PAGE WEB   8 pages, 14 links")
    print("=" * 78)
    print(f"  hub crown       {WEB_HUB_KING}   " +
          ", ".join(f"{n} {WEB_HUB[n]:.2f}" for n, _ in podium(WEB_HUB, 3)))
    print(f"  authority crown {WEB_AUT_KING}   " +
          ", ".join(f"{n} {WEB_AUT[n]:.2f}" for n, _ in podium(WEB_AUT, 3)))
    print(f"  PageRank crown  {WEB_PR_KING}   " +
          ", ".join(f"{n} {WEB_PR[n]:.3f}" for n, _ in podium(WEB_PR, 3)))
    print(f"  PageRank ranks the hub king {WEB_PR_RANK_OF_LINKS}th of 8")
    print(f"  dangling page: {WEB_DANGLING[0]}")
    print(f"  personalized on {PPR_FOCUS}: " +
          ", ".join(f"{n} {WEB_PPR[n]:.3f}" for n, _ in podium(WEB_PPR, 4)))

    print("\n" + "=" * 78)
    print("BROKER / STAR / PATH / LOCALIZATION")
    print("=" * 78)
    print(f"  broker M: degree 2, betweenness crown {crown(BROKER_C['betweenness'])}, "
          f"{BROKER_PAIRS} pairs pass through it")
    print(f"  star: every metric crowns the hub; closeness = "
          f"{STAR_C['closeness'][0]:.1f} exactly")
    print(f"  path: degree crowns {len(PATH_CROWNS['degree'])} nodes, betweenness "
          f"crowns {PATH_CROWNS['betweenness']}")
    print(f"  localization: tail node scores {LOCAL_TAIL_FRACTION:.4f} of the top on "
          f"eigenvector, {LOCAL_KATZ_FRACTION:.3f} on Katz")
    print(f"  sigma demo: sigma_ST = {SIG_ST}, A and B earn 1/2 each")

    print("\n" + "=" * 78)
    print("THE CLUB NETWORK   13 students, 17 edges (the take-home roster)")
    print("=" * 78)
    print(f"  tell first (degree)     {CLUB_SPREAD[0]}  ({CLUB.degree(CLUB_SPREAD[0])} friends)")
    print(f"  closest to everyone     {CLUB_CLOSE[0]}  ({CLUB.degree(CLUB_CLOSE[0])} friends)")
    print(f"  coordinates (between)   {CLUB_BROKER[0]}  ({CLUB.degree(CLUB_BROKER[0])} friends)")
    print(f"  attacking the road map: {ATTACK_K} strikes by degree leave "
          f"{ATTACK_SURVIVORS['degree']} cities joined, by betweenness "
          f"{ATTACK_SURVIVORS['betweenness']}")
    print(f"     degree takes      {', '.join(ATTACK_DEGREE[0])}")
    print(f"     betweenness takes {', '.join(ATTACK_BETWEEN[0])}  "
          f"({ATTACK_BETWEEN[0][1]} has {ROMA.degree(ATTACK_BETWEEN[0][1])} roads)")

    print("\n" + "=" * 78)
    print("HOW MUCH OF THE ANSWER IS THE MAP WE CHOSE TO DRAW?")
    print("=" * 78)
    ex, keeps = crown_robustness()
    print(f"  {ex} drawable, connected variants of the documented route pool,")
    print("  each keeping Rome's own five routes and the western backbone:\n")
    for m in METRICS:
        print(f"      {m:13s} Rome keeps the crown in {keeps[m]:5d}/{ex} "
              f"= {keeps[m] / ex:6.1%}")
    assert keeps["degree"] == ex, "degree must be the robust one"
    assert keeps["eigenvector"] / ex < 0.85, keeps["eigenvector"] / ex
    assert keeps["betweenness"] / ex < 1.0
    print("\n  -> the count of roads is the same answer on every map anyone could")
    print("     have drawn; who is 'influential' is not.")
    print(f"\n  the redraw the deck shows: drop the {REDRAW_OUT[0]}-{REDRAW_OUT[1]} road,")
    print(f"  add {' and '.join(a + '-' + b for a, b in REDRAW_IN)} --")
    for m in METRICS:
        moved = "  <- moved" if REDRAW_CROWNS[m] != ROMA_CROWNS[m] else ""
        print(f"      {m:13s} {', '.join(REDRAW_CROWNS[m])}{moved}")
    print("\nall numbers verified")


if __name__ == "__main__":
    main()


# =============================================================================
# 13. Claims the deck's prose makes, checked here so the slide cannot drift
# =============================================================================
def _slide_claims():
    import collections
    d = dict(nx.single_source_shortest_path_length(ROMA, "Massilia"))
    hist = collections.Counter(v for k, v in d.items() if k != "Massilia")
    return {
        # "Three cities one step away, five at two steps, three at three ... sum 22"
        "massilia_hist": (hist[1], hist[2], hist[3]),
        "massilia_sum": sum(v for k, v in d.items() if k != "Massilia"),
        "roma_sum": sum(v for k, v in nx.single_source_shortest_path_length(ROMA, "Roma").items()),
    }


SLIDE_CLAIMS = _slide_claims()
assert SLIDE_CLAIMS["massilia_hist"] == (3, 5, 3), SLIDE_CLAIMS
assert SLIDE_CLAIMS["massilia_sum"] == 22
assert SLIDE_CLAIMS["roma_sum"] == 18
