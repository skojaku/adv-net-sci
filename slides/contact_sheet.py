#!/usr/bin/env python3
"""Lay a rendered deck out as thumbnail contact sheets.

    python3 slides/contact_sheet.py m04                  # 3 x 5, one PDF
    python3 slides/contact_sheet.py m04 --grid 5x3       # 5 across, 3 down
    python3 slides/contact_sheet.py m04 --png            # also one PNG per sheet

Reads `<deck>/review/slide.*.png`, which `gatelib render` (or marp's `--images png`)
writes, and never re-renders: a contact sheet of a stale render would be a contact
sheet of a deck that no longer exists, so the newest source file is compared against
the newest PNG and the run refuses if the source is newer.

The page is sized to the grid rather than to paper. A 3 x 5 sheet of 16:9 slides comes
out near square, which is what fits A4 portrait; forcing the grid into a fixed A4 box
instead would leave a third of the page blank under the last row.
"""

import argparse
import pathlib
import re
import sys

from PIL import Image, ImageDraw, ImageFont

THUMB_W = 480                 # 16:9, so the height follows
GUTTER = 28
MARGIN = 56
CAPTION = 34
HEADER = 56

INK = (17, 17, 17)
RULE = (196, 196, 196)
DIM = (120, 120, 120)
PAPER = (255, 255, 255)

# The deck's own body face, then whatever the machine has. A missing font silently
# becomes a 10px bitmap, which is unreadable at thumbnail scale, so the fallback list
# ends in an explicit failure rather than in PIL's default.
FACES = [
    "/System/Library/Fonts/Supplemental/Arial.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def face(size):
    for p in FACES:
        if pathlib.Path(p).exists():
            return ImageFont.truetype(p, size)
    sys.exit(f"no usable font found; tried {FACES}")


def slides(deck):
    """Every rendered slide, in slide order, with the render checked for staleness."""
    pngs = sorted((deck / "review").glob("slide.*.png"),
                  key=lambda p: int(re.search(r"(\d+)", p.name).group(1)))
    if not pngs:
        sys.exit(f"no {deck}/review/slide.*.png -- render the deck first:\n"
                 f"  cd ~/.claude/skills/slide && "
                 f"python3 -m gatelib render {deck.resolve()}")
    newest_png = max(p.stat().st_mtime for p in pngs)
    src = sorted(deck.glob("*.md")) + sorted((deck / "figures").glob("*.png"))
    stale = [p for p in src if p.stat().st_mtime > newest_png]
    if stale:
        sys.exit(f"{len(stale)} source file(s) are newer than the render "
                 f"(e.g. {stale[0]}) -- re-render before sheeting.")
    return pngs


def sheet(page_slides, first, title, cols, rows):
    """One page: `cols` x `rows` thumbnails, each captioned with its slide number."""
    tw, th = THUMB_W, round(THUMB_W * 9 / 16)
    cell_h = th + CAPTION
    w = MARGIN * 2 + cols * tw + (cols - 1) * GUTTER
    h = MARGIN * 2 + HEADER + rows * cell_h + (rows - 1) * GUTTER

    page = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(page)
    d.text((MARGIN, MARGIN), title, font=face(30), fill=INK)
    d.line([(MARGIN, MARGIN + 44), (w - MARGIN, MARGIN + 44)], fill=RULE, width=2)

    num = face(22)
    for i, png in enumerate(page_slides):
        cx = MARGIN + (i % cols) * (tw + GUTTER)
        cy = MARGIN + HEADER + (i // cols) * (cell_h + GUTTER)
        im = Image.open(png).convert("RGB").resize((tw, th), Image.LANCZOS)
        page.paste(im, (cx, cy))
        # A hairline, because a white slide on white paper has no edge otherwise.
        d.rectangle([cx, cy, cx + tw - 1, cy + th - 1], outline=RULE, width=1)
        d.text((cx, cy + th + 8), f"{first + i:02d}", font=num, fill=DIM)
    return page


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("deck", help="deck directory, e.g. m04")
    ap.add_argument("--grid", default="3x5", help="COLSxROWS per sheet (default 3x5)")
    ap.add_argument("--png", action="store_true", help="also write one PNG per sheet")
    ap.add_argument("-o", "--out", help="output PDF (default <deck>/<deck>-thumbs.pdf)")
    a = ap.parse_args()

    deck = pathlib.Path(a.deck)
    if not deck.is_dir():
        sys.exit(f"{deck} is not a directory")
    cols, rows = (int(v) for v in a.grid.lower().split("x"))
    per = cols * rows

    pngs = slides(deck)
    # The deck is the .md with marp front matter -- picking the first .md alphabetically
    # named the first sheet after README.md.
    decks = [m for m in sorted(deck.glob("*.md"))
             if "marp: true" in m.read_text()[:400]]
    if len(decks) != 1:
        sys.exit(f"expected exactly one marp deck in {deck}, found {decks}")
    name = decks[0].stem
    pages = [pngs[i:i + per] for i in range(0, len(pngs), per)]
    sheets = [sheet(chunk, 1 + i * per,
                    f"{name}  ·  {1 + i * per}-{i * per + len(chunk)} of {len(pngs)}",
                    cols, rows)
              for i, chunk in enumerate(pages)]

    out = pathlib.Path(a.out) if a.out else deck / f"{name}-thumbs.pdf"
    sheets[0].save(out, "PDF", resolution=150.0, save_all=True,
                   append_images=sheets[1:])
    print(f"{out}  {len(sheets)} sheet(s), {len(pngs)} slides, {cols}x{rows}")
    if a.png:
        for i, s in enumerate(sheets, 1):
            p = out.with_name(f"{out.stem}-{i}.png")
            s.save(p)
            print(f"  {p}  {s.size[0]}x{s.size[1]}")


if __name__ == "__main__":
    main()
