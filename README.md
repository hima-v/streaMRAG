# streaMRAG

A self-improving memory agent for evidence streams. A vision-language memory agent reads a stream of
timestamped photos one at a time and keeps a small, token-limited memory under a plain-text **memory
strategy**. After the last photo, a fixed answering agent answers questions from that memory alone. A
Hyperagents-style **meta agent** reads how a strategy did, rewrites its own instructions (the **meta
harness**) and then proposes a better strategy. See `codebase_plan.md` (§11) for the design.

## Replicating the main experiment

One 24 GB GPU (reference: RTX 3090), Linux, CUDA 12.x driver, Python ≥ 3.12.

```bash
# 1. environment (.venv with torch 2.7.1+cu126, transformers 4.53.x, mamba-ssm 2.2.5)
bash scripts/setup_env.sh
source .venv/bin/activate

# 2. data: DisasterVQA (543 MB, md5-checked) -> data/raw/disastervqa/
python scripts/download_data.py disastervqa

# 3. evidence streams: 70 short streams (10 photos, 5 questions each) -> data/processed/streams/v2/disastervqa/len10/
python scripts/build_streams.py disastervqa --length 10

# 4. the experiment: 5 iterations -> 5 scored nodes in outputs/archive/disastervqa/run1/
python scripts/run_experiment.py --dataset disastervqa --archive run1 --iterations 5

# 5. plots: best_score.png and archive_tree.png in the archive folder
python scripts/visualize_run.py --dataset disastervqa --archive run1
```

The first run downloads about 40 GB of model weights to the Hugging Face cache (`~/.cache/huggingface`).
Each iteration takes about 20 minutes on an RTX 3090, so 5 iterations take about 1.5–2 hours.

**What the command runs.** With no `--experiment`, the dataset's default experiment `short5` from
`configs/experiments/disastervqa.yaml` is used:

| setting | value |
|---|---|
| evaluation streams | 5 short streams (10 photos, 5 questions each = 25 questions per node), chosen round-robin over disaster types with seed 0: `dvqa-hurricane-len10-010`, `dvqa-flood-len10-024`, `dvqa-earthquake-len10-054`, `dvqa-wildfire-len10-064`, `dvqa-fire-len10-066` |
| starting node | minimal seeds: strategy "Update the memory with the new item.", meta harness "Improve the memory strategy." |
| memory budget | 512 tokens |
| strategy / harness | both dynamic (the meta agent may change both) |
| parent selection | best-scoring node (ties go to the newest) |

- **Iteration 1** creates node 0 from the minimal seeds and scores it.
- **Each later iteration** picks the best-scoring node as parent. The meta agent reads only that parent's
  strategy, meta harness and evaluation log. It writes a new meta harness, then a new strategy following
  it. The child is scored on the same 5 streams. Sampling is seeded by the child's id (seed = 1000 × id +
  attempt), so a rerun proposes the same children up to GPU numerical differences.
- **Scoring a node:**
  1. For each stream, the memory agent starts from empty memory and reads the photos one at a time. It
     never sees the questions.
  2. After the last photo, the answering agent answers the stream's questions from the final memory,
     citing memory lines.
  3. The evaluator scores each answer: 1 if correct with a valid citation and supported evidence, 0.5 if
     partial or the evidence is insufficient, else 0. A citation is invalid if it names a memory line that
     does not exist. If the evaluator model's reply can't be read even after one retry, the question
     scores 0 with outcome `evaluator_error`, which is counted separately.
  4. The node score is the mean over the 5 streams.

**Continuing or restarting.**
- **Continuing:** running the same command again with the same `--archive` continues that archive. It
  reads the stored settings and streams, and `--iterations N` adds N more nodes. An interrupted node is
  recreated or resumed.
- **Fresh run:** if `outputs/archive/disastervqa/run1/` already exists, pick a new archive name.

**Choosing the evaluation streams of a new archive.**
- **Same streams as another run:** add `--streams-from run3`. The new archive uses exactly that archive's
  streams, which makes the two runs directly comparable.
- **New streams:** add `--exclude-streams-from run3` (several archive names may follow). The new archive picks
  its streams only from those the listed archives did not use.
- **Default:** with neither flag, streams are chosen round-robin over disaster types with
  `--selection-seed` (default 0). Seed 0 gives the five streams listed above.

**Checking a replication.** `evaluation_streams.md` at the archive root should list the five streams
above. The stream builder is deterministic, so every stream's `manifest.content_sha256` matches across
machines.

## Agents and models

| role | model (`configs/eval.yaml` → `configs/models.yaml`) | prompt |
|---|---|---|
| memory agent: perceives each photo, edits memory | `nemotron-12b-vl` (Nemotron-Nano-12B-v2-VL, int8, reasoning off) | `configs/memory/frame_minimal.txt` + the node's strategy |
| meta agent: writes a new harness, then a new strategy | `nemotron-12b-vl` (same model; temperature 0.7, top_p 0.95) | `configs/meta/frames/*_minimal.txt` + the node's harness |
| answering agent (fixed) | `qwen2-vl-7b` (BF16) | `configs/answering/prompt.txt` |
| evaluator (fixed) | `qwen2-vl-7b` + deterministic rules | `configs/judge/` |

- **Running both models on one GPU:** the two models never share the GPU. Nemotron runs the memory
  passes (and the meta agent), is unloaded, and then Qwen2-VL answers and evaluates.
- **Nemotron patches:** Nemotron needs a few upstream fixes, applied automatically in
  `src/streamrag/models/nemotron_vl.py` and switched in `configs/models.yaml`:
  - a working generation cache (4–9× faster, output verified identical);
  - an unquantized `lm_head`;
  - last-token-only logits, which avoids a 3.6 GiB allocation on long meta-agent prompts.

```python
from streamrag.models import load_model
vlm = load_model("qwen2-vl-7b")
vlm.generate("Describe the scene.", images=[img])        # image(s)
vlm.generate("What happens?", frames=list_of_pil_frames)  # video = sampled frames
vlm.generate("Plain text prompt")                         # text only
```

Smoke test: `python scripts/smoke_models.py` (or `--models qwen2-vl-2b nli-deberta-large`). Other entries in
`configs/models.yaml` (`qwen2-vl-2b`, `claims-qwen3-4b`, `nli-deberta-large`, `embed-bge-small`) are for
baselines and the planned NLI strategy; the main experiment does not load them.

## Other experiments

`--experiment` picks a named setup in `configs/experiments/<dataset>.yaml`. Any setting can be overridden
on the command line for a **new** archive (see `python scripts/run_experiment.py --help`).

| experiment | streams | questions per node |
|---|---|---|
| `short5` (default) | 5 short | 25 |
| `short_all` | all 70 short | 350 |
| `long5` | 5 long (20 photos) | 50 |
| `long_all` | all 34 long | 340 |
| `short5_fixed_meta` | ablation: meta harness never changes | 25 |
| `short5_fixed_strategy` | ablation: strategy never changes | 25 |
| `short5_qwen_memory` | as `short5`, but Qwen2-VL-7B is the memory agent (the meta agent stays Nemotron) | 25 |

```bash
python scripts/build_streams.py disastervqa --length 20     # needed once for the long experiments
python scripts/run_experiment.py --dataset disastervqa --experiment long5 --archive long_run1 --iterations 5

# Qwen2-VL-7B memory agent on the same 5 streams as run3, or on 5 streams run3 did not use
python scripts/run_experiment.py --dataset disastervqa --experiment short5_qwen_memory --archive qwen_run1 --iterations 5 --streams-from run3
python scripts/run_experiment.py --dataset disastervqa --experiment short5_qwen_memory --archive qwen_run2 --iterations 5 --exclude-streams-from run3
```

- **Choosing models:** an experiment may set `memory_agent`, `meta_agent`, `answering_agent` or `evaluator`
  to any model name in `configs/models.yaml`. Roles it does not set come from `configs/eval.yaml`. The roles
  are stored in the archive when it is created. When the memory agent and the meta agent differ, the loop
  loads them one after the other, so only one model is on the GPU at a time.
- **Memory budget:** memory tokens are always counted with the Nemotron tokenizer, so a 512-token budget means
  the same amount of text whichever memory agent is used.

- **Overrides:** `--budget`, `--memory-strategy fixed|dynamic`, `--meta-harness fixed|dynamic`,
  `--parent-selection best|score_child_prop`, `--stream-length 10|20`, `--n-streams N|all`,
  `--stream-selection stratified|random|list`, `--selection-seed`, `--profile minimal|default`,
  `--memory-agent <model>`, `--streams-from <archive>`, `--exclude-streams-from <archive> ...`.
- **Long meta logs:** the evaluation log the meta agent reads grows by about 1,500 tokens per stream.
  `short_all` and `long_all` would need a cap on that log before they are practical.
- **Other datasets:** the same experiment names can be defined for another dataset in
  `configs/experiments/<dataset>.yaml`, once that dataset has a stream builder. Then
  `--dataset <other> --experiment short5` runs the same setup there. This is how the planned transfer test
  will run: within DisasterVQA, all buildable streams count as dev.

## Outputs

`outputs/archive/<dataset>/<archive>/`:

```
archive.json                   all nodes: parent, scores, settings, prompt versions
evaluation_streams.md          the evaluation streams: photos, posting times, dataset facts, questions
summary.md                     one row per node: score, per-stream scores, correct answers
best_score.png, archive_tree.png    from visualize_run.py
node_XXXX/
  strategy.md, meta_harness.md   the node's memory strategy and meta harness
  report.md                      how the node was made, its scores, and the log its children will read
  meta_log.md                    the evaluation log the meta agent reads when this node is a parent
  meta_raw_harness.txt, meta_raw_strategy.txt   the meta agent's raw replies (children only)
  scores.json
  runs/<stream>/
    evaluation.md                memory at question time, then each question: gold answer, the agent's answer, citations, outcome, score
    snapshots.json               memory after every step
    memory_log.json              the memory agent's edits per step (raw output kept)
    answers.json, judgments.json, scores.json
```

The console prints one line per event:
`<date time> [archive | iteration i/n | node k | stream s] +elapsed message`.
Evaluator verdicts are cached in `outputs/judge_cache_v2.jsonl`, keyed by the prompt and the image contents.

**Evaluator versions.** Scores record `evaluator_version` (currently 2; see the docstring of
`src/streamrag/eval/judge.py` for what changed). `run_experiment.py` refuses to continue an archive scored
with an older version, because parent selection would compare inconsistent scores. Rescore it first:

```bash
python scripts/rescore_archive.py --dataset disastervqa --archive run3
```

This reuses the saved memory snapshots and answers and reruns only the evaluator, which takes minutes. Old
files are kept as `*_v1.*`, and `rescore.md` in the archive compares old and new scores. Parents already
chosen with the old scores stay as they were.

**Tests:** `python -m pytest tests -q` (fake models, no GPU, under a second).

## Data

Not in git (see `.gitignore`): `.venv/`, `data/raw/`, `data/processed/`, `outputs/`, `third_party/`, `.env`.
Set `HF_TOKEN` in `.env` if a model repository is gated. Data and output locations can be moved with
`STREAMRAG_DATA` / `STREAMRAG_OUTPUTS`.

| dataset | what | download | streams |
|---|---|---|---|
| `disastervqa` | 1,395 disaster photos, 4,405 QA | `python scripts/download_data.py disastervqa` | `build_streams.py disastervqa --length 10\|20` |
| `videomme` | 100 seeded long videos, 3 MC questions each, subtitles | `... videomme --n-videos 3` | not yet |
| `m3bench` | M3-Bench-Robot: robot videos, open QA with ask-timestamps | `... m3bench --n-videos 3` | not yet |
| `mindcube` | MindCube-Tiny: 1,050 MC spatial questions over 408 photo sets | `... mindcube` | not yet |

DisasterVQA streams (`configs/streams.yaml`, `src/streamrag/data/streams.py`):
- **Photos:** only photos with a recoverable posting time are used. The time comes from the tweet ID or the
  MEDIC file name.
- **Streams:** photos are split into non-overlapping, time-ordered windows of 10 or 20 photos from one
  disaster type, giving 70 short or 34 long streams.
- **Questions:** each stream has 5 or 10 questions, each about one photo in it, taken from the dataset's own
  QA. Pairs whose answer holds for 3 or more photos are dropped as non-distinctive.
- **Hidden facts:** the verified annotations are given only to the evaluator.

`python -m streamrag.data.view disastervqa --n 2` draws a dataset timeline and contact sheet into
`outputs/viz/`.

**Sample streams (`examples/`):** one hand-curated 20-item stream per dataset, from an earlier planning
stage (`codebase_plan.md` §9). Rebuild with `python scripts/make_sample_streams.py all`. They keep their
dataset licenses (M3-Bench is CC BY-NC-SA), so keep this repo private.

## Layout

```
configs/
  experiments/<dataset>.yaml   named experiment setups
  eval.yaml                    model roles, generation limits, seed profiles
  streams.yaml                 stream construction
  models.yaml, data.yaml
  memory/  meta/  strategies/seeds/  answering/  judge/    prompt frames, seeds and fixed prompts
scripts/
  setup_env.sh, download_data.py, build_streams.py
  run_experiment.py            the self-improving loop
  visualize_run.py             plots of an archive
  smoke_models.py, run_memory.py, score_run.py, make_sample_streams.py, cache_captions.py
src/streamrag/
  models/                      Nemotron / Qwen2-VL / text LM / NLI / embedder wrappers + registry
  data/                        dataset loaders, stream builder (streams.py), viewer
  memory/agent.py              memory pass (JSON edit ops, provenance, token budget)
  qa/answering.py              answering agent
  eval/judge.py, reports.py    evaluator, scores, meta log, Markdown reports
  meta/archive.py, meta_agent.py   archive + parent selection, meta agent
  baselines/, perception/, memory/{claims,temporal_nli,...}.py, meta/{policy,loop}.py   earlier phases / planned NLI work
```

## Meta agent constraints

- **Inputs and outputs:** the meta agent is a single text-only model call with no tools: no bash, no file
  access, no code execution. It sees only the direct parent's strategy, meta harness and evaluation log.
  It returns a new meta harness and a new strategy in tags.
- **What it can change:** only those two plain-text instructions. The memory budget, the answering and
  evaluator prompts, and all Python code are fixed.
- **Length limits:** harnesses are capped at 400 words and strategies at 250 words.
- **Duplicates:** a proposal that duplicates an existing sibling is re-sampled. The meta agent is never
  shown its siblings.

## Licenses of external material

DisasterVQA CC BY-SA 4.0 · M3-Bench CC BY-NC-SA 4.0 · MindCube MIT · Video-MME (see dataset card) ·
HyperAgents code CC BY-NC-SA 4.0 (ideas reimplemented, not vendored) · Nemotron: NVIDIA Open Model License · Qwen: Apache-2.0.
