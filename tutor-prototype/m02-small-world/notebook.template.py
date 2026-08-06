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
#     "traitlets",
#     "numpy",
#     "pandas",
#     "pillow",
# ]
# ///

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
  // Label ink follows the fill. White was hardcoded, which is 1.25:1 on the
  // neutral #E4E6EA and 2.93:1 on amber — so on cp2's ripple three of four
  // labels were invisible, including the D the question is about, and on
  // cp5's ring the amber friends were the least legible nodes in the figure.
  const inkFor = (hex) => {
    const lum = (h) => {
      const m = /^#?([0-9a-f]{6})$/i.exec(h || "");
      if (!m) return null;
      const n = parseInt(m[1], 16);
      const lin = (c) => { c /= 255; return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4); };
      return 0.2126 * lin((n >> 16) & 255) + 0.7152 * lin((n >> 8) & 255) + 0.0722 * lin(n & 255);
    };
    const bg = lum(hex);
    if (bg == null) return "#1D1E21";
    // Take whichever ink reads better, rather than thresholding on white:
    // amber is the mid-luminance fill where white fails (2.93:1) and so does
    // a mid-grey ink — #1D1E21 clears it at 5.68:1, and this also covers any
    // fill added later.
    const ratio = (a, b) => (Math.max(a, b) + 0.05) / (Math.min(a, b) + 0.05);
    return ratio(bg, lum("#FFFFFF")) >= ratio(bg, lum("#1D1E21")) ? "#FFFFFF" : "#1D1E21";
  };
  node.append("text")
    .text(d => d.label ?? d.id)
    .attr("text-anchor", "middle").attr("dy", "0.35em")
    .attr("fill", d => inkFor(d.color || "#35577F"))
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


# The ⚖️ appeal box lives at the BOTTOM of the page, always: the notebook
# tool re-pins these two cells below every cell it inserts, finding them by
# the "tutor_stuck_send" marker in their code. They are anonymous (def _) on
# purpose — nb_fresh_start's wipe deletes every NAMED cell.
@app.cell(hide_code=True)
def _(mo):
    tutor_stuck_text = mo.ui.text_area(
        placeholder=(
            "What's going on? e.g. \"I answered this and I think it should count\", "
            "\"I'd like a fresh try at this one\", \"we're going in circles — let's move on\""
        ),
        rows=2,
    )
    tutor_stuck_send = mo.ui.run_button(label="⚖️ Tutor gets stuck — call the referee")
    mo.accordion({
        "⚖️ Stuck with your tutor?": mo.vstack([
            mo.md(
                "<span style='color:#6A6D75;font-size:13px'>If the two of you are "
                "going in circles — you think an answer should count, you want a "
                "fresh try, or you'd rather move on — say so below and press the "
                "button. A second, stronger model reads the whole situation and "
                "makes a call your tutor has to follow. Using it is never held "
                "against you.</span>"
            ),
            tutor_stuck_text,
            tutor_stuck_send,
        ])
    })
    return tutor_stuck_send, tutor_stuck_text


@app.cell(hide_code=True)
def _(mo, tutor_stuck_send, tutor_stuck_text):
    from pathlib import Path as _P_appeal

    if tutor_stuck_send.value:
        _P_appeal("session_artifacts").mkdir(exist_ok=True)
        (_P_appeal("session_artifacts") / "appeal.txt").write_text(
            (tutor_stuck_text.value or "").strip() or "(no details given)"
        )
        with open("session_artifacts/student_signal.txt", "a") as _f:
            _f.write("tutor_stuck\n")
        _appeal_out = mo.md(
            "<span style='color:#6A6D75;font-size:13px'>✅ <strong>The referee is "
            "reading your case.</strong> It can take a minute — your tutor will "
            "come back to you in the terminal with the decision.</span>"
        )
    else:
        _appeal_out = mo.md("")
    _appeal_out
    return


if __name__ == "__main__":
    app.run()
