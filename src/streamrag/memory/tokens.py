"""Token counting for memory budgets (one tokenizer for every method: configs/eval.yaml)."""
from __future__ import annotations

from functools import lru_cache

from streamrag.config import load_yaml, model_cfg


@lru_cache(maxsize=1)
def _tokenizer():
    from transformers import AutoTokenizer
    name = load_yaml("eval")["budget_tokenizer"]
    return AutoTokenizer.from_pretrained(model_cfg(name)["hf_id"], trust_remote_code=True)


@lru_cache(maxsize=200_000)
def count_tokens(text: str) -> int:
    return len(_tokenizer()(text, add_special_tokens=False).input_ids)


def fmt_t(t: float | None) -> str:
    """Seconds -> 'MM:SS' (minutes unbounded)."""
    if t is None:
        return "--:--"
    m, s = divmod(int(round(t)), 60)
    return f"{m:02d}:{s:02d}"
