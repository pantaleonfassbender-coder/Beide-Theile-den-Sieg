"""Tafel zu Modul 3: Ausschnitt der Kartenaufnahme der Rheinlande durch Tranchot und v. Müffling (1801–1828),
Uckerath bis Kircheib, aus dem WMS-Dienst Geobasis NRW (Lizenz dl-de/zero-2.0). Der untere Rand des Abrufs zeigt
ein anschließendes Blatt anderer Aufnahme und wird abgeschnitten. Schreibt assets/plates/tranchot.jpg und _t.jpg.
Lauf aus dem Repository:  python tools/fetch-tranchot.py
"""
import io
import urllib.request
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "assets" / "plates"
URL = ("https://www.wms.nrw.de/geobasis/wms_nw_tranchot?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&LAYERS=nw_tranchot"
       "&STYLES=&CRS=EPSG:4326&BBOX=50.69,7.34,50.75,7.49&WIDTH=2400&HEIGHT=1440&FORMAT=image/png")

im = Image.open(io.BytesIO(urllib.request.urlopen(URL).read())).convert("RGB")
w, h = im.size
im = im.crop((0, 0, w, int(h * 0.735)))
big = im.copy(); big.thumbnail((1600, 1600)); big.save(OUT / "tranchot.jpg", quality=86)
th = im.copy(); th.thumbnail((520, 520)); th.save(OUT / "tranchot_t.jpg", quality=82)
print("ok", big.size)
