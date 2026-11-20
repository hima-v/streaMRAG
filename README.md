# streaMRAG

NLI-guided, temporally grounded memory updates for unbounded event QA, with a
Hyperagent-style policy-improvement loop. See `codebase_plan.md` for the design and
`streamrag_pipeline.png` for the architecture.

## Setup

```bash
bash scripts/setup_env.sh          # .venv: torch 2.7.1+cu126, transformers 4.53.x, mamba-ssm 2.2.5
source .venv/bin/activate
```

The prebuilt mamba-ssm / causal-conv1d wheels are why torch is pinned to 2.7.1+cu126; changing it
means building those from source. Reference hardware for the timings in `codebase_plan.md` is one
24 GB GPU (RTX 3090).

Not in git (see `.gitignore`): `.venv/`, `data/raw/`, `data/processed/`, `outputs/`, `third_party/`, `.env`.
Each person creates the env and downloads data with the commands below. Model weights go to the
Hugging Face cache (`~/.cache/huggingface`); set `HF_TOKEN` in `.env` if a repo is gated.
Data/output locations can be moved with `STREAMRAG_DATA` / `STREAMRAG_OUTPUTS`.

## Models (`configs/models.yaml`)

| name | role | notes |
|---|---|---|
| `nemotron-12b-vl` | captioner, QA reader, meta agent | 8-bit bitsandbytes (BF16 does not fit 24 GB) |
| `qwen2-vl-7b`, `qwen2-vl-2b` | alternative captioners / baselines | BF16 |
| `claims-qwen3-4b` | atomic claim extraction | BF16 |
| `nli-deberta-large` | NLI relation classifier | swappable for the NLI ablation |
| `embed-bge-small` | candidate retrieval | |

```python
from streamrag.models import load_model
vlm = load_model("qwen2-vl-7b")
vlm.generate("Describe the scene.", images=[img])        # image(s)
vlm.generate("What happens?", frames=list_of_pil_frames)  # video = sampled frames
vlm.generate("Plain text prompt")                         # text only
```

Smoke test (writes `outputs/smoke/models.json`):

```bash
python scripts/smoke_models.py                    # all models
python scripts/smoke_models.py --models qwen2-vl-2b nli-deberta-large
```

## Data (`configs/data.yaml`, files under `data/raw/`)

| dataset | what | download |
|---|---|---|
| `disastervqa` | 1,395 disaster images, 4,405 QA → 178 pseudo-streams of 8 images | `python scripts/download_data.py disastervqa` (558 MB, md5-checked) |
| `videomme` | 100 seeded long videos (30–60 min), 3 MC questions each, subtitles | `... videomme --max-chunks 1` (one 5 GB chunk) or `... videomme` (until all 100 found; ≤101 GB transferred, only selected videos kept) |
| `m3bench` | M3-Bench-Robot: 100 robot videos, 1,276 open QA with ask-timestamps, dialogue subtitles | `... m3bench --n-videos 3` or `--n-videos all` (125.7 GB) |
| `mindcube` | MindCube-Tiny: 1,050 MC spatial questions over 408 photo sets | `... mindcube` (644 MB) |

Every dataset is converted to `Stream(observations=[Observation...], qa=[QAItem...])`
(`src/streamrag/types.py`). Video observations are frame references decoded on demand.

```bash
python -m streamrag.data.view disastervqa --n 2      # timeline + QA, contact sheet -> outputs/viz/
python -m streamrag.data.view m3bench --stream m3r-bedroom_01
```

or `notebooks/02_explore_data.ipynb`.

## Layout

```
configs/            models.yaml, data.yaml, policy/default/ (editable policy package)
src/streamrag/
  models/           VLM / LM / NLI / embedder wrappers + registry
  data/             dataset loaders, viewer
  video/            frame sampling, contact sheets
  perception/       caption cache (stub)
  memory/           Phase 1: claims, retrieval, temporal NLI, update, store, consolidation (stubs)
  qa/               Phase 2: evidence chain + answer/abstain (stub)
  baselines/        FIFO, latest-per-key, periodic summary, similarity merge, ACC-RAG-lite (stub)
  meta/             Phase 3: policy package + patch validation, archive + parent selection, meta agent/loop (stubs)
  eval/             metrics, bootstrap CIs
scripts/            setup_env.sh, download_data.py, smoke_models.py, cache_captions.py
```

## Meta agent constraints

The meta agent is a single text-only LLM call with no tools (no bash, no file access).
It returns a JSON patch that `streamrag.meta.policy.apply_patch` validates: only values of
existing keys in `policy.yaml` / `meta.yaml` (type- and range-checked), the four prompt
files, and `notes.md` can change. The memory budget is frozen. Python code is never edited.

## Licenses of external material

DisasterVQA CC BY-SA 4.0 · M3-Bench CC BY-NC-SA 4.0 · MindCube MIT · Video-MME (see dataset card) ·
HyperAgents code CC BY-NC-SA 4.0 (ideas reimplemented, not vendored) · Nemotron: NVIDIA Open Model License · Qwen: Apache-2.0.
