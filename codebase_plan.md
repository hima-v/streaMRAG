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
│       └── prompts/{caption,claims,qa,meta}.txt
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
│   │   ├── synthetic.py        # Phase-0 simulated incident streams (stub; pipeline_planning §1)
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
│   └── eval/                   # metrics (QA acc, evidence recall, abstention F1, relation macro-F1), bootstrap CI
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
| Synthetic incidents | — | Stub for now. Later: a parent VLM writes a situation report, QA, and gold relation labels from DisasterVQA images + Video-MME clips (pipeline_planning §1), giving the H1 gold-labelled streams. |

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

| Hyperagents | streaMRAG |
|---|---|
| Hyperagent repo | A **policy package** `configs/policy/<gen>/`: `policy.yaml` (τ, top-k, NLI thresholds, mutable-attribute list, eviction weights) + `prompts/{caption,claims,qa}.txt` (task agent) + `prompts/meta.txt` and `meta.yaml` (meta agent: what it reads, how many traces, edit budget) + `notes.md` (the meta agent's persistent memory). |
| Meta agent edits any code | The meta agent (local Nemotron, text-only, **no tools: no bash, no file-system access, no Python edits**) returns a JSON patch over the policy package. The patch is validated against a schema (allowed keys, types, ranges, prompt length) and *may edit `meta.txt`/`meta.yaml` itself*, which is the metacognitive part. Any patch touching a key or file outside the policy package is rejected. No Docker is needed because nothing executable is edited. |
| Eval results folder | `outputs/meta/<run>/gen_XXX/`: dev scores, per-item failure traces (wrong relation label, evicted-but-needed claim, wrong abstain), and the archive's performance history. Giving the meta agent the history up front seeds the "performance tracking" behaviour the paper found emerged. |
| Staged eval | 10 dev streams first. Full dev split only if the staged score beats the parent's or is ≥ (parent − ε). |
| Archive + parent selection | `meta/archive.py`: `archive.jsonl` + `gen_XXX/metadata.json` (parent, patch, scores, n_children). Selection uses `score_child_prop`. |
| Final test | The best generation by dev score is tested **once** on held-out streams. |
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
| M4 (next phase) | `cache_captions.py` over the sampled frames | Captions cached for 5 videos; per-frame time estimate checked against the 18 GPU-h budget |

Phase 1/2/3 implementation comes after M4 and is out of scope for this setup step. Its interfaces exist as stubs from M0 on.

---

## 7. Decisions (2026-11-20)

1. **Datasets:** Video-SCOUT dropped for now. **M3-Bench-Robot and MindCube-Tiny are full datasets** alongside DisasterVQA and Video-MME (M3 in the milestones is no longer optional).
2. **Nemotron precision:** **int8 for reported numbers** (and development). The paper's resource section should be updated from "4-bit, 8–12 GB" to "8-bit, ~13–16 GB on one 24 GB GPU".
3. **Claim extraction** uses a smaller text model (`Qwen/Qwen3-4B-Instruct-2507`, BF16). Nemotron remains the captioner, QA reader and meta agent.
4. **Meta agent edit surface:** policy values and prompt files only (Level 1, including the meta prompt). **No bash tool, no Python-file edits.** Level 2 is removed from the plan for the main results.

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

**Compute risk:** Nemotron int8 at ~8 s per 97-token caption → ~21k frames ≈ 45–50 GPU-h, against 18 h budgeted in the proposal. Levers: shorter captions (cap `max_new_tokens` ~60), fewer frames (1 per 30–60 s), skip near-duplicate frames, or Qwen2-VL-7B captions (~1.6 s) with Nemotron kept for QA and the meta agent. Decide before M4.

**Data notes:**
- DisasterVQA: 178 pseudo-streams (8 images each, grouped by disaster type). Questions are per image ("…in the image?"), so stream-level QA needs the image reference or a rewrite (e.g. "In the photo at 03:00…") before it measures memory rather than perception.
- Video-MME: chunk 01 held 4 of the 100 selected long videos. Getting all 100 means downloading most of the 101 GB, keeping roughly 100 × ~0.4 GB. 745 of 900 videos have subtitles (HTML tags stripped).
- M3-Bench-Robot: 1,276 QA over 100 videos; each question has the timestamp at which it is asked (`t_query`). The videos are ~1.25 GB each (125.7 GB total); 2 downloaded so far. License is CC BY-NC-SA.
- MindCube-Tiny: 1,050 questions over 408 photo sets (215 among / 184 around / 9 rotation sets; rotation sets carry ~22 questions each).
