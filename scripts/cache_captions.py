"""Caption every visual observation once and cache the text (milestone M4).

  python scripts/cache_captions.py videomme m3bench --split dev
  python scripts/cache_captions.py mindcube --split dev --limit 10
  python scripts/cache_captions.py videomme --model qwen2-vl-7b --limit 1   # compare captioners

Uses configs/policy/default/prompts/caption.txt and configs/eval.yaml (captioner,
caption_max_new_tokens). Resume-safe; only downloaded videos are captioned.
"""
from __future__ import annotations

import argparse
import time

from streamrag.config import load_yaml
from streamrag.data import get_dataset
from streamrag.eval.splits import filter_split
from streamrag.meta.policy import PolicyPackage
from streamrag.models import load_model
from streamrag.perception.caption import caption_key, caption_stream


def main() -> None:
    cfg = load_yaml("eval")
    ap = argparse.ArgumentParser()
    ap.add_argument("datasets", nargs="+")
    ap.add_argument("--model", default=cfg["captioner"])
    ap.add_argument("--split", default="dev", choices=["dev", "test", "all"])
    ap.add_argument("--limit", type=int, help="max streams per dataset")
    ap.add_argument("--max-new-tokens", type=int, default=cfg["caption_max_new_tokens"])
    a = ap.parse_args()

    prompt = PolicyPackage.load().prompts["caption.txt"]
    key = caption_key(prompt, a.max_new_tokens)
    vlm = load_model(a.model)
    print(f"captioner={a.model} key={key} max_new_tokens={a.max_new_tokens}")
    for name in a.datasets:
        streams = filter_split(get_dataset(name).to_streams(), name, a.split)[: a.limit]
        n_tot = s_tot = 0.0
        t0 = time.time()
        for i, s in enumerate(streams):
            n, secs = caption_stream(s, vlm, a.model, prompt, a.max_new_tokens)
            n_tot += n
            s_tot += secs
            if n:
                print(f"[{name}] {i + 1}/{len(streams)} {s.stream_id}: {n} captions, "
                      f"{secs / n:.2f} s/caption", flush=True)
        rate = f"{s_tot / n_tot:.2f} s/caption" if n_tot else "all cached"
        print(f"[{name}] {len(streams)} streams, {int(n_tot)} new captions, {rate}, "
              f"wall {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
