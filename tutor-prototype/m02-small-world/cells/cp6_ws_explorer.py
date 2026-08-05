# Premade cells for checkpoint cp6_watts_strogatz — the rewiring explorer.
# Insert AFTER the student commits a prediction.
# describe: A legend defining the symbols (L = average distance, C = clustering, L0/C0 = the p=0 ring baseline), a rewiring-probability slider p, and a 60-dot ring on a drag-able network widget where rewired shortcut edges are rust lines; the title shows L/L0 and C/C0 live.
# --- cell: cp6_legend ---
mo.md(
    r"""**Reading the dials:** $L$ = average distance — how many steps apart a
typical pair is. $C$ = clustering — how often two of your friends know each
other. $L_0$ and $C_0$ are those same numbers for the untouched ring
($p=0$), so $L/L_0 = 1$ means "unchanged" and $L/L_0 = 0.2$ means distances
shrank to a fifth."""
)
# --- cell: cp6_p ---
cp6_p = mo.ui.slider(
    steps=[0.0, 0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1.0],
    value=0.0,
    label="rewiring probability p",
)
cp6_p
# --- cell: cp6_ws_fig ---
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
    mo.md(f"**p = {_p} &nbsp;&nbsp; distance L/L₀ = {_Lr:.2f} &nbsp;&nbsp; clustering C/C₀ = {_Cr:.2f}**"),
    netviz(_ringe + _short, highlight=_short, layout=_pos60, width=820, height=820),
])
