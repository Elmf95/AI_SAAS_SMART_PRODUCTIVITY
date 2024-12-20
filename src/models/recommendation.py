import os
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Gestion dynamique des chemins : ROOT_DIR = racine du projet
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

# Import des chemins définis dans paths.py
from paths import (
    RAW_DATA_DIR,
    PROCESSED_DATA_DIR,
    CLEANED_DATA_DIR,
)


# Charger les données nécessaires
def load_data():
    task_data = pd.read_csv(os.path.join(PROCESSED_DATA_DIR, "task_data_enriched.csv"))
    satisfaction_data = pd.read_csv(
        os.path.join(PROCESSED_DATA_DIR, "satisfaction_summary.csv")
    )
    return task_data, satisfaction_data


# Modèle de recommandation basé sur le contenu
def content_based_recommendation():
    # Charger les données enrichies
    task_data, satisfaction_data = load_data()

    # Fusionner les données pour inclure les descriptions et évaluations des outils
    merged_data = task_data.merge(satisfaction_data, on="product_id", how="inner")

    # Vectoriser les descriptions d'outils SaaS pour créer des vecteurs TF-IDF
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(
        merged_data["description"]
    )  # Assurez-vous qu'une colonne 'description' existe

    # Calculer la similarité cosinus entre les outils
    cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Fonction de recommandation
    def recommend_tools(product_id, num_recommendations=5):
        # Trouver l'index du produit
        idx = merged_data.index[merged_data["product_id"] == product_id][0]

        # Obtenir les scores de similarité
        sim_scores = list(enumerate(cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Obtenir les indices des produits similaires
        top_indices = [i[0] for i in sim_scores[1 : num_recommendations + 1]]
        return merged_data.iloc[top_indices][["product_id", "name", "avg_rating"]]

    # Exemple d'utilisation
    product_id_to_recommend = 101  # À remplacer par un ID réel dans votre dataset
    recommendations = recommend_tools(product_id_to_recommend)
    print("Recommandations :")
    print(recommendations)


if __name__ == "__main__":
    content_based_recommendation()
