# streaMRAG — Codebase Setup Plan

Goal of this first step: a repo skeleton for the full streaMRAG pipeline (Phases 1–3 in `streamrag_pipeline.png`), with **working code only for (a) loading and running inference on our models and (b) downloading, loading and viewing samples from our datasets**. Pipeline stages (claim extraction, temporal NLI, memory, consolidation, QA, Hyperagent loop) are created as typed stubs, so later work fills them in without moving anything.

---

## 0. Facts that drive the design

| Item | Finding | Consequence |
|---|---|---|
| Reference GPU (all timings in this doc) | NVIDIA RTX 3090, 24 GB. Full datasets need several hundred GB of disk (§8). | Nemotron-12B in BF16 (~25 GB of weights) **does not fit** a 24 GB card. Run it in 8-bit (~13 GB); 4-bit is an option for 8–12 GB cards. Qwen2-VL-2B/7B fit in BF16. |
| Nemotron-Nano-12B-v2-VL | Needs `trust_remote_code`, pins `transformers>4.53,<4.54`, needs `mamba-ssm==2.2.5`, `causal_conv1d`, `timm`, `open_clip_torch`. No video decoding: we pass frames ourselves (2 fps, 8–128 frames). The `/no_think` system prompt turns reasoning off. FP8/NVFP4 variants target vLLM on Hopper/Blackwell and are no use on Ampere cards such as the 3090. | Primary backend is HF transformers + bitsandbytes. vLLM (install from main) is an optional second env. Video = our own frame sampler + a multi-image/`videos=` call. |
| Qwen2-VL-2B/7B | `Qwen2VLForConditionalGeneration` + `AutoProcessor` + `qwen-vl-utils.process_vision_info`. Takes video as a file path or a list of frame paths, with `fps`/`max_pixels`. | Works under transformers 4.53, so **one env** can serve all three VLMs. |
| DisasterVQA | Zenodo record 20306919: one file, `DisasterVQA-Dataset-v3.zip` (557.6 MB, md5 `4a3576c78a5d71a556ecc081bcc2cd28`), CC BY-SA 4.0. 1,395 images, 4,405 QA (binary / MC / open). Supposedly contains `disastervqa_annotations.jsonl`, `disastervqa_model_outputs.jsonl`, `taxonomy.json`. HF mirror at `QCRI/DisasterVQA`. | Images only, no time axis. Used as the "social-media image stream" source and as seed material for the simulated incident streams (pipeline_planning.md §1). Field names must be checked after download. |
| Video-MME | `lmms-eval/Video-MME`: `videomme/test-00000-of-00001.parquet` (405 kB), `subtitle.zip` (7.5 MB), `videos_chunked_01..20.zip` (~101 GB in total). | Download the parquet and subtitles first. Pick 100 *long* videos, then fetch chunks one at a time, extract only the selected videos and delete each zip. Read column names from the parquet; don't assume them. |
| VideoStir | `RomGai/VideoStir` is **method code** (ACL 2026), not a dataset. Its sample data and checkpoints are on Google Drive; it uses LLaVA-Video-7B and LongVideoBench. | Treat as a baseline/reference under `third_party/`, not under `data/`. |
| ACC-RAG | Paper only (EMNLP Findings 2025). | Baseline to reimplement lightly under `baselines/`. |
| Proposal datasets missing from `data/README.md` | M3-Bench-Robot is on HF (`ByteDance-Seed/M3-Bench`, 100 robot videos). MindCube is on HF (`MLL-Lab/MindCube`, `data.zip` → `raw/MindCube_tinybench.jsonl`). No public release of Video-SCOUT was found. | M3-Bench-Robot and MindCube-Tiny are full datasets. Video-SCOUT is dropped for now (§7). |

---

## 1. Repository layout

```
Agents282/
├── pyproject.toml              # package "streamrag", extras: [vllm], [dev]
├── README.md                   # quickstart: env, smoke tests, data download
├── configs/
│   ├── models.yaml             # model registry (ids, dtype/quant, max frames, default gen args)
│   ├── data.yaml               # dataset roots, sample sizes, splits, seeds
│   └── policy/default/         # editable policy P (Phase 3 edits this; see §5)
│       ├── policy.yaml         # τ, top-k, NLI thresholds, mutable attrs, eviction weights, budget B
│       └── prompts/{claims,meta}.txt   # editable; caption/answer/evaluator prompts live outside (§9.5)
├── src/streamrag/
│   ├── types.py                # Observation, Claim, MemoryEntry, QAItem, Stream (dataclasses)
│   ├── models/
│   │   ├── base.py             # VLM interface: generate(messages, images=None, frames=None, **gen)
│   │   ├── registry.py         # load_model(name) from configs/models.yaml, singleton cache
│   │   ├── nemotron_vl.py      # HF + bitsandbytes 8/4-bit, /no_think toggle, frame-list video
│   │   ├── qwen2_vl.py         # HF + qwen_vl_utils
│   │   ├── vllm_client.py      # optional: OpenAI-compatible client for `vllm serve`
│   │   ├── nli.py              # cross-encoder NLI (DeBERTa-v3 MNLI) → {entail,contradict,neutral}
│   │   └── embed.py            # sentence-transformers embedder (+ optional CLIP)
│   ├── video/frames.py         # PyAV frame sampler: every N s or fixed count → PIL + timestamps
│   ├── data/
│   │   ├── base.py             # Dataset protocol: download(), load() -> list[Sample], to_streams()
│   │   ├── disastervqa.py
│   │   ├── videomme.py
│   │   ├── m3bench.py
│   │   ├── mindcube.py
│   │   ├── synthetic.py        # 20-item evidence streams + ground-truth QA (§9.2–9.3; stub)
│   │   └── view.py             # CLI viewer: print QA, write frame/image contact sheet
│   ├── perception/caption.py   # VLM → timestamped captions, cached to disk (stub + cache util)
│   ├── memory/                 # Phase 1 stubs
│   │   ├── claims.py           # ① atomic claim extraction
│   │   ├── retrieve.py         # ② candidate retrieval
│   │   ├── temporal_nli.py     # ③ NLI + temporal gate → REINFORCE/ADD/STATE_CHANGE/CONFLICT
│   │   ├── update.py           # ④ typed update operator
│   │   ├── store.py            # ⑤ bi-temporal claim memory, token counting, text rendering
│   │   └── consolidate.py      # ⑥ budgeted, relation-aware eviction
│   ├── qa/answer.py            # Phase 2 stubs: parse question → time-anchored retrieval → cite/abstain
│   ├── baselines/              # FIFO, latest-per-key, periodic summary, similarity-merge, ACC-RAG-lite
│   ├── meta/                   # Phase 3 (Hyperagent-style loop), stubs; see §5
│   │   ├── policy.py           # load/validate/diff policy packages
│   │   ├── meta_agent.py       # LLM proposes an edited policy (JSON patch) from failure traces
│   │   ├── archive.py          # generations, scores, lineage, parent selection
│   │   └── loop.py             # select → mutate → staged eval → full eval → archive
│   └── eval/                   # checkpoint runner, evaluator agent, ESQA (§9.4), retention, bootstrap CI
├── scripts/
│   ├── setup_env.sh
│   ├── download_data.py        # `python scripts/download_data.py disastervqa|videomme|all`
│   ├── smoke_models.py         # one image + one short clip per model, prints output + latency + VRAM
│   └── cache_captions.py       # (next milestone) run the VLM once over the sampled frames
├── notebooks/
│   ├── 01_models_smoke.ipynb
│   └── 02_explore_data.ipynb
├── third_party/                # git clones only (VideoStir); gitignored
├── data/                       # README.md (kept), raw/ and processed/ gitignored
└── outputs/                    # captions cache, runs, archives; gitignored
```

Design rule: **everything after perception is text.** VLM captions are computed once and cached (`outputs/captions/<dataset>/<video_id>.jsonl`). The memory pipeline, baselines and the meta loop then replay cached text, so each dev evaluation in Phase 3 is cheap. This matches the proposal's compute table (VLM captioning is 18 of the 31 GPU-h).

---

## 2. Environment

- **Main env** (`.venv`, Python 3.12): `torch` (CUDA 12.x), `transformers>=4.53,<4.54`, `accelerate`, `bitsandbytes`, `mamba-ssm==2.2.5`, `causal-conv1d`, `timm`, `open_clip_torch`, `qwen-vl-utils`, `sentence-transformers`, `av`, `pillow`, `pandas`, `pyarrow`, `huggingface_hub`, `pyyaml`, `tiktoken` (token budgets), `tqdm`, `jupyter`.
  - `mamba-ssm`/`causal-conv1d` compile against the installed torch/CUDA. `setup_env.sh` installs torch first, then these with `--no-build-isolation`, and runs a check that imports both.
  - Pin exact versions in `pyproject.toml` once the smoke tests pass.
- **Optional vLLM env** (`.venv-vllm`): `VLLM_USE_PRECOMPILED=1 pip install git+https://github.com/vllm-project/vllm.git@main`, then `vllm serve ... --trust-remote-code --video-pruning-rate 0`. Only worth it for throughput during bulk captioning. Kept separate because vLLM main brings its own transformers.
- Hugging Face token in `.env` (gitignored) in case any repo is gated.

---

## 3. Models (working code in this step)

`configs/models.yaml`:

```yaml
nemotron-12b-vl:
  hf_id: nvidia/NVIDIA-Nemotron-Nano-12B-v2-VL-BF16
  backend: hf
  quant: int8            # int8 for development and reported numbers (§7)
  trust_remote_code: true
  reasoning: false       # injects "/no_think" system msg
  video: {fps: 2, min_frames: 8, max_frames: 128}
qwen2-vl-7b: {hf_id: Qwen/Qwen2-VL-7B-Instruct, backend: hf, dtype: bf16, max_pixels: 602112}
qwen2-vl-2b: {hf_id: Qwen/Qwen2-VL-2B-Instruct, backend: hf, dtype: bf16}
claims: {hf_id: Qwen/Qwen3-4B-Instruct-2507, backend: hf, dtype: bf16}   # claim extraction (§7)
nli:   {hf_id: MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli}   # swappable (ablation)
embed: {hf_id: BAAI/bge-small-en-v1.5}
```

Common interface (`models/base.py`):

```python
class VLM(Protocol):
    def generate(self, prompt: str, images: list[Image] | None = None,
                 frames: list[Image] | None = None, system: str | None = None,
                 max_new_tokens: int = 256) -> str: ...
```

- **Nemotron wrapper**: `AutoModelForCausalLM.from_pretrained(..., trust_remote_code=True, quantization_config=BitsAndBytesConfig(...))`, plus `AutoProcessor` and `AutoTokenizer`. The vision tower and projector stay unquantized via `llm_int8_skip_modules` (find the module names with `model.named_modules()` on first load). Build the prompt with `tokenizer.apply_chat_template`. Images go through `images=`. Video goes through `videos=frames` with `pixel_values_videos`. Set `model.video_pruning_rate` from config. The same wrapper serves text-only calls (claim extraction, QA, meta agent) when no image is given.
- **Qwen2-VL wrapper**: follows the model card. Frames are passed as a `{"type":"video","video":[frame paths],"fps":...}` entry.
- **`smoke_models.py`**: for each model, runs (1) a caption of one DisasterVQA image, (2) a caption of 8 frames from one Video-MME clip, (3) a text-only prompt. Logs output, latency, and peak `torch.cuda.max_memory_allocated()`. For NLI it runs 3 fixed premise/hypothesis pairs (the hallway example) and checks the labels.
- **Risk to check first**: bitsandbytes quantization of the custom Mamba-hybrid Nemotron code. If int8/nf4 fails, fallbacks in order: (a) `device_map="auto"` with CPU offload in BF16 (slow, but correct for captions computed once); (b) a community GGUF build via llama.cpp; (c) Qwen2-VL-7B as the captioner, with Nemotron used only where it fits.

---

## 4. Datasets (working code in this step)

Common types (`types.py`):

```python
@dataclass
class Observation:          # one element of an input stream
    stream_id: str; t: float; source: str          # e.g. "camera", "radio", "sitrep", "social"
    modality: Literal["image", "frame", "text"]
    path: str | None = None; text: str | None = None; meta: dict = field(default_factory=dict)

@dataclass
class QAItem:
    qa_id: str; stream_id: str; question: str; answer: str
    options: list[str] | None = None; t_query: float | None = None
    qtype: str | None = None; evidence_ids: list[str] | None = None
```

Each loader exposes `download()`, `load(split) -> list[Sample]` (raw records) and `to_streams() -> list[tuple[list[Observation], list[QAItem]]]`, so the pipeline sees one format for every dataset.

| Dataset | download() | to_streams() |
|---|---|---|
| **DisasterVQA** | Zenodo zip → `data/raw/disastervqa/`, check md5, unzip. Fallback: HF `QCRI/DisasterVQA` via `snapshot_download`. After the first download, print the JSONL keys and lock the field mapping in code. | Group images by disaster type/event (taxonomy or source dataset) into pseudo-streams with synthetic timestamps. Per pipeline_planning §1, create *j* random orderings per stream. QA comes straight from the annotations. |
| **Video-MME** | `hf_hub_download` the parquet and `subtitle.zip`. `select_videos(duration="long", n=100, seed)` writes `data/processed/videomme/selected.json`. Then, for each chunk: download, extract only the matching `*.mp4`, delete the zip (peak disk ≈ 5 GB). | One stream per video. Frames are sampled by `video/frames.py` (1 frame / 30 s by default, configurable). Subtitles become optional `text` observations (source = "asr"). The 3 MC questions per video become `QAItem` with options. |
| **M3-Bench-Robot** | `snapshot_download("ByteDance-Seed/M3-Bench", allow_patterns=robot*)`. Check the layout first. | One stream per video. Open QA, judged later by an LLM. |
| **MindCube-Tiny** | `MLL-Lab/MindCube` `data.zip` → `raw/MindCube_tinybench.jsonl` + images. | Each scene's photos arrive one at a time. 20% of test items get images deleted, so the gold answer becomes "not enough evidence". |
| **Synthetic evidence streams** | — | **The main evaluation input** (§9): fixed-length trajectories of 20 timestamped evidence items built from each dataset, each with ground-truth QA linked to the evidence that supports it. Not built yet (`data/synthetic.py` is a stub). |

**Viewer** (`python -m streamrag.data.view <dataset> --n 3 [--stream ID]`):
- Prints stream metadata, the observation timeline (t, source, modality, text preview) and QA items.
- Writes a contact sheet PNG (frames/images in a grid, labelled with timestamps) to `outputs/viz/<dataset>/<stream_id>.png`.
- `notebooks/02_explore_data.ipynb` calls the same functions inline and adds basic stats: video durations, QA type counts, images per pseudo-stream.

---

## 5. Hyperagents: review and how we use it

**Paper:** Zhang et al., *Hyperagents*, arXiv 2603.19461 (Meta et al., 2026). Code: `facebookresearch/HyperAgents`, licensed **CC BY-NC-SA 4.0**. Reimplement the ideas and cite them; don't copy their code into our repo.

### What it is
- A **hyperagent** is one editable program that contains both a *task agent* (solves the task) and a *meta agent* (modifies the task agent **and itself**). Because the improvement procedure is editable, the system can get better at improving. The paper calls this **metacognitive self-modification**.
- **DGM-H** keeps the Darwin Gödel Machine's open-ended archive. Each iteration it (1) samples a parent from the archive, (2) has the parent's meta agent edit a copy of the whole codebase (in Docker; the result is stored as a patch lineage), (3) runs a compile check, then a **staged eval** on a small subset (full eval only if the staged score is above 0), and (4) adds the child to the archive.
- **Parent selection** (`score_child_prop` in their code): weight = `sigmoid(10·(score − mean_top3)) · exp(−(n_children/8)³)`, then sampled. The score comes from the validation split when one exists. *Our diagram says "score × novelty". In their code the second factor is a child-count penalty, not a novelty term. We should use their formula, or define novelty explicitly.*
- **Initial agent is deliberately simple**: the task agent is a single LLM call, and the meta agent gets "modify any part of the codebase at {repo}" plus a bash tool and a file-edit tool, the eval results folder, and the number of iterations left.
- **Results:** gains on paper review (0 → 0.71) and robot reward design (0.06 → 0.37). Removing self-improvement of the meta agent, or removing the archive (always taking the latest child), gives little to no progress.
- **Transfer (imp@k):** hold a meta agent fixed, let it generate *k* task agents, and report the test gain of the best one (selected on validation) over the starting agent. Meta agents taken from DGM-H runs reach imp@50 = 0.63 on an unseen domain (IMO grading), and nearly all of that comes from the **transferred meta agent** (0.62) rather than the task agent (0.10). The meta-level features that emerged and transferred were **performance tracking** (records and compares metrics across generations) and **persistent memory** (notes carried across iterations).
- Their reported results use 5 runs, medians with 1,000-resample bootstrap CIs, and Wilcoxon tests. This matches our proposal's protocol.

### Mapping onto streaMRAG Phase 3

> **Superseded in part by §11 (2026-11-21):** the editable unit is now a free-text **memory strategy** given to the Nemotron memory agent, not a key/value policy package. The archive, parent selection, staged eval and transfer ideas below still apply.

| Hyperagents | streaMRAG |
|---|---|
| Hyperagent repo | A **policy package** `configs/policy/<gen>/`: `policy.yaml` (τ, top-k, NLI thresholds, mutable-attribute list, eviction weights) + `prompts/claims.txt` (task agent) + `prompts/meta.txt` and `meta.yaml` (meta agent: what it reads, how many traces, edit budget) + `notes.md` (the meta agent's persistent memory). The caption, answering and evaluator prompts are **not** in the package (§9.5): the meta agent must not be able to change how evidence is perceived, how questions are answered, or how answers are judged. |
| Meta agent edits any code | The meta agent (local Nemotron, text-only, **no tools: no bash, no file-system access, no Python edits**) returns a JSON patch over the policy package. The patch is validated against a schema (allowed keys, types, ranges, prompt length) and *may edit `meta.txt`/`meta.yaml` itself*, which is the metacognitive part. Any patch touching a key or file outside the policy package is rejected. No Docker is needed because nothing executable is edited. |
| Eval results folder | `outputs/meta/<run>/gen_XXX/`: dev scores, per-item failure traces taken from the evaluator agent's judgments (§9.4): the question, checkpoint, gold supporting evidence, and whether that evidence was never stored, evicted or merged away, plus the answer given. Also the archive's performance history. Giving the meta agent the history up front seeds the "performance tracking" behaviour the paper found emerged. |
| Score | **Mean checkpoint ESQA on dev streams** (§9.4), at a fixed budget B. This is the number the archive stores and parent selection uses. |
| Staged eval | 10 dev streams first. Full dev split only if the staged score beats the parent's or is ≥ (parent − ε). |
| Archive + parent selection | `meta/archive.py`: `archive.jsonl` + `gen_XXX/metadata.json` (parent, patch, scores, n_children). Selection uses `score_child_prop`. |
| Final test | The best generation by dev ESQA is tested **once** on held-out test streams, against the baseline memories under the same streams, answerer, evaluator and budget. |
| Baselines / ablations | (1) fixed default policy (no meta), (2) meta with a frozen `meta.txt` (= "w/o self-improve", ADAS-like), (3) no archive (always the latest child), (4) full DGM-H-style loop. These cover and extend pipeline_planning.md §2's three settings. |
| Cross-domain transfer | Run the loop on domain A (e.g. Video-MME-Long). Freeze the resulting meta agent, run *k* = 20–30 iterations on domain B (DisasterVQA streams / MindCube) with meta-agent self-edits turned off, and report **imp@k**. Then transfer only the meta agent vs only the task policy. This is exactly pipeline_planning.md §3's "cross-task transfer". |

**Risks:** (a) a 4/8-bit 12B model may propose weak edits, whereas the paper used frontier API models. Mitigations: a narrow, schema-checked edit surface, few-shot examples of good edits in the initial `meta.txt`, and rejection of invalid patches without spending eval budget. (b) Overfitting the dev split. Mitigations: split by video/scene, never by question, and test once. (c) Cost per iteration stays small only if captions and NLI results are cached (keyed by the hash of (premise, hypothesis, model)).

In this setup step, `meta/` contains only the stub classes, the policy schema, and `configs/policy/default/`.

---

## 6. Milestones and acceptance checks

| # | Deliverable | Done when |
|---|---|---|
| M0 ✅ | Skeleton, `pyproject.toml`, `setup_env.sh`, `.gitignore`, `git init` | `pip install -e .` works; `import streamrag` succeeds; mamba-ssm/causal-conv1d import |
| M1 ✅ | `models/` wrappers + `smoke_models.py` | All 3 VLMs caption one image and one 8-frame clip. NLI labels the hallway pairs correctly. VRAM and latency logged to `outputs/smoke/models.json` |
| M2 ✅ (Video-MME: 4/100 videos; run `download_data.py videomme` for the rest) | DisasterVQA + Video-MME download/load/view | `download_data.py disastervqa` passes the md5 check. `view disastervqa --n 3` and `view videomme --n 3` print QA and write contact sheets. Video-MME selection = 100 long videos, extracted |
| M3 ✅ | M3-Bench-Robot + MindCube-Tiny loaders | Same viewer check |
| M4 | **Deterministic stream builder** (§10.2–10.4): rule-based streams + answerability matrix + evidence scope, from dataset fields only | `build_streams.py` reproduces byte-identical `data/processed/streams/v2/` from the same dataset versions and config; invariant tests pass (§10.8) |
| M5 | **Probe + local judge** (§10.5–10.7): probe at any step, deterministic checks, local LLM judge, known-answer judge tests | Judge passes the known-answer test suite (§10.7); baseline curves over t = 1..20 on dev streams at B = 256/512/1024; human–judge agreement on ~200 hand-labelled probes |
| M6 | **Strategy-driven memory agent** (§11.1–11.3): Nemotron harness (raw images + text in, memory edit ops out) with provenance and budget enforcement; seed strategies (incl. the streaMRAG NLI-guided strategy) | Seed strategies scored on dev streams next to the code baselines |
| M7 | **Archive + meta agent** (§11.4–11.5): checkpoints (score node → child with updated strategy + meta harness) on one dev stream per dataset; fixed/dynamic ablations; held-out NLI strategy | Archive per dataset with G checkpoints per condition; fixed/fixed control reproduces its scores; best node scored on other dev streams and once on test |
| M8 | **Transfer** (§11.6): best strategy and/or meta harness moved to another dataset | imp@k for the four transfer conditions |
| (deferred) | Captioning of visual evidence that has no dataset text | Only after the stream set is curated (M4), and only for items that need it |

Interfaces for M4–M7 exist as stubs; parts of M5 (baseline memories, runner, scoring, splits) already exist from steps 1–2 (§8).

---

## 7. Decisions (2026-11-20)

1. **Datasets:** Video-SCOUT dropped for now. **M3-Bench-Robot and MindCube-Tiny are full datasets** alongside DisasterVQA and Video-MME (M3 in the milestones is no longer optional).
2. **Nemotron precision:** **int8 for reported numbers** (and development). The paper's resource section should be updated from "4-bit, 8–12 GB" to "8-bit, ~13–16 GB on one 24 GB GPU".
3. ~~**Claim extraction** uses a smaller text model (`Qwen/Qwen3-4B-Instruct-2507`, BF16). Nemotron remains the captioner, QA reader and meta agent.~~ *Superseded by decision 10: Qwen3-4B is now the evaluator, so claim extraction moves to Nemotron.*
4. **Meta agent edit surface:** policy values and prompt files only (Level 1, including the meta prompt). **No bash tool, no Python-file edits.** Level 2 is removed from the plan for the main results.
5. **Evaluation input:** synthetic evidence streams of **20 timestamped evidence items** built from the datasets, each with ground-truth QA (§9). This replaces whole-video streams as the main evaluation unit.
6. **Evaluation protocol:** a separate answering agent answers each stream's questions from the memory at **three checkpoints (after 1 item, after 10, after all 20)**. A separate evaluator agent judges correctness and how well the cited memory supports each answer. The resulting **ESQA** score is the metric for whether the memory agent is improving, and it is what baselines are compared on (§9.4).
7. **No bulk captioning for now.** Streams are built from text the datasets already contain. Captioning comes later, and only for evidence items without text.
8. **Reproducibility (2026-11-21):** evaluation streams are built by fixed rules from dataset fields only (no external model, no hand-curation), with dataset-derived answerability for every step. The memory agent can be probed at any step 1–20, and scoring uses deterministic checks plus a local, pinned LLM judge validated on an automatically generated known-answer suite (§10).
9. **Stream content and judging (2026-11-21):** video streams use capped items (more steps, not longer items); M3-Bench `uncertain` cells are excluded from the main score; DisasterVQA (and MindCube) items carry only the photo, with dataset annotations kept as judge-only reference facts; the judge is Qwen2-VL-7B-Instruct (§10.10). *Judge model superseded by decision 10.*
10. **Model roles and equal halves (2026-11-21):** ~~**Nemotron** is the dynamic memory agent: everything that turns incoming evidence into memory (perception of images, claim extraction, summaries/consolidation), plus the meta agent. **Qwen2-VL-7B** is the fixed answering agent with its own fixed prompt. **Qwen3-4B** is the fixed evaluator agent.~~ *(roles superseded by decision 11)* W = 60 s and C = 200 tokens are confirmed. The two halves of every stream receive equal context; the longer half is never rejected, the shorter one is completed with clipped content (§10.2). Equal context = equal number of steps (confirmed).
11. **Strategy-driven memory agent and archive (2026-11-21, corrected):** **Nemotron** is the memory agent. There is no separate perception stage: in one step the memory agent perceives the incoming evidence (images and text) and manages it in its limited memory. Across runs it varies only in the **text strategy** assigned to the run. **The same Nemotron, with its own meta prompting** (dataset-specific meta prompt), is the **meta agent** that proposes new strategies from a previous one and its evaluation. Every (strategy, evaluation) is a node in an **archive tree** (child = strategy adapted from its parent). **Qwen2-VL-7B** is both the fixed answering agent and the fixed evaluator, with separate fixed prompts. Qwen3-4B is not used in the main pipeline (§11).
12. **Archive mechanics (2026-11-21):** an archive node = (memory strategy, meta harness). Each checkpoint scores the node on **one dev stream** and the meta agent (Nemotron) always creates a child with an updated strategy and harness. The `memory_strategy` and `meta_harness` switches (fixed / dynamic) are ablations. The NLI-guided method is a held-out strategy condition. Archives stay within one dataset for now; transfer comes later (§11).
13. **First experiment (2026-11-21):** Nemotron runs **without reasoning mode** in both roles (speed). Only the **photo streams** are run for now, starting with **DisasterVQA**; the video datasets wait. A checkpoint is: score node N = (S, H) on its dev stream → the meta agent writes the **new meta harness H′** → child node N′ is created with H′ → the meta agent, now following **H′**, writes the child's strategy S′ from the parent strategy S → **the child is tested on the same dev stream as its parent**; one stream is reused for every node of an archive, so scores are directly comparable (§11.9).

---

## 8. Setup status and findings (2026-11-20)

**M0–M3 done.** `.venv` (torch 2.7.1+cu126, transformers 4.53.3, mamba-ssm 2.2.5, bitsandbytes 0.50.2), package `streamrag`, all four loaders + viewer, six models passing `scripts/smoke_models.py` (results in `outputs/smoke/models.json`).

| Model | Load | Image caption | 8-frame clip | Peak VRAM |
|---|---|---|---|---|
| nemotron-12b-vl (int8) | 30 s | ~8–11 s (97 tok) | ~8–9 s | 16.2 GB |
| qwen2-vl-7b (bf16) | — | 1.6 s | 1.2 s | 15.7 GB |
| qwen2-vl-2b (bf16) | 3 s | 0.9 s | 1.2 s | 4.6 GB |
| claims-qwen3-4b (bf16) | 3 s | text 1.6 s | — | 8.2 GB |
| nli-deberta-large | 1 s | 3/3 hallway pairs correct | — | 0.8 GB |
| embed-bge-small | 2 s | sim(related)=0.81, sim(unrelated)=0.57 | — | 1.0 GB |

**Nemotron upstream bugs, patched in `models/nemotron_vl.py` (we don't edit the downloaded model code):**
1. With our own `llm_int8_skip_modules`, bitsandbytes no longer skips `lm_head`, and NemotronH casts hidden states to `lm_head.weight.dtype` (int8). Fix: keep `lm_head` in the skip list.
2. Generation never reused the KV/Mamba cache: `prepare_inputs_for_generation` passes `past_key_values` but `forward` only takes `cache_params`; the cache class lacks `conv_kernel_size` and calls `.device` on a list; `NemotronHBlock.forward` never gives the cache to attention layers. Every decode step recomputed the whole sequence (16 tok/s at 30 tokens of context → 4 tok/s at 800). Patched all four; at int8 threshold 6.0 the cached output matches uncached greedy decoding (55/55 teacher-forced tokens; identical long-text output). Speedup: image 38 → 8 s, 8-frame clip 80 → 9 s, text 15 → 4 s. Toggle: `fix_generation_cache` in `configs/models.yaml`.
3. `int8_threshold: 0.0` (pure int8 matmuls) is ~1.5× faster still, but drifts more from uncached output (45/47 tokens). We keep the standard 6.0.

**Compute risk (captioning, now deferred):** Nemotron int8 takes ~10 s per caption with the tightened prompt (Qwen2-VL-7B ~3.5 s). With 20-item streams built mostly from dataset text (§9.2), only evidence items without text need captions, which is far below the ~21k frames of the original plan.

**Steps 1–2 status (code exists, reusable for M5):** *(Note: after §7 decision 11 the standalone caption cache below is not part of the main pipeline, because perception happens inside the Nemotron memory agent. It remains usable for the code baselines, which need text.)* caption cache (`perception/caption.py`, `scripts/cache_captions.py`, resume-safe; paused after ~30 test images); fixed dev/test splits (`eval/splits.py` → `data/processed/splits.json`); memory interface (`memory/base.py`, `memory/tokens.py`); five baseline memories (`baselines/memories.py`: fifo, retrieve_all, latest_replace, similarity_merge, periodic_summary); streaming runner (`eval/runner.py`, currently answers at each question's own timestamp — needs the checkpoint mode of §9.4); scoring with LLM judge and bootstrap CIs (`eval/metrics.py`, `scripts/score_run.py` — correctness only, needs the evidence-support judgment of §9.4). The caption prompt was tightened because Nemotron invented street names, times and weather.

**Data notes:**
- DisasterVQA: 178 pseudo-streams (8 images each, grouped by disaster type). Questions are per image ("…in the image?"), so stream-level QA needs the image reference or a rewrite (e.g. "In the photo at 03:00…") before it measures memory rather than perception.
- Video-MME: chunk 01 held 4 of the 100 selected long videos. Getting all 100 means downloading most of the 101 GB, keeping roughly 100 × ~0.4 GB. 745 of 900 videos have subtitles (HTML tags stripped).
- M3-Bench-Robot: 1,276 QA over 100 videos; each question has the timestamp at which it is asked (`t_query`). The videos are ~1.25 GB each (125.7 GB total); 2 downloaded so far. License is CC BY-NC-SA.
- MindCube-Tiny: 1,050 questions over 408 photo sets (215 among / 184 around / 9 rotation sets; rotation sets carry ~22 questions each).

---

## 9. Synthetic evidence streams and checkpoint evaluation

> **Superseded in part by §10 (2026-11-21).** §10 makes stream construction fully deterministic from dataset fields (no model in the loop, no hand-curation), replaces the parent-model evidence links of §9.2 with dataset-derived answerability, and generalizes the three checkpoints of §9.4 to probing at any step 1–20. Where §9 and §10 disagree, §10 applies.

This section defines the main evaluation of the memory compression agent. The question it answers: **does the memory the agent keeps still provide the evidence needed to answer questions about the stream, at every point in the stream, within a fixed token budget?** The same evaluation scores the baseline memories, the streaMRAG default policy, and every policy generation the meta agent proposes.

### 9.1 Overview

```
dataset annotations ──► synthetic stream: 20 timestamped evidence items  +  ground-truth QA
                                    │                                   (each QA linked to the
                                    ▼                                    evidence that supports it)
              memory agent (method under test) ingests items 1..20, memory ≤ B tokens
                                    │
              checkpoints:  after item 1  ·  after item 10  ·  after item 20
                                    │  memory snapshot
                                    ▼
              answering agent: answers ALL stream questions from the snapshot only,
                               cites the memory lines it used, or abstains
                                    │
                                    ▼
              evaluator agent: judges each answer against the gold answer and gold evidence,
                               and how well the cited memory supports it
                                    │
                                    ▼
              ESQA score per (question, checkpoint) → per stream → per method / policy
```

### 9.2 Synthetic evidence streams (M4)

A **stream** is a trajectory of **N = 20 evidence items**. Each item has an `evidence_id`, a timestamp `t`, a source (camera, social post, radio/ASR, dialogue, situation report), a modality, its content (text, plus a media reference where one exists) and provenance (dataset and original id). Streams are built once, versioned, and saved to `data/processed/streams/v1/<dataset>/<split>/<stream_id>.json`. Every method reads the same files.

**Text first, no new captioning.** Items use text the datasets already contain: DisasterVQA's verified per-image QA facts, Video-MME subtitles, M3-Bench dialogue subtitles, MindCube `captions.txt` (15 scenes). Visual items without any text get captions later, once the stream set is curated (§7.7).

| Dataset | One stream = 20 items from | Ground-truth QA | Supporting-evidence links |
|---|---|---|---|
| DisasterVQA | 20 images of one disaster type (or event cluster). Item text = the image's verified facts, rendered from its QA annotations (e.g. "Road flooded: no. Vehicles can pass: no. Damaged: bridge, road."). | The annotated questions about those images, reworded to name the item ("the photo received at 03:00 …"), plus stream-level questions that need several items (counts, comparisons, before/after). | Given directly: each question belongs to one image. Stream-level questions list all items they use. |
| Video-MME (long) | 20 consecutive segments of one video. Item = that segment's subtitle text + a keyframe reference. | The video's 3 MC questions. | Not in the dataset. A parent model proposes the supporting segments; the team verifies them on dev streams. |
| M3-Bench-Robot | 20 segments of one robot video. Item = the segment's dialogue lines + a keyframe reference. | The video's open questions (each has an ask-time). | The question's timestamp and `before_clip` bound the search; segments are proposed by a parent model and verified. |
| MindCube-Tiny | Photo sets have 2–4 views, so a stream joins several photo sets from the same setting (each photo is one item, with caption text where it exists). | That setting's MC spatial questions. | Given directly: each question names its photo set. |

- **Delivery orders:** each stream is also emitted in *j* reorderings of its evidence (pipeline_planning.md §1), so methods are tested on evidence arriving early, late or out of logical order. Gold answerability (§9.3) is recomputed per ordering.
- **Splits:** a stream inherits the split of the video, scene or image group it is built from (`data/processed/splits.json`), so dev and test never share source material.
- **Optional, later:** LLM-written situation reports or radio messages grounded in the visual items (pipeline_planning.md §1) to add multi-source text, and gold NLI relation labels between items for the intrinsic H1 evaluation (relation macro-F1). The checkpoint ESQA below does not depend on them.

### 9.3 Ground-truth QA per stream

Every QA item stores: question, gold answer, answer format (mc / mc_multi / yesno / open), question type, **supporting evidence ids (≥ 1)**, and its source annotation id.

- **Answerability at a checkpoint:** a question is answerable after *k* items only if all of its supporting items are among the first *k* delivered. Otherwise its gold answer at that checkpoint is **"Not enough evidence."**, and abstaining is correct.
- **Coverage:** each stream must have questions whose evidence arrives early, in the middle and late, so every checkpoint has both answerable and not-yet-answerable questions. Multi-item questions only become answerable when their last supporting item arrives, which is what makes the middle checkpoint informative. Target: ≥ 6 QA per stream.
- **Retention questions:** questions about early items are the ones a lossy memory fails at the final checkpoint, so each stream needs some.

### 9.4 Evaluation stage: answering agent, evaluator agent, ESQA (M5)

**Roles.** The three agents are kept separate so that the method being evaluated cannot influence how it is judged.

| Role | Sees | Produces | Fixed? |
|---|---|---|---|
| **Memory agent** (method under test: a baseline, the streaMRAG default policy, or a meta-agent generation) | Evidence items one at a time | Its memory, ≤ B tokens (B = 256 / 512 / 1024). Every memory line keeps the ids of the evidence it came from. | Varies; this is what is compared |
| **Answering agent** | Only the memory snapshot at the checkpoint, the current stream time, and the question | An answer that cites the memory lines it used, or "Not enough evidence." | Same model and prompt for every method |
| **Evaluator agent** | Question, gold answer, gold supporting evidence (original text), the answer, and the cited memory lines | Judgments (below) as JSON | Same model and prompt for every method |

**Checkpoints.** The memory snapshot is frozen after item **1**, item **10** (N/2) and item **20** (N). At each checkpoint the answering agent answers **all** of the stream's questions, including those not yet answerable.

**Judgments per (question, checkpoint).**
1. *Correctness:* correct / incorrect / abstained. Exact match for mc, mc_multi and yesno; the evaluator decides for open answers.
2. *Evidence support:* do the cited memory lines support the answer? **full / partial / none**. A correct answer with no support (a guess, or prior knowledge) is not credited.
3. *Evidence retention* (no LLM needed): which of the question's gold supporting items are still represented in memory, using the evidence ids each memory line carries. This separates "the evidence was lost" from "the evidence was there but the answer was wrong".

**ESQA (evidence-supported QA) score.**

| Situation at the checkpoint | Score |
|---|---|
| Answerable, answer correct, support **full** | 1 |
| Answerable, answer correct, support **partial** | 0.5 |
| Answerable, answer correct but **unsupported**, or wrong, or abstained | 0 |
| Not yet answerable, agent **abstains** | 1 |
| Not yet answerable, agent answers anyway | 0 |

- Reported per checkpoint (**ESQA@1, ESQA@10, ESQA@20**) and as the **mean over the three checkpoints, the primary metric**, at each budget B.
- Also reported: answer accuracy (correctness only), evidence retention, abstention precision/recall, memory tokens, and time per update.
- 95% bootstrap CIs resample **streams**, not questions, because questions within a stream are correlated. The proposal's 1,000 resamples are kept.

**How it is used.**
- **Comparison with baselines:** fifo, retrieve_all, latest_replace, similarity_merge, periodic_summary, and the streaMRAG default policy all run on the same streams, orderings, budgets, answering agent and evaluator agent. Only memory management differs.
- **Is the memory agent improving?** Phase 3 stores the mean dev ESQA of each policy generation in the archive and uses it for parent selection (§5). The evaluator's low-scoring judgments, with the retention diagnosis, become the failure traces the meta agent reads. The best generation is scored once on the test streams.
- **Validation of the evaluator:** 100 evaluator judgments on dev are checked by hand (as in the proposal). The evaluator should be a different model from the meta agent where possible (e.g. Nemotron answers and proposes edits, Qwen3 judges), to limit self-preference.

**Cost per run:** 3 checkpoints × Q questions × (1 answer + up to 1 judgment). With Q ≈ 6 that is ~36 LLM calls per stream, per method, per budget. Evaluator verdicts are cached by (question, answer, cited lines), so repeated runs and unchanged answers cost nothing. The meta loop's staged eval (10 dev streams) keeps per-generation cost to a few hundred calls.

### 9.5 Changes this implies for the existing code

| Area | Change |
|---|---|
| `data/synthetic.py` | Build v1 streams per dataset (§9.2), write JSON, plus a loader returning `Stream` objects with `QAItem.evidence_ids` filled. |
| `types.py` | Helper `answerable(q, delivered_ids)`; evidence items keep provenance. |
| `memory/base.py`, baselines | Memory lines get stable ids and carry their source evidence ids (`Note.obs_ids` already exists); rendering shows line ids so answers can cite them. |
| `eval/runner.py` | Checkpoint mode: snapshot after items 1, N/2, N and ask all questions at each (replaces answering at each question's own timestamp). |
| `qa/answer.py` | Answering-agent prompt asks for cited line ids; parse citations. The prompt lives in code/config **outside** the policy package. |
| `eval/evaluator.py` (new) | Evaluator prompt → JSON {correct, support, rationale}; retention from provenance; ESQA aggregation; verdict cache. |
| `eval/metrics.py`, `scripts/score_run.py` | Per-checkpoint ESQA, retention, abstention P/R, stream-level bootstrap. |
| `meta/policy.py` | Remove `qa.txt` and `caption.txt` from the editable prompt files; editable prompts become `claims.txt` and `meta.txt`. Failure traces come from evaluator output. |

### 9.6 Open questions

1. Is N = 20 used for every dataset, including MindCube, whose photo sets are small?
2. Timestamps: real video time for Video-MME/M3-Bench segments, and fixed spacing (e.g. 60 s) for image datasets?
3. How many streams per dataset and split, and how many delivery orders *j* per stream?
4. Evaluator model: a different model from the answering agent and meta agent, or the same model with a separate prompt?
5. Is 0.5 the right credit for partially supported answers, or should support be scored separately from correctness?
6. Are LLM-written situation reports and radio messages part of v1, or added after the dataset-only streams work?

---

## 10. Reproducible stream construction and evidence-grounded judging (2026-11-21)

**Requirement.** Anyone on the team can rebuild the same evidence streams and re-score any run **without an external model or a person in the loop**:
- Streams, questions, gold answers, chronological order and answerability labels come only from dataset fields, through fixed rules.
- Every model used in evaluation runs locally, at a pinned version, with greedy decoding and versioned prompts.
- The memory agent can be probed at **any step t = 1..N** (N = 20 for the photo datasets, longer for the video datasets, §10.2): given what is in its memory after item t, answer a question with cited evidence, or abstain.

The hand-curated samples in `examples/` (built by `make_sample_streams.py`) remain only as readable references and as test cases for the rule-based builder. They are not the evaluation set, because their M3-Bench and Video-MME evidence links were chosen by hand.

### 10.1 What the datasets provide, and the rule this leads to

| Dataset | Question → evidence location in the dataset | Time axis in the dataset | Gold answer format |
|---|---|---|---|
| DisasterVQA | **Exact:** each question belongs to one image (`image_id`) | Posting time from tweet id / MEDIC file name | yes/no, multiple choice, open (list of accepted answers) |
| MindCube-Tiny | **Exact:** each question lists the photos it uses (`images`) | None (order of `images`; synthetic spacing) | multiple choice letter |
| M3-Bench-Robot | **Only an upper bound:** the question is asked at `timestamp`, so everything needed is in the video before that time | Video time | open text |
| Video-MME | **Only an upper bound:** questions assume the whole video has been watched | Video time | multiple choice letter |

**Rule (source-level answerability).** A question is *answerable* at step t once all content the dataset says it depends on has been delivered: its image(s) for DisasterVQA and MindCube, its video up to `timestamp` for M3-Bench, its whole video for Video-MME. It is *not yet answerable* while none of that content has arrived. In between (part of the source has arrived, but not up to the dataset's bound) its status is *uncertain*, because the datasets don't say where inside the source the answer is.

This gives a three-valued label for every (question, step) pair, computed from dataset fields alone:

| Label | Meaning | Correct behaviour | Used in the primary score |
|---|---|---|---|
| `answerable` | All dataset-required content delivered | Answer correctly, citing in-scope evidence | Yes |
| `not_yet` | None of the question's source delivered | Abstain ("Not enough evidence.") | Yes |
| `uncertain` | Source partly delivered (M3-Bench / Video-MME only) | Either: abstain, or answer with evidence the judge confirms | **No (decided 2026-11-21): reported separately, never hand-labelled** |

Streams are laid out so that `uncertain` cells are rare and the `answerable` / `not_yet` cells test retention and abstention cleanly (§10.2).

### 10.2 Stream layout: two blocks, chronological

Every stream is chronological and made of **block A** followed by **block B**. Each block is filled from one or more source units in their real order. **5 questions are drawn from block A's sources and 5 from block B's.** That makes exactly 5 questions answerable at the **block boundary** (the "half" checkpoint) and all 10 at the last step, and keeps all of block B's questions `not_yet` throughout block A by construction.

- **Photo datasets (DisasterVQA, MindCube):** one photo per step, 10 + 10 = **20 steps**, with the boundary at step 10.
- **Video datasets (M3-Bench, Video-MME):** item length is capped and steps are added instead (decided 2026-11-21). The stream length N and boundary step depend on the videos and are stored in the stream file.

| Dataset | Source unit | One step = | Block = | Question becomes `answerable` at |
|---|---|---|---|---|
| DisasterVQA | photo | 1 photo | 10 photos of one disaster type, consecutive in posting time | the step of its photo (`not_yet` before it) |
| MindCube | scene (2–4 photos) | 1 photo | whole scenes packed to exactly 10 photos (deterministic subset-sum over the dev/test scene list) | the step of the last photo it uses (`not_yet` before) |
| M3-Bench | video | one capped item (below) | one video from 0 to a cut time | the step whose item contains its ask time; `uncertain` from the start of its block until then; `not_yet` while its block hasn't started |
| Video-MME | video | one capped item (below) | 2 whole videos (3 questions each, 5 kept) | the last step of its video; `uncertain` during its video; `not_yet` before |

**Capped video items (deterministic).** A video is cut into consecutive windows of fixed length W (default 60 s). If a window's dialogue exceeds C tokens (default 200, counted with the budget tokenizer), it is split at subtitle-line boundaries into consecutive items of ≤ C tokens each. Each item gets one keyframe at the midpoint of its time span. A ~34 min M3-Bench video therefore gives ~35–45 steps per block, and a Video-MME block of two ~45 min videos ~90–110 steps.

**Equal halves for video streams (no rejections; decided 2026-11-21).** Both blocks receive the same context: the same number of steps L, so the same number of capped items and keyframes. Text-token totals of the two halves are recorded in the stream file. L is fixed per stream as follows:
1. For each block, compute its **minimum length** m: the steps needed for its 5 selected questions to become `answerable`.
   - M3-Bench: the item containing the 5th-earliest ask time of the block's video.
   - Video-MME: the end of the block's question videos.
2. Set **L = max(m_A, m_B)**.
3. **Fill each block to exactly L steps:**
   - **M3-Bench:** continue the block's own video past its minimum cut and clip it at step L. This is real continuation, and all chosen questions stay answerable because their ask times are earlier.
   - **Video-MME,** or an M3-Bench video that ends before L: append **filler** from an unused video of the same split (seeded choice, no questions asked about it), clipped at step L.
4. **Question content is never clipped.** Clipping the end of a Video-MME question video would remove the dataset's whole-video answerability bound for its questions, so the extra length always comes from continuation or filler.

The block boundary is therefore always step L, and the stream has N = 2L steps.

**Item content.** Only what the dataset provides to an observer, never the annotations used to score:
- **Video items (M3-Bench, Video-MME):** every subtitle/dialogue line whose start time falls in the item's span, so the stream contains *all* speech up to the cut and nothing is selected by hand, plus the keyframe.
- **DisasterVQA photos:** **the photo only**, with its posting time and platform. The dataset's verified observations are *not* given to the memory agent (decided 2026-11-21): reading the evidence and recovering those observations is the memory agent's job. They are kept in the stream file as `reference_facts` for the judge only (§10.6).
- **MindCube photos:** **the photo only**, with the view direction needed to resolve "image k" references, which the question text states anyway. The annotated object names are kept as judge-only `reference_facts`, following the same principle as DisasterVQA.
- **Times:** real video time, or real posting time for DisasterVQA. For MindCube and between concatenated videos, a fixed synthetic spacing that is stored in the stream file.

**Perception is the memory agent's job; there is no separate perception stage** (decision 11). Images (photos and video keyframes) arrive raw, together with the item's dataset text, and go straight to the memory agent (**Nemotron**, a VLM). In the same step it reads the evidence and decides what to write into its limited memory, following its strategy. What the agent notices in an image is therefore part of what a strategy controls (e.g. "record vehicles, water level and people for each photo"). Nothing is pre-captioned or shared between strategies. Captions are cached per (model, prompt, image) only to make replays fast; this is not a pre-captioned dataset. Making the caption prompt part of the editable policy is a possible later ablation.

**Question text** is the dataset's, plus a fixed reference prefix when several sources share a stream ("About the photo posted Sep 04 07:10 UTC: …", "In video 2 of this stream: …", "(image 1 = E05, image 2 = E06) …"). The original text is kept in `original`. Gold answers are never edited. For open answers, all accepted answers are kept.

**Selection is seeded and rule-based:** which sources form a stream, which 5 questions per block (stratified by question type), and which keyframes, all from `configs/streams.yaml` (seed, block sizes, k, spacing). Dev/test assignment is by source unit, so a video, scene or photo group never appears in both splits.

**Filtering without hand-picking.** Some questions can't be answered from what a stream contains, e.g. visual details between keyframes. Two fixed filters drop these:
1. A **metadata filter:** e.g. drop Video-MME "Information Synopsis" items in v2, because they need the whole video at once and suit only the final step.
2. A **full-context oracle filter** (video datasets): the fixed answering agent (Qwen2-VL-7B, a VLM) sees *all* items of the question's source directly, uncompressed text and keyframes, and the fixed evaluator (Qwen2-VL-7B, evaluator prompt) scores the answer. No memory agent is involved, so the filter is the same for every strategy. If the local judge doesn't mark its answer correct, the question is dropped. Because the models, prompts and decoding are fixed, this filter is itself reproducible, and it sets the ceiling every memory method is compared against. DisasterVQA and MindCube questions are not filtered, since the dataset already verifies them against their photos. Their oracle score (answering agent given the question's own photos directly) is reported as the perception ceiling instead.

**Expected yield:**
- DisasterVQA: ~70 streams.
- MindCube: ~50–100 streams.
- M3-Bench: 50 streams (video pairs), or 100 if each video serves as block A in one stream and block B in another.
- Video-MME: ~20–25 streams from the 100 selected long videos.

### 10.3 Stream file format (v2)

`data/processed/streams/v2/<dataset>/<split>/<stream_id>.json`:
- `n_steps` (= 2L for video streams, 20 for photo streams), `boundary_step` (= L or 10), `block_text_tokens` (text-token total of each half), `filler` (which items are filler and their source video).
- `items[]`: `item_id`, `step`, `t`, `source_unit`, `span`, `text` (dataset speech only; empty for photos), `frames[]` (paths + timestamps), `provenance` (dataset ids). These are the fields the memory agent receives.
- `reference_facts{item_id: [...]}`: **judge-only** annotations for an item (DisasterVQA verified observations, MindCube object names). Never passed to the memory or answering agent.
- `questions[]`: `qa_id`, `question`, `original`, `gold`, `accepted_answers`, `format`, `qtype`, `block`, and:
  - `evidence_scope`: the item ids that may legitimately support the answer. Exact items for DisasterVQA and MindCube; for M3-Bench and Video-MME, the items of the question's source up to its answerable step.
  - `answerability`: a list of `n_steps` labels (`answerable` / `not_yet` / `uncertain`), one per step.
- `manifest`: builder version, config hash, dataset versions (Zenodo md5, Hugging Face revision hashes), and a content hash of the stream.

### 10.4 Builder

`scripts/build_streams.py <dataset> --split dev|test --config configs/streams.yaml` → v2 files plus a summary table (streams, questions per block, answerability counts per step). It uses the existing loaders, frame sampler and splits. No network access is needed beyond the dataset downloads, and no model except the optional oracle filter (§10.2), which reads the fixed local models.

### 10.5 Probing the memory agent at any step

**Agents and models (decision 11):**

| Role | Model | Fixed or varied | Sees |
|---|---|---|---|
| **Memory agent** | Nemotron-Nano-12B-v2-VL (int8) | Model and harness fixed; **only the text strategy varies** between runs (§11) | Strategy text, current memory, the new item (raw image(s) + dataset text), the step and budget B. It perceives the item and outputs memory edits in one call |
| **Meta agent** | Nemotron-Nano-12B-v2-VL (same model) | Its own meta prompting: a dataset-specific meta prompt (`configs/meta/<dataset>.txt`) | A parent strategy, its evaluation results and memory logs; outputs a child strategy (§11.4) |
| **Answering agent** | Qwen2-VL-7B-Instruct (BF16) | Fixed model and fixed answering prompt (`configs/answering/prompt.txt`) | Only the memory snapshot at step t, the current time and the question |
| **Evaluator agent** | Qwen2-VL-7B-Instruct (same model as answering) | Fixed model and fixed evaluator prompts (`configs/judge/`) | Question, gold answer, predicted answer, cited memory lines, and the original content of cited items (images + dataset text + judge-only reference facts) |

**Answering and evaluation share a model (decided).** The judge design (`LLM judge architecture.txt` §11) prefers an independent evaluator, because a model may favour answers in its own style. Mitigations:
- Separate, fixed prompts for the two roles, and the evaluator never sees the answering prompt.
- Deterministic checks decide every closed-format answer, abstention and citation-scope question without the evaluator.
- Neither role shares a model with the memory agent being evaluated (Nemotron).
- The known-answer suite (§10.7) and the human check measure the evaluator's bias directly. In particular, it must reject wrong answers written in the answering agent's own style.

**Staged execution.** Nemotron (~16 GB) and Qwen2-VL-7B (~16 GB) don't fit on one 24 GB GPU together, so a run has three passes with files in between. Each pass can be re-run on its own:
1. **Memory pass** (Nemotron + strategy): feed the stream item by item (images + text) and save the memory snapshot (lines + provenance) at every probed step, plus the per-step logs → `snapshots.jsonl`, `memory_log.jsonl`.
2. **Answer pass** (Qwen2-VL-7B, answering prompt): answer every (step, question) probe from the snapshots → `answers.jsonl`.
3. **Evaluation pass** (Qwen2-VL-7B, evaluator prompts + deterministic checks) → `judgments.jsonl` and scores.

The answer and evaluation passes reuse one loaded Qwen2-VL-7B.

**Cost of a memory pass:** one Nemotron call per step with an image costs ~8–11 s (§8). That is ~3–4 min for a 20-step photo stream and ~10–40 min for a video stream (~70–220 steps), per strategy.

```
probe(stream, method, budget B, step t, question q):
    memory = method.fresh(B);  feed items 1..t in order         # snapshot M_t, ≤ B tokens
    answer = answering_agent(M_t lines with ids, current time, q)
          -> JSON {"answer": ... | "NOT_ENOUGH_EVIDENCE", "cited": [memory line ids]}
    cited_items = provenance(cited)                               # memory line ids → item ids (deterministic)
```

- Every memory line keeps the ids of the items it came from. This already exists as `Note.obs_ids` for the baselines and must be added for the streaMRAG claims. So citations always resolve to original items without any model.
- A run probes a chosen grid of steps × all 10 questions. The memory is fed once, and snapshots are taken at each probed step.
  - **Photo streams (20 steps):** every step by default (200 probes per stream).
  - **Video streams (~70–220 steps):** the default grid is step 1, every 10% of the stream, the block boundary, each question's `answerable` step, and the last step (~15 probe steps). Any other step can be probed on request.
- The answering agent (Qwen2-VL-7B) is fixed (model, prompt, greedy decoding) and identical for every strategy and baseline. It sees only the snapshot, never the raw items.

### 10.6 Scoring a probe: deterministic checks first, local LLM judge second

**Deterministic checks (no model):**

| Check | When | Output |
|---|---|---|
| Abstention | label `not_yet` | 1 if it abstained, else 0 (premature answer = unsupported claim) |
| Closed-format correctness | mc / mc_multi / yesno | exact match against `gold` |
| Citation validity | it answered | cited items ⊆ delivered items (no citing the future) and cited ∩ `evidence_scope` ≠ ∅ |
| Evidence recall (exact datasets) | DisasterVQA / MindCube | \|cited ∩ scope\| / \|scope\| |
| Retention | always | fraction of `evidence_scope` items still represented in M_t (via provenance); separates "evidence lost" from "evidence kept but misused" |
| Unnecessary abstention | label `answerable` | abstained = 0 |

**Local LLM judge = the evaluator agent, Qwen2-VL-7B with the evaluator prompts** (implements the three stages in `LLM judge architecture.txt`):
1. **Answer judge (text):** question, gold and accepted answers, predicted answer → `correct` 1 / `partial` 0.5 / `incorrect` 0 with a short reason. Used for open answers (M3-Bench, DisasterVQA open). Closed formats skip it.
2. **Evidence judge:** question, predicted answer, and the *original* content of the cited items → `supported` / `unsupported` / `insufficient`. The evaluator is a VLM, so it sees the original images (photos and keyframes) together with the dataset speech and, for DisasterVQA and MindCube, the judge-only `reference_facts`. It reads the original items, not the memory agent's own descriptions of them, so a wrong memory line can't vouch for itself.
   - If the evaluator can't decide from the cited items, it returns `insufficient`. These cases are counted separately and sampled for the human check.
3. **Aggregation:** combines the deterministic checks and the judge outputs into the probe score and a failure category (missing evidence, wrong citation, unsupported answer, premature answer, unnecessary abstention, possible reasoning error), as structured JSON per probe.

**Probe score (ESQA-t):**

| Label at step t | Outcome | Score |
|---|---|---|
| `answerable` | correct, citation valid, evidence `supported` | 1 |
| `answerable` | partially correct or `insufficient` evidence | 0.5 |
| `answerable` | wrong, unsupported, invalid citation, or abstained | 0 |
| `not_yet` | abstained | 1 |
| `not_yet` | answered | 0 |
| `uncertain` | reported separately: abstain rate, and grounded-early-answer rate (correct + supported) | — |

Reported as **curves over the stream** (accuracy on `answerable`, abstention accuracy on `not_yet`, retention; video streams plotted by relative position t/N), the mean over probed steps (primary metric), and the summary at step 1 / block boundary / last step. 95% CIs bootstrap over streams.

**Judge reproducibility.**
- Model (decision 11): **Qwen2-VL-7B-Instruct** (BF16, pinned revision) with fixed evaluator prompts, for both the answer judge and the evidence judge. It is the same model as the answering agent (see the mitigations in §10.5) and a different model from the memory agent and meta agent (Nemotron).
- Settings: greedy decoding, versioned prompts in `configs/judge/`, and a JSON schema with a fixed parse-and-retry rule.
- Verdicts are cached by hash(inputs, model revision, prompt version), so re-scoring is free and identical.
- The judge never changes during the meta-agent loop.

### 10.7 Validating the judge without people in the loop (plus a small human check)

**Known-answer test suite.** Generated automatically from the streams, so every case has a label known by construction:

| Case | Built from | Expected verdict |
|---|---|---|
| Correct answer, cites scope item | gold answer + an item in `evidence_scope` | correct + supported |
| Correct answer, cites a wrong item | gold answer + an item from another source in the stream | correct + unsupported (citation invalid) |
| Wrong answer, cites scope item | a wrong MC option, or another question's gold answer for open questions | incorrect |
| Premature answer | gold answer at a `not_yet` step | score 0 by the deterministic check |
| Unnecessary abstention | abstain at an `answerable` step | score 0 |
| Paraphrased correct answer (open) | another accepted answer from `accepted_answers` | correct |

The judge must reach a set accuracy (e.g. ≥ 95% on the deterministic cases, ≥ 90% on the LLM cases) before it is used. This suite is re-run whenever the judge model or prompt changes.

**Human check:** ~200 real probes stratified by dataset, label and verdict, labelled once by two team members. Human–judge agreement (Cohen's κ) is reported. The labels are stored in the repo, so the check is reproducible.

### 10.8 Reproducibility checks (tests in CI or locally)

- **Rebuild:** the same dataset versions and config give byte-identical stream files (content hash in the manifest).
- **Invariants:** items are strictly chronological; 20 steps for photo streams; every video item ≤ C tokens and ≤ W seconds; 5 + 5 questions per block; block B questions are `not_yet` at every step ≤ `boundary_step`; every `answerable` label is consistent with the dataset bound; `evidence_scope` ⊆ items of the question's source; no `reference_facts` text appears in any item's `text`.
- **Re-scoring:** the same run outputs + judge cache give identical scores.
- **Hand samples:** on the four `examples/` samples, the builder's answerability for the hand-linked questions must be compatible with the hand links (a hand-linked item never falls outside `evidence_scope`).

### 10.9 Code changes

| Area | Change |
|---|---|
| `configs/streams.yaml` (new) | seed, block layout, window length W, item token cap C, synthetic spacing, filters |
| `src/streamrag/data/streams.py` (new) | rule-based builders per dataset, answerability matrix, evidence scope, v2 writer/loader |
| `scripts/build_streams.py` (new) | CLI + summary table + invariant checks |
| `memory/base.py`, baselines, streaMRAG store | every memory line keeps source item ids; `snapshot()` |
| `configs/answering/prompt.txt` (new) | fixed answering-agent prompt (Qwen2-VL-7B), outside the editable policy package |
| `eval/runner.py` | three-pass execution: memory (snapshots + logs) → answers → judgments, each written to file |
| `eval/runner.py` | probe mode: feed once, snapshot at probed steps, ask the question grid |
| `qa/answer.py` | answering-agent JSON output with cited memory line ids; abstention token |
| `eval/judge.py` (new) | deterministic checks, text answer judge, visual/text evidence judge, aggregation, verdict cache |
| `configs/judge/` (new) | versioned judge prompts and model revisions |
| `scripts/test_judge.py` (new) | known-answer suite (§10.7) |
| `eval/metrics.py`, `scripts/score_run.py` | ESQA-t curves, per-label metrics, stream bootstrap |

### 10.10 Decisions (2026-11-21) and remaining questions

Decided:
1. M3-Bench `uncertain` cells stay out of the primary score; there is no hand-labelling.
2. Video items are capped (W = 60 s, C = 200 tokens by default) and video streams get more steps instead of longer items.
3. The judge is Qwen2-VL-7B-Instruct for both judge stages.
4. DisasterVQA items carry the photo only. The verified observations are judge-only reference facts, because recovering them from the image is the memory agent's job. The same applies to MindCube object annotations.

5. *(follow-up)* W = 60 s and C = 200 tokens are confirmed as defaults.
6. *(follow-up)* Equal halves: both halves receive the same number of steps L; the shorter half is completed by continuing its own video (M3-Bench) or with clipped filler from an unused video. No stream or pairing is rejected for length, and question videos are never clipped.
7. *(follow-up)* Roles: Nemotron = dynamic memory agent (perception, claims, consolidation, and the meta agent); Qwen2-VL-7B = fixed answering agent with a fixed prompt; Qwen3-4B = fixed evaluator. This supersedes item 3 above (judge model) and §7 decision 3 (claim extractor).

8. *(follow-up)* Equal context = equal number of steps (confirmed).
9. *(follow-up)* Roles changed again by §7 decision 11 and §11: Nemotron = memory agent (perceives evidence and manages memory in one step) and meta agent (own meta prompting); Qwen2-VL-7B = answering agent + evaluator. Items 3 and 7 above are superseded.

---

## 11. Strategy-driven memory agent, meta agent and archive (2026-11-21, revised)

This section defines what is varied and improved in the experiments.

- **Memory agent:** a fixed model (**Nemotron-Nano-12B-v2-VL**, int8, reasoning off) in a fixed harness. It perceives each incoming piece of evidence (images and text) and manages it in its limited memory. What varies between runs is the **memory strategy**: a text document assigned to the run.
- **Meta agent:** the same Nemotron (reasoning off, for speed; decision 13), driven by its own **meta harness**: a text document saying how to propose better strategies for this dataset.
- **Scoring:** a strategy is scored by the downstream performance of the fixed answering agent (Qwen2-VL-7B) as judged by the fixed evaluator (Qwen2-VL-7B, evaluator prompts) plus the deterministic checks (§10.6).
- **Archive:** each **node** holds a (memory strategy, meta harness) pair and its score. Every checkpoint scores a node and creates a child node with an updated strategy and an updated meta harness (each possibly unchanged, depending on the ablation). For now, archives are built **within one dataset**, and a strategy is scored and improved on **a single dev stream**.

```
checkpoint on node N0 = (S0, H0):  score S0 on the dev stream → 0.41
                                   meta agent (Nemotron, harness H0) reads S0, its score,
                                   failures and memory logs → writes S1 and H1
        child node N1 = (S1, H1)
checkpoint on node N1:             score S1 → 0.47;  meta agent (harness H1) → S2, H2
        child node N2 = (S2, H2)   …
```

### 11.1 Memory strategy and meta harness

| | Memory strategy S | Meta harness H |
|---|---|---|
| **Used by** | memory agent (Nemotron, reasoning off), at every step of a run | meta agent (Nemotron, reasoning off), once per checkpoint |
| **Says** | how to perceive and manage evidence: what to look for in images and text, what to store, how to phrase memory lines, when to merge, update or delete, how to treat repeated, changed or conflicting information, what to protect when over budget | how to turn a strategy's evaluation into a better strategy for this dataset: what the dataset's streams and questions look like, how to read the failure categories and memory logs, what kinds of changes to try or avoid, and (if dynamic) how to improve itself |
| **Form** | plain text, ≤ 500 tokens | plain text, ≤ 800 tokens |
| **Identity** | `strategy_id` = SHA-256 prefix of the text | `harness_id` = SHA-256 prefix of the text |
| **Fixed part (not editable)** | the harness frame around it: output format (edit ops), provenance and budget rules (§11.2) | the frame around it: inputs given, output JSON schema, length caps (§11.4) |

Neither is ever executed as code. Every run records the `strategy_id` it used, and every proposal records the `harness_id` that produced it. Seed strategies live in `configs/strategies/seeds/` and seed meta harnesses in `configs/meta/<dataset>.md`.

### 11.2 Memory-agent harness (fixed for every run)

At each step t the harness calls Nemotron once (greedy decoding, reasoning off) with:
1. A fixed system frame: the output format, the budget rule and the provenance rule.
2. **The strategy S.**
3. The current memory as numbered lines: `[m12 | 03:20 | src E03,E07] text`.
4. The new item: its id, time, source, dataset text, and its **raw image(s)** (photo or keyframe). Perceiving the image is part of this same call.
5. The budget B and current usage.

The agent replies with **memory edit operations** in JSON:

```json
{"add":    [{"text": "...", "sources": ["E08"]}],
 "update": [{"id": "m12", "text": "...", "sources": ["E03", "E07", "E08"]}],
 "delete": ["m4"]}
```

**Harness rules:**
- **Provenance:** an edit may only cite items that have already been delivered, and an updated line keeps or extends its sources, so every memory line traces back to original items (§10.5–10.6).
- **Budget:** if memory exceeds B after the edits, the agent gets one retry with "over budget by X tokens". If it is still over, a deterministic fallback deletes the oldest lines until it fits, and the step is logged as a budget violation.
- **Invalid output:** one retry; then the step is a no-op, logged as invalid.
- **Logs per step** (`memory_log.jsonl`): the edits, violations, memory size and latency, for the meta agent.

**Cost:** ~8–11 s per step with an image, so ~3–4 min per 20-step photo stream and ~10–40 min per video stream (§10.5).

### 11.3 Strategies that are measured

**Seed strategies (archive roots).** Written once by the team in `configs/strategies/seeds/`. Each includes generic guidance on what to record from images (people, objects, their states, hazards, visible text):

| Seed | Idea |
|---|---|
| `append_recent` | Store each item briefly; when over budget, drop the oldest lines |
| `rolling_summary` | Keep a running summary; fold old lines into it when over budget |
| `entity_index` | One line per entity or attribute with its latest value and the time it was last confirmed |

**Held-out NLI strategy (decided 2026-11-21).** The proposal's NLI-guided method is its own **held-out condition**. It is measured on the same streams with the same answering agent, evaluator and budget, but it is not a root of the evolving archive and the meta agent never edits it. Its harness adds one fixed step that the other strategies don't have:
1. The memory agent (Nemotron) perceives the new item and lists candidate atomic facts.
2. The harness computes the DeBERTa NLI relation (entail / contradict / neutral) between each candidate fact and the related memory lines, and the temporal gate labels each pair reinforce / add / state change / conflict (§9, pipeline_plan2.md ③).
3. The memory agent applies the `streamrag_nli` strategy text using those labels and returns the usual edit ops.

Comparing it with the seeds and the evolved strategies measures what the explicit NLI relations add.

**Code baselines** (fifo, retrieve_all, latest_replace, similarity_merge, periodic_summary) are text-only, so they would see no image content in the photo streams. They are kept only for the video datasets, where items carry dataset speech, unless the team decides to give them a fixed caption step.

### 11.4 Meta agent and the checkpoint

**A checkpoint on node N = (S, H)** does two things in one go:
1. **Score:** run the memory pass with S on the archive's dev stream (from step 1), then the answer and evaluation passes. Attach the score, judgments and memory logs to N.
2. **Propose:** call the meta agent (Nemotron, reasoning off, greedy) with the fixed meta frame + **H** + the inputs below. It must return a **child node N′ = (S′, H′)**, and a child is always created.

**Meta inputs:**
- the strategy S;
- its scores (mean ESQA, per label, per checkpoint, retention, abstention, budget violations);
- up to K failure cases from the evaluator's judgments (default K = 20). Each case has the question, step, gold answer, predicted answer, failure category, the evaluator's note on what the cited image or item actually shows, and a retention diagnosis from the memory logs (evidence never stored / stored then deleted at step k / still in memory but misused);
- a lineage summary: the ancestors' scores and one-line rationales, i.e. performance tracking.

**Meta output (fixed JSON schema):**

```json
{"strategy": "<complete new memory strategy>",
 "harness":  "<complete new meta harness>",
 "rationale": "...", "changes": ["..."]}
```

**Fixed vs dynamic (ablation switches, recorded in every node):**

| Switch | Fixed | Dynamic |
|---|---|---|
| `memory_strategy` | S′ = S (the meta agent's `strategy` field is ignored) | S′ = the meta agent's new strategy |
| `meta_harness` | H′ = H (the `harness` field is ignored) | H′ = the meta agent's new harness (metacognitive self-modification, §5) |

The harness checks lengths, that the result isn't empty, and that the JSON schema is valid. Under "dynamic", a child identical to its parent is allowed but logged.

**The four ablation conditions:**

| `memory_strategy` | `meta_harness` | What it tests |
|---|---|---|
| fixed | fixed | Repeat-run control: should reproduce the parent score exactly (greedy decoding), confirming determinism |
| dynamic | fixed | Strategy improvement with a fixed improvement procedure (ADAS-like, "w/o self-improve" in §5) |
| dynamic | dynamic | Full self-improvement: better strategies *and* a better way of producing them (DGM-H-like) |
| fixed | dynamic | The meta harness evolves while the strategy is held fixed. Scores stay constant, so this only produces harnesses, which can later be paired with dynamic strategies or transferred |

### 11.5 Archive

`outputs/archive/<dataset>/<archive_name>/`:
- `archive.jsonl`: one line per node.
- `node_XXXX/strategy.md`, `node_XXXX/meta_harness.md`, `node_XXXX/meta.json`, `node_XXXX/runs/<stream_id>/{snapshots,memory_log,answers,judgments}.jsonl`, `node_XXXX/scores.json`.

| Node field | Content |
|---|---|
| `node_id`, `parent_id` | tree structure (`null` for roots) |
| `strategy_id`, `harness_id` | the exact texts in this node |
| `switches` | `memory_strategy` and `meta_harness`: fixed / dynamic |
| `created_by` | `seed` or `meta`, with the rationale and listed changes from the parent's proposal |
| `eval_stream` | dataset, split, stream id, budget B (one dev stream for now) |
| `scores` | mean ESQA on the eval stream, per checkpoint and label, retention, abstention, budget violations |
| `models` | pinned revisions of Nemotron and Qwen2-VL-7B; frame and prompt versions; reasoning modes |
| `n_children` | for parent selection |

**Loop** (`scripts/evolve.py`):

```
archive = root node(s) (seed S, seed H for this dataset)
repeat for G checkpoints:
    N = archive.select_node()          # unscored child first; else a scored node by score_child_prop (seeded)
    checkpoint(N):  score N (if not yet scored)  →  propose child N′ = (S′, H′)  →  archive.add(N′)
```

- **Single dev stream for now (decided).** Every node in an archive is scored on the same single dev stream, and the meta agent sees only that stream's results. Scores on a single stream overfit easily, so the best node is afterwards scored on the other dev streams and then once on test streams. These scores are reported and never used for selection.
- **Within one dataset for now (decided).** Each archive belongs to one dataset. Seeds and meta harnesses are per dataset.
- **Repeatability:** greedy decoding, fixed frames, cached evaluator verdicts and seeded node selection make the whole archive reproducible. The fixed/fixed control (§11.4) checks this in every archive.

### 11.6 Later: transfer across datasets

After the within-dataset archives work, take the best node of dataset A and start an archive on dataset B from it. Four transfer conditions:

| Transferred to B | Meaning |
|---|---|
| strategy S only (with B's seed harness) | do good memory strategies carry over? |
| meta harness H only (with B's seed strategy) | does a good way of improving strategies carry over? |
| both S and H | full transfer |
| neither (B's seeds) | reference |

Each condition gets k checkpoints on B's dev stream and reports imp@k (§5). In Hyperagents the transferred meta agent carried most of the benefit; this tests the same question for memory management.

### 11.7 Code changes

| Area | Change |
|---|---|
| `configs/strategies/seeds/*.md` (new) | seed strategies + the held-out `streamrag_nli` strategy |
| `configs/meta/<dataset>.md` (new) | seed meta harness per dataset |
| `src/streamrag/memory/agent.py` (new) | Nemotron memory-agent harness: frame with strategy, memory and raw item (image + text), edit ops, provenance and budget rules, retries, step logs, snapshots; NLI variant for the held-out strategy |
| `src/streamrag/meta/strategy.py` (new) | text documents with ids (strategy, meta harness): load/save, hash, length checks. Replaces the key/value patch of `meta/policy.py` |
| `meta/meta_agent.py` | meta frames (inputs + JSON schema), Nemotron reasoning off, parse, apply the fixed/dynamic switches |
| `meta/archive.py` | node = (strategy, harness, switches, eval stream, scores, run paths); `select_node` (unscored child first, else `score_child_prop`) |
| `scripts/run_strategy.py` (new) | score one (strategy, stream) or one code baseline: 3 passes |
| `scripts/evolve.py` (new) | the checkpoint loop with `--memory-strategy fixed|dynamic --meta-harness fixed|dynamic` |
| `configs/models.yaml` | role entries: memory agent and meta agent → Nemotron (reasoning off); answering agent + evaluator → Qwen2-VL-7B |

### 11.8 Decisions (2026-11-21) and remaining questions

Decided:
1. The NLI-guided method is a held-out strategy condition, measured but not evolved.
2. Strategies are scored, and improvements proposed, on a single dev stream for now.
3. Every checkpoint scores a node and always creates a child with an updated strategy and an updated meta harness. Each can be fixed or dynamic, and both switches are ablations.
4. Archives stay within one dataset for now; cross-dataset transfer of strategies and/or harnesses comes later (§11.6).
5. ~~The meta agent runs with Nemotron's reasoning mode on~~ Both the memory agent and the meta agent run with reasoning off (decision 13).

Remaining:
1. Code baselines in photo streams: drop them for DisasterVQA and MindCube (the seeds serve as baselines), or give them a fixed caption step?
2. Which dev stream per dataset is the single archive stream? Proposed: the first dev stream the builder produces (seeded), recorded in the archive.
3. How many checkpoints G per archive for the first experiments (e.g. 10 per condition)? At ~10–40 min each on photo datasets, the 4 conditions × 10 checkpoints take about 7–27 GPU-hours per dataset.

### 11.9 First experiment protocol (2026-11-21)

- **Data:** rule-built DisasterVQA dev streams (§10.2): 20 consecutive flood photos with a recoverable posting time, 5 + 5 questions per stream. Questions whose (question, answer) pair occurs on ≥ 3 photos in the stream are excluded as non-distinctive. Memory budget B = 512.
- **Checkpoint order:**
  1. score N = (S, H) on the archive's stream;
  2. the meta agent (following the fixed harness-update frame and H) writes H′;
  3. create child N′ with H′;
  4. the meta agent (following H′) writes S′ from S;
  5. the child N′ = (S′, H′) is scored on the **same stream** at the next checkpoint. One stream is reused for all nodes of the archive.
- **Meta feedback** may include the judge-only reference facts of items behind failed answers, so the meta agent learns what perception missed. The memory agent never sees them. Because the child is scored on the same stream, those facts can teach stream-specific details; held-out dev streams measure whether gains generalize (§11.5).
- **Comparability (decided):** every node of an archive is scored on the same single stream, so parent and child scores are directly comparable.
- **Status of scores:** provisional until the known-answer judge suite (§10.7) exists.

### 11.10 Minimal-start profile (Hyperagents setup, 2026-11-21)

To observe self-improvement, the main archives start from minimal texts, as in Hyperagents. There, the initial task agent is a single model call and the initial meta agent's whole instruction is "Modify any part of the codebase at {repo_path}".
- **Seed memory strategy** (`configs/strategies/seeds/minimal.md`): "Update the memory with the new item."
- **Seed meta harness** (`configs/meta/minimal.md`, dataset-agnostic): "Improve the memory strategy."
- **Fixed frames** (`memory/frame_minimal.txt`, `meta/frames/*_minimal.txt`): only the inputs and the output format. The memory frame states that questions will later be answered from the memory, the edit-op format, the provenance rule and the budget. The meta frames show the harness, strategy and evaluation log and ask for the new text in tags. They contain no advice about what makes a good strategy or harness.
- Selected with `run_checkpoint.py --profile minimal` and recorded in every node (`models.profile` + prompt hashes). The earlier detailed profile (`default`, archive `demo`) is kept for comparison.

### 11.11 Experiment loop as implemented (2026-11-21)

`scripts/run_experiment.py --dataset disastervqa --archive <name> [--iterations 3]`. One iteration adds and scores exactly one node, so 3 iterations from scratch give 3 nodes, and re-running continues the archive:
- **Empty archive:** create root node 0 from the `minimal` profile seeds (default) and score it on the first dev stream (or `--stream`).
- **Otherwise:**
  1. The parent is the **best-scoring node** (ties → newest node; `--parent-selection score_child_prop` is available).
  2. The meta agent (Nemotron, reasoning off) sees **only the direct parent's** strategy, meta harness and evaluation log, with no siblings and no lineage. It writes H′ and then, following H′, S′.
  3. It **samples** (temperature 0.7, top-p 0.95) with seed = 1000 × child id, so runs are reproducible and a re-selected parent yields a new child. A child identical to an existing sibling is re-sampled with the next seed (up to 3 times); sibling content is never shown to the meta agent.
  4. The child is scored on the **same stream** as every other node.
- Archive settings (stream, budget, profile, switches) are fixed at creation and stored in the root node.

### 11.12 End-of-stream evaluation and stream length (2026-11-21)

- **Questions are asked only after the last item of an evidence stream** (decided). The memory agent never sees the questions. The per-step probing of §10.5 is not used in the experiment, though the answer pass can still be run on any saved snapshot for later analysis.
- **Stream length is a setting** (`run_experiment.py --stream-length N`, stored in the root node). The rule-built base stream (20 DisasterVQA photos) is split into consecutive evidence streams of N items (`segment_stream`). Each stream keeps the questions whose photo lies inside it, and streams without questions are dropped. With N = 10, every node is tested on photos 1–10 and 11–20 (5 questions each), each from empty memory.
- **Node score** = mean of the per-stream scores (mean ESQA over each stream's questions at its end). The meta log gives the node score and then one section per stream.
- **No code execution:** strategies and meta harnesses are plain text read by the memory and meta agents (decision 4). Code-like text a meta agent writes is not executed.
