"""
preprocess.py

Utility functions for preparing text for classical
machine learning models.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
import json
from src.config import OUTPUTS_DIR


def combine_inputs(df):
    """
    Combine resume and job description into a single
    text sequence.

    Parameters
    ----------
    df : pandas.DataFrame

    Returns
    -------
    pandas.DataFrame
    """

    df = df.copy()

    df["combined_text"] = (
        "[RESUME]\n"
        + df["resume_text"]
        + "\n\n[JOB]\n"
        + df["job_text"]
    )

    return df

def prepare_data(dataset_path, test_size=0.2, random_state=42):
    """
    Load the dataset, combine the resume and job description,
    create a stratified train/test split, and save the split
    for reproducibility.
    """
    X, y = load_dataset(dataset_path)

    indices = X.index

    X_train, X_test, y_train, y_test, train_idx, test_idx = train_test_split(
        X,
        y,
        indices,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

    split = {
        "train_indices": train_idx.tolist(),
        "test_indices": test_idx.tolist(),
    }

    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    with open(OUTPUTS_DIR / "train_test_indices.json", "w") as f:
        json.dump(split, f, indent=4)

    return X_train, X_test, y_train, y_test


def load_dataset(dataset_path):
    """
    Load and prepare the Career Readiness Dataset.
    Returns
    -------
    tuple
        X : combined input text
        y : readiness labels
    """
    df = pd.read_csv(dataset_path)
    df = combine_inputs(df)
    X = df["combined_text"]
    y = df["readiness_label"]

    return X, y