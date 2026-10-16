"""Grafik zu Modul 6: Stationen der Erinnerung 1796–1851, nach den Texten des Apparats.

Jede Station nennt ihren Beleg. Schreibt assets/plates/vizerinnerung.jpg und _t.jpg.
Lauf aus dem Repository:  python tools/viz-erinnerung.py
"""
import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "plates"
FRZ, KAIS, LAND, REZ, INK, MUTED = "#2b4f86", "#8a6d2f", "#3f6b3a", "#7a7064", "#231c22", "#7a7064"

# (Jahr, Text, Beleg, Farbe, Zeile)
EV = [
    (1796.73, "Begräbnis auf dem Petersberg,\nSalut vom Ehrenbreitstein", "Marceau [15]", FRZ, 1),
    (1797.73, "Verbrennung zum Jahrestag;\nGrabmal nach Kléber, Inschriften", "Erinnerung [1]–[3]", FRZ, 2),
    (1797.9, "Lavallées Lobrede, Paris", "Marceau [6]", FRZ, 3),
    (1816.5, "Byron, Childe Harold III:\n„Honour to Marceau!“", "Erinnerung [4]–[5]", REZ, 1),
    (1818.5, "Jourdan: das Fort „au pouvoir\ndes étrangers“", "Marceau [12]", FRZ, 3),
    (1819.0, "Abbruch der Pyramide für die Festung, Asche verweht", "Erinnerung [8]", KAIS, 2),
    (1820.95, "König Friedrich Wilhelm III.\nan Marceaus Schwester", "Erinnerung [9]", KAIS, 1),
    (1834.5, "Bleibtreu: der 19. Juni „ein Sieg\nder östreichischen Waffen“ in der Volksmeinung", "Kircheib [25]", LAND, 1),
    (1834.5, "Bleibtreu: Denkstein im Höchstenbacher Wald", "Erinnerung [6]", LAND, 3),
    (1851.5, "Stramberg: Schiefertafel bei Höchstenbach,\n„pleuré … de l'habitant“", "Erinnerung [7]", REZ, 2),
]


def main():
    n = len(EV)
    fig, ax = plt.subplots(figsize=(8.6, 0.62 * n + 1.4), dpi=150)
    fig.patch.set_facecolor("#f4efe6")
    ax.set_facecolor("#f4efe6")
    ax.set_xlim(0, 100); ax.set_ylim(-n - 0.9, 1.4)
    ax.axis("off")
    ax.text(0, 1.3, "Was erinnert wurde, 1796–1851", fontsize=12, color=INK, va="top")
    ax.plot([13, 13], [-n + 0.4, 0.2], color=INK, lw=1)
    for k, (x, t, ref, c, row) in enumerate(EV):
        y = -k
        ax.text(11, y, "nach 1815" if x == 1819.0 else str(int(x)), ha="right", va="center", fontsize=9, color=INK, weight="bold")
        ax.plot(13, y, "o", color=c, ms=7, zorder=3)
        ax.text(16, y, t.replace("\n", " "), ha="left", va="center", fontsize=8.6, color=INK)
        ax.text(100, y, ref, ha="right", va="center", fontsize=7.8, color=MUTED)
    ax.text(0, -n - 0.6, "Fast alle Stationen gelten Marceau. Für die Toten von Altenkirchen und Kircheib\n"
            "nennen die hier gelesenen Quellen kein Denkmal.",
            fontsize=7.8, color=MUTED, style="italic", va="center")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    im = Image.open(buf).convert("RGB")
    big = im.copy(); big.thumbnail((1600, 1600)); big.save(OUT / "vizerinnerung.jpg", quality=88)
    th = im.copy(); th.thumbnail((520, 520)); th.save(OUT / "vizerinnerung_t.jpg", quality=84)
    print("ok", big.size)


if __name__ == "__main__":
    main()
