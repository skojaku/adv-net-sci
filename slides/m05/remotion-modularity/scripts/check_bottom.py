"""python3 scripts/check_bottom.py  (after `npm run review`)

Every slide keeps the lower part of the canvas free for subtitles. This finds, in each still of out/review, the lowest row that
has ink (the page number is ignored) and reports every slide that reaches below SAFE_BOTTOM. Also reports content that comes
closer than 40 px to the left, right or top edge. Needs Pillow and numpy.
"""
import glob
import re
import sys

import numpy as np
from PIL import Image

SAFE_BOTTOM = 920   # keep in step with SAFE_BOTTOM in src/components/Frame.tsx
EDGE = 40
PARTS: set = set()  # this deck has no section dividers

bad = 0
worst = 0
for f in sorted(glob.glob('out/review/S*-s*.png')):
    n = int(re.search(r'S(\d+)-s', f)[1])
    if n in PARTS:
        continue
    ink = np.array(Image.open(f).convert('L')) < 235
    ink[1000:, 1700:] = False  # the page number
    ys = np.where(ink.any(axis=1))[0]
    xs = np.where(ink.any(axis=0))[0]
    worst = max(worst, ys.max())
    problems = []
    if ys.max() > SAFE_BOTTOM:
        problems.append(f'bottom {ys.max()} > {SAFE_BOTTOM}')
    if ys.min() < EDGE or xs.min() < EDGE or xs.max() > 1920 - EDGE:
        problems.append(f'edge: top {ys.min()}, left {xs.min()}, right {xs.max()}')
    if problems:
        bad += 1
        print(f.split('/')[-1], '; '.join(problems))
print(f'lowest ink anywhere: y = {worst}; {bad} still(s) flagged')
sys.exit(1 if bad else 0)
