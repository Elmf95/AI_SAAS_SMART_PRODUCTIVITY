import os
import sys
import pandas as pd

# Gestion dynamique des chemins
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

# Import des chemins définis dans paths.py
from paths import PROCESSED_DATA_DIR, OUTPUT_DIR

# Chargement du dataset
reviews_path = os.path.join(PROCESSED_DATA_DIR, "amazon_reviews_summary.csv")
reviews_df = pd.read_csv(reviews_path)

# Affichage des colonnes disponibles pour validation
print("Colonnes disponibles dans le fichier :")
print(reviews_df.columns)

# Vérification des colonnes nécessaires
required_columns = ["productid", "avg_score", "num_reviews"]
if not all(col in reviews_df.columns for col in required_columns):
    raise ValueError(
        f"Les colonnes nécessaires {required_columns} sont manquantes dans amazon_reviews_summary.csv."
    )

# Analyse des scores moyens (avg_score)
print("Analyse des scores moyens en cours...")
reviews_df["sentiment"] = reviews_df["avg_score"].apply(
    lambda x: "positive" if x >= 4 else ("neutral" if 3 <= x < 4 else "negative")
)

# Sauvegarde des résultats enrichis
os.makedirs(OUTPUT_DIR, exist_ok=True)
output_file = os.path.join(OUTPUT_DIR, "amazon_reviews_sentiments.csv")
reviews_df.to_csv(output_file, index=False)
print(f"Analyse des sentiments terminée. Résultats sauvegardés dans {output_file}.")
