# Portfolio-management-
Le dossier `excel/` contient l'intégralité du travail original 
Le dossier `python/` ne duplique aucune donnée : il lit directement
dans ces fichiers Excel à chaque exécution.

## Contenu de `python/scripts/`

| Fichier | Rôle |
|---|---|
| `excel_loader.py` | Ouvre les 2 fichiers Excel et extrait les tableaux (seul fichier à les lire) |
| `risk_metrics.py` | Formules de risque et de performance (Sharpe, Treynor, Alpha de Jensen, Tracking Error, Ratio d'Information) |
| `optimizer.py` | Optimisation de portefeuille selon Markowitz (SciPy), frontière efficiente |
| `charts.py` | Graphiques de performance, contribution et rebalancement |
| `plot_efficient_frontier.py` | Frontière efficiente avec positionnement du portefeuille réel |
| `plot_correlation.py` | Matrice de corrélation des rendements journaliers (686 jours, 2023-2025) |

## Lancer le projet

```bash
cd python
pip install -r requirements.txt
python scripts/charts.py
python scripts/plot_efficient_frontier.py
python scripts/plot_correlation.py
```

Les graphiques sont générés dans `python/figures/`.

## Méthodologie

1. **Sélection des valeurs** : analyse fondamentale (ratios boursiers, diagnostic
   financier, BFR) et sectorielle — 11 titres, 8 secteurs.
2. **Construction du portefeuille** : poids contraints selon le poids du titre
   dans le MASI 20.
3. **Gestion du risque** : matrice de variance-covariance, rebalancement par
   Solveur (semaines 5 et 7) pour aligner le risque du portefeuille sur le marché.
4. **Attribution de performance** : décomposition par titre (effet sélection
   vs effet allocation).
5. **Indicateurs de performance ajustée au risque** : Sharpe, Treynor, Alpha
   de Jensen, Ratio d'Information, Tracking Error.
6. **Prolongement quantitatif (Python)** : optimisation Mean-Variance
   (Markowitz) sur l'historique complet des cours, frontière efficiente,
   analyse de corrélation.
