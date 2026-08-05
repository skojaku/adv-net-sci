# Premade cell for cp2's reveal — the six pairs, visually.
# Insert AFTER the student has produced both answers (never before).
# describe: An Altair bar chart, one bar per pair (A-B, A-C, A-D, B-C, B-D, C-D), bar length is the shortest-path distance (all 1 except A-D which is 2, shown in rust); hovering a bar shows its exact distance. Title shows the average 7/6 = about 1.17.
# --- cell: cp2_pairs_fig ---
_pairs = [("A", "B", 1), ("A", "C", 1), ("A", "D", 2), ("B", "C", 1), ("B", "D", 1), ("C", "D", 1)]
_df = pd.DataFrame(_pairs, columns=["u", "v", "distance"])
_df["pair"] = _df["u"] + "–" + _df["v"]
_df["highlight"] = _df["distance"] > 1

_fig = alt.Chart(_df).mark_bar(size=22, cornerRadiusEnd=4).encode(
    y=alt.Y("pair:N", sort=_df["pair"].tolist(), title=None),
    x=alt.X("distance:Q", title="shortest-path distance", scale=alt.Scale(domain=[0, 2.4])),
    color=alt.condition("datum.highlight", alt.value("#B4552D"), alt.value("#35577F")),
    tooltip=["pair", "distance"],
).properties(
    title="All 6 pairs, distance — average 7/6 ≈ 1.17",
    height=220,
)
mo.vstack([
    _fig,
    mo.md(
        "<span style='color:#6A6D75;font-size:13px'>One bar per pair of "
        "people — with four people there are exactly six pairs, and every "
        "pair gets counted once. Bar length is that pair's distance, so a "
        "one-step bar means they are directly connected; the **rust bar is "
        "the only pair that needs a detour**. Average path length is just "
        "the mean of these six bars — the single number in the title.</span>"
    ),
])
