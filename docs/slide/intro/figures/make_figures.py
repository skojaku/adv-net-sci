#!/usr/bin/env python3
"""Figure generator for the course intro deck.

Every drawing is authored at 1 bp = 1 slide pixel, so a 36 pt label lands at
36 px type (15.5 px x-height) on the slide with no rescaling to reconcile.
Containers: full width 1080 px, `cols` column 537 px, height cap 380 px.

Gates enforced here (the render gate `check_render.py` re-measures on the slide):
  * pdflatex log must not contain a font substitution
  * ink must not touch the canvas edge (a touch is a clip, not a crop)
  * no two node discs may overlap
  * no text box may intersect a disc or another text box
  * every drawn coordinate must lie inside the canvas

Text extents come from TeX itself (one calibration run typesets every string and
reports \\wd/\\ht), never from a characters-times-width estimate.
"""

import os
import re
import subprocess
import sys
import tempfile
from math import cos, hypot, radians, sin

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))

# theme palette — nothing else may appear in a figure
ACCENT = "3959A6"
ACCENT2 = "B14434"
ACCENT3 = "DAB167"
GRAY = "6b6b6b"
INK = "000000"

LABEL_PT = 36  # 36 pt => 15.5 px x-height at 1 bp = 1 px
DISC_D = 40  # node disc diameter in bp (gate band is 26-52 px)
PT_TO_BP = 72 / 72.27  # TeX pt -> PostScript big point
PX_PER_BP = 4  # the render gate measures figures authored at 4 px per bp

PREAMBLE = r"""
\documentclass[border=0pt]{standalone}
\usepackage{lmodern}
\usepackage[T1]{fontenc}
\usepackage{tikz}
\usetikzlibrary{arrows.meta,calc}
"""


# --------------------------------------------------------------------------
# text measurement — TeX reports the box, we do not guess it
# --------------------------------------------------------------------------

_TEXT_CACHE: dict[tuple[str, int], tuple[float, float]] = {}


def measure(strings, size=LABEL_PT):
    """Return {string: (width_bp, height_bp)} measured by pdflatex."""
    todo = sorted({s for s in strings if (s, size) not in _TEXT_CACHE})
    if todo:
        body = []
        for i, s in enumerate(todo):
            body.append(
                r"\sbox0{\fontsize{%d}{%d}\selectfont %s}"
                r"\typeout{MEAS|%d|\the\wd0|\the\ht0|\the\dp0}" % (size, size, s, i)
            )
        tex = PREAMBLE + r"\begin{document}" + "".join(body) + r"\mbox{}\end{document}"
        log = _pdflatex(tex, "measure")
        got = {}
        for m in re.finditer(r"MEAS\|(\d+)\|([\d.]+)pt\|([\d.]+)pt\|([\d.]+)pt", log):
            i, w, h, d = int(m.group(1)), *(float(g) for g in m.group(2, 3, 4))
            got[i] = (w * PT_TO_BP, (h + d) * PT_TO_BP)
        assert len(got) == len(todo), f"measured {len(got)} of {len(todo)} strings"
        for i, s in enumerate(todo):
            _TEXT_CACHE[(s, size)] = got[i]
    return {s: _TEXT_CACHE[(s, size)] for s in strings}


def xheight(size=LABEL_PT):
    return measure(["x"], size)["x"][1]


def _pdflatex(tex, stem):
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, stem + ".tex")
        with open(src, "w") as fh:
            fh.write(tex)
        proc = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", src],
            cwd=td,
            capture_output=True,
            text=True,
        )
        log = proc.stdout + proc.stderr
        if proc.returncode != 0:
            raise SystemExit(f"pdflatex failed for {stem}:\n{log[-3000:]}")
        assert "not available" not in log, (
            f"{stem}: LaTeX substituted a font size — the label is not the size you asked "
            f"for.\n{[l for l in log.splitlines() if 'not available' in l]}"
        )
        pdf = os.path.join(td, stem + ".pdf")
        return log if not os.path.exists(pdf) else (log, open(pdf, "rb").read())[0] if False else log


def _pdflatex_png(tex, stem, out, w, h):
    with tempfile.TemporaryDirectory() as td:
        src = os.path.join(td, stem + ".tex")
        with open(src, "w") as fh:
            fh.write(tex)
        proc = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", src],
            cwd=td,
            capture_output=True,
            text=True,
        )
        log = proc.stdout + proc.stderr
        if proc.returncode != 0:
            raise SystemExit(f"pdflatex failed for {stem}:\n{log[-3000:]}")
        assert "not available" not in log, f"{stem}: font size substituted by LaTeX"
        subprocess.run(
            ["pdftoppm", "-r", str(72 * PX_PER_BP), "-png", "-singlefile",
             os.path.join(td, stem + ".pdf"), os.path.join(td, stem)],
            check=True,
        )
        im = Image.open(os.path.join(td, stem + ".png")).convert("RGB")
    # pdftoppm rounds the page box; pad or crop to the declared canvas
    want = (w * PX_PER_BP, h * PX_PER_BP)
    if im.size != want:
        canvas = Image.new("RGB", want, "white")
        canvas.paste(im, (0, 0))
        im = canvas
    if os.path.exists(out):
        os.remove(out)  # a green build must not be able to leave a stale file
    im.save(out)
    return im


# --------------------------------------------------------------------------
# the drawing surface — every primitive records itself so the gates can see it
# --------------------------------------------------------------------------


class Fig:
    def __init__(self, name, w, h, container):
        self.name, self.w, self.h, self.container = name, w, h, container
        self.body = []
        self.discs = []  # (x, y, diameter)
        self.boxes = []  # (x0, y0, x1, y1, what)

    # -- primitives ---------------------------------------------------------

    def _pt(self, x, y):
        assert 0 <= x <= self.w and 0 <= y <= self.h, (
            f"{self.name}: ({x:.0f},{y:.0f}) is outside the {self.w}x{self.h} canvas — "
            f"ink drawn off the page never renders"
        )
        return f"({x:.2f},{y:.2f})"

    def disc(self, x, y, fill=ACCENT, d=DISC_D, border=None, bw=0):
        self._pt(x, y)
        opts = f"fill=c{fill}"
        opts += f", draw=c{border}, line width={bw}bp" if border else ", draw=none"
        self.body.append(f"\\filldraw[{opts}] {self._pt(x, y)} circle ({d / 2 + (bw / 2 if border else 0):.2f});")
        self.discs.append((x, y, d + (bw if border else 0)))

    def seg(self, x1, y1, x2, y2, color=GRAY, lw=2, arrow=False, bend=0):
        opt = f"draw=c{color}, line width={lw}bp"
        if arrow:
            opt += ", -{Latex[length=9bp,width=8bp]}"
        b = f" to[bend left={bend}] " if bend else " -- "
        self.body.append(f"\\draw[{opt}] {self._pt(x1, y1)}{b}{self._pt(x2, y2)};")

    def box(self, cx, cy, w, h, fill="ffffff", draw=INK, lw=2.5):
        self._pt(cx - w / 2, cy - h / 2)
        self._pt(cx + w / 2, cy + h / 2)
        self.body.append(
            f"\\filldraw[fill=c{fill}, draw=c{draw}, "
            f"line width={lw}bp, rounded corners=6bp] "
            f"{self._pt(cx - w / 2, cy - h / 2)} rectangle {self._pt(cx + w / 2, cy + h / 2)};"
        )

    def text(self, x, y, s, anchor="center", color=INK, size=LABEL_PT, guard=True):
        w, h = measure([s], size)[s]
        ax = {"center": 0.5, "west": 0.0, "east": 1.0}
        ay = {"center": 0.5, "south": 0.0, "north": 1.0}
        hx = anchor.split()[-1] if anchor.split()[-1] in ax else "center"
        hy = anchor.split()[0] if anchor.split()[0] in ay else "center"
        x0 = x - ax[hx] * w
        y0 = y - ay[hy] * h
        self._pt(x0, y0)
        self._pt(x0 + w, y0 + h)
        self.body.append(
            f"\\node[anchor={anchor}, inner sep=0, text=c{color}] at "
            f"{self._pt(x, y)} {{\\fontsize{{{size}}}{{{size}}}\\selectfont {s}}};"
        )
        if guard:
            self.boxes.append((x0, y0, x0 + w, y0 + h, s))

    # -- gates --------------------------------------------------------------

    def _check_geometry(self):
        for i, (x1, y1, d1) in enumerate(self.discs):
            for x2, y2, d2 in self.discs[i + 1:]:
                gap = hypot(x2 - x1, y2 - y1) - (d1 + d2) / 2
                assert gap >= 6, (
                    f"{self.name}: two discs overlap or touch (gap {gap:.1f}bp) at "
                    f"({x1:.0f},{y1:.0f}) and ({x2:.0f},{y2:.0f})"
                )
        pad = 4
        for i, b in enumerate(self.boxes):
            for c in self.boxes[i + 1:]:
                if b[0] - pad < c[2] and c[0] - pad < b[2] and b[1] - pad < c[3] and c[1] - pad < b[3]:
                    raise AssertionError(
                        f"{self.name}: label {b[4]!r} overlaps label {c[4]!r} — shorten the "
                        f"note or move the drawing; never shrink the type"
                    )
            for x, y, d in self.discs:
                nx, ny = max(b[0], min(x, b[2])), max(b[1], min(y, b[3]))
                if hypot(x - nx, y - ny) < d / 2 + pad:
                    raise AssertionError(
                        f"{self.name}: label {b[4]!r} sits on the disc at ({x:.0f},{y:.0f}) — "
                        f"move the label; never shrink the type"
                    )

    def emit(self):
        self._check_geometry()
        tex = (
            PREAMBLE
            + "".join(
                f"\\definecolor{{c{c}}}{{HTML}}{{{c.upper()}}}"
                for c in (ACCENT, ACCENT2, ACCENT3, GRAY, INK, "ffffff")
            )
            + r"\begin{document}\begin{tikzpicture}[x=1bp,y=1bp]"
            + f"\\useasboundingbox (0,0) rectangle ({self.w},{self.h});"
            + "".join(self.body)
            + r"\end{tikzpicture}\end{document}"
        )
        out = os.path.join(HERE, self.name)
        im = _pdflatex_png(tex, self.name.replace(".png", ""), out, self.w, self.h)
        check_ink(out, im, self.name, self.container, self.w, self.h)
        return im


def check_ink(path, im, name, container, w, h):
    """Ink must stay off the canvas edge, and the drawing must fill its box."""
    gray = np.asarray(im.convert("L"))
    ys, xs = np.where(gray < 235)
    xs, ys = xs / PX_PER_BP, ys / PX_PER_BP
    assert xs.size, f"{name}: nothing was drawn"
    assert not (xs.min() <= 2 or xs.max() >= w - 3 or ys.min() <= 2 or ys.max() >= h - 3), (
        f"{name}: ink touches the canvas edge ({xs.min()},{xs.max()},{ys.min()},{ys.max()} "
        f"in {w}x{h}) — that is a clip, not a crop"
    )
    for axis, lo, hi, size in (("x", xs.min(), xs.max(), w), ("y", ys.min(), ys.max(), h)):
        margin = (lo + (size - hi)) / size
        assert margin <= 0.30, (
            f"{name}: {margin:.0%} of the {axis} axis is empty margin — the deck would be "
            f"scaling whitespace, not the drawing"
        )
    scale = min(container / w, 380 / h, 1.0)
    assert h <= 380, f"{name}: {h}bp tall exceeds the 380px `fig` cap; the type would shrink"
    xh = xheight() * scale
    assert xh >= 15.0, (
        f"{name}: {LABEL_PT}pt type lands at {xh:.1f}px x-height in a {container}px "
        f"container (floor 15px) — the figure is too wide or too tall for its container"
    )
    print(f"  {name:24s} {w}x{h} bp  x-h {xh:.1f}px  [{container}px container]")


# --------------------------------------------------------------------------
# figures
# --------------------------------------------------------------------------


def fig_flightpath():
    """Why Spain, and not Mexico's neighbour: distance measured in flights."""
    f = Fig("flightpath.png", 1080, 330, 1080)
    mex, gua, nyc, mad = (150, 200), (150, 80), (520, 250), (930, 190)
    f.seg(*mex, *nyc, color=ACCENT, lw=11)
    f.seg(*nyc, *mad, color=ACCENT, lw=11)
    f.seg(*mex, *mad, color=ACCENT, lw=7)
    f.seg(*mex, *gua, color=ACCENT, lw=1.5)
    for p in (mex, gua, nyc, mad):
        f.disc(*p)
    f.text(150, 228, "Mexico City", anchor="south")
    f.text(150, 52, "Guatemala City", anchor="north")
    f.text(520, 278, "New York", anchor="south")
    f.text(930, 218, "Madrid", anchor="south")
    f.text(1060, 30, "thicker line: more passengers a day", anchor="south east", color=GRAY)
    return f


def _wheel():
    hub = (540, 170)
    ring = [
        (540 + 400 * cos(radians(a)), 170 + 115 * sin(radians(a)))
        for a in range(0, 360, 45)
    ]
    return hub, ring


def fig_interbank_1():
    """Banks are a network: every line is a loan."""
    f = Fig("interbank_1.png", 1080, 340, 1080)
    hub, ring = _wheel()
    for p in ring:
        f.seg(*hub, *p, color=GRAY, lw=2.5)
    for a, b in zip(ring, ring[1:] + ring[:1]):
        f.seg(*a, *b, color=GRAY, lw=2.5)
    f.disc(*hub)
    for p in ring:
        f.disc(*p)
    return f


def fig_interbank_2():
    """One borrower defaults and the loss travels out along its loans."""
    f = Fig("interbank_2.png", 1080, 340, 1080)
    hub, ring = _wheel()
    for a, b in zip(ring, ring[1:] + ring[:1]):
        f.seg(*a, *b, color=GRAY, lw=2.5)
    for p in ring:
        dx, dy = p[0] - hub[0], p[1] - hub[1]
        n = hypot(dx, dy)
        f.seg(
            hub[0] + dx / n * 26, hub[1] + dy / n * 26,
            hub[0] + dx / n * (n - 30), hub[1] + dy / n * (n - 30),
            color=ACCENT2, lw=5, arrow=True,
        )
    f.disc(*hub, fill=ACCENT2)
    for p in ring:
        f.disc(*p)
    return f


CHAIN = ["xz", "liblzma", "systemd", "sshd", "server"]


def _chain(f, cy):
    w = measure(CHAIN)
    widths = [w[s][0] + 48 for s in CHAIN]
    gap = (1040 - sum(widths)) / (len(CHAIN) - 1)
    x = 20
    centers = []
    for s, bw in zip(CHAIN, widths):
        centers.append(x + bw / 2)
        f.box(x + bw / 2, cy, bw, 90)
        f.text(x + bw / 2, cy, s)
        x += bw + gap
    for (c1, w1), (c2, w2) in zip(zip(centers, widths), list(zip(centers, widths))[1:]):
        f.seg(c1 + w1 / 2 + 6, cy, c2 - w2 / 2 - 6, cy, color=INK, lw=3, arrow=True)
    return centers, widths


def fig_xz_1():
    """The dependency chain the backdoor travelled down."""
    f = Fig("xz_1.png", 1080, 130, 1080)
    _chain(f, 65)
    return f


def fig_xz_2():
    """A maintainer at the head of the chain owns everything below it."""
    f = Fig("xz_2.png", 1080, 300, 1080)
    centers, widths = _chain(f, 70)
    s = "a trusted maintainer"
    tw = measure([s])[s][0] + 48
    f.box(tw / 2 + 20, 240, tw, 90, draw=ACCENT2)
    f.text(tw / 2 + 20, 240, s, color=ACCENT2)
    f.seg(tw / 2 + 20, 193, centers[0], 118, color=ACCENT2, lw=3, arrow=True)
    return f


def fig_pollinator():
    """Who pollinates whom: a network drawn by evolution."""
    f = Fig("pollinator.png", 520, 340, 537)
    top = [(70, 250), (260, 250), (450, 250)]
    bot = [(70, 90), (260, 90), (450, 90)]
    for i, j in ((0, 0), (0, 1), (1, 1), (2, 1), (2, 2)):
        f.seg(*top[i], *bot[j], color=GRAY, lw=2.5)
    for p in top:
        f.disc(*p, fill=ACCENT2)
    for p in bot:
        f.disc(*p, fill=ACCENT)
    f.text(260, 300, "pollinators", anchor="south", color=ACCENT2)
    f.text(260, 40, "plants", anchor="north", color=ACCENT)
    return f


def fig_regular_graph():
    """A textbook graph: every node the same, every neighbourhood the same."""
    f = Fig("regular_graph.png", 520, 340, 537)
    xs, ys = [60, 160, 260, 360, 460], [60, 170, 280]
    for y in ys:
        for a, b in zip(xs, xs[1:]):
            f.seg(a, y, b, y, color=GRAY, lw=2.5)
    for x in xs:
        for a, b in zip(ys, ys[1:]):
            f.seg(x, a, x, b, color=GRAY, lw=2.5)
    for y in ys:
        for x in xs:
            f.disc(x, y)
    return f


def fig_konigsberg():
    """Königsberg: four banks, seven bridges."""
    f = Fig("konigsberg.png", 520, 340, 537)
    isl, east, north, south = (80, 170), (440, 170), (260, 300), (260, 40)
    f.seg(*isl, *north, color=ACCENT, lw=4, bend=32)
    f.seg(*isl, *north, color=ACCENT, lw=4, bend=-32)
    f.seg(*isl, *south, color=ACCENT, lw=4, bend=-32)
    f.seg(*isl, *south, color=ACCENT, lw=4, bend=32)
    f.seg(*isl, *east, color=ACCENT, lw=4)
    f.seg(*north, *east, color=ACCENT, lw=4)
    f.seg(*south, *east, color=ACCENT, lw=4)
    for p in (isl, east, north, south):
        f.disc(*p, fill=GRAY)
    return f


GRADE = [("Quiz", 10), ("Lecture", 10), ("Homework", 20), ("Exam", 30), ("Project", 30)]
GRADE_FILL = [ACCENT, ACCENT2, ACCENT3, GRAY, INK]


def fig_grading():
    """One square is one percent of the grade."""
    assert sum(n for _, n in GRADE) == 100, "the grade must add to 100"
    f = Fig("grading.png", 1080, 320, 1080)
    pitch, side, rows = 46, 40, 5
    x = 32
    for (name, n), fill in zip(GRADE, GRADE_FILL):
        cols = n // rows
        for c in range(cols):
            for r in range(rows):
                f.box(x + c * pitch + side / 2, 40 + r * pitch + side / 2, side, side,
                      fill=fill, draw=fill, lw=0.4)
        f.text(x + cols * pitch / 2 - 3, 280, name, anchor="south")
        x += cols * pitch + 24
    return f


def fig_philosophers():
    """Four answers to one question, 2500 years apart."""
    out = os.path.join(HERE, "philosophers.jpg")
    names = [("phil_thales.jpg", "Thales"), ("phil_pythagoras.jpg", "Pythagoras"),
             ("phil_democritus.jpg", "Democritus"), ("phil_descartes.jpg", "Descartes")]
    src_dir = os.path.join(HERE, "src")
    side, gap, pad = 240 * PX_PER_BP, 20 * PX_PER_BP, 30 * PX_PER_BP
    w, h = 4 * side + 3 * gap + 2 * pad, 310 * PX_PER_BP
    canvas = Image.new("RGB", (w, h), "white")
    font = ImageFont.truetype(
        os.path.join(os.path.dirname(__import__("matplotlib").__file__),
                     "mpl-data/fonts/ttf/DejaVuSans.ttf"), 36 * PX_PER_BP)
    d = ImageDraw.Draw(canvas)
    for i, (src, label) in enumerate(names):
        im = Image.open(os.path.join(src_dir, src)).convert("RGB")
        s = min(im.size)
        im = im.crop(((im.width - s) // 2, 0, (im.width - s) // 2 + s, s)).resize((side, side))
        x = pad + i * (side + gap)
        canvas.paste(im, (x, 20 * PX_PER_BP))
        tw = d.textlength(label, font=font)
        assert tw <= side, f"philosophers: {label!r} is wider than its portrait"
        d.text((x + (side - tw) / 2, 272 * PX_PER_BP), label, fill="black", font=font)
    if os.path.exists(out):
        os.remove(out)
    canvas.save(out, quality=92)
    xh = d.textbbox((0, 0), "x", font=font)
    print(f"  philosophers.jpg         {w // PX_PER_BP}x{h // PX_PER_BP} bp  "
          f"x-h {(xh[3] - xh[1]) / PX_PER_BP:.1f}px  [1080px container]")
    assert w == 1080 * PX_PER_BP, f"philosophers montage is {w}px, not 1080bp wide"
    return canvas


FIGURES = [fig_flightpath, fig_interbank_1, fig_interbank_2, fig_xz_1, fig_xz_2,
           fig_pollinator, fig_regular_graph, fig_konigsberg, fig_grading]


def main():
    print(f"x-height of {LABEL_PT}pt type: {xheight():.1f}bp (floor 15.0)")
    assert xheight() >= 15.0, "the label size is under the legibility floor before any scaling"
    bad = []
    for fn in FIGURES:
        try:
            fn().emit()
        except AssertionError as e:
            bad.append(str(e))
            print(f"  FAIL {fn.__name__}: {e}")
    try:
        fig_philosophers()
    except AssertionError as e:
        bad.append(str(e))
        print(f"  FAIL fig_philosophers: {e}")
    if bad:
        sys.exit(1)
    print(f"{len(FIGURES) + 1} figures written, 0 failed")


if __name__ == "__main__":
    main()
