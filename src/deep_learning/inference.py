"""
inference.py

Load the trained DistilBERT model and make predictions.
"""

import torch
from src.config import MODEL_DIR

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
)

# MODEL_PATH = "models/distilbert"

LABELS = {
    0: "Ready",
    1: "Ready with Short Ramp-Up",
    2: "Requires Significant Preparation",
}


tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)

model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)

model.eval()


def predict(resume_text, job_description):
    """
    Predict career readiness from resume and job description.
    """

    text = "[RESUME]\n" + resume_text + "\n\n[JOB]\n" + job_description

    inputs = tokenizer(
        text,
        truncation=True,
        padding=True,
        max_length=384,
        return_tensors="pt",
    )

    with torch.no_grad():

        outputs = model(**inputs)

        probabilities = torch.softmax(
            outputs.logits,
            dim=1,
        )

        prediction = torch.argmax(
            probabilities,
            dim=1,
        ).item()

        confidence = probabilities[0][prediction].item()

    return {
        "label": LABELS[prediction],
        "confidence": round(confidence * 100, 1),
    }
