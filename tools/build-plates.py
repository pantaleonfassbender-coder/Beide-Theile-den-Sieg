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

# Kartentafeln aus offenen Diensten (Bild von tools/fetch-*.py), Quelle und Fundort
WMS = {"tranchot": "Kartenaufnahme der Rheinlande durch Tranchot und v. Müffling (1801–1828), Geobasis NRW, dl-de/zero-2.0",
       "petersberg": "Kartenaufnahme der Rheinlande durch Tranchot und v. Müffling, Blatt Koblenz; ©GeoBasis-DE / LVermGeoRP (2026), dl-de/by-2-0, http://www.lvermgeo.rlp.de [Daten bearbeitet: Ausschnitt]"}
WMS_URL = {"tranchot": "https://www.wms.nrw.de/geobasis/wms_nw_tranchot", "petersberg": "http://www.lvermgeo.rlp.de"}

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
    ("vizaltenkirchen", "frz", "viz:vizaltenkirchen", "Altenkirchen, 4. Juni 1796", "Altenkirchen, 4 June 1796",
     "Grafik des Apparats nach Angeli (S. 77–81), Erzherzog Carl (Grundsätze II, S. 53–56) und Schels (S. 148): die vier französischen Kolonnen, die kaiserlichen Posten am Morgen und der Rückzug nach Freilingen. Orte nach heutigen Koordinaten; die Pfeile verbinden die Orte, die die Quellen nennen, und zeigen keinen Wegverlauf.",
     "The apparatus's graphic after Angeli (pp. 77–81), Archduke Charles (Grundsätze II, pp. 53–56) and Schels (p. 148): the four French columns, the Imperial posts in the morning and the retreat to Freilingen. Places by today's coordinates; the arrows join the places the sources name and do not show the line of the roads.",
     "#/text/altenkirchen/angriff/14"),
    ("bellange", "frz", "commons:Bataille d'Altenkirchen, 4 juin 1796.jpg", "Bellangé: Bataille d'Altenkirchen", "Bellangé: Bataille d'Altenkirchen",
     "Hippolyte Bellangé, Bataille d'Altenkirchen, 4 juin 1796, Gemälde 1838/39, Versailles. Ein Bild der Erinnerung, vierzig Jahre nach dem Gefecht gemalt, kein Augenzeugnis.",
     "Hippolyte Bellangé, Bataille d'Altenkirchen, 4 juin 1796, painting of 1838/39, Versailles. A picture of memory, painted forty years after the action, not an eyewitness record.",
     "#/text/altenkirchen/angriff/12"),
    ("lefebvre", "frz", "commons:Marechal-Lefebvre.jpg", "François-Joseph Lefebvre", "François-Joseph Lefebvre",
     "François-Joseph Lefebvre als Offizier der Revolution, Bildnis von Ferdinand Wachsmuth, 1834, Versailles. Am 4. Juni 1796 führte er die Vorhutdivision und die mittlere Kolonne gegen Altenkirchen.",
     "François-Joseph Lefebvre as an officer of the Revolution, portrait by Ferdinand Wachsmuth, 1834, Versailles. On 4 June 1796 he led the advance-guard division and the centre column against Altenkirchen.",
     "#/text/altenkirchen/angriff/13"),
    ("soult", "frz", "commons:Jean-de-Dieu Soult, maréchal duc de Dalmatie (1769-1851).jpg", "Jean-de-Dieu Soult", "Jean-de-Dieu Soult",
     "Jean-de-Dieu Soult als Marschall, Bildnis von Louis Henri de Rudder nach Jean Broc (1805), Versailles. 1796 führte er die linke Kolonne bei Altenkirchen; seine Erinnerungen erschienen 1854.",
     "Jean-de-Dieu Soult as marshal, portrait by Louis Henri de Rudder after Jean Broc (1805), Versailles. In 1796 he led the left column at Altenkirchen; his memoirs appeared in 1854.",
     "#/text/altenkirchen/angriff/18"),
    ("richepanse", "frz", "commons:Rioult - Antoine Richepance (1770-1802).jpg", "Antoine Richepanse", "Antoine Richepanse",
     "Antoine Richepanse, Bildnis von Louis Édouard Rioult, 1846, nach einem Familienbildnis, Musée de l'Armée. Kléber ernannte ihn am 4. Juni 1796 auf dem Schlachtfeld vorläufig zum Brigadegeneral.",
     "Antoine Richepanse, portrait by Louis Édouard Rioult, 1846, after a family portrait, Musée de l'Armée. Kléber made him provisional brigadier-general on the field on 4 June 1796.",
     "#/text/altenkirchen/zahlen/19"),
    ("vizkircheib", "kais", "viz:vizkircheib", "Kircheib und Uckerath, 19. Juni 1796", "Kircheib and Uckerath, 19 June 1796",
     "Grafik des Apparats nach Pajol (1874, S. 303–306), Erzherzog Carl (Grundsätze II, S. 94–97) und Angeli (S. 116–117): Klébers Lager bei Uckerath, Krays Vorhut von Weyerbusch, die drei französischen Kolonnen, die Kolonne gegen Blankenberg, und die Uhrzeiten, wie verschiedene Quellen sie nennen. Orte nach heutigen Koordinaten, die Sieg nur schematisch; Pfeile ohne Wegverlauf.",
     "The apparatus's graphic after Pajol (1874, pp. 303–306), Archduke Charles (Grundsätze II, pp. 94–97) and Angeli (pp. 116–117): Kléber's camp at Uckerath, Kray's advance guard from Weyerbusch, the three French columns, the column against Blankenberg, and the times as different sources give them. Places by today's coordinates, the Sieg only schematic; arrows without the line of the roads.",
     "#/text/kircheib/gefecht/12"),
    ("tranchot", "land", "wms:tranchot", "Uckerath und Kircheip auf der Tranchot-Karte", "Uckerath and Kircheip on the Tranchot map",
     "Ausschnitt der Kartenaufnahme der Rheinlande durch Tranchot und v. Müffling, aufgenommen 1801–1828, wenige Jahre nach dem Gefecht: links „Ukerath“, in der Mitte die Heide, auf der nach dem Augenzeugen Stockhausen die Franzosen lagerten („auf der Heide an der Marck“), rechts „Kircheip“ an der Straße nach Altenkirchen, dazwischen die Schluchten, die die Quellen nennen. Norden oben; die Blätter sind nicht nachgeglichen.",
     "Detail of the survey of the Rhineland by Tranchot and von Müffling, made 1801–1828, a few years after the action: on the left “Ukerath”, in the middle the heath on which, according to the eyewitness Stockhausen, the French camped (“auf der Heide an der Marck”), on the right “Kircheip” on the road to Altenkirchen, and between them the ravines the sources mention. North at the top; the sheets are not adjusted to each other.",
     "#/text/kircheib/uckerath/23"),
    ("kray", "kais", "commons:Portret van Paul Kray von Krajowa, RP-P-1908-5026.jpg", "Paul Kray", "Paul Kray",
     "Paul Kray von Krajowa, Stich von Carl Heinrich Rahl nach Joseph Anton Kapeller, Rijksmuseum Amsterdam. Am 19. Juni 1796 führte er die Vorhut des Erzherzogs gegen Kircheib; am Tag danach schrieb er seinem Bruder von einem „herrlichen Sieg“.",
     "Paul Kray von Krajowa, engraving by Carl Heinrich Rahl after Joseph Anton Kapeller, Rijksmuseum Amsterdam. On 19 June 1796 he led the Archduke's advance guard against Kircheib; the next day he wrote to his brother of a “glorious victory”.",
     "#/text/kircheib/gefecht/15"),
    ("ney", "frz", "commons:Michel Ney (1792).jpg", "Michel Ney", "Michel Ney",
     "Michel Ney als Unterleutnant der Husaren 1792, Bildnis von Adolphe Brune, 1834, Versailles. Am 19. Juni 1796 führte er als Generaladjutant Dragoner gegen Krays Reiterei; der Marschall des Kaiserreichs wurde er erst später.",
     "Michel Ney as a sub-lieutenant of hussars in 1792, portrait by Adolphe Brune, 1834, Versailles. On 19 June 1796, as adjutant-general, he led dragoons against Kray's cavalry; he became a marshal of the Empire only later.",
     "#/text/kircheib/gefecht/12"),
    ("vizland", "land", "viz:vizland", "Was die Armeen 1796 nahmen", "What the armies took in 1796",
     "Grafik des Apparats: die Lieferungen und Beuten, die in den Texten des Apparats mit Zahlen belegt sind, nach Seiten getrennt, jede mit ihrem Beleg. Keine Summe; die Quellen sind zu lückenhaft, und die Wiesbadener Zahlen betreffen nicht das Gebiet zwischen Sieg und Westerwald.",
     "The apparatus's graphic: the deliveries and captures documented with figures in the apparatus's texts, separated by side, each with its reference. No total; the sources are too incomplete, and the Wiesbaden figures do not concern the area between the Sieg and the Westerwald.",
     "#/text/land/lasten/5"),
    ("neuwied", "land", "commons:Neuwied 1784.jpg", "Neuwied, 1784", "Neuwied, 1784",
     "Neuwied aus der Vogelschau, Stich von 1784, Zeichner unbekannt: die Stadt mit ihren rechtwinklig angelegten Straßen, dahinter der Rhein. Zwölf Jahre später lag die Stadt zwischen den Fronten, die Franzosen auf der Rheininsel, die Österreicher in der Stadt.",
     "Neuwied from a bird's-eye view, engraving of 1784, artist unknown: the town with its streets laid out at right angles, the Rhine behind. Twelve years later the town lay between the lines, the French on the Rhine island, the Austrians in the town.",
     "#/text/land/stadt/12"),
    ("vizmarceau", "frz", "viz:vizmarceau", "Marceaus letzte Stunden", "Marceau's last hours",
     "Grafik des Apparats: die Uhrzeiten vom 19. bis 21. September 1796, wie Lavallée, Souhait, Jourdan und Stramberg sie nennen. Die drei Todeszeiten stehen nebeneinander; der Apparat wählt keine.",
     "The apparatus's graphic: the times from 19 to 21 September 1796 as Lavallée, Souhait, Jourdan and Stramberg give them. The three times of death stand side by side; the apparatus chooses none.",
     "#/text/marceau/tod/11"),
    ("marceau", "frz", "commons:Antoine-François Sergent, General Francois Severin Desgraviers Marceau, NGA 43328.jpg", "Marceau, Farbaquatinta von Sergent", "Marceau, colour aquatint by Sergent",
     "François-Séverin Marceau, Farbaquatinta von Antoine-François Sergent, National Gallery of Art, Washington. Die Unterschrift nennt ihn „né à Chartres, soldat à XVI ans, général à XXIII, mort à XXVII“ und sein Grab im „fort Pétersberg (auj. Fort Marceau)“. Sergent widmete ein zweites Blatt „à son épouse Emira Marceau“ (siehe die folgende Tafel); die Bilder entstanden in Marceaus Familie.",
     "François-Séverin Marceau, colour aquatint by Antoine-François Sergent, National Gallery of Art, Washington. The legend calls him “born at Chartres, soldier at 16, general at 23, dead at 27” and names his grave in the “fort Pétersberg (now Fort Marceau)”. Sergent dedicated a second sheet “to his wife Emira Marceau” (see the next plate); the images came from Marceau's family.",
     "#/text/marceau/schuss/5"),
    ("grabmal", "frz", "commons:A la mémoire du général Marceau mort de ses blessures à Altenkirchen, agé de XXVII ans, l'an IV de la République française... - estampe - gravé par Sergent et offert à son épouse Emira Marceau - btv1b84126268.jpg",
     "„A la mémoire du général Marceau“, 1797", "“A la mémoire du général Marceau”, 1797",
     "Aquatinta von Sergent, 1797, Bibliothèque nationale de France: ein Grabmal unter Kiefern in einer Landschaft, davor trauernde Frauen und ein Soldat. Die Inschrift: „mort de ses blessures à Altenkirchen, âgé de XXVII ans“. Ein erdachtes Bild, kein Abbild des Grabes auf dem Petersberg.",
     "Aquatint by Sergent, 1797, Bibliothèque nationale de France: a tomb under pines in a landscape, with mourning women and a soldier. The inscription: “died of his wounds at Altenkirchen, aged 27”. An imagined picture, not a likeness of the grave on the Petersberg.",
     "#/text/marceau/ehren/15"),
    ("petersberg", "rezeption", "wms:petersberg", "„Tombeau du Gal Marceau“ auf der Tranchot-Karte", "“Tombeau du Gal Marceau” on the Tranchot map",
     "Ausschnitt der Kartenaufnahme der Rheinlande durch Tranchot und v. Müffling, Blatt Koblenz, aufgenommen in den ersten Jahren nach 1800: auf dem Petersberg nördlich der Mosel „Tombeau du Gal Marceau“, darunter „Sepulture du Gal Hoche“, gegenüber die Stadt Koblenz. Die Karte zeigt das Grabmal an seinem ursprünglichen Ort, vor dem Festungsbau. Norden oben.",
     "Detail of the survey of the Rhineland by Tranchot and von Müffling, sheet Koblenz, made in the first years after 1800: on the Petersberg north of the Moselle “Tombeau du Gal Marceau”, below it “Sepulture du Gal Hoche”, opposite the town of Koblenz. The map shows the tomb in its original place, before the fortress was built. North at the top.",
     "#/text/erinnerung/grab/2"),
    ("vizerinnerung", "rezeption", "viz:vizerinnerung", "Was erinnert wurde, 1796–1851", "What was remembered, 1796–1851",
     "Grafik des Apparats: die Stationen der Erinnerung in den Texten dieses Apparats, jede mit ihrem Beleg. Fast alle gelten Marceau; für die Toten der Gefechte bei Altenkirchen und Kircheib nennen die hier gelesenen Quellen kein Denkmal.",
     "The apparatus's graphic: the stations of memory in this apparatus's texts, each with its reference. Almost all concern Marceau; for the dead of the actions at Altenkirchen and Kircheib the sources read here name no memorial.",
     "#/text/erinnerung/grab/1"),
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
        url = "https://commons.wikimedia.org/wiki/File:" + urllib.parse.quote(name.replace(" ", "_")) if kind == "commons" else WMS_URL.get(name, "")
        source = f"Wikimedia Commons, {name}" if kind == "commons" else WMS.get(name, "Grafik des Apparats, CC BY 4.0")
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
