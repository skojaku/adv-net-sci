# /// script
# dependencies = [
#     "marimo",
#     "numpy==2.3.2",
# ]
# [tool.marimo.display]
# default_width = "medium"
# [tool.marimo.formatting]
# line_length = 120
# ///
#
# TEMPLATE. Do not edit the built notebook — edit this file and run
#
#     python tools/build_m01_lab.py
#
# which fills in the two %%MARKERS%% below with base64 of
#   - adv-net-sci-ops/pair-notebook/m01-euler-tour/lecture-hall.css  (the look)
#   - lecture-note/assets/anim.{css,js} + assets/anim/route-namer.js
#     + the #route-namer rules out of slides/m01/network-science.css
#     welded into one self-contained page  (the walk/trail/path visual)
# and writes notebooks/m01-euler-tour/pen-and-paper-lab.py.
#
# The assets are inlined rather than fetched because this notebook is uploaded
# to molab as a single file and has to work in a room with bad wifi.

import base64

import marimo

__generated_with = "0.14.13"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import base64

    import marimo as mo
    import numpy as np

    return base64, mo, np


@app.cell(hide_code=True)
def _(base64, mo):
    _css = base64.b64decode("%%LECTURE_HALL_CSS_B64%%").decode("utf-8")
    mo.Html(f"<style>{_css}</style>")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    # Module 1 Lab — hand the network to the machine

    Keep your pen-and-paper sheet next to the laptop. Every section below asks
    you for a number you have already written on it.

    /// admonition | How to work in pairs
    One laptop between two people. The person who is **not** typing reads the
    question out loud and says the answer they expect **before** the other one
    runs the cell. Swap after every section.
    ///
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## A — Walk, trail, path

    On the paper you gave three routes their names. Here is the same graph,
    live: **click a place, then click a neighbour**. The name of your route
    updates on every click.
    """
    )
    return


@app.cell(hide_code=True)
def _(base64, mo):
    _viz = base64.b64decode("%%ANIM_HTML_B64%%").decode("utf-8")
    mo.iframe(_viz, height=560)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    /// admonition | Do this before moving on
    1. Build a route that is a **trail but not a path**. What did you have to
       do? Say it out loud to your partner.
    2. Build a route that is a **walk but not a trail**.
    3. Try to build a route that is a **path but not a trail**. What happens,
       and why?
    ///

    Now type one of your routes below and let the machine name it. Use the
    place names, separated by spaces — for example `Dorm Cafe Gym Cafe Lib`.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    route_box = mo.ui.text(
        value="Lib Gym Dorm Cafe Gym",
        label="your route",
        full_width=True,
    )
    route_box
    return (route_box,)


@app.cell(hide_code=True)
def _(mo, route_box):
    _names = ["Dorm", "Cafe", "Lib", "Gym"]
    _edges = {(0, 1), (1, 2), (2, 3), (3, 0), (1, 3)}

    def _edge(i, j):
        return (min(i, j), max(i, j)) in _edges

    def _name_route(words):
        try:
            seq = [_names.index(w) for w in words]
        except ValueError as exc:
            return f"**I do not know that place.** Use {', '.join(_names)}. ({exc})"
        if len(seq) < 2:
            return "**Give me at least two places.**"
        used = []
        for a, b in zip(seq, seq[1:]):
            if not _edge(a, b):
                return f"**{_names[a]} and {_names[b]} are not joined.** That is not a route at all."
            used.append((min(a, b), max(a, b)))
        edge_twice = len(used) != len(set(used))
        node_twice = len(seq) != len(set(seq))
        closed = seq[0] == seq[-1]
        if edge_twice:
            name, why = "walk", "an edge came round twice, so no stricter name is left"
        elif node_twice:
            name, why = "trail", "no edge twice, but a place came round again"
        else:
            name, why = "path", "nothing repeats at all"
        if closed and not edge_twice:
            name = "cycle" if not node_twice else "circuit"
            why += ", and it ends where it started"
        return f"### {name}\n\n{why}"

    mo.md(_name_route(route_box.value.split()))
    return


@app.cell(hide_code=True)
def _(draw_graph, mo):
    mo.md(
        rf"""
    ## B — The same network, written as numbers

    A computer cannot look at a picture. This is the four-node network from
    **Question 5** on your sheet.

    {mo.as_html(draw_graph([(-1.0, 0.0), (0.0, 0.0), (0.7, 0.55), (0.7, -0.55)],
                           [(0, 1), (1, 2), (1, 3), (2, 3)],
                           ["1", "2", "3", "4"]))}

    Type the four rows of the adjacency matrix you filled in on paper. Write
    each row as four digits, for example the first row is `0100`.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    rows = mo.ui.array(
        [mo.ui.text(value="0100", label="row 1"),
         mo.ui.text(value="", label="row 2"),
         mo.ui.text(value="", label="row 3"),
         mo.ui.text(value="", label="row 4")],
    )
    rows
    return (rows,)


@app.cell(hide_code=True)
def _(mo, np, rows):
    _truth = np.array([[0, 1, 0, 0], [1, 0, 1, 1], [0, 1, 0, 1], [0, 1, 1, 0]])

    def _read(rs):
        out = []
        for r in rs:
            digits = [c for c in r.value.strip() if c in "01"]
            if len(digits) != 4:
                return None
            out.append([int(c) for c in digits])
        return np.array(out)

    A = _read(rows.value if hasattr(rows, "value") else rows)
    if A is None:
        _msg = "Fill in all four rows, four digits each (only 0 and 1)."
    elif not np.array_equal(A, A.T):
        _msg = (
            "**Your matrix is not symmetric.** A line between 3 and 4 has to show up "
            "twice: once in row 3, once in row 4. Find the entry you wrote only once."
        )
    elif np.array_equal(A, _truth):
        _msg = "**That is the network.** Row totals: " + ", ".join(
            str(int(s)) for s in A.sum(axis=1)
        ) + " — compare with 6(b) on your sheet."
    else:
        _wrong = int((A != _truth).sum())
        _msg = f"**Not yet — {_wrong} entries differ.** Check the diagonal first: can a node be joined to itself here?"

    mo.md(_msg)
    return (A,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Now square it

    On paper you predicted three things about $A^2$: the entry in row 1
    column 3, the entry in row 1 column 2, and the diagonal. Read them off your
    sheet, say them out loud, **then** run the next cell.
    """
    )
    return


@app.cell(hide_code=True)
def _(A, matrix_html, mo, np):
    if A is None:
        mo.md("*(fill in the matrix above first)*")
    else:
        _A2 = A @ A
        mo.md(
            f"""
    {mo.as_html(matrix_html(A, "A"))}

    {mo.as_html(matrix_html(_A2, "A²"))}

    Diagonal of $A^2$: {", ".join(str(int(x)) for x in np.diag(_A2))} —
    and the row totals of $A$ were {", ".join(str(int(x)) for x in A.sum(axis=1))}.
    """
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### Where do those numbers come from?

    Move the slider. For each $k$ you get $A^k$, and underneath, **every route
    of exactly $k$ steps** from node 1 to the node you choose — found by brute
    force, not by matrix algebra. Check that the count matches the entry.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    k_slider = mo.ui.slider(1, 5, value=2, label="length k", show_value=True)
    target = mo.ui.dropdown(["1", "2", "3", "4"], value="3", label="to node")
    mo.hstack([k_slider, target], justify="start", gap=2)
    return k_slider, target


@app.cell(hide_code=True)
def _(A, k_slider, matrix_html, mo, np, target):
    if A is None:
        mo.md("*(fill in the matrix above first)*")
    else:
        _k = k_slider.value
        _j = int(target.value) - 1
        _Ak = np.linalg.matrix_power(A, _k)

        def _routes(start, end, steps):
            if steps == 0:
                return [[start]] if start == end else []
            out = []
            for nxt in range(4):
                if A[start, nxt]:
                    for tail in _routes(nxt, end, steps - 1):
                        out.append([start] + tail)
            return out

        _found = _routes(0, _j, _k)
        _listing = "\n".join(
            "- " + " → ".join(str(n + 1) for n in r) for r in _found
        ) or "- *(none)*"

        mo.md(
            f"""
    {mo.as_html(matrix_html(_Ak, f"A^{_k}"))}

    Entry in **row 1, column {_j + 1}** of $A^{{{_k}}}$ is
    **{int(_Ak[0, _j])}**.

    Every {_k}-step route from node 1 to node {_j + 1}:

    {_listing}

    That is **{len(_found)}** of them.
    """
        )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    /// admonition | Say it out loud before you scroll
    Set $k = 3$ and the target to node 2. Look at the routes it lists. **One of
    them uses the same line twice, and one visits a node twice.**

    So $(A^k)_{ij}$ counts routes that may repeat anything. Using the three
    names from Part A, that means $A^k$ counts **walks** — not trails, and not
    paths. Write that on your sheet.
    ///
    """
    )
    return


@app.cell(hide_code=True)
def _(draw_graph, mo):
    mo.md(
        rf"""
    ## C — Is the network in one piece?

    A new network, six nodes. You are given only the matrix.

    ```
        1  2  3  4  5  6
    1 [ 0  0  1  0  1  0 ]
    2 [ 0  0  0  1  0  0 ]
    3 [ 1  0  0  0  1  0 ]
    4 [ 0  1  0  0  0  1 ]
    5 [ 1  0  1  0  0  0 ]
    6 [ 0  0  0  1  0  0 ]
    ```

    Before you run anything: with your partner, decide whether you can walk
    from node 1 to node 2. Then run the cell.

    {mo.as_html(draw_graph(
        [(-1.0, 0.6), (0.2, 0.6), (1.0, 0.0), (-0.4, -0.6), (-1.2, -0.4), (0.8, -0.8)],
        [(0, 2), (0, 4), (2, 4), (1, 3), (3, 5)],
        ["1", "2", "3", "4", "5", "6"]))}
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    step = mo.ui.slider(0, 4, value=0, label="step", show_value=True)
    seed = mo.ui.dropdown(["1", "2", "3", "4", "5", "6"], value="1", label="start from node")
    mo.hstack([seed, step], justify="start", gap=2)
    return seed, step


@app.cell(hide_code=True)
def _(mo, np, seed, step):
    B = np.array(
        [[0, 0, 1, 0, 1, 0],
         [0, 0, 0, 1, 0, 0],
         [1, 0, 0, 0, 1, 0],
         [0, 1, 0, 0, 0, 1],
         [1, 0, 1, 0, 0, 0],
         [0, 0, 0, 1, 0, 0]]
    )

    def _grow(start, steps):
        seen = {start}
        history = [set(seen)]
        for _ in range(steps):
            nxt = set(seen)
            for i in sorted(seen):
                nxt |= {j for j in range(6) if B[i, j]}
            history.append(set(nxt))
            if nxt == seen:
                break
            seen = nxt
        return history

    _hist = _grow(int(seed.value) - 1, step.value)
    _now = _hist[min(step.value, len(_hist) - 1)]
    _settled = len(_hist) > 1 and _hist[-1] == _hist[-2]

    _lines = "\n".join(
        f"- step {i}: {{{', '.join(str(n + 1) for n in sorted(s))}}}"
        for i, s in enumerate(_hist)
    )

    mo.md(
        f"""
    {_lines}

    The set you can reach is **{{{', '.join(str(n + 1) for n in sorted(_now))}}}**
    — {len(_now)} of the 6 nodes.
    {"It has stopped growing." if _settled else "Push the slider one more step."}
    """
    )
    return (B,)


@app.cell(hide_code=True)
def _(B, mo, np):
    def _components(M):
        n = M.shape[0]
        left, out = set(range(n)), []
        while left:
            seed_node = min(left)
            seen, frontier = {seed_node}, [seed_node]
            while frontier:
                i = frontier.pop()
                for j in range(n):
                    if M[i, j] and j not in seen:
                        seen.add(j)
                        frontier.append(j)
            out.append(sorted(seen))
            left -= seen
        return out

    _comps = _components(B)
    _shown = " and ".join(
        "{" + ", ".join(str(n + 1) for n in c) + "}" for c in _comps
    )

    mo.md(
        f"""
    A set that stops growing like that is a **connected component**. This
    network has **{len(_comps)}**: {_shown}.

    /// admonition | Back to the bridges
    Only nodes 2 and 6 have a left-over line — two of them, not three or
    four. Your rule from Question 3 says a route crossing every line exactly
    once should exist, and it does not.

    Write the missing condition on your sheet, using the word *component*.
    ///

    Row totals, for the record: {", ".join(str(int(x)) for x in np.asarray(B).sum(axis=1))}.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ## D — Storing a big network

    The four-node matrix in section B used **16** boxes to store **4** lines.
    Twelve boxes held a zero.

    For a network of 8 billion people the matrix needs $64 \times 10^{18}$
    boxes. Almost all of them would be zero. So we throw the zeros away and
    keep two lists.

    - `indices` — every node's neighbours, glued together in node order.
    - `indptr` — the position in `indices` where each node's block begins,
      with the length of `indices` as a final entry.

    For the four-node network, node 1's neighbours are `[2]`, so `indices`
    starts `2, ...` and `indptr` starts `0, 1, ...`.

    Fill in the rest. Write the numbers separated by spaces.
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    indices_box = mo.ui.text(value="2 1 3 4", label="indices", full_width=True)
    indptr_box = mo.ui.text(value="0 1", label="indptr", full_width=True)
    mo.vstack([indices_box, indptr_box])
    return indices_box, indptr_box


@app.cell(hide_code=True)
def _(indices_box, indptr_box, mo):
    _want_indices = [2, 1, 3, 4, 2, 4, 2, 3]
    _want_indptr = [0, 1, 4, 6, 8]

    def _nums(s):
        try:
            return [int(x) for x in s.replace(",", " ").split()]
        except ValueError:
            return None

    _i = _nums(indices_box.value)
    _p = _nums(indptr_box.value)
    _out = []

    if _i is None or _p is None:
        _out.append("Whole numbers separated by spaces, please.")
    else:
        if _i == _want_indices:
            _out.append("`indices` — **correct**.")
        elif len(_i) != 8:
            _out.append(
                f"`indices` should have {2 * 4} entries: every line shows up twice, "
                f"once from each end. You have {len(_i)}."
            )
        else:
            _out.append("`indices` — not yet. Take the nodes strictly in order 1, 2, 3, 4.")

        if _p == _want_indptr:
            _out.append("`indptr` — **correct**.")
        elif len(_p) != 5:
            _out.append(
                f"`indptr` needs {4 + 1} entries: one per node, plus the length of "
                f"`indices` at the end. You have {len(_p)}."
            )
        else:
            _out.append(
                "`indptr` — not yet. Each entry is the previous entry plus the number "
                "of neighbours of the previous node."
            )

        if _i == _want_indices and _p == _want_indptr:
            _out.append(
                "\n---\n\n**Now cover the picture with your hand and use only the two "
                "lists.** The degree of node 3 is `indptr[3] - indptr[2]` = "
                f"{_want_indptr[3] - _want_indptr[2]}. Node 4's neighbours are "
                f"`indices[{_want_indptr[3]}:{_want_indptr[4]}]` = "
                f"{_want_indices[_want_indptr[3]:_want_indptr[4]]}. "
                "Write both rules on your sheet in words."
            )

    mo.md("\n\n".join(_out))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(
        r"""
    ### What it is bad at

    Add one line, between node 1 and node 4. The lists become

    ```
    indices = [2, 4,  1, 3, 4,  2, 4,  1, 2, 3]
    indptr  = [0, 2, 5, 7, 10]
    ```

    /// admonition | Last question of the lab
    Compare with what you wrote. **How many of the ten numbers in `indices`
    sit in a different place than before?** And how many entries of `indptr`
    changed?

    Then answer, in one sentence each: what is this way of storing a network
    good at, and what is it bad at? That sentence is the last line on your
    paper sheet.
    ///
    """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    def matrix_html(M, name):
        n_rows, n_cols = M.shape
        head = "".join(f"<th>{j + 1}</th>" for j in range(n_cols))
        body = "".join(
            "<tr><th>" + str(i + 1) + "</th>"
            + "".join(f"<td>{int(M[i, j])}</td>" for j in range(n_cols))
            + "</tr>"
            for i in range(n_rows)
        )
        return mo.Html(
            "<div class='lab-mat'><div class='lab-mat-name'>" + name + "</div>"
            "<table><thead><tr><th></th>" + head + "</tr></thead>"
            "<tbody>" + body + "</tbody></table></div>"
            "<style>"
            ".lab-mat{display:inline-block;margin:0.4rem 1.2rem 0.4rem 0;vertical-align:top}"
            ".lab-mat-name{font-weight:700;margin-bottom:0.2rem}"
            ".lab-mat table{border-collapse:collapse}"
            ".lab-mat th,.lab-mat td{border:1px solid #D9D2C2;padding:0.25rem 0.55rem;"
            "text-align:center;font-variant-numeric:tabular-nums}"
            ".lab-mat thead th{border:none;color:#6A6D75;font-weight:600}"
            ".lab-mat tbody th{border:none;color:#6A6D75;font-weight:600}"
            "</style>"
        )

    return (matrix_html,)


@app.cell(hide_code=True)
def _(mo):
    def draw_graph(pos, edges, labels, w=380, h=210):
        xs = [p[0] for p in pos]
        ys = [p[1] for p in pos]
        pad, r = 30, 16
        sx = (w - 2 * pad) / max(1e-9, (max(xs) - min(xs)))
        sy = (h - 2 * pad) / max(1e-9, (max(ys) - min(ys)))
        def X(x):
            return pad + (x - min(xs)) * sx
        def Y(y):
            return h - pad - (y - min(ys)) * sy

        lines = "".join(
            f"<line x1='{X(pos[a][0]):.1f}' y1='{Y(pos[a][1]):.1f}' "
            f"x2='{X(pos[b][0]):.1f}' y2='{Y(pos[b][1]):.1f}' "
            "stroke='#1D1E21' stroke-width='2.2'/>"
            for a, b in edges
        )
        discs = "".join(
            f"<circle cx='{X(p[0]):.1f}' cy='{Y(p[1]):.1f}' r='{r}' fill='#FFFFFF' "
            "stroke='#1D1E21' stroke-width='2.2'/>"
            f"<text x='{X(p[0]):.1f}' y='{Y(p[1]) + 5:.1f}' text-anchor='middle' "
            f"font-size='15' fill='#1D1E21'>{lab}</text>"
            for p, lab in zip(pos, labels)
        )
        return mo.Html(
            f"<svg viewBox='0 0 {w} {h}' width='100%' style='max-width:{w}px' "
            f"role='img'>{lines}{discs}</svg>"
        )

    return (draw_graph,)


if __name__ == "__main__":
    app.run()
