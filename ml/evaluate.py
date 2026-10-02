from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from ml.train import load_dataset


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--model", default="models/pdf_malware_rf.joblib")
    args = ap.parse_args()
    X, y, _ = load_dataset(args.csv)
    model = joblib.load(args.model)
    pred = model.predict(X)
    prob = model.predict_proba(X)[:, 1]
    metrics = {
        "accuracy": accuracy_score(y, pred),
        "precision": precision_score(y, pred, zero_division=0),
        "recall": recall_score(y, pred, zero_division=0),
        "f1": f1_score(y, pred, zero_division=0),
        "roc_auc": roc_auc_score(y, prob),
        "confusion_matrix": confusion_matrix(y, pred).tolist(),
    }
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
