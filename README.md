# Beide Theile den Sieg – Both Sides Claimed the Victory

Altenkirchen, Kircheib und Höchstenbach 1796: ein zweisprachiger Quellenapparat zu drei Gefechten an derselben Straße zwischen Sieg und Westerwald, am 4. Juni, 19. Juni und 19. September 1796. Gemeinfreie Drucke im deutschen, französischen oder englischen Original, mit eigener deutscher und englischer Übersetzung; Oberfläche Deutsch und Englisch.

Altenkirchen, Kircheib and Höchstenbach, 1796: a bilingual documentary apparatus on three actions along the same road between the Sieg and the Westerwald. Public-domain prints in the German, French or English original, with German and English translations; interface in German and English.

Der Titel ist ein Satz des Erzherzogs Carl über den 19. Juni: „Beide Theile eigneten sich den Sieg zu, beide hatten tapfer gekämpft und viel verloren.“ (*Grundsätze der Strategie*, II. Theil, Wien 1814, S. 98.)

Live: https://beide-theile-den-sieg.netlify.app/

**Stufe 1 abgeschlossen (Version 1.0.0, 16. Oktober 2026):** sechs Module mit 103 Stellen, 21 Tafeln, 25 Zeitleistenstationen und 18 Vergleiche.

1. *Der Feldzug am Niederrhein und die Territorien, 1795–1796* (Jourdan 1818, Erzherzog Carl 1814, Dahlhoff 1874, Bleibtreu 1834)
2. *Altenkirchen, 4. Juni 1796* (Jourdan, Carl, Klébers Meldungen bei Pajol 1877, Angeli 1896, Soult 1854, Schels 1841, Regimentsgeschichte Jordis 1812)
3. *Kircheib und Uckerath, 19. Juni 1796* (Carl, Angeli, Jourdan, Klébers zwei Briefe vom Tag, Pajol 1874, Krays Brief an seinen Bruder, Verlustverzeichnis 1877, der Augenzeuge Stockhausen bei Bleibtreu)
4. *Land und Leute: Requisition, Neutralität, Plünderung* (Jourdans Instruktion vom 26. Mai, Klébers Proklamation, National-Zeitung 1796, das Wiesbadener Tagebuch von W. Lautz, Neuwied bei Bleibtreu)
5. *Höchstenbach und Marceau, 19.–21. September 1796* (Angeli, Carl, Jourdan, Soult, das Journal des Hauptmanns Souhait vom Sterbebett in Altenkirchen, National-Zeitung, Stramberg 1851)
6. *Erinnerung* (Lavallée 1797, Sergent bei Stramberg, Byron 1816, Bleibtreu, Lautz)

Jede Stelle ist am Seitenbild gelesen, in der Schreibung des Drucks. Die Anmerkungen nennen die Widersprüche der Quellen (14.000 oder 40.000 Mann, 3.000 Gefangene oder zehn Kompanien, fünf Todesstunden Marceaus), die Gewalt beider Armeen gegen das Land, und was nur Gerücht oder spätere Ausschmückung ist. Was geprüft und nicht aufgenommen wurde, steht mit Begründung in `data/modules.json` und auf der Seite „Texte“.

## Zitieren

Fassbender, Pantaleon. *Beide Theile den Sieg. Altenkirchen, Kircheib und Höchstenbach 1796. Ein zweisprachiger Quellenapparat.* 2026. https://beide-theile-den-sieg.netlify.app/. Bitte zitieren Sie für jede wörtlich übernommene Stelle auch die gedruckte Quelle. Metadaten: `CITATION.cff`, `.zenodo.json`.

## Prüfen

```
python tools/verify.py
```

## Dateien

- `data/modules.json`: die Module, und was nicht aufgenommen wurde.
- `data/<modul>.json`: die Texte; `data/timeline.json`, `data/compare.json`, `data/plates.json`.
- `tools/`: die Bauskripte je Modul (`build-*.py`), die Grafiken (`viz-*.py`), die Tafeln (`build-plates.py`, `fetch-*.py`) und die Prüfung (`verify.py`).
- `index.html`, `app.js` (Hash-Routen, Sprachumschalter), `style.css`, `legal.html`, `_headers`.

Lokal: `python -m http.server` im Repository, dann `http://localhost:8000/`.

Das Begleitspiel, ein Hexspiel über die drei Gefechte für beide Seiten, entsteht im Repository *Beide-Theile-Spiel*: https://beide-theile-spiel.netlify.app/

## Lizenzen

Code MIT; redaktionelle Texte CC BY 4.0; Editionen und Übersetzungen CC0 1.0. Kartenausschnitte der Tranchot-Aufnahme: Geobasis NRW (dl-de/zero-2.0) und ©GeoBasis-DE / LVermGeoRP (dl-de/by-2-0). Siehe [LICENSES.md](LICENSES.md).
