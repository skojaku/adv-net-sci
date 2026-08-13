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

# name -> (container, vertical anchor of the crop: 0 top, 0.5 centre, 1 bottom)
PHOTOS = {
    "airline_routes.jpg": ("full", 0.55),
    "internet_map.jpg": ("cols", 0.5),
    "lehman.jpg": ("cols", 0.15),
    "brain_tracts.jpg": ("cols", 0.5),
    "digesting_duck.jpg": ("cols", 0.28),
    "von_neumann.jpg": ("cols", 0.12),
    "euler.jpg": ("cols", 0.14),
    "deadlift.jpg": ("cols", 0.45),
    "pen_paper.jpg": ("cols", 0.5),
    "sci-topic-net.png": ("cols", 0.5),
    "ecog.png": ("cols", 0.5),
    "super-charger.png": ("cols", 0.5),
}


def main():
    for name, (container, anchor) in PHOTOS.items():
        src = os.path.join(SRC, name.replace(".jpg", ".png") if name == "airline_routes.jpg" else name)
        im = Image.open(src)
        im = im.convert("RGB") if name.endswith(".jpg") else im.convert("RGBA").convert("RGB")
        ratio = COL_RATIO if container == "cols" else FULL_RATIO
        w, h = im.size
        if w / h < ratio:  # too tall for its slot
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
