"""Build rule-based evidence streams (codebase_plan.md §10) and print a summary.

  python scripts/build_streams.py disastervqa --length 10     # short streams (10 photos, 5 questions)
  python scripts/build_streams.py disastervqa --length 20     # long streams (20 photos, 10 questions)

By default every timestamped photo of every disaster type is used (--split all) and streams never
share photos. Files go to data/processed/streams/v2/disastervqa/len<length>/.
"""
from __future__ import annotations

import argparse
import collections

from streamrag.data.streams import build_disastervqa, write_streams

BUILDERS = {"disastervqa": build_disastervqa}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("dataset", choices=list(BUILDERS))
    ap.add_argument("--length", type=int, default=10, choices=[10, 20], help="photos per stream")
    ap.add_argument("--split", default="all", choices=["all", "dev", "test"])
    a = ap.parse_args()
    streams = BUILDERS[a.dataset](a.split, a.length)
    paths = write_streams(streams)
    by_type = collections.Counter(s["disaster_type"] for s in streams)
    for s, p in zip(streams, paths):
        fmts = collections.Counter(q["format"] for q in s["questions"])
        print(f"{s['stream_id']}: {s['items'][0]['time_str']} -> {s['items'][-1]['time_str']} | "
              f"{len(s['questions'])} questions {dict(fmts)} | sha {s['manifest']['content_sha256']}")
    print(f"\n{len(streams)} streams of {a.length} photos, {sum(len(s['questions']) for s in streams)} questions; "
          f"by disaster type: {dict(by_type)}\n-> {paths[0].parent if paths else '(none)'}")
