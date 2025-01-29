import os
import sys
import pandas as pd

# Gestion dynamique des chemins
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

# Import des chemins définis dans paths.py
from paths import OUTPUT_DIR, RECOMMENDATION_RESULTS_DIR

# Chargement du dataset enrichi avec les sentiments
sentiments_path = os.path.join(OUTPUT_DIR, "amazon_reviews_sentiments.csv")
sentiments_df = pd.read_csv(sentiments_path)

# Vérification des colonnes nécessaires
required_columns = ["productid", "avg_score", "num_reviews", "sentiment"]
for col in required_columns:
    if col not in sentiments_df.columns:
        raise ValueError(
            f"La colonne '{col}' est manquante dans amazon_reviews_sentiments.csv."
        )


# Fonction de recommandation
def generate_recommendations(df, min_reviews=5, sentiment_filter="positive"):
    """
    Génère des recommandations basées sur les sentiments des critiques.
    :param df: DataFrame contenant les sentiments.
    :param min_reviews: Nombre minimal de critiques pour inclure un produit.
    :param sentiment_filter: Sentiment à utiliser pour filtrer les critiques.
    :return: DataFrame avec les produits recommandés.
    """
    # Filtrer les produits avec un sentiment donné
    filtered_reviews = df[df["sentiment"].str.lower() == sentiment_filter.lower()]

    # Agréger les critiques par produit
    product_summary = (
        filtered_reviews.groupby("productid")
        .agg(
            total_reviews=("num_reviews", "sum"),
            avg_score=("avg_score", "mean"),
        )
        .reset_index()
    )

    # Filtrer les produits ayant un nombre minimal de critiques
    recommended_products = product_summary[
        product_summary["total_reviews"] >= min_reviews
    ]
    recommended_products = recommended_products.sort_values(
        by=["avg_score", "total_reviews"], ascending=False
    )

    return recommended_products


# Générer les recommandations
print("Génération des recommandations en cours...")
recommended_products_df = generate_recommendations(sentiments_df)

# Sauvegarder les recommandations
os.makedirs(RECOMMENDATION_RESULTS_DIR, exist_ok=True)
recommendations_file = os.path.join(
    RECOMMENDATION_RESULTS_DIR, "recommended_products.csv"
)
recommended_products_df.to_csv(recommendations_file, index=False)
print(f"Recommandations générées et sauvegardées dans {recommendations_file}.")

# Afficher un aperçu des recommandations
print("Aperçu des produits recommandés :")
print(recommended_products_df.head(10))
