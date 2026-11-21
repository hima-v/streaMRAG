"""Meta agent (codebase_plan.md §11.4): the same Nemotron as the memory agent (reasoning off),
driven by its meta harness. It sees only its direct parent's strategy, harness and evaluation log,
and samples with a fixed seed per child (reproducible; a re-selected parent gets a new attempt).
Creating a child makes two calls:
  1. harness update: current harness H + evaluated strategy S + evaluation log -> new harness H'
  2. strategy update: following H', parent strategy S + evaluation log -> child strategy S'
Each call is skipped (text copied) when its switch is 'fixed'.
"""
from __future__ import annotations

from streamrag.config import CONFIG_DIR, load_yaml
from streamrag.parsing import parse_tag

HARNESS_FRAME = (CONFIG_DIR / "meta" / "frames" / "harness_update.txt").read_text()
STRATEGY_FRAME = (CONFIG_DIR / "meta" / "frames" / "strategy_update.txt").read_text()


def _clean(text: str) -> str:
    """Drop prompt delimiters the model sometimes copies (<<< >>>)."""
    return text.replace("<<<", "").replace(">>>", "").strip()


def _cap_words(text: str, n: int) -> str:
    """Keep at most n words, cutting at the last sentence end inside the limit when possible."""
    text = _clean(text)
    words = text.split()
    if len(words) <= n:
        return text
    cut = " ".join(words[:n])
    end = max(cut.rfind(". "), cut.rfind(".\n"), cut.rfind("\n"))
    return cut[:end + 1].strip() if end > len(cut) // 2 else cut


class MetaAgent:
    def __init__(self, vlm, dataset: str, harness_frame: str | None = None, strategy_frame: str | None = None):
        self.vlm, self.dataset = vlm, dataset
        self.harness_frame = harness_frame or HARNESS_FRAME
        self.strategy_frame = strategy_frame or STRATEGY_FRAME
        cfg = load_yaml("eval")
        self.max_new_tokens = cfg["meta_agent"]["max_new_tokens"]
        self.max_harness_words = cfg["meta_agent"]["max_harness_words"]
        self.max_strategy_words = cfg["memory_agent"]["max_strategy_words"]
        m = cfg["meta_agent"]
        self.gen = {"repetition_penalty": m.get("repetition_penalty"), "temperature": m.get("temperature"),
                    "top_p": m.get("top_p")}

    def update_harness(self, harness: str, strategy: str, log: str, seed: int | None = None) -> dict:
        prompt = self.harness_frame.format(dataset=self.dataset, harness=harness.strip(), strategy=strategy.strip(),
                                      log=log, max_words=self.max_harness_words)
        raw = self.vlm.generate(prompt, max_new_tokens=self.max_new_tokens, seed=seed, **self.gen)
        new = parse_tag(raw, "harness")
        return {"text": _cap_words(new, self.max_harness_words) if new else harness,
                "rationale": parse_tag(raw, "rationale") or "", "raw": raw, "parsed": bool(new)}

    def update_strategy(self, harness: str, strategy: str, log: str, budget: int, seed: int | None = None) -> dict:
        prompt = self.strategy_frame.format(dataset=self.dataset, harness=harness.strip(), strategy=strategy.strip(),
                                       log=log, budget=budget, max_words=self.max_strategy_words)
        raw = self.vlm.generate(prompt, max_new_tokens=self.max_new_tokens, seed=seed, **self.gen)
        new = parse_tag(raw, "strategy")
        changes = [c.strip("- ").strip() for c in (parse_tag(raw, "changes") or "").splitlines() if c.strip()]
        return {"text": _cap_words(new, self.max_strategy_words) if new else strategy,
                "rationale": parse_tag(raw, "rationale") or "", "changes": changes, "raw": raw,
                "parsed": bool(new)}
