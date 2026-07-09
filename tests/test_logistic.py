from src.config import PROCESSED_DIR, OUTPUTS_DIR

from src.classical.logistic_model import train_logistic

from src.evaluation.metrics import (
    evaluate,
    print_metrics,
    save_metrics,
)
import pandas as pd
import json

dataset = PROCESSED_DIR / "career_readiness_dataset.csv"

y_true, y_pred, model, vectorizer, train_idx, test_idx = train_logistic(dataset)
predictions = pd.DataFrame({
    "true_label": y_true,
    "prediction": y_pred,
})

predictions.to_csv(
    OUTPUTS_DIR / "logistic_predictions.csv",
    index=False,
)

results = evaluate(y_true, y_pred)

print_metrics(results)

save_metrics(
    results,
    OUTPUTS_DIR / "logistic_metrics.json",
)

split = {
    "train_indices": train_idx.tolist(),
    "test_indices": test_idx.tolist(),
}

with open(
    OUTPUTS_DIR / "train_test_indices.json",
    "w",
) as f:
    json.dump(split, f, indent=4)

print(pd.Series(y_pred).value_counts())