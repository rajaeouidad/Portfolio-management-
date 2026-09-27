"""
plot_efficient_frontier.py
---------------------------
Trace la frontiere efficiente de Markowitz et y place : le portefeuille
Max Sharpe theorique, le portefeuille reel du TP, et chaque titre individuel.

A lancer depuis le dossier python/ : python scripts/plot_efficient_frontier.py
"""

import sys
import pathlib
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(str(pathlib.Path(__file__).resolve().parent))
from excel_loader import load_returns, load_performance_titres
from optimizer import annualized_stats, efficient_frontier, optimize_max_sharpe, portfolio_performance

FIG_DIR = pathlib.Path(__file__).resolve().parent.parent / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)


def main():
    returns = load_returns()
    mean_annual, cov_annual, vol_annual = annualized_stats(returns)
    rf = 0.0308

    target_returns, frontier_vol = efficient_frontier(mean_annual, cov_annual)

    w_opt = optimize_max_sharpe(mean_annual, cov_annual)
    ret_opt, vol_opt = portfolio_performance(w_opt, mean_annual, cov_annual)

    # Poids reels du TP, lus directement depuis l'Excel (pas de valeurs en dur)
    perf_titres = load_performance_titres().set_index("titre")
    correspondance = {"IAM": "IAM", "Sothema": "Sothema", "RISMA": "RISMA", "Sonasid": "Sonasid",
                       "ATW": "ATTIJARIWAFA BANK", "Sanlam": "Sanlam", "MarsaMaroc": "Marsa maroc",
                       "CimentsDuMaroc": "Ciments du Maroc", "LabelVie": "Label vie", "Tgcc": "Tgcc", "HPS": "HPS"}
    w_tp = np.array([perf_titres.loc[correspondance[t], "poids_ptf"] for t in mean_annual.index])
    ret_tp, vol_tp = portfolio_performance(w_tp, mean_annual, cov_annual)

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(frontier_vol, target_returns, color="#1f4e79", lw=2, label="Frontière efficiente (Markowitz)")
    ax.scatter(vol_annual, mean_annual, color="#9fa8b0", s=40, zorder=3, label="Titres individuels")
    for titre in mean_annual.index:
        ax.annotate(titre, (vol_annual[titre], mean_annual[titre]), fontsize=7,
                    xytext=(4, 2), textcoords="offset points", color="#555")

    ax.scatter([vol_opt], [ret_opt], color="#2e7d32", s=140, marker="*", zorder=4,
               label=f"Max Sharpe théorique (Sharpe={((ret_opt-rf)/vol_opt):.2f})")
    ax.scatter([vol_tp], [ret_tp], color="#c0392b", s=140, marker="D", zorder=4,
               label=f"Portefeuille réel du TP (Sharpe={((ret_tp-rf)/vol_tp):.2f})")

    ax.set_xlabel("Volatilité annualisée")
    ax.set_ylabel("Rendement annualisé attendu")
    ax.set_title("Frontière efficiente de Markowitz — 11 titres, 686 jours de bourse")
    ax.legend(fontsize=8, loc="upper left")
    ax.xaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
    ax.yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1.0))
    fig.tight_layout()
    fig.savefig(FIG_DIR / "frontiere_efficiente_markowitz.png", dpi=140)
    plt.close(fig)

    print("Graphe sauvegarde :", FIG_DIR / "frontiere_efficiente_markowitz.png")
    print(f"Portefeuille reel du TP  : rendement={ret_tp*100:.1f}%  vol={vol_tp*100:.1f}%  Sharpe={(ret_tp-rf)/vol_tp:.2f}")
    print(f"Max Sharpe theorique     : rendement={ret_opt*100:.1f}%  vol={vol_opt*100:.1f}%  Sharpe={(ret_opt-rf)/vol_opt:.2f}")


if __name__ == "__main__":
    main()
