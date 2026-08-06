# Premade cells for cp4's reveal — one cable, three worlds.
# Switching the radio redraws the ring and updates the average distance.
# describe: A choice - no extra cable / short cable (2 apart) / long cable (opposite) - that redraws an 8-dot ring on a drag-able network widget; the chosen cable is a rust line and the title shows the average distance.
# --- cell: cp4_choice ---
cp4_choice = mo.ui.radio(
    options=["no extra cable", "short cable (2 apart)", "long cable (opposite)"],
    value="no extra cable",
    label="Compare three placements",
)
cp4_choice
# --- cell: cp4_compare_fig ---
_edges = [(i, (i + 1) % 8) for i in range(8)]
_extra = None
if cp4_choice.value == "short cable (2 apart)":
    _extra = (0, 2)
elif cp4_choice.value == "long cable (opposite)":
    _extra = (0, 4)
_G = nx.cycle_graph(8)
if _extra:
    _G.add_edge(*_extra)
    _edges.append(_extra)
_L = nx.average_shortest_path_length(_G)

mo.vstack([
    mo.md(
        f"**Average distance: {_L:.2f}**\n\n"
        "<span style='color:#6A6D75;font-size:13px'>The same 8-dot ring three "
        "times over. The **rust line is the one extra cable**; the number "
        "above is the average trip length over all 28 pairs, recomputed every "
        "time you switch. Flip between the three options and watch only that "
        "number: same ring, same single extra line, and the only thing that "
        "changed is where it was put.</span>"
    ),
    netviz(_edges, highlight=[_extra] if _extra else [], layout="circle"),
])
