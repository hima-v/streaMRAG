"""MindCube-Tiny (MLL-Lab/MindCube, MIT): 1,050 MC spatial questions
(600 among / 250 around / 200 rotation). Each question has a set of photos of one scene.
A stream = one photo set delivered one photo at a time; all questions over that set are
asked at the end. (The "not enough evidence" variant from the proposal — deleting photos
for 20% of test questions — is built at evaluation time, not here.)
"""
from __future__ import annotations

import json
import zipfile
from collections import OrderedDict

from huggingface_hub import hf_hub_download

from streamrag.data._io import safe_extract
from streamrag.data.base import StreamDataset
from streamrag.types import Observation, QAItem, Stream


class MindCubeTiny(StreamDataset):
    name = "mindcube"

    @property
    def data_root(self):
        return self.raw / "data"

    def download(self, **kw) -> None:
        if (self.data_root / "raw" / self.cfg["split_file"]).exists():
            print(f"[mindcube] already extracted in {self.data_root}")
            return
        z = hf_hub_download(self.cfg["hf_repo"], "data.zip", repo_type="dataset",
                            local_dir=self.raw)
        with zipfile.ZipFile(z) as zf:
            safe_extract(zf, self.raw)
        print(f"[mindcube] extracted to {self.data_root}")

    def load(self) -> list[dict]:
        path = self.require(self.data_root / "raw" / self.cfg["split_file"])
        return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

    def to_streams(self, limit: int | None = None) -> list[Stream]:
        groups: OrderedDict[tuple, list[dict]] = OrderedDict()
        for r in self.load():
            groups.setdefault(tuple(r["images"]), []).append(r)
        dt = self.cfg["frame_dt_s"]
        streams = []
        for k, (imgs, rs) in enumerate(groups.items()):
            setting = rs[0]["id"].split("_")[0]
            sid = f"mc-{setting}-{k:04d}"
            obs = [Observation(f"{sid}/img{i}", sid, float(i * dt), "camera", "image",
                               path=str(self.data_root / p), meta={"view": p.split("/")[-1]})
                   for i, p in enumerate(imgs)]
            qa = [QAItem(f"{sid}/{r['id']}", sid, r["question"], r["gt_answer"],
                         t_query=float(len(imgs) * dt), qtype=setting,
                         meta={"format": "mc", "category": r.get("category"), "type": r.get("type")})
                  for r in rs]
            scene = "/".join(imgs[0].split("/")[:-1])   # photo folder = scene
            streams.append(Stream(sid, self.name, obs, qa,
                                  meta={"setting": setting, "split_key": scene}))
            if limit and len(streams) >= limit:
                break
        return streams
