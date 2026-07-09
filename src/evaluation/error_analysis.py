"""
error_analysis.py

Generate representative model errors for the report.
"""

import pandas as pd

predictions = pd.read_csv("data/outputs/distilbert_predictions.csv")

errors = predictions[predictions["true_label"] != predictions["prediction"]]

errors.to_csv(
    "data/outputs/error_analysis.csv",
    index=False,
)

print()

print("=" * 60)

print("Total Errors")

print(len(errors))

print()

print(errors.head(5))

print()

print("=" * 60)

print("Saved to outputs/error_analysis.csv")
