"""Meta agent — STUB. A single text-only LLM call (Nemotron), no tools.

Input prompt = policy package (policy.yaml, meta.yaml, prompts, notes.md) + ancestor score
history (if meta.show_archive_history) + `meta.n_failure_traces` dev failure traces.
Output = JSON patch, validated by streamrag.meta.policy.apply_patch. Because meta.txt and
meta.yaml are in the package, the meta agent can rewrite its own instructions.
"""
from __future__ import annotations

from streamrag.meta.archive import GenRecord
from streamrag.meta.policy import PolicyPackage


class MetaAgent:
    def __init__(self, model_name: str = "nemotron-12b-vl"):
        self.model_name = model_name

    def build_prompt(self, pkg: PolicyPackage, history: list[GenRecord], traces: list[dict]) -> str:
        raise NotImplementedError

    def propose(self, pkg: PolicyPackage, history: list[GenRecord], traces: list[dict]) -> dict:
        """Return a JSON patch dict (not yet validated)."""
        raise NotImplementedError
