"""Video-MME (lmms-eval/Video-MME). We use `n_videos` long videos (30–60 min).

Videos ship in 20 zip chunks (~5 GB each, ~101 GB total). download() fetches one chunk
at a time, extracts only the selected videos and deletes the zip.
"""
from __future__ import annotations

import json
import random
import shutil
import zipfile
from pathlib import Path

import pandas as pd
from huggingface_hub import hf_hub_download

from streamrag.data._io import parse_srt, safe_extract
from streamrag.data.base import StreamDataset
from streamrag.types import Observation, QAItem, Stream
from streamrag.video.frames import sample_times, video_duration

PARQUET = "videomme/test-00000-of-00001.parquet"
N_CHUNKS = 20


class VideoMME(StreamDataset):
    name = "videomme"

    @property
    def video_dir(self) -> Path:
        return self.raw / "videos"

    def _hf(self, filename: str, local_dir: Path | None = None) -> Path:
        return Path(hf_hub_download(self.cfg["hf_repo"], filename, repo_type="dataset",
                                    local_dir=local_dir or self.raw))

    def download(self, max_chunks: int | None = None, **kw) -> None:
        self._hf(PARQUET)
        sub = self._hf("subtitle.zip")
        if not (self.raw / "subtitle").exists():
            with zipfile.ZipFile(sub) as zf:
                safe_extract(zf, self.raw)
        wanted = set(self.selected())
        self.video_dir.mkdir(parents=True, exist_ok=True)
        fetched = 0
        for i in range(1, N_CHUNKS + 1):
            missing = {v for v in wanted if not (self.video_dir / f"{v}.mp4").exists()}
            if not missing:
                break
            if max_chunks is not None and fetched >= max_chunks:
                print(f"[videomme] stopped after {fetched} chunk(s); {len(missing)} selected videos missing")
                break
            tmp = self.raw / "_chunks"
            z = self._hf(f"videos_chunked_{i:02d}.zip", local_dir=tmp)
            fetched += 1
            with zipfile.ZipFile(z) as zf:
                members = [m for m in zf.namelist() if Path(m).stem in missing and m.endswith(".mp4")]
                safe_extract(zf, tmp / "x", members)
                for m in members:
                    shutil.move(str(tmp / "x" / m), self.video_dir / Path(m).name)
            shutil.rmtree(tmp)
            print(f"[videomme] chunk {i:02d}: extracted {len(members)} selected videos")
        n = sum((self.video_dir / f"{v}.mp4").exists() for v in wanted)
        print(f"[videomme] {n}/{len(wanted)} selected videos present in {self.video_dir}")

    def load(self) -> list[dict]:
        df = pd.read_parquet(self.require(self.raw / PARQUET))
        df["options"] = df["options"].map(list)
        return df.to_dict("records")

    def selected(self) -> list[str]:
        """Fixed, seeded choice of `n_videos` videos of the configured duration (videoIDs)."""
        path = self.processed / f"selected_{self.cfg['duration']}_{self.cfg['n_videos']}.json"
        if path.exists():
            return json.loads(path.read_text())
        df = pd.read_parquet(self.require(self.raw / PARQUET))
        ids = sorted(df.loc[df.duration == self.cfg["duration"], "videoID"].unique())
        sel = sorted(random.Random(self.cfg["seed"]).sample(ids, min(self.cfg["n_videos"], len(ids))))
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(sel, indent=1))
        return sel

    def to_streams(self, limit: int | None = None, only_available: bool = True) -> list[Stream]:
        recs = self.load()
        sel = self.selected()
        by_vid: dict[str, list[dict]] = {}
        for r in recs:
            if r["videoID"] in sel:
                by_vid.setdefault(r["videoID"], []).append(r)
        streams = []
        for vid in sel:
            vpath = self.video_dir / f"{vid}.mp4"
            if only_available and not vpath.exists():
                continue
            sid = f"vmme-{vid}"
            obs: list[Observation] = []
            dur = None
            if vpath.exists():
                dur = video_duration(str(vpath))
                for t in sample_times(dur, every_s=self.cfg["frame_every_s"]):
                    obs.append(Observation(f"{sid}/f{t:07.1f}", sid, t, "camera", "frame",
                                           path=str(vpath), meta={"video_t": t}))
            srt = self.raw / "subtitle" / f"{vid}.srt"
            if srt.exists():
                for k, (s, e, text) in enumerate(parse_srt(srt)):
                    obs.append(Observation(f"{sid}/asr{k:04d}", sid, s, "asr", "text",
                                           text=text, meta={"t_end": e}))
            obs.sort(key=lambda o: o.t)
            rs = by_vid.get(vid, [])
            qa = [QAItem(f"{sid}/{r['question_id']}", sid, r["question"], r["answer"],
                         options=r["options"], t_query=dur, qtype=r["task_type"],
                         meta={"domain": r["domain"], "sub_category": r["sub_category"]})
                  for r in rs]
            meta = {k: rs[0][k] for k in ("video_id", "duration", "domain", "sub_category", "url")} if rs else {}
            streams.append(Stream(sid, self.name, obs, qa, meta={**meta, "video_s": dur}))
            if limit and len(streams) >= limit:
                break
        return streams
