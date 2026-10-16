"""Grafik zu Modul 4: belegte Lieferungen und Beute 1796, nach Seiten, als Rechnungsbuch.

Nur Zahlen, die in den Texten des Apparats stehen; jede Zeile nennt ihren Beleg. Schreibt
assets/plates/vizland.jpg und _t.jpg. Lauf aus dem Repository:  python tools/viz-land.py
"""
import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "plates"
FRZ, KAIS, INK, MUTED = "#2b4f86", "#8a6d2f", "#231c22", "#7a7064"

# (Seite, Wann, Wo, Was, Beleg)
ROWS = [
    ("frz", "4. Juni", "Hachenburg", "12.000 Rationen gebackenes Brot, Mehl, Futter (vorgefunden)", "Altenkirchen [19]"),
    ("frz", "4. Juni", "Dierdorf", "600 Säcke Hafer, 150.000 Rationen Heu, Mehl, Brot (Magazin)", "Altenkirchen [23]"),
    ("frz", "6.–7. Juni", "Neuwied", "Brot, Fleisch, Fourage; etwa 1.000 Arbeiter für die Schanzen", "Land [5]"),
    ("frz", "Juli", "Wiesbaden", "für General Marceau täglich 20 Pfund Rindfleisch, ½ Kalb, ½ Hammel,\n2 Gänse, 12 Pfund Butter, 50–60 Flaschen Wein", "Land [8]"),
    ("frz", "Juli", "Amt Idstein", "200 Stück Hornvieh, 700 Malter Hafer; 66 Stück und 400 Malter\nmit 4.375 Gulden abgelöst", "Land [8]"),
    ("frz", "25. Juli", "Wiesbaden", "17 Bäcker: täglich 20.000 Pfund Brot, dazu 4.000 Pfund von der Stadt", "Land [8]"),
    ("kais", "20. Juni", "zwischen Wied und Sayn", "Roggenfelder für das Lager abgeschnitten", "Feldzug [14]; Land [12]"),
    ("kais", "Herbst", "Frankfurt, Mainz → Lahn", "alle 5 Tage 4.000 Zentner Mehl, 14.000 Malter Hafer;\n1.200 Wagen requiriert, Exekutionskommando bei Gmelin", "Land [6]"),
    ("kais", "Herbst", "Weyerbusch, Uckerath,\nLindler", "drei kaiserliche Magazine", "Land [7]"),
]


def main():
    fig, ax = plt.subplots(figsize=(10, 6.6), dpi=150)
    fig.patch.set_facecolor("#f4efe6")
    ax.set_facecolor("#f4efe6")
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.axis("off")
    ax.text(0, 98, "Was die Armeen 1796 nahmen: belegte Lieferungen", fontsize=13, color=INK, va="top")
    ax.text(0, 93.5, "Nur Zahlen aus den Texten des Apparats, jede mit ihrem Beleg. Keine Summe: die Quellen sind zu lückenhaft.",
            fontsize=8.2, color=MUTED, va="top", style="italic")
    y = 86
    heads = [(0, "wann"), (11, "wo"), (31, "was"), (86, "Beleg")]
    for x, h in heads:
        ax.text(x + 1.4, y, h, fontsize=8, color=MUTED, va="center")
    ax.plot([0, 100], [y - 2.2, y - 2.2], color="#dacfc0", lw=1)
    y -= 6
    last = None
    for side, when, where, what, ref in ROWS:
        c = FRZ if side == "frz" else KAIS
        if side != last:
            ax.text(0, y, "Sambre-und-Maas-Armee" if side == "frz" else "Kaiserliche Armee", fontsize=9.5, color=c, weight="bold", va="center")
            y -= 5
            last = side
        lines = max(what.count("\n"), where.count("\n")) + 1
        ax.add_patch(plt.Rectangle((0, y - 3.5 * lines + 0.3), 0.8, 3.5 * lines, color=c))
        ax.text(1.4, y, when, fontsize=8.2, color=INK, va="top")
        ax.text(12.4, y, where, fontsize=8.2, color=INK, va="top", linespacing=1.35)
        ax.text(32.4, y, what, fontsize=8.2, color=INK, va="top", linespacing=1.35)
        ax.text(87.4, y, ref, fontsize=7.6, color=MUTED, va="top")
        y -= 3.4 + 3.4 * lines
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    im = Image.open(buf).convert("RGB")
    big = im.copy(); big.thumbnail((1600, 1600)); big.save(OUT / "vizland.jpg", quality=88)
    th = im.copy(); th.thumbnail((520, 520)); th.save(OUT / "vizland_t.jpg", quality=84)
    print("ok", big.size)


if __name__ == "__main__":
    main()
