"""Sentence embedder for candidate retrieval."""
from __future__ import annotations

import numpy as np
from sentence_transformers import SentenceTransformer


class Embedder:
    def __init__(self, name: str, cfg: dict):
        self.name, self.cfg = name, cfg
        self.model = SentenceTransformer(cfg["hf_id"], device=cfg.get("device", "cuda:0"))

    def encode(self, texts: list[str]) -> np.ndarray:
        return self.model.encode(texts, normalize_embeddings=True, convert_to_numpy=True)
