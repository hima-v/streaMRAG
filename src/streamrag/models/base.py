"""Model interfaces. Every VLM / LM wrapper exposes the same generate() signature."""
from __future__ import annotations

from abc import ABC, abstractmethod

import torch
from PIL import Image


class VLM(ABC):
    """Vision-language model. Text-only calls pass neither images nor frames."""

    name: str

    @abstractmethod
    def generate(self, prompt: str, images: list[Image.Image] | None = None,
                 frames: list[Image.Image] | None = None, system: str | None = None,
                 max_new_tokens: int = 256) -> str: ...


class TextLM(ABC):
    name: str

    @abstractmethod
    def generate(self, prompt: str, system: str | None = None,
                 max_new_tokens: int = 256) -> str: ...


def torch_dtype(name: str | None) -> torch.dtype | str:
    return {"bfloat16": torch.bfloat16, "float16": torch.float16,
            "float32": torch.float32, None: "auto"}[name]


def free_cuda() -> None:
    import gc
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
