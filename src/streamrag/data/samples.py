"""Shared writer for hand-curated sample evidence streams (codebase_plan.md §9).

Every sample has 20 evidence items (text + image) and 10 questions whose answers are
supported by listed evidence items. The example instance delivers the items in the given
order and asks every question at checkpoints 1, 10 and 20. `write_sample` checks that
exactly half of the questions are supported by items 1-10 and the other half only by
items 11-20, and fails otherwise.

Output folder: stream.json, example_chronological.json, images/, contact_sheet.jpg, README.md
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

from PIL import Image

from streamrag.video.frames import contact_sheet

N_EVIDENCE, N_QUESTIONS, CHECKPOINTS = 20, 10, (1, 10, 20)
ABSTAIN = "Not enough evidence."


def build_example(stream: dict) -> dict:
    """Delivery in list order + per-checkpoint gold answers; validates the 5/5 split."""
    items, questions = stream["evidence"], stream["questions"]
    assert len(items) == N_EVIDENCE, f"{len(items)} evidence items"
    assert len(questions) == N_QUESTIONS, f"{len(questions)} questions"
    ids = [it["evidence_id"] for it in items]
    assert len(set(ids)) == N_EVIDENCE, "duplicate evidence ids"
    pos = {eid: i + 1 for i, eid in enumerate(ids)}
    half = N_EVIDENCE // 2
    table, counts = [], {k: 0 for k in CHECKPOINTS}
    for q in questions:
        missing = [e for e in q["supporting_evidence"] + q.get("related_evidence", []) if e not in pos]
        assert not missing, f"{q['qa_id']}: unknown evidence {missing}"
        ready = max(pos[e] for e in q["supporting_evidence"])
        first = ready <= half
        if not first:
            assert all(pos[e] > half for e in q["supporting_evidence"]), \
                f"{q['qa_id']}: second-half question uses first-half evidence"
        row = {"qa_id": q["qa_id"], "question": q["question"], "answerable_from_item": ready,
               "half": "first" if first else "second", "gold_by_checkpoint": {}}
        for k in CHECKPOINTS:
            row["gold_by_checkpoint"][str(k)] = q["answer"] if ready <= k else ABSTAIN
            counts[k] += ready <= k
        table.append(row)
    n_first = sum(r["half"] == "first" for r in table)
    assert n_first == N_QUESTIONS // 2, f"{n_first} first-half questions (need {N_QUESTIONS // 2})"
    return {
        "example_id": f"{stream['stream_id']}-chronological", "stream_id": stream["stream_id"],
        "delivery": [{"position": i + 1, "evidence_id": it["evidence_id"], "t_delivery": it["t_event"]}
                     for i, it in enumerate(items)],
        "checkpoints": list(CHECKPOINTS),
        "answerable_counts": {str(k): v for k, v in counts.items()},
        "first_half_questions": [r["qa_id"] for r in table if r["half"] == "first"],
        "second_half_questions": [r["qa_id"] for r in table if r["half"] == "second"],
        "questions": table,
    }


def write_sample(out: Path, stream: dict, images: dict[str, Image.Image], title: str,
                 notes: list[str], image_labels: dict[str, str] | None = None) -> dict:
    """Write one sample folder. `images` maps evidence_id -> PIL image."""
    example = build_example(stream)
    if out.exists():
        shutil.rmtree(out)
    (out / "images").mkdir(parents=True)
    for it in stream["evidence"]:
        im = images[it["evidence_id"]].convert("RGB")
        im.thumbnail((640, 640))
        im.save(out / "images" / f"{it['evidence_id']}.jpg", quality=85)
        it["image"] = f"images/{it['evidence_id']}.jpg"
    (out / "stream.json").write_text(json.dumps(stream, indent=1, ensure_ascii=False))
    (out / "example_chronological.json").write_text(json.dumps(example, indent=1, ensure_ascii=False))
    labels = image_labels or {}
    contact_sheet([images[it["evidence_id"]] for it in stream["evidence"]],
                  [f"{it['evidence_id']} {labels.get(it['evidence_id'], '')}" for it in stream["evidence"]],
                  cols=5, thumb=256).save(out / "contact_sheet.jpg", quality=85)
    _readme(out, stream, example, title, notes)
    print(f"wrote {out} | answerable at checkpoints {example['answerable_counts']}")
    return example


def _fmt_answer(q: dict) -> str:
    a = q["answer"]
    a = ", ".join(a) if isinstance(a, list) else str(a)
    if q.get("options") and isinstance(q["options"], dict):
        keys = q["answer"] if isinstance(q["answer"], list) else [q["answer"]]
        a += " (" + "; ".join(q["options"].get(k, k) for k in keys) + ")"
    elif q.get("options") and isinstance(q["options"], list):
        a = next((o for o in q["options"] if o.startswith(f"{a}.")), a)
    return a.replace("|", "/")


def _readme(out: Path, stream: dict, ex: dict, title: str, notes: list[str]) -> None:
    qmap = {q["qa_id"]: q for q in stream["questions"]}
    c = ex["answerable_counts"]
    L = [f"# {title}", "", *notes, "",
         "- `stream.json`: 20 evidence items (text + image) and 10 questions with supporting-evidence links.",
         "- `example_chronological.json`: delivery in the listed order, with the gold answer of every "
         "question at checkpoints 1, 10 and 20 (\"Not enough evidence.\" before its evidence has arrived).",
         "- `contact_sheet.jpg`: all 20 images.", "",
         f"**Answerable questions per checkpoint:** after item 1: {c['1']}, after item 10: {c['10']}, "
         f"after item 20: {c['20']}.", "", "## Questions", "",
         "| # | Question | Gold answer | Supporting evidence | Answerable from item | Half |",
         "|---|---|---|---|---|---|"]
    for i, r in enumerate(sorted(ex["questions"], key=lambda r: r["answerable_from_item"]), 1):
        q = qmap[r["qa_id"]]
        rel = f" (related: {', '.join(q['related_evidence'])})" if q.get("related_evidence") else ""
        qtext = q["question"].replace("\n", " ").replace("|", "/")
        L.append(f"| {i} | {qtext} | {_fmt_answer(q)} | {', '.join(q['supporting_evidence'])}{rel} "
                 f"| {r['answerable_from_item']} | {r['half']} |")
    L += ["", "## Evidence (in delivery order)", ""]
    for it in stream["evidence"]:
        sup = [q["qa_id"] for q in stream["questions"] if it["evidence_id"] in q["supporting_evidence"]]
        tag = f"supports {', '.join(sup)}" if sup else it.get("curation_note", "")
        L += [f"### {it['evidence_id']} · {it.get('time_str', '')} · {tag}", "",
              f"![{it['evidence_id']}]({it['image']})", "", "```", it["text"], "```", ""]
    (out / "README.md").write_text("\n".join(L))
