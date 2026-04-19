#!/usr/bin/env python3

import os
import pickle

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

_DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "landmarks.csv")
_MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "models", "rf_libras.pkl")

def _load_data():
    df = pd.read_csv(_DATA_PATH)
    X = df.drop("label", axis=1).values
    y = df["label"].values
    return X, y

def main():
    X, y = _load_data()
    print(f"{len(X)} amostras carregadas ({len(set(y))} classes)")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    print(classification_report(y_test, model.predict(X_test)))

    os.makedirs(os.path.dirname(_MODEL_PATH), exist_ok=True)
    with open(_MODEL_PATH, "wb") as f:
        pickle.dump({"model": model}, f)
    print(f"salvo em {_MODEL_PATH}")

if __name__ == "__main__":
    main()