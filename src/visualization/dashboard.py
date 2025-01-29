import streamlit as st
import pandas as pd
import os
import sys

# Gestion dynamique des chemins
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

# Import des chemins définis dans paths.py
from paths import PROCESSED_DATA_DIR


# Fonction pour charger les datasets
def load_dataset(file_path):
    try:
        return pd.read_csv(file_path)
    except FileNotFoundError:
        st.error(f"Fichier introuvable : {file_path}")
        return None
    except Exception as e:
        st.error(f"Erreur lors du chargement de {file_path} : {e}")
        return None


# Liste des datasets enrichis et summary avec chemins dynamiques
datasets_enriched = {
    "Amazon Reviews": os.path.join(PROCESSED_DATA_DIR, "amazon_reviews_enriched.csv"),
    "HR Dashboard": os.path.join(PROCESSED_DATA_DIR, "hr_dashboard_enriched.csv"),
    "Project Tools": os.path.join(PROCESSED_DATA_DIR, "project_tools_enriched.csv"),
    "Task Assignment": os.path.join(PROCESSED_DATA_DIR, "task_assignment_enriched.csv"),
    "VM Cloud": os.path.join(PROCESSED_DATA_DIR, "vmCloud_enriched.csv"),
}

datasets_summary = {
    "Amazon Reviews": os.path.join(PROCESSED_DATA_DIR, "amazon_reviews_summary.csv"),
    "HR Dashboard": os.path.join(PROCESSED_DATA_DIR, "hr_dashboard_summary.csv"),
    "Project Tools": os.path.join(PROCESSED_DATA_DIR, "project_tools_summary.csv"),
    "Task Assignment": os.path.join(PROCESSED_DATA_DIR, "task_assignment_summary.csv"),
    "VM Cloud": os.path.join(PROCESSED_DATA_DIR, "vmcloud_summary.csv"),
}

# Interface utilisateur
st.title("Visualisation des Datasets Enrichis et Résumés")

dataset_type = st.radio("Choisissez le type de dataset :", ["Enrichi", "Résumé"])

if dataset_type == "Enrichi":
    selected_dataset = st.selectbox(
        "Sélectionnez un dataset enrichi :", list(datasets_enriched.keys())
    )
    file_path = datasets_enriched[selected_dataset]
else:
    selected_dataset = st.selectbox(
        "Sélectionnez un dataset résumé :", list(datasets_summary.keys())
    )
    file_path = datasets_summary[selected_dataset]

# Chargement et affichage du dataset
if file_path:
    st.write(f"### Dataset sélectionné : {selected_dataset} ({dataset_type.lower()})")
    dataset = load_dataset(file_path)

    if dataset is not None:
        st.write("Aperçu des données :")
        st.dataframe(dataset.head())

        # Options supplémentaires : statistiques, graphiques, etc.
        if st.checkbox("Afficher les statistiques descriptives"):
            st.write(dataset.describe())

        if st.checkbox("Afficher les colonnes disponibles"):
            st.write(dataset.columns.tolist())
