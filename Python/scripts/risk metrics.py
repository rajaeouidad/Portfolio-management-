"""
risk_metrics.py
----------------
Fonctions de calcul des indicateurs de risque et de performance
utilisés dans le TP (equivalent Python des formules Excel).

Ces fonctions reproduisent en code ce qui a ete fait "a la main"
dans les onglets VAR-COVAR, Beta et Comparaison PF-MASI du fichier Excel.
"""

import numpy as np


def rendement_annualise(rendement_hebdo_moyen: float, freq: int = 52) -> float:
    """Annualise un rendement hebdomadaire moyen (rendement geometrique)."""
    return (1 + rendement_hebdo_moyen) ** freq - 1


def ecart_type_annualise(ecart_type_hebdo: float, freq: int = 52) -> float:
    """Annualise un ecart-type hebdomadaire (racine du temps)."""
    return ecart_type_hebdo * np.sqrt(freq)


def beta(rendements_titre: np.ndarray, rendements_marche: np.ndarray) -> float:
    """Beta = Cov(titre, marche) / Var(marche)."""
    cov_matrix = np.cov(rendements_titre, rendements_marche)
    return cov_matrix[0, 1] / cov_matrix[1, 1]


def sharpe_ratio(rendement_ptf: float, taux_sans_risque: float, ecart_type_ptf: float) -> float:
    """Ratio de Sharpe = (Rp - Rf) / sigma_p."""
    return (rendement_ptf - taux_sans_risque) / ecart_type_ptf


def treynor_ratio(rendement_ptf: float, taux_sans_risque: float, beta_ptf: float) -> float:
    """Ratio de Treynor = (Rp - Rf) / beta_p."""
    return (rendement_ptf - taux_sans_risque) / beta_ptf


def jensen_alpha(rendement_ptf: float, taux_sans_risque: float,
                  beta_ptf: float, rendement_marche: float) -> float:
    """Alpha de Jensen = (Rp - Rf) - beta_p * (Rm - Rf) (CAPM)."""
    return (rendement_ptf - taux_sans_risque) - beta_ptf * (rendement_marche - taux_sans_risque)


def m2_measure(rendement_ptf: float, taux_sans_risque: float,
               ecart_type_ptf: float, ecart_type_marche: float, rendement_marche: float) -> float:
    """Mesure M2 : performance du PTF ajustee pour avoir le meme risque que le marche."""
    sharpe_p = sharpe_ratio(rendement_ptf, taux_sans_risque, ecart_type_ptf)
    return taux_sans_risque + sharpe_p * ecart_type_marche - rendement_marche


def tracking_error(rendements_ptf: np.ndarray, rendements_marche: np.ndarray) -> float:
    """Tracking Error = ecart-type des rendements actifs (Rp - Rm)."""
    ecarts = np.array(rendements_ptf) - np.array(rendements_marche)
    return np.std(ecarts, ddof=1)


def information_ratio(rendement_ptf: float, rendement_marche: float, te: float) -> float:
    """Ratio d'Information = (Rp - Rm) / Tracking Error."""
    return (rendement_ptf - rendement_marche) / te


if __name__ == "__main__":
    # Exemple de verification avec les chiffres finaux du TP (slide 15)
    rf = 0.0308
    rp, rm = 0.0082, 0.0901
    sigma_p, sigma_m = 0.14226, 0.14218
    beta_p = 0.99

    print("Sharpe PTF :", round(sharpe_ratio(rp, rf, sigma_p), 2))
    print("Treynor PTF :", round(treynor_ratio(rp, rf, beta_p), 3))
    print("Alpha de Jensen :", round(jensen_alpha(rp, rf, beta_p, rm) * 100, 2), "%")
