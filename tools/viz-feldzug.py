"""Grafik zu Modul 1: die Stellungen am 31. Mai 1796 nach Jourdan (S. 22–23) und Carl (S. 46–47).

Flüsse Rhein, Mosel, Main aus Natural Earth (gemeinfrei, beim Bau geladen); Sieg und Lahn nur als Beschriftung an
der Mündung. Orte nach ihren heutigen Koordinaten (gerundet). Schreibt assets/plates/vizfeldzug.jpg und _t.jpg.
Lauf aus dem Repository:  python tools/viz-feldzug.py
"""
import io
import json
import urllib.request
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "plates"
NE = "https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_10m_rivers_lake_centerlines.geojson"
BOX = (6.3, 8.9, 49.45, 51.35)  # lon0, lon1, lat0, lat1
FRZ, KAIS, INK, RIVER = "#2b4f86", "#8a6d2f", "#231c22", "#7fa3bf"

# (Name, lon, lat, Seite, Text, Ausrichtung)
PLACES = [
    ("Düsseldorf", 6.78, 51.23, "frz", "Kléber mit Lefebvre und Collaud", "r"),
    ("Köln", 6.96, 50.94, "frz", "Infanteriereserve", "l"),
    ("Bonn", 7.10, 50.73, "frz", "", "l"),
    ("Koblenz", 7.60, 50.36, "frz", "Division Grenier", "r"),
    ("Kirchberg", 7.41, 49.94, "frz", "Hauptquartier Jourdans", "r"),
    ("Birkenfeld", 7.17, 49.65, "frz", "Division Marceau", "l"),
    ("Baumholder", 7.33, 49.62, "kais", "Gros des Erzherzogs", "r"),
    ("Altenkirchen", 7.65, 50.69, "kais", "Hauptcorps Württemberg", "l"),
    ("Hachenburg", 7.82, 50.66, "kais", "", "rd"),
    ("Dierdorf", 7.66, 50.55, "kais", "", "r"),
    ("Niederpleis", 7.23, 50.77, "kais", "Vorhut Kienmaier", "r"),
    ("Daaden", 7.97, 50.73, "kais", "Gottesheim", "ru"),
    ("Neuwied", 7.46, 50.43, "kais", "Finke", "l"),
]
LABELS = [("Rhein", 7.12, 50.55), ("Mosel", 6.55, 49.72), ("Sieg", 7.32, 50.83), ("Lahn", 8.02, 50.24), ("Hunsrück", 7.05, 49.80)]


def main():
    data = json.load(urllib.request.urlopen(urllib.request.Request(NE, headers={"User-Agent": "BeideTheile/0.1"})))
    fig, ax = plt.subplots(figsize=(8, 7.2), dpi=150)
    fig.patch.set_facecolor("#f4efe6")
    ax.set_facecolor("#f4efe6")
    for ft in data["features"]:
        if ft["properties"].get("name") not in ("Rhine", "Mosel", "Main"):
            continue
        g = ft["geometry"]
        for line in (g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]):
            xs = [c[0] for c in line]; ys = [c[1] for c in line]
            ax.plot(xs, ys, color=RIVER, lw=2.2, zorder=1)
    # Klébers Auftrag: über Düsseldorf an die Sieg
    ax.annotate("", xy=(7.25, 50.80), xytext=(6.85, 51.15),
                arrowprops=dict(arrowstyle="-|>", color=FRZ, lw=2, ls="--"), zorder=2)
    ax.text(6.36, 50.98, "Auftrag an Kléber:\nüber Düsseldorf an\nSieg und Lahn", color=FRZ, fontsize=8.5, style="italic")
    tri = [(7.65, 50.69), (7.82, 50.66), (7.66, 50.55), (7.65, 50.69)]
    ax.fill([p[0] for p in tri], [p[1] for p in tri], color=KAIS, alpha=0.18, zorder=1)
    for name, lon, lat, side, txt, al in PLACES:
        c = FRZ if side == "frz" else KAIS
        ax.plot(lon, lat, marker="s" if side == "frz" else "o", ms=7, color=c, zorder=3)
        label = name + (f"\n{txt}" if txt else "")
        dx = 0.04 if al.startswith("r") else -0.04
        dy = 0.04 if al == "ru" else -0.04 if al == "rd" else 0
        ax.text(lon + dx, lat + dy, label, fontsize=8, ha="left" if al.startswith("r") else "right", va="center", color=INK, zorder=4)
    for t, lon, lat in LABELS:
        ax.text(lon, lat, t, fontsize=9, color="#4d7290" if t != "Hunsrück" else "#7a7064", style="italic")
    ax.set_xlim(BOX[0], BOX[1]); ax.set_ylim(BOX[2], BOX[3])
    ax.set_aspect(1 / 0.64)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#dacfc0")
    ax.set_title("Die Stellungen am 31. Mai 1796", fontsize=12, color=INK, loc="left")
    ax.plot([], [], "s", color=FRZ, label="Sambre-und-Maas-Armee (nach Jourdan)")
    ax.plot([], [], "o", color=KAIS, label="Kaiserliche (nach Jourdan und Carl)")
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.16), fontsize=8, frameon=False)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    im = Image.open(buf).convert("RGB")
    OUT.mkdir(parents=True, exist_ok=True)
    big = im.copy(); big.thumbnail((1600, 1600)); big.save(OUT / "vizfeldzug.jpg", quality=88)
    th = im.copy(); th.thumbnail((520, 520)); th.save(OUT / "vizfeldzug_t.jpg", quality=84)
    print("ok", big.size)


if __name__ == "__main__":
    main()
