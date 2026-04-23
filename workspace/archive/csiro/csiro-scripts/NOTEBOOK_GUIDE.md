# Notebook Guide

Single reference for cell roles, CONFIG options, paths, and run order. The notebook uses the package (`utils.notebook`, `run_command_with_streaming`, etc.) and stays lean: CONFIG in Cell 0, `_run_cell_X` + `run_notebook_cell` in each pipeline cell.

---

## Cell 0: Setup and Configuration (REQUIRED)

Run first. Sets `sys.path`, imports, and central CONFIG.

### Paths

- **scripts_path**: Where the competition scripts package lives.
  - **Kaggle**: `/kaggle/input/<COMPETITION>-scripts/scripts` (e.g. `/kaggle/input/csiro-scripts/scripts`)
  - **Local**: `../<COMPETITION>-scripts/scripts` (e.g. `../csiro-scripts/scripts`)
- **Helpers**: `get_data_root_path()`, `get_output_path(relative_path)`, `get_run_py_path()` from `utils.system` (or `utils.system.io`) — resolve data root, output dir, and `run.py` for Kaggle vs local.

### Imports (from scripts_path)

- `from utils import run_command_with_streaming`
- `from utils.system import setup_environment` (and optionally `get_data_root_path`, `get_output_path`, `get_run_py_path`)
- `from utils.notebook import run_notebook_cell` (or `utils.system.notebook` if that re-export exists)
- `from config.model_constants import get_pretrained_weights_path`

### Central CONFIG

| Variable | Purpose |
|----------|---------|
| **Model** | |
| `MODEL_NAME` | Organizes results by architecture (e.g. `'dinov2'`, `'timm_efficientnet_b3'`). |
| `MODEL` | `get_pretrained_weights_path(MODEL_NAME)` — pretrained weights, not trained checkpoints. |
| `REGRESSION_MODEL_TYPE` | `'lgbm'`, `'xgboost'`, or `'ridge'` for regression-based pipelines. |
| **Dataset** | |
| `DATASET` | `'split'` (left/right splits) or `'full'` (full images). |
| **Grid (1b)** | |
| `SEARCH_TYPE` | `'defaults'`, `'quick'`, `'in_depth'`, `'thorough'`; `'focused_in_depth'` / `'focused_thorough'` require `PREVIOUS_RESULTS_FILE`. |
| `PREVIOUS_RESULTS_FILE` | `None` (auto-detect) or explicit path for focused search. |
| **Regression grid (1c)** | |
| `REGRESSION_SEARCH_TYPE` | `'defaults'`, `'quick'`, `'in_depth'`, `'thorough'`. |
| `REGRESSION_FEATURE_FILE` | e.g. `'variant_0163_features.npz'`. |
| **Training (2a, 2b, 2c)** | |
| `FRESH_TRAIN` | `True`: start fresh; `False`: resume from checkpoints. |
| `EXPORT_ONLY` | `True`: skip training, only export; `False`: train (or resume). |
| `SELECTED_VARIANT_ID` | (2a) `None` = best CV; or e.g. `'variant_0001'`. |
| `FEATURE_EXTRACTION_MODEL` | (2b, 2c) e.g. `'dinov2_base'`. |
| `DATA_MANIPULATION_COMBO` | (2b, 2c) e.g. `'combo_63'` or `None` (combo_00). |
| `EXTRACT_FEATURES` | (2b, 2c) `True` = extract from scratch; `False` = load from cache. |
| `REGRESSION_MODEL_VARIANT_ID` | (2b) `None` = best; or specific variant. |
| `REGRESSION_MODEL_IDS` | (2c) List of `model_id` from gridsearch, e.g. `["080","083"]`. |
| **Submission (3a, 3b)** | |
| `SUBMISSION_MODEL_PATH` | `None` (auto), explicit path, or working-dir priority. |
| **Ensembles / stacking (4a, 4b, 5a–5c)** | |
| `REGRESSION_ENSEMBLE_CONFIG` | (4b) `model_types`, `model_versions`, `method`, `score_type`. |
| `STACKING_CONFIG` | (5a) Base models, `model_versions`, `meta_model_alpha`, `n_folds`. |
| `STACKING_ENSEMBLE_CONFIG` | (5b) `model_types`, `ensemble_configs` per type, `meta_model_alpha`, `n_folds`. |
| `HYBRID_STACKING_CONFIG` | (5c) `regression_ensembles`, `end_to_end_ensembles`, `meta_model_alpha`, `n_folds`. |

### RUN_CELLS

Dict `{ '1a', '1b', '1c', '2a', '2b', '2c', '3a', '3b', '4a', '4b', '5a', '5b', '5c' }` → `True`/`False`. Set to `True` only for cells you want to run.

### Bootstrap

- `setup_environment(model_name=MODEL, download_weights=False)`
- `print("Setup complete. See NOTEBOOK_GUIDE.md.")` (optional)

---

## Cells 1a–1c (ONLINE)

Need internet/GPU and data. Run on Kaggle or equivalent.

### 1a: Dataset Grid Search

- **Inputs**: `MODEL`, `DATASET`.
- **Outputs**: `outputs/dataset_grid_search_{dataset_type}/dataset_gridsearch_{dataset_type}_results.json` (and logs).
- **When**: To find best preprocessing/augmentation combo before hyperparameter or end-to-end training.

### 1b: Hyperparameter Grid Search

- **Inputs**: `MODEL`, `DATASET`, `SEARCH_TYPE`, `PREVIOUS_RESULTS_FILE` (for `focused_*`).
- **Outputs**: `outputs/hyperparameter_grid_search_{dataset_type}/hyperparameter_gridsearch_{dataset_type}_results.json`, `hyperparameter_grid_search_output.log`.
- **When**: After 1a (or with fixed dataset config) to tune training hyperparameters. `focused_*` requires `PREVIOUS_RESULTS_FILE`.

### 1c: Regression Hyperparameter Tuning

- **Inputs**: `REGRESSION_FEATURE_FILE`, `REGRESSION_MODEL_TYPE`, `REGRESSION_SEARCH_TYPE`, `get_data_root_path()`.
- **Outputs**: Regression grid search results (see package for exact paths).
- **When**: After feature extraction; to tune LGBM/XGBoost/Ridge on cached features.

---

## Cells 2a–2c (ONLINE for training, OFFLINE for export-only)

### 2a: End-to-End Train and Export

- **Inputs**: `MODEL`, `MODEL_NAME`, `DATASET`, `FRESH_TRAIN`, `EXPORT_ONLY`, `SELECTED_VARIANT_ID`; `results_file` from `detect_train_export_mode(DATASET, MODEL_NAME, FRESH_TRAIN)`.
- **Outputs**: Exported model (e.g. `best_model/`). Uses best variant from grid search unless `SELECTED_VARIANT_ID` is set.
- **When**: After 1a+1b for full training; or with `EXPORT_ONLY=True` to export an already-trained model.

### 2b: Feature Extraction + Regression Train + Export

- **Inputs**: `MODEL`, `FEATURE_EXTRACTION_MODEL`, `REGRESSION_MODEL_TYPE`, `DATASET`, `DATA_MANIPULATION_COMBO`, `EXTRACT_FEATURES`, `FRESH_TRAIN`, `EXPORT_ONLY`, `REGRESSION_MODEL_VARIANT_ID`.
- **Outputs**: Exported regression model. Does not require 1a/1b for feature extraction; uses pretrained feature extractor.
- **When**: Two-stage pipeline: extract features (or load from cache), then train and export regression head.

### 2c: Multi-Variant Regression Training

- **Inputs**: `MODEL`, `FEATURE_EXTRACTION_MODEL`, `REGRESSION_MODEL_TYPE`, `REGRESSION_MODEL_IDS`, `DATASET`, `EXTRACT_FEATURES`, `FRESH_TRAIN`, `DATA_MANIPULATION_COMBO`.
- **Outputs**: One exported regression model per `model_id` in `REGRESSION_MODEL_IDS`.
- **When**: To train several regression variants from 1c for later ensembling.

---

## Cells 3a–3b (OFFLINE)

For submission only. Assume data and models are available (e.g. from Kaggle inputs).

### 3a: End-to-End Submission

- **Inputs**: `MODEL`, `MODEL_NAME`, `DATASET`, `SUBMISSION_MODEL_PATH` (or auto-detect via `detect_submission_model_path(..., model_type='end_to_end')`).
- **Outputs**: `submission.csv` (or package default).

### 3b: Regression Model Submission

- **Inputs**: `REGRESSION_MODEL_TYPE`, `DATASET`, `SUBMISSION_MODEL_PATH` (or auto-detect, `model_type='regression'`). Feature-extractor name comes from model metadata.
- **Outputs**: `submission.csv`.

---

## Cells 4a–4b, 5a–5c (OFFLINE)

Ensemble and stacking. Models are assumed uploaded/available at configured paths or versions.

### 4a: Ensemble (End-to-End)

- **Cell-local**: `MODEL_CONFIGS` (path → weight), `SCORE_TYPE`, `METHOD`. Build `MODEL_PATHS` and optionally `SUBMISSION_SCORES` from them.
- **Outputs**: `submission.csv` from ensembled end-to-end models.

### 4b: Regression Ensemble

- **Inputs**: `REGRESSION_ENSEMBLE_CONFIG` (`model_types`, `model_versions`, `method`, `score_type`), `DATASET`.
- **Outputs**: `submission.csv` from ensembled regression models.

### 5a: Stacking (Single Models)

- **Inputs**: `STACKING_CONFIG` (base `model_types`, `model_versions`, `meta_model_alpha`, `n_folds`), `DATASET`.
- **Outputs**: `submission.csv` from stacked base models.

### 5b: Stacking (Ensemble Models)

- **Inputs**: `STACKING_ENSEMBLE_CONFIG` (per-type `ensemble_configs`, `meta_model_alpha`, `n_folds`), `DATASET`.
- **Outputs**: `submission.csv` from stacking ensemble base models.

### 5c: Hybrid Stacking (Regression + End-to-End)

- **Inputs**: `HYBRID_STACKING_CONFIG` (`regression_ensembles`, `end_to_end_ensembles`, `meta_model_alpha`, `n_folds`), `DATASET`.
- **Outputs**: `submission.csv` from stacking regression and end-to-end ensembles.

---

## Typical Run Order

1. **Setup**: Cell 0.
2. **Grid (choose one path)**:
   - 1a → 1b (dataset then hyperparameters for end-to-end), or
   - 1c (regression only, with pre-extracted features).
3. **Training (choose one)**:
   - 2a (end-to-end), or
   - 2b (feature extraction + regression), or
   - 2c (multi-variant regression).
4. **Submission (choose one or more)**:
   - 3a or 3b (single model), or
   - 4a, 4b, 5a, 5b, 5c (ensembles/stacking).

---

## Paths (Kaggle vs Local)

- **Kaggle**: Data and models under `/kaggle/input/...`; scripts e.g. `/kaggle/input/csiro-scripts/scripts`; output under `/kaggle/working/` (or as chosen by `get_output_path`).
- **Local**: Scripts e.g. `../csiro-scripts/scripts`; `get_data_root_path()` and `get_output_path()` follow contest/path configuration.
- Use `get_data_root_path()`, `get_output_path(relative_path)`, `get_run_py_path()` instead of hardcoding.
