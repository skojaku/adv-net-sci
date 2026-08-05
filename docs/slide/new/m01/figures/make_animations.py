#!/usr/bin/env python3
"""Animated route figures, as looping GIFs.

Why GIF. The lecture is given from Marp's HTML output, so the deck should get
its density from motion rather than from more text on the slide. Marp's HTML
sanitiser strips inline `<svg>` (and `--html` does not get it through either),
and the module README already records that an `<img>` pointing at an `.svg`
tends to render blank inside Marp's own `foreignObject`. A GIF has neither
problem: Marp emits `<img src="figures/x.gif">` by relative path and the browser
animates it. Static export shows a frame, which is fine.

Kept separate from make_figures.py so the two can be worked on independently;
the geometry and palette are imported from there so they cannot drift.

    python3 figures/make_animations.py
"""

import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from matplotlib.animation import PillowWriter  # noqa: E402

sys.path.insert(0, str(Path(__file__).resolve().parent))
from make_figures import (  # noqa: E402
    ACCENT2,
    CAMPUS_EDGES,
    CAMPUS_POS,
    EDGE_W,
    INK,
    MUTED,
    NODE_R,
    OUT,
)

from io import BytesIO  # noqa: E402

from PIL import Image  # noqa: E402

FPS = 14
SECONDS_PER_EDGE = 0.85
HOLD_SECONDS = 1.2      # pause on the completed route before looping
DPI = 200

# The routes the vocabulary slides teach. Each is a sequence of stops; the
# animation walks it edge by edge so students see the rule being obeyed (or, for
# the walk, broken) rather than reading it.
ROUTES = {
    # A walk may reuse an edge: Cafe-Gym is crossed twice, there and back.
    "walk": ["Dorm", "Cafe", "Gym", "Cafe", "Lib"],
    # A trail may revisit a node but never an edge: Gym appears twice.
    "trail": ["Lib", "Gym", "Dorm", "Cafe", "Gym"],
    # A path repeats nothing.
    "path": ["Lib", "Cafe", "Dorm", "Gym"],
}


def _fit_label(ax, text, radius, start_pt=20.0):
    """Shrink a node label until it fits inside its disc.

    The static figures hit this too: "Dorm" at the deck's normal label size
    overflows a node and renders as "or". Measuring is the only reliable way,
    since the answer depends on the word, the font and the figure's scale.
    """
    fig = ax.figure
    fig.canvas.draw()
    # Disc diameter in display pixels, with a little interior margin.
    p0 = ax.transData.transform((0, 0))
    p1 = ax.transData.transform((radius, 0))
    budget = 2 * abs(p1[0] - p0[0]) * 0.82
    size = start_pt
    while size > 5:
        text.set_fontsize(size)
        if text.get_window_extent(fig.canvas.get_renderer()).width <= budget:
            return size
        size -= 0.5
    return size


def _draw_base(ax):
    """The campus graph itself, in the same styling the static figures use."""
    for u, v in CAMPUS_EDGES:
        ax.plot(
            [CAMPUS_POS[u][0], CAMPUS_POS[v][0]],
            [CAMPUS_POS[u][1], CAMPUS_POS[v][1]],
            color=MUTED, linewidth=EDGE_W, zorder=1, solid_capstyle="round",
        )
    for name, (x, y) in CAMPUS_POS.items():
        ax.add_patch(plt.Circle((x, y), NODE_R, facecolor=INK, edgecolor="none", zorder=3))
        t = ax.text(x, y, name, ha="center", va="center", color="white", zorder=4)
        _fit_label(ax, t, NODE_R)


def _route_points(stops, samples_per_edge=26):
    """Dense points along the route, so the stroke can grow smoothly."""
    xs, ys = [], []
    for a, b in zip(stops, stops[1:]):
        (x0, y0), (x1, y1) = CAMPUS_POS[a], CAMPUS_POS[b]
        t = np.linspace(0, 1, samples_per_edge)
        xs += list(x0 + (x1 - x0) * t)
        ys += list(y0 + (y1 - y0) * t)
    return np.array(xs), np.array(ys)


def animate_route(name, stops):
    xs, ys = _route_points(stops)
    n_edges = len(stops) - 1
    draw_frames = int(FPS * SECONDS_PER_EDGE * n_edges)
    hold_frames = int(FPS * HOLD_SECONDS)

    fig, ax = plt.subplots(figsize=(4.4, 4.4))
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-0.45, 1.45)
    ax.set_aspect("equal")
    ax.set_axis_off()
    _draw_base(ax)

    # The route is drawn over the graph; the moving head marks where you are.
    route, = ax.plot([], [], color=ACCENT2, linewidth=EDGE_W + 2.5, zorder=2,
                     solid_capstyle="round", solid_joinstyle="round")
    # Below the node discs (zorder 3), so it never sits on top of a node label.
    # Mid-edge it shows; on a node the disc covers it, which reads correctly.
    head = ax.scatter([], [], s=90, color=ACCENT2, zorder=2)

    # Assemble the GIF by hand rather than through PillowWriter. Its default
    # save path leaves frame-differencing artifacts -- the drawn route came out
    # visibly dashed where it should be solid -- and writing whole frames with
    # an explicit disposal avoids that at the cost of a larger file.
    frames = []
    for f in range(draw_frames + hold_frames):
        k = min(f, draw_frames) / draw_frames
        upto = max(2, int(k * len(xs)))
        route.set_data(xs[:upto], ys[:upto])
        head.set_offsets([[xs[upto - 1], ys[upto - 1]]])
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=DPI, facecolor="white")
        buf.seek(0)
        frames.append(Image.open(buf).convert("RGB").convert("P", palette=Image.ADAPTIVE))
    plt.close(fig)

    path = OUT / f"campus-{name}-anim.gif"
    frames[0].save(
        path, save_all=True, append_images=frames[1:], optimize=False,
        duration=int(1000 / FPS), loop=0, disposal=2,
    )
    print(f"wrote {path.name}  ({draw_frames + hold_frames} frames)")


if __name__ == "__main__":
    for name, stops in ROUTES.items():
        animate_route(name, stops)
    print("done")
