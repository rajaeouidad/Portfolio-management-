"""
charts.py
---------
Genere les graphiques a partir des tableaux lus directement dans les
fichiers Excel (via excel_loader.py). Aucun fichier CSV n'est utilise.

A lancer depuis le dossier python/ :  python scripts/charts.py
"""

import sys
import pathlib
import matplotlib.pyplot as plt

sys.path.append(str(pathlib.Path(__file__).resolve().parent))
from excel_loader import (load_performance_titres, load_contributions_hebdo,
                           load_indicateurs_risque, load_rebalancement_history)

FIG_DIR = pathlib.Path(__file__).resolve().parent.parent / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams["figure.dpi"] = 130
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False


def plot_contribution_hebdo():
    df = load_contributions_hebdo()
    fig, ax = plt.subplots(figsize=(7, 4))
    x = range(len(df))
    width = 0.35
    ax.bar([i - width / 2 for i in x], df["contribution_ptf"], width, label="Portefeuille", color="#1f4e79")
    ax.bar([i + width / 2 for i in x], df["contribution_bench"], width, label="MASI 20", color="#c9a227")
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["semaine"])
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Contribution a la performance")
    ax.set_title("Contribution hebdomadaire a la performance : Portefeuille vs MASI 20")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / "contribution_hebdomadaire.png")
    plt.close(fig)


def plot_performance_par_titre():
    df = load_performance_titres().sort_values("performance_w3_w9")
    colors = ["#c0392b" if v < 0 else "#1f4e79" for v in df["performance_w3_w9"]]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(df["titre"], df["performance_w3_w9"], color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Performance W3 -> W9")
    ax.set_title("Performance individuelle des titres du portefeuille")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "performance_par_titre.png")
    plt.close(fig)


def plot_attribution_par_titre():
    df = load_performance_titres().sort_values("attribution")
    colors = ["#c0392b" if v < 0 else "#2e7d32" for v in df["attribution"]]
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.barh(df["titre"], df["attribution"], color=colors)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("Attribution a la performance")
    ax.set_title("Attribution de performance par titre (selection vs allocation)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "attribution_par_titre.png")
    plt.close(fig)


def plot_risque_rendement():
    df = load_performance_titres()
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(df["ecart_type"], df["performance_w3_w9"], s=df["poids_ptf"] * 1500,
               c="#1f4e79", alpha=0.7, edgecolors="white")
    for _, row in df.iterrows():
        ax.annotate(row["titre"], (row["ecart_type"], row["performance_w3_w9"]),
                    fontsize=8, xytext=(4, 4), textcoords="offset points")
    ax.axhline(0, color="black", linewidth=0.6)
    ax.set_xlabel("Ecart-type hebdomadaire du titre")
    ax.set_ylabel("Performance W3 -> W9")
    ax.set_title("Couple risque-rendement par titre (taille = poids dans le PTF)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "risque_rendement.png")
    plt.close(fig)


def plot_rebalancement(semaine: str):
    df = load_rebalancement_history()
    d = df[df["semaine"] == semaine]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    x = range(len(d))
    width = 0.35
    ax.bar([i - width / 2 for i in x], d["poids_avant"], width, label="Avant", color="#9fa8b0")
    ax.bar([i + width / 2 for i in x], d["poids_apres"], width, label="Apres", color="#1f4e79")
    ax.set_xticks(list(x))
    ax.set_xticklabels(d["titre"], rotation=45, ha="right")
    ax.set_ylabel("Poids dans le portefeuille")
    ax.set_title(f"Rebalancement du portefeuille - {semaine}")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"rebalancement_{semaine}.png")
    plt.close(fig)


def plot_indicateurs_risque():
    df = load_indicateurs_risque().dropna(subset=["masi20"])
    fig, ax = plt.subplots(figsize=(7, 5))
    x = range(len(df))
    width = 0.35
    ax.bar([i - width / 2 for i in x], df["portefeuille"], width, label="Portefeuille", color="#1f4e79")
    ax.bar([i + width / 2 for i in x], df["masi20"], width, label="MASI 20", color="#c9a227")
    ax.set_xticks(list(x))
    ax.set_xticklabels(df["indicateur"], rotation=30, ha="right")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title("Indicateurs de risque et de performance : Portefeuille vs MASI 20")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIG_DIR / "indicateurs_risque.png")
    plt.close(fig)


if __name__ == "__main__":
    plot_contribution_hebdo()
    plot_performance_par_titre()
    plot_attribution_par_titre()
    plot_risque_rendement()
    plot_rebalancement("W5")
    plot_rebalancement("W7")
    plot_indicateurs_risque()
    print(f"Graphes generes dans : {FIG_DIR}")
