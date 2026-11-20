"""Policy packages and validated meta-agent patches.

A policy package is a directory: policy.yaml, meta.yaml, notes.md, prompts/*.txt.
The meta agent returns a JSON patch; `apply_patch` accepts ONLY
  - new values for existing keys of policy.yaml / meta.yaml (same type, within RANGES),
  - full replacement text for the four allowed prompt files,
  - replacement text for notes.md.
Anything else (new keys, other files, code) is rejected. The meta agent has no tools:
no bash, no file access, no Python edits.
"""
from __future__ import annotations

import copy
import shutil
from dataclasses import dataclass, field
from pathlib import Path

import yaml

from streamrag.config import CONFIG_DIR

DEFAULT_POLICY = CONFIG_DIR / "policy" / "default"
PROMPT_FILES = ("caption.txt", "claims.txt", "qa.txt", "meta.txt")
MAX_TEXT_CHARS = 4000

# Numeric ranges for editable keys (dotted paths). Keys not listed keep type checks only.
RANGES: dict[str, tuple[float, float]] = {
    "budget_tokens": (256, 1024),
    "retrieval.top_k": (1, 50),
    "retrieval.min_similarity": (0.0, 1.0),
    "nli.entail_threshold": (0.0, 1.0),
    "nli.contradict_threshold": (0.0, 1.0),
    "temporal.tau_seconds": (0, 3600),
    "eviction_weights.support": (0.0, 10.0),
    "eviction_weights.recency": (0.0, 10.0),
    "eviction_weights.relation_bonus": (0.0, 10.0),
    "qa.max_evidence_lines": (1, 200),
    "n_failure_traces": (1, 100),
    "max_edits_per_step": (1, 10),
}
FROZEN = {"budget_tokens"}   # the memory budget is an experimental condition, not a knob


class PatchError(ValueError):
    pass


@dataclass
class PolicyPackage:
    policy: dict
    meta: dict
    prompts: dict[str, str]
    notes: str = ""
    path: Path | None = field(default=None, compare=False)

    @classmethod
    def load(cls, path: Path = DEFAULT_POLICY) -> "PolicyPackage":
        path = Path(path)
        return cls(policy=yaml.safe_load((path / "policy.yaml").read_text()),
                   meta=yaml.safe_load((path / "meta.yaml").read_text()),
                   prompts={f: (path / "prompts" / f).read_text() for f in PROMPT_FILES},
                   notes=(path / "notes.md").read_text() if (path / "notes.md").exists() else "",
                   path=path)

    def save(self, path: Path) -> None:
        path = Path(path)
        if path.exists():
            shutil.rmtree(path)
        (path / "prompts").mkdir(parents=True)
        (path / "policy.yaml").write_text(yaml.safe_dump(self.policy, sort_keys=False))
        (path / "meta.yaml").write_text(yaml.safe_dump(self.meta, sort_keys=False))
        (path / "notes.md").write_text(self.notes)
        for f, text in self.prompts.items():
            (path / "prompts" / f).write_text(text)
        self.path = path

    def get(self, dotted: str):
        node = self.policy
        for k in dotted.split("."):
            node = node[k]
        return node


def _set_checked(tree: dict, dotted: str, value, where: str) -> None:
    keys = dotted.split(".")
    node = tree
    for k in keys[:-1]:
        if not isinstance(node, dict) or k not in node:
            raise PatchError(f"{where}: unknown key '{dotted}'")
        node = node[k]
    leaf = keys[-1]
    if not isinstance(node, dict) or leaf not in node:
        raise PatchError(f"{where}: unknown key '{dotted}'")
    if dotted in FROZEN:
        raise PatchError(f"{where}: '{dotted}' is frozen")
    old = node[leaf]
    if isinstance(old, dict):
        raise PatchError(f"{where}: '{dotted}' is a section; edit its leaves")
    if isinstance(old, bool) != isinstance(value, bool):
        raise PatchError(f"{where}: '{dotted}' must be {type(old).__name__}")
    if isinstance(old, (int, float)) and not isinstance(old, bool):
        if not isinstance(value, (int, float)):
            raise PatchError(f"{where}: '{dotted}' must be numeric")
        lo, hi = RANGES.get(dotted, (float("-inf"), float("inf")))
        if not lo <= value <= hi:
            raise PatchError(f"{where}: '{dotted}'={value} outside [{lo}, {hi}]")
        value = type(old)(value) if isinstance(old, int) and float(value).is_integer() else value
    elif isinstance(old, list):
        if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
            raise PatchError(f"{where}: '{dotted}' must be a list of strings")
    elif isinstance(old, str) and not isinstance(value, str):
        raise PatchError(f"{where}: '{dotted}' must be a string")
    node[leaf] = value


def apply_patch(pkg: PolicyPackage, patch: dict) -> tuple[PolicyPackage, int]:
    """Return (new package, number of edits). Raises PatchError on any disallowed edit."""
    allowed_top = {"policy", "meta", "prompts", "notes", "rationale"}
    if extra := set(patch) - allowed_top:
        raise PatchError(f"unknown patch fields {sorted(extra)}")
    new = copy.deepcopy(pkg)
    n = 0
    for k, v in (patch.get("policy") or {}).items():
        _set_checked(new.policy, k, v, "policy")
        n += 1
    for k, v in (patch.get("meta") or {}).items():
        _set_checked(new.meta, k, v, "meta")
        n += 1
    for f, text in (patch.get("prompts") or {}).items():
        if f not in PROMPT_FILES:
            raise PatchError(f"prompts: '{f}' is not an editable prompt file")
        if not isinstance(text, str) or not text.strip() or len(text) > MAX_TEXT_CHARS:
            raise PatchError(f"prompts: '{f}' must be non-empty text <= {MAX_TEXT_CHARS} chars")
        new.prompts[f] = text
        n += 1
    if "notes" in patch:
        if not isinstance(patch["notes"], str) or len(patch["notes"]) > MAX_TEXT_CHARS:
            raise PatchError(f"notes must be text <= {MAX_TEXT_CHARS} chars")
        new.notes = patch["notes"]
    if n > pkg.meta.get("max_edits_per_step", 3):
        raise PatchError(f"{n} edits > max_edits_per_step={pkg.meta['max_edits_per_step']}")
    return new, n
