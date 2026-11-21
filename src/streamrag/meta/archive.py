"""Archive of (memory strategy, meta harness) nodes (codebase_plan.md §11.5).

outputs/archive/<dataset>/<archive_name>/
  archive.json                  all nodes (indented; older archives: archive.jsonl)
  node_XXXX/strategy.md         memory strategy S
  node_XXXX/meta_harness.md     meta harness H
  node_XXXX/meta.json           node record
  node_XXXX/runs/<stream_id>/   snapshots.json, memory_log.json, answers.json, judgments.json
  node_XXXX/scores.json, meta_log.md, checkpoint_report.md
"""
from __future__ import annotations

import hashlib
import json
import math
import random
from dataclasses import asdict, dataclass, field
from pathlib import Path

from streamrag.config import OUTPUT_DIR
from streamrag.records import read_records, write_json


def text_id(text: str) -> str:
    return hashlib.sha256(text.strip().encode()).hexdigest()[:12]


@dataclass
class Node:
    node_id: int
    parent_id: int | None
    dataset: str
    eval_stream: str
    budget: int
    strategy_id: str
    harness_id: str
    switches: dict                      # {"memory_strategy": fixed|dynamic, "meta_harness": fixed|dynamic}
    created_by: dict                    # {"kind": seed|meta, ...rationale/changes}
    scores: dict | None = None
    models: dict = field(default_factory=dict)
    stream_length: int = 0              # items per evidence stream (0 = whole base stream)
    eval_streams: list = field(default_factory=list)   # stream ids every node of the archive is scored on


class Archive:
    def __init__(self, dataset: str, name: str):
        self.dir = OUTPUT_DIR / "archive" / dataset / name
        self.dir.mkdir(parents=True, exist_ok=True)
        self.path = self.dir / "archive.json"
        self.nodes: dict[int, Node] = {}
        if self.path.exists() or (self.dir / "archive.jsonl").exists():
            for rec in read_records(self.path):          # older archives: archive.jsonl, last line per id wins
                n = Node(**rec)
                self.nodes[n.node_id] = n

    def node_dir(self, node_id: int) -> Path:
        d = self.dir / f"node_{node_id:04d}"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def save(self, node: Node, strategy: str | None = None, harness: str | None = None) -> None:
        d = self.node_dir(node.node_id)
        if strategy is not None:
            (d / "strategy.md").write_text(strategy.strip() + "\n")
        if harness is not None:
            (d / "meta_harness.md").write_text(harness.strip() + "\n")
        (d / "meta.json").write_text(json.dumps(asdict(node), indent=2))
        self.nodes[node.node_id] = node
        write_json(self.path, [asdict(n) for n in sorted(self.nodes.values(), key=lambda n: n.node_id)])

    def strategy(self, node_id: int) -> str:
        return (self.node_dir(node_id) / "strategy.md").read_text()

    def harness(self, node_id: int) -> str:
        return (self.node_dir(node_id) / "meta_harness.md").read_text()

    def new_id(self) -> int:
        return max(self.nodes, default=-1) + 1

    def children(self, node_id: int) -> list[Node]:
        return [n for n in self.nodes.values() if n.parent_id == node_id]

    def lineage(self, node_id: int) -> list[Node]:
        out, cur = [], self.nodes.get(node_id)
        while cur is not None:
            out.append(cur)
            cur = self.nodes.get(cur.parent_id) if cur.parent_id is not None else None
        return out[::-1]

    def select_parent(self, method: str = "best", rng: random.Random | None = None) -> Node:
        """Parent for the next child among scored nodes.
        best: highest mean ESQA (ties -> newest node). score_child_prop: HyperAgents weighting."""
        scored = [n for n in self.nodes.values() if n.scores is not None]
        if not scored:
            raise RuntimeError("no scored node to select as parent")
        if method == "best":
            return max(scored, key=lambda n: (n.scores["esqa_mean"], n.node_id))
        rng = rng or random.Random(len(self.nodes))
        sc = [n.scores["esqa_mean"] for n in scored]
        mid = sum(sorted(sc, reverse=True)[:3]) / min(3, len(sc))
        w = [1 / (1 + math.exp(-10 * (n.scores["esqa_mean"] - mid))) *
             math.exp(-((len(self.children(n.node_id)) / 8) ** 3)) for n in scored]
        return rng.choices(scored, weights=w, k=1)[0]

    def select_node(self, rng: random.Random | None = None) -> Node:
        """Unscored node first (lowest id); else a scored node by score_child_prop (HyperAgents)."""
        unscored = [n for n in self.nodes.values() if n.scores is None]
        if unscored:
            return min(unscored, key=lambda n: n.node_id)
        rng = rng or random.Random(0)
        cands = list(self.nodes.values())
        sc = [n.scores["esqa_mean"] for n in cands]
        mid = sum(sorted(sc, reverse=True)[:3]) / min(3, len(sc))
        w = [1 / (1 + math.exp(-10 * (n.scores["esqa_mean"] - mid))) *
             math.exp(-((len(self.children(n.node_id)) / 8) ** 3)) for n in cands]
        return rng.choices(cands, weights=w, k=1)[0]
