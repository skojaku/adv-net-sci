# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["pillow"]
# ///
"""Roman-world basemap for the Module 06 opening slide.

Downloads OpenStreetMap standard raster tiles once, caches
them in figures/data/tiles/, and composes one static PNG in Web Mercator
(EPSG:3857, no reprojection):

    figures/data/roma-basemap.png          the map, ~2000 px wide
    figures/data/roma-basemap.json         bbox, image size, pixel position of each city
    figures/data/roma-basemap-preview.png  the map with red pins and names (a check, not for slides)

Run:  uv run slides/m06/figures/make_basemap.py            (from the repo root)
      uv run slides/m06/figures/make_basemap.py --preview  (re-draw the preview only)

City coordinates are read from ROMA_POS in verify_numbers.py (not imported, since
that module pulls in networkx; the dict literal is parsed instead).

Attribution that must appear on the slide:  (c) OpenStreetMap contributors (openstreetmap.org/copyright)
"""
import ast
import json
import math
import sys
import time
import urllib.request
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
TILES = DATA / "tiles"
OUT_PNG = DATA / "roma-basemap.png"
OUT_JSON = DATA / "roma-basemap.json"
OUT_PREVIEW = DATA / "roma-basemap-preview.png"
OUT_PALE = DATA / "roma-basemap-pale.png"

# One zoom level; only the tiles that cover the extent are fetched (z=6: 49 tiles, z=7: ~170).
# The mosaic is cropped to the extent and scaled so that the width is OUT_WIDTH.
ZOOM = 7
TILE_PX = 256
OUT_WIDTH = 2000

# Londinium (lon -0.1) .. Alexandria (29.9), Tarraco (lat 41.1 is not the south edge;
# Alexandria 31.2 is) .. Londinium (51.5); margin in degrees so pins and names fit.
MARGIN_LON = 1.7
MARGIN_LAT = 1.1

# CARTO "light_nolabels" (https://a.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png) would be
# the first choice (no labels), but as of 2026-10 every CARTO raster tile, @2x included, answers
# 200 with a blank tile stamped "API KEY REQUIRED". So the OSM standard tiles are used. They carry
# modern place names; the lecturer must cover or crop them (see the report).
SOURCES = [
    # (name, url template, attribution)
    ("osm-standard", "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
     "© OpenStreetMap contributors"),
]
USER_AGENT = "adv-net-sci-lecture-basemap/1.0 (Binghamton University course; skojaku@binghamton.edu)"

R = 6378137.0
ORIGIN = math.pi * R  # half the world width in metres


def merc(lon, lat):
    x = math.radians(lon) * R
    y = math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)) * R
    return x, y


def read_roma_pos():
    tree = ast.parse((HERE / "verify_numbers.py").read_text())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "ROMA_POS" for t in node.targets):
            return {k: tuple(v) for k, v in ast.literal_eval(node.value).items()}
    raise SystemExit("ROMA_POS not found in verify_numbers.py")


def fetch(z, x, y):
    """Return the cached tile path, downloading it (politely) if absent."""
    for name, tmpl, _ in SOURCES:
        p = TILES / name / str(z) / str(x) / f"{y}.png"
        if p.exists() and p.stat().st_size > 0:
            return p
    last = None
    for name, tmpl, _ in SOURCES:
        p = TILES / name / str(z) / str(x) / f"{y}.png"
        url = tmpl.format(z=z, x=x, y=y)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
            data = urllib.request.urlopen(req, timeout=30).read()
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
            time.sleep(0.4)  # be polite
            return p
        except Exception as e:  # try the next source
            last = e
    raise SystemExit(f"could not fetch tile {z}/{x}/{y}: {last}")


def pale(img, keep=0.35, lift=0.15):
    """Desaturate (keep = share of colour kept) and blend toward white (lift), so a labelled
    OSM tile works as a quiet background. lift = 0.15 keeps the sea about 33 grey levels
    darker than the land (lift 0.55 left 12 to 18, which vanished on a projector)."""
    from PIL import ImageEnhance
    img = ImageEnhance.Color(img).enhance(keep)
    return Image.blend(img, Image.new("RGB", img.size, "white"), lift)


def build():
    pos = read_roma_pos()
    lons = [p[0] for p in pos.values()]
    lats = [p[1] for p in pos.values()]
    west, east = min(lons) - MARGIN_LON, max(lons) + MARGIN_LON
    south, north = min(lats) - MARGIN_LAT, max(lats) + MARGIN_LAT
    x0m, y0m = merc(west, south)   # lower-left in metres
    x1m, y1m = merc(east, north)   # upper-right in metres

    world_px = TILE_PX * 2 ** ZOOM
    m_per_px = 2 * ORIGIN / world_px

    def to_world_px(xm, ym):  # Web Mercator metres -> world pixel (origin top-left)
        return (xm + ORIGIN) / m_per_px, (ORIGIN - ym) / m_per_px

    px_w, py_n = to_world_px(x0m, y1m)   # top-left
    px_e, py_s = to_world_px(x1m, y0m)   # bottom-right
    tx0, tx1 = int(px_w // TILE_PX), int(px_e // TILE_PX)
    ty0, ty1 = int(py_n // TILE_PX), int(py_s // TILE_PX)
    n_tiles = (tx1 - tx0 + 1) * (ty1 - ty0 + 1)
    print(f"zoom {ZOOM}, tiles x {tx0}..{tx1}, y {ty0}..{ty1} ({n_tiles} tiles)")

    mosaic = Image.new("RGB", ((tx1 - tx0 + 1) * TILE_PX, (ty1 - ty0 + 1) * TILE_PX), "white")
    for tx in range(tx0, tx1 + 1):
        for ty in range(ty0, ty1 + 1):
            tile = Image.open(fetch(ZOOM, tx, ty)).convert("RGB")
            if tile.size != (TILE_PX, TILE_PX):
                tile = tile.resize((TILE_PX, TILE_PX), Image.LANCZOS)
            mosaic.paste(tile, ((tx - tx0) * TILE_PX, (ty - ty0) * TILE_PX))

    # exact crop of the requested extent, then scale to OUT_WIDTH
    left, top = px_w - tx0 * TILE_PX, py_n - ty0 * TILE_PX
    right, bottom = px_e - tx0 * TILE_PX, py_s - ty0 * TILE_PX
    crop = mosaic.crop((round(left), round(top), round(right), round(bottom)))
    scale = OUT_WIDTH / crop.width
    out_h = round(crop.height * scale)
    img = crop.resize((OUT_WIDTH, out_h), Image.LANCZOS)
    img.save(OUT_PNG, optimize=True)
    pale(img).save(OUT_PALE, optimize=True)

    # pixel positions: exact Web Mercator -> output pixel
    sx = OUT_WIDTH / (x1m - x0m)
    sy = out_h / (y1m - y0m)
    cities = {}
    for name, (lon, lat) in pos.items():
        xm, ym = merc(lon, lat)
        cities[name] = {"lon": lon, "lat": lat,
                        "px": round((xm - x0m) * sx, 1), "py": round((y1m - ym) * sy, 1)}
    info = {
        "crs": "EPSG:3857 (Web Mercator), no reprojection",
        "source": SOURCES[0][0], "attribution": SOURCES[0][2], "zoom": ZOOM,
        "tile_px": TILE_PX,
        "bbox_lonlat": {"west": west, "south": south, "east": east, "north": north},
        "bbox_mercator_m": {"xmin": x0m, "ymin": y0m, "xmax": x1m, "ymax": y1m},
        "image": {"width": OUT_WIDTH, "height": out_h, "aspect_w_over_h": round(OUT_WIDTH / out_h, 4)},
        "cities": cities,
    }
    OUT_JSON.write_text(json.dumps(info, indent=2, ensure_ascii=False))
    print(f"wrote {OUT_PNG.name} {OUT_WIDTH}x{out_h} (w/h = {OUT_WIDTH / out_h:.3f})")
    return info


def preview(info=None):
    info = info or json.loads(OUT_JSON.read_text())
    img = Image.open(OUT_PNG).convert("RGB")
    d = ImageDraw.Draw(img)
    font = None
    for f in ("/System/Library/Fonts/Helvetica.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"):
        try:
            font = ImageFont.truetype(f, 28)
            break
        except OSError:
            pass
    font = font or ImageFont.load_default()
    for name, c in info["cities"].items():
        x, y = c["px"], c["py"]
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=(220, 30, 30), outline="white", width=3)
        if x > img.width - 260:  # label to the left of the pin so it is not cut off
            d.text((x - 14, y - 14), name, fill=(150, 0, 0), font=font, anchor="ra",
                   stroke_width=3, stroke_fill="white")
        else:
            d.text((x + 14, y - 14), name, fill=(150, 0, 0), font=font, stroke_width=3, stroke_fill="white")
    img.save(OUT_PREVIEW)
    print(f"wrote {OUT_PREVIEW.name}")


if __name__ == "__main__":
    DATA.mkdir(parents=True, exist_ok=True)
    if "--preview" in sys.argv and OUT_JSON.exists():
        preview()
    else:
        preview(build())
