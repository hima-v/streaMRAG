"""Build the hand-curated sample evidence streams (one per dataset) in examples/.

  python scripts/make_sample_streams.py all
  python scripts/make_sample_streams.py m3bench videomme

Each sample: 20 evidence items (text + image) and 10 dataset questions, each linked to the
evidence item(s) that support its answer. Items are delivered in their real order, and the
selections below were chosen so that exactly 5 questions are supported by items 1-10 and
the other 5 only by items 11-20 (checked by streamrag.data.samples). All samples use dev-split
material only, and no captioning: item text comes from the datasets (subtitles, dialogue,
verified QA facts, view annotations).
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import json
import re

from streamrag.config import RAW_DIR, ROOT
from streamrag.data._io import hms_to_s, parse_srt
from streamrag.data.samples import write_sample
from streamrag.memory.tokens import fmt_t
from streamrag.video.frames import frames_at

EXAMPLES = ROOT / "examples"


def window_text(subs, lo: float, hi: float, speakers: bool) -> str:
    out = []
    for s, e, t in subs:
        if lo <= s < hi:
            if speakers and ":" in t:
                spk, txt = t.split(":", 1)
                out.append(f"{spk.strip()}: {txt.strip()}")
            else:
                out.append(t.strip())
    return "\n".join(out)


# ----------------------------------------------------------------------------- M3-Bench-Robot
M3_VIDEO = "bedroom_04"
M3_EVIDENCE = [  # (id, start, end, key frame, note)
    ("E01", "00:00", "00:25", "00:10", "supports Q10 (black coffee)"),
    ("E02", "02:28", "03:10", "02:40", "related to Q07: Mia finds black coats classy (not nail polish)"),
    ("E03", "04:00", "04:50", "04:20", "supports Q11 (magazines, wanting to be beautiful)"),
    ("E04", "06:55", "07:30", "07:24", "supports Q07 (black nail polish, 'the color that I like')"),
    ("E05", "08:45", "09:20", "09:08", "distractor: Emma does NOT like black"),
    ("E06", "11:10", "11:36", "11:18", "supports Q01, part 1 ('not too much')"),
    ("E07", "12:08", "12:31", "12:18", "supports Q01, part 2 ('control the intensity')"),
    ("E08", "14:10", "14:50", "14:30", "distractor: nail-painting practice"),
    ("E09", "15:40", "16:25", "16:00", "distractor: red nails with a blue shirt"),
    ("E10", "16:55", "17:46", "17:20", "supports Q02 (liked Little Lee before)"),
    ("E11", "17:46", "18:28", "18:03", "supports Q03 (busy, too many advertisements)"),
    ("E12", "18:28", "19:00", "18:45", "distractor: boyfriend, lead-in to clothing talk"),
    ("E13", "19:00", "19:40", "19:16", "supports Q06 (Japanese style in college, Korean now)"),
    ("E14", "19:40", "20:15", "19:55", "supports Q05 (Emma obsessed with vintage)"),
    ("E15", "20:15", "21:00", "20:30", "related to Q05 (more vintage talk); Mia sometimes wears only black"),
    ("E16", "21:00", "21:50", "21:25", "distractor: styling advice, shopping plans"),
    ("E17", "22:38", "23:06", "22:46", "supports Q08 (Emma wants chocolate, Mia chips)"),
    ("E18", "24:28", "25:36", "25:00", "distractor: tasting each other's snacks ('a little bit salty')"),
    ("E19", "25:36", "26:25", "25:50", "supports Q04 (always says she'll sleep early, never does)"),
    ("E20", "26:28", "27:17", "26:50", "distractor: closing chat, going to bed"),
]
M3_QUESTIONS = {  # question id -> (supporting, related)
    "bedroom_04_Q10": (["E01"], []), "bedroom_04_Q11": (["E03"], []),
    "bedroom_04_Q07": (["E04"], ["E02"]), "bedroom_04_Q01": (["E06", "E07"], []),
    "bedroom_04_Q02": (["E10"], []), "bedroom_04_Q03": (["E11"], []),
    "bedroom_04_Q06": (["E13"], []), "bedroom_04_Q05": (["E14"], ["E15"]),
    "bedroom_04_Q08": (["E17"], []), "bedroom_04_Q04": (["E19"], []),
}


def build_m3bench() -> None:
    raw = RAW_DIR / "m3bench"
    subs = parse_srt(raw / "subtitles" / "robot" / f"{M3_VIDEO}.srt")
    ann = {q["question_id"]: q for q in json.loads((raw / "robot.json").read_text())[M3_VIDEO]["qa_list"]}
    frames = frames_at(str(raw / "videos" / "robot" / f"{M3_VIDEO}.mp4"), [hms_to_s(e[3]) for e in M3_EVIDENCE])
    items, images = [], {}
    for (eid, a, b, key, note), img in zip(M3_EVIDENCE, frames):
        lo, hi = hms_to_s(a), hms_to_s(b)
        items.append({"evidence_id": eid, "t_event": lo, "time_str": f"video {fmt_t(lo)}-{fmt_t(hi)}",
                      "window": [lo, hi], "source": "robot camera + dialogue", "modality": "text+image",
                      "text": window_text(subs, lo, hi, speakers=True), "image_t": hms_to_s(key),
                      "curation_note": note,
                      "provenance": {"dataset": "M3-Bench-Robot", "video": M3_VIDEO, "license": "CC BY-NC-SA 4.0"}})
        images[eid] = img
    questions = []
    for qid, (sup, rel) in M3_QUESTIONS.items():
        q = ann[qid]
        questions.append({"qa_id": qid, "question": q["question"], "answer": q["answer"], "format": "open",
                          "qtype": q["type"], "supporting_evidence": sup, "related_evidence": rel,
                          "original": {"timestamp": q["timestamp"], "reasoning_zh": q["reasoning"]}})
    stream = {"stream_id": f"m3r-{M3_VIDEO}-sample-v1", "dataset": "m3bench", "split": "dev",
              "evidence": items, "questions": questions}
    write_sample(EXAMPLES / f"m3bench_{M3_VIDEO}", stream, images,
                 f"Sample evidence stream: M3-Bench-Robot `{M3_VIDEO}` (dev split)",
                 ["One robot-view video (27.5 min). Item text = the dialogue subtitles in a 25-70 s window; "
                  "image = the frame at the key line. All 10 answers are in the dialogue; from ~12:00 the "
                  "camera is still, so later frames add little.",
                  "Source: M3-Bench (ByteDance-Seed), CC BY-NC-SA 4.0. Non-commercial research use only."],
                 {e[0]: e[3] for e in M3_EVIDENCE})


# ----------------------------------------------------------------------------- DisasterVQA
DVQA_ORDER = ["img-906", "img-138", "img-139", "img-213", "img-214", "img-216", "img-205", "img-206",
              "img-218", "img-207", "img-882", "img-219", "img-883", "img-912", "img-142", "img-910",
              "img-872", "img-879", "img-902", "img-875"]
DVQA_QUESTIONS = {  # image -> substring identifying the question to ask about it
    "img-138": "emergency responders", "img-213": "white truck", "img-216": "flotation",
    "img-205": "objects are visible", "img-218": "attempting to drive",
    "img-882": "under the water", "img-883": "on the roof", "img-142": "level of floodwater",
    "img-910": "children", "img-902": "assist themselves",
}
DVQA_NOTES = {"img-872": "distractor: FOUR trapped vehicles (vs. two underwater in E11)"}
_FORMAT = {"Binary": "yesno", "Multiple-Choice": "mc", "Open-Ended": "open"}


def _post_time(path: str) -> tuple[dt.datetime, str]:
    name = path.split("/")[-1]
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})", name)
    if m:
        return dt.datetime(*map(int, m.groups())), "file name"
    m = re.match(r"(\d{17,19})_", name)   # tweet snowflake id encodes the post time
    ms = (int(m.group(1)) >> 22) + 1288834974657
    return dt.datetime.fromtimestamp(ms / 1000, dt.UTC).replace(tzinfo=None, second=0, microsecond=0), "tweet id"


def _fact(r: dict) -> str:
    stem = r["question"].split("?")[0].strip() + "?"
    a = r["groundtruth_answer"]
    if r.get("choices"):
        a = ", ".join(r["choices"][x] for x in (a if isinstance(a, list) else [a]))
    elif isinstance(a, list):
        a = a[0]
    return f"- {stem} {a}"


def build_disastervqa() -> None:
    from PIL import Image
    from streamrag.data import get_dataset
    ds = get_dataset("disastervqa")
    by_img = collections.defaultdict(list)
    for r in ds.load():
        by_img[r["image_id"]].append(r)
    root = ds._annotations_path().parent
    times = {i: _post_time(by_img[i][0]["image_path"]) for i in DVQA_ORDER}
    t0 = min(t for t, _ in times.values())
    items, images, questions = [], {}, []
    for k, img in enumerate(DVQA_ORDER, 1):
        eid, rs = f"E{k:02d}", by_img[img]
        t, how = times[img]
        tstr = t.strftime("%b %d %H:%M") + " UTC"
        qtext = DVQA_QUESTIONS.get(img)
        note = DVQA_NOTES.get(img, "distractor" if not qtext else "")
        items.append({"evidence_id": eid, "t_event": (t - t0).total_seconds(), "time_str": tstr,
                      "source": f"social media photo ({rs[0]['dataset_source']})", "modality": "text+image",
                      "text": f"Flood photo posted {tstr}.\nVerified observations:\n" + "\n".join(map(_fact, rs)),
                      "curation_note": note,
                      "provenance": {"dataset": "DisasterVQA", "image_id": img, "image_path": rs[0]["image_path"],
                                     "time_from": how, "license": "CC BY-SA 4.0"}})
        images[eid] = Image.open(root / rs[0]["image_path"])
        if qtext:
            r = next(x for x in rs if qtext in x["question"])
            gold = r["groundtruth_answer"]
            fmt = "mc_multi" if isinstance(gold, list) and r.get("choices") and len(gold) > 1 else \
                _FORMAT[r["question_type"]]
            ans = gold[0] if isinstance(gold, list) and fmt in ("mc", "open") else gold
            questions.append({"qa_id": r["question_id"], "question": f"About the photo posted {tstr}: {r['question']}",
                              "answer": ans, "accepted_answers": gold if isinstance(gold, list) else [gold],
                              "options": r.get("choices"), "format": fmt, "qtype": r["question_type"],
                              "supporting_evidence": [eid], "related_evidence": [],
                              "original": {"question": r["question"], "image_id": img}})
    stream = {"stream_id": "dvqa-flood-2017-sample-v1", "dataset": "disastervqa", "split": "dev",
              "evidence": items, "questions": questions}
    write_sample(EXAMPLES / "disastervqa_flood_2017", stream, images,
                 "Sample evidence stream: DisasterVQA flood photos, Aug 27 - Sep 19 2017 (dev split)",
                 ["20 flood photos from the dev split, in real posting order (times from tweet ids or "
                  "file names). Item text = the photo's verified facts from the DisasterVQA annotations "
                  "(no captioning), so each answer appears in its item's text; the memory test is keeping "
                  "the right fact tied to the right photo time.",
                  "Source: DisasterVQA (QCRI), CC BY-SA 4.0; images from MEDIC and CrisisMMD."],
                 {f"E{k:02d}": times[i][0].strftime("%m-%d %H:%M") for k, i in enumerate(DVQA_ORDER, 1)})


# ----------------------------------------------------------------------------- Video-MME
VMME_VIDEOS = {  # videoID -> label used in item text and question prefix
    "YtAL8y2lACs": "Ross Ice Shelf expedition documentary",
    "PHe0bXAIuk0": "'How the economic machine works' explainer",
    "O7zcPvQDIMU": "Norman Conquest history documentary",
    "iOjmy8zkDGQ": "Earth formation documentary",
    "qd2ivr-5oEM": "CBC news broadcast",
}
VMME_EVIDENCE = [  # (id, video, start, end, key frame, note)
    ("E01", "YtAL8y2lACs", "06:01", "06:30", "06:16", "related: huge crevasses in the shear zone"),
    ("E02", "YtAL8y2lACs", "13:00", "13:30", "13:15", "supports helicopter-caution question"),
    ("E03", "YtAL8y2lACs", "15:20", "15:50", "15:30", "distractor"),
    ("E04", "YtAL8y2lACs", "22:00", "22:42", "22:25", "supports fracture question (shearing)"),
    ("E05", "YtAL8y2lACs", "23:00", "23:40", "23:20", "distractor: crevasse rescue / GPR"),
    ("E06", "PHe0bXAIuk0", "00:00", "00:45", "00:20", "supports main-focus question"),
    ("E07", "PHe0bXAIuk0", "05:08", "05:40", "05:20", "supports mechanism question"),
    ("E08", "PHe0bXAIuk0", "08:00", "08:35", "08:15", "related: 'my spending is another person's income'"),
    ("E09", "PHe0bXAIuk0", "12:00", "12:35", "12:15", "distractor: inflation"),
    ("E10", "PHe0bXAIuk0", "18:00", "18:30", "18:15", "supports recession-vs-deleveraging question"),
    ("E11", "O7zcPvQDIMU", "13:55", "14:30", "14:10", "distractor: Edward's death, Harold's coronation (wrong options)"),
    ("E12", "O7zcPvQDIMU", "20:15", "21:20", "20:45", "supports after-Stamford-Bridge question"),
    ("E13", "iOjmy8zkDGQ", "02:04", "02:52", "02:30", "distractor: core accretion, solar wind"),
    ("E14", "iOjmy8zkDGQ", "23:19", "23:58", "23:47", "supports double-barreled-shotgun question"),
    ("E15", "qd2ivr-5oEM", "02:30", "03:00", "02:45", "supports ship power-loss question"),
    ("E16", "qd2ivr-5oEM", "08:05", "09:10", "08:30", "supports Marineland question"),
    ("E17", "qd2ivr-5oEM", "12:50", "13:25", "13:05", "supports NOT-mentioned question (Israel-Hamas talks)"),
    ("E18", "qd2ivr-5oEM", "13:45", "14:15", "13:55", "supports NOT-mentioned question (Raptors gambling probe)"),
    ("E19", "qd2ivr-5oEM", "26:20", "26:50", "26:30", "related: guest discusses the first blackout"),
    ("E20", "qd2ivr-5oEM", "34:00", "34:40", "34:15", "supports NOT-mentioned question (Haiti journalist)"),
]
VMME_QUESTIONS = [  # (videoID, index among its 3 questions, supporting, related)
    ("YtAL8y2lACs", 1, ["E02"], ["E01"]), ("YtAL8y2lACs", 2, ["E04"], ["E01"]),
    ("PHe0bXAIuk0", 0, ["E06"], []), ("PHe0bXAIuk0", 1, ["E07"], ["E08"]), ("PHe0bXAIuk0", 2, ["E10"], []),
    ("O7zcPvQDIMU", 1, ["E12"], ["E11"]), ("iOjmy8zkDGQ", 1, ["E14"], []),
    ("qd2ivr-5oEM", 2, ["E15"], ["E19"]), ("qd2ivr-5oEM", 1, ["E16"], []),
    ("qd2ivr-5oEM", 0, ["E17", "E18", "E20"], []),
]


def build_videomme() -> None:
    import pandas as pd
    from streamrag.data import get_dataset
    from streamrag.video.frames import video_duration
    ds = get_dataset("videomme")
    ds.fetch_videos(list(VMME_VIDEOS))
    df = pd.read_parquet(RAW_DIR / "videomme" / "videomme" / "test-00000-of-00001.parquet")
    offset, t = {}, 0.0
    for v in VMME_VIDEOS:   # stream time = videos played back to back in this order
        offset[v] = t
        t += video_duration(str(ds.video_dir / f"{v}.mp4"))
    items, images = [], {}
    for eid, v, a, b, key, note in VMME_EVIDENCE:
        lo, hi = hms_to_s(a), hms_to_s(b)
        subs = parse_srt(RAW_DIR / "videomme" / "subtitle" / f"{v}.srt")
        images[eid] = frames_at(str(ds.video_dir / f"{v}.mp4"), [hms_to_s(key)])[0]
        items.append({"evidence_id": eid, "t_event": round(offset[v] + lo, 1),
                      "time_str": f"{VMME_VIDEOS[v]} {fmt_t(lo)}-{fmt_t(hi)}", "window": [lo, hi],
                      "source": f"video: {VMME_VIDEOS[v]}", "modality": "text+image",
                      "text": f"[{VMME_VIDEOS[v]}, {fmt_t(lo)}]\n" + window_text(subs, lo, hi, speakers=False),
                      "image_t": hms_to_s(key), "curation_note": note,
                      "provenance": {"dataset": "Video-MME", "videoID": v, "license": "see dataset card"}})
    questions = []
    for v, idx, sup, rel in VMME_QUESTIONS:
        r = df[df.videoID == v].iloc[idx]
        questions.append({"qa_id": r.question_id, "question": f"In the {VMME_VIDEOS[v]}: {r.question}",
                          "answer": r.answer, "options": list(r.options), "format": "mc",
                          "qtype": r.task_type, "supporting_evidence": sup, "related_evidence": rel,
                          "original": {"question": r.question, "videoID": v, "url": r.url}})
    stream = {"stream_id": "vmme-5video-sample-v1", "dataset": "videomme", "split": "dev",
              "evidence": items, "questions": questions}
    write_sample(EXAMPLES / "videomme_5videos", stream, images,
                 "Sample evidence stream: Video-MME, 5 long dev videos",
                 ["Video-MME has only 3 questions per video, so the stream joins segments of 5 long dev "
                  "videos played back to back (stream time = offset of the video + segment time). Item text "
                  "= the subtitles in a 30-65 s window; image = frame at the key line. Questions are prefixed "
                  "with their video's name because several videos share the stream. Whole-video summary "
                  "questions and answers that only appear on screen were not used.",
                  "Source: Video-MME (lmms-eval/Video-MME); see the dataset card for terms."],
                 {e[0]: f"{e[1][:5]} {e[4]}" for e in VMME_EVIDENCE})


# ----------------------------------------------------------------------------- MindCube-Tiny
MC_SCENES = [  # (scene folder, number of questions to use); first three = items 1-10
    ("other_all_image/among/shoe_216", 3),
    ("other_all_image/around/4a0b0219bbf9862766e8fdbb860d565b07ec53baa798820bbc309dc912539887", 1),
    ("other_all_image/around/a89812fe7ffacebfef15c98058ad1e660941c3a041132e772035715fb3113852", 1),
    ("other_all_image/among/shoe_013", 3),
    ("other_all_image/around/3d789fc9eb1286e1318a4a941e818ec4a0f51b25a81ae53a949114d5211916bb", 1),
    ("other_all_image/around/a47664c84880a655d1aab273620e00e57f66bbe47c9ff463b26584225fddedee", 1),
]
MC_DT = 60.0   # synthetic seconds between photos (MindCube has no time axis)


_NOT_OBJECTS = {"none", "left", "right", "front", "back", "face", "behind", "little", "heavey",
                "heavy", "total", "self", "middle", ""}


def _strings(x) -> list[str]:
    """Object names in MindCube meta_info (which also holds direction / weight labels)."""
    if isinstance(x, str):
        return [] if x.strip().lower() in _NOT_OBJECTS else [x]
    if isinstance(x, list):
        return [s for y in x for s in _strings(y)]
    return []


def build_mindcube() -> None:
    from PIL import Image
    from streamrag.data import get_dataset
    ds = get_dataset("mindcube")
    by = collections.defaultdict(list)
    for r in ds.load():
        by["/".join(r["images"][0].split("/")[:-1])].append(r)
    items, images, questions, eid_of = [], {}, [], {}
    for sc, nq in MC_SCENES:
        rs = sorted(by[sc], key=lambda r: r["id"])
        full = max(rs, key=lambda r: len(r["images"]))           # question using all photos
        views = re.search(r"\(([^)]*(?:front|back|left|right)[^)]*)\)", full["question"])
        views = [v.strip().replace("and ", "") for v in views.group(1).split(",")] if views else \
            [f"view {i + 1}" for i in range(len(full["images"]))]
        subject = re.search(r"showing the (.+?) from different viewpoints", full["question"])
        label = f"the {subject.group(1)} scene" if subject and subject.group(1) != "same scene" else \
            f"room scene {sc.split('/')[-1][:6]}"
        objs = sorted({o for r in rs for o in _strings(r["meta_info"])}, key=str.lower)
        for p, view in zip(full["images"], views):
            eid = f"E{len(items) + 1:02d}"
            eid_of[p] = eid
            items.append({"evidence_id": eid, "t_event": len(items) * MC_DT,
                          "time_str": f"t+{fmt_t(len(items) * MC_DT)}, {label}, {view} view",
                          "source": "robot camera photo", "modality": "text+image",
                          "text": f"Photo of {label}, taken from the {view} side."
                                  + (f"\nObjects annotated in this scene: {', '.join(objs)}." if objs else ""),
                          "curation_note": "distractor for questions about other scenes",
                          "provenance": {"dataset": "MindCube-Tiny", "image": p, "license": "MIT"}})
            images[eid] = Image.open(ds.data_root / p)
        # pick questions that use only this scene's photos, preferring distinct answers
        picked, seen = [], set()
        for r in sorted(rs, key=lambda r: (-len(r["images"]), r["id"])):
            if all(p in eid_of for p in r["images"]) and r["gt_answer"] not in seen:
                picked.append(r)
                seen.add(r["gt_answer"])
            if len(picked) == nq:
                break
        for r in picked:
            mapping = ", ".join(f"image {i + 1} = {eid_of[p]}" for i, p in enumerate(r["images"]))
            questions.append({"qa_id": r["id"], "question": f"({mapping}) {r['question']}",
                              "answer": r["gt_answer"], "format": "mc", "qtype": r["id"].split("_")[0],
                              "supporting_evidence": [eid_of[p] for p in r["images"]], "related_evidence": [],
                              "original": {"question": r["question"], "category": r.get("category")}})
    stream = {"stream_id": "mc-6scene-sample-v1", "dataset": "mindcube", "split": "dev",
              "evidence": items, "questions": questions}
    write_sample(EXAMPLES / "mindcube_6scenes", stream, images,
                 "Sample evidence stream: MindCube-Tiny, 6 dev scenes",
                 ["20 photos from 6 dev scenes (4 + 3 + 3 photos in items 1-10, 4 + 3 + 3 in items 11-20), "
                  "60 s apart (MindCube has no time axis). Item text comes only from the dataset's own "
                  "annotations: which side the photo was taken from and the annotated object names. "
                  "MindCube answers are spatial, so the support is in the images, not the text: a text-only "
                  "memory cannot answer these questions. Questions are prefixed with which evidence item "
                  "each 'image k' refers to.",
                  "Source: MindCube (MLL-Lab), MIT license."],
                 {it["evidence_id"]: it["time_str"].split(", ", 1)[1][:22] for it in items})


BUILDERS = {"m3bench": build_m3bench, "disastervqa": build_disastervqa,
            "videomme": build_videomme, "mindcube": build_mindcube}

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("datasets", nargs="+", choices=[*BUILDERS, "all"])
    for name in (list(BUILDERS) if "all" in ap.parse_args().datasets else ap.parse_args().datasets):
        BUILDERS[name]()
