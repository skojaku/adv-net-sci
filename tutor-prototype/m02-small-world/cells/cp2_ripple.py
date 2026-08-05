# Premade cells for checkpoint cp2_distance — the "wave from A" explorer.
# describe: A 4-person network - A, B, C, D - with a 'steps from A' slider (0-3); people reachable within that many steps light up amber, like a wave from A, on a drag-able network widget.
# --- cell: cp2_steps ---
cp2_steps = mo.ui.slider(0, 3, value=0, step=1, label="steps from A")
cp2_steps
# --- cell: cp2_ripple_fig ---
_edges = [("A", "B"), ("A", "C"), ("B", "C"), ("B", "D"), ("C", "D")]
_G = nx.Graph()
_G.add_edges_from(_edges)

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

_colors = {
    _n: ("#B4552D" if _n == "A" else ("#C98A2D" if _n in _reached else "#E4E6EA"))
    for _n in _G.nodes()
}
mo.vstack([
    mo.md(
        f"**Wave from A — {cp2_steps.value} step(s)**\n\n"
        "<span style='color:#6A6D75;font-size:13px'>Four people, five "
        "friendships. **A** is rust; **amber** dots are everyone A can reach "
        "in that many steps or fewer; **grey** dots are still out of range. "
        "Drag the slider up one notch at a time and watch who joins — the "
        "step at which someone first turns amber IS their distance from A. "
        "You can drag the dots too; moving them changes nothing but the "
        "picture.</span>"
    ),
    netviz(_edges, node_colors=_colors),
])
