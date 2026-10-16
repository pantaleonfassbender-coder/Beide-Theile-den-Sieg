"""Grafik zu Modul 2: das Gefecht bei Altenkirchen am 4. Juni 1796, nach Angeli (S. 77–81) und Carl (S. 53–56).

Orte nach ihren heutigen Koordinaten (gerundet, OpenStreetMap/Wikipedia); Wege der Kolonnen schematisch als
Pfeile zwischen den Orten, die die Quellen nennen, nicht als Straßenverlauf. Schreibt assets/plates/vizaltenkirchen.jpg
und _t.jpg. Lauf aus dem Repository:  python tools/viz-altenkirchen.py
"""
import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "plates"
BOX = (7.33, 7.90, 50.49, 50.78)  # lon0, lon1, lat0, lat1
FRZ, KAIS, INK = "#2b4f86", "#8a6d2f", "#231c22"

P = {
    "Uckerath": (7.369, 50.730), "Kircheib": (7.459, 50.709), "Weyerbusch": (7.551, 50.713),
    "Mehren": (7.510, 50.686), "Hilgenroth": (7.652, 50.737), "Altenkirchen": (7.646, 50.687),
    "Almersbach": (7.629, 50.674), "Schöneberg": (7.604, 50.665), "Kroppach": (7.736, 50.692),
    "Eichelhardt": (7.700, 50.718), "Wahlrod": (7.718, 50.649), "Hachenburg": (7.820, 50.661),
    "Höchstenbach": (7.743, 50.632), "Steinebach": (7.803, 50.611), "Freilingen": (7.834, 50.560),
    "Neustadt": (7.429, 50.621), "Dierdorf": (7.659, 50.549), "Molsberg": (7.967, 50.482),
}
# (Ort, Seite, Text, Ausrichtung)
LABELS = [  # (Ort, Seite, Text, dx, dy, ha)
    ("Uckerath", "frz", "Lager 3. Juni", 0.012, 0, "left"), ("Kircheib", "frz", "", 0, -0.011, "center"),
    ("Weyerbusch", "kais", "", -0.006, 0.010, "right"),
    ("Mehren", "frz", "", -0.012, 0, "right"), ("Hilgenroth", "frz", "", 0.012, 0, "left"),
    ("Altenkirchen", "kais", "", 0.012, 0.004, "left"),
    ("Almersbach", "kais", "", -0.006, -0.010, "left"),
    ("Schöneberg", "kais", "", -0.010, 0, "right"), ("Kroppach", "kais", "rechter Flügel", 0.012, 0, "left"),
    ("Eichelhardt", "kais", "1 Bat. Darmstädter", 0.012, 0, "left"), ("Wahlrod", "kais", "", 0.012, 0, "left"),
    ("Hachenburg", "frz", "Lefebvre am Abend", 0.012, 0, "left"), ("Höchstenbach", "kais", "", -0.012, 0, "right"),
    ("Steinebach", "kais", "Arrièregarde am Abend", 0.012, 0, "left"), ("Freilingen", "kais", "Nacht zum 5. Juni", 0.012, 0, "left"),
    ("Neustadt", "frz", "", -0.012, 0, "right"), ("Dierdorf", "frz", "Ney, Magazin", 0.012, 0, "left"),
]


def arrow(ax, pts, color, ls="-", lw=2.2):
    for a, b in zip(pts, pts[1:-1]):
        ax.plot([P[a][0], P[b][0]], [P[a][1], P[b][1]], color=color, lw=lw, ls=ls, zorder=2)
    a, b = pts[-2], pts[-1]
    ax.annotate("", xy=P[b], xytext=P[a], arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, shrinkA=4, shrinkB=6), zorder=2)


def main():
    fig, ax = plt.subplots(figsize=(9.2, 6.4), dpi=150)
    fig.patch.set_facecolor("#f4efe6")
    ax.set_facecolor("#f4efe6")
    # französische Kolonnen am 4. Juni (Angeli S. 78; Carl S. 53; Schels S. 148)
    arrow(ax, ["Kircheib", "Weyerbusch", "Altenkirchen"], FRZ, lw=3)
    arrow(ax, ["Weyerbusch", "Mehren", "Almersbach"], FRZ)
    arrow(ax, ["Weyerbusch", "Hilgenroth", "Kroppach"], FRZ)
    arrow(ax, ["Uckerath", "Neustadt", "Dierdorf"], FRZ, ls="--")
    # kaiserlicher Rückzug (Carl S. 56; Angeli S. 80–81)
    arrow(ax, ["Altenkirchen", "Wahlrod", "Höchstenbach", "Freilingen"], KAIS, ls=":")
    for name, side, txt, dx, dy, ha in LABELS:
        x, y = P[name]
        c = FRZ if side == "frz" else KAIS
        ax.plot(x, y, marker="s" if side == "frz" else "o", ms=6.5, color=c, zorder=3)
        lab = name + (f"\n{txt}" if txt else "")
        ax.text(x + dx, y + dy, lab, fontsize=7.6, ha=ha, va="center", color=INK, zorder=4)
    ax.text(7.345, 50.777, "Französisch: Lefebvre (Mitte) auf der Chaussee; Brunet (rechts) über Mehren\n"
            "gegen Almersbach; Soult (links) über Hilgenroth auf Kroppach; Ney über Neustadt gegen Dierdorf",
            fontsize=7.4, color=FRZ, va="top", style="italic")
    ax.text(7.345, 50.495, "Kaiserlich am Morgen (Angeli S. 77–78):\n"
            "Vorposten Kienmayer bei Weyerbusch bis 7 Uhr;\n"
            "O'Donell-Freikorps und Tiroler Jäger in Almersbach;\n"
            "1 Komp. Jordis bei Schöneberg, 11 Komp. Jordis\n"
            "auf den Höhen südlich Altenkirchen;\n"
            "Kaiser-Infanterie in der Stadt",
            fontsize=7.4, color=KAIS, va="bottom", style="italic")
    ax.set_xlim(BOX[0], BOX[1]); ax.set_ylim(BOX[2], BOX[3])
    ax.set_aspect(1 / 0.64)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#dacfc0")
    ax.set_title("Altenkirchen, 4. Juni 1796", fontsize=12, color=INK, loc="left")
    ax.plot([], [], color=FRZ, lw=2.2, label="französische Kolonnen (Angeli, Carl, Schels)")
    ax.plot([], [], color=KAIS, lw=2.2, ls=":", label="kaiserlicher Rückzug (Carl, Angeli)")
    ax.legend(loc="lower right", bbox_to_anchor=(1.0, 0.0), fontsize=7.6, frameon=False)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    im = Image.open(buf).convert("RGB")
    OUT.mkdir(parents=True, exist_ok=True)
    big = im.copy(); big.thumbnail((1600, 1600)); big.save(OUT / "vizaltenkirchen.jpg", quality=88)
    th = im.copy(); th.thumbnail((520, 520)); th.save(OUT / "vizaltenkirchen_t.jpg", quality=84)
    print("ok", big.size)


if __name__ == "__main__":
    main()
