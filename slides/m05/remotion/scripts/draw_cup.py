"""python3 scripts/draw_cup.py [out.png]
Draws the cup of tea that stands next to the keyboard in every frame of the narrator (out/character/cup-layer.png, RGBA, the size of the Gemini pictures, 1264 x 848).
Drawn here, not by the image model (lecturer: the model's cup was glossy): thick black outline like the character's, flat pale-blue glaze (the colour of the wristbands),
one matte lavender shadow along the lower right, flat tea, a thin steam wisp, and no highlight. scripts/prep_character.py pastes this layer into every frame.
Needs numpy and Pillow. Drawn at 4x and reduced, so that the lines are smooth.
"""
import sys

import numpy as np
from PIL import Image, ImageDraw

W, H = 1264, 848
K = 4  # supersampling
OUT = sys.argv[1] if len(sys.argv) > 1 else 'out/character/cup-layer.png'

INK = (30, 30, 30, 255)
GLAZE = (186, 218, 236, 255)  # pale blue, a little lighter than the wristband (157, 203, 224)
SHADE = (172, 178, 222, 255)  # matte lavender, like the shading of the character
TEA = (201, 146, 88, 255)  # flat warm brown
STEAM = (140, 140, 150, 255)
LINE = 11  # outline width of the character's body lines (11 to 13 px on this canvas)

# the cup: the rim centre, the half widths, the height of the bowl (canvas pixels)
CX, RIM_Y = 1150, 508
RIM_RX, RIM_RY = 66, 17
BASE_RX, BOTTOM_Y = 40, 604


def s(v):
    return v * K  # a canvas length in the supersampled drawing


def sx(x):
    return (x - OX) * K


def sy(y):
    return (y - OY) * K


def ellipse_box(cx, cy, rx, ry):
    return [sx(cx - rx), sy(cy - ry), sx(cx + rx), sy(cy + ry)]


def bowl_polygon(n=40):
    """the outline of the bowl: the left side of the rim, down to the base, along the foot, up the right side"""
    pts = []
    for i in range(n + 1):  # left side, rim to base: a gentle curve
        t = i / n
        x = CX - RIM_RX + (RIM_RX - BASE_RX) * (t ** 1.6)
        y = RIM_Y + (BOTTOM_Y - RIM_Y) * t
        pts.append((x, y))
    for i in range(1, n):  # the foot: the lower half of an ellipse
        a = np.pi * i / n
        pts.append((CX - BASE_RX * np.cos(a), BOTTOM_Y + 9 * np.sin(a)))
    for i in range(n + 1):  # right side, base to rim
        t = 1 - i / n
        x = CX + RIM_RX - (RIM_RX - BASE_RX) * (t ** 1.6)
        y = RIM_Y + (BOTTOM_Y - RIM_Y) * t
        pts.append((x, y))
    return pts


OX, OY, LW, LH = 1030, 380, 260, 270  # the box around the cup, canvas pixels: drawn here at K x, then pasted into the full layer
big = Image.new('RGBA', (LW * K, LH * K), (0, 0, 0, 0))
d = ImageDraw.Draw(big)

# handle: a thick black C that starts inside the bowl (the bowl is drawn over its ends)
hcx, hcy, hrx, hry = CX + RIM_RX - 20, RIM_Y + 50, 40, 34
box = [sx(hcx - hrx), sy(hcy - hry), sx(hcx + hrx), sy(hcy + hry)]
d.arc(box, start=-80, end=95, fill=INK, width=s(LINE + 3))

# bowl: black outline (the polygon grown by the line width), the glaze inside, a matte shadow along the lower right
poly = [(sx(x), sy(y)) for x, y in bowl_polygon()]
d.polygon(poly, fill=INK)
mask = Image.new('L', big.size, 0)
ImageDraw.Draw(mask).polygon(poly, fill=255)
inner = mask.copy()
# erode the inside by the line width: paint the glaze on a shrunken copy
from PIL import ImageFilter  # noqa: E402

inner = inner.filter(ImageFilter.MinFilter(2 * s(LINE) + 1))  # the glaze starts one line width inside the outline
glaze = Image.new('RGBA', big.size, GLAZE)
big.paste(glaze, (0, 0), inner)
# the shadow: the inner shape minus the same shape moved up and to the left
shift = Image.new('L', big.size, 0)
shift.paste(inner, (-s(20), -s(11)))
sh = np.asarray(inner).astype(int) - np.asarray(shift).astype(int)
sh_mask = Image.fromarray(np.clip(sh, 0, 255).astype('uint8'), 'L')
big.paste(Image.new('RGBA', big.size, SHADE), (0, 0), sh_mask)

# rim: an ellipse with the outline, the tea inside
d.ellipse(ellipse_box(CX, RIM_Y, RIM_RX, RIM_RY), fill=INK)
d.ellipse(ellipse_box(CX, RIM_Y, RIM_RX - LINE // 2, RIM_RY - LINE // 2), fill=GLAZE)
d.ellipse(ellipse_box(CX, RIM_Y + 2, RIM_RX - 13, RIM_RY - 8), fill=INK)
d.ellipse(ellipse_box(CX, RIM_Y + 2, RIM_RX - 18, RIM_RY - 12), fill=TEA)

# steam: two thin wisps
for x0, top, amp in ((CX - 12, RIM_Y - 96, 9), (CX + 14, RIM_Y - 78, 7)):
    pts = []
    for i in range(41):
        t = i / 40
        pts.append((sx(x0 + amp * np.sin(t * 2 * np.pi * 1.1)), sy(RIM_Y - 22 - (RIM_Y - 22 - top) * t)))
    d.line(pts, fill=STEAM, width=s(6), joint='curve')
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0] - s(3), p[1] - s(3), p[0] + s(3), p[1] + s(3)], fill=STEAM)

small = big.resize((LW, LH), Image.LANCZOS)
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
img.paste(small, (OX, OY))
img.save(OUT)
a = np.asarray(img)[:, :, 3] > 8
ys, xs = np.where(a)
print('wrote', OUT, 'bbox', xs.min(), ys.min(), xs.max(), ys.max())
