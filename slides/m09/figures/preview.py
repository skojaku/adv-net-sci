"""python3 figures/preview.py name [name ...]  ->  figures/_build/png/<name>.png (2x), for looking at a figure."""
import subprocess, sys
from pathlib import Path
HERE = Path(__file__).resolve().parent
out = HERE / "_build" / "png"; out.mkdir(parents=True, exist_ok=True)
for n in sys.argv[1:]:
    subprocess.run(["pdftocairo", "-png", "-r", "144", "-singlefile", str(HERE / "_build" / f"{n}.pdf"), str(out / n)], check=True)
    print(out / f"{n}.png")
