# Premade cells for cp4's reveal — one cable, three worlds.
# Switching the radio redraws the ring and updates the average distance.
# describe: A choice - no extra cable / short cable (2 apart) / long cable (opposite) - that redraws an 8-dot ring; the chosen cable is red and the title shows the average distance.
# --- cell: cp4_choice ---
cp4_choice = mo.ui.radio(
    options=["no extra cable", "short cable (2 apart)", "long cable (opposite)"],
    value="no extra cable",
    label="Where does your one cable go?",
)
cp4_choice
# --- cell: cp4_compare_fig ---
_G = nx.cycle_graph(8)
if cp4_choice.value == "short cable (2 apart)":
    _G.add_edge(0, 2)
elif cp4_choice.value == "long cable (opposite)":
    _G.add_edge(0, 4)
_pos = nx.circular_layout(_G)
_L = nx.average_shortest_path_length(_G)
_ring_edges = [e for e in _G.edges() if abs(e[0] - e[1]) in (1, 7)]
_extra_edges = [e for e in _G.edges() if abs(e[0] - e[1]) not in (1, 7)]

_fig, _ax = plt.subplots(figsize=(5, 4))
nx.draw_networkx_nodes(
    _G, _pos, ax=_ax, node_color="#60a5fa", node_size=900, edgecolors="black", linewidths=1
)
nx.draw_networkx_edges(_G, _pos, ax=_ax, edgelist=_ring_edges, width=2, edge_color="#94a3b8")
nx.draw_networkx_edges(_G, _pos, ax=_ax, edgelist=_extra_edges, width=3.5, edge_color="#e11d48")
nx.draw_networkx_labels(_G, _pos, ax=_ax, font_size=12, font_color="white", font_weight="bold")
_ax.set_title(f"Average distance: {_L:.2f}", fontsize=15)
_ax.axis("off")
_fig
