# Premade cell for checkpoint cp3_clustering — A and A's five friends.
# Friendships among the friends (B-F, C-E) are highlighted in rust.
# describe: A drag-able network widget - A in the middle (rust) connected to five friends B, C, D, E, F; the two friendships among the friends (B-F and C-E) are drawn as rust lines.
# --- cell: cp3_fig ---
_edges = [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "F"), ("B", "F"), ("C", "E")]
_friend_edges = [("B", "F"), ("C", "E")]
mo.vstack([
    mo.md("**A and A's five friends — rust lines = a friendship between two of A's friends**"),
    netviz(_edges, highlight=_friend_edges, node_colors={"A": "#B4552D"}),
])
