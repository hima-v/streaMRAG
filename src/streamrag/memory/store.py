"""⑤ Bi-temporal claim memory — STUB (implemented after the setup milestones)."""
from __future__ import annotations

from streamrag.types import MemoryEntry


class ClaimMemory:
    def __init__(self):
        self.entries: dict[str, MemoryEntry] = {}

    def render(self) -> str:
        return "\n".join(e.render() for e in self.entries.values())

    def n_tokens(self) -> int:
        raise NotImplementedError

    def valid_at(self, t: float) -> list[MemoryEntry]:
        raise NotImplementedError
