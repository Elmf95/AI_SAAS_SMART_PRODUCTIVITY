import os
import sys
import pandas as pd
from datetime import datetime

# Gestion dynamique des chemins : ROOT_DIR = racine du projet
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(ROOT_DIR)

# Import des chemins définis dans paths.py
from paths import PROCESSED_DATA_DIR, CLEANED_DATA_DIR


# Chargement des fichiers nettoyés
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
    # Chargement des données nettoyées
    amazon_reviews, hr_dashboard, project_tools, task_assignment, vmCloud_data = (
        load_cleaned_data()
    )

    # Amazon Reviews Summary
    amazon_reviews["score"] = pd.to_numeric(amazon_reviews["score"], errors="coerce")
    amazon_summary = (
        amazon_reviews.groupby("productid")
        .agg(avg_score=("score", "mean"), num_reviews=("score", "count"))
        .reset_index()
    )
    amazon_summary.to_csv(
        os.path.join(CLEANED_DATA_DIR, "amazon_reviews_summary.csv"), index=False
    )

    # HR Dashboard Summary
    hr_dashboard["joining_date"] = pd.to_datetime(
        hr_dashboard["joining_date"], errors="coerce"
    )
    hr_dashboard["experience"] = (
        pd.Timestamp.now() - hr_dashboard["joining_date"]
    ).dt.days / 365.0
    hr_summary = (
        hr_dashboard.groupby("department")
        .agg(
            avg_productivity=("productivity_(%)", "mean"),
            avg_satisfaction=("satisfaction_rate_(%)", "mean"),
            avg_experience=("experience", "mean"),
        )
        .reset_index()
    )
    hr_summary.to_csv(
        os.path.join(CLEANED_DATA_DIR, "hr_dashboard_summary.csv"), index=False
    )

    # Project Tools Summary
    project_tools["final_selected_tool"] = (
        project_tools["final_selected_tool"].str.strip().str.lower()
    )
    tools_summary = project_tools["final_selected_tool"].value_counts().reset_index()
    tools_summary.columns = ["tool_name", "selection_count"]
    tools_summary.to_csv(
        os.path.join(CLEANED_DATA_DIR, "project_tools_summary.csv"), index=False
    )

    # Task Assignment Summary
    task_assignment_summary = (
        task_assignment.groupby(["category", "skill"])
        .size()
        .reset_index(name="task_count")
    )
    task_assignment_summary.to_csv(
        os.path.join(CLEANED_DATA_DIR, "task_assignment_summary.csv"), index=False
    )

    # VMCloud Summary
    vmcloud_summary = (
        vmCloud_data.groupby("task_type")
        .agg(
            avg_cpu_usage=("cpu_usage", "mean"),
            avg_memory_usage=("memory_usage", "mean"),
            avg_network_traffic=("network_traffic", "mean"),
        )
        .reset_index()
    )
    vmcloud_summary.to_csv(
        os.path.join(CLEANED_DATA_DIR, "vmcloud_summary.csv"), index=False
    )


if __name__ == "__main__":
    feature_engineering()
