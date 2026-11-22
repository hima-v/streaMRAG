"""Human-readable Markdown reports for an experiment run.

- write_streams_md:     <archive>/evaluation_streams.md, one section per evaluation stream
                        (photos with posting times and dataset facts, questions with gold answers)
- write_stream_eval_md: <node>/runs/<stream>/evaluation.md, written after answering + evaluation:
                        1) the memory snapshot the answering agent had at test time,
                        2) every question with gold answer, the agent's answer and cited evidence,
                           and the evaluation outcome and score
Images are linked by relative path (VS Code / GitHub Markdown preview show them).
"""
from __future__ import annotations

import os
from pathlib import Path

from streamrag.eval.judge import answer_text_of

OUTCOME = {
    "correct": "correct, cited the right photo, evidence supports it",
    "partially_correct": "partially correct, evidence supports it",
    "evidence_insufficient": "correct, but the evaluator could not confirm it from the cited photo",
    "unsupported": "correct answer text, but the cited photo does not support it",
    "invalid_citation": "correct answer, but it did not cite the question's photo",
    "wrong_answer_evidence_in_memory": "wrong answer although memory had a note about the photo",
    "wrong_answer_evidence_missing": "wrong answer; memory had no note about the photo",
    "unnecessary_abstention": "abstained although memory had a note about the photo",
    "abstained_evidence_missing": "abstained; memory had no note about the photo",
    "correct_abstention": "correctly abstained (photo not yet received)",
    "premature_answer": "answered before the photo was received",
}


def _img(path: str, md_dir: Path, width: int = 180) -> str:
    return f'<img src="{os.path.relpath(path, md_dir)}" width="{width}">'


def _cell(x) -> str:
    return str(x).replace("|", "/").replace("\n", " ")


def _options(q: dict) -> str:
    if not q.get("options"):
        return ""
    return " · ".join(f"**{k}.** {v}" for k, v in q["options"].items())


def write_streams_md(arch_dir: Path, streams: list[dict], setup: dict) -> Path:
    md_path = arch_dir / "evaluation_streams.md"
    nq = sum(len(s["questions"]) for s in streams)
    L = [f"# Evaluation streams: archive `{arch_dir.name}`", "",
         f"Experiment `{setup.get('experiment')}` · dataset `{setup.get('dataset')}` · "
         f"{len(streams)} streams of {streams[0]['n_steps']} photos · {nq} questions · memory budget "
         f"{setup.get('budget')} tokens · stream selection `{setup.get('stream_selection')}` (seed "
         f"{setup.get('selection_seed')})"
         + (f", reused from archive `{setup['streams_from']}`" if setup.get("streams_from") else "")
         + (f", excluding the streams of {', '.join(f'`{x}`' for x in setup['exclude_streams_from'])}"
            if setup.get("exclude_streams_from") else "") + ".", "",
         "Every node of this archive is scored on exactly these streams. In each stream the memory agent sees "
         "the photos one at a time (starting from empty memory) and never sees the questions; the questions "
         "are asked once, after the last photo, and the node score is the mean of the stream scores.", "",
         "The *dataset facts* are DisasterVQA's verified annotations of each photo. They are shown here for "
         "readers and are used only by the evaluator, never given to the memory or answering agent.", ""]
    L += ["| stream | disaster type | photos | posted | questions |", "|---|---|---|---|---|"]
    for s in streams:
        L.append(f"| [`{s['stream_id']}`](#{s['stream_id']}) | {s['disaster_type']} | {s['n_steps']} | "
                 f"{s['items'][0]['time_str'][:10]} → {s['items'][-1]['time_str'][:10]} | {len(s['questions'])} |")
    for s in streams:
        asked = {q["evidence_scope"][0] for q in s["questions"]}
        L += ["", f"## {s['stream_id']}", "",
              f"{s['disaster_type']} · {s['n_steps']} photos · {s['items'][0]['time_str']} → "
              f"{s['items'][-1]['time_str']} · {len(s['questions'])} questions after the last photo", "",
              "| step | item | posted | photo | dataset facts (evaluator only) |", "|---|---|---|---|---|"]
        for it in s["items"]:
            mark = " **(asked)**" if it["item_id"] in asked else ""
            facts = "<br>".join(_cell(f) for f in s["reference_facts"][it["item_id"]])
            L.append(f"| {it['step']} | {it['item_id']}{mark} | {it['time_str']}<br>{it['source']} | "
                     f"{_img(it['frames'][0]['path'], arch_dir, 160)} | {facts} |")
        L += ["", "**Questions** (asked after the last photo):", "",
              "| item | format | question | options | gold answer |", "|---|---|---|---|---|"]
        for q in s["questions"]:
            L.append(f"| {q['evidence_scope'][0]} | {q['format']} | {_cell(q['original'])} | {_cell(_options(q))} | "
                     f"{_cell(answer_text_of(q, q['gold']))} |")
    md_path.write_text("\n".join(L) + "\n")
    return md_path


def write_stream_eval_md(run_dir: Path, seg: dict, snap: dict, answers: list[dict], rows: list[dict],
                         sc: dict, node_id: int, budget: int) -> Path:
    md_path = run_dir / "evaluation.md"
    items = {it["item_id"]: it for it in seg["items"]}
    qs = {q["qa_id"]: q for q in seg["questions"]}
    lines = {l["id"]: l for l in snap["lines"]}
    L = [f"# Node {node_id} · stream `{seg['stream_id']}` · evaluation", "",
         f"{seg['disaster_type']} · {seg['n_steps']} photos ({seg['items'][0]['item_id']}–{seg['items'][-1]['item_id']}, "
         f"{seg['items'][0]['time_str']} → {seg['items'][-1]['time_str']}) · questions asked after step {snap['step']}", "",
         f"**Stream score: {sc['esqa_mean']}** · {sc['correct_count']} questions correct with valid evidence · "
         f"evidence still in memory for {sc['retention_final']} of the questions · abstained on {sc['abstained']}", "",
         f"## 1. Memory available to the answering agent (after step {snap['step']})", "",
         f"{len(snap['lines'])} lines, {snap['tokens']} / {budget} tokens. This is everything the answering agent "
         f"sees, besides the question; it never sees the photos.", "",
         "| line | sources (item @ posted) | text |", "|---|---|---|"]
    for l in snap["lines"]:
        src = "<br>".join(f"{s} @ {items[s]['time_str']}" if s in items else s for s in l["sources"])
        L.append(f"| {l['id']} | {src} | {_cell(l['text'])} |")
    if not snap["lines"]:
        L.append("| — | — | (memory is empty) |")

    L += ["", "## 2. Questions, answers and evaluation", "",
          "| # | item | question | gold answer | agent's answer | cited lines | outcome | score |",
          "|---|---|---|---|---|---|---|---|"]
    for i, (a, r) in enumerate(zip(answers, rows), 1):
        q = qs[a["qa_id"]]
        given = "NOT_ENOUGH_EVIDENCE" if a["abstained"] else answer_text_of(q, a["pred"])
        L.append(f"| {i} | {q['evidence_scope'][0]} | {_cell(q['original'])} | {_cell(answer_text_of(q, q['gold']))} | "
                 f"{_cell(given)} | {', '.join(a['cited_lines']) or '—'} | `{r['category']}` | {r['score']} |")
    for i, (a, r) in enumerate(zip(answers, rows), 1):
        q = qs[a["qa_id"]]
        scope = q["evidence_scope"][0]
        it = items[scope]
        given = "NOT_ENOUGH_EVIDENCE" if a["abstained"] else answer_text_of(q, a["pred"])
        L += ["", f"### Question {i}: about {scope} (posted {it['time_str']})", "",
              f"{_img(it['frames'][0]['path'], run_dir, 220)}", "",
              f"**Question:** {q['question']}"]
        if q.get("options"):
            L.append(f"\n**Options:** {_options(q)}")
        L += ["", f"- **Gold answer:** {answer_text_of(q, q['gold'])}"
              + (f" (accepted: {', '.join(map(str, q['accepted_answers']))})" if q["format"] == "open" else ""),
              f"- **Agent's answer:** {given}  (raw: `{_cell(a['answer_raw'])}`)",
              f"- **Cited memory lines:** {', '.join(a['cited_lines']) or 'none'}"]
        for cid in a["cited_lines"]:
            if cid in lines:
                L.append(f"    - {cid} [src {', '.join(lines[cid]['sources'])}]: {_cell(lines[cid]['text'])}")
            else:
                L.append(f"    - {cid}: (no such line in memory)")
        mem_about = [l for l in snap["lines"] if scope in l["sources"]]
        L += [f"- **Cited photos:** {', '.join(a['cited_items']) or 'none'} (the question is about {scope})",
              f"- **Memory about {scope}:** " + (" | ".join(f"{l['id']}: {_cell(l['text'])}" for l in mem_about)
                                                if mem_about else "none (the photo is not in memory)"),
              f"- **What the photo shows (dataset facts):** " + "; ".join(seg["reference_facts"][scope])]
        checks = []
        if "correctness" in r:
            checks.append(f"answer correctness {r['correctness']} ({r.get('correctness_by')})")
            checks.append(f"citation {'valid' if r.get('citation_valid') else 'invalid'}")
        if r.get("evidence_verdict"):
            checks.append(f"evaluator: evidence {r['evidence_verdict']} ({_cell(r.get('evidence_reason', ''))})")
        L += [f"- **Checks:** " + ("; ".join(checks) if checks else "abstained, so no answer to check"),
              f"- **Outcome:** `{r['category']}`: {OUTCOME.get(r['category'], '')}",
              f"- **Score:** {r['score']}"]
    md_path.write_text("\n".join(L) + "\n")
    return md_path
