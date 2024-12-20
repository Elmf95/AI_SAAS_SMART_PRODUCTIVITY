import os
import sys
import pandas as pd
import sqlite3
import hashlib

# Gestion dynamique des chemins
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

from paths import RAW_DATA_DIR, PROCESSED_DATA_DIR


def hash_file(file_path):
    """
    Calculer le hash MD5 d'un fichier pour vérifier son intégrité.
    """
    hasher = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hasher.update(chunk)
    return hasher.hexdigest()


def load_datasets():
    """
    Charger les datasets bruts depuis RAW_DATA_DIR et associer les fichiers.
    """
    datasets = {}

    # Association des fichiers
    datasets["Employee Productivity and Satisfaction HR Data"] = pd.read_csv(
        os.path.join(RAW_DATA_DIR, "hr_dashboard_data.csv")
    )
    datasets["amazon_reviews"] = pd.read_csv(os.path.join(RAW_DATA_DIR, "Reviews.csv"))
    datasets["Software Project Management Tools"] = pd.read_csv(
        os.path.join(RAW_DATA_DIR, "SPMQA Data Visualization - Sheet1.csv")
    )
    datasets["Skill-Based Task Assignment"] = pd.read_csv(
        os.path.join(RAW_DATA_DIR, "Task Categories.csv")
    )
    datasets["Cloud Computing Performance Metrics"] = pd.read_csv(
        os.path.join(RAW_DATA_DIR, "vmCloud_data.csv")
    )

    # Charger la base de données SQLite Amazon Reviews
    sqlite_path = os.path.join(RAW_DATA_DIR, "database.sqlite")
    conn = sqlite3.connect(sqlite_path)
    datasets["amazon_reviews_db"] = pd.read_sql_query("SELECT * FROM Reviews", conn)
    conn.close()

    return datasets


def verify_hashes():
    """
    Vérifier les hashes des fichiers à l'aide de `hashes.txt`.
    """
    hashes_path = os.path.join(RAW_DATA_DIR, "hashes.txt")
    with open(hashes_path, "r") as file:
        lines = file.readlines()

    # Extraire les hashes de référence
    reference_hashes = {}
    for line in lines:
        if "MD5" in line:
            file_name = line.split("(")[1].split(")")[0]
            hash_value = line.split("=")[1].strip()
            reference_hashes[file_name] = hash_value

    # Vérifier chaque fichier
    for file_name, reference_hash in reference_hashes.items():
        file_path = os.path.join(RAW_DATA_DIR, file_name)
        if os.path.exists(file_path):
            computed_hash = hash_file(file_path)
            if computed_hash == reference_hash:
                print(f"Hash OK for {file_name}")
            else:
                print(
                    f"Hash mismatch for {file_name}: expected {reference_hash}, got {computed_hash}"
                )
        else:
            print(f"File {file_name} not found!")


if __name__ == "__main__":
    print("### Vérification des fichiers avec les hashes ###")
    verify_hashes()

    print("\n### Chargement et exploration des datasets ###")
    try:
        datasets = load_datasets()
        for name, dataset in datasets.items():
            print(f"\n--- Dataset: {name} ---")
            print(f"Shape: {dataset.shape}")
            print(f"Columns: {list(dataset.columns)}")
            print(f"First rows:\n{dataset.head()}")
    except Exception as e:
        print(f"Erreur lors du chargement des datasets : {e}")
