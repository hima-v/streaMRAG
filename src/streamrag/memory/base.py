"""Common interface for every memory method (baselines and streaMRAG).

All methods see the same text observations in time order and must answer from at most
`budget_tokens` of context. Only memory management differs between methods.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from streamrag.memory.tokens import count_tokens, fmt_t
from streamrag.types import Observation, QAItem


@dataclass
class Note:
    """One memory line for the note-based baselines."""
    t_start: float
    text: str
    source: str
    t_end: float | None = None
    support: int = 1
    obs_ids: list[str] = field(default_factory=list)
    _tokens: int | None = field(default=None, repr=False)

    def render(self) -> str:
        span = fmt_t(self.t_start) if self.t_end in (None, self.t_start) else \
            f"{fmt_t(self.t_start)}-{fmt_t(self.t_end)}"
        sup = f" (x{self.support})" if self.support > 1 else ""
        return f"[{span}] {self.source}{sup}: {self.text}"

    @property
    def tokens(self) -> int:
        if self._tokens is None:
            self._tokens = count_tokens(self.render()) + 1   # +1 for the newline
        return self._tokens

    def touch(self) -> None:
        self._tokens = None


class Memory(ABC):
    name: str = "memory"

    def __init__(self, budget_tokens: int):
        self.budget = budget_tokens

    @abstractmethod
    def observe(self, obs: Observation) -> None:
        """Ingest one text observation (caption, subtitle, report line)."""

    @abstractmethod
    def context(self, q: QAItem) -> str:
        """Evidence text given to the reader for question q (<= budget tokens)."""

    @abstractmethod
    def n_tokens(self) -> int:
        """Current stored memory size in tokens."""


def note_from_obs(obs: Observation) -> Note:
    return Note(t_start=obs.t, text=" ".join((obs.text or "").split()), source=obs.source,
                obs_ids=[obs.obs_id])
