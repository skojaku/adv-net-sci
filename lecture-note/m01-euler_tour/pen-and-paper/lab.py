# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "numpy==2.2.6",
#     "pandas==2.3.1",
#     "tabulate",
#     "python-igraph==0.11.9",
#     "matplotlib==3.10.3",
# ]
# ///
#
# Part 4 of the Module 1 pen-and-paper sheet, done alone at a laptop.
#
# It is the mini-project's notebook with the group work taken out and the city
# nailed down: the four Upstate New York cities and seven highways the student
# has just spent an hour drawing on. Everything asked here is something they
# have already written in pencil, which is the point -- the machine agrees with
# them, or one of the two is wrong and they find out which.
#
# The map drawing is deliberately the sheet's map, down to the bends in the
# roads, so a student looking from paper to screen sees the same thing twice.

import marimo

__generated_with = "0.24.0"
app = marimo.App(width="medium", css_file="lecture-hall.css")

with app.setup(hide_code=True):
    # The drawing kit. Nothing here is yours to edit.
    import marimo as mo
    import numpy as np
    import pandas as pd
    import igraph
    import matplotlib.pyplot as plt

    INK = "#1D1E21"
    RULE = "#D9D2C2"
    BLUE = "#3959A6"
    RUST = "#B14434"
    PAPER = "#FFFDF7"
    MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"
    SANS = "system-ui,-apple-system,'Segoe UI',Roboto,sans-serif"
    WOBBLE = "7px 4px 8px 5px / 5px 8px 4px 7px"

    # The sheet's map. Cities are numbered the way the edge list needs them,
    # 0 to 3, and the roads are in the order the animation walks them.
    NY_NAMES = ["Ithaca", "Syracuse", "Binghamton", "Albany"]
    NY_EDGES = [(0, 1), (0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 3)]
    NY_ROADS = ["NY-13", "NY-34", "NY-79", "I-81", "I-90", "I-88", "NY-7"]
    NY_NOTES = [
        "Ithaca -- Syracuse, round by Cortland",
        "Ithaca -- Syracuse again, round by Auburn",
        "Ithaca -- Binghamton",
        "Syracuse -- Binghamton",
        "Syracuse -- Albany, the Thruway",
        "Binghamton -- Albany",
        "Binghamton -- Albany again",
    ]
    # Question 1(b): US-11 runs beside I-81, so it joins the same two cities.
    US11_EDGE = (1, 2)

    # The four-node network from Part 3 of the sheet. On paper it is numbered
    # 1 to 4; here it is 0 to 3, which is the first thing to go wrong.
    SHEET_EDGES = [(0, 1), (1, 2), (1, 3), (2, 3)]

    # Pixel positions lifted from the sheet's TikZ, so the two maps look alike.
    _NY_POS = {0: (54, 151), 1: (150, 43), 2: (132, 193), 3: (348, 121)}
    _NY_LABEL_POS = {0: (36, 156), 1: (150, 26), 2: (132, 214), 3: (348, 104)}
    _NY_PATHS = [
        "M54,151 Q130,120 150,43",
        "M54,151 Q74,74 150,43",
        "M54,151 Q93,190 132,193",
        "M150,43 Q165,118 132,193",
        "M150,43 Q249,58 348,121",
        "M132,193 Q240,127 348,121",
        "M132,193 Q240,187 348,121",
    ]
    _NY_SHIELD_POS = [
        (116, 108),
        (88, 86),
        (93, 181),
        (152, 126),
        (249, 70),
        (240, 142),
        (240, 172),
    ]
    _US11_PATH = "M150,43 Q215,118 132,193"
    _US11_SHIELD = (196, 118)

    # A pen, not a plotter: fractal noise pushes every stroke off true by a
    # couple of pixels. Fixed seed, so the drawing keeps the same wobble instead
    # of vibrating as the slider moves. Text is drawn outside the filtered
    # group, because wobbly letters are simply hard to read.
    _PEN = (
        '<defs><filter id="lh-pen" x="-15%" y="-15%" width="130%" height="130%">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" '
        'seed="7" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" '
        'xChannelSelector="R" yChannelSelector="G"/></filter></defs>'
    )

    def _shield(x, y, text, hot=False):
        """A route marker, drawn outside the wobble so the number stays legible."""
        w = 8 + 6.2 * len(text)
        return (
            f'<rect x="{x - w / 2:.0f}" y="{y - 8}" width="{w:.0f}" height="16" '
            f'rx="3" fill="{RUST if hot else PAPER}" stroke="{INK}" '
            f'stroke-width="1.4" opacity="0.96"/>'
            f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="10" '
            f'font-family="{SANS}" font-weight="700" '
            f'fill="{PAPER if hot else INK}">{text}</text>'
        )

    def ny_svg(done=(), live=None, lit_nodes=(), us11=False):
        """The sheet's map. `done` are roads behind you, `live` is the one now."""
        out = [
            # The box reaches left of zero so that Ithaca's name, which hangs off
            # the westernmost city, is inside the drawing.
            '<svg viewBox="-30 0 430 232" width="100%" style="max-width:430px;'
            'display:block" xmlns="http://www.w3.org/2000/svg">',
            _PEN,
            '<g filter="url(#lh-pen)">',
            f'<path d="M-30,0 H150 Q90,30 -30,52 Z" fill="{BLUE}" opacity="0.10"/>',
        ]
        paths = list(_NY_PATHS) + ([_US11_PATH] if us11 else [])
        for k, d in enumerate(paths):
            if k == live:
                color, width, opacity = RUST, 5.5, 1
            elif k in done:
                color, width, opacity = BLUE, 3.5, 1
            else:
                color, width, opacity = INK, 2.5, 0.2
            out.append(
                f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
                f'opacity="{opacity}" stroke-linecap="round"/>'
            )
        for i, (x, y) in _NY_POS.items():
            out.append(
                f'<circle cx="{x}" cy="{y}" r="13" '
                f'fill="{RUST if i in lit_nodes else PAPER}" '
                f'stroke="{INK}" stroke-width="2.5"/>'
            )
        out.append("</g>")
        out.append(
            f'<text x="30" y="20" font-size="10" font-family="{SANS}" '
            f'fill="{INK}" opacity="0.45" transform="rotate(-13 30 20)">'
            "Lake Ontario</text>"
        )
        shields = list(zip(_NY_SHIELD_POS, NY_ROADS)) + (
            [(_US11_SHIELD, "US-11")] if us11 else []
        )
        for k, ((x, y), name) in enumerate(shields):
            out.append(_shield(x, y, name, hot=(k == live)))
        for i, (x, y) in _NY_POS.items():
            out.append(
                f'<text x="{x}" y="{y + 4}" text-anchor="middle" font-size="12" '
                f'font-family="{SANS}" font-weight="700" '
                f'fill="{PAPER if i in lit_nodes else INK}">{i}</text>'
            )
        for i, (x, y) in _NY_LABEL_POS.items():
            anchor = {0: "end"}.get(i, "middle")
            out.append(
                f'<text x="{x}" y="{y}" text-anchor="{anchor}" '
                f'font-size="11" font-family="{SANS}" font-weight="700" '
                f'fill="{INK}" opacity="0.75">{NY_NAMES[i]}</text>'
            )
        out.append("</svg>")
        return "".join(out)

    def ny_edgelist_html(upto, live=None):
        """The edge list filling up. Always seven lines tall, so it never jumps."""
        rows = []
        for k in range(len(NY_EDGES)):
            i, j = NY_EDGES[k]
            if k == live:
                style = f"color:{RUST};font-weight:700"
            elif k < upto:
                style = f"color:{BLUE}"
            else:
                style = "opacity:0.15"
            text = f"({i}, {j})," if (k < upto or k == live) else "&nbsp;"
            hint = f"  # {NY_ROADS[k]}, {NY_NOTES[k]}" if k == live else ""
            rows.append(
                f'<div style="{style};line-height:1.7;white-space:pre">    {text}{hint}</div>'
            )
        return (
            f'<div style="font-family:{MONO};font-size:13px;line-height:1.7;'
            f'color:{INK}">ROADS = [' + "".join(rows) + "]</div>"
        )

    def matrix_html(A, lit=(), lit_row=None, show_sums=False, names=None):
        """The adjacency matrix as a hand-ruled table."""
        n = len(A)
        lit = set(lit)
        hstyle = (
            f"padding:2px 6px;font-size:11px;font-family:{SANS};"
            "opacity:0.55;font-weight:700"
        )
        head = '<th style="width:24px"></th>' + "".join(
            f'<th style="{hstyle}">{j}</th>' for j in range(n)
        )
        if show_sums:
            head += f'<th style="{hstyle};padding-left:14px">degree</th>'
        rows = [f"<tr>{head}</tr>"]
        for i in range(n):
            hot = i == lit_row
            cells = [
                f'<th style="{hstyle};text-align:right;'
                f'opacity:{0.9 if hot else 0.55}">{i}</th>'
            ]
            for j in range(n):
                if (i, j) in lit:
                    bg, fg = RUST, PAPER
                elif hot:
                    bg, fg = "rgba(57,89,166,0.14)", INK
                else:
                    bg, fg = "transparent", INK
                cells.append(
                    f'<td style="padding:6px 10px;text-align:center;background:{bg};'
                    f"color:{fg};font-family:{MONO};font-size:14px;"
                    f'border:1.5px solid {RULE};border-radius:{WOBBLE}">{int(A[i][j])}</td>'
                )
            if show_sums:
                cells.append(
                    f'<td style="padding:6px 10px 6px 16px;text-align:center;'
                    f"font-weight:700;font-family:{MONO};font-size:14px;"
                    f'color:{RUST if hot else INK};opacity:{1 if hot else 0.45}">'
                    f"{int(sum(A[i]))}</td>"
                )
            rows.append("<tr>" + "".join(cells) + "</tr>")
        html = (
            '<table style="border-collapse:separate;border-spacing:2px;margin:0">'
            + "".join(rows)
            + "</table>"
        )
        if names is not None and lit_row is not None:
            html += (
                f'<div style="margin-top:10px;font-size:14px;font-family:{SANS};'
                f'color:{INK}"><b>{names[lit_row]}</b> &rarr; degree '
                f'<b style="color:{RUST}">{int(sum(A[lit_row]))}</b></div>'
            )
        return html

    def two_col(left, right, left_basis=320):
        return mo.Html(
            '<div style="display:flex;gap:26px;align-items:center;'
            'justify-content:flex-start;flex-wrap:wrap">'
            f'<div style="flex:0 0 {left_basis}px;max-width:100%">{left}</div>'
            f'<div style="flex:0 1 auto">{right}</div></div>'
        )

    def step_slider(stop, label):
        """Short on purpose: full width for seven steps reads as a progress bar
        rather than as something to drag."""
        return mo.ui.slider(0, stop, value=0, label=label, show_value=True)

    def plain_adjacency(edges, n):
        """The kit's own, so the animations run before your code exists."""
        A = np.zeros((n, n), dtype=int)
        for i, j in edges:
            A[i, j] += 1
            A[j, i] += 1
        return A

    def draw(edges, n, title=""):
        """Draw any edge list, in pen. Nodes carry their NUMBER, never their
        name: a long label either runs off the figure or lands on a road. The
        key beside the drawing says which number is which."""
        n = max(n, 1 + max(max(e) for e in edges))
        g = igraph.Graph(n=n, edges=[tuple(e) for e in edges], directed=False)
        g.vs["label"] = [str(i) for i in range(n)]
        igraph.autocurve(g, attribute="curved")
        with plt.rc_context({"path.sketch": (1.6, 70, 2)}):
            fig, ax = plt.subplots(figsize=(5.2, 4.2))
            fig.patch.set_facecolor(PAPER)
            igraph.plot(
                g,
                target=ax,
                layout=g.layout("kk"),
                vertex_size=42,
                vertex_color=PAPER,
                vertex_frame_color=INK,
                vertex_frame_width=2.2,
                vertex_label_size=12,
                vertex_label_color=INK,
                edge_width=2.2,
                edge_color=INK,
                edge_curved=g.es["curved"],
                margin=34,
            )
            ax.set_title(title, color=INK, fontsize=12)
            ax.set_axis_off()
        plt.close(fig)
        return fig

    def key_html(names, deg=None):
        """Which number is which city, and optionally its degree."""
        rows = []
        for i, nm in enumerate(names):
            tail = (
                f'<span style="color:{RUST};font-family:{MONO}">'
                f"&nbsp;&nbsp;{int(deg[i])}</span>"
                if deg is not None
                else ""
            )
            rows.append(
                f'<div style="margin:5px 0;line-height:1.4">'
                f'<b style="font-family:{MONO};color:{BLUE}">{i}</b>&nbsp; {nm}{tail}</div>'
            )
        head = (
            f'<div style="font-size:11px;opacity:0.55;font-weight:700;'
            f'letter-spacing:0.02em">CITY{"  ·  DEGREE" if deg is not None else ""}</div>'
        )
        return mo.Html(
            f'<div style="font-family:{SANS};font-size:14px;color:{INK}">'
            f"{head}{''.join(rows)}</div>"
        )

    def is_connected(A):
        """True if every city can be reached from every other one."""
        g = igraph.Graph.Adjacency(np.asarray(A).tolist(), mode="undirected")
        return g.is_connected()

    def note(text, tone=BLUE):
        return mo.Html(
            f'<div style="border-left:3px solid {tone};padding:2px 0 2px 14px;'
            f'margin:14px 0;font-family:{SANS};font-size:16px;color:{INK}">{text}</div>'
        )

    WAITING = mo.Html(
        f'<div style="font-family:{SANS};font-size:15px;color:#6A6D75;'
        f'border:1.5px dashed {RULE};border-radius:{WOBBLE};padding:10px 14px;'
        'display:inline-block">Waiting on the cell above.</div>'
    )

    def roads_ready(roads):
        """True once ROADS is the map on the sheet, in any order."""
        try:
            return sorted(tuple(sorted(e)) for e in roads) == sorted(
                tuple(sorted(e)) for e in NY_EDGES
            )
        except Exception:
            return False

    def adjacency_ready(fn):
        try:
            return np.array_equal(
                fn([(0, 1), (0, 1), (1, 2)], 3),
                np.array([[0, 2, 0], [2, 0, 1], [0, 1, 0]]),
            )
        except Exception:
            return False

    def degrees_ready(fn):
        try:
            return list(np.asarray(fn(plain_adjacency(NY_EDGES, 4))).ravel()) == [
                3,
                4,
                4,
                3,
            ]
        except Exception:
            return False

    def euler_ready(fn):
        try:
            return fn(plain_adjacency([(0, 1), (1, 2), (2, 0)], 3)) == "circuit"
        except Exception:
            return False


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    # Part 4 · Hand the map to the machine

    **On your own**, with the sheet next to the laptop.

    Every number this notebook asks for is one you have already written in
    pencil. When the screen and the sheet disagree, one of them is wrong, and
    finding out which is the exercise.

    Cells marked ✍️ are yours. Everything else runs itself.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 1 · Write the map down

    A map becomes a **list of pairs** — one line per road. The four cities are
    numbered `0`–`3`. Drag the slider and watch the list fill up:
    """)
    return


@app.cell(hide_code=True)
def _():
    anim1 = step_slider(6, "road")
    anim1
    return (anim1,)


@app.cell(hide_code=True)
def _(anim1):
    two_col(
        ny_svg(done=set(range(anim1.value)), live=anim1.value),
        ny_edgelist_html(upto=anim1.value, live=anim1.value),
        left_basis=400,
    )
    return


@app.cell(hide_code=True)
def _():
    note(
        "NY-34 writes <code>(0, 1)</code> a <b>second time</b>. Not a typo — "
        "two different roads run from Ithaca to Syracuse, and the sheet made you "
        "drive both.",
        RUST,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ The seven roads

    Two are written for you. Add the other five, one line per road. The order
    does not matter; the pairs do.
    """)
    return


@app.cell
def _():
    ROADS = [
        (0, 1),  # NY-13, Ithaca -- Syracuse
        (0, 1),  # NY-34, Ithaca -- Syracuse again
        ...,  # TASK
        ...,  # TASK
        ...,  # TASK
        ...,  # TASK
        ...,  # TASK
    ]
    return (ROADS,)


@app.cell(hide_code=True)
def _(ROADS):
    _clean = [e for e in ROADS if isinstance(e, (tuple, list)) and len(e) == 2]
    if roads_ready(_clean):
        _msg = f'<b style="color:{BLUE}">That is the map.</b>'
    elif len(_clean) != 7:
        _msg = (
            f'<b style="color:{RUST}">You have {len(_clean)} roads; the map has '
            "seven.</b>"
        )
    else:
        _deg = plain_adjacency(_clean, 4).sum(axis=1)
        _want = [3, 4, 4, 3]
        _bad = [
            f"{NY_NAMES[i]} touches {int(_deg[i])} of your roads, not {_want[i]}"
            for i in range(4)
            if int(_deg[i]) != _want[i]
        ]
        _msg = f'<b style="color:{RUST}">Not yet.</b>' + (
            '<div style="font-size:14px;opacity:0.75;margin-top:6px">'
            + "; ".join(_bad)
            + " — the counts are Question 3 on the sheet.</div>"
            if _bad
            else '<div style="font-size:14px;opacity:0.75;margin-top:6px">The '
            "degrees are right but the roads are not: two cities are joined by "
            "the wrong number of them.</div>"
        )
    mo.Html(f'<div style="font-family:{SANS};font-size:16px;color:{INK}">{_msg}</div>')
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 2 · Look at it

    The same seven roads, drawn by the machine. It puts the cities wherever it
    likes — **the layout is not geography**, and that is the point: Ithaca is
    still the city with three roads whether you draw it west or upside down.
    """)
    return


@app.cell(hide_code=True)
def _(ROADS):
    if not roads_ready([e for e in ROADS if isinstance(e, (tuple, list))]):
        _out = WAITING
    else:
        _out = mo.hstack(
            [draw(ROADS, 4, "Upstate New York"), key_html(NY_NAMES)],
            widths=[3, 2],
            align="center",
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 3 · Matrix, then degree

    A grid where row `i`, column `j` holds **how many roads join i and j**. It
    is the grid you filled in for Question 6(a), on a bigger map.
    """)
    return


@app.cell(hide_code=True)
def _():
    anim2 = step_slider(6, "road")
    anim2
    return (anim2,)


@app.cell(hide_code=True)
def _(anim2):
    _i, _j = NY_EDGES[anim2.value]
    two_col(
        ny_edgelist_html(upto=anim2.value, live=anim2.value),
        matrix_html(
            plain_adjacency(NY_EDGES[: anim2.value + 1], 4), lit={(_i, _j), (_j, _i)}
        ),
        left_basis=250,
    )
    return


@app.cell(hide_code=True)
def _():
    note(
        "A pair is a <b>coordinate</b>. <code>(0, 1)</code> is row 0, column 1."
        "<br>It lights <b>two</b> cells — the grid is a mirror."
        "<br>The second Ithaca--Syracuse road made it <b>2, not 1</b> — add, do "
        "not set.",
        RUST,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ Fill in the two lines
    """)
    return


@app.function
def to_adjacency(edges, n):
    """A[i, j] = how many roads join city i and city j."""
    A = np.zeros((n, n), dtype=int)
    for i, j in edges:
        ...  # TASK
        ...  # TASK
    return A


@app.cell(hide_code=True)
def _():
    _A = to_adjacency(NY_EDGES, 4)
    _ok = isinstance(_A, np.ndarray) and np.array_equal(
        _A, plain_adjacency(NY_EDGES, 4)
    )
    two_col(
        matrix_html(_A if isinstance(_A, np.ndarray) else np.zeros((4, 4), int)),
        f'<div style="font-family:{SANS};font-size:16px;color:{INK}">'
        + (
            f'<b style="color:{BLUE}">The map, as a grid.</b>'
            if _ok
            else f'<b style="color:{RUST}">Not yet.</b>'
            '<div style="font-size:14px;opacity:0.75;margin-top:6px">A '
            "<code>1</code> where the animation showed <code>2</code> means you "
            "are setting, not adding. A grid that is not a mirror means you "
            "filled one cell of the two.</div>"
        )
        + "</div>",
        left_basis=200,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    **Degree** — how many roads touch a city — is now a row, added up. That is
    Question 6(b), and it is also the count you made in Question 3.
    """)
    return


@app.cell(hide_code=True)
def _():
    anim3 = step_slider(3, "city")
    anim3
    return (anim3,)


@app.cell(hide_code=True)
def _(anim3):
    two_col(
        ny_svg(
            done={k for k, e in enumerate(NY_EDGES) if anim3.value in e},
            lit_nodes={anim3.value},
        ),
        matrix_html(
            plain_adjacency(NY_EDGES, 4),
            lit_row=anim3.value,
            show_sums=True,
            names=NY_NAMES,
        ),
        left_basis=400,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ Degree
    """)
    return


@app.function
def degrees(A):
    """How many roads touch each city.

    TASK: one line, no loop. Every road at city i left a count somewhere in
    row i.
    """
    ...


@app.cell(hide_code=True)
def _(ROADS):
    if not (
        roads_ready([e for e in ROADS if isinstance(e, (tuple, list))])
        and adjacency_ready(to_adjacency)
        and degrees_ready(degrees)
    ):
        _out = WAITING
    else:
        _deg = degrees(to_adjacency(ROADS, 4))
        _out = mo.md(
            f"""
    {pd.DataFrame({"city": NY_NAMES, "degree": _deg}).to_markdown(index=False)}

    Degrees add up to **{int(np.sum(_deg))}**, and seven roads must give 14.
    **{int(np.sum(np.asarray(_deg) % 2 == 1))}** cities are odd — the ones you
    marked as having a left-over road.
    """
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 4 · Two-step routes

    Question 6 used a smaller network — four nodes, four lines. On paper you
    numbered them **1 to 4**. Python counts from **0**, so paper node 1 is row
    `0` here, paper node 3 is row `2`, and everything is shifted by one. This is
    the single most common way to get a right answer and read it wrong.
    """)
    return


@app.cell(hide_code=True)
def _():
    if not adjacency_ready(to_adjacency):
        _out = WAITING
    else:
        _A = to_adjacency(SHEET_EDGES, 4)
        _out = mo.hstack(
            [
                mo.vstack(
                    [
                        mo.md("**$A$** — your Question 6(a) grid"),
                        mo.Html(matrix_html(_A)),
                    ]
                ),
                mo.vstack(
                    [
                        mo.md("**$A^2$** — your Question 6(d) prediction"),
                        mo.Html(matrix_html(_A @ _A)),
                    ]
                ),
            ],
            widths=[1, 1],
            align="start",
            gap=2,
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    note(
        "Row 0, column 2 of $A^2$ is the number of 2-step routes from paper node "
        "<b>1</b> to paper node <b>3</b>. Row 0, column 1 says why you could not "
        "find any from 1 to 2. The diagonal is the degrees again — a 2-step "
        "route that comes back is one road out and the same road home.",
        BLUE,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    # 5 · The rule

    A drive passing *through* a city uses roads in pairs, so an **odd** city has
    one left over — you must **start** or **end** there. A drive has one start
    and one end.

    | odd cities | you get | return |
    |---|---|---|
    | 0 | drive every road once, finish where you began | `"circuit"` |
    | 2 | drive every road once, finish elsewhere | `"path"` |
    | anything else | nothing | `"impossible"` |

    A map in two pieces is **always** impossible, whatever the degrees say.
    `is_connected(A)` is written for you — check it first.
    """)
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ### ✍️ Euler's rule
    """)
    return


@app.function
def euler_status(A):
    """Return "circuit", "path", or "impossible" for the map A.

    TASK: the rule is the table above. The two things you have are
    `degrees(A)` and `is_connected(A)`.
    """
    ...


@app.cell(hide_code=True)
def _():
    _cases = [
        (NY_EDGES, 4, "path"),
        ([(0, 1), (1, 2), (2, 0)], 3, "circuit"),
        ([(0, 1), (2, 3)], 4, "impossible"),  # two pieces: degrees alone lie
    ]
    _ok = all(euler_status(plain_adjacency(_e, _n)) == _w for _e, _n, _w in _cases)
    note(
        "Correct, on Upstate New York and on a map in two pieces."
        if _ok
        else "Not yet. The seven roads should say path, a triangle circuit — and "
        "two roads in different worlds impossible, however even the degrees are.",
        BLUE if _ok else RUST,
    )
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ## The verdict, twice

    Question 1(a) was the seven roads. Question 1(b) added **US-11** beside
    I-81. Your rule now answers both, and it never looked at a picture.
    """)
    return


@app.cell(hide_code=True)
def _(ROADS):
    if not (
        roads_ready([e for e in ROADS if isinstance(e, (tuple, list))])
        and adjacency_ready(to_adjacency)
        and degrees_ready(degrees)
        and euler_ready(euler_status)
    ):
        _out = WAITING
    else:
        _story = {
            "circuit": "Drive every road once and come home.",
            "path": "Drive every road once, but you cannot come home — start at "
            "one odd city and finish at the other.",
            "impossible": "A drive has one start and one end, and that is not "
            "enough left-over roads to go round.",
        }
        _cards = []
        for _title, _edges in [
            ("1(a) · seven roads", list(ROADS)),
            ("1(b) · with US-11", list(ROADS) + [US11_EDGE]),
        ]:
            _A = to_adjacency(_edges, 4)
            _deg = np.asarray(degrees(_A))
            _odd = int(np.sum(_deg % 2 == 1))
            _status = euler_status(_A)
            _cards.append(
                mo.Html(
                    f'<div style="font-family:{SANS};padding-right:26px">'
                    f'<div style="font-size:12px;opacity:0.55;font-weight:700">'
                    f"{_title.upper()}</div>"
                    f'<div style="font-size:32px;font-weight:700;color:{RUST};'
                    f'margin:4px 0">{_status}</div>'
                    f'<div style="font-size:16px;color:{INK}">{_odd} odd cities. '
                    f'{_story.get(_status, "That is not one of the three strings.")}'
                    "</div></div>"
                )
            )
        _out = mo.hstack(_cards, widths=[1, 1], align="start")
    _out
    return


@app.cell(hide_code=True)
def _(ROADS):
    if not roads_ready([e for e in ROADS if isinstance(e, (tuple, list))]):
        _out = WAITING
    else:
        _out = two_col(
            ny_svg(done=set(range(7)), us11=False),
            ny_svg(done=set(range(8)), us11=True),
            left_basis=330,
        )
    _out
    return


@app.cell(hide_code=True)
def _():
    mo.md(r"""
    ---

    ## Finished early?

    Your rule never looked at a picture, so it runs on any network. The karate
    club will say `impossible` — every real network does. The question is **how
    far**: `k/2` new edges for `k` odd nodes.
    """)
    return


@app.cell
def _():
    if adjacency_ready(to_adjacency) and euler_ready(euler_status):
        _g = igraph.Graph.Famous("Zachary")
        _A = np.array(_g.get_adjacency().data)
        _odd = int(np.sum(np.asarray(degrees(_A)) % 2 == 1))
        print(f"karate club: {_g.vcount()} nodes, {_g.ecount()} edges")
        print(f"  {euler_status(_A)}, {_odd} odd nodes, {_odd // 2} edges to add")
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
