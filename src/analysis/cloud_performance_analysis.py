import os
import sys
import pandas as pd

# Gestion dynamique des chemins
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

from paths import PROCESSED_DATA_DIR, RECOMMENDATION_RESULTS_DIR

performance_data_path = os.path.join(PROCESSED_DATA_DIR, "vmCloud_enriched.csv")
recommended_products_path = os.path.join(
    RECOMMENDATION_RESULTS_DIR, "recommended_products.csv"
)

if not os.path.exists(performance_data_path):
    raise FileNotFoundError(f"Fichier introuvable : {performance_data_path}")
if not os.path.exists(recommended_products_path):
    raise FileNotFoundError(f"Fichier introuvable : {recommended_products_path}")

performance_data = pd.read_csv(performance_data_path)
recommendations = pd.read_csv(recommended_products_path)

required_columns_performance = [
    "cpu_usage",
    "memory_usage",
    "network_traffic",
    "power_consumption",
    "execution_time",
]

missing_columns_performance = [
    col for col in required_columns_performance if col not in performance_data.columns
]
if missing_columns_performance:
    raise ValueError(
        f"Colonnes manquantes dans vmCloud_enriched.csv : {missing_columns_performance}"
    )

required_columns_recommendations = ["productid"]
if "productid" not in recommendations.columns:
    raise ValueError(
        "La colonne 'productid' est manquante dans recommended_products.csv."
    )


def normalize(column):
    if column.min() == column.max():
        return column - column.min()
    return (column - column.min()) / (column.max() - column.min())


# Normalisation des colonnes
for col in required_columns_performance:
    performance_data[f"{col}_normalized"] = normalize(performance_data[col])

# Calcul du score de performance
performance_data["performance_score"] = (
    0.3 * (1 - performance_data["cpu_usage_normalized"])
    + 0.3 * (1 - performance_data["memory_usage_normalized"])
    - 0.2 * performance_data["execution_time_normalized"]
    + 0.1 * (1 - performance_data["power_consumption_normalized"])
    + 0.1 * (1 - performance_data["network_traffic_normalized"])
)

# Vérification des scores calculés
print("Résumé des scores de performance :")
print(performance_data["performance_score"].describe())

# Association des scores aux produits
recommendations = recommendations.merge(
    performance_data[["vm_id", "performance_score"]],
    left_on="productid",
    right_on="vm_id",
    how="left",
)

recommendations["performance_score"].fillna(0, inplace=True)
print("Produits sans données de performance :")
print(recommendations[recommendations["performance_score"] == 0])

recommendations = recommendations.sort_values(by="performance_score", ascending=False)

output_path = os.path.join(
    RECOMMENDATION_RESULTS_DIR, "recommendations_with_performance.csv"
)
os.makedirs(RECOMMENDATION_RESULTS_DIR, exist_ok=True)
recommendations.to_csv(output_path, index=False)

print(f"Analyse terminée. Résultats sauvegardés à : {output_path}")
