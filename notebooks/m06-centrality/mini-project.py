# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "python-igraph==0.11.9",
# ]
# ///
#
# Mini project M06 -- Where do New York's referrals jam, and how do you fix it?
#
# Two questions, built on one simulated referral network among the hospitals of
# New York City.
#
#   Q1  Which hospitals are the bottlenecks?  First with no capacity limit
#       (betweenness is exactly the answer), then with capacity limits
#       (betweenness stops being the answer; the team designs a score that is).
#   Q2  With a fixed budget, write a function that upgrades the network.
#
# The notebook travels alone (molab, one file). The hospitals, their catchment
# populations, the two referral networks and the two capacity vectors are
# literals between the BUILT-DATA markers below, written by
# tools/build_m06_mini_data.py. Nothing is fetched at run time.
#
# TWO PENCIL CELLS. PLAN_1B and PLAN_2 are the team's reasoning in plain English
# and are what is graded. The code beside each is the same reasoning as code,
# which the team's coding agent may write from the plan.
#
# Calibration (the starting code and the benchmarks are run by the notebook
# itself; the numbers on the page are the numbers we see). Averages over A, B:
#   Q1a  in-degree 0.71, PageRank 0.73, closeness 0.79, betweenness 1.00 (exact)
#   Q1b  betweenness 0.45, betweenness x population 0.27,
#        benchmark (a 4-step walk seeded by the overload) 0.81
#   Q2   do nothing 2.35% unserved, random spending 1.67%, starting code 1.67%,
#        benchmark 1.22%, a greedy search that runs the simulator 0.71%

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    # The kit. Nothing here is yours to edit.
    import time
    import types

    import igraph
    import marimo as mo
    import numpy as np

    # ---------------------------------------------------------------- style
    INK, MUTED, RULE = "#1a1a1a", "#6b6b6b", "#d8d4cc"
    RUST, BLUE = "#b5482f", "#2f5d8a"
    SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
    MONO = "ui-monospace, 'SF Mono', Menlo, Consolas, monospace"

    # ---------------------------------------------------------------- data
    # BUILT-DATA-BEGIN
    HOSPITALS = [
        ('Long Island Jewish Medical Center', 40.7547, -73.7066, 120600),
        ('David H. Koch Center For Cancer Care', 40.7676, -73.9516, 40900),
        ('Maimonides Midwood Community Hospital', 40.6134, -73.9490, 157900),
        ('New York-Presbyterian David H. Koch Center', 40.7648, -73.9553, 7400),
        ('University Hospital of Brooklyn', 40.6545, -73.9450, 164400),
        ('Maimonides Medical Center', 40.6394, -73.9984, 375100),
        ('Long Island Jewish Forest Hills', 40.7287, -73.8510, 234000),
        ('Staten Island University Hosp-North', 40.5845, -74.0856, 127800),
        ('Hospital for Special Surgery', 40.7654, -73.9542, 10800),
        ('Calvary Hospital', 40.6464, -74.0210, 81100),
        ("Staten Island University Hospital Prince's Bay", 40.5168, -74.1968, 135800),
        ('Montefiore Medical Center - Henry & Lucy Moses Div', 40.8799, -73.8799, 76700),
        ('Flushing Hospital Medical Center', 40.7555, -73.8155, 276700),
        ('Mount Sinai Brooklyn', 40.6180, -73.9432, 148200),
        ('Mount Sinai -  Behavioral Health Center', 40.7208, -73.9911, 114000),
        ('Queens Hospital Center', 40.7172, -73.8036, 316400),
        ('Metropolitan Hospital Center', 40.7848, -73.9437, 72800),
        ('BronxCare Hospital Center (Bronx)', 40.8436, -73.9115, 147800),
        ('Mount Sinai Hospital - Mount Sinai Hospital of Queens', 40.7683, -73.9245, 209000),
        ('Northwell Greenwich Village Hospital', 40.7376, -74.0005, 124000),
        ('NYU Langone Hospital-Brooklyn', 40.6466, -74.0204, 52700),
        ('Mount Sinai Morningside', 40.8059, -73.9616, 126100),
        ('Bellevue Hospital Center', 40.7396, -73.9765, 33500),
        ('St Johns Episcopal Hospital So Shore', 40.5986, -73.7528, 147000),
        ('Montefiore Medical Center-Wakefield Hospital', 40.8946, -73.8614, 119900),
        ('Kingsbrook Jewish Medical Village', 40.6594, -73.9340, 81900),
        ('Elmhurst Hospital Center', 40.7443, -73.8857, 423000),
        ('New York Eye and Ear Infirmary of Mount Sinai', 40.7322, -73.9847, 79400),
        ('New York-Presbyterian Hospital - New York Weill Cornell Center', 40.7641, -73.9549, 35200),
        ('Jacobi Medical Center', 40.8574, -73.8467, 136900),
        ('New York-Presbyterian Hospital - Columbia Presbyterian Center', 40.8413, -73.9407, 175000),
        ('Mount Sinai West', 40.7701, -73.9878, 193800),
        ('Woodhull Medical & Mental Health Center', 40.7005, -73.9417, 397900),
        ('SBH Health System', 40.8539, -73.8910, 180900),
        ('New York-Presbyterian Hospital - Allen Hospital', 40.8725, -73.9128, 165100),
        ('Lenox Hill Hospital', 40.7739, -73.9606, 89700),
        ('Kings County Hospital Center', 40.6558, -73.9441, 46100),
        ("Montefiore Einstein Children's Center for Mental Health of the Children's Hospital at Montefiore Einstein", 40.8461, -73.8385, 65200),
        ('NewYork-Presbyterian/Queens', 40.7475, -73.8260, 73800),
        ('Calvary Hospital Inc', 40.8473, -73.8447, 2700),
        ('Harlem Hospital Center', 40.8143, -73.9405, 134600),
        ('Brookdale Hospital Medical Center', 40.6551, -73.9126, 394100),
        ('RUMC-Bayley Seton', 40.6214, -74.0748, 72900),
        ('Interfaith Medical Center', 40.6779, -73.9375, 237200),
        ('North Central Bronx Hospital', 40.8805, -73.8815, 62500),
        ('Montefiore Medical Center - Montefiore Westchester Square', 40.8404, -73.8482, 193500),
        ('NewYork-Presbyterian Brooklyn Methodist Hospital', 40.6681, -73.9789, 111900),
        ('Mount Sinai Hospital', 40.7905, -73.9538, 95300),
        ('South Brooklyn Health', 40.5866, -73.9658, 307600),
        ('Montefiore Med Center - Jack D Weiler Hosp of A Einstein College Div', 40.8496, -73.8451, 9200),
        ('BronxCare Hospital Center (Bronx)', 40.8318, -73.9037, 210000),
        ('NYU Langone Hospitals', 40.7429, -73.9742, 103200),
        ('Brooklyn Hospital Center - Downtown Campus', 40.6898, -73.9775, 137400),
        ('New York-Presbyterian/Lower Manhattan Hospital', 40.7104, -74.0055, 99600),
        ('NYU Langone Hospital - Joseph S. and Diane H. Steinberg Ambulatory Care Center', 40.6909, -73.9975, 83600),
        ('Richmond University Medical Center', 40.6358, -74.1067, 172400),
        ('Memorial Hospital for Cancer and Allied Diseases', 40.7644, -73.9568, 76000),
        ('Henry J. Carter Specialty Hospital', 40.8030, -73.9408, 75200),
        ('NYU Langone Orthopedic Hospital', 40.7341, -73.9831, 51500),
        ('Lincoln Medical & Mental Health Center', 40.8177, -73.9242, 136800),
        ('Jamaica Hospital Medical Center', 40.7014, -73.8163, 472400),
    ]
    EDGES = {
        'A': [(0, 12), (0, 15), (0, 32), (0, 58), (1, 3), (1, 8), (1, 25), (1, 60), (2, 10), (2, 13), (2, 42), (2, 48), (3, 8), (3, 28), (3, 45), (3, 60), (4, 2), (4, 19), (4, 25), (4, 36), (5, 9), (5, 20), (5, 27), (5, 31), (6, 9), (6, 26), (6, 38), (6, 50), (7, 26), (7, 37), (7, 42), (7, 55), (8, 3), (8, 28), (8, 32), (8, 38), (9, 2), (9, 5), (9, 20), (9, 30), (10, 7), (10, 46), (10, 55), (11, 24), (11, 32), (11, 39), (11, 44), (12, 6), (12, 21), (12, 28), (12, 38), (13, 2), (13, 48), (13, 60), (14, 18), (14, 27), (14, 58), (15, 14), (15, 29), (15, 38), (15, 60), (16, 7), (16, 35), (16, 47), (17, 26), (17, 33), (17, 49), (17, 50), (18, 1), (18, 12), (18, 16), (18, 32), (19, 15), (19, 27), (19, 58), (20, 5), (20, 9), (20, 45), (20, 53), (21, 16), (21, 34), (21, 47), (21, 57), (22, 30), (22, 36), (22, 51), (22, 58), (23, 15), (23, 21), (23, 60), (24, 4), (24, 11), (24, 44), (24, 60), (25, 4), (25, 36), (25, 41), (25, 43), (26, 6), (26, 10), (26, 18), (26, 33), (27, 16), (27, 22), (27, 40), (27, 58), (28, 3), (28, 8), (28, 10), (28, 48), (29, 39), (29, 49), (29, 55), (29, 60), (30, 17), (30, 32), (30, 33), (30, 59), (31, 6), (31, 35), (31, 43), (31, 56), (32, 8), (32, 40), (32, 43), (32, 52), (33, 11), (33, 17), (33, 48), (33, 50), (34, 33), (34, 37), (34, 44), (34, 57), (35, 1), (35, 8), (35, 46), (35, 57), (36, 4), (36, 25), (36, 47), (37, 23), (37, 32), (37, 39), (37, 49), (38, 5), (38, 6), (38, 12), (38, 28), (39, 5), (39, 37), (39, 49), (39, 51), (40, 3), (40, 38), (40, 57), (40, 59), (41, 25), (41, 36), (41, 52), (42, 7), (42, 20), (42, 34), (42, 55), (43, 1), (43, 15), (43, 25), (43, 36), (44, 11), (44, 22), (44, 24), (44, 51), (45, 17), (45, 31), (45, 37), (45, 39), (46, 31), (46, 50), (46, 52), (46, 54), (47, 16), (47, 45), (47, 57), (47, 59), (48, 2), (48, 9), (48, 13), (48, 16), (49, 37), (49, 39), (49, 50), (49, 56), (50, 17), (50, 41), (50, 44), (50, 59), (51, 22), (51, 47), (51, 54), (51, 58), (52, 12), (52, 24), (52, 46), (52, 54), (53, 0), (53, 14), (53, 48), (53, 54), (54, 12), (54, 26), (54, 52), (54, 53), (55, 5), (55, 7), (55, 15), (55, 42), (56, 3), (56, 12), (56, 28), (56, 51), (57, 19), (57, 40), (57, 47), (57, 52), (58, 13), (58, 22), (58, 27), (58, 53), (59, 29), (59, 40), (59, 57), (60, 6), (60, 15)],
        'B': [(0, 5), (0, 12), (0, 15), (0, 36), (1, 3), (1, 8), (1, 15), (1, 54), (2, 13), (2, 48), (2, 57), (3, 8), (3, 21), (3, 28), (3, 34), (4, 6), (4, 25), (4, 36), (4, 37), (5, 3), (5, 9), (5, 20), (5, 28), (6, 26), (6, 30), (6, 38), (6, 52), (7, 11), (7, 42), (7, 49), (7, 55), (8, 3), (8, 12), (8, 28), (8, 45), (9, 5), (9, 6), (9, 17), (9, 20), (10, 6), (10, 7), (10, 26), (10, 55), (11, 24), (11, 29), (11, 32), (11, 44), (12, 6), (12, 27), (12, 31), (12, 38), (13, 2), (13, 34), (13, 35), (13, 48), (14, 27), (14, 39), (14, 45), (14, 58), (15, 8), (15, 38), (15, 60), (16, 17), (16, 35), (16, 47), (16, 55), (17, 33), (17, 38), (17, 41), (17, 50), (18, 1), (18, 16), (18, 43), (18, 47), (19, 17), (19, 27), (19, 40), (19, 58), (20, 0), (20, 5), (20, 9), (20, 23), (21, 34), (21, 47), (21, 57), (21, 60), (22, 18), (22, 51), (22, 58), (22, 60), (23, 15), (23, 18), (23, 33), (23, 60), (24, 11), (24, 44), (24, 55), (24, 56), (25, 4), (25, 13), (25, 34), (25, 36), (26, 0), (26, 6), (26, 18), (26, 31), (27, 22), (27, 47), (27, 48), (27, 58), (28, 2), (28, 3), (28, 7), (28, 8), (29, 15), (29, 39), (29, 43), (29, 49), (30, 17), (30, 22), (30, 23), (30, 59), (31, 5), (31, 35), (31, 56), (31, 58), (32, 25), (32, 41), (32, 43), (32, 52), (33, 17), (33, 28), (33, 50), (33, 59), (34, 12), (34, 33), (34, 44), (34, 45), (35, 1), (35, 8), (35, 40), (36, 4), (36, 18), (36, 20), (36, 25), (37, 5), (37, 39), (37, 45), (37, 49), (38, 6), (38, 12), (38, 43), (38, 51), (39, 13), (39, 24), (39, 37), (39, 49), (40, 30), (40, 50), (40, 57), (40, 59), (41, 25), (41, 27), (41, 36), (41, 38), (42, 7), (42, 41), (42, 53), (42, 55), (43, 18), (43, 25), (43, 36), (43, 50), (44, 11), (44, 14), (44, 24), (44, 26), (45, 37), (45, 39), (45, 41), (45, 46), (46, 50), (46, 52), (46, 54), (47, 6), (47, 16), (47, 57), (48, 2), (48, 13), (48, 44), (48, 52), (49, 25), (49, 37), (49, 39), (49, 43), (50, 17), (50, 29), (50, 59), (51, 9), (51, 19), (51, 22), (51, 58), (52, 32), (52, 41), (52, 46), (52, 54), (53, 14), (53, 17), (53, 26), (53, 54), (54, 9), (54, 52), (54, 53), (55, 7), (55, 10), (55, 15), (55, 42), (56, 3), (56, 28), (56, 32), (56, 42), (57, 11), (57, 25), (57, 40), (57, 47), (58, 22), (58, 27), (58, 35), (58, 46), (59, 4), (59, 12), (59, 40), (59, 57), (60, 2), (60, 6), (60, 11), (60, 15)],
    }
    CAPACITY = {
        'A': [126900, 78200, 284000, 6100, 149000, 306700, 313400, 129200, 15700, 36600, 284900, 76100, 389500, 144500, 99600, 403900, 109400, 139800, 202200, 175000, 36900, 66100, 41500, 112700, 52400, 58900, 355200, 48100, 18600, 144300, 271600, 180900, 295100, 223000, 236300, 81200, 61100, 108100, 69700, 1900, 163100, 456600, 123900, 137900, 48100, 137500, 53200, 104600, 404300, 6800, 406100, 154800, 188900, 123700, 133200, 98100, 103800, 102200, 24100, 165800, 437500],
        'B': [255500, 9500, 226300, 7100, 277100, 415500, 495900, 120700, 8000, 98100, 153600, 60800, 230500, 190800, 145700, 235900, 57500, 61000, 414300, 104400, 89600, 141700, 74800, 273400, 128800, 148500, 256900, 130300, 16800, 148800, 263100, 199600, 314100, 117200, 131800, 134000, 64100, 54000, 39200, 3400, 65300, 289000, 48800, 308600, 64700, 221800, 117800, 65400, 364500, 16200, 192300, 127800, 120900, 147300, 105100, 238100, 82800, 146500, 40800, 109600, 337000],
    }
    # BUILT-DATA-END

    NAMES = [h[0] for h in HOSPITALS]
    LAT = np.array([h[1] for h in HOSPITALS])
    LON = np.array([h[2] for h in HOSPITALS])
    POP = np.array([h[3] for h in HOSPITALS], dtype=float)
    N = len(HOSPITALS)
    SCENARIOS = list(EDGES)

    HOPS = 4  # a patient is passed on at most this many times
    BUDGET = 100.0
    EDGE_COST = 8.0  # one new referral link
    UNIT = 10_000  # patients of extra capacity ...
    UNIT_COST = 4.0  # ... cost this much
    TIME_BUDGET = 20.0  # seconds per city for your function

    # ------------------------------------------------------------ the model
    def simulate(edges, capacity):
        """Everyone goes to the nearest hospital. A hospital treats patients
        until its capacity is used; the rest are split equally among the
        hospitals it refers to. A patient is passed on at most HOPS times; after
        that nobody takes them.

        Returns arrived (patients sent to a hospital by others, taken or not),
        dropped (patients nobody took, by the hospital that gave up last) and
        unserved (their share of the whole population)."""
        out = [[] for _ in range(N)]
        for i, j in edges:
            out[i].append(j)
        served = np.zeros(N)
        carry = POP.copy()
        arrived = np.zeros(N)
        dropped = np.zeros(N)
        for hop in range(HOPS + 1):
            nxt = np.zeros(N)
            for i in range(N):
                if carry[i] <= 0:
                    continue
                take = min(max(capacity[i] - served[i], 0.0), carry[i])
                served[i] += take
                over = carry[i] - take
                if hop < HOPS and out[i]:
                    for j in out[i]:
                        nxt[j] += over / len(out[i])
                else:
                    dropped[i] += over
            arrived += nxt
            carry = nxt
        return types.SimpleNamespace(
            arrived=arrived, dropped=dropped, unserved=dropped.sum() / POP.sum()
        )

    def pass_through(edges):
        """No capacity limit. Every hospital sends one patient to every other
        hospital, along the shortest referral path (ties split equally).
        Counts, for each hospital, the patients that pass through it on the way
        to somewhere else."""
        g = igraph.Graph(n=N, edges=list(edges), directed=True)
        traffic = np.zeros(N)
        for s in range(N):
            paths = g.get_all_shortest_paths(s, mode="out")
            by_target = {}
            for p in paths:
                if len(p) > 1:
                    by_target.setdefault(p[-1], []).append(p)
            for ps in by_target.values():
                for p in ps:
                    for mid in p[1:-1]:
                        traffic[mid] += 1.0 / len(ps)
        return traffic

    CITY = {
        k: types.SimpleNamespace(
            edges=[tuple(e) for e in EDGES[k]], capacity=np.array(CAPACITY[k], dtype=float)
        )
        for k in SCENARIOS
    }
    TRAFFIC = {k: pass_through(CITY[k].edges) for k in SCENARIOS}
    SIM0 = {k: simulate(CITY[k].edges, CITY[k].capacity) for k in SCENARIOS}
    ARRIVED = {k: SIM0[k].arrived for k in SCENARIOS}

    def graph_of(k):
        return igraph.Graph(n=N, edges=list(CITY[k].edges), directed=True)

    def city_of(k):
        """A fresh copy of one city, for your function to read."""
        c = CITY[k]
        return types.SimpleNamespace(
            n=N,
            names=list(NAMES),
            lat=LAT.copy(),
            lon=LON.copy(),
            pop=POP.copy(),
            capacity=c.capacity.copy(),
            edges=list(c.edges),
            graph=igraph.Graph(n=N, edges=list(c.edges), directed=True),
            budget=BUDGET,
            edge_cost=EDGE_COST,
            unit=UNIT,
            unit_cost=UNIT_COST,
        )

    # ------------------------------------------------------------- scoring
    def _ranks(x):
        x = np.asarray(x, dtype=float)
        order = np.argsort(x, kind="stable")
        r = np.empty(len(x))
        r[order] = np.arange(len(x))
        for v in np.unique(x):
            m = x == v
            if m.sum() > 1:
                r[m] = r[m].mean()
        return r

    def spearman(a, b):
        """Rank correlation: 1 when two scores order the hospitals identically,
        0 when they are unrelated, -1 when the order is reversed."""
        ra, rb = _ranks(a), _ranks(b)
        if ra.std() == 0 or rb.std() == 0:
            return 0.0
        return float(np.corrcoef(ra, rb)[0, 1])

    def _vector(v):
        v = np.asarray(v, dtype=float).reshape(-1)
        if v.shape != (N,):
            raise ValueError(f"return one number per hospital ({N}), got {v.shape[0]}")
        if not np.isfinite(v).all():
            raise ValueError("a score is NaN or infinite")
        return v

    def score_scores(fn, truth, arity):
        rows = {}
        for k in SCENARIOS:
            t0 = time.time()
            notes = []
            value = 0.0
            try:
                c = city_of(k)
                args = [c.graph] if arity == 1 else [c.graph, c.pop, c.capacity]
                value = spearman(_vector(fn(*args)), truth[k])
            except Exception as err:  # noqa: BLE001 -- shown to the team
                notes.append(f"{type(err).__name__}: {err}")
            rows[k] = {"value": value, "seconds": time.time() - t0, "notes": notes}
        return rows

    def _proposal(p, c):
        """Turn what propose() returned into (new edges, extra capacity), or
        raise ValueError saying what is wrong with it."""
        if not isinstance(p, dict):
            raise ValueError('return a dict with the keys "edges" and "capacity"')
        have = set(c.edges)
        new, extra = [], np.zeros(N)
        for e in p.get("edges", []):
            i, j = int(e[0]), int(e[1])
            if not (0 <= i < N and 0 <= j < N) or i == j:
                raise ValueError(f"edge {(i, j)} is not a pair of different hospitals")
            if (i, j) in have:
                raise ValueError(f"edge {(i, j)} already exists (or is listed twice)")
            have.add((i, j))
            new.append((i, j))
        for k, v in dict(p.get("capacity", {})).items():
            k, v = int(k), float(v)
            if not 0 <= k < N or not np.isfinite(v) or v < 0:
                raise ValueError(f"capacity {k}: {v} is not a hospital and a number >= 0")
            extra[k] += v
        cost = EDGE_COST * len(new) + UNIT_COST * extra.sum()
        if cost > BUDGET + 1e-9:
            raise ValueError(f"the proposal costs {cost:.1f}, the budget is {BUDGET:.0f}")
        return new, extra * UNIT, cost

    def run_proposal(fn, k):
        t0 = time.time()
        c = city_of(k)
        notes, new, extra, cost = [], [], np.zeros(N), 0.0
        try:
            new, extra, cost = _proposal(fn(c), CITY[k])
        except Exception as err:  # noqa: BLE001 -- shown to the team
            notes.append(f"{type(err).__name__}: {err}  (nothing was applied)")
        sim = simulate(CITY[k].edges + new, CITY[k].capacity + extra)
        return {
            "value": sim.unserved,
            "seconds": time.time() - t0,
            "notes": notes,
            "new": new,
            "extra": extra,
            "cost": cost,
            "sim": sim,
        }

    def score_proposal(fn):
        return {k: run_proposal(fn, k) for k in SCENARIOS}

    def overall(rows):
        return float(np.mean([r["value"] for r in rows.values()]))

    # --------------------------------------------------------- references
    def _walk(edges, seed, hops):
        P = np.zeros((N, N))
        for i, j in edges:
            P[i, j] = 1.0
        P /= P.sum(axis=1, keepdims=True)
        x, total = seed.astype(float), np.zeros(N)
        for _ in range(hops):
            x = (P * x[:, None]).sum(axis=0)
            total += x
        return total

    def ref_closeness(g):
        return np.nan_to_num(np.array(g.closeness(mode="in")))

    def ref_pagerank(g):
        return np.array(g.pagerank())

    def benchmark_1b(g, pop, capacity):
        """Deliberately not named in the notebook. Beating it is the game."""
        return _walk(g.get_edgelist(), np.maximum(pop - capacity, 0.0), HOPS)

    def benchmark_2(c):
        """Deliberately not named in the notebook. Beating it is the game."""
        sim = simulate(c.edges, c.capacity)
        short = np.maximum(c.pop - c.capacity, 0.0)
        spare = np.maximum(c.capacity - c.pop, 0.0)
        have, edges = set(c.edges), []
        for a in np.argsort(-short)[:3]:
            for b in np.argsort(-spare):
                if a != b and (int(a), int(b)) not in have:
                    edges.append((int(a), int(b)))
                    break
        left = BUDGET - EDGE_COST * len(edges)
        want = np.maximum(sim.arrived + c.pop - c.capacity, 0.0)
        share = want / want.sum()
        return {
            "edges": edges,
            "capacity": {i: float(share[i] * left / UNIT_COST) for i in range(N)},
        }

    def random_2(c):
        rng = np.random.default_rng(7)
        have = set(c.edges)
        edges = []
        while len(edges) < 3:
            e = (int(rng.integers(N)), int(rng.integers(N)))
            if e[0] != e[1] and e not in have:
                have.add(e)
                edges.append(e)
        left = BUDGET - EDGE_COST * 3
        picks = rng.choice(N, size=10, replace=False)
        return {"edges": edges, "capacity": {int(i): left / UNIT_COST / 10 for i in picks}}

    def nothing_2(c):
        return {"edges": [], "capacity": {}}

    # ------------------------------------------------------------- drawing
    def _bar_row(label, value, top, tone, fmt, bold=False):
        width = 0 if top <= 0 else max(0.0, min(100.0, 100.0 * value / top))
        weight = "700" if bold else "400"
        return (
            f'<tr><td style="padding:4px 14px 4px 0;font-family:{SANS};'
            f'font-size:14px;color:{INK};font-weight:{weight};white-space:nowrap">'
            f"{label}</td>"
            f'<td style="width:260px;padding:4px 10px 4px 0">'
            f'<div style="background:#efece6;height:12px;border-radius:2px">'
            f'<div style="width:{width:.1f}%;height:12px;background:{tone};'
            f'border-radius:2px"></div></div></td>'
            f'<td style="font-family:{MONO};font-size:14px;color:{INK};'
            f'font-weight:{weight};padding:4px 0">{fmt(value)}</td></tr>'
        )

    def scoreboard(title, lines, caption, fmt):
        """lines: (label, value, tone, bold)."""
        top = max([v for _, v, _, _ in lines] + [1e-9])
        body = "".join(_bar_row(l, v, top, t, fmt, b) for l, v, t, b in lines)
        return mo.Html(
            f'<div style="font-family:{SANS};font-size:13px;color:{MUTED};'
            f'letter-spacing:.06em;text-transform:uppercase;margin:16px 0 4px">'
            f"{title}</div>"
            f'<table style="border-collapse:collapse">{body}</table>'
            f'<div style="font-family:{SANS};font-size:13px;color:{MUTED};'
            f'margin-top:6px">{caption}</div>'
        )

    def table_html(head, rows, highlight=None):
        cells = "".join(
            f'<th style="text-align:{"left" if i < 1 else "right"};'
            f"padding:4px 18px 6px 0;font-family:{SANS};font-size:12px;"
            f'color:{MUTED};font-weight:700">{h}</th>'
            for i, h in enumerate(head)
        )
        body = "".join(
            "<tr>"
            + "".join(
                f'<td style="text-align:{"left" if i < 1 else "right"};'
                f"padding:5px 18px 5px 0;border-top:1px solid {RULE};"
                f'font-family:{MONO if i > 0 else SANS};font-size:14px;'
                f'color:{RUST if i == highlight else INK}">{v}</td>'
                for i, v in enumerate(row)
            )
            + "</tr>"
            for row in rows
        )
        return mo.Html(
            f'<table style="border-collapse:collapse;margin:10px 0">'
            f"<tr>{cells}</tr>{body}</table>"
        )

    def note(text, tone=BLUE):
        return mo.Html(
            f'<div style="border-left:3px solid {tone};padding:2px 0 2px 14px;'
            f'margin:14px 0;font-family:{SANS};font-size:16px;color:{INK}">'
            f"{text}</div>"
        )

    def complaints(rows):
        out = [f"<b>city {k}</b>: {'; '.join(r['notes'])}" for k, r in rows.items() if r["notes"]]
        out += [
            f"<b>city {k}</b>: took {r['seconds']:.0f}s, over the {TIME_BUDGET:.0f}s budget"
            for k, r in rows.items()
            if r["seconds"] > TIME_BUDGET
        ]
        return note("<br>".join(out), RUST) if out else mo.Html("")

    def _ramp(t):
        """0 -> pale, 1 -> rust."""
        lo, hi = np.array([239, 233, 223]), np.array([181, 72, 47])
        r, g_, b = (lo + (hi - lo) * float(np.clip(t, 0, 1))).astype(int)
        return f"rgb({r},{g_},{b})"

    def svg_map(values, k, size=560, extra_edges=(), extra_capacity=None, fmt="{:,.0f}"):
        """The city. One circle per hospital, area ~ the people it serves, fill
        ~ `values` (rank-scaled, so one huge value does not wash out the rest).
        Thin grey lines are referral links; rust lines are links you added; a
        ring marks a hospital whose capacity you raised."""
        pad = 24
        ky = np.cos(np.radians(LAT.mean()))
        x = (LON - LON.min()) * ky
        y = LAT.max() - LAT
        scale = (size - 2 * pad) / max(x.max(), y.max())
        sx, sy = pad + x * scale, pad + y * scale
        r = _ranks(values) / max(N - 1, 1)
        rad = 3.5 + 9.0 * np.sqrt(POP / POP.max())
        links = "".join(
            f'<line x1="{sx[i]:.1f}" y1="{sy[i]:.1f}" x2="{sx[j]:.1f}" y2="{sy[j]:.1f}" '
            f'stroke="#ddd8cd" stroke-width="0.5"/>'
            for i, j in CITY[k].edges
        )
        added = "".join(
            f'<line x1="{sx[i]:.1f}" y1="{sy[i]:.1f}" x2="{sx[j]:.1f}" y2="{sy[j]:.1f}" '
            f'stroke="{BLUE}" stroke-width="1.8"/>'
            for i, j in extra_edges
        )
        rings = ""
        if extra_capacity is not None:
            rings = "".join(
                f'<circle cx="{sx[i]:.1f}" cy="{sy[i]:.1f}" r="{rad[i] + 3.5:.1f}" '
                f'fill="none" stroke="{BLUE}" stroke-width="1.8"/>'
                for i in range(N)
                if extra_capacity[i] > 0
            )
        dots = "".join(
            f'<circle cx="{sx[i]:.1f}" cy="{sy[i]:.1f}" r="{rad[i]:.1f}" '
            f'fill="{_ramp(r[i])}" stroke="{INK}" stroke-width="1">'
            f"<title>#{i} {NAMES[i]} · {fmt.format(values[i])}</title></circle>"
            for i in range(N)
        )
        return mo.Html(
            f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
            f'style="background:#ffffff;border:1px solid {RULE};border-radius:4px">'
            f"{links}{added}{rings}{dots}</svg>"
        )

    def top_table(values, label, how=8, fmt="{:,.0f}"):
        order = np.argsort(-np.asarray(values))[:how]
        return table_html(
            ["hospital", "#", label],
            [[NAMES[i][:34], str(i), fmt.format(values[i])] for i in order],
        )


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Mini project m06

    ## The city

    There are 61 hospitals in New York City (the map below shows them), and 8.8 million people. Everyone goes to the nearest hospital, so each hospital serves a **catchment**: the people nearer to it than to any other. The circle area is the catchment size.

    Hospitals pass patients to each other along **referral links** (grey lines; the link $i \to j$ means $i$ may send patients to $j$). Locations and populations are real (NYS Department of Health, 2020 Census). **Who refers to whom, and how many patients each hospital can treat, are simulation assumptions.** There are two cities, A and B: the same hospitals and people, but different referral links and capacities. Everything you write must work on both.

    The notebook has two questions. Question 1 is about finding the bottlenecks, and question 2 is about fixing them.
    """)
    return


@app.cell(hide_code=True)
def _():
    explore_city = mo.ui.radio(options=SCENARIOS, value=SCENARIOS[0], label="city")
    explore_color = mo.ui.dropdown(
        options=[
            "people in the catchment",
            "spare capacity (capacity minus people)",
            "Q1a: traffic passing through, no capacity limit",
            "Q1b: referrals received, with capacity limits",
        ],
        value="people in the catchment",
        label="colour by",
    )
    mo.hstack([explore_city, explore_color], justify="start", gap=2)
    return explore_city, explore_color


@app.cell(hide_code=True)
def _(explore_city, explore_color):
    _k, _what = explore_city.value, explore_color.value
    if _what.startswith("people"):
        _v, _lab = POP, "people"
    elif _what.startswith("spare"):
        _v, _lab = CITY[_k].capacity - POP, "capacity − people"
    elif _what.startswith("Q1a"):
        _v, _lab = TRAFFIC[_k], "patients passing through"
    else:
        _v, _lab = ARRIVED[_k], "referrals received"
    mo.hstack(
        [svg_map(_v, _k), top_table(_v, _lab)],
        justify="start",
        gap=2,
        wrap=True,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # Question 1. Which hospitals are the bottlenecks?

    ## 1a. Without capacity limits

    Suppose a patient at any hospital may need a specialist at any other hospital. Every hospital sends **one patient to every other hospital**, along the shortest referral path (if there are several shortest paths, the patient is split equally among them). A hospital's **traffic** is the number of patients that pass through it on their way to somewhere else, not counting the ones that start or end there. The map above shows it under "Q1a".

    Write `bottleneck_no_capacity(g)`. It receives the referral network `g` (an `igraph.Graph`, directed, vertices `0..60`) and returns **one number per hospital**, higher meaning more traffic. It is scored by how well its ranking of the hospitals agrees with the true traffic ranking (rank correlation, 1 is perfect), averaged over the two cities.
    """)
    return


@app.function
# Q1a — return one number per hospital: higher = more patients pass through.
def bottleneck_no_capacity(g):
    """Starting version: the number of hospitals that refer to this one."""
    return np.array(g.indegree())


@app.cell(hide_code=True)
def _():
    _mine = score_scores(bottleneck_no_capacity, TRAFFIC, 1)
    _rows = {
        "in-degree (the starting code)": score_scores(lambda g: np.array(g.indegree()), TRAFFIC, 1),
        "closeness": score_scores(ref_closeness, TRAFFIC, 1),
        "PageRank": score_scores(ref_pagerank, TRAFFIC, 1),
    }
    _lines = [(n, overall(r), MUTED, False) for n, r in _rows.items()] + [
        ("your team", overall(_mine), RUST, True)
    ]
    mo.vstack(
        [
            scoreboard(
                "1a · traffic without capacity limits",
                _lines,
                "rank correlation with the true traffic, averaged over cities A and B. higher is better.",
                lambda v: f"{v:.2f}",
            ),
            table_html(
                ["city", "your correlation"],
                [[f"city {k}", f"{r['value']:.2f}"] for k, r in _mine.items()],
                highlight=1,
            ),
            complaints(_mine),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## 1b. With capacity limits

    Now the hospitals have capacities (the map above, "spare capacity", shows where there is room). The patients do not choose a specialist any more; they simply get ill:

    1. Every person goes to the nearest hospital.
    2. A hospital treats patients until its capacity is used up. The rest are **split equally among the hospitals it refers to**.
    3. A hospital that receives referred patients does the same: treats what it can, passes on the rest.
    4. A patient is passed on at most **4 times**. After that nobody takes them and they are unserved.

    A hospital's **load** is the number of referred patients sent to it, whether or not it could treat them. Look at the map coloured by "Q1b: referrals received" and compare it with "Q1a".

    Write `bottleneck_with_capacity(g, pop, capacity)`: the network, the catchment sizes and the capacities (each an array of length 61 except `g`), returning one number per hospital. It is scored the same way, against the load. The starting code is the answer to 1a. **Your score has to hold up on both cities.**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ 1. Your reasoning, in English

    Write 4 to 10 plain sentences a person could follow with a pencil: what the simulation does that your 1a answer does not, and how your score reflects it. This text is graded; the agent codes from it.
    """)
    return


@app.cell
def _():
    # ✍️ 1 — describe your score for 1b in plain English.
    PLAN_1B = """
    ...
    """
    return


@app.function
# Q1b — return one number per hospital: higher = more referred patients arrive.
def bottleneck_with_capacity(g, pop, capacity):
    """Starting version: the answer to 1a, betweenness, ignoring pop and
    capacity."""
    return np.array(g.betweenness(directed=True))


@app.cell(hide_code=True)
def _():
    _mine = score_scores(bottleneck_with_capacity, ARRIVED, 3)
    _lines = [
        (
            "betweenness (the starting code)",
            overall(score_scores(lambda g, p, c: np.array(g.betweenness(directed=True)), ARRIVED, 3)),
            MUTED,
            False,
        ),
        ("benchmark", overall(score_scores(benchmark_1b, ARRIVED, 3)), BLUE, False),
        ("your team", overall(_mine), RUST, True),
    ]
    mo.vstack(
        [
            scoreboard(
                "1b · referrals received with capacity limits",
                _lines,
                "rank correlation with the simulated load, averaged over cities A and B. higher is better.",
                lambda v: f"{v:.2f}",
            ),
            table_html(
                ["city", "your correlation"],
                [[f"city {k}", f"{r['value']:.2f}"] for k, r in _mine.items()],
                highlight=1,
            ),
            complaints(_mine),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # Question 2. Fix it with a budget

    You run the health system, with a budget of **100**. You may

    - **add referral links**: any ordered pair of different hospitals that is not linked yet costs **8**;
    - **add capacity** at any hospital: **10,000 patients** of capacity costs **4** (fractions are fine);
    - nothing else. No new hospitals, and no links removed.

    Write `propose(city)`. It receives one city and returns a proposal:

    ```python
    {"edges": [(3, 41), (17, 5)],         # new links: from hospital 3 to 41, from 17 to 5
     "capacity": {12: 6.0, 30: 2.5}}      # units of 10,000: hospital 12 gets 60,000, hospital 30 gets 25,000
    ```

    | what | gives |
    | :--- | :--- |
    | `city.n`, `city.names` | 61, and the hospital names |
    | `city.lat`, `city.lon` | where each hospital is |
    | `city.pop` | people in each catchment |
    | `city.capacity` | patients each hospital can treat |
    | `city.edges` | the current links, a list of `(from, to)` |
    | `city.graph` | the same links as a directed `igraph.Graph` |
    | `city.budget`, `city.edge_cost`, `city.unit`, `city.unit_cost` | 100, 8, 10000, 4 |

    The score is the **share of people left unserved** by the simulation of 1b after your changes, averaged over cities A and B. Lower is better. A proposal that costs too much, repeats a link or names a hospital that does not exist is **rejected whole** and nothing is applied. The same function is run on each city and sees only that city. It must work on any city of this kind, not only on A and B.

    Your answers to Question 1 are tools you can use here: `bottleneck_with_capacity` is yours to call.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ 2. Your reasoning, in English

    Write 4 to 10 plain sentences a person could follow with a pencil: where you put the money, why there, and why you split it between links and capacity as you did. This text is graded; the agent codes from it.
    """)
    return


@app.cell
def _():
    # ✍️ 2 — describe your proposal in plain English.
    PLAN_2 = """
    ...
    """
    return


@app.function
# Q2 — spend the budget.
def propose(city):
    """Starting version: split the whole budget evenly among the five hospitals
    with the largest catchments, as extra capacity. No new links."""
    biggest = np.argsort(-city.pop)[:5]
    each = city.budget / city.unit_cost / 5
    return {"edges": [], "capacity": {int(i): each for i in biggest}}


@app.cell(hide_code=True)
def _():
    _mine = score_proposal(propose)
    _ref = {
        name: overall(score_proposal(fn))
        for name, fn in [
            ("do nothing", nothing_2),
            ("spend at random", random_2),
            ("benchmark", benchmark_2),
        ]
    }
    _lines = [
        ("do nothing", _ref["do nothing"], MUTED, False),
        ("spend at random", _ref["spend at random"], MUTED, False),
        ("benchmark", _ref["benchmark"], BLUE, False),
        ("your team", overall(_mine), RUST, True),
    ]
    mo.vstack(
        [
            scoreboard(
                "2 · people left unserved",
                _lines,
                "share of the population nobody takes, averaged over cities A and B. lower is better.",
                lambda v: f"{100 * v:.2f}%",
            ),
            table_html(
                ["city", "unserved", "links added", "capacity added", "spent"],
                [
                    [
                        f"city {k}",
                        f"{100 * r['value']:.2f}%",
                        str(len(r["new"])),
                        f"{r['extra'].sum():,.0f}",
                        f"{r['cost']:.0f} / {BUDGET:.0f}",
                    ]
                    for k, r in _mine.items()
                ],
                highlight=1,
            ),
            complaints(_mine),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Watch your proposal

    The map is coloured by the patients nobody could take, by the hospital that gave up on them last. Blue lines are the links you added; blue rings are the hospitals whose capacity you raised.
    """)
    return


@app.cell(hide_code=True)
def _():
    watch_city = mo.ui.radio(options=SCENARIOS, value=SCENARIOS[0], label="city")
    watch_when = mo.ui.radio(options=["before", "after your proposal"], value="after your proposal", label="")
    mo.hstack([watch_city, watch_when], justify="start", gap=2)
    return watch_city, watch_when


@app.cell(hide_code=True)
def _(watch_city, watch_when):
    _k = watch_city.value
    if watch_when.value == "before":
        _sim, _new, _extra = SIM0[_k], (), None
    else:
        _r = run_proposal(propose, _k)
        _sim, _new, _extra = _r["sim"], _r["new"], _r["extra"]
    mo.hstack(
        [
            svg_map(_sim.dropped, _k, extra_edges=_new, extra_capacity=_extra),
            mo.vstack(
                [
                    note(f"<b>{100 * _sim.unserved:.2f}%</b> of the people unserved.", BLUE),
                    top_table(_sim.dropped, "people unserved"),
                ]
            ),
        ],
        justify="start",
        gap=2,
        wrap=True,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    ## Submit

    - One submission per team.
    - Create the URL to your notebook with the Share button at the top, then click `🔗 Copy Notebook URL`.
    - Submit the link through the Google Form: **<https://go.skojaku.com/m06mini>**
    - The two English cells (✍️ 1 and ✍️ 2) are worth more than the three scores. A team that explains a design, implements it and loses to the benchmark has done the assignment. A team with a good score and a vague paragraph has not.
    """)
    return


if __name__ == "__main__":
    app.run()
