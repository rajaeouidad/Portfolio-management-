"""
optimizer.py
------------
Optimisation Mean-Variance (Markowitz) sur les 11 titres du portefeuille.

Ne lit plus aucun fichier CSV : les cours de bourse viennent directement
du fichier Excel, via excel_loader.load_returns().
"""

import sys
import pathlib
import numpy as np
import pandas as pd
from scipy.optimize import minimize

sys.path.append(str(pathlib.Path(__file__).resolve().parent))
from excel_loader import load_returns  # <- lit directement Le_detail_...xlsx


def annualized_stats(returns: pd.DataFrame, freq: int = 252):
    """Rendement et volatilite annualises, et matrice de covariance annualisee."""
    mean_daily = returns.mean()
    cov_daily = returns.cov()
    mean_annual = mean_daily * freq
    cov_annual = cov_daily * freq
    vol_annual = np.sqrt(np.diag(cov_annual))
    return mean_annual, cov_annual, pd.Series(vol_annual, index=returns.columns)


def portfolio_performance(weights: np.ndarray, mean_annual: pd.Series, cov_annual: pd.DataFrame):
    ret = float(np.dot(weights, mean_annual))
    vol = float(np.sqrt(weights.T @ cov_annual.values @ weights))
    return ret, vol


def negative_sharpe(weights, mean_annual, cov_annual, rf):
    ret, vol = portfolio_performance(weights, mean_annual, cov_annual)
    return -(ret - rf) / vol


def min_variance(weights, mean_annual, cov_annual):
    _, vol = portfolio_performance(weights, mean_annual, cov_annual)
    return vol


def optimize_max_sharpe(mean_annual, cov_annual, rf=0.0308, bounds=(0, 0.20)):
    n = len(mean_annual)
    x0 = np.repeat(1 / n, n)
    constraints = ({"type": "eq", "fun": lambda w: np.sum(w) - 1},)
    bnds = tuple(bounds for _ in range(n))
    result = minimize(negative_sharpe, x0, args=(mean_annual, cov_annual, rf),
                       method="SLSQP", bounds=bnds, constraints=constraints)
    return result.x


def efficient_frontier(mean_annual, cov_annual, n_points=40, bounds=(0, 0.20)):
    n = len(mean_annual)
    target_returns = np.linspace(mean_annual.min(), mean_annual.max(), n_points)
    frontier_vol = []
    bnds = tuple(bounds for _ in range(n))

    for target in target_returns:
        constraints = (
            {"type": "eq", "fun": lambda w: np.sum(w) - 1},
            {"type": "eq", "fun": lambda w, t=target: portfolio_performance(w, mean_annual, cov_annual)[0] - t},
        )
        x0 = np.repeat(1 / n, n)
        result = minimize(min_variance, x0, args=(mean_annual, cov_annual),
                           method="SLSQP", bounds=bnds, constraints=constraints)
        frontier_vol.append(result.fun if result.success else np.nan)

    return target_returns, np.array(frontier_vol)


if __name__ == "__main__":
    returns = load_returns()
    mean_annual, cov_annual, vol_annual = annualized_stats(returns)

    print(f"Periode : {returns.index.min().date()} -> {returns.index.max().date()} "
          f"({len(returns)} jours de bourse)")
    print("\nVolatilite annualisee par titre :")
    print(vol_annual.sort_values(ascending=False).round(4))

    w_opt = optimize_max_sharpe(mean_annual, cov_annual)
    ret_opt, vol_opt = portfolio_performance(w_opt, mean_annual, cov_annual)
    print(f"\nPortefeuille Max Sharpe (poids <= 20%) :")
    for titre, w in zip(mean_annual.index, w_opt):
        if w > 0.001:
            print(f"  {titre:<20} {w*100:5.2f}%")
    print(f"  -> Rendement attendu : {ret_opt*100:.2f}% | Volatilite : {vol_opt*100:.2f}% "
          f"| Sharpe : {(ret_opt-0.0308)/vol_opt:.2f}")
