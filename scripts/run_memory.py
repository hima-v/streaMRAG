"""Run memory method(s) over a dataset split from cached captions and write predictions.

  python scripts/run_memory.py mindcube --methods fifo retrieve_all --budgets 256 1024
  python scripts/run_memory.py m3bench --methods all --budgets 1024 --reader nemotron-12b-vl
  python scripts/run_memory.py disastervqa --methods fifo --limit 2 --reader qwen2-vl-2b   # quick check

Then score with: python scripts/score_run.py outputs/runs/<dataset>/<split>/<run>
"""
from __future__ import annotations

import argparse

from streamrag.baselines.memories import BASELINES, build_memory, needs
from streamrag.config import load_yaml
from streamrag.data import get_dataset
from streamrag.eval.runner import run_dataset, run_dir
from streamrag.eval.splits import filter_split
from streamrag.meta.policy import PolicyPackage
from streamrag.models import load_model
from streamrag.perception.caption import caption_key, is_complete, text_stream


def main() -> None:
    cfg = load_yaml("eval")
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("--methods", nargs="+", default=["fifo"], help=f"{BASELINES} or 'all'")
    ap.add_argument("--budgets", nargs="+", type=int, default=cfg["budgets"])
    ap.add_argument("--split", default="dev", choices=["dev", "test", "all"])
    ap.add_argument("--reader", default=cfg["reader"])
    ap.add_argument("--captioner", default=cfg["captioner"])
    ap.add_argument("--caption-max-new-tokens", type=int, default=cfg["caption_max_new_tokens"])
    ap.add_argument("--limit", type=int, help="max streams")
    ap.add_argument("--tag", default="")
    a = ap.parse_args()
    methods = BASELINES if a.methods == ["all"] else a.methods

    prompt = PolicyPackage.load().prompts["caption.txt"]
    key = caption_key(prompt, a.caption_max_new_tokens)
    streams = filter_split(get_dataset(a.dataset).to_streams(), a.dataset, a.split)
    cached = [s for s in streams if is_complete(s, a.captioner, key)]
    if len(cached) < len(streams):
        print(f"{len(streams) - len(cached)} of {len(streams)} streams are not fully captioned; "
              f"skipping them (run scripts/cache_captions.py {a.dataset} --split {a.split})")
    streams = cached[: a.limit]
    if not streams:
        raise SystemExit("nothing to run")

    reader = load_model(a.reader)
    embedder = load_model("embed-bge-small") if any("embedder" in needs(m) for m in methods) else None
    obs_cache: dict[str, list] = {}

    def get_obs(s):
        if s.stream_id not in obs_cache:
            obs_cache[s.stream_id] = text_stream(s, a.captioner, prompt, a.caption_max_new_tokens)
        return obs_cache[s.stream_id]

    for m in methods:
        for b in a.budgets:
            out = run_dir(a.dataset, a.split, m, b, a.reader, a.tag)
            print(f"== {m} B={b} -> {out}")
            run_dataset(streams, get_obs, lambda: build_memory(m, b, embedder=embedder, llm=reader),
                        reader, out, {"dataset": a.dataset, "split": a.split, "method": m,
                                      "budget": b, "reader": a.reader, "captioner": a.captioner,
                                      "caption_key": key, "n_streams": len(streams)})


if __name__ == "__main__":
    main()
