# Premade cell for cp2's reveal — the six pairs, visually.
# Insert AFTER the student has produced both answers (never before).
# describe: Six pairs of circles stacked vertically - A-B, A-C, A-D, B-C, B-D, C-D - each pair joined by a line with its shortest-path distance on top (all 1, except A-D which is 2, shown in rust-red); the title shows the average 7/6 = about 1.17.
# --- cell: cp2_pairs_fig ---
_pairs = [("A", "B", 1), ("A", "C", 1), ("A", "D", 2), ("B", "C", 1), ("B", "D", 1), ("C", "D", 1)]
_fig, _ax = plt.subplots(figsize=(4.5, 5.5))
for _i, (_u, _v, _d) in enumerate(_pairs):
    _y = len(_pairs) - _i
    _hl = _d > 1
    _node_color = "#B4552D" if _hl else "#35577F"
    _ax.plot([1, 3], [_y, _y], color="#6A6D75", lw=2, zorder=1)
    for _x, _lab in ((1, _u), (3, _v)):
        _ax.scatter([_x], [_y], s=950, c=_node_color, edgecolors="#1D1E21", zorder=2)
        _ax.text(_x, _y, _lab, ha="center", va="center", color="white",
                 fontsize=13, fontweight="bold", zorder=3)
    _ax.text(2, _y + 0.16, str(_d), ha="center", va="bottom", fontsize=15,
             fontweight="bold", color="#B4552D" if _hl else "#35373C")
_ax.set_xlim(0.3, 3.7)
_ax.set_ylim(0.3, len(_pairs) + 0.9)
_ax.set_title("All 6 pairs, distance on top — average 7/6 ≈ 1.17", fontsize=12)
_ax.axis("off")
_fig
