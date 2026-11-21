"""Fixed dev/test splits by video / scene (never by question).

Units: Video-MME = selected video, M3-Bench = robot video, MindCube = scene (photo folder),
DisasterVQA = pseudo-stream (all orderings of one stream share a unit). The split is
computed over the full unit list (not only what is downloaded) and saved to
data/processed/splits.json so every teammate gets the same split.
"""
from __future__ import annotations

import json
import random

from streamrag.config import PROCESSED_DIR, load_yaml
from streamrag.types import Stream

SPLITS_PATH = PROCESSED_DIR / "splits.json"


def _units(dataset: str) -> list[str]:
    from streamrag.data import get_dataset
    ds = get_dataset(dataset)
    if dataset == "videomme":
        return [f"vmme-{v}" for v in ds.selected()]
    if dataset == "m3bench":
        return [f"m3r-{r['video']}" for r in ds.load()]
    if dataset == "mindcube":
        return sorted({s.meta["split_key"] for s in ds.to_streams()})
    if dataset == "disastervqa":
        return sorted({s.meta["split_key"] for s in ds.to_streams()})
    raise KeyError(dataset)


def make_splits(datasets: list[str] | None = None, overwrite: bool = False) -> dict:
    cfg = load_yaml("eval")["splits"]
    splits = json.loads(SPLITS_PATH.read_text()) if SPLITS_PATH.exists() else {}
    for name in datasets or list(cfg["dev"]):
        if name in splits and not overwrite:
            continue
        units = sorted(_units(name))
        random.Random(f"{cfg['seed']}-{name}").shuffle(units)
        n = cfg["dev"][name]
        n_dev = n if isinstance(n, int) else round(n * len(units))
        splits[name] = {"dev": sorted(units[:n_dev]), "test": sorted(units[n_dev:])}
    SPLITS_PATH.parent.mkdir(parents=True, exist_ok=True)
    SPLITS_PATH.write_text(json.dumps(splits, indent=1))
    return splits


def split_units(dataset: str, split: str) -> set[str]:
    splits = json.loads(SPLITS_PATH.read_text()) if SPLITS_PATH.exists() else {}
    if dataset not in splits:
        splits = make_splits([dataset])
    return set(splits[dataset][split])


def filter_split(streams: list[Stream], dataset: str, split: str | None) -> list[Stream]:
    if split in (None, "all"):
        return streams
    units = split_units(dataset, split)
    return [s for s in streams if s.meta.get("split_key", s.stream_id) in units]
