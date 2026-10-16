"""Grafik zu Modul 5: die letzten 60 Stunden Marceaus, 19.–21. September 1796, nach den Uhrzeiten der Quellen.

Jede Marke nennt ihre Quelle; die Todeszeiten stehen nebeneinander, ohne dass eine gewählt wird.
Schreibt assets/plates/vizmarceau.jpg und _t.jpg. Lauf aus dem Repository:  python tools/viz-marceau.py
"""
import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "plates"
FRZ, KAIS, INK, MUTED, DEATH = "#2b4f86", "#8a6d2f", "#231c22", "#7a7064", "#8a2f2f"


def h(day, hour):  # Stunden ab 19. Sept. 0 Uhr
    return (day - 19) * 24 + hour


# (Stunde, Text, Quelle, Zeile, Farbe)
EVENTS = [
    (h(19, 7), "Aufbruch von\nFreilingen", "Lavallée", 1, FRZ),
    (h(19, 10), "aus dem Wald von\nHöchstenbach", "Lavallée", 0, FRZ),
    (h(19, 19), "erster Verband", "Souhait", 1, FRZ),
    (h(20, 9), "Besuch Haddiks, Chirurgen", "Souhait", 1, KAIS),
    (h(21, 1), "diktiert seine letzten Verfügungen", "Souhait", 0, FRZ),
]
DEATHS = [
    (h(21, 3.2), "bald nach 3 Uhr", "Souhait (Journal, 21. Sept.)"),
    (h(21, 5), "5 Uhr morgens", "Jourdan (1818)"),
    (h(21, 18), "6 Uhr abends", "Stramberg (1851)"),
]


def main():
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=150)
    fig.patch.set_facecolor("#f4efe6")
    ax.set_facecolor("#f4efe6")
    ax.set_xlim(h(19, 4), h(21, 22)); ax.set_ylim(-3.2, 4.0)
    ax.axis("off")
    ax.plot([h(19, 4), h(21, 22)], [0, 0], color=INK, lw=1.2)
    for d in (19, 20, 21):
        for hh in (0, 6, 12, 18):
            x = h(d, hh)
            if x < h(19, 4):
                continue
            big = hh == 0
            ax.plot([x, x], [-0.18 if not big else -0.35, 0.18 if not big else 0.35], color=INK, lw=1.4 if big else 0.8)
            ax.text(x, -0.55, f"{hh} Uhr" if not big else f"{d}. Sept.", ha="center", va="top",
                    fontsize=7.4 if not big else 8.4, color=MUTED if not big else INK, weight="bold" if big else "normal")
    # Gefecht und Transport (ohne genaue Stunde)
    ax.axvspan(h(19, 10), h(19, 15), ymin=0.47, ymax=0.53, color=FRZ, alpha=0.25)
    ax.text(h(19, 10.6), 0.35, "Schuss; drei Stunden\nTransport (Souhait)", ha="left", va="bottom", fontsize=7.4, color=FRZ, style="italic")
    for x, t, src, row, c in EVENTS:
        y = 1.5 if row == 0 else 2.5
        ax.plot([x, x], [0.12, y - 0.15], color=c, lw=0.8, ls=":")
        ax.plot(x, 0, "o", color=c, ms=5)
        ax.text(x, y, f"{t}\n{src}", ha="left" if x < h(19, 11) else "center", va="bottom", fontsize=7.6, color=INK)
    for i, (x, t, src) in enumerate(DEATHS):
        y = -1.4 - 0.85 * (i % 2)
        ax.plot([x, x], [-0.12, y + 0.15], color=DEATH, lw=0.9)
        ax.plot(x, 0, "v", color=DEATH, ms=8)
        ax.text(x, y, f"† {t}\n{src}", ha=("right", "left", "center")[i], va="top", fontsize=7.6, color=DEATH)
    ax.text(h(19, 4), 3.95, "Marceaus letzte Stunden nach den Quellen, 19.–21. September 1796", fontsize=11.5, color=INK, va="top")
    ax.text(h(19, 4), -2.9, "Carl (1814): „starb nach einigen Tagen“; National-Zeitung (1796): „den 21sten“. Keine Quelle wird gewählt.",
            fontsize=7.6, color=MUTED, style="italic", va="bottom")
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    im = Image.open(buf).convert("RGB")
    big = im.copy(); big.thumbnail((1600, 1600)); big.save(OUT / "vizmarceau.jpg", quality=88)
    th = im.copy(); th.thumbnail((520, 520)); th.save(OUT / "vizmarceau_t.jpg", quality=84)
    print("ok", big.size)


if __name__ == "__main__":
    main()
