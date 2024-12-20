import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Gestion dynamique des chemins : ROOT_DIR = racine du projet
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

# Import des chemins définis dans paths.py
from paths import PROCESSED_DATA_DIR, ANALYSIS_DIR

# Création du dossier de sortie pour les analyses
os.makedirs(ANALYSIS_DIR, exist_ok=True)

# Fichiers nettoyés
files_to_analyze = {
    "hr_dashboard_data": os.path.join(
        PROCESSED_DATA_DIR, "hr_dashboard_data_cleaned.csv"
    ),
    "amazon_reviews": os.path.join(PROCESSED_DATA_DIR, "amazon_reviews_cleaned.csv"),
    "project_tools": os.path.join(PROCESSED_DATA_DIR, "project_tools_cleaned.csv"),
    "task_assignment": os.path.join(PROCESSED_DATA_DIR, "task_assignment_cleaned.csv"),
    "cloud_metrics": os.path.join(PROCESSED_DATA_DIR, "cloud_metrics_cleaned.csv"),
}


# Fonction pour l'analyse exploratoire
def exploratory_analysis(file_name, file_path):
    """Réalise une analyse exploratoire sur un fichier CSV."""
    print(f"Analyse exploratoire de {file_name}...")
    try:
        df = pd.read_csv(file_path)

        # Statistiques descriptives
        stats = df.describe(include="all").transpose()
        stats_file = os.path.join(ANALYSIS_DIR, f"{file_name}_stats.csv")
        stats.to_csv(stats_file)
        print(f"Statistiques descriptives sauvegardées : {stats_file}")

        # Visualisation des distributions
        for col in df.select_dtypes(include=["float", "int"]).columns:
            plt.figure(figsize=(8, 6))
            sns.histplot(df[col], kde=True, bins=30, color="blue")
            plt.title(f"Distribution de {col}")
            plt.xlabel(col)
            plt.ylabel("Fréquence")
            plt.grid(True)
            plot_file = os.path.join(
                ANALYSIS_DIR, f"{file_name}_{col}_distribution.png"
            )
            plt.savefig(plot_file)
            plt.close()
            print(f"Distribution de {col} sauvegardée : {plot_file}")

        # Matrice de corrélation
        if len(df.select_dtypes(include=["float", "int"]).columns) > 1:
            corr = df.corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
            plt.title(f"Matrice de corrélation - {file_name}")
            corr_file = os.path.join(ANALYSIS_DIR, f"{file_name}_correlation.png")
            plt.savefig(corr_file)
            plt.close()
            print(f"Matrice de corrélation sauvegardée : {corr_file}")

    except Exception as e:
        print(f"Erreur lors de l'analyse exploratoire de {file_name}: {e}")


# Processus principal
def main():
    for name, path in files_to_analyze.items():
        exploratory_analysis(name, path)


if __name__ == "__main__":
    main()
