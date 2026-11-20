"""Phase 3 loop (offline, dev split only) — STUB.

for it in range(n_iters):
    parent = archive.select_parent("score_child_prop")
    patch  = meta_agent.propose(parent.policy, archive.lineage(parent), parent.traces)
    child, n = apply_patch(parent.policy, patch)        # reject -> record invalid, continue
    staged = evaluate(child, dev_streams[:10])           # staged eval
    full   = evaluate(child, dev_streams) if staged >= parent.staged - eps else None
    archive.add(GenRecord(...))
best = archive.best(); evaluate(best, test_streams)      # once

Ablations: --frozen-meta (meta.txt/meta.yaml edits rejected = "w/o self-improve"),
--parent latest (= "w/o archive"), --no-meta (default policy only).
Transfer (imp@k): load a meta package from run A, freeze it, run k iterations on domain B,
report test(best) - test(initial).
"""
from __future__ import annotations


def run_loop(*args, **kwargs):
    raise NotImplementedError
