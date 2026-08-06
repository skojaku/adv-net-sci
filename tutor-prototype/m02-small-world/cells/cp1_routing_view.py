# Premade cell for checkpoint cp1_routing — the letter-holder's view.
# Built only AFTER the student has answered the existence-vs-findability
# question: the picture shows the holder's blindness, which IS the answer,
# so it lands with the reveal, never before.
# describe: A drag-able network widget - twelve dots in a circle. The rust dot is whoever holds the letter right now, and the rust lines are the only friendships the holder can actually see, running to their amber friends. The navy dot on the far side is the Boston target. Every grey dot and grey line exists, but the holder cannot see who knows whom out there.
# --- cell: cp1_routing_fig ---
_edges = [
    (0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6),
    (6, 7), (7, 8), (8, 9), (9, 10), (10, 11), (11, 0),
    (0, 2), (3, 5), (7, 9),
]
_colors = {0: "#B4552D", 1: "#C98A2D", 2: "#C98A2D", 11: "#C98A2D", 6: "#35577F"}
mo.vstack([
    mo.md("**The letter-holder's view**"),
    mo.md(
        "<span style='color:#6A6D75;font-size:13px'>The **rust** dot is "
        "whoever holds the letter right now, and the **rust lines** are the "
        "only friendships they can actually see — the ones running to their "
        "own **amber** friends. The **navy** dot on the far side is the "
        "Boston target. Every **grey** dot and line exists, but the holder "
        "has no idea who out there knows whom: they pick ONE amber friend "
        "and hope. Dots are drag-able.</span>"
    ),
    netviz(
        _edges,
        highlight=[(0, 1), (0, 2), (0, 11)],
        node_colors={_n: _colors.get(_n, "#E4E6EA") for _n in range(12)},
    ),
])
