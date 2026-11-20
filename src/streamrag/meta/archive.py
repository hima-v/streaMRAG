"""Archive of policy generations + DGM-H-style parent selection.

Layout: outputs/meta/<run>/archive.jsonl (one line per generation) and
outputs/meta/<run>/gen_XXXX/{policy/, patch.json, scores.json, traces.jsonl}.
"""
from __future__ import annotations

import json
import math
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass
class GenRecord:
    gen_id: int
    parent_id: int | None
    dev_score: float | None = None          # full dev score (None if staged eval failed)
    staged_score: float | None = None
    n_edits: int = 0
    valid: bool = True                      # patch validated and evaluated
    meta: dict = field(default_factory=dict)


class Archive:
    def __init__(self, run_dir: Path):
        self.run_dir = Path(run_dir)
        self.run_dir.mkdir(parents=True, exist_ok=True)
        self.path = self.run_dir / "archive.jsonl"
        self.records: list[GenRecord] = []
        if self.path.exists():
            self.records = [GenRecord(**json.loads(line)) for line in self.path.read_text().splitlines()]

    def gen_dir(self, gen_id: int) -> Path:
        return self.run_dir / f"gen_{gen_id:04d}"

    def add(self, rec: GenRecord) -> None:
        self.records.append(rec)
        with open(self.path, "a") as f:
            f.write(json.dumps(asdict(rec)) + "\n")

    def n_children(self, gen_id: int) -> int:
        return sum(r.parent_id == gen_id and r.valid for r in self.records)

    def lineage(self, gen_id: int) -> list[GenRecord]:
        by_id = {r.gen_id: r for r in self.records}
        out, cur = [], by_id.get(gen_id)
        while cur is not None:
            out.append(cur)
            cur = by_id.get(cur.parent_id) if cur.parent_id is not None else None
        return out[::-1]

    def best(self) -> GenRecord:
        return max((r for r in self.records if r.dev_score is not None), key=lambda r: r.dev_score)

    def select_parent(self, method: str = "score_child_prop", rng: random.Random | None = None) -> GenRecord:
        """score_child_prop (HyperAgents default): weight = sigmoid(10*(s - mean_top3)) * exp(-(n_children/8)^3)."""
        rng = rng or random.Random()
        cands = [r for r in self.records if r.valid and r.dev_score is not None]
        if not cands:
            raise RuntimeError("archive has no evaluated generations")
        if method == "latest":
            return cands[-1]
        if method == "best":
            return max(cands, key=lambda r: r.dev_score)
        if method == "random":
            return rng.choice(cands)
        scores = [r.dev_score for r in cands]
        mid = sum(sorted(scores, reverse=True)[:3]) / min(3, len(scores))
        w = []
        for r in cands:
            s = 1.0 / (1.0 + math.exp(-10.0 * (r.dev_score - mid)))
            p = 1.0 if method == "score_prop" else math.exp(-((self.n_children(r.gen_id) / 8.0) ** 3))
            w.append(s * p)
        return rng.choices(cands, weights=w, k=1)[0]
