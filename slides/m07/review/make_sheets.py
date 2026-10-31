#!/usr/bin/env python3
"""Red-pen sheets from review/_r/wf.NNN.png.
landscape A4: 4 columns x 3 rows (12 per page); portrait A4: 2 columns x 4 rows (8 per page).
Usage: python3 review/make_sheets.py   (run after: marp deck.md --images png --image-scale 2 -o review/_r/wf.png)"""
import glob, os, re
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DPI = 200
A4 = (int(8.27 * DPI), int(11.69 * DPI))  # portrait pixels
FONT = "/System/Library/Fonts/Helvetica.ttc"


def font(sz):
    try:
        return ImageFont.truetype(FONT, sz)
    except Exception:
        return ImageFont.load_default()


def labels():
    """slide number -> short caption (layout / beat) from deck.md notes."""
    deck = open(os.path.join(ROOT, "deck.md")).read()
    parts = deck.split("\n---\n")
    out = {}
    for blk in parts:
        m = re.search(r"\[#(\d+)\] beat: ([^\n]*)", blk)
        if m:
            out[int(m.group(1))] = m.group(2)
    return out


def sheets(files, cols, rows, landscape, out_pdf, title):
    W, H = (A4[1], A4[0]) if landscape else A4
    margin = int(0.35 * DPI)
    head = int(0.30 * DPI)
    gap_x, gap_y = int(0.18 * DPI), int(0.30 * DPI)  # room for caption and pen
    cap_h = int(0.20 * DPI)
    cw = (W - 2 * margin - (cols - 1) * gap_x) // cols
    ch = int(cw * 9 / 16)
    # fit rows
    avail = H - 2 * margin - head
    need = rows * (ch + cap_h) + (rows - 1) * gap_y
    if need > avail:
        s = avail / need
        cw, ch = int(cw * s), int(ch * s)
        cap_h = int(cap_h * s)
    lab = labels()
    per = cols * rows
    pages = []
    for p0 in range(0, len(files), per):
        page = Image.new("RGB", (W, H), "white")
        d = ImageDraw.Draw(page)
        n = p0 // per + 1
        total = (len(files) + per - 1) // per
        d.text((margin, margin - int(0.05 * DPI)), f"{title}   sheet {n}/{total}", fill="#444444", font=font(int(0.14 * DPI)))
        x0 = margin + (W - 2 * margin - (cols * cw + (cols - 1) * gap_x)) // 2
        for k, f in enumerate(files[p0:p0 + per]):
            r, c = divmod(k, cols)
            x = x0 + c * (cw + gap_x)
            y = margin + head + r * (ch + cap_h + gap_y)
            im = Image.open(f).convert("RGB").resize((cw, ch), Image.LANCZOS)
            page.paste(im, (x, y))
            d.rectangle([x - 1, y - 1, x + cw, y + ch], outline="#888888", width=2)
            num = int(re.search(r"(\d+)\.png$", f).group(1))
            d.text((x, y + ch + 4), f"#{num}  {lab.get(num, '')}"[:int(cw / (0.075 * DPI) * 1.15)], fill="#B14434", font=font(int(0.115 * DPI)))
        pages.append(page)
    pages[0].save(out_pdf, save_all=True, append_images=pages[1:], resolution=DPI)
    return len(pages)


if __name__ == "__main__":
    files = sorted(glob.glob(os.path.join(HERE, "_r", "wf.*.png")))
    a = sheets(files, 4, 3, True, os.path.join(ROOT, "sheets-landscape.pdf"), "M07 random walks: wireframe v1 (landscape 4x3)")
    b = sheets(files, 2, 4, False, os.path.join(ROOT, "sheets-portrait.pdf"), "M07 random walks: wireframe v1 (portrait 2x4)")
    print("landscape pages", a, "portrait pages", b)
    # PNG previews of the first page of each, for QA
    import subprocess
