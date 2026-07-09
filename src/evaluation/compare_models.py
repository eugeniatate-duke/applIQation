"""
compare_models.py

Compare all trained models and generate a summary table.
"""

import json
import pandas as pd
from src.config import OUTPUTS_DIR


def load_metrics(filename):
    """
    Load a metrics JSON file.
    """
    with open(OUTPUTS_DIR / filename, "r") as f:
        return json.load(f)


def compare_models():
    """
    Create a comparison table for all models.
    """
    baseline = load_metrics("baseline_metrics.json")
    logistic = load_metrics("logistic_metrics.json")
    distilbert = load_metrics("distilbert_metrics.json")

    results = pd.DataFrame([
        {
            "Model": "Naive Baseline",
            "Accuracy": baseline["accuracy"],
            "Precision": baseline["precision"],
            "Recall": baseline["recall"],
            "Macro F1": baseline["f1"],
        },
        {
            "Model": "Logistic Regression",
            "Accuracy": logistic["accuracy"],
            "Precision": logistic["precision"],
            "Recall": logistic["recall"],
            "Macro F1": logistic["f1"],
        },
        {
            "Model": "DistilBERT",
            "Accuracy": distilbert["accuracy"],
            "Precision": distilbert["precision"],
            "Recall": distilbert["recall"],
            "Macro F1": distilbert["f1"],
        },
    ])

    results = results.round(3)

    print("\nModel Comparison\n")
    print(results)

    results.to_csv(
        OUTPUTS_DIR / "model_comparison.csv",
        index=False,
    )

    return results


if __name__ == "__main__":
    compare_models()