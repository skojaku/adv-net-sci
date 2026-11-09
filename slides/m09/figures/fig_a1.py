"""Group a1: Fourier / convolution on images, part 1.

    cd slides/m09 && uv run --quiet --with numpy --with scipy --with networkx --with pillow \
        --with scikit-image python figures/fig_a1.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np                                   # noqa: E402
from PIL import Image                                # noqa: E402
from scipy.ndimage import gaussian_filter            # noqa: E402
from scipy.signal import convolve2d                  # noqa: E402

from common import *                                 # noqa: E402,F403

HLINK = "#9B6BC9"
STEPS = ["#F4E6FF", "#D9B8F5", "#B88AE0", "#9B6BC9"]


# ---------------------------------------------------------------- helpers
def txt(at, s, anchor="center", size="fssmall", extra=""):
    ex = f", {extra}" if extra else ""
    return rf"\node[inner sep=1\px, anchor={anchor}, font=\{size}{ex}] at {P(*at)} {{{s}}};"


def rgb(v):
    v = int(v)
    return f"{{rgb,255:red,{v};green,{v};blue,{v}}}"


def hexfill(h):
    return f"{{rgb,255:red,{int(h[1:3],16)};green,{int(h[3:5],16)};blue,{int(h[5:7],16)}}}"


def fmt(v):
    return f"${int(v)}$"


def rect(x0, y0, x1, y1, fill="white", lw="1.5\\px", draw="ink"):
    f = f"fill={fill}, " if fill else ""
    if draw and draw.startswith("#"):
        draw = hexfill(draw)
    if fill in ("hl",):
        pass
    d = f"draw={draw}, line width={lw}" if draw else "draw=none"
    return rf"\path[{f}{d}] {P(x0, y0)} rectangle {P(x1, y1)};"


def grid(x0, ytop, vals, cw, ch=None, fills=None, textcol=None, lw="1.5\\px", outer="2\\px"):
    """Matrix of numbers; (x0, ytop) is the top-left corner. Returns (tikz, (xl, yb, xr, yt))."""
    ch = ch or cw
    n, m = vals.shape
    out = []
    for i in range(n):
        for j in range(m):
            xa, ya = x0 + j * cw, ytop - (i + 1) * ch
            fl = hexfill(fills[i][j]) if fills and fills[i][j] else "white"
            out.append(rect(xa, ya, xa + cw, ya + ch, fl, lw))
    for i in range(n):
        for j in range(m):
            xa, ya = x0 + j * cw, ytop - (i + 1) * ch
            col = (textcol[i][j] if textcol else "ink")
            out.append(txt((xa + cw / 2, ya + ch / 2), fmt(vals[i, j]), extra=f"text={col}"))
    out.append(rect(x0, ytop - n * ch, x0 + m * cw, ytop, None, outer))
    return "\n".join(out), (x0, ytop - n * ch, x0 + m * cw, ytop)


def bracket(x0, y0, x1, y1, gap=8, arm=12, lw="2\\px"):
    """Square brackets around the box (x0,y0)-(x1,y1)."""
    xl, xr = x0 - gap, x1 + gap
    return "\n".join([
        rf"\draw[line width={lw}] {P(xl + arm, y1)} -- {P(xl, y1)} -- {P(xl, y0)} -- {P(xl + arm, y0)};",
        rf"\draw[line width={lw}] {P(xr - arm, y1)} -- {P(xr, y1)} -- {P(xr, y0)} -- {P(xr - arm, y0)};",
    ])


def resized(arr, size, name):
    im = Image.fromarray(np.clip(arr, 0, 255).astype("uint8")).resize((size * 2, size * 2), Image.LANCZOS)
    p = IMG / f"{name}.png"
    im.save(p)
    return p


def norm_abs(o):
    a = np.abs(o)
    return 255 * np.clip(a / np.percentile(a, 96), 0, 1)


SOBEL_X = np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], float)
SOBEL_Y = SOBEL_X.T
BLUR = np.ones((3, 3)) / 9


def edge_out(img, k):
    return convolve2d(img.astype(float), k, mode="same", boundary="symm")


# ---------------------------------------------------------------- a01
def a01_pixels():
    img = camera()
    r0, c0 = 150, 236                       # 4 x 4 patch next to the nose
    patch = img[r0:r0 + 4, c0:c0 + 4].astype(int)
    S = 210
    p = resized(img, S, "a01_photo")
    cell_w, cell_h = 100, 66
    mh = 4 * cell_h
    cy = 40 + 52 + mh / 2                   # room for the label under the matrix
    parts = [picture(p, (S / 2, cy), S, S)]
    px = (c0 + 2) / 512 * S
    py = cy + S / 2 - (r0 + 2) / 512 * S
    parts.append(rect(px - 9, py - 9, px + 9, py + 9, None, "3.5\\px", HLINK))
    mx0 = S + 62
    my_top = cy + mh / 2
    tc = [["white" if patch[i, j] < 110 else "ink" for j in range(4)] for i in range(4)]
    xl, yb, xr, yt = mx0, my_top - mh, mx0 + 4 * cell_w, my_top
    for i in range(4):
        for j in range(4):
            xa, ya = mx0 + j * cell_w, my_top - (i + 1) * cell_h
            parts.append(rect(xa, ya, xa + cell_w, ya + cell_h, rgb(patch[i, j]), "1.5\\px"))
    for i in range(4):
        for j in range(4):
            xa, ya = mx0 + j * cell_w, my_top - (i + 1) * cell_h
            parts.append(txt((xa + cell_w / 2, ya + cell_h / 2), f"${patch[i, j]}$", extra=f"text={tc[i][j]}"))
    parts.append(bracket(xl, yb, xr, yt, gap=12, arm=9))
    parts.append(rf"\draw[arr] {P(px + 14, py)} -- {P(xl - 30, (yb + yt) / 2 + 40)};")
    parts.append(txt((S / 2, cy - S / 2 - 34), "image"))
    parts.append(txt(((xl + xr) / 2, yb - 34), r"4 $\times$ 4 pixels"))
    B("a01_pixels", *parts)


# ---------------------------------------------------------------- a02
def a02_conv_window():
    K = np.array([[1, 0, -1]] * 3, float)
    seed_ok = None
    for seed in range(2000):
        rs = np.random.RandomState(seed)
        f = gaussian_filter(rs.rand(6, 6), 1.0, mode="nearest")
        f = np.round(9 * (f - f.min()) / (f.max() - f.min())).astype(int)
        out = convolve2d(f, K, mode="valid").astype(int)
        if np.abs(out).max() <= 9 and abs(out[1, 2]) >= 3 and len(np.unique(out)) >= 8 and np.unique(f).size >= 6:
            seed_ok = seed
            break
    assert seed_ok is not None
    print("a02 seed", seed_ok)
    cw, cwk, ch = 66, 92, 70
    cyc = 300
    x_in = 0
    xk = x_in + 6 * cw + 56
    xo = xk + 3 * cwk + 56
    ytop = lambda n: cyc + n * ch / 2
    parts = []
    wr, wc = 1, 2
    fills = [[("#F4E6FF" if (wr <= i < wr + 3 and wc <= j < wc + 3) else None) for j in range(6)] for i in range(6)]
    g, (xl, yb, xr, yt) = grid(x_in, ytop(6), f, cw, ch, fills=fills)
    parts.append(g)
    parts.append(rect(x_in + wc * cw, yt - (wr + 3) * ch, x_in + (wc + 3) * cw, yt - wr * ch, None, "4\\px", "ink"))
    parts.append(txt(((xl + xr) / 2, yb - 36), "input"))
    g, (kl, kb, kr, kt) = grid(xk, ytop(3), K, cwk, ch)
    parts.append(g)
    parts.append(txt(((kl + kr) / 2, kb - 36), "kernel"))
    ofills = [["#F4E6FF" if (i, j) == (wr, wc) else None for j in range(4)] for i in range(4)]
    g, (ol, ob, orr, ot) = grid(xo, ytop(4), out, cwk, ch, fills=ofills)
    parts.append(g)
    parts.append(rect(xo + wc * cwk, ot - (wr + 1) * ch, xo + (wc + 1) * cwk, ot - wr * ch, None, "4\\px", "ink"))
    parts.append(txt(((ol + orr) / 2, ob - 36), "output"))
    parts.append(txt(((xr + kl) / 2, cyc), r"$\ast$", size="fslarge"))
    parts.append(txt(((kr + ol) / 2, cyc), r"$=$", size="fslarge"))
    B("a02_conv_window", *parts)


# ---------------------------------------------------------------- a03
def a03_kernel_outputs():
    img = camera()
    S_in, S_out = 190, 170
    pin_ = resized(img, S_in, "a03_photo")
    rows = [("vertical edge", SOBEL_X, "a03_vedge"), ("horizontal edge", SOBEL_Y, "a03_hedge"), ("blur", BLUR, "a03_blur")]
    pitch = 190
    H = 3 * pitch
    cwk, chk = 78, 58
    xt = S_in + 14                                   # trunk x
    xl = xt + 16                                     # label left
    xs = xl + 374                                    # "*" centre
    xk = xs + 104                                    # kernel left
    xa0 = xk + 3 * cwk + 8
    xo = xa0 + 46
    ys = [H - pitch / 2 - i * pitch for i in range(3)]
    parts = [picture(pin_, (S_in / 2, H / 2), S_in, S_in)]
    parts.append(rf"\draw[line width=2\px] {P(S_in, H / 2)} -- {P(xt, H / 2)};")
    parts.append(rf"\draw[line width=2\px] {P(xt, ys[0])} -- {P(xt, ys[2])};")
    for (name, k, fn), y in zip(rows, ys):
        o = edge_out(img, k)
        o = np.clip(o, 0, 255) if name == "blur" else norm_abs(o)
        po = resized(o, S_out, fn)
        parts.append(rf"\draw[line width=2\px] {P(xt, y)} -- {P(xl - 4, y)};")
        parts.append(txt((xl, y), name, anchor="west"))
        parts.append(txt((xs, y), r"$\ast$", size="fslarge"))
        if name == "blur":
            vals = np.ones((3, 3), int)
            parts.append(txt((xk - 8, y), "1/9", anchor="east"))
        else:
            vals = k.astype(int)
        g, _ = grid(xk, y + 1.5 * chk, vals, cwk, chk)
        parts.append(g)
        parts.append(rf"\draw[arr] {P(xa0, y)} -- {P(xo - 6, y)};")
        parts.append(picture(po, (xo + S_out / 2, y), S_out, S_out))
    B("a03_kernel_outputs", *parts)


# ---------------------------------------------------------------- a04
def a04_playground():
    img = camera()
    k = np.array([[-1, -1, -1], [-1, 8, -1], [-1, -1, -1]], float)
    S = 230
    pin_ = resized(img, S, "a04_photo")
    po = resized(norm_abs(edge_out(img, k)), S, "a04_out")
    cy = 130
    cw, ch = 92, 62
    pad = 14
    gap_arrow = 110
    xi = 0
    xk = xi + S + gap_arrow + pad
    xo = xk + 3 * cw + pad + gap_arrow
    parts = [picture(pin_, (xi + S / 2, cy), S, S)]
    kl, kr = xk, xk + 3 * cw
    parts.append(rect(kl - pad, cy - 1.5 * ch - pad, kr + pad, cy + 1.5 * ch + pad, "hl", "2\\px", HLINK))
    g, _ = grid(xk, cy + 1.5 * ch, k.astype(int), cw, ch)
    parts.append(g)
    parts.append(picture(po, (xo + S / 2, cy), S, S))
    parts.append(rf"\draw[arr] {P(xi + S + 10, cy)} -- {P(kl - pad - 10, cy)};")
    parts.append(rf"\draw[arr] {P(kr + pad + 10, cy)} -- {P(xo - 10, cy)};")
    ly = cy + S / 2 + 36
    parts.append(txt((xi + S / 2, ly), "Image"))
    parts.append(txt(((kl + kr) / 2, ly), "Kernel"))
    parts.append(txt((xo + S / 2, ly), "Output"))
    parts.append(txt((xo + S, ly + 84), "interactive", anchor="east", extra="draw=ink, line width=2\\px, fill=white, inner xsep=8\\px, inner ysep=4\\px"))
    B("a04_playground", *parts)


# ---------------------------------------------------------------- a05
def a05_receptive_planes():
    c, sk, dep = 60, 0.55, 0.36
    cx = 330
    gap = 100
    sizes = [7, 5, 3]                         # bottom, middle, top
    hh = [n * c * dep / 2 for n in sizes]
    cy = [hh[0] + 2]
    cy.append(cy[0] + hh[0] + gap + hh[1])
    cy.append(cy[1] + hh[1] + gap + hh[2])

    def pt(k, u, v):
        n = sizes[k]
        up, vp = u - n / 2, v - n / 2
        return (cx + (up + sk * vp) * c, cy[k] + dep * vp * c)

    def cell(k, i, j, fill):
        a, b, cc, d = pt(k, j, i), pt(k, j + 1, i), pt(k, j + 1, i + 1), pt(k, j, i + 1)
        f = f"fill={hexfill(fill)}, " if fill else "fill=white, "
        return rf"\path[{f}draw=ink, line width=1.5\px] {P(*a)} -- {P(*b)} -- {P(*cc)} -- {P(*d)} -- cycle;"

    shade = {0: (1, 5, STEPS[1]), 1: (1, 3, STEPS[2]), 2: (1, 1, STEPS[3])}   # (first, last, colour)
    parts = []
    names = ["input", "layer 1", "layer 2"]
    for k in range(3):
        n = sizes[k]
        lo, hi, col = shade[k]
        for i in range(n):
            for j in range(n):
                inside = lo <= i < hi + (0 if k == 2 else 0) and lo <= j < hi
                parts.append(cell(k, i, j, col if lo <= i <= hi and lo <= j <= hi else None))
        # outer outline
        q = [pt(k, 0, 0), pt(k, n, 0), pt(k, n, n), pt(k, 0, n)]
        parts.append(rf"\draw[line width=2.5\px] " + " -- ".join(P(*z) for z in q) + " -- cycle;")
        lx, ly = pt(k, 0, n / 2)
        parts.append(txt((lx - 20, ly), names[k], anchor="east"))
        if k > 0:
            pass
    # links: the patch of plane k+1 -> patch of plane k
    def corners(k):
        lo, hi, _ = shade[k]
        return [pt(k, lo, lo), pt(k, hi + 1, lo), pt(k, hi + 1, hi + 1), pt(k, lo, hi + 1)]
    for k in (1, 0):
        up = corners(k + 1)
        dn = corners(k)
        for a, b in zip(up, dn):
            parts.append(rf"\draw[line width=1.5\px] {P(*a)} -- {P(*b)};")
    B("a05_receptive_planes", *parts)


# ---------------------------------------------------------------- a06
def a06_waves_1d():
    t = np.linspace(0, 1, 301)
    comps = [(1.0, 1, "$c_1$"), (0.6, 3, "$c_3$"), (0.3, 7, "$c_7$")]
    f = sum(c * np.sin(2 * np.pi * k * t) for c, k, _ in comps)
    unit = 50
    x0, x1 = 136, 500
    gap = 66
    halves = [np.abs(f).max() * unit] + [max(c * unit, 30) for c, _, _ in comps]
    cys = []
    top = sum(halves) * 2 + gap * 3 + 3
    y = top
    for h in halves:
        cys.append(y - h)
        y -= 2 * h + gap

    def curve(y, vals, cw=2):
        pts = " -- ".join(P(x0 + (x1 - x0) * tt, y + unit * v) for tt, v in zip(t, vals))
        return rf"\draw[line width={cw}\px, line join=round] {pts};"

    parts = []
    parts.append(rf"\draw[-{{Stealth[length=9bp, width=7bp]}}, line width=1\px] {P(x0 - 6, cys[0])} -- {P(x1 + 16, cys[0])};")
    parts.append(txt((x1 + 20, cys[0]), "$t$", anchor="west"))
    parts.append(curve(cys[0], f))
    parts.append(txt((56, cys[0]), "$f(t)$"))
    ops = ["$=$", "$+$", "$+$"]
    for i, (c, k, lab) in enumerate(comps):
        y = cys[i + 1]
        parts.append(curve(y, c * np.sin(2 * np.pi * k * t)))
        parts.append(txt((56, y), lab))
        parts.append(txt((56, (y + halves[i + 1] + cys[i] - halves[i]) / 2), ops[i]))
    B("a06_waves_1d", *parts)


# ---------------------------------------------------------------- a13
def a13_image_row():
    img = camera()
    S = 300
    row = 330
    p = resized(img, S, "a13_photo")
    ytop_img = 600
    cy = ytop_img - S / 2
    parts = [picture(p, (S / 2, cy), S, S)]
    yb = ytop_img - (row + 0.5) / 512 * S
    parts.append(rect(0, yb - 5, S, yb + 5, "hl", "1.5\\px", HLINK))
    parts.append(txt((S + 24, ytop_img - 40), "image", anchor="west"))
    parts.append(rf"\draw[arr] {P(S + 70, yb)} -- {P(S + 8, yb)};")
    parts.append(txt((S + 78, yb), "one row", anchor="west"))
    # arrow down and the curve
    parts.append(rf"\draw[arr] {P(S / 2, ytop_img - S - 6)} -- {P(S / 2, ytop_img - S - 56)};")
    vals = img[row].astype(float)
    n = 200
    r = np.interp(np.linspace(0, 511, n), np.arange(512), vals)
    x0, x1 = 130, 650
    y0 = 64
    h = 150
    pts = " -- ".join(P(x0 + (x1 - x0) * i / (n - 1), y0 + h * v / 255) for i, v in enumerate(r))
    parts.append(rf"\draw[-{{Stealth[length=9bp, width=7bp]}}, line width=1\px] {P(x0 - 6, y0 - 6)} -- {P(x1 + 16, y0 - 6)};")
    parts.append(txt((x1 + 22, y0 - 6), "$t$", anchor="west"))
    parts.append(rf"\draw[line width=2\px, line join=round] {pts};")
    parts.append(txt((56, y0 + h * 0.5), "$f(t)$"))
    B("a13_image_row", *parts)


if __name__ == "__main__":
    a01_pixels()
    a02_conv_window()
    a03_kernel_outputs()
    a04_playground()
    a06_waves_1d()
    a13_image_row()
