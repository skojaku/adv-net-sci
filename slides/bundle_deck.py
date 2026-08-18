#!/usr/bin/env python3
"""Build one self-contained HTML file from a Marp deck.

`marp -o deck.html` writes HTML that still points outward: `figures/*.png` beside
the deck, and the animation kit in `lecture-note/assets/`. Move that file alone to
another machine and the slides come up blank. This bundles every local reference
into the file itself -- images as base64 `data:` URIs, scripts and stylesheets as
literal text -- so the result opens offline, from a USB stick, with nothing next
to it.

    python3 ../bundle_deck.py intro.md                  -> intro.standalone.html
    python3 ../bundle_deck.py intro.md --max-width 1600 -> the same, downscaled

Figures are authored at 4 px per bp (4320 px full width), which no projector
resolves. `--max-width` resizes anything wider before encoding; 1600 is ample for
a 1280x720 slide and cuts the file several times over. Without it nothing is
touched and the bundle is pixel-identical to the ordinary render.

Give it an already-rendered `.html` instead of the `.md` to skip the marp call.
"""

import argparse
import base64
import io
import mimetypes
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

THEME_NAMES = ("theme.css", "network-science.css")
RASTER = {"image/png", "image/jpeg", "image/webp"}
EXTERNAL = re.compile(r"^(data:|https?:|//|#|mailto:)")

# <script src="x.js"></script> and <link rel=stylesheet href="x.css">
SCRIPT_TAG = re.compile(r"<script\b([^>]*?)\ssrc=\"([^\"]+)\"([^>]*?)>\s*</script>", re.I)
LINK_TAG = re.compile(r"<link\b[^>]*?\shref=\"([^\"]+)\"[^>]*?>", re.I)
SRC_ATTR = re.compile(r"\ssrc=\"([^\"]+)\"")
CSS_URL = re.compile(r"url\(\s*(['\"]?)([^'\")]+)\1\s*\)")


def find_theme(deck: Path) -> Path:
    for name in THEME_NAMES:
        candidate = deck.parent / name
        if candidate.exists():
            return candidate
    sys.exit(f"no theme stylesheet beside {deck.name}: looked for {', '.join(THEME_NAMES)}")


def render(deck: Path, theme: Path, out: Path) -> None:
    """Run marp. --html is not optional: the deck carries a live <script> stage."""
    if shutil.which("marp") is None:
        sys.exit("marp not on PATH -- install @marp-team/marp-cli, or pass a rendered .html")
    subprocess.run(
        ["marp", deck.name, "--theme", theme.name, "--allow-local-files", "--html",
         "--no-stdin", "-o", str(out.resolve())],
        cwd=deck.parent,
        check=True,
    )


def downscale(raw: bytes, mime: str, max_width: int) -> bytes:
    from PIL import Image

    with Image.open(io.BytesIO(raw)) as im:
        if im.width <= max_width:
            return raw
        height = round(im.height * max_width / im.width)
        im = im.resize((max_width, height), Image.LANCZOS)
        buf = io.BytesIO()
        if mime == "image/jpeg":
            im.convert("RGB").save(buf, "JPEG", quality=88, optimize=True, progressive=True)
        else:
            im.save(buf, "PNG", optimize=True)
    return buf.getvalue() if buf.tell() < len(raw) else raw


class Bundler:
    def __init__(self, base: Path, max_width: int | None):
        self.base = base
        self.max_width = max_width
        self.inlined: list[tuple[str, int]] = []
        self.missing: list[str] = []

    def resolve(self, ref: str) -> Path | None:
        if EXTERNAL.match(ref):
            return None
        path = (self.base / ref.split("?")[0].split("#")[0]).resolve()
        if not path.is_file():
            self.missing.append(ref)
            return None
        return path

    def read(self, path: Path) -> bytes:
        raw = path.read_bytes()
        mime = mimetypes.guess_type(path.name)[0] or ""
        if self.max_width and mime in RASTER:
            raw = downscale(raw, mime, self.max_width)
        self.inlined.append((str(path.relative_to(self.base)) if path.is_relative_to(self.base)
                             else str(path), len(raw)))
        return raw

    def data_uri(self, path: Path) -> str:
        mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        return f"data:{mime};base64," + base64.b64encode(self.read(path)).decode()

    def text(self, path: Path) -> str:
        return self.read(path).decode("utf-8")

    # --- the four kinds of reference in a marp render ----------------------

    def do_scripts(self, html: str) -> str:
        def swap(m):
            path = self.resolve(m.group(2))
            if path is None:
                return m.group(0)
            body = self.text(path).replace("</script", r"<\/script")
            return f"<script{m.group(1)}{m.group(3)}>\n{body}\n</script>"

        return SCRIPT_TAG.sub(swap, html)

    def do_links(self, html: str) -> str:
        def swap(m):
            ref = m.group(1)
            if not ref.split("?")[0].endswith(".css"):
                return m.group(0)
            path = self.resolve(ref)
            if path is None:
                return m.group(0)
            return f"<style>\n{self.do_css(self.text(path))}\n</style>"

        return LINK_TAG.sub(swap, html)

    def do_src(self, html: str) -> str:
        def swap(m):
            path = self.resolve(m.group(1))
            return m.group(0) if path is None else f' src="{self.data_uri(path)}"'

        return SRC_ATTR.sub(swap, html)

    def do_css(self, css: str) -> str:
        def swap(m):
            path = self.resolve(m.group(2))
            return m.group(0) if path is None else f'url("{self.data_uri(path)}")'

        return CSS_URL.sub(swap, css)

    def run(self, html: str) -> str:
        html = self.do_scripts(html)
        html = self.do_links(html)
        html = self.do_src(html)
        return self.do_css(html)


def leftovers(html: str) -> list[str]:
    """Anything still pointing outside the file. A clean bundle has none."""
    refs = [m.group(1) for m in re.finditer(r"\s(?:src|href)=\"([^\"]+)\"", html)]
    refs += [m.group(2) for m in CSS_URL.finditer(html)]
    return sorted({r for r in refs if not EXTERNAL.match(r)})


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("deck", type=Path, help="deck .md (rendered first) or an existing .html")
    ap.add_argument("-o", "--out", type=Path, help="default: <deck>.standalone.html")
    ap.add_argument("--theme", type=Path, help="override the theme .css beside the deck")
    ap.add_argument("--max-width", type=int, metavar="PX",
                    help="downscale images wider than PX before encoding")
    args = ap.parse_args()

    deck = args.deck.resolve()
    if not deck.is_file():
        sys.exit(f"no such deck: {deck}")
    out = (args.out or deck.with_suffix("").with_suffix(".standalone.html")).resolve()

    tmp = None
    if deck.suffix == ".md":
        theme = (args.theme.resolve() if args.theme else find_theme(deck))
        tmp = Path(tempfile.mkdtemp(prefix="bundle_deck.")) / "render.html"
        render(deck, theme, tmp)
        source = tmp
    else:
        source = deck

    bundler = Bundler(deck.parent, args.max_width)
    html = bundler.run(source.read_text(encoding="utf-8"))
    out.write_text(html, encoding="utf-8")
    if tmp is not None:
        shutil.rmtree(tmp.parent, ignore_errors=True)

    for ref, size in sorted(bundler.inlined, key=lambda p: -p[1])[:5]:
        print(f"  {size / 1024:8.0f} KB  {ref}")
    print(f"inlined {len(bundler.inlined)} assets -> {out.name} "
          f"({out.stat().st_size / 1024 / 1024:.1f} MB)")

    remaining = leftovers(html) + bundler.missing
    if remaining:
        print("still points outside the file:", file=sys.stderr)
        for ref in sorted(set(remaining)):
            print(f"  {ref}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
