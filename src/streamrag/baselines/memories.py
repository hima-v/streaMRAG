"""Baseline memories (proposal §4.2). All share the Memory interface and the token budget.

fifo              keep the newest notes that fit the budget (drop oldest)
retrieve_all      keep every note (unbounded store); at question time pack the top-k
                  most similar notes into the budget, in time order
latest_replace    a new note replaces its most similar stored note (cos >= threshold);
                  then FIFO eviction. History of the replaced note is lost.
similarity_merge  a new note similar to a stored one (cos >= threshold) is merged into it
                  without checking meaning (time span extended, support +1, text kept);
                  then FIFO eviction.
periodic_summary  when memory exceeds the budget, an LLM rewrites it into a shorter
                  timestamped log (target = summary_target_frac * budget); FIFO as fallback.
acc_rag_lite      (not implemented yet)
"""
from __future__ import annotations

import re

import numpy as np

from streamrag.config import load_yaml
from streamrag.memory.base import Memory, Note, note_from_obs
from streamrag.memory.tokens import count_tokens, fmt_t
from streamrag.types import Observation, QAItem

BASELINES = ["fifo", "retrieve_all", "latest_replace", "similarity_merge", "periodic_summary"]


class NoteMemory(Memory):
    """List of notes kept within budget by dropping the oldest."""

    def __init__(self, budget_tokens: int):
        super().__init__(budget_tokens)
        self.notes: list[Note] = []

    def n_tokens(self) -> int:
        return sum(n.tokens for n in self.notes)

    def render(self, notes: list[Note] | None = None) -> str:
        return "\n".join(n.render() for n in (self.notes if notes is None else notes))

    def evict_fifo(self) -> None:
        total = self.n_tokens()
        while self.notes and total > self.budget:
            total -= self.notes.pop(0).tokens

    def context(self, q: QAItem) -> str:
        return self.render()


class FIFOMemory(NoteMemory):
    name = "fifo"

    def observe(self, obs: Observation) -> None:
        if obs.text:
            self.notes.append(note_from_obs(obs))
            self.evict_fifo()


class _EmbedMixin:
    embedder = None

    def _embed(self, texts: list[str]) -> np.ndarray:
        return self.embedder.encode(texts)


class RetrieveAllMemory(NoteMemory, _EmbedMixin):
    """Unbounded store; the budget applies to the context handed to the reader."""
    name = "retrieve_all"

    def __init__(self, budget_tokens: int, embedder, top_k: int = 64):
        super().__init__(budget_tokens)
        self.embedder, self.top_k = embedder, top_k
        self.vecs: list[np.ndarray] = []

    def observe(self, obs: Observation) -> None:
        if obs.text:
            n = note_from_obs(obs)
            self.notes.append(n)
            self.vecs.append(self._embed([n.text])[0])

    def context(self, q: QAItem) -> str:
        if not self.notes:
            return ""
        query = q.question + (" " + " ".join(map(str, q.options.values() if isinstance(q.options, dict)
                                                  else q.options)) if q.options else "")
        sims = np.stack(self.vecs) @ self._embed([query])[0]
        picked, used = [], 0
        for i in np.argsort(-sims)[: self.top_k]:
            if used + self.notes[i].tokens > self.budget:
                continue
            picked.append(i)
            used += self.notes[i].tokens
        return self.render([self.notes[i] for i in sorted(picked)])


class _SimilarityMemory(NoteMemory, _EmbedMixin):
    def __init__(self, budget_tokens: int, embedder, threshold: float = 0.85):
        super().__init__(budget_tokens)
        self.embedder, self.threshold = embedder, threshold
        self.vecs: list[np.ndarray] = []

    def _match(self, v: np.ndarray, source: str) -> int | None:
        if not self.notes:
            return None
        sims = np.stack(self.vecs) @ v
        for i in np.argsort(-sims):
            if sims[i] < self.threshold:
                return None
            if self.notes[i].source == source:
                return int(i)
        return None

    def evict_fifo(self) -> None:
        total = self.n_tokens()
        while self.notes and total > self.budget:
            total -= self.notes.pop(0).tokens
            self.vecs.pop(0)


class LatestReplaceMemory(_SimilarityMemory):
    name = "latest_replace"

    def observe(self, obs: Observation) -> None:
        if not obs.text:
            return
        n = note_from_obs(obs)
        v = self._embed([n.text])[0]
        i = self._match(v, n.source)
        if i is not None:
            del self.notes[i], self.vecs[i]
        self.notes.append(n)
        self.vecs.append(v)
        self.evict_fifo()


class SimilarityMergeMemory(_SimilarityMemory):
    name = "similarity_merge"

    def observe(self, obs: Observation) -> None:
        if not obs.text:
            return
        n = note_from_obs(obs)
        v = self._embed([n.text])[0]
        i = self._match(v, n.source)
        if i is not None:
            old = self.notes[i]
            old.t_end, old.support = obs.t, old.support + 1
            old.obs_ids.append(obs.obs_id)
            old.touch()
        else:
            self.notes.append(n)
            self.vecs.append(v)
        self.evict_fifo()


SUMMARY_PROMPT = """Rewrite the timestamped notes below into a shorter log of at most {target} tokens.
Keep timestamps, who/what/where, quantities, and every change of state (what was true before and after).
Drop repetition. Write one event per line in the form "[MM:SS] source: text". Output only the log.

Notes:
{notes}

Shorter log:"""

_LINE = re.compile(r"^\s*\[(\d+):(\d{2})(?:-\d+:\d{2})?\]\s*([\w-]+)?\s*(?:\(x\d+\))?\s*:?\s*(.*)$")


class PeriodicSummaryMemory(NoteMemory):
    name = "periodic_summary"

    def __init__(self, budget_tokens: int, llm, target_frac: float = 0.5):
        super().__init__(budget_tokens)
        self.llm, self.target = llm, max(32, int(target_frac * budget_tokens))
        self.n_summaries = 0

    def observe(self, obs: Observation) -> None:
        if not obs.text:
            return
        self.notes.append(note_from_obs(obs))
        if self.n_tokens() > self.budget:
            self._summarize()
            self.evict_fifo()   # fallback if the LLM overshoots the target

    def _summarize(self) -> None:
        t0 = self.notes[0].t_start
        out = self.llm.generate(SUMMARY_PROMPT.format(target=self.target, notes=self.render()),
                                max_new_tokens=int(self.target * 1.3))
        notes = []
        for line in out.splitlines():
            if not line.strip():
                continue
            m = _LINE.match(line)
            if m:
                t = int(m.group(1)) * 60 + int(m.group(2))
                notes.append(Note(t_start=float(t), text=m.group(4).strip(),
                                  source=(m.group(3) or "summary")))
            else:
                notes.append(Note(t_start=notes[-1].t_start if notes else t0,
                                  text=line.strip(), source="summary"))
        self.notes = notes
        self.n_summaries += 1


def build_memory(method: str, budget: int, embedder=None, llm=None) -> Memory:
    cfg = load_yaml("eval")["baselines"]
    if method == "fifo":
        return FIFOMemory(budget)
    if method == "retrieve_all":
        return RetrieveAllMemory(budget, embedder, cfg["retrieve_top_k"])
    if method == "latest_replace":
        return LatestReplaceMemory(budget, embedder, cfg["similarity_threshold"])
    if method == "similarity_merge":
        return SimilarityMergeMemory(budget, embedder, cfg["similarity_threshold"])
    if method == "periodic_summary":
        return PeriodicSummaryMemory(budget, llm, cfg["summary_target_frac"])
    raise ValueError(f"Unknown method '{method}'. Known: {BASELINES}")


def needs(method: str) -> set[str]:
    return {"retrieve_all": {"embedder"}, "latest_replace": {"embedder"},
            "similarity_merge": {"embedder"}, "periodic_summary": {"llm"}}.get(method, set())


__all__ = ["BASELINES", "build_memory", "needs", "fmt_t", "count_tokens"]
