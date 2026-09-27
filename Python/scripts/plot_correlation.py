"""
plot_correlation.py
---------------------
Genere la heatmap de la matrice de correlation des rendements journaliers
des 11 titres, lus directement depuis le fichier Excel.

A lancer depuis le dossier python/ : python scripts/plot_correlation.py
"""

import sys
import pathlib
import matplotlib.pyplot as plt

sys.path.append(str(pathlib.Path(__file__).resolve().parent))
from excel_loader import load_returns

FIG_DIR = pathlib.Path(__file__).resolve().parent.parent / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    returns = load_returns()
    corr = returns.corr()

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(corr, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.columns)

    for i in range(len(corr)):
        for j in range(len(corr)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center",
                    fontsize=7, color="white" if abs(corr.iloc[i, j]) > 0.5 else "black")

    fig.colorbar(im, ax=ax, label="Corrélation")
    ax.set_title("Matrice de corrélation des rendements journaliers")
    fig.tight_layout()
    fig.savefig(FIG_DIR / "matrice_correlation.png", dpi=140)
    plt.close(fig)
    print("Graphe sauvegarde :", FIG_DIR / "matrice_correlation.png")

    avg_corr = (corr.sum().sum() - len(corr)) / (len(corr) ** 2 - len(corr))
    print(f"Correlation moyenne entre paires de titres : {avg_corr:.2f}")


if __name__ == "__main__":
    main()
