"""Download datasets into data/raw/<name>/.

  python scripts/download_data.py disastervqa mindcube
  python scripts/download_data.py videomme --max-chunks 1     # metadata + first 5 GB chunk
  python scripts/download_data.py videomme                    # all chunks until the 100 selected long videos are found
  python scripts/download_data.py m3bench --n-videos 3        # annotations, subtitles, 3 videos (~4 GB)
  python scripts/download_data.py m3bench --n-videos all      # all 100 videos (125.7 GB)
  python scripts/download_data.py all
"""
from __future__ import annotations

import argparse

from streamrag.data import DATASETS, get_dataset


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("datasets", nargs="+", choices=[*DATASETS, "all"])
    ap.add_argument("--max-chunks", type=int, default=None, help="videomme: max zip chunks to fetch")
    ap.add_argument("--n-videos", default="3", help="m3bench: number of videos or 'all'")
    a = ap.parse_args()
    names = list(DATASETS) if "all" in a.datasets else a.datasets
    for name in names:
        ds = get_dataset(name)
        if name == "videomme":
            ds.download(max_chunks=a.max_chunks)
        elif name == "m3bench":
            ds.download(n_videos=None if a.n_videos == "all" else int(a.n_videos))
        else:
            ds.download()


if __name__ == "__main__":
    main()
