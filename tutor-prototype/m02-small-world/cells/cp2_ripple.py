# Premade cells for checkpoint cp2_distance — the "wave from A" explorer.
# --- cell: cp2_steps ---
cp2_steps = mo.ui.slider(0, 3, value=0, step=1, label="steps from A")
cp2_steps
# --- cell: cp2_ripple_fig ---
_G = nx.Graph()
_G.add_edges_from([("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D")])
_pos = nx.circular_layout(_G)

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

_colors = [
    "#e11d48" if _n == "A" else ("#f59e0b" if _n in _reached else "#cbd5e1")
    for _n in _G.nodes()
]
_fig, _ax = plt.subplots(figsize=(5, 4))
nx.draw_networkx_nodes(
    _G, _pos, ax=_ax, node_color=_colors, node_size=1400, edgecolors="black", linewidths=1
)
nx.draw_networkx_edges(_G, _pos, ax=_ax, width=2, edge_color="#94a3b8")
nx.draw_networkx_labels(_G, _pos, ax=_ax, font_size=14, font_color="white", font_weight="bold")
_ax.set_title(f"Wave from A — {cp2_steps.value} step(s)", fontsize=15)
_ax.axis("off")
_fig
