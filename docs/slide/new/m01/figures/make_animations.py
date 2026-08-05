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
    ACCENT,
    ACCENT2,
    ACCENT3,
    CAMPUS_EDGES,
    CAMPUS_POS,
    EDGE_W,
    INK,
    MUTED,
    NODE_R,
    OUT,
    PANEL,
    RULE,
    _assert_fits_container,
    _finalize,
    draw_matrix,
    graph5_adjacency,
)

from io import BytesIO  # noqa: E402

from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402
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


# ---------------------------------------------------------------------------
# CSR construction (Part Seven follow-up, "Store only the nonzeros")
# ---------------------------------------------------------------------------
# The lecturer's own framing (round-13 review): the static build is well composed, but he
# wants to press a button / step a slider through the ORDERING structure while he talks --
# the point of CSR is that one row of the matrix becomes one CONTIGUOUS slice of indices/
# data, in scan order, and that only reads as a sequence if it happens in front of the room
# rather than sitting fully built on arrival. Marp restricts scripting (see module docstring
# above), so a slider isn't reachable -- this is the same "loop instead of interact" answer
# already shipped for Walk/Trail/Path, applied to the construction _fig_csr draws statically.
#
# Geometry, palette and the row-drawing convention are duplicated from make_figures._fig_csr
# rather than imported, on purpose: that function's fontsizes/margins are tuned against ITS
# OWN containment assertions for a figure that is always fully built, and re-deriving them
# per revealed-length here would be re-litigating a fight already won. CSR_VALUE_FS etc.
# below are the same numbers _fig_csr landed on -- if that figure's sizing changes, re-check
# these too (there's no shared constant precisely because fs()-scaling and containment don't
# commute the same way for a row of length 2 as for one of length 12; see _fig_csr's own W/
# VALUE_FS notes for why fixed points, not fs(), are used here as well).
CSR_W = 9.6
CSR_VALUE_FS, CSR_ROWLABEL_FS = 20.8, 21.2
CSR_MATRIX_FS = 23.5
CSR_FPS = 8
CSR_ENTRY_FRAMES = 5      # frames each newly-revealed (indices, data) pair holds before the next
CSR_BOUNDARY_FRAMES = 9   # extra hold once a row's indptr boundary + connectors land
CSR_INTRO_FRAMES = 6      # frames at the very start: matrix shown, nothing scanned yet
CSR_FINAL_FRAMES = 20     # hold on the fully-built figure before the loop restarts


def _csr_data():
    # Same graph, same construction loop as make_figures._fig_csr -- kept in lockstep by
    # eye (both are five lines) rather than imported, since importing a helper out of a
    # function-local scope would mean reaching into _fig_csr's internals from outside.
    adj = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 4], 3: [1, 4], 4: [2, 3]}
    data, indices, indptr = [], [], [0]
    for i in range(5):
        for j in adj[i]:
            data.append(1)
            indices.append(j)
        indptr.append(len(data))
    return indptr, indices, data


def _csr_row(axR, y, values, label, highlight_range=None):
    """Draw only `values` (already the revealed slice, not the full array) -- the reveal
    state IS the row's length, so growing the array is just passing a longer slice."""
    cells = []
    for i, v in enumerate(values):
        fc = ACCENT3 if highlight_range and highlight_range[0] <= i < highlight_range[1] else PANEL
        box = FancyBboxPatch((i - 0.5, y - 0.34), 1.0, 0.68,
                              boxstyle="round,pad=0.02,rounding_size=0.1",
                              facecolor=fc, edgecolor=RULE, linewidth=1.0, zorder=2)
        axR.add_patch(box)
        t = axR.text(i, y, str(v), ha="center", va="center", fontsize=CSR_VALUE_FS, color=INK, zorder=3)
        cells.append((t, box))
    axR.text(-0.85, y, label, ha="right", va="center", fontsize=CSR_ROWLABEL_FS, color=ACCENT,
              fontweight="bold", zorder=3)
    # Same containment check _fig_csr's row() closure runs -- the round this animation was
    # built in is the one where a bare "fits inside" check shipped "10"/"12" merged into
    # "1012"; every frame here grows the same two-digit values into the same boxes, so it
    # gets the same assertion, not a pass on the assumption that copying working numbers
    # is enough.
    renderer = _finalize(axR)
    for t, box in cells:
        _assert_fits_container(renderer, t, box, f"csr-anim row {label!r} value {t.get_text()!r}",
                                margin_frac=0.10)


def _csr_connectors(axR, indptr, row_i, y_indptr, y_row2, y_row3):
    """indptr[row_i] and indptr[row_i+1] bracket row_i's slice -- same connector geometry
    as _fig_csr's (hand-placed there for row 1 only; generalised here to any row so the
    animation can show it for whichever row just finished)."""
    lo, hi = indptr[row_i], indptr[row_i + 1]
    for pos, xb in zip((row_i, row_i + 1), (lo - 0.5, hi - 0.5)):
        axR.add_patch(FancyArrowPatch((pos, y_indptr - 0.32), (xb, y_row2 + 0.32),
                                       arrowstyle="-", color=ACCENT3, linewidth=2.2, zorder=1))
        axR.plot([xb, xb], [y_row2 - 0.32, y_row3 - 0.32], color=ACCENT3, linewidth=2.0,
                  linestyle=(0, (4, 3)), zorder=1)


def _csr_frame_sequence(indptr, data):
    """(n_revealed, matrix row to highlight, row whose connectors to draw or None) per
    frame. One pass, row 0 to row 4, entries revealed one at a time within each row, then
    a hold on that row's indptr boundary + connectors before moving to the next row."""
    row_bounds = list(zip(indptr, indptr[1:]))
    seq = [(0, 0, None)] * CSR_INTRO_FRAMES
    for i, (lo, hi) in enumerate(row_bounds):
        for p in range(lo + 1, hi + 1):
            seq += [(p, i, None)] * CSR_ENTRY_FRAMES
        seq += [(hi, i, i)] * CSR_BOUNDARY_FRAMES
    # Final hold shows row 1's connectors, not row 4's -- row 1 is the worked example the
    # static csr-build.png/csr-payoff.png use on the slides right after this animation, so
    # the frame the loop rests on is the same one the deck shows next, not an arbitrary one.
    seq += [(len(data), 1, 1)] * CSR_FINAL_FRAMES
    return seq


def _draw_csr_frame(axA, axR, A, indptr, indices, data, n_revealed, highlight_row, connector_row):
    axA.clear()
    axR.clear()
    draw_matrix(axA, A, row_highlight=highlight_row, row_highlight_color=ACCENT3, cell_fs=CSR_MATRIX_FS)
    axA.tick_params(labeltop=False, labelleft=False, length=0)

    axR.set_xlim(-3.0, 11.5)
    axR.set_ylim(-0.6, 3.0)
    axR.set_axis_off()

    row_bounds = list(zip(indptr, indptr[1:]))
    n_rows_done = sum(1 for lo, hi in row_bounds if n_revealed >= hi)
    indptr_shown = indptr[: n_rows_done + 1]

    y_indptr, y_row2, y_row3 = 2.35, 1.3, 0.0
    hl_indptr = (connector_row, connector_row + 2) if connector_row is not None else None
    hl_slice = row_bounds[connector_row] if connector_row is not None else None
    _csr_row(axR, y_indptr, indptr_shown, "indptr", highlight_range=hl_indptr)
    _csr_row(axR, y_row2, indices[:n_revealed], "indices", highlight_range=hl_slice)
    _csr_row(axR, y_row3, data[:n_revealed], "data", highlight_range=hl_slice)

    if connector_row is not None:
        _csr_connectors(axR, indptr, connector_row, y_indptr, y_row2, y_row3)


def animate_csr_build():
    indptr, indices, data = _csr_data()
    A = graph5_adjacency()
    seq = _csr_frame_sequence(indptr, data)

    fig = plt.figure(figsize=(CSR_W, 5.0))
    fig.subplots_adjust(left=0.01, right=0.995, top=0.98, bottom=0.02)
    gs = fig.add_gridspec(1, 2, width_ratios=[0.72, 2.04], wspace=0.15)
    axA = fig.add_subplot(gs[0, 0])
    axR = fig.add_subplot(gs[0, 1])

    frames = []
    for n_revealed, highlight_row, connector_row in seq:
        _draw_csr_frame(axA, axR, A, indptr, indices, data, n_revealed, highlight_row, connector_row)
        buf = BytesIO()
        fig.savefig(buf, format="png", dpi=160, facecolor="white")
        buf.seek(0)
        frames.append(Image.open(buf).convert("RGB").convert("P", palette=Image.ADAPTIVE))
    plt.close(fig)

    path = OUT / "csr-build-anim.gif"
    frames[0].save(
        path, save_all=True, append_images=frames[1:], optimize=False,
        duration=int(1000 / CSR_FPS), loop=0, disposal=2,
    )
    print(f"wrote {path.name}  ({len(frames)} frames)")


if __name__ == "__main__":
    for name, stops in ROUTES.items():
        animate_route(name, stops)
    animate_csr_build()
    print("done")
