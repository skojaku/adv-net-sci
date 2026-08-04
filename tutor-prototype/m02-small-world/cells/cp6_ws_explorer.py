# Premade cells for checkpoint cp6_watts_strogatz — the rewiring explorer.
# Insert AFTER the student commits a prediction, with
# done_signal="cp6_watts_strogatz" for the Done button.
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

_D = nx.connected_watts_strogatz_graph(60, 4, _p, seed=5) if _p > 0 else nx.watts_strogatz_graph(60, 4, 0)
_posd = nx.circular_layout(_D)
_ringe = [e for e in _D.edges() if min(abs(e[0] - e[1]), 60 - abs(e[0] - e[1])) <= 2]
_short = [e for e in _D.edges() if min(abs(e[0] - e[1]), 60 - abs(e[0] - e[1])) > 2]

_fig, _ax = plt.subplots(figsize=(6, 5))
nx.draw_networkx_nodes(_D, _posd, ax=_ax, node_color="#cbd5e1", node_size=60, edgecolors="none")
nx.draw_networkx_edges(_D, _posd, ax=_ax, edgelist=_ringe, width=1, edge_color="#cbd5e1")
nx.draw_networkx_edges(_D, _posd, ax=_ax, edgelist=_short, width=1.8, edge_color="#e11d48")
_ax.set_title(
    f"p = {_p}    distance L/L₀ = {_Lr:.2f}    clustering C/C₀ = {_Cr:.2f}",
    fontsize=13,
)
_ax.axis("off")
_fig
