"""
metrics.py

Reusable evaluation functions for all models.

Every model should output predictions only.
This module computes evaluation metrics.
"""

import pandas as pd
import json

from pathlib import Path

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)


def evaluate(y_true, y_pred):
    """
    Compute evaluation metrics.

    Parameters
    ----------
    y_true : list
    y_pred : list

    Returns
    -------
    dict
    """
    results = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, average="macro"),
        "recall": recall_score(y_true, y_pred, average="macro"),
        "f1": f1_score(y_true, y_pred, average="macro"),
        "confusion_matrix": confusion_matrix(y_true, y_pred),
        "classification_report": classification_report(y_true, y_pred),
    }

    return results


def print_metrics(results):
    """
    Print evaluation metrics.
    """

    print(f"\nAccuracy : {results['accuracy']:.3f}")
    print(f"Precision: {results['precision']:.3f}")
    print(f"Recall   : {results['recall']:.3f}")
    print(f"F1 Score : {results['f1']:.3f}")

    print("\nConfusion Matrix\n")
    print(results["confusion_matrix"])

    print("\nClassification Report\n")
    print(results["classification_report"])



def save_metrics(results, output_file):
    """
    Save evaluation metrics to JSON.
    """
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output = results.copy()
    output["accuracy"] = round(output["accuracy"], 3)
    output["precision"] = round(output["precision"], 3)
    output["recall"] = round(output["recall"], 3)
    output["f1"] = round(output["f1"], 3)
    output["confusion_matrix"] = output["confusion_matrix"].tolist()

    with open(output_file, "w") as f:
        json.dump(output, f, indent=4)