"""python3 figures/check_size.py name W H  ->  exits 1 if figures/<name>.svg is larger than W x H slide px."""
import re, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
name, W, H = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
head = (HERE / f"{name}.svg").read_text()[:600]
w = float(re.search(r'width="([\d.]+)pt"', head).group(1)) / 0.75
h = float(re.search(r'height="([\d.]+)pt"', head).group(1)) / 0.75
ok = w <= W + 0.5 and h <= H + 0.5
print(f"{name}: {w:.0f} x {h:.0f} px (limit {W:.0f} x {H:.0f})", "OK" if ok else "TOO BIG")
sys.exit(0 if ok else 1)
