"""
distilbert_model.py

Fine-tune DistilBERT for career readiness classification.
"""

import numpy as np
import pandas as pd
from src.evaluation.metrics import (
    evaluate,
    save_metrics,
)
from src.config import OUTPUTS_DIR

from transformers import (
    AutoModelForSequenceClassification,
    Trainer,
    TrainingArguments,
)

from evaluate import load

from src.deep_learning.distilbert_dataset import (
    MODEL_NAME,
    load_hf_dataset,
    tokenize_dataset,
)

LABEL_MAP = {
    "Ready": 0,
    "Ready with Short Ramp-Up": 1,
    "Requires Significant Preparation": 2,
}

ID_TO_LABEL = {v: k for k, v in LABEL_MAP.items()}

accuracy = load("accuracy")
f1 = load("f1")


def compute_metrics(eval_pred):
    """
    Compute evaluation metrics.
    """

    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)

    return {
        "accuracy": accuracy.compute(
            predictions=predictions,
            references=labels,
        )["accuracy"],

        "f1": f1.compute(
            predictions=predictions,
            references=labels,
            average="macro",
        )["f1"],
    }


def train_distilbert(
    dataset_path,
    learning_rate=2e-5,
    epochs=3,
):
    """
    Fine-tune DistilBERT.
    """

    train_ds, test_ds = load_hf_dataset(dataset_path)

    train_ds, tokenizer = tokenize_dataset(train_ds)
    test_ds, _ = tokenize_dataset(test_ds)

    model = AutoModelForSequenceClassification.from_pretrained(
        MODEL_NAME,
        num_labels=3,
    )

    training_args = TrainingArguments(
        output_dir="models/distilbert",
        num_train_epochs=epochs,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        eval_strategy="epoch",
        save_strategy="epoch",
        logging_strategy="steps",
        logging_steps=20,
        learning_rate=learning_rate,
        weight_decay=0.01,
        load_best_model_at_end=True,
        report_to="none",
        seed=42,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_ds,
        eval_dataset=test_ds,
        tokenizer=tokenizer,
        compute_metrics=compute_metrics,
    )

    trainer.train()

    predictions = trainer.predict(test_ds)

    predicted_labels = np.argmax(
        predictions.predictions,
        axis=1
    )

    true_labels = predictions.label_ids

    results = evaluate(
        true_labels,
        predicted_labels
    )

    save_metrics(
        results,
        OUTPUTS_DIR / "distilbert_metrics.json"
    )

    predictions_df = pd.DataFrame({
        "true_label": [ID_TO_LABEL[x] for x in true_labels],
        "prediction": [ID_TO_LABEL[x] for x in predicted_labels],
    })

    predictions_df.to_csv(
        OUTPUTS_DIR / "distilbert_predictions.csv",
        index=False,
    )

    trainer.save_model("models/distilbert")
    tokenizer.save_pretrained("models/distilbert")

    return trainer, results
