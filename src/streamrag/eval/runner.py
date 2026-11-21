"""Streaming evaluation: feed text observations in time order; whenever the stream time
passes a question's t_query, answer it from the current memory.

Output: outputs/runs/<dataset>/<split>/<method>_B<budget>_<reader>/
  predictions.jsonl  one line per question (resume-safe per stream)
  config.json        run settings (captioner key, reader, budget, ...)
"""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Callable

from streamrag.config import OUTPUT_DIR
from streamrag.memory.base import Memory
from streamrag.memory.tokens import count_tokens
from streamrag.qa.answer import answer_question
from streamrag.types import Observation, QAItem


def run_stream(obs: list[Observation], qa: list[QAItem], memory: Memory, reader) -> list[dict]:
    end = obs[-1].t if obs else 0.0
    pending = sorted(qa, key=lambda q: q.t_query if q.t_query is not None else end + 1)
    out: list[dict] = []
    update_s: list[float] = []

    def answer_due(t_next: float | None) -> None:
        while pending and (t_next is None or (pending[0].t_query is not None
                                              and pending[0].t_query < t_next)):
            q = pending.pop(0)
            ctx = memory.context(q)
            t0 = time.time()
            ans = answer_question(q, ctx, reader)
            out.append({
                "qa_id": q.qa_id, "stream_id": q.stream_id, "question": q.question,
                "options": q.options, "gold": q.answer, "format": q.meta.get("format", "open"),
                "qtype": q.qtype, "t_query": q.t_query, **ans,
                "memory_tokens": memory.n_tokens(), "context_tokens": count_tokens(ctx),
                "n_obs_seen": n_seen, "answer_s": round(time.time() - t0, 3),
            })

    n_seen = 0
    for o in obs:
        answer_due(o.t)
        t0 = time.time()
        memory.observe(o)
        update_s.append(time.time() - t0)
        n_seen += 1
    answer_due(None)
    mean_update = sum(update_s) / len(update_s) if update_s else 0.0
    for r in out:
        r["mean_update_ms"] = round(1000 * mean_update, 2)
    return out


def run_dir(dataset: str, split: str, method: str, budget: int, reader_name: str,
            tag: str = "") -> Path:
    name = f"{method}_B{budget}_{reader_name}" + (f"_{tag}" if tag else "")
    return OUTPUT_DIR / "runs" / dataset / split / name


def run_dataset(streams, get_obs: Callable, make_memory: Callable[[], Memory], reader,
                out_dir: Path, config: dict) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "config.json").write_text(json.dumps(config, indent=1))
    pred_path = out_dir / "predictions.jsonl"
    done = set()
    if pred_path.exists():
        done = {json.loads(line)["stream_id"] for line in pred_path.read_text().splitlines() if line}
    with open(pred_path, "a") as f:
        for i, s in enumerate(streams):
            if s.stream_id in done or not s.qa:
                continue
            t0 = time.time()
            rows = run_stream(get_obs(s), s.qa, make_memory(), reader)
            for r in rows:
                f.write(json.dumps(r, default=str) + "\n")
            f.flush()
            print(f"  [{i + 1}/{len(streams)}] {s.stream_id}: {len(rows)} questions, "
                  f"{time.time() - t0:.0f}s", flush=True)
    return pred_path
