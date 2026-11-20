"""Perception: VLM captions for frames/images, cached to outputs/captions/<dataset>/<stream_id>.jsonl — STUB (implemented after the setup milestones)."""
from __future__ import annotations

from pathlib import Path

from streamrag.config import OUTPUT_DIR
from streamrag.types import Observation, Stream


def cache_path(stream: Stream, model: str) -> Path:
    return OUTPUT_DIR / "captions" / model / stream.dataset / f"{stream.stream_id}.jsonl"


def caption_stream(stream: Stream, model: str, prompt: str) -> list[Observation]:
    """Return text observations (one caption per visual observation), reading/writing the cache."""
    raise NotImplementedError
