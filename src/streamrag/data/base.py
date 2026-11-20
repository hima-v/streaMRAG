"""Dataset protocol: download() fetches raw files, load() returns raw records,
to_streams() converts them to the common Stream format used by the pipeline."""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from streamrag.config import PROCESSED_DIR, RAW_DIR, data_cfg
from streamrag.types import Stream


class StreamDataset(ABC):
    name: str

    def __init__(self, **overrides):
        self.cfg = {**data_cfg(self.name), **overrides}
        self.raw = RAW_DIR / self.name
        self.processed = PROCESSED_DIR / self.name

    @abstractmethod
    def download(self, **kw) -> None: ...

    @abstractmethod
    def load(self) -> list[dict]:
        """Raw annotation records."""

    @abstractmethod
    def to_streams(self, limit: int | None = None) -> list[Stream]: ...

    def require(self, path: Path) -> Path:
        if not path.exists():
            raise FileNotFoundError(
                f"{path} missing. Run: python scripts/download_data.py {self.name}")
        return path
