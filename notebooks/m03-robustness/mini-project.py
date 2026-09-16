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
# The notebook travels alone. Everything it needs -- the five networks, the
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
# Reference numbers for the five networks are in
# adv-net-sci-ops/mini-project/m03-robustness/DESIGN.md. Nothing in this file
# quotes a number that was not measured by calibrate.py in that folder.

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    # The kit. Nothing here is yours to edit.
    import time

    import igraph
    import marimo as mo
    import numpy as np

    # ---------------------------------------------------------------- style
    INK, MUTED, RULE = "#1a1a1a", "#6b6b6b", "#d8d4cc"
    RUST, BLUE, GREEN = "#b5482f", "#2f5d8a", "#3f7a4e"
    SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
    MONO = "'SF Mono', Menlo, monospace"

    # ------------------------------------------------------------ the rules
    BETA = 0.04  # chance one infected neighbour infects you on one day
    SEEDS_PER_OUTBREAK = 3  # people who start every outbreak
    OUTBREAKS = 40  # outbreaks averaged per network
    VACCINE_SHARE = 0.10  # doses, as a share of the population
    QUARANTINE_SHARE = 0.05  # isolation beds, as a share of the population
    DETECT_AT = 0.10  # the outbreak is noticed at this prevalence
    TIME_BUDGET = 20.0  # seconds one picker gets on one network

    # ------------------------------------------------------- the five towns
    def _largest_piece(n, edges):
        h = igraph.Graph(n, sorted({tuple(sorted(e)) for e in edges}))
        comp = h.connected_components()
        big = int(np.argmax(comp.sizes()))
        return h.induced_subgraph(
            [v for v in range(n) if comp.membership[v] == big]
        )

    def _erdos_renyi(n, k, seed):
        r = np.random.default_rng(seed)
        iu = np.triu_indices(n, 1)
        pick = r.choice(len(iu[0]), int(round(n * k / 2)), replace=False)
        return _largest_piece(n, zip(iu[0][pick].tolist(), iu[1][pick].tolist()))

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

    def _barabasi_albert(n, m, seed):
        r = np.random.default_rng(seed)
        targets, repeated, e = list(range(m)), [], []
        for v in range(m, n):
            for t in set(targets):
                e.append((v, t))
            repeated += targets + [v] * m
            targets = [int(x) for x in r.choice(repeated, m, replace=False)]
        return _largest_piece(n, e)

    def _block_model(n, blocks, p_in, p_out, seed):
        r = np.random.default_rng(seed)
        b = np.repeat(np.arange(blocks), n // blocks)
        n = len(b)
        P = np.where(b[:, None] == b[None, :], p_in, p_out)
        iu = np.triu_indices(n, 1)
        d = r.random(len(iu[0])) < P[iu]
        return _largest_piece(n, zip(iu[0][d].tolist(), iu[1][d].tolist()))

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
    # horizon is where an unprotected outbreak passes 85% of the town, and the
    # quarantine horizon is 40% of that, because quarantine is judged on the
    # weeks right after the outbreak is found, not on the end of the world.
    TOWNS = {
        "random": (lambda: _erdos_renyi(300, 5.0, 11), 45, 18),
        "grid": (lambda: _grid(18, 18), 155, 62),
        "scale-free": (lambda: _barabasi_albert(300, 2, 12), 55, 22),
        "blocks": (lambda: _block_model(320, 4, 0.065, 0.0006, 13), 50, 20),
        "blocks+hubs": (
            lambda: _degree_corrected_block_model(500, 4, 2.6, 6.0, 0.02, 14),
            50,
            20,
        ),
    }

    NETWORKS = {name: spec[0]() for name, spec in TOWNS.items()}
    VACCINE_DAYS = {name: spec[1] for name, spec in TOWNS.items()}
    QUARANTINE_DAYS = {name: spec[2] for name, spec in TOWNS.items()}
    ADJACENCY = {
        name: np.array(g.get_adjacency().data, dtype=np.float64)
        for name, g in NETWORKS.items()
    }

    # G1 .. G5, for pointing at one town without writing its name out
    LABEL = {
        name: "G" + "\u2081\u2082\u2083\u2084\u2085"[i]
        for i, name in enumerate(TOWNS)
    }

    def budget_for(name, share):
        return int(round(share * NETWORKS[name].vcount()))

    # ------------------------------------------------------- the SI epidemic
    def si_step(A, infected, alive, rng):
        """One day of it. A susceptible person who is still in the population
        catches it from each infected neighbour with probability BETA, and the
        neighbours act independently, so with m infected neighbours the chance
        of staying clean is (1 - BETA)**m. Nobody ever recovers. This is SI."""
        exposure = A @ infected.astype(np.float64)
        caught = rng.random(infected.shape) < 1.0 - (1.0 - BETA) ** exposure
        return infected | (~infected & alive & caught)

    def _run_many(A, alive, starts, days, rng):
        """OUTBREAKS outbreaks at once. Columns are outbreaks."""
        n = A.shape[0]
        infected = np.zeros((n, starts.shape[1]), bool)
        for c in range(starts.shape[1]):
            infected[starts[:, c], c] = True
        for _ in range(days):
            exposure = A @ infected.astype(np.float64)
            caught = rng.random(infected.shape) < 1.0 - (1.0 - BETA) ** exposure
            infected |= ~infected & alive[:, None] & caught
        return infected

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
            picked = picker(g.copy(), budget)
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
                infected = np.zeros(n, bool)
                infected[rng.choice(n, SEEDS_PER_OUTBREAK, replace=False)] = True
                everyone = np.ones(n, bool)
                while infected.sum() / n < DETECT_AT:
                    infected = si_step(A, infected, everyone, rng)
                known, people = contact_trace(g, infected)
                clock = time.perf_counter()
                picked = picker(known.copy(), budget)
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
                    still_out = si_step(A, still_out, alive, rng)
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
    def rival_nobody(g, budget):
        return []

    def rival_random_people(g, budget):
        return list(
            np.random.default_rng(7).choice(g.vcount(), budget, replace=False)
        )

    def rival_random_known(known, budget):
        return list(
            np.random.default_rng(7).choice(
                known.vcount(), min(budget, known.vcount()), replace=False
            )
        )

    def benchmark_a(g, budget):
        """Deliberately not named in the notebook. Beating it is the game."""
        h = g.copy()
        h.vs["origin"] = list(range(g.vcount()))
        out = []
        for _ in range(budget):
            v = int(np.argmax(h.degree()))
            out.append(h.vs[v]["origin"])
            h.delete_vertices(v)
        return out

    def benchmark_b(known, budget):
        """Also not named."""
        cases = [i for i in range(known.vcount()) if known.vs[i]["case"]]
        cases.sort(key=lambda i: -known.degree(i))
        return cases[:budget]

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

    def note(text, tone=BLUE):
        return mo.Html(
            f'<div style="border-left:3px solid {tone};padding:2px 0 2px 14px;'
            f'margin:14px 0;font-family:{SANS};font-size:16px;color:{INK}">'
            f"{text}</div>"
        )

    def waiting(what):
        return mo.Html(
            f'<div style="font-family:{SANS};font-size:15px;color:{MUTED};'
            f'border:1.5px dashed {RULE};border-radius:4px;padding:10px 14px;'
            f'display:inline-block">Waiting on {what}.</div>'
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
    # Who gets the vaccine, and who gets the phone call?

    **Module 3 Mini-Project.** Team size: up to 3. Time limit: 90 minutes.

    An outbreak is threatening five towns, and your public health department
    is critically low on resources.

    You will make two strategic interventions:

    - **Phase 1: Pre-Outbreak Allocation.** You have the complete network map,
      but no active cases yet. Decide where to deploy preventative vaccines to
      blunt transmission.
    - **Phase 2: Active Contact Tracing.** The disease is actively spreading.
      Armed only with a roster of positive cases and their self-reported
      contacts, decide whom to call and isolate.

    ## Submission Requirements

    Submit exactly four notebook cells:

    - **A1 (Markdown / English):** Strategy and rationale for vaccine
      allocation.
    - **A2 (Python):** Implementation code for the vaccination strategy.
    - **B1 (Markdown / English):** Strategy and rationale for contact tracing.
    - **B2 (Python):** Implementation code for the tracing intervention.

    **Grading focuses primarily on your written English explanations in A1 and
    B1.**
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Rules & Parameters

    **Disease Dynamics (SI Model).** Individuals exist in one of two states:
    Susceptible (S) or Infected (I). There is no recovery. Each day, an
    infected node transmits the pathogen to each susceptible neighbor with
    probability $\beta = 0.04$. Each simulation run initializes with three
    randomly selected "patient zeroes."

    **Evaluation Metric.** The final attack rate (proportion of the population
    infected by the end of the simulation), averaged across 40 runs and across
    all five town networks. **Lower is better.** Random seeds are strictly
    fixed, so identical code produces deterministic results, and the number
    you see here is the number we see when we read your submission.

    **Integrity Constraint.** Do not alter any part of the test harness in the
    hidden setup cell. Modifying the harness will invalidate your output and
    disqualify your score.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### The five towns

    Let the five towns be represented by graphs $G_1, \dots, G_5$.

    None correspond to real places. Each reflects a distinct theoretical model
    of social connectivity with its own graph topology. Because their network
    properties differ significantly, a strategy optimized for one graph $G_i$
    may perform poorly on another $G_j$.
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
    _head = ["", "network", "people", "links", "mean k", "max k", "doses", "beds"]
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
    **Doses** is 10% of the town and **beds** is 5%. In task B the outbreak is
    found once 10% of the town already has it.

    ---

    ## Task A. The vaccine arrives before the disease does

    You have the whole network in front of you and enough doses for 10% of the
    town. A vaccinated person cannot catch it and cannot pass it on, so for
    the purposes of the epidemic they are simply gone.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ A1. Your vaccination algorithm, in English

    Write it so somebody who has never seen your code could carry it out with
    a pencil. Four to ten sentences.

    **This cell is what is graded.** Your coding agent writes A2 from it.
    """)
    return


@app.cell
def _():
    # ✍️ A1 — describe your vaccination algorithm in plain English.
    PLAN_A = """
    ...
    """
    return (PLAN_A,)


@app.cell(hide_code=True)
def _(PLAN_A):
    _words = len(PLAN_A.replace(".", " ").split())
    if PLAN_A.strip().strip(".") == "":
        _out = waiting("A1")
    elif _words < 40:
        _out = note(f"{_words} words. Too short to hand to anybody.", RUST)
    else:
        _out = mo.vstack(
            [note(f"{_words} words.", GREEN), mo.md(PLAN_A)]
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ A2. The same algorithm, as code

    ```python
    def choose_vaccination(g, budget):
        ...
    ```

    `g` is an `igraph.Graph`, a private copy you may destroy. Return at most
    `budget` vertex ids as a list of `int`. `igraph` and `numpy` only, 20
    seconds per network.
    """)
    return


@app.cell
def _():
    # ✍️ A2 — implement the algorithm you described in A1.
    def choose_vaccination(g, budget):
        return []
    return (choose_vaccination,)


@app.cell(hide_code=True)
def _(choose_vaccination):
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
    ---

    ## Task B. The outbreak is already running

    Nobody was vaccinated. The outbreak is found once **10% of the town is
    infected**, and you get isolation beds for 5%.

    **You do not see the network.** You see every known **case**, every person
    a case named as a contact, and every link that **touches a case**. Two
    contacts who were never asked about each other are not connected in your
    copy.
    """)
    return


@app.cell(hide_code=True)
def _():
    _g = NETWORKS["blocks+hubs"]
    _rng = np.random.default_rng(2000)
    _inf = np.zeros(_g.vcount(), bool)
    _inf[_rng.choice(_g.vcount(), SEEDS_PER_OUTBREAK, replace=False)] = True
    _all = np.ones(_g.vcount(), bool)
    while _inf.sum() / _g.vcount() < DETECT_AT:
        _inf = si_step(ADJACENCY["blocks+hubs"], _inf, _all, _rng)
    _known, _ = contact_trace(_g, _inf)
    _cases = sum(_known.vs["case"])
    note(
        f"One outbreak on <b>blocks+hubs</b>, for scale. The town has "
        f"{_g.vcount()} people and {_g.ecount()} links. When it is found there "
        f"are <b>{_cases} cases</b>, the tracing turns up "
        f"<b>{_known.vcount() - _cases} contacts</b>, and you hold "
        f"<b>{_known.ecount()} links</b> out of the {_g.ecount()} that exist. "
        f"You have <b>{budget_for('blocks+hubs', QUARANTINE_SHARE)} beds</b>."
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ B1. Your quarantine algorithm, in English

    Same as A1, for the traced graph. Four to ten sentences.

    **This cell is what is graded.** Your coding agent writes B2 from it.
    """)
    return


@app.cell
def _():
    # ✍️ B1 — describe your quarantine algorithm in plain English.
    PLAN_B = """
    ...
    """
    return (PLAN_B,)


@app.cell(hide_code=True)
def _(PLAN_B):
    _words = len(PLAN_B.replace(".", " ").split())
    if PLAN_B.strip().strip(".") == "":
        _out = waiting("B1")
    elif _words < 40:
        _out = note(f"{_words} words. Too short to hand to anybody.", RUST)
    else:
        _out = mo.vstack([note(f"{_words} words.", GREEN), mo.md(PLAN_B)])
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ B2. The same algorithm, as code

    ```python
    def choose_quarantine(known, budget):
        ...
    ```

    `known` is an `igraph.Graph` on the traced people, carrying one vertex
    attribute, `known.vs["case"]`, which is `True` for a case and `False` for
    a contact. Return at most `budget` vertex ids **of `known`**, not of the
    real network.

    A quarantined person stops infecting and stops being infected. Cases and
    healthy contacts are both allowed.
    """)
    return


@app.cell
def _():
    # ✍️ B2 — implement the algorithm you described in B1.
    def choose_quarantine(known, budget):
        return []
    return (choose_quarantine,)


@app.cell(hide_code=True)
def _(choose_quarantine):
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

    One submission per team, at **<https://go.skojaku.com/m03mini>**. The form
    asks for your Binghamton email addresses, your two scores, the text of A1
    and B1, and this notebook file. Save the notebook first, because marimo
    writes your cells back into this `.py`.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    ## For your coding agent

    > You are helping a student team on a marimo notebook, `mini-project.py`.
    >
    > Edit **only** the cells marked `# ✍️ A2` and `# ✍️ B2`. Do not touch the
    > setup cell, `PLAN_A` or `PLAN_B`.
    >
    > Implement `PLAN_A` as `choose_vaccination(g, budget)` and `PLAN_B` as
    > `choose_quarantine(known, budget)`. Implement what is written, not what
    > you would have written. If a plan is ambiguous, stop and ask the
    > students rather than guessing.
    >
    > `igraph` and `numpy` only. Return a list of `int`, at most `budget` of
    > them, indexing `known` in B2. Do not read anything from the setup cell
    > inside the two functions and do not special-case a network.
    >
    > Then run it and report both scores. If a plan loses to the benchmark,
    > say so rather than tuning the code until it does not.
    """)
    return


if __name__ == "__main__":
    app.run()
