# Feature Extraction Cache Files

This directory contains pre-extracted features from images using various model and data manipulation combinations.

## Naming Convention

Feature files follow the naming pattern:

```
variant_{model_id}{combo_numeric}_features.npz
```

Where:
- `model_id`: Two-digit model identifier (e.g., `01`, `02`)
- `combo_numeric`: Two-digit combo identifier extracted from combo_id (e.g., `00`, `01`)
- Example: `variant_0100_features.npz` = model 01 (dinov2_base) + combo_000

## Model ID Mapping

| Model ID | Model Name |
|----------|-----------|
| `01` | dinov2_base |
| `02` | timm_efficientnet_b3 |

To add new models, update `MODEL_ID_MAP` in `csiro-scripts/scripts/config/model_constants.py`.

## Combo ID Mapping

Combo IDs reference data manipulation combinations stored in `csiro-metadata/data_manipulation/metadata.json`.

The numeric part of the combo_id (e.g., `combo_000` → `00`, `combo_001` → `01`) is used in the filename.

### Finding Combo ID

To find the combo_id for a specific preprocessing/augmentation combination:

1. Check `csiro-metadata/data_manipulation/metadata.json`
2. Find the entry with matching `preprocessing_list` and `augmentation_list`
3. Use the `combo_id` field (e.g., `combo_000`, `combo_001`)

### Examples

- `variant_0100_features.npz`
  - Model: `dinov2_base` (ID: `01`)
  - Combo: `combo_000` (numeric: `00`)
  - Preprocessing: `[]` (empty)
  - Augmentation: `[]` (empty)

- `variant_0101_features.npz`
  - Model: `dinov2_base` (ID: `01`)
  - Combo: `combo_001` (numeric: `01`)
  - Preprocessing: `[]` (empty)
  - Augmentation: `["blurring"]`

- `variant_0200_features.npz`
  - Model: `timm_efficientnet_b3` (ID: `02`)
  - Combo: `combo_000` (numeric: `00`)
  - Preprocessing: `[]` (empty)
  - Augmentation: `[]` (empty)

## File Structure

Each `.npz` file contains:
- `all_features`: Features array of shape (N_total, feat_dim)
- `all_targets`: Targets array of shape (N_total, 3)
- `fold_assignments`: Fold assignments array of shape (N_total,)
- `metadata`: JSON string with cache information

## Usage

Feature files are automatically discovered and used by the feature extraction pipeline. The system searches in priority order:

1. `/kaggle/input/csiro-extracted-features/` (persistent, highest priority)
2. `/kaggle/working/features/` (temporary, fallback)

## Generating Feature Files

Feature files are generated automatically during training when:
- `config.model.feature_extraction_mode = True`
- `config.model.extract_features = True`

The system will:
1. Extract model_id from `config.model.feature_extraction_model_name`
2. Get or create combo_id from `config.data.preprocessing_list` and `config.data.augmentation_list`
3. Generate filename using `generate_feature_filename(model_id, combo_id)`
4. Save features to the appropriate directory

