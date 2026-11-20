"""② Candidate retrieval: embedding top-k + entity/attribute key + alias resolution — STUB (implemented after the setup milestones)."""
from __future__ import annotations

from streamrag.memory.store import ClaimMemory
from streamrag.types import Claim, MemoryEntry


def candidates(claim: Claim, memory: ClaimMemory, top_k: int, min_similarity: float) -> list[MemoryEntry]:
    raise NotImplementedError
