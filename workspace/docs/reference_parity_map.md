# Reference parity map (Phase 0 · Run 1)

Generated: 2026-04-08

Goal: enumerate **scoring-critical** logic in the reference notebooks and map each piece to your `layers` implementation (if any), with a **parity status**:

- **FULL**: same concept + same core algorithmic behavior + same inputs/outputs
- **PARTIAL**: concept exists but key mechanics differ, are stubbed, or interfaces don’t match
- **MISSING**: no equivalent implementation/wiring in `layers`

Reference set scanned:

- `reference notebooks/11-25-lb-5.ipynb`
- `reference notebooks/arc-2-2026-qwen3-unsloth-mar-26.ipynb`
- `reference notebooks/nvarc-arc-2025-winning-solution-for-t4x2-gpu.ipynb`
- `reference notebooks/8-75-nvarc-arc-2025-winning-solution-for-t4.ipynb` (minified JSON; patterns match the above via grep)
- `working/arc-agi-2-notebook.ipynb`

`layers` surface for ARC-AGI-2 used for mapping:

- `input/kaggle-ml-comp-scripts/scripts/layers/layer_1_competition/level_1_impl/level_arc_agi_2/`

---

## Layered architecture mapping (what belongs where)

This repo’s ARC implementation is already split into useful “levels”. For parity work, being explicit about ownership helps prevent “almost parity” work landing in the wrong layer.

- **`level_0`**: pure primitives (schemas, transforms, decode/rank math, deterministic helpers). No orchestration.
- **`level_1`**: domain logic built on `level_0` (formatters, small evaluators, model definitions that are framework-light).
- **`level_2`**: backend-facing code (torch/transformers/unsloth), model load, KV-cache stepping, checkpoint inference.
- **`level_3`**: inference orchestration (compose augmentations + backend calls + decoding + ranking per task).
- **`level_4`**: submit strategy dispatch (`single` / `ensemble` / `llm_tta_dfs` routing).
- **`level_5`**: pipeline stages that write end artifacts (e.g. `submission.json`) and manage run metadata.
- **`level_6`**: validate-first wrappers and composite pipeline flows returning `PipelineResult`.
- **`level_7`**: CLI argument parsing / handlers.

The reference notebooks also implement an **artifact pipeline** that you do not yet have as a first-class stage:

- “inference outputs” store (bz2+pickle) → `ArcDecoder` selection → submission

In the layered architecture, that likely becomes:

- **`level_0`**: artifact record schema + selection scorer functions over records (`kgmon` / `probmul`).
- **`level_1`**: `ArcDecoder`-like object that loads records and runs selectors.
- **`level_5`**: a stage that writes/reads the inference-output store and produces `submission.json`.

---

## 1) Model loading logic

| Notebook | Function / block | Purpose | Already in `layers`? | Parity |
|---|---|---|---|---|
| `11-25-lb-5.ipynb` | `FastLanguageModel.from_pretrained(...)` + `FastLanguageModel.get_peft_model(...)` | Load Qwen3 base model + attach LoRA (Unsloth). | **No** (Unsloth path absent). | **MISSING** |
| `arc-2-2026-qwen3-unsloth-mar-26.ipynb` | Same as above + `unsloth.models.qwen3` flash attention patching | Load model + patch attention implementation to avoid VRAM blowups / GQA issues. | **No** | **MISSING** |
| `nvarc-arc-2025-winning-solution-for-t4x2-gpu.ipynb` | Same as above | Same. | **No** | **MISSING** |
| `8-75-nvarc-arc-2025-winning-solution-for-t4.ipynb` | (grep indicates same patterns) | Same. | **No** | **MISSING** |
| (layers) | `ArcLmBackendConfig` + `build_lm_backend(...)` (`level_2/arc_lm_backend.py`) | Choose `mock://` backend or plain `transformers` backend. | N/A | **PARTIAL** (different backend family; no Unsloth parity) |

Notes (critical):

- Your `layers` backend selection is **`mock://` or vanilla `transformers`**, not Unsloth.
- The reference kernels include **explicit runtime patching** (e.g., SDPA wrapper) that materially affects feasibility/perf on Kaggle GPUs.

Layer placement (target vs current):

- **Target level**: **`level_2`** (backend + load + runtime patches).
- **Current**: `level_2/arc_lm_backend.py` exists but does not implement Unsloth/Qwen3 patching or LoRA attach semantics from the notebooks.

---

## 2) Tokenization logic

| Notebook | Function / block | Purpose | Already in `layers`? | Parity |
|---|---|---|---|---|
| `11-25-lb-5.ipynb` | `QwenFormatter.fmt_query`, `fmt_reply`, `fmt_train` | Build Qwen chat-format prompt strings using digit-grid text + `<|im_start|>...` markers. | **Yes**: `ArcQwenGridChatFormatter` (`level_1/lm_qwen_chat_format.py`). | **PARTIAL** (format concept matches; token IDs/special tokens handling differs) |
| `11-25-lb-5.ipynb` | `QwenFormatter.max_new_tokens()` | Compute max generation length using tokenizer encoding of a max 30×30 grid reply. | **Yes**: `ArcQwenGridChatFormatter.max_new_tokens_for_max_grid()` | **PARTIAL** |
| `11-25-lb-5.ipynb` | `QwenFormatter.convert_tokens_to_array(...)` | Decode token IDs → text → grid (digits per line) with validation. | **Yes**: `ArcQwenGridChatFormatter.decode_tokens_to_grid(...)` + `arc_text_lines_to_grid` | **PARTIAL** (validation / stopping token conventions differ) |
| `arc-2-2026-qwen3-unsloth-mar-26.ipynb` | same `QwenFormatter` | same | same | same |
| `nvarc-arc-2025-winning-solution-for-t4x2-gpu.ipynb` | same `QwenFormatter` | same | same | same |

Critical mismatch drivers:

- Reference notebooks define **explicit ARC token IDs** (`ARC_VOCAB`, `ARC_TOKENS`, `PAD_ID`, `EOS_ID`, etc.) used by decoding/DFS and scoring; your `layers` decoding treats tokens as 0..9 colors **by convention** and does not encode the reference’s special-token gating behavior.

Layer placement (target vs current):

- **Target level**: formatter + parse in **`level_1`**, token-id conventions in **`level_0`**.
- **Current**: chat formatter is in `level_1/lm_qwen_chat_format.py` (good), but the “token ID contract” is not centralized and not consumed by a turbo-DFS implementation.

---

## 3) DFS / decoding logic

| Notebook | Function / block | Purpose | Already in `layers`? | Parity |
|---|---|---|---|---|
| `11-25-lb-5.ipynb` | `turbo_dfs(...)` | Recursive DFS/beam search over **true model logits** using `past_key_values`, pruning by `max_score` (NLL threshold). | **No direct equivalent**. | **MISSING** |
| `11-25-lb-5.ipynb` | `inference_turbo_dfs(...)` | Initialize cache from prefix tokens; run `turbo_dfs`; return sorted beams per batch. | **No** | **MISSING** |
| `arc-2-2026-qwen3-unsloth-mar-26.ipynb` | `turbo_dfs` + explicit memory cleanup (`del outputs`, etc.) | Same decode but with extra OOM prevention. | **No** | **MISSING** |
| `nvarc-arc-2025-winning-solution-for-t4x2-gpu.ipynb` | same `turbo_dfs` / `inference_turbo_dfs` | same | **No** | **MISSING** |
| (layers) | `decode_grid_candidates(...)` (`level_0/decoder_dfs.py`) | Beam decode over **per-cell probability grids** (not token logits / KV cache). | N/A | **PARTIAL** (beam-ish, but wrong primitive: cell probs vs token logits) |
| (layers) | `decode_tokens_to_grids(...)` (`level_0/token_decoder.py`) | Beam expansion using a `token_probs_provider(prefix)` callback; fixed \(H×W\) length; **no KV caching**. | N/A | **PARTIAL** (shape constraint similar; not `turbo_dfs`) |

Critical: reference decode is **logits-first** (token-level) with KV caching and EOS handling; current `layers` decode is **distribution-first** (cell-prob grids) or callback-based without cache semantics.

Layer placement (target vs current):

- **Target level**:
  - `level_0`: pure search bookkeeping + pruning policy
  - `level_2`: backend “step” function (KV cache in/out, logits out)
  - `level_3`: per-task orchestration and budgeting
- **Current**: `level_0/decoder_dfs.py` and `level_0/token_decoder.py` are useful, but they are not the same primitive as `turbo_dfs`.

---

## 4) Augmentation logic

| Notebook | Function / block | Purpose | Already in `layers`? | Parity |
|---|---|---|---|---|
| `11-25-lb-5.ipynb` | `permute_mod`, `ArcDataset.forward_mod`, `ArcDataset.invert_mod` | Apply/invert transforms encoded in key strings: rot90, transpose, permute(color), etc. | **Yes**: `AugmentationSpec`, `apply_augmentation`, `invert_augmentation` (`level_0/augmentations.py`). | **PARTIAL** (ops exist; key-string protocol differs) |
| `11-25-lb-5.ipynb` | `ArcDataset.augment(...)` | Generate many deterministic transform variants, including transpose + random permutations. | **Yes**: `generate_augmentation_specs(...)` | **PARTIAL** (sampling scheme differs; dataset/key behavior differs) |
| Other refs | same pattern | same | same | same |

Layer placement (target vs current):

- **Target level**: pure augmentations in **`level_0`** (current: `level_0/augmentations.py` ✅).
- **Missing for artifact parity**: a stable codec between “reference key strings” (`.rot90.`, `.transpose.`, `permute##########`) and `AugmentationSpec` (should live in `level_0`).

---

## 5) Candidate ranking logic

Reference notebooks have **two distinct ranking layers**:

1. **Within-decode**: rank beams/candidates by beam score / NLL.
2. **Across augmentations / duplicate solutions**: merge duplicates by grid hash; then score merged groups using `kgmon` / `probmul`-style getters.

| Notebook | Function / block | Purpose | Already in `layers`? | Parity |
|---|---|---|---|---|
| `11-25-lb-5.ipynb` | `score_sum(...)` + `score_kgmon(...)` | Merge duplicates by grid hash; prefer frequently occurring + low augmentation score mean. | **Yes**: `ensemble_score_kgmon(...)` (`level_0/ensemble_reference_rankers.py`). | **PARTIAL** (ported idea; may not match exact guess dict schema) |
| `11-25-lb-5.ipynb` | `score_full_probmul_3(...)` | Alternative selector using baseline-adjusted beam + aug scores. | **Yes**: `ensemble_score_full_probmul_3(...)` | **PARTIAL** |
| (layers) | `rank_candidate_grids(...)` (`level_0/candidate_scoring.py`) | Rank `CandidatePrediction`s by weighted combo of consistency, model score, augmentation likelihood. | Exists, but it’s **not** the same as reference selection scorers. | **PARTIAL** |

Layer placement (target vs current):

- **Target level**:
  - `level_0`: reference selection scorer functions (already present) + artifact record schema
  - `level_1`: selector runner (`ArcDecoder`-like) over loaded artifacts
- **Current**:
  - `level_0/ensemble_reference_rankers.py` is a good port of the *ranking formulas*.
  - `level_0/candidate_scoring.py` ranks a different object type (`CandidatePrediction`), which is fine for your `llm_tta` path but not a drop-in replacement for the reference artifact selector stage.

---

## 6) Task adaptation / fine-tuning

| Notebook | Function / block | Purpose | Already in `layers`? | Parity |
|---|---|---|---|---|
| `11-25-lb-5.ipynb` | `UnslothFixedTrainer` + `UnslothTrainingArguments` + `trainer.train()` | Fine-tune/adapt LoRA weights (or similar) inside the kernel. | **No** Unsloth training integration. | **MISSING** |
| `arc-2-2026-qwen3-unsloth-mar-26.ipynb` | Alternative `UnslothFixedTrainer.compute_loss` + compile disabling env vars | Same, plus stabilizers for torch.compile / dynamo. | **No** | **MISSING** |
| (layers) | `run_task_adaptation(...)` (`level_0/arc_lm_adaptation.py`) | Loop calling `backend.adapt_for_task(...)` for `steps`. | Present | **PARTIAL** (backend adaptation is stubbed / non-equivalent today) |
| (layers) | `TransformersArcLmBackend.adapt_for_task(...)` (`level_2/arc_lm_backend.py`) | Placeholder no-op. | Present | **MISSING** (behavior) |

Layer placement (target vs current):

- **Target level**: adaptation/training logic in **`level_2`** (backend) + **`level_5`** (stage), with configs in `level_0`.
- **Current**: correct scaffold split exists, but the backend implementation is not present.

---

## 7) Artifact generation (decoded results, inference outputs)

| Notebook | Function / block | Purpose | Already in `layers`? | Parity |
|---|---|---|---|---|
| `11-25-lb-5.ipynb` | `pickle.dump(decoded_result, bz2.BZ2File(...))` | Write per-task decoded beam/candidate objects to a store (e.g. `/kaggle/inference_outputs`). | **No** | **MISSING** |
| `11-25-lb-5.ipynb` | File protocol: `*.out{i}` records include `solution`, `beam_score`, `score_aug`, etc. | Defines schema consumed later by `ArcDecoder`. | **No stable equivalent schema** | **MISSING** |
| (layers) | `run_submission_pipeline(...)` writes `submission.json` directly (`level_5/stages.py`) | Produces final Kaggle submission file, not intermediate decoded artifacts. | Yes | **PARTIAL** (end artifact exists; intermediate artifact pipeline does not) |

Layer placement (target vs current):

- **Target level**:
  - `level_0`: artifact record schema + to/from dict
  - `level_5`: file IO + store layout + stage entrypoints
- **Current**: `level_5/stages.py` directly writes `submission.json` without producing the intermediate inference-output store.

---

## 8) Selection / final answer logic

| Notebook | Function / block | Purpose | Already in `layers`? | Parity |
|---|---|---|---|---|
| `11-25-lb-5.ipynb` | `ArcDecoder.load_decoded_results(...)` | Load bz2-pickled decoded outputs keyed by puzzle id; group them under `decoded_results`. | **No** | **MISSING** |
| `11-25-lb-5.ipynb` | `ArcDecoder.run_selection_algo(selection_algorithm=score_kgmon)` | Run `score_kgmon` or `score_full_probmul_3` over grouped guess dicts; return ordered guesses per puzzle. | **Partially**: reference rankers exist; no artifact loader / orchestrated selection stage. | **PARTIAL** |
| `11-25-lb-5.ipynb` | `ArcDataset.get_submission(...)` + `validate_submission(...)` | Fill Kaggle submission dict and validate by comparing to known outputs. | **Some equivalents** exist (submission JSON writing + postprocessing), but not this exact selection pipeline. | **PARTIAL** |
| (layers) | `ARC26PostProcessor().normalize_submission(...)` (`level_5/stages.py`) | Normalize output structure for Kaggle submission. | Yes | **PARTIAL** (postprocess exists; upstream selection differs) |

Layer placement (target vs current):

- **Target level**:
  - `level_1`: `ArcDecoder`-like selection runner using `level_0` scoring functions
  - `level_5`: submission assembly stage (plus postprocess)
- **Current**: only the final-submission path exists as a stage; the intermediate selection stage is missing.

---

## Working notebook wiring (for parity relevance)

`working/arc-agi-2-notebook.ipynb` is currently a **CLI orchestrator**: it calls `cmds.build_submit_command(...)` and streams output. It does **not** implement:

- Unsloth/Qwen model load
- `turbo_dfs` token-level decode
- bz2/pickle artifact output store
- `ArcDecoder` selection stage

Therefore, for “reference score parity” it will require additional wiring (Phase 6) after implementing the missing/partial components in Phases 1–5.

Notebook wiring (layer touchpoints):

- Notebook calls `level_0/notebook_commands.py` (command builder) → CLI (`level_7`) → pipelines (`level_6`/`level_5`).
- For reference parity, the notebook must eventually be able to configure:
  - model backend (`level_2`)
  - decode strategy (`level_0`/`level_3`)
  - artifact stage on/off (`level_5`/`level_1`)
  - selection scorer choice (`level_0`/`level_1`)

---

## Phase 0 · Run 1 summary (scoring-critical deltas)

Highest-impact gaps versus the reference notebooks:

1. **LM backend parity**: Unsloth model load + LoRA attach + attention patching (**MISSING**)
2. **Turbo DFS decode**: KV-cache logits DFS with EOS gating and pruning (**MISSING**)
3. **Artifact pipeline**: write/read per-task decoded results and run selection over them (**MISSING**)
4. **Task adaptation**: actual fine-tuning/adaptation behavior (**MISSING** in practice)

Lower-level but still important:

- Augmentation sampling protocol + key-string scheme (**PARTIAL**)
- Candidate ranking (kgmon/probmul) exists, but requires matching guess-schema + stage orchestration (**PARTIAL**)

