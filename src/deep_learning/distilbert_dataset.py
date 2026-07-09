"""
distilbert_dataset.py

Prepare the Career Readiness Dataset for DistilBERT.
"""

import json
import pandas as pd

from datasets import Dataset
from transformers import AutoTokenizer

from src.config import OUTPUTS_DIR


MODEL_NAME = "distilbert-base-uncased"


LABEL_MAP = {
    "Ready": 0,
    "Ready with Short Ramp-Up": 1,
    "Requires Significant Preparation": 2,
}


def load_hf_dataset(dataset_path):
    """
    Load the dataset and recreate the exact train/test split
    used by the classical model.
    """

    df = pd.read_csv(dataset_path)

    df["text"] = (
        "[RESUME]\n"
        + df["resume_text"]
        + "\n\n[JOB]\n"
        + df["job_text"]
    )

    df["label"] = df["readiness_label"].map(LABEL_MAP)

    with open(
        OUTPUTS_DIR / "train_test_indices.json",
        "r",
    ) as f:

        split = json.load(f)

    train_df = df.iloc[
        split["train_indices"]
    ].reset_index(drop=True)

    test_df = df.iloc[
        split["test_indices"]
    ].reset_index(drop=True)

    train_df = train_df[["text", "label"]]
    test_df = test_df[["text", "label"]]    

    return (
        Dataset.from_pandas(train_df),
        Dataset.from_pandas(test_df),
    )


def tokenize_dataset(dataset):
    """
    Tokenize a Hugging Face dataset.
    """

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME
    )

    def tokenize(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            padding="max_length",
            max_length=384,
        )

    dataset = dataset.map(
        tokenize,
        batched=True,
    )

    return dataset, tokenizer