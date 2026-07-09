from src.config import PROCESSED_DIR

from src.deep_learning.distilbert_model import train_distilbert

dataset = PROCESSED_DIR / "career_readiness_dataset.csv"

trainer, results = train_distilbert(dataset)

print(results)