"""Grafik zu Modul 3: das Gefecht bei Kircheib und Uckerath am 19. Juni 1796, nach Pajol 1874 (S. 303–306),
Erzherzog Carl (S. 94–97) und Angeli (S. 116–117).

Orte nach ihren heutigen Koordinaten (gerundet, OpenStreetMap); Pfeile verbinden die Orte, die die Quellen nennen,
und zeigen keinen Wegverlauf. Schreibt assets/plates/vizkircheib.jpg und _t.jpg.
Lauf aus dem Repository:  python tools/viz-kircheib.py
"""
import io
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "plates"
BOX = (7.19, 7.60, 50.635, 50.815)
FRZ, KAIS, INK = "#2b4f86", "#8a6d2f", "#231c22"

P = {
    "Siegburg": (7.207, 50.793), "Hennef": (7.285, 50.775), "Blankenberg": (7.348, 50.769),
    "Uckerath": (7.369, 50.730), "Süchterscheid": (7.387, 50.748), "Jungeroth": (7.391, 50.705),
    "Meisenbach": (7.423, 50.714), "Kircheib": (7.459, 50.709), "Weyerbusch": (7.551, 50.713),
    "Buchholz": (7.393, 50.687), "Ruppichteroth": (7.483, 50.844),
}
LABELS = [  # (Ort, Seite, Text, dx, dy, ha)
    ("Siegburg", "frz", "Übergang am 20. Juni", 0.004, 0.012, "left"),
    ("Hennef", "frz", "", 0.006, 0.006, "left"),
    ("Blankenberg", "frz", "2 Bat.; fiel kampflos (Pajol)", 0.008, 0.006, "left"),
    ("Uckerath", "frz", "Lager, Quartier Klébers", -0.008, -0.004, "right"),
    ("Süchterscheid", "frz", "Leval (links)", 0.008, 0.002, "left"),
    ("Jungeroth", "frz", "", -0.008, 0.002, "right"),
    ("Meisenbach", "frz", "Vorposten; Bastoul (rechts)", 0.004, -0.009, "center"),
    ("Kircheib", "kais", "Kray: 2 Bat., 2 Komp. Tiroler,\nHöhen dahinter: Mylius", 0.006, 0.016, "left"),
    ("Weyerbusch", "kais", "Anmarsch ab 6 Uhr;\nUnterstützung hält hier", 0.0, -0.016, "center"),
]


def arrow(ax, a, b, color, ls="-", lw=2.2):
    ax.annotate("", xy=P[b], xytext=P[a],
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw, ls=ls, shrinkA=5, shrinkB=7), zorder=2)


def main():
    fig, ax = plt.subplots(figsize=(9.2, 6.4), dpi=150)
    fig.patch.set_facecolor("#f4efe6")
    ax.set_facecolor("#f4efe6")
    ax.plot([7.20, 7.29, 7.35, 7.42, 7.50, 7.58], [50.795, 50.783, 50.772, 50.776, 50.770, 50.776],
            color="#7fa3bf", lw=2.4, zorder=1)
    ax.text(7.50, 50.781, "Sieg (schematisch)", fontsize=7.6, color="#4d7290", style="italic")
    # Krays Vormarsch und Klébers Gegenangriff
    arrow(ax, "Weyerbusch", "Kircheib", KAIS, lw=2.6)
    arrow(ax, "Uckerath", "Kircheib", FRZ, lw=3)
    arrow(ax, "Uckerath", "Süchterscheid", FRZ)
    arrow(ax, "Jungeroth", "Meisenbach", FRZ)
    ax.annotate("", xy=P["Blankenberg"], xytext=(7.43, 50.765),
                arrowprops=dict(arrowstyle="-|>", color=KAIS, lw=1.8, ls="--", shrinkB=7), zorder=2)
    ax.text(7.432, 50.758, "Kolonne längs der Sieg\ngegen Blankenberg (Pajol)", fontsize=7.4, color=KAIS, style="italic")
    arrow(ax, "Uckerath", "Siegburg", FRZ, ls=":")
    for name, side, txt, dx, dy, ha in LABELS:
        x, y = P[name]
        c = FRZ if side == "frz" else KAIS
        ax.plot(x, y, marker="s" if side == "frz" else "o", ms=6.5, color=c, zorder=3)
        lab = name + (f"\n{txt}" if txt else "")
        ax.text(x + dx, y + dy, lab, fontsize=7.6, ha=ha, va="center", color=INK, zorder=4)
    ax.text(7.195, 50.638, "Uhrzeiten nach Pajol: 1 Uhr Überfall auf einen Vorposten · gegen 6 Uhr Kolonnen aus Weyerbusch ·\n"
            "gegen 8 Uhr Richepanse weicht · gegen 9 Uhr Angriff · 16 Uhr zurück im Lager. Kray: Angriff gegen 11 Uhr;\n"
            "Carl: Sturm gegen Mittag; Kléber: Ende 15 Uhr. Abzug in der Nacht, um 10 Uhr abends (Pajol).",
            fontsize=7.2, color=INK, va="bottom", style="italic")
    ax.set_xlim(BOX[0], BOX[1]); ax.set_ylim(BOX[2], BOX[3])
    ax.set_aspect(1 / 0.64)
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values():
        s.set_color("#dacfc0")
    ax.set_title("Kircheib und Uckerath, 19. Juni 1796", fontsize=12, color=INK, loc="left")
    ax.plot([], [], color=FRZ, lw=2.2, label="Kléber: Kolonnen; Rückzug über Siegburg (punktiert)")
    ax.plot([], [], color=KAIS, lw=2.2, label="Kray: Vorhut (Carl, Angeli, Kray)")
    ax.legend(loc="upper right", fontsize=7.6, frameon=False)
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", facecolor=fig.get_facecolor())
    im = Image.open(buf).convert("RGB")
    big = im.copy(); big.thumbnail((1600, 1600)); big.save(OUT / "vizkircheib.jpg", quality=88)
    th = im.copy(); th.thumbnail((520, 520)); th.save(OUT / "vizkircheib_t.jpg", quality=84)
    print("ok", big.size)


if __name__ == "__main__":
    main()
