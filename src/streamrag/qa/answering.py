"""Fixed answering agent (codebase_plan.md §10.5): answers a question from a memory snapshot only,
citing memory line ids, or abstains with NOT_ENOUGH_EVIDENCE."""
from __future__ import annotations

import hashlib
import re
from pathlib import Path

from streamrag.config import CONFIG_DIR
from streamrag.data.streams import ABSTAIN
from streamrag.parsing import parse_json_object
from streamrag.records import lines, write_json

PROMPT = (CONFIG_DIR / "answering" / "prompt.txt").read_text()
INSTRUCTIONS = {
    "mc": "Answer with the letter of the correct option.",
    "mc_multi": "Several options may be correct: answer with all correct letters, separated by commas.",
    "yesno": "Answer Yes or No.",
    "open": "Answer in one to five words.",
}


def render_snapshot(snap: dict, item_time: dict) -> str:
    out = []
    for l in snap["lines"]:
        src = ", ".join(f"{s} @{item_time.get(s, '?')}" for s in l["sources"])
        out.append(f"{l['id']} [src {src}] {l['text']}")
    return "\n".join(out) or "(empty)"


def build_prompt(q: dict, snap: dict, item_time: dict) -> str:
    opts = ""
    if q.get("options"):
        opts = "\nOPTIONS:\n" + "\n".join(f"{k}. {v}" for k, v in q["options"].items())
    return PROMPT.format(memory=render_snapshot(snap, item_time), step=snap["step"],
                         question=q["question"], options=opts, instruction=INSTRUCTIONS[q["format"]])


def parse_answer(raw: str, fmt: str, line_ids: set[str]) -> dict:
    obj = parse_json_object(raw) or {}
    ans = str(obj.get("answer", raw)).strip()
    cited = [c for c in (obj.get("cited") or []) if isinstance(c, str)]
    abstained = ABSTAIN.lower() in ans.lower().replace(" ", "_") or "not enough evidence" in ans.lower()
    pred = None
    if not abstained:
        if fmt == "mc":
            m = re.match(r"^\(?([A-H])\b", ans) or re.search(r"\b([A-H])\b", ans)
            pred = m.group(1) if m else ans
        elif fmt == "mc_multi":
            pred = sorted(set(re.findall(r"\b([A-H])\b", ans))) or ans
        elif fmt == "yesno":
            m = re.match(r"^\W*(yes|no)\b", ans, re.I)
            pred = m.group(1).capitalize() if m else ans
        else:
            pred = ans
    return {"answer_raw": ans, "pred": pred, "abstained": abstained,
            "cited_lines": cited, "cited_unknown": [c for c in cited if c not in line_ids], "parsed": bool(obj)}


def run_answer_pass(vlm, stream: dict, snaps: list[dict], out_path: Path, progress=print) -> list[dict]:
    item_time = {it["item_id"]: it["time_str"] for it in stream["items"]}
    rows, cache = [], {}
    N, nq = len(snaps), len(stream["questions"])
    for snap in snaps:
        line_src = {l["id"]: l["sources"] for l in snap["lines"]}
        for q in stream["questions"]:
            prompt = build_prompt(q, snap, item_time)
            key = hashlib.sha256(prompt.encode()).hexdigest()
            if key not in cache:
                cache[key] = vlm.generate(prompt, max_new_tokens=80)
            a = parse_answer(cache[key], q["format"], set(line_src))
            cited_items = sorted({s for c in a["cited_lines"] for s in line_src.get(c, [])})
            rows.append({"step": snap["step"], "qa_id": q["qa_id"],
                         "label": q["answerability"][snap["step"] - 1], **a, "cited_items": cited_items,
                         "raw": lines(cache[key])})
        n_abst = sum(r["abstained"] for r in rows[-nq:])
        progress(f"answer step {snap['step']:2d}/{N}: {nq} questions ({nq - n_abst} answered, {n_abst} abstained)")
    write_json(out_path, rows)
    return rows
