"""Download datasets into data/raw/<name>/.

  python scripts/download_data.py disastervqa mindcube
  python scripts/download_data.py videomme --split dev        # metadata + the 20 dev videos (~5 GB)
  python scripts/download_data.py videomme                    # all 100 selected long videos (only those bytes are transferred)
  python scripts/download_data.py m3bench --n-videos 3        # annotations, subtitles, 3 videos (~4 GB)
  python scripts/download_data.py m3bench --n-videos 2 --split dev
  python scripts/download_data.py m3bench --n-videos all      # all 100 videos (125.7 GB)
  python scripts/download_data.py all
"""
from __future__ import annotations

import argparse

from streamrag.data import DATASETS, get_dataset


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("datasets", nargs="+", choices=[*DATASETS, "all"])
    ap.add_argument("--n-videos", default=None, help="m3bench/videomme: number of videos or 'all' (m3bench default 3)")
    ap.add_argument("--split", choices=["dev", "test"], help="m3bench/videomme: only videos from this split")
    a = ap.parse_args()
    names = list(DATASETS) if "all" in a.datasets else a.datasets
    for name in names:
        ds = get_dataset(name)
        n = None if a.n_videos in (None, "all") else int(a.n_videos)
        if name == "videomme":
            ds.download(n_videos=n, split=a.split)
        elif name == "m3bench":
            ds.download(n_videos=None if a.n_videos == "all" else (n or 3), split=a.split)
        else:
            ds.download()


if __name__ == "__main__":
    main()
