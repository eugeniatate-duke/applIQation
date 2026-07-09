"""
preprocess.py

Utility functions for preparing text for classical
machine learning models.
"""

import pandas as pd
from sklearn.model_selection import train_test_split


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
    and create a stratified train/test split.
    """

    X, y = load_dataset(dataset_path)
    indices = X.index

    return train_test_split(X,y,indices,test_size=test_size,random_state=random_state,stratify=y,)


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