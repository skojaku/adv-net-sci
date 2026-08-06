# Premade cell for checkpoint cp3_clustering — A and A's five friends.
# The friendships among the friends are highlighted in rust; the student
# COUNTS them, so neither the describe line nor the caption may say how
# many there are (the describe line is what the tutor reads aloud).
# describe: A drag-able network widget - the DOT A sits in the middle and is coloured rust; its five friends B, C, D, E, F sit around it. The lines from A out to its friends are GREY. Only the lines running BETWEEN two of those friends are rust, for the student to find and count.
# --- cell: cp3_fig ---
_edges = [("A", "B"), ("A", "C"), ("A", "D"), ("A", "E"), ("A", "F"), ("B", "F"), ("C", "E")]
_friend_edges = [("B", "F"), ("C", "E")]
mo.vstack([
    mo.md(
        "**A and A's five friends**\n\n"
        "<span style='color:#6A6D75;font-size:13px'>**A** is the rust dot in "
        "the middle; B, C, D, E and F are its five friends. The grey lines "
        "from A are A's own friendships — ignore those. The **rust lines run "
        "between two of A's friends**: those are the ones that say "
        "\"my friends know each other\". Find them and count them yourself. "
        "Dots are drag-able if the picture gets tangled.</span>"
    ),
    netviz(_edges, highlight=_friend_edges, node_colors={"A": "#B4552D"}),
])
