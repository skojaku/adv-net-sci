# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "marimo",
#     "igraph",
#     "networkx",
#     "matplotlib",
#     "seaborn",
#     "altair",
#     "anywidget",
#     "numpy",
#     "pandas",
#     "pillow",
# ]
# ///

# REFERENCE NOTEBOOK (golden sample) — what a finished m02 session looks like.
# Assembled from the module's templates (cells/*.py), the lesson note
# skeletons (lesson/ch*.yaml), and a FICTIONAL student's answers, so the
# finished shape can be reviewed (TUTOR_REVIEW_RUBRIC.md Part S) without
# running a live session. Real notebooks grow one cell at a time in
# conversation; this file only shows the destination.

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium", css_file="lecture-hall.css")


@app.cell(hide_code=True)
def _(mo):
    # One single string literal on purpose: marimo round-trips mo.md cells
    # through its markdown serializer, and implicit string concatenation
    # corrupts them (the code itself gets wrapped as markdown content).
    mo.md(
        r"""<p style="text-align:right; color:#6A6D75; font-size:12px; margin:0;">🐛 Something broken or odd? Email Prof. Sadamori Kojaku &middot; <a href="mailto:skojaku@binghamton.edu" style="color:#35577F;">skojaku@binghamton.edu</a></p>"""
    )
    return


@app.cell(hide_code=True)
def reference_banner(mo):
    mo.md(
        r"""<p style="border:1px solid #C98A2D; border-radius:6px; padding:8px 12px; color:#6A6D75; font-size:13px;">📎 <strong>Reference notebook.</strong> A golden sample assembled from the module's templates and note skeletons, with a <em>fictional</em> student's answers ("Kim", comfortable with Python). It shows the finished shape a real session grows toward — it is not a graded record.</p>"""
    )
    return


@app.cell(hide_code=True)
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _():
    import matplotlib.pyplot as plt
    import networkx as nx
    import numpy as np
    import seaborn as sns

    # Match figures to the lecture-hall notebook theme (lecture-hall.css).
    # seaborn first (set_theme resets rc), then our palette on top.
    sns.set_theme(style="ticks")
    plt.rcParams.update(
        {
            "figure.facecolor": "#FFFFFF",
            "axes.facecolor": "#FFFFFF",
            "savefig.facecolor": "#FFFFFF",
            "text.color": "#35373C",
            "axes.edgecolor": "#6A6D75",
            "axes.labelcolor": "#35373C",
            "axes.titlecolor": "#1D1E21",
            "xtick.color": "#6A6D75",
            "ytick.color": "#6A6D75",
            "font.family": "sans-serif",
            "font.sans-serif": ["IBM Plex Sans", "DejaVu Sans"],
            "axes.prop_cycle": plt.cycler(
                color=["#1F3A5F", "#B4552D", "#35577F", "#C98A2D", "#6A6D75"]
            ),
        }
    )
    sns.set_palette(["#1F3A5F", "#B4552D", "#35577F", "#C98A2D", "#6A6D75"])
    return nx, np, plt, sns


@app.cell(hide_code=True)
def _():
    import altair as alt
    import igraph as ig
    import pandas as pd

    return alt, ig, pd


@app.cell(hide_code=True)
def _():
    import anywidget as _anywidget
    import traitlets as _traitlets

    class _NetViz(_anywidget.AnyWidget):
        _esm = r"""
import * as d3 from "https://esm.sh/d3@7";

function render({ model, el }) {
  const W = model.get("width"), H = model.get("height");
  el.innerHTML = "";
  const svg = d3.select(el).append("svg")
    .attr("viewBox", `0 0 ${W} ${H}`)
    .style("max-width", "100%").style("height", "auto");

  const nodes = model.get("nodes").map(d => ({...d}));
  const links = model.get("links").map(d => ({...d}));
  const byId = new Map(nodes.map(d => [d.id, d]));
  links.forEach(l => { l.source = byId.get(l.source); l.target = byId.get(l.target); });
  const straight = links.filter(l => l.source !== l.target);
  const loops = links.filter(l => l.source === l.target);

  const link = svg.append("g").selectAll("line").data(straight).join("line")
    .attr("stroke", d => d.color || "#6A6D75")
    .attr("stroke-width", d => d.width || 2)
    .attr("stroke-linecap", "round");
  const loop = svg.append("g").selectAll("path").data(loops).join("path")
    .attr("fill", "none")
    .attr("stroke", d => d.color || "#6A6D75")
    .attr("stroke-width", d => d.width || 2);

  const node = svg.append("g").selectAll("g").data(nodes).join("g")
    .style("cursor", "grab");
  node.append("circle")
    .attr("r", d => d.r || 16)
    .attr("fill", d => d.color || "#35577F")
    .attr("stroke", "#1D1E21").attr("stroke-width", 1);
  node.append("text")
    .text(d => d.label ?? d.id)
    .attr("text-anchor", "middle").attr("dy", "0.35em")
    .attr("fill", "#FFFFFF")
    .style("font", "600 12px 'IBM Plex Sans', sans-serif")
    .style("pointer-events", "none");

  function place() {
    link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
    loop.attr("d", d => {
      const x = d.source.x, y = d.source.y, r = d.source.r || 16;
      return `M ${x - 6} ${y - r + 4} C ${x - 30} ${y - r - 34}, ${x + 30} ${y - r - 34}, ${x + 6} ${y - r + 4}`;
    });
    node.attr("transform", d => `translate(${d.x},${d.y})`);
  }

  const hasPos = nodes.every(d => d.x != null && d.y != null);
  if (hasPos && !model.get("physics")) {
    place();
    node.call(d3.drag().on("drag", (ev, d) => { d.x = ev.x; d.y = ev.y; place(); }));
  } else {
    const sim = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).distance(70).strength(0.8))
      .force("charge", d3.forceManyBody().strength(-220))
      .force("center", d3.forceCenter(W / 2, H / 2))
      .force("collide", d3.forceCollide(24))
      .on("tick", place);
    node.call(d3.drag()
      .on("start", (ev, d) => { if (!ev.active) sim.alphaTarget(0.25).restart(); d.fx = d.x; d.fy = d.y; })
      .on("drag", (ev, d) => { d.fx = ev.x; d.fy = ev.y; })
      .on("end", (ev, d) => { if (!ev.active) sim.alphaTarget(0); d.fx = d.fy = null; }));
  }
}
export default { render };
"""
        nodes = _traitlets.List([]).tag(sync=True)
        links = _traitlets.List([]).tag(sync=True)
        width = _traitlets.Int(560).tag(sync=True)
        height = _traitlets.Int(420).tag(sync=True)
        physics = _traitlets.Bool(False).tag(sync=True)

    def netviz(
        edges,
        highlight=(),
        node_colors=None,
        nodes=None,
        layout="circle",
        physics=False,
        width=560,
        height=420,
    ):
        """Draw a small network as a themed, drag-able D3 widget.

        edges: [(u, v), ...] — node names appear in first-seen order;
               (u, u) draws a self-loop arc above the node.
        highlight: edges to paint rust-red (e.g. shortcuts).
        node_colors: {node: "#hex"} overrides (default themed blue).
        nodes: extra nodes to include even if they have no edges.
        layout: "circle" (default), a {node: (x, y)} dict with 0..1 coords,
                or None for a live force layout. physics=True also forces it.
        """
        import math

        ids = []
        for _u, _v in edges:
            for _t in (_u, _v):
                if _t not in ids:
                    ids.append(_t)
        for _t in nodes or []:
            if _t not in ids:
                ids.append(_t)
        node_colors = node_colors or {}
        hi = {frozenset(e) for e in highlight}
        pos = {}
        if isinstance(layout, dict):
            pos = {k: (float(x), float(y)) for k, (x, y) in layout.items()}
        elif layout == "circle" and ids:
            for _i, _nid in enumerate(ids):
                _a = 2 * math.pi * _i / len(ids) - math.pi / 2
                pos[_nid] = (0.5 + 0.42 * math.cos(_a), 0.5 + 0.42 * math.sin(_a))
        # One scale for both axes, then centre: scaling 0..1 coords by width
        # and height separately turned every ring into a 4:3 ellipse.
        _s = min(width, height)
        _ox, _oy = (width - _s) / 2, (height - _s) / 2
        node_list = []
        for _nid in ids:
            _d = {"id": str(_nid), "color": node_colors.get(_nid, "#35577F")}
            if _nid in pos:
                _d["x"] = _ox + pos[_nid][0] * _s
                _d["y"] = _oy + pos[_nid][1] * _s
            node_list.append(_d)
        link_list = [
            {
                "source": str(_u),
                "target": str(_v),
                **(
                    {"color": "#B4552D", "width": 3.5}
                    if frozenset((_u, _v)) in hi
                    else {}
                ),
            }
            for _u, _v in edges
        ]
        return _NetViz(
            nodes=node_list,
            links=link_list,
            width=width,
            height=height,
            physics=bool(physics) or not pos,
        )

    return (netviz,)


@app.cell(hide_code=True)
def _(alt, ig, mo, netviz, np, nx, pd, plt):
    def run_student_code(code, env=None):
        """Run code from a fill-in exercise box; show stdout + last expression.

        Errors come back as one friendly line, not a wall of traceback."""
        import ast
        import contextlib
        import io

        ns = {
            "mo": mo, "ig": ig, "nx": nx, "np": np,
            "plt": plt, "alt": alt, "pd": pd, "netviz": netviz,
        }
        ns.update(env or {})
        buf = io.StringIO()
        try:
            tree = ast.parse(code or "", mode="exec")
            last = None
            if tree.body and isinstance(tree.body[-1], ast.Expr):
                last = ast.Expression(tree.body[-1].value)
                tree.body = tree.body[:-1]
            with contextlib.redirect_stdout(buf):
                exec(compile(tree, "<your code>", "exec"), ns)
                result = (
                    eval(compile(last, "<your code>", "eval"), ns)
                    if last is not None
                    else None
                )
        except Exception as e:
            line = getattr(e, "lineno", None)
            tb = getattr(e, "__traceback__", None)
            while tb is not None:
                if tb.tb_frame.f_code.co_filename == "<your code>":
                    line = tb.tb_lineno
                tb = tb.tb_next
            where = f" on line {line}" if line else ""
            return mo.md(
                f"🤔 **Python hiccup{where}:** `{type(e).__name__}: {e}`\n\n"
                "*Read it slowly — it usually names the problem. "
                "Fix it and press ▶ Run again.*"
            )
        parts = []
        if buf.getvalue():
            parts.append(mo.md(f"```\n{buf.getvalue()}\n```"))
        if result is not None:
            parts.append(result)
        if not parts:
            parts.append(
                mo.md(
                    "✅ *Ran without errors — nothing to display yet. "
                    "End with a bare value (like `my_L`) to show it.*"
                )
            )
        return mo.vstack(parts)

    return (run_student_code,)


@app.cell(hide_code=True)
def ch1_header(mo):
    mo.md("""
    ## Chapter 1 of 5 — A Letter Across a Country

    It begins with an experiment. In the 1960s, letters were mailed to
    strangers in Nebraska with one rule — pass it only to someone you know
    on a first-name basis — and one target: a stockbroker in Boston. How
    many hands does a letter like that need? My guess is below, next to
    what actually happened.
    """)
    return


@app.cell(hide_code=True)
def cp1_milgram_img(mo):
    mo.vstack([
        mo.image(
            src="assets/milgram-small-world-experiment.png",
            width=520,
            caption="Milgram's letter experiment (1960s)",
        ),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>Read the picture as a "
            "relay. A packet starts with a randomly chosen person in Omaha, "
            "Nebraska, and has to reach one named stockbroker near Boston. Nobody "
            "may post it directly: each holder passes it to a single person they "
            "know on a first-name basis and who they think sits closer to the "
            "target. Each arrow is one such hand-off. The experiment counts the "
            "arrows.</span>"
        ),
    ])
    return


@app.cell(hide_code=True)
def cp1_milgram_note(mo):
    mo.md(r"""
    ### 🌍 Six degrees of separation
    In the 1960s, Stanley Milgram mailed packets to strangers in Nebraska
    with one rule: pass it to someone you know on a first-name basis,
    until it reaches a Boston stockbroker. The letters that arrived took
    about **6 hops** (64 of 160 made it). A 2012 study re-measured this on
    Facebook's 721 million users: **4.74 steps** on average.

    > **My guess:** about 20 — the country is huge — but the real number was far smaller.
    """)
    return


@app.cell(hide_code=True)
def detour_lost_letters(alt, mo, pd):
    _lost = pd.DataFrame({
        "outcome": ["arrived — counted", "lost — never counted"],
        "letters": [64, 96],
    })
    mo.vstack([
        mo.md(r"""
        ### 🧭 **Detour:** What about the letters that got lost?
        > *"Only 64 of the 160 letters arrived. Doesn't that make the 6 unfair?"*

        Milgram's "about 6" is an average over the **letters that arrived** —
        the 96 that got lost don't count. This is **survivorship bias**:
        judging a whole group by the members who made it to the end. The
        lost letters were probably on *longer* chains, so 6 is likely an
        under-estimate.

        **The honest takeaway:** the result doesn't rest on Milgram alone. A
        2012 study covered *every* pair of Facebook's 721 million users —
        nothing lost — and still found 4.74 steps.
        """),
        alt.Chart(_lost)
        .mark_bar()
        .encode(
            x=alt.X("letters:Q", title="letters"),
            y=alt.Y("outcome:N", title=None, sort=None),
            color=alt.Color(
                "outcome:N",
                legend=None,
                scale=alt.Scale(range=["#35577F", "#B4552D"]),
            ),
        )
        .properties(
            width=420,
            height=90,
            title="160 letters mailed — the famous average rests on the blue bar",
        ),
    ])
    return


@app.cell(hide_code=True)
def ch2_header(mo):
    mo.md("""
    ## Chapter 2 of 5 — Measuring Smallness

    "Small" needs a number before it means anything. This chapter builds
    the module's two measuring sticks. First **distance** — how many steps
    separate two people — on a four-person network, and then again by hand
    on paper. Then a second measure that distance cannot see at all, about
    the shape of one person's own circle of friends.
    """)
    return


@app.cell(hide_code=True)
def cp2_steps(mo):
    cp2_steps = mo.ui.slider(0, 3, value=0, step=1, label="steps from A")
    cp2_steps
    return (cp2_steps,)


@app.cell(hide_code=True)
def cp2_ripple_fig(cp2_steps, mo, netviz, nx):
    _edges = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D")]
    _G = nx.Graph()
    _G.add_edges_from(_edges)

    _reached = set()
    _frontier = {"A"}
    for _ in range(cp2_steps.value):
        _nxt = set()
        for _u in _frontier:
            for _v in _G[_u]:
                if _v != "A" and _v not in _reached:
                    _reached.add(_v)
                    _nxt.add(_v)
        _frontier = _nxt

    _colors = {
        _n: ("#B4552D" if _n == "A" else ("#C98A2D" if _n in _reached else "#E4E6EA"))
        for _n in _G.nodes()
    }
    mo.vstack([
        mo.md(f"**Wave from A — {cp2_steps.value} step(s)**"),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>Four people, five "
            "friendships. **A** is rust; **amber** dots are everyone A can reach "
            "in that many steps or fewer; **grey** dots are still out of range. "
            "Drag the slider up one notch at a time and watch who joins — the "
            "step at which someone first turns amber IS their distance from A. "
            "You can drag the dots too; moving them changes nothing but the "
            "picture.</span>"
        ),
        netviz(_edges, node_colors=_colors),
    ])
    return


@app.cell(hide_code=True)
def cp2_pairs_fig(alt, mo, pd):
    _pairs = [("A", "B", 1), ("A", "C", 1), ("A", "D", 2), ("B", "C", 1), ("B", "D", 1), ("C", "D", 1)]
    _df = pd.DataFrame(_pairs, columns=["u", "v", "distance"])
    _df["pair"] = _df["u"] + "–" + _df["v"]
    _df["highlight"] = _df["distance"] > 1

    mo.vstack([
        alt.Chart(_df)
        .mark_bar(size=22, cornerRadiusEnd=4)
        .encode(
            y=alt.Y("pair:N", sort=_df["pair"].tolist(), title=None),
            x=alt.X(
                "distance:Q",
                title="shortest-path distance",
                scale=alt.Scale(domain=[0, 2.4]),
            ),
            color=alt.condition(
                "datum.highlight", alt.value("#B4552D"), alt.value("#35577F")
            ),
            tooltip=["pair", "distance"],
        )
        .properties(
            title="All 6 pairs, distance — average 7/6 ≈ 1.17",
            height=220,
        ),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>One bar per pair of "
            "people — with four people there are exactly six pairs, and every "
            "pair gets counted once. Bar length is that pair's distance, so a "
            "one-step bar means they are directly connected; the **rust bar is "
            "the only pair that needs a detour**. Average path length is just "
            "the mean of these six bars — the single number in the title.</span>"
        ),
    ])
    return


@app.cell(hide_code=True)
def cp2_distance_note(mo):
    mo.md(r"""
    ### 📏 Distance and average path length
    The **distance** $d(u,v)$ between two people is the number of edges on
    the shortest route between them. Averaging over every pair gives the
    **average path length** $L$ — one number for how far apart a whole
    network sits. Here five pairs sit at distance 1 and A–D at 2, so
    $L = 7/6 \approx 1.17$. "Six degrees" is exactly this number, measured
    on a whole country.

    > **I worked out:** A to D is 2 — you have to go through B or C. Average: five pairs are 1 and A–D is 2, so 7/6 ≈ 1.17.
    """)
    return


@app.cell(hide_code=True)
def cp2_paperwork_photo(mo):
    cp2_paperwork_photo = mo.ui.file(
        kind="area",
        filetypes=[".jpg", ".jpeg", ".png", ".webp"],
        label="Photo of your paper work",
    )
    mo.vstack([
        cp2_paperwork_photo,
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>Drop a phone photo of "
            "your paper here — the 5-dot ring, your list of all 10 pairs with a "
            "distance beside each, and the average at the bottom. Working shown "
            "beats a tidy answer.</span>"
        ),
    ])
    return (cp2_paperwork_photo,)


@app.cell(hide_code=True)
def cp2_paperwork_photo_preview(cp2_paperwork_photo, mo):
    _files = list(cp2_paperwork_photo.value or [])
    cp2_paperwork_photo_send = mo.ui.run_button(
        label="📨 Send to my tutor", disabled=not _files
    )
    if not _files:
        _out = mo.vstack([
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>*Your photo appears "
                "here once you drop it in above.*</span>"
            ),
            cp2_paperwork_photo_send,
        ])
    else:
        _out = mo.vstack([
            mo.image(_files[0].contents, width=420),
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>This is exactly what "
                "your tutor will see. Missed a pair, or want to redo the table? Drop "
                "another photo into the box above — it replaces this one, as many "
                "times as you like. When it looks right, press send.</span>"
            ),
            cp2_paperwork_photo_send,
        ])
    _out
    return (cp2_paperwork_photo_send,)


@app.cell(hide_code=True)
def cp2_paperwork_photo_sent(cp2_paperwork_photo, cp2_paperwork_photo_send, mo):
    if cp2_paperwork_photo_send.value and (cp2_paperwork_photo.value or []):
        from pathlib import Path as _P

        _P("session_artifacts").mkdir(exist_ok=True)
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("cp2_paperwork_photo\n")
        _sent = mo.md("✅ **Sent.** Your tutor is looking at it now.")
    else:
        _sent = mo.md(
            "<span style='color:#6A6D75;font-size:13px'>*Press the button above "
            "when the photo looks right — that is what tells your tutor to look.*</span>"
        )
    _sent
    return


@app.cell(hide_code=True)
def cp2_paperwork_photo_view(mo):
    mo.vstack([
        mo.md(
            "<span style='border:1px dashed #C98A2D; border-radius:6px; "
            "display:block; padding:26px 12px; text-align:center; color:#6A6D75; "
            "font-size:13px;'>📷 <strong>My photographed page sits here.</strong>"
            "<br>In a real session this cell holds the saved photo; a reference "
            "notebook has no photograph of its own to show.</span>"
        ),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>📷 My own work on paper "
            "— the task: draw a 5-dot ring, find the distance for all 10 pairs, then the average.</span>"
        ),
    ])
    return


@app.cell(hide_code=True)
def cp2_paperwork_note(mo):
    mo.md(r"""
    ### ✏️ By hand: distance on a 5-ring
    Same two ideas as before — $d(u,v)$, the distance between two people
    (the fewest lines you cross to get from $u$ to $v$), and $L$, the
    average of $d(u,v)$ over every pair — computed entirely on paper this
    time, on a network no widget ever showed. 5 pairs sit at distance 1,
    5 "across the circle" pairs sit at distance 2, so $L = 15/10 = 1.5$.

    > **My work:** neighbors AB, BC, CD, DE, EA are all 1. The across pairs AC, AD, BD, BE, CE are 2 each. Sum 5 + 10 = 15, over 10 pairs = 1.5.
    """)
    return


@app.cell(hide_code=True)
def cp3_fig(mo, netviz):
    _edges = [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "F"), ("B", "F"), ("C", "E")]
    _friend_edges = [("B", "F"), ("C", "E")]
    mo.vstack([
        mo.md("**A and A's five friends — rust lines = a friendship between two of A's friends**"),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>**A** is the rust dot in "
            "the middle; B, C, D, E and F are its five friends. The grey lines "
            "from A are A's own friendships — ignore those. The **rust lines run "
            "between two of A's friends**: those are the ones that say "
            '"my friends know each other". Find them and count them yourself. '
            "Dots are drag-able if the picture gets tangled.</span>"
        ),
        netviz(_edges, highlight=_friend_edges, node_colors={"A": "#B4552D"}),
    ])
    return


@app.cell(hide_code=True)
def cp3_clustering_note(mo):
    mo.md(r"""
    ### 🤝 Local clustering — do my friends know each other?
    The **local clustering coefficient** of a person $i$ is
    $C_i = \frac{\text{friendships among } i\text{'s friends}}{\text{possible ones}}$.
    A has 5 friends, so up to 10 friendships could exist among them; 2 do,
    so $C_A = 2/10 = 0.2$. Averaging $C_i$ over everyone gives the
    network's clustering $C$ — typically HIGH in social networks.

    > **I worked out:** count the friend-pairs that are friends themselves and divide by all possible pairs. Two rust lines — B–F and C–E — so 2 out of 10 = 0.2.
    """)
    return


@app.cell(hide_code=True)
def ch3_header(mo):
    mo.md("""
    ## Chapter 3 of 5 — One Extra Line

    A ring of dots, and one extra cable to spend anywhere. Where should it
    go? That one choice opens this chapter's real question — what a single
    link can do to a whole network — and leads to the formulas for how a
    ring's clustering and distances behave as it grows.
    """)
    return


@app.cell(hide_code=True)
def cp4_photo(mo):
    cp4_photo = mo.ui.file(
        kind="area",
        filetypes=[".jpg", ".jpeg", ".png", ".webp"],
        label="Photo of your drawing",
    )
    mo.vstack([
        cp4_photo,
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>Drop a phone photo of "
            "your 8-dot ring here — the drawing with your one extra cable on it. "
            "It does not need to be neat; it needs to show which two dots you "
            "joined.</span>"
        ),
    ])
    return (cp4_photo,)


@app.cell(hide_code=True)
def cp4_photo_preview(cp4_photo, mo):
    _files = list(cp4_photo.value or [])
    cp4_photo_send = mo.ui.run_button(label="📨 Send to my tutor", disabled=not _files)
    if not _files:
        _out = mo.vstack([
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>*Your photo appears "
                "here once you drop it in above.*</span>"
            ),
            cp4_photo_send,
        ])
    else:
        _out = mo.vstack([
            mo.image(_files[0].contents, width=420),
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>This is exactly what "
                "your tutor will see. Not the one you meant? Drop another photo "
                "into the box above — it replaces this one, as many times as you "
                "like. When it looks right, press send.</span>"
            ),
            cp4_photo_send,
        ])
    _out
    return (cp4_photo_send,)


@app.cell(hide_code=True)
def cp4_photo_sent(cp4_photo, cp4_photo_send, mo):
    if cp4_photo_send.value and (cp4_photo.value or []):
        from pathlib import Path as _P

        _P("session_artifacts").mkdir(exist_ok=True)
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("cp4_photo\n")
        _sent = mo.md("✅ **Sent.** Your tutor is looking at it now.")
    else:
        _sent = mo.md(
            "<span style='color:#6A6D75;font-size:13px'>*Press the button above "
            "when the photo looks right — that is what tells your tutor to look.*</span>"
        )
    _sent
    return


@app.cell(hide_code=True)
def cp4_photo_view(mo):
    mo.vstack([
        mo.md(
            "<span style='border:1px dashed #C98A2D; border-radius:6px; "
            "display:block; padding:26px 12px; text-align:center; color:#6A6D75; "
            "font-size:13px;'>📷 <strong>My photographed page sits here.</strong>"
            "<br>In a real session this cell holds the saved photo; a reference "
            "notebook has no photograph of its own to show.</span>"
        ),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>📷 My own work on paper "
            "— the task: draw an 8-dot ring and add ONE extra cable where it shrinks travel the most.</span>"
        ),
    ])
    return


@app.cell(hide_code=True)
def cp4_choice(mo):
    cp4_choice = mo.ui.radio(
        options=["no extra cable", "short cable (2 apart)", "long cable (opposite)"],
        value="no extra cable",
        label="Where does your one cable go?",
    )
    cp4_choice
    return (cp4_choice,)


@app.cell(hide_code=True)
def cp4_compare_fig(cp4_choice, mo, netviz, nx):
    _edges = [(i, (i + 1) % 8) for i in range(8)]
    _extra = None
    if cp4_choice.value == "short cable (2 apart)":
        _extra = (0, 2)
    elif cp4_choice.value == "long cable (opposite)":
        _extra = (0, 4)
    _G = nx.cycle_graph(8)
    if _extra:
        _G.add_edge(*_extra)
        _edges.append(_extra)
    _L = nx.average_shortest_path_length(_G)

    mo.vstack([
        mo.md(f"**Average distance: {_L:.2f}**"),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>The same 8-dot ring three "
            "times over. The **rust line is the one extra cable**; the number "
            "above is the average trip length over all 28 pairs, recomputed every "
            "time you switch. Flip between the three options and watch only that "
            "number: same ring, same single extra line, and the only thing that "
            "changed is where it was put.</span>"
        ),
        netviz(_edges, highlight=[_extra] if _extra else [], layout="circle"),
    ])
    return


@app.cell(hide_code=True)
def cp4_shortcut_drawing_note(mo):
    mo.md(r"""
    ### 🔌 One cable, two very different effects
    Same single line, two jobs. Between nearby dots it closes a
    **triangle** — clustering goes up. Across the ring it is a
    **shortcut** — trips get shorter for everyone at once. On this
    8-dot ring the average distance goes $2.29 \rightarrow 2.07$ with a
    short cable and $2.29 \rightarrow 1.96$ with a long one: about half
    again as much travel saved, from one line placed differently. WHERE
    a link goes matters more than HOW MANY links there are — and the
    bigger the ring, the wider that gap gets.

    > **My cable:** I connected the two dots straight across from each other — the far pairs have the worst trips, and a bridge in the middle cuts all of them down at once.
    """)
    return


@app.cell(hide_code=True)
def cp5_ring_controls(mo):
    cp5_ring_k = mo.ui.slider(
        steps=[2, 4, 6], value=2, label="k (friends per person)", show_value=True
    )
    cp5_ring_show = mo.ui.checkbox(
        value=False, label="check my count (highlight friendships among the amber dots)"
    )
    mo.hstack([cp5_ring_k, cp5_ring_show], justify="start", gap=2)
    return cp5_ring_k, cp5_ring_show


@app.cell(hide_code=True)
def cp5_ring_fig(cp5_ring_k, cp5_ring_show, mo, netviz):
    import math as _math

    _N = 12
    _k = cp5_ring_k.value
    _half = _k // 2

    # Explicit node order (0..N-1) for the circle layout — netviz's own
    # "circle" string layout orders nodes by first appearance in the edge
    # list, which a deduped/sorted edge set scrambles (a node can land in the
    # wrong slot). Position every node ourselves instead.
    _pos = {
        _i: (
            0.5 + 0.42 * _math.cos(2 * _math.pi * _i / _N - _math.pi / 2),
            0.5 + 0.42 * _math.sin(2 * _math.pi * _i / _N - _math.pi / 2),
        )
        for _i in range(_N)
    }
    _edges = [(_i, (_i + _d) % _N) for _i in range(_N) for _d in range(1, _half + 1)]
    _edge_lookup = {tuple(sorted(e)) for e in _edges}

    _friends = sorted({_d % _N for _d in range(1, _half + 1)} | {(-_d) % _N for _d in range(1, _half + 1)})
    _friend_pairs = [
        (_friends[_i], _friends[_j])
        for _i in range(len(_friends))
        for _j in range(_i + 1, len(_friends))
        if tuple(sorted((_friends[_i], _friends[_j]))) in _edge_lookup
    ]
    _node_colors = {0: "#B4552D", **{_f: "#C98A2D" for _f in _friends}}
    _hl = _friend_pairs if cp5_ring_show.value else []
    mo.vstack([
        mo.md(
            "**Node 0** is the rust dot; the **amber dots are its friends** "
            f"({_half} on each side). Every line is a friendship — the ones to "
            "count are the lines that join *two amber dots*."
        ),
        netviz(_edges, highlight=_hl, node_colors=_node_colors, layout=_pos),
    ])
    return


@app.cell(hide_code=True)
def cp5_ring_paperwork_photo(mo):
    cp5_ring_paperwork_photo = mo.ui.file(
        kind="area",
        filetypes=[".jpg", ".jpeg", ".png", ".webp"],
        label="Photo of your ring working (triangles + formulas)",
    )
    mo.vstack([
        cp5_ring_paperwork_photo,
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>Drop a phone photo of "
            "your derivation here — node 0's friends, which pairs among them "
            "already know each other, and the two formulas you ended up with. "
            "Crossings-out are fine and welcome.</span>"
        ),
    ])
    return (cp5_ring_paperwork_photo,)


@app.cell(hide_code=True)
def cp5_ring_paperwork_photo_preview(cp5_ring_paperwork_photo, mo):
    _files = list(cp5_ring_paperwork_photo.value or [])
    cp5_ring_paperwork_photo_send = mo.ui.run_button(
        label="📨 Send to my tutor", disabled=not _files
    )
    if not _files:
        _out = mo.vstack([
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>*Your photo appears "
                "here once you drop it in above.*</span>"
            ),
            cp5_ring_paperwork_photo_send,
        ])
    else:
        _out = mo.vstack([
            mo.image(_files[0].contents, width=420),
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>This is exactly what "
                "your tutor will see. Want to fix a step and try again? Drop another "
                "photo into the box above — it replaces this one, as many times as "
                "you like. When it looks right, press send.</span>"
            ),
            cp5_ring_paperwork_photo_send,
        ])
    _out
    return (cp5_ring_paperwork_photo_send,)


@app.cell(hide_code=True)
def cp5_ring_paperwork_photo_sent(
    cp5_ring_paperwork_photo, cp5_ring_paperwork_photo_send, mo
):
    if cp5_ring_paperwork_photo_send.value and (cp5_ring_paperwork_photo.value or []):
        from pathlib import Path as _P

        _P("session_artifacts").mkdir(exist_ok=True)
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("cp5_ring_paperwork_photo\n")
        _sent = mo.md("✅ **Sent.** Your tutor is looking at it now.")
    else:
        _sent = mo.md(
            "<span style='color:#6A6D75;font-size:13px'>*Press the button above "
            "when the photo looks right — that is what tells your tutor to look.*</span>"
        )
    _sent
    return


@app.cell(hide_code=True)
def cp5_ring_paperwork_photo_view(mo):
    mo.vstack([
        mo.md(
            "<span style='border:1px dashed #C98A2D; border-radius:6px; "
            "display:block; padding:26px 12px; text-align:center; color:#6A6D75; "
            "font-size:13px;'>📷 <strong>My photographed page sits here.</strong>"
            "<br>In a real session this cell holds the saved photo; a reference "
            "notebook has no photograph of its own to show.</span>"
        ),
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>📷 My own work on paper "
            "— the task: count the friendships among node 0's friends at k=4, then write down how C and L depend on N and k.</span>"
        ),
    ])
    return


@app.cell(hide_code=True)
def cp5_ring_formula_note(mo):
    mo.md(r"""
    ### 🔺 Clustering and path length on a ring — as formulas
    Four letters: $N$ = people in the ring, $k$ = friends each person
    has, $C$ = clustering (how often two of your friends know each
    other), $L$ = average distance (typical steps between two people).

    On a ring where everyone has $k$ friends ($k/2$ per side),
    $C(k) = \frac{3(k-2)}{4(k-1)}$ — a function of $k$ ONLY, never $N$.
    $k=2$ gives $C=0$, $k=4$ gives $C=0.5$, the value I counted out. Every
    neighbourhood is identical, so node 0's $C_0$ is the ring's $C$.

    Path length grows with the crowd instead: the farthest trip is about
    $N/k$ hops — half a ring at $k/2$ places per hop — and the average is
    about half that, $L \approx N/(2k)$.

    > **My work:** at k=2 my two friends sit on opposite sides of me, two steps apart — never friends, so C = 0. At k=4, of the 6 possible pairs 3 already exist, so C₀ = 3/6 = 0.5. Swapping in 1000 people changes nothing near me — C stays 0.5. Farthest trip ≈ 1000/4 = 250 hops, and the average is about half that, so L ≈ N/(2k).
    """)
    return


@app.cell(hide_code=True)
def cp5_tension_note(mo):
    mo.md(r"""
    ### ⚖️ The puzzle: clustered AND close?
    Same four letters as before: $C$ = clustering (how often two of your
    friends know each other), $L$ = average distance (typical number of
    steps between two people), $N$ = how many people there are, $k$ = how
    many friends each person has.

    **Ring world:** tight communities (high $C$, independent of $N$) but
    journeys that get longer and longer as $N$ grows ($L \approx N/(2k)$).
    **Random world:** short journeys (low $L$) but no community (low
    $C$). Real social networks somehow have BOTH high clustering and
    short paths — neither extreme world explains it.

    > **My take on the two worlds:** the ring is cosy — my friends all know each other — but a letter crawls, L blows up with N. The random world delivers mail fast but none of my friends know each other. Real life somehow gets both.
    """)
    return


@app.cell(hide_code=True)
def ch4_header(mo):
    mo.md("""
    ## Chapter 4 of 5 — Turning One Dial

    Chapter 3 ended in a tension: the ring world is clustered but
    far-flung, the random world is close but has no community. This
    chapter puts a dial between the two worlds — rewire a fraction $p$ of
    the ring's links to random targets — and watches what each measure
    does as the dial turns: first on a slider, then with real code at
    N=2000.
    """)
    return


@app.cell(hide_code=True)
def cp6_legend(mo):
    mo.md(
        r"""**Reading the dials:** $p$ = the fraction of the ring's links picked
up and reconnected to someone chosen at random — the slider below. $L$ =
average distance — how many steps apart a typical pair is. $C$ = clustering
— how often two of your friends know each other. $L_0$ and $C_0$ are those
same numbers for the untouched ring ($p=0$), so $L/L_0 = 1$ means
"unchanged" and $L/L_0 = 0.2$ means distances shrank to a fifth."""
    )
    return


@app.cell(hide_code=True)
def cp6_p(mo):
    cp6_p = mo.ui.slider(
        steps=[0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0],
        value=0.0,
        label="rewiring probability p",
    )
    cp6_p
    return (cp6_p,)


@app.cell(hide_code=True)
def cp6_ws_fig(cp6_p, mo, netviz, nx):
    _p = float(cp6_p.value)
    _n, _k = 200, 4

    _ring = nx.watts_strogatz_graph(_n, _k, 0)
    _L0 = nx.average_shortest_path_length(_ring)
    _C0 = nx.average_clustering(_ring)

    _Ls, _Cs = [], []
    for _seed in (1, 2, 3):
        _H = nx.connected_watts_strogatz_graph(_n, _k, _p, seed=_seed) if _p > 0 else _ring
        _Ls.append(nx.average_shortest_path_length(_H))
        _Cs.append(nx.average_clustering(_H))
    _Lr = (sum(_Ls) / len(_Ls)) / _L0
    _Cr = (sum(_Cs) / len(_Cs)) / _C0

    import math as _math

    _D = nx.connected_watts_strogatz_graph(60, 4, _p, seed=5) if _p > 0 else nx.watts_strogatz_graph(60, 4, 0)
    _ringe = [e for e in _D.edges() if min(abs(e[0] - e[1]), 60 - abs(e[0] - e[1])) <= 2]
    _short = [e for e in _D.edges() if min(abs(e[0] - e[1]), 60 - abs(e[0] - e[1])) > 2]

    # Explicit node order (0..59) for the circle layout — netviz's "circle"
    # string layout orders nodes by first appearance in the edge list, and
    # nx.Graph.edges() after rewiring does NOT visit nodes in index order, so
    # the string layout scrambles node positions. Position every node ourselves.
    _pos60 = {
        _i: (
            0.5 + 0.42 * _math.cos(2 * _math.pi * _i / 60 - _math.pi / 2),
            0.5 + 0.42 * _math.sin(2 * _math.pi * _i / 60 - _math.pi / 2),
        )
        for _i in range(60)
    }
    mo.vstack([
        mo.md(
            f"**p = {_p} &nbsp;&nbsp; distance L/L₀ = {_Lr:.2f} &nbsp;&nbsp; "
            f"clustering C/C₀ = {_Cr:.2f}**\n\n"
            f"<span style='color:#6A6D75;font-size:13px'>The two numbers are measured "
            f"on a {_n}-person ring (averaged over 3 tries). The picture below is a "
            f"60-dot sketch of the same rewiring, small enough to see.</span>"
        ),
        netviz(_ringe + _short, highlight=_short, layout=_pos60, width=820, height=820),
    ])
    return


@app.cell(hide_code=True)
def cp6_watts_strogatz_note(mo):
    mo.md(r"""
    ### 🎛️ The Watts–Strogatz recipe (1998)
    The dials: $p$ = the fraction of links picked up and reconnected to a
    random person; $L$ = average distance (typical steps between two
    people); $C$ = clustering (how often two of your friends know each
    other). $L_0$ and $C_0$ are the same two on the untouched ring, so the
    ratios read "compared to before".

    Rewiring only about 1% of a ring's links ($p \approx 0.01$) already
    pulls distance down hard — here $L/L_0$ falls to about $0.6$ — while
    clustering barely moves ($C/C_0 \approx 1$). Those few rewires are the
    long cables from my drawing: rare enough to keep the communities, long
    enough to shortcut the whole ring. That's the small-world recipe, and
    it's why six degrees works.

    > **My prediction:** distance drops a lot, clustering barely changes → **what I actually saw:**
    L/L₀ fell off a cliff around p ≈ 0.01 — down to 0.61 — while C/C₀ was still 0.97. Called it, but the cliff came earlier than I expected.
    """)
    return


@app.cell(hide_code=True)
def cp6_large_n_ed(mo):
    cp6_large_n_ed = mo.ui.code_editor(
        value='''# 1. Set a LARGE network size — much bigger than the N=200 you played with.
N = 2000  # try 2000
k = 4
p_values = [0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0]

L0 = C0 = None
rows = []
for p in p_values:
    G = nx.connected_watts_strogatz_graph(N, k, p, seed=1) if p > 0 else nx.watts_strogatz_graph(N, k, 0)
    # 2. Measure the average distance of G — nx.average_shortest_path_length
    L = nx.average_shortest_path_length(G)
    # 3. Measure the average clustering of G — nx.average_clustering
    C = nx.average_clustering(G)
    if p == 0.0:
        L0, C0 = L, C
    rows.append({"p": str(p), "L/L0": L / L0, "C/C0": C / C0})

df = pd.DataFrame(rows).melt("p", var_name="measure", value_name="ratio")
alt.Chart(df).mark_line(point=True).encode(
    x=alt.X("p:O", title="rewiring probability p"),
    y=alt.Y("ratio:Q", title="ratio to p=0 baseline"),
    color=alt.Color("measure:N", scale=alt.Scale(range=["#B4552D", "#35577F"])),
).properties(title=f"N={N}, k={k}")
''',
        language="python",
        label="Your experiment — fill the ... blanks, then press ▶ Run below",
    )
    cp6_large_n_ed
    return (cp6_large_n_ed,)


@app.cell(hide_code=True)
def cp6_large_n_out(cp6_large_n_ed, mo, run_student_code):
    mo.vstack([
        mo.md(
            "<span style='color:#6A6D75;font-size:13px'>▶ Run — output below is "
            "as it appeared after the student ran their filled-in code. It takes "
            "a minute on a network this size.</span>"
        ),
        run_student_code(cp6_large_n_ed.value),
    ])
    return


@app.cell(hide_code=True)
def cp6_large_n_experiment_note(mo):
    mo.md(r"""
    ### 💻 The phase transition, at scale
    Same experiment as the slider, but coded and run on a much bigger
    network — $N$, the number of people, is 2000 here instead of 200. I
    swept $p$ (the fraction of links rewired at random) and plotted
    $L/L_0$ (average distance, compared to the untouched ring) against
    $C/C_0$ (clustering, compared to the untouched ring).

    > **What I found:** same cliff, but earlier — at N=2000 the L/L₀ drop is already big by p = 0.005, while C/C₀ hasn't moved. The fraction of rewires you need got smaller as N grew, not bigger.
    """)
    return


@app.cell(hide_code=True)
def ch5_header(mo):
    mo.md("""
    ## Chapter 5 of 5 — Mastery Check

    No new machinery in this final chapter — just two tests of whether the
    story holds. First an AI hands me its analysis of a network and asks
    me to sign off on it. Then a friend asks the question this module
    opened with, and I have to answer it in my own words.
    """)
    return


@app.cell(hide_code=True)
def cp7_redteam_note(mo):
    mo.md(r"""
    ### 🕵️ Reviewing an AI's claim
    "High clustering ⇒ small world" is NOT enough: small-world means BOTH
    high clustering AND short paths. My counterexample: the $p=0$ ring —
    very clustered, yet enormous distances. The proper check is the
    small-world index $\sigma$, one number that compares both $C$
    (clustering — how often two of your friends know each other) and $L$
    (average distance — the typical number of steps between two people)
    against a random network of the same size.

    > **My review of the AI's analysis:** I wouldn't sign it. They only measured clustering — small-world needs short paths too. My own k=4 ring had C = 0.5 with terrible distances. I'd ask for L, compared against a random network, before believing the claim — the σ index does exactly that.
    """)
    return


@app.cell(hide_code=True)
def cp8_wrapup_note(mo):
    mo.md(r"""
    ### 🎓 The whole story, in my own words
    > Most of your friends live near you, so the world is clumpy. But a few people keep far-away links, and those shortcuts cut the distance for everyone at once. Six steps is enough because almost every route can jump onto one of those shortcuts.

    Local links make clusters; a few long-range shortcuts exist; those
    shortcuts pull everyone close. That's how a letter crosses a country
    in about six steps.
    """)
    return


@app.cell(hide_code=True)
def session_record(mo):
    mo.md(r"""
    ## 📋 Session record

    *Your answer to each question, and every word you typed while working on*
    *it — this is what gets reviewed, not the code. Hints are never held*
    *against you.*

    **cp0_welcome** · pass

    *How do you feel about Python?*

    > comfortable with Python

    *You chose:* "comfortable with Python"

    *Tutor's note:* Calibrated the session — code cells stay visible.

    **cp1_milgram** · prediction

    *For the letters that made it, how many hands on average?*

    > about 20

    *You chose:* "about 20"

    *You typed:* "way off — the country is huge, I'd never have said 6"

    *Tutor's note:* Honest reconciliation after the reveal; full pass.

    **cp2_distance** · pass

    *Distance from A to D, then the average over all 6 pairs?*

    > A to D is 2. Average 7/6 ≈ 1.17

    *You typed:* "2 — you have to go through B or C" · "five pairs are 1 and A–D is 2, so 7/6 ≈ 1.17"

    *Tutor's note:* Listed all six pairs unprompted before averaging.

    **cp2_paperwork** · pass

    *By hand on a 5-ring: every pair's distance, then the average.*

    > neighbors AB, BC, CD, DE, EA are all 1. The across pairs AC, AD, BD, BE, CE are 2 each. Sum 5 + 10 = 15, over 10 pairs = 1.5.

    *You typed:* "neighbors AB, BC, CD, DE, EA are all 1. The across pairs AC, AD, BD, BE, CE are 2 each. Sum 5 + 10 = 15, over 10 pairs = 1.5."

    *Tutor's note:* Photo shows the ring, all 10 pairs listed, average at the bottom.

    **cp3_clustering** · pass

    *How many friendships exist among A's five friends, out of how many possible?*

    > count the friend-pairs that are friends themselves and divide by all possible pairs. Two rust lines — B–F and C–E — so 2 out of 10 = 0.2.

    *You typed:* "count the friend-pairs that are friends themselves and divide by all possible pairs" · "two rust lines — B–F and C–E — so 2 out of 10 = 0.2"

    *Tutor's note:* Reached the ratio without being given the denominator.

    **cp4_shortcut_drawing** · pass

    *One extra cable on an 8-ring — where does it go, and why there?*

    > the far pairs have the worst trips, and a bridge in the middle cuts all of them down at once

    *You typed:* "the far pairs have the worst trips, and a bridge in the middle cuts all of them down at once"

    *Tutor's note:* Photo shows a chord between dots 0 and 4 — straight across.

    **cp5_ring_formula** · pass_with_hints · 1 hint

    *Does C depend on N? And how does L relate to N and k?*

    > at k=2 my two friends sit on opposite sides of me, two steps apart — never friends, so C = 0. At k=4, of the 6 possible pairs 3 already exist, so C₀ = 3/6 = 0.5. Swapping in 1000 people changes nothing near me — C stays 0.5. Farthest trip ≈ 1000/4 = 250 hops, and the average is about half that, so L ≈ N/(2k).

    *You typed:* "at k=2 my two friends sit on opposite sides of me, two steps apart — never friends, so C = 0" · "of the 6 possible pairs 3 already exist, so C₀ = 3/6 = 0.5" · "swapping in 1000 people changes nothing near me — C stays 0.5" · "farthest trip ≈ 1000/4 = 250 hops, and the average is about half that, so L ≈ N/(2k)"

    *Tutor's note:* Needed one hint to split "half a ring" from "places per hop"; the rest was theirs.

    **cp5_tension** · pass

    *What do your two formulas say about the ring world, and about the random world?*

    > the ring is cosy — my friends all know each other — but a letter crawls, L blows up with N. The random world delivers mail fast but none of my friends know each other. Real life somehow gets both.

    *You typed:* "the ring is cosy — my friends all know each other — but a letter crawls, L blows up with N" · "the random world delivers mail fast but none of my friends know each other. Real life somehow gets both"

    *Tutor's note:* Named both trade-offs and landed on "neither world" by themselves.

    **cp6_watts_strogatz** · prediction

    *Which notch drops L/L₀ the most, and what is C/C₀ there?*

    > L/L₀ fell off a cliff around p ≈ 0.01 — down to 0.61 — while C/C₀ was still 0.97. Called it, but the cliff came earlier than I expected.

    *You chose:* "distance drops a lot, clustering barely changes"

    *You typed:* "L/L₀ fell off a cliff around p ≈ 0.01 — down to 0.61 — while C/C₀ was still 0.97. Called it, but the cliff came earlier than I expected."

    *Tutor's note:* Prediction correct and reconciled against the numbers on screen.

    **cp6_large_n_experiment** · pass

    *At which p does L/L₀ drop most on your own chart, and is that p bigger or smaller than at N=200?*

    > same cliff, but earlier — at N=2000 the L/L₀ drop is already big by p = 0.005, while C/C₀ hasn't moved. The fraction of rewires you need got smaller as N grew, not bigger.

    *You typed:* "same cliff, but earlier — at N=2000 the L/L₀ drop is already big by p = 0.005, while C/C₀ hasn't moved" · "the fraction of rewires you need got smaller as N grew, not bigger"

    *Tutor's note:* Ran the sweep at N=2000 and read the comparison off their own chart.

    **cp7_redteam** · pass

    *Would you sign off on the AI's small-world claim? What would you check?*

    > I wouldn't sign it. They only measured clustering — small-world needs short paths too. My own k=4 ring had C = 0.5 with terrible distances. I'd ask for L, compared against a random network, before believing the claim — the σ index does exactly that.

    *You typed:* "I wouldn't sign it. They only measured clustering — small-world needs short paths too. My own k=4 ring had C = 0.5 with terrible distances. I'd ask for L, compared against a random network, before believing the claim — the σ index does exactly that."

    *Tutor's note:* Cited their own p=0 ring as the counterexample, unprompted.

    **cp8_wrapup** · pass

    *How can a letter cross a whole country in about six steps?*

    > Most of your friends live near you, so the world is clumpy. But a few people keep far-away links, and those shortcuts cut the distance for everyone at once. Six steps is enough because almost every route can jump onto one of those shortcuts.

    *You typed:* "Most of your friends live near you, so the world is clumpy. But a few people keep far-away links, and those shortcuts cut the distance for everyone at once. Six steps is enough because almost every route can jump onto one of those shortcuts."

    *Tutor's note:* All three ingredients — clusters, rare long links, everyone close.

    ### 🧭 Your own questions (1)

    - *Only 64 of the 160 letters arrived — doesn't that make the 6 unfair?*
    """)
    return


if __name__ == "__main__":
    app.run()
