# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "python-igraph==0.11.9",
# ]
# ///
#
# Mini project M03 -- Who gets the vaccine, and who gets the phone call?
#
# The notebook travels alone. Everything it needs -- the two networks, the
# epidemic, the scoreboard -- is generated inside this file, so a student can
# curl it and run it with no data and no repository.
#
# FOUR PENCIL CELLS, AND ONLY FOUR. Two per task: one where the team writes
# what its algorithm does in plain English, one where the algorithm exists as
# code. The plain-English cell is written first and is the thing that is
# graded. The code cell may be written by the team's coding agent from that
# description, which is the whole point of the exercise: if the description is
# vague, the agent builds the wrong thing and the score says so.
#
# EDGE_P and the per-town day horizons were calibrated by simulation, not
# guessed: EDGE_P is comfortably above the bond-percolation threshold of
# every town (the grid needs the highest, so it sets the floor), and each
# day horizon is the day an unprotected outbreak's mean size first passes
# 85% of that town, with the quarantine horizon fixed at 40% of it.

import marimo

__generated_with = "0.24.2"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    # The kit. Nothing here is yours to edit.
    import time

    import igraph
    import marimo as mo
    import numpy as np

    # ---------------------------------------------------------------- style
    INK, MUTED, RULE = "#1a1a1a", "#6b6b6b", "#d8d4cc"
    RUST, BLUE = "#b5482f", "#2f5d8a"
    SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
    MONO = "'SF Mono', Menlo, monospace"

    # ------------------------------------------------------------ the rules
    EDGE_P = 0.6  # chance one link ever carries the disease -- decided once
    SEEDS_PER_OUTBREAK = 3  # people who start every outbreak
    OUTBREAKS = 40  # outbreaks averaged per network
    VACCINE_SHARE = 0.10  # doses, as a share of the population
    QUARANTINE_SHARE = 0.05  # isolation rooms, as a share of the population
    DETECT_AT = 0.10  # the outbreak is noticed at this prevalence
    TIME_BUDGET = 20.0  # seconds one picker gets on one network

    # ------------------------------------------------------- the two towns
    def _largest_piece(n, edges):
        h = igraph.Graph(n, sorted({tuple(sorted(e)) for e in edges}))
        comp = h.connected_components()
        big = int(np.argmax(comp.sizes()))
        return h.induced_subgraph(
            [v for v in range(n) if comp.membership[v] == big]
        )

    def _grid(rows, cols):
        e = []
        for i in range(rows):
            for j in range(cols):
                v = i * cols + j
                if j + 1 < cols:
                    e.append((v, v + 1))
                if i + 1 < rows:
                    e.append((v, v + cols))
        return _largest_piece(rows * cols, e)

    def _degree_corrected_block_model(n, blocks, gamma, kbar, mix, seed):
        """Same blocks, but people inside a block differ wildly in how many
        friends they have. The degrees come from a Pareto tail, so this is the
        one network with both communities and hubs."""
        r = np.random.default_rng(seed)
        b = np.repeat(np.arange(blocks), n // blocks)
        n = len(b)
        theta = r.pareto(gamma - 1, n) + 1.0
        theta /= theta.mean()
        P = np.outer(theta, theta) * np.where(
            b[:, None] == b[None, :], 1.0, mix
        )
        P *= kbar / P.sum(1).mean()
        P = np.clip(P, 0.0, 1.0)
        iu = np.triu_indices(n, 1)
        d = r.random(len(iu[0])) < P[iu]
        return _largest_piece(n, zip(iu[0][d].tolist(), iu[1][d].tolist()))

    # name -> (builder, days the vaccination run lasts, days the quarantine
    # run lasts). Both horizons were calibrated, not guessed: the vaccination
    # horizon is where an unprotected outbreak passes 85% of the town under
    # EDGE_P-bond percolation, and the quarantine horizon is 40% of that,
    # because quarantine is judged on the weeks right after the outbreak is
    # found, not on the end of the world.
    TOWNS = {
        "grid": (lambda: _grid(18, 18), 30, 12),
        "blocks+hubs": (
            lambda: _degree_corrected_block_model(500, 4, 2.6, 6.0, 0.02, 14),
            10,
            4,
        ),
    }

    NETWORKS = {name: spec[0]() for name, spec in TOWNS.items()}
    VACCINE_DAYS = {name: spec[1] for name, spec in TOWNS.items()}
    QUARANTINE_DAYS = {name: spec[2] for name, spec in TOWNS.items()}
    ADJACENCY = {
        name: np.array(g.get_adjacency().data, dtype=np.float64)
        for name, g in NETWORKS.items()
    }

    # G1, G2, for pointing at one town without writing its name out
    LABEL = {
        name: "G" + "\u2081\u2082"[i]
        for i, name in enumerate(TOWNS)
    }

    def budget_for(name, share):
        return int(round(share * NETWORKS[name].vcount()))

    def layout_for(name, g):
        """Node positions for drawing. The grid keeps its actual rows and
        columns -- a force layout twists a lattice into something that no
        longer reads as one."""
        if name == "grid":
            cols = round(g.vcount() ** 0.5)
            return {v: (v % cols, v // cols) for v in range(g.vcount())}
        return {v: tuple(p) for v, p in enumerate(g.layout("fr"))}

    # ------------------------------------------------------- the SI epidemic
    def percolate(A, p, rng):
        """Which links can ever carry the disease, decided once per outbreak
        -- not redrawn every day. Each link is open with probability p,
        independently of every other link. This is bond percolation: the
        outbreak is then just whoever the seeds can reach through open
        links."""
        n = A.shape[0]
        iu = np.triu_indices(n, 1)
        open_edges = np.zeros_like(A)
        open_edges[iu] = (A[iu] > 0) & (rng.random(len(iu[0])) < p)
        return open_edges + open_edges.T

    def si_step(A_open, infected, alive):
        """One day of it. A susceptible, living person catches it today if an
        open link reaches them from someone already infected. Nobody ever
        recovers. This is SI, run over the percolated network."""
        exposure = A_open[:, infected].sum(axis=1)
        return infected | (~infected & alive & (exposure > 0))

    def _run_many(A, alive, starts, days, rng):
        """OUTBREAKS outbreaks, each on its own percolated network. Columns
        are outbreaks."""
        cols = []
        for c in range(starts.shape[1]):
            A_open = percolate(A, EDGE_P, rng)
            infected = np.zeros(A.shape[0], bool)
            infected[starts[:, c]] = True
            for _ in range(days):
                infected = si_step(A_open, infected, alive)
            cols.append(infected)
        return np.stack(cols, axis=1)

    def _outbreak_starts(alive, rng):
        pool = np.flatnonzero(alive)
        return np.stack(
            [
                rng.choice(pool, SEEDS_PER_OUTBREAK, replace=False)
                for _ in range(OUTBREAKS)
            ],
            axis=1,
        )

    # -------------------------------------------------------------- marking
    def _clean(chosen, limit, budget, what):
        """Whatever the picker returned, turn it into at most `budget`
        distinct valid ids, and say plainly what was thrown away."""
        notes = []
        try:
            ids = [int(v) for v in chosen]
        except TypeError:
            raise TypeError(
                f"{what} must return a list of whole numbers, got "
                f"{type(chosen).__name__}."
            ) from None
        bad = [v for v in ids if not 0 <= v < limit]
        if bad:
            notes.append(f"{len(bad)} id(s) outside 0..{limit - 1}, dropped")
            ids = [v for v in ids if 0 <= v < limit]
        seen, uniq = set(), []
        for v in ids:
            if v not in seen:
                seen.add(v)
                uniq.append(v)
        if len(uniq) < len(ids):
            notes.append(f"{len(ids) - len(uniq)} repeat(s), dropped")
        if len(uniq) > budget:
            notes.append(f"{len(uniq) - budget} over budget, dropped")
            uniq = uniq[:budget]
        return np.array(uniq, dtype=int), notes

    def score_vaccination(picker):
        """Hand out the doses, then let the outbreak run. Returns the share of
        each town infected on the last day, averaged over OUTBREAKS."""
        rows = {}
        for name, g in NETWORKS.items():
            budget = budget_for(name, VACCINE_SHARE)
            clock = time.perf_counter()
            picked = picker(list(range(g.vcount())), g.get_edgelist(), budget)
            spent = time.perf_counter() - clock
            vaccinated, notes = _clean(picked, g.vcount(), budget, "choose_vaccination")
            alive = np.ones(g.vcount(), bool)
            alive[vaccinated] = False
            starts = _outbreak_starts(alive, np.random.default_rng(1000))
            final = _run_many(
                ADJACENCY[name],
                alive,
                starts,
                VACCINE_DAYS[name],
                np.random.default_rng(1001),
            )
            rows[name] = {
                "infected": float(final.sum(0).mean() / g.vcount()),
                "used": int(len(vaccinated)),
                "budget": budget,
                "seconds": spent,
                "notes": notes,
            }
        return rows

    def contact_trace(g, infected):
        """What the health department actually holds. Every known case, every
        person a case named, and every link that touches a case. Links between
        two people who are both merely contacts are invisible, because nobody
        was asked about them."""
        cases = np.flatnonzero(infected)
        named = {int(v): g.neighbors(int(v)) for v in cases}
        people = sorted(set(cases.tolist()) | {u for s in named.values() for u in s})
        index = {p: i for i, p in enumerate(people)}
        links = sorted(
            {tuple(sorted((index[v], index[u]))) for v in named for u in named[v]}
        )
        known = igraph.Graph(len(people), links)
        known.vs["case"] = [bool(infected[p]) for p in people]
        return known, people

    def score_quarantine(picker):
        """Let the outbreak run unseen to DETECT_AT, hand over the contact
        tracing, take the picker's isolation list, then run the clock on."""
        rows = {}
        for name, g in NETWORKS.items():
            n = g.vcount()
            budget = budget_for(name, QUARANTINE_SHARE)
            A = ADJACENCY[name]
            totals, spent, notes = [], 0.0, []
            for run in range(OUTBREAKS):
                rng = np.random.default_rng(2000 + run)
                A_open = percolate(A, EDGE_P, rng)
                infected = np.zeros(n, bool)
                infected[rng.choice(n, SEEDS_PER_OUTBREAK, replace=False)] = True
                everyone = np.ones(n, bool)
                while infected.sum() / n < DETECT_AT:
                    grown = si_step(A_open, infected, everyone)
                    if (grown == infected).all():
                        break  # stalled below detection on its own -- a
                        # sub-critical outbreak, the way percolation goes
                    infected = grown
                known, people = contact_trace(g, infected)
                _nodes = list(range(known.vcount()))
                _cases = [v for v in _nodes if known.vs[v]["case"]]
                clock = time.perf_counter()
                picked = picker(_nodes, known.get_edgelist(), _cases, budget)
                spent += time.perf_counter() - clock
                local, note = _clean(
                    picked, known.vcount(), budget, "choose_quarantine"
                )
                if note and not notes:
                    notes = note
                alive = np.ones(n, bool)
                alive[[people[i] for i in local]] = False
                still_out = infected & alive
                for _ in range(QUARANTINE_DAYS[name]):
                    still_out = si_step(A_open, still_out, alive)
                totals.append((still_out | infected).sum() / n)
            rows[name] = {
                "infected": float(np.mean(totals)),
                "used": budget,
                "budget": budget,
                "seconds": spent / OUTBREAKS,
                "notes": notes,
            }
        return rows

    def overall(rows):
        return float(np.mean([r["infected"] for r in rows.values()]))

    # ------------------------------------------------- the anonymous rivals
    def rival_nobody(*args):
        return []

    def rival_random_people(nodes, edges, budget):
        return list(np.random.default_rng(7).choice(nodes, budget, replace=False))

    def rival_random_known(nodes, edges, cases, budget):
        return list(
            np.random.default_rng(7).choice(
                nodes, min(budget, len(nodes)), replace=False
            )
        )

    def _degrees(nodes, edges):
        deg = {v: 0 for v in nodes}
        for u, v in edges:
            deg[u] += 1
            deg[v] += 1
        return deg

    def benchmark_a(nodes, edges, budget):
        """Deliberately not named in the notebook. Beating it is the game."""
        neighbors = {v: set() for v in nodes}
        for u, v in edges:
            neighbors[u].add(v)
            neighbors[v].add(u)
        out = []
        for _ in range(budget):
            v = max(neighbors, key=lambda x: len(neighbors[x]))
            out.append(v)
            for u in neighbors.pop(v):
                neighbors[u].discard(v)
        return out

    def benchmark_b(nodes, edges, cases, budget):
        """Also not named."""
        deg = _degrees(nodes, edges)
        return sorted(cases, key=lambda i: -deg[i])[:budget]

    # ------------------------------------------------------------- drawing
    def _bar_row(label, value, worst, tone, bold=False):
        width = 0 if worst <= 0 else min(100.0, 100.0 * value / worst)
        weight = "700" if bold else "400"
        return (
            f'<tr><td style="padding:4px 14px 4px 0;font-family:{SANS};'
            f'font-size:14px;color:{INK};font-weight:{weight};white-space:nowrap">'
            f"{label}</td>"
            f'<td style="width:260px;padding:4px 10px 4px 0">'
            f'<div style="background:#efece6;height:12px;border-radius:2px">'
            f'<div style="width:{width:.1f}%;height:12px;background:{tone};'
            f'border-radius:2px"></div></div></td>'
            f'<td style="font-family:{MONO};font-size:14px;color:{tone};'
            f'font-weight:{weight};padding:4px 0">{value:.3f}</td></tr>'
        )

    def scoreboard(title, lines):
        """lines: (label, value, tone, bold)."""
        worst = max([v for _, v, _, _ in lines] + [1e-9])
        body = "".join(_bar_row(l, v, worst, t, b) for l, v, t, b in lines)
        return mo.Html(
            f'<div style="font-family:{SANS};font-size:13px;color:{MUTED};'
            f'letter-spacing:.06em;text-transform:uppercase;margin:16px 0 4px">'
            f"{title}</div>"
            f'<table style="border-collapse:collapse">{body}</table>'
            f'<div style="font-family:{SANS};font-size:13px;color:{MUTED};'
            f'margin-top:6px">share of the town infected when the clock stops. '
            f"lower is better.</div>"
        )

    def per_town(rows, other=None):
        head = ["", "network", "n", "budget", "your score"]
        if other:
            head.append("benchmark")
        cells = "".join(
            f'<th style="text-align:{"left" if i < 2 else "right"};'
            f'padding:4px 18px 6px 0;font-family:{SANS};font-size:12px;'
            f'color:{MUTED};font-weight:700">{h}</th>'
            for i, h in enumerate(head)
        )
        body = ""
        for name, r in rows.items():
            vals = [
                LABEL[name],
                name,
                str(NETWORKS[name].vcount()),
                str(r["budget"]),
                f"{r['infected']:.3f}",
            ]
            if other:
                vals.append(f"{other[name]['infected']:.3f}")
            body += "<tr>" + "".join(
                f'<td style="text-align:{"left" if i < 2 else "right"};'
                f'padding:5px 18px 5px 0;border-top:1px solid {RULE};'
                f'font-family:{MONO if i > 1 else SANS};font-size:14px;'
                f'color:{MUTED if i == 0 else RUST if i == 4 else INK}">'
                f"{v}</td>"
                for i, v in enumerate(vals)
            ) + "</tr>"
        return mo.Html(
            f'<table style="border-collapse:collapse;margin:10px 0">'
            f"<tr>{cells}</tr>{body}</table>"
        )

    def svg_network(nodes, edges, pos, colors, edge_colors=None, size=460):
        """A bare node-link drawing. `nodes` is a list of ids, `edges` a list
        of (u, v) id pairs, `pos` and `colors` dicts (or lists) keyed by
        those same ids. No igraph, no matplotlib -- just SVG, so any graph
        source works."""
        xs = [pos[v][0] for v in nodes]
        ys = [pos[v][1] for v in nodes]
        lo_x, hi_x = min(xs), max(xs)
        lo_y, hi_y = min(ys), max(ys)
        pad = 16

        def sx(x):
            return pad + (x - lo_x) / (hi_x - lo_x + 1e-9) * (size - 2 * pad)

        def sy(y):
            return pad + (y - lo_y) / (hi_y - lo_y + 1e-9) * (size - 2 * pad)

        lines = "".join(
            f'<line x1="{sx(pos[u][0]):.1f}" y1="{sy(pos[u][1]):.1f}" '
            f'x2="{sx(pos[v][0]):.1f}" y2="{sy(pos[v][1]):.1f}" '
            f'stroke="{edge_colors[i] if edge_colors else RULE}" stroke-width="1.2"/>'
            for i, (u, v) in enumerate(edges)
        )
        dots = "".join(
            f'<circle cx="{sx(pos[v][0]):.1f}" cy="{sy(pos[v][1]):.1f}" r="4.5" '
            f'fill="{colors[v]}" stroke="white" stroke-width="0.8"/>'
            for v in nodes
        )
        return mo.Html(
            f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
            f'style="background:#ffffff;border:1px solid {RULE};border-radius:4px">'
            f"{lines}{dots}</svg>"
        )

    def note(text, tone=BLUE):
        return mo.Html(
            f'<div style="border-left:3px solid {tone};padding:2px 0 2px 14px;'
            f'margin:14px 0;font-family:{SANS};font-size:16px;color:{INK}">'
            f"{text}</div>"
        )

    def complaints(rows):
        bad = {k: r["notes"] for k, r in rows.items() if r["notes"]}
        slow = {k: r["seconds"] for k, r in rows.items() if r["seconds"] > TIME_BUDGET}
        out = []
        for k, v in bad.items():
            out.append(f"<b>{k}</b>: {', '.join(v)}")
        for k, v in slow.items():
            out.append(f"<b>{k}</b>: took {v:.0f}s, over the {TIME_BUDGET:.0f}s budget")
        if not out:
            return mo.Html("")
        return note("<br>".join(out), RUST)


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Mini project m03

    ## Task

    Your goal is to design a pre-outbreak vaccination strategy (Task A) and an active-outbreak isolation strategy (Task B).

    Complete cells A1–B2 with written English explanations and matching Python code.

    - **Task A.** You see the whole network. No cases yet. Pick who gets the shot.
    - **Task B.** The disease is already spreading. You see the cases and the
      people they named (contact traced). Pick who should be locked up to contain the epidemics.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Rules

    - There are two states: susceptible and infected. No one recovers.
    - Every link is open with probability $p = 0.6$, determined once per outbreak and not redrawn daily. This is bond percolation: a day is one step outward through open links from whoever is already infected.
    - Every run begins with three randomly chosen individuals.
    - The score is the final fraction of the town infected, averaged over 40 runs across two towns. **Lower is better.**
    - The seed is fixed. It is the same code, the same numbers every time.
    - Do not modify the setup cell.

    ## Feel free to use AI for coding but don't let it generate ideas.

    You can use `pi` agents to help you code based on the description of your intervention strategy. Don't use it to generate the strategy itself.

    You can use so-called a *pair agent* that directly edits the marimo notebook. The tutor has this feature built-in, so all you need to do is to tell the agent which notebook you are working on. Copy & paste the following prompt:

    ```markdown

    ```

    This connects your pi agent to the marimo notebook. You can talk to it and turn your ideas into code.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Networks

    We have two networks $G_1, G_2$. Each one represents a different social network. Find a prevention and control strategy that is effective for both.
    """)
    return


@app.cell(hide_code=True)
def _():
    _rows = []
    for _name, _g in NETWORKS.items():
        _d = np.array(_g.degree())
        _rows.append(
            (
                LABEL[_name],
                _name,
                str(_g.vcount()),
                str(_g.ecount()),
                f"{_d.mean():.1f}",
                str(int(_d.max())),
                str(budget_for(_name, VACCINE_SHARE)),
                str(budget_for(_name, QUARANTINE_SHARE)),
            )
        )
    _head = ["", "network", "people", "links", "mean k", "max k", "doses", "rooms"]
    _cells = "".join(
        f'<th style="text-align:{"left" if _i < 2 else "right"};'
        f'padding:4px 16px 6px 0;font-family:{SANS};font-size:12px;'
        f'color:{MUTED};font-weight:700">{_h}</th>'
        for _i, _h in enumerate(_head)
    )
    _body = "".join(
        "<tr>"
        + "".join(
            f'<td style="text-align:{"left" if _i < 2 else "right"};'
            f'padding:5px 16px 5px 0;border-top:1px solid {RULE};'
            f'font-family:{MONO if _i > 1 else SANS};font-size:14px;'
            f'color:{MUTED if _i == 0 else INK}">{_c}</td>'
            for _i, _c in enumerate(_r)
        )
        + "</tr>"
        for _r in _rows
    )
    mo.Html(
        f'<table style="border-collapse:collapse;margin:8px 0">'
        f"<tr>{_cells}</tr>{_body}</table>"
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    ## Task A. Vaccine first, disease later

    You see the whole network. Doses for 10%. A vaccinated person cannot catch it
    and cannot pass it on.

    ### Watch it spread

    Nobody vaccinated. Pick a town, drag the day slider, and watch how far
    the disease gets -- blue links are open, meaning they can carry it; grey
    links can't. The button picks new starting people without changing
    which links are open.
    """)
    return


@app.cell(hide_code=True)
def _():
    demo_radio = mo.ui.radio(
        options=list(NETWORKS.keys()), value="grid", label="town"
    )
    reseed_button = mo.ui.button(
        value=0, on_click=lambda v: v + 1, label="pick new starting people"
    )
    day_slider = mo.ui.slider(0, 40, value=0, label="day", show_value=True)
    mo.hstack([demo_radio, reseed_button, day_slider], justify="start", gap=2)
    return day_slider, demo_radio, reseed_button


@app.cell(hide_code=True)
def _(
    day_slider,
    demo_days,
    demo_edges,
    demo_nodes,
    demo_open_edges,
    demo_pos,
):
    _inf = demo_days[day_slider.value]
    _colors = {v: (RUST if _inf[v] else INK) for v in demo_nodes}
    _edge_colors = [
        BLUE if (u, v) in demo_open_edges else "#e5e1d8" for u, v in demo_edges
    ]
    mo.vstack(
        [
            note(
                f"Day {day_slider.value}: <b>{int(_inf.sum())}</b> of "
                f"{len(demo_nodes)} infected "
                f"({100 * _inf.sum() / len(demo_nodes):.0f}%).",
                BLUE,
            ),
            svg_network(demo_nodes, demo_edges, demo_pos, _colors, _edge_colors),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ A1. Your vaccination plan, in English

    Plain words. Somebody with a pencil should be able to follow it. Four to ten
    sentences.

    Graded. Your agent writes A2 from it.
    """)
    return


@app.cell
def _():
    # ✍️ A1 — describe your vaccination algorithm in plain English.
    PLAN_A = """
    ...
    """
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ A2. The same plan, as code

    `nodes` is a list of ids. `edges` is a list of `(u, v)` id pairs. Return
    at most `budget` ids from `nodes`, as `int`.
    """)
    return


@app.function
# ✍️ A2 — implement the algorithm you described in A1.
def choose_vaccination(nodes, edges, budget):
    """Return at most `budget` ids from `nodes` to vaccinate, e.g. [3, 17, 42]."""
    return []


@app.cell(hide_code=True)
def _():
    _mine = score_vaccination(choose_vaccination)
    _bench = score_vaccination(benchmark_a)
    _lines = [
        ("nobody vaccinated", overall(score_vaccination(rival_nobody)), MUTED, False),
        ("a random 10%", overall(score_vaccination(rival_random_people)), MUTED, False),
        ("benchmark", overall(_bench), BLUE, False),
        ("your team", overall(_mine), RUST, True),
    ]
    mo.vstack(
        [
            scoreboard("task A", _lines),
            per_town(_mine, _bench),
            complaints(_mine),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
 
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    ## Task B. The disease is already running

    Nobody was vaccinated. Found once 10% is infected. Quaranteen 5% of people in the network. You do not see the network. You see every **case**, everyone a case **named**, and every link **touching a case**. Nothing else.

    Everything in light grey is invisible to you -- it exists, but nobody
    told the health department about it. Red is a confirmed case. Blue is
    someone a case named.
    """)
    return


@app.cell(hide_code=True)
def _():
    demoB_radio = mo.ui.radio(
        options=list(NETWORKS.keys()), value="blocks+hubs", label="town"
    )
    demoB_button = mo.ui.button(
        value=0, on_click=lambda v: v + 1, label="new outbreak"
    )
    mo.hstack([demoB_radio, demoB_button], justify="start", gap=2)
    return demoB_button, demoB_radio


@app.cell(hide_code=True)
def _(
    demoB_edges,
    demoB_infected,
    demoB_nodes,
    demoB_observed_edges,
    demoB_observed_nodes,
    demoB_pos,
):
    _unseen = "#ece9e2"
    _colors = {
        v: (
            RUST
            if demoB_infected[v]
            else BLUE
            if v in demoB_observed_nodes
            else _unseen
        )
        for v in demoB_nodes
    }
    _edge_colors = [
        INK if tuple(sorted((u, v))) in demoB_observed_edges else _unseen
        for u, v in demoB_edges
    ]
    _cases = int(demoB_infected.sum())
    _contacts = len(demoB_observed_nodes) - _cases
    mo.vstack(
        [
            note(
                f"<b>{_cases}</b> case(s), <b>{_contacts}</b> named contact(s). "
                f"Everything in light grey never reaches the health department.",
                BLUE,
            ),
            svg_network(demoB_nodes, demoB_edges, demoB_pos, _colors, _edge_colors),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ B1. Your isolation plan, in English

    Same as A1. Four to ten sentences.

    Graded. Your agent writes B2 from it.
    """)
    return


@app.cell
def _():
    # ✍️ B1 — describe your quarantine algorithm in plain English.
    PLAN_B = """
    ...
    """
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ B2. The same plan, as code

    `nodes` is a list of the traced people's ids. `edges` is a list of
    `(u, v)` id pairs among them. `cases` is the subset of `nodes` that are
    confirmed, the rest are contacts. Return at most `budget` ids **from
    `nodes`**. An isolated person stops infecting and stops catching.
    """)
    return


@app.function
# ✍️ B2 — implement the algorithm you described in B1.
def choose_quarantine(nodes, edges, cases, budget):
    """Return at most `budget` ids from `nodes` to isolate, e.g. [0, 5]."""
    return []


@app.cell(hide_code=True)
def _():
    _mine_b = score_quarantine(choose_quarantine)
    _bench_b = score_quarantine(benchmark_b)
    _lines_b = [
        ("nobody isolated", overall(score_quarantine(rival_nobody)), MUTED, False),
        (
            "a random 5% of the traced",
            overall(score_quarantine(rival_random_known)),
            MUTED,
            False,
        ),
        ("benchmark", overall(_bench_b), BLUE, False),
        ("your team", overall(_mine_b), RUST, True),
    ]
    mo.vstack(
        [
            scoreboard("task B", _lines_b),
            per_town(_mine_b, _bench_b),
            complaints(_mine_b),
        ]
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    ## Submit

    One per team: **<https://go.skojaku.com/m03mini>**

    Your emails, both scores, A1, B1, and this file. Save the notebook first.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    ## For your coding agent

    > A marimo notebook, `mini-project.py`.
    >
    > - Edit `# ✍️ A2` and `# ✍️ B2`. Nothing else. Not `PLAN_A`, not `PLAN_B`,
    >   not the setup cell.
    > - Build `PLAN_A` as `choose_vaccination(nodes, edges, budget)`. Build
    >   `PLAN_B` as `choose_quarantine(nodes, edges, cases, budget)`.
    > - Build what is written, not what you would have written.
    > - Plan unclear? Stop. Ask the students.
    > - `igraph` and `numpy` only. Return `list[int]`, at most `budget`, in
    >   both cases ids from `nodes`.
    > - Do not read the setup cell inside the functions. Do not special-case a
    >   town.
    > - Run it. Report both scores. If a plan loses to the benchmark, say so.
    """)
    return


@app.cell(hide_code=True)
def _(demo_radio):
    _demo_g = NETWORKS[demo_radio.value]
    demo_nodes = list(range(_demo_g.vcount()))
    demo_edges = _demo_g.get_edgelist()
    demo_pos = layout_for(demo_radio.value, _demo_g)
    demo_open = percolate(ADJACENCY[demo_radio.value], EDGE_P, np.random.default_rng(2))
    demo_open_edges = {(u, v) for u, v in demo_edges if demo_open[u, v] > 0}
    return demo_edges, demo_nodes, demo_open, demo_open_edges, demo_pos


@app.cell(hide_code=True)
def _(demo_nodes, demo_open, reseed_button):
    _rng = np.random.default_rng(100 + reseed_button.value)
    _infected = np.zeros(len(demo_nodes), bool)
    _infected[_rng.choice(len(demo_nodes), SEEDS_PER_OUTBREAK, replace=False)] = True
    _alive = np.ones(len(demo_nodes), bool)
    demo_days = [_infected]
    for _ in range(40):
        _infected = si_step(demo_open, _infected, _alive)
        demo_days.append(_infected)
    return (demo_days,)


@app.cell(hide_code=True)
def _(demoB_button, demoB_radio):
    _g = NETWORKS[demoB_radio.value]
    _A = ADJACENCY[demoB_radio.value]
    _rng = np.random.default_rng(300 + demoB_button.value)
    _open = percolate(_A, EDGE_P, _rng)
    _infected = np.zeros(_g.vcount(), bool)
    _infected[_rng.choice(_g.vcount(), SEEDS_PER_OUTBREAK, replace=False)] = True
    _everyone = np.ones(_g.vcount(), bool)
    while _infected.sum() / _g.vcount() < DETECT_AT:
        _grown = si_step(_open, _infected, _everyone)
        if (_grown == _infected).all():
            break  # stalled below detection on its own
        _infected = _grown
    _known, _people = contact_trace(_g, _infected)
    demoB_infected = _infected
    demoB_nodes = list(range(_g.vcount()))
    demoB_edges = _g.get_edgelist()
    demoB_pos = layout_for(demoB_radio.value, _g)
    demoB_observed_nodes = set(_people)
    demoB_observed_edges = {
        tuple(sorted((_people[u], _people[v]))) for u, v in _known.get_edgelist()
    }
    return (
        demoB_edges,
        demoB_infected,
        demoB_nodes,
        demoB_observed_edges,
        demoB_observed_nodes,
        demoB_pos,
    )


if __name__ == "__main__":
    app.run()
