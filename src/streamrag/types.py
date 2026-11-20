"""Shared data types. Every dataset is converted to Streams of Observations + QAItems,
and every pipeline stage after perception works on text (Claims / MemoryEntries)."""
from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Literal

from PIL import Image

Modality = Literal["image", "frame", "text"]


@dataclass
class Observation:
    """One element of an input stream, delivered at stream time `t` (seconds)."""
    obs_id: str
    stream_id: str
    t: float
    source: str                     # "camera", "social", "asr", "sitrep", ...
    modality: Modality
    path: str | None = None         # image file, or video file for modality="frame"
    text: str | None = None         # native text, or a cached caption
    meta: dict = field(default_factory=dict)

    def load_image(self) -> Image.Image:
        """Decode the image (or the video frame at time t)."""
        if self.modality == "image":
            return Image.open(self.path).convert("RGB")
        if self.modality == "frame":
            from streamrag.video.frames import frame_at
            return frame_at(self.path, self.meta.get("video_t", self.t))
        raise ValueError(f"{self.obs_id} is a text observation")


@dataclass
class QAItem:
    qa_id: str
    stream_id: str
    question: str
    answer: str | list[str]
    options: list[str] | dict[str, str] | None = None
    t_query: float | None = None    # stream time at which the question is asked
    qtype: str | list[str] | None = None
    evidence_ids: list[str] | None = None
    meta: dict = field(default_factory=dict)


@dataclass
class Stream:
    stream_id: str
    dataset: str
    observations: list[Observation]
    qa: list[QAItem]
    meta: dict = field(default_factory=dict)

    @property
    def duration(self) -> float:
        return max((o.t for o in self.observations), default=0.0)


# ---- Phase 1 memory types (used by the stubs in streamrag.memory) ----

class Relation(str, Enum):
    REINFORCE = "reinforce"
    ADD = "add"
    STATE_CHANGE = "state_change"
    CONFLICT = "conflict"


@dataclass
class Claim:
    """Atomic fact extracted from one observation."""
    claim_id: str
    entity: str
    attribute: str
    value: str
    t: float
    source: str
    obs_id: str
    modality: Modality = "text"
    hedged: bool = False
    confidence: float = 1.0


@dataclass
class MemoryEntry:
    """Bi-temporal memory line: a claim valid on [t_start, t_end)."""
    entry_id: str
    claim: Claim
    t_start: float
    t_end: float | None = None
    status: Literal["active", "superseded", "conflict"] = "active"
    support: int = 1
    source_ids: list[str] = field(default_factory=list)
    linked: list[str] = field(default_factory=list)   # conflict partners / predecessor

    def render(self) -> str:
        end = "" if self.t_end is None else f"{self.t_end:.0f}"
        return (f"#{self.entry_id} [{self.t_start:.0f}-{end}) "
                f"{self.claim.entity}.{self.claim.attribute}={self.claim.value} x{self.support}")
