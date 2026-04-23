# CSIRO Image2Biomass Prediction Competition

Predict pasture biomass from images using deep learning.

## Overview

This project implements a solution for the [CSIRO Image2Biomass Prediction](https://www.kaggle.com/competitions/csiro-biomass) Kaggle competition. The goal is to predict five biomass components from pasture images:

- **Dry_Green_g**: Dry green vegetation (excluding clover)
- **Dry_Dead_g**: Dry dead material
- **Dry_Clover_g**: Dry clover biomass
- **GDM_g**: Green dry matter (Green + Clover)
- **Dry_Total_g**: Total dry biomass (GDM + Dead)

## Strategy

Based on a reference implementation achieving 0.54 score:

- **Framework**: PyTorch with `timm` library
- **Model**: EfficientNet (B0-B4) pretrained on ImageNet
- **Prediction**: Model outputs 3 targets directly (Dry_Green_g, Dry_Clover_g, Dry_Dead_g), derives GDM_g and Dry_Total_g
- **Training**: 5-fold cross-validation, SmoothL1Loss, AdamW optimizer
- **Evaluation**: Weighted R² metric matching competition formula

## Project Structure

```
scripts/
├── cli/                    # Command-line interface and routing
│   └── command_router.py   # Routes CLI commands to pipelines
├── config/                 # Configuration management
│   └── config.py           # Dataclass-based configuration
├── data/                   # Data loading, preprocessing, and augmentation
│   ├── loading/            # CSV and image loading utilities
│   │   ├── load_csv.py     # CSV file loading with error handling
│   │   ├── load_jpg.py     # Image loading (PIL-based)
│   │   ├── aggregate_train.py  # Aggregate train.csv (5 rows → 1 row per image)
│   │   └── utils.py        # Path validation and batch processing
│   ├── preprocessing/      # Image preprocessing operations
│   │   ├── resizing.py     # Image resizing
│   │   ├── normalization.py # ImageNet normalization
│   │   ├── contrast_enhancement.py # Histogram equalization, CLAHE
│   │   ├── noise_reduction.py # Gaussian blur, bilateral, median filtering
│   │   └── utils.py        # PIL/numpy conversion utilities
│   ├── data_augmentation/  # Training-time augmentations
│   │   ├── blurring.py     # Gaussian blur augmentation
│   │   ├── color_jittering.py # Color jitter augmentation
│   │   ├── geometric_transformations.py # Rotation, translation, scaling, shearing
│   │   └── noise_addition.py # Gaussian noise addition
│   └── transforms/         # Transform pipeline composition
│       └── transform_factory.py # Factory for building train/val transform pipelines
├── datasets/               # PyTorch Dataset classes
│   └── biomass_dataset.py  # Main dataset class for training/inference
├── evaluation/             # Metrics and loss functions
│   ├── metrics.py          # Weighted R² calculation (competition metric)
│   ├── losses.py           # Loss function factory
│   ├── constants.py        # Target weights, order, and definitions
│   └── utils.py            # Array validation utilities
├── models/                 # Model architectures
│   └── timm_model.py       # Timm model wrapper with custom regression head
├── training/               # Training logic
│   ├── base_model_trainer.py # Core training loop with early stopping, checkpointing
│   └── training_test_split.py # K-fold cross-validation splitting
├── testing/                # Inference and prediction
│   └── inference.py        # Test set inference and submission generation
├── pipelines/              # High-level pipeline orchestration
│   ├── train_only.py       # Training pipeline
│   ├── test_only.py        # Inference pipeline
│   ├── train_test.py       # Train then test pipeline
│   ├── grid_search.py      # Hyperparameter grid search
│   ├── dataset_grid_search.py # Preprocessing/augmentation grid search
│   ├── submit_best_variant.py # Submit using best variant from grid search
│   ├── submit_lightweight.py # Lightweight submission (offline, Pipeline A)
│   ├── train_and_export.py # Train and export model (Pipeline C)
│   └── export_model.py     # Export existing trained model
├── utils/                  # Shared utility functions (organized into subpackages)
│   ├── training/           # Training-related utilities
│   │   ├── checkpoint_utils.py # Model checkpoint save/load
│   │   ├── checkpoint_cleanup.py # Grid search checkpoint cleanup
│   │   ├── fold_utils.py   # Best fold selection utilities
│   │   └── training_results_utils.py # Training results management
│   ├── modeling/          # Model-related utilities
│   │   ├── model_export_utils.py # Model export for submission
│   │   └── best_variant_utils.py # Best variant selection from grid search
│   ├── data/              # Data-related utilities
│   │   ├── preprocessing_utils.py # Preprocessing/augmentation config parsing
│   │   └── dataset_cache_utils.py # Dataset variant caching
│   ├── system/            # System-level utilities
│   │   ├── logging_utils.py # Logging configuration
│   │   ├── seed_utils.py  # Random seed management
│   │   ├── device_utils.py # GPU/CPU device management
│   │   ├── path_utils.py  # Directory creation utilities
│   │   └── environment_utils.py # Environment setup (Kaggle/local detection)
│   ├── config/            # Configuration utilities
│   │   └── config_utils.py # Configuration loading and updates
│   ├── validation.py      # General validation utilities
│   ├── command_utils.py   # Subprocess command execution
│   ├── view_results_utils.py # Results viewing utilities
│   └── weight_cache_utils.py # Pretrained weight caching
├── grid_search/            # Grid search parameter definitions
│   └── __init__.py         # Parameter grid generators
└── run.py                  # Main entry point (CLI runner)
```

## Installation

### Quick Start

```bash
# Recommended: Use a virtual environment (especially on Windows)
python -m venv venv
venv\Scripts\activate  # On Windows
# source venv/bin/activate  # On Linux/Mac

pip install -r requirements.txt
```

### Windows Users

If you encounter path length errors during installation, see [INSTALLATION_TROUBLESHOOTING.md](INSTALLATION_TROUBLESHOOTING.md) for solutions.

**Quick fix**: Create a virtual environment in a short path:
```bash
python -m venv C:\venv\csiro
C:\venv\csiro\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Command-Line Interface

All functionality is accessed through `run.py` with subcommands:

#### Training

Train a model with cross-validation:

```bash
python scripts/run.py train \
    --data-root /path/to/data \
    --model efficientnet_b3 \
    --preprocessing resize,normalize \
    --data-augmentation geometric_transformations,color_jittering \
    --batch-size 32 \
    --lr 0.001 \
    --log-file outputs/training.log
```

#### Testing/Inference

Generate submission from trained model:

```bash
python scripts/run.py test \
    --data-root /path/to/data \
    --model efficientnet_b3 \
    --model-path models/best_model.pth
```

#### Train and Test

Train model then immediately test with best fold:

```bash
python scripts/run.py train_test \
    --data-root /path/to/data \
    --model efficientnet_b3
```

#### Grid Search

**Hyperparameter Grid Search:**
```bash
python scripts/run.py grid_search \
    --data-root /path/to/data \
    --model efficientnet_b3 \
    --search-type quick  # or 'in_depth'
```

**Dataset Grid Search (Preprocessing/Augmentation):**
```bash
python scripts/run.py dataset_grid_search \
    --data-root /path/to/data \
    --model efficientnet_b3 \
    --log-file outputs/grid_search.log
```

#### Model Export and Submission

**Train and Export (Pipeline C):**
```bash
python scripts/run.py train_and_export \
    --data-root /path/to/data \
    --model efficientnet_b3 \
    --results-file outputs/dataset_grid_search/dataset_gridsearch_results.json \
    --export-dir /kaggle/working/best_model
```

**Export Existing Model:**
```bash
python scripts/run.py export_model \
    --data-root /path/to/data \
    --model efficientnet_b3 \
    --variant-id variant_0067 \
    --export-dir /kaggle/working/best_model
```

**Submit Best Variant:**
```bash
python scripts/run.py submit_best \
    --data-root /path/to/data \
    --model efficientnet_b3 \
    --results-file outputs/dataset_grid_search/dataset_gridsearch_results.json
```

**Lightweight Submission (Pipeline A - Offline):**
```bash
python scripts/run.py submit \
    --data-root /path/to/data \
    --model efficientnet_b3 \
    --model-path /kaggle/input/model/best_model.pth \
    --metadata-path /kaggle/input/model/model_metadata.json
```

#### Utilities

**Cleanup Grid Search Checkpoints:**
```bash
python scripts/run.py cleanup_grid_search \
    --model-dir models/ \
    --results-file outputs/dataset_grid_search/dataset_gridsearch_results.json \
    --keep-top 20
```

### Common Arguments

All commands support these common arguments:

- `--data-root`: Data root directory (required for most commands)
- `--model`: Timm model name (e.g., `efficientnet_b0`, `efficientnet_b3`)
- `--preprocessing`: Comma-separated preprocessing list (e.g., `resize,normalize,contrast_enhancement`)
- `--data-augmentation`: Comma-separated augmentation list (e.g., `geometric_transformations,color_jittering,blurring`)
- `--log-file`: Optional log file path for output

### Notebook Usage (Kaggle)

The `notebook.ipynb` provides a Kaggle-friendly interface using the same `run.py` commands:

**Cell 1: Setup (Required)**
- Environment detection (Kaggle vs local)
- Weight download setup
- Path configuration

**Cell 2a: Pipeline A - Submission (OFFLINE)**
- Lightweight submission for Kaggle submission button
- Works with uploaded model checkpoint + metadata
- No internet required

**Cell 2b: Pipeline B - Grid Search (ONLINE)**
- Comprehensive dataset grid search
- Tests all preprocessing/augmentation combinations
- Results saved incrementally

**Cell 2c: Pipeline C - Train & Export (ONLINE)**
- Train best model and export for submission
- Can use best variant from grid search
- Exports model + metadata + results.json

## Architecture Overview

### Package Responsibilities

- **`cli/`**: Command routing - dispatches CLI commands to appropriate pipelines
- **`config/`**: Configuration management - dataclass-based config with validation
- **`data/`**: Data operations
  - `loading/`: File I/O (CSV, images) with error handling
  - `preprocessing/`: Image preprocessing (resize, normalize, contrast, noise reduction)
  - `data_augmentation/`: Training-time augmentations (geometric, color, blur, noise)
  - `transforms/`: Transform pipeline composition (factory pattern)
- **`datasets/`**: PyTorch Dataset classes for training/inference
- **`evaluation/`**: Metrics (weighted R²) and loss functions
- **`models/`**: Model architectures (timm wrapper)
- **`training/`**: Training logic (trainer, CV splits)
- **`testing/`**: Inference and submission generation
- **`pipelines/`**: High-level orchestration (combines training/testing/grid search)
- **`utils/`**: Shared utilities (logging, paths, checkpoints, etc.)
- **`grid_search/`**: Parameter grid definitions

### Design Principles

- **DRY (Don't Repeat Yourself)**: Common patterns abstracted into utilities
- **SOLID**: Single responsibility per package/class, clear interfaces
- **YAGNI (You Ain't Gonna Need It)**: No unnecessary abstractions
- **Separation of Concerns**: Clear boundaries between packages
- **Fail Fast**: Clear error messages and validation

### Key Abstractions

- **Transform Factory**: Builds train/val transform pipelines from config
- **Pipeline Pattern**: High-level workflows (train, test, grid search)
- **Command Router**: Dispatches CLI commands to pipelines
- **Config System**: Dataclass-based configuration with validation
- **Checkpoint System**: Model save/load with metadata

## Configuration

Configuration is managed through `scripts/config/config.py` using dataclasses:

- **ModelConfig**: Model architecture, pretrained weights, input size
- **TrainingConfig**: Batch size, learning rate, epochs, early stopping
- **DataConfig**: Data paths, preprocessing/augmentation lists, image size
- **CVConfig**: Cross-validation settings (n_folds, shuffle, random_state)
- **PathConfig**: Output directories (model, output, log)
- **EvaluationConfig**: Metric and loss function settings
- **DeviceConfig**: GPU/CPU device preferences

Configuration can be:
- Set via CLI arguments (see `--preprocessing`, `--data-augmentation`, etc.)
- Loaded from JSON files
- Modified programmatically

## Evaluation Metric

The competition uses a weighted R² score computed over all (image, target) pairs:

- **Weights**: Dry_Green_g (0.1), Dry_Dead_g (0.1), Dry_Clover_g (0.1), GDM_g (0.2), Dry_Total_g (0.5)
- **Formula**: R² = 1 - (RSS / TSS) where both are weighted sums
- **Implementation**: `evaluation/metrics.py` - matches competition formula exactly

## Development Guidelines

### Code Standards

- **Type Hints**: All functions must have complete type hints
- **Docstrings**: All public functions/classes must have docstrings
- **Error Handling**: Use appropriate exception types with clear messages
- **Logging**: Use structured logging with appropriate levels
- **Validation**: Validate inputs at function boundaries

### Adding New Features

1. **New Preprocessing**: Add to `data/preprocessing/` with corresponding transform builder
2. **New Augmentation**: Add to `data/data_augmentation/` with validation utilities
3. **New Pipeline**: Add to `pipelines/` and register in `cli/command_router.py`
4. **New Utility**: Add to appropriate `utils/` file or create new one if needed

### Testing

- Run individual commands to verify functionality
- Check logs for errors and warnings
- Verify checkpoint resumption works correctly
- Test grid search resumability

## License

This project is for the Kaggle competition. See competition rules for details.
