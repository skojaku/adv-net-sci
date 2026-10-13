#!/usr/bin/env python3
"""Pieces of the slide theme that are drawn, not typeset.

    brush-hot.png    the brush underline under a key term (`strong` in network-science.css)
                     and under the title slide's rule; transparent, stretched by CSS

Drawn with figlib's own brush, so the theme's underlines are the same stroke as the
figures' underlines.
"""

import numpy as np
from PIL import Image

import figlib as F


def _transparent(im, hexcol):
    """White paper to transparency: the darkness of each pixel becomes its alpha."""
    a = np.asarray(im.convert("RGB")).astype(np.float32)
    alpha = (255.0 - a.min(axis=2)) / (255.0 - min(int(hexcol[i:i + 2], 16) for i in (0, 2, 4)))
    alpha = (alpha.clip(0, 1) * 255).astype(np.uint8)
    rgba = np.zeros(a.shape[:2] + (4,), np.uint8)
    rgba[..., :3] = a.clip(0, 255).astype(np.uint8)
    rgba[..., 3] = alpha
    out = Image.fromarray(rgba, "RGBA")
    ys, xs = np.where(alpha > 8)
    return out.crop((xs.min(), ys.min(), xs.max() + 1, ys.max() + 1))


def brush_hot():
    W, H = 600, 40
    body = F.underline(10, W - 10, H / 2, color="hot", w=12, bow=2.0)
    im = F.render(body, W, H)
    out = _transparent(im, F.HOT).resize((1200, 40), Image.LANCZOS)
    out.save(F.OUT / "brush-hot.png")
    F._built.append("brush-hot")
    print(f"  brush-hot.png  {out.size[0]}x{out.size[1]}px (transparent)")


FIGURES = [("brush-hot", brush_hot)]

if __name__ == "__main__":
    F.run(FIGURES)
