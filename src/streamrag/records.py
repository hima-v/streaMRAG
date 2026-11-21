"""Human-readable run outputs: indented JSON files (one list of records per file).

Older archives wrote one-record-per-line .jsonl; `read_records` reads either, so old runs stay
loadable. Long model outputs are stored as lists of lines so they read naturally.
"""
from __future__ import annotations

import json
from pathlib import Path


def _fmt(obj, level: int = 0, width: int = 100) -> str:
    """Indented JSON in which short lists of plain values stay on one line."""
    pad, inner = "  " * level, "  " * (level + 1)
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        items = [f"{inner}{json.dumps(str(k), ensure_ascii=False)}: {_fmt(v, level + 1, width)}" for k, v in obj.items()]
        return "{\n" + ",\n".join(items) + "\n" + pad + "}"
    if isinstance(obj, (list, tuple)):
        if not obj:
            return "[]"
        if all(not isinstance(x, (dict, list, tuple)) for x in obj):
            flat = json.dumps(list(obj), ensure_ascii=False, default=str)
            if len(flat) + len(inner) <= width:
                return flat
        return "[\n" + ",\n".join(inner + _fmt(x, level + 1, width) for x in obj) + "\n" + pad + "]"
    return json.dumps(obj, ensure_ascii=False, default=str)


def write_json(path: Path, obj) -> Path:
    path = Path(path).with_suffix(".json")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(_fmt(obj) + "\n")
    return path


def read_records(path: Path) -> list:
    """Read <name>.json (list) or, for older runs, <name>.jsonl."""
    path = Path(path)
    j, jl = path.with_suffix(".json"), path.with_suffix(".jsonl")
    if j.exists():
        return json.loads(j.read_text())
    if jl.exists():
        return [json.loads(line) for line in jl.read_text().splitlines() if line.strip()]
    raise FileNotFoundError(f"{j} (or {jl.name}) not found")


def lines(text: str) -> list[str]:
    """Store long model output as a list of lines (readable in indented JSON)."""
    return text.splitlines() or [""]
