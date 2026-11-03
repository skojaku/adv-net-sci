"""Make a single-file copy of the rendered deck: python3 make_standalone.py
Inlines scrub.js and every figures/*.png as a data: URI (figures shrunk to <=1600 px wide),
so the HTML works when uploaded alone (Brightspace). Input m07-random-walks.html, output m07-random-walks-standalone.html."""
import base64, io, re
from PIL import Image

SRC, OUT, MAXW = "m07-random-walks.html", "m07-random-walks-standalone.html", 1600
html = open(SRC, encoding="utf-8").read()

def png_uri(path):
    im = Image.open(path)
    if im.width > MAXW:
        im = im.resize((MAXW, round(im.height * MAXW / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

cache = {}
def sub(m):
    p = m.group(2)
    if p not in cache:
        cache[p] = png_uri(p)
    return m.group(1) + cache[p]

html = re.sub(r'''((?:src=|url\()["']?)(figures/[^"')\s>]+\.png)''', sub, html)
js = open("scrub.js", encoding="utf-8").read()
html = html.replace('<script src="scrub.js"></script>', "<script>" + js + "</script>")
open(OUT, "w", encoding="utf-8").write(html)
print(len(cache), "figures,", round(len(html) / 1e6, 1), "MB;", "external refs left:",
      len(re.findall(r'''(?:src=|url\()["']?(?!data:|http|#)[^"')\s>]*figures''', html)), "figures,",
      html.count('src="scrub.js"'), "scrub.js")
