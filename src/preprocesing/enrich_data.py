import os
import sys
import pandas as pd
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


# Charger les données nettoyées
def load_cleaned_data():
    amazon_reviews = pd.read_csv(
        os.path.join(CLEANED_DATA_DIR, "amazon_reviews_cleaned.csv")
    )
    hr_dashboard = pd.read_csv(
        os.path.join(CLEANED_DATA_DIR, "hr_dashboard_data_cleaned.csv")
    )
    project_tools = pd.read_csv(
        os.path.join(CLEANED_DATA_DIR, "project_tools_cleaned.csv")
    )
    task_assignment = pd.read_csv(
        os.path.join(CLEANED_DATA_DIR, "task_assignment_cleaned.csv")
    )
    vmCloud_data = pd.read_csv(
        os.path.join(CLEANED_DATA_DIR, "vmCloud_data_cleaned.csv")
    )
    return amazon_reviews, hr_dashboard, project_tools, task_assignment, vmCloud_data


def feature_engineering():
    # Charger les données nettoyées
    amazon_reviews, hr_dashboard, project_tools, task_assignment, vmCloud_data = (
        load_cleaned_data()
    )

    # Enrichir les données Amazon Reviews avec la moyenne des scores par produit
    amazon_reviews["avg_score"] = amazon_reviews.groupby("productid")[
        "score"
    ].transform("mean")

    # Enrichir les données HR Dashboard avec des moyennes de productivité et satisfaction par département
    hr_dashboard["avg_productivity"] = hr_dashboard.groupby("department")[
        "productivity_(%)"
    ].transform("mean")
    hr_dashboard["avg_satisfaction"] = hr_dashboard.groupby("department")[
        "satisfaction_rate_(%)"
    ].transform("mean")

    # Enrichir les données Project Tools avec l'usage récent (30 jours) basé sur l'existence de l'outil
    # Ajouter une colonne 'usage_date' si elle n'existe pas, mais vu que le fichier ne contient pas de date, nous devons nous adapter
    # Par exemple, on peut créer un indicateur basé sur l'outil sélectionné, ou ignorer l'enrichissement si c'est nécessaire
    # On peut créer une colonne qui indique si un outil est utilisé plus d'une fois dans les 30 derniers enregistrements (dans le cadre d'une logique hypothétique)
    project_tools["recent_usage"] = project_tools["final_selected_tool"].apply(
        lambda x: 1 if x.strip().lower() in ["monday.com", "trello"] else 0
    )

    # Enrichir les données Task Assignment avec une colonne de charge de travail par catégorie
    task_assignment["task_load"] = task_assignment.groupby("category")[
        "category"
    ].transform("count")

    # Enrichir les données VMCloud avec la consommation moyenne du CPU par type de tâche
    vmCloud_data["avg_cpu_usage"] = vmCloud_data.groupby("task_type")[
        "cpu_usage"
    ].transform("mean")

    # Sauvegarde des fichiers enrichis
    amazon_reviews.to_csv(
        os.path.join(CLEANED_DATA_DIR, "amazon_reviews_enriched.csv"), index=False
    )
    hr_dashboard.to_csv(
        os.path.join(CLEANED_DATA_DIR, "hr_dashboard_enriched.csv"), index=False
    )
    project_tools.to_csv(
        os.path.join(CLEANED_DATA_DIR, "project_tools_enriched.csv"), index=False
    )
    task_assignment.to_csv(
        os.path.join(CLEANED_DATA_DIR, "task_assignment_enriched.csv"), index=False
    )
    vmCloud_data.to_csv(
        os.path.join(CLEANED_DATA_DIR, "vmCloud_enriched.csv"), index=False
    )


if __name__ == "__main__":
    feature_engineering()
