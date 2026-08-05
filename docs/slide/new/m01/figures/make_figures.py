#!/usr/bin/env python3
"""Generate Module 01 slide figures in the network-science theme palette.

Every figure obeys the review's global rules: uniform node size/fill unless a
slide explains the encoding, planar (crossing-free) layouts, legible-from-the-
back-row minimum sizes, and the fixed six-color palette below.
"""

from pathlib import Path

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import matplotlib.text as mtext
import matplotlib.transforms as mtransforms
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

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

LABEL_FS = 18
TITLE_FS = 18
ANNOT_FS = 17
EDGE_W = 3.5

# Output widths range ~3in (selfloop) to ~11in (csr-build), but every PNG gets shrunk
# to roughly the same displayed width in the deck. A fixed point-size therefore reads
# ~4x larger in a narrow figure than in a wide one. `fs()` scales a base point-size by
# a figure's own width relative to this reference so apparent text size stays constant.
FONT_REF_WIDTH = 5.2


def fs(base_pt, width_in, ref=FONT_REF_WIDTH):
    return round(base_pt * width_in / ref, 1)


# Same problem as fs(), for scatter markers: `s` is an area in points^2, rendered at a
# FIXED dpi regardless of a figure's own width, so its pixel diameter in the raw PNG does
# NOT depend on figsize -- but every PNG then gets shrunk to the same displayed width in
# the deck, so a marker drawn at a fixed `s` in an 11in-wide figure ends up much smaller
# on-slide than the same `s` in a 3.6in-wide figure (the R3 "cross-figure scale" minor:
# measured node diameters 71-109px for figures that should read as the same size). Since
# displayed diameter is proportional to sqrt(s)/width_in, s must scale as width_in^2 to
# keep it constant -- unlike fs() (linear in width), this one is squared.
NODE_S_REF = 2200


def node_s(width_in, base_s=NODE_S_REF, ref=FONT_REF_WIDTH):
    return base_s * (width_in / ref) ** 2


# The node marker's OWN rendered radius, in points, at the reference width -- derived
# straight from NODE_S_REF (area = pi * r^2) rather than a separately hand-picked constant.
# R4 fix (Major 18): _draw_directed used a hand-picked shrink of 24pt against a true radius
# of sqrt(2200/pi)=26.46pt, undershooting by ~2.5pt (~7px at dpi=200) -- enough that
# directed-indegree's arrowheads visibly stopped short of the node they point to. Deriving
# the shrink from the same constant that sizes the marker keeps the two in lock-step by
# construction; +3pt on top is deliberate overlap (a curved edge's shrink acts along its
# *local tangent*, not the radial direction, so a curved arc needs a small buffer beyond
# the geometric radius to still land inside the disc after that skew).
NODE_RADIUS_PT_REF = (NODE_S_REF / np.pi) ** 0.5


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


def node_radius_data(ax, size_pt2):
    """Radius, in DATA units, of an `ax.scatter(..., s=size_pt2)` marker at ax's current
    transform -- the geometric radius implied by the marker's own area, not a hand-measured
    guess (see fig_selfloop's R5 fix for what a stale guess costs)."""
    r_pt = (size_pt2 / np.pi) ** 0.5
    dx, dy = data_units_per_point(ax)
    return r_pt * dx, r_pt * dy


def scatter_bbox_px(ax, centers, size_pt2):
    """Display-space (x0, y0, x1, y1) bbox covering every marker of an `s=size_pt2` scatter
    at `centers` (data coords) -- collection.get_window_extent() does not compute this (an
    isolated repro returns an all-inf box for a PathCollection built from `s=`), so this
    derives it from the marker's own known geometry instead."""
    r_pt = (size_pt2 / np.pi) ** 0.5
    r_px = r_pt * ax.figure.dpi / 72.0
    xs, ys = [], []
    for (x, y) in centers:
        px, py = ax.transData.transform((x, y))
        xs += [px - r_px, px + r_px]
        ys += [py - r_px, py + r_px]
    return min(xs), min(ys), max(xs), max(ys)


def _content_px_bbox(ax, extra_scatter=()):
    """(x0, y0, x1, y1), display pixels: the true rendered union of every line/patch/text
    currently in `ax` (measured with the real renderer) plus any scatter markers passed as
    `extra_scatter=[(center, size_pt2), ...]` (collections don't self-report their extent --
    see scatter_bbox_px). Shared by save_fit and place_label's obstacle geometry."""
    renderer = _finalize(ax)
    boxes = []
    for artist_list in (ax.lines, ax.patches, ax.texts):
        for a in artist_list:
            bb = a.get_window_extent(renderer)
            if np.isfinite([bb.x0, bb.y0, bb.x1, bb.y1]).all():
                boxes.append((bb.x0, bb.y0, bb.x1, bb.y1))
    for center, size in extra_scatter:
        boxes.append(scatter_bbox_px(ax, [center], size))
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
                      **kwargs):
    """Like place_label, but for a labelled leader: `text` starts near `xytext` and is
    nudged clear of `obstacles` exactly as place_label does, then a thin `color` leader is
    drawn from the settled label to the `xy` target it explains. Use this (not a bare
    place_label + hand-drawn line) whenever the label needs to point at something -- the
    leader is drawn from the settled label's true edge, so it can never end up short of, or
    crossing through, the label the way a hand-picked xytext sometimes did.

    `arrowstyle`, default "-" (a bare leader line): pass e.g. "-|>" for an arrowhead pointing
    at `xy`.
    """
    arrowprops = dict(arrowstyle=arrowstyle, color=color, lw=lw)
    if mutation_scale is not None:
        arrowprops["mutation_scale"] = mutation_scale
    t = ax.annotate(text, xy=xy, xytext=xytext, color=color, fontsize=fontsize, ha=ha, va=va,
                     zorder=zorder, arrowprops=arrowprops, **kwargs)
    return _settle_text(ax, t, obstacles, color=color, clearance_pt=clearance_pt,
                         push_pt=push_pt, max_iter=max_iter, name=name or text, text=text)


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
def draw_annotation_stroke(ax, pts, *, color=MUTED, lw=None, dashed=False, zorder=5,
                            node_obstacles=(), edge_obstacles=(), rim_clearance_pt=2.0,
                            name="stroke"):
    """Draw `pts` (a data-coord polyline -- 2 points for a straight leader, or the sampled
    output of something like _bracket_points for an arc) as an annotation stroke, then
    verify by construction that it reads as one:

    - `lw` defaults to 40% of EDGE_W and is asserted to never exceed that -- an annotation
      stroke must never be drawn at (or near) edge weight. Pass `dashed=True` for a dashed
      token instead of/in addition to the thinner weight.
    - every sampled point on the stroke is asserted to clear every disc in `node_obstacles`
      (circle_obstacle(...)) by at least `rim_clearance_pt` points beyond its TRUE rendered
      rim -- a pairing arc must float clear of every node, including the ones its own edges
      connect to, never landing on or inside a neighbouring disc.
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
            f"draw_annotation_stroke: {name!r} comes within {mind - r_px:.1f}px of a node "
            f"disc's rim (needs >= {clear_px:.1f}px clearance) -- it terminates on or inside "
            f"a disc it was not meant to touch."
        )

    for i in range(len(px) - 1):
        a, b = px[i], px[i + 1]
        for eobs in edge_obstacles:
            epts = np.array([ax.transData.transform(p) for p in eobs["pts"]])
            for j in range(len(epts) - 1):
                d = _seg_seg_dist(a, b, epts[j], epts[j + 1])
                assert d > 0.5, (
                    f"draw_annotation_stroke: {name!r} crosses a live edge it was not meant "
                    f"to touch -- reroute it or exclude that edge if the crossing is intended."
                )
    return pts


def save(fig, name, dpi=200):
    path = OUT / name
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white", pad_inches=0.15)
    plt.close(fig)
    print("wrote", path.name)


def save_fit(fig, ax, name, extra_scatter=(), pad_frac=0.08, pad_min_in=0.04, out_dpi=None):
    """Save `fig`, cropped EXACTLY to the true rendered extent of everything drawn in `ax`
    (measured with the real renderer, via _content_px_bbox) plus any
    `extra_scatter=[(center, size_pt2), ...]` markers, with a small margin. The crop is
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
    """
    measure_dpi = fig.dpi
    x0, y0, x1, y1 = _content_px_bbox(ax, extra_scatter=extra_scatter)
    padx = max((x1 - x0) * pad_frac, pad_min_in * measure_dpi)
    pady = max((y1 - y0) * pad_frac, pad_min_in * measure_dpi)
    bbox_in = mtransforms.Bbox([[(x0 - padx) / measure_dpi, (y0 - pady) / measure_dpi],
                                 [(x1 + padx) / measure_dpi, (y1 + pady) / measure_dpi]])
    path = OUT / name
    fig.savefig(path, dpi=(out_dpi or measure_dpi), bbox_inches=bbox_in, facecolor="white")
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
    path = OUT / name
    fig.savefig(path, dpi=dpi, facecolor="white")
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
NODE_SIZE_5 = 2200


def draw_graph5(ax, edge_color=MUTED, highlight_edges=(), highlight_color=ACCENT2,
                 node_colors=None, highlight_nodes=(), size=NODE_SIZE_5, label_fs=LABEL_FS):
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
    xs = [pos[n][0] for n in nodes]
    ys = [pos[n][1] for n in nodes]
    colors = [(node_colors or {}).get(n, ACCENT2 if n in highlight_nodes else INK) for n in nodes]
    ax.scatter(xs, ys, s=size, c=colors, zorder=3, linewidths=0)
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
NODE_SIZE_K = 2400


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


def draw_knodes(ax, colors=None, labels_inside=None, size=NODE_SIZE_K):
    order = ["N", "S", "A", "B"]
    xs = [KPOS[n][0] for n in order]
    ys = [KPOS[n][1] for n in order]
    cs = [(colors or {}).get(n, INK) for n in order]
    ax.scatter(xs, ys, s=size, c=cs, zorder=3, linewidths=0)
    for n in order:
        x, y = KPOS[n]
        txt = (labels_inside or {}).get(n, n)
        ax.text(x, y, txt, ha="center", va="center", color="white", fontsize=LABEL_FS,
                zorder=4, fontfamily="serif")


def k_limits(ax, pad=0.85, xpad=None):
    # xpad, if given, widens only the x-range -- KPOS is a symmetric square, so a plain
    # equal pad crops to a slightly-portrait aspect once bbox_inches="tight" is applied;
    # a touch more x-room lands it at <=0.95 without touching node/edge geometry.
    xpad = pad if xpad is None else xpad
    ax.set_xlim(-1 - xpad, 1 + xpad)
    ax.set_ylim(-1 - pad, 1 + pad)
    clean(ax)


def k_obstacles(size, node_colors=None, edge_color=MUTED):
    # Every node disc (true rendered radius) and every one of the seven bridge curves --
    # kept or dashed, they're all real ink on the figure -- as obstacles for place_label /
    # place_annotation. Shared by every Konigsberg-family figure that adds a label on top of
    # draw_kedges/draw_knodes, so a label placed near this graph is checked against the SAME
    # geometry regardless of which figure draws it.
    node_colors = node_colors or {}
    r_pt = (size / np.pi) ** 0.5
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


def draw_city_sketch(ax, bridge_color=INK, bridge_width=6.5):
    # R4 fix (Minor, slides 007/008): the sketch had no water at all -- four landmass
    # blobs floating in plain white, connected by bridges, with nothing distinguishing
    # "gap between landmasses" from "edge of the page." Slide 007 asks "river width?" and
    # slide 008's build claims "geography, distance... about to go" over a picture that
    # never showed either. A pale band behind the two long N/S banks and around the A/B
    # islands reads as the Pregel without competing with the bridges or landmass fills.
    ax.add_patch(mpatches.Rectangle((CITY_XLIM[0], -1.45), CITY_XLIM[1] - CITY_XLIM[0], 2.9,
                                     facecolor=CITY_WATER_COLOR, edgecolor="none", zorder=0))
    # Bridges connect landmass CENTRES and sit at zorder=1, under the landmass polygons
    # (zorder=2) -- each line's middle segment is covered by the shapes it starts/ends
    # inside, leaving only the water-crossing stretch visible, same trick as the old boxes.
    for u, v, rad in CITY_BRIDGES:
        ax.add_patch(FancyArrowPatch(CITY_CENTERS[u], CITY_CENTERS[v], connectionstyle=f"arc3,rad={rad}",
                                      arrowstyle="-", color=bridge_color, linewidth=bridge_width,
                                      capstyle="round", zorder=1))
    for n, (x, y) in CITY_CENTERS.items():
        rx, ry, seed = CITY_SHAPE[n]
        pts = _irregular_blob(x, y, rx, ry, seed)
        ax.add_patch(mpatches.Polygon(pts, closed=True, facecolor=PANEL, edgecolor=MUTED,
                                       linewidth=1.8, joinstyle="round", zorder=2))
        ax.text(x, y, n, ha="center", va="center", fontsize=LABEL_FS, color=MUTED, zorder=3)
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
    # Frame 1: identical geometry to konigsberg-sketch.png -- the build has to start
    # from the actual city sketch, not from an already-abstracted node-link diagram.
    fig, ax = plt.subplots(figsize=(6.9, 5.6))
    draw_city_sketch(ax)
    save(fig, "abstraction-1-map.png")


def fig_abstraction_2_nodes():
    # R3 fix (Major 10): NO edges -- the slide's own text is "Four landmasses. Four dots."
    # Drawing all seven bridges here (as before) made 009->010 a no-op except edge colour.
    W = 5.4
    fig, ax = plt.subplots(figsize=(W, W))
    draw_knodes(ax, size=node_s(W))
    k_limits(ax, xpad=1.1)
    save(fig, "abstraction-2-nodes.png")


def fig_abstraction_3_graph():
    # Edges introduced here, in the standard graph colour (MUTED) -- this frame is the one
    # that earns the slide title "each bridge becomes an edge".
    W = 5.4
    fig, ax = plt.subplots(figsize=(W, W))
    draw_kedges(ax, color=MUTED, width=EDGE_W)
    draw_knodes(ax, size=node_s(W))
    k_limits(ax, xpad=1.1)
    save(fig, "abstraction-3-graph.png")


def fig_multigraph():
    # Minor fix: nodes were labelled P/Q, but the slide text says "Konigsberg has two
    # bridges between the same pair of landmasses" -- relabel to the deck's own N/A.
    W = 4.6
    # R4 fix (Policy 2): ylim/figsize height cut to match the arcs' actual peak height
    # (+-0.18 data units, at rad=0.30 over a 1.2-unit chord) plus the node radius -- was
    # 26% ink in height, wrapping a flat two-node graph in a figure sized for something
    # much taller.
    #
    # R5 fix (Policy 2): that hand-picked xlim/ylim still only bought 63%x45% ink (measured)
    # -- save_fit (see fig_selfloop) crops to the real rendered extent instead of a guess.
    fig, ax = plt.subplots(figsize=(W, 1.4))
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-0.34, 0.34)
    clean(ax)
    P, Q = (-0.6, 0.0), (0.6, 0.0)
    for rad in (0.30, -0.30):
        ax.add_patch(FancyArrowPatch(P, Q, connectionstyle=f"arc3,rad={rad}", arrowstyle="-",
                                      color=MUTED, linewidth=EDGE_W, zorder=1))
    ax.scatter([P[0], Q[0]], [P[1], Q[1]], s=node_s(W), c=INK, zorder=3, linewidths=0)
    for (x, y), t in zip([P, Q], ["N", "A"]):
        ax.text(x, y, t, ha="center", va="center", color="white", fontsize=LABEL_FS, zorder=4)
    # "two bridges, two edges" removed -- it is the figcaption verbatim (duplicated-caption fix).
    save_fit(fig, ax, "multigraph.png", extra_scatter=[(P, node_s(W)), (Q, node_s(W))],
             pad_frac=0.10, pad_min_in=0.05)


# R4 fix (Policy 2): figsize shrunk (5.6 -> 3.0 square) so the loop+node fill a much
# bigger share of the saved canvas -- see fig_edge_single_node for why bbox_inches="tight"
# doesn't do this on its own (Axes.get_tightbbox() still reports close to the full
# declared xlim/ylim). Was 23% x 40% ink.
SELFLOOP_W = 3.0


def _draw_selfloop(ax, r, number_badges=False, badge_fs=11.5):
    # r: the node's TRUE radius in DATA units at ax's CURRENT transform (see
    # node_radius_data) -- not a hand-measured guess. R5 fix (Blocker 2/3): the previous
    # version hard-coded r=0.135 "measured from a render", which had gone stale against the
    # actual node_s()-derived marker size -- the true radius at this figsize was ~0.04, a
    # 3x mismatch -- so the loop's legs were rooted 13-19px above the disc they were meant
    # to visibly meet, and the tick marks (also placed at the wrong r) floated with them.
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
        # R6 fix (Blocker 2): badges now centre ON the rim, at the two points the legs
        # actually attach to (previously offset onto the (deleted) tick marks, 100px from
        # the real attachment point) -- same small ring-plus-digit token as before, just
        # anchored where the answer is actually pointing.
        for i, (x, y) in enumerate((leave, ret), start=1):
            ax.add_patch(mpatches.Circle((x, y), r * 0.42, facecolor="white", edgecolor=MUTED,
                                          linewidth=1.4, zorder=6))
            ax.text(x, y, str(i), ha="center", va="center", color=MUTED,
                    fontsize=badge_fs, zorder=7)
    ax.scatter([cx], [cy], s=node_s(SELFLOOP_W), c=INK, zorder=3, linewidths=0)
    ax.text(cx, cy, "X", ha="center", va="center", color="white",
            fontsize=fs(LABEL_FS, SELFLOOP_W), zorder=4)


def _build_selfloop_fig(name, number_badges, show_k=False):
    # R5 fix (Blocker 2/3, Policy 2): draw against ANY reasonable, generous xlim/ylim (its
    # exact value no longer matters -- see save_fit) so node_radius_data resolves a real
    # r, build the geometry off that r, then crop directly to the true rendered pixel
    # extent via save_fit. (A first attempt tightened xlim/ylim to content and re-measured
    # r each pass -- since a scatter marker's DATA-unit radius depends on the current
    # xlim/ylim, that feedback loop had no stable fixed point and spiralled to zero.)
    W = SELFLOOP_W
    fig, ax = plt.subplots(figsize=(W, W))
    ax.set_xlim(-1.0, 1.0)
    ax.set_ylim(-1.0, 1.0)
    clean(ax)
    rx, ry = node_radius_data(ax, node_s(W))
    r = (rx + ry) / 2
    _draw_selfloop(ax, r, number_badges=number_badges)
    if show_k:
        ax.text(0, -1.55 * r, "k = 2", ha="center", va="top", color=MUTED, fontsize=13, zorder=6)
    # out_dpi bumped well above the file default: this crop is physically small (well under
    # 1in across) and the deck displays it at the same ~520px column width as every other
    # figure regardless of source size, so a low native pixel count here would upscale and
    # go soft on-slide in a way none of the wider figures do.
    save_fit(fig, ax, name, extra_scatter=[((0, 0), node_s(W))], pad_frac=0.10, pad_min_in=0.05,
             out_dpi=1200)


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
    # Plain scatter + straight lines only (no data-unit patches) -- safe to let width and
    # height scale independently so the crop hits a landscape aspect without adding padding.
    W = 4.8
    fig, ax = plt.subplots(figsize=(W, 4.2))
    pos = _star_positions(4)
    for i in range(1, 5):
        ax.plot([pos[0][0], pos[i][0]], [pos[0][1], pos[i][1]], color=MUTED, linewidth=EDGE_W, zorder=1)
    leaf_xy = [pos[i] for i in range(1, 5)]
    s = node_s(W)
    ax.scatter([p[0] for p in leaf_xy], [p[1] for p in leaf_xy], s=s, c=INK, zorder=3, linewidths=0)
    ax.scatter([pos[0][0]], [pos[0][1]], s=s, c=INK, zorder=3, linewidths=0)
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
    ax.annotate("k = 4", xy=(0, -0.16), xytext=(0.85, -1.25), fontsize=ANNOT_FS, color=MUTED,
                ha="center", va="center", arrowprops=dict(arrowstyle="-", color=MUTED, lw=1.2))
    ax.set_xlim(-1.35, 1.35)
    ax.set_ylim(-1.72, 1.3)
    clean(ax, equal=False)
    save(fig, "degree-definition.png")


def _bracket(ax, center, p1, p2, color=MUTED, gap_deg=16, lw=None, zorder=5, n=40):
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
    lw = EDGE_W if lw is None else lw
    pts = _bracket_points(center, p1, p2, gap_deg=gap_deg, n=n)
    ax.plot(pts[:, 0], pts[:, 1], color=color, linewidth=lw, zorder=zorder, solid_capstyle="round")


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


def fig_parity_even():
    W = 4.8
    fig, ax = plt.subplots(figsize=(W, 4.4))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.28, 1.28)
    clean(ax, equal=False)
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
    # from the graph. Distinctly lighter (about half the weight) settles it as annotation,
    # not structure -- same "half-weight, not same-weight" move as the self-loop's ticks.
    bracket_lw = EDGE_W * 0.5
    node_r_pt = (node_s(W) / np.pi) ** 0.5
    obstacles = [circle_obstacle(pos[i], node_r_pt, color=INK) for i in pos]
    for i in range(1, 5):
        obstacles.append(line_obstacle([pos[0], pos[i]], EDGE_W, color=MUTED))

    top_pts = _bracket_points(pos[0], near[1], near[2])
    _bracket(ax, pos[0], near[1], near[2], lw=bracket_lw)
    bot_pts = _bracket_points(pos[0], near[3], near[4])
    _bracket(ax, pos[0], near[3], near[4], lw=bracket_lw)
    # R5 fix (Major 12): each "in-out" now anchors at ITS OWN bracket's peak (with the arc
    # itself as an obstacle, plus every node/edge) instead of sitting ~95px away at the
    # frame's top/bottom edge with a node in between -- bring the label to the mark it names.
    top_peak = tuple(top_pts[len(top_pts) // 2])
    bot_peak = tuple(bot_pts[len(bot_pts) // 2])
    place_label(ax, (top_peak[0], top_peak[1] + 0.22), "in–out",
                obstacles=obstacles + [line_obstacle(top_pts, bracket_lw, color=MUTED)],
                color=MUTED, fontsize=ANNOT_FS, ha="center", va="bottom", clearance_pt=3.0,
                zorder=6, name="parity-even:in-out-top")
    place_label(ax, (bot_peak[0], bot_peak[1] - 0.22), "in–out",
                obstacles=obstacles + [line_obstacle(bot_pts, bracket_lw, color=MUTED)],
                color=MUTED, fontsize=ANNOT_FS, ha="center", va="top", clearance_pt=3.0,
                zorder=6, name="parity-even:in-out-bot")
    xs = [pos[0][0]] + [pos[i][0] for i in range(1, 5)]
    ys = [pos[0][1]] + [pos[i][1] for i in range(1, 5)]
    ax.scatter(xs, ys, s=node_s(W), c=INK, zorder=3, linewidths=0)
    # title removed -- duplicated the figcaption verbatim
    save(fig, "parity-even.png")


def fig_parity_odd():
    W = 4.8
    fig, ax = plt.subplots(figsize=(W, 4.4))
    # leaves at 60 / 180 / 300 deg so none sits under the bracket label at the top
    pos = _star_positions(3, start=60)
    # 1,2 = bracketed pair (upper-right / left); 3 = leftover (lower-right). MUTED, not
    # INK -- deck-wide structural edge colour (see fig_parity_even).
    ax.plot([pos[0][0], pos[1][0]], [pos[0][1], pos[1][1]], color=MUTED, linewidth=EDGE_W, zorder=1)
    ax.plot([pos[0][0], pos[2][0]], [pos[0][1], pos[2][1]], color=MUTED, linewidth=EDGE_W, zorder=1)
    # only the leftover *edge* is accent2 -- the node at its far end stays INK so students
    # don't read the node itself as "the leftover thing" (F1 fix).
    ax.plot([pos[0][0], pos[3][0]], [pos[0][1], pos[3][1]], color=ACCENT2, linewidth=4.5, zorder=1)
    near = {i: (pos[0][0] + 0.55 * (pos[i][0] - pos[0][0]), pos[0][1] + 0.55 * (pos[i][1] - pos[0][1]))
            for i in range(1, 4)}
    _bracket(ax, pos[0], near[1], near[2])
    # label sits on the bisector of the bracketed pair, clear of every node
    bisector = np.deg2rad((60 + 180) / 2)
    lx, ly = 1.05 * np.cos(bisector), 1.05 * np.sin(bisector)
    ax.text(lx, ly, "in–out", ha="center", va="center", color=MUTED, fontsize=ANNOT_FS, zorder=6)
    xs = [pos[0][0], pos[1][0], pos[2][0], pos[3][0]]
    ys = [pos[0][1], pos[1][1], pos[2][1], pos[3][1]]
    ax.scatter(xs, ys, s=node_s(W), c=INK, zorder=3, linewidths=0)
    # R3 fix (Blocker 2): anchored just past leaf 3 (not at the edge midpoint) with
    # ha="left", va="top" so the text grows away from both the centre disc and the
    # accent-2 stroke instead of centering back over them; annotation gray, not
    # accent-2-on-accent-2 (the exact defect already fixed for the Euler examples).
    # Minor fix: 0.16/0.14 left the "l" grazing the disc; a bit more clearance settles it.
    lox, loy = pos[3][0] + 0.22, pos[3][1] - 0.19
    ax.text(lox, loy, "left over", ha="left", va="top", color=MUTED, fontsize=ANNOT_FS, zorder=6)
    ax.set_xlim(-1.6, 1.95)
    ax.set_ylim(-1.45, 1.25)
    clean(ax, equal=False)
    save(fig, "parity-odd.png")


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
    W = 5.6
    fig, ax = plt.subplots(figsize=(W, 3.6))
    ax.set_xlim(-0.55, 4.8)
    ax.set_ylim(-1.15, 1.35)
    clean(ax)
    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=MUTED,
                 linewidth=EDGE_W, zorder=1, solid_capstyle="round")

    # R6 fix (Blocker 3, root cause): this is a 6-node chain drawn at the SAME node_s(W)
    # reference every other (compact, 3-5 node) figure in the deck uses. At full size the
    # marker's fixed in-inches radius covered ~48% of the ~1.01-data-unit spacing between
    # adjacent nodes -- discs nearly touching, only a ~0.037-data-unit (~6px) sliver of each
    # edge exposed outside both rims. Every "even" pairing arc's endpoint (62% of the way
    # along its edge) landed 0.10+ data units INSIDE the far node's own disc no matter how
    # thin the arc was drawn or how far its tip was pushed -- confirmed directly (measured
    # every arc's minimum distance to every node at the old size: -0.044 data units of
    # penetration into the worst-case neighbour, i.e. inside its rim, not just close to it).
    # There was no room for the fix the review asked for ("float clear of every disc") until
    # the discs themselves shrink. NODE_SCALE (all six nodes, uniformly -- the "same size
    # unless the slide explains an encoding" rule stays intact) restores a ~29% exposed gap,
    # matching parity-even's own ~27% (same measurement, see fig_parity_even's node radius),
    # verified below by draw_annotation_stroke's own clearance assertions rather than eyeballed.
    NODE_SCALE = 0.55
    s = node_s(W) * NODE_SCALE
    colors = {n: (ACCENT2 if n in ("S", "E") else INK) for n in pos}
    xs = [pos[n][0] for n in pos]
    ys = [pos[n][1] for n in pos]
    ax.scatter(xs, ys, s=s, c=[colors[n] for n in pos], zorder=3, linewidths=0)

    node_r_pt = (s / np.pi) ** 0.5
    obstacles = [circle_obstacle(pos[n], node_r_pt, color=colors[n]) for n in pos]
    for u, v in edges:
        obstacles.append(line_obstacle([pos[u], pos[v]], EDGE_W, color=MUTED))

    # R5 fix (Major 10): "start"/"end" were clipped by their own accent-2 discs -- a fixed
    # 0.34 offset stopped clearing once the node's true rendered radius (see node_r_pt) grew
    # past it. Routed through place_label so it can't happen again.
    for n, txt in (("S", "start"), ("E", "end")):
        x, y = pos[n]
        dy, va = (-0.34, "top") if n == "S" else (0.34, "bottom")
        label_t = place_label(ax, (x, y + dy), txt, obstacles=obstacles, color=ACCENT2,
                               fontsize=ANNOT_FS - 2, ha="center", va=va, clearance_pt=3.0,
                               zorder=5, name=f"parity-bound:{txt}")
        # "odd" stacks under/over "start"/"end" -- once THOSE are pushed clear of the disc
        # (above), a fixed offset from the node can no longer be trusted to also clear
        # them; checked against the settled label itself via text_obstacle.
        dy2 = dy - 0.30 if n == "S" else dy + 0.30
        place_label(ax, (x, y + dy2), "odd", obstacles=obstacles + [text_obstacle(label_t, color=ACCENT2)],
                    color=ACCENT2, fontsize=ANNOT_FS - 5, ha="center", va=va, clearance_pt=3.0,
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
        ly = hy - 0.40 if is_peak else hy + 0.40
        va = "top" if is_peak else "bottom"
        place_label(ax, (hx, ly), "even", obstacles=obstacles, color=MUTED,
                    fontsize=ANNOT_FS - 4, ha="center", va=va, clearance_pt=3.0, zorder=6,
                    name=f"parity-bound:even-{node}")
    save(fig, "parity-bound.png")


def fig_konigsberg_blank():
    W = 5.2
    fig, ax = plt.subplots(figsize=(W, W))
    draw_kedges(ax)
    draw_knodes(ax, size=node_s(W))
    k_limits(ax, xpad=1.1)
    save(fig, "konigsberg-blank.png")


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
    W = 5.2
    fig, ax = plt.subplots(figsize=(W, 5.6))
    # xlim/ylim/aspect finalized BEFORE any place_label call, since label placement measures
    # the real (post-aspect) data<->pixel transform.
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-1.95, 1.85)
    clean(ax)
    draw_kedges(ax)
    # R3 fix (Major 12/13): keep the N/A/B/S letters INSIDE each node (every other
    # Konigsberg figure -- 008-011, 021 -- uses those letters, and slide 021 has students
    # count degrees on the letter-labelled blank; swapping letters for bare digit values
    # here broke that cross-check). Degrees go just OUTSIDE each node instead, in accent-2
    # to match the node fill. The old bottom "all four odd" annotation is dropped -- it
    # repeated the figcaption, which repeats the bullet list (duplicate-caption fix).
    node_colors = {n: ACCENT2 for n in "NSAB"}
    draw_knodes(ax, colors=node_colors, size=node_s(W))
    # R5 fix (Major 9): these degree numerals are ACCENT2 sitting right outside an ACCENT2
    # disc -- exactly the "recurring failure" pattern the review flagged five times. Routed
    # through place_label: it starts at the same 0.34-out offset as before, but is now
    # measured against the disc's TRUE rendered radius and nudged/raises rather than
    # trusting the hand-picked 0.34 to still clear it.
    obstacles = k_obstacles(node_s(W), node_colors=node_colors)
    for n, d in labels.items():
        ox, oy = K_OUTWARD[n]
        ha, va = K_OUTWARD_ALIGN[n]
        place_label(ax, (KPOS[n][0] + 0.34 * ox, KPOS[n][1] + 0.34 * oy), d, obstacles=obstacles,
                    color=ACCENT2, fontsize=ANNOT_FS, ha=ha, va=va, fontweight="bold", zorder=5,
                    clearance_pt=3.0, name=f"konigsberg-degrees:{n}")
    save(fig, "konigsberg-degrees.png")


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
    W = 5.2
    fig, ax = plt.subplots(figsize=(W, W))
    ax.set_xlim(-2.15, 2.15)
    ax.set_ylim(-1.85, 1.85)
    clean(ax)
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
    draw_knodes(ax, colors=node_colors, size=node_s(W))
    obstacles = k_obstacles(node_s(W), node_colors=node_colors)
    for n, d in labels.items():
        ox, oy = K_OUTWARD[n]
        ha, va = K_OUTWARD_ALIGN[n]
        color = ACCENT2 if n in odd else MUTED
        place_label(ax, (KPOS[n][0] + 0.34 * ox, KPOS[n][1] + 0.34 * oy), d, obstacles=obstacles,
                    color=color, fontsize=ANNOT_FS, ha=ha, va=va, fontweight="bold", zorder=5,
                    clearance_pt=3.0, name=f"konigsberg-bombed:degree-{n}")
    # R5 fix (Blocker 1): "destroyed" now gets ONE leader PER removed bridge (there are two),
    # each anchored on that bridge's own dashed curve at its peak -- previously a single
    # leader pointed at a spot that, because of the sign bug above, sat on the solid A-N
    # curve instead. Both labels sit in the open exterior margin so the leader approaches
    # each dash head-on rather than running near-parallel to any live edge.
    na2_xy = tuple(_arc3_points(KPOS["N"], KPOS["A"], -0.30, n=101)[50])
    sa2_xy = tuple(_arc3_points(KPOS["S"], KPOS["A"], -0.30, n=101)[50])
    place_annotation(ax, na2_xy, "destroyed", xytext=(-1.65, 1.05), obstacles=obstacles,
                      color=MUTED, fontsize=ANNOT_FS, ha="center", va="center",
                      clearance_pt=4.0, name="konigsberg-bombed:destroyed-NA2")
    place_annotation(ax, sa2_xy, "destroyed", xytext=(-1.65, -1.05), obstacles=obstacles,
                      color=MUTED, fontsize=ANNOT_FS, ha="center", va="center",
                      clearance_pt=4.0, name="konigsberg-bombed:destroyed-SA2")
    # "two odd -> now possible" removed -- it is the figcaption verbatim.
    save(fig, "konigsberg-bombed.png")


def _trace_graph(pos, edges, trail, odd_labels=None, label_offsets=None, hub_label=None, width_in=5.2):
    # Label color is annotation gray, not ACCENT2 -- the traced route and the node fills
    # are already ACCENT2, so ACCENT2 text sitting on an ACCENT2 edge was unreadable
    # (F3 fix). Offsets are per-node so a label never sits on top of an incident edge.
    #
    # R4 fix (Policy 1): edges back to the deck's standard structural colour (MUTED) --
    # ACCENT2 previously meant "every edge", which is no signal at all. In this figure
    # family accent-2 now means exactly one thing: an ODD-degree node (the two ends of a
    # path). A node passed as `hub_label` is EVEN (Euler-circuit's start=end node has
    # degree 4) and must not be coloured accent-2 for that -- see fig_euler_circuit_example.
    W = width_in
    fig, ax = plt.subplots(figsize=(W, 4.6))
    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=MUTED,
                 linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    nodes = list(pos.keys())
    colors = [ACCENT2 if n in (odd_labels or {}) else INK for n in nodes]
    xs = [pos[n][0] for n in nodes]
    ys = [pos[n][1] for n in nodes]
    ax.scatter(xs, ys, s=node_s(W), c=colors, zorder=3, linewidths=0)
    if odd_labels:
        for n, txt in odd_labels.items():
            x, y = pos[n]
            dx, dy = (label_offsets or {}).get(n, (0, -0.32))
            ha = "center" if dx == 0 else ("left" if dx > 0 else "right")
            va = "center" if dy == 0 else ("bottom" if dy > 0 else "top")
            ax.text(x + dx, y + dy, txt, ha=ha, va=va, color=MUTED, fontsize=ANNOT_FS, zorder=4)
    if hub_label:
        # A thin ring, not an accent-2 fill -- this node is EVEN, so it must not carry the
        # "odd" colour. The ring marks "this is the node that's both start and end"; the
        # text sits well clear of the disc and of the edges the ring itself sits inside of.
        x, y = pos[hub_label]
        # Radius matches the ring convention used elsewhere at this same node/data scale
        # (circuit.png's "revisited" ring): a touch larger than the node disc so it reads
        # as a ring around the node, not a second, smaller disc on top of it.
        ax.add_patch(mpatches.Circle((x, y), 0.2, facecolor="none", edgecolor=ACCENT2,
                                      linewidth=3, zorder=5))
        dx, dy = (label_offsets or {}).get(hub_label, (0, -0.55))
        ax.text(x + dx, y + dy, "start = end", ha="center", va="top", color=MUTED,
                fontsize=ANNOT_FS, zorder=4)
    clean(ax)
    return fig, ax


def fig_euler_path_example():
    pos = {"BL": (0, 0), "BR": (1, 0), "TL": (0, 1), "TR": (1, 1), "T": (0.5, 1.7)}
    edges = [("BL", "BR"), ("BR", "TR"), ("TR", "T"), ("T", "TL"), ("TL", "BL"), ("TL", "TR")]
    # TL's incident edges run straight down and straight right from it, so a label
    # placed *below* TL sits on the TL-BL edge; offset sideways instead. Same for TR.
    fig, ax = _trace_graph(pos, edges, None, odd_labels={"TL": "start", "TR": "end"},
                            label_offsets={"TL": (-0.34, 0), "TR": (0.34, 0)})
    ax.set_xlim(-0.85, 1.85)
    ax.set_ylim(-0.25, 1.9)
    save(fig, "euler-path-example.png")


def fig_euler_circuit_example():
    # R4 fix (Policy 1): C has degree 4 -- EVEN -- so it must not be accent-2 (that colour
    # is reserved for odd nodes elsewhere in this figure family); see _trace_graph. Also
    # (Minor): "start = end" used to sit pressed into the V of the two lower edges with a
    # few px clearance -- label_offsets pushes it further below the ring, and the axis
    # extends to keep it inside the frame.
    pos = {"C": (0, 0), "L1": (-1, 0.65), "L2": (-1, -0.65), "R1": (1, 0.65), "R2": (1, -0.65)}
    edges = [("C", "L1"), ("L1", "L2"), ("L2", "C"), ("C", "R1"), ("R1", "R2"), ("R2", "C")]
    fig, ax = _trace_graph(pos, edges, None, hub_label="C", label_offsets={"C": (0, -0.62)})
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.35, 1.15)
    save(fig, "euler-circuit-example.png")


# ===========================================================================
# Part 4 -- vocabulary
# ===========================================================================
CAMPUS_POS = {"Dorm": (0, 1), "Cafe": (1, 1), "Lib": (1, 0), "Gym": (0, 0)}
CAMPUS_EDGES = [("Dorm", "Cafe"), ("Cafe", "Lib"), ("Lib", "Gym"), ("Gym", "Dorm"), ("Cafe", "Gym")]
NODE_SIZE_C = node_s(4.7)  # matches CAMPUS_FIGSIZE width, defined below


def draw_campus_base(ax, skip_edges=()):
    skip = {frozenset(e) for e in skip_edges}
    for u, v in CAMPUS_EDGES:
        if frozenset((u, v)) in skip:
            continue
        ax.plot([CAMPUS_POS[u][0], CAMPUS_POS[v][0]], [CAMPUS_POS[u][1], CAMPUS_POS[v][1]],
                 color=MUTED, linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    nodes = list(CAMPUS_POS.keys())
    xs = [CAMPUS_POS[n][0] for n in nodes]
    ys = [CAMPUS_POS[n][1] for n in nodes]
    ax.scatter(xs, ys, s=NODE_SIZE_C, c=INK, zorder=3, linewidths=0)
    for n in nodes:
        x, y = CAMPUS_POS[n]
        # 4-letter names (Dorm, Cafe) run edge-to-edge inside the disc at the full label
        # size; give them interior margin by dropping a couple of points (F4/F3 fix).
        label_fs = LABEL_FS if len(n) <= 3 else LABEL_FS - 3
        ax.text(x, y, n, ha="center", va="center", color="white", fontsize=label_fs, zorder=4,
                fontfamily="serif")


# One shared figsize + axis extent for all four campus frames -- previously base used a
# different figsize than walk/trail/path, so aspect='equal' fit each to a different scale
# and the graph visibly jumped in size when the build returned to it (F4/F3 fix).
CAMPUS_FIGSIZE = (4.7, 4.2)


def campus_axes(ax):
    ax.set_xlim(-0.4, 1.5)
    ax.set_ylim(-0.4, 1.3)
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
    # R4 fix (Policy 1): the walk doubles back over Cafe-Gym (there and back), so this
    # frame drew that pair as THREE parallel strokes -- the base graph's gray straight
    # edge plus the two accent-2 curves -- reading as three edges where the graph has one.
    # The two accent-2 curves already show "this edge, twice"; the underlying gray edge
    # only needs to be hidden on this one frame (campus-trail/path/base still draw it).
    fig, ax = plt.subplots(figsize=CAMPUS_FIGSIZE)
    draw_campus_base(ax, skip_edges=[("Cafe", "Gym")])
    cx, cy = CAMPUS_POS["Cafe"]
    gx, gy = CAMPUS_POS["Gym"]
    dx, dy = CAMPUS_POS["Dorm"]
    lx, ly = CAMPUS_POS["Lib"]
    route = [(dx, dy, cx, cy), (cx, cy, gx, gy), (gx, gy, cx, cy), (cx, cy, lx, ly)]
    for i, (x0, y0, x1, y1) in enumerate(route):
        rad = 0.18 if i in (1, 2) else 0.0
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), connectionstyle=f"arc3,rad={rad}",
                                      arrowstyle="-|>", mutation_scale=22, shrinkA=24, shrinkB=24,
                                      color=ACCENT2, linewidth=4.2, zorder=2))
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
    campus_axes(ax)  # finalize xlim/ylim/aspect before place_annotation measures anything
    node_r_pt = (NODE_SIZE_C / np.pi) ** 0.5
    obstacles = [circle_obstacle(CAMPUS_POS[n], node_r_pt, color=INK) for n in CAMPUS_POS]
    for u, v in CAMPUS_EDGES:
        if frozenset((u, v)) == frozenset(("Cafe", "Gym")):
            continue  # hidden on this frame -- see skip_edges above
        obstacles.append(line_obstacle([CAMPUS_POS[u], CAMPUS_POS[v]], EDGE_W, color=MUTED))
    for i, (x0, y0, x1, y1) in enumerate(route):
        rad = 0.18 if i in (1, 2) else 0.0
        pts = _arc3_points((x0, y0), (x1, y1), rad, n=30) if rad else [(x0, y0), (x1, y1)]
        obstacles.append(line_obstacle(pts, 4.2, color=ACCENT2))
    place_annotation(ax, ((cx + gx) / 2 + 0.08, (cy + gy) / 2 - 0.02), "same edge,\ntwice",
                      xytext=(1.12, 0.45), obstacles=obstacles, color=MUTED,
                      fontsize=ANNOT_FS - 2, ha="center", va="center", clearance_pt=4.0,
                      zorder=5, name="campus-walk:same-edge-twice")
    # title removed -- duplicated the figcaption verbatim
    save_fixed(fig, "campus-walk.png")


def fig_campus_trail():
    fig, ax = plt.subplots(figsize=CAMPUS_FIGSIZE)
    draw_campus_base(ax)
    seq = ["Lib", "Gym", "Dorm", "Cafe", "Gym"]
    for a, b in zip(seq, seq[1:]):
        x0, y0 = CAMPUS_POS[a]
        x1, y1 = CAMPUS_POS[b]
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=22,
                                      shrinkA=24, shrinkB=24, color=ACCENT2, linewidth=4.2, zorder=2))
    gx, gy = CAMPUS_POS["Gym"]
    ax.add_patch(mpatches.Circle((gx, gy), 0.19, facecolor="none", edgecolor=ACCENT2, linewidth=3, zorder=5))
    # R3 fix (Major 25): the ring around Gym had no label -- a student saw one ringed node
    # and one word ("start", at Lib) and couldn't tell which one the ring meant. Gym's
    # incident edges run up (Dorm), upper-right (Cafe) and right (Lib) -- all at y >= 0 --
    # so the label sits just below the Gym-Lib edge, inside the shared campus_axes bbox.
    ax.text(gx + 0.42, gy - 0.17, "visited twice", ha="center", va="top", color=ACCENT2,
            fontsize=ANNOT_FS - 2, zorder=5)
    # "start" marks where the trail begins -- the Euler examples mark start/end, this
    # frame previously did not (F4 fix). Lib's only edges run left (to Gym) and up (to
    # Cafe), so a label to its right is clear of both.
    lx, ly = CAMPUS_POS["Lib"]
    ax.text(lx + 0.3, ly, "start", ha="left", va="center", color=ACCENT2, fontsize=ANNOT_FS, zorder=5)
    # title removed -- duplicated the figcaption verbatim
    campus_axes(ax)
    save_fixed(fig, "campus-trail.png")


def fig_campus_path():
    fig, ax = plt.subplots(figsize=CAMPUS_FIGSIZE)
    draw_campus_base(ax)
    seq = ["Lib", "Cafe", "Dorm", "Gym"]
    for a, b in zip(seq, seq[1:]):
        x0, y0 = CAMPUS_POS[a]
        x1, y1 = CAMPUS_POS[b]
        ax.add_patch(FancyArrowPatch((x0, y0), (x1, y1), arrowstyle="-|>", mutation_scale=22,
                                      shrinkA=24, shrinkB=24, color=ACCENT2, linewidth=4.2, zorder=2))
    # title removed -- duplicated the figcaption verbatim
    campus_axes(ax)
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


def _circuit_cycle_base(ax, width_in):
    pos = {"C": (0, 0), "L1": (-1, 0.65), "L2": (-1, -0.65), "R1": (1, 0.65), "R2": (1, -0.65)}
    edges = [("C", "L1"), ("L1", "L2"), ("L2", "C"), ("C", "R1"), ("R1", "R2"), ("R2", "C")]
    for u, v in edges:
        ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=MUTED,
                 linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    xs = [pos[n][0] for n in pos]
    ys = [pos[n][1] for n in pos]
    ax.scatter(xs, ys, s=node_s(width_in), c=INK, zorder=3, linewidths=0)
    ax.set_xlim(-1.55, 1.55)
    ax.set_ylim(-1.15, 1.15)
    clean(ax)
    return pos


# R3 fix (Blocker 3): circuit-vs-cycle.png was a two-panel figure with baked-in titles
# ("circuit (closed trail)" / "cycle (closed path)") that both the "Circuit" and "Cycle"
# slides embedded whole -- advancing between them changed nothing on screen (md5-identical
# renders) and the Circuit slide displayed the fully-labelled Cycle definition beside it.
# circuit.png / cycle.png are single-panel, with no baked-in title -- the figcaption now
# carries what each one is.
def fig_circuit():
    W = 4.8
    fig, ax = plt.subplots(figsize=(W, 4.6))
    pos = _circuit_cycle_base(ax, W)
    route = ["L1", "L2", "C", "R1", "R2", "C", "L1"]
    for a, b in zip(route, route[1:]):
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=ACCENT2,
                 linewidth=4.5, zorder=2, solid_capstyle="round")
    ax.add_patch(mpatches.Circle(pos["C"], 0.2, facecolor="none", edgecolor=ACCENT2, linewidth=3, zorder=5))
    # Minor fix: this ring had no label, while campus-trail's identical ring (same meaning
    # -- a node the route revisits) already carries one; C sits at positions 2 and 5 of the
    # 6-step route. Straight down is the one direction clear of all four of C's edges.
    ax.text(pos["C"][0], pos["C"][1] - 0.40, "visited twice", ha="center", va="top",
            color=ACCENT2, fontsize=ANNOT_FS - 2, zorder=5)
    save(fig, "circuit.png")


def fig_cycle():
    W = 4.8
    fig, ax = plt.subplots(figsize=(W, 4.6))
    pos = _circuit_cycle_base(ax, W)
    route = ["L1", "L2", "C", "L1"]
    for a, b in zip(route, route[1:]):
        ax.plot([pos[a][0], pos[b][0]], [pos[a][1], pos[b][1]], color=ACCENT2,
                 linewidth=4.5, zorder=2, solid_capstyle="round")
    save(fig, "cycle.png")


def fig_graph_labeled():
    # GRAPH5_POS spans y:[-0.9,1.0] but only x:[0,1] -- content is inherently portrait.
    # draw_graph5 uses only scatter markers (fixed point-size) and straight lines, so
    # dropping the equal-aspect constraint lets the box hit a landscape ratio without
    # adding dead space: nodes stay perfectly round, only line angles skew slightly.
    W = 5.4
    fig, ax = plt.subplots(figsize=(W, 4.5))
    draw_graph5(ax, label_fs=fs(LABEL_FS, W), size=node_s(W))
    ax.set_xlim(-0.35, 1.35)
    ax.set_ylim(-1.15, 1.2)
    clean(ax, equal=False)
    save(fig, "graph-labeled.png")


def fig_adjacency_matrix():
    # Left panel: the graph itself, with one edge and its two symmetric matrix cells tied
    # together in ACCENT2 -- the slide is titled "Writing a graph as a matrix" and the old
    # figure showed only the matrix (F4 Blocker fix).
    W = 9.2
    fig, axes = plt.subplots(1, 2, figsize=(W, 4.7))
    hi_edge = (1, 3)
    ax = axes[0]
    # node_s() keyed to this panel's own share of W, not the whole 2-panel figure -- GRAPH5
    # nodes sit only ~1 data-unit apart, so scaling by the FULL figure width (as fs() does
    # for the label, fine since text stays small either way) massively over-sized and
    # overlapped them here.
    draw_graph5(ax, highlight_edges=[hi_edge], label_fs=fs(LABEL_FS, W), size=node_s(W / 2))
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-1.4, 1.4)
    clean(ax)

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
    W = 9.4
    fig, axes = plt.subplots(1, 2, figsize=(W, 4.4))
    ax = axes[0]
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-1.4, 1.4)
    clean(ax)
    # node_s() keyed to this panel's own share of W -- see fig_adjacency_matrix.
    draw_graph5(ax, label_fs=fs(LABEL_FS, W), size=node_s(W / 2))
    route_a = [(1, 2), (2, 4)]
    route_b = [(1, 3), (3, 4)]
    for u, v in route_a:
        ax.plot([GRAPH5_POS[u][0], GRAPH5_POS[v][0]], [GRAPH5_POS[u][1], GRAPH5_POS[v][1]],
                 color=ACCENT2, linewidth=EDGE_W + 1.5, zorder=2, solid_capstyle="round")
    for u, v in route_b:
        ax.plot([GRAPH5_POS[u][0], GRAPH5_POS[v][0]], [GRAPH5_POS[u][1], GRAPH5_POS[v][1]],
                 color=ACCENT3, linewidth=EDGE_W + 1.5, zorder=2, solid_capstyle="round")
    # R5 fix (Major 16): neither route colour was ever named in the figure itself (only the
    # figcaption's "2 two-step routes" hinted at them), so a reader had to guess which
    # colour was which path. Captioned directly beside each route, in its own colour.
    node_r_pt = (node_s(W / 2) / np.pi) ** 0.5
    graph_obstacles = [circle_obstacle(GRAPH5_POS[n], node_r_pt, color=INK) for n in GRAPH5_POS]
    for u, v in GRAPH5_EDGES:
        hl = ACCENT2 if (u, v) in route_a or (v, u) in route_a else (
            ACCENT3 if (u, v) in route_b or (v, u) in route_b else MUTED)
        graph_obstacles.append(line_obstacle([GRAPH5_POS[u], GRAPH5_POS[v]], EDGE_W + 1.5, color=hl))
    # Fixed, not fs()-scaled: fs(16, W) with W=9.4 (the FULL two-panel figure width) sizes
    # for a single panel filling 9.4in, but each panel here is under half that -- the
    # literal fs() scale (~29pt) was wide enough that both captions pushed past their own
    # panel's xlim into the MATRIX panel's space next door, where nothing in this panel's
    # obstacle list could see (or avoid) the matrix's own row labels (same failure the deck
    # already documents for fig_connected_vs_not / fig_circuit_vs_cycle's panel_fs, and for
    # fig_memory_payoff's title_fs above). Stacked below node 4 -- shared by both routes,
    # with real open space beneath it -- instead of beside nodes 2/3, which sit close enough
    # to the panel boundary that any real caption width runs into it.
    route_fs = 15
    n4x, n4y = GRAPH5_POS[4]
    label_a = place_label(ax, (n4x, n4y - 0.28), "1→2→4", obstacles=graph_obstacles,
                           color=ACCENT2, fontsize=route_fs, ha="center", va="top", clearance_pt=4.0,
                           zorder=5, name="adjacency-squared:route-a")
    # Pre-offset a second line's worth below route_a's own anchor (not the same point) --
    # place_label nudges away from overlap, but two labels started exactly on top of each
    # other have no "away" that clears both at once within a few points per nudge.
    place_label(ax, (n4x, n4y - 0.28 - 0.22), "1→3→4",
                obstacles=graph_obstacles + [text_obstacle(label_a, color=None)],
                color=ACCENT3, fontsize=route_fs, ha="center", va="top", clearance_pt=4.0,
                zorder=5, name="adjacency-squared:route-b")

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
    W = 10.0
    pos = {0: (-1, 0.5), 1: (-1, -0.5), 2: (-0.15, 0), 3: (0.8, 0), 4: (1.7, 0)}
    all_edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4)]

    def panel(ax, edges, title):
        for u, v in edges:
            ax.plot([pos[u][0], pos[v][0]], [pos[u][1], pos[v][1]], color=MUTED,
                     linewidth=EDGE_W, zorder=1, solid_capstyle="round")
        xs = [pos[n][0] for n in pos]
        ys = [pos[n][1] for n in pos]
        ax.scatter(xs, ys, s=1700, c=INK, zorder=3, linewidths=0)
        # Minor fix (slide 039): fs(TITLE_FS, W) scales by the FULL 10in figure width, but
        # each panel is only half of it -- same over-scale circuit-vs-cycle already avoids
        # with a fixed panel_fs. The literal fs() scale rendered these titles ~50px against
        # 27px body text, inverting the deck's own type hierarchy; fixed instead.
        ax.set_title(title, fontsize=21, color=INK, pad=10)
        ax.set_xlim(-1.5, 2.1)
        ax.set_ylim(-0.9, 0.95)
        clean(ax)

    fig, axes = plt.subplots(1, 2, figsize=(W, 3.6))
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
NODE_SIZE_BAND = 900


def draw_band(ax, node_colors=None, default_color=INK):
    for u, v in BAND_EDGES:
        ax.plot([BAND_POS[u][0], BAND_POS[v][0]], [BAND_POS[u][1], BAND_POS[v][1]],
                 color=MUTED, linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    nodes = list(BAND_POS.keys())
    xs = [BAND_POS[n][0] for n in nodes]
    ys = [BAND_POS[n][1] for n in nodes]
    colors = [(node_colors or {}).get(n, default_color) for n in nodes]
    ax.scatter(xs, ys, s=NODE_SIZE_BAND, c=colors, zorder=3, linewidths=0)


BAND_W = 10.4


def band_axes(ax, with_labels=True):
    ax.set_xlim(-0.4, 7.2)
    ax.set_ylim(-0.85, 1.3)
    clean(ax)
    if with_labels:
        # NOT a literal fs() scale: the three labels sit at fixed x-positions only ~3.2
        # units apart, so the full ~36pt scale (correct for this figure's 10.4in width in
        # principle) makes adjacent labels overlap. A modest, safe bump instead.
        label_fs = 20
        ax.text(1.2, -0.62, "component 1", color=MUTED, fontsize=label_fs, ha="center")
        ax.text(4.4, -0.62, "component 2", color=MUTED, fontsize=label_fs, ha="center")
        ax.text(6.4, -0.62, "component 3", color=MUTED, fontsize=label_fs, ha="center")


def fig_components_band():
    fig, ax = plt.subplots(figsize=(BAND_W, 3.4))
    draw_band(ax)
    band_axes(ax)
    save(fig, "components-band.png")


def fig_components_bare():
    # Same picture, same positions, no "component N" labels: the "run the sweep"
    # exercise asks students how many components there are, so the labelled
    # version would answer its own question before the thinking beat starts.
    fig, ax = plt.subplots(figsize=(BAND_W, 3.4))
    draw_band(ax)
    band_axes(ax, with_labels=False)
    save(fig, "components-bare.png")


def fig_sweep_1():
    fig, ax = plt.subplots(figsize=(BAND_W, 3.4))
    draw_band(ax, node_colors={"L0": ACCENT2})
    band_axes(ax)
    save(fig, "sweep-1.png")


def fig_sweep_2():
    fig, ax = plt.subplots(figsize=(BAND_W, 3.4))
    colors = {n: ACCENT2 for n in LADDER_POS}
    draw_band(ax, node_colors=colors)
    band_axes(ax)
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
    draw_band(ax)

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

    node_r_pt = (NODE_SIZE_BAND / np.pi) ** 0.5
    obstacles = [circle_obstacle(BAND_POS[n], node_r_pt, color=INK) for n in BAND_POS]
    for u, v in BAND_EDGES:
        obstacles.append(line_obstacle([BAND_POS[u], BAND_POS[v]], EDGE_W, color=MUTED))
    for xmin, xmax, ymin, ymax in enclosures:
        x0, x1, y0, y1 = xmin - xpad, xmax + xpad, ymin - ypad, ymax + ypad
        obstacles.append(line_obstacle([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)],
                                        1.6, color=MUTED))

    # R5 fix (Blocker 5): 15pt measured at 11px on-slide, below the 13px page number and far
    # under the 21px body copy -- bumped to a size that actually reads from the back row.
    label_fs = 18
    for i, n in enumerate(ladder_order, start=1):
        x, y = BAND_POS[n]
        above = y > 0.5  # top row (y=0.9) vs bottom row (y=0.0)
        va = "bottom" if above else "top"
        anchor = (x, y + 0.30) if above else (x, y - 0.30)
        place_label(ax, anchor, str(i), obstacles=obstacles, color=MUTED, fontsize=label_fs,
                    ha="center", va=va, clearance_pt=3.0, zorder=4, name=f"sweep3-ladder-{i}")
    for i, n in enumerate(tri_order, start=1):
        x, y = BAND_POS[n]
        above = y > 0.4  # M2 (apex) vs M0/M1 (base)
        va = "bottom" if above else "top"
        anchor = (x, y + 0.30) if above else (x, y - 0.30)
        place_label(ax, anchor, str(i), obstacles=obstacles, color=MUTED, fontsize=label_fs,
                    ha="center", va=va, clearance_pt=3.0, zorder=4, name=f"sweep3-tri-{i}")
    for i, n in enumerate(pair_order, start=1):
        x, y = BAND_POS[n]
        place_label(ax, (x, y + 0.30), str(i), obstacles=obstacles, color=MUTED,
                    fontsize=label_fs, ha="center", va="bottom", clearance_pt=3.0, zorder=4,
                    name=f"sweep3-pair-{i}")

    save(fig, "sweep-3.png")


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

    ax = axes[0]
    ax.scatter(rx, ry, s=4, color="#e6e6e6", zorder=1)
    ax.scatter(bx, by, s=4, color=ACCENT, zorder=2)
    ax.add_patch(mpatches.Rectangle((-frame, -frame), 2 * frame, 2 * frame, fill=False,
                                     edgecolor=RULE, linewidth=1.6, zorder=3))
    ax.set_xlim(-frame * 1.08, frame * 1.08)
    ax.set_ylim(-frame * 1.08, frame * 1.08)
    clean(ax)
    ax.set_title("N = 1,200", fontsize=panel_fs, color=INK, pad=10)
    # Minor fix (slide 043): "1 dot" silently meant 1 node on the left and ~1,700 nodes on
    # the right, never stated; a second line on each panel makes the per-dot count
    # explicit instead of leaving it to be inferred from the two node-count titles.
    #
    # R5 fix (Major 20): this slide displays at w:520 in the deck -- measured against that,
    # even the R4 bump (ANNOT_FS+1 = 18pt fixed, since W/2 here equals FONT_REF_WIDTH
    # exactly) renders at ~12px on-slide, back below the page number. Bumped again to a size
    # that actually clears it at the real display width.
    key_fs = 22
    ax.text(0.5, -0.05, "pale: 200 more nodes\n1 dot = 1 node", ha="center",
            va="top", color=MUTED, fontsize=key_fs, transform=ax.transAxes)

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
    ax.scatter(fx, fy, s=4, color="#e6e6e6", zorder=1)
    ax.scatter(bx, by, s=4, color=ACCENT, zorder=2)
    ax.set_xlim(-frame2 * 1.05, frame2 * 1.05)
    ax.set_ylim(-frame2 * 1.05, frame2 * 1.05)
    clean(ax)
    ax.set_title("N = 10,000,000", fontsize=panel_fs, color=INK, pad=10)
    # Minor fix: the left panel's "pale dots" note explained its gray field; the right
    # panel's much bigger gray field (~10M nodes) had no equivalent, so one gray encoding
    # silently carried two different magnitudes -- and, unlike the left panel, one dot
    # here does NOT mean one node (6,000 dots stand in for ~9,999,000). Spelled out.
    #
    # R5 fix (Major 20): that note explained the PALE dots' scale but never said the BLUE
    # ones keep the left panel's "1 dot = 1 node" rule unchanged (still literally the same
    # 1,000-point bx/by array, just plotted inside a much bigger frame) -- so a reader
    # applying the pale key ("1 dot ~ 1,700 nodes") to the blue speck too would read it as
    # ~1,700 nodes, overstating the actual 1,000 by 70%. States the blue rule explicitly.
    #
    # R6 fix (Blocker 7): "(1 dot = 1 node)" was true of the DATA (bx/by is still the same
    # 1,000-point array) but false of what a student can actually see -- the panel renders
    # that array as ONE 4x5px blue speck, so the printed key told a reader applying it
    # literally to count the giant component as one node. Says what the eye actually sees
    # (a single dot, at this scale) instead of implying a literal one-dot-per-node count --
    # kept short (not the fuller "0.01% of the area" phrasing) so it doesn't grow past the
    # wspace budget and collide with the left panel's key again (see the R4/R5 fixes above).
    per_dot = round((10_000_000 - 1000) / n_field, -2)
    ax.text(0.5, -0.05, f"blue: still 1,000 -- one dot at this scale\n"
            f"pale: ~9,999,000 more, 1 dot ≈ {per_dot:,.0f}",
            ha="center", va="top", color=MUTED, fontsize=key_fs - 4, transform=ax.transAxes)

    # "same 1,000 nodes" removed -- near-duplicate of the figcaption; the per-panel note
    # above now explains the gray dots directly instead.
    save(fig, "giant-scale.png")


DIR_POS = {"A": (0.0, 0.75), "B": (0.87, -0.375), "C": (-0.87, -0.375)}


def _draw_directed(ax, edges, width_in):
    # R3 fix (Major 23): DIR_POS is not quite equilateral (B-C is longer than A-B/C-A), so
    # networkx's node_size-based arrow shrink -- a single heuristic shared across all edges
    # of a call -- landed inconsistently (A->B arrowhead ~10px short of B, C->A flush).
    # FancyArrowPatch's shrinkA/shrinkB (points, applied per edge, same mechanism already
    # used for the campus arrows) equalises the gap regardless of edge length or curvature.
    #
    # R4 fix (Major 18): that "equalises" claim didn't hold for directed-indegree -- the
    # shrink constant (24pt) undershot the marker's true radius (26.46pt, see
    # NODE_RADIUS_PT_REF), so `shrink` was bumped to radius+3pt on the theory that a curved
    # edge's shrink acts along its local tangent and needs a buffer to still land on the
    # disc after that skew.
    #
    # R5 fix (Major 14): that theory was never actually measured against the renderer, and
    # it was backwards. Measured directly (FancyArrowPatch.get_window_extent vs. the target
    # node's true centre, swept over shrink 0-40pt, for every edge in this triangle): the
    # tangent-skew effect is small (the gap still closes at ~2.75px per point of shrink,
    # against a theoretical 1:1 of dpi/72=2.78px/pt) -- the real reason radius+3 undershot is
    # that arrowstyle "-|>"'s own head geometry doesn't reach the connector's raw endpoint
    # even at shrink=0 (an baked-in ~11-25px gap, varying per edge angle). Net effect: the
    # right correction is radius MINUS a few points, not plus. NODE_RADIUS_PT_REF - 4 is the
    # smallest shrink that closed EVERY edge in the calibration sweep (the tightest edge,
    # A-C/B-C, needed radius-3.9pt almost exactly); the slightly-shorter A-B edge overshoots
    # a few px into the disc at this value, which reads as flush, not as a gap.
    s = node_s(width_in)
    shrink = fs(NODE_RADIUS_PT_REF - 4, width_in)
    mscale = fs(30, width_in)
    for u, v in edges:
        ax.add_patch(FancyArrowPatch(DIR_POS[u], DIR_POS[v], connectionstyle="arc3,rad=0.12",
                                      arrowstyle="-|>", mutation_scale=mscale, shrinkA=shrink,
                                      shrinkB=shrink, color=MUTED, linewidth=EDGE_W, zorder=1))
    xs = [DIR_POS[n][0] for n in "ABC"]
    ys = [DIR_POS[n][1] for n in "ABC"]
    ax.scatter(xs, ys, s=s, c=INK, zorder=3, linewidths=0)
    for n in "ABC":
        ax.text(*DIR_POS[n], n, ha="center", va="center", color="white", fontsize=LABEL_FS, zorder=4)
    # no title -- see fig_directed_strong/fig_directed_weak: baked-in titles were stripped
    # deck-wide in an earlier round; the figcaption is the single caption channel.
    #
    # R4 fix (Policy 2): tightened from (-1.35,1.35)/(-1.05,1.15) -- directed-strong/weak
    # now save with save_fixed() (no tight-bbox crop, see fig_directed_strong), so this
    # margin is exactly what ends up as dead canvas. Still clears the widest content
    # (node B/C at x=+-0.87 plus their own radius, ~0.17 data units at this figsize).
    ax.set_xlim(-1.08, 1.08)
    ax.set_ylim(-0.85, 0.95)
    clean(ax)


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
    W = 4.8
    fig, ax = plt.subplots(figsize=(W, 4.5))
    _draw_directed(ax, [("A", "B"), ("A", "C"), ("B", "C")], W)
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
    W = 4.8
    fig, ax = plt.subplots(figsize=(W, 4.5))
    _draw_directed(ax, [("A", "B"), ("B", "C"), ("C", "A")], W)
    save_fixed(fig, "directed-strong.png")


def fig_directed_weak():
    # save_fixed(), not save() -- see fig_directed_strong.
    W = 4.8
    fig, ax = plt.subplots(figsize=(W, 4.5))
    _draw_directed(ax, [("A", "B"), ("B", "C")], W)
    save_fixed(fig, "directed-weak.png")


def fig_directed_indegree():
    # NEW -- slide 061's point is that degree splits into in-degree and out-degree, but
    # directed-arrows.png (reused there before) carries no in/out counts at all.
    edges = [("A", "B"), ("B", "C"), ("C", "A")]
    indeg = {n: sum(1 for _, v in edges if v == n) for n in "ABC"}
    outdeg = {n: sum(1 for u, _ in edges if u == n) for n in "ABC"}
    assert all(indeg[n] == 1 and outdeg[n] == 1 for n in "ABC"), \
        f"3-cycle should be in=out=1 everywhere; got in={indeg} out={outdeg}"
    W = 5.4
    fig, ax = plt.subplots(figsize=(W, 4.7))
    _draw_directed(ax, edges, W)
    # R3 fix (Major 23): node A's disc overlapped the baseline of its own label (raised
    # further here) and the "in 1 / out 1" strings weren't yet clear of the discs.
    offsets = {"A": (0.0, 0.44), "B": (0.55, -0.16), "C": (-0.55, -0.16)}
    ha = {"A": "center", "B": "left", "C": "right"}
    for n in "ABC":
        x, y = DIR_POS[n]
        dx, dy = offsets[n]
        ax.text(x + dx, y + dy, "in 1 / out 1", ha=ha[n], va="center", color=MUTED,
                fontsize=ANNOT_FS, zorder=5)
    ax.set_xlim(-2.05, 2.05)
    ax.set_ylim(-1.15, 1.5)
    save(fig, "directed-indegree.png")


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
    W = 8.4
    node1_edges = [(1, 0), (1, 2), (1, 3)]
    hi = {frozenset(e) for e in node1_edges}
    fig = plt.figure(figsize=(W, 5.0))
    gs = fig.add_gridspec(1, 2, width_ratios=[1.5, 1.0], wspace=0.25)

    ax = fig.add_subplot(gs[0, 0])
    # node_s() keyed to this panel's own share of W (1.5 of the 2.5 gridspec units) --
    # see fig_adjacency_matrix.
    draw_graph5(ax, highlight_edges=node1_edges, highlight_nodes={1}, label_fs=fs(LABEL_FS, W),
                size=node_s(W * 1.5 / 2.5))
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-1.4, 1.4)
    clean(ax)

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
        ax.text(0.95, y, f"{u} — {v}", ha="center", va="center", fontsize=20, color=INK, zorder=3)
    ax.set_xlim(-0.3, 2.2)
    ax.set_ylim(-0.55, 5.7)
    # title removed -- duplicated the figcaption verbatim
    clean(ax)
    save(fig, "store-edgelist.png")


def fig_store_adjlist():
    adj = {0: [1, 2], 1: [0, 2, 3], 2: [0, 1, 4], 3: [1, 4], 4: [2, 3]}
    W = 10.6
    fig, axes = plt.subplots(1, 2, figsize=(W, 5.0))
    ax = axes[0]
    # node_s() keyed to this panel's own share of W -- see fig_adjacency_matrix.
    draw_graph5(ax, highlight_edges=[(1, 0), (1, 2), (1, 3)], highlight_nodes={1}, label_fs=fs(LABEL_FS, W),
                size=node_s(W / 2))
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-1.4, 1.4)
    clean(ax)

    ax = axes[1]
    y0 = 5
    for i, n in enumerate(range(5)):
        y = y0 - i
        text = f"{n} → " + ", ".join(str(m) for m in adj[n])
        hl = n == 1
        edgecolor = ACCENT2 if hl else "none"
        lw = 2.6 if hl else 0
        ax.add_patch(FancyBboxPatch((0.0, y - 0.35), 2.6, 0.7,
                                     boxstyle="round,pad=0.02,rounding_size=0.3",
                                     facecolor=PANEL, edgecolor=edgecolor, linewidth=lw, zorder=2))
        # Fixed size, not fs()-scaled: rows like "1 -> 0, 2, 3" must stay inside a
        # 2.6-unit-wide box -- the literal fs() scale (~37pt) overflowed it.
        ax.text(1.3, y, text, ha="center", va="center", fontsize=18, color=INK, zorder=3)
    ax.set_xlim(-0.3, 2.9)
    ax.set_ylim(0.2, 5.7)
    # title removed -- duplicated the figcaption verbatim
    clean(ax)
    save(fig, "store-adjlist.png")


def fig_store_matrix():
    W = 9.6
    fig, axes = plt.subplots(1, 2, figsize=(W, 5.0))
    ax = axes[0]
    # node_s() keyed to this panel's own share of W -- see fig_adjacency_matrix.
    draw_graph5(ax, highlight_edges=[(1, 0), (1, 2), (1, 3)], highlight_nodes={1}, label_fs=fs(LABEL_FS, W),
                size=node_s(W / 2))
    ax.set_xlim(-0.45, 1.45)
    ax.set_ylim(-1.4, 1.4)
    clean(ax)

    ax = axes[1]
    A = graph5_adjacency()
    # title removed -- duplicated the figcaption verbatim
    draw_matrix(ax, A, row_highlight=1, cell_fs=fs(18, W))
    # R5 fix (Major 17): red (node 1, its three edges, and the matrix row) was never
    # explained anywhere on the slide -- the body talks only about n x n and O(n^2), and the
    # figcaption just counts cells, so a reader had no way to connect the colour to what it
    # marks. States it directly, tied to the row it's pointing at.
    cols = [j for j in range(A.shape[0]) if A[1, j]]
    cols_txt = ", ".join(str(c) for c in cols)
    place_label(ax, (2, A.shape[0] - 0.1), f"row 1 (red) is node 1's row: 1s at columns {cols_txt}",
                obstacles=[text_obstacle(t) for t in ax.get_xticklabels() + ax.get_yticklabels()],
                color=ACCENT2, fontsize=fs(14, W), ha="center", va="top", clearance_pt=4.0,
                zorder=5, name="store-matrix:row-caption")
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
    gs = fig.add_gridspec(1, 2, width_ratios=[0.62, 2.0], wspace=0.28)

    # Cells are only ~0.9 data-units apart and indptr/index values run into two digits
    # (10, 11, 12) -- VALUE_FS is measured (not guessed) to clear the box at this width:
    # matplotlib text-extent for "12" is ~1.28x the point size, and each box now renders
    # ~25pt wide (measured against the reclaimed-margin layout above), so anything under
    # ~19pt leaves real margin. Still a real increase over the pre-R3 9.5px render --
    # clears the 18px page number the review measured against.
    VALUE_FS, ROWLABEL_FS = fs(12.0, W), fs(12.5, W)

    axA = fig.add_subplot(gs[0, 0])
    A = graph5_adjacency()
    draw_matrix(axA, A, row_highlight=1, row_highlight_color=ACCENT3, cell_fs=VALUE_FS)
    # title removed -- the review's "no suptitle" fix already dropped the old 11px
    # explanatory line; this panel doesn't need one either.

    axR = fig.add_subplot(gs[0, 1])
    axR.set_xlim(-1.6, 12.0)
    # R5 fix (Blocker 7): bottom margin pulled in from -1.35 -- that was sized for a second
    # text line now deleted (see below); keeping the old margin would leave dead white space
    # under the one remaining line.
    axR.set_ylim(-0.95 if payoff else -0.6, 3.0)
    axR.set_axis_off()

    def row(y, values, label, highlight_range=None):
        for i, v in enumerate(values):
            fc = ACCENT3 if highlight_range and highlight_range[0] <= i < highlight_range[1] else PANEL
            # Minor fix (slide 053): 0.88-wide boxes let two-digit values (10, 12) touch
            # their own box edge and abut the next cell, reading as "8 1012"; a touch wider.
            axR.add_patch(FancyBboxPatch((i - 0.46, y - 0.34), 0.92, 0.68,
                                          boxstyle="round,pad=0.02,rounding_size=0.1",
                                          facecolor=fc, edgecolor=RULE, linewidth=1.0, zorder=2))
            axR.text(i, y, str(v), ha="center", va="center", fontsize=VALUE_FS, color=INK, zorder=3)
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
        axR.text(mid, -0.65, "indptr[2] − indptr[1] = 5 − 2 = 3 = k₁", ha="center", va="center",
                 color=ACCENT3, fontsize=fs(12.5, W), fontweight="bold", zorder=3)

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
    # NEW (Major 8): slide 055 ("The payoff: memory") split off from csr-payoff.png with
    # only the asymptotic O(n^2)-vs-O(nnz) claim -- the CONCRETE evidence stayed behind on
    # 054's figure (see fig_csr_payoff's R5 fix, Blocker 7: that line is deleted from
    # there). This is that evidence, with its own figure.
    #
    # R6 fix (Blocker 8, "the figure asserts something false, and it is my error"): the R5
    # spec asked for a "12 vs 25" count, but 12 is only the `data` array -- CSR is THREE
    # arrays (data, indices, indptr), and this figure's own dense grid was never compared
    # against their combined size. Computed directly from the actual graph: data has nnz=12
    # entries, indices has nnz=12, indptr has n+1=6 -- CSR stores 30 numbers here, MORE than
    # dense's 25. The old figure (and the slide body) asserted the opposite. Fixed honestly:
    # draw all three CSR arrays (matching what slide 057's own figure already shows, so the
    # two no longer contradict each other), total them truthfully, and show WHERE the
    # crossover actually falls instead of implying it happens at any size.
    A = graph5_adjacency()
    n = A.shape[0]
    dense = A.size

    # CSR arrays derived directly from A (row-major scan), not a separately hand-typed
    # adjacency list -- the R6 spec's own error (an uncaught "12" that quietly excluded two
    # of the three arrays) was exactly this kind of number nobody re-derived from the data.
    indptr = [0]
    indices = []
    data = []
    for i in range(n):
        row = [j for j in range(n) if A[i, j]]
        indices.extend(row)
        data.extend([1] * len(row))
        indptr.append(len(indices))
    nnz = len(data)
    csr_total = len(data) + len(indices) + len(indptr)
    assert nnz == 12 and dense == 25, f"expected 12 nonzeros of 25 dense cells, got {nnz}/{dense}"
    assert csr_total == 30, f"expected CSR to store 12+12+6=30 numbers, got {csr_total}"
    assert csr_total > dense, "this example is supposed to be the counterexample -- CSR should lose here"

    W = 8.6
    # R6 fix (Blocker 8, layout): height bumped 3.4 -> 5.0 to fit the crossover table added
    # below (see the R6 fix comment near the table itself). With clean(ax)'s aspect="equal"
    # and the OLD, shorter 3.4in height, the much-taller y-range this content now needs
    # forced matplotlib to letterbox the axes box down to ~4.8in of the figure's 8.6in width
    # (confirmed directly: get_window_extent() measured 4.81in used, not the ~6.67in a
    # non-letterboxed equal-aspect axes gets at this figsize) -- every x-position compressed
    # into that narrower box, which is what made the two titles overlap and the CSR row
    # labels bleed into the matrix panel. 5.0in is the height at which this content's data
    # aspect ratio stops forcing any letterboxing (measured the same way).
    fig, ax = plt.subplots(figsize=(W, 5.0))
    cell = 0.92
    # Fixed, not fs()-scaled: fs() scales by the FULL figure width, correct for a single
    # panel filling that width, but this figure is two panels of very different widths (the
    # 5-wide dense grid vs. the 12-wide CSR strip) sharing one figure -- the literal fs()
    # scale (title_fs ~28pt) sized the titles for the WIDE strip and overran the narrow
    # dense panel so hard the two titles physically overlapped (same failure the deck
    # already documents in fig_connected_vs_not / fig_circuit_vs_cycle's panel_fs).
    cell_fs = 20
    title_fs = 17

    for i in range(n):
        for j in range(n):
            v = int(A[i, j])
            fc = ACCENT if v else PANEL
            tc = "white" if v else INK
            x, y = j, n - 1 - i
            ax.add_patch(mpatches.Rectangle((x, y), cell, cell, facecolor=fc,
                                             edgecolor=RULE, linewidth=0.8, zorder=1))
            ax.text(x + cell / 2, y + cell / 2, str(v), ha="center", va="center",
                    color=tc, fontsize=cell_fs, zorder=2)
    # R6 fix (layout): shortened from "dense: 25 numbers stored" -- measured directly (see
    # the R6 fix on `gap` below), the two titles' bboxes overlapped by ~2 data units at the
    # old wording's width, regardless of panel spacing. Dropping the redundant "stored" (the
    # caption below already says "numbers stored") buys back the width instead.
    t_dense = ax.text(n * cell / 2, n + 0.55, f"dense: {dense} numbers", ha="center", va="bottom",
                       color=INK, fontsize=title_fs, fontweight="bold", zorder=2)

    # CSR block: all THREE arrays, stacked (indptr is shorter -- n+1, not nnz -- so its row
    # is visibly narrower; that width difference IS part of the honest picture). Real values,
    # same order fig_csr_build/_payoff already draw, so this matches slide 057's own figure.
    #
    # R6 fix (layout): gap widened 1.4 -> 2.6 and the row-label anchor pulled in -- measured
    # directly (get_window_extent on "indices", the widest label, at label_fs=12): its own
    # rendered width is ~1.76 data units, more than the old 0.55pt anchor offset left before
    # hitting the matrix's right edge at x=n*cell -- it was rendering ON TOP of the matrix's
    # last column, not beside it. This gap/offset/font combination is verified below (not
    # just chosen by eye) via the same renderer-measurement the label-placement guard uses.
    gap = 2.6
    x0 = n * cell + gap
    box_w, box_h = cell, 0.68
    row_fs = 15
    label_fs = 12
    label_dx = 0.5
    row_ys = {"indptr": 2.94, "data": 1.64, "indices": 0.34}

    def csr_row(values, y, label):
        for k, v in enumerate(values):
            x = x0 + k * cell
            ax.add_patch(FancyBboxPatch((x - box_w * 0.02, y - box_h / 2), box_w * 0.96, box_h,
                                         boxstyle="round,pad=0.02,rounding_size=0.08",
                                         facecolor=ACCENT3, edgecolor=RULE, linewidth=0.8, zorder=1))
            ax.text(x + box_w / 2 - box_w * 0.02, y, str(v), ha="center", va="center",
                    color=INK, fontsize=row_fs, zorder=2)
        label_t = ax.text(x0 - label_dx, y, label, ha="right", va="center", color=ACCENT,
                           fontsize=label_fs, fontweight="bold", zorder=2)
        renderer = _finalize(ax)
        lb = label_t.get_window_extent(renderer)
        matrix_right_px = ax.transData.transform((n * cell, 0))[0]
        assert lb.x0 >= matrix_right_px, (
            f"fig_memory_payoff: row label {label!r} (left edge {lb.x0:.0f}px) overlaps the "
            f"dense matrix (right edge {matrix_right_px:.0f}px) -- widen `gap` or shrink "
            f"label_fs/label_dx."
        )

    csr_row(indptr, row_ys["indptr"], "indptr")
    csr_row(data, row_ys["data"], "data")
    csr_row(indices, row_ys["indices"], "indices")
    t_csr = ax.text(x0 + nnz * cell / 2, n + 0.55,
                     f"CSR: {csr_total} numbers ({len(data)} + {len(indices)} + {len(indptr)})",
                     ha="center", va="bottom", color=INK, fontsize=title_fs, fontweight="bold", zorder=2)

    # R6 fix: measured, not eyeballed -- the two titles' own rendered bboxes must not overlap
    # (this exact failure -- two panel titles colliding mid-word -- is what R6 found here and
    # what fig_connected_vs_not/fig_circuit_vs_cycle's panel_fs comment already documents as
    # a recurring class of bug in this file).
    renderer = _finalize(ax)
    b_dense = t_dense.get_window_extent(renderer)
    b_csr = t_csr.get_window_extent(renderer)
    assert b_dense.x1 <= b_csr.x0, (
        f"fig_memory_payoff: panel titles overlap ({b_dense.x1:.0f}px vs {b_csr.x0:.0f}px) -- "
        f"shorten the wording, shrink title_fs, or widen the panel gap."
    )

    # Caption sits below both blocks -- checked against the lower of the matrix's own bottom
    # row and the CSR block's bottom (indices) row.
    bottom_y = min(0.0, row_ys["indices"] - box_h / 2)
    obstacles = [line_obstacle([(0, bottom_y), (x0 + nnz * cell, bottom_y)], EDGE_W, color=None)]
    place_label(ax, ((n * cell + x0 + nnz * cell) / 2, bottom_y - 0.25),
                f"CSR pays for indices + indptr on top of data -- {csr_total} numbers here, "
                f"more than dense's {dense}",
                obstacles=obstacles, color=MUTED, fontsize=14, ha="center", va="top",
                clearance_pt=4.0, name="memory-payoff:caption")

    # R6 fix (Blocker 8, continued): the toy example is the honest COUNTEREXAMPLE, not the
    # whole story -- show where the asymptotic O(n^2) vs O(nnz) claim actually kicks in.
    # Both larger rows come from _csr_vs_dense_counts (same formula as the n=5 row above,
    # just evaluated at a bigger n), not hand-typed numbers.
    dense_1k, csr_1k = _csr_vs_dense_counts(1_000, 6)
    dense_100k, csr_100k = _csr_vs_dense_counts(100_000, 6)
    assert (dense_1k, csr_1k) == (1_000_000, 13_001), (dense_1k, csr_1k)
    assert (dense_100k, csr_100k) == (10_000_000_000, 1_300_001), (dense_100k, csr_100k)

    table_x = 0.0
    table_top = bottom_y - 0.95
    table_fs = 13
    rows = [
        (f"n = 5          (avg degree 2.4):  dense {dense:,}"
         f"  ·  CSR {csr_total:,}  (dense wins here)"),
        (f"n = 1,000      (avg degree 6):    dense {dense_1k:,}"
         f"  ·  CSR {csr_1k:,}  (CSR wins ~{dense_1k / csr_1k:.0f}×)"),
        (f"n = 100,000    (avg degree 6):    dense {dense_100k:,}"
         f"  ·  CSR {csr_100k:,}  (CSR wins ~{dense_100k / csr_100k:,.0f}×)"),
    ]
    for i, line in enumerate(rows):
        ax.text(table_x, table_top - i * 0.5, line, ha="left", va="top",
                color=MUTED, fontsize=table_fs, family="monospace", zorder=2)

    ax.set_xlim(-0.3, x0 + nnz * cell + 0.3)
    ax.set_ylim(table_top - len(rows) * 0.5 - 0.2, n * cell + 1.0)
    clean(ax)
    save_fit(fig, ax, "csr-memory.png", pad_frac=0.05, pad_min_in=0.08)


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
    W = 10.0
    fig, ax = plt.subplots(figsize=(W, 5.0))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    # bottom-right: large + sparse -- CSR's regime
    ax.add_patch(mpatches.Rectangle((3, 0), 7, 5, facecolor=PANEL, edgecolor=RULE, linewidth=1.5, zorder=1))
    ax.text(6.5, 3.2, "CSR", ha="center", va="center", fontsize=22, color=INK, fontweight="bold", zorder=2)
    ax.text(6.5, 1.7, "large + sparse", ha="center", va="center", fontsize=17, color=MUTED, zorder=2)

    # top-left: small + dense -- dense array's regime
    ax.add_patch(mpatches.Rectangle((0, 5), 3, 5, facecolor=PANEL, edgecolor=RULE, linewidth=1.5, zorder=1))
    ax.text(1.5, 8.3, "dense\narray", ha="center", va="center", fontsize=20, color=INK, fontweight="bold", zorder=2)
    ax.text(1.5, 6.3, "small\n(or dense)", ha="center", va="center", fontsize=16, color=MUTED, zorder=2)

    # top-right: large + dense -- rare in practice, unfilled but no longer unlabeled
    ax.text(6.5, 8.0, "large + dense", ha="center", va="center", fontsize=17, color=MUTED, zorder=2)
    ax.text(6.5, 6.5, "rare in practice", ha="center", va="center", fontsize=16, color=MUTED, zorder=2)

    # bottom-left: small + sparse -- either format works, size dominates
    ax.text(1.5, 3.3, "small +\nsparse", ha="center", va="center", fontsize=16, color=MUTED, zorder=2)
    ax.text(1.5, 1.4, "either\nis fine", ha="center", va="center", fontsize=16, color=MUTED, zorder=2)

    ax.plot([3, 3], [0, 10], color=RULE, linewidth=1.2, zorder=1)
    ax.plot([0, 10], [5, 5], color=RULE, linewidth=1.2, zorder=1)

    # R5 fix (Major 19): the arrow sat at x=8.6, but "large + sparse" (and "large + dense"
    # above it) render far wider than their short word count suggests at this fontsize --
    # measured directly, both span roughly x=[4.4, 8.6] -- so the arrow's head landed
    # exactly on the terminal "e" of "sparse" and its shaft grazed "dense"'s. Moved to
    # x=9.3, clear of both (measured, not guessed) with real margin before the panel edge
    # at x=10.
    arrow_x = 9.3
    place_annotation(ax, (arrow_x, 1.1), "real networks\nlive here", xytext=(arrow_x, 9.2),
                      obstacles=[], color=MUTED, fontsize=fs(ANNOT_FS, W), ha="center",
                      lw=2, arrowstyle="-|>", name="format-regimes:real-networks")
    ax.set_xlabel("network size →", fontsize=fs(18, W), color=INK)
    ax.set_ylabel("density →", fontsize=fs(18, W), color=INK)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color(RULE)
    save(fig, "format-regimes.png")


# ===========================================================================
# Part 7 -- edge cases
# ===========================================================================
# R4 fix (Policy 2): bbox_inches="tight" turns out NOT to crop a bare `ax.scatter()` down
# to the marker's own footprint -- Axes.get_tightbbox() still reports (close to) the full
# declared xlim/ylim extent even with the axis off, confirmed by an isolated repro. At the
# old figsize=(3.3, 2.85) with xlim/ylim (-0.7,0.7)/(-0.6,0.6), that left a ~33px dot on a
# 571x498 canvas -- 15% x 17% ink. A small, closely-matched xlim/ylim (not a bigger marker)
# is what actually controls the saved canvas size here; the marker keeps a fixed,
# legible point-size (matching the reference node size used everywhere else, node_s at
# FONT_REF_WIDTH) instead of shrinking with the now-small figsize.
#
# R5 fix (Policy 2): that hand-picked xlim/ylim still only bought 45-49% ink (measured) --
# save_fit (see fig_selfloop's R5 fix) replaces the guess with a crop measured directly off
# the real rendered content, same as the self-loop family. out_dpi bumped for the same
# reason too: the true content here is tiny in inches, so a low native pixel count would go
# soft once the deck scales it back up to its usual on-slide width.
EDGE_SINGLE_FIGSIZE = (1.48, 1.3)
EDGE_SINGLE_NODE_S = node_s(FONT_REF_WIDTH)


def fig_edge_single_node():
    # A lone scatter marker -- safe to drop equal-aspect for a landscape crop; the dot
    # itself stays perfectly round either way (scatter markers are sized in points).
    fig, ax = plt.subplots(figsize=EDGE_SINGLE_FIGSIZE)
    ax.set_xlim(-0.55, 0.55)
    ax.set_ylim(-0.48, 0.48)
    clean(ax, equal=False)
    ax.scatter([0], [0], s=EDGE_SINGLE_NODE_S, c=INK, zorder=2, linewidths=0)
    save_fit(fig, ax, "edge-single-node.png", extra_scatter=[((0, 0), EDGE_SINGLE_NODE_S)],
             pad_frac=0.14, pad_min_in=0.05, out_dpi=1200)


def fig_edge_single_node_answer():
    # Minor fix: slide 059's caption asserts "one node, one component" but the reused
    # edge-single-node.png (same figure as the still-open question on 058) has nothing
    # visual marking a component -- a thin ring earns the word, and distinguishes the
    # "answer" frame from the "question" frame it was previously identical to.
    fig, ax = plt.subplots(figsize=EDGE_SINGLE_FIGSIZE)
    ax.set_xlim(-0.55, 0.55)
    ax.set_ylim(-0.48, 0.48)
    clean(ax, equal=False)
    ax.add_patch(mpatches.Circle((0, 0), 0.32, facecolor="none", edgecolor=MUTED, linewidth=2.2, zorder=1))
    ax.scatter([0], [0], s=EDGE_SINGLE_NODE_S, c=INK, zorder=2, linewidths=0)
    save_fit(fig, ax, "edge-single-node-answer.png", extra_scatter=[((0, 0), EDGE_SINGLE_NODE_S)],
             pad_frac=0.14, pad_min_in=0.05, out_dpi=1200)


def fig_edge_disconnected():
    W = 6.0
    fig, ax = plt.subplots(figsize=(W, 3.2))
    t1 = {"a": (-1.3, 0.55), "b": (-1.95, -0.4), "c": (-0.65, -0.4)}
    t2 = {"d": (1.3, 0.55), "e": (0.65, -0.4), "f": (1.95, -0.4)}
    for tri in (t1, t2):
        keys = list(tri.keys())
        for i in range(3):
            u, v = keys[i], keys[(i + 1) % 3]
            ax.plot([tri[u][0], tri[v][0]], [tri[u][1], tri[v][1]], color=MUTED,
                     linewidth=EDGE_W, zorder=1, solid_capstyle="round")
    allpos = {**t1, **t2}
    xs = [p[0] for p in allpos.values()]
    ys = [p[1] for p in allpos.values()]
    # R5 fix (Major 15): the old xlim/ylim margin around the outermost node CENTRES (b/f at
    # x=+-1.95, a/d at y=0.55, b/c/e/f at y=-0.4) was 0.30-0.35 data units -- less than the
    # marker's own true radius (~0.42, measured -- see node_radius_data). scatter markers
    # clip to the AXES limits at render time (clip_on=True by default), so every outermost
    # disc got a flat edge exactly at the frame boundary: two flat tops, one flat left, one
    # flat bottom. clip_on=False is a belt-and-suspenders second guard -- even if a future
    # edit narrows the margin again, the marker still won't visibly guillotine (though the
    # tight crop below could still cut close, so the margin fix is the one actually load-
    # bearing here).
    ax.scatter(xs, ys, s=node_s(W), c=INK, zorder=3, linewidths=0, clip_on=False)
    # "every degree even" removed -- it is the figcaption verbatim on this slide's first use.
    ax.set_xlim(-2.42, 2.42)
    ax.set_ylim(-0.87, 0.97)
    clean(ax)
    save(fig, "edge-disconnected.png")


# ===========================================================================
# Wrap-up
# ===========================================================================
def fig_recap():
    W = 6.6
    fig, ax = plt.subplots(figsize=(W, 5.6))
    draw_kedges(ax)
    draw_knodes(ax, size=node_s(W))
    # R3 fix (Major 22): the label sat close enough to the dashed "one component" bracket
    # that "parity" clipped it, and the solid leader crossed the dashed arc right beside the
    # text. Kept in the upper-left (clearly outside the radius-1.5 dashed circle even once
    # the text's own width is accounted for) but lowered below "one component"'s own row so
    # the two labels no longer collide with each other either; the leader now points at
    # node A's left side, not its centre.
    #
    # R4 fix (Minor, slide 065): -0.16 landed the arrow tip INSIDE node A's own disc
    # (radius ~0.37 data-units at this figsize) -- the leader ran past the boundary it was
    # supposed to stop at. -0.42 clears it.
    ax.annotate("degree → parity", xy=(KPOS["A"][0] - 0.42, KPOS["A"][1]), xytext=(-2.6, 1.35),
                 fontsize=ANNOT_FS, color=MUTED, ha="left",
                 arrowprops=dict(arrowstyle="-", color=MUTED, lw=1.3))
    # "one component" and "A: 4x4 matrix" are both global facts about the whole graph, not
    # facts about any single node or edge -- the old leaders crossed the N-B edge and
    # landed on node B respectively (F2 fix). A dashed bracket enclosing all four nodes
    # replaces the "one component" leader; "A: 4x4 matrix" is a plain floating label.
    bracket = mpatches.Ellipse((0, 0), 3.0, 3.0, fill=False, edgecolor=MUTED, linewidth=1.4,
                                linestyle=(0, (5, 4)), zorder=1)
    ax.add_patch(bracket)
    ax.text(0, 1.72, "one component", ha="center", va="bottom", color=MUTED, fontsize=ANNOT_FS)
    ax.text(0, -1.72, "A: 4 × 4 matrix", ha="center", va="top", color=MUTED, fontsize=ANNOT_FS)
    ax.set_xlim(-2.85, 2.15)
    ax.set_ylim(-2.15, 2.25)
    clean(ax)
    save(fig, "recap.png")


def fig_smallworld_teaser():
    # (a) k=4 ring lattice -- each node joined to its two nearest neighbors on *each*
    # side (not just one), so the base ring actually has the triangle-free-but-clustered
    # structure a small-world figure needs (the old j=(i+1)%n ring was k=2, with zero
    # triangles -- a counterexample to "high clustering", not an example of it).
    # (b) shortcuts use varied chord lengths, not four exact diameters that all cross the
    # center and read as a hub that doesn't exist (F2/F4 fix).
    # R3 fix (Major 20): at n=20 the node discs touched each other, sitting at zorder=3
    # over the edges' zorder=1, so BOTH the i-i+1 and i-i+2 edges were fully occluded and
    # the ring rendered as a smooth gray annulus. Fewer, more widely spaced nodes (n=12-14)
    # and much smaller discs (s ~ 180, not 620) give every second-neighbor chord room to
    # clear the discs it passes near.
    n = 13
    fig, ax = plt.subplots(figsize=(5.6, 5.6))
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False)
    pts = {i: (np.cos(a), np.sin(a)) for i, a in enumerate(angles)}
    for i in range(n):
        for step in (1, 2):
            j = (i + step) % n
            ax.plot([pts[i][0], pts[j][0]], [pts[i][1], pts[j][1]], color=MUTED,
                     linewidth=EDGE_W, zorder=1)
    for u, v in [(0, 4), (2, 7), (5, 11), (9, 12)]:
        ax.plot([pts[u][0], pts[v][0]], [pts[u][1], pts[v][1]], color=ACCENT2, linewidth=EDGE_W, zorder=2)
    xs = [pts[i][0] for i in range(n)]
    ys = [pts[i][1] for i in range(n)]
    ax.scatter(xs, ys, s=180, c=INK, zorder=3, linewidths=0)
    # "a few shortcuts change everything" removed -- it is the figcaption verbatim.
    # A touch of extra x-room (the ring itself stays circular) lands the crop <=0.95.
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.3, 1.3)
    clean(ax)
    save(fig, "smallworld-teaser.png")


if __name__ == "__main__":
    fig_konigsberg_sketch()

    fig_abstraction_1_map()
    fig_abstraction_2_nodes()
    fig_abstraction_3_graph()
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
    fig_components_bare()
    fig_sweep_1()
    fig_sweep_2()
    fig_sweep_3()
    fig_giant_scale()
    fig_directed_arrows()
    fig_directed_strong()
    fig_directed_weak()
    fig_directed_indegree()

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

    fig_recap()
    fig_smallworld_teaser()

    print("done")
