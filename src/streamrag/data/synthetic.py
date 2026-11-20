"""Simulated incident streams (pipeline_planning.md §1) — STUB.

Planned: a parent VLM (Nemotron) is shown a subset of DisasterVQA images / Video-MME clips
and writes (1) a ~300-word situation report, (2) QA pairs grounded in the visual evidence,
(3) gold relation labels (reinforce / add / state-change / conflict) between consecutive
evidence items. Each report R_i with evidence E_i is emitted in j random delivery orders.
These give the gold-labelled streams for H1 (relation macro-F1).
"""
from __future__ import annotations

from streamrag.data.base import StreamDataset
from streamrag.types import Stream


class SyntheticIncidents(StreamDataset):
    name = "synthetic"

    def __init__(self, **overrides):  # no configs/data.yaml entry yet
        self.cfg = overrides

    def download(self, **kw) -> None:
        raise NotImplementedError("Synthetic streams are generated, not downloaded.")

    def load(self) -> list[dict]:
        raise NotImplementedError

    def to_streams(self, limit: int | None = None) -> list[Stream]:
        raise NotImplementedError
