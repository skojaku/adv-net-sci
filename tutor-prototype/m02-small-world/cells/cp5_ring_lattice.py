# Premade cells for checkpoint cp5_ring_formula — the ring-lattice degree
# explorer. The student COUNTS the friend-pairs themselves; the widget must
# never print the count or C₀ (that is the checkpoint's own answer, and the
# k=6 fresh_variant's too). The "check my count" box only highlights the
# pairs after they have committed to a number — still no number shown.
# describe: A 12-dot ring on a drag-able network widget with a friend-count slider k (2, 4, or 6) and a "check my count" box; node 0 is rust, its k nearest neighbours are amber, and ticking the box highlights any friendship that already exists between two amber dots. No counts and no clustering value are shown — the student does the counting.
# --- cell: cp5_ring_controls ---
cp5_ring_k = mo.ui.slider(steps=[2, 4, 6], value=2, label="k (friends per person)")
cp5_ring_show = mo.ui.checkbox(
    value=False, label="check my count (highlight friendships among the amber dots)"
)
mo.hstack([cp5_ring_k, cp5_ring_show], justify="start", gap=2)
# --- cell: cp5_ring_fig ---
import math as _math

_N = 12
_k = cp5_ring_k.value
_half = _k // 2

# Explicit node order (0..N-1) for the circle layout — netviz's own
# "circle" string layout orders nodes by first appearance in the edge
# list, which a deduped/sorted edge set scrambles (a node can land in the
# wrong slot). Position every node ourselves instead.
_pos = {
    _i: (
        0.5 + 0.42 * _math.cos(2 * _math.pi * _i / _N - _math.pi / 2),
        0.5 + 0.42 * _math.sin(2 * _math.pi * _i / _N - _math.pi / 2),
    )
    for _i in range(_N)
}
_edges = [(_i, (_i + _d) % _N) for _i in range(_N) for _d in range(1, _half + 1)]
_edge_lookup = {tuple(sorted(e)) for e in _edges}

_friends = sorted({_d % _N for _d in range(1, _half + 1)} | {(-_d) % _N for _d in range(1, _half + 1)})
_friend_pairs = [
    (_friends[_i], _friends[_j])
    for _i in range(len(_friends))
    for _j in range(_i + 1, len(_friends))
    if tuple(sorted((_friends[_i], _friends[_j]))) in _edge_lookup
]
_node_colors = {0: "#B4552D", **{_f: "#C98A2D" for _f in _friends}}
_hl = _friend_pairs if cp5_ring_show.value else []
mo.vstack([
    mo.md(
        "**Node 0** is the rust dot; the **amber dots are its friends** "
        f"({_half} on each side). Every line is a friendship — the ones to "
        "count are the lines that join *two amber dots*."
    ),
    netviz(_edges, highlight=_hl, node_colors=_node_colors, layout=_pos),
])
