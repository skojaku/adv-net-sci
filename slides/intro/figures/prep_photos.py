#!/usr/bin/env python3
"""Crop the deck's photographs to the aspect their container can actually show.

The render gate fails a figure whose height cap binds before its width does: in a
`cols` column that means taller than 0.708 x width, full width it means taller than
0.352 x width. A photo past that ratio is displayed smaller than its slot, so the
crop here is not cosmetic — it is what makes the picture fill the column.

Sources live in `src/`; this script is the only thing that writes the deck-facing
copies, so re-running it always reproduces them.
"""

import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src")

COL_RATIO = 537 / 380  # width / height a `cols` figure can use
FULL_RATIO = 1080 / 380
AUTHORED_FULL_MIN = 3400  # the gate reads a file under ~3000px wide as column-authored

# name -> (container, vertical anchor of the crop: 0 top, 0.5 centre, 1 bottom, fit)
#
# fit="crop" trims the top and bottom to reach the container's aspect; fit="pad" adds
# white to the left and right instead. A portrait whose subject is a single face or a
# single map cannot be cropped to a landscape slot without cutting through the subject
# (von Neumann lost his mouth and Euler his chin that way), so those are padded: the
# picture ends up narrower than the column but nothing is missing from it.
PHOTOS = {
    "airline_routes.jpg": ("full", 0.55, "crop"),
    "internet_map.jpg": ("cols", 0.5, "crop"),
    "lehman.jpg": ("cols", 0.15, "crop"),
    "brain_tracts.jpg": ("cols", 0.5, "crop"),
    "digesting_duck.jpg": ("cols", 0.28, "crop"),
    "von_neumann.jpg": ("cols", 0.12, "pad"),
    "euler.jpg": ("cols", 0.14, "pad"),
    "deadlift.jpg": ("cols", 0.45, "crop"),
    "pen_paper.jpg": ("cols", 0.5, "crop"),
    "sci-topic-net.png": ("cols", 0.5, "crop"),
    "ecog.png": ("cols", 0.5, "crop"),
    "super-charger.png": ("cols", 0.5, "crop"),
    "xz_video_thumb.jpg": ("cols", 0.5, "crop"),
}

# name -> (left, top, right, bottom) taken before anything else. The supercharger
# source stacks two copies of the same map; one of them is the figure.
PRECROP = {
    "super-charger.png": (0, 4, 524, 288),
}


def main():
    for name, (container, anchor, fit) in PHOTOS.items():
        src = os.path.join(SRC, name.replace(".jpg", ".png") if name == "airline_routes.jpg" else name)
        im = Image.open(src)
        im = im.convert("RGB") if name.endswith(".jpg") else im.convert("RGBA").convert("RGB")
        if name in PRECROP:
            im = im.crop(PRECROP[name])
        ratio = COL_RATIO if container == "cols" else FULL_RATIO
        w, h = im.size
        if w / h < ratio:  # too tall for its slot
            if fit == "pad":
                new_w = int(h * ratio) + 1
                canvas = Image.new("RGB", (new_w, h), "white")
                canvas.paste(im, ((new_w - w) // 2, 0))
                im = canvas
            else:
                new_h = int(w / ratio)
                top = int((h - new_h) * anchor)
                im = im.crop((0, top, w, top + new_h))
        if container == "full" and im.width < AUTHORED_FULL_MIN:
            s = AUTHORED_FULL_MIN / im.width
            im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        if container == "cols" and im.width > 3000:
            s = 3000 / im.width
            im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
        out = os.path.join(HERE, name)
        if os.path.exists(out):
            os.remove(out)
        im.save(out, quality=92) if name.endswith(".jpg") else im.save(out)
        print(f"  {name:24s} {im.width}x{im.height}  ratio {im.width / im.height:.2f}  [{container}]")


if __name__ == "__main__":
    main()
