# /// script
# requires-python = ">=3.10,<3.14"
# dependencies = ["pillow", "fonttools", "brotli"]
# ///
"""Make a single-file copy of the rendered deck: uv run make_standalone.py

Run it after `render.sh m08-embedding.md html`. Input m08-embedding.html, output
m08-embedding-standalone.html, which works when uploaded alone (Brightspace, the
lecture note) and offline. It inlines:
  - every <img> (figures/*.svg, the QR code, the WordNet PNG shrunk to 1100 px wide, as WebP)
  - the three animations (anim/*.html) as iframe srcdoc, each with its Source Sans 3
    fonts subset to the characters it uses and inlined as woff2
  - KaTeX's fonts, taken from the KaTeX copy inside marp-cli (same version as the CDN
    link marp writes), woff2 only
"""
import base64, html as htmlmod, io, mimetypes, re, subprocess, sys
from pathlib import Path

from fontTools import subset
from PIL import Image

SRC, OUT, MAXW = Path("m08-embedding.html"), Path("m08-embedding-standalone.html"), 1100
EXTERNAL = re.compile(r"^(data:|https?:|//|#|mailto:)")


def b64(raw, mime):
    return f"data:{mime};base64," + base64.b64encode(raw).decode()


def image_uri(path):
    mime = mimetypes.guess_type(path.name)[0]
    raw = path.read_bytes()
    if mime == "image/png":
        im = Image.open(path)
        if im.width > MAXW:  # a photo-like figure: shrink, and WebP keeps the alpha
            im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, "WEBP", quality=85, method=6)
            return b64(buf.getvalue(), "image/webp")
    return b64(raw, mime)


def font_uri(path, chars):
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["*"]
    font = subset.load_font(str(path), opts)
    sub = subset.Subsetter(opts)
    sub.populate(unicodes=sorted(ord(c) for c in chars))
    sub.subset(font)
    buf = io.BytesIO()
    subset.save_font(font, buf, opts)
    return b64(buf.getvalue(), "font/woff2")


def anim_srcdoc(path):
    text = path.read_text(encoding="utf-8")
    chars = set(htmlmod.unescape(text)) | {chr(c) for c in range(0x20, 0x7F)}
    chars |= {chr(int(h, 16)) for h in re.findall(r"\\u([0-9a-fA-F]{4})", text)}

    def font(m):
        return f"url({font_uri(path.parent / m.group(1), chars)}) format('woff2')"

    text = re.sub(r"url\((fonts/[^)]+\.otf)\)(?:\s*format\([^)]*\))?", font, text)
    return text.replace("&", "&amp;").replace('"', "&quot;")


def katex_fonts():
    root = subprocess.run(["npm", "root", "-g"], capture_output=True, text=True).stdout.strip()
    d = Path(root) / "@marp-team/marp-cli/node_modules/katex/dist/fonts"
    return d if d.is_dir() else None


page = SRC.read_text(encoding="utf-8")
base = SRC.parent.resolve()

# 1. images
cache = {}
def img(m):
    ref = m.group(1)
    if EXTERNAL.match(ref):
        return m.group(0)
    if ref not in cache:
        cache[ref] = image_uri((base / ref).resolve())
    return f'<img src="{cache[ref]}"'
page = re.sub(r'<img src="([^"]+)"', img, page)

# 2. animations
def frame(m):
    return f'<iframe{m.group(1)}srcdoc="{anim_srcdoc(base / m.group(2))}"'
page = re.sub(r'<iframe([^>]*?)src="(anim/[^"]+\.html)"', frame, page)

# 3. KaTeX fonts
kdir = katex_fonts()
version = re.search(r"katex@([0-9.]+)/dist/fonts", page)
if kdir is None or version is None:
    print("KaTeX fonts not found locally; the CDN links stay", file=sys.stderr)
else:
    have = re.search(r'"version":\s*"([^"]+)"', (kdir.parent.parent / "package.json").read_text()).group(1)
    if have != version.group(1):
        sys.exit(f"local KaTeX is {have}, the deck links {version.group(1)}")
    cdn = re.escape(f"https://cdn.jsdelivr.net/npm/katex@{have}/dist/fonts/")
    def kfont(m):
        return f'src:url({b64((kdir / (m.group(1) + ".woff2")).read_bytes(), "font/woff2")}) format("woff2")'
    page = re.sub(rf"src:url\('{cdn}([\w-]+)\.woff2'\) format\(\"woff2\"\)"
                  rf"(?:,\s*url\('{cdn}[\w.-]+'\) format\(\"\w+\"\))*", kfont, page)

OUT.write_text(page, encoding="utf-8")

left = [r for r in re.findall(r'\s(?:src|href)="([^"]+)"', page) if not EXTERNAL.match(r)]
left += [r for r in re.findall(r"url\(['\"]?([^'\")]+)", page) if not EXTERNAL.match(r)]
left += re.findall(r"https://cdn\.jsdelivr\.net[^'\")]*", page)
print(f"{len(cache)} images, 3 animations -> {OUT} ({OUT.stat().st_size / 1e6:.1f} MB)")
if left:
    print("still points outside the file:", *sorted(set(left)), sep="\n  ", file=sys.stderr)
    sys.exit(1)
