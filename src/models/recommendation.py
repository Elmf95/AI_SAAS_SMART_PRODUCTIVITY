import os
import sys
import pandas as pd

# Gestion dynamique des chemins : ROOT_DIR = racine du projet
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

# Import des chemins définis dans paths.py
from paths import PROCESSED_DATA_DIR, CLEANED_DATA_DIR

# Définition des fichiers
DATASETS = {
    "amazon_reviews": {
        "enriched": "amazon_reviews_enriched.csv",
        "summary": "amazon_reviews_summary.csv",
    },
    "hr_dashboard": {
        "enriched": "hr_dashboard_enriched.csv",
        "summary": "hr_dashboard_summary.csv",
    },
    "project_tools": {
        "enriched": "project_tools_enriched.csv",
        "summary": "project_tools_summary.csv",
    },
    "task_assignment": {
        "enriched": "task_assignment_enriched.csv",
        "summary": "task_assignment_summary.csv",
    },
    "vmCloud": {"enriched": "vmCloud_enriched.csv", "summary": "vmcloud_summary.csv"},
}


# Fonction pour charger un fichier et effectuer une analyse
def analyze_dataset(dataset_name, file_path):
    print(f"Analyse du dataset : {dataset_name} (fichier : {file_path})")

    if not os.path.exists(file_path):
        print(
            f"Le fichier {file_path} n'existe pas. Vérifiez le chemin et réessayez.\n"
        )
        return

    try:
        # Charger le fichier
        df = pd.read_csv(file_path)

        # Exemple simple d'analyse : statistiques générales
        print(f"--- Statistiques pour {dataset_name} ---\n")
        stats = df.describe(include="all").transpose()
        print(stats, "\n")

        # Identifier les colonnes avec valeurs manquantes
        missing_data = df.isnull().sum()
        missing_columns = missing_data[missing_data > 0].sort_values(ascending=False)
        if not missing_columns.empty:
            print(
                f"Colonnes avec valeurs manquantes pour {dataset_name} :\n{missing_columns}\n"
            )
        else:
            print(f"Aucune valeur manquante détectée dans {dataset_name}.\n")

        # Identifier les doublons éventuels
        duplicate_rows = df.duplicated().sum()
        if duplicate_rows > 0:
            print(f"{duplicate_rows} doublons détectés dans {dataset_name}.\n")
        else:
            print(f"Aucun doublon détecté dans {dataset_name}.\n")

        # Aperçu des premières lignes
        print(f"--- Aperçu des 5 premières lignes de {dataset_name} ---")
        print(df.head(), "\n")
    except pd.errors.EmptyDataError:
        print(f"Le fichier {file_path} est vide. Impossible d'effectuer l'analyse.\n")
    except Exception as e:
        print(f"Erreur lors de l'analyse de {dataset_name} : {e}")


# Fonction pour sauvegarder un rapport sous format CSV
def save_report(stats, missing_columns, duplicate_rows, dataset_name):
    output_dir = os.path.join(ROOT_DIR, "reports")
    os.makedirs(output_dir, exist_ok=True)
    report_path = os.path.join(output_dir, f"{dataset_name}_report.csv")

    # Sauvegarde des statistiques
    try:
        stats["missing_values"] = missing_columns
        stats["duplicates"] = duplicate_rows
        stats.to_csv(report_path)
        print(f"Rapport sauvegardé dans : {report_path}\n")
    except Exception as e:
        print(f"Erreur lors de la sauvegarde du rapport : {e}")


# Processus principal
def main():
    print("Démarrage du traitement des datasets...\n")

    for dataset_name, files in DATASETS.items():
        enriched_file = os.path.join(CLEANED_DATA_DIR, files["enriched"])
        summary_file = os.path.join(PROCESSED_DATA_DIR, files["summary"])

        # Analyse des fichiers enriched
        print(f"--- Traitement du fichier ENRICHED pour {dataset_name} ---")
        analyze_dataset(dataset_name + " (enriched)", enriched_file)

        # Analyse des fichiers summary
        print(f"--- Traitement du fichier SUMMARY pour {dataset_name} ---")
        analyze_dataset(dataset_name + " (summary)", summary_file)


if __name__ == "__main__":
    main()
