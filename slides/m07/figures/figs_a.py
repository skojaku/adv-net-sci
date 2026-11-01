#!/usr/bin/env python3
"""Worker A: the drawn scenes and the small graphs of the M07 deck.

    pearson-walker     L-c    a stick figure on a field, the first steps of a walk
    pearson-answer     L-g    5 paths and 10,000 end points (Pearson 1905)
    fields             L-b    pollen, mosquito, web: three fields, then "and on a network?"
    walk-rule          L-b    the rule: each of 4 edges carries 1/4
    two-comm-q         L-c    two 5-cliques and one edge, the walker in community 1
    two-comm-walk      L-b    the walk coloured by community, and the time strip
    clique-q / -a      L-a    a 10-clique and the distance curve (empty axes / the curve)
    twoclique-q / -a   L-a    the same for two 5-cliques joined by one edge
    no-larger          L-b    one step replaces every number by the average of its neighbours
    detailed-balance   L-a    the flow along one edge is equal in both directions
    tasks-diamond      L-c    the 4-node diamond and the QR placeholder for the Part 3 notebook

Every number comes from smallgraphs.py or is computed here from a seeded walk and asserted.
Community 1 is cool (blue), community 2 is hot (red); a walker is a ring in ink.
"""

import math

import numpy as np

import figlib as F
import smallgraphs as G

# The display caps of the deck's layouts (theme.css): B 480 (420 with a take), A 380 (320 with a
# sub and a take), G 600, C 470.  figlib's own table was written for the m04 container.
F.FIG_H.update({"a": 380, "at": 320, "b": 480, "bt": 420, "g": 600, "c": 470})

ARROW = "-{Stealth[length=10bp,width=8bp]}"
HEAD = "{Stealth[length=10bp,width=8bp]}"
CA, CB = "cool", "hot"                     # community 1 / community 2
FA, FB = "cool!45", "hot!45"               # their node fills


def comm_fill(n):
    return FA if n < 5 else FB


def edges_ink(edges, pos, color="ink", w=F.EDGE_W, opacity=None):
    return "".join(F.seg(pos[a], pos[b], color=color, w=w, opacity=opacity) for a, b in edges)


def discs_ink(pos, fills=None, size=F.NODE, labels=None):
    out = ""
    for n, p in pos.items():
        fill = (fills or {}).get(n, "white")
        out += F.disc(p[0], p[1], str((labels or {}).get(n, "")), fill=fill, size=size)
    return out


def pent(cx, cy, r, first_angle):
    """five points on a circle, the first at first_angle (degrees), counter-clockwise."""
    return [(cx + r * math.cos(math.radians(first_angle + 72 * k)),
             cy + r * math.sin(math.radians(first_angle + 72 * k))) for k in range(5)]


def two_clique_layout(cxa, cxb, cy, r):
    """TWOC: nodes 0-4 on the left pentagon (node 4 faces the right), 5-9 on the right (node 5
    faces the left); the bridge is the edge 4-5."""
    pos = {}
    for k, p in enumerate(pent(cxa, cy, r, 0)):
        pos[[4, 0, 1, 2, 3][k]] = p
    for k, p in enumerate(pent(cxb, cy, r, 180)):
        pos[[5, 6, 7, 8, 9][k]] = p
    return pos


TWOC_EDGES = [tuple(e) for e in G.TWOC.edges()]
assert len(TWOC_EDGES) == 21


def walk_nodes(P, start, steps, seed):
    return G.walk(P, start, steps, np.random.default_rng(seed))


# ============================================================================ photo composites
PHOTOS = F.OUT / "photos"


def _photo(name, crop, box_px):
    """crop = (x0, y0, x1, y1) in source pixels; box_px = (w, h) in raster pixels."""
    from PIL import Image
    im = Image.open(PHOTOS / name).convert("RGB").crop(crop)
    return im.resize(box_px, Image.LANCZOS)


def emit_photo(name, body, container, h, hmod, photos, centred=False):
    """Render the TikZ body, paste the photos on the 4x raster (after the grain, so a photo is not
    mottled), then run figlib's gates and save.  photos = [(PIL image, (x, y_from_top, w, h) in bp)]."""
    from PIL import Image
    w = F.DESIGN[container]
    im = F.render(body, w, h)
    for ph, (x, y, pw, pwh) in photos:
        assert ph.size == (int(pw * F.PXBP), int(pwh * F.PXBP)), (name, ph.size)
        im.paste(ph, (int(x * F.PXBP), int(y * F.PXBP)))
    im, fw, fh, *_ = F.crop_and_check(name, im, container, hmod, nodes=False)
    if centred:
        xs = np.where(np.asarray(im.convert("L")) < 200)[1]
        off = ((xs.min() + xs.max()) / 2 - fw / 2) / F.PXBP
        assert abs(off) <= 4, f"{name}: the ink is {off:+.1f}bp off the centre of the canvas"
    im.save(F.OUT / f"{name}.png")
    F._built.append(name)
    F._report(name, im, container, hmod)


def frame_rect(x0, y0, x1, y1, color="pale", w=3.0):
    return f"\\draw[{color},line width={w}bp] ({x0},{y0}) rectangle ({x1},{y1});\n"


# ============================================================================ pearson-walker
def f_pearson_walker():
    """TOP: the walker on a field, one yard per step.  BELOW it: the pub (photo)."""
    H, dy = 560.0, 262.0                       # canvas height; the drawing is shifted up by dy
    ox, oy = 186.0, 120.0                       # where the walker stands (screen, before the shift)
    sh, sy = 0.28, 0.5                          # the field is drawn at an angle: shear and squash
    L = 70                                      # one yard, in field units

    def S(u, v):
        return (ox + u + sh * v, oy + sy * v)

    o = f"\\begin{{scope}}[shift={{(0,{dy})}}]\n"
    us = list(range(-140, 281, L))
    vs = list(range(-70, 211, L))
    for v in vs:
        o += F.seg(S(us[0], v), S(us[-1], v), color="muted", w=1.7, opacity=0.55)
    for u in us:
        o += F.seg(S(u, vs[0]), S(u, vs[-1]), color="muted", w=1.7, opacity=0.55)
    pts = [(0.0, 0.0)]
    for a in [38, 112, 8, -42, 76]:               # five steps of one yard, random directions
        pts.append((pts[-1][0] + L * math.cos(math.radians(a)), pts[-1][1] + L * math.sin(math.radians(a))))
    assert all(us[0] <= u <= us[-1] and vs[0] <= v <= vs[-1] for u, v in pts)
    sp = [S(u, v) for u, v in pts]
    o += F.polyline(sp, color="hot", w=5.0)
    for p in sp[1:]:
        o += F.dot(p[0], p[1], color="hot", d=13)
    x, y = sp[0]                                  # the stick figure, standing on the start
    o += F.sketch_circle(x, y + 118, 30, color="ink", w=3.2)
    for p, q in [((x, y + 103), (x, y + 50)), ((x, y + 50), (x - 20, y)), ((x, y + 50), (x + 20, y)),
                 ((x, y + 92), (x - 30, y + 62)), ((x, y + 92), (x + 30, y + 62))]:
        o += F.seg(p, q, color="ink", w=4.0)
    mid = ((sp[0][0] + sp[1][0]) / 2, (sp[0][1] + sp[1][1]) / 2)
    t, _ = F.aside("1 yard", at=(mid[0] + 96, mid[1] - 26), target=(mid[0] + 12, mid[1] - 2), anchor="west", bend=-25)
    o += t
    o += "\\end{scope}\n"
    # the pub, directly under the drawing: a pale frame, the photo pasted over it
    px0, pw, ph_ = 18.0, 500.0, 250.0
    ptop = H - (oy + sy * -70 + dy) + 14             # just below the lowest grid line
    o += frame_rect(px0 - 2, H - ptop + 2, px0 + pw + 2, H - ptop - ph_ - 2)
    pub = _photo("pub.jpg", (90, 520, 1300, 1130), (int(pw * F.PXBP), int(ph_ * F.PXBP)))
    emit_photo("pearson-walker", o, "col", int(H), "c", [(pub, (px0, ptop, pw, ph_))])


# ============================================================================ pearson-answer
def _cloud(xy, side, cx, cy, ss=3):
    """10,000 translucent dots as one transparent PNG (10,000 TikZ fills exceed TeX's memory)."""
    from PIL import Image
    n = int(side * ss)
    r = 1.7 * ss
    k = int(2 * r + 3)
    yy, xx = np.mgrid[0:k, 0:k]
    stamp = (((xx - k / 2) ** 2 + (yy - k / 2) ** 2) <= r * r).astype(np.float32)
    cnt = np.zeros((n, n), dtype=np.float32)
    for x, y in xy:
        px, py = int((x + side / 2) * ss - k / 2), int((side / 2 - y) * ss - k / 2)
        cnt[py:py + k, px:px + k] += stamp
    out = np.zeros((n, n, 4), dtype=np.uint8)
    out[..., 0], out[..., 1], out[..., 2] = 0x39, 0x59, 0xA6
    out[..., 3] = ((1 - 0.70 ** cnt) * 255).astype(np.uint8)
    path = F.OUT / "_cloud.png"
    Image.fromarray(out, "RGBA").save(path)
    return f"\\node at ({cx},{cy}) {{\\pgfimage[width={side}bp]{{{path}}}}};\n"


def f_pearson_answer():
    sc = 7.0                                    # px per yard; both panels the same
    cxl, cxr, cy = 215.0, 800.0, 215.0
    rng = np.random.default_rng(1905)
    o = ""
    # left: 5 walkers of 100 unit steps
    cols = ["cool!70", "hot!70", "deep!60", "tealc", "olivec"]
    for k in range(5):
        a = rng.uniform(0, 2 * np.pi, 100)
        xy = np.vstack([[0, 0], np.cumsum(np.c_[np.cos(a), np.sin(a)], axis=0)]) * sc
        assert np.abs(xy).max() < 190, "a path leaves its panel"
        o += F.polyline([(cxl + x, cy + y) for x, y in xy], color=cols[k], w=3.0)
        o += F.dot(cxl + xy[-1][0], cy + xy[-1][1], color=cols[k], d=10)
    # right: the end points of 10,000 walkers
    a = rng.uniform(0, 2 * np.pi, (10000, 100))
    end = np.c_[np.cos(a).sum(axis=1), np.sin(a).sum(axis=1)]
    rms = float(np.sqrt((end ** 2).sum(axis=1).mean()))
    assert abs(rms - 10) / 10 < 0.03, rms          # the typical distance after 100 unit steps is 10
    keep = (np.abs(end) * sc < 195).all(axis=1)
    assert keep.mean() > 0.995
    o += _cloud(end[keep] * sc, 400, cxr, cy)
    o += (f"\\draw[muted,line width=3bp,dash pattern=on 9bp off 7bp] ({cxr:.1f},{cy:.1f}) circle ({10 * sc:.1f}bp);\n")
    for cx in (cxl, cxr):
        o += F.disc(cx, cy, "", fill="ink", size=14)
    o += F.text(cxl, cy + 215, "5 walkers", anchor="south")
    o += F.text(cxr, cy + 215, "10,000 walkers", anchor="south")
    t, _ = F.aside("typical\\\\distance after\\\\100 steps", at=(600, cy - 70), target=(cxr - 10 * sc * 0.72, cy - 10 * sc * 0.70),
                   anchor="east", bend=-25)
    o += t
    t, _ = F.aside("the start", at=(cxl + 20, cy + 140), target=(cxl + 2, cy + 12), anchor="south", bend=30)
    o += t
    F.emit("pearson-answer", o, container="full", h=520, hmod="g", nodes=False)


# ============================================================================ fields
def f_fields():
    """Three panels, centred: pollen (Perrin's trace), a mosquito (photo), the web (drawing)."""
    from PIL import Image
    H = 350.0
    pw, ph_, gap = 320.0, 240.0, 30.0
    x0 = [(1080 - (3 * pw + 2 * gap)) / 2 + k * (pw + gap) for k in range(3)]        # 30, 380, 730
    top = 12.0                                                                        # raster top of every panel
    ty1, ty0 = H - top, H - top - ph_                                                  # tikz y of the panel
    o = ""
    for k in range(3):
        o += frame_rect(x0[k] - 2, ty0 - 2, x0[k] + pw + 2, ty1 + 2)
    # (3) the web: a small graph with a surfer, centred in its panel
    cx, cy = x0[2] + pw / 2, (ty0 + ty1) / 2
    off = {0: (-87, 65), 1: (1, 95), 2: (85, 33), 3: (-71, -75), 4: (19, -33), 5: (87, -95)}
    wpos = {n: (cx + 1.12 * a, cy + 1.0 * b) for n, (a, b) in off.items()}
    wed = [(0, 1), (1, 2), (0, 4), (1, 4), (3, 4), (4, 5), (2, 5), (3, 0)]
    for a_, b_ in wed:
        o += F.seg(wpos[a_], wpos[b_], color="ink", w=2.6)
    o += discs_ink(wpos, size=F.NODE)
    o += F.ring(*wpos[4], size=F.NODE, color="hot", w=3.4, grow=16)
    for k, cap in enumerate(["a grain in water\\\\(Perrin's trace)", "mosquitoes\\\\and malaria", "the web, 1998\\\\(a random surfer)"]):
        o += F.text(x0[k] + pw / 2, ty0 - 12, cap, anchor="north")
    # (1) Perrin's trace, recoloured grey; (2) the mosquito
    pr0 = Image.open(PHOTOS / "perrin.png").convert("RGBA")
    pr = Image.new("RGBA", pr0.size, "white")
    pr.alpha_composite(pr0)
    pr = pr.convert("L")
    pr = pr.resize((int(pr.width * (ph_ - 16) / pr.height), int(ph_ - 16)), Image.LANCZOS)
    pr = pr.point(lambda v: int(255 - (255 - v) * 0.78)).convert("RGB")
    canvas = Image.new("RGB", (int(pw * F.PXBP), int(ph_ * F.PXBP)), "white")
    pr4 = pr.resize((int(pr.width * F.PXBP), int(pr.height * F.PXBP)), Image.LANCZOS)
    canvas.paste(pr4, ((canvas.width - pr4.width) // 2, (canvas.height - pr4.height) // 2))
    mq = _photo("mosquito.jpg", (380, 60, 1900, 1200), (int(pw * F.PXBP), int(ph_ * F.PXBP)))
    emit_photo("fields", o, "full", int(H), "b", [(canvas, (x0[0], top, pw, ph_)), (mq, (x0[1], top, pw, ph_))],
               centred=True)


# ============================================================================ polya
def _lattice_walk(dim, steps, seed):
    rng = np.random.default_rng(seed)
    axis = rng.integers(0, dim, steps)
    sign = rng.choice([-1, 1], steps)
    d = np.zeros((steps, dim), dtype=int)
    d[np.arange(steps), axis] = sign
    return np.vstack([np.zeros((1, dim), dtype=int), np.cumsum(d, axis=0)])


def _returns(path):
    return int((np.abs(path[1:]).sum(axis=1) == 0).sum())


def _frac_returning(dim, walkers, steps, seed):
    """fraction of walkers that have been back at the start at least once within `steps`, and at step 400."""
    rng = np.random.default_rng(seed)
    pos = np.zeros((walkers, dim), dtype=np.int16)
    back = np.zeros(walkers, dtype=bool)
    at400 = None
    for t in range(1, steps + 1):
        axis = rng.integers(0, dim, walkers)
        pos[np.arange(walkers), axis] += rng.choice(np.array([-1, 1], dtype=np.int16), walkers)
        back |= (pos == 0).all(axis=1)
        if t == 400:
            at400 = back.mean()
    return back.mean(), at400


def f_polya():
    steps = 400
    # a seed for each panel: 2D comes back to the start several times, 3D never does
    s2 = next(s for s in range(1, 2000) if _returns(_lattice_walk(2, steps, s)) in (4, 5, 6, 7)
              and np.ptp(_lattice_walk(2, steps, s), axis=0).max() >= 26)
    s3 = next(s for s in range(1, 2000) if _returns(_lattice_walk(3, steps, s)) == 0
              and 26 <= np.ptp(_lattice_walk(3, steps, s)[:, :2] + 0.0, axis=0).max() <= 38
              and np.abs(_lattice_walk(3, steps, s)[-1]).sum() >= 24)
    p2, p3 = _lattice_walk(2, steps, s2), _lattice_walk(3, steps, s3)
    r2, r3 = _returns(p2), _returns(p3)
    assert r2 >= 4 and r3 <= 1, (r2, r3)
    # the probabilities behind the picture (Polya 1921): 3D, the chance of ever coming back is 0.34
    f3, f3_400 = _frac_returning(3, 10000, 2000, 7)
    f2, f2_400 = _frac_returning(2, 10000, 2000, 7)
    assert 0.30 <= f3 <= 0.36, f3
    # 2D: the return probability is 1 in the limit, but the approach is very slow (about 1 - pi/ln n)
    assert 0.50 <= f2 <= 0.72 and f2 > f2_400 > f3, (f2, f2_400, f3)
    print(f"    polya: seeds {s2} / {s3}; returns {r2} / {r3}; within 2,000 steps: 2D {f2:.2f}, 3D {f3:.2f}")

    def to_screen(path, dim):
        if dim == 2:
            return path.astype(float)
        x, y, z = path.T.astype(float)             # an oblique projection of the cubic lattice
        return np.c_[x + 0.55 * z, y + 0.35 * z]

    o = ""
    panels = [("2D", p2, 2, 275.0), ("3D", p3, 3, 805.0)]
    cy = 270.0
    xys = [to_screen(p, d) for _, p, d, _cx in panels]
    size = max((xy.max(axis=0) - xy.min(axis=0)).max() for xy in xys)
    sc = 360.0 / size                              # one scale for both panels
    for (name, p, d, cx), xy in zip(panels, xys):
        o += frame_rect(cx - 250, cy - 190, cx + 250, cy + 190)
        o += F.text(cx, cy + 190 + 8, name, anchor="south", size=F.FONT)
        mid = (xy.max(axis=0) + xy.min(axis=0)) / 2
        pts = [(cx + sc * (a - mid[0]), cy + sc * (b - mid[1])) for a, b in xy]
        o += F.polyline(pts, color="muted", w=2.6)
        o += F.dot(*pts[-1], color="ink", d=13)
        o += F.ring(*pts[0], size=22, color="hot", w=3.6, grow=8)
        o += F.dot(*pts[0], color="hot", d=14)
    o += F.text(275.0, cy - 190 - 8, f"back at the start {r2} times", anchor="north")
    o += F.text(805.0, cy - 190 - 8, "never back at the start", anchor="north")
    F.emit("polya", o, container="full", h=int(2 * cy + 30), hmod="g", nodes=False)


# ============================================================================ walk-rule
RULE_PX = {0: (540, 262), 1: (150, 372), 2: (62, 182), 3: (935, 372), 4: (1018, 182), 5: (790, 34), 6: (290, 34)}


def f_walk_rule():
    pos = RULE_PX
    edges = [tuple(e) for e in G.RULE.edges()]
    F.assert_planar_drawing(edges, pos, "walk-rule")
    o = edges_ink(edges, pos, color="ink", w=2.8)
    o += discs_ink(pos, fills={0: "white"})
    o += F.ring(*pos[0], size=F.NODE, color="ink", w=3.0, grow=22)
    for nb in (1, 2, 3, 4):
        (x0, y0), (x1, y1) = pos[0], pos[nb]
        mx, my = x0 + (x1 - x0) * 0.5, y0 + (y1 - y0) * 0.5
        dx, dy = x1 - x0, y1 - y0
        L = math.hypot(dx, dy)
        nx_, ny_ = -dy / L, dx / L
        if ny_ < 0:                                  # put every label on the upper side of its edge
            nx_, ny_ = -nx_, -ny_
        o += f"\\fill[white] ({mx + nx_ * 34 - 36:.1f},{my + ny_ * 34 - 21:.1f}) rectangle ({mx + nx_ * 34 + 36:.1f},{my + ny_ * 34 + 21:.1f});\n"
        o += F.text(mx + nx_ * 34, my + ny_ * 34, "1/4", color="hot", anchor="center")
    t, _ = F.aside("no memory of where\\\\it came from", at=(540, 90), target=(540, pos[0][1] - 40),
                   anchor="south", bend=0)
    o += t
    F.emit("walk-rule", o, container="full", h=450, hmod="b", nodes=True)


# ============================================================================ two-comm-q
def f_two_comm_q():
    pos = two_clique_layout(130, 407, 215, 78)
    o = ""
    for cx, col in ((130, CA), (407, CB)):
        o += (f"\\draw[{col},line width=2.6bp,dash pattern=on 10bp off 7bp,opacity=0.65] "
              f"({cx},215) circle (124bp);\n")
    inner = [e for e in TWOC_EDGES if e != (4, 5)]
    o += edges_ink(inner, pos, color="ink", w=2.2, opacity=0.8)
    o += F.seg(pos[4], pos[5], color="ink", w=F.HEAVY_W)
    o += discs_ink(pos, fills={n: comm_fill(n) for n in pos})
    o += F.ring(*pos[2], size=F.NODE, color="ink", w=3.0, grow=20)
    mid = ((pos[4][0] + pos[5][0]) / 2, 215)
    t, _ = F.aside("one edge", at=(mid[0], 395), target=(mid[0], 222), anchor="south", bend=0, gap=10)
    o += t
    F.emit("two-comm-q", o, container="col", h=480, hmod="c", nodes=True)


# ============================================================================ two-comm-walk
def _find_walk(P, comm, steps=400):
    """A seeded walk from node 0 whose first 60 steps cross once or more and whose mean run
    length (steps per visit to a community) is within 14 to 30."""
    for seed in range(1, 400):
        path = G.walk(P, 0, steps, np.random.default_rng(seed))
        c = comm[path]
        runs = 1 + int((c[1:] != c[:-1]).sum())
        cross = np.flatnonzero(c[:61] != c[0])
        if 19 <= steps / runs <= 23 and len(cross) and 12 <= cross[0] <= 40 and (c[:61] != c[0]).sum() >= 12:
            return seed, path, steps / runs
    raise AssertionError("no seed gives a walk with runs of 19-23 steps")


def f_two_comm_walk():
    comm = np.array([0] * 5 + [1] * 5)
    seed, path, mean_run = _find_walk(G.PTC, comm)
    assert 19 <= mean_run <= 23
    pos = two_clique_layout(120, 390, 215, 88)
    rng = np.random.default_rng(seed)
    jit = {i: (rng.normal(0, 5), rng.normal(0, 5)) for i in range(61)}
    pts = [(pos[n][0] + jit[i][0], pos[n][1] + jit[i][1]) for i, n in enumerate(path[:61])]
    o = ""
    inner = TWOC_EDGES
    o += edges_ink(inner, pos, color="muted", w=2.0, opacity=0.6)
    # runs of one colour along the first 60 steps (a step takes the colour of the node it leaves)
    i = 0
    while i < 60:
        j = i
        while j < 60 and comm[path[j]] == comm[path[i]]:
            j += 1
        o += F.brush(pts[i:j + 1], color=CB if comm[path[i]] else CA, w=8.0, opacity=0.95, strands=5, seed=i)
        i = j
    o += discs_ink(pos, fills={n: "white" for n in pos}, size=F.NODE)
    o += F.ring(*pos[0], size=F.NODE, color="ink", w=3.0, grow=20)
    # the time strip: 400 steps, one cell per step, merged into runs
    sx0, sx1, sy0, sy1 = 580.0, 1060.0, 160.0, 225.0
    cw = (sx1 - sx0) / 400
    c = comm[path[:400]]
    k = 0
    while k < 400:
        m = k
        while m < 400 and c[m] == c[k]:
            m += 1
        o += f"\\fill[{CB if c[k] else CA}] ({sx0 + k * cw:.2f},{sy0}) rectangle ({sx0 + m * cw:.2f},{sy1});\n"
        k = m
    o += f"\\draw[ink,line width=2.4bp] ({sx0},{sy0}) rectangle ({sx1},{sy1});\n"
    o += F.seg((sx0, sy0 - 26), (sx1 + 6, sy0 - 26), color="ink", w=3.0, arrow=ARROW, sketch=False)
    o += F.text(sx1, sy0 - 40, "time", anchor="north east")
    # the longest run gets the aside
    runs, k = [], 0
    while k < 400:
        m = k
        while m < 400 and c[m] == c[k]:
            m += 1
        runs.append((k, m))
        k = m
    a, b = max(runs, key=lambda r: r[1] - r[0])
    tx = sx0 + (a + b) / 2 * cw
    t, _ = F.aside("about 21 steps\\\\per visit", at=(min(tx, sx1 - 170), sy1 + 95),
                   target=(tx, sy1 + 5), anchor="south", bend=0)
    o += t
    F.emit("two-comm-walk", o, container="full", h=430, hmod="b", nodes=True)
    print(f"    two-comm-walk: seed {seed}, mean run {mean_run:.1f} steps, {len(runs)} runs")


# ============================================================================ clique / twoclique pairs
AXBOX = (540.0, 128.0, 1040.0, 292.0)


def _inset_axes(xmax, xticks):
    ax = F.Axes(AXBOX, (0, xmax), (0, 2), xlabel="steps", ylabel="distance", xticks=xticks,
                yticks=[0, 1, 2], xfmt=lambda v: f"{int(v)}", yfmt=lambda v: f"{int(v)}")
    o = ax.frame()
    o += F.seg(ax.P(0, G.EPS), ax.P(xmax, G.EPS), color="muted", w=2.6, dash=F.DASH)
    o += F.text(ax.X(xmax) - 6, ax.Y(G.EPS) + 8, "$\\epsilon = \\frac{1}{2}$", color="muted", anchor="south east", size=F.FONT_MATH)
    return ax, o


def _curve(ax, ts, d, color, label=None):
    o = F.polyline([ax.P(t, v) for t, v in zip(ts, d)], color=color, w=4.2)
    for t, v in zip(ts, d):
        o += F.dot(*ax.P(t, v), color=color, d=11)
    return o


def f_clique():
    pos = {k: (150 + 112 * math.cos(math.radians(90 - 36 * k)), 150 + 112 * math.sin(math.radians(90 - 36 * k)))
           for k in range(10)}
    edges = [tuple(e) for e in G.CLIQUE10.edges()]
    assert len(edges) == 45
    q = edges_ink(edges, pos, color="ink", w=1.6, opacity=0.55)
    q += discs_ink(pos)
    q += F.ring(*pos[0], size=F.NODE, color="ink", w=3.0, grow=18)
    ax, a_ = _inset_axes(4, [0, 1, 2, 3, 4])
    q += a_
    ts = list(range(0, 5))
    d = G.worst_dist(G.PC10, G.PIC10, ts)
    assert d[0] > 1.5 and d[1] <= G.EPS and G.mixing_time(G.PC10, G.PIC10, G.EPS) == G.TMIXC10 == 1
    a = q + _curve(ax, ts, d, "hot")
    a += F.seg(ax.P(1, d[1]), ax.P(1, 0), color="hot", w=2.6, dash=F.DASH)
    a += F.ring(*ax.P(1, d[1]), size=F.NODE - 12, color="hot", w=3.0, grow=10)
    F.emit_group([("clique-q", q), ("clique-a", a)], container="full", h=330, hmod="at", nodes=True)


def f_twoclique():
    pos = two_clique_layout(100, 322, 150, 64)
    q = ""
    inner = [e for e in TWOC_EDGES if e != (4, 5)]
    q += edges_ink(inner, pos, color="ink", w=2.0, opacity=0.8)
    q += F.seg(pos[4], pos[5], color="ink", w=F.HEAVY_W)
    q += discs_ink(pos, fills={n: comm_fill(n) for n in pos})
    q += F.ring(*pos[2], size=F.NODE, color="ink", w=3.0, grow=20)
    ax, a_ = _inset_axes(20, [0, 5, 10, 15, 20])
    q += a_
    ts = list(range(0, 21))
    d = G.worst_dist(G.PTC, G.PITC, ts)
    dc = G.worst_dist(G.PC10, G.PIC10, ts)
    tm = G.mixing_time(G.PTC, G.PITC, G.EPS)
    assert tm == G.TMIXTC and d[tm] <= G.EPS < d[tm - 1]
    a = q
    a += F.polyline([ax.P(t, v) for t, v in zip(ts, dc)], color="muted", w=3.6)
    a += F.text(ax.X(3) + 18, ax.Y(0.8) + 14, "10-clique", color="muted", anchor="west")
    a += F.polyline([ax.P(t, v) for t, v in zip(ts, d)], color="hot", w=4.4)
    a += F.seg(ax.P(tm, d[tm]), ax.P(tm, 0), color="hot", w=2.6, dash=F.DASH)
    a += F.ring(*ax.P(tm, d[tm]), size=F.NODE - 12, color="hot", w=3.0, grow=10)
    F.emit_group([("twoclique-q", q), ("twoclique-a", a)], container="full", h=330, hmod="at", nodes=True)


# ============================================================================ no-larger
NL_NEIGH = {"left": 7, "up": 5, "right": 9, "down": 3}        # the four neighbours of node i; i holds the largest, 9


def f_no_larger():
    """One node and its four neighbours, before and after one averaging step."""
    vals = list(NL_NEIGH.values())
    f_i = 9
    avg = sum(vals) / len(vals)
    assert f_i == max(vals) and avg == 6.0 and avg < f_i              # (7+5+9+3)/4 = 6 <= 9
    assert all(v <= f_i for v in vals)
    # a check on a real graph: one step of P never raises the maximum
    P = G.trans(G.adj(G.RULE, range(7)))
    f = np.array([1, 4, 9, 6, 5, 5, 7], dtype=float)
    assert (P @ f).max() <= f.max() + 1e-12
    cy, dx, dy = 160.0, 118.0, 100.0

    def star(cx, centre):
        pos = {"i": (cx, cy), "left": (cx - dx, cy), "right": (cx + dx, cy), "up": (cx, cy + dy), "down": (cx, cy - dy)}
        o = "".join(F.seg(pos["i"], pos[k], color="ink", w=2.8) for k in NL_NEIGH)
        o += F.disc(*pos["i"], str(centre), fill="white")
        for k, v in NL_NEIGH.items():
            o += F.disc(*pos[k], str(v), fill="white")
        o += F.ring(*pos["i"], size=F.NODE, color="hot", w=3.4, grow=20)
        o += F.text(cx + 40, cy + 40, "$i$", anchor="west", size=F.FONT_MATH, color="hot")
        return o

    o = star(190.0, 9) + star(890.0, 6)
    o += F.seg((380, cy), (700, cy), color="muted", w=4.4, arrow=ARROW, sketch=False)
    o += F.text(540, cy + 24, "replace by the\\\\average of the\\\\neighbours", color="muted", anchor="south")
    o += F.text(540, cy - 24, "$(7+5+9+3)\\div 4 = 6$", size=F.FONT_MATH, anchor="north")
    F.emit("no-larger", o, container="full", h=330, hmod="at", nodes=True)


# ============================================================================ detailed-balance
def f_detailed_balance():
    # 5 edges in all: i has 3 (one to j, two to others), j has 2 (one to i, one to another); 2m = 10
    k_i, k_j, two_m = 3, 2, 10
    pi_i, pi_j = k_i / two_m, k_j / two_m
    assert math.isclose(pi_i / k_i, pi_j / k_j) and math.isclose(pi_i / k_i, 0.1)
    xi, xj, y = 270.0, 810.0, 168.0
    o = ""
    for dy in (62, -62):
        o += F.seg((xi, y), (xi - 150, y + dy), color="muted", w=2.8)
    o += F.seg((xj, y), (xj + 160, y), color="muted", w=2.8)
    o += F.disc(xi - 150, y + 62, "", fill="pale") + F.disc(xi - 150, y - 62, "", fill="pale")
    o += F.disc(xj + 160, y, "", fill="pale")
    o += F.disc(xi, y, "i", fill="white") + F.disc(xj, y, "j", fill="white")
    o += (f"\\draw[ink,line width=3.4bp,{ARROW}] ({xi + 30},{y + 14}) to[bend left=14] ({xj - 30},{y + 14});\n")
    o += (f"\\draw[ink,line width=3.4bp,{ARROW}] ({xj - 30},{y - 14}) to[bend left=14] ({xi + 30},{y - 14});\n")
    xm = (xi + xj) / 2
    o += F.text(xm, y + 54, "$\\pi_i\\cdot\\frac{1}{k_i}=0.3\\cdot\\frac{1}{3}=0.1$", size=F.FONT_MATH, anchor="south")
    o += F.text(xm, y + 104, "at $i$, then a step to $j$", color="muted", size=F.FONT_MATH, anchor="south")
    o += F.text(xm, y - 54, "$\\pi_j\\cdot\\frac{1}{k_j}=0.2\\cdot\\frac{1}{2}=0.1$", size=F.FONT_MATH, anchor="north")
    o += F.text(xm, y - 104, "at $j$, then a step to $i$", color="muted", size=F.FONT_MATH, anchor="north")
    o += F.text(xm, y, "$=$", size=F.FONT_MATH + 14, color="hot", anchor="center")
    F.emit("detailed-balance", o, container="full", h=340, hmod="at", nodes=True)


# ============================================================================ tasks-diamond
def f_tasks_diamond():
    xy = G.DIAMOND_XY
    pos = {n: (40 + 62 * x, 130 + 66 * y) for n, (x, y) in xy.items()}
    edges = [tuple(e) for e in G.DIAMOND.edges()]
    F.assert_planar_drawing(edges, pos, "tasks-diamond")
    o = edges_ink(edges, pos, color="ink", w=2.8)
    o += discs_ink(pos, labels={n: n for n in pos})
    o += F.text(130, 78, "Part 2", anchor="south")
    bx0, by0, bx1, by1 = 312, 110, 527, 330
    o += f"\\draw[muted,line width=3bp,dash pattern=on 12bp off 8bp] ({bx0},{by0}) rectangle ({bx1},{by1});\n"
    o += F.text((bx0 + bx1) / 2, (by0 + by1) / 2 + 6, "QR code\\\\Part 3\\\\notebook", color="muted", anchor="center")
    F.emit("tasks-diamond", o, container="col", h=360, hmod="c", nodes=True)


FIGURES = [
    ("pearson-walker", f_pearson_walker), ("polya", f_polya), ("fields", f_fields),
    ("walk-rule", f_walk_rule), ("two-comm-q", f_two_comm_q), ("two-comm-walk", f_two_comm_walk),
    ("clique", f_clique), ("twoclique", f_twoclique), ("no-larger", f_no_larger),
    ("detailed-balance", f_detailed_balance), ("tasks-diamond", f_tasks_diamond),
]

if __name__ == "__main__":
    F.run(FIGURES)
