"""python3 scripts/prep_character.py
Turns the chosen Gemini pictures of out/character/ into the frames of the narrator (src/video/character/*.png): the white page is made transparent, every frame is
shifted so that the top of the head sits at the same pixels as in the rest frame (the frames are swapped during the video, a head that jumps would look like a twitch),
and all frames are cropped to one common box. Needs numpy and Pillow.
"""
import os
from collections import deque

import numpy as np
from PIL import Image

SRC = 'out/character'
OUT = 'src/video/character'
# frame name -> source picture (see scripts/gen_character.py: base2 = P2 (the prone boy, feet up), pframe-1/2 = typing A/B (the far hand lifted), pframe-21 = typing C (the near hand lifted, made from a rough collage cleaned up by the model), pframe-3 = troubled face while typing, pframe-5 = shrug)
FRAMES = {'rest': 'base2', 'typeA': 'pframe-1', 'typeB': 'pframe-2', 'typeC': 'pframe-21', 'worry': 'pframe-3', 'shrug': 'pframe-5'}
WIDTH = 640  # px of the saved frames; they are shown at about 260 px, so this is sharp at 2x
SEARCH = 70  # largest shift tried, px


def load(name):
    return np.asarray(Image.open(f'{SRC}/{name}.png').convert('RGB')).astype(np.int16)


def background(rgb):
    """the white page: near-white pixels connected to the border of the picture (the black outline closes the character)"""
    h, w, _ = rgb.shape
    near = rgb.min(axis=2) >= 244
    seen = np.zeros((h, w), bool)
    q = deque()
    for x in range(w):
        for y in (0, h - 1):
            if near[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    for y in range(h):
        for x in (0, w - 1):
            if near[y, x] and not seen[y, x]:
                seen[y, x] = True
                q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and near[ny, nx] and not seen[ny, nx]:
                seen[ny, nx] = True
                q.append((ny, nx))
    return seen


def to_rgba(rgb):
    bg = background(rgb)
    # the anti-aliased rim of the black outline: the first two pixels next to the page become partly transparent
    rim = bg.copy()
    for _ in range(2):
        r = rim.copy()
        r[1:, :] |= rim[:-1, :]
        r[:-1, :] |= rim[1:, :]
        r[:, 1:] |= rim[:, :-1]
        r[:, :-1] |= rim[:, 1:]
        rim = r
    alpha = np.full(bg.shape, 255.0)
    m = rgb.min(axis=2).astype(float)
    edge = rim & ~bg
    alpha[edge] = np.clip((250 - m[edge]) / (250 - 40), 0, 1) * 255
    alpha[bg] = 0
    out = np.dstack([rgb, alpha]).astype(np.uint8)
    out[edge, 0:3] = 20  # the rim belongs to the black outline
    return out


def dark(rgb):
    return (rgb.min(axis=2) < 90).astype(np.float32)


def head_box(ref):
    """rows, columns of the top of the head (the hair cap), which is the same in every frame: found from the topmost dark pixels of the rest frame"""
    d = dark(ref)
    top = int(np.where(d.any(axis=1))[0][0])
    xs = np.where(d[top + 40])[0]
    cx = int((xs.min() + xs.max()) / 2)
    return slice(top, top + 200), slice(max(cx - 250, 0), cx + 250)


def shift_for(ref, img):
    """how many px img must move (dy, dx) to put the top of its head on the head of ref (cross-correlation of the outlines, by FFT)"""
    box = head_box(ref)
    a = dark(ref)[box]
    b = dark(img)[box]
    A = np.fft.rfft2(a)
    B = np.fft.rfft2(b)
    cc = np.fft.irfft2(A * np.conj(B), s=a.shape)
    best, arg = -1, (0, 0)
    for dy in range(-SEARCH, SEARCH + 1):
        for dx in range(-SEARCH, SEARCH + 1):
            v = cc[dy % a.shape[0], dx % a.shape[1]]
            if v > best:
                best, arg = v, (dy, dx)
    return arg


def shifted(arr, dy, dx):
    h, w = arr.shape[:2]
    out = np.zeros_like(arr)
    ys, yd = (slice(0, h - dy), slice(dy, h)) if dy >= 0 else (slice(-dy, h), slice(0, h + dy))
    xs, xd = (slice(0, w - dx), slice(dx, w)) if dx >= 0 else (slice(-dx, w), slice(0, w + dx))
    out[yd, xd] = arr[ys, xs]
    return out


os.makedirs(OUT, exist_ok=True)
rgbs = {k: load(v) for k, v in FRAMES.items()}
ref = rgbs['rest']
aligned = {}
for k, rgb in rgbs.items():
    dy, dx = (0, 0) if k == 'rest' else shift_for(ref, rgb)
    print(f'{k:6s} <- {FRAMES[k]:7s} shift dy={dy:+d} dx={dx:+d}')
    aligned[k] = shifted(to_rgba(rgb), dy, dx)

# one crop box for all frames, so that swapping frames never moves the picture
union = np.zeros(ref.shape[:2], bool)
for a in aligned.values():
    union |= a[:, :, 3] > 8
ys, xs = np.where(union)
pad = 10
box = (max(xs.min() - pad, 0), max(ys.min() - pad, 0), min(xs.max() + pad, ref.shape[1]), min(ys.max() + pad, ref.shape[0]))
print('crop box', box, 'size', box[2] - box[0], 'x', box[3] - box[1])
for k, a in aligned.items():
    im = Image.fromarray(a, 'RGBA').crop(box)
    im = im.resize((WIDTH, round(WIDTH * im.height / im.width)), Image.LANCZOS)
    im.save(f'{OUT}/{k}.png', optimize=True)
    print(f'saved {OUT}/{k}.png', im.size, os.path.getsize(f'{OUT}/{k}.png') // 1024, 'KB')
import json

json.dump({'width': im.size[0], 'height': im.size[1]}, open(f'{OUT}/size.json', 'w'))  # the frames share this size (Character.tsx reads it)
