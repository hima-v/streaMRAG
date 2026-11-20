"""Load each model, run one image caption, one short-clip caption and one text prompt;
log outputs, latency and peak VRAM to outputs/smoke/models.json.

  python scripts/smoke_models.py                       # all models
  python scripts/smoke_models.py --models qwen2-vl-2b nli-deberta-large
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path

import torch
from PIL import Image

from streamrag.config import OUTPUT_DIR, load_yaml
from streamrag.models import load_model, unload

NLI_PAIRS = [  # (premise, hypothesis, expected)
    ("The hallway is empty.", "The hallway is empty of people.", "entailment"),
    ("The hallway is empty.", "A person is walking in the hallway.", "contradiction"),
    ("The hallway is empty.", "The door at the end of the hallway is red.", "neutral"),
]
TEXT_PROMPT = ("Split into atomic claims as a JSON list of {entity, attribute, value}: "
               "'A man walks into the hallway; the door is shut.'")


def sample_inputs() -> tuple[Image.Image, list[Image.Image], str]:
    """One disaster image + 8 frames from a downloaded video (falls back to synthetic)."""
    from streamrag.config import DATA_DIR
    from streamrag.data import get_dataset

    def rel(p: str) -> str:  # keep local absolute paths out of the shared results file
        return str(Path(p).relative_to(DATA_DIR)) if Path(p).is_relative_to(DATA_DIR) else Path(p).name

    img, frames, src = None, None, []
    try:
        s = get_dataset("disastervqa").to_streams(limit=1)[0]
        img = s.observations[0].load_image()
        src.append(rel(s.observations[0].path))
    except Exception as e:  # noqa: BLE001
        print("no DisasterVQA image:", e)
    for name in ("videomme", "m3bench"):
        try:
            streams = get_dataset(name).to_streams(limit=1)
            if streams:
                vis = [o for o in streams[0].observations if o.modality == "frame"]
                pick = [vis[int(i * len(vis) / 8)] for i in range(8)]
                frames = [o.load_image() for o in pick]
                src.append(f"{rel(pick[0].path)} @ {[o.t for o in pick]}")
                break
        except Exception as e:  # noqa: BLE001
            print(f"no {name} frames:", e)
    img = img or Image.new("RGB", (640, 480), "gray")
    frames = frames or [Image.new("RGB", (640, 360), c) for c in ["red", "green"] * 4]
    return img, frames, "; ".join(src) or "synthetic"


def timed(fn):
    torch.cuda.synchronize()
    t0 = time.time()
    out = fn()
    torch.cuda.synchronize()
    return out, round(time.time() - t0, 2)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", nargs="*", default=list(load_yaml("models")))
    ap.add_argument("--out", default=str(OUTPUT_DIR / "smoke" / "models.json"))
    a = ap.parse_args()
    img, frames, src = sample_inputs()
    out_path = Path(a.out)
    results = json.loads(out_path.read_text()) if out_path.exists() else {}
    results["_inputs"] = src

    for name in a.models:
        kind = load_yaml("models")[name]["kind"]
        print(f"\n===== {name} ({kind})")
        torch.cuda.reset_peak_memory_stats()
        r: dict = {"kind": kind}
        model = None
        try:
            model, r["load_s"] = timed(lambda: load_model(name))
            if kind in ("nemotron_vl", "qwen2_vl", "vllm"):
                prompt = "Describe this scene in two sentences for an incident log."
                r["image"], r["image_s"] = timed(lambda: model.generate(prompt, images=[img], max_new_tokens=96))
                r["video"], r["video_s"] = timed(lambda: model.generate(
                    "Describe what happens across these video frames in two sentences.",
                    frames=frames, max_new_tokens=96))
                r["text"], r["text_s"] = timed(lambda: model.generate(TEXT_PROMPT, max_new_tokens=160))
            elif kind == "text_lm":
                r["text"], r["text_s"] = timed(lambda: model.generate(TEXT_PROMPT, max_new_tokens=160))
            elif kind == "nli":
                preds = [model.label(p, h) for p, h, _ in NLI_PAIRS]
                r["nli"] = [{"premise": p, "hypothesis": h, "expected": e, "pred": y}
                            for (p, h, e), y in zip(NLI_PAIRS, preds)]
                r["nli_ok"] = all(x["pred"] == x["expected"] for x in r["nli"])
            elif kind == "embed":
                v = model.encode(["hallway is empty", "nobody in the corridor", "the house is on fire"])
                r["cos_sim"] = [round(float(v[0] @ v[1]), 3), round(float(v[0] @ v[2]), 3)]
            r["ok"] = True
        except Exception as e:  # noqa: BLE001
            import traceback
            traceback.print_exc()
            r["ok"], r["error"] = False, f"{type(e).__name__}: {e}"
        r["peak_vram_gb"] = round(torch.cuda.max_memory_allocated() / 2**30, 2)
        for k, v in r.items():
            print(f"  {k}: {v}")
        results[name] = r
        model = None  # drop our reference so unload() can actually free VRAM
        unload()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(results, indent=1))
    print(f"\nwrote {out_path}")


if __name__ == "__main__":
    main()
