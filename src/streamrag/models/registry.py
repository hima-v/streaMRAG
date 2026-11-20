"""load_model(name) -> wrapper instance, based on configs/models.yaml. Instances are cached."""
from __future__ import annotations

from streamrag.config import model_cfg
from streamrag.models.base import free_cuda

_CACHE: dict[str, object] = {}


def _cls(kind: str):
    if kind == "nemotron_vl":
        from streamrag.models.nemotron_vl import NemotronVL
        return NemotronVL
    if kind == "qwen2_vl":
        from streamrag.models.qwen2_vl import Qwen2VL
        return Qwen2VL
    if kind == "text_lm":
        from streamrag.models.text_lm import HFTextLM
        return HFTextLM
    if kind == "nli":
        from streamrag.models.nli import NLIModel
        return NLIModel
    if kind == "embed":
        from streamrag.models.embed import Embedder
        return Embedder
    if kind == "vllm":
        from streamrag.models.vllm_client import VLLMClient
        return VLLMClient
    raise ValueError(f"Unknown model kind '{kind}'")


def load_model(name: str, **overrides):
    if name not in _CACHE:
        cfg = {**model_cfg(name), **overrides}
        _CACHE[name] = _cls(cfg["kind"])(name, cfg)
    return _CACHE[name]


def unload(name: str | None = None) -> None:
    """Drop one (or all) cached models and free GPU memory."""
    for k in [name] if name else list(_CACHE):
        _CACHE.pop(k, None)
    free_cuda()
