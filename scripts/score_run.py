"""Score run directories: exact match for closed formats, LLM judge for open answers.

  python scripts/score_run.py outputs/runs/mindcube/dev/*           # many runs -> one table
  python scripts/score_run.py outputs/runs/m3bench/dev/fifo_B1024_nemotron-12b-vl --judge nemotron-12b-vl

Writes <run>/scores.jsonl and <run>/metrics.json, and prints a summary table.
Judge verdicts are cached in scores.jsonl, so re-scoring is free.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from streamrag.config import load_yaml
from streamrag.eval.metrics import exact_score, judge_score, summarize


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("runs", nargs="+", type=Path)
    ap.add_argument("--judge", default=load_yaml("eval")["judge"])
    a = ap.parse_args()
    judge = None
    table = []
    for run in a.runs:
        pred_path = run / "predictions.jsonl"
        if not pred_path.exists():
            continue
        rows = [json.loads(line) for line in pred_path.read_text().splitlines() if line]
        prev = {}
        if (run / "scores.jsonl").exists():
            prev = {r["qa_id"]: r for r in map(json.loads, (run / "scores.jsonl").read_text().splitlines())
                    if r.get("judge") == a.judge or r.get("judge") is None}
        for r in rows:
            s = exact_score(r)
            r["judge"] = None
            if s is None:
                if r["qa_id"] in prev and prev[r["qa_id"]].get("judge") == a.judge:
                    s = prev[r["qa_id"]]["score"]
                else:
                    if judge is None:
                        from streamrag.models import load_model
                        judge = load_model(a.judge)
                    s = judge_score(r, judge)
                r["judge"] = a.judge
            r["score"] = s
        (run / "scores.jsonl").write_text("".join(json.dumps(r, default=str) + "\n" for r in rows))
        m = summarize(rows)
        m["run"] = run.name
        m["config"] = json.loads((run / "config.json").read_text()) if (run / "config.json").exists() else {}
        (run / "metrics.json").write_text(json.dumps(m, indent=1))
        table.append(m)
    print(f"{'run':45s} {'n':>5s} {'acc':>6s} {'95% CI':>15s} {'abst':>5s} {'mem_tok':>8s} {'ctx_tok':>8s} {'upd_ms':>7s}")
    for m in table:
        print(f"{m['run']:45s} {m['n']:5d} {m['accuracy']:6.3f} [{m['ci95'][0]:.3f}, {m['ci95'][1]:.3f}] "
              f"{m['abstain_rate']:5.2f} {m['mean_memory_tokens']:8.1f} {m['mean_context_tokens']:8.1f} "
              f"{m['mean_update_ms']:7.2f}")


if __name__ == "__main__":
    main()
