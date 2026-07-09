"""
Small DistilBERT hyperparameter tuning.
"""

from itertools import product
import pandas as pd

from src.deep_learning.distilbert_model import train_distilbert

LEARNING_RATES = [
    2e-5,
    3e-5,
]

EPOCHS = [
    2,
    3,
]

results = []

for lr, epochs in product(
    LEARNING_RATES,
    EPOCHS,
):

    print("=" * 60)
    print(f"LR={lr} Epochs={epochs}")

    trainer, metrics = train_distilbert(
        dataset_path="data/processed/career_readiness_dataset.csv",
        learning_rate=lr,
        epochs=epochs,
    )

    results.append(
        {
            "learning_rate": lr,
            "epochs": epochs,
            "accuracy": metrics["accuracy"],
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "macro_f1": metrics["f1"],
        }
    )

df = pd.DataFrame(results)

print(df)

df.to_csv(
    "data/outputs/distilbert_tuning_results.csv",
    index=False,
)
