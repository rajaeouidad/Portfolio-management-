#  Simulation de Gestion de Portefeuille Actions — MASI 20

**Gestion active d'un portefeuille de 11 valeurs cotées à la Bourse de Casablanca, sur 10 semaines, en conditions réelles de marché**

Étude complète combinant sélection de titres (analyse fondamentale et sectorielle), construction de portefeuille sous contraintes, gestion du risque par optimisation (Solveur Excel), attribution de performance, et prolongement quantitatif en Python (modèle de Markowitz, frontière efficiente).

---

##  Précision méthodologique

Le portefeuille a été construit pour **répliquer le risque du marché** (bêta et écart-type quasi identiques au MASI 20), et non pour maximiser le rendement  conformément à l'objectif du TP. Sur la période étudiée, il **sous-performe le benchmark** en rendement brut (voir tableau ci-dessous) ; l'analyse de la frontière efficiente en Python permet de situer précisément cet écart et d'identifier la marge d'optimisation restante.

---

## 📊 Résultats clés

| Indicateur | Portefeuille | MASI 20 |
|---|---|---|
| Écart-type annualisé | 14,23 % | 14,22 % |
| Bêta | 0,99 | 1,00 |
| Rendement annualisé | 0,82 % | 9,01 % |
| Ratio de Sharpe | -0,16 | 0,42 |
| Ratio de Treynor | -0,02 | 0,06 |
| Alpha de Jensen | -8,17 % | – |
| Ratio d'Information | 7,89 | – |
| Tracking Error | -1,04 % | – |

**Constat** : le rebalancement par Solveur a atteint son objectif d'alignement du risque (bêta et écart-type quasi identiques au marché), mais le portefeuille reste en retrait sur le rendement l'analyse Markowitz en Python quantifie précisément cette marge de progression.

---

##  Structure du projet

```
gestion-portefeuille-masi/
│
├── excel/
│   ├── Le_detail_du_projet_de_gestion_de_portfeuille.xlsx   → données et calculs sources (Solveur, VAR-COVAR, argumentaires par titre)
│   └── Le_recap_du_projet_de_gestion_de_portfeuille.xlsx    → tableaux de synthèse (performance, risque, rebalancement)
│
└── python/
    ├── requirements.txt
    ├── scripts/
    │   ├── excel_loader.py                  → lecture directe des 2 fichiers Excel (aucune donnée dupliquée)
    │   ├── risk_metrics.py                  → formules de risque et de performance (Sharpe, Treynor, Alpha de Jensen)
    │   ├── optimizer.py                     → optimisation de portefeuille selon Markowitz (SciPy)
    │   ├── charts.py                        → graphiques de performance, contribution, rebalancement
    │   ├── plot_efficient_frontier.py       → frontière efficiente avec positionnement du portefeuille réel
    │   └── plot_correlation.py              → matrice de corrélation des rendements journaliers
    └── figures/
        └── 9 graphiques générés (.png)
```

---

##  Méthodologie

1. **Sélection des valeurs** — analyse fondamentale (ratios boursiers : PER, PBR, DY) et diagnostic financier (autonomie financière, liquidité générale, ROE, BFR) sur 11 titres, 8 secteurs
2. **Construction du portefeuille** — poids contraints selon le poids de chaque titre dans le MASI 20 (max 10 %, 15 % ou 20 % selon les cas)
3. **Gestion du risque** — matrice de variance-covariance, rebalancement par Solveur Excel (semaines 5 et 7) pour aligner l'écart-type et le bêta du portefeuille sur ceux du marché
4. **Attribution de performance** — décomposition de la performance par titre (effet sélection vs effet allocation)
5. **Indicateurs de performance ajustée au risque** — Sharpe, Treynor, Alpha de Jensen, Ratio d'Information, Tracking Error
6. **Prolongement quantitatif (Python)** — optimisation Mean-Variance (Markowitz) sur 686 jours de cotation (2023-2025), frontière efficiente, matrice de corrélation inter-titres

Le détail complet des argumentaires par titre (faits marquants, catalyseurs 2025) est disponible dans les onglets dédiés du fichier Excel source.

---

## 🛠️ Outils utilisés

`Excel` (Solveur, matrice VAR-COVAR) · `Python` (NumPy, SciPy, Pandas, Matplotlib  ) · analyse fondamentale et diagnostic financier

---

## 📌 À propos

Projet académique réalisé dans le cadre du cours de Gestion de Portefeuille (ENCG, semestre 7), pour développer les compétences en gestion active de portefeuille, analyse quantitative du risque et optimisation
