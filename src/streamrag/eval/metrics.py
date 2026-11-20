"""Metrics: QA accuracy, evidence recall, abstention F1, relation macro-F1, bootstrap CIs — STUB (implemented after the setup milestones)."""
from __future__ import annotations

import numpy as np


def bootstrap_ci(values: list[float], n: int = 1000, alpha: float = 0.05, seed: int = 0) -> tuple[float, float, float]:
    """Mean and (1-alpha) bootstrap CI over per-question scores."""
    rng = np.random.default_rng(seed)
    v = np.asarray(values, dtype=float)
    means = rng.choice(v, size=(n, len(v)), replace=True).mean(1)
    return float(v.mean()), float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2))
