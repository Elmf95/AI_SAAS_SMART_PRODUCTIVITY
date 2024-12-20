import os
import sys
import pandas as pd
import sqlite3
import numpy as np

# Gestion dynamique des chemins : ROOT_DIR = racine du projet
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

# Import des chemins définis dans paths.py
from paths import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    CLEANED_DATA_DIR,
)

# Fichiers à nettoyer
files_to_clean = {
    "hr_dashboard_data": os.path.join(RAW_DATA_DIR, "hr_dashboard_data.csv"),
    "amazon_reviews": os.path.join(RAW_DATA_DIR, "Reviews.csv"),
    "project_tools": os.path.join(
        RAW_DATA_DIR, "SPMQA Data Visualization - Sheet1.csv"
    ),
    "task_assignment": os.path.join(RAW_DATA_DIR, "Task Categories.csv"),
    "cloud_metrics": os.path.join(RAW_DATA_DIR, "vmCloud_data.csv"),
    "amazon_reviews_db": os.path.join(RAW_DATA_DIR, "database.sqlite"),
}


# Fonction de nettoyage général
def clean_data(df):
    """Nettoie un DataFrame selon les étapes standard."""
    # 1. Supprimer les doublons
    df = df.drop_duplicates()

    # 2. Supprimer les colonnes ou lignes avec trop de valeurs manquantes
    missing_threshold = (
        0.4  # Supprimer les colonnes avec plus de 40% de valeurs manquantes
    )
    df = df.loc[:, df.isnull().mean() < missing_threshold]

    # Supprimer les lignes avec plus de 50% de données manquantes
    row_missing_threshold = 0.5
    df = df[df.isnull().mean(axis=1) < row_missing_threshold]

    # 3. Imputer les valeurs manquantes pour les colonnes restantes
    for col in df.select_dtypes(include=["float", "int"]).columns:
        df[col] = df[col].fillna(df[col].mean())  # Remplacer NaN par la moyenne

    for col in df.select_dtypes(include=["object"]).columns:
        df[col] = df[col].fillna("Inconnu")  # Remplacer NaN par "Inconnu"

    # 4. Standardiser les noms des colonnes
    df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

    # 5. Gestion des colonnes contenant des timestamps Unix et conversion en dates
    for col in df.columns:
        if df[col].dtype in [
            "int64",
            "float64",
        ]:  # Vérifier si la colonne est numérique
            # Vérifier si la colonne semble contenir un timestamp Unix valide
            if (
                df[col].max() > 1000000000
            ):  # Valeur typique pour un timestamp Unix valide
                try:
                    # Convertir le timestamp Unix en date
                    df[col] = pd.to_datetime(df[col], unit="s", errors="coerce")
                    # Gérer les dates incohérentes (comme 1970-01-01)
                    df[col] = df[col].apply(lambda x: np.nan if x.year == 1970 else x)
                except Exception:
                    pass  # Si la conversion échoue, on laisse les valeurs inchangées

    # 6. Corriger les types de données (par exemple, convertir les dates)
    for col in df.columns:
        if "date" in col or "time" in col:
            try:
                df[col] = pd.to_datetime(df[col], errors="coerce")
                # Gérer les dates incohérentes (comme 1970-01-01)
                df[col] = df[col].apply(lambda x: np.nan if x.year == 1970 else x)
            except Exception:
                pass  # Ignorer si la conversion échoue

    # 7. Gestion spéciale de la colonne `execution_time`
    if "execution_time" in df.columns:
        # Essayer de convertir `execution_time` en datetime
        df["execution_time"] = pd.to_datetime(df["execution_time"], errors="coerce")
        # Remplacer les dates invalides par NaT
        df["execution_time"] = df["execution_time"].apply(
            lambda x: np.nan if pd.isna(x) else x
        )

    return df


# Fonction pour nettoyer un fichier SQLite
def clean_sqlite(file_path, table_name, output_path):
    """Nettoie une table dans une base SQLite et enregistre le résultat."""
    try:
        print(f"Nettoyage de la table {table_name} dans {file_path}...")
        conn = sqlite3.connect(file_path)
        df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
        conn.close()

        df_cleaned = clean_data(df)

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df_cleaned.to_csv(output_path, index=False)
        print(f"Table nettoyée enregistrée : {output_path}")
    except Exception as e:
        print(f"Erreur lors du nettoyage de {file_path}: {e}")


# Processus principal
def main():
    # Nettoyer et sauvegarder chaque fichier
    for name, file_path in files_to_clean.items():
        if name == "amazon_reviews_db":  # Cas particulier pour la base SQLite
            output_path = os.path.join(PROCESSED_DATA_DIR, "amazon_reviews_cleaned.csv")
            clean_sqlite(file_path, "Reviews", output_path)
        else:
            output_path = os.path.join(PROCESSED_DATA_DIR, f"{name}_cleaned.csv")
            print(f"Traitement de {file_path}...")
            try:
                df = pd.read_csv(file_path)
                df_cleaned = clean_data(df)
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                df_cleaned.to_csv(output_path, index=False)
                print(f"Fichier nettoyé enregistré : {output_path}")
            except Exception as e:
                print(f"Erreur lors du traitement de {file_path}: {e}")


if __name__ == "__main__":
    main()
