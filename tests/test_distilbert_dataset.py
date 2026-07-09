from src.config import PROCESSED_DIR

from src.deep_learning.distilbert_dataset import (
    load_hf_dataset,
    tokenize_dataset,
)

dataset = PROCESSED_DIR / "career_readiness_dataset.csv"

train_ds, test_ds = load_hf_dataset(dataset)

train_ds, tokenizer = tokenize_dataset(train_ds)

print(train_ds[0])