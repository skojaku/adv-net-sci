# Premade cell for checkpoint cp3_global_clustering — the two triplet
# shapes, mirroring the lecture slide's closed/open triplet figure in the
# notebook theme. Built only AFTER the student has named the closed shape
# themselves: the caption labels both shapes outright.
# describe: A drag-able network widget with two separate three-dot groups side by side - on the left P, Q, R with all three lines drawn in rust (a closed triplet, better known as a triangle), on the right X, Y, Z where X links to Y and to Z but the Y-Z line is missing (an open triplet, named by its middle person X).
# --- cell: cp3_triplets_fig ---
_edges = [("P", "Q"), ("Q", "R"), ("R", "P"), ("X", "Y"), ("X", "Z")]
mo.vstack([
    mo.md("**Closed triplet (left) — open triplet (right)**"),
    mo.md(
        "<span style='color:#6A6D75;font-size:13px'>Two trios. Left: P, Q "
        "and R, with **all three friendships there (rust)** — a **closed** "
        "triplet, better known as a triangle. Right: X knows Y and Z, but Y "
        "and Z never met — still a triplet, just **open**: one line short "
        "of a triangle. A triplet is named by its middle person — on the "
        "right that is X; in a triangle every corner takes a turn in the "
        "middle, which is why one triangle shows up three times in a "
        "triplet count. Dots are drag-able.</span>"
    ),
    netviz(
        _edges,
        highlight=[("P", "Q"), ("Q", "R"), ("R", "P")],
        layout={
            "P": (0.25, 0.15), "Q": (0.08, 0.80), "R": (0.42, 0.80),
            "X": (0.75, 0.15), "Y": (0.58, 0.80), "Z": (0.92, 0.80),
        },
    ),
])
