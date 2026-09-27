# Simulation de Gestion de Portefeuille 

Simulation de gestion active d'un portefeuille actions coté sur le marché marocain
(indice MASI 20), réalisée sur 10 semaines dans le cadre du cours de Gestion de
Portefeuille (ENCG) : sélection des titres, construction du portefeuille,
gestion du risque par optimisation sous contraintes, attribution de performance,
et calcul des indicateurs de performance ajustée au risque.

Le travail a été mené sur Excel (Solveur, matrice de variance-covariance), puis
prolongé en Python pour reproduire et enrichir l'analyse quantitative
(optimisation de Markowitz, frontière efficiente, matrice de corrélation).

## Résultats clés

| Indicateur           | Portefeuille | MASI 20 |
|-----------------------|:---:|:---:|
| Écart-type annualisé  | 14,23% | 14,22% |
| Bêta                  | 0,99 | 1,00 |
| Rendement annualisé   | 0,82% | 9,01% |
| Ratio de Sharpe       | -0,16 | 0,42 |
| Alpha de Jensen       | -8,17% | – |

Le portefeuille a été construit pour répliquer le risque du marché (bêta et
écart-type quasi identiques, via rebalancement par Solveur en semaines 5 et 7),
mais sous-performe le benchmark sur la période — analyse détaillée dans
`python/figures/`.

## Structure du projet

.
├── excel/
│ ├── Le_detail_du_projet_de_gestion_de_portfeuille.xlsx → toutes les données et calculs sources (Solveur, VAR-COVAR, argumentaires)
│ └── Le_recap_du_projet_de_gestion_de_portfeuille.xlsx → tableaux de synthèse (performance, risque, rebalancement)
└── python/
├── requirements.txt
├── scripts/ → code Python, lit directement les fichiers Excel ci-dessus
└── figures/ → graphiques générés par les scripts


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
6. **Prolongement quantitatif (Python)** : optimisation Mean-Variance
   (Markowitz) sur l'historique complet des cours, frontière efficiente,
   analyse de corrélation.
