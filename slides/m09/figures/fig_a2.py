"""Group a2: Fourier, part 2.  a07 .. a12.

Run:  cd slides/m09 && uv run --quiet --with numpy --with scipy --with networkx --with pillow \
          --with scikit-image python figures/fig_a2.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import *  # noqa: E402,F401,F403

import numpy as np  # noqa: E402

LW = r"line width=2\px"


# ---------------------------------------------------------------------------------- helpers
def poly(xs, ys, style: str = "ink") -> str:
    pts = " -- ".join(P(x, y) for x, y in zip(xs, ys))
    return rf"\draw[{style}, {LW}, line join=round] {pts};"


def curve(vals, ox, oy, w, sy, style: str = "ink") -> str:
    """Polyline of `vals` spread over width w from (ox, oy) (oy = the zero line)."""
    n = len(vals)
    xs = [ox + w * i / (n - 1) for i in range(n)]
    return poly(xs, [oy + sy * v for v in vals], style)


def dots(vals, ox, oy, pitch, sy, r=8, style="ink") -> str:
    """One dot per value on the baseline y = oy; the baseline itself is drawn by the caller."""
    return "\n".join(rf"\fill[{style}] {P(ox + pitch * i, oy + sy * v)} circle ({r}\px);" for i, v in enumerate(vals))


def baseline(x0, x1, y, arrow_end=False) -> str:
    tip = ", -{Stealth[length=8bp, width=6bp]}" if arrow_end else ""
    return rf"\draw[line width=1.5\px{tip}] {P(x0, y)} -- {P(x1, y)};"


def txt(at, text, anchor="center", extra="") -> str:
    return label(at, text, anchor=anchor, extra=extra)


def arrow_down(x, y0, y1) -> str:
    return rf"\draw[arr] {P(x, y0)} -- {P(x, y1)};"


def matrix(cx, cy, vals, cw=62, ch=52) -> str:
    """A bracketed matrix of text entries centred at (cx, cy)."""
    r, c = len(vals), len(vals[0])
    w, h = c * cw, r * ch
    out = []
    for i in range(r):
        for j in range(c):
            x = cx - w / 2 + cw * (j + .5)
            y = cy + h / 2 - ch * (i + .5)
            out.append(rf"\node[inner sep=0pt, font=\fssmall] at {P(x, y)} {{${vals[i][j]}$}};")
    x0, x1, yt, yb, k = cx - w / 2 - 4, cx + w / 2 + 4, cy + h / 2 + 2, cy - h / 2 - 2, 12
    out.append(rf"\draw[{LW}] {P(x0 + k, yt)} -- {P(x0, yt)} -- {P(x0, yb)} -- {P(x0 + k, yb)};")
    out.append(rf"\draw[{LW}] {P(x1 - k, yt)} -- {P(x1, yt)} -- {P(x1, yb)} -- {P(x1 - k, yb)};")
    return "\n".join(out)


def spectrum_log(img):
    """Centred log-magnitude spectrum of a 2D array, as float in [0, 1]."""
    F = np.fft.fftshift(np.fft.fft2(img))
    L = np.log1p(np.abs(F))
    return F, L


def to_u8(a, lo=None, hi=None):
    lo = a.min() if lo is None else lo
    hi = a.max() if hi is None else hi
    return np.clip((a - lo) / (hi - lo + 1e-12), 0, 1) * 255


# --------------------------------------------------------------------------- the 1D signals
N = 64
T = np.arange(N) / N


def signal(t):
    return np.sin(2 * np.pi * t) + 0.6 * np.sin(6 * np.pi * t) + 0.3 * np.sin(14 * np.pi * t)


def amp_spectrum(x):
    """|c_k|, k = 0..N/2: amplitude of the cosine/sine pair at k cycles per window."""
    X = np.fft.rfft(x) / len(x)
    a = np.abs(X)
    a[1:] *= 2
    return a


# ------------------------------------------------------------------------------------- a07
def a07():
    W = 700
    tt = np.linspace(0, 1, 400)
    f = signal(tt)
    c = amp_spectrum(signal(T))[:9]
    parts = []
    # top panel
    parts.append(txt((0, 518), "time domain", "west"))
    cy, sy = 392, 50
    parts.append(txt((0, cy), r"$f(t)$", "west"))
    parts.append(baseline(88, 668, cy, arrow_end=True))
    parts.append(txt((690, cy - 28), r"$t$"))
    parts.append(curve(f, 98, cy, 540, sy))
    # bottom panel
    parts.append(txt((0, 268), "frequency domain", "west"))
    base, ox, pitch = 120, 96, 68
    band_x = ox + pitch
    parts.append(rf"\fill[hl] {P(band_x - 30, base - 18)} rectangle {P(band_x + 30, base + 118)};")
    parts.append(baseline(ox - 40, ox + pitch * 8 + 40, base))
    parts.append(dots(c, ox, base, pitch, 100, r=8))
    parts.append(txt((0, base + 56), r"$|c_k|$", "west"))
    for k in range(9):
        parts.append(txt((ox + pitch * k, base - 42), str(k)))
    parts.append(txt((ox - 40, 40), "slow", "west"))
    parts.append(txt((ox + pitch * 8 + 40, 40), "fast", "east"))
    parts.append(rf"\draw[arr] {P(ox + 64, 40)} -- {P(ox + pitch * 8 - 40, 40)};")
    B("a07_time_freq", *parts)


# ------------------------------------------------------------------------------------- a08
def a08():
    rng = np.random.default_rng(1)
    f = signal(T) + 0.25 * rng.standard_normal(N)
    L = 19
    h = L // 2
    gs = np.exp(-0.5 * (np.arange(-h, h + 1) / 3.0) ** 2)
    gs /= gs.sum()
    full = np.convolve(f, gs)
    fg = np.zeros(N)
    for i, v in enumerate(full):                      # circular wrap, so the DFT identity is exact
        fg[(i - h) % N] += v
    g64 = np.zeros(N)
    for i, v in enumerate(gs):
        g64[(i - h) % N] += v
    assert np.allclose(np.fft.fft(fg), np.fft.fft(f) * np.fft.fft(g64))
    K = 13
    sp = [amp_spectrum(f)[:K], np.abs(np.fft.rfft(g64))[:K], amp_spectrum(fg)[:K]]   # |g^| = |DFT g|, g sums to 1
    assert np.allclose(sp[2], sp[0] * sp[1])

    pw, gap = 146, 50
    x0 = 124
    xs = [x0 + i * (pw + gap) for i in range(3)]          # panel left edges
    ytop, ybot = 520, 112                                  # centre of the curve panel / baseline of dot panel
    parts = []
    # row labels
    parts.append(txt((0, ytop), "spatial", "west"))
    parts.append(txt((0, ybot + 45), "spectral", "west"))
    # spatial row
    sy_f, sy_g = 32, 190
    gdisp = np.roll(g64, N // 2)
    series = [(f, sy_f), (gdisp, sy_g), (fg, sy_f)]
    names = [r"$f$", r"$g$", r"$f * g$"]
    for i, (v, sy) in enumerate(series):
        if i == 1:
            parts.append(curve(v, xs[i], ytop - 50, pw, sy))
            parts.append(baseline(xs[i], xs[i] + pw, ytop - 50))
        else:
            parts.append(curve(v, xs[i], ytop, pw, sy))
            parts.append(baseline(xs[i], xs[i] + pw, ytop, arrow_end=False)
                         .replace("line width=1.5", "line width=1.0").replace("ink", "ink"))
        parts.append(txt((xs[i] + pw / 2, ytop - 90), names[i]))
    # spectral row
    hat = [r"$\hat f$", r"$\hat g$", r"$\widehat{f * g}$"]
    pitch = (pw - 12) / (K - 1)
    for i in range(3):
        parts.append(baseline(xs[i], xs[i] + pw, ybot))
        parts.append(dots(sp[i], xs[i] + 6, ybot, pitch, 105, r=4.5))
        parts.append(txt((xs[i] + pw / 2, ybot - 38), hat[i]))
    # operators
    for i, (o1, o2) in enumerate([(r"$*$", r"$\times$"), (r"$=$", r"$=$")]):
        xm = xs[i] + pw + gap / 2
        parts.append(txt((xm, ytop - 20), o1))
        parts.append(txt((xm, ybot + 45), o2))
    # Fourier transform arrows
    ya, yb = ytop - 120, ybot + 135
    ym = (ya + yb) / 2
    for i in range(3):
        xm = xs[i] + pw / 2
        if i == 1:
            parts.append(rf"\draw[arr] {P(xm, ya)} -- {P(xm, yb)};")
        else:
            parts.append(rf"\draw[arr] {P(xm, ya)} -- {P(xm, yb)};")
    parts.append(rf"\node[fill=white, inner xsep=8\px, inner ysep=2\px, font=\fssmall] at {P(xs[1] + pw / 2, ym)} {{Fourier transform}};")
    B("a08_conv_theorem", *parts)


# ------------------------------------------------------------------------------------- a09
def a09():
    S = 250
    u, v = 3, 2
    n = 2 * S
    x = (np.arange(n) + .5) / n
    X, Y = np.meshgrid(x, x[::-1])                      # row 0 is the top of the image = largest y
    img = np.cos(2 * np.pi * (u * X + v * Y))
    p1 = save_png(to_u8(img, -1, 1), "a09_stripes")
    cy = 150
    parts = [picture(p1, (S / 2, cy), S, S, interpolate=True)]
    cx = S + 34 + 150                                     # plane centre; axes run to +-150 (u, v in [-5, 5])
    px_u = 30
    parts.append(rf"\draw[arr, line width=1.5\px] {P(cx - 150, cy)} -- {P(cx + 166, cy)};")
    parts.append(rf"\draw[arr, line width=1.5\px] {P(cx, cy - 150)} -- {P(cx, cy + 166)};")
    parts.append(txt((cx + 174, cy), r"$u$", "west"))
    parts.append(txt((cx + 14, cy + 168), r"$v$", "west"))
    dx, dy = cx + u * px_u, cy + v * px_u
    parts.append(rf"\draw[{LW}] {P(cx, cy)} -- {P(dx, dy)};")
    parts.append(rf"\fill[hl, draw=ink, {LW}] {P(dx, dy)} circle (9\px);")
    ang = np.degrees(np.arctan2(dy - cy, dx - cx))        # direction: angle of the line, an arc from the u axis
    r_arc = 60
    parts.append(rf"\draw[line width=1.5\px] {P(cx + r_arc, cy)} arc[start angle=0, end angle={ang:.2f}, radius={r_arc * .75:.2f}bp];")
    am = np.radians(ang / 2)
    parts.append(txt((cx + 14, cy - 100), "direction", "west"))
    parts.append(rf"\draw[line width=1.4\px] {P(cx + 66, cy - 78)} -- {P(cx + r_arc * np.cos(am), cy + r_arc * np.sin(am) - 2)};")
    mx, my = cx + 0.78 * (dx - cx), cy + 0.78 * (dy - cy)   # frequency: the length of the line
    parts.append(txt((cx + 14, cy + 112), "frequency", "west"))
    parts.append(rf"\draw[line width=1.4\px] {P(mx, cy + 88)} -- {P(mx, my + 2)};")
    parts.append(txt((S / 2, cy + S / 2 + 28), "image"))
    parts.append(rf"\draw[arr, dashed, line width=1.5\px] {P(cx - 150 + 4, cy + 40)} -- {P(S + 8, cy + 40)};")
    B("a09_wave_2d", *parts)


# ------------------------------------------------------------------------------------ a10
def a10():
    S = 268
    img = camera().astype(float)
    F, Lg = spectrum_log(img)
    p_img = save_png(img, "a10_photo")
    p_sp = save_png(to_u8(Lg, np.percentile(Lg, 3), np.percentile(Lg, 99.95)), "a10_spectrum")
    gap = 72
    cy = 170
    parts = [picture(p_img, (S / 2, cy), S, S, interpolate=True),
             picture(p_sp, (S + gap + S / 2, cy), S, S, interpolate=True)]
    cx = S + gap + S / 2
    parts.append(txt((S / 2, cy - S / 2 - 30), r"image $X$"))
    parts.append(txt((cx, cy - S / 2 - 30), r"spectrum $\hat X$"))
    top = cy + S / 2
    ly = top + 62
    # leader lines with a white halo, then rings
    for (tx, ty, ex, ey) in [(cx - 24, ly - 22, cx, cy), (cx + S / 2 + 6, ly - 22, cx + S / 2, cy + S / 2)]:
        parts.append(rf"\draw[white, line width=4\px] {P(tx, ty)} -- {P(ex, ey)};")
        parts.append(rf"\draw[ink, line width=2\px] {P(tx, ty)} -- {P(ex, ey)};")
    parts.append(rf"\fill[hl, draw=ink, {LW}] {P(cx, cy)} circle (8\px);")
    parts.append(rf"\fill[hl, draw=ink, {LW}] {P(cx + S / 2, cy + S / 2)} circle (8\px);")
    parts.append(txt((cx - 24, ly), "low"))
    parts.append(txt((cx + S / 2 - 18, ly), "high"))
    parts.append(rf"\draw[arr, dashed, line width=1.5\px] {P(S + 10, cy)} -- {P(S + gap - 10, cy)};")
    parts.append(txt((S + gap / 2, cy + 28), r"$\mathcal{F}$"))
    B("a10_fft_image", *parts)


# ------------------------------------------------------------------------------------ a11
def a11():
    S = 210
    img = camera().astype(float)
    n = img.shape[0]
    F, Lg = spectrum_log(img)
    lo_l, hi_l = np.percentile(Lg, 1), np.percentile(Lg, 99.8)
    yy, xx = np.mgrid[:n, :n]
    r = np.hypot(xx - n / 2, yy - n / 2)
    R = 32
    masks = {"full": np.ones_like(r), "low": (r <= R).astype(float), "high": (r > R).astype(float)}
    spec_png, rec_png = [], []
    for k, m in masks.items():
        s = np.where(m > 0, to_u8(Lg, lo_l, hi_l), 0.0)
        spec_png.append(save_png(s, f"a11_spec_{k}"))
        rec = np.abs(np.fft.ifft2(np.fft.ifftshift(F * m)))
        if k == "high":
            rec = to_u8(rec, 0, np.percentile(rec, 99.5))
        else:
            rec = to_u8(rec, 0, 255)
        rec_png.append(save_png(rec, f"a11_rec_{k}"))
    names = ["original", "keep low", "keep high"]
    x0 = 150
    pitch = (1167 - x0) / 3
    ys = 262 + S / 2 - 5
    yi = 2 + S / 2
    parts = [txt((0, ys), "spectrum", "west"), txt((0, yi), "image", "west")]
    for i in range(3):
        cx = x0 + pitch * (i + .5)
        parts.append(picture(spec_png[i], (cx, ys), S, S, interpolate=True))
        parts.append(picture(rec_png[i], (cx, yi), S, S, interpolate=True))
        parts.append(rf"\draw[arr] {P(cx, ys - S / 2 - 5)} -- {P(cx, yi + S / 2 + 5)};")
        parts.append(txt((cx, ys + S / 2 + 28), names[i]))
        parts.append(txt((cx + 18, (ys + yi) / 2 + 2), r"$\mathcal{F}^{-1}$", "west"))
    B("a11_masks", *parts)


# ------------------------------------------------------------------------------------ a12
def a12():
    S = 250
    kernels = {
        "blur": np.ones((3, 3)) / 9,
        "vertical edge": np.array([[1, 0, -1], [2, 0, -2], [1, 0, -1]], float),
        "horizontal edge": np.array([[1, 2, 1], [0, 0, 0], [-1, -2, -1]], float),
    }
    ent = {
        "blur": [["1"] * 3 for _ in range(3)],
        "vertical edge": [["1", "0", "-1"], ["2", "0", "-2"], ["1", "0", "-1"]],
        "horizontal edge": [["1", "2", "1"], ["0", "0", "0"], ["-1", "-2", "-1"]],
    }
    x0 = 260
    pitch = (1167 - x0) / 3
    ym, yi, yn = 432, 195, 30
    parts = [txt((0, ym), "kernel", "west"),
             txt((0, yi + 60), "frequency", "west"),
             txt((0, yi + 20), "response", "west"),
             rf"\node[tag, anchor=west, align=left] at {P(0, yi - 50)} {{bright =\\ passed}};"]
    for i, (name, k) in enumerate(kernels.items()):
        cx = x0 + pitch * (i + .5)
        parts.append(matrix(cx + (34 if i == 0 else 0), ym, ent[name], cw=66, ch=52))
        if i == 0:
            parts.append(txt((cx - 84, ym), r"\fslarge$\dfrac{1}{9}$"))
        H = np.abs(np.fft.fftshift(np.fft.fft2(k, s=(64, 64))))
        png = save_png(to_u8(H, 0, H.max()), f"a12_resp_{i}", scale=8, nearest=False)
        parts.append(picture(png, (cx, yi), S, S, interpolate=True))
        parts.append(txt((cx, yn), name if i else "blur"))
    B("a12_kernel_response", *parts)


if __name__ == "__main__":
    for fn in (a07, a08, a09, a10, a11, a12):
        fn()
        print(fn.__name__, "ok")
