"""③ Temporal NLI relation classifier: NLI(stored, new) + temporal gate — STUB (implemented after the setup milestones)."""
from __future__ import annotations

from streamrag.types import Claim, MemoryEntry, Relation


def classify(new: Claim, stored: list[MemoryEntry], policy: dict) -> tuple[Relation, MemoryEntry | None]:
    """entail -> REINFORCE; neutral/no match -> ADD;
    contradict & dt > tau & mutable attribute -> STATE_CHANGE; otherwise contradict -> CONFLICT."""
    raise NotImplementedError
