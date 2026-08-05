#!/usr/bin/env python3
"""Generate Module 01 slide figures in the network-science theme palette.

Every figure obeys the review's global rules: uniform node size/fill unless a
slide explains the encoding, planar (crossing-free) layouts, legible-from-the-
back-row minimum sizes, and the fixed six-color palette below.
"""

import os
import re
import sys
from pathlib import Path

import matplotlib
# R7 fix (found chasing Blocker 3): force a headless, non-HiDPI backend BEFORE pyplot picks
# one on its own. On a Retina Mac, matplotlib's default interactive backend (here, macosx)
# silently reports fig.dpi as 400 -- double the 200 this whole file assumes throughout (see
# the dpi comment below) -- because it renders for a 2x-density display. save()/save_fixed()
# hardcode dpi=200 explicitly so they were never affected, but save_fit's OUTPUT dpi defaults
# to `measure_dpi = fig.dpi` when no `out_dpi` is given, so on this backend it silently saved
# at 400dpi instead of 200 -- exactly double, on every save_fit figure, with nothing about the
# figure's own content to blame. This is what made csr-memory.png's width backend-dependent
# rather than content-dependent (confirmed: forcing Agg here dropped an otherwise-identical
# render from 3858px to 1929px). Agg is also simply the right backend for a batch script with
# no display -- deterministic and portable across whatever machine runs `python3
# figures/make_figures.py`.
matplotlib.use("Agg")
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
from PIL import Image

OUT = Path(__file__).resolve().parent

ACCENT = "#3959A6"
ACCENT2 = "#B14434"
ACCENT3 = "#DAB167"
INK = "#000000"
MUTED = "#6b6b6b"
PANEL = "#f7f4f1"
RULE = "#dddddd"

plt.rcParams.update(
    {
        "font.family": "serif",
        "font.size": 14,
        "axes.edgecolor": RULE,
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        # R5 fix: every save*() in this file renders the final PNG at dpi=200 explicitly
        # (savefig(dpi=200) always re-renders independently of the figure's own dpi --
        # confirmed byte-identical output regardless of this setting), so that part was
        # never the bug. But `fig.dpi` ALSO governs every INTERMEDIATE fig.canvas.draw() /
        # get_window_extent() call the place_label/save_fit geometry helpers use to measure
        # real pixel positions -- and matplotlib's default (100) doesn't match the 200 those
        # helpers assume when converting between points, pixels, and inches. Left at the
        # default, that mismatch silently scaled every measurement by 2x (confirmed: it
        # produced a selfloop crop 1/4 the intended area). Setting the default here, once,
        # keeps every measurement self-consistent with what actually gets saved.
        "figure.dpi": 200,
    }
)

# R10 fix (FIXES_R10.md, Blocker 2 -- in-disc node labels measured 7-9px on 11 slides):
# every node in this deck renders at exactly NODE_DIAM_IN*dpi = 150px native, by construction
# (fit_node_scale always targets it -- see that function's own module note), REGARDLESS of
# which figure, its margin, or its `w:` -- so a label's on-slide size, as a FRACTION of the
# on-slide node diameter, is fixed by the ratio of LABEL_FS to NODE_DIAM_IN alone and is the
# SAME across every figure (both scale by the deck's one per-image downscale together, being
# pixels of the same raster). That ratio is what was wrong, not any one figure's own crop or
# `w:` -- so this is a single, deck-wide constant, not a per-figure tune. Measured directly
# (matplotlib serif, dpi=200): a capital letter's rendered ink-height is ~2.0px per pt. Target
# ink-height = 40% of the 150px native node diameter = 60px -> 60/2.0 = 30pt.
LABEL_FS = 30
TITLE_FS = 18
ANNOT_FS = 17
EDGE_W = 3.5

# ---------------------------------------------------------------------------
# on-slide text legibility (R12, "the one thing that has not landed")
# ---------------------------------------------------------------------------
# Round 10 fixed node-interior labels (LABEL_FS, above) by reasoning about their size as a
# FRACTION of the node they sit inside. That trick doesn't exist for a free-standing
# annotation ("start"/"end", "destroyed", a CSR array digit) -- there is no fixed anchor to
# take a ratio against, so nine rounds of hand-picked point sizes on those kept regressing:
# fixed on the named figure, reappeared on the next one nobody re-measured.
#
# What actually determines a free-standing label's on-slide size is now deterministic
# (FIXES_R12.md): the deck's CSS scales every figure PNG by
#   scale = min(container_px / file_w_px, MAX_FIG_H / file_h_px, 1.0)
# where container_px is 537px inside a `.cols` column or 1120px full-width (the `w:NNN`
# directive in the deck is INERT -- network-science.css sets `width: auto !important`), and
# a font rasterized at `render_dpi` lands on-slide at `fontsize_pt * (render_dpi/72) *
# scale`. Nothing here is measured by eye: `_assert_text_legible` computes it from the
# actual saved file and the actual deck markup, and runs from every save()/save_fit()/
# save_fixed() call, so a figure that ships text under the floor fails the BUILD, not a
# later review pass.
MAX_FIG_H = 380   # network-science.css: section .fig img { max-height } -- check_render.py
                  # derives the same cap independently; kept in sync since both read it off
                  # the theme, not off any one figure.
COL_W = 537       # <div class="cols"> column width -- confirmed via getComputedStyle in a
                  # real browser render (536.98px measured; check_render.py has the same
                  # number from the same measurement).
FULL_W = 1120     # full-width .fig container: content area 1280 - 2*80px theme padding.

# The floor itself: body prose is 30px (CSS), which measures 21px of actual cap/digit ink on
# the rendered slide -- nothing in a figure is allowed to read smaller than the prose next to
# it. This is the number FIXES_R12.md names directly; not a per-figure tune.
TEXT_LEGIBLE_PX = 21

# Tuning aid, not part of the normal build: plain `python3 figures/make_figures.py` still
# raises on the FIRST undersized label, same as every other assertion in this file. Setting
# MF_COLLECT_TEXT=1 instead collects every violation across the whole run and reports them
# together at the end -- needed because R12's fix touches "effectively all" figures
# (FIXES_R12.md's own words), and fixing them one crash-and-rerun at a time is exactly the
# per-label workflow that regressed twice already.
_COLLECT_TEXT_FAILURES = os.environ.get("MF_COLLECT_TEXT") == "1"
_TEXT_FAILURES = []

_DECK_PATH = OUT.parent / "m01-euler-tour.md"
_deck_containers_cache = None


def _deck_containers():
    """basename -> narrowest container (px) a figure is placed in, read straight from the
    deck (mirrors check_render.py's own slides_with_figures()) so the legibility check below
    uses the SAME container width the rendered slide actually will. A figure referenced from
    more than one slide takes the smallest container it appears in -- the worst-case scale it
    must still clear. A figure not (yet) referenced in the deck falls back to FULL_W, the
    more forgiving of the two, in _assert_text_legible.

    Cached at module scope: this file calls save()/save_fit()/save_fixed() ~60 times in one
    run, and the deck is ~30KB -- re-reading and re-parsing it that often is pure overhead
    for a file that never changes mid-run.
    """
    global _deck_containers_cache
    if _deck_containers_cache is None:
        out = {}
        if _DECK_PATH.exists():
            text = _DECK_PATH.read_text()
            # parts[0] is the YAML front matter; parts[1:] are the slides themselves, exactly
            # as check_render.py's slides_with_figures() splits them.
            for chunk in text.split("\n---\n")[1:]:
                for m in re.finditer(r"!\[[^\]]*\]\((figures/[^)]+)\)", chunk):
                    base = m.group(1).rsplit("/", 1)[-1]
                    container = COL_W if 'class="cols"' in chunk else FULL_W
                    out[base] = min(out.get(base, container), container)
        _deck_containers_cache = out
    return _deck_containers_cache


def _iter_rendered_text(fig):
    """Every Text artist that will actually appear in the saved PNG.

    NOT fig.findobj(mtext.Text): confirmed directly (against this exact codebase's own
    figures) that it also turns up stale Tick-label Text objects matplotlib caches
    internally -- e.g. a subplot's default (0.0, 0.2, ... 1.0) tick labels, generated by an
    intermediate fig.canvas.draw() (fit_node_scale calls one) while that axes still had its
    factory-default xlim=(0,1) from BEFORE its own set_xlim/clean() ran, then never
    discarded. Axes.set_axis_off() only makes the AXIS skip drawing its ticks at render time
    (checked once, at the axes level) -- it does not touch each cached Tick label's own
    get_visible(), so those ghosts still turn up with `visible=True` and a plausible-looking
    fontsize, and would otherwise fail the build over text nobody will ever see.

    Walking each axes' OWN artist lists instead sidesteps this entirely: `ax.texts` is
    exactly (and only) what ax.text()/ax.annotate() added to THIS axes, unambiguous by
    construction. Tick labels and the xaxis/yaxis .label Text (set_xlabel/set_ylabel) are
    part of Axis.draw(), which Axes.draw() skips outright when axison is False -- confirmed
    directly (a set_axis_off() axes with set_xlabel/set_xticklabels calls renders neither) --
    so those are only pulled in for an axes actually switched on, and tick labels are further
    filtered to the ones actually get_visible(). ax.title is NOT part of Axis.draw() -- it is
    always drawn regardless of axison (confirmed the same way: a set_axis_off() axes still
    renders its set_title() text) -- several figures in this file call clean(ax) BEFORE
    set_title(), so this is checked unconditionally, not gated behind axison like the rest.
    """
    for ax in fig.axes:
        yield from ax.texts
        if ax.title.get_text().strip():
            yield ax.title
        if not ax.axison:
            continue  # clean(ax)'d axes: no rendered ticks/axis-label to check
        for t in ax.get_xticklabels() + ax.get_yticklabels():
            if t.get_visible():
                yield t
        if ax.xaxis.label.get_text().strip():
            yield ax.xaxis.label
        if ax.yaxis.label.get_text().strip():
            yield ax.yaxis.label


def _assert_text_legible(fig, name, out_w_px, out_h_px, render_dpi):
    """Every piece of text in `fig` must land at >= TEXT_LEGIBLE_PX on the slide the deck
    actually places it on (FIXES_R12.md's one derived rule):

        scale       = min(container / out_w_px, MAX_FIG_H / out_h_px, 1.0)
        on_slide_px = fontsize_pt * (render_dpi / 72) * scale

    `out_w_px`/`out_h_px`: the SAVED FILE's own pixel size, read back off disk rather than
    recomputed from figsize*dpi -- save() and save_fit() both crop via bbox_inches (a tight
    bbox, or an explicit inches Bbox), which changes the final size in ways this function has
    no business re-deriving and risking a drift from what actually landed on disk.

    `render_dpi`: the dpi THIS save actually rasterized text at -- out_dpi for a save_fit
    that used one, otherwise the plain save dpi. NOT necessarily `fig.dpi`, which only
    describes the on-screen figure used for layout math, not what got written to the file
    (see TINY_OUT_DPI's own module note: a handful of figures are deliberately saved at a
    LOWER dpi than they were laid out at).

    `container`: looked up by filename in `_deck_containers()`, so a figure used inside a
    `.cols` column is held to the tighter 537px box, not the more forgiving 1120px full
    width, exactly like the slide it lands on.
    """
    container = _deck_containers().get(name, FULL_W)
    scale = min(container / out_w_px, MAX_FIG_H / out_h_px, 1.0)
    worst = None
    for t in _iter_rendered_text(fig):
        txt = t.get_text().strip()
        if not txt:
            continue
        fs_pt = t.get_fontsize()
        on_slide_px = fs_pt * (render_dpi / 72.0) * scale
        if worst is None or on_slide_px < worst[0]:
            worst = (on_slide_px, txt)
        if on_slide_px < TEXT_LEGIBLE_PX - 1e-6:
            msg = (
                f"{name}: text {txt!r} at {fs_pt}pt lands {on_slide_px:.1f}px on the slide "
                f"(container={container}px, file={out_w_px:.0f}x{out_h_px:.0f}px, "
                f"render_dpi={render_dpi:.1f}, scale={scale:.3f}) -- below the {TEXT_LEGIBLE_PX}"
                f"px floor. Raise this figure's fontsize or crop its canvas margin -- both "
                f"raise `scale`/the effective point size the same way."
            )
            if _COLLECT_TEXT_FAILURES:
                _TEXT_FAILURES.append(msg)
            else:
                raise AssertionError(msg)
    if worst is not None:
        print(f"  text-min {name}: {worst[0]:.1f}px on-slide ({worst[1]!r}, container={container}px)")


# Output widths range ~3in (selfloop) to ~11in (csr-build), but every PNG gets shrunk
# to roughly the same displayed width in the deck. A fixed point-size therefore reads
# ~4x larger in a narrow figure than in a wide one. `fs()` scales a base point-size by
# a figure's own width relative to this reference so apparent text size stays constant.
FONT_REF_WIDTH = 5.2


def fs(base_pt, width_in, ref=FONT_REF_WIDTH):
    return round(base_pt * width_in / ref, 1)


# ---------------------------------------------------------------------------
# R8 fix: nodes are Circle patches, not ax.scatter markers (FIXES_R8_CIRCLE.md)
# ---------------------------------------------------------------------------
# Six consecutive rounds failed the same defect class under three different-looking
# symptoms (self-loop legs that don't meet their node, arrowheads that don't arrive, rings
# drawn inside the disc they were meant to encircle) because every node in this file was an
# ax.scatter marker, whose `s` is an area in points^2 -- a SCREEN unit, decoupled from data
# coordinates. So a marker's radius *in the data-coordinate system every edge/annotation is
# computed in* depended on the axes' current xlim/ylim, and every figure in this deck has
# its own xlim/ylim -- so every boundary computation against a node was a guess, wrong by a
# different factor in every figure (measured: same scatter s=900 at figsize 4x4 has a data-
# unit radius of 0.0672 / 0.1344 / 0.2688 depending on whether xlim is (0,1) / (0,2) / (0,4)).
#
# A `Circle(center, r)` patch's radius is in DATA units and is invariant to xlim/ylim -- so
# NODE_R below is exact everywhere, by construction, with nothing left to guess.
NODE_R = 0.12  # data units -- the ONE node radius, used by every figure in this file.
               # Picked small enough to clear the tightest inter-node spacing anywhere in
               # the deck (the band/ladder figures, nodes 0.8 data units apart -- a NODE_R
               # any bigger than ~0.2 starts crowding those) while staying comfortably
               # visible against graph5/Konigsberg's ~1.0-1.4 unit spacing. The single value
               # is what makes every formula below ("edges stop at NODE_R from centre",
               # "rings are drawn at k*NODE_R") exact and figure-independent.

# Deck-wide rendered node diameter, in PHYSICAL inches -- picked to match the Konigsberg
# family's own current look (measured off konigsberg-blank.png before this fix: ~150px
# native at dpi=200, i.e. 0.75in) per FIXES_R8_CIRCLE.md's own instruction ("pick the target
# from the figures that already look right"). Every OTHER figure's node now renders at this
# exact physical size too, regardless of that figure's own data range -- see fit_node_scale.
NODE_DIAM_IN = 0.75

# R10 fix (FIXES_R10.md, "the one cause, one level further out"): NODE_DIAM_IN's own physical
# size only controls ON-SLIDE node size for figures the deck actually SCALES DOWN (via its
# fixed max-height:380px, or -- for a `.cols` slide -- whatever pixel width that column's
# grid track resolves to, which varies slide to slide and is NOT the `w:NNN` directive: this
# deck's theme sets `width: auto !important` on every figure image specifically to defeat
# that directive -- confirmed directly, by rendering a real copy of the deck with a figure's
# own `w:` changed from 520 to 50 and reading getComputedStyle: computed width was identical
# either way). A handful of figures (one or two bare nodes, nothing else) stay under BOTH of
# those caps even padded, so nothing ever scales them down -- they render at native 1:1
# resolution on whatever slide they land on, so the only way to hit the deck's on-slide
# node-diameter band (26-52px) for THESE figures is to make the node itself that size
# natively -- not by overriding fit_node_scale's target_in (which would leave every OTHER
# point-sized element -- LABEL_FS, ANNOT_FS, EDGE_W -- at its normal-figure size, badly out
# of proportion with a suddenly-tiny node), but via `save_fit`'s `out_dpi`: it renders the
# SAME physical-inch crop (measured, like everywhere else, at this module's 200dpi) at a
# LOWER final resolution, which rescales EVERY element uniformly (node, text, line widths are
# all defined in physical points/inches, so one dpi change shrinks all of them together,
# preserving every proportion the deck-wide constants already establish). 38px target
# diameter, at NODE_DIAM_IN=0.75in -> the dpi at which 0.75in rasterizes to exactly 38px.
TINY_OUT_DPI = 38 / NODE_DIAM_IN


def data_units_per_point(ax):
    """(dx, dy): data units spanned by one point (1/72 in) along each axis, at ax's
    CURRENT transform. Valid only once xlim/ylim/aspect are at their final values."""
    _finalize(ax)
    inv = ax.transData.inverted()
    ppp = ax.figure.dpi / 72.0  # display px per point
    x0, y0 = inv.transform((0, 0))
    x1, _ = inv.transform((ppp, 0))
    _, y1 = inv.transform((0, ppp))
    return abs(x1 - x0), abs(y1 - y0)


def node_radius_pt(ax, r=NODE_R):
    """`r` (DATA units, default NODE_R) converted EXACTLY to points at `ax`'s current
    transform -- for APIs that only take points (FancyArrowPatch's shrinkA/shrinkB,
    circle_obstacle's r_pt). Not a guess: data_units_per_point is a plain unit conversion at
    the real, current transform, unlike the deleted node_s()/node_radius_data() (which
    estimated a *scatter marker's* radius, the thing this whole fix removes)."""
    dx, dy = data_units_per_point(ax)
    return r / ((dx + dy) / 2)


def fit_node_scale(fig, ax, r=NODE_R, target_in=None):
    """Rescale `fig` IN PLACE (via set_size_inches -- preserving whatever aspect ratio or
    multi-panel gridspec proportions it already has) so that a Circle of DATA-unit radius
    `r`, measured against `ax`'s CURRENT xlim/ylim/aspect, renders at exactly `target_in`
    (default NODE_DIAM_IN) physical inches in diameter -- the deck-wide node size, point 2
    of FIXES_R8_CIRCLE.md.

    Measured against the real renderer (a probe conversion via data_units_per_point), not
    computed from subplot-margin/width_ratio/letterboxing algebra -- those differ figure to
    figure (single panel vs. gridspec vs. custom width_ratios all use a different fraction
    of the figure for their axes box), and re-deriving that fraction by hand per figure is
    exactly the kind of guess this whole fix removes. This works identically whether `ax` is
    the only axes in `fig` or one panel of several.

    Call once every axes that will carry a node -- `ax` -- has its xlim/ylim/aspect at their
    FINAL values (nothing needs to be drawn on it yet: a Circle's rendered size depends only
    on the transform, not on what's drawn), and BEFORE any width-keyed styling (fs(), mostly)
    that assumes the figure's final physical size. Returns the figure's new width in inches,
    for exactly that purpose -- e.g. `W = fit_node_scale(fig, ax)`.
    """
    fig.canvas.draw()
    dx, dy = data_units_per_point(ax)
    cur_diam_in = 2 * r / (72.0 * ((dx + dy) / 2))
    target = NODE_DIAM_IN if target_in is None else target_in
    factor = target / cur_diam_in
    w, h = fig.get_size_inches()
    fig.set_size_inches(w * factor, h * factor)
    fig.canvas.draw()
    return fig.get_size_inches()[0]


NODE_GID = "deck-node"  # tags every node Circle patch, so save()/save_fit()/save_fixed()
                         # can find and verify them without every caller asserting by hand.


def draw_node(ax, center, color=INK, r=NODE_R, zorder=3):
    """THE canonical node marker -- a Circle patch of DATA-unit radius `r` (default
    NODE_R), never an ax.scatter marker (see the module note above `NODE_R`)."""
    c = mpatches.Circle(center, r, facecolor=color, edgecolor="none", zorder=zorder)
    c.set_gid(NODE_GID)
    ax.add_patch(c)
    return c


def draw_nodes(ax, centers, colors=None, r=NODE_R, zorder=3):
    """Draw one draw_node() per entry of `centers`.

    `centers`: a list of (x, y), or a dict name -> (x, y).
    `colors`: a list matching `centers`' iteration order, a dict matching `centers`' keys
    (only meaningful if `centers` is a dict), a single colour applied to every node, or None
    (defaults every node to INK).
    """
    if isinstance(centers, dict):
        keys = list(centers.keys())
        pts = [centers[k] for k in keys]
        cs = [colors.get(k, INK) for k in keys] if isinstance(colors, dict) else colors
    else:
        pts = list(centers)
        cs = colors
    if cs is None:
        cs = [INK] * len(pts)
    elif isinstance(cs, str):
        cs = [cs] * len(pts)
    return [draw_node(ax, p, color=c, r=r, zorder=zorder) for p, c in zip(pts, cs)]


def draw_ring(ax, center, k=1.6, r=NODE_R, color=ACCENT2, lw=None, zorder=5, node_obstacles=(),
              edge_obstacles=(), name="ring"):
    """A ring meant to ENCLOSE a node (e.g. "this node was revisited") -- drawn at `k * r`,
    k > 1 asserted, so a ring can never again be drawn smaller than the disc it encircles
    (FIXES_R8_CIRCLE.md point 3; the concrete bug that motivated this: a ring hand-radius'd
    against a stale/guessed node size landed INSIDE the disc it was meant to surround)."""
    assert k > 1.0, (
        f"draw_ring: {name!r} k={k} must be > 1 -- a ring must enclose its node, not sit "
        f"inside or flush with its rim."
    )
    pts = _circle_points(center, k * r)
    return draw_annotation_stroke(ax, pts, color=color, lw=lw, zorder=zorder,
                                   node_obstacles=node_obstacles, edge_obstacles=edge_obstacles,
                                   name=name)


def _arrow_tip_gap_pt(ax, mutation_scale, lw, rad=0.0, arrowstyle="-|>"):
    """Measured (not guessed) gap, in points, between a FancyArrowPatch's rendered TIP and
    its nominal (shrinkA=shrinkB=0) endpoint -- draws a disposable probe patch on `ax`,
    measures where the real renderer actually puts the tip relative to the endpoint it was
    given, and removes it. FIXES_R8_CIRCLE.md point 3 / the R4-R5 history in
    draw_arrow_edge's own docstring: this gap is real (matplotlib's arrowhead geometry does
    not put the tip exactly at the path's nominal endpoint) and previous rounds either
    ignored it or hand-guessed a correction that drifted; self-calibrating it against the
    actual renderer, every time, is what makes draw_arrow_edge's shrink exact instead of a
    guess that can go stale under a matplotlib version bump.

    `lw` matters: measured directly (sweeping linewidth 0-8pt), the gap is proportional to
    the stroke's OWN linewidth (~1.12pt of gap per 1pt of linewidth -- the head's stroked
    outline extends past its mathematical apex by an amount set by the miter join, which
    scales with linewidth), not a fixed constant independent of it. The probe must be drawn
    at the SAME `lw` the real arrow will use, or this calibration is measuring the wrong
    patch (the R8 bug this shipped with: linewidth=1's ~1.12pt gap doesn't hold at
    linewidth=4.2, off by over 3pt -- exactly the campus arrows' own stroke weight).
    """
    a, b = (0.0, 0.0), (1.0, 0.0)
    probe = FancyArrowPatch(a, b, arrowstyle=arrowstyle, mutation_scale=mutation_scale,
                             shrinkA=0, shrinkB=0, linewidth=lw, connectionstyle=f"arc3,rad={rad}")
    ax.add_patch(probe)
    ax.figure.canvas.draw()
    verts_data = probe.get_path().vertices
    d = np.hypot(verts_data[:, 0] - b[0], verts_data[:, 1] - b[1])
    tip = verts_data[np.argmin(d)]
    gap_data = np.hypot(tip[0] - b[0], tip[1] - b[1])
    probe.remove()
    dx, dy = data_units_per_point(ax)
    return gap_data / ((dx + dy) / 2)


def draw_arrow_edge(ax, u, v, mutation_scale, rad=0.0, color=MUTED, lw=EDGE_W, zorder=1,
                     r=NODE_R, name="arrow-edge"):
    """A directed edge from `u` to `v` (data coords) whose ARROWHEAD TIP lands, by
    construction and verified against the real renderer, exactly on `v`'s rim (distance `r`
    from `v`'s centre) -- FIXES_R8_CIRCLE.md point 3 ("arrowheads inset by exactly NODE_R
    plus the head length ... without a hand-picked standoff"). shrinkA/shrinkB are derived
    from `node_radius_pt` MINUS the measured tip gap (`_arrow_tip_gap_pt`, at this SAME
    `lw`) so the head's true tip -- not the path's nominal, pre-head endpoint -- reaches the
    rim; this is what replaces the R4/R5 hand-picked `NODE_RADIUS_PT_REF - 4` constant tuned
    by eye against one figure's own edges.
    """
    gap_pt = _arrow_tip_gap_pt(ax, mutation_scale, lw, rad=rad)
    shrink = node_radius_pt(ax, r) - gap_pt
    patch = FancyArrowPatch(u, v, connectionstyle=f"arc3,rad={rad}", arrowstyle="-|>",
                             mutation_scale=mutation_scale, shrinkA=shrink, shrinkB=shrink,
                             color=color, linewidth=lw, zorder=zorder)
    ax.add_patch(patch)
    ax.figure.canvas.draw()
    verts_data = patch.get_path().vertices
    d_to_v = np.hypot(verts_data[:, 0] - v[0], verts_data[:, 1] - v[1])
    tip = verts_data[np.argmin(d_to_v)]
    dist = np.hypot(tip[0] - v[0], tip[1] - v[1])
    dx, dy = data_units_per_point(ax)
    eps = 1.5 * ((dx + dy) / 2)  # ~1.5pt tolerance, in data units
    assert abs(dist - r) < eps, (
        f"draw_arrow_edge: {name!r} tip lands {dist:.4f} data units from {v} (target "
        f"{r:.4f}) -- off by {(dist - r) / ((dx + dy) / 2):+.2f}pt, outside the 1.5pt "
        f"tolerance. The arrowhead does not arrive."
    )
    return patch


def _assert_node_diameters(fig, name, tol=0.06, expected_diam_in=None):
    """Point 2 of FIXES_R8_CIRCLE.md: every node in `fig`, measured against the real
    renderer, must be within `tol` of the deck-wide NODE_DIAM_IN target at this figure's own
    dpi -- run from every save*() below, against every Circle draw_node()/draw_nodes() ever
    tagged NODE_GID, so a figure that skipped fit_node_scale() fails the build instead of
    shipping an inconsistent node size for a human to catch by eye.

    `expected_diam_in`: unused by every current caller (see TINY_OUT_DPI's own module note --
    those figures shrink via `save_fit`'s `out_dpi` instead, which keeps every element's
    PROPORTION intact and needs no change here, since the assertion runs at the module's
    normal 200dpi regardless of what a caller later renders the file at). Kept as an escape
    hatch for a figure that genuinely needs a different physical node size, not just a
    different output resolution."""
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    target = (expected_diam_in if expected_diam_in is not None else NODE_DIAM_IN) * fig.dpi
    diam_seen = None
    for ax in fig.axes:
        for p in ax.patches:
            if p.get_gid() != NODE_GID:
                continue
            bb = p.get_window_extent(renderer)
            d_px = (bb.width + bb.height) / 2
            diam_seen = d_px
            assert abs(d_px - target) / target < tol, (
                f"{name}: node diameter {d_px:.1f}px != deck target {target:.1f}px at "
                f"dpi={fig.dpi} (off by {(d_px - target) / target * 100:+.1f}%) -- this "
                f"figure's axes was not sized via fit_node_scale() before drawing its nodes."
            )
    if diam_seen is not None:
        print(f"  node-diam {name}: {diam_seen:.1f}px (native, dpi={fig.dpi})")


# ---------------------------------------------------------------------------
# label placement guard (R5, "the recurring failure")
# ---------------------------------------------------------------------------
# Five rounds running, some figure shipped a text label drawn on top of a filled disc or
# on a stroke of its own colour -- fixed on the named figure each time, then reappeared on
# the next figure someone drew, because every label in this file was positioned by a
# hand-picked (dx, dy) offset that was only ever checked by eye against ONE render. This
# section is the fix: a single placement routine, backed by matplotlib's own renderer (not
# a guess), that every annotation-style label in the file is routed through. It measures
# real obstacle geometry (node discs by their true rendered radius, edges/arcs by their
# actual sampled path and stroke width), nudges the label away from anything it overlaps,
# and -- the part a hand-picked offset can never do -- RAISES instead of shipping a figure
# where it couldn't find a clear spot, so a collision fails the build instead of the review.
#
# Node-interior digit/letter labels (white text centred on its own disc) and matrix-cell
# values (colour already chosen to contrast the cell fill) are a different, already-safe
# pattern -- both are deliberately drawn ON a shape, in a colour chosen for contrast against
# THAT shape -- and are not routed through this guard.
def _finalize(ax):
    # `text.get_window_extent` / `transData` only reflect the FINAL data<->pixel mapping
    # (aspect corrections included) after a draw -- call this after xlim/ylim/aspect are
    # set to their final values, not before.
    ax.figure.canvas.draw()
    return ax.figure.canvas.get_renderer()


def _content_px_bbox(ax):
    """(x0, y0, x1, y1), display pixels: the true rendered union of every line/patch/text
    currently in `ax` (measured with the real renderer). Nodes are Circle patches now (see
    NODE_R above), so they are already covered by the `ax.patches` pass below -- unlike the
    old ax.scatter markers, which needed a separate scatter_bbox_px reconstruction because a
    PathCollection built from `s=` doesn't self-report a usable get_window_extent(). Shared
    by save_fit and place_label's obstacle geometry."""
    renderer = _finalize(ax)
    boxes = []
    for artist_list in (ax.lines, ax.patches, ax.texts):
        for a in artist_list:
            bb = a.get_window_extent(renderer)
            if np.isfinite([bb.x0, bb.y0, bb.x1, bb.y1]).all():
                boxes.append((bb.x0, bb.y0, bb.x1, bb.y1))
    assert boxes, "_content_px_bbox: nothing drawn to fit"
    x0 = min(b[0] for b in boxes); y0 = min(b[1] for b in boxes)
    x1 = max(b[2] for b in boxes); y1 = max(b[3] for b in boxes)
    return x0, y0, x1, y1


def circle_obstacle(center, r_pt, color=None):
    return {"kind": "circle", "center": tuple(center), "r_pt": r_pt, "color": color}


def line_obstacle(pts, width_pt, color=None):
    return {"kind": "line", "pts": [tuple(p) for p in pts], "width_pt": width_pt, "color": color}


def text_obstacle(artist, color=None):
    # `artist`: the Text/Annotation returned by place_label/place_annotation (see
    # `return_artist=True`) -- lets a LATER label avoid stacking on an EARLIER one after the
    # earlier one has already been nudged somewhere the caller didn't originally anchor it.
    return {"kind": "text", "artist": artist, "color": color}


def _pt_seg_dist(p, a, b):
    # Distance (px) from point p to segment a-b, all in display coords, plus the closest
    # point on the segment -- used to test a label's bbox against a sampled edge/arc.
    ap = p - a
    ab = b - a
    denom = np.dot(ab, ab)
    t = 0.0 if denom == 0 else np.clip(np.dot(ap, ab) / denom, 0.0, 1.0)
    closest = a + t * ab
    return np.hypot(*(p - closest)), closest


def _seg_seg_dist(a, b, c, d):
    # Minimum distance (px) between segment a-b and segment c-d -- exactly 0 if they cross.
    # A label's bbox edge (a-b) checked against an obstacle segment (c-d) THIS way (not by
    # sampling a handful of points on the bbox and taking point-to-segment distances) is
    # what actually catches a line running straight through the middle of the box: a line
    # crossing, say, 30% of the way along the box's top edge has distance 0 there, but every
    # one of the box's own CORNERS and MIDPOINT can still be comfortably far from it -- point
    # sampling missed exactly this (confirmed: it let "same edge, twice" settle with the
    # Cafe->Lib arrow running straight through "twice", undetected).
    def cross(o, p, q):
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
    d1, d2 = cross(c, d, a), cross(c, d, b)
    d3, d4 = cross(a, b, c), cross(a, b, d)
    if ((d1 > 0) != (d2 > 0)) and ((d3 > 0) != (d4 > 0)):
        return 0.0
    return min(_pt_seg_dist(a, c, d)[0], _pt_seg_dist(b, c, d)[0],
               _pt_seg_dist(c, a, b)[0], _pt_seg_dist(d, a, b)[0])


def _obstacle_push(ax, bbox, obs, clearance_px):
    # If `obs` overlaps the label bbox (display coords) by less than `clearance_px`, return
    # (penetration_depth_px, unit_push_vector) pointing from the obstacle toward the label;
    # otherwise None. `bbox`: (x0, y0, x1, y1).
    x0, y0, x1, y1 = bbox
    cx_box, cy_box = (x0 + x1) / 2, (y0 + y1) / 2
    if obs["kind"] == "circle":
        ocx, ocy = ax.transData.transform(obs["center"])
        r_px = obs["r_pt"] * (ax.figure.dpi / 72.0) + clearance_px
        nx = min(max(ocx, x0), x1)
        ny = min(max(ocy, y0), y1)
        d = np.hypot(ocx - nx, ocy - ny)
        if d >= r_px:
            return None
        push = np.array([cx_box - ocx, cy_box - ocy])
    elif obs["kind"] == "text":
        # A previously-settled label, checked as a plain axis-aligned rectangle (its true
        # CURRENT glyph box -- mtext.Text.get_window_extent, not Annotation's arrow-inclusive
        # override, see _settle_text) -- so a later label (e.g. "odd" stacking under "start")
        # can't land on top of an earlier one that place_label already had to nudge.
        renderer = ax.figure.canvas.get_renderer()
        tb = mtext.Text.get_window_extent(obs["artist"], renderer)
        ox0, oy0, ox1, oy1 = tb.x0 - clearance_px, tb.y0 - clearance_px, tb.x1 + clearance_px, tb.y1 + clearance_px
        if x1 < ox0 or x0 > ox1 or y1 < oy0 or y0 > oy1:
            return None
        ocx, ocy = (ox0 + ox1) / 2, (oy0 + oy1) / 2
        r_px = max(ox1 - ox0, oy1 - oy0) / 2 + clearance_px
        push = np.array([cx_box - ocx, cy_box - ocy])
    else:  # "line"
        pts_px = np.array([ax.transData.transform(p) for p in obs["pts"]])
        r_px = obs["width_pt"] * (ax.figure.dpi / 72.0) / 2 + clearance_px
        # The bbox's own four EDGES (not a handful of sampled points) against every obstacle
        # segment, via true segment-to-segment distance -- see _seg_seg_dist for why point
        # sampling isn't enough (a line can cross straight through a box's interior without
        # ever coming close to a corner, midpoint, or centre).
        corners = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
        rect_edges = list(zip(corners, corners[1:] + corners[:1]))
        mind = np.inf
        closest_edge = None
        for ra, rb in rect_edges:
            ra, rb = np.array(ra), np.array(rb)
            for i in range(len(pts_px) - 1):
                d = _seg_seg_dist(ra, rb, pts_px[i], pts_px[i + 1])
                if d < mind:
                    mind, closest_edge = d, (ra, rb, pts_px[i], pts_px[i + 1])
        if mind >= r_px:
            return None
        # Push direction: away from the obstacle segment's own closest point to the box
        # centre (works whether the box centre sits outside the segment or the segment
        # crosses straight through the box, where "closest point on segment" is well inside).
        _, _, sc, sd = closest_edge
        _, closest_on_seg = _pt_seg_dist(np.array([cx_box, cy_box]), sc, sd)
        push = np.array([cx_box, cy_box]) - closest_on_seg
    norm = np.linalg.norm(push)
    if norm < 1e-6:
        push = np.array([0.0, 1.0])
        norm = 1.0
    return (r_px, push / norm)


def _settle_text(ax, t, obstacles, *, color, clearance_pt, push_pt, max_iter, name, text):
    # Shared core for place_label (a bare ax.text) and place_annotation (an ax.annotate with
    # a leader) -- both produce a Text-like artist whose `.set_position` moves the label
    # itself (for an Annotation, that's `xytext`; the leader/`xy` target is untouched), so
    # the same nudge loop works for either.
    fig = ax.figure
    renderer = _finalize(ax)
    clearance_px = clearance_pt * fig.dpi / 72.0

    for _ in range(max_iter):
        # Text.get_window_extent, called on the class directly (not t.get_window_extent) --
        # Annotation overrides get_window_extent to include the ARROW's own extent, which
        # reaches all the way to `xy`. Measuring that instead of just the glyph box made the
        # obstacle near `xy` look like it was still touching the label no matter how far the
        # label itself was pushed away, and the loop never converged. Only the glyph box is
        # the thing that must not sit on an obstacle; the leader is allowed to cross other ink.
        bbox = mtext.Text.get_window_extent(t, renderer)
        b = (bbox.x0, bbox.y0, bbox.x1, bbox.y1)
        worst = None
        for obs in obstacles:
            hit = _obstacle_push(ax, b, obs, clearance_px)
            if hit is None:
                continue
            r_px, push = hit
            if worst is None or r_px > worst[0]:
                worst = (r_px, push)
        if worst is None:
            break
        _, push = worst
        cur_px = np.array(ax.transData.transform(t.get_position()))
        new_px = cur_px + push * (push_pt * fig.dpi / 72.0)
        new_xy = ax.transData.inverted().transform(new_px)
        t.set_position((new_xy[0], new_xy[1]))
        renderer = _finalize(ax)
    else:
        t.remove()
        raise RuntimeError(
            f"place_label: {name!r} ({text!r}) could not clear its obstacles after "
            f"{max_iter} nudges -- the layout has no room for this label; fix the geometry "
            f"or the anchor, don't loosen this check."
        )

    # Explicit guard for the recurring failure, independent of the general clearance loop
    # above: a label must never end up nearer than its own clearance to an obstacle sharing
    # its exact colour token (accent-2 on accent-2, MUTED on MUTED), even if some caller
    # passed obstacles with no colour set for everything else.
    bbox = mtext.Text.get_window_extent(t, renderer)
    b = (bbox.x0, bbox.y0, bbox.x1, bbox.y1)
    for obs in obstacles:
        if obs.get("color") != color:
            continue
        hit = _obstacle_push(ax, b, obs, 0.0)
        assert hit is None, (
            f"place_label: {name!r} is the same colour ({color}) as a {obs['kind']} obstacle "
            f"it still sits next to -- never draw a label on a same-colour fill/stroke."
        )

    # Returns the artist itself (not just its final position) so a LATER label can be
    # checked against it via text_obstacle() -- e.g. two labels stacked under the same node,
    # where the first one's settled position isn't known until place_label has already
    # nudged it there.
    return t


def place_label(ax, xy, text, obstacles=(), *, color=MUTED, fontsize=ANNOT_FS,
                 ha="center", va="center", clearance_pt=5.0, zorder=6, max_iter=100,
                 push_pt=2.5, name=None, **kwargs):
    """Draw `text` at data-coord `xy`, nudging it away from any `obstacles` entry it comes
    within `clearance_pt` points of, until it clears all of them, then return the settled
    Text artist (wrap it in text_obstacle(...) to check a LATER label against it). Raises
    RuntimeError if no clear position turns up within `max_iter` nudges -- a build failure
    here means the layout genuinely has no room for this label, which is exactly the case a
    hand-picked offset would otherwise ship silently.

    obstacles: iterable of circle_obstacle(...) / line_obstacle(...) / text_obstacle(...).
    """
    x, y = xy
    t = ax.text(x, y, text, color=color, fontsize=fontsize, ha=ha, va=va, zorder=zorder, **kwargs)
    return _settle_text(ax, t, obstacles, color=color, clearance_pt=clearance_pt,
                         push_pt=push_pt, max_iter=max_iter, name=name or text, text=text)


def place_annotation(ax, xy, text, xytext, obstacles=(), *, color=MUTED, fontsize=ANNOT_FS,
                      ha="center", va="center", clearance_pt=5.0, zorder=6, max_iter=100,
                      push_pt=2.5, name=None, lw=1.2, arrowstyle="-", mutation_scale=None,
                      node_obstacles=(), edge_obstacles=(), rim_clearance_pt=2.0, **kwargs):
    """Like place_label, but for a labelled leader: `text` starts near `xytext` and is
    nudged clear of `obstacles` exactly as place_label does, then a thin `color` leader is
    drawn from the settled label to the `xy` target it explains. Use this (not a bare
    place_label + hand-drawn line) whenever the label needs to point at something -- the
    leader is drawn from the settled label's true edge, so it can never end up short of, or
    crossing through, the label the way a hand-picked xytext sometimes did.

    `arrowstyle`, default "-" (a bare leader line): pass e.g. "-|>" for an arrowhead pointing
    at `xy`.

    R7 fix ("the one thing to fix first"): `obstacles` only ever kept the TEXT clear -- the
    leader matplotlib draws from the settled text to `xy` was never checked against anything,
    which is exactly how konigsberg-bombed's "destroyed" leader crossed a live bridge and
    campus-walk's "same edge, twice" leader crossed two red strokes on its way to landing in
    the gap between them. Pass `node_obstacles`/`edge_obstacles` (same shapes
    draw_annotation_stroke takes) to run the SAME crossing/clearance assertion against the
    leader's actual path -- sampled densely from the settled label position to `xy`, which is
    a strict superset of the visible arrow (matplotlib clips the arrow to the text's own
    bbox edge, a sub-segment of this line), so passing this check guarantees the visible
    stroke passes it too.
    """
    arrowprops = dict(arrowstyle=arrowstyle, color=color, lw=lw)
    if mutation_scale is not None:
        arrowprops["mutation_scale"] = mutation_scale
    t = ax.annotate(text, xy=xy, xytext=xytext, color=color, fontsize=fontsize, ha=ha, va=va,
                     zorder=zorder, arrowprops=arrowprops, **kwargs)
    result = _settle_text(ax, t, obstacles, color=color, clearance_pt=clearance_pt,
                           push_pt=push_pt, max_iter=max_iter, name=name or text, text=text)
    if node_obstacles or edge_obstacles:
        anchor = result.get_position()
        leader_pts = np.linspace(np.asarray(anchor, dtype=float), np.asarray(xy, dtype=float), 40)
        _check_stroke_clear(ax, leader_pts, node_obstacles=node_obstacles,
                             edge_obstacles=edge_obstacles, rim_clearance_pt=rim_clearance_pt,
                             name=f"place_annotation: {name or text!r}")
    return result


# ---------------------------------------------------------------------------
# non-edge stroke guard (R6, "the missing assertion")
# ---------------------------------------------------------------------------
# place_label/place_annotation (above) check that a TEXT label never sits on an obstacle.
# Nothing in the file checked that a non-edge STROKE -- a pairing arc, a leader line, a tick
# mark -- is visually distinguishable from a graph edge. That omission is what let the
# self-loop's tick marks (drawn in INK, near edge weight) and parity-bound's pairing arcs
# (drawn in MUTED at full EDGE_W, the same token as the edges themselves) both get read as
# extra edges/attachments rather than annotations -- three of round 6's Blockers trace back
# to this one gap. Every stroke in this file that is NOT a graph edge should be drawn
# through this function instead of a bare ax.plot/add_patch.
def _check_stroke_clear(ax, pts, *, node_obstacles=(), edge_obstacles=(), rim_clearance_pt=2.0,
                         name="stroke"):
    """Shared assertion core for draw_annotation_stroke and place_annotation's leader check:
    `pts` (a data-coord polyline) must clear every disc in `node_obstacles` by at least
    `rim_clearance_pt` points beyond its TRUE rendered rim, and must not cross any edge in
    `edge_obstacles`. Factored out so BOTH an explicitly-drawn stroke (draw_annotation_stroke)
    and a matplotlib-rendered annotation arrow (place_annotation) run through the identical
    geometric test -- one assertion, not two hand-written copies that could drift apart.
    """
    pts = np.asarray(pts, dtype=float)
    renderer = _finalize(ax)
    dpi_scale = ax.figure.dpi / 72.0
    px = np.array([ax.transData.transform(p) for p in pts])
    clear_px = rim_clearance_pt * dpi_scale

    for obs in node_obstacles:
        ocx, ocy = ax.transData.transform(obs["center"])
        r_px = obs["r_pt"] * dpi_scale
        d = np.hypot(px[:, 0] - ocx, px[:, 1] - ocy)
        mind = d.min()
        assert mind >= r_px + clear_px - 1e-6, (
            f"{name!r} comes within {mind - r_px:.1f}px of a node disc's rim (needs >= "
            f"{clear_px:.1f}px clearance) -- it terminates on or inside a disc it was not "
            f"meant to touch."
        )

    for i in range(len(px) - 1):
        a, b = px[i], px[i + 1]
        for eobs in edge_obstacles:
            epts = np.array([ax.transData.transform(p) for p in eobs["pts"]])
            for j in range(len(epts) - 1):
                d = _seg_seg_dist(a, b, epts[j], epts[j + 1])
                assert d > 0.5, (
                    f"{name!r} crosses a live edge it was not meant to touch -- reroute it or "
                    f"exclude that edge if the crossing is intended."
                )
    return pts


def draw_annotation_stroke(ax, pts, *, color=MUTED, lw=None, dashed=False, zorder=5,
                            node_obstacles=(), edge_obstacles=(), rim_clearance_pt=2.0,
                            name="stroke"):
    """Draw `pts` (a data-coord polyline -- 2 points for a straight leader, a sampled arc from
    something like _bracket_points, or a sampled closed ring from _circle_points) as an
    annotation stroke, then verify by construction that it reads as one:

    - `lw` defaults to 40% of EDGE_W and is asserted to never exceed that -- an annotation
      stroke must never be drawn at (or near) edge weight. Pass `dashed=True` for a dashed
      token instead of/in addition to the thinner weight.
    - every sampled point on the stroke is asserted to clear every disc in `node_obstacles`
      (circle_obstacle(...)) by at least `rim_clearance_pt` points beyond its TRUE rendered
      rim -- a pairing arc must float clear of every node, including the ones its own edges
      connect to, never landing on or inside a neighbouring disc. (A ring MEANT to encircle
      its own node still satisfies this: its sampled radius is larger than the node's true
      rim, so every sampled point still clears it.)
    - the stroke is asserted not to cross any edge in `edge_obstacles` (line_obstacle(...)),
      checked segment-by-segment via the same _seg_seg_dist machinery the label guard uses.
      Pass only the edges this stroke has no business touching -- e.g. a bracket pairing two
      edges at a hub excludes those two from `edge_obstacles` (it is deliberately anchored
      near them) but includes every other edge in the figure.
    """
    lw = (EDGE_W * 0.4) if lw is None else lw
    assert lw <= EDGE_W * 0.4 + 1e-9, (
        f"draw_annotation_stroke: {name!r} at {lw}pt reads as an edge (EDGE_W={EDGE_W}pt) -- "
        f"annotation strokes must draw at <=40% of EDGE_W and/or dashed, never at edge weight."
    )
    pts = np.asarray(pts, dtype=float)
    style = dict(color=color, linewidth=lw, zorder=zorder, solid_capstyle="round")
    if dashed:
        style["linestyle"] = (0, (3, 2))
    ax.plot(pts[:, 0], pts[:, 1], **style)
    _check_stroke_clear(ax, pts, node_obstacles=node_obstacles, edge_obstacles=edge_obstacles,
                         rim_clearance_pt=rim_clearance_pt, name=f"draw_annotation_stroke: {name!r}")
    return pts


def _circle_points(center, r, n=72):
    """Sampled (x, y) polyline tracing a full circle of DATA-unit radius `r` around `center`,
    closed (first point repeated at the end) -- shared by every ring-style annotation (a node
    a route revisits, a component boundary) so each one is checkable by draw_annotation_stroke
    exactly like a bracket or a leader, instead of being a bare add_patch(Circle(...)) no
    assertion ever looks at.
    """
    cx, cy = center
    t = np.linspace(0, 2 * np.pi, n)
    return np.column_stack([cx + r * np.cos(t), cy + r * np.sin(t)])


def draw_annotation_badge(ax, center, r_pt, *, edgecolor=MUTED, facecolor="white", lw=1.4,
                           text=None, text_color=None, text_fontsize=None, node_obstacles=(),
                           rim_clearance_pt=2.0, zorder=6, name="badge"):
    """Draw a small FILLED circular badge (radius `r_pt`, points -- like a node marker, not a
    data-unit ring) at `center`, then assert by construction that its fill never overlaps any
    node disc in `node_obstacles`: unlike a stroke (which only needs its PATH to clear a disc),
    a filled badge's entire interior is opaque ink, so the check is circle-circle separation
    (centre-to-centre distance >= badge radius + disc radius + clearance) rather than
    path-to-rim distance. This is the guard round 6's badges skipped -- they filled straight
    through the node they were meant to mark (R7 Blocker 2).

    Pass `text`/`text_color`/`text_fontsize` to also draw a centred numeral/label on the badge.
    """
    renderer = _finalize(ax)
    dpi_scale = ax.figure.dpi / 72.0
    ccx, ccy = ax.transData.transform(center)
    r_px = r_pt * dpi_scale
    clear_px = rim_clearance_pt * dpi_scale
    for obs in node_obstacles:
        ocx, ocy = ax.transData.transform(obs["center"])
        d = np.hypot(ccx - ocx, ccy - ocy)
        or_px = obs["r_pt"] * dpi_scale
        assert d >= r_px + or_px + clear_px - 1e-6, (
            f"draw_annotation_badge: {name!r} (fill) overlaps a node disc by "
            f"{r_px + or_px + clear_px - d:.1f}px -- a filled badge must sit entirely OUTSIDE "
            f"every node disc it is not itself drawn on, never gouge into one."
        )
    # Radius is specified in POINTS (matches node/marker convention) -- convert to a data-unit
    # patch radius via the same points-per-data-unit factor used elsewhere in this file.
    dpp_x, dpp_y = data_units_per_point(ax)
    dpp = (dpp_x + dpp_y) / 2
    ax.add_patch(mpatches.Circle(center, r_pt * dpp, facecolor=facecolor, edgecolor=edgecolor,
                                  linewidth=lw, zorder=zorder))
    if text is not None:
        ax.text(center[0], center[1], text, ha="center", va="center",
                color=text_color or edgecolor, fontsize=text_fontsize, zorder=zorder + 1)


def save(fig, name, dpi=200):
    _assert_node_diameters(fig, name)
    path = OUT / name
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white", pad_inches=0.15)
    with Image.open(path) as im:
        out_w_px, out_h_px = im.size
    _assert_text_legible(fig, name, out_w_px, out_h_px, dpi)
    plt.close(fig)
    print("wrote", path.name)


def save_fit(fig, ax, name, pad_frac=0.08, pad_min_in=0.04, out_dpi=None, expected_diam_in=None):
    """Save `fig`, cropped EXACTLY to the true rendered extent of everything drawn in `ax`
    (measured with the real renderer, via _content_px_bbox), with a small margin. The crop is
    computed directly as an inches Bbox passed to `bbox_inches`, NOT via xlim/ylim + the
    string "tight".

    Two reasons: (1) `bbox_inches="tight"` crops to the AXES BOX (essentially the declared
    xlim/ylim, mapped through the figure's subplot layout), not to sparse content within it
    -- confirmed directly (Axes.get_tightbbox() returns close to the full data window even
    with only a small marker drawn and the axis off); tightening the DECLARED xlim/ylim is
    the only thing that has ever controlled final image size in this file (see
    fig_edge_single_node's older comment). (2) for content whose own geometry is sized
    relative to a marker's data-unit radius (e.g. a self-loop rooted on its node's boundary
    -- scatter markers have a FIXED pixel size, so their apparent DATA-unit radius depends on
    the CURRENT xlim/ylim), tightening xlim/ylim to fit content and then re-measuring is a
    feedback loop with no stable fixed point -- an earlier version of this fix tried exactly
    that and the window spiralled to zero across iterations. Measuring in PIXELS once and
    cropping directly in inches sidesteps both problems: the pixel geometry never changes
    just because the saved crop does.

    `out_dpi`, if given, renders the FINAL file at a different resolution than the one used
    to measure content (`fig.dpi`) -- needed when the tightly-cropped bbox is physically
    small in inches (e.g. selfloop's whole canvas is ~0.5in across): saving that at the
    same 200dpi everything else uses would leave too few native pixels for a crop this
    small to stay crisp once the deck scales it back up to its usual on-slide width. The
    inches bbox itself is always computed from `fig.dpi` (what the measurement actually
    used) regardless of `out_dpi` -- only the final pixel density changes.

    `expected_diam_in`: see _assert_node_diameters.
    """
    _assert_node_diameters(fig, name, expected_diam_in=expected_diam_in)
    measure_dpi = fig.dpi
    x0, y0, x1, y1 = _content_px_bbox(ax)
    padx = max((x1 - x0) * pad_frac, pad_min_in * measure_dpi)
    pady = max((y1 - y0) * pad_frac, pad_min_in * measure_dpi)
    bbox_in = mtransforms.Bbox([[(x0 - padx) / measure_dpi, (y0 - pady) / measure_dpi],
                                 [(x1 + padx) / measure_dpi, (y1 + pady) / measure_dpi]])
    path = OUT / name
    render_dpi = out_dpi or measure_dpi
    fig.savefig(path, dpi=render_dpi, bbox_inches=bbox_in, facecolor="white")
    with Image.open(path) as im:
        out_w_px, out_h_px = im.size
    _assert_text_legible(fig, name, out_w_px, out_h_px, render_dpi)
    plt.close(fig)
    print("wrote", path.name)


def save_fixed(fig, name, dpi=200):
    # Unlike save(), no bbox_inches="tight" -- for a family of figures meant to render at
    # an IDENTICAL size (e.g. the campus walk/trail/path/base build), 'tight' crops to each
    # frame's own actual ink extent, which differs frame to frame (campus-trail's "start"
    # label reached further right than base/walk/path ever draw, so it alone cropped 11px
    # wider and the graph visibly shifted between frames). Saving the full, uncropped
    # canvas at exactly figsize*dpi guarantees identical dimensions for every frame that
    # shares the same figsize.
    _assert_node_diameters(fig, name)
    path = OUT / name
    fig.savefig(path, dpi=dpi, facecolor="white")
    with Image.open(path) as im:
        out_w_px, out_h_px = im.size
    _assert_text_legible(fig, name, out_w_px, out_h_px, dpi)
    plt.close(fig)
    print("wrote", path.name)


def clean(ax, equal=True):
    ax.set_axis_off()
    if equal:
        ax.set_aspect("equal")


# ---------------------------------------------------------------------------
# shared graph: the 5-node running example (Part 4 onward)
# ---------------------------------------------------------------------------
GRAPH5_POS = {0: (0, 1), 1: (1, 1), 2: (0, 0), 3: (1, 0), 4: (0.5, -0.9)}
GRAPH5_EDGES = [(0, 1), (0, 2), (1, 2), (1, 3), (2, 4), (3, 4)]

# R9 fix ("the one cause", FIXES_R9.md) -- same reasoning as KONIGSBERG_R (see its own
# module note): GRAPH5_POS's own node spread (min spacing 1.0 data units) fixes the
# on-slide diameter for every graph5-based figure independent of target_in, and it measured
# 21.9-29.5px against the 34-40px target. r boosted, relative to spacing, well under the
# ~0.25 crowding ceiling.
GRAPH5_R = 0.17


def draw_graph5(ax, edge_color=MUTED, highlight_edges=(), highlight_color=ACCENT2,
                 node_colors=None, highlight_nodes=(), r=NODE_R, label_fs=LABEL_FS):
    pos = GRAPH5_POS
    he = {frozenset(e) for e in highlight_edges}
    for u, v in GRAPH5_EDGES:
        if frozenset((u, v)) in he:
            continue
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=edge_color,
                linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    for u, v in GRAPH5_EDGES:
        if frozenset((u, v)) in he:
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=highlight_color,
                     linewidth=EDGE_W + 1, zorder=2, solid_capstyle="round")
    nodes = list(pos.keys())
    colors = [(node_colors or {}).get(n, ACCENT2 if n in highlight_nodes else INK) for n in nodes]
    draw_nodes(ax, [pos[n] for n in nodes], colors=colors, r=r, zorder=3)
    for n in nodes:
        x, y = pos[n]
        ax.text(x, y, str(n), ha="center", va="center", color="white",
                fontsize=label_fs, zorder=4, fontfamily="serif")


def graph5_adjacency():
    n = 5
    A = np.zeros((n, n), dtype=int)
    for u, v in GRAPH5_EDGES:
        A[u, v] = 1
        A[v, u] = 1
    return A


# ---------------------------------------------------------------------------
# shared: matrix rendering (adjacency matrices, CSR dense block)
# ---------------------------------------------------------------------------
def draw_matrix(ax, M, row_highlight=None, row_highlight_color=ACCENT2,
                 cell_highlight=None, cell_highlight_color=ACCENT2, title=None, cell_fs=18, equal=True):
    n = M.shape[0]
    for i in range(n):
        for j in range(n):
            v = M[i, j]
            fc = PANEL if v == 0 else ACCENT
            ax.add_patch(mpatches.Rectangle((j - 0.5, i - 0.5), 1, 1, facecolor=fc,
                                             edgecolor=RULE, linewidth=0.8, zorder=1))
            tc = INK if v == 0 else "white"
            ax.text(j, i, str(int(v)), ha="center", va="center", fontsize=cell_fs, color=tc, zorder=2)
    if row_highlight is not None:
        ax.add_patch(mpatches.Rectangle((-0.5, row_highlight - 0.5), n, 1, fill=False,
                                         edgecolor=row_highlight_color, linewidth=3, zorder=3))
    if cell_highlight is not None:
        cells = cell_highlight if isinstance(cell_highlight, list) else [cell_highlight]
        for i, j in cells:
            ax.add_patch(mpatches.Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False,
                                             edgecolor=cell_highlight_color, linewidth=3, zorder=3))
    ax.set_xlim(-0.5, n - 0.5)
    ax.set_ylim(n - 0.5, -0.5)
    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(range(n), fontsize=cell_fs, color=INK)
    ax.set_yticklabels(range(n), fontsize=cell_fs, color=INK)
    ax.xaxis.set_ticks_position("top")
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    if equal:
        ax.set_aspect("equal")
    # `title` intentionally unused by every caller below -- the figcaption is the single
    # caption channel now. Kept as a parameter in case a future two-panel comparison needs
    # a per-panel label.
    if title:
        ax.set_title(title, fontsize=cell_fs, color=INK, pad=14)


# ---------------------------------------------------------------------------
# shared: Königsberg multigraph layout (rule 2, exact positions)
# ---------------------------------------------------------------------------
# R9 fix ("The one cause", FIXES_R9.md): the deck-wide NODE_R (0.12 data units) sizes every
# node to the SAME target_in physical inches (NODE_DIAM_IN), but that scales the whole
# figure -- canvas included -- so the on-slide result (after the deck's CSS shrinks each PNG
# to fit its column) depends only on the ratio of node radius to this layout's OWN node
# spread, never on target_in (a uniform figure rescale cancels exactly against the CSS's own
# scale-to-fit -- verified against real marp renders, see FIXES_R9.md). KPOS's nodes sit
# 1.0-2.0 data units apart, giving every Konigsberg-family figure the SAME measured on-slide
# diameter regardless of target_in: 23.4-24.0px against the 34-40px target. The only real
# lever is the node radius ITSELF, relative to that fixed spread -- so this family gets its
# own, larger r, threaded through draw_knodes/k_obstacles/fit_node_scale everywhere it's
# used. 0.19 clears the family's own tightest spacing (N-A etc., 1.41 units) with enormous
# margin (ratio 0.135, versus the ~0.25 ceiling the band/ladder figures need to respect).
KONIGSBERG_R = 0.19

# Fixed point sizes (LABEL_FS/ANNOT_FS are the deck-wide 18/17pt defaults) are NOT
# automatically fixed by KONIGSBERG_R alone -- on-slide text size still depends on this
# family's own canvas-to-container ratio, which the r-boost only partly closes. Measured
# after the r-boost: node letters at LABEL_FS landed ~12px on-slide, degree numerals at
# ANNOT_FS ~15.6px -- both still under the 16px page-number floor. Bumped on top of the
# boost, not instead of it.
# R12 fix ("the one thing that has not landed"): both bumped again and DECOUPLED from
# ANNOT_FS (28 = ANNOT_FS+11 was coincidence, not a derivation -- a later ANNOT_FS change
# would have silently dragged this family's numerals with it). Sized directly against this
# round's derived floor: paired with the pad_min_in cut on the same family's save_fit calls
# (see konigsberg-blank/abstraction-2/3's own notes -- 1.5in of padding was dragging scale
# down to ~0.25 for no reason, THE cause this round traced), 30pt clears TEXT_LEGIBLE_PX with
# real margin at the ~0.32 scale that padding cut lands on.
KONIGSBERG_LABEL_FS = 36
KONIGSBERG_DEGREE_FS = 36
# recap.png's own xlim/ylim is wider than the rest of the family (it has to fit the dashed
# "one component" bracket around the whole diamond), so the same KONIGSBERG_R lands a
# smaller on-slide disc there (measured: 31.7px vs 36.5-37.5px for the rest) -- a bigger r,
# scoped to that one figure, closes the gap the same way KONIGSBERG_R itself was derived.
KONIGSBERG_R_RECAP = 0.22

KPOS = {"N": (0.0, 1.0), "S": (0.0, -1.0), "A": (-1.0, 0.0), "B": (1.0, 0.0)}
KEDGES = [
    ("NA1", "N", "A", 0.30),
    ("NA2", "N", "A", -0.30),
    ("SA1", "S", "A", 0.30),
    ("SA2", "S", "A", -0.30),
    ("NB", "N", "B", 0.0),
    ("SB", "S", "B", 0.0),
    ("AB", "A", "B", 0.0),
]
def kedge_degrees(removed=()):
    deg = {n: 0 for n in "NSAB"}
    for eid, u, v, _rad in KEDGES:
        if eid in removed:
            continue
        deg[u] += 1
        deg[v] += 1
    return deg


def _arc3_points(p1, p2, rad, n=200):
    # Reproduce matplotlib's own "arc3" connection style (a quadratic Bezier whose control
    # point sits `rad` * |p2-p1| off the p1-p2 midpoint, perpendicular to the chord) so a
    # dash pattern can be hand-placed along the SAME curve FancyArrowPatch would draw.
    #
    # R5 fix (Blocker 1): the control-point offset here was the NEGATION of matplotlib's own
    # ConnectionStyle.Arc3.connect(), which computes cx,cy = mid + rad*(dy, -dx) (confirmed
    # against its source directly). This function instead used mid + rad*(-dy, dx) -- so for
    # any rad, _arc3_points(rad) traced the same curve the REAL arc3 draws for -rad. Königsberg's
    # removed bridges (NA2/SA2, rad=-0.30) were dashed along THIS function's rad=-0.30, which
    # -- with the sign bug -- is real-arc3's rad=+0.30 curve: exactly the path already drawn
    # solid for the surviving parallel bridge (NA1/SA1, real rad=+0.30). The dashed "removed"
    # bridge was rendered exactly on top of the live one, not as a separate mirrored curve, so
    # it visually vanished (its dashes fall on a path already fully covered by a solid stroke
    # of the same colour) -- exactly the round-5 regression (five solid edges, no dashed ones).
    p1, p2 = np.asarray(p1, dtype=float), np.asarray(p2, dtype=float)
    mid = (p1 + p2) / 2
    d = p2 - p1
    ctrl = mid + rad * np.array([d[1], -d[0]])
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * p1 + 2 * (1 - t) * t * ctrl + t ** 2 * p2


def _draw_dashed_arc(ax, p1, p2, rad, color, width, n_dashes=6, zorder=1):
    # R4 fix (Blocker 4): FancyArrowPatch's own `linestyle=(0,(5,4))` dashing starts its
    # phase at the patch's start and simply stops wherever the path ends -- if that happens
    # to fall in a gap (as it did for both destroyed bridges in konigsberg-bombed.png), the
    # LAST visible dash stops well short of the endpoint, and the disc drawn on top (which
    # should hide the line right up to its boundary) has nothing left there to hide -- the
    # line reads as floating, detached from the node. Sampling the same arc explicitly and
    # slicing it into a fixed, odd number of dash/gap segments guarantees a dash (not a
    # gap) covers BOTH endpoints, so the visible line always reaches the disc it's drawn
    # under, regardless of the arc's length.
    pts = _arc3_points(p1, p2, rad)
    n = len(pts)
    seg_count = 2 * n_dashes - 1
    bounds = np.linspace(0, n - 1, seg_count + 1).round().astype(int)
    for i in range(0, seg_count, 2):  # even segments = dashes; odd segments = gaps (skipped)
        a, b = bounds[i], min(bounds[i + 1] + 1, n)
        ax.plot(pts[a:b, 0], pts[a:b, 1], color=color, linewidth=width,
                solid_capstyle="round", zorder=zorder)


def draw_kedges(ax, removed=(), removed_color=MUTED, color=MUTED, width=EDGE_W):
    # Removed bridges dash at the *same* weight as a live edge, in annotation gray -- the
    # old pale-RULE dashes at 2.2pt were barely separable from white (F1/F3 fix).
    for eid, u, v, rad in KEDGES:
        if eid in removed:
            _draw_dashed_arc(ax, KPOS[u], KPOS[v], rad, removed_color, width, zorder=1)
        else:
            ax.add_patch(FancyArrowPatch(KPOS[u], KPOS[v], connectionstyle=f"arc3,rad={rad}",
                                          arrowstyle="-", color=color, linewidth=width, zorder=1))


def draw_knodes(ax, colors=None, labels_inside=None, r=NODE_R, label_fs=LABEL_FS):
    order = ["N", "S", "A", "B"]
    cs = [(colors or {}).get(n, INK) for n in order]
    draw_nodes(ax, [KPOS[n] for n in order], colors=cs, r=r, zorder=3)
    for n in order:
        x, y = KPOS[n]
        txt = (labels_inside or {}).get(n, n)
        ax.text(x, y, txt, ha="center", va="center", color="white", fontsize=label_fs,
                zorder=4, fontfamily="serif")


def k_limits(ax, pad=0.85, xpad=None):
    # xpad, if given, widens only the x-range -- KPOS is a symmetric square, so a plain
    # equal pad crops to a slightly-portrait aspect once bbox_inches="tight" is applied;
    # a touch more x-room lands it at <=0.95 without touching node/edge geometry.
    xpad = pad if xpad is None else xpad
    ax.set_xlim(-1 - xpad, 1 + xpad)
    ax.set_ylim(-1 - pad, 1 + pad)
    clean(ax)


def k_obstacles(ax, node_colors=None, edge_color=MUTED, r=NODE_R):
    # Every node disc (true rendered radius) and every one of the seven bridge curves --
    # kept or dashed, they're all real ink on the figure -- as obstacles for place_label /
    # place_annotation. Shared by every Konigsberg-family figure that adds a label on top of
    # draw_kedges/draw_knodes, so a label placed near this graph is checked against the SAME
    # geometry regardless of which figure draws it.
    node_colors = node_colors or {}
    r_pt = node_radius_pt(ax, r)
    obs = [circle_obstacle(KPOS[n], r_pt, color=node_colors.get(n, INK)) for n in "NSAB"]
    for eid, u, v, rad in KEDGES:
        pts = _arc3_points(KPOS[u], KPOS[v], rad, n=40) if rad else [KPOS[u], KPOS[v]]
        obs.append(line_obstacle(pts, EDGE_W, color=edge_color))
    return obs


def assert_dashed_distinct_from_live(removed, min_sep=0.05):
    # R5 fix (Blocker 1): the exact failure this guards against -- a dashed "removed" bridge
    # silently rendered on the SAME path as a live one (a sign bug in _arc3_points, since
    # fixed) -- produced a figure with five solid edges and no visible dashes at all. Compare
    # every removed edge's sampled curve against every LIVE edge between the same node pair
    # and fail loudly if they coincide, instead of relying on a human re-counting dashes.
    live = [(eid, u, v, rad) for eid, u, v, rad in KEDGES if eid not in removed]
    dashed = [(eid, u, v, rad) for eid, u, v, rad in KEDGES if eid in removed]
    assert len(dashed) == 2, f"expected exactly two dashed (removed) bridges, got {dashed}"
    for deid, du, dv, drad in dashed:
        # Every curve between the same two nodes shares the SAME two endpoints exactly (both
        # start/end at the node centres), so comparing full curves always finds a zero-distance
        # match right at N/A or S/A regardless of how different the curvature is -- that's not
        # coincidence, it's just two edges meeting the same node. Compare only the INTERIOR
        # (t in [0.2, 0.8]), where two genuinely different arcs must separate.
        dpts = _arc3_points(KPOS[du], KPOS[dv], drad, n=101)[20:81]
        for leid, lu, lv, lrad in live:
            if {lu, lv} != {du, dv}:
                continue
            lpts = _arc3_points(KPOS[lu], KPOS[lv], lrad, n=101)[20:81]
            mind = min(np.hypot(*(dp - lp)) for dp in dpts for lp in lpts)
            assert mind > min_sep, (
                f"dashed {deid} coincides with live edge {leid} (min separation {mind:.4f} "
                f"data units, need > {min_sep})"
            )


# ===========================================================================
# Part 1 -- the puzzle
# ===========================================================================
# Shared irregular landmass geometry -- used by both konigsberg-sketch (Part 1) and
# abstraction-1-map (Part 2, frame 1) so the two are the *same picture*: the abstraction
# build has to start from this sketch, not from an already-abstracted node-link diagram.
#
# R3 fix (Major 11): the old geometry was four rounded rectangles -- already abstract
# shapes, so frame 1 of the abstraction build contradicted its own caption ("Geography,
# distance, shape -- all of it is about to go"). `_irregular_blob` traces a wavy,
# seeded-but-reproducible coastline instead, so N/S read as river banks and A/B as
# irregular islands -- a real sketch, not a diagram -- while the seven bridges stay
# individually countable straight/curved segments crossing the water gaps between them.
def _irregular_blob(cx, cy, rx, ry, seed, n=40, jitter=0.16):
    rng = np.random.default_rng(seed)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    radii = 1.0 + rng.uniform(-jitter, jitter, n)
    for _ in range(2):  # two smoothing passes: a traced coastline, not a jagged polygon
        radii = (radii + np.roll(radii, 1) + np.roll(radii, -1)) / 3
    return [(cx + rx * r * np.cos(a), cy + ry * r * np.sin(a)) for a, r in zip(angles, radii)]


CITY_CENTERS = {"N": (0.0, 1.9), "S": (0.0, -1.9), "A": (-0.85, 0.05), "B": (0.95, -0.05)}
CITY_SHAPE = {  # (rx, ry, seed) -- hand-tuned so N/S clear the A/B islands with a visible gap
    "N": (2.15, 0.45, 1), "S": (2.15, 0.45, 2), "A": (0.62, 0.95, 3), "B": (0.55, 0.85, 4),
}
CITY_BRIDGES = [
    ("N", "A", 0.15), ("N", "A", -0.15),
    ("S", "A", 0.15), ("S", "A", -0.15),
    ("N", "B", 0.0), ("S", "B", 0.0), ("A", "B", 0.0),
]
CITY_XLIM = (-2.75, 2.75)
CITY_YLIM = (-2.65, 2.65)


CITY_WATER_COLOR = "#dbe6ee"
CITY_LABEL_FS = 21  # see draw_city_sketch's own note on why this is not LABEL_FS -- R12 fix:
                     # was 18pt, 20.6px on-slide against konigsberg-sketch.png's own
                     # container/scale, just under the 21px floor.


def draw_city_sketch(ax, bridge_color=INK, bridge_width=6.5, fade=False):
    # R4 fix (Minor, slides 007/008): the sketch had no water at all -- four landmass
    # blobs floating in plain white, connected by bridges, with nothing distinguishing
    # "gap between landmasses" from "edge of the page." Slide 007 asks "river width?" and
    # slide 008's build claims "geography, distance... about to go" over a picture that
    # never showed either. A pale band behind the two long N/S banks and around the A/B
    # islands reads as the Pregel without competing with the bridges or landmass fills.
    #
    # R9 fix (Blocker 3): `fade=True` is the actual first cut for slide 008 -- see
    # fig_abstraction_1_map. Every geographic element (water, coastlines, bridges) fades
    # toward white; only the N/A/B/S labels hold full strength (bigger, INK not MUTED) --
    # so the render matches the caption ("the labels are all that survive the cut") instead
    # of being byte-identical to konigsberg-sketch.png's full-strength sketch.
    water_color = "#eef3f7" if fade else CITY_WATER_COLOR
    land_fill = "#fbfbfa" if fade else PANEL
    land_edge = "#c9c9c9" if fade else MUTED
    land_lw = 1.1 if fade else 1.8
    b_color = "#c9c9c9" if fade else bridge_color
    b_width = 3.5 if fade else bridge_width
    label_color = INK if fade else MUTED
    # R10 fix: decoupled from the deck-wide LABEL_FS (bumped for fit_node_scale-normalized
    # DISC labels -- see LABEL_FS's own module note). These are landmass-blob labels, not
    # node discs -- no 150px-native-diameter invariant applies to them -- so tying their size
    # to LABEL_FS was coincidental, not principled, and would have doubled this map's labels
    # for a reason that has nothing to do with this figure. CITY_LABEL_FS keeps the size this
    # figure was actually tuned at.
    label_fs = CITY_LABEL_FS * 1.4 if fade else CITY_LABEL_FS
    ax.add_patch(mpatches.Rectangle((CITY_XLIM[0], -1.45), CITY_XLIM[1] - CITY_XLIM[0], 2.9,
                                     facecolor=water_color, edgecolor="none", zorder=0))
    # Bridges connect landmass CENTRES and sit at zorder=1, under the landmass polygons
    # (zorder=2) -- each line's middle segment is covered by the shapes it starts/ends
    # inside, leaving only the water-crossing stretch visible, same trick as the old boxes.
    for u, v, rad in CITY_BRIDGES:
        ax.add_patch(FancyArrowPatch(CITY_CENTERS[u], CITY_CENTERS[v], connectionstyle=f"arc3,rad={rad}",
                                      arrowstyle="-", color=b_color, linewidth=b_width,
                                      capstyle="round", zorder=1))
    for n, (x, y) in CITY_CENTERS.items():
        rx, ry, seed = CITY_SHAPE[n]
        pts = _irregular_blob(x, y, rx, ry, seed)
        ax.add_patch(mpatches.Polygon(pts, closed=True, facecolor=land_fill, edgecolor=land_edge,
                                       linewidth=land_lw, joinstyle="round", zorder=2))
        ax.text(x, y, n, ha="center", va="center", fontsize=label_fs, color=label_color,
                fontweight="bold" if fade else "normal", zorder=3)
    ax.set_xlim(*CITY_XLIM)
    ax.set_ylim(*CITY_YLIM)
    clean(ax)


def fig_konigsberg_sketch():
    fig, ax = plt.subplots(figsize=(6.9, 5.6))
    draw_city_sketch(ax)
    save(fig, "konigsberg-sketch.png")


# ===========================================================================
# Part 2 -- abstraction (3-step build)
# ===========================================================================
def fig_abstraction_1_map():
    # R9 fix (Blocker 3, "the build's first step is a null step"): this used to call
    # draw_city_sketch() with no arguments -- byte-identical to konigsberg-sketch.png, so
    # slides 005/007/008 showed the same picture three slides running while 008's caption
    # ("N, A, B, S -- the labels are all that survive the cut") described a cut this render
    # never made. fade=True makes it a real first cut: see draw_city_sketch's own note.
    fig, ax = plt.subplots(figsize=(6.9, 5.6))
    draw_city_sketch(ax, fade=True)
    save(fig, "abstraction-1-map.png")


def fig_abstraction_2_nodes():
    # R3 fix (Major 10): NO edges -- the slide's own text is "Four landmasses. Four dots."
    # Drawing all seven bridges here (as before) made 009->010 a no-op except edge colour.
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    k_limits(ax, xpad=1.1)
    fit_node_scale(fig, ax, r=KONIGSBERG_R)
    draw_knodes(ax, r=KONIGSBERG_R, label_fs=KONIGSBERG_LABEL_FS)
    # R10 fix (FIXES_R10.md): save() (bbox_inches="tight") crops to k_limits' generous
    # xpad/pad DATA window, not to the four dots actually drawn in it -- measured 34% ink.
    # save_fit crops to the real rendered extent instead; `w:` (reported to the deck agent)
    # is what now controls on-slide size.
    # R10 fix, round 2: 0.15in pad landed a 1089px-tall canvas -- under max-height:380px's
    # OWN 1096px break-even point (see TINY_OUT_DPI's module note: the deck never upscales,
    # so a canvas under 380px displays at native 1:1, which measured 52.4px here, just over
    # the 52px ceiling). Pushed above the cap so the deck's own downscale brings the node
    # back under it.
    #
    # R12 fix ("the one thing that has not landed"): R10's 1.5in overshot that goal by a lot
    # -- it pushed the canvas to ~1540px tall, i.e. scale ~0.25, when clearing the 52px node
    # ceiling only needs scale <~0.35 (150px native * 0.35 = 52.5px). The gap between those
    # two was pure excess margin, and it was landing directly on every label's on-slide size
    # (on_slide_px = fontsize_pt * dpi/72 * scale -- the SAME scale that shrinks the node
    # shrinks every label with it). 0.4in targets scale ~0.32 (node ~48px, comfortably inside
    # 26-52) instead of overshooting to 0.25.
    save_fit(fig, ax, "abstraction-2-nodes.png", pad_frac=0.08, pad_min_in=0.5)


def fig_abstraction_3_graph():
    # Edges introduced here, in the standard graph colour (MUTED) -- this frame is the one
    # that earns the slide title "each bridge becomes an edge".
    fig, ax = plt.subplots(figsize=(5.4, 5.4))
    k_limits(ax, xpad=1.1)
    fit_node_scale(fig, ax, r=KONIGSBERG_R)
    draw_kedges(ax, color=MUTED, width=EDGE_W)
    draw_knodes(ax, r=KONIGSBERG_R, label_fs=KONIGSBERG_LABEL_FS)
    # R10 fix: see fig_abstraction_2_nodes -- same save()->save_fit swap.
    # R12 fix: see fig_abstraction_2_nodes -- same pad_min_in cut (1.5in -> 0.4in).
    save_fit(fig, ax, "abstraction-3-graph.png", pad_frac=0.08, pad_min_in=0.5)


MULTI_P, MULTI_Q = (-0.6, 0.0), (0.6, 0.0)


def _draw_multigraph_pair(ax, r=NODE_R):
    # Shared by fig_multigraph_bridges (matrix-free) and fig_multigraph (matrix) -- the two
    # must never draw the N-A pair differently (R9 fix, Blocker 2's own point: two slides
    # that explain a figure differently need two FILES, not one file quietly diverging).
    #
    # Minor fix: nodes were labelled P/Q, but the slide text says "Konigsberg has two
    # bridges between the same pair of landmasses" -- relabel to the deck's own N/A.
    for rad in (0.30, -0.30):
        ax.add_patch(FancyArrowPatch(MULTI_P, MULTI_Q, connectionstyle=f"arc3,rad={rad}",
                                      arrowstyle="-", color=MUTED, linewidth=EDGE_W, zorder=1))
    draw_nodes(ax, [MULTI_P, MULTI_Q], colors=INK, r=r, zorder=3)
    for (x, y), t in zip([MULTI_P, MULTI_Q], ["N", "A"]):
        ax.text(x, y, t, ha="center", va="center", color="white", fontsize=LABEL_FS, zorder=4)
    # "two bridges, two edges" not baked in -- it is the figcaption verbatim (duplicated-caption fix).


def fig_multigraph_bridges():
    # R9 fix (Blocker 2): matrix-free variant for slide 012 ("Two bridges, one pair"). That
    # slide never names a matrix, a row, a column or either colour, and the adjacency matrix
    # isn't defined until slide 054 -- sharing fig_multigraph()'s file (which carries a 2x2
    # blue-filled, red-outlined matrix) taught an unexplained grid 41 slides early
    # (FIGURE_GUIDE.md: "never share a figure between slides that explain it differently").
    # This is exactly fig_multigraph()'s left panel, alone, at its own natural crop.
    fig, ax = plt.subplots(figsize=(3.4, 2.6))
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.85, 0.85)
    clean(ax)
    fit_node_scale(fig, ax)
    _draw_multigraph_pair(ax)
    # R10 fix (FIXES_R10.md): a lone N-A pair is nearly all of this figure's content (like
    # selfloop/edge-single-node -- see SELFLOOP_PAD_IN's note), which used to mean padding the
    # canvas out to land a fixed w:520 on target -- exactly the "90% white canvas" defect
    # check_render.py now catches (this figure measured 7% ink). Small, fixed pad; `w:`
    # (reported to the deck agent) controls on-slide size instead.
    save_fit(fig, ax, "multigraph-bridges.png", pad_frac=0.08, pad_min_in=0.18, out_dpi=TINY_OUT_DPI)


def fig_multigraph():
    # R9 fix (Blocker 2): matrix version, now exclusive to slide 054 -- slide 012 uses
    # fig_multigraph_bridges() (matrix-free) instead. See that function's own note.
    #
    # R7 fix (Major 21): the slide's own claim is about a MATRIX ENTRY (a multigraph's cell
    # counts parallel edges, not just 0/1), but the figure used to draw only the two discs
    # and two arcs -- no matrix anywhere, so the thing the slide is about was never actually
    # shown. A 2x2 matrix panel, N/A labelled to match the pair on the left, with the "2"
    # cell (both directions -- the matrix is symmetric) highlighted the same way every other
    # matrix figure in the deck highlights its point cell.
    fig, axes = plt.subplots(1, 2, figsize=(6.2, 2.5), gridspec_kw={"width_ratios": [1.5, 1]})
    ax = axes[0]
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.85, 0.85)
    clean(ax)
    # R9 fix ("the one cause", FIXES_R9.md): this pair's own spacing (1.2 data units) fixed
    # the on-slide diameter at 28.8px independent of target_in -- see KONIGSBERG_R's module
    # note. 0.16 (ratio 0.133) stays well under the ~0.25 crowding ceiling.
    R = 0.16
    W = fit_node_scale(fig, ax, r=R)
    _draw_multigraph_pair(ax, r=R)

    ax2 = axes[1]
    M = np.array([[0, 2], [2, 0]])
    # R12 fix ("the one thing that has not landed"): 24.7pt (fs(20, W/2)) landed under the
    # 21px floor once measured against this figure's own container/scale.
    matrix_fs = fs(24, W / 2)
    draw_matrix(ax2, M, cell_highlight=[(0, 1), (1, 0)], cell_fs=matrix_fs)
    ax2.set_xticklabels(["N", "A"], fontsize=matrix_fs, color=INK)
    ax2.set_yticklabels(["N", "A"], fontsize=matrix_fs, color=INK)
    save(fig, "multigraph.png")


# R4 fix (Policy 2): figsize shrunk (5.6 -> 3.0 square) so the loop+node fill a much
# bigger share of the saved canvas -- see fig_edge_single_node for why bbox_inches="tight"
# doesn't do this on its own (Axes.get_tightbbox() still reports close to the full
# declared xlim/ylim). Was 23% x 40% ink.
SELFLOOP_W = 3.0
# R9 fix (FIXES_R9.md "The one cause"): this used to save at out_dpi=1200, six times the
# 200dpi every other figure uses, on the theory (written right where SELFLOOP_OUT_DPI was
# consumed, below) that "the deck displays it at the same ~520px column width as every other
# figure regardless of source size" -- FALSE. The deck's CSS (`width:auto !important;
# max-width:100%; max-height:380px`) scales each image by its OWN native pixel size, so a
# tight crop (pad_frac=0.10 -- content barely bigger than the node+loop) at ANY dpi renders
# HUGE on the slide: measured on the actual rendered slide, 178.5px (question) / 137.5px
# (answer) against a 34-40px deck target, independent of out_dpi (out_dpi inflates the disc
# AND the canvas by the same factor, so the on-slide ratio -- and thus the bug -- survives
# it unchanged; the "six times everything else" was purely a wasted-resolution symptom, not
# the cause of the oversized on-slide render).
#
# R9's own fix went the OTHER wrong way (FIXES_R10.md, "the one cause, one level further
# out"): it padded the SAVED crop out to ~3in of absolute margin so a FIXED w:520 directive
# would land the right on-slide size -- but that margin is what a student's eye actually
# sees: check_render.py measures this canvas as 90%+ white, the loop+node landing at 2-4% of
# its box. On-slide size has TWO independent levers (the crop's own pixel dimensions, and the
# deck's per-slide `w:` directive) and R9 only ever pulled the first one. Pull the second
# instead: crop to ink plus a small fixed pad (SELFLOOP_PAD_IN below), so the canvas IS the
# drawing, and let `w:` (chosen per figure, reported to the deck agent -- see
# fig_selfloop/fig_selfloop_answer's own call) do the on-slide-size work that used to be done
# by bloating the canvas.
SELFLOOP_PAD_IN = 0.16


# R12 fix ("the one thing that has not landed"): this whole family saves through
# TINY_OUT_DPI (~50.7dpi, not the deck's usual 200) specifically so it renders at native
# resolution (scale=1.0 -- see TINY_OUT_DPI's own module note), which means on_slide_px =
# fontsize_pt * (50.7/72) -- NO deck downscale ever helps here, so the floor translates
# directly to a point-size floor: 21 / (50.7/72) = 29.8pt. Sized with margin above that.
SELFLOOP_ANNOT_FS = 34


def _draw_selfloop(ax, r=NODE_R, number_badges=False, badge_fs=SELFLOOP_ANNOT_FS):
    # r: NODE_R, the deck-wide canonical node radius in DATA units -- exact by construction
    # (Circle patches, not a scatter marker's guessed radius; see the module note above
    # NODE_R). R5 fix (Blocker 2/3, historical): the previous version hard-coded r=0.135
    # "measured from a render", which went stale against the marker size then in use -- a 3x
    # mismatch that rooted the loop's legs 13-19px off the disc. That whole class of bug
    # (a radius measured/guessed once, then drifting out of sync with what's actually drawn)
    # is what NODE_R being a single source of truth removes.
    #
    # R3 fix (Major 14): the old loop sat *behind* the node (zorder=1 under the node's
    # zorder=3) so both attachment points were covered by the disc, and it read as a
    # second, empty node balanced on the first. Shrink it, draw it in FRONT, and root it
    # at two visibly separated points on the disc boundary (leave ~135 deg, return ~45 deg).
    #
    # R6 fix (Blocker 1, fourth round on this figure): R5's own gap turned out to be
    # FancyArrowPatch's default shrinkA/shrinkB (2pt each, applied even for arrowstyle="-")
    # -- confirmed directly by rendering this exact patch and measuring: with the default it
    # stops 5.6px short of `leave`/`ret` at BOTH ends (2pt * dpi/72 = 2*200/72, exactly); with
    # shrinkA=shrinkB=0 the rendered path lands on `leave`/`ret` to floating-point precision.
    # `leave`/`ret` were already correct -- ON the true rim, by construction (r*cos/r*sin) --
    # every earlier round's fix (including the tick marks meant to visually "complete" the
    # attachment) was patching a symptom the shrink parameter was quietly causing. The ticks
    # are deleted outright per the round-6 spec ("take the simple option") -- they were never
    # needed once the legs actually reach the rim, and they were the thing actually making
    # the node read as having three attachments (INK, 64-70px long, crossing the gray legs).
    cx, cy = 0.0, 0.0
    leave_ang, return_ang = 135, 45
    leave = (r * np.cos(np.deg2rad(leave_ang)), r * np.sin(np.deg2rad(leave_ang)))
    ret = (r * np.cos(np.deg2rad(return_ang)), r * np.sin(np.deg2rad(return_ang)))
    # negative rad: for a left-to-right p1->p2 (as leave->ret is here), matplotlib's arc3
    # bulges to the *right* of the travel direction for positive rad -- i.e. downward,
    # into the node -- so this needs the opposite sign to arc up and over the top.
    loop = FancyArrowPatch(leave, ret, connectionstyle="arc3,rad=-2.6", arrowstyle="-",
                            color=MUTED, linewidth=EDGE_W, capstyle="round", zorder=5,
                            shrinkA=0, shrinkB=0)
    ax.add_patch(loop)

    # Assert the legs actually land on the rim (not just "should, by construction") --
    # measured on the real rendered path, the same way the R6 diagnosis above was made, so a
    # future change to shrink/connectionstyle/capstyle can't silently reopen this gap.
    renderer = _finalize(ax)
    path_disp = loop.get_transform().transform(loop.get_path().vertices)
    leave_px = ax.transData.transform(leave)
    ret_px = ax.transData.transform(ret)
    gap_leave = np.hypot(*(path_disp[0] - leave_px))
    gap_ret = np.hypot(*(path_disp[-1] - ret_px))
    assert gap_leave < 2.0 and gap_ret < 2.0, (
        f"_draw_selfloop: loop legs land {gap_leave:.1f}px / {gap_ret:.1f}px off the rim "
        f"(must be < 2px) -- the loop must visibly close on the node."
    )

    if number_badges:
        # R7 fix (Blocker 2, a regression R6 introduced): R6 centred an OPAQUE white disc ON
        # the rim -- a badge of radius 0.42r straddling a point that sits exactly AT radius r
        # from centre puts roughly half its fill INSIDE the node. Confirmed directly: a
        # topmost-black-row scan found the node's own rendered top edge dropping 15-30px at
        # both badge x-positions -- two bites out of the node's shoulders, reading as a
        # three-lobed blob, and hiding the two attachment points the badges exist to mark on
        # the one slide whose whole point is that the loop attaches twice.
        #
        # Badges now sit OUTSIDE the node entirely -- bare numerals, no disc/fill (this
        # function's own documented fallback: "or drop the discs and set bare numerals in
        # annotation gray") -- offset radially outward from each attachment point, with a
        # hairline leader that stops short of the rim. Routed through draw_annotation_stroke
        # so clearance from the node disc AND from the loop's own path is asserted against
        # the real renderer, not eyeballed -- exactly the guard R6 built but never called from
        # here.
        loop_pts = _arc3_points(leave, ret, -2.6, n=60)
        node_obs = [circle_obstacle((cx, cy), node_radius_pt(ax, r))]
        loop_obs = [line_obstacle(loop_pts, EDGE_W, color=MUTED)]
        for i, (x, y) in enumerate((leave, ret), start=1):
            ang = np.arctan2(y - cy, x - cx)
            u = np.array([np.cos(ang), np.sin(ang)])
            leader_pts = np.array([np.array([x, y]) + u * r * 0.22, np.array([x, y]) + u * r * 0.55])
            # lw left at draw_annotation_stroke's own default (40% of EDGE_W) -- an
            # annotation stroke must stay visibly thinner than the loop it sits beside, and
            # the loop is now plain EDGE_W (see the module note above _draw_selfloop).
            draw_annotation_stroke(ax, leader_pts, node_obstacles=node_obs, edge_obstacles=loop_obs,
                                    zorder=6, name=f"selfloop-answer:leader-{i}")
            tx, ty = np.array([x, y]) + u * r * 0.85
            ax.text(tx, ty, str(i), ha="center", va="center", color=MUTED,
                    fontsize=badge_fs, fontweight="bold", zorder=7)
    draw_node(ax, (cx, cy), color=INK, r=r, zorder=3)
    # LABEL_FS, not fs()-scaled: this is a node-INTERIOR letter, the same convention every
    # other node-interior digit/letter label in the deck uses (draw_knodes/draw_graph5) --
    # and since every node now shares one PHYSICAL diameter (NODE_DIAM_IN, deck-wide), a
    # fixed point size is automatically the same proportion of the node everywhere, with no
    # per-figure scale needed.
    ax.text(cx, cy, "X", ha="center", va="center", color="white", fontsize=LABEL_FS, zorder=4)


def _build_selfloop_fig(name, number_badges, show_k=False):
    # Draw against ANY reasonable, generous xlim/ylim (its exact value no longer matters --
    # see save_fit) at NODE_R -- a Circle's data-unit radius is exact and does not depend on
    # xlim/ylim (unlike the old scatter marker, whose apparent DATA-unit radius depended on
    # the CURRENT xlim/ylim -- see the module note above NODE_R for what that cost across six
    # rounds), so there is no feedback loop to worry about here at all.
    fig, ax = plt.subplots(figsize=(SELFLOOP_W, SELFLOOP_W))
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    clean(ax)
    fit_node_scale(fig, ax)
    _draw_selfloop(ax, NODE_R, number_badges=number_badges)
    if show_k:
        # R9 fix ("free-standing annotations... need their own size bump", FIXES_R9.md): was
        # 13pt, ~9px on-slide -- under the 16px page-number floor.
        ax.text(0, -1.55 * NODE_R, "k = 2", ha="center", va="top", color=MUTED,
                fontsize=SELFLOOP_ANNOT_FS, zorder=6)
    # R10 fix: plain 200dpi, cropped to ink plus a small fixed pad -- the on-slide target is
    # now hit by the deck's own `w:` directive (see the module note above SELFLOOP_PAD_IN),
    # not by canvas bloat.
    save_fit(fig, ax, name, pad_frac=0.08, pad_min_in=SELFLOOP_PAD_IN, out_dpi=TINY_OUT_DPI)


def fig_selfloop():
    # "both ends attach here" is the figcaption verbatim (duplicated-caption fix) -- not
    # repeated in-figure.
    _build_selfloop_fig("selfloop.png", number_badges=False)


def fig_selfloop_answer():
    # NEW (Major 17): slide 058 ("Two") answered the previous slide's question with the
    # SAME picture (selfloop.png, byte-identical) and a caption claiming "k gains 2" that
    # nothing in the figure showed -- neither a "2" nor a "k". This variant numbers the two
    # attachment points the answer is counting and prints the resulting degree.
    _build_selfloop_fig("selfloop-answer.png", number_badges=True, show_k=True)


# ===========================================================================
# Part 3 -- degree and parity
# ===========================================================================
def _star_positions(k, r=1.0, start=90):
    pos = {0: (0.0, 0.0)}
    for i in range(1, k + 1):
        ang = np.deg2rad(start + 360 * (i - 1) / k)
        pos[i] = (r * np.cos(ang), r * np.sin(ang))
    return pos


def fig_degree_definition():
    fig, ax = plt.subplots(figsize=(4.8, 4.2))
    pos = _star_positions(4)
    for i in range(1, 5):
        ax.plot([pos[0][0], pos[i][0]], [pos[0][1], pos[i][1]], color=MUTED, linewidth=EDGE_W, zorder=1)
    # Minor fix: the in-node "4" was dropped -- with no other node in the deck carrying a
    # number, it read as a node ID rather than a degree count, and it was one of three
    # places "k = 4" appeared (also below the figure, also in the figcaption). The
    # below-figure label is pushed further down and the axis extended so it clears the
    # bottom leaf's disc.
    #
    # R4 fix (Minor, slide 015): that label sat directly under the BOTTOM leaf (degree 1),
    # not the centre hub the "4" actually counts -- and the figcaption repeated it besides.
    # A leader ties the label to the hub explicitly, routed through the empty lower-right
    # quadrant so it doesn't cross either the bottom or right leaf.
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.72, 1.3)
    clean(ax)  # finalize limits BEFORE measuring the hub's true rendered radius
    # R9 fix ("the one cause", FIXES_R9.md): _star_positions(4)'s own spacing (hub-to-leaf
    # 1.0 data units) fixes the on-slide diameter independent of target_in, and it measured
    # 29.3px against the 34-40px target -- see KONIGSBERG_R's module note for the mechanism.
    # 0.15 clears this spacing with room to spare (ratio 0.15, vs the ~0.25 ceiling).
    R = 0.15
    fit_node_scale(fig, ax, r=R)
    leaf_xy = [pos[i] for i in range(1, 5)]
    draw_nodes(ax, leaf_xy, colors=INK, r=R, zorder=3)
    draw_node(ax, pos[0], color=INK, r=R, zorder=3)
    # R7 fix (item 1 of the fix-first table, slide 015): the old bare ax.annotate aimed its
    # leader at (0, -0.16) -- 13.7px INSIDE the hub's own disc, not at its rim -- and drew at
    # 4px against 7px edges (57% of edge weight), both because nothing ever measured the
    # hub's TRUE rendered radius or checked the leader against it. Routed through
    # place_annotation with node_obstacles=[hub] and edge_obstacles=[every leaf edge]: the
    # target now sits just past the hub's real rim along the same lower-right bearing toward
    # the label (clear of the bottom/right leaf edges, which the corridor was always meant to
    # dodge), and the assertion -- not a hand-picked (x, y) -- is what guarantees it.
    ang = np.deg2rad(-55)  # lower-right bearing toward the label, between the bottom (-90) and
    tip = (R * 1.18 * np.cos(ang), R * 1.18 * np.sin(ang))  # right (0) leaf edges
    node_r_pt = node_radius_pt(ax, R)
    hub_obstacle = [circle_obstacle(pos[0], node_r_pt, color=INK)]
    leaf_edges = [line_obstacle([pos[0], pos[i]], EDGE_W, color=MUTED) for i in range(1, 5)]
    # R9 fix ("free-standing annotations... need their own size bump", FIXES_R9.md): was
    # ANNOT_FS (17pt), ~11.4px on-slide -- under the 16px page-number floor.
    # place_annotation's own obstacle-clearance loop absorbs the larger footprint safely.
    # R12 fix ("the one thing that has not landed"): 24pt was still under the deck-wide 30px
    # body-type floor. place_annotation's own settle loop is what confirms 30 still clears.
    place_annotation(ax, tip, "k = 4", xytext=(0.85, -1.25), obstacles=hub_obstacle,
                      node_obstacles=hub_obstacle, edge_obstacles=leaf_edges,
                      color=MUTED, fontsize=30, ha="center", va="center",
                      clearance_pt=4.0, lw=1.2, name="degree-definition:k=4")
    # R12 fix: save() (bbox_inches="tight") crops to the declared xlim/ylim window, not to
    # what's drawn -- same excess-margin fix as konigsberg-degrees.png's own note.
    save_fit(fig, ax, "degree-definition.png", pad_frac=0.04, pad_min_in=0.15)


def _bracket(ax, center, p1, p2, color=MUTED, gap_deg=16, lw=None, zorder=5, n=40,
             node_obstacles=(), edge_obstacles=(), name="bracket"):
    # R3 fix (Blocker 1): auto-picked the arc's curvature sign so it bulges AWAY from
    # `center` -- hand-picking the sign is what had left parity-even's lower bracket
    # bulging back *into* the node.
    #
    # R4 fix (Major 9): that arc still ran FROM a point sitting ON each edge (p1/p2, at a
    # fixed fraction along it), so for a stretch near each endpoint the bracket and the
    # edge line coincided -- every bracketed edge read as changing colour partway along its
    # own length ("black at x=850, grey at x=880"). A bracket is instead an arc of a circle
    # CENTRED ON THE NODE, at the SAME radius as p1/p2, swept only over the angular range
    # BETWEEN the two edges with a fixed inset (`gap_deg`) from each -- a radial line only
    # touches a circle centred on that same point at the matching angle, and both edges'
    # angles are excluded from the swept range by construction, so the bracket can never
    # sit on top of either edge, regardless of how the two edges are laid out.
    #
    # R7 fix ("the one thing to fix first"): this used to `ax.plot` the arc directly, at a
    # default lw of a full EDGE_W -- the SAME token as the edges it sits beside (parity-odd's
    # bracket, and one of parity-even's two, were both still at this default, undetected
    # because nothing ever checked a bracket's own weight or its clearance from the hub disc
    # it is centred on). Routed through draw_annotation_stroke -- default lw is now 40% of
    # EDGE_W (asserted, not assumed) and the arc's clearance from `node_obstacles` /
    # crossing of `edge_obstacles` is verified against the real renderer.
    lw = (EDGE_W * 0.4) if lw is None else lw
    pts = _bracket_points(center, p1, p2, gap_deg=gap_deg, n=n)
    draw_annotation_stroke(ax, pts, color=color, lw=lw, zorder=zorder,
                            node_obstacles=node_obstacles, edge_obstacles=edge_obstacles,
                            name=name)


def _bracket_points(center, p1, p2, gap_deg=16, n=40):
    # Geometry shared by _bracket (draws it) and any caller that needs the SAME points as an
    # obstacle (e.g. a label anchored right beside its own bracket, not on top of it).
    cx, cy = center
    a1 = np.arctan2(p1[1] - cy, p1[0] - cx)
    a2 = np.arctan2(p2[1] - cy, p2[0] - cx)
    d = (a2 - a1 + np.pi) % (2 * np.pi) - np.pi  # signed short way round from a1 to a2
    r = np.hypot(p1[0] - cx, p1[1] - cy)
    gap = np.deg2rad(gap_deg)
    t = np.linspace(gap, abs(d) - gap, n) * np.sign(d)
    ang = a1 + t
    return np.column_stack([cx + r * np.cos(ang), cy + r * np.sin(ang)])


# R12 fix ("the one thing that has not landed" -- "in-out"/"start"/"end"/"odd"/"even" are
# among the labels the lecturer named by name): hoisted out of fig_parity_even/_odd/_bound's
# three separate local definitions (all 26, all bumped for the same reason -- one constant,
# not three copies that could drift) and raised again now the deck-wide floor is 30px body
# type. Paired with each figure's own save()->save_fit() swap below.
PARITY_ANNOT_FS = 42


def fig_parity_even():
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.28, 1.28)
    clean(ax)
    fit_node_scale(fig, ax)
    pos = _star_positions(4, start=45)
    # deck-wide structural edge colour is MUTED (R4 Minor: Part Three drew edges black
    # while Parts Five-Seven drew them annotation gray; MUTED is what the majority of the
    # deck already used, so parity-even/odd move to match rather than the other way round).
    for i in range(1, 5):
        ax.plot([pos[0][0], pos[i][0]], [pos[0][1], pos[i][1]], color=MUTED, linewidth=EDGE_W, zorder=1)
    # R3 fix (Blocker 1): near-points pulled further out (0.42 -> 0.55 of the way to each
    # leaf) so both brackets clear the node disc with visible daylight, not a graze.
    near = {i: (pos[0][0] + 0.55 * (pos[i][0] - pos[0][0]), pos[0][1] + 0.55 * (pos[i][1] - pos[0][1]))
            for i in range(1, 5)}
    # R5 fix (Major 12): the bracket used the SAME token as the edges it ties together --
    # EDGE_W gray -- so it read as a fifth edge crossing the middle, not a mark distinct
    # from the graph. Distinctly lighter settles it as annotation, not structure -- same
    # move as the self-loop's ticks.
    #
    # R7 fix ("the one thing to fix first"): was EDGE_W*0.5 -- OVER draw_annotation_stroke's
    # 40%-of-EDGE_W cap (this bracket now routes through it, below), and one of the two
    # (bottom) had never actually been checked against the hub disc it curves around.
    bracket_lw = EDGE_W * 0.4
    node_r_pt = node_radius_pt(ax)
    node_obs = [circle_obstacle(pos[i], node_r_pt, color=INK) for i in pos]
    edge_obs = {i: line_obstacle([pos[0], pos[i]], EDGE_W, color=MUTED) for i in range(1, 5)}
    obstacles = node_obs + list(edge_obs.values())

    top_pts = _bracket_points(pos[0], near[1], near[2])
    _bracket(ax, pos[0], near[1], near[2], lw=bracket_lw, node_obstacles=node_obs,
             edge_obstacles=[edge_obs[3], edge_obs[4]], name="parity-even:bracket-top")
    bot_pts = _bracket_points(pos[0], near[3], near[4])
    _bracket(ax, pos[0], near[3], near[4], lw=bracket_lw, node_obstacles=node_obs,
             edge_obstacles=[edge_obs[1], edge_obs[2]], name="parity-even:bracket-bot")
    # R5 fix (Major 12): each "in-out" now anchors at ITS OWN bracket's peak (with the arc
    # itself as an obstacle, plus every node/edge) instead of sitting ~95px away at the
    # frame's top/bottom edge with a node in between -- bring the label to the mark it names.
    top_peak = tuple(top_pts[len(top_pts) // 2])
    bot_peak = tuple(bot_pts[len(bot_pts) // 2])
    # R9 fix ("free-standing annotations... need their own size bump", FIXES_R9.md): ANNOT_FS
    # (17pt) on this figure's own canvas measured ~11px on-slide, under the 16px page-number
    # floor -- these are free-standing (not node-interior), so they don't inherit the r-boost
    # fix's benefit the way fixed-size node labels do. Bumped directly (see the module-level
    # PARITY_ANNOT_FS for the R12 follow-up).
    place_label(ax, (top_peak[0], top_peak[1] + 0.22), "in–out",
                obstacles=obstacles + [line_obstacle(top_pts, bracket_lw, color=MUTED)],
                color=MUTED, fontsize=PARITY_ANNOT_FS, ha="center", va="bottom", clearance_pt=3.0,
                zorder=6, name="parity-even:in-out-top")
    place_label(ax, (bot_peak[0], bot_peak[1] - 0.22), "in–out",
                obstacles=obstacles + [line_obstacle(bot_pts, bracket_lw, color=MUTED)],
                color=MUTED, fontsize=PARITY_ANNOT_FS, ha="center", va="top", clearance_pt=3.0,
                zorder=6, name="parity-even:in-out-bot")
    draw_nodes(ax, [pos[i] for i in range(5)], colors=INK, zorder=3)
    # title removed -- duplicated the figcaption verbatim
    # R12 fix ("the one thing that has not landed"): save() (bbox_inches="tight") crops to
    # the declared xlim/ylim window, not to what's drawn -- same excess-margin fix as
    # konigsberg-degrees.png's own note.
    save_fit(fig, ax, "parity-even.png", pad_frac=0.04, pad_min_in=0.15)


def fig_parity_odd():
    fig, ax = plt.subplots(figsize=(4.8, 4.4))
    # leaves at 60 / 180 / 300 deg so none sits under the bracket label at the top
    pos = _star_positions(3, start=60)
    # xlim/ylim/aspect finalized BEFORE any place_label/draw_annotation_stroke call, since
    # both measure the real (post-aspect) data<->pixel transform.
    ax.set_xlim(-1.6, 1.95)
    ax.set_ylim(-1.45, 1.25)
    clean(ax)
    fit_node_scale(fig, ax)
    # 1,2 = bracketed pair (upper-right / left); 3 = leftover (lower-right). MUTED, not
    # INK -- deck-wide structural edge colour (see fig_parity_even).
    ax.plot([pos[0][0], pos[1][0]], [pos[0][1], pos[1][1]], color=MUTED, linewidth=EDGE_W, zorder=1)
    ax.plot([pos[0][0], pos[2][0]], [pos[0][1], pos[2][1]], color=MUTED, linewidth=EDGE_W, zorder=1)
    # only the leftover *edge* is accent2 -- the node at its far end stays INK so students
    # don't read the node itself as "the leftover thing" (F1 fix).
    ax.plot([pos[0][0], pos[3][0]], [pos[0][1], pos[3][1]], color=ACCENT2, linewidth=4.5, zorder=1)
    near = {i: (pos[0][0] + 0.55 * (pos[i][0] - pos[0][0]), pos[0][1] + 0.55 * (pos[i][1] - pos[0][1]))
            for i in range(1, 4)}
    # R7 fix ("the one thing to fix first"): this bracket used to draw at the bare default
    # (full EDGE_W -- exactly edge weight) with no clearance/crossing check at all. Routed
    # through _bracket's node/edge obstacles like parity-even's pair.
    node_r_pt_odd = node_radius_pt(ax)
    odd_node_obs = [circle_obstacle(pos[i], node_r_pt_odd, color=INK) for i in pos]
    odd_leftover_edge = line_obstacle([pos[0], pos[3]], 4.5, color=ACCENT2)
    _bracket(ax, pos[0], near[1], near[2], node_obstacles=odd_node_obs,
             edge_obstacles=[odd_leftover_edge], name="parity-odd:bracket")
    # label sits on the bisector of the bracketed pair, clear of every node
    # R9 fix ("free-standing annotations... need their own size bump", FIXES_R9.md): see
    # parity-even's PARITY_ANNOT_FS note -- same fix, same reason (now a module constant).
    bisector = np.deg2rad((60 + 180) / 2)
    lx, ly = 1.05 * np.cos(bisector), 1.05 * np.sin(bisector)
    ax.text(lx, ly, "in–out", ha="center", va="center", color=MUTED, fontsize=PARITY_ANNOT_FS, zorder=6)
    draw_nodes(ax, [pos[0], pos[1], pos[2], pos[3]], colors=INK, zorder=3)
    # R3 fix (Blocker 2): anchored just past leaf 3 (not at the edge midpoint) with
    # ha="left", va="top" so the text grows away from both the centre disc and the
    # accent-2 stroke instead of centering back over them; annotation gray, not
    # accent-2-on-accent-2 (the exact defect already fixed for the Euler examples).
    #
    # R7 fix (Minor, slide 019): a hand-picked (0.22, -0.19) offset still left the "l"
    # ascender grazing the disc rim (0.8px clearance, measured) -- routed through place_label
    # against the real node discs and edges so the settle loop -- not another hand-picked
    # number -- is what guarantees clearance.
    node_obs_odd = [circle_obstacle(pos[i], node_r_pt_odd, color=INK) for i in pos]
    edge_obs_odd = [line_obstacle([pos[0], pos[1]], EDGE_W, color=MUTED),
                     line_obstacle([pos[0], pos[2]], EDGE_W, color=MUTED),
                     odd_leftover_edge]
    place_label(ax, (pos[3][0] + 0.22, pos[3][1] - 0.19), "left over",
                obstacles=node_obs_odd + edge_obs_odd, color=MUTED, fontsize=PARITY_ANNOT_FS,
                ha="left", va="top", clearance_pt=3.0, zorder=6, name="parity-odd:left-over")
    # R12 fix: see fig_parity_even -- same save()->save_fit swap.
    save_fit(fig, ax, "parity-odd.png", pad_frac=0.04, pad_min_in=0.15)


def fig_parity_bound():
    # NEW (Major 9): slide 020 states the parity bound ("a walk has at most two odd
    # nodes") with no visual at all -- last text baseline sits well above the frame's
    # bottom half. A genuine simple walk makes the bound visible by construction: every
    # INTERIOR node has exactly two incident walk-edges (even), while the two ENDPOINTS
    # -- the only nodes allowed to be odd -- are marked start/end in accent-2.
    #
    # R4 fix (Major 8): only P2 carried the pairing bracket and neither end was labelled
    # odd, so the figure's own claim ("<=2 odd") was nowhere actually visible -- a reader
    # saw one bracketed node and two coloured dots, not "every interior node pairs up, only
    # the ends don't." Every interior node now gets the same bracket (one shared "even"
    # label states what the repeated motif means, so it isn't said four times); both ends
    # get "odd" under their start/end label.
    #
    # R4 fix (Policy 1): edges back to the deck's standard structural colour (MUTED) --
    # accent-2 here means exactly one thing, the two endpoints.
    path = ["S", "P1", "P2", "P3", "P4", "E"]
    pos = {"S": (0, 0), "P1": (0.85, 0.55), "P2": (1.7, 0), "P3": (2.55, 0.55), "P4": (3.4, 0), "E": (4.25, 0.55)}
    edges = list(zip(path, path[1:]))
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.set_xlim(-0.55, 4.8)
    ax.set_ylim(-1.15, 1.35)
    clean(ax)
    # R9 fix ("the one cause", FIXES_R9.md): this chain's own spacing (~1.01 data units)
    # fixes the on-slide diameter independent of target_in -- measured 21.2px against the
    # 34-40px target, the worst offender in the deck (see KONIGSBERG_R's module note for the
    # mechanism). The next block's bracket arcs (near1/near2 at a FIXED 0.62 fraction of each
    # ~1.01-unit edge, i.e. ~0.63 data units from the hub) were tuned against the old,
    # smaller disc -- 0.19 (ratio 0.188, still under the ~0.25 crowding ceiling, and well
    # under the 0.63 the brackets sit at) leaves them real daylight, verified by
    # draw_annotation_stroke's own node-clearance assertion below, not just asserted here.
    R = 0.19
    fit_node_scale(fig, ax, r=R)
    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=MUTED,
                 linewidth=EDGE_W, zorder=1, solid_capstyle="round")

    # R6 fix (Blocker 3, historical): this 6-node chain used to need a hand-picked
    # NODE_SCALE=0.55 shrink because the old scatter-derived node size, tuned against a
    # DIFFERENT figure's own xlim, covered ~48% of this chain's ~1.01-data-unit spacing --
    # discs nearly touching. NODE_R (0.12 data units, deck-wide, see the module note above
    # it) was picked with exactly this chain's spacing as one of its constraints, so it
    # already leaves real daylight here with no per-figure scale-down.
    colors = {n: (ACCENT2 if n in ("S", "E") else INK) for n in pos}
    draw_nodes(ax, pos, colors=colors, r=R, zorder=3)

    node_r_pt = node_radius_pt(ax, R)
    obstacles = [circle_obstacle(pos[n], node_r_pt, color=colors[n]) for n in pos]
    for u, v in edges:
        obstacles.append(line_obstacle([pos[u], pos[v]], EDGE_W, color=MUTED))

    # R9 fix ("free-standing annotations... need their own size bump", FIXES_R9.md): the old
    # ANNOT_FS-2/-5 sizes measured ~9px/7px on-slide, under the 16px page-number floor --
    # these are free-standing, so they don't inherit the r-boost fix's benefit the way
    # node-interior labels do. Bumped directly, same size for both so "odd" doesn't read as
    # a lesser afterthought under "start"/"end" (now a module constant, see PARITY_ANNOT_FS).
    # R5 fix (Major 10): "start"/"end" were clipped by their own accent-2 discs -- a fixed
    # 0.34 offset stopped clearing once the node's true rendered radius (see node_r_pt) grew
    # past it. Routed through place_label so it can't happen again.
    for n, txt in (("S", "start"), ("E", "end")):
        x, y = pos[n]
        dy, va = (-0.34, "top") if n == "S" else (0.34, "bottom")
        label_t = place_label(ax, (x, y + dy), txt, obstacles=obstacles, color=ACCENT2,
                               fontsize=PARITY_ANNOT_FS, ha="center", va=va, clearance_pt=3.0,
                               zorder=5, name=f"parity-bound:{txt}")
        # "odd" stacks under/over "start"/"end" -- once THOSE are pushed clear of the disc
        # (above), a fixed offset from the node can no longer be trusted to also clear
        # them; checked against the settled label itself via text_obstacle.
        dy2 = dy - 0.30 if n == "S" else dy + 0.30
        place_label(ax, (x, y + dy2), "odd", obstacles=obstacles + [text_obstacle(label_t, color=ACCENT2)],
                    color=ACCENT2, fontsize=PARITY_ANNOT_FS, ha="center", va=va, clearance_pt=3.0,
                    zorder=5, name=f"parity-bound:odd-{n}")

    # R5 fix (Major 11): near1/near2 sat at 0.4 of the way along a ~1-unit edge -- close
    # enough to the node's true radius that the bracket arc (drawn at THAT radius, see
    # _bracket) hugged the disc boundary and read as rim-light, not a bracket tying two
    # edges. Pushed out to 0.62 (parity-even's equivalent fix went 0.42 -> 0.55 for a
    # longer edge; this path's edges are shorter, so it needs to go further in fraction
    # terms to clear the same absolute radius) for real daylight between disc and arc.
    # R5 fix (Major 11): every interior node's bracket now gets its OWN "even" label
    # (previously only P2's did, so the figure's own claim -- every interior node pairs up
    # -- was only demonstrated once out of four times) -- placed via place_label so each
    # clears its own bracket, its node, and the path's edges.
    #
    # R6 fix (Blocker 3): the bracket arc now goes through draw_annotation_stroke (the R6
    # "missing assertion" fix) instead of a bare _bracket() call -- drawn at 40% of EDGE_W
    # (was full EDGE_W, the same token as the edges it sits beside) and verified, not just
    # eyeballed, to float clear of EVERY node disc (not only its own hub) and to cross no
    # edge other than the two it is pairing. Node discs are the smaller NODE_SCALE ones
    # (see above) -- without that shrink this assertion would fail by construction, which is
    # exactly the bug the old figure shipped with.
    node_discs = [circle_obstacle(pos[n], node_r_pt) for n in pos]
    for node in ("P1", "P2", "P3", "P4"):
        i = path.index(node)
        left, right = path[i - 1], path[i + 1]
        hx, hy = pos[node]
        near1 = (hx + 0.62 * (pos[left][0] - hx), hy + 0.62 * (pos[left][1] - hy))
        near2 = (hx + 0.62 * (pos[right][0] - hx), hy + 0.62 * (pos[right][1] - hy))
        arc_pts = _bracket_points((hx, hy), near1, near2)
        other_edges = [line_obstacle([pos[u], pos[v]], EDGE_W)
                       for (u, v) in edges if node not in (u, v)]
        draw_annotation_stroke(ax, arc_pts, node_obstacles=node_discs, edge_obstacles=other_edges,
                                lw=EDGE_W * 0.4, zorder=5, name=f"parity-bound:even-arc-{node}")
        is_peak = hy > 0.4  # P1/P3 (peaks, y=0.55): bracket bulges BELOW; P2/P4 (valleys): above
        va = "top" if is_peak else "bottom"
        # R7 fix (item 16, slide 020): the old fixed (hx, hy +/- 0.40) anchor sat INSIDE the
        # arc's own radius (~0.62 of an ~1.0-unit edge), on the SAME angular bisector the arc
        # bulges toward -- i.e. directly under the ink, not beside it -- and the arc was never
        # even passed as an obstacle, so place_label had no way to know to move. Struck
        # through on all four, on the one slide whose entire point is parity. Anchored instead
        # at the arc's own peak sample (its true rendered midpoint) and pushed further out
        # along that SAME radial bearing -- beyond the arc, not under it -- with the arc itself
        # now a real obstacle so the settle loop, not another hand-picked offset, guarantees
        # clearance.
        peak_pt = arc_pts[len(arc_pts) // 2]
        d = np.array(peak_pt) - np.array((hx, hy))
        d = d / np.linalg.norm(d)
        anchor = (hx + d[0] * 1.0, hy + d[1] * 1.0)
        place_label(ax, anchor, "even",
                    obstacles=obstacles + [line_obstacle(arc_pts, EDGE_W * 0.4, color=MUTED)],
                    color=MUTED, fontsize=PARITY_ANNOT_FS, ha="center", va=va, clearance_pt=4.0,
                    zorder=6, name=f"parity-bound:even-{node}")
    # R12 fix: save() (bbox_inches="tight") crops to the declared xlim/ylim window, not to
    # what's drawn -- same excess-margin fix as konigsberg-degrees.png's own note. Also fixes
    # a node-diameter regression from the deck side: this slide moved out of a `.cols` column
    # to full-width (container 537 -> 1120px) since the last render, which raises `scale`
    # enough that the OLD, tighter crop (h=1073px) pushed the node to 53.1px, just over the
    # 52px ceiling -- a bit more pad_min_in restores headroom under both caps at once.
    save_fit(fig, ax, "parity-bound.png", pad_frac=0.04, pad_min_in=0.6)


def fig_konigsberg_blank():
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    k_limits(ax, xpad=1.1)
    fit_node_scale(fig, ax, r=KONIGSBERG_R)
    draw_kedges(ax)
    draw_knodes(ax, r=KONIGSBERG_R, label_fs=KONIGSBERG_LABEL_FS)
    # R10 fix (FIXES_R10.md): see fig_abstraction_2_nodes -- same save()->save_fit swap
    # (measured 34% ink under the old k_limits-window crop).
    # R12 fix: see fig_abstraction_2_nodes -- same pad_min_in cut (1.5in -> 0.5in).
    save_fit(fig, ax, "konigsberg-blank.png", pad_frac=0.08, pad_min_in=0.5)


# Outward direction for a degree label placed just outside each node -- KPOS is the unit
# diamond, so "outward" is simply each node's own unit vector from the centre.
K_OUTWARD = {"N": (0, 1), "S": (0, -1), "A": (-1, 0), "B": (1, 0)}
K_OUTWARD_ALIGN = {"N": ("center", "bottom"), "S": ("center", "top"),
                    "A": ("right", "center"), "B": ("left", "center")}


def fig_konigsberg_degrees():
    labels = {"N": "3", "S": "3", "A": "5", "B": "3"}
    deg = kedge_degrees()
    assert {n: str(d) for n, d in deg.items()} == labels, f"degrees {deg} != labels {labels}"
    assert all(d % 2 == 1 for d in deg.values()), "all four Konigsberg landmasses must be odd"
    fig, ax = plt.subplots(figsize=(5.2, 5.6))
    # xlim/ylim/aspect finalized BEFORE any place_label call, since label placement measures
    # the real (post-aspect) data<->pixel transform.
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-1.95, 1.85)
    clean(ax)
    fit_node_scale(fig, ax, r=KONIGSBERG_R)
    draw_kedges(ax)
    # R3 fix (Major 12/13): keep the N/A/B/S letters INSIDE each node (every other
    # Konigsberg figure -- 008-011, 021 -- uses those letters, and slide 021 has students
    # count degrees on the letter-labelled blank; swapping letters for bare digit values
    # here broke that cross-check). Degrees go just OUTSIDE each node instead, in accent-2
    # to match the node fill. The old bottom "all four odd" annotation is dropped -- it
    # repeated the figcaption, which repeats the bullet list (duplicate-caption fix).
    node_colors = {n: ACCENT2 for n in "NSAB"}
    draw_knodes(ax, colors=node_colors, r=KONIGSBERG_R, label_fs=KONIGSBERG_LABEL_FS)
    # R5 fix (Major 9): these degree numerals are ACCENT2 sitting right outside an ACCENT2
    # disc -- exactly the "recurring failure" pattern the review flagged five times. Routed
    # through place_label: it starts at the same 0.34-out offset as before, but is now
    # measured against the disc's TRUE rendered radius and nudged/raises rather than
    # trusting the hand-picked 0.34 to still clear it.
    #
    # R9 fix (Blocker 7 + "the one cause"): KONIGSBERG_R replaces the deck-wide NODE_R for
    # this whole family (see its own module-level note) -- the outward offset scales with it
    # (0.34 was picked for the old, smaller radius) so the numeral starts the same fraction
    # of a node-radius clear of the bigger disc, and DEGREE_FS replaces ANNOT_FS so the
    # numeral itself is legible: measured on the rendered slide, the old ANNOT_FS=17
    # numerals were 5-6px against a 16px page number; this figure's on-slide scale roughly
    # tracks the KONIGSBERG_R boost (see the module note), so a fixed point bump on top of
    # that -- not relying on the boost alone -- is what clears the floor with margin.
    obstacles = k_obstacles(ax, node_colors=node_colors, r=KONIGSBERG_R)
    off = 0.34 * (KONIGSBERG_R / NODE_R)
    for n, d in labels.items():
        ox, oy = K_OUTWARD[n]
        ha, va = K_OUTWARD_ALIGN[n]
        place_label(ax, (KPOS[n][0] + off * ox, KPOS[n][1] + off * oy), d, obstacles=obstacles,
                    color=ACCENT2, fontsize=KONIGSBERG_DEGREE_FS, ha=ha, va=va, fontweight="bold", zorder=5,
                    clearance_pt=3.0, name=f"konigsberg-degrees:{n}")
    # R12 fix ("the one thing that has not landed"): was save() (bbox_inches="tight"), which
    # crops to the DECLARED xlim/ylim window, not to what's actually drawn in it -- the same
    # excess-margin problem fig_abstraction_2_nodes' own note describes, just reached via a
    # generous xlim/ylim instead of a big pad_min_in. save_fit crops to the true rendered
    # extent (letters, degree numerals and all -- both are real Text artists in ax.texts, so
    # _content_px_bbox already includes them) with a small pad instead.
    save_fit(fig, ax, "konigsberg-degrees.png", pad_frac=0.03, pad_min_in=0.15)


def fig_konigsberg_bombed():
    removed = {"NA2", "SA2"}
    labels = {"N": "2", "S": "2", "A": "3", "B": "3"}
    deg = kedge_degrees(removed)
    assert {n: str(d) for n, d in deg.items()} == labels, f"degrees {deg} != labels {labels}"
    odd = {n for n, d in deg.items() if d % 2 == 1}
    assert odd == {"A", "B"}, f"removing {removed} should leave exactly A, B odd; got {odd}"
    # R5 fix (Blocker 1): _arc3_points had the sign of matplotlib's own arc3 control-point
    # offset backwards, so a "removed" edge's dashed replica traced the SAME path as the
    # live parallel bridge instead of mirroring it -- five solid edges, no visible dashes.
    # Fixed at the source (_arc3_points); this assertion is the regression guard so it can
    # never silently come back.
    assert_dashed_distinct_from_live(removed)
    fig, ax = plt.subplots(figsize=(5.2, 5.2))
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-1.85, 1.85)
    clean(ax)
    fit_node_scale(fig, ax, r=KONIGSBERG_R)
    draw_kedges(ax, removed=removed)
    # R4 fix (Blocker 4): this used to swap the N/A/B/S letters for the bare degree VALUES
    # inside the disc -- but slide 026 (the question this slide answers, konigsberg-degrees
    # .png) puts the letters inside and the degrees outside, and slide 021 has students
    # count degrees on a letter-labelled blank. A student who worked out "remove one A-N
    # and one A-S" from the letters couldn't then check their answer against this figure.
    # Letters back inside (draw_knodes' default); degrees outside via the same K_OUTWARD
    # placement as konigsberg-degrees.png, coloured to match: accent-2 (still odd) for
    # A/B, MUTED (now even) for N/S -- accent-2 keeps its one meaning in this figure,
    # "still odd after the bombing."
    node_colors = {"N": INK, "S": INK, "A": ACCENT2, "B": ACCENT2}
    draw_knodes(ax, colors=node_colors, r=KONIGSBERG_R, label_fs=KONIGSBERG_LABEL_FS)
    obstacles = k_obstacles(ax, node_colors=node_colors, r=KONIGSBERG_R)
    off = 0.34 * (KONIGSBERG_R / NODE_R)
    for n, d in labels.items():
        ox, oy = K_OUTWARD[n]
        ha, va = K_OUTWARD_ALIGN[n]
        color = ACCENT2 if n in odd else MUTED
        place_label(ax, (KPOS[n][0] + off * ox, KPOS[n][1] + off * oy), d, obstacles=obstacles,
                    color=color, fontsize=KONIGSBERG_DEGREE_FS, ha=ha, va=va, fontweight="bold", zorder=5,
                    clearance_pt=3.0, name=f"konigsberg-bombed:degree-{n}")
    # R5 fix (Blocker 1): "destroyed" now gets ONE label PER removed bridge (there are two).
    #
    # R7 fix ("the one thing to fix first", table row 027): R5's version used a leader from
    # the open exterior margin (xytext=(-1.65, +-1.05)) to each dash's own peak -- but NA2/SA2
    # are the INNER of each parallel pair (rad=-0.30, curving back toward the centre; NA1/SA1
    # at rad=+0.30 bulge further OUT). Checked with a real crossing assertion for the first
    # time this round: NA1 sits physically between the exterior margin and NA2 for its ENTIRE
    # length, so no straight leader from outside the diamond can reach NA2 without crossing
    # it (confirmed by sweeping several exterior anchors -- all fail the same way; this is a
    # geometric dead end, not a bad offset). Per the spec's fallback: no leader. Each label
    # sits directly beside its own dash, inside the diamond where NA2/SA2 actually curve,
    # settled by place_label against every node and every bridge (live and dashed) so it
    # can't drift onto anything else instead.
    na2_xy = tuple(_arc3_points(KPOS["N"], KPOS["A"], -0.30, n=101)[50])
    sa2_xy = tuple(_arc3_points(KPOS["S"], KPOS["A"], -0.30, n=101)[50])
    # R9 fix (Blocker 4): NA2 and SA2 are NOT symmetric the way the R7 comment above assumed
    # -- measured directly (distance from the diamond's centre): NA2 sits at 0.49 (the INNER
    # arc of its pair, curving toward the centre) while SA2 sits at 0.92 (the OUTER arc,
    # curving away) -- NA1/SA1 are the mirror image (0.92 / 0.49). The old "-0.27, +-0.27"
    # offset for both assumed they curved the same way: for SA2 (genuinely outer) it pushed
    # further outward, clear of the inner SA1 (74px away, fine); for NA2 (actually inner) the
    # SAME outward-pointing offset pushed it toward the diamond's exterior margin -- straight
    # at NA1, the outer live bridge -- landing 2.8px from it. NA2's offset is flipped here to
    # continue INWARD (the concave side its own arc already bulges toward), symmetric with
    # how SA2's offset continues OUTWARD -- both now move away from their respective live
    # neighbour instead of toward it.
    # R10 fix (Major 7 -- was ANNOT_FS = 17pt, measured 12px on-slide; Minor -- the two
    # labels' clearance_pt differed 9.0 vs 4.0 for no stated reason, landing 34.0px vs 10.6px
    # clear of their own dash, a 3x gap between two labels doing the identical job).
    # fontsize bumped to 23pt (calibrated off the 12px/17pt measurement to land ~16px on-slide
    # -- NOT this file's usual 30pt: NA2 sits in the narrow gap between the two live/dashed
    # bridge arcs, the tightest spot in the whole family, and 30pt has no room to settle
    # there). clearance_pt equalised to 5.0 so both labels settle the same distance out.
    #
    # R12 fix ("the one thing that has not landed" -- "destroyed" is one of the labels the
    # lecturer named by name): 23pt was still under the floor once the deck-wide 30px body
    # type set it. 26pt is the biggest place_label's own settle loop still finds room for in
    # NA2's tight gap (checked directly: 27 raises RuntimeError, no clear position found)
    # -- and paired with the save()->save_fit swap below (same excess-margin fix as
    # konigsberg-degrees.png), 26pt clears TEXT_LEGIBLE_PX with margin.
    place_label(ax, (na2_xy[0] + 0.16, na2_xy[1] - 0.08), "destroyed", obstacles=obstacles,
                color=MUTED, fontsize=29, ha="left", va="center", clearance_pt=5.0,
                name="konigsberg-bombed:destroyed-NA2")
    place_label(ax, (sa2_xy[0] - 0.27, sa2_xy[1] - 0.27), "destroyed", obstacles=obstacles,
                color=MUTED, fontsize=29, ha="right", va="center", clearance_pt=5.0,
                name="konigsberg-bombed:destroyed-SA2")
    # "two odd -> now possible" removed -- it is the figcaption verbatim.
    # R12 fix: save() (bbox_inches="tight") crops to the declared xlim/ylim window, not to
    # what's drawn -- see konigsberg-degrees.png's own note, same swap, same reason.
    save_fit(fig, ax, "konigsberg-bombed.png", pad_frac=0.015, pad_min_in=0.08)


# R12 fix: "start"/"end"/"start = end" -- the labels this figure family exists to show --
# were splitting between ANNOT_FS (17pt, the odd_labels path) and a bare 30 (the hub_label
# path). One constant for both.
TRACE_LABEL_FS = 36


def _trace_graph(pos, edges, trail, odd_labels=None, label_offsets=None, hub_label=None, width_in=5.2,
                  xlim=None, ylim=None):
    # Label color is annotation gray, not ACCENT2 -- the traced route and the node fills
    # are already ACCENT2, so ACCENT2 text sitting on an ACCENT2 edge was unreadable
    # (F3 fix). Offsets are per-node so a label never sits on top of an incident edge.
    #
    # R4 fix (Policy 1): edges back to the deck's standard structural colour (MUTED) --
    # ACCENT2 previously meant "every edge", which is no signal at all. In this figure
    # family accent-2 now means exactly one thing: an ODD-degree node (the two ends of a
    # path). A node passed as `hub_label` is EVEN (Euler-circuit's start=end node has
    # degree 4) and must not be coloured accent-2 for that -- see fig_euler_circuit_example.
    fig, ax = plt.subplots(figsize=(width_in, 4.6))
    # R7 fix (found routing the hub ring through draw_annotation_stroke): both callers used
    # to set xlim/ylim on the returned `ax` AFTER this function returned -- so the ring drawn
    # below (when hub_label is given) measured its own clearance against matplotlib's
    # autoscaled DEFAULT view, not the view the caller actually saves. Both callers now pass
    # `xlim`/`ylim` in directly (required -- see the assert below) so every measurement in
    # this function, including fit_node_scale's, uses the real FINAL transform throughout.
    assert xlim is not None and ylim is not None, "_trace_graph: pass the final xlim/ylim in"
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    clean(ax)  # aspect must be locked before any measurement below (see comment above)
    fit_node_scale(fig, ax)
    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=MUTED,
                 linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    nodes = list(pos.keys())
    colors = [ACCENT2 if n in (odd_labels or {}) else INK for n in nodes]
    draw_nodes(ax, pos, colors=dict(zip(nodes, colors)), zorder=3)
    if odd_labels:
        # R12 fix ("the one thing that has not landed" -- "start"/"end" here is the label
        # the lecturer named by name, and the worst offender two reviewers measured: a bare
        # ax.text at ANNOT_FS with no clearance check). Routed through place_label like every
        # other free-standing annotation in this file: TRACE_LABEL_FS instead of ANNOT_FS,
        # and the settle loop -- not the hand-picked offsets alone -- guarantees it clears
        # every node disc and edge, not just the one it was tuned against by eye.
        node_r_pt_odd = node_radius_pt(ax)
        odd_obstacles = [circle_obstacle(pos[n], node_r_pt_odd,
                                          color=(ACCENT2 if n in odd_labels else INK))
                          for n in nodes]
        odd_obstacles += [line_obstacle([pos[u], pos[v]], EDGE_W, color=MUTED) for u, v in edges]
        for n, txt in odd_labels.items():
            x, y = pos[n]
            dx, dy = (label_offsets or {}).get(n, (0, -0.32))
            ha = "center" if dx == 0 else ("left" if dx > 0 else "right")
            va = "center" if dy == 0 else ("bottom" if dy > 0 else "top")
            place_label(ax, (x + dx, y + dy), txt, obstacles=odd_obstacles, color=MUTED,
                        fontsize=TRACE_LABEL_FS, ha=ha, va=va, clearance_pt=3.0, zorder=4,
                        name=f"trace-graph:{n}-odd-label")
    if hub_label:
        # A thin ring, not an accent-2 fill -- this node is EVEN, so it must not carry the
        # "odd" colour. The ring marks "this is the node that's both start and end"; the
        # text sits well clear of the disc and of the edges the ring itself sits inside of.
        x, y = pos[hub_label]
        # R7 fix ("the one thing to fix first"): routed through draw_annotation_stroke (as a
        # sampled circle) instead of a bare add_patch -- its clearance from the node disc it
        # encircles, and from every edge, is now asserted against the real renderer instead
        # of assumed from "a touch larger than the node disc". lw capped at 40% of EDGE_W
        # (was a flat 3pt, at or above edge weight for some callers' figsizes).
        node_r_pt_hub = node_radius_pt(ax)
        hub_edges = [line_obstacle([pos[u], pos[v]], EDGE_W, color=MUTED)
                     for (u, v) in edges if hub_label not in (u, v)]
        draw_ring(ax, (x, y), k=1.7, color=ACCENT2, zorder=5,
                  node_obstacles=[circle_obstacle((x, y), node_r_pt_hub)],
                  edge_obstacles=hub_edges, name="trace-graph:hub-ring")
        # R10 fix (FIXES_R10.md, Blocker 5): the label used to sit 0.55-0.62 data units below
        # the ring with no leader -- measured on slide 025 at 58.5px clear of it, 8px tall,
        # with nothing else on the slide saying what the ring means. This label IS the ring's
        # only gloss ("start = end" -- the circuit starts and ends here), so it has to read as
        # attached to the ring, not floating nearby. Default anchor is now directly beside the
        # ring (this family's own edges run in diagonal pairs, so straight left/right/up/down
        # are the gaps between them -- asserted, not assumed, via place_label's own obstacle
        # check against the ring and every edge); `label_offsets` can still override per
        # caller. Sized to clear the page-number floor with real margin, not just past it.
        ring_r_pt = 1.7 * node_r_pt_hub
        text_obstacles = [circle_obstacle((x, y), ring_r_pt)] + [
            line_obstacle([pos[u], pos[v]], EDGE_W, color=MUTED) for u, v in edges
        ]
        if label_offsets and hub_label in label_offsets:
            dx, dy = label_offsets[hub_label]
            anchor = (x + dx, y + dy)
            ha = "center" if dx == 0 else ("left" if dx > 0 else "right")
            va = "center" if dy == 0 else ("bottom" if dy > 0 else "top")
        else:
            # Below, not beside: the text is wide and short, and straight down is the widest
            # of the four clear gaps (114 degrees, between the two lower diagonal edges) --
            # room enough for the whole phrase without place_label needing more than a small
            # nudge, unlike either side gap (which a wide horizontal string can run past into
            # an upper edge before place_label finds daylight).
            _, dpp_y = data_units_per_point(ax)
            anchor = (x, y - ring_r_pt * dpp_y * 1.3)
            ha, va = "center", "top"
        place_label(ax, anchor, "start = end", obstacles=text_obstacles, color=MUTED,
                    fontsize=TRACE_LABEL_FS, ha=ha, va=va, clearance_pt=4.0, zorder=6,
                    name=f"trace-graph:{hub_label}-hub-label")
    clean(ax)
    return fig, ax


def fig_euler_path_example():
    pos = {"BL": (0, 0), "BR": (1, 0), "TL": (0, 1), "TR": (1, 1), "T": (0.5, 1.7)}
    edges = [("BL", "BR"), ("BR", "TR"), ("TR", "T"), ("T", "TL"), ("TL", "BL"), ("TL", "TR")]
    # TL's incident edges run straight down and straight right from it, so a label
    # placed *below* TL sits on the TL-BL edge; offset sideways instead. Same for TR.
    fig, ax = _trace_graph(pos, edges, None, odd_labels={"TL": "start", "TR": "end"},
                            label_offsets={"TL": (-0.34, 0), "TR": (0.34, 0)},
                            xlim=(-0.85, 1.85), ylim=(-0.25, 1.9))
    # R12 fix ("the one thing that has not landed"): save() (bbox_inches="tight") crops to
    # the declared xlim/ylim window, not to what's drawn -- same excess-margin fix as
    # konigsberg-degrees.png's own note.
    save_fit(fig, ax, "euler-path-example.png", pad_frac=0.04, pad_min_in=0.15)


def fig_euler_circuit_example():
    # R4 fix (Policy 1): C has degree 4 -- EVEN -- so it must not be accent-2 (that colour
    # is reserved for odd nodes elsewhere in this figure family); see _trace_graph.
    #
    # R10 fix (FIXES_R10.md, Blocker 5): "start = end" now uses _trace_graph's default
    # placement (right beside the ring -- see that function's own note) instead of a
    # hand-picked offset below it, so no more label_offsets override here.
    pos = {"C": (0, 0), "L1": (-1, 0.65), "L2": (-1, -0.65), "R1": (1, 0.65), "R2": (1, -0.65)}
    edges = [("C", "L1"), ("L1", "L2"), ("L2", "C"), ("C", "R1"), ("R1", "R2"), ("R2", "C")]
    fig, ax = _trace_graph(pos, edges, None, hub_label="C",
                            xlim=(-1.55, 1.55), ylim=(-1.35, 1.15))
    # R12 fix: see fig_euler_path_example -- same save()->save_fit swap.
    save_fit(fig, ax, "euler-circuit-example.png", pad_frac=0.08, pad_min_in=0.4)


# ===========================================================================
# Part 4 -- vocabulary
# ===========================================================================
CAMPUS_POS = {"Dorm": (0, 1), "Cafe": (1, 1), "Lib": (1, 0), "Gym": (0, 0)}
CAMPUS_EDGES = [("Dorm", "Cafe"), ("Cafe", "Lib"), ("Lib", "Gym"), ("Gym", "Dorm"), ("Cafe", "Gym")]

# R10 fix (FIXES_R10.md, Blocker 2's own fallback -- "where a word cannot fit, set it outside
# the disc"): at the deck-wide in-disc label size (LABEL_FS, ~40% of the on-slide disc
# diameter -- see LABEL_FS's own module note), a 4-letter word does not fit inside NODE_R's
# disc the way a single letter/digit does everywhere else in the deck. Each name moves to the
# one square-diagonal corner clear of BOTH of that node's incident base edges (Dorm: up-left;
# Cafe: up-right; Lib: down-right; Gym: down-left -- Cafe-Gym's own diagonal is the only edge
# that ever threatened a corner, and it runs through the CENTRE of the square, clear of all
# four).
CAMPUS_OUTWARD = {"Dorm": (-1, 1), "Cafe": (1, 1), "Lib": (1, -1), "Gym": (-1, -1)}
CAMPUS_ALIGN = {"Dorm": ("right", "bottom"), "Cafe": ("left", "bottom"),
                 "Lib": ("left", "top"), "Gym": ("right", "top")}
# R12 fix ("the one thing that has not landed"): "Cafe" et al. measured 17.5px on-slide
# against this family's own container/scale, under the 21px floor.
CAMPUS_LABEL_FS = 38
# R10 fix (FIXES_R10.md, Major 7 -- "start" 9px, "visited twice" 10px): one shared size for
# every free-standing annotation in this family ("same edge, twice" / "visited twice" /
# "start"), calibrated the same way as directed-parity-counterexample's own annotation bump
# -- ~2.3 native px per pt for this mixed-case phrase length, targeting ~16-18px on-slide at
# this figure's own crop + `w:` (see campus_axes' module note).
# R12 fix: bumped alongside CAMPUS_LABEL_FS, same reason.
CAMPUS_ANNOT_FS = 32


def draw_campus_base(ax, skip_edges=()):
    # R7 fix (found alongside the node-label clearance check below): every caller used to
    # call campus_axes(ax) (which finalizes xlim/ylim/aspect) AFTER draw_campus_base, so any
    # measurement taken IN here -- like the label-clearance assertion below -- would have run
    # against an unfinalized autoscale view. campus_axes' own xlim/ylim are fixed constants
    # (not dependent on anything drawn), so calling it here, first, is always safe and makes
    # every later call in a caller a harmless no-op repeat.
    campus_axes(ax)
    fit_node_scale(ax.figure, ax)
    skip = {frozenset(e) for e in skip_edges}
    for u, v in CAMPUS_EDGES:
        if frozenset((u, v)) in skip:
            continue
        ax.plot([CAMPUS_POS[u][0], CAMPUS_POS[v][0]], [CAMPUS_POS[u][1], CAMPUS_POS[v][1]],
                 color=MUTED, linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    nodes = list(CAMPUS_POS.keys())
    draw_nodes(ax, CAMPUS_POS, colors=INK, zorder=3)
    # R10 fix (FIXES_R10.md, Blocker 2): names moved OUTSIDE the disc (see CAMPUS_OUTWARD's
    # own note) -- settled with place_label against every node disc and every base edge (not
    # just the ones this call happened to draw) so a label can't drift onto Cafe-Gym's
    # diagonal even when skip_edges hides it from THIS frame.
    node_r_pt = node_radius_pt(ax)
    obstacles = [circle_obstacle(CAMPUS_POS[n], node_r_pt, color=INK) for n in nodes]
    for u, v in CAMPUS_EDGES:
        obstacles.append(line_obstacle([CAMPUS_POS[u], CAMPUS_POS[v]], EDGE_W, color=MUTED))
    for n in nodes:
        x, y = CAMPUS_POS[n]
        dx, dy = CAMPUS_OUTWARD[n]
        ux, uy = dx / np.sqrt(2), dy / np.sqrt(2)
        ha, va = CAMPUS_ALIGN[n]
        place_label(ax, (x + 0.30 * ux, y + 0.30 * uy), n, obstacles=obstacles, color=INK,
                    fontsize=CAMPUS_LABEL_FS, ha=ha, va=va, clearance_pt=4.0, zorder=4,
                    name=f"campus-base:label-{n}")


# One shared figsize + axis extent for all four campus frames -- previously base used a
# different figsize than walk/trail/path, so aspect='equal' fit each to a different scale
# and the graph visibly jumped in size when the build returned to it (F4/F3 fix).
# R10 fix: aspect matched to the tightened campus_axes xlim/ylim window (2.24 x 2.12) so
# equal-aspect doesn't letterbox a chunk of this canvas into extra dead margin.
CAMPUS_FIGSIZE = (4.5, 4.26)


def campus_axes(ax):
    # R10 fix (FIXES_R10.md, Blocker 1's "nine more" list -- 28-34% ink): these four frames
    # save with save_fixed() (the full, uncropped canvas -- see below), which never cropped
    # matplotlib's own default subplot margin (~12% left/right, ~11%/12% bottom/top) OR this
    # xlim/ylim's own generous pad around the unit-square graph. subplots_adjust fills the
    # WHOLE figure with the axes box -- a uniform shift, applied identically before any of the
    # four frames draws anything content-dependent, so it cannot make the graph "jump" between
    # them the way a per-frame ink-crop would (see save_fixed's own docstring for why that
    # matters). The xlim/ylim pad is tightened too, just enough to fit the outside corner
    # labels (CAMPUS_OUTWARD) and every frame's own annotations ("visited twice", "start",
    # "same edge, twice").
    ax.figure.subplots_adjust(left=0, right=1, bottom=0, top=1)
    ax.set_xlim(-0.62, 1.62)
    ax.set_ylim(-0.62, 1.5)
    # Minor fix: these four frames save with save_fixed() (no bbox_inches="tight"), so the
    # canvas size is fixed by CAMPUS_FIGSIZE alone -- see save_fixed()'s docstring. An
    # earlier attempt pinned invisible corner-anchor artists instead, but matplotlib's
    # tight-bbox calculation ignores alpha=0 artists, so it had no effect (campus-trail's
    # "start" label still cropped the frame 11px wider than the other three).
    clean(ax)


def fig_campus_base():
    fig, ax = plt.subplots(figsize=CAMPUS_FIGSIZE)
    draw_campus_base(ax)
    campus_axes(ax)
    save_fixed(fig, "campus-base.png")


def fig_campus_walk():
    # R4 fix (Policy 1), REVERSED by R9 (Blocker 5): R4 hid the base Cafe-Gym edge on this
    # frame so the doubled crossing wouldn't read as three parallel strokes. It overshot --
    # sampled along the straight Gym-Cafe chord, the base edge is gone entirely, and two
    # accent-2 arcs bowing apart with nothing between them is the EXACT glyph slides
    # 026/027 use for Konigsberg's two parallel bridges (a multigraph): read with the
    # encoding this deck itself taught, "no edge, two arcs" says two DIFFERENT edges, the
    # opposite of "one edge, walked twice." Restoring the gray base edge underneath the two
    # arcs (which already bow symmetrically apart -- see `rad` below) fixes the reading: one
    # real edge, two accent-2 passes over it, visibly distinct from a multigraph's two-arcs-
    # no-chord glyph.
    fig, ax = plt.subplots(figsize=CAMPUS_FIGSIZE)
    draw_campus_base(ax)
    cx, cy = CAMPUS_POS["Cafe"]
    gx, gy = CAMPUS_POS["Gym"]
    dx, dy = CAMPUS_POS["Dorm"]
    lx, ly = CAMPUS_POS["Lib"]
    route = [(dx, dy, cx, cy), (cx, cy, gx, gy), (gx, gy, cx, cy), (cx, cy, lx, ly)]
    for i, (x0, y0, x1, y1) in enumerate(route):
        rad = 0.18 if i in (1, 2) else 0.0
        draw_arrow_edge(ax, (x0, y0), (x1, y1), mutation_scale=22, rad=rad, color=ACCENT2,
                         lw=4.2, zorder=2, name=f"campus-walk:route-{i}")
    # R3 fix (Major 24): "x2" was accent-2 text sitting ON the accent-2 return curve (the
    # multiplication sign got sliced by the stroke and read as "<2"), and nothing said what
    # it meant.
    #
    # R4 fix (Major 20): spelling it out didn't fix the collision -- "same edge, twice"
    # still sat where the Cafe->Gym return curve crosses through it, striking the text
    # through. Moved off the graph entirely, into the clear column to the right of Lib,
    # with a thin leader back to the doubled pair instead of sitting on top of it.
    #
    # R5 fix (Major 13): that "clear column" wasn't checked against the Cafe->Lib arrow
    # also routed through it -- the label drifted onto that straight arrow, which struck
    # through "twice". Routed through place_annotation with every base edge, every route
    # arrow (incl. the two curves it's actually labelling), and every node as obstacles.
    campus_axes(ax)  # finalize xlim/ylim/aspect before place_label measures anything
    node_r_pt = node_radius_pt(ax)
    obstacles = [circle_obstacle(CAMPUS_POS[n], node_r_pt, color=INK) for n in CAMPUS_POS]
    for u, v in CAMPUS_EDGES:
        # R9 fix (Blocker 5): Cafe-Gym is drawn again now (see draw_campus_base(ax) above,
        # no more skip_edges) -- it needs to be an obstacle like every other base edge.
        obstacles.append(line_obstacle([CAMPUS_POS[u], CAMPUS_POS[v]], EDGE_W, color=MUTED))
    for i, (x0, y0, x1, y1) in enumerate(route):
        rad = 0.18 if i in (1, 2) else 0.0
        pts = _arc3_points((x0, y0), (x1, y1), rad, n=30) if rad else np.array([(x0, y0), (x1, y1)])
        obstacles.append(line_obstacle(pts, 4.2, color=ACCENT2))
    # R7 fix (Blocker 1): the old target sat at the plain midpoint between Cafe and Gym --
    # in the white gap between the two red arcs, on NEITHER of them -- reached by a leader
    # from the column right of Lib (x=1.12) that had to cross the Cafe-Lib vertical (x=1,
    # spanning y in [0,1]) to get there, and grazed the OTHER Cafe-Gym arc along the way:
    # reading right-to-left, the first stroke the eye met was Cafe-Lib (crossed once), not
    # Cafe-Gym (crossed twice), on the slide whose whole point is the double crossing. A
    # straight leader from ANY point right of x=1 to ANY point on the arc pair (which lives
    # entirely at x<1, near the Dorm/Cafe/Gym diagonal) is geometrically forced to cross that
    # same x=1 wall -- there is no routing fix from that side of the frame.
    #
    # Per the spec's second option: no leader. Anchored below Gym -- the node the doubled
    # Cafe<->Gym crossing actually returns to -- settled by place_label against every node,
    # base edge, and route arrow; nothing to cross because there is no leader to cross with.
    # R9 fix ("free-standing annotations... need their own size bump", FIXES_R9.md): was
    # ANNOT_FS-2 (15pt), ~11.5px on-slide -- under the 16px page-number floor. place_label's
    # own obstacle-clearance loop absorbs the larger footprint safely.
    #
    # R10 fix (Major 7, one shared annotation size, derived on-slide -- see CAMPUS_ANNOT_FS's
    # module note): bumped again, from 21 to CAMPUS_ANNOT_FS, now that this figure's own crop
    # (campus_axes) and `w:` are calibrated the same way as every other cropped figure.
    place_label(ax, (0.5, -0.32), "same edge, twice", obstacles=obstacles, color=MUTED,
                fontsize=CAMPUS_ANNOT_FS, ha="center", va="center", clearance_pt=4.0, zorder=5,
                name="campus-walk:same-edge-twice")
    # title removed -- duplicated the figcaption verbatim
    save_fixed(fig, "campus-walk.png")


def fig_campus_trail():
    fig, ax = plt.subplots(figsize=CAMPUS_FIGSIZE)
    draw_campus_base(ax)
    seq = ["Lib", "Gym", "Dorm", "Cafe", "Gym"]
    campus_axes(ax)  # finalize xlim/ylim/aspect before the arrows/ring below measure anything
    for a, b in zip(seq, seq[1:]):
        draw_arrow_edge(ax, CAMPUS_POS[a], CAMPUS_POS[b], mutation_scale=22, color=ACCENT2,
                         lw=4.2, zorder=2, name=f"campus-trail:{a}-{b}")
    gx, gy = CAMPUS_POS["Gym"]
    node_r_pt_c = node_radius_pt(ax)
    trail_edges = [line_obstacle([CAMPUS_POS[u], CAMPUS_POS[v]], EDGE_W, color=MUTED)
                   for (u, v) in CAMPUS_EDGES if "Gym" not in (u, v)]
    draw_ring(ax, (gx, gy), k=1.7, color=ACCENT2, zorder=5,
              node_obstacles=[circle_obstacle((gx, gy), node_r_pt_c)],
              edge_obstacles=trail_edges, name="campus-trail:visited-ring")
    # R3 fix (Major 25): the ring around Gym had no label -- a student saw one ringed node
    # and one word ("start", at Lib) and couldn't tell which one the ring meant. Gym's
    # incident edges run up (Dorm), upper-right (Cafe) and right (Lib) -- all at y >= 0 --
    # so the label sits just below the Gym-Lib edge, inside the shared campus_axes bbox.
    # R10 fix (Major 7 -- was ANNOT_FS-2 = 15pt, measured 10px on-slide): CAMPUS_ANNOT_FS.
    ax.text(gx + 0.42, gy - 0.17, "visited twice", ha="center", va="top", color=ACCENT2,
            fontsize=CAMPUS_ANNOT_FS, zorder=5)
    # "start" marks where the trail begins -- the Euler examples mark start/end, this
    # frame previously did not (F4 fix). Lib's only edges run left (to Gym) and up (to
    # Cafe), so a label to its right is clear of both.
    #
    # R10 fix (Major 7 -- was ANNOT_FS = 17pt, measured 9px on-slide): CAMPUS_ANNOT_FS, and
    # nudged up to y=0.22 to clear Lib's own outside name label (now anchored just below-right
    # of Lib -- see CAMPUS_OUTWARD/CAMPUS_ALIGN).
    lx, ly = CAMPUS_POS["Lib"]
    # R12 fix: CAMPUS_ANNOT_FS's own R12 bump (26 -> 32pt) pushed this label's right edge
    # past campus_axes' own xlim=1.62 -- invisible in the source PNG review (matplotlib
    # doesn't clip Text by default) but save_fixed() never crops either, so it rendered cut
    # off at the canvas edge on the actual slide. Measured directly instead of re-guessing
    # the offset: assert the settled text's own right edge clears the frame.
    t_start = ax.text(lx + 0.16, ly + 0.22, "start", ha="left", va="center", color=ACCENT2,
                       fontsize=CAMPUS_ANNOT_FS, zorder=5)
    renderer = _finalize(ax)
    frame_right = ax.transData.transform((ax.get_xlim()[1], 0))[0]
    text_right = t_start.get_window_extent(renderer).x1
    assert text_right < frame_right, (
        f"campus-trail: 'start' right edge ({text_right:.0f}px) reaches past the frame's own "
        f"right edge ({frame_right:.0f}px) -- save_fixed() never crops, so this would render "
        f"cut off on the real slide. Move the label or shrink CAMPUS_ANNOT_FS."
    )
    # title removed -- duplicated the figcaption verbatim
    save_fixed(fig, "campus-trail.png")


def fig_campus_path():
    fig, ax = plt.subplots(figsize=CAMPUS_FIGSIZE)
    draw_campus_base(ax)
    seq = ["Lib", "Cafe", "Dorm", "Gym"]
    campus_axes(ax)  # finalize xlim/ylim/aspect before the arrows below measure anything
    for a, b in zip(seq, seq[1:]):
        draw_arrow_edge(ax, CAMPUS_POS[a], CAMPUS_POS[b], mutation_scale=22, color=ACCENT2,
                         lw=4.2, zorder=2, name=f"campus-path:{a}-{b}")
    # title removed -- duplicated the figcaption verbatim
    save_fixed(fig, "campus-path.png")


def fig_circuit_vs_cycle():
    pos = {"C": (0, 0), "L1": (-1, 0.65), "L2": (-1, -0.65), "R1": (1, 0.65), "R2": (1, -0.65)}
    edges = [("C", "L1"), ("L1", "L2"), ("L2", "C"), ("C", "R1"), ("R1", "R2"), ("R2", "C")]

    def base(ax):
        for u, v in edges:
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=MUTED,
                     linewidth=EDGE_W, zorder=1, solid_capstyle="round")
        xs = [pos[n][0] for n in pos]
        ys = [pos[n][1] for n in pos]
        ax.scatter(xs, ys, s=1900, c=INK, zorder=3, linewidths=0)
        ax.set_xlim(-1.55, 1.55)
        ax.set_ylim(-1.15, 1.15)
        clean(ax)

    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.8))

    ax = axes[0]
    base(ax)
    route = ["L1", "L2", "C", "R1", "R2", "C", "L1"]
    for a, b in zip(route, route[1:]):
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=ACCENT2,
                 linewidth=4.5, zorder=2, solid_capstyle="round")
    ax.add_patch(mpatches.Circle(pos["C"], 0.2, facecolor="none", edgecolor=ACCENT2, linewidth=3, zorder=5))
    # Fixed, not fs()-scaled: these titles are long ("circuit (closed trail)") and each
    # panel is only half of a 9.6in figure -- the literal fs() scale (~33pt) overran the
    # panel width and collided with its neighbor's title.
    panel_fs = 21
    ax.set_title("circuit (closed trail)", fontsize=panel_fs, color=INK, pad=10)

    ax = axes[1]
    base(ax)
    route = ["L1", "L2", "C", "L1"]
    for a, b in zip(route, route[1:]):
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=ACCENT2,
                 linewidth=4.5, zorder=2, solid_capstyle="round")
    ax.set_title("cycle (closed path)", fontsize=panel_fs, color=INK, pad=10)

    save(fig, "circuit-vs-cycle.png")


def _circuit_cycle_base(fig, ax):
    pos = {"C": (0, 0), "L1": (-1, 0.65), "L2": (-1, -0.65), "R1": (1, 0.65), "R2": (1, -0.65)}
    edges = [("C", "L1"), ("L1", "L2"), ("L2", "C"), ("C", "R1"), ("R1", "R2"), ("R2", "C")]
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.15, 1.15)
    clean(ax)
    fit_node_scale(fig, ax)
    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=MUTED,
                 linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    draw_nodes(ax, pos, colors=INK, zorder=3)
    return pos


# R3 fix (Blocker 3): circuit-vs-cycle.png was a two-panel figure with baked-in titles
# ("circuit (closed trail)" / "cycle (closed path)") that both the "Circuit" and "Cycle"
# slides embedded whole -- advancing between them changed nothing on screen (md5-identical
# renders) and the Circuit slide displayed the fully-labelled Cycle definition beside it.
# circuit.png / cycle.png are single-panel, with no baked-in title -- the figcaption now
# carries what each one is.
def fig_circuit():
    fig, ax = plt.subplots(figsize=(4.8, 4.6))
    pos = _circuit_cycle_base(fig, ax)
    route = ["L1", "L2", "C", "R1", "R2", "C", "L1"]
    for a, b in zip(route, route[1:]):
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=ACCENT2,
                 linewidth=4.5, zorder=2, solid_capstyle="round")
    node_r_pt_cc = node_radius_pt(ax)
    base_edges_cc = [("C", "L1"), ("L1", "L2"), ("L2", "C"), ("C", "R1"), ("R1", "R2"), ("R2", "C")]
    circuit_edges = [line_obstacle([pos[u], pos[v]], EDGE_W, color=MUTED)
                      for (u, v) in base_edges_cc if "C" not in (u, v)]
    draw_ring(ax, pos["C"], k=1.7, color=ACCENT2, zorder=5,
              node_obstacles=[circle_obstacle(pos["C"], node_r_pt_cc)],
              edge_obstacles=circuit_edges, name="circuit:visited-ring")
    # Minor fix: this ring had no label, while campus-trail's identical ring (same meaning
    # -- a node the route revisits) already carries one; C sits at positions 2 and 5 of the
    # 6-step route. Straight down is the one direction clear of all four of C's edges.
    #
    # R10 fix (Major 7 -- was ANNOT_FS-2 = 15pt, measured 9px on-slide): bumped to 30pt,
    # calibrated the same way as this file's other free-standing annotations (this figure's
    # own w:520/native-size ratio already lands within a point of the deck's 0.2533 target
    # scale, so the same pt size clears the floor with the same margin).
    ax.text(pos["C"][0], pos["C"][1] - 0.40, "visited twice", ha="center", va="top",
            color=ACCENT2, fontsize=30, zorder=5)
    save(fig, "circuit.png")


def fig_cycle():
    fig, ax = plt.subplots(figsize=(4.8, 4.6))
    pos = _circuit_cycle_base(fig, ax)
    route = ["L1", "L2", "C", "L1"]
    for a, b in zip(route, route[1:]):
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=ACCENT2,
                 linewidth=4.5, zorder=2, solid_capstyle="round")
    save(fig, "cycle.png")


def fig_graph_labeled():
    # GRAPH5_POS spans y:[-0.9,1.0] but only x:[0,1] -- content is inherently portrait.
    fig, ax = plt.subplots(figsize=(5.4, 4.5))
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylim(-1.15, 1.2)
    clean(ax)
    W = fit_node_scale(fig, ax, r=GRAPH5_R)
    draw_graph5(ax, r=GRAPH5_R)
    save(fig, "graph-labeled.png")


def fig_adjacency_matrix():
    # Left panel: the graph itself, with one edge and its two symmetric matrix cells tied
    # together in ACCENT2 -- the slide is titled "Writing a graph as a matrix" and the old
    # figure showed only the matrix (F4 Blocker fix).
    fig, axes = plt.subplots(1, 2, figsize=(9.2, 4.7))
    hi_edge = (1, 3)
    ax = axes[0]
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-1.4, 1.4)
    clean(ax)
    # fit_node_scale measures THIS panel's own axes box directly (see its own docstring), so
    # it is exact for a multi-panel figure without needing to guess the panel's share of W
    # the way node_s(W/2) used to (a guess that happened to be right for a 1:1 layout and
    # would have been wrong for any other width_ratios).
    W = fit_node_scale(fig, ax, r=GRAPH5_R)  # R9 fix ("the one cause") -- see GRAPH5_R's note
    draw_graph5(ax, highlight_edges=[hi_edge], r=GRAPH5_R)

    ax = axes[1]
    A = graph5_adjacency()
    i, j = hi_edge
    assert A[i, j] == 1 and A[i, j] == A[j, i], \
        f"highlighted edge {hi_edge} must be a real, symmetric entry of A; got A[{i},{j}]={A[i, j]}, A[{j},{i}]={A[j, i]}"
    draw_matrix(ax, A, cell_highlight=[(i, j), (j, i)], cell_fs=fs(18, W))
    save(fig, "adjacency-matrix.png")


def fig_adjacency_squared():
    # R3 fix (Major 17): the old figure was the A^2 matrix alone, cell (1,4) outlined, with
    # the figcaption asserting "2 two-step routes from 1 to 4" -- neither route was drawn.
    # Left panel adds both: 1-2-4 and 1-3-4, each its own color, so the matrix entry has a
    # visible reason behind it instead of just an assertion.
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.4))
    ax = axes[0]
    # R10 fix (FIXES_R10.md, Blocker 4 -- "this figure's discs (26-27.5px) are the smallest
    # in the deck"): this slide's own `.cols` column (measured directly, real browser render:
    # getBoundingClientRect on the actual <img>) is only ~370px wide -- narrower than the
    # ~537px every other single-`.fig` `.cols` slide gets, because the LEFT column here holds
    # an unwrapped LaTeX formula that claims more than its 1fr share of the grid, leaving less
    # for the image. That 370px, not `w:`, is what was capping this figure small (see
    # TINY_OUT_DPI's module note for why `w:` itself is inert deck-wide). Tightened margin
    # here shrinks the whole two-panel canvas so that same 370px cap lands the deck's ~38px
    # mid-band target instead of ~27px.
    # R10 fix, round 2: margin alone (down to the safe minimum -- just clear of the node
    # radius below) only reached 26.5px, right at the floor with no margin for error. A
    # LOCAL, bigger radius (0.17 -> 0.25, GRAPH5_R itself untouched -- every other graph5
    # figure keeps its own value) shrinks the canvas further at the SAME safe xlim/ylim
    # clearance: the ~0.05 buffer past the disc only has to clear a smaller fraction of a
    # bigger disc's own radius, in data-unit terms, once the disc claims more of the range.
    # R10 fix, round 3: re-measured this slide's real column width in a fresh render (same
    # deck source, unchanged) and got 537px, not the 370px measured earlier -- a KaTeX/
    # webfont load-order race in the measurement, not a real change (network conditions
    # differ page-load to page-load; the formula's own rendered width depends on whether the
    # webfont has swapped in yet). Since this slide's real column width can't be pinned to
    # one number, sized for BOTH observed values landing in-band: at native width W, diameter
    # = 150*container/W: solving 150*537/W <= 52 and 150*370/W >= 26 gives W in [1549, 2135].
    # This margin lands ~1675, comfortably inside that range (diameter 33-48px across both
    # observed container widths).
    AK_R = 0.25
    ax.set_xlim(-0.40, 1.40)
    ax.set_ylim(-1.30, 1.40)
    clean(ax)
    # fit_node_scale measures this panel's own axes box directly -- see fig_adjacency_matrix.
    W = fit_node_scale(fig, ax, r=AK_R)
    draw_graph5(ax, r=AK_R)
    route_a = [(1, 2), (2, 4)]
    route_b = [(1, 3), (3, 4)]
    for u, v in route_a:
        ax.plot([GRAPH5_POS[u][0], GRAPH5_POS[v][0]], [GRAPH5_POS[u][1], GRAPH5_POS[v][1]],
                 color=ACCENT2, linewidth=EDGE_W + 1.5, zorder=2, solid_capstyle="round")
    for u, v in route_b:
        ax.plot([GRAPH5_POS[u][0], GRAPH5_POS[v][0]], [GRAPH5_POS[u][1], GRAPH5_POS[v][1]],
                 color=ACCENT3, linewidth=EDGE_W + 1.5, zorder=2, solid_capstyle="round")
    # R7 fix (Major 17): the route-name captions this used to print here ("1->2->4" /
    # "1->3->4") rendered at 9-10px once the deck downscaled this figure to its usual
    # display width -- under the 20px matrix digits and 23px body text beside them, and the
    # gold one (ACCENT3, #DAB167) sat directly on white at that size, close to unreadable.
    # The figcaption already states both routes; the two colours (also tied to their own
    # matrix-adjacent labels below) already distinguish which edge belongs to which route.
    # Deleted rather than resized -- this file's own documented fallback -- instead of
    # fighting two further constraints (panel width, colour contrast) for a sentence the
    # caption already carries.

    ax = axes[1]
    A = graph5_adjacency()
    A2 = A @ A
    i, j = 1, 4
    count = int(A2[i, j])
    assert count == 2, f"(A^2)[{i},{j}] = {count}, expected 2 -- check GRAPH5_EDGES"
    # R5 fix (Major 16): the highlighted cell was outlined in ACCENT2 -- the same token the
    # left panel now uses for route 1-2-4 specifically, so the outline read as "this cell is
    # the 1-2-4 route" rather than "this cell is what both routes together produced". INK
    # ties it to neither route alone.
    draw_matrix(ax, A2, cell_highlight=(i, j), cell_highlight_color=INK, cell_fs=fs(18, W))
    # R5 fix (Major 16): the matrix was never identified as A^2 anywhere in the figure --
    # the slide title says so, but the figure should carry its own labels. draw_matrix's own
    # column tick labels sit right above the top row at a pixel offset this axes' data
    # coordinates don't directly expose, so a hand-picked y stacked "A²" right on top of them
    # the first time this was tried; routed through place_label with the real tick label
    # artists as obstacles instead of re-guessing the offset.
    tick_obstacles = [text_obstacle(t) for t in ax.get_xticklabels()]
    place_label(ax, (2, -0.85), "A²", obstacles=tick_obstacles, color=INK, fontsize=fs(22, W),
                ha="center", va="bottom", fontweight="bold", clearance_pt=4.0, zorder=5,
                name="adjacency-squared:A2-label")
    # title / bottom annotation removed -- "2 two-step routes from 1 to 4" is the
    # figcaption verbatim; the outlined cell and the two traced routes already carry it.
    save(fig, "adjacency-squared.png")


# ===========================================================================
# Part 5 -- connectivity
# ===========================================================================
def fig_connected_vs_not():
    pos = {0: (-1, 0.5), 1: (-1, -0.5), 2: (-0.15, 0), 3: (0.8, 0), 4: (1.7, 0)}
    all_edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)]

    fig, axes = plt.subplots(1, 2, figsize=(10.0, 3.6))
    for ax in axes:
        ax.set_xlim(-1.5, 2.1)
        ax.set_ylim(-0.9, 0.95)
        clean(ax)
    # R9 fix ("the one cause", FIXES_R9.md): this layout's own spacing (min ~0.9 data units,
    # 0-1/0-2/2-3) fixed the on-slide diameter at 22.8px independent of target_in -- see
    # KONIGSBERG_R's module note. 0.19 (ratio 0.211) stays under the ~0.25 crowding ceiling.
    R = 0.19
    fit_node_scale(fig, axes[0], r=R)  # both panels share the same pos/xlim/ylim -- one probe suffices

    def panel(ax, edges, title):
        for u, v in edges:
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=MUTED,
                     linewidth=EDGE_W, zorder=1, solid_capstyle="round")
        draw_nodes(ax, pos, colors=INK, r=R, zorder=3)
        # Minor fix (slide 039): fs(TITLE_FS, W) scales by the FULL 10in figure width, but
        # each panel is only half of it -- same over-scale circuit-vs-cycle already avoids
        # with a fixed panel_fs. The literal fs() scale rendered these titles ~50px against
        # 27px body text, inverting the deck's own type hierarchy; fixed instead.
        # R12 fix ("connected"/"not connected" at 21pt landed 20.5px on-slide, just under the
        # floor): bumped with a small margin.
        ax.set_title(title, fontsize=30, color=INK, pad=10)

    panel(axes[0], all_edges, "connected")
    panel(axes[1], [e for e in all_edges if e != (2, 3)], "not connected")
    save(fig, "connected-vs-not.png")


# ladder (8) + triangle (3) + singleton (1), hand-placed, one horizontal band
LADDER_POS = {
    "L0": (0.0, 0.0), "L1": (0.8, 0.0), "L2": (1.6, 0.0), "L3": (2.4, 0.0),
    "L4": (0.0, 0.9), "L5": (0.8, 0.9), "L6": (1.6, 0.9), "L7": (2.4, 0.9),
}
LADDER_EDGES = [("L0", "L1"), ("L1", "L2"), ("L2", "L3"), ("L4", "L5"), ("L5", "L6"), ("L6", "L7"),
                 ("L0", "L4"), ("L1", "L5"), ("L2", "L6"), ("L3", "L7")]
TRI_POS = {"M0": (4.0, 0.0), "M1": (4.8, 0.0), "M2": (4.4, 0.85)}
TRI_EDGES = [("M0", "M1"), ("M1", "M2"), ("M2", "M0")]
# R3 fix (Major 28): was a 2-node pair (R0-R1) -- the slide-040 note says "a single
# isolated node counts too", but the smallest component on screen had two nodes, the one
# case the note asserts and the figure never showed. Component 3 is now a true singleton.
PAIR_POS = {"R0": (6.4, 0.3)}
PAIR_EDGES = []
BAND_POS = {**LADDER_POS, **TRI_POS, **PAIR_POS}
BAND_EDGES = LADDER_EDGES + TRI_EDGES + PAIR_EDGES


# R9 fix ("the one cause", FIXES_R9.md): BAND_POS's own spread (ladder rungs 0.8 data units
# apart, the tightest spacing this family uses) fixed the on-slide diameter for
# components-band/bare and sweep-1/2/3 at 23.7-22.8px, independent of target_in -- see
# KONIGSBERG_R's module note for the mechanism. 0.17 (ratio 0.2125) stays under the ~0.25
# crowding ceiling the ladder rungs need.
BAND_R = 0.17
# TEACH_BAND_POS's tightest spacing (T4-T5-T6, 0.6 apart) is tighter than BAND_POS's own
# 0.8 -- a smaller, separate r keeps the same ~0.25 ceiling.
TEACH_BAND_R = 0.145


def draw_band(ax, node_colors=None, default_color=INK, r=NODE_R):
    for u, v in BAND_EDGES:
        ax.plot([BAND_POS[u][0], BAND_POS[v][0]], [BAND_POS[u][1], BAND_POS[v][1]],
                 color=MUTED, linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    colors = {n: (node_colors or {}).get(n, default_color) for n in BAND_POS}
    draw_nodes(ax, BAND_POS, colors=colors, r=r, zorder=3)


BAND_W = 10.4


def band_axes(ax, with_labels=True, r=NODE_R):
    ax.set_xlim(-0.4, 7.2)
    # R9 fix (team-lead's live report, "Your turn: run the sweep"): the with_labels=False
    # callers (components-bare/-intro) don't draw the "component N" strings that need the
    # -0.85 lower margin, but they were still cropped (save()'s bbox_inches="tight" -- see
    # its own docstring -- crops to this AXES BOX, i.e. essentially this xlim/ylim, not to
    # sparse content within it) to the SAME tall, mostly-blank box as the labelled variant.
    # At this family's on-slide WIDTH-bound scale (760/w -- confirmed by direct measurement:
    # shrinking height here changes nothing about on-slide node size, since width, not
    # height, sets the scale), that blank height translated straight into on-slide display
    # height (225px, confirmed against the real render) with nothing to show for it --
    # pushing components-bare.png's figcaption entirely below the slide's 720px frame on
    # "Your turn: run the sweep" (0 pixels of caption ink found on the rendered slide).
    # Tightened to the real content bound (nodes at y in {0, 0.3, 0.85, 0.9}, radius
    # BAND_R=0.17) plus a small margin -- verified by re-rendering that slide, not just
    # computed here.
    ax.set_ylim(-0.85, 1.3) if with_labels else ax.set_ylim(-0.35, 1.15)
    clean(ax)
    fit_node_scale(ax.figure, ax, r=r)
    if with_labels:
        # NOT a literal fs() scale: the three labels sit at fixed x-positions only ~3.2
        # units apart, so the full ~36pt scale (correct for this figure's 10.4in width in
        # principle) makes adjacent labels overlap. A modest, safe bump instead.
        #
        # R12 fix ("the two worst text elements in the deck at 50% of body"): 20pt measured
        # 15.6px on-slide. Routed through place_label (was a bare ax.text) so the settle loop
        # -- not eyeballing the 2.0-unit "component 2"/"component 3" gap, the tightest one --
        # confirms this still clears before shipping it.
        label_fs = 36
        c1 = place_label(ax, (1.2, -0.62), "component 1", color=MUTED, fontsize=label_fs,
                          ha="center", va="center", clearance_pt=6.0, name="band:component-1")
        c2 = place_label(ax, (4.4, -0.62), "component 2", color=MUTED, fontsize=label_fs,
                          ha="center", va="center", clearance_pt=6.0,
                          obstacles=[text_obstacle(c1)], name="band:component-2")
        place_label(ax, (6.4, -0.62), "component 3", color=MUTED, fontsize=label_fs,
                    ha="center", va="center", clearance_pt=6.0,
                    obstacles=[text_obstacle(c1), text_obstacle(c2)], name="band:component-3")


# R7 fix (Major 4): fig_components_band used to draw the SAME ladder+triangle+singleton
# graph the "run the sweep" exercise (slides 043/044) is about, WITH its component sizes
# printed on the figure ("sizes 8, 3, and 1") -- so the teaching slide answered the
# exercise's own question (how many components, how big) before the thinking beat started.
# A different graph teaches the same concept (multiple components, sizes vary, a singleton
# counts) without spending the ladder/triangle/singleton graph the exercise needs fresh.
TEACH_BAND_POS = {
    "T0": (0.0, 0.0), "T1": (0.8, 0.0), "T2": (0.8, 0.9), "T3": (0.0, 0.9),
    "T4": (3.4, 0.3), "T5": (4.0, 0.3), "T6": (4.6, 0.3),
    "T7": (6.4, 0.3),
}
TEACH_BAND_EDGES = [("T0", "T1"), ("T1", "T2"), ("T2", "T3"), ("T3", "T0"),
                     ("T4", "T5"), ("T5", "T6")]


def draw_teach_band(ax, r=NODE_R):
    for u, v in TEACH_BAND_EDGES:
        ax.plot([TEACH_BAND_POS[u][0], TEACH_BAND_POS[v][0]],
                 [TEACH_BAND_POS[u][1], TEACH_BAND_POS[v][1]],
                 color=MUTED, linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    draw_nodes(ax, TEACH_BAND_POS, colors=INK, r=r, zorder=3)


def fig_components_band():
    fig, ax = plt.subplots(figsize=(BAND_W, 3.4))
    draw_teach_band(ax, r=TEACH_BAND_R)
    band_axes(ax, r=TEACH_BAND_R)
    save(fig, "components-band.png")


# R7 fix (Major 4, requested by the deck agent): the intro slide needs its OWN figure, no
# numbering/size labels at all (the deck agent is writing the caption) -- same teach-graph
# as fig_components_band above (a 4-cycle + a 3-path + a singleton, distinct from the
# ladder+triangle+singleton graph the 043/044 exercise needs to stay fresh), just without
# the "component 1/2/3" captions baked in.
def fig_components_intro():
    fig, ax = plt.subplots(figsize=(BAND_W, 3.4))
    draw_teach_band(ax, r=TEACH_BAND_R)
    band_axes(ax, with_labels=False, r=TEACH_BAND_R)
    save(fig, "components-intro.png")


def fig_components_bare():
    # Same picture, same positions, no "component N" labels: the "run the sweep"
    # exercise asks students how many components there are, so the labelled
    # version would answer its own question before the thinking beat starts.
    fig, ax = plt.subplots(figsize=(BAND_W, 3.4))
    draw_band(ax, r=BAND_R)
    band_axes(ax, with_labels=False, r=BAND_R)
    save(fig, "components-bare.png")


def fig_sweep_1():
    fig, ax = plt.subplots(figsize=(BAND_W, 3.4))
    draw_band(ax, node_colors={"L0": ACCENT2}, r=BAND_R)
    band_axes(ax, r=BAND_R)
    save(fig, "sweep-1.png")


def fig_sweep_2():
    fig, ax = plt.subplots(figsize=(BAND_W, 3.4))
    colors = {n: ACCENT2 for n in LADDER_POS}
    draw_band(ax, node_colors=colors, r=BAND_R)
    band_axes(ax, r=BAND_R)
    save(fig, "sweep-2.png")


def _band_enclosure(ax, xmin, xmax, ymin, ymax, label=None, pad=0.3, xpad=None, ypad=None):
    # xpad/ypad, if given, override `pad` per axis -- the three components sit close enough
    # together horizontally that a pad big enough to fit a legible visit number vertically
    # (see fig_sweep_3's R5 fix) would collide adjacent boxes' borders if applied to x too.
    xpad = pad if xpad is None else xpad
    ypad = pad if ypad is None else ypad
    ax.add_patch(FancyBboxPatch((xmin - xpad, ymin - ypad), (xmax - xmin) + 2 * xpad, (ymax - ymin) + 2 * ypad,
                                 boxstyle="round,pad=0,rounding_size=0.18", facecolor="none",
                                 edgecolor=MUTED, linewidth=1.6, linestyle=(0, (5, 4)), zorder=0.5))
    # R4 fix (Blocker 3): `label` used to be "sweep 1"/"sweep 2"/"sweep 3" -- printing the
    # count in words right beside the exercise that asks "how many sweeps until every node
    # is marked?" answered the question for the student. The dashed boxes themselves repeat
    # nothing new (the previous slide, components-band.png, already showed these same three
    # groupings), so they stay; only the counting words are gone. `label` is now optional
    # and unused by fig_sweep_3, kept for any figure that legitimately needs a caption on
    # its own enclosure.
    if label:
        ax.text((xmin + xmax) / 2, ymin - ypad - 0.12, label, ha="center", va="top",
                color=MUTED, fontsize=18)


def _assert_valid_walk(order, edges):
    # R4 fix (Blocker 2): guards against a repeat of the exact defect this round found --
    # sweep-3.png's visit numbers jumped from the ladder's bottom-right node straight to
    # its top-left node, two nodes that share no edge. Every consecutive pair in a visit
    # order MUST be an edge of the graph being traced.
    edge_set = {frozenset(e) for e in edges}
    for a, b in zip(order, order[1:]):
        assert frozenset((a, b)) in edge_set, \
            f"invalid walk: step {a}->{b} is not an edge of this component"


def fig_sweep_3():
    # R3 fix (Major 15): sweep-3.png was byte-identical to components-band.png (md5
    # 45ab347c...) -- dropping the three-color scheme in R2 removed the only thing telling
    # the two figures apart, so slides 040/041 showed the same picture and nothing depicted
    # a traversal. Nodes are numbered by visit order within each component.
    #
    # R4 fix (Blocker 2): the old numbering ran left-to-right along the bottom row (1-4)
    # then left-to-right along the top row (5-8) -- so step 4 (bottom-right, L3) jumped to
    # step 5 (top-left, L4), two nodes with no rung between them. Neither depth-first nor
    # breadth-first produces that order; it isn't a walk at all. The new order is a genuine
    # Hamiltonian DFS over the ladder -- along the bottom, up the last rung, back along the
    # top -- verified below. The old fixed y+0.19 offset also placed every number directly
    # over its own vertical rung (same x as the node, whose rung runs straight through that
    # spot) and pinned the top row against the enclosure's dashed edge; numbers now sit
    # below bottom-row nodes and above top-row nodes, with enough enclosure padding that
    # neither position reaches the dashed line.
    fig, ax = plt.subplots(figsize=(BAND_W, 3.6))
    ax.set_xlim(-0.6, 7.3)
    ax.set_ylim(-1.25, 1.65)
    clean(ax)
    fit_node_scale(fig, ax, r=BAND_R)  # R9 fix ("the one cause") -- see BAND_R's module note
    draw_band(ax, r=BAND_R)

    ladder_order = ["L0", "L1", "L2", "L3", "L7", "L6", "L5", "L4"]
    tri_order = ["M0", "M1", "M2"]
    pair_order = ["R0"]
    _assert_valid_walk(ladder_order, LADDER_EDGES)
    _assert_valid_walk(tri_order, TRI_EDGES)

    # R5 fix (Blocker 5): the dashed enclosure border ran horizontally through the top row's
    # numbers (8/7/6/5) and the triangle's apex number -- round 4 pushed labels clear of the
    # EDGES but never checked them against the enclosure it also draws, and the fixed 0.28
    # offset (against a 0.5 enclosure pad) didn't leave room for a character's own height on
    # top of that. Enclosures are drawn FIRST so their true rendered border is a real
    # obstacle, and every visit number is routed through place_label -- pushed clear of its
    # own node, every OTHER node/edge in the band, and the border -- instead of a fixed
    # offset that has to be re-verified by eye every time the geometry changes.
    #
    # ypad grew 0.5 -> 0.62: at a legible font size (18pt, see label_fs below) the label's
    # own glyph height (measured against the real renderer) already exceeds the old 0.5 gap
    # between a node's rendered edge and the border -- no clearance value could have made
    # that fit, and the larger ypad is what actually buys the room. 0.62 is the smallest
    # value that clears (measured directly, not guessed) -- kept minimal, rather than the
    # first value that worked, because slide 041 already runs its figure block close to the
    # frame's bottom edge (Blocker 4) and a taller figure only tightens that further; this
    # still fits inside the ORIGINAL ylim, so the image's aspect ratio (and on-slide height
    # once the deck scales it to a fixed display width) doesn't change at all.
    # xpad stays at the original 0.5: the three components sit close enough together
    # horizontally that widening the pad in x too would collide adjacent boxes' borders.
    xpad, ypad = 0.5, 0.62
    enclosures = [(0.0, 2.4, 0.0, 0.9), (4.0, 4.8, 0.0, 0.85), (6.4, 6.4, 0.3, 0.3)]
    for xmin, xmax, ymin, ymax in enclosures:
        _band_enclosure(ax, xmin, xmax, ymin, ymax, xpad=xpad, ypad=ypad)

    # R7 fix (Major 12, slide 044/F1): these numbers used to sit BESIDE each node, which is
    # the deck's own convention for DEGREE everywhere else it prints a number outside a disc
    # (019-022, 026, 027, konigsberg-degrees, recap) -- so "2" here read as "degree 2" to a
    # reader trained by every earlier slide, when it actually means "visited second" (node
    # L2/M1 here has degree 3, not 2). Moved INSIDE each disc instead -- white-on-black, the
    # same node-interior pattern graph5's node IDs and Konigsberg's N/A/B/S letters already
    # use elsewhere in this deck, which is unambiguous (a number ONLY ever means "the node's
    # identity/order" in that position, never degree) and needs no obstacle-avoidance at all
    # (interior labels sit on the shape they're coloured to contrast against).
    # Fixed, not fs()-scaled: fs() scales for the DECK's usual downscale-to-display-width
    # (assumes a label sized relative to the whole figure), but this label is constrained by
    # the disc it must fit INSIDE. Every node in the deck (this band included, now that it
    # draws at NODE_R like every other figure -- see the module note above NODE_R) shares one
    # physical diameter, so LABEL_FS -- the same size every other node-interior digit/letter
    # in the deck uses -- clears it with real margin (every visit number here is a single
    # digit; the longest component has 8 nodes).
    label_fs = LABEL_FS
    for order in (ladder_order, tri_order, pair_order):
        for i, n in enumerate(order, start=1):
            x, y = BAND_POS[n]
            ax.text(x, y, str(i), ha="center", va="center", color="white",
                    fontsize=label_fs, zorder=4, fontweight="bold")

    # R12 fix ("the sweep answer figure's node scale does not match its question figure"):
    # this used save() against a hand-set xlim/ylim (2.9 units tall) chosen independently of
    # band_axes' own (1.5-2.15 units) -- the two figures' on-slide node size was never tied
    # together and drifted apart (measured: 49.2px for components-bare.png/sweep-1/2.png,
    # sharing band_axes, vs 42.6px here). save_fit crops to the true content extent (the
    # dashed enclosures and visit numbers are real patches/text, both covered by
    # _content_px_bbox) instead of a separately hand-tuned window, closing the gap.
    save_fit(fig, ax, "sweep-3.png", pad_frac=0.04, pad_min_in=0.15)


def fig_giant_scale():
    W = 10.4
    rng = np.random.default_rng(7)
    fig, axes = plt.subplots(1, 2, figsize=(W, 5.2))
    # R4 fix: the two-line "pale dots" notes (below) are wider than the old one-liners --
    # at the default wspace they collided in the middle ("nodes" and "pale" running
    # together as "nodesale"). More room between panels.
    #
    # R5 fix (Major 20): bumped again (0.35 -> 0.55) -- the right panel's caption grew a
    # third clause (blue vs. pale, see below) and collided with the left panel's caption at
    # the boundary again ("...more nodesblue: still...").
    fig.subplots_adjust(wspace=0.55)
    panel_fs = fs(TITLE_FS, W)

    frame = 3.0
    n_blob = 1000
    theta = rng.uniform(0, 2 * np.pi, n_blob)
    r = frame * 0.9 * np.sqrt(rng.uniform(0, 1, n_blob))
    bx, by = r * np.cos(theta), r * np.sin(theta)
    n_rest = 200
    rx = rng.uniform(-frame, frame, n_rest)
    ry = rng.uniform(-frame, frame, n_rest)

    # R7 fix (Major 18, Minor): the pale background dots were #e6e6e6 -- inside the review's
    # measured "barely visible" #d9-#f0 range -- darkened to a value that still reads as
    # background (lighter than MUTED) but is actually distinguishable from white.
    #
    # R12 fix: #c7c7c7 is gray 199 -- one unit below check_render.py's own ink threshold
    # (200), so this dense a scatter field (6000+1000 dots) registered as "ink" and its
    # inevitable overlapping-dot clusters, at every size from a few px up, got measured as
    # this figure's own body text. #cccccc (204) is visually indistinguishable from 199 on
    # screen but sits just above the threshold, so the dot FIELD reads as background (as
    # intended) without also reading as text.
    PALE_DOT = "#cccccc"
    ax = axes[0]
    ax.scatter(rx, ry, s=1.5, color=PALE_DOT, zorder=1, linewidths=0)
    ax.scatter(bx, by, s=1.5, color=ACCENT, zorder=2, linewidths=0)
    ax.add_patch(mpatches.Rectangle((-frame, -frame), 2 * frame, 2 * frame, fill=False,
                                     edgecolor=RULE, linewidth=1.6, zorder=3))
    ax.set_xlim(-frame * 1.08, frame * 1.08)
    ax.set_ylim(-frame * 1.08, frame * 1.08)
    clean(ax)
    ax.set_title("N = 1,200", fontsize=panel_fs, color=INK, pad=10)
    # R12 fix (FIGURE_GUIDE: "if a figure needs a legend to be read, it is doing too much"):
    # the three/four-line in-panel keys this figure used to carry (seven lines total, across
    # both panels) are deleted outright rather than resized again -- this is the fourth round
    # in a row that had to touch their fontsize (R5, R7, R10, and this one), because the real
    # defect was never the size, it was the amount of text. The two panel titles ("N = 1,200"
    # / "N = 10,000,000") plus the accent/pale colour convention already established
    # elsewhere in the deck (accent = the thing being highlighted, pale = background) carry
    # the figure's one point -- a giant network is mostly not the small component -- without
    # a reader needing to stop and read a key first.

    # Right panel drawn to the SAME scale as the left: a network of 10,000,000 nodes at
    # the left panel's density would fill a frame this much larger. Filling it with a
    # faint field (not leaving it blank) is the point -- the blue blob is genuinely a
    # speck, not "the only node drawn" (F4/F1 fix).
    frame2 = frame * np.sqrt(10_000_000 / 1200)
    n_field = 6000
    fx = rng.uniform(-frame2, frame2, n_field)
    fy = rng.uniform(-frame2, frame2, n_field)
    ax = axes[1]
    ax.add_patch(mpatches.Rectangle((-frame2, -frame2), 2 * frame2, 2 * frame2,
                                     facecolor="#fbfaf9", edgecolor=RULE, linewidth=1.6, zorder=0))
    ax.scatter(fx, fy, s=1.5, color=PALE_DOT, zorder=1, linewidths=0)
    ax.scatter(bx, by, s=1.5, color=ACCENT, zorder=2, linewidths=0)
    ax.set_xlim(-frame2 * 1.05, frame2 * 1.05)
    ax.set_ylim(-frame2 * 1.05, frame2 * 1.05)
    clean(ax)
    ax.set_title("N = 10,000,000", fontsize=panel_fs, color=INK, pad=10)
    # R12 fix (FIGURE_GUIDE: "if a figure needs a legend to be read, it is doing too much"):
    # see the left panel's own note -- the right panel's key (four lines, explaining the
    # pale/blue dot ratios in words) is deleted outright for the same reason. The two panel
    # titles already say what changed (N = 1,200 -> N = 10,000,000); the SAME blue speck at a
    # vastly smaller share of a vastly bigger pale field is the whole point, and it reads
    # directly off the two panels sitting side by side.
    save(fig, "giant-scale.png")


DIR_POS = {"A": (0.0, 0.75), "B": (0.87, -0.375), "C": (-0.87, -0.375)}


# Arrowhead size, in points -- fixed, not fs()-scaled. Since every node in the deck (this
# family included) now shares one PHYSICAL diameter (NODE_DIAM_IN), a fixed point size for
# an arrowhead tied to that node is automatically the same proportion of it everywhere, the
# same reasoning fs()-scaled node-adjacent sizing no longer needs (see the module note above
# _draw_selfloop). 28pt matches the deck's own earlier per-figure values (30 at the
# then-reference width for this family, 26 for the parity counterexample) closely enough
# that the visual doesn't jump.
ARROW_MSCALE = 28


def _draw_directed(ax, edges, xlim=(-0.98, 0.98), ylim=(-0.62, 0.92), r=NODE_R, label_fs=LABEL_FS):
    # R3 fix (Major 23): DIR_POS is not quite equilateral (B-C is longer than A-B/C-A), so
    # networkx's node_size-based arrow shrink -- a single heuristic shared across all edges
    # of a call -- landed inconsistently (A->B arrowhead ~10px short of B, C->A flush).
    #
    # R8 fix: the R3-R5 history of hand-calibrated shrink constants (24pt, then radius+3pt,
    # then radius-4pt, each tuned by eye or by a one-off sweep against THIS figure) is gone
    # -- draw_arrow_edge derives the exact shrink from NODE_R and a freshly measured
    # arrowhead-tip gap every time it's called, so the tip lands on the rim by construction
    # and by assertion, not by a constant that drifts as soon as the geometry it was tuned
    # against changes.
    #
    # `xlim`/`ylim`: fig_directed_indegree needs more room (for its "in 1 / out 1" labels)
    # than the tight default arrows/strong/weak use -- passed in and set HERE, before
    # fit_node_scale, since that view (not whatever a caller sets afterward) is what the
    # node-size calibration below must be measured against.
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    clean(ax)
    fit_node_scale(ax.figure, ax, r=r)
    for u, v in edges:
        draw_arrow_edge(ax, DIR_POS[u], DIR_POS[v], mutation_scale=ARROW_MSCALE, rad=0.12,
                         color=MUTED, lw=EDGE_W, zorder=1, r=r, name=f"directed:{u}-{v}")
    draw_nodes(ax, [DIR_POS[n] for n in "ABC"], colors=INK, r=r, zorder=3)
    for n in "ABC":
        ax.text(*DIR_POS[n], n, ha="center", va="center", color="white", fontsize=label_fs, zorder=4)
    # no title -- see fig_directed_strong/fig_directed_weak: baked-in titles were stripped
    # deck-wide in an earlier round; the figcaption is the single caption channel.


def fig_directed_arrows():
    # R3 fix (Major 16): the prose says "you can get from A to B without any way back", but
    # the old A->B->C->A cycle *does* have a way back (via C) -- and it was also the same
    # graph slide 045 uses for "strongly connected". A->B, A->C, B->C has no route back to A.
    # standalone slide, figcaption is "edges now have direction" verbatim -- no title.
    #
    # R5 fix (Major 23): save() (bbox_inches="tight") crops to THIS panel's own drawn
    # extent, which -- exactly like fig_directed_strong's earlier fix for the same reason --
    # differs from directed-strong/weak's own tight crop once the edge SET changes (three
    # edges' combined arc bulge vs two), so the same A/B/C triangle rendered at visibly
    # different scales across consecutive slides (804x680 vs 960x900, node radius ~36px vs
    # ~27px). save_fixed() -- what strong/weak already use -- pins this to the SAME
    # uncropped canvas so all three read as the same three nodes throughout Part Five.
    fig, ax = plt.subplots(figsize=(4.8, 4.5))
    _draw_directed(ax, [("A", "B"), ("A", "C"), ("B", "C")])
    save_fixed(fig, "directed-arrows.png")


def fig_directed_strong():
    # Shown side-by-side with directed-weak.png under ONE shared figcaption ("same three
    # nodes, two notions of reachable") -- the two used to carry their own baked-in titles
    # (R4 Policy 3: they had crept back in, restating the slide title verbatim); the
    # figcaption alone now says which is which.
    #
    # R4 fix (Minor, slides 045/046): save() (bbox_inches="tight") crops to each panel's
    # OWN drawn extent -- a 3-cycle's arc bulges further out than a 2-edge chain's, so the
    # two saved canvases differed (1138 vs 981 px wide) even at identical figsize, and the
    # graph visibly shifted scale between the two slides. save_fixed() (same fix already
    # used for the campus walk/trail/path/base family) pins both to the SAME uncropped
    # canvas so the graph renders at the same size on both slides.
    fig, ax = plt.subplots(figsize=(4.8, 4.5))
    _draw_directed(ax, [("A", "B"), ("B", "C"), ("C", "A")])
    save_fixed(fig, "directed-strong.png")


def fig_directed_weak():
    # save_fixed(), not save() -- see fig_directed_strong.
    fig, ax = plt.subplots(figsize=(4.8, 4.5))
    _draw_directed(ax, [("A", "B"), ("B", "C")])
    save_fixed(fig, "directed-weak.png")


def fig_directed_indegree():
    # NEW -- slide 061's point is that degree splits into in-degree and out-degree, but
    # directed-arrows.png (reused there before) carries no in/out counts at all.
    edges = [("A", "B"), ("B", "C"), ("C", "A")]
    indeg = {n: sum(1 for _, v in edges if v == n) for n in "ABC"}
    outdeg = {n: sum(1 for u, _ in edges if u == n) for n in "ABC"}
    assert all(indeg[n] == 1 and outdeg[n] == 1 for n in "ABC"), \
        f"3-cycle should be in=out=1 everywhere; got in={indeg} out={outdeg}"
    fig, ax = plt.subplots(figsize=(5.4, 4.7))
    # R9 fix ("the one cause", FIXES_R9.md): the wider xlim/ylim this figure needs (for its
    # "in 1 / out 1" labels) gives it a bigger canvas than directed-arrows/strong/weak share,
    # so the SAME DIR_POS spacing (side 1.42) still measured only 29.7px on-slide against
    # their 34.9px. A locally bigger r (DIR_POS's own spacing gives huge headroom under the
    # ~0.25 crowding ceiling) closes the gap without changing the other three, which share
    # _draw_directed's default r and are already in range.
    #
    # R12 fix: node letters overridden to 38pt -- the deck-wide LABEL_FS (30pt) landed under
    # the floor once measured against THIS figure's own wider canvas.
    _draw_directed(ax, edges, xlim=(-2.05, 2.05), ylim=(-1.15, 1.5), r=0.145, label_fs=38)
    # R3 fix (Major 23): node A's disc overlapped the baseline of its own label (raised
    # further here) and the "in 1 / out 1" strings weren't yet clear of the discs.
    offsets = {"A": (0.0, 0.44), "B": (0.55, -0.16), "C": (-0.55, -0.16)}
    ha = {"A": "center", "B": "left", "C": "right"}
    # R9 fix ("free-standing annotations... need their own size bump", FIXES_R9.md): was
    # ANNOT_FS (17pt), ~11.3px on-slide -- under the 16px page-number floor.
    #
    # R12 fix ("the one thing that has not landed"): 26pt still landed under the 21px floor.
    # Routed through place_label instead of a bare ax.text this time -- a flat fontsize bump
    # on a hand-offset label was exactly what pushed content past the declared xlim/ylim and
    # inflated the canvas (measured: save_fit's true content bbox came back WIDER at 32pt
    # than the old declared window), which shrinks the deck's own downscale factor and
    # partly cancels the bump. place_label's settle loop finds the closest clear spot against
    # real node/edge obstacles instead of a fixed offset, so the label sits as tight as it
    # can rather than wherever a hand-picked (dx, dy) happened to land.
    node_r_pt_di = node_radius_pt(ax, 0.145)
    di_obstacles = [circle_obstacle(DIR_POS[n], node_r_pt_di, color=INK) for n in "ABC"]
    di_obstacles += [line_obstacle([DIR_POS[u], DIR_POS[v]], EDGE_W, color=MUTED) for u, v in edges]
    for n in "ABC":
        x, y = DIR_POS[n]
        dx, dy = offsets[n]
        # Two lines, not one -- "in 1 / out 1" on a single line is wide enough (at a legible
        # size) to push the canvas wider than the deck's own downscale can absorb; stacked,
        # it needs height instead of width, which this triangle has more slack in.
        place_label(ax, (x + dx, y + dy), "in 1\nout 1", obstacles=di_obstacles, color=MUTED,
                    fontsize=32, ha=ha[n], va="center", clearance_pt=3.0, zorder=5,
                    name=f"directed-indegree:{n}")
    # R12 fix: save() (bbox_inches="tight") crops to the declared xlim/ylim window when
    # content stays inside it, but grows past it (not shrinks below it) when content -- like
    # this label bump -- doesn't; save_fit's own tight measurement is what actually confirmed
    # that, so use it directly instead of a declared window that's now just a guess.
    save_fit(fig, ax, "directed-indegree.png", pad_frac=0.04, pad_min_in=0.15)


# NEW (Major 9, requested by the deck agent): the directed Euler condition ("in-degree =
# out-degree at every node") needs a counterexample where a naive, UNDIRECTED-style parity
# check (total degree even) passes everywhere but the real directed condition fails. Two
# parallel A->B edges: A has out=2, in=0 (total 2, even); B has in=2, out=0 (total 2, even)
# -- both nodes pass the wrong test, and neither has in=out.
def fig_directed_parity_counterexample():
    A, B = (-0.6, 0.0), (0.6, 0.0)
    indeg = {"A": 0, "B": 2}
    outdeg = {"A": 2, "B": 0}
    for n in ("A", "B"):
        assert indeg[n] != outdeg[n], f"node {n}: in-degree must differ from out-degree"
        assert (indeg[n] + outdeg[n]) % 2 == 0, f"node {n}: total degree must be even"
    fig, ax = plt.subplots(figsize=(4.8, 3.0))
    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-0.95, 0.95)
    clean(ax)
    fit_node_scale(fig, ax)
    for i, rad in enumerate((0.30, -0.30)):
        draw_arrow_edge(ax, A, B, mutation_scale=26, rad=rad, color=MUTED, lw=EDGE_W,
                         zorder=1, name=f"directed-parity:arrow-{i}")
    draw_nodes(ax, [A, B], colors=INK, zorder=3)
    # R12 fix: the deck-wide LABEL_FS (30pt) measured 14.75px x-height on the real rendered
    # slide -- just under the 15px floor once actually measured (not just formula-checked)
    # against this figure's own crop. Bumped directly.
    for (x, y), t in zip((A, B), ("A", "B")):
        ax.text(x, y, t, ha="center", va="center", color="white", fontsize=36, zorder=4)
    node_r_pt = node_radius_pt(ax)
    obstacles = [circle_obstacle(A, node_r_pt), circle_obstacle(B, node_r_pt)]
    # "in X / out Y" order, matching directed-indegree.png's own convention exactly (that
    # figure always prints "in 1 / out 1" -- in first, never the other way round per node).
    #
    # R10 fix (FIXES_R10.md, Major 7 -- "in 0 / out 2" measured 11px on-slide): bumped from
    # ANNOT_FS-1 (16pt) to 30pt, calibrated against this figure's own new crop (see the
    # save_fit call below) so it lands ~16-18px on-slide -- clear of the 13px page-number
    # floor with real margin, not just past it.
    place_label(ax, (A[0], A[1] - 0.5), "in 0 / out 2", obstacles=obstacles, color=MUTED,
                fontsize=36, ha="center", va="top", clearance_pt=4.0, zorder=5,
                name="directed-parity:A")
    place_label(ax, (B[0], B[1] - 0.5), "in 2 / out 0", obstacles=obstacles, color=MUTED,
                fontsize=36, ha="center", va="top", clearance_pt=4.0, zorder=5,
                name="directed-parity:B")
    # R10 fix (FIXES_R10.md, Blocker 1's "nine more" list -- 22% ink, the worst of the nine):
    # save()'s bbox_inches="tight" crops to this axes' DECLARED xlim/ylim (-1.3..1.3 x
    # -0.95..0.95), not to the two nodes + labels actually drawn in it. save_fit crops to the
    # real rendered extent; `w:` (reported to the deck agent) controls on-slide size instead.
    #
    # R12 fix ("an order of magnitude smaller than its siblings"): out_dpi=TINY_OUT_DPI was
    # calibrated for a figure that's basically ONE node (selfloop, edge-single-node) --
    # applied here, to a two-node-plus-two-annotation-blocks figure, it shrank the whole
    # saved file to 353x149px, small enough that it renders at native 1:1 with no deck
    # downscale at all (the drawing itself only 61px tall on the actual slide). Dropped in
    # favour of the deck's normal 200dpi, same as directed-arrows/strong/weak -- this figure
    # has enough content to earn its own share of the 380px height cap like they do.
    save_fit(fig, ax, "directed-parity-counterexample.png", pad_frac=0.08, pad_min_in=0.9)


# ===========================================================================
# Part 6 -- representation
# ===========================================================================
def fig_store_edgelist():
    # Highlight all three of node 1's edges/rows, matching store-adjlist.png -- the prose
    # on this slide says finding node 1's neighbours means scanning every row, so a single
    # highlighted edge understated what "scanning" finds (slide-047 consistency fix).
    #
    # The list panel is much taller-than-wide (6 rows) than the graph panel is -- with two
    # plain equal-width subplots, equal-aspect centers each panel's box inside its cell,
    # leaving a dead gap between them that a global tight-bbox crop can't remove. A
    # GridSpec sized to each panel's own content aspect closes that gap.
    node1_edges = [(1, 0), (1, 2), (1, 3)]
    hi = {frozenset(e) for e in node1_edges}
    fig = plt.figure(figsize=(8.4, 5.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1.0], wspace=0.25)

    ax = fig.add_subplot(gs[0, 0])
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-1.4, 1.4)
    clean(ax)
    # fit_node_scale measures this panel's own axes box directly -- correct regardless of
    # the gridspec's width_ratios -- see fig_adjacency_matrix.
    W = fit_node_scale(fig, ax, r=GRAPH5_R)  # R9 fix ("the one cause") -- see GRAPH5_R's note
    draw_graph5(ax, highlight_edges=node1_edges, highlight_nodes={1}, r=GRAPH5_R)

    ax = fig.add_subplot(gs[0, 1])
    y0 = 5
    for i, (u, v) in enumerate(GRAPH5_EDGES):
        y = y0 - i
        hl = frozenset((u, v)) in hi
        edgecolor = ACCENT2 if hl else "none"
        lw = 2.6 if hl else 0
        ax.add_patch(FancyBboxPatch((0.0, y - 0.35), 1.9, 0.7,
                                     boxstyle="round,pad=0.02,rounding_size=0.3",
                                     facecolor=PANEL, edgecolor=edgecolor, linewidth=lw, zorder=2))
        # Fixed size, not fs()-scaled: "0 -- 1" must stay clear of a 1.9-unit-wide box.
        # R9 fix ("free-standing annotations... need their own size bump", FIXES_R9.md): was
        # 20pt, ~15.3px on-slide -- just under the 16px page-number floor. Checked against
        # the box width directly (get_window_extent): the longest row ("0 -- 1") uses under
        # a quarter of the box's own rendered width even at this size, real room to spare.
        # R12 fix ("the one thing that has not landed"): 22pt still landed under the 21px
        # floor once measured against this figure's own container/scale -- the box has real
        # room (see the note above), so raised directly.
        ax.text(0.95, y, f"{u} — {v}", ha="center", va="center", fontsize=30, color=INK, zorder=3)
    ax.set_xlim(-0.3, 2.2)
    ax.set_ylim(-0.55, 5.7)
    # title removed -- duplicated the figcaption verbatim
    clean(ax)
    save(fig, "store-edgelist.png")


def fig_store_adjlist():
    adj = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 4], 3: [1, 4], 4: [2, 3]}
    fig, axes = plt.subplots(1, 2, figsize=(10.6, 5.0))
    ax = axes[0]
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-1.4, 1.4)
    clean(ax)
    W = fit_node_scale(fig, ax, r=GRAPH5_R)  # R9 fix ("the one cause") -- see GRAPH5_R's note
    # R12 fix ("the one thing that has not landed"): the deck-wide LABEL_FS (30pt) landed
    # 19.7px on-slide against THIS figure's own wider-than-usual (10.6in) canvas -- overridden
    # directly rather than raising the shared constant every OTHER graph5 figure already
    # clears with margin.
    draw_graph5(ax, highlight_edges=[(1, 0), (1, 2), (1, 3)], highlight_nodes={1}, r=GRAPH5_R,
                label_fs=38)

    ax = axes[1]
    y0 = 5
    for i, n in enumerate(range(5)):
        y = y0 - i
        # R7 fix (Minor, slide 055): "->" reads as direction -- a claim this deck elsewhere
        # establishes explicitly for directed graphs -- but this is a plain adjacency list
        # for an UNDIRECTED graph. A colon carries no directional claim.
        text = f"{n}: " + ", ".join(str(m) for m in adj[n])
        hl = n == 1
        edgecolor = ACCENT2 if hl else "none"
        lw = 2.6 if hl else 0
        ax.add_patch(FancyBboxPatch((0.0, y - 0.35), 2.6, 0.7,
                                     boxstyle="round,pad=0.02,rounding_size=0.3",
                                     facecolor=PANEL, edgecolor=edgecolor, linewidth=lw, zorder=2))
        # Fixed size, not fs()-scaled: rows like "1 -> 0, 2, 3" must stay inside a
        # 2.6-unit-wide box -- the literal fs() scale (~37pt) overflowed it.
        # R9 fix ("free-standing annotations... need their own size bump", FIXES_R9.md): was
        # 18pt, ~11.4px on-slide -- under the 16px page-number floor. Checked against the box
        # width directly (get_window_extent): the longest row ("1: 0, 2, 3") uses under a
        # quarter of the box's own rendered width even at this size, real room to spare.
        # R12 fix ("the one thing that has not landed"): 26pt still landed under the 21px
        # floor once measured against this figure's own container/scale -- more room to
        # raise it further (see the note above).
        ax.text(1.3, y, text, ha="center", va="center", fontsize=34, color=INK, zorder=3)
    ax.set_xlim(-0.3, 2.9)
    ax.set_ylim(0.2, 5.7)
    # title removed -- duplicated the figcaption verbatim
    clean(ax)
    save(fig, "store-adjlist.png")


def fig_store_matrix():
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 5.0))
    ax = axes[0]
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-1.4, 1.4)
    clean(ax)
    W = fit_node_scale(fig, ax, r=GRAPH5_R)  # R9 fix ("the one cause") -- see GRAPH5_R's note
    # R12 fix ("the one thing that has not landed"): see fig_store_adjlist's own note --
    # same override, same reason (this figure's canvas is wider than the deck-wide LABEL_FS
    # was calibrated against).
    draw_graph5(ax, highlight_edges=[(1, 0), (1, 2), (1, 3)], highlight_nodes={1}, r=GRAPH5_R,
                label_fs=38)

    ax = axes[1]
    A = graph5_adjacency()
    # title removed -- duplicated the figcaption verbatim
    draw_matrix(ax, A, row_highlight=1, cell_fs=fs(18, W))
    # R7 fix (Major 20): the "row 1 (red) is node 1's row: 1s at columns ..." sentence this
    # used to print here was baked-in AND repeated verbatim as the deck's own figcaption --
    # L2 bans duplicate captions the same as it bans tables. The red row/edges/node already
    # carry the connection visually (same red on the graph panel's highlighted node/edges and
    # this panel's highlighted row); the sentence explaining it belongs in exactly one place,
    # the figcaption, not baked into the PNG a second time.
    save(fig, "store-matrix.png")


def _fig_csr(name, payoff=False):
    # R3 fix (Major 19): at the old figsize=(11.2, 5.6), the array panel's text rendered
    # ~9.5px in the deck -- smaller than the 18px page number -- because a fixed point-size
    # shrinks hardest in an 11.2in-wide figure once it's scaled down to the ~520px display
    # column every w:520 figure shares. Narrower figsize (less to shrink) AND dropping the
    # per-cell position-index sub-row (the least load-bearing element, freeing width for a
    # wider array-panel share) both apply together, since neither alone bought enough room
    # for the two-digit indptr/index values (10, 11, 12) without overlapping cells.
    adj = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 4], 3: [1, 4], 4: [2, 3]}
    data, indices, indptr = [], [], [0]
    for i in range(5):
        for j in adj[i]:
            data.append(1)
            indices.append(j)
        indptr.append(len(data))
    # indptr = [0, 2, 5, 8, 10, 12]; row 1 = data[2:5] == indices[2:5]

    # The matrix only ever shows single digits (0/1); the array panel has to fit two-digit
    # values (10, 11, 12) into 12 columns -- so the matrix panel's share is cut hard, not
    # the old ~1:1.7, to give the array panel's cells as much width as possible.
    #
    # R4 fix (Major 14): a fixed cell_fs=13 in the matrix panel next to fs()-scaled array
    # cells left the matrix as the least legible element on the slide once R3 fixed only
    # the array side (10-14px row bands). Rather than cut the inset (it's the one thing on
    # this slide tying the array back to the graph everyone already knows), its panel gets
    # enough of the figure's width that its cells render at the SAME size as the array
    # cells -- one cell_fs for both, computed once below.
    W = 7.8
    fig = plt.figure(figsize=(W, 5.0))
    # Matplotlib's default subplot margins (~12.5% left, ~10% right of the FIGURE) were
    # quietly eating into both panels' width -- measured directly, axR was rendering at
    # only 3.83in even though its width_ratio nominally implied ~6.3in. Reclaiming that
    # margin (this figure has no axis ticks/labels of its own needing the room) is what
    # actually buys the matrix panel's cells the size bump Major 14 asks for, without
    # inflating W further.
    fig.subplots_adjust(left=0.01, right=0.995, top=0.98, bottom=0.02)
    # R12 fix: shifted toward the array panel (0.62:2.0 -> 0.55:2.05) -- the matrix panel
    # only ever shows single digits (0/1), which need far less width than the array panel's
    # two-digit values (10, 11, 12) packed 12 to a row, so it can give up some share. NOT
    # shifted as far as a first attempt (0.32:2.3) tried: that starved the matrix panel badly
    # enough that its OWN tick labels (0-4, at cell_fs -- see MATRIX_FS below) overflowed
    # its axes box and printed on top of "data"/"indices" next door -- rendered and caught by
    # eye, not by an assertion, which is exactly the failure mode this file's
    # _assert_*-style checks exist to catch instead.
    gs = fig.add_gridspec(1, 2, width_ratios=[0.5, 2.04], wspace=0.15)

    # Cells are only ~0.9 data-units apart and indptr/index values run into two digits
    # (10, 11, 12) -- VALUE_FS is measured (not guessed) to clear the box at this width:
    # matplotlib text-extent for "12" is ~1.28x the point size, and each box now renders
    # ~25pt wide (measured against the reclaimed-margin layout above), so anything under
    # ~19pt leaves real margin. Still a real increase over the pre-R3 9.5px render --
    # clears the 18px page number the review measured against.
    #
    # R12 fix ("the one thing that has not landed"): 18pt (fs(12.0, W)) still landed 16px
    # on-slide against the 21px floor once measured against THIS figure's own container/
    # scale. Bumped and checked directly against the box width via the `row()` closure's own
    # assertion below, instead of trusting a stale hand-measurement in this comment.
    #
    # R12 fix, second: MATRIX_FS is no longer tied to VALUE_FS -- the matrix panel's own
    # (now smaller) width caps what its single-digit cells can carry independently of
    # whatever the array panel's two-digit boxes need; matching them was the R4 fix's
    # intent when both panels split the width evenly, not a constraint that survives this
    # round's uneven split.
    VALUE_FS, ROWLABEL_FS = fs(15.1, W), fs(15.6, W)
    MATRIX_FS = fs(19.0, W)

    axA = fig.add_subplot(gs[0, 0])
    A = graph5_adjacency()
    draw_matrix(axA, A, row_highlight=1, row_highlight_color=ACCENT3, cell_fs=MATRIX_FS)
    # title removed -- the review's "no suptitle" fix already dropped the old 11px
    # explanatory line; this panel doesn't need one either.
    # R12 fix: this inset is a small visual callback ("same matrix, same red row you saw
    # two slides ago"), not a place a student reads row/column INDICES off of -- store-
    # matrix.png already does that job at full size. Its own row/col tick labels were the
    # thing actually overflowing this shrunken panel (confirmed: removing them, not
    # shrinking MATRIX_FS further, is what stopped "01234" printing on top of "data" next
    # door) -- dropped outright rather than fought over with an even smaller fontsize.
    # draw_matrix moves ticks to the top (xaxis.set_ticks_position("top")), so it's
    # labeltop, not labelbottom, that actually gates the column-index row -- confirmed by
    # the first attempt at this (labelbottom=False) rendering "01234" anyway.
    axA.tick_params(labeltop=False, labelleft=False, length=0)

    axR = fig.add_subplot(gs[0, 1])
    # R12 fix: right margin tightened from 12.0 -- 0.54 units of pure dead space past the
    # last box (right edge at 11.46). Left margin, in the OTHER direction, had to grow
    # instead of shrink: measured directly (get_window_extent, not eyeballed), "indices" at
    # ROWLABEL_FS overflowed a -1.6-units-left margin by ~190px, well into the matrix
    # panel's own column -- caught by the assertion below, not by a human re-reading the
    # PNG. -3.4 is the smallest left bound that clears it with real margin.
    axR.set_xlim(-3.0, 11.5)
    # R5 fix (Blocker 7): bottom margin pulled in from -1.35 -- that was sized for a second
    # text line now deleted (see below); keeping the old margin would leave dead white space
    # under the one remaining line.
    # R12 fix: payoff's bottom margin grew again (-0.95 -> -1.5) to fit the "indptr[2] -
    # indptr[1]..." line broken onto two rows -- see that text's own note below.
    axR.set_ylim(-1.5 if payoff else -0.6, 3.0)
    axR.set_axis_off()

    def row(y, values, label, highlight_range=None):
        for i, v in enumerate(values):
            fc = ACCENT3 if highlight_range and highlight_range[0] <= i < highlight_range[1] else PANEL
            # Minor fix (slide 053): 0.88-wide boxes let two-digit values (10, 12) touch
            # their own box edge and abut the next cell, reading as "8 1012"; a touch wider.
            box = FancyBboxPatch((i - 0.5, y - 0.34), 1.0, 0.68,
                                  boxstyle="round,pad=0.02,rounding_size=0.1",
                                  facecolor=fc, edgecolor=RULE, linewidth=1.0, zorder=2)
            axR.add_patch(box)
            t = axR.text(i, y, str(v), ha="center", va="center", fontsize=VALUE_FS, color=INK, zorder=3)
            # R12 fix: VALUE_FS was bumped for on-slide legibility (see the module note
            # above) without re-measuring whether a two-digit value still clears its own
            # box -- measure it directly instead of trusting the stale hand-calibration the
            # old comment here was built on.
            renderer = _finalize(axR)
            tb = t.get_window_extent(renderer)
            bb = box.get_window_extent(renderer)
            assert tb.width <= bb.width, (
                f"csr row {label!r}: {v!r} at {VALUE_FS}pt is {tb.width:.0f}px wide, wider "
                f"than its own {bb.width:.0f}px box -- shrink VALUE_FS or widen the box."
            )
        axR.text(-0.85, y, label, ha="right", va="center", fontsize=ROWLABEL_FS, color=ACCENT,
                  fontweight="bold", zorder=3)

    y_indptr, y_data, y_indices = 2.35, 1.3, 0.0
    # indptr row (6 entries), highlight positions 1 and 2 (values 2 and 5)
    row(y_indptr, indptr, "indptr", highlight_range=(1, 3))
    row(y_data, data, "data", highlight_range=(2, 5))
    row(y_indices, indices, "indices", highlight_range=(2, 5))

    # connector lines: indptr[1] -> left boundary of run; indptr[2] -> right boundary.
    # Boundary x-positions are hand-placed box edges (index - 0.44); assert they still
    # match indptr so a future change to `adj` can't silently point the connectors wrong.
    assert (indptr[1], indptr[2]) == (2, 5), f"connector boundaries assume indptr[1:3]==(2,5), got {indptr[1:3]}"
    for i, xb in zip((1, 2), (1.5, 4.5)):
        axR.add_patch(FancyArrowPatch((i, y_indptr - 0.32), (xb, y_data + 0.32),
                                       arrowstyle="-", color=ACCENT3, linewidth=2.2, zorder=1))
        axR.plot([xb, xb], [y_data - 0.32, y_indices - 0.32], color=ACCENT3, linewidth=2.0,
                  linestyle=(0, (4, 3)), zorder=1)

    if payoff:
        # R3 fix (Major 18): slide 053 embedded the SAME csr-build.png as slide 052, under
        # the identical caption, printing neither of this slide's own results. This variant
        # spells out the row-1 slice length below the arrays (there's no room beside a
        # single 0.88-unit cell for a sentence this long) -- the "degree" half of "degree
        # and memory".
        #
        # R5 fix (Blocker 7): the memory claim ("stores nnz = 12 numbers here, not the dense
        # 5x5 = 25") used to print here too, in 12px gray under the arrays -- the third round
        # this exact claim got split off the degree slide, and only the asymptotic O(n^2) vs
        # O(nnz) statement actually moved with it. Deleted outright; the concrete 12-vs-25
        # count now lives on slide 055's own figure (fig_memory_payoff) as the evidence for
        # that slide's asymptotic claim, where it belongs.
        mid = 5.2
        # R12 fix ("the one thing that has not landed"): 18.75pt (fs(12.5, W)) landed 17px
        # on-slide against the 21px floor. This line spans nearly the full axR width with
        # no box to overflow, unlike the array cells above -- room to raise it directly.
        # R12 fix ("the one thing that has not landed"): one line at a size that clears the
        # legibility floor is wider than the array panel itself, and bbox_inches="tight"
        # widens the WHOLE canvas to fit it -- which shrinks the deck's downscale factor for
        # every OTHER element on the slide (the array digits above), undoing their own R12
        # fix. Broken across two lines instead, so a legible size fits within the panel's own
        # natural width.
        axR.text(mid, -0.75, "indptr[2] − indptr[1]\n= 5 − 2 = 3 = k₁", ha="center", va="center",
                 color=ACCENT3, fontsize=fs(18.0, W), fontweight="bold", zorder=3, linespacing=1.3)

    # R12 fix: catches, by construction, the exact failure the first attempt at this round's
    # width rebalance shipped (MATRIX_FS too big for its shrunken panel -- its own tick
    # labels bled out of axA and printed on top of axR's "data"/"indices" labels; only
    # caught because someone looked at the PNG). axA's true rendered extent (every artist,
    # including tick labels) must not reach axR's true rendered extent.
    renderer = _finalize(fig)
    bbA = axA.get_tightbbox(renderer)
    bbR = axR.get_tightbbox(renderer)
    assert bbA.x1 < bbR.x0, (
        f"_fig_csr: matrix panel's rendered content (right edge {bbA.x1:.0f}px) overlaps "
        f"the array panel's (left edge {bbR.x0:.0f}px) -- MATRIX_FS is too big for its "
        f"panel's width_ratio share, or the panels need more wspace."
    )

    save(fig, name)


def fig_csr_build():
    _fig_csr("csr-build.png")


def fig_csr_payoff():
    _fig_csr("csr-payoff.png", payoff=True)


def _csr_vs_dense_counts(n, avg_degree):
    """(dense, csr) total NUMBERS stored for an n x n adjacency at the given average row
    degree -- dense stores n**2 cells; CSR stores nnz (data) + nnz (indices) + (n+1)
    (indptr). Used by fig_memory_payoff to compute its illustrative larger-n rows the same
    way it computes its real n=5 example, so nothing in that figure is hand-typed."""
    nnz = round(avg_degree * n)
    dense = n * n
    csr = 2 * nnz + (n + 1)
    return dense, csr


def fig_memory_payoff():
    # R9 fix (Blocker 6, "bar charts are now out"): FIGURE_GUIDE.md bans bars outright --
    # "Bars encode one number as a length and then need a scale to decode it" -- and this
    # figure's own n=100,000 pair was the guide's worked example of exactly that failure:
    # measured, dense drew at 85px / CSR at 11px (a drawn ratio of 7.7:1) under a label
    # reading "7,700x", a thousandfold gap with no axis, no break-mark scale note, and a
    # SECOND bar pair two rows up sharing the same frame at a completely different implied
    # scale (1px =~ 0.39 units there vs 1px =~ 118M units here). No amount of "clearer
    # labeling" fixes that -- the fix is to stop encoding the numbers as lengths at all.
    #
    # Also dropped per the same fix: the n=5 dense-matrix + CSR-array top half, which was
    # slides 052/053's own figure (_fig_csr) shown a third time, and the baked-in sentence
    # underneath it, which duplicated the slide body.
    #
    # What is left is the numbers themselves, annotated -- the actual claim this slide makes
    # ("the payoff: memory" is about n=100,000, not the small honest counterexample) -- with
    # the ratio computed and stated once, and the assumption behind it (average degree 6)
    # printed beside it so the claim is checkable against the two numbers above it.
    dense, csr = _csr_vs_dense_counts(100_000, 6)
    assert (dense, csr) == (10_000_000_000, 1_300_001), (dense, csr)
    ratio = dense / csr

    # Fixed point sizes, not fs()-scaled: fs() scales by the FINAL figure width, but that
    # width is exactly what this layout has to SOLVE for (wide enough to clear the two
    # numbers, "10,000,000,000" vs "1,300,001", without them overlapping) -- scaling the
    # font by the answer to that question is a feedback loop with no fixed point. A fixed
    # size plus a generous xlim, cropped tight by save_fit regardless of the final width,
    # sidesteps it (same reasoning fig_csr_build/_payoff already documented for their own
    # two-panels-of-different-widths layout).
    # R12 fix ("the one thing that has not landed"): tag_fs/ratio_fs/note_fs measured
    # 18.3/20.1/18.3px on-slide against this figure's own container/scale, under the 21px
    # floor -- bumped with margin.
    num_fs = 30
    tag_fs = 24
    ratio_fs = 26
    note_fs = 24

    fig, ax = plt.subplots(figsize=(9.5, 3.35))
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 4.55)
    clean(ax)

    t_dense = ax.text(3.6, 3.55, f"{dense:,}", ha="center", va="center", color=INK,
                       fontsize=num_fs, fontweight="bold", zorder=2)
    ax.text(3.6, 2.7, "dense", ha="center", va="center", color=MUTED, fontsize=tag_fs, zorder=2)

    t_csr = ax.text(12.4, 3.55, f"{csr:,}", ha="center", va="center", color=ACCENT3,
                     fontsize=num_fs, fontweight="bold", zorder=2)
    ax.text(12.4, 2.7, "CSR", ha="center", va="center", color=MUTED, fontsize=tag_fs, zorder=2)

    # Assert the two numbers actually clear each other -- this is a two-column figure with
    # no axis/legend to catch an overlap the way a plot's own ticks would.
    renderer = _finalize(ax)
    b_dense = t_dense.get_window_extent(renderer)
    b_csr = t_csr.get_window_extent(renderer)
    assert b_dense.x1 < b_csr.x0, (
        f"fig_memory_payoff: the two numbers overlap ({b_dense.x1:.0f}px vs {b_csr.x0:.0f}px) "
        f"-- widen the xlim gap between them."
    )

    arrow = FancyArrowPatch((6.0, 3.55), (10.0, 3.55), arrowstyle="-|>", mutation_scale=16,
                             color=MUTED, linewidth=1.6, zorder=1,
                             connectionstyle="arc3,rad=-0.25")
    ax.add_patch(arrow)

    # Ratio stated once, computed from the two numbers above -- never hardcoded (the guide's
    # own rule: "Compute every number a figure prints from the data").
    ax.text(8.0, 1.55, f"CSR is {ratio:,.0f}× smaller", ha="center", va="center",
            color=INK, fontsize=ratio_fs, fontweight="bold", zorder=2)
    ax.text(8.0, 0.75, "n = 100,000, average degree 6", ha="center", va="center",
            color=MUTED, fontsize=note_fs, zorder=2)

    save_fit(fig, ax, "csr-memory.png", pad_frac=0.08, pad_min_in=0.06)


def fig_format_regimes():
    # All four quadrants labeled now, not just the two the deck cares about -- the other
    # two were blank and unexplained (F1/F5 fix). Only theme tokens: the old off-token
    # fills (#e8e5e0 / #f7f2ef-ish) are gone; the two *answer* quadrants get PANEL, the
    # other two are left on the plain white background so they read as secondary.
    # Font sizes here are fixed, not fs()-scaled: the two left quadrants are only 3 of
    # 10 x-units wide, a hard layout constraint independent of the figure's own width,
    # so scaling text by overall figure width (as elsewhere) overflowed them.
    #
    # R4 fix (Major 13 / Policy 2): this slide's `.fig.tight` div was believed to cap the
    # image at 320px tall, not the deck's usual 430px, so the figure was shrunk to 4.85x3.35
    # to compensate.
    #
    # R5 fix (Major 19): that premise didn't hold -- measured against the actual rendered
    # slide, format-regimes.png displays at the SAME ~760px column every other `w:760`
    # figure gets (connected-vs-not.png, components-band.png, ...), so the 4.85in figure was
    # shrinking itself for a cap that wasn't being applied, dragging every label down with
    # it. Regenerated at the size those siblings use.
    # R10 fix (Major 16): xlim widened past the 0-10 grid (to 11.8) to give the "real
    # networks live here" callout its OWN dedicated margin at the right, instead of
    # squeezing it into the same 10-unit box the four quadrants use -- see arrow_x below.
    W = 10.0
    fig, ax = plt.subplots(figsize=(11.8, 5.0))
    ax.set_xlim(0, 11.8)
    ax.set_ylim(0, 10)

    # R10 fix (Major 16 -- the four regime labels measured 8px on-slide against 16-18px axis
    # labels in this same figure, a 2x in-figure disparity). Calibrated off that measurement
    # (8px at the old 16-17pt -> ~0.48 native-px-per-pt at this figure's own w:760 scale) to
    # clear the floor with real margin: one shared size for every regime/outcome tag in the
    # figure (REGIME_FS), distinct from the bold quadrant headline names (CSR / dense array),
    # which are already legible and unflagged. Capped at 22 (not the ~34 the calibration alone
    # would suggest) -- the left quadrants are only 3 of 10 x-units wide and 5 of 10 y-units
    # tall, and every text position below was re-measured (get_window_extent) at this size to
    # confirm neither quadrant's headline+regime pair crosses the other's, nor the y=5 rule.
    # R12 fix ("the one thing that has not landed"): 22pt still measured under the 15px
    # x-height floor on the real rendered slide. Bumped again; re-measured (below) to confirm
    # nothing in the two narrow left quadrants collides.
    REGIME_FS = 30

    # bottom-right: large + sparse -- CSR's regime
    ax.add_patch(mpatches.Rectangle((3, 0), 7, 5, facecolor=PANEL, edgecolor=RULE, linewidth=1.5, zorder=1))
    ax.text(6.5, 3.2, "CSR", ha="center", va="center", fontsize=26, color=INK, fontweight="bold", zorder=2)
    ax.text(6.5, 1.8, "large + sparse", ha="center", va="center", fontsize=REGIME_FS, color=MUTED, zorder=2)

    # top-left: small + dense -- dense array's regime
    ax.add_patch(mpatches.Rectangle((0, 5), 3, 5, facecolor=PANEL, edgecolor=RULE, linewidth=1.5, zorder=1))
    ax.text(1.5, 8.5, "dense\narray", ha="center", va="center", fontsize=26, color=INK, fontweight="bold", zorder=2)
    ax.text(1.5, 6.35, "small\n(or dense)", ha="center", va="center", fontsize=REGIME_FS, color=MUTED, zorder=2)

    # top-right: large + dense -- rare in practice, unfilled but no longer unlabeled
    ax.text(6.5, 8.3, "large + dense", ha="center", va="center", fontsize=REGIME_FS, color=MUTED, zorder=2)
    ax.text(6.5, 6.6, "rare in practice", ha="center", va="center", fontsize=REGIME_FS, color=MUTED, zorder=2)

    # bottom-left: small + sparse -- either format works, size dominates
    ax.text(1.5, 3.5, "small +\nsparse", ha="center", va="center", fontsize=REGIME_FS, color=MUTED, zorder=2)
    ax.text(1.5, 1.1, "either\nis fine", ha="center", va="center", fontsize=REGIME_FS, color=MUTED, zorder=2)

    ax.plot([3, 3], [0, 10], color=RULE, linewidth=1.2, zorder=1)
    ax.plot([0, 10], [5, 5], color=RULE, linewidth=1.2, zorder=1)

    # R5 fix (Major 19): the arrow sat at x=8.6, but "large + sparse" (and "large + dense"
    # above it) render far wider than their short word count suggests at this fontsize --
    # measured directly, both span roughly x=[4.4, 8.6] -- so the arrow's head landed
    # exactly on the terminal "e" of "sparse" and its shaft grazed "dense"'s.
    #
    # R10 fix (Major 16): moving x=9.3 -> x=10.9, INTO the new margin past the grid's own
    # x=10 edge (see xlim above), rather than trying to squeeze this callout and the bigger
    # REGIME_FS text into the same 10 units -- re-measured (get_window_extent) at REGIME_FS
    # to confirm real clearance from "large + dense"/"rare in practice" (>1 data unit).
    arrow_x = 10.9
    place_annotation(ax, (arrow_x, 1.1), "real networks\nlive here", xytext=(arrow_x, 9.2),
                      obstacles=[], color=MUTED, fontsize=REGIME_FS, ha="center",
                      lw=2, arrowstyle="-|>", name="format-regimes:real-networks")
    ax.set_xlabel("network size →", fontsize=fs(18, W), color=INK)
    # R10 fix: set_xlabel centers on the full AXES width by default, but that width now
    # includes the callout's margin past x=10 (see xlim above) -- re-centred under the actual
    # 0-10 grid instead of the whole 0-11.8 canvas. y picked to match this label's own default
    # vertical offset (checked against the rendered PNG, not the mixed-unit value
    # xaxis.label.get_position() returns before a layout pass -- that value is in POINTS, not
    # axes-fraction, and feeding it straight into set_label_coords blew the canvas up 80x).
    ax.xaxis.set_label_coords((10 / 11.8) / 2, -0.08)
    ax.set_ylabel("density →", fontsize=fs(18, W), color=INK)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(RULE)
    save(fig, "format-regimes.png")


# ===========================================================================
# Part 7 -- edge cases
# ===========================================================================
# R4 fix (Policy 2): bbox_inches="tight" turns out NOT to crop a bare marker down to its own
# footprint -- Axes.get_tightbbox() still reports (close to) the full declared xlim/ylim
# extent even with the axis off, confirmed by an isolated repro. save_fit (see fig_selfloop's
# R5 fix) replaces that guess with a crop measured directly off the real rendered content.
#
# R8 fix: figsize is square now (was 1.48x1.3, landscape) -- a lone node is Circle-drawn now
# (see the module note above NODE_R), and a Circle needs equal aspect to render round; the
# old landscape figsize relied on ax.scatter's aspect-independence, which no longer applies.
EDGE_SINGLE_FIGSIZE = (1.4, 1.4)

# R9 fix (FIXES_R9.md): the old out_dpi=1200 + pad_min_in=0.05 combo was the OTHER figure
# that "bypasses the machinery" -- one lone node is nearly the whole canvas (content ~150px
# square at 200dpi, whatever the out_dpi), so the CSS scale-to-fit (`max-height:380px`,
# `width:auto`) barely shrinks it: measured on the real rendered slide, 296px against a
# 34-40px target -- 41% of slide height, under a caption reading "the smallest possible
# graph".
#
# R10 fix (FIXES_R10.md, "the one cause, one level further out"): R9's answer -- pad the
# canvas out with ~3.25in of absolute white margin so a FIXED w:520 lands the target size --
# is exactly what check_render.py now measures as the defect: this canvas at 1-3% ink, the
# disc landing at 39-63px on a side inside a 380x380 box that is otherwise blank. A figure
# this sparse (one disc, nothing else) has TWO independent on-slide-size levers -- the crop's
# own pixel size, and the deck's per-slide `w:` -- and padding the canvas only ever pulled the
# first one. Small, fixed pad here; `w:` (chosen per figure and reported to the deck agent)
# does the on-slide-size work instead.
EDGE_SINGLE_PAD_IN = 0.18


def fig_edge_single_node():
    fig, ax = plt.subplots(figsize=EDGE_SINGLE_FIGSIZE)
    ax.set_xlim(-0.55, 0.55)
    ax.set_ylim(-0.55, 0.55)
    clean(ax)
    fit_node_scale(fig, ax)
    draw_node(ax, (0, 0), color=INK, zorder=2)
    save_fit(fig, ax, "edge-single-node.png", pad_frac=0.08, pad_min_in=EDGE_SINGLE_PAD_IN,
             out_dpi=TINY_OUT_DPI)


def fig_edge_single_node_answer():
    # Minor fix: slide 059's caption asserts "one node, one component" but the reused
    # edge-single-node.png (same figure as the still-open question on 058) has nothing
    # visual marking a component -- a thin ring earns the word, and distinguishes the
    # "answer" frame from the "question" frame it was previously identical to.
    fig, ax = plt.subplots(figsize=EDGE_SINGLE_FIGSIZE)
    ax.set_xlim(-0.55, 0.55)
    ax.set_ylim(-0.55, 0.55)
    clean(ax)
    fit_node_scale(fig, ax)
    node_r_pt_es = node_radius_pt(ax)
    draw_ring(ax, (0, 0), k=1.7, color=MUTED, lw=0.65, zorder=1,
              node_obstacles=[circle_obstacle((0, 0), node_r_pt_es)],
              name="edge-single-node-answer:ring")
    draw_node(ax, (0, 0), color=INK, zorder=2)
    save_fit(fig, ax, "edge-single-node-answer.png", pad_frac=0.08, pad_min_in=EDGE_SINGLE_PAD_IN,
             out_dpi=TINY_OUT_DPI)


def fig_edge_disconnected():
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    t1 = {"a": (-1.3, 0.55), "b": (-1.95, -0.4), "c": (-0.65, -0.4)}
    t2 = {"d": (1.3, 0.55), "e": (0.65, -0.4), "f": (1.95, -0.4)}
    # R5 fix (Major 15, historical): the old xlim/ylim margin around the outermost node
    # centres (b/f at x=+-1.95) was narrower than the scatter marker's own true radius, so
    # the outermost discs got flat-clipped at the frame boundary. NODE_R (0.12 data units)
    # is small enough, deck-wide, that this margin (0.47 data units to the frame edge) clears
    # it with real room to spare -- no clip_on=False guard needed any more.
    ax.set_xlim(-2.42, 2.42)
    ax.set_ylim(-0.87, 0.97)
    clean(ax)
    # R9 fix ("the one cause", FIXES_R9.md): this layout's own spacing (min 1.15 data units)
    # fixed the on-slide diameter at 25.3px independent of target_in -- see KONIGSBERG_R's
    # module note. 0.18 (ratio 0.157) stays well under the ~0.25 crowding ceiling.
    R = 0.18
    fit_node_scale(fig, ax, r=R)
    for tri in (t1, t2):
        keys = list(tri.keys())
        for i in range(3):
            u, v = keys[i], keys[(i + 1) % 3]
            ax.plot([tri[u][0], tri[v][0]], [tri[u][1], tri[v][1]], color=MUTED,
                     linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    allpos = {**t1, **t2}
    draw_nodes(ax, allpos, colors=INK, r=R, zorder=3)
    # "every degree even" removed -- it is the figcaption verbatim on this slide's first use.
    save(fig, "edge-disconnected.png")


# R7 fix (Major 5, requested by the deck agent): slide 068 used to reuse edge-disconnected.png
# (the two-triangles figure above) under the SAME figcaption slide 039 already used it under,
# 29 slides earlier -- the class works through the identical picture twice, and 039's own beat
# is pre-spoiled by the time 068 shows up. A different disconnected, all-even-degree graph:
# two separate 4-cycles (squares), same "two pieces, every node even" point, new picture.
def fig_edge_disconnected_2():
    fig, ax = plt.subplots(figsize=(6.0, 3.2))
    sq1 = {"a": (-1.75, 0.45), "b": (-0.85, 0.45), "c": (-0.85, -0.45), "d": (-1.75, -0.45)}
    sq2 = {"e": (0.85, 0.45), "f": (1.75, 0.45), "g": (1.75, -0.45), "h": (0.85, -0.45)}
    # Same margin reasoning as fig_edge_disconnected above.
    ax.set_xlim(-2.3, 2.3)
    ax.set_ylim(-0.9, 0.9)
    clean(ax)
    # R9 fix ("the one cause", FIXES_R9.md): this layout's own spacing (min 0.9 data units)
    # fixed the on-slide diameter at 26.6px independent of target_in -- see KONIGSBERG_R's
    # module note. 0.165 (ratio 0.183) stays under the ~0.25 crowding ceiling.
    R = 0.165
    fit_node_scale(fig, ax, r=R)
    for sq in (sq1, sq2):
        keys = list(sq.keys())
        for i in range(4):
            u, v = keys[i], keys[(i + 1) % 4]
            ax.plot([sq[u][0], sq[v][0]], [sq[u][1], sq[v][1]], color=MUTED,
                     linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    allpos = {**sq1, **sq2}
    draw_nodes(ax, allpos, colors=INK, r=R, zorder=3)
    save(fig, "edge-disconnected-2.png")


# ===========================================================================
# Wrap-up
# ===========================================================================
def fig_recap():
    fig, ax = plt.subplots(figsize=(6.6, 5.6))
    ax.set_xlim(-2.85, 2.15)
    ax.set_ylim(-2.15, 2.25)
    clean(ax)  # xlim/ylim/aspect finalized before any place_label call below
    fit_node_scale(fig, ax, r=KONIGSBERG_R_RECAP)  # R9 fix ("the one cause") -- see module note
    draw_kedges(ax)
    # R7 fix (Major 15, slide 069): "degree -> parity" pointed at bare node A with no degree
    # anywhere on the figure -- the label had no visible referent, and its leader overlapped
    # the dashed "one component" bracket for ~60px before landing 18px outside A, on nothing.
    # Same degree treatment as konigsberg-degrees.png/konigsberg-bombed.png (the deck's own
    # established convention: letters inside, degree numerals outside in accent-2 for odd) --
    # Konigsberg's four degrees (3, 3, 5, 3) are ALL odd, so all four nodes colour accent-2
    # here too, same as konigsberg-degrees.png.
    node_colors = {n: ACCENT2 for n in "NSAB"}
    draw_knodes(ax, colors=node_colors, r=KONIGSBERG_R_RECAP, label_fs=KONIGSBERG_LABEL_FS)
    obstacles = k_obstacles(ax, node_colors=node_colors, r=KONIGSBERG_R_RECAP)
    off = 0.34 * (KONIGSBERG_R_RECAP / NODE_R)
    deg = kedge_degrees()
    # R10 fix (FIXES_R10.md, Blocker 3): each settled degree numeral is kept (place_label
    # returns the real Text artist) and fed forward as an obstacle to "one component" below --
    # this used to be the ONE figure in the family where a later label was placed with no
    # knowledge of an earlier one, and it collided with exactly the numeral (N's, the top of
    # the diamond) that a bare ax.text a few lines down could not have known about.
    degree_texts = []
    for n, d in deg.items():
        ox, oy = K_OUTWARD[n]
        ha, va = K_OUTWARD_ALIGN[n]
        t = place_label(ax, (KPOS[n][0] + off * ox, KPOS[n][1] + off * oy), str(d),
                         obstacles=obstacles, color=ACCENT2, fontsize=KONIGSBERG_DEGREE_FS,
                         ha=ha, va=va, fontweight="bold", zorder=5, clearance_pt=3.0,
                         name=f"recap:degree-{n}")
        degree_texts.append(t)
    # R9 fix (Blocker 8): "degree -> parity" deleted outright. It never had a working leader
    # (R7's own fallback, "beside the numerals" with no line, still doesn't read as pointing
    # at anything in particular), and it never had a working REFERENT either: Konigsberg's
    # four degrees are (3, 3, 5, 3) -- every one of them odd -- so "parity" has exactly one
    # value on this graph and nothing to contrast it against; colouring all four nodes the
    # same accent-2 is the honest picture, not a broken attempt at a two-colour key. The
    # degree numerals above already carry the fact this label duplicated.
    #
    # "adjacency matrix, 4 x 4" deleted outright too -- no matrix is drawn anywhere in this
    # figure (FIXES_R9.md, Blocker 8). "one component" is the only one of the original three
    # annotations with a real referent (the dashed bracket below); it is the only one kept.
    bracket = mpatches.Ellipse((0, 0), 3.0, 3.0, fill=False, edgecolor=MUTED, linewidth=1.4,
                                linestyle=(0, (5, 4)), zorder=1)
    ax.add_patch(bracket)
    # R10 fix (FIXES_R10.md, Blocker 3 -- "one component" printed ON TOP of N's degree
    # numeral, min ink-to-ink distance 1.0px, 19px of "component" falling inside the "3"'s own
    # bounding box): a bare ax.text at a hand-picked (0, 1.72) had no idea N's numeral (also
    # hand-placed, at the diamond's own top) landed right there. Routed through place_label
    # against every degree numeral (degree_texts, above) plus the usual node/edge obstacles,
    # so it settles clear of N's "3" instead of guessing a y that used to almost match it.
    place_label(ax, (0, 1.72), "one component", obstacles=obstacles + [text_obstacle(t) for t in degree_texts],
                color=MUTED, fontsize=KONIGSBERG_DEGREE_FS, ha="center", va="bottom",
                clearance_pt=4.0, zorder=5, name="recap:one-component")
    # R12 fix ("the one thing that has not landed"): save() (bbox_inches="tight") crops to
    # the declared xlim/ylim window (generous, to fit the dashed "one component" ellipse with
    # room), not to what's actually drawn -- same excess-margin problem as
    # konigsberg-degrees.png, same fix: save_fit measures the TRUE rendered extent (the
    # ellipse patch is in ax.patches, so _content_px_bbox already covers it) with a small pad.
    save_fit(fig, ax, "recap.png", pad_frac=0.02, pad_min_in=0.1)


def fig_smallworld_teaser():
    # (a) k=4 ring lattice -- each node joined to its two nearest neighbors on *each*
    # side (not just one), so the base ring actually has the triangle-free-but-clustered
    # structure a small-world figure needs (the old j=(i+1)%n ring was k=2, with zero
    # triangles -- a counterexample to "high clustering", not an example of it).
    # (b) shortcuts use varied chord lengths, not four exact diameters that all cross the
    # center and read as a hub that doesn't exist (F2/F4 fix).
    # R3 fix (Major 20, historical): at n=20 the node discs touched each other, sitting at
    # zorder=3 over the edges' zorder=1, so BOTH the i-i+1 and i-i+2 edges were fully
    # occluded and the ring rendered as a smooth gray annulus. Fewer, more widely spaced
    # nodes (n=13) still give every second-neighbor chord room to clear the discs it passes
    # near, even at the deck-wide NODE_R this figure now draws at like every other one (R8
    # fix -- this was the deck's most undersized node, 9px, against 148px on the Konigsberg
    # figures the review picked as the target; see the module note above NODE_R).
    # R8 fix: n must be small enough that the i<->i+2 chord clears the intermediate
    # node it passes, or the second-neighbour edges vanish behind the discs and the
    # ring reads as a plain cycle -- no visible triangle, which is the one thing this
    # figure exists to show. The chord sits cos(2*pi/n) from the centre; the
    # intermediate node's inner edge is at 1-NODE_R. At the old n=13 that clearance
    # was -0.005 (the chord grazed the disc); n=9 gives +0.114.
    n = 9
    fig, ax = plt.subplots(figsize=(5.6, 5.6))
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    pts = {i: (np.cos(a), np.sin(a)) for i, a in enumerate(angles)}
    chord_clearance = (1.0 - NODE_R) - np.cos(2 * np.pi / n)
    assert chord_clearance > 0.05, (
        f"smallworld: second-neighbour chord clears the intermediate node by only "
        f"{chord_clearance:.3f} data units at n={n} -- the triangles will be hidden"
    )
    # "a few shortcuts change everything" removed -- it is the figcaption verbatim.
    # A touch of extra x-room (the ring itself stays circular) lands the crop <=0.95.
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.3, 1.3)
    clean(ax)
    fit_node_scale(fig, ax)
    for i in range(n):
        for step in (1, 2):
            j = (i + step) % n
            ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], color=MUTED,
                     linewidth=EDGE_W, zorder=1)
    for u, v in [(0, 4), (1, 6), (3, 7), (2, 8)]:
        ax.plot([pts[u][0], pts[v][0]], [pts[u][1], pts[v][1]], color=ACCENT2, linewidth=EDGE_W, zorder=2)
    draw_nodes(ax, pts, colors=INK, zorder=3)
    save(fig, "smallworld-teaser.png")


if __name__ == "__main__":
    fig_konigsberg_sketch()

    fig_abstraction_1_map()
    fig_abstraction_2_nodes()
    fig_abstraction_3_graph()
    fig_multigraph_bridges()
    fig_multigraph()
    fig_selfloop()
    fig_selfloop_answer()

    fig_degree_definition()
    fig_parity_even()
    fig_parity_odd()
    fig_parity_bound()
    fig_konigsberg_blank()
    fig_konigsberg_degrees()
    fig_euler_path_example()
    fig_euler_circuit_example()
    fig_konigsberg_bombed()

    fig_campus_base()
    fig_campus_walk()
    fig_campus_trail()
    fig_campus_path()
    fig_circuit_vs_cycle()
    fig_circuit()
    fig_cycle()
    fig_graph_labeled()
    fig_adjacency_matrix()
    fig_adjacency_squared()

    fig_connected_vs_not()
    fig_components_band()
    fig_components_intro()
    fig_components_bare()
    fig_sweep_1()
    fig_sweep_2()
    fig_sweep_3()
    fig_giant_scale()
    fig_directed_arrows()
    fig_directed_strong()
    fig_directed_weak()
    fig_directed_indegree()
    fig_directed_parity_counterexample()

    fig_store_edgelist()
    fig_store_adjlist()
    fig_store_matrix()
    fig_csr_build()
    fig_csr_payoff()
    fig_memory_payoff()
    fig_format_regimes()

    fig_edge_single_node()
    fig_edge_single_node_answer()
    fig_edge_disconnected()
    fig_edge_disconnected_2()

    fig_recap()
    fig_smallworld_teaser()

    if _TEXT_FAILURES:
        print(f"\n{len(_TEXT_FAILURES)} text-legibility failure(s) (MF_COLLECT_TEXT=1):")
        for m in _TEXT_FAILURES:
            print("  " + m)
        sys.exit(1)

    print("done")
