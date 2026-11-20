"""Project paths and YAML config loading."""
from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = ROOT / "configs"
DATA_DIR = Path(os.environ.get("STREAMRAG_DATA", ROOT / "data"))
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
OUTPUT_DIR = Path(os.environ.get("STREAMRAG_OUTPUTS", ROOT / "outputs"))


@lru_cache(maxsize=None)
def load_yaml(name: str) -> dict:
    """Load configs/<name>.yaml (cached)."""
    with open(CONFIG_DIR / f"{name}.yaml") as f:
        return yaml.safe_load(f)


def model_cfg(name: str) -> dict:
    cfgs = load_yaml("models")
    if name not in cfgs:
        raise KeyError(f"Unknown model '{name}'. Known: {sorted(cfgs)}")
    return dict(cfgs[name])


def data_cfg(name: str) -> dict:
    cfg = load_yaml("data")
    return {"seed": cfg.get("seed", 0), **cfg[name]}
