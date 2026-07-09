"""
generate_report_figures.py

Generate figures for the final report.
"""

import json
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay

OUTPUT_DIR = Path("data/outputs")
FIGURES_DIR = OUTPUT_DIR / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_json(filename):
    with open(OUTPUT_DIR / filename, "r") as f:
        return json.load(f)


# ----------------------------------------------------
# Model comparison
# ----------------------------------------------------

comparison = pd.read_csv(OUTPUT_DIR / "model_comparison.csv")

plt.figure(figsize=(6, 4))

plt.bar(
    comparison["Model"],
    comparison["Accuracy"],
)

plt.ylabel("Accuracy")

plt.title("Model Comparison")

plt.ylim(0, 1)

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "01_model_comparison.png",
    dpi=300,
)

plt.close()


# ----------------------------------------------------
# Logistic confusion matrix
# ----------------------------------------------------

plt.figure(figsize=(5, 5))

logistic = load_json("logistic_metrics.json")

disp = ConfusionMatrixDisplay(
    confusion_matrix=np.array(logistic["confusion_matrix"]),
    display_labels=[
        "Ready",
        "Ramp-Up",
        "Preparation",
    ],
)

disp.plot(values_format="d")

plt.title("Logistic Regression")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "02_logistic_confusion_matrix.png",
    dpi=300,
)

plt.close()


# ----------------------------------------------------
# DistilBERT confusion matrix
# ----------------------------------------------------

plt.figure(figsize=(5, 5))

distilbert = load_json("distilbert_metrics.json")

disp = ConfusionMatrixDisplay(
    confusion_matrix=np.array(distilbert["confusion_matrix"]),
    display_labels=[
        "Ready",
        "Ramp-Up",
        "Preparation",
    ],
)

disp.plot(values_format="d")

plt.title("DistilBERT")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "03_distilbert_confusion_matrix.png",
    dpi=300,
)

plt.close()


# ----------------------------------------------------
# Hyperparameter tuning
# ----------------------------------------------------

tuning = pd.read_csv(OUTPUT_DIR / "logistic_tuning_results.csv")

plt.figure(figsize=(6, 4))

plt.plot(
    tuning["C"],
    tuning["macro_f1"],
    marker="o",
)

plt.xscale("log")

plt.xlabel("C")

plt.ylabel("Macro F1")

plt.title("Logistic Regression Hyperparameter Tuning")

plt.tight_layout()

plt.savefig(
    FIGURES_DIR / "04_hyperparameter_tuning.png",
    dpi=300,
)

plt.close()

print()

print("Figures saved to")

print(FIGURES_DIR)
