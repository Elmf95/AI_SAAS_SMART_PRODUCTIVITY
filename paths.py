import os
import sys

# Ajouter le répertoire racine du projet au sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))  # Chemin vers la racine du projet
sys.path.append(ROOT_DIR)

# Définir les chemins des différents dossiers et fichiers
DATA_DIR = os.path.join(ROOT_DIR, "data")  # Répertoire des données
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")  # Données brutes
PROCESSED_DATA_DIR = os.path.join(DATA_DIR, "processed")
CLEANED_DATA_DIR = os.path.join(DATA_DIR, "clean")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")
RECOMMENDATION_RESULTS_DIR = os.path.join(DATA_DIR, "recommendation")

# Configurer le chemin vers le dossier src et ses sous-dossiers
SRC_DIR = os.path.join(ROOT_DIR, "src")
MODELS_DIR = os.path.join(SRC_DIR, "models")
API_DIR = os.path.join(SRC_DIR, "api")
UTILS_DIR = os.path.join(SRC_DIR, "utils")
ANALYSIS_DIR = os.path.join(SRC_DIR, "analysis")

# Ajouter ces chemins au sys.path pour pouvoir les importer directement
sys.path.append(MODELS_DIR)
sys.path.append(API_DIR)
sys.path.append(UTILS_DIR)


# Retourner les chemins pour une utilisation dans les scripts
def get_paths():
    return {
        "ROOT_DIR": ROOT_DIR,
        "RAW_DATA_DIR": RAW_DATA_DIR,
        "CLEANED_DATA_DIR": CLEANED_DATA_DIR,
        "MODELS_DIR": MODELS_DIR,
        "API_DIR": API_DIR,
        "UTILS_DIR": UTILS_DIR,
    }
