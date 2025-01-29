import os
import sys
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Gestion dynamique des chemins
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

# Import des chemins définis dans paths.py
from paths import PROCESSED_DATA_DIR, CLEANED_DATA_DIR, OUTPUT_DIR

# Chargement des datasets
roles_path = os.path.join(
    PROCESSED_DATA_DIR, "task_assignment_summary.csv"
)  # Rôles et tâches
tools_path = os.path.join(
    PROCESSED_DATA_DIR, "project_tools_summary.csv"
)  # Outils SaaS

roles_df = pd.read_csv(roles_path)
tools_df = pd.read_csv(tools_path)

# Diagnostic des colonnes disponibles
print("Colonnes disponibles dans tools_df :", tools_df.columns)
print("Extrait des données tools_df :", tools_df.head())

# Ajouter une colonne fictive 'tool_description' si elle est absente
if "tool_description" not in tools_df.columns:
    print("La colonne 'tool_description' est manquante. Ajout d'une colonne fictive.")
    tools_df["tool_description"] = tools_df["tool_name"] + " - Description fictive"

# Vérification et ajout de colonnes nécessaires pour roles_df
if "role_description" not in roles_df.columns:
    print("La colonne 'role_description' est manquante. Ajout d'une colonne fictive.")
    roles_df["role_description"] = roles_df["skill"] + " - Description par défaut"

# Vérification des colonnes nécessaires
required_role_columns = ["skill", "role_description"]
required_tool_columns = ["tool_name", "tool_description"]

if not all(col in roles_df.columns for col in required_role_columns):
    raise ValueError(
        f"Les colonnes {required_role_columns} sont manquantes dans roles_df."
    )
if not all(col in tools_df.columns for col in required_tool_columns):
    raise ValueError(
        f"Les colonnes {required_tool_columns} sont manquantes dans tools_df."
    )

# Vectorisation des descriptions d'outils avec TF-IDF
tfidf_vectorizer = TfidfVectorizer(stop_words="english")
tool_vectors = tfidf_vectorizer.fit_transform(tools_df["tool_description"])


def recommend_tools_for_role(role_name, top_n=10):
    """
    Recommande des outils SaaS en fonction du rôle spécifié.
    """
    # Trouver la description du rôle spécifié
    role_row = roles_df[
        roles_df["skill"] == role_name
    ]  # Utiliser "skill" comme nom de rôle
    if role_row.empty:
        raise ValueError(f"Le rôle '{role_name}' n'existe pas dans le dataset.")

    role_description = role_row.iloc[0]["role_description"]
    role_vector = tfidf_vectorizer.transform([role_description])

    # Calculer la similarité cosine entre le rôle et tous les outils
    similarities = cosine_similarity(role_vector, tool_vectors).flatten()

    # Trier les outils par similarité (ordre décroissant)
    top_indices = similarities.argsort()[::-1][:top_n]
    top_tools = tools_df.iloc[top_indices].copy()
    top_tools["similarity_score"] = similarities[top_indices]

    return top_tools[["tool_name", "tool_description", "similarity_score"]]


def save_recommendations(role_name, recommendations, output_file):
    """
    Sauvegarde les recommandations dans un fichier CSV.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    file_path = os.path.join(OUTPUT_DIR, output_file)
    recommendations.to_csv(file_path, index=False)
    print(f"Recommandations sauvegardées dans {file_path}")


# Exemple d'utilisation
if __name__ == "__main__":
    role_input = input("Entrez un rôle professionnel (par exemple, ADTK) : ")
    try:
        recommendations = recommend_tools_for_role(role_input)
        print(f"Recommandations pour le rôle '{role_input}' :\n", recommendations)

        # Sauvegarder dans un fichier
        output_file = f"recommendations_for_{role_input.replace(' ', '_')}.csv"
        save_recommendations(role_input, recommendations, output_file)

    except ValueError as e:
        print(f"Erreur : {e}")
