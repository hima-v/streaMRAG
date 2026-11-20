"""Caption every visual observation once and cache the text (milestone M4) — STUB.

  python scripts/cache_captions.py videomme --model nemotron-12b-vl --limit 5

Planned: for each stream, for each frame/image observation, run the VLM with
configs/policy/default/prompts/caption.txt and append {obs_id, t, caption, model} to
outputs/captions/<model>/<dataset>/<stream_id>.jsonl (resume-safe). Everything downstream
(memory, baselines, meta loop) reads these captions instead of the VLM.
"""
from __future__ import annotations

if __name__ == "__main__":
    raise SystemExit("Not implemented yet (milestone M4). See streamrag.perception.caption.")
