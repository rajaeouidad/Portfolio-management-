"""
excel_loader.py
----------------
Ce fichier est le SEUL endroit du projet qui ouvre les fichiers Excel.
Toutes les autres fonctions (risk_metrics.py, optimizer.py, charts.py)
appellent les fonctions d'ici pour obtenir leurs donnees -- elles n'ouvrent
jamais un fichier Excel elles-memes.

Deux fichiers sources, ranges dans le dossier excel/ (a la racine du repo,
a cote du dossier python/) :
  - Le_detail_du_projet_de_gestion_de_portfeuille.xlsx  -> cours de bourse (onglet "R-R PF")
  - Le_recap_du_projet_de_gestion_de_portfeuille.xlsx   -> tous les tableaux de synthese (onglet "Recap ")
"""

from pathlib import Path
import openpyxl
import pandas as pd

# --------------------------------------------------------------------------
# CHEMINS : on remonte depuis CE fichier (python/src/excel_loader.py)
# jusqu'a la racine du repo, puis on descend dans excel/
# --------------------------------------------------------------------------
RACINE = Path(__file__).resolve().parent.parent.parent
FICHIER_DETAIL = RACINE / "excel" / "Le_detail_du_projet_de_gestion_de_portfeuille.xlsx"
FICHIER_RECAP = RACINE / "excel" / "Le_recap_du_projet_de_gestion_de_portfeuille.xlsx"


def load_prices() -> pd.DataFrame:
    """Cours de cloture quotidiens des 11 titres (2023-2025).
    Source : Le_detail_...xlsx, onglet 'R-R PF', lignes 3 a 693."""
    df = pd.read_excel(FICHIER_DETAIL, sheet_name="R-R PF", header=1, usecols="A:L")
    df = df.rename(columns={"ATTIJARIWAFA BANK": "ATW", "Marsa maroc": "MarsaMaroc",
                             "Ciments du Maroc": "CimentsDuMaroc", "Label vie": "LabelVie"})
    df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
    df = df.dropna(subset=["Date"]).sort_values("Date").set_index("Date")
    df = df.apply(pd.to_numeric, errors="coerce")
    return df


def load_returns() -> pd.DataFrame:
    """Rendements journaliers (%) calcules a partir des cours de cloture."""
    prices = load_prices()
    return prices.pct_change().dropna()


def load_performance_titres() -> pd.DataFrame:
    """Table des 11 titres apres rebalancement : poids, performance,
    contribution, attribution, beta, ecart-type.
    Source : Recap.xlsx, onglet 'Recap ', lignes 41 a 51 (colonnes C a L)."""
    wb = openpyxl.load_workbook(FICHIER_RECAP, data_only=True)
    ws = wb["Recap "]
    lignes = []
    for r in range(41, 52):
        lignes.append({
            "titre": ws.cell(r, 4).value,
            "poids_masi": ws.cell(r, 5).value,
            "poids_ptf": ws.cell(r, 6).value,
            "performance_w3_w9": ws.cell(r, 7).value,
            "contrib_ptf": ws.cell(r, 8).value,
            "contrib_bench": ws.cell(r, 9).value if isinstance(ws.cell(r, 9).value, (int, float)) else 0.0,
            "attribution": ws.cell(r, 10).value,
            "beta": ws.cell(r, 11).value,
            "ecart_type": ws.cell(r, 12).value,
        })
    return pd.DataFrame(lignes)


def load_contributions_hebdo() -> pd.DataFrame:
    """Contribution hebdomadaire du portefeuille et du benchmark, W4 a W9.
    Source : Recap.xlsx, onglet 'Recap ', lignes 57 a 62 (colonnes D a F)."""
    wb = openpyxl.load_workbook(FICHIER_RECAP, data_only=True)
    ws = wb["Recap "]
    lignes = []
    for r in range(57, 63):
        lignes.append({
            "semaine": ws.cell(r, 4).value,
            "contribution_ptf": ws.cell(r, 5).value,
            "contribution_bench": ws.cell(r, 6).value,
        })
    return pd.DataFrame(lignes)


def load_indicateurs_risque() -> pd.DataFrame:
    """Indicateurs de risque et de performance : Portefeuille vs MASI 20.
    Source : Recap.xlsx, onglet 'Recap ', lignes 66 a 74 (colonnes D a F)."""
    wb = openpyxl.load_workbook(FICHIER_RECAP, data_only=True)
    ws = wb["Recap "]
    lignes = []
    for r in range(66, 75):
        lignes.append({
            "indicateur": ws.cell(r, 4).value,
            "portefeuille": ws.cell(r, 5).value,
            "masi20": ws.cell(r, 6).value,
        })
    df = pd.DataFrame(lignes)
    df["masi20"] = pd.to_numeric(df["masi20"], errors="coerce")  # les '-' deviennent NaN
    return df


# Correspondance entre les codes abreges utilises dans le tableau de
# rebalancement et les noms complets des titres (verifie manuellement
# a partir de l'ordre des colonnes dans le fichier Excel)
CODES_TITRES = {
    "IAM": "IAM", "LBV": "Label vie", "TGC": "Tgcc", "HPS": "HPS",
    "AWB": "ATTIJARIWAFA BANK", "SAH": "Sanlam", "MSA": "Marsa maroc",
    "CMA": "Ciments du Maroc", "SOT": "Sothema", "SID": "Sonasid", "RIS": "RISMA",
}


def load_rebalancement_history() -> pd.DataFrame:
    """Poids avant/apres pour les 2 rebalancements (semaine 5 et semaine 7).
    Source : Recap.xlsx, onglet 'Recap ', lignes 22-27 (S5) et 30-35 (S7)."""
    wb = openpyxl.load_workbook(FICHIER_RECAP, data_only=True)
    ws = wb["Recap "]
    lignes = []

    # Semaine 5 : codes en ligne 22, colonnes D a N (4 a 14)
    for col in range(4, 15):
        code = ws.cell(22, col).value
        if code:
            lignes.append({
                "semaine": "W5",
                "titre": CODES_TITRES.get(code, code),
                "poids_avant": ws.cell(26, col).value,
                "poids_apres": ws.cell(27, col).value,
            })

    # Semaine 7 : codes en ligne 30, colonnes D a N
    for col in range(4, 15):
        code = ws.cell(30, col).value
        if code:
            lignes.append({
                "semaine": "W7",
                "titre": CODES_TITRES.get(code, code),
                "poids_avant": ws.cell(34, col).value,
                "poids_apres": ws.cell(35, col).value,
            })

    return pd.DataFrame(lignes)


if __name__ == "__main__":
    print("=== Cours de cloture ===")
    print(load_prices().tail(3))
    print("\n=== Performance par titre ===")
    print(load_performance_titres())
    print("\n=== Contributions hebdo ===")
    print(load_contributions_hebdo())
    print("\n=== Indicateurs de risque ===")
    print(load_indicateurs_risque())
    print("\n=== Rebalancement ===")
    print(load_rebalancement_history())
