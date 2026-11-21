"""Evaluation of probes (codebase_plan.md §10.6): deterministic checks first, then the fixed
local evaluator (Qwen2-VL-7B with the prompts in configs/judge/) for open-answer correctness and
evidence support. Also builds the evaluation log fed to the meta agent (§11.4).
"""
from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path

from PIL import Image

from streamrag.config import CONFIG_DIR, OUTPUT_DIR
from streamrag.parsing import parse_json_object
from streamrag.records import write_json

ANSWER_PROMPT = (CONFIG_DIR / "judge" / "answer.txt").read_text()
EVIDENCE_PROMPT = (CONFIG_DIR / "judge" / "evidence.txt").read_text()
CACHE_PATH = OUTPUT_DIR / "judge_cache.jsonl"


def _norm(s) -> str:
    return re.sub(r"[^a-z0-9 ]", "", str(s).lower()).strip()


class Evaluator:
    """Fixed evaluator with a persistent verdict cache keyed by (model, prompt, images)."""

    def __init__(self, vlm, model_name: str):
        self.vlm, self.model_name = vlm, model_name
        self.cache = {}
        if CACHE_PATH.exists():
            for line in CACHE_PATH.read_text().splitlines():
                r = json.loads(line)
                self.cache[r["key"]] = r["out"]
        self.n_calls = 0

    def _ask(self, prompt: str, images: list[str]) -> dict:
        key = hashlib.sha256(json.dumps([self.model_name, prompt, images]).encode()).hexdigest()
        if key not in self.cache:
            imgs = [Image.open(p).convert("RGB") for p in images]
            raw = self.vlm.generate(prompt, images=imgs or None, max_new_tokens=80)
            self.n_calls += 1
            out = parse_json_object(raw) or {"verdict": "unparsed", "reason": raw[:200]}
            self.cache[key] = out
            CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
            with open(CACHE_PATH, "a") as f:
                f.write(json.dumps({"key": key, "out": out}) + "\n")
        return self.cache[key]

    def answer_verdict(self, q: dict, pred: str) -> dict:
        ref = "; ".join(map(str, q["accepted_answers"]))
        return self._ask(ANSWER_PROMPT.format(question=q["original"], reference=ref, candidate=pred), [])

    def evidence_verdict(self, q: dict, answer_text: str, items: list[dict], facts: dict) -> dict:
        desc = ", ".join(f"{it['item_id']} (posted {it['time_str']})" for it in items)
        fact_txt = "\n".join(f"{it['item_id']}: " + "; ".join(facts.get(it["item_id"], [])) for it in items)
        prompt = EVIDENCE_PROMPT.format(items=desc, facts=fact_txt, question=q["original"], answer=answer_text)
        return self._ask(prompt, [f["path"] for it in items for f in it["frames"]][:3])


def answer_text_of(q: dict, pred) -> str:
    """Readable form of a prediction (letters -> option text) for the judges and logs."""
    if q.get("options") and pred is not None:
        letters = pred if isinstance(pred, list) else [pred]
        return ", ".join(f"{l} ({q['options'].get(l, '?')})" for l in letters)
    return str(pred)


def correctness(q: dict, a: dict, ev: Evaluator) -> tuple[float, str]:
    fmt, pred = q["format"], a["pred"]
    if fmt == "mc":
        return float(pred == q["gold"]), "exact"
    if fmt == "mc_multi":
        return float(isinstance(pred, list) and sorted(pred) == sorted(q["gold"])), "exact"
    if fmt == "yesno":
        return float(_norm(pred) == _norm(q["gold"])), "exact"
    p = _norm(pred)
    for acc in q["accepted_answers"]:            # open: accepted-answer match before the LLM
        if p and (p == _norm(acc) or (len(_norm(acc)) > 2 and _norm(acc) in p and len(p) <= 3 * len(_norm(acc)))):
            return 1.0, "accepted_match"
    v = ev.answer_verdict(q, str(pred)).get("verdict", "")
    return {"correct": 1.0, "partial": 0.5}.get(v, 0.0), f"llm:{v}"


def retention_history(item_id: str, snaps: list[dict], upto: int) -> dict:
    """When the item entered memory and whether it was still there at step `upto`."""
    hist = [(sn["step"], item_id in {s for l in sn["lines"] for s in l["sources"]})
            for sn in snaps if sn["step"] <= upto]
    present = [p for _, p in hist]
    if not any(present):
        return {"status": "never_stored"}
    stored = hist[present.index(True)][0]
    if present[-1]:
        return {"status": "in_memory", "stored_at": stored}
    deleted = next(st for st, p in hist if st > stored and not p)
    return {"status": "deleted", "stored_at": stored, "deleted_at": deleted}


def evaluate(stream: dict, snaps: list[dict], answers: list[dict], ev: Evaluator, out_path: Path,
             progress=print) -> list[dict]:
    """Score every answered probe (here: each question at the end of the stream)."""
    items = {it["item_id"]: it for it in stream["items"]}
    qs = {q["qa_id"]: q for q in stream["questions"]}
    snap_at = {sn["step"]: sn for sn in snaps}
    rows = []
    for a in answers:
        q, t = qs[a["qa_id"]], a["step"]
        snap = snap_at[t]
        scope = q["evidence_scope"]
        delivered = {it["item_id"] for it in stream["items"] if it["step"] <= t}
        mem_src = {s for l in snap["lines"] for s in l["sources"]}
        retained = any(s in mem_src for s in scope)
        r = {"step": t, "qa_id": q["qa_id"], "label": a["label"], "abstained": a["abstained"],
             "pred": a["pred"], "cited_items": a["cited_items"], "retained": retained}
        if a["label"] == "not_yet":
            r.update(score=1.0 if a["abstained"] else 0.0,
                     category="correct_abstention" if a["abstained"] else "premature_answer")
        elif a["abstained"]:
            r.update(score=0.0, category="unnecessary_abstention" if retained else "abstained_evidence_missing")
        else:
            c, how = correctness(q, a, ev)
            cited = set(a["cited_items"])
            cite_ok = cited <= delivered and bool(cited & set(scope))
            r.update(correctness=c, correctness_by=how, citation_valid=cite_ok)
            if c == 0:
                r.update(score=0.0, category="wrong_answer_evidence_in_memory" if retained
                         else "wrong_answer_evidence_missing")
            elif not cite_ok:
                r.update(score=0.0, category="invalid_citation")
            else:
                ev_items = [items[i] for i in scope if i in cited]
                v = ev.evidence_verdict(q, answer_text_of(q, a["pred"]), ev_items, stream["reference_facts"])
                r["evidence_verdict"] = v.get("verdict")
                r["evidence_reason"] = v.get("reason")
                if v.get("verdict") == "supported":
                    r.update(score=c, category="correct" if c == 1 else "partially_correct")
                elif v.get("verdict") == "unsupported":
                    r.update(score=0.0, category="unsupported")
                else:
                    r.update(score=0.5 * c, category="evidence_insufficient")
        rows.append(r)
    write_json(out_path, rows)
    progress(f"evaluated {len(rows)} questions: score {sum(r['score'] for r in rows) / max(1, len(rows)):.2f} "
             f"({ev.n_calls} evaluator calls)")
    return rows


def summarize(stream: dict, rows: list[dict], mem_logs: list[dict], snaps: list[dict]) -> dict:
    """Scores for one evidence stream evaluated at its end."""
    mean = lambda xs: round(sum(xs) / len(xs), 4) if xs else None
    return {
        "esqa_mean": mean([r["score"] for r in rows]),
        "answered_correct": mean([float(r.get("correctness", 0) == 1) for r in rows]),
        "abstained": mean([float(r["abstained"]) for r in rows]),
        "correct_count": f"{sum(r['score'] == 1 for r in rows)}/{len(rows)}",
        "retention_final": mean([float(r["retained"]) for r in rows]),
        "categories": dict(collections.Counter(r["category"] for r in rows)),
        "budget_fallbacks": sum(1 for l in mem_logs if l.get("fallback")),
        "final_memory_tokens": snaps[-1]["tokens"],
        "final_memory_lines": len(snaps[-1]["lines"]),
        "n_questions": len(rows), "n_items": len(stream["items"]),
    }


def combine(per_stream: dict[str, dict]) -> dict:
    """Node score = mean of the per-stream scores."""
    vals = [s["esqa_mean"] for s in per_stream.values() if s["esqa_mean"] is not None]
    cats = collections.Counter()
    for s in per_stream.values():
        cats.update(s["categories"])
    n_q = sum(s["n_questions"] for s in per_stream.values())
    n_right = sum(int(s["correct_count"].split("/")[0]) for s in per_stream.values())
    return {"esqa_mean": round(sum(vals) / len(vals), 4) if vals else None,
            "correct_count": f"{n_right}/{n_q}",
            "retention_final": round(sum(s["retention_final"] * s["n_questions"] for s in per_stream.values()) / n_q, 4),
            "abstained": round(sum(s["abstained"] * s["n_questions"] for s in per_stream.values()) / n_q, 4),
            "budget_fallbacks": sum(s["budget_fallbacks"] for s in per_stream.values()),
            "categories": dict(cats), "streams": per_stream}


def build_meta_log(stream: dict, rows: list[dict], snaps: list[dict], mem_logs: list[dict],
                   scores: dict, budget: int, max_cases: int = 12) -> str:
    """Evaluation log of one evidence stream for the meta agent (§11.4)."""
    qs = {q["qa_id"]: q for q in stream["questions"]}
    items = {it["item_id"]: it for it in stream["items"]}
    snap_at = {sn["step"]: sn for sn in snaps}
    L = [f"STREAM {stream['stream_id']}: {len(stream['items'])} photos ({stream['items'][0]['item_id']}-"
         f"{stream['items'][-1]['item_id']}), memory budget {budget} tokens. The memory agent never sees the "
         f"questions; {len(qs)} questions were asked once, after the last photo.",
         f"SCORE: {scores['esqa_mean']} ({scores['correct_count']} questions correct with valid evidence; "
         f"abstained on {scores['abstained']}; evidence still in memory for {scores['retention_final']} of the "
         f"questions; final memory {scores['final_memory_lines']} lines / {scores['final_memory_tokens']} tokens; "
         f"budget fallbacks {scores['budget_fallbacks']}).",
         "OUTCOMES: " + ", ".join(f"{k}={v}" for k, v in sorted(scores["categories"].items())),
         "", "PER QUESTION (asked after the last photo):"]
    for r in rows[:max_cases]:
        q = qs[r["qa_id"]]
        scope = q["evidence_scope"][0]
        hist = retention_history(scope, snaps, r["step"])
        diag = {"never_stored": "evidence never stored (no memory line ever cited this photo)",
                "deleted": f"evidence stored at step {hist.get('stored_at')}, deleted at step {hist.get('deleted_at')}",
                "in_memory": f"evidence in memory (stored at step {hist.get('stored_at')})"}[hist["status"]]
        mem = [l["text"] for l in snap_at[r["step"]]["lines"] if scope in l["sources"]]
        L.append(f"* {r['category']} | {scope} (posted {items[scope]['time_str']}): {q['original']}")
        L.append(f"  gold: {answer_text_of(q, q['gold'])} | given: "
                 f"{'NOT_ENOUGH_EVIDENCE' if r['abstained'] else answer_text_of(q, r['pred'])} | {diag}")
        if r["score"] < 1:
            L.append(f"  memory about {scope}: " + (" | ".join(mem) if mem else "(none)"))
            L.append(f"  what the photo actually shows (dataset facts): " + "; ".join(stream["reference_facts"][scope]))
        if r.get("evidence_reason") and r["score"] < 1:
            L.append(f"  evaluator: {r.get('evidence_verdict')} - {r['evidence_reason']}")
    L.append("MEMORY PER STEP (lines / tokens / fallback): " + "; ".join(
        f"{m['step']}:{m['n_lines']}/{m['tokens']}{'/' + m['fallback'] if m.get('fallback') else ''}" for m in mem_logs))
    L.append("FINAL MEMORY:")
    L += [f"  {l['id']} [src {', '.join(l['sources'])}] {l['text']}" for l in snaps[-1]["lines"]]
    return "\n".join(L)
