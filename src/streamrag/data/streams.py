"""Rule-based evidence streams (codebase_plan.md §10), built only from dataset fields.

Currently implemented: DisasterVQA. A stream = 20 consecutive photos of one disaster type (dev
or test images with a recoverable posting time), split into block A (steps 1-10) and block B
(steps 11-20). 5 questions are drawn from each block's photos, so exactly 5 questions are
answerable after step 10 and all 10 after step 20.

What the memory agent receives per item: the photo, its posting time and platform. The
dataset's verified observations are stored as judge-only `reference_facts`.
"""
from __future__ import annotations

import collections
import datetime as dt
import hashlib
import json
import random
import re
from pathlib import Path

from streamrag.config import PROCESSED_DIR, load_yaml

ABSTAIN = "NOT_ENOUGH_EVIDENCE"
_FORMAT = {"Binary": "yesno", "Multiple-Choice": "mc", "Open-Ended": "open"}


def stream_dir(dataset: str, split: str, version: str | None = None) -> Path:
    return PROCESSED_DIR / "streams" / (version or load_yaml("streams")["version"]) / dataset / split


def load_stream(path: str | Path) -> dict:
    return json.loads(Path(path).read_text())


def list_streams(dataset: str, split: str) -> list[Path]:
    return sorted(stream_dir(dataset, split).glob("*.json"))


# ----------------------------------------------------------------------------- DisasterVQA
def post_time(image_path: str) -> dt.datetime | None:
    """Posting time from a MEDIC file name (..._YYYY-MM-DD_HH-MM...) or a tweet snowflake id."""
    name = image_path.split("/")[-1]
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})", name)
    if m:
        return dt.datetime(*map(int, m.groups()))
    m = re.match(r"(\d{17,19})_", name)
    if m:
        ms = (int(m.group(1)) >> 22) + 1288834974657
        return dt.datetime.fromtimestamp(ms / 1000, dt.UTC).replace(tzinfo=None, second=0, microsecond=0)
    return None


def _stem(question: str) -> str:
    return question.split("?")[0].strip() + "?"


def _answer_text(r: dict) -> str:
    a = r["groundtruth_answer"]
    if r.get("choices"):
        return ", ".join(r["choices"][x] for x in (a if isinstance(a, list) else [a]))
    return a[0] if isinstance(a, list) else str(a)


def _question_record(r: dict, item_id: str, time_str: str, step: int, n_steps: int) -> dict:
    gold = r["groundtruth_answer"]
    if r.get("choices"):
        letters = gold if isinstance(gold, list) else [gold]
        fmt = "mc_multi" if len(letters) > 1 else "mc"
        gold_out = letters if fmt == "mc_multi" else letters[0]
        accepted = [r["choices"][x] for x in letters]
    else:
        fmt = _FORMAT[r["question_type"]] if r["question_type"] != "Multiple-Choice" else "open"
        accepted = gold if isinstance(gold, list) else [gold]
        gold_out = accepted[0]
    return {
        "qa_id": r["question_id"],
        "question": f"About the photo posted {time_str} (item {item_id}): {r['question']}",
        "original": r["question"], "gold": gold_out, "accepted_answers": accepted,
        "options": r.get("choices"), "format": fmt, "qtype": r["question_type"],
        "evidence_scope": [item_id],
        "answerability": ["answerable" if t >= step else "not_yet" for t in range(1, n_steps + 1)],
    }


def build_disastervqa(split: str = "all", length: int = 20) -> list[dict]:
    """Non-overlapping streams of `length` timestamped photos of one disaster type, in posting order.

    The stream is made of length/block_size blocks (block_size = 10); each block contributes
    questions_per_block (= 5) questions about photos inside it. So a short stream (10 photos) has
    5 questions and a long stream (20 photos) has 10, spread over both halves. split='all' uses every
    photo of the dataset (files go to the pool folder 'len<length>'); 'dev'/'test' use the old splits.
    """
    from streamrag.data import get_dataset
    from streamrag.eval.splits import split_units

    cfg_all = load_yaml("streams")
    cfg = cfg_all["disastervqa"]
    ds = get_dataset("disastervqa")
    root = ds._annotations_path().parent
    by_img = collections.defaultdict(list)
    for r in ds.load():
        by_img[r["image_id"]].append(r)
    if split == "all":                                   # every photo of the dataset (no dev/test split)
        split_imgs, pool = set(by_img), f"len{length}"
    else:
        units = split_units("disastervqa", split)
        split_imgs = {o.meta["image_id"] for s in ds.to_streams()
                      if s.meta["split_key"] in units and s.meta["ordering"] == 0 for o in s.observations}
        pool = split
    B, n_q = cfg["block_size"], cfg["questions_per_block"]
    assert length % B == 0, f"length must be a multiple of {B}"
    streams = []
    for dtype in cfg["disaster_types"]:
        timed = sorted(((post_time(by_img[i][0]["image_path"]), i) for i in split_imgs
                        if by_img[i][0]["disaster_type"] == dtype and post_time(by_img[i][0]["image_path"])),
                       key=lambda x: (x[0], x[1]))
        start = 0
        while start + length <= len(timed):
            window = timed[start:start + length]
            sid = (f"dvqa-{dtype}-len{length}-{len(streams):03d}" if split == "all"
                   else f"dvqa-{dtype}-{split}-{len(streams):03d}")
            s = _make_stream(window, by_img, root, dtype, pool, sid, B, n_q, cfg, cfg_all["seed"])
            if s is None:
                start += 1            # rule: slide by one photo until a valid window is found
                continue
            streams.append(s)
            start += length           # non-overlapping streams
    return streams


def _make_stream(window, by_img, root, dtype, pool, sid, B, n_q, cfg, seed) -> dict | None:
    N = len(window)
    t0 = window[0][0]
    items, refs, item_of = [], {}, {}
    for step, (t, img) in enumerate(window, 1):
        r0 = by_img[img][0]
        eid = f"E{step:02d}"
        item_of[img] = (eid, step, t.strftime("%Y-%m-%d %H:%M UTC"))
        platform = "Twitter" if re.match(r"\d{17,19}_", r0["image_path"].split("/")[-1]) else "web"
        items.append({"item_id": eid, "step": step, "t": (t - t0).total_seconds(),
                      "time_str": t.strftime("%Y-%m-%d %H:%M UTC"),
                      "source": f"social media photo ({platform})", "text": "",
                      "frames": [{"path": str(root / r0["image_path"]), "t": (t - t0).total_seconds()}],
                      "provenance": {"dataset": "DisasterVQA", "image_id": img,
                                     "image_path": r0["image_path"],
                                     "dataset_source": r0["dataset_source"]}})
        refs[eid] = [f"{_stem(r['question'])} {_answer_text(r)}" for r in by_img[img]]

    # non-distinctive (question, answer) pairs: occur on too many photos of this window
    pair_count = collections.Counter((_stem(r["question"]).lower(), _answer_text(r).lower())
                                     for _, img in window for r in by_img[img])
    cand = lambda img: [r for r in by_img[img]
                        if pair_count[(_stem(r["question"]).lower(), _answer_text(r).lower())]
                        < cfg["nondistinctive_min_photos"]]
    rng = random.Random(f"{seed}-{sid}")
    questions = []
    for bi in range(N // B):
        block = window[bi * B:(bi + 1) * B]
        imgs = [img for _, img in block if cand(img)]
        rng.shuffle(imgs)
        picked, used = [], set()
        fmt_cycle = cfg["format_order"]
        k = 0
        while len(picked) < n_q and k < 4 * len(imgs) * len(fmt_cycle):
            want = fmt_cycle[k % len(fmt_cycle)]
            for img in imgs:
                if img in used:
                    continue
                rs = [r for r in cand(img) if _FORMAT[r["question_type"]] == want]
                if rs:
                    picked.append(rng.choice(sorted(rs, key=lambda r: r["question_id"])))
                    used.add(img)
                    break
            k += 1
        for img in imgs:                          # fill with any format if still short
            if len(picked) >= n_q:
                break
            if img not in used:
                picked.append(rng.choice(sorted(cand(img), key=lambda r: r["question_id"])))
                used.add(img)
        if len(picked) < n_q:
            return None
        for r in sorted(picked, key=lambda r: item_of[r["image_id"]][1]):
            eid, step, tstr = item_of[r["image_id"]]
            q = _question_record(r, eid, tstr, step, N)
            q["block"] = "AB"[bi] if N // B <= 2 else str(bi + 1)
            questions.append(q)

    stream = {"stream_id": sid, "dataset": "disastervqa", "split": pool, "disaster_type": dtype,
              "n_steps": N, "boundary_step": B if N // B > 1 else None, "block_size": B,
              "items": items, "reference_facts": refs, "questions": questions}
    body = json.dumps(stream, sort_keys=True).encode()
    stream["manifest"] = {
        "builder": "streamrag.data.streams.build_disastervqa", "version": load_yaml("streams")["version"],
        "config_sha256": hashlib.sha256(json.dumps(load_yaml("streams"), sort_keys=True).encode()).hexdigest()[:16],
        "dataset": {"name": "DisasterVQA", "zenodo_md5": "4a3576c78a5d71a556ecc081bcc2cd28"},
        "content_sha256": hashlib.sha256(body).hexdigest()[:16],
    }
    check_stream(stream)
    return stream


def check_stream(s: dict) -> None:
    """Invariants of §10.8 (raises AssertionError)."""
    N = s["n_steps"]
    B = s.get("block_size") or s.get("boundary_step") or N
    assert len(s["items"]) == N and [it["step"] for it in s["items"]] == list(range(1, N + 1))
    ts = [it["t"] for it in s["items"]]
    assert ts == sorted(ts), "items not chronological"
    ids = {it["item_id"] for it in s["items"]}
    per_block = collections.Counter(q["block"] for q in s["questions"])
    assert len(set(per_block.values())) == 1, f"unequal questions per block: {per_block}"
    for q in s["questions"]:
        assert set(q["evidence_scope"]) <= ids and len(q["answerability"]) == N
        bi = "AB".index(q["block"]) if q["block"] in "AB" else int(q["block"]) - 1
        assert all(a == "not_yet" for a in q["answerability"][:bi * B]), q["qa_id"]
        assert q["answerability"][(bi + 1) * B - 1] == "answerable", q["qa_id"]
        assert q["answerability"][-1] == "answerable", q["qa_id"]
    facts = " ".join(f for fs in s["reference_facts"].values() for f in fs)
    assert all(it["text"] == "" or it["text"] not in facts for it in s["items"])


def write_streams(streams: list[dict]) -> list[Path]:
    out = []
    for s in streams:
        d = stream_dir(s["dataset"], s["split"])
        d.mkdir(parents=True, exist_ok=True)
        p = d / f"{s['stream_id']}.json"
        p.write_text(json.dumps(s, indent=1, ensure_ascii=False))
        out.append(p)
    return out


def segment_stream(stream: dict, length: int | None) -> list[dict]:
    """Split a base stream into consecutive, independent evidence streams of `length` items
    (None/0 = whole stream). Each evidence stream is relabelled from the start: items E01..EN at
    steps 1..N, with the questions (text, evidence scope, answerability) and reference facts
    remapped to the new ids. The base item id/step are kept in `base_item_id` / `base_step`.
    Segments without questions are dropped.
    """
    n = len(stream["items"])
    length = length or n
    n_seg = -(-n // length)
    out = []
    for k, start in enumerate(range(0, n, length), 1):
        chunk = stream["items"][start:start + length]
        rename = {it["item_id"]: f"E{i:02d}" for i, it in enumerate(chunk, 1)}
        qs = [q for q in stream["questions"] if set(q["evidence_scope"]) <= set(rename)]
        if not qs:
            continue
        t0 = chunk[0]["t"]
        items = [{**it, "item_id": rename[it["item_id"]], "step": i, "t": it["t"] - t0,
                  "base_item_id": it["item_id"], "base_step": it["step"],
                  "provenance": {**it["provenance"], "base_item_id": it["item_id"]}}
                 for i, it in enumerate(chunk, 1)]
        questions = []
        for q in qs:
            text = q["question"]
            for old in q["evidence_scope"]:
                text = text.replace(f"(item {old})", f"(item {rename[old]})")
            questions.append({**q, "question": text, "evidence_scope": [rename[e] for e in q["evidence_scope"]],
                              "answerability": q["answerability"][start:start + len(chunk)],
                              "base_evidence_scope": q["evidence_scope"]})
        sid = stream["stream_id"] if n_seg == 1 else f"{stream['stream_id']}-s{k}of{n_seg}"
        out.append({**stream, "stream_id": sid, "parent_stream": stream["stream_id"], "items": items,
                    "questions": questions, "n_steps": len(items), "base_steps": [chunk[0]["step"], chunk[-1]["step"]],
                    "boundary_step": None,
                    "reference_facts": {rename[i]: stream["reference_facts"][i] for i in rename}})
    return out


def select_streams(streams: list[dict], n, method: str = "stratified", seed: int = 0,
                   ids: list[str] | None = None) -> list[dict]:
    """Choose the evaluation streams of an experiment (deterministic).

    stratified: round-robin over disaster types (most streams first), seeded order within a type
    random:     seeded sample;   list: exactly `ids`;   n = 'all' or None: every stream
    """
    if method == "list":
        by_id = {s["stream_id"]: s for s in streams}
        missing = [i for i in ids or [] if i not in by_id]
        assert not missing, f"unknown stream ids: {missing}"
        return [by_id[i] for i in ids]
    if n in (None, "all") or int(n) >= len(streams):
        return list(streams)
    n = int(n)
    rng = random.Random(seed)
    if method == "random":
        return sorted(rng.sample(streams, n), key=lambda s: s["stream_id"])
    groups = collections.defaultdict(list)
    for s in sorted(streams, key=lambda s: s["stream_id"]):
        groups[s["disaster_type"]].append(s)
    for g in groups.values():
        rng.shuffle(g)
    order = sorted(groups, key=lambda t: (-len(groups[t]), t))
    out = []
    while len(out) < n:
        for t in order:
            if groups[t] and len(out) < n:
                out.append(groups[t].pop(0))
    return out
