from __future__ import annotations

import json
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder


# ============================================================
# PROJECT PATHS
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = ROOT / "data" / "raw" / "PDFMalware2022.parquet"
MODEL_PATH = ROOT / "models" / "pdf_malware_rf.joblib"
META_PATH = ROOT / "models" / "pdf_malware_rf.json"
CM_PATH = ROOT / "reports" / "confusion_matrix.png"

MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
CM_PATH.parent.mkdir(parents=True, exist_ok=True)


# ============================================================
# LOAD DATASET
# ============================================================

print("=" * 70)
print("PDFShield AI - PDF Malware Detection Training")
print("=" * 70)

print("\n[1/7] Loading dataset...")

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset not found:\n{DATA_PATH}"
    )

df = pd.read_parquet(DATA_PATH)

print(f"Dataset shape: {df.shape}")


# ============================================================
# VALIDATE DATASET
# ============================================================

if "Class" not in df.columns:
    raise ValueError(
        f"'Class' column not found. Available columns:\n{df.columns.tolist()}"
    )

print("\nClass distribution:")
print(df["Class"].value_counts())


# ============================================================
# PREPARE TARGET
# ============================================================

print("\n[2/7] Preparing target and features...")

label_mapping = {
    "Benign": 0,
    "Malicious": 1,
}

y = df["Class"].map(label_mapping)

if y.isna().any():
    unknown = df.loc[y.isna(), "Class"].unique()
    raise ValueError(
        f"Unknown class values found: {unknown}"
    )

y = y.astype(int)


# ============================================================
# REMOVE IDENTIFIER
# ============================================================

# FileName identifies the PDF but is not a useful security feature.
X = df.drop(
    columns=["Class", "FileName"],
    errors="ignore",
).copy()

print(f"Number of raw features: {X.shape[1]}")


# ============================================================
# IDENTIFY FEATURE TYPES
# ============================================================

numeric_features = X.select_dtypes(
    include=["number"]
).columns.tolist()

categorical_features = X.select_dtypes(
    include=["object", "category", "string"]
).columns.tolist()

print(f"Numeric features: {len(numeric_features)}")
print(f"Categorical features: {len(categorical_features)}")


# ============================================================
# PREPROCESSING
# ============================================================

print("\n[3/7] Building preprocessing pipeline...")

numeric_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="median"),
        )
    ]
)

categorical_pipeline = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(strategy="most_frequent"),
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="ignore",
                sparse_output=False,
            ),
        ),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        (
            "numeric",
            numeric_pipeline,
            numeric_features,
        ),
        (
            "categorical",
            categorical_pipeline,
            categorical_features,
        ),
    ]
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("\n[4/7] Splitting dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y,
)

print(f"Training samples: {len(X_train)}")
print(f"Testing samples:  {len(X_test)}")


# ============================================================
# RANDOM FOREST
# ============================================================

print("\n[5/7] Training Random Forest...")

classifier = RandomForestClassifier(
    n_estimators=350,
    random_state=42,
    class_weight="balanced_subsample",
    n_jobs=-1,
    min_samples_leaf=2,
)

model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor,
        ),
        (
            "classifier",
            classifier,
        ),
    ]
)

model.fit(X_train, y_train)

print("Training completed successfully.")


# ============================================================
# EVALUATION
# ============================================================

print("\n[6/7] Evaluating model...")

pred = model.predict(X_test)

prob = model.predict_proba(X_test)[:, 1]

accuracy = accuracy_score(y_test, pred)
precision = precision_score(y_test, pred)
recall = recall_score(y_test, pred)
f1 = f1_score(y_test, pred)
roc_auc = roc_auc_score(y_test, prob)

print("\n" + "=" * 70)
print("MODEL PERFORMANCE")
print("=" * 70)

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")
print(f"ROC-AUC  : {roc_auc:.4f}")

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        pred,
        target_names=["Benign", "Malicious"],
        digits=4,
    )
)

# Confusion matrix
cm = confusion_matrix(y_test, pred)

print("\nConfusion Matrix:")
print(cm)


# ============================================================
# SAVE CONFUSION MATRIX
# ============================================================

fig, ax = plt.subplots(figsize=(7, 6))

display = ConfusionMatrixDisplay(
    confusion_matrix=cm,
    display_labels=["Benign", "Malicious"],
)

display.plot(ax=ax)

ax.set_title(
    "PDFShield AI - Random Forest Confusion Matrix"
)

plt.tight_layout()
plt.savefig(
    CM_PATH,
    dpi=200,
    bbox_inches="tight",
)

plt.close()

print(f"\nConfusion matrix saved to:")
print(CM_PATH)


# ============================================================
# SAVE MODEL
# ============================================================

print("\n[7/7] Saving trained model...")

joblib.dump(model, MODEL_PATH)

metadata = {
    "dataset": "PDFMalware2022.parquet",
    "rows": int(len(df)),
    "raw_features": int(X.shape[1]),
    "numeric_features": numeric_features,
    "categorical_features": categorical_features,
    "label_mapping": {
        "0": "Benign",
        "1": "Malicious",
    },
    "test_size": 0.20,
    "random_state": 42,
    "model": "RandomForestClassifier",
    "n_estimators": 350,
    "metrics": {
        "accuracy": float(accuracy),
        "precision": float(precision),
        "recall": float(recall),
        "f1": float(f1),
        "roc_auc": float(roc_auc),
    },
}

META_PATH.write_text(
    json.dumps(metadata, indent=2)
)

print(f"Model saved to:")
print(MODEL_PATH)

print(f"\nMetadata saved to:")
print(META_PATH)


# ============================================================
# COMPLETE
# ============================================================

print("\n" + "=" * 70)
print("TRAINING COMPLETE")
print("=" * 70)