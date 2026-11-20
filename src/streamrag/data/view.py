"""View dataset samples.

  python -m streamrag.data.view disastervqa --n 2
  python -m streamrag.data.view videomme --n 1 --max-frames 12
  python -m streamrag.data.view m3bench --stream m3r-bedroom_01

Prints the observation timeline and QA, and writes a contact sheet PNG per stream to
outputs/viz/<dataset>/<stream_id>.png.
"""
from __future__ import annotations

import argparse
import textwrap
from pathlib import Path

from streamrag.config import OUTPUT_DIR
from streamrag.data import get_dataset
from streamrag.types import Stream
from streamrag.video.frames import contact_sheet


def fmt_t(t: float | None) -> str:
    if t is None:
        return "   ?   "
    m, s = divmod(int(t), 60)
    return f"{m:03d}:{s:02d}"


def show_stream(s: Stream, max_obs: int = 15, max_qa: int = 5, max_frames: int = 12,
                out_dir: Path | None = None) -> Path | None:
    n_vis = sum(o.modality != "text" for o in s.observations)
    print(f"\n=== {s.stream_id}  ({s.dataset})  obs={len(s.observations)} "
          f"(visual={n_vis})  qa={len(s.qa)}  meta={ {k: v for k, v in s.meta.items() if v is not None} }")
    for o in s.observations[:max_obs]:
        desc = o.text if o.modality == "text" else Path(o.path).name
        print(f"  [{fmt_t(o.t)}] {o.source:7s} {o.modality:5s} {textwrap.shorten(str(desc), 90)}")
    if len(s.observations) > max_obs:
        print(f"  ... {len(s.observations) - max_obs} more")
    for q in s.qa[:max_qa]:
        opts = f"\n        options: {q.options}" if q.options is not None else ""
        print(f"  Q@{fmt_t(q.t_query)} [{q.qtype}] {textwrap.shorten(q.question, 160)}{opts}"
              f"\n        A: {q.answer}")
    if len(s.qa) > max_qa:
        print(f"  ... {len(s.qa) - max_qa} more questions")

    vis = [o for o in s.observations if o.modality != "text"]
    if not vis or max_frames <= 0:
        return None
    if len(vis) > max_frames:                     # evenly spaced subset
        vis = [vis[int(i * len(vis) / max_frames)] for i in range(max_frames)]
    imgs = [o.load_image() for o in vis]
    sheet = contact_sheet(imgs, [f"{fmt_t(o.t)} {o.source}" for o in vis])
    out_dir = out_dir or OUTPUT_DIR / "viz" / s.dataset
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / f"{s.stream_id.replace('/', '_')}.png"
    sheet.save(path)
    print(f"  contact sheet -> {path}")
    return path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset")
    ap.add_argument("--n", type=int, default=2, help="number of streams to show")
    ap.add_argument("--stream", help="show one stream id")
    ap.add_argument("--max-frames", type=int, default=12)
    ap.add_argument("--no-images", action="store_true")
    a = ap.parse_args()

    ds = get_dataset(a.dataset)
    streams = ds.to_streams(limit=None if a.stream else a.n)
    if a.stream:
        streams = [s for s in streams if s.stream_id == a.stream]
    if not streams:
        print("No streams available (videos not downloaded yet?)")
    for s in streams:
        show_stream(s, max_frames=0 if a.no_images else a.max_frames)


if __name__ == "__main__":
    main()
