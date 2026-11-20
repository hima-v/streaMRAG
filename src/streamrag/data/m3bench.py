"""M3-Bench-Robot (ByteDance-Seed/M3-Bench, CC BY-NC-SA 4.0): 100 robot-perspective videos
(~1.25 GB each, 125.7 GB total) with open-ended QA. Each question carries the timestamp
at which it is asked, so `t_query` is meaningful here.
QA annotations live in the M3-Agent GitHub repo (data/annotations/robot.json).
"""
from __future__ import annotations

import json
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download

from streamrag.data._io import hms_to_s, http_download, parse_srt
from streamrag.data.base import StreamDataset
from streamrag.types import Observation, QAItem, Stream
from streamrag.video.frames import sample_times, video_duration


class M3BenchRobot(StreamDataset):
    name = "m3bench"

    def _hf(self, filename: str) -> Path:
        return Path(hf_hub_download(self.cfg["hf_repo"], filename, repo_type="dataset",
                                    local_dir=self.raw))

    def download(self, n_videos: int | None = 3, **kw) -> None:
        """Annotations + all subtitles + the first `n_videos` videos (None = all 100)."""
        http_download(self.cfg["annotations_url"], self.raw / "robot.json")
        files = HfApi().list_repo_files(self.cfg["hf_repo"], repo_type="dataset")
        for f in sorted(f for f in files if f.startswith("subtitles/robot/")):
            self._hf(f)
        vids = sorted(f for f in files if f.startswith("videos/robot/") and f.endswith(".mp4"))
        for f in vids[:n_videos] if n_videos is not None else vids:
            print(f"[m3bench] {f}")
            self._hf(f)
        n = len(list((self.raw / "videos" / "robot").glob("*.mp4")))
        print(f"[m3bench] {n}/{len(vids)} videos present")

    def load(self) -> list[dict]:
        data = json.loads(self.require(self.raw / "robot.json").read_text())
        return [{"video": k, **v} for k, v in sorted(data.items())]

    def to_streams(self, limit: int | None = None, only_available: bool = True) -> list[Stream]:
        streams = []
        for rec in self.load():
            vid = rec["video"]
            vpath = self.raw / "videos" / "robot" / f"{vid}.mp4"
            if only_available and not vpath.exists():
                continue
            sid = f"m3r-{vid}"
            obs: list[Observation] = []
            dur = None
            if vpath.exists():
                dur = video_duration(str(vpath))
                for t in sample_times(dur, every_s=self.cfg["frame_every_s"]):
                    obs.append(Observation(f"{sid}/f{t:07.1f}", sid, t, "camera", "frame",
                                           path=str(vpath), meta={"video_t": t}))
            srt = self.raw / "subtitles" / "robot" / f"{vid}.srt"
            if srt.exists():
                for k, (s, e, text) in enumerate(parse_srt(srt)):
                    obs.append(Observation(f"{sid}/asr{k:04d}", sid, s, "asr", "text",
                                           text=text, meta={"t_end": e}))
            obs.sort(key=lambda o: o.t)
            qa = [QAItem(f"{sid}/{q['question_id']}", sid, q["question"], q["answer"],
                         t_query=hms_to_s(q["timestamp"]) if q.get("timestamp") else dur,
                         qtype=q.get("type"),
                         meta={"before_clip": q.get("before_clip"), "reasoning_zh": q.get("reasoning")})
                  for q in rec["qa_list"]]
            streams.append(Stream(sid, self.name, obs, qa, meta={"video_s": dur}))
            if limit and len(streams) >= limit:
                break
        return streams
