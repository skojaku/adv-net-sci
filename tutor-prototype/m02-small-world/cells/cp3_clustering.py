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
_colors = ["#B4552D" if _n == "A" else "#35577F" for _n in _G.nodes()]
nx.draw_networkx_nodes(
    _G, _pos, ax=_ax, node_color=_colors, node_size=1400, edgecolors="#24211C", linewidths=1
)
nx.draw_networkx_edges(_G, _pos, ax=_ax, edgelist=_spoke_edges, width=2, edge_color="#6B6459")
nx.draw_networkx_edges(_G, _pos, ax=_ax, edgelist=_friend_edges, width=3.5, edge_color="#C98A2D")
nx.draw_networkx_labels(_G, _pos, ax=_ax, font_size=14, font_color="#FBF7F0", font_weight="bold")
_ax.set_title("A and A's five friends — orange = friends who know each other", fontsize=12)
_ax.axis("off")
_fig
