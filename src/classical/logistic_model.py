"""
logistic_model.py

Train and evaluate a Logistic Regression classifier using TF-IDF features.
"""

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import pandas as pd
import joblib
from pathlib import Path

from src.classical.preprocess import prepare_data

MODEL_DIR = Path("models/logistic")
MODEL_DIR.mkdir(parents=True, exist_ok=True)

def train_logistic(dataset_path, C=1.0, min_df = 2):
    """
    Train a Logistic Regression model.

    Parameters
    ----------
    dataset_path : Path

    Returns
    -------
    y_test : pandas.Series
    predictions : ndarray
    """

    # Create train/test split
    X_train, X_test, y_train, y_test, train_idx, test_idx = prepare_data(dataset_path)
    # X_train, X_test, y_train, y_test = prepare_data(dataset_path)

    print("\nTraining labels")
    print(y_train.value_counts())
    print("\nTesting labels")
    print(y_test.value_counts())

    # Convert text into TF-IDF features
    vectorizer = TfidfVectorizer(
        stop_words="english",
        max_features=5000,
        ngram_range=(1, 2),
        min_df=min_df,
    )

    X_train = vectorizer.fit_transform(X_train)
    print(X_train.shape)
    X_test = vectorizer.transform(X_test)

    # Train Logistic Regression
    model = LogisticRegression(
        C = C,
        max_iter=1000,
        class_weight="balanced",
        random_state=42,
    )

    model.fit(X_train, y_train)
    print(len(vectorizer.vocabulary_))
    predictions = model.predict(X_test)
    print(model.classes_)

    print("\nPredicted labels")
    print(pd.Series(predictions).value_counts())

    joblib.dump(model, MODEL_DIR / "logistic_regression.pkl")
    joblib.dump(vectorizer, MODEL_DIR / "tfidf_vectorizer.pkl")

    return (
        y_test,
        predictions,
        model,
        vectorizer,
        train_idx,
        test_idx,
    )
