"""④ Typed update operator — STUB (implemented after the setup milestones)."""
from __future__ import annotations

from streamrag.memory.store import ClaimMemory
from streamrag.types import Claim, MemoryEntry, Relation


def apply_update(memory: ClaimMemory, claim: Claim, relation: Relation, match: MemoryEntry | None) -> None:
    raise NotImplementedError
