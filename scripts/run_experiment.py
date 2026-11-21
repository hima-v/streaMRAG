"""Run the self-improving memory-agent experiment (codebase_plan.md §11).

Each dataset has its own setups file, configs/experiments/<dataset>.yaml, with named experiments
(short5, long5, ...); --dataset picks the file and --experiment the setup.

  # build the stream pools once
  python scripts/build_streams.py disastervqa --length 10      # 70 short streams (5 questions each)
  python scripts/build_streams.py disastervqa --length 20      # 34 long streams (10 questions each)

  # new archive from the minimal seeds: 3 iterations -> 3 scored nodes, each on the same 5 short streams
  python scripts/run_experiment.py --dataset disastervqa --experiment short5 --archive run3

  # continue it (settings and streams are read from the archive)
  python scripts/run_experiment.py --dataset disastervqa --archive run3 --iterations 5

One iteration adds and scores exactly one node:
  - empty archive: create the root node from the profile's seeds (default profile: minimal)
  - otherwise:     parent = best-scoring node; the meta agent (Nemotron, following the parent's
                   meta harness) reads ONLY the parent's strategy, harness and evaluation log and
                   writes a new meta harness H', then, following H', a new memory strategy S' from
                   the parent's strategy -> child node (S', H'). Sampling is seeded by the child's id.
  - score the node on the archive's evaluation streams (the same streams for every node):
      memory pass  (Nemotron + strategy; never sees the questions)  for each stream, from empty memory
      answer pass  (Qwen2-VL-7B, fixed prompt)       only after the LAST item of each stream
      evaluation   (Qwen2-VL-7B + deterministic rules) -> stream score; node score = mean over streams
"""
from __future__ import annotations

import argparse
import datetime as dt
import time
from pathlib import Path

import yaml

from streamrag.quiet import quiet

quiet()                                   # silence library logging before any model code is imported

from streamrag.config import CONFIG_DIR, load_yaml  # noqa: E402
from streamrag.data.streams import list_streams, load_stream, segment_stream, select_streams, stream_dir  # noqa: E402
from streamrag.eval.judge import (Evaluator, answer_text_of, build_meta_log, combine,  # noqa: E402
                                  evaluate, summarize)
from streamrag.memory.agent import run_memory_pass  # noqa: E402
from streamrag.meta.archive import Archive, Node, text_id  # noqa: E402
from streamrag.meta.meta_agent import MetaAgent  # noqa: E402
from streamrag.models import load_model, unload  # noqa: E402
from streamrag.qa.answering import run_answer_pass  # noqa: E402
from streamrag.records import read_records, write_json  # noqa: E402
from streamrag.eval.reports import write_stream_eval_md, write_streams_md  # noqa: E402


class Progress:
    """One line per event: <timestamp> [run | iteration i/n | node k | stream s] +elapsed message."""

    def __init__(self, run: str, n_iter: int):
        self.run, self.n_iter, self.it, self.node, self.stream = run, n_iter, 0, None, None
        self.t0 = time.time()

    def __call__(self, msg: str) -> None:
        parts = [self.run] + ([f"iteration {self.it}/{self.n_iter}"] if self.it else [])
        if self.node is not None:
            parts.append(f"node {self.node}")
        if self.stream:
            parts.append(f"stream {self.stream}")
        m, sec = divmod(int(time.time() - self.t0), 60)
        now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{now} [{' | '.join(parts)}] +{m:02d}:{sec:02d}  {msg}", flush=True)


def profile_files(profile: str, dataset: str) -> dict:
    return {k: v.format(dataset=dataset) for k, v in load_yaml("eval")["profiles"][profile].items()}


def read_cfg(rel: str) -> str:
    return (CONFIG_DIR / rel).read_text()


def prompt_versions(profile: str, dataset: str) -> dict:
    pf = profile_files(profile, dataset)
    files = [pf["memory_frame"], pf["harness_frame"], pf["strategy_frame"],
             "answering/prompt.txt", "judge/answer.txt", "judge/evidence.txt"]
    return {f: text_id(read_cfg(f)) for f in files}


def eval_streams(node: Node) -> list[dict]:
    if node.eval_streams:                               # experiment-config archives: fixed list of stream ids
        d = stream_dir(node.dataset, node.eval_stream)
        return [load_stream(d / f"{sid}.json") for sid in node.eval_streams]
    for p in list_streams(node.dataset, "dev"):         # older archives: one base stream, split into segments
        s = load_stream(p)
        if s["stream_id"] == node.eval_stream:
            return segment_stream(s, node.stream_length)
    raise SystemExit(f"stream {node.eval_stream} not found; run: python scripts/build_streams.py {node.dataset} --split dev")


# ----------------------------------------------------------------------------- steps
def create_root(arch: Archive, setup: dict, roles: dict, progress: Progress) -> Node:
    pool = f"len{setup['stream_length']}"
    pool_streams = [load_stream(p) for p in list_streams(setup["dataset"], pool)]
    if not pool_streams:
        raise SystemExit(f"no {pool} streams; run: python scripts/build_streams.py {setup['dataset']} "
                         f"--length {setup['stream_length']}")
    chosen = select_streams(pool_streams, setup["n_streams"], setup["stream_selection"],
                            setup["selection_seed"], setup.get("streams"))
    pf = profile_files(setup["profile"], setup["dataset"])
    S, H = read_cfg(pf["seed_strategy"]), read_cfg(pf["seed_harness"])
    node = Node(0, None, setup["dataset"], pool, setup["budget"], text_id(S), text_id(H),
                {"memory_strategy": setup["memory_strategy"], "meta_harness": setup["meta_harness"]},
                {"kind": "seed", "strategy": f"configs/{pf['seed_strategy']}", "harness": f"configs/{pf['seed_harness']}"},
                models={**roles, "profile": setup["profile"], "prompts": prompt_versions(setup["profile"], setup["dataset"]),
                        "experiment": setup},
                stream_length=setup["stream_length"], eval_streams=[c["stream_id"] for c in chosen])
    arch.save(node, S, H)
    md = write_streams_md(arch.dir, chosen, setup)
    progress.node = 0
    progress(f"created root node 0 from the {setup['profile']} seeds | experiment {setup['experiment']}: "
             f"{len(chosen)} streams of {setup['stream_length']} photos "
             f"({sum(len(c['questions']) for c in chosen)} questions), budget {setup['budget']} tokens | {md.name}")
    return node


def propose_child(arch: Archive, parent: Node, roles: dict, nemotron, progress: Progress) -> Node:
    root = arch.nodes[0]
    profile = root.models.get("profile", "minimal")
    pf = profile_files(profile, parent.dataset)
    S, H = arch.strategy(parent.node_id), arch.harness(parent.node_id)
    log = (arch.node_dir(parent.node_id) / "meta_log.md").read_text()   # direct parent only
    meta = MetaAgent(nemotron, parent.dataset, read_cfg(pf["harness_frame"]), read_cfg(pf["strategy_frame"]))
    sw = root.switches
    child_id = arch.new_id()
    progress.node, progress.stream = child_id, None
    progress(f"parent = node {parent.node_id} (best score {parent.scores['esqa_mean']})")
    siblings = {(k.strategy_id, k.harness_id) for k in arch.children(parent.node_id)}
    for attempt in range(load_yaml("eval")["meta_agent"]["max_resample"] + 1):
        seed = 1000 * child_id + attempt
        if sw["meta_harness"] == "dynamic":
            progress("meta agent: writing the new meta harness")
        h = meta.update_harness(H, S, log, seed) if sw["meta_harness"] == "dynamic" else \
            {"text": H, "rationale": "(meta harness fixed)", "parsed": True, "raw": ""}
        if sw["memory_strategy"] == "dynamic":
            progress("meta agent: writing the new memory strategy (following the new harness)")
        s = meta.update_strategy(h["text"], S, log, parent.budget, seed + 1) if sw["memory_strategy"] == "dynamic" else \
            {"text": S, "rationale": "(memory strategy fixed)", "changes": [], "parsed": True, "raw": ""}
        fixed_both = sw["meta_harness"] == "fixed" and sw["memory_strategy"] == "fixed"
        if fixed_both or (text_id(s["text"]), text_id(h["text"])) not in siblings:
            break
        progress(f"child duplicates a sibling; re-sampling (attempt {attempt + 1})")
    child = Node(child_id, parent.node_id, parent.dataset, parent.eval_stream, parent.budget,
                 text_id(s["text"]), text_id(h["text"]), sw,
                 {"kind": "meta", "harness_rationale": h.get("rationale"), "strategy_rationale": s.get("rationale"),
                  "changes": s.get("changes"), "harness_parsed": h.get("parsed"), "strategy_parsed": s.get("parsed"),
                  "meta_seed": seed},
                 models={**roles, "profile": profile, "prompts": prompt_versions(profile, parent.dataset),
                         "experiment": root.models.get("experiment")},
                 stream_length=parent.stream_length, eval_streams=list(parent.eval_streams))
    arch.save(child, s["text"], h["text"])
    d = arch.node_dir(child.node_id)
    (d / "meta_raw_harness.txt").write_text(h.get("raw", ""))
    (d / "meta_raw_strategy.txt").write_text(s.get("raw", ""))
    progress(f"created child node {child.node_id} (harness {child.harness_id}, strategy {child.strategy_id})")
    return child


def memory_passes(arch: Archive, node: Node, nemotron, progress: Progress) -> list[tuple]:
    pf = profile_files(arch.nodes[0].models.get("profile", "minimal"), node.dataset)
    out = []
    for seg in eval_streams(node):
        run_dir = arch.node_dir(node.node_id) / "runs" / seg["stream_id"]
        progress.node, progress.stream = node.node_id, seg["stream_id"]
        progress(f"memory pass: {seg['n_steps']} evidence items ({seg['items'][0]['item_id']}-"
                 f"{seg['items'][-1]['item_id']}), starting from empty memory")
        snaps = run_memory_pass(nemotron, arch.strategy(node.node_id), seg, node.budget, run_dir,
                                read_cfg(pf["memory_frame"]), progress)
        out.append((seg, run_dir, snaps))
    return out


def answer_and_evaluate(arch: Archive, node: Node, roles: dict, runs: list[tuple], cfg, progress: Progress):
    progress.stream = None
    progress(f"loading answering agent + evaluator ({roles['answering_agent']})")
    qwen = load_model(roles["answering_agent"])
    ev = Evaluator(load_model(roles["evaluator"]), roles["evaluator"])
    per_stream, results = {}, []
    for seg, run_dir, snaps in runs:
        progress.stream = seg["stream_id"]
        progress(f"answer pass: {len(seg['questions'])} questions asked after the last item ({seg['items'][-1]['item_id']})")
        answers = run_answer_pass(qwen, seg, [snaps[-1]], run_dir / "answers.json", lambda m: None)
        rows = evaluate(seg, snaps, answers, ev, run_dir / "judgments.json", progress)
        mem_logs = read_records(run_dir / "memory_log")
        sc = summarize(seg, rows, mem_logs, snaps)
        write_json(run_dir / "scores.json", sc)
        write_stream_eval_md(run_dir, seg, snaps[-1], answers, rows, sc, node.node_id, node.budget)
        per_stream[seg["stream_id"]] = sc
        log = build_meta_log(seg, rows, snaps, mem_logs, sc, node.budget, cfg["meta_agent"]["max_failure_cases"])
        results.append((seg, rows, sc, log, snaps))
    scores = combine(per_stream)
    node.scores = scores
    arch.save(node)
    d = arch.node_dir(node.node_id)
    write_json(d / "scores.json", scores)
    header = (f"NODE SCORE: {scores['esqa_mean']} = mean over {len(results)} evidence stream(s): "
              + ", ".join(f"{sid} {s['esqa_mean']}" for sid, s in per_stream.items()) + "\n")
    (d / "meta_log.md").write_text(header + "\n\n".join(r[3] for r in results) + "\n")
    write_report(arch, node, results)
    progress.stream = None
    progress(f"DONE node {node.node_id}: score {scores['esqa_mean']} ("
             + ", ".join(f"{sid.rsplit('-', 1)[-1]} {s['esqa_mean']}" for sid, s in per_stream.items())
             + f") | correct {scores['correct_count']} | evidence retained {scores['retention_final']}")
    return scores


# ----------------------------------------------------------------------------- reports
def write_report(arch: Archive, node: Node, results: list[tuple]) -> None:
    sc, cb = node.scores, node.created_by
    md = [f"# Node {node.node_id}" + (f" (child of node {node.parent_id})" if node.parent_id is not None else " (root)"),
          "", f"Archive `{arch.dir.name}` · dataset `{node.dataset}` · base stream `{node.eval_stream}` · "
          f"{len(results)} evidence stream(s) of {results[0][0]['n_steps']} items · budget {node.budget} tokens · "
          f"profile `{node.models.get('profile')}` · switches {node.switches}",
          "", "Questions are asked only after the last item of each stream; the memory agent never sees them.", ""]
    if cb.get("kind") == "meta":
        md += ["## How this node was created", "",
               f"The meta agent took parent node {node.parent_id}'s strategy, meta harness and evaluation log "
               f"(`node_{node.parent_id:04d}/meta_log.md`), wrote the new meta harness below, then followed it to "
               f"write the new memory strategy.", "",
               f"- Harness rationale: {cb.get('harness_rationale') or '(none given)'}",
               f"- Strategy rationale: {cb.get('strategy_rationale') or '(none given)'}",
               *[f"- Change: {c}" for c in (cb.get("changes") or [])], ""]
    else:
        md += [f"Root node: seed strategy `{cb.get('strategy')}`, seed meta harness `{cb.get('harness')}`.", ""]
    md += [f"## Memory strategy (`{node.strategy_id}`)", "", "```", arch.strategy(node.node_id).strip(), "```", "",
           f"## Meta harness (`{node.harness_id}`)", "", "```", arch.harness(node.node_id).strip(), "```", "",
           "## Score", "", f"**Node score (mean over streams): {sc['esqa_mean']}** · correct {sc['correct_count']} · "
           f"evidence retained {sc['retention_final']} · abstained {sc['abstained']} · budget fallbacks {sc['budget_fallbacks']}",
           "", "| stream | items | score | correct | evidence retained | final memory |", "|---|---|---|---|---|---|"]
    for seg, rows, s, log, snaps in results:
        md.append(f"| `{seg['stream_id']}` | {seg['items'][0]['item_id']}-{seg['items'][-1]['item_id']} | "
                  f"{s['esqa_mean']} | {s['correct_count']} | {s['retention_final']} | "
                  f"{s['final_memory_lines']} lines, {s['final_memory_tokens']} tok |")
    for seg, rows, s, log, snaps in results:
        qs = {q["qa_id"]: q for q in seg["questions"]}
        md += ["", f"## Stream `{seg['stream_id']}` ([evaluation.md](runs/{seg['stream_id']}/evaluation.md))", "",
               "| item | question | gold | answer | outcome | evidence in memory |", "|---|---|---|---|---|---|"]
        for r in rows:
            q = qs[r["qa_id"]]
            ans = "NOT_ENOUGH_EVIDENCE" if r["abstained"] else answer_text_of(q, r["pred"])
            md.append(f"| {q['evidence_scope'][0]} | {q['original'].replace('|', '/')} | "
                      f"{answer_text_of(q, q['gold']).replace('|', '/')} | {str(ans).replace('|', '/')} | "
                      f"`{r['category']}` | {'yes' if r['retained'] else 'no'} |")
        md += ["", "Final memory:", "", "```"] + \
              [f"{l['id']} [src {', '.join(l['sources'])}] {l['text']}" for l in snaps[-1]["lines"]] + ["```"]
    md += ["", "## Evaluation log (fed to the meta agent if this node is chosen as a parent)", "", "```",
           (arch.node_dir(node.node_id) / "meta_log.md").read_text().strip(), "```"]
    (arch.node_dir(node.node_id) / "report.md").write_text("\n".join(md) + "\n")


def write_summary(arch: Archive) -> None:
    md = [f"# Archive `{arch.dir.name}`", "", "| node | parent | score | per stream | correct | strategy | harness |",
          "|---|---|---|---|---|---|---|"]
    for n in sorted(arch.nodes.values(), key=lambda n: n.node_id):
        s = n.scores or {}
        per = ", ".join(f"{v['esqa_mean']}" for v in (s.get("streams") or {}).values())
        md.append(f"| [{n.node_id}](node_{n.node_id:04d}/report.md) | {'—' if n.parent_id is None else n.parent_id} | "
                  f"{s.get('esqa_mean', 'not scored')} | {per} | {s.get('correct_count', '')} | "
                  f"`{n.strategy_id}` | `{n.harness_id}` |")
    (arch.dir / "summary.md").write_text("\n".join(md) + "\n")


# ----------------------------------------------------------------------------- main
OVERRIDABLE = ["profile", "budget", "memory_strategy", "meta_harness", "parent_selection", "stream_length",
               "n_streams", "stream_selection", "selection_seed"]


def load_setup(a) -> dict:
    path = Path(a.config) if a.config else Path(CONFIG_DIR) / "experiments" / f"{a.dataset}.yaml"
    if not path.exists():
        raise SystemExit(f"no experiment config for dataset '{a.dataset}': expected {path} "
                         f"(copy configs/experiments/disastervqa.yaml and adapt it; the dataset also needs a "
                         f"stream builder in streamrag.data.streams)")
    a.config = str(path)
    cfg = yaml.safe_load(path.read_text())
    if cfg.get("dataset") != a.dataset:
        raise SystemExit(f"{path} is for dataset '{cfg.get('dataset')}', not '{a.dataset}'")
    name = a.experiment or cfg["default_experiment"]
    if name not in cfg["experiments"]:
        raise SystemExit(f"unknown experiment '{name}'; choose from {sorted(cfg['experiments'])}")
    setup = {**cfg.get("defaults", {}), **cfg["experiments"][name], "experiment": name, "dataset": cfg["dataset"],
             "config": str(a.config)}
    for k in OVERRIDABLE:
        if getattr(a, k) is not None:
            setup[k] = getattr(a, k)
    if a.iterations is not None:
        setup["iterations"] = a.iterations
    return setup


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dataset", required=True, help="dataset / domain, e.g. disastervqa")
    ap.add_argument("--config", help="experiment config file (default: configs/experiments/<dataset>.yaml)")
    ap.add_argument("--experiment", help="experiment name in the dataset's config, e.g. short5 (default: its default_experiment)")
    ap.add_argument("--archive", required=True, help="archive name (outputs/archive/<dataset>/<archive>)")
    ap.add_argument("--iterations", type=int, help="nodes to add and score in this run (default: from config)")
    g = ap.add_argument_group("overrides (only used when the archive is new, except parent_selection)")
    g.add_argument("--profile")
    g.add_argument("--budget", type=int)
    g.add_argument("--memory-strategy", choices=["fixed", "dynamic"])
    g.add_argument("--meta-harness", choices=["fixed", "dynamic"])
    g.add_argument("--parent-selection", choices=["best", "score_child_prop"])
    g.add_argument("--stream-length", type=int, choices=[10, 20])
    g.add_argument("--n-streams")
    g.add_argument("--stream-selection", choices=["stratified", "random", "list"])
    g.add_argument("--selection-seed", type=int)
    a = ap.parse_args()
    setup = load_setup(a)
    roles = load_yaml("eval")["roles"]
    cfg = load_yaml("eval")
    arch = Archive(a.dataset, a.archive)
    progress = Progress(a.archive, setup["iterations"])
    if arch.nodes:
        r = arch.nodes[0]
        stored = r.models.get("experiment") or {}
        parent_sel = a.parent_selection or stored.get("parent_selection", "best")
        progress(f"continuing archive with {len(arch.nodes)} nodes (experiment {stored.get('experiment', '?')}, "
                 f"{len(r.eval_streams) or 'segmented'} streams of {r.stream_length or 'whole'} photos, budget "
                 f"{r.budget}, switches {r.switches}); stored settings are used")
        if r.eval_streams and not (arch.dir / "evaluation_streams.md").exists():
            write_streams_md(arch.dir, eval_streams(r), stored)
    else:
        parent_sel = setup["parent_selection"]
        progress(f"new archive at {arch.dir} (experiment {setup['experiment']} from {setup['config']})")

    for it in range(1, setup["iterations"] + 1):
        progress.it, progress.node, progress.stream = it, None, None
        progress(f"loading memory/meta agent ({roles['memory_agent']})")
        nemotron = load_model(roles["memory_agent"])          # memory agent and meta agent: same model
        unscored = sorted((n for n in arch.nodes.values() if n.scores is None), key=lambda n: n.node_id)
        if not arch.nodes:
            node = create_root(arch, setup, roles, progress)
        elif unscored:
            node = unscored[0]
            progress.node = node.node_id
            progress(f"resuming previously unscored node {node.node_id}")
        else:
            parent = arch.select_parent(parent_sel)
            node = propose_child(arch, parent, roles, nemotron, progress)
        runs = memory_passes(arch, node, nemotron, progress)
        del nemotron
        unload()
        answer_and_evaluate(arch, node, roles, runs, cfg, progress)
        unload()
        write_summary(arch)
        best = arch.select_parent("best")
        progress.node, progress.stream = None, None
        progress(f"best so far: node {best.node_id} with score {best.scores['esqa_mean']} "
                 f"({len(arch.nodes)} nodes in the archive)")
    print(f"\narchive: {arch.dir}\n  evaluation_streams.md, summary.md, node_XXXX/report.md, "
          f"node_XXXX/runs/<stream>/evaluation.md\n  plots: python scripts/visualize_run.py "
          f"--dataset {setup['dataset']} --archive {a.archive}")


if __name__ == "__main__":
    main()
