# Premade cell for checkpoint cp3_clustering — A and A's five friends.
# Friendships among the friends (B-F, C-E) are highlighted.
# describe: A in the middle with five friends B, C, D, E, F; the two friendships among the friends (B-F and C-E) are drawn in orange.
# --- cell: cp3_fig ---
_G = nx.Graph()
_G.add_edges_from(
    [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "F"), ("B", "F"), ("C", "E")]
)
_pos = nx.circular_layout(_G)
_friend_edges = [("B", "F"), ("C", "E")]
_spoke_edges = [e for e in _G.edges() if "A" in e]

_fig, _ax = plt.subplots(figsize=(5, 4))
_colors = ["#e11d48" if _n == "A" else "#60a5fa" for _n in _G.nodes()]
nx.draw_networkx_nodes(
    _G, _pos, ax=_ax, node_color=_colors, node_size=1400, edgecolors="black", linewidths=1
)
nx.draw_networkx_edges(_G, _pos, ax=_ax, edgelist=_spoke_edges, width=2, edge_color="#94a3b8")
nx.draw_networkx_edges(_G, _pos, ax=_ax, edgelist=_friend_edges, width=3.5, edge_color="#f59e0b")
nx.draw_networkx_labels(_G, _pos, ax=_ax, font_size=14, font_color="white", font_weight="bold")
_ax.set_title("A and A's five friends — orange = friends who know each other", fontsize=12)
_ax.axis("off")
_fig
