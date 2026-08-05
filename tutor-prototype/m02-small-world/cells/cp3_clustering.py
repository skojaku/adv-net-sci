# Premade cell for checkpoint cp3_clustering — A and A's five friends.
# The friendships among the friends are highlighted in rust; the student
# COUNTS them, so neither the describe line nor the caption may say how
# many there are (the describe line is what the tutor reads aloud).
# describe: A drag-able network widget - A in the middle (rust) connected to five friends B, C, D, E, F; any friendship that already exists between two of those friends is drawn as a rust line, for the student to find and count.
# --- cell: cp3_fig ---
_edges = [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "F"), ("B", "F"), ("C", "E")]
_friend_edges = [("B", "F"), ("C", "E")]
mo.vstack([
    mo.md("**A and A's five friends — rust lines = a friendship between two of A's friends**"),
    netviz(_edges, highlight=_friend_edges, node_colors={"A": "#B4552D"}),
])
