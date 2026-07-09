from src.classical.logistic_model import train_logistic
from src.evaluation.metrics import evaluate
import pandas as pd

DATASET = "data/processed/career_readiness_dataset.csv"

results = []

for c in [0.1, 1, 10]:

    print("=" * 60)
    print(f"C = {c}")

    (
        y_true,
        y_pred,
        _,
        _,
        _,
        _,
    ) = train_logistic(
        DATASET,
        C=c,
    )

    metrics = evaluate(
        y_true,
        y_pred,
    )

    results.append(
        {
            "C": c,
            "min_df": 2,
            "accuracy": metrics["accuracy"],
            "precision": metrics["precision"],
            "recall": metrics["recall"],
            "macro_f1": metrics["f1"],
        }
    )

    print(metrics)

df = pd.DataFrame(results)

df.to_csv(
    "data/outputs/logistic_tuning_results.csv",
    index=False,
)

print(df)
