"""Scoring: exact match for mc / mc_multi / yesno, LLM judge for open answers,
bootstrap CIs over questions, breakdown by question type."""
from __future__ import annotations

from collections import defaultdict

import numpy as np

JUDGE_PROMPT = """Question: {question}
Reference answer: {gold}
Candidate answer: {pred}
Is the candidate answer correct, i.e. does it give the same information as the reference
(extra correct detail is fine)? Reply with only "yes" or "no"."""


def bootstrap_ci(values: list[float], n: int = 1000, alpha: float = 0.05, seed: int = 0) -> tuple[float, float, float]:
    """Mean and (1-alpha) bootstrap CI over per-question scores."""
    v = np.asarray(values, dtype=float)
    if len(v) == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    means = rng.choice(v, size=(n, len(v)), replace=True).mean(1)
    return float(v.mean()), float(np.quantile(means, alpha / 2)), float(np.quantile(means, 1 - alpha / 2))


def exact_score(row: dict) -> float | None:
    """1/0 for closed formats, None if an LLM judge is needed."""
    if row["abstained"]:
        return 0.0
    fmt, pred, gold = row["format"], row["pred"], row["gold"]
    if fmt == "mc":
        return float(pred is not None and pred == str(gold).strip())
    if fmt == "mc_multi":
        g = gold if isinstance(gold, list) else [gold]
        return float(sorted(pred or []) == sorted(g))
    if fmt == "yesno":
        return float(pred is not None and pred.lower() == str(gold).strip().lower())
    return None


def judge_score(row: dict, judge) -> float:
    gold = "; ".join(row["gold"]) if isinstance(row["gold"], list) else row["gold"]
    out = judge.generate(JUDGE_PROMPT.format(question=row["question"], gold=gold, pred=row["pred"]),
                         max_new_tokens=4)
    return float(out.strip().lower().startswith("yes"))


def summarize(rows: list[dict]) -> dict:
    scores = [r["score"] for r in rows]
    acc, lo, hi = bootstrap_ci(scores)
    by_type: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        types = r["qtype"] if isinstance(r["qtype"], list) else [r["qtype"]]
        for t in types:
            by_type[str(t)].append(r["score"])
    return {
        "n": len(rows),
        "accuracy": round(acc, 4), "ci95": [round(lo, 4), round(hi, 4)],
        "abstain_rate": round(float(np.mean([r["abstained"] for r in rows])), 4) if rows else None,
        "mean_memory_tokens": round(float(np.mean([r["memory_tokens"] for r in rows])), 1) if rows else None,
        "mean_context_tokens": round(float(np.mean([r["context_tokens"] for r in rows])), 1) if rows else None,
        "mean_update_ms": round(float(np.mean([r["mean_update_ms"] for r in rows])), 2) if rows else None,
        "by_qtype": {t: {"n": len(v), "accuracy": round(float(np.mean(v)), 4)}
                     for t, v in sorted(by_type.items())},
    }
