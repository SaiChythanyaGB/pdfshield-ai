"""Feature-space robustness experiment.

This is intentionally a safe simulation: it perturbs numerical feature vectors
rather than modifying or executing real malicious PDFs.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


def adversarial_sweep(model, X: pd.DataFrame, y_true: int, steps: int = 9, strength: float = 0.15):
    """Perturb selected numeric features toward the benign direction.

    This is a teaching-oriented black-box robustness experiment, not a claim that
    every perturbation corresponds to a valid PDF transformation.
    """
    row = X.iloc[[0]].copy()
    baseline = float(model.predict_proba(row)[0, 1])
    numeric = row.select_dtypes(include=[np.number]).columns.tolist()
    if not numeric:
        return pd.DataFrame()

    # Use a deterministic subset to keep the demo interpretable.
    selected = numeric[: min(8, len(numeric))]
    records = []
    for i, alpha in enumerate(np.linspace(0, strength, steps)):
        trial = row.copy()
        for c in selected:
            v = float(trial.iloc[0][c])
            trial.iloc[0, trial.columns.get_loc(c)] = max(0.0, v * (1.0 - alpha))
        p = float(model.predict_proba(trial)[0, 1])
        records.append({"step": i, "perturbation": alpha, "malicious_probability": p, "prediction": int(p >= 0.5)})
    out = pd.DataFrame(records)
    out.attrs["baseline_probability"] = baseline
    out.attrs["true_label"] = y_true
    return out
