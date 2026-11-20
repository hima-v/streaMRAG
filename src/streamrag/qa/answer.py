"""Phase 2: parse question -> time-anchored retrieval -> chronological chain -> answer/abstain — STUB (implemented after the setup milestones)."""
from __future__ import annotations

from streamrag.memory.store import ClaimMemory
from streamrag.types import QAItem


def answer(q: QAItem, memory: ClaimMemory, policy: dict, prompt: str) -> dict:
    """Return {"answer": str, "cited": [entry_ids], "abstained": bool}."""
    raise NotImplementedError
