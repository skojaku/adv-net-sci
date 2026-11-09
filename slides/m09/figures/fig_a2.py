"""Group a2: Fourier, part 2.  a07 .. a12, a10_fft_interactive, a14_wave_interactive.

Run:  cd slides/m09 && uv run --quiet --with numpy --with scipy --with networkx --with pillow \
          --with scikit-image python figures/fig_a2.py [a07 a08 ...]   (no argument = all)
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


def matrix(cx, cy, vals, cw=76, ch=60) -> str:
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



def stripes(u, v, n, phase=0.0):
    """cos(2 pi (u x + v y) + phase) on [0,1]^2, row 0 = top (y up), as float in [-1, 1]."""
    x = (np.arange(n) + .5) / n
    X, Y = np.meshgrid(x, x[::-1])
    return np.cos(2 * np.pi * (u * X + v * Y) + phase)


# ------------------------------------------------------------------------------------- a07
def a07():
    tt = np.linspace(0, 1, 400)
    f = signal(tt)
    c = amp_spectrum(signal(T))[:9]
    parts = []
    # time domain (top)
    parts.append(txt((0, 568), "time domain", "west"))
    cy, sy = 466, 46
    parts.append(txt((0, cy), r"$f(t)$", "west"))
    parts.append(baseline(112, 668, cy, arrow_end=True))
    parts.append(txt((683, cy - 32), r"$t$"))
    parts.append(curve(f, 122, cy, 530, sy))
    # frequency domain (bottom)
    parts.append(txt((0, 332), "frequency domain", "west"))
    base, ox, pitch = 138, 96, 68
    band_x = ox + pitch
    parts.append(rf"\fill[hl] {P(band_x - 30, base - 18)} rectangle {P(band_x + 30, base + 118)};")
    parts.append(baseline(ox - 40, ox + pitch * 8 + 40, base))
    parts.append(dots(c, ox, base, pitch, 100, r=8))
    parts.append(txt((0, base + 70), r"$|c_k|$", "west"))
    for k in (0, 4, 8):
        parts.append(txt((ox + pitch * k, base - 44), str(k)))
    parts.append(txt((ox - 40, 26), "slow", "west"))
    parts.append(txt((ox + pitch * 8 + 40, 26), "fast", "east"))
    parts.append(rf"\draw[arr] {P(ox + 100, 26)} -- {P(ox + pitch * 8 - 70, 26)};")
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

    pw, gap = 160, 104
    xs = [i * (pw + gap) for i in range(3)]               # panel left edges
    ytop, ybot = 478, 68                                   # curve row centre / dot row baseline
    parts = []
    parts.append(txt((0, 552), "spatial", "west"))
    parts.append(txt((0, 212), "spectral", "west"))
    sy_f, sy_g = 24, 260
    gdisp = np.roll(g64, N // 2)
    series = [(f, sy_f), (gdisp, sy_g), (fg, sy_f)]
    names = [r"$f$", r"$g$", r"$f * g$"]
    for i, (v, sy) in enumerate(series):
        y0 = ytop - 46 if i == 1 else ytop
        parts.append(curve(v, xs[i], y0, pw, sy))
        parts.append(rf"\draw[line width=1.0\px] {P(xs[i], y0)} -- {P(xs[i] + pw, y0)};")
        parts.append(txt((xs[i] + pw / 2, ytop - 84), names[i]))
    hat = [r"$\hat f$", r"$\hat g$", r"$\widehat{f * g}$"]
    pitch = (pw - 12) / (K - 1)
    for i in range(3):
        parts.append(baseline(xs[i], xs[i] + pw, ybot))
        parts.append(dots(sp[i], xs[i] + 6, ybot, pitch, 92, r=4.5))
        parts.append(txt((xs[i] + pw / 2, ybot - 48), hat[i]))
    for i, (o1, o2) in enumerate([(r"$*$", r"$\times$"), (r"$=$", r"$=$")]):
        xm = xs[i] + pw + gap / 2
        parts.append(txt((xm, ytop - 20), o1))
        parts.append(txt((xm, ybot + 45), o2))
    ya, yb = ytop - 114, 262
    ym = (ya + yb) / 2
    for i in range(3):
        xm = xs[i] + pw / 2
        parts.append(rf"\draw[arr] {P(xm, ya)} -- {P(xm, yb)};")
    xl = (xs[0] + xs[1]) / 2 + pw / 2                      # label between the first two arrows
    parts.append(rf"\node[align=center, font=\fssmall, inner sep=1\px] at {P(xl, ym)} {{Fourier\\transform}};")
    B("a08_conv_theorem", *parts)


# ------------------------------------------------------------------------------------- a09
def a09():
    S = 220
    u, v = 3, 2
    n = 2 * S
    p1 = save_png(to_u8(stripes(u, v, n), -1, 1), "a09_stripes")
    p2 = save_png(to_u8(stripes(u, v, n, np.pi), -1, 1), "a09_stripes_shift")   # half a period later
    parts = [picture(p1, (S / 2, 440), S, S, interpolate=True),
             picture(p2, (S / 2, 112), S, S, interpolate=True),
             txt((S + 26, 440), "wave", "west"),
             rf"\node[anchor=west, align=left, font=\fssmall, inner sep=1\px] at {P(S + 26, 112)} {{phase\\shift}};"]
    cx, cy, un = 458, 318, 36                              # plane centre; 36 px per unit, u and v in [-5, 5]
    parts.append(rf"\draw[arr, line width=1.5\px] {P(cx - 182, cy)} -- {P(cx + 190, cy)};")
    parts.append(rf"\draw[arr, line width=1.5\px] {P(cx, cy - 182)} -- {P(cx, cy + 190)};")
    parts.append(txt((cx + 200, cy - 2), r"$u$", "west"))
    parts.append(txt((cx + 16, cy + 200), r"$v$", "west"))
    dx, dy = cx + u * un, cy + v * un
    parts.append(rf"\draw[{LW}] {P(cx, cy)} -- {P(dx, dy)};")
    parts.append(rf"\fill[hl, draw=ink, {LW}] {P(dx, dy)} circle (9\px);")
    ang = np.degrees(np.arctan2(dy - cy, dx - cx))
    r_arc = 56
    parts.append(rf"\draw[line width=1.5\px] {P(cx + r_arc, cy)} arc[start angle=0, end angle={ang:.2f}, radius={r_arc * .75:.2f}bp];")
    parts.append(txt((cx + 92, cy - 46), "angle"))
    parts.append(rf"\draw[line width=1.4\px] {P(cx + r_arc, cy - 14)} -- {P(cx + r_arc, cy - 3)};")
    mx = cx + 0.6 * (dx - cx)
    my = cy + 0.6 * (dy - cy)
    parts.append(txt((cx + 100, cy + 134), "length"))
    parts.append(rf"\draw[line width=1.4\px] {P(mx, cy + 104)} -- {P(mx, my + 3)};")
    B("a09_wave_2d", *parts)


# ------------------------------------------------------------------------------------ a10 (old)
def a10():
    S = 268
    img = camera().astype(float)
    F, Lg = spectrum_log(img)
    p_img = save_png(img, "a10_photo")
    p_sp = save_png(to_u8(Lg, np.percentile(Lg, 3), np.percentile(Lg, 99.95)), "a10_spectrum")
    gap = 100
    cy = 170
    parts = [picture(p_img, (S / 2, cy), S, S, interpolate=True),
             picture(p_sp, (S + gap + S / 2, cy), S, S, interpolate=True)]
    cx = S + gap + S / 2
    parts.append(txt((S / 2, cy - S / 2 - 34), "image"))
    parts.append(txt((cx, cy - S / 2 - 34), "spectrum"))
    top = cy + S / 2
    ly = top + 66
    for (tx, ty, ex, ey) in [(cx - 40, ly - 30, cx, cy), (cx + S / 2 + 6, ly - 30, cx + S / 2, cy + S / 2)]:
        parts.append(rf"\draw[white, line width=4\px] {P(tx, ty)} -- {P(ex, ey)};")
        parts.append(rf"\draw[ink, line width=2\px] {P(tx, ty)} -- {P(ex, ey)};")
    parts.append(rf"\fill[hl, draw=ink, {LW}] {P(cx, cy)} circle (8\px);")
    parts.append(rf"\fill[hl, draw=ink, {LW}] {P(cx + S / 2, cy + S / 2)} circle (8\px);")
    parts.append(txt((cx - 40, ly), "low"))
    parts.append(txt((cx + S / 2 - 30, ly), "high"))
    parts.append(rf"\draw[arr, dashed, line width=1.5\px] {P(S + 10, cy)} -- {P(S + gap - 10, cy)};")
    parts.append(txt((S + gap / 2, cy + 36), r"$\mathcal{F}$"))
    B("a10_fft_image", *parts)


# ------------------------------------------------------------------------- a10_fft_interactive
def a10_interactive():
    from PIL import Image
    n, S = 128, 300
    img = np.asarray(Image.fromarray(camera()).resize((n, n), Image.LANCZOS), float)
    F = np.fft.fftshift(np.fft.fft2(img))
    Lg = np.log1p(np.abs(F))
    fx, fy = 10, -6                                        # selected point: 10 right of the centre, 6 above it
    r_sel, c_sel = n // 2 + fy, n // 2 + fx                # its row and column in the shifted spectrum
    c = F[r_sel, c_sel]
    rr, cc = np.mgrid[:n, :n]
    wave_n = np.cos(2 * np.pi * (fx * cc + fy * rr) / n + np.angle(c))      # the wave of that point
    chk = np.fft.fftshift(np.fft.fft2(wave_n))
    pk = np.unravel_index(np.argmax(np.abs(chk)), chk.shape)
    assert pk in {(r_sel, c_sel), (n - r_sel, n - c_sel)}, pk      # its spectrum peaks at the chosen point (or its mirror)
    m = 4 * n
    tt = (np.arange(m) + .5) / m * n - .5
    CC, RR = np.meshgrid(tt, tt)
    wave = np.cos(2 * np.pi * (fx * CC + fy * RR) / n + np.angle(c))
    p_img = save_png(img, "a10i_photo", scale=1)
    p_sp = save_png(to_u8(Lg, np.percentile(Lg, 2), np.percentile(Lg, 99.7)), "a10i_spectrum")
    p_w = save_png(to_u8(wave, -1, 1), "a10i_wave")
    gap = (1158 - 3 * S) / 2
    cxs = [S / 2 + i * (S + gap) for i in range(3)]
    cy = 330
    parts = [picture(p_img, (cxs[0], cy), S, S, interpolate=True),
             picture(p_sp, (cxs[1], cy), S, S, interpolate=True),
             picture(p_w, (cxs[2], cy), S, S, interpolate=True)]
    ly = cy - S / 2 - 40
    for x, t in zip(cxs, [r"image $X$", "spectrum", "wave"]):
        parts.append(txt((x, ly), t))
    # selected point as a lavender ring
    px = cxs[1] - S / 2 + (c_sel + .5) / n * S
    py = cy + S / 2 - (r_sel + .5) / n * S
    parts.append(rf"\draw[ink, line width=10\px] {P(px, py)} circle (16\px);")
    parts.append(rf"\draw[hlink, line width=6\px] {P(px, py)} circle (16\px);")
    # mouse cursor next to the ring
    k = 1.15
    cur = [(0, 0), (0, -34), (9, -26), (17, -42), (25, -38), (17, -23), (29, -23)]
    pts = " -- ".join(P(px + 12 + k * a, py - 8 + k * b) for a, b in cur) + " -- cycle"
    parts.append(rf"\filill[white, draw=ink, {LW}, line join=round] {pts};".replace(r"\filill", r"\filldraw"))
    # arrows between the panels
    for i in range(2):
        xa, xb = cxs[i] + S / 2 + 14, cxs[i + 1] - S / 2 - 14
        parts.append(rf"\draw[arr, line width=1.5\px] {P(xa, cy)} -- {P(xb, cy)};")
    parts.append(txt((cxs[0] + S / 2 + gap / 2, cy + 40), "FFT"))
    parts.append(rf"\node[tag, anchor=east] at {P(1160, cy + S / 2 + 44)} {{interactive}};")
    B("a10_fft_interactive", *parts)
    print("  selected (fx, fy) =", (fx, fy), "wave peak at", pk)


# ------------------------------------------------------------------------- a14_wave_interactive
def a14():
    S = 430
    u, v, ph = 3, 2, 0.0
    p = save_png(to_u8(stripes(u, v, S, ph), -1, 1), "a14_stripes")
    parts = [picture(p, (S / 2, S / 2 + 12), S, S, interpolate=True)]
    lx, x0, x1, vx = 470, 700, 1040, 1085
    rows = [("u", u, (u + 5) / 10, "3"), ("v", v, (v + 5) / 10, "2"), ("phase", ph, ph / (2 * np.pi), "0")]
    ys = [352, 227, 102]
    for (name, val, t, txtval), y in zip(rows, ys):
        parts.append(txt((lx, y), name, "west"))
        parts.append(rf"\draw[{LW}] {P(x0, y)} -- {P(x1, y)};")
        for xe in (x0, x1):
            parts.append(rf"\draw[{LW}] {P(xe, y - 10)} -- {P(xe, y + 10)};")
        xk = x0 + t * (x1 - x0)
        parts.append(rf"\draw[hlink, line width=6\px] {P(x0, y)} -- {P(xk, y)};")
        parts.append(rf"\fill[hl, draw=ink, {LW}] {P(xk, y)} circle (16\px);")
        parts.append(txt((vx, y), txtval, "west"))
    parts.append(rf"\node[tag, anchor=east] at {P(1160, S + 12 + 4)} {{interactive}};")
    B("a14_wave_interactive", *parts)


# ------------------------------------------------------------------------------------ a11
def a11():
    S = 225
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
    pitch = 1166 / 3
    yi = S / 2
    ys = S + 70 + S / 2
    parts = []
    for i in range(3):
        cx = pitch * (i + .5)
        parts.append(picture(spec_png[i], (cx, ys), S, S, interpolate=True))
        parts.append(picture(rec_png[i], (cx, yi), S, S, interpolate=True))
        parts.append(rf"\draw[arr] {P(cx, ys - S / 2 - 4)} -- {P(cx, yi + S / 2 + 4)};")
        parts.append(txt((cx, ys + S / 2 + 38), names[i]))
        parts.append(txt((cx + 20, (ys + yi) / 2), r"$\mathcal{F}^{-1}$", "west"))
    B("a11_masks", *parts)


# ------------------------------------------------------------------------------------ a12
def a12():
    S = 230
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
    x0 = 205
    pitch = (1158 - x0) / 3
    yn_top = 0 + 116                                       # names (two lines) hang down from here to y = 0
    yi = yn_top + 10 + S / 2
    ym = yi + S / 2 + 48 + 90
    parts = [rf"\node[tag, anchor=west, align=left] at {P(0, yi)} {{bright =\\ passed}};"]
    for i, (name, k) in enumerate(kernels.items()):
        cx = x0 + pitch * (i + .5)
        parts.append(matrix(cx + (40 if i == 0 else 0), ym, ent[name], cw=80, ch=60))
        if i == 0:
            parts.append(txt((cx - 112, ym), r"\fslarge$\dfrac{1}{9}$"))
        H = np.abs(np.fft.fftshift(np.fft.fft2(k, s=(64, 64))))
        png = save_png(to_u8(H, 0, H.max()), f"a12_resp_{i}", scale=8, nearest=False)
        parts.append(picture(png, (cx, yi), S, S, interpolate=True))
        parts.append(rf"\draw[arr] {P(cx, ym - 90 - 8)} -- {P(cx, yi + S / 2 + 6)};")
        nm = name.replace(" ", r"\\")
        parts.append(rf"\node[anchor=north, align=center, font=\fssmall, inner sep=1\px] at {P(cx, yn_top)} {{{nm}}};")
    B("a12_kernel_response", *parts)


FUNCS = {"a07": a07, "a08": a08, "a09": a09, "a10": a10, "a10_fft_interactive": a10_interactive,
         "a14": a14, "a11": a11, "a12": a12}

if __name__ == "__main__":
    for key in (sys.argv[1:] or list(FUNCS)):
        FUNCS[key]()
        print(key, "ok")
