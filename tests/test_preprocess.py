from src.config import PROCESSED_DIR

from src.classical.preprocess import load_dataset

dataset = PROCESSED_DIR / "career_readiness_dataset.csv"

# df = load_dataset(dataset)

# print(df["combined_text"].iloc[0][:1000])

X, y = load_dataset(dataset)

print(X.iloc[0])

print("\nLabel:", y.iloc[0])
