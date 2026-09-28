# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "python-igraph==0.11.9",
# ]
# ///
#
# Mini project M04 -- Who did your survey reach?
#
# Grown from the 2025 respondent-driven-sampling assignment
# (advnetsci-node-degree): the same idea -- a survey that spreads by friends
# naming friends, and a sample the friendship paradox tilts toward hubs --
# turned into a team exercise in the shape of the M03 mini-project.
#
# The notebook travels alone. The two towns, the colours, the survey and the
# scoreboard are all generated inside this file.
#
# TWO PENCIL CELLS. PLAN is the team's algorithm in plain English and is what
# is graded. run_survey is the same algorithm as code, which the team's coding
# agent may write from PLAN. A vague plan builds the wrong code, and the score
# says so.
#
# The colours were calibrated by simulation, not guessed. With BUDGET = 150
# and three seeds, averaged over 50 surveys, the error ladder is roughly
#
#                           grid    blocks
#   150 people at random    0.05    0.05    (the floor; not allowed here)
#   starting code           0.10    0.15    (snowball, count the sample)
#   benchmark               0.10    0.10    (snowball, weight by 1/degree)
#   one-coupon chains, 1/k  0.09    0.08    (a plan a team can find)
#
# so re-weighting alone fixes the blocks town and does nothing for the grid,
# where the survey is stuck in one neighbourhood of colour patches. A team has
# to change who gets asked, not only how the answers are counted, to win on
# both.

import marimo

__generated_with = "0.25.0"
app = marimo.App(width="medium")

with app.setup(hide_code=True):
    # The kit. Nothing here is yours to edit.
    import random
    import time
    import types

    import igraph
    import marimo as mo
    import numpy as np

    # ---------------------------------------------------------------- style
    INK, MUTED, RULE = "#1a1a1a", "#6b6b6b", "#d8d4cc"
    RUST, BLUE = "#b5482f", "#2f5d8a"
    SANS = "'Helvetica Neue', Helvetica, Arial, sans-serif"
    MONO = "'SF Mono', Menlo, monospace"

    # The four groups. The name is what a respondent tells you; the hex is
    # only for drawing. Checked for colour-blind separation on white.
    GROUPS = {
        "blue": "#2a78d6",
        "orange": "#eb6834",
        "aqua": "#1baf7a",
        "yellow": "#eda100",
    }
    COLOR_NAMES = list(GROUPS)

    # ------------------------------------------------------------ the rules
    BUDGET = 150  # interviews you can pay for, per survey
    SEEDS = 3  # people drawn at random to start every survey
    COUPONS = 3  # friends one respondent can name
    SURVEYS = 50  # surveys averaged per town
    TIME_BUDGET = 20.0  # seconds all SURVEYS surveys get on one town

    # ------------------------------------------------------- the two towns
    def _largest_piece(n, edges, attrs):
        h = igraph.Graph(n, sorted({tuple(sorted(e)) for e in edges}))
        for key, values in attrs.items():
            h.vs[key] = list(values)
        comp = h.connected_components()
        big = int(np.argmax(comp.sizes()))
        return h.induced_subgraph(
            [v for v in range(n) if comp.membership[v] == big]
        )

    def _grid(side, diagonal, seed):
        """A square lattice. Each square also gets each of its two diagonals
        with probability `diagonal`, so degrees run from 2 to 8 instead of
        being almost all 4."""
        r = np.random.default_rng(seed)
        e = []
        for i in range(side):
            for j in range(side):
                v = i * side + j
                if j + 1 < side:
                    e.append((v, v + 1))
                if i + 1 < side:
                    e.append((v, v + side))
                if i + 1 < side and j + 1 < side and r.random() < diagonal:
                    e.append((v, v + side + 1))
                if i + 1 < side and j > 0 and r.random() < diagonal:
                    e.append((v, v + side - 1))
        n = side * side
        return _largest_piece(
            n,
            e,
            {"x": [v % side for v in range(n)], "y": [v // side for v in range(n)]},
        )

    def _degree_corrected_block_model(n, blocks, gamma, kbar, mix, seed):
        """Four communities, and inside each one a few hubs and many people
        with two or three friends (a Pareto tail of degrees)."""
        r = np.random.default_rng(seed)
        b = np.repeat(np.arange(blocks), n // blocks)
        n = len(b)
        theta = r.pareto(gamma - 1, n) + 1.0
        theta /= theta.mean()
        P = np.outer(theta, theta) * np.where(b[:, None] == b[None, :], 1.0, mix)
        P *= kbar / P.sum(1).mean()
        P = np.clip(P, 0.0, 1.0)
        iu = np.triu_indices(n, 1)
        d = r.random(len(iu[0])) < P[iu]
        return _largest_piece(
            n, zip(iu[0][d].tolist(), iu[1][d].tolist()), {"block": b}
        )

    def _paint(g, affinity, lean, seed):
        """Give everyone a colour. `affinity` (people x colours) says which
        colours are common where a person lives; `lean` says how much each
        colour leans toward people with many friends. Both are tendencies,
        not rules: the draw is random."""
        r = np.random.default_rng(seed)
        logk = np.log(np.array(g.degree(), float))
        z = (logk - logk.mean()) / logk.std()
        s = affinity + np.outer(z, lean)
        return np.argmax(s + r.gumbel(size=s.shape), axis=1)

    def _grid_town():
        side = 30
        g = _grid(side, 0.25, 1)
        # Colour comes in patches a few streets wide: 22 blob centres,
        # each belonging to one colour.
        xy = np.array([g.vs["x"], g.vs["y"]], float).T
        r = np.random.default_rng(5)
        m = side * side // 40
        centres = r.uniform(0, side, (m, 2))
        owner = np.arange(m) % len(GROUPS)
        near = np.exp(
            -((xy[:, None, :] - centres[None]) ** 2).sum(-1) / (2 * 3.0**2)
        )
        affinity = np.zeros((g.vcount(), len(GROUPS)))
        for j in range(m):
            affinity[:, owner[j]] = np.maximum(affinity[:, owner[j]], near[:, j])
        return g, _paint(g, 2.0 * affinity, np.array([0.4, 0.1, -0.1, -0.4]), 6)

    def _block_town():
        g = _degree_corrected_block_model(1000, 4, 2.5, 7.0, 0.03, 14)
        # Each community has a favourite colour, and blue leans toward hubs.
        home = np.eye(len(GROUPS))[np.array(g.vs["block"])]
        lean = np.array([0.8, 0.27, -0.27, -0.8])
        return g, _paint(g, 1.0 * home, lean, 7)

    TOWNS = {"grid": _grid_town(), "blocks": _block_town()}
    NETWORKS = {name: town[0] for name, town in TOWNS.items()}
    COLORS = {name: town[1] for name, town in TOWNS.items()}
    TRUE_SHARES = {
        name: np.bincount(c, minlength=len(GROUPS)) / len(c)
        for name, c in COLORS.items()
    }

    # G1, G2, for pointing at one town without writing its name out
    LABEL = {name: "G" + "₁₂"[i] for i, name in enumerate(TOWNS)}

    def _layout(name, g):
        """The grid keeps its streets. The block town gets a force layout,
        drawn once with a fixed seed so it never moves."""
        if name == "grid":
            return [(x, y) for x, y in zip(g.vs["x"], g.vs["y"])]
        igraph.set_random_number_generator(random.Random(3))
        return [tuple(p) for p in g.layout("fr", niter=1500)]

    LAYOUTS = {name: _layout(name, g) for name, g in NETWORKS.items()}

    # ---------------------------------------------------------- the survey
    def open_survey(name, rng):
        """One survey of one town. Returns (survey, record).

        `survey` is the only door into the town: the seeds, and two things
        you can do -- interview someone, and ask someone you interviewed to
        name a friend. `record` is what the drawing replays: every interview
        in order, with who referred that person."""
        g, colors = NETWORKS[name], COLORS[name]
        seeds = [int(v) for v in rng.choice(g.vcount(), SEEDS, replace=False)]
        reachable = set(seeds)
        answers = {}
        referred_by = {}
        left_to_name = {}
        record = []

        def budget_left():
            return BUDGET - len(answers)

        def interview(person):
            person = int(person)
            if person in answers:
                return dict(answers[person])  # asking twice is free
            if person not in reachable:
                raise ValueError(
                    f"person {person} was never named by anyone you "
                    "interviewed, and is not a seed. You cannot reach them."
                )
            if budget_left() <= 0:
                raise RuntimeError(
                    f"no budget left: all {BUDGET} interviews are spent."
                )
            answers[person] = {
                "degree": int(g.degree(person)),
                "color": COLOR_NAMES[colors[person]],
            }
            friends = g.neighbors(person)
            left_to_name[person] = [
                int(f) for f in rng.permutation(friends)[:COUPONS]
            ]
            record.append((person, referred_by.get(person)))
            return dict(answers[person])

        def refer(person):
            person = int(person)
            if person not in answers:
                raise ValueError(
                    f"interview person {person} before asking them to name "
                    "a friend."
                )
            if not left_to_name[person]:
                return None  # out of coupons, or out of friends
            friend = left_to_name[person].pop()
            reachable.add(friend)
            referred_by.setdefault(friend, person)
            return friend

        survey = types.SimpleNamespace(
            colors=list(COLOR_NAMES),
            seeds=list(seeds),
            budget=BUDGET,
            budget_left=budget_left,
            interview=interview,
            refer=refer,
        )
        return survey, record

    # -------------------------------------------------------------- marking
    def clean_estimate(estimate):
        """Whatever came back, turn it into one share per colour that sums
        to 1, and say plainly what was thrown away."""
        notes = []
        if not isinstance(estimate, dict):
            raise TypeError(
                "run_survey must return a dict like {'blue': 0.3, ...}, got "
                f"{type(estimate).__name__}."
            )
        unknown = [k for k in estimate if k not in GROUPS]
        if unknown:
            notes.append(f"unknown colour(s) {unknown}, dropped")
        v = np.array([max(float(estimate.get(c, 0.0)), 0.0) for c in COLOR_NAMES])
        if v.sum() <= 0:
            notes.append("all shares zero")
            return np.full(len(GROUPS), 1 / len(GROUPS)), notes
        if abs(v.sum() - 1) > 1e-6:
            notes.append("shares did not add up to 1, rescaled")
        return v / v.sum(), notes

    def error_of(shares, name):
        """Total variation distance: the share of your estimate that sits on
        the wrong colour. 0 is perfect, 1 is as wrong as it gets."""
        return float(0.5 * np.abs(shares - TRUE_SHARES[name]).sum())

    def score(fn):
        rows = {}
        for name in NETWORKS:
            errors, notes, spent = [], [], 0.0
            for run in range(SURVEYS):
                survey, _ = open_survey(name, np.random.default_rng(1000 + run))
                clock = time.perf_counter()
                try:
                    shares, note = clean_estimate(fn(survey))
                except Exception as err:  # noqa: BLE001 -- say it, score it
                    shares, note = None, [f"{type(err).__name__}: {err}"]
                spent += time.perf_counter() - clock
                if note and not notes:
                    notes = note
                errors.append(1.0 if shares is None else error_of(shares, name))
            rows[name] = {"error": float(np.mean(errors)), "seconds": spent, "notes": notes}
        return rows

    def overall(rows):
        return float(np.mean([r["error"] for r in rows.values()]))

    # ------------------------------------------------- the anonymous rivals
    def _snowball(survey):
        """Interview the seeds, hand every respondent all their coupons, and
        interview whoever they name, first come first served."""
        queue, met = list(survey.seeds), []
        while queue and survey.budget_left() > 0:
            person = queue.pop(0)
            if person in met:
                continue
            met.append(person)
            answer = survey.interview(person)
            yield answer
            friend = survey.refer(person)
            while friend is not None:
                queue.append(friend)
                friend = survey.refer(person)

    def floor_score():
        rows = {}
        for name, c in COLORS.items():
            errors = []
            for run in range(SURVEYS):
                pick = np.random.default_rng(1000 + run).choice(
                    len(c), BUDGET, replace=False
                )
                errors.append(
                    error_of(np.bincount(c[pick], minlength=len(GROUPS)) / BUDGET, name)
                )
            rows[name] = {"error": float(np.mean(errors)), "seconds": 0.0, "notes": []}
        return rows

    def starting_code(survey):
        counts = {c: 0 for c in survey.colors}
        for answer in _snowball(survey):
            counts[answer["color"]] += 1
        total = sum(counts.values())
        return {c: counts[c] / total for c in counts}

    def benchmark(survey):
        """Deliberately not named in the notebook. Beating it is the game."""
        weight = {c: 0.0 for c in survey.colors}
        for answer in _snowball(survey):
            weight[answer["color"]] += 1 / answer["degree"]
        total = sum(weight.values())
        return {c: weight[c] / total for c in weight}

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
            f'<td style="font-family:{MONO};font-size:14px;color:{INK};'
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
            f'margin-top:6px">share of the estimate on the wrong colour, '
            f"averaged over {SURVEYS} surveys per town. lower is better.</div>"
        )

    def table_html(head, rows, highlight=None):
        cells = "".join(
            f'<th style="text-align:{"left" if i < 2 else "right"};'
            f'padding:4px 18px 6px 0;font-family:{SANS};font-size:12px;'
            f'color:{MUTED};font-weight:700">{h}</th>'
            for i, h in enumerate(head)
        )
        body = "".join(
            "<tr>"
            + "".join(
                f'<td style="text-align:{"left" if i < 2 else "right"};'
                f'padding:5px 18px 5px 0;border-top:1px solid {RULE};'
                f'font-family:{MONO if i > 1 else SANS};font-size:14px;'
                f'color:{MUTED if i == 0 else RUST if i == highlight else INK}">'
                f"{v}</td>"
                for i, v in enumerate(row)
            )
            + "</tr>"
            for row in rows
        )
        return mo.Html(
            f'<table style="border-collapse:collapse;margin:10px 0">'
            f"<tr>{cells}</tr>{body}</table>"
        )

    def per_town(rows, other):
        return table_html(
            ["", "town", "people", "your error", "benchmark"],
            [
                [
                    LABEL[name],
                    name,
                    str(NETWORKS[name].vcount()),
                    f"{r['error']:.3f}",
                    f"{other[name]['error']:.3f}",
                ]
                for name, r in rows.items()
            ],
            highlight=3,
        )

    def swatch(color, size=10):
        return (
            f'<span style="display:inline-block;width:{size}px;height:{size}px;'
            f'border-radius:50%;background:{GROUPS[color]};margin-right:6px;'
            f'vertical-align:middle"></span>'
        )

    def svg_survey(name, record, upto, size=520):
        """The town, every person a circle whose area grows with their degree
        and whose fill is their colour. People the survey has not reached are
        faded. A dark line runs from each respondent to the person who named
        them."""
        g, colors, pos = NETWORKS[name], COLORS[name], LAYOUTS[name]
        xs = [p[0] for p in pos]
        ys = [p[1] for p in pos]
        lo_x, hi_x, lo_y, hi_y = min(xs), max(xs), min(ys), max(ys)
        pad = 18

        def sx(x):
            return pad + (x - lo_x) / (hi_x - lo_x + 1e-9) * (size - 2 * pad)

        def sy(y):
            return pad + (y - lo_y) / (hi_y - lo_y + 1e-9) * (size - 2 * pad)

        deg = np.array(g.degree())
        radius = 1.6 + 1.1 * np.sqrt(deg)
        met = [p for p, _ in record[:upto]]
        met_set = set(met)
        links = "".join(
            f'<line x1="{sx(pos[u][0]):.1f}" y1="{sy(pos[u][1]):.1f}" '
            f'x2="{sx(pos[v][0]):.1f}" y2="{sy(pos[v][1]):.1f}" '
            f'stroke="#ebe7df" stroke-width="0.6"/>'
            for u, v in g.get_edgelist()
        )
        chain = "".join(
            f'<line x1="{sx(pos[by][0]):.1f}" y1="{sy(pos[by][1]):.1f}" '
            f'x2="{sx(pos[p][0]):.1f}" y2="{sy(pos[p][1]):.1f}" '
            f'stroke="{INK}" stroke-width="1.6"/>'
            for p, by in record[:upto]
            if by is not None
        )

        def dot(v, faded):
            hex_ = GROUPS[COLOR_NAMES[colors[v]]]
            if faded:
                return (
                    f'<circle cx="{sx(pos[v][0]):.1f}" cy="{sy(pos[v][1]):.1f}" '
                    f'r="{radius[v]:.1f}" fill="{hex_}" fill-opacity="0.22"/>'
                )
            return (
                f'<circle cx="{sx(pos[v][0]):.1f}" cy="{sy(pos[v][1]):.1f}" '
                f'r="{radius[v]:.1f}" fill="{hex_}" stroke="{INK}" '
                f'stroke-width="1.2"/>'
            )

        # biggest first, so a hub never hides the people beside it
        order = np.argsort(-deg)
        faded = "".join(dot(v, True) for v in order if v not in met_set)
        solid = "".join(dot(v, False) for v in order if v in met_set)
        return mo.Html(
            f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
            f'style="background:#ffffff;border:1px solid {RULE};border-radius:4px">'
            f"{links}{faded}{chain}{solid}</svg>"
        )

    def share_bars(title, shares, truth):
        """One row per colour: a bar for `shares`, a black tick where the
        town really is."""
        rows = ""
        for i, c in enumerate(COLOR_NAMES):
            w, t = 100 * shares[i], 100 * truth[i]
            rows += (
                f'<tr><td style="padding:3px 10px 3px 0;font-family:{SANS};'
                f'font-size:14px;color:{INK};white-space:nowrap">'
                f"{swatch(c)}{c}</td>"
                f'<td style="width:220px;padding:3px 10px 3px 0">'
                f'<div style="position:relative;background:#efece6;height:12px;'
                f'border-radius:2px">'
                f'<div style="width:{min(w, 100) * 2:.1f}%;max-width:100%;height:12px;'
                f'background:{GROUPS[c]};border-radius:2px"></div>'
                f'<div style="position:absolute;left:{min(t * 2, 100):.1f}%;top:-3px;'
                f'width:2px;height:18px;background:{INK}"></div></div></td>'
                f'<td style="font-family:{MONO};font-size:13px;color:{INK};'
                f'white-space:nowrap">{w:.0f}%'
                f'<span style="color:{MUTED}"> · town {t:.0f}%</span></td></tr>'
            )
        return mo.Html(
            f'<div style="font-family:{SANS};font-size:13px;color:{MUTED};'
            f'letter-spacing:.06em;text-transform:uppercase;margin:10px 0 4px">'
            f"{title}</div>"
            f'<table style="border-collapse:collapse">{rows}</table>'
        )

    def note(text, tone=BLUE):
        return mo.Html(
            f'<div style="border-left:3px solid {tone};padding:2px 0 2px 14px;'
            f'margin:14px 0;font-family:{SANS};font-size:16px;color:{INK}">'
            f"{text}</div>"
        )

    def complaints(rows):
        out = [f"<b>{k}</b>: {', '.join(r['notes'])}" for k, r in rows.items() if r["notes"]]
        out += [
            f"<b>{k}</b>: took {r['seconds']:.0f}s, over the "
            f"{TIME_BUDGET:.0f}s budget"
            for k, r in rows.items()
            if r["seconds"] > TIME_BUDGET
        ]
        return note("<br>".join(out), RUST) if out else mo.Html("")


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Mini project m04

    ## Task

    Everyone in town is blue, orange, aqua, or yellow. Your goal is to estimate each color's share of the town. There is no list of residents, so you start from 3 random people (seeds) and have 150 interviews. Each interview gives color and degree (number of friends); that person names up to 3 friends, and only named people can be interviewed next.

    People reached through friends tend to have many friends, and colors lean weakly with degree, biasing the sample. Colors also cluster, keeping surveys local.

    Match a 150-person random sample by changing who you interview, how you count, or both. Cell 1 is your graded English plan. An AI agent may write Cell 2's code from it.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Rules

    Friends named are picked at random; you cannot choose them, and they may already be interviewed. Only seeds and named people can be interviewed. Each new interview costs 1 of your 150 budget; interviewing the same person again is free. An interview yields color and degree only.

    Your score is the fraction of your estimate placed on the wrong colors, averaged over 50 surveys per town across two towns. Lower is better, and 0 is perfect. The random numbers are fixed, so the same code always gets the same score. Use only the `survey` object; do not edit the setup cell.

    ## Use AI for the code, not for the idea

    Write cell 1 (the plan, graded) yourselves; an AI agent may write cell 2 (the code) from it. To pair an AI agent with this notebook, follow the [marimo pair quickstart](https://docs.marimo.io/guides/generate_with_ai/marimo_pair/#quickstart).
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Two towns

    $G_1$ is a grid with colors in patches. $G_2$ has four communities, each favoring one color, plus hubs. The table below lists size, mean and max degree, and true color shares for checking; your code never sees them. Your algorithm must work on both.
    """)
    return


@app.cell(hide_code=True)
def _():
    _rows = []
    for _name, _g in NETWORKS.items():
        _d = np.array(_g.degree())
        _rows.append(
            [LABEL[_name], _name, str(_g.vcount()), str(_g.ecount()), f"{_d.mean():.1f}", str(int(_d.max()))]
            + [f"{100 * s:.0f}%" for s in TRUE_SHARES[_name]]
        )
    table_html(
        ["", "town", "people", "links", "mean k", "max k"]
        + [f"{swatch(c)}{c}" for c in COLOR_NAMES],
        _rows,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## Watch a survey

    Choose a town and a survey (the starting code or yours). The slider replays interviews in order, and "new seeds" restarts. Circle size shows degree, fill shows color, faded nodes were not reached, and dark lines show who named whom. Bars compare colors met against the town (black tick), and display the final estimate and error.
    """)
    return


@app.cell(hide_code=True)
def _():
    town_radio = mo.ui.radio(options=list(NETWORKS), value="blocks", label="town")
    who_radio = mo.ui.radio(
        options=["starting code", "your team"], value="starting code", label="survey"
    )
    reseed_button = mo.ui.button(
        value=0, on_click=lambda v: v + 1, label="new seeds"
    )
    step_slider = mo.ui.slider(
        0, BUDGET, value=BUDGET, label="interviews", show_value=True
    )
    mo.hstack([town_radio, who_radio, reseed_button, step_slider], justify="start", gap=2)
    return reseed_button, step_slider, town_radio, who_radio


@app.cell(hide_code=True)
def _(demo_estimate, demo_record, step_slider, town_radio):
    _name = town_radio.value
    _upto = min(step_slider.value, len(demo_record))
    _met = [p for p, _ in demo_record[:_upto]]
    _colors = COLORS[_name]
    _raw = (
        np.bincount(_colors[_met], minlength=len(GROUPS)) / len(_met)
        if _met
        else np.zeros(len(GROUPS))
    )
    _panel = [
        note(
            f"<b>{_upto}</b> of {len(demo_record)} interviews.",
            BLUE,
        ),
        share_bars("the people met so far", _raw, TRUE_SHARES[_name]),
    ]
    if isinstance(demo_estimate, str):
        _panel.append(note(demo_estimate, RUST))
    else:
        _panel.append(
            share_bars(
                f"what run_survey reports · error {error_of(demo_estimate, _name):.3f}",
                demo_estimate,
                TRUE_SHARES[_name],
            )
        )
    mo.hstack(
        [svg_survey(_name, demo_record, _upto), mo.vstack(_panel)],
        justify="start",
        gap=2,
        wrap=True,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ 1. Your survey plan, in English

    Write 4 to 10 plain sentences a person could follow with a pencil: who you interview, in what order, and how you turn answers into shares. This plan is graded; the agent codes from it.
    """)
    return


@app.cell
def _():
    # ✍️ 1 — describe your survey and your estimate in plain English.
    PLAN = """
    ...
    """
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ 2. The same plan, as code

    `run_survey(survey)` returns a dictionary of shares per color rescaled to sum to 1, such as `{"blue": 0.3, "orange": 0.2, "aqua": 0.25, "yellow": 0.25}`.

    | what | gives |
    | :--- | :--- |
    | `survey.seeds` | the 3 starting ids |
    | `survey.colors` | the four color names |
    | `survey.budget` | 150 |
    | `survey.budget_left()` | interviews left |
    | `survey.interview(person)` | `{"degree": 4, "color": "aqua"}`; costs 1 the first time |
    | `survey.refer(person)` | one friend id, or `None` after 3; interview person first |

    The starting code is a plain snowball sample that counts colors as they come. Replace it.
    """)
    return


@app.function
# ✍️ 2 — implement the algorithm you described in PLAN.
def run_survey(survey):
    """Spend the budget, then return your estimate of each colour's share of
    the town, e.g. {"blue": 0.3, "orange": 0.2, "aqua": 0.25, "yellow": 0.25}.

    This starting version is a plain snowball: interview the seeds, ask every
    respondent to name friends, interview whoever is named first, and report
    the colours of the people met, as they are."""
    queue = list(survey.seeds)
    met = []
    counts = {color: 0 for color in survey.colors}
    while queue and survey.budget_left() > 0:
        person = queue.pop(0)
        if person in met:
            continue
        met.append(person)
        answer = survey.interview(person)  # {"degree": 4, "color": "aqua"}
        counts[answer["color"]] += 1
        friend = survey.refer(person)
        while friend is not None:
            queue.append(friend)
            friend = survey.refer(person)
    total = sum(counts.values())
    return {color: counts[color] / total for color in counts}


@app.cell(hide_code=True)
def _():
    _mine = score(run_survey)
    _bench = score(benchmark)
    _lines = [
        (f"{BUDGET} people drawn at random (not allowed)", overall(floor_score()), MUTED, False),
        ("starting code", overall(score(starting_code)), MUTED, False),
        ("benchmark", overall(_bench), BLUE, False),
        ("your team", overall(_mine), RUST, True),
    ]
    mo.vstack([scoreboard("the survey", _lines), per_town(_mine, _bench), complaints(_mine)])
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    ## Submit

    - One submission per team.
    - Create the URL to your notebook with the Share button at the top, then click `🔗 Copy Notebook URL`.
    - Submit the link through the Google Form: **<https://go.skojaku.com/m04mini>**
    """)
    return


@app.cell(hide_code=True)
def _(reseed_button, town_radio, who_radio):
    _fn = starting_code if who_radio.value == "starting code" else run_survey
    _survey, demo_record = open_survey(
        town_radio.value, np.random.default_rng(500 + reseed_button.value)
    )
    try:
        demo_estimate, _ = clean_estimate(_fn(_survey))
    except Exception as _err:  # noqa: BLE001 -- show it beside the drawing
        demo_estimate = f"run_survey stopped: {type(_err).__name__}: {_err}"
    return demo_estimate, demo_record


if __name__ == "__main__":
    app.run()
