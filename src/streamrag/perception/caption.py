"""Perception: caption every visual observation once and cache the text.

Cache: outputs/captions/<model>/<prompt_hash>/<dataset>/<stream_id>.jsonl, one line per
visual observation: {obs_id, t, source, caption, secs}. Resume-safe: existing lines are
reused. Changing the caption prompt or max_new_tokens changes <prompt_hash>, so different
caption settings never mix. All memory methods read the same cached captions.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path

from streamrag.config import OUTPUT_DIR
from streamrag.types import Observation, Stream
from streamrag.video.frames import frames_at


def caption_key(prompt: str, max_new_tokens: int) -> str:
    return hashlib.sha1(f"{prompt}\x00{max_new_tokens}".encode()).hexdigest()[:8]


def cache_path(stream: Stream, model: str, key: str) -> Path:
    return OUTPUT_DIR / "captions" / model / key / stream.dataset / f"{stream.stream_id}.jsonl"


def read_cache(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text().splitlines():
        if line.strip():
            rec = json.loads(line)
            out[rec["obs_id"]] = rec
    return out


def is_complete(stream: Stream, model: str, key: str) -> bool:
    """True if every visual observation of the stream has a cached caption."""
    cache = read_cache(cache_path(stream, model, key))
    return all(o.obs_id in cache for o in stream.observations if o.modality != "text")


def caption_stream(stream: Stream, vlm, model: str, prompt: str,
                   max_new_tokens: int = 96) -> tuple[int, float]:
    """Caption all uncached visual observations. Returns (n_new, seconds spent)."""
    key = caption_key(prompt, max_new_tokens)
    path = cache_path(stream, model, key)
    done = read_cache(path)
    todo = [o for o in stream.observations if o.modality != "text" and o.obs_id not in done]
    if not todo:
        return 0, 0.0
    path.parent.mkdir(parents=True, exist_ok=True)
    spent = 0.0
    # decode all frames of one video in a single pass
    frames: dict[str, object] = {}
    vids: dict[str, list[Observation]] = {}
    for o in todo:
        if o.modality == "frame":
            vids.setdefault(o.path, []).append(o)
    for vpath, obs in vids.items():
        times = [o.meta.get("video_t", o.t) for o in obs]
        for o, im in zip(sorted(obs, key=lambda x: x.meta.get("video_t", x.t)),
                         frames_at(vpath, sorted(times))):
            frames[o.obs_id] = im
    with open(path, "a") as f:
        for o in todo:
            img = frames.pop(o.obs_id, None) or o.load_image()
            t0 = time.time()
            cap = vlm.generate(prompt, images=[img], max_new_tokens=max_new_tokens)
            dt = time.time() - t0
            spent += dt
            f.write(json.dumps({"obs_id": o.obs_id, "t": o.t, "source": o.source,
                                "caption": " ".join(cap.split()), "secs": round(dt, 2)}) + "\n")
            f.flush()
    return len(todo), spent


def text_stream(stream: Stream, model: str, prompt: str, max_new_tokens: int = 96,
                strict: bool = True) -> list[Observation]:
    """The stream as text only: cached captions replace visual observations, native text
    (subtitles, dialogue, reports) passes through. Sorted by time."""
    path = cache_path(stream, model, caption_key(prompt, max_new_tokens))
    cache = read_cache(path)
    out: list[Observation] = []
    missing = 0
    for o in stream.observations:
        if o.modality == "text":
            out.append(o)
        elif o.obs_id in cache:
            out.append(Observation(o.obs_id, o.stream_id, o.t, o.source, "text",
                                   text=cache[o.obs_id]["caption"],
                                   meta={**o.meta, "caption_of": o.modality, "path": o.path}))
        else:
            missing += 1
    if missing and strict:
        raise FileNotFoundError(
            f"{missing} uncached visual observations in {stream.stream_id}. Run: "
            f"python scripts/cache_captions.py {stream.dataset} --model {model}")
    return sorted(out, key=lambda o: o.t)
