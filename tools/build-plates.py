"""Tafeln: Bilder von Wikimedia Commons (nur mit Gemeinfreiheits- oder CC0-Vorlage auf der Dateiseite) und eigene
Grafiken (tools/viz-*.py). Schreibt assets/plates/<id>.jpg (max. 1600 px), <id>_t.jpg und data/plates.json.
Lauf aus dem Repository:  python tools/build-plates.py [ids…]
"""
import io
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "plates"
UA = {"User-Agent": "BeideTheile/0.1 (educational; pantaleonfassbender@gmail.com)"}
OK = re.compile(r"\{\{\s*(PD-|Licensed-PD|cc-zero|CC0)", re.I)

LEDE = "Bildnisse, Karten und Pläne aus gemeinfreien Beständen, und die Grafiken des Apparats. Jede Tafel nennt ihr Original."
LEDE_EN = "Portraits, maps and plans from public-domain holdings, and the apparatus's own graphics. Every plate names its original."
CREDIT = "Gemeinfreie Bilder über Wikimedia Commons, jeweils mit ihrem Original genannt; eigene Grafiken CC BY 4.0, Flüsse aus Natural Earth (gemeinfrei)."
CREDIT_EN = "Public-domain images via Wikimedia Commons, each named with its original; the apparatus's own graphics CC BY 4.0, rivers from Natural Earth (public domain)."

# id, Seite, Quelle ("commons:Datei" oder "viz:Datei"), Titel, Titel EN, Bildunterschrift, EN, Verweis
PLATES = [
    ("vizfeldzug", "kais", "viz:vizfeldzug", "Die Stellungen am 31. Mai 1796", "The positions on 31 May 1796",
     "Grafik des Apparats nach Jourdan (Mémoires, S. 22–23) und Erzherzog Carl (Grundsätze II, S. 46–47): Kléber bei Düsseldorf, Jourdans Hauptquartier in Kirchberg im Hunsrück, das Gros des Erzherzogs bei Baumholder, der Prinz von Württemberg zwischen Altenkirchen, Hachenburg und Dierdorf, seine Vorhut an der Sieg. Orte nach heutigen Koordinaten; Sieg und Lahn nur beschriftet.",
     "The apparatus's graphic after Jourdan (Mémoires, pp. 22–23) and Archduke Charles (Grundsätze II, pp. 46–47): Kléber at Düsseldorf, Jourdan's headquarters at Kirchberg in the Hunsrück, the Archduke's main body at Baumholder, the Prince of Württemberg between Altenkirchen, Hachenburg and Dierdorf, his advance guard on the Sieg. Places by today's coordinates; the Sieg and the Lahn only labelled.",
     "#/text/feldzug/plan/4"),
    ("carl", "kais", "commons:Archduke Charles of Austria (J.B. Seele, 1800).jpg", "Erzherzog Carl", "Archduke Charles",
     "Erzherzog Carl von Österreich, Bildnis von Johann Baptist Seele, 1800. 1796 führte er die kaiserliche Armee am Niederrhein; 1814 schrieb er die Geschichte dieses Feldzugs als Lehrbuch der Strategie.",
     "Archduke Charles of Austria, portrait by Johann Baptist Seele, 1800. In 1796 he commanded the Imperial army on the Lower Rhine; in 1814 he wrote the history of that campaign as a textbook of strategy.",
     "#/text/feldzug/kuendigung/3"),
    ("jourdan", "frz", "commons:JEAN BAPTISTE JOURDAN (1762-1833).jpg", "Jean-Baptiste Jourdan", "Jean-Baptiste Jourdan",
     "Jean-Baptiste Jourdan, Oberbefehlshaber der Sambre-und-Maas-Armee 1796, Bildnis von Julie Volpelière nach Horace Vernet, 1834. Seine Erinnerungen an den Feldzug erschienen 1818.",
     "Jean-Baptiste Jourdan, commander-in-chief of the Army of the Sambre and Meuse in 1796, portrait by Julie Volpelière after Horace Vernet, 1834. His memoirs of the campaign appeared in 1818.",
     "#/text/feldzug/kuendigung/1"),
    ("kleber", "frz", "commons:Louis Léopold Boilly - Portrait du général Jean-Baptiste Kléber (1753-1800) - P720 - Musée Carnavalet.jpg",
     "Jean-Baptiste Kléber", "Jean-Baptiste Kléber",
     "General Jean-Baptiste Kléber, Bildnis von Louis-Léopold Boilly, 1800, Musée Carnavalet, Paris. 1796 führte er den linken Flügel der Sambre-und-Maas-Armee über die Sieg.",
     "General Jean-Baptiste Kléber, portrait by Louis-Léopold Boilly, 1800, Musée Carnavalet, Paris. In 1796 he led the left wing of the Army of the Sambre and Meuse across the Sieg.",
     "#/text/feldzug/plan/5"),
    ("wuerttemberg", "kais", "commons:Ferdinand Württemberg Litho.jpg", "Ferdinand von Württemberg", "Ferdinand of Württemberg",
     "Prinz Ferdinand von Württemberg, Lithographie von Friedrich Lieder und Alois von Saar, um 1830. 1796 führte er den rechten Flügel der kaiserlichen Armee zwischen Lahn und Sieg.",
     "Prince Ferdinand of Württemberg, lithograph by Friedrich Lieder and Alois von Saar, about 1830. In 1796 he commanded the right wing of the Imperial army between the Lahn and the Sieg.",
     "#/text/feldzug/sieg/9"),
]


def api(params):
    q = urllib.parse.urlencode({**params, "format": "json"})
    req = urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers=UA)
    for wait in (0, 20, 60, 120):
        time.sleep(wait)
        try:
            return json.load(urllib.request.urlopen(req))
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
    raise RuntimeError("rate-limited")


def commons(fname):
    d = api({"action": "query", "titles": "File:" + fname, "prop": "imageinfo|revisions", "rvprop": "content",
             "rvslots": "main", "iiprop": "url", "iiurlwidth": "1600"})
    pg = next(iter(d["query"]["pages"].values()))
    if not OK.search(pg["revisions"][0]["slots"]["main"]["*"]):
        raise SystemExit(f"keine Gemeinfreiheits-/CC0-Vorlage: {fname}")
    ii = pg["imageinfo"][0]
    for wait in (0, 20, 60):
        time.sleep(wait)
        try:
            return urllib.request.urlopen(urllib.request.Request(ii.get("thumburl") or ii["url"], headers=UA)).read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
    raise RuntimeError("rate-limited")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    only = set(sys.argv[1:])
    meta = []
    for pid, side, src, t, t_en, c, c_en, cite in PLATES:
        kind, _, name = src.partition(":")
        url = "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(name.replace(" ", "_")) if kind == "commons" else ""
        source = f"Wikimedia Commons, {name}" if kind == "commons" else "Grafik des Apparats, CC BY 4.0"
        if kind == "commons" and (not only or pid in only):
            im = Image.open(io.BytesIO(commons(name))).convert("RGB")
            big = im.copy(); big.thumbnail((1600, 1600)); big.save(OUT / f"{pid}.jpg", quality=86)
            th = im.copy(); th.thumbnail((520, 520)); th.save(OUT / f"{pid}_t.jpg", quality=82)
            print("ok", pid, big.size)
            time.sleep(6)
        meta.append({"id": pid, "side": side, "titel": t, "titel_en": t_en, "caption": c, "caption_en": c_en,
                     "source": source, "url": url, "cite": cite})
    (ROOT / "data" / "plates.json").write_text(json.dumps({"lede": LEDE, "lede_en": LEDE_EN, "credit": CREDIT,
                                                           "credit_en": CREDIT_EN, "plates": meta}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
