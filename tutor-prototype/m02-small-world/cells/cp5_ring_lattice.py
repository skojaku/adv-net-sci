# Premade cells for checkpoint cp5_ring_formula — the ring-lattice degree
# explorer. Lets the student check their by-hand triangle count against the
# picture: k=2 highlights nothing (no triangles possible); k=4 highlights
# exactly 3 of the 6 possible friend-pairs; k=6 highlights 9 of 15.
# describe: A 12-dot ring on a drag-able network widget with a friend-count slider k (2, 4, or 6); node 0's k nearest neighbors light up amber, and any friendship already existing between two of those neighbors is drawn as a rust line; the caption shows the live-computed clustering C for node 0.
# --- cell: cp5_ring_k ---
cp5_ring_k = mo.ui.slider(steps=[2, 4, 6], value=2, label="k (friends per person)")
cp5_ring_k
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
_possible = _k * (_k - 1) // 2
_Ci = len(_friend_pairs) / _possible if _possible else 0.0

_node_colors = {0: "#B4552D", **{_f: "#C98A2D" for _f in _friends}}
mo.vstack([
    mo.md(
        f"**Node 0 has {_k} friends. Friendships already among them: "
        f"{len(_friend_pairs)} of {_possible} possible → C₀ = {_Ci:.2f}**"
    ),
    netviz(_edges, highlight=_friend_pairs, node_colors=_node_colors, layout=_pos),
])
