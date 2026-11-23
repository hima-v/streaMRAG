"""Rescore an archive with the current evaluator (src/streamrag/eval/judge.py, EVALUATOR_VERSION).

  python scripts/rescore_archive.py --dataset disastervqa --archive qwen_run1

Reuses each node's saved memory snapshots and answers, so only the evaluator runs (Qwen2-VL-7B for
evidence checks and open answers); no memory or answering passes. For every scored node it rewrites
runs/<stream>/{judgments,scores}.json, evaluation.md, the node's scores.json, meta_log.md and report.md,
and the archive's archive.json and summary.md (node scores updated). The previous files are kept once as *_v1.* (never
overwritten by later rescoring). <archive>/rescore.md compares old and new scores.

Rescoring corrects the scores but not the archive's history: parents were chosen with the old scores,
and children were proposed from the old meta logs.
"""
from __future__ import annotations

import argparse
import collections
import json
import shutil
import time
from pathlib import Path

from streamrag.quiet import quiet

quiet()

from run_experiment import Progress, eval_streams, write_report, write_summary  # noqa: E402
from streamrag.config import load_yaml  # noqa: E402
from streamrag.eval.judge import (EVALUATOR_VERSION, Evaluator, build_meta_log, combine,  # noqa: E402
                                  evaluate, summarize)
from streamrag.eval.reports import write_stream_eval_md  # noqa: E402
from streamrag.meta.archive import Archive  # noqa: E402
from streamrag.models import load_model  # noqa: E402
from streamrag.records import read_records, write_json  # noqa: E402


def keep_v1(path: Path) -> None:
    """Copy path -> <stem>_v1<suffix> once."""
    old = path.with_name(f"{path.stem}_v1{path.suffix}")
    if path.exists() and not old.exists():
        shutil.copy2(path, old)


def v1(path: Path) -> Path:
    return path.with_name(f"{path.stem}_v1{path.suffix}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", required=True)
    ap.add_argument("--archive", required=True)
    ap.add_argument("--force", action="store_true", help="also rescore nodes already at the current version")
    a = ap.parse_args()

    arch = Archive(a.dataset, a.archive)
    if not arch.nodes:
        raise SystemExit(f"archive {arch.dir} is empty")
    cfg = load_yaml("eval")
    progress = Progress(f"rescore {a.archive}", 0)
    old_scores = {n.node_id: dict(n.scores) for n in arch.nodes.values() if n.scores}
    old_best = arch.select_parent("best").node_id
    todo = sorted((n for n in arch.nodes.values() if n.scores and
                   (a.force or n.scores.get("evaluator_version", 1) != EVALUATOR_VERSION)), key=lambda n: n.node_id)
    if not todo:
        print(f"all nodes are already scored with evaluator version {EVALUATOR_VERSION} (use --force to redo)")
        return
    keep_v1(arch.path)
    keep_v1(arch.dir / "summary.md")
    ev_name = arch.nodes[0].models.get("evaluator") or cfg["roles"]["evaluator"]
    progress(f"{len(todo)} nodes to rescore with evaluator version {EVALUATOR_VERSION}; loading {ev_name}")
    ev = Evaluator(load_model(ev_name), ev_name)
    t0 = time.time()
    changes = []                                         # (node, stream, qa, old category/score, new)
    for node in todo:
        progress.node = node.node_id
        d = arch.node_dir(node.node_id)
        per_stream, results = {}, []
        for seg in eval_streams(node):
            run_dir = d / "runs" / seg["stream_id"]
            progress.stream = seg["stream_id"]
            snaps = read_records(run_dir / "snapshots.json")
            answers = read_records(run_dir / "answers.json")
            mem_logs = read_records(run_dir / "memory_log")
            for f in ("judgments.json", "scores.json", "evaluation.md"):
                keep_v1(run_dir / f)
            old_rows = {r["qa_id"]: r for r in read_records(v1(run_dir / "judgments.json"))}
            rows = evaluate(seg, snaps, answers, ev, run_dir / "judgments.json", progress)
            sc = summarize(seg, rows, mem_logs, snaps)
            write_json(run_dir / "scores.json", sc)
            write_stream_eval_md(run_dir, seg, snaps[-1], answers, rows, sc, node.node_id, node.budget)
            for r in rows:
                o = old_rows.get(r["qa_id"], {})
                if (o.get("category"), o.get("score")) != (r["category"], r["score"]):
                    changes.append((node.node_id, seg["stream_id"], r["qa_id"], o.get("category"), o.get("score"),
                                    r["category"], r["score"]))
            per_stream[seg["stream_id"]] = sc
            log = build_meta_log(seg, rows, snaps, mem_logs, sc, node.budget, cfg["meta_agent"]["max_failure_cases"])
            results.append((seg, rows, sc, log, snaps))
        progress.stream = None
        scores = combine(per_stream)
        for f in ("scores.json", "meta_log.md", "report.md"):
            keep_v1(d / f)
        node.scores = scores
        arch.save(node)
        write_json(d / "scores.json", scores)
        header = (f"NODE SCORE: {scores['esqa_mean']} = mean over {len(results)} evidence stream(s): "
                  + ", ".join(f"{sid} {s['esqa_mean']}" for sid, s in per_stream.items()) + "\n")
        (d / "meta_log.md").write_text(header + "\n\n".join(r[3] for r in results) + "\n")
        write_report(arch, node, results)
        progress(f"node {node.node_id}: {old_scores[node.node_id]['esqa_mean']} -> {scores['esqa_mean']}"
                 + (f" ({scores['evaluator_errors']} evaluator errors)" if scores["evaluator_errors"] else ""))
    write_summary(arch)
    new_best = arch.select_parent("best").node_id
    write_rescore_md(arch, old_scores, changes, old_best, new_best, ev.n_calls, time.time() - t0)
    progress.node = None
    progress(f"done in {(time.time() - t0) / 60:.1f} min; best node {old_best} -> {new_best}; "
             f"{len(changes)} question outcomes changed | {arch.dir / 'rescore.md'}")


def write_rescore_md(arch: Archive, old: dict, changes: list, old_best: int, new_best: int,
                     n_calls: int, secs: float) -> None:
    nodes = sorted(arch.nodes.values(), key=lambda n: n.node_id)
    cat_moves = collections.Counter((c[3], c[5]) for c in changes)
    L = [f"# Rescore of archive `{arch.dir.name}` with evaluator version {EVALUATOR_VERSION}", "",
         f"{len(old)} nodes · {len(changes)} question outcomes changed · {n_calls} evaluator calls · "
         f"{secs / 60:.1f} min", "",
         f"**Best node: {old_best} (old) → {new_best} (new).** Parents in this archive were chosen with the old "
         f"scores, so its history is unchanged; only the scores are corrected.", "",
         "Previous files are kept as `*_v1.*` next to the new ones.", "",
         "## Node scores", "",
         "| node | parent | old score | new score | change | old correct | new correct | evaluator errors |",
         "|---|---|---|---|---|---|---|---|"]
    for n in nodes:
        o, s = old.get(n.node_id) or {}, n.scores or {}
        diff = (s.get("esqa_mean") or 0) - (o.get("esqa_mean") or 0)
        L.append(f"| {n.node_id} | {'—' if n.parent_id is None else n.parent_id} | {o.get('esqa_mean')} | "
                 f"{s.get('esqa_mean')} | {diff:+.2f} | {o.get('correct_count')} | {s.get('correct_count')} | "
                 f"{s.get('evaluator_errors', 0)} |")
    L += ["", "## Outcome changes (old → new, all nodes)", "", "| old outcome | new outcome | questions |", "|---|---|---|"]
    L += [f"| `{a}` | `{b}` | {k} |" for (a, b), k in cat_moves.most_common()]
    if not cat_moves:
        L.append("| — | — | 0 |")
    L += ["", "## Changed questions", "", "| node | stream | question | old | new |", "|---|---|---|---|---|"]
    L += [f"| {n} | `{sid}` | {qa} | `{oc}` {os_} | `{nc}` {ns} |" for n, sid, qa, oc, os_, nc, ns in changes]
    (arch.dir / "rescore.md").write_text("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
