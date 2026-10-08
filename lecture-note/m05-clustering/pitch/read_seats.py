# /// script
# dependencies = ["opencv-python-headless", "numpy"]
# ///
"""Photo of hand-drawn circles -> seats.csv (id,x,y) + an overlay to check by eye.

    uv run read_seats.py photo.jpg seats.csv overlay.png
"""
import csv, string, sys

import cv2
import numpy as np

src, out_csv, out_png = sys.argv[1:4]
img = cv2.imread(src)
H, W = img.shape[:2]
gray = cv2.GaussianBlur(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY), (5, 5), 0)
# local threshold: survives shadows and uneven light on the paper
ink = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 51, 15)
ink = cv2.morphologyEx(ink, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))   # close small gaps in a pen stroke
cnts, _ = cv2.findContours(ink, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def stats(c):
    a, p = cv2.contourArea(c), cv2.arcLength(c, True)
    return a, (4 * np.pi * a / p**2 if p else 0)

big = [c for c in cnts if stats(c)[0] > 0.0003 * H * W]
ref = np.median([stats(c)[0] for c in big])
good, bad = [], []
for c in big:
    a, circ = stats(c)
    (good if 0.4 * ref < a < 2.2 * ref and circ > 0.6 else bad).append(c)

pts = []
for c in good:
    m = cv2.moments(c)
    pts.append((m["m10"] / m["m00"], m["m01"] / m["m00"]))
pts.sort()                                  # left to right
P = np.array(pts)
D = np.linalg.norm(P[:, None] - P[None], axis=2)
np.fill_diagonal(D, np.inf)
unit = np.median(D.min(axis=1))             # one "seat width": the usual distance to the nearest neighbour
ids = list(string.ascii_uppercase) + [a + b for a in string.ascii_uppercase for b in string.ascii_uppercase]
with open(out_csv, "w", newline="") as f:
    w = csv.writer(f); w.writerow(["id", "x", "y"])
    for i, (x, y) in enumerate(P):
        w.writerow([ids[i], round(x / unit, 2), round((H - y) / unit, 2)])   # y up, like the notebook's picture

over = img.copy()
cv2.drawContours(over, bad, -1, (0, 0, 255), 3)          # rejected shapes in red
for i, (x, y) in enumerate(P):
    cv2.circle(over, (int(x), int(y)), 6, (255, 0, 0), -1)
    cv2.putText(over, ids[i], (int(x) + 10, int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)
cv2.imwrite(out_png, over)
print(f"{len(P)} circles found, {len(bad)} shapes rejected (red). One seat width = {unit:.1f} px.")
