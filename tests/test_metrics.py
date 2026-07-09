from src.config import PROCESSED_DIR, OUTPUTS_DIR

from src.baseline.baseline_model import evaluate_baseline
from src.evaluation.metrics import (
    evaluate,
    print_metrics,
    save_metrics,
)

dataset = PROCESSED_DIR / "career_readiness_dataset.csv"

df, y_true, y_pred = evaluate_baseline(dataset)
df[
    [
        "example_id",
        "role",
        "job_title",
        "readiness_label",
        "baseline_prediction"
    ]
].to_csv(
    OUTPUTS_DIR / "baseline_predictions.csv",
    index=False
)

results = evaluate(y_true, y_pred)

print_metrics(results)

save_metrics(
    results,
    OUTPUTS_DIR / "baseline_metrics.json"
)