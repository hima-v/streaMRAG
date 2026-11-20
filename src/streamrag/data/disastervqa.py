"""DisasterVQA (Zenodo 20306919, CC BY-SA 4.0): 1,395 disaster images, 4,405 QA.

Images have no time axis, so we build pseudo-streams: images of one disaster type are
chunked into streams of `stream_len` and delivered `stream_dt_s` apart, optionally in
`n_orderings` random permutations (pipeline_planning.md §1). They serve as the
"social-media image" source.
"""
from __future__ import annotations

import json
import random
import zipfile
from collections import defaultdict
from pathlib import Path

from streamrag.data._io import http_download, safe_extract
from streamrag.data.base import StreamDataset
from streamrag.types import Observation, QAItem, Stream


class DisasterVQA(StreamDataset):
    name = "disastervqa"

    def download(self, **kw) -> None:
        if self._annotations_path(must_exist=False):
            print(f"[disastervqa] already extracted in {self.raw}")
            return
        z = http_download(self.cfg["zenodo_url"], self.raw / "DisasterVQA-Dataset-v3.zip",
                          md5=self.cfg["md5"])
        with zipfile.ZipFile(z) as zf:
            safe_extract(zf, self.raw)
        z.unlink()
        print(f"[disastervqa] extracted to {self.raw}")

    def _annotations_path(self, must_exist: bool = True) -> Path | None:
        hits = sorted(self.raw.rglob("disastervqa_annotations.jsonl")) if self.raw.exists() else []
        if not hits and must_exist:
            self.require(self.raw / "disastervqa_annotations.jsonl")
        return hits[0] if hits else None

    def load(self) -> list[dict]:
        with open(self._annotations_path()) as f:
            return [json.loads(line) for line in f if line.strip()]

    def _image_path(self, rel: str) -> str:
        root = self._annotations_path().parent
        p = root / rel
        if not p.exists():       # tolerate a different top-level folder inside the zip
            hits = list(self.raw.rglob(Path(rel).name))
            p = hits[0] if hits else p
        return str(p)

    def to_streams(self, limit: int | None = None) -> list[Stream]:
        recs = self.load()
        by_image: dict[str, list[dict]] = defaultdict(list)
        for r in recs:
            by_image[r["image_id"]].append(r)
        by_type: dict[str, list[str]] = defaultdict(list)
        for img_id, rs in by_image.items():
            by_type[rs[0].get("disaster_type") or "unknown"].append(img_id)

        L, dt, n_ord = self.cfg["stream_len"], self.cfg["stream_dt_s"], self.cfg["n_orderings"]
        streams: list[Stream] = []
        for dtype in sorted(by_type):
            ids = sorted(by_type[dtype], key=lambda s: int(s.split("-")[-1]) if s.split("-")[-1].isdigit() else s)
            for c in range(0, len(ids), L):
                chunk = ids[c:c + L]
                for j in range(n_ord):
                    order = chunk[:]
                    if j > 0:
                        random.Random(hash((self.cfg["seed"], dtype, c, j)) & 0xFFFFFFFF).shuffle(order)
                    sid = f"dvqa-{dtype}-{c // L:03d}-o{j}"
                    obs, qa = [], []
                    for k, img_id in enumerate(order):
                        r0 = by_image[img_id][0]
                        oid = f"{sid}/{img_id}"
                        obs.append(Observation(
                            obs_id=oid, stream_id=sid, t=float(k * dt), source="social",
                            modality="image", path=self._image_path(r0["image_path"]),
                            meta={"image_id": img_id, "dataset_source": r0.get("dataset_source"),
                                  "disaster_type": dtype}))
                        for r in by_image[img_id]:
                            qa.append(QAItem(
                                qa_id=f"{sid}/{r['question_id']}", stream_id=sid,
                                question=r["question"], answer=r["groundtruth_answer"],
                                options=r.get("choices"), t_query=float(len(order) * dt),
                                qtype=r.get("question_type"), evidence_ids=[oid],
                                meta={k: r.get(k) for k in
                                      ("crisis_info_type", "crisis_info_code", "region")}))
                    streams.append(Stream(sid, self.name, obs, qa,
                                          meta={"disaster_type": dtype, "ordering": j}))
                    if limit and len(streams) >= limit:
                        return streams
        return streams
