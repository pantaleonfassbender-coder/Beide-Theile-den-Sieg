"""Tafel zu Modul 6: Ausschnitt der Kartenaufnahme der Rheinlande durch Tranchot und v. Müffling, Blatt Koblenz,
mit „Tombeau du Gal Marceau“ auf dem Petersberg, aus dem WMS-Dienst des LVermGeo Rheinland-Pfalz
(Datenlizenz Deutschland – Namensnennung 2.0; Nennung: ©GeoBasis-DE / LVermGeoRP (2026), dl-de/by-2-0,
http://www.lvermgeo.rlp.de [Daten bearbeitet]). Bearbeitung: Ausschnitt und Verkleinerung.
Schreibt assets/plates/petersberg.jpg und _t.jpg. Lauf aus dem Repository:  python tools/fetch-petersberg.py
"""
import io
import urllib.request
from pathlib import Path
from PIL import Image

OUT = Path(__file__).resolve().parent.parent / "assets" / "plates"
URL = ("https://geo4.service24.rlp.de/wms/hktm.fcgi?SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&LAYERS=rp_hktm"
       "&STYLES=&CRS=EPSG:4326&BBOX=50.355,7.565,50.380,7.605&WIDTH=1800&HEIGHT=1600&FORMAT=image/png")

im = Image.open(io.BytesIO(urllib.request.urlopen(URL).read())).convert("RGB")
big = im.copy(); big.thumbnail((1600, 1600)); big.save(OUT / "petersberg.jpg", quality=86)
th = im.copy(); th.thumbnail((520, 520)); th.save(OUT / "petersberg_t.jpg", quality=82)
print("ok", big.size)
