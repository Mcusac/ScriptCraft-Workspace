# Scripts
## run.py
  - main runner file
  - should only need to call this file with proper cli commands to use any and all logic in scripts properly

## cli package
  - contains all CLI-related logic for command routing and execution
  - command_router.py: routes CLI commands to appropriate pipeline functions using command pattern
  - commands.py: defines Command enum with all valid CLI commands (train, test, grid_search, etc.)
  - provides unified interface for executing all pipelines via run.py

## config package
  - contains all configuration definitions and constants - single source of truth for all configurable values
  - config.py: main Config dataclass with nested sub-configs (ModelConfig, TrainingConfig, DataConfig, CVConfig, etc.)
  - evaluation_constants.py: target weights, target order, and evaluation constants
  - model_constants.py: model-specific constants and pretrained weight paths
  - path_constants.py: default paths and image size constants
  - progress_config.py: progress tracking configuration
  - eliminates magic numbers - all values are centralized and configurable

## contest package
  - contains contest abstraction system for making the codebase reusable across different competitions
  - abstracts contest-specific logic (targets, data schema, post-processing, paths) into pluggable implementations
  - base.py: abstract base classes (ContestConfig, ContestDataSchema, ContestPostProcessor, ContestPaths)
  - registry.py: contest registration and detection system with auto-registration
  - csiro/: CSIRO-specific contest implementation
    - config.py: CSIRO contest configuration (target weights, order, derived targets)
    - data_schema.py: CSIRO data schema (CSV columns, sample ID format)
    - paths.py: CSIRO path constants (Kaggle dataset names, local paths)
    - post_processing.py: CSIRO post-processing logic (constraint enforcement)
  - purpose: enables codebase reuse across multiple competitions by isolating contest-specific logic

## dataset_manipulation package
  - contains all logic related to "manipulating" the training data
  - includes essential manipulation (things that are always needed to prepare the data)
  - contains optional manipulation techniques that can be used if desired or if the situation calls for it (a specific model needs it)

 ### essential sub-package
   - contains logic that is ALWAYS required for data preparation and loading
   - these operations are mandatory and cannot be skipped

  #### streaming sub-package
    - contains streaming dataset implementations using PyTorch IterableDataset
    - base_streaming_dataset.py: base class for memory-efficient streaming (loads images on-demand)
    - streaming_biomass_dataset.py: full image dataset implementation
    - streaming_biomass_split_dataset.py: left/right split dataset implementation
    - purpose: avoid loading all images into memory at once (critical for large datasets)

  #### loading sub-package
    - contains data loading and aggregation utilities
    - aggregate_train.py: aggregates train.csv from 5 rows per image to 1 row per image
    - load_csv.py: CSV loading utilities
    - load_jpg.py: image loading utilities
    - purpose: prepare data structures needed for dataset creation
  
  #### preprocessing sub-package
    - contains essential preprocessing transforms that are always applied
    - normalization.py: ImageNet normalization (always applied automatically)
    - resizing.py: image resizing transforms
    - purpose: standard preprocessing required for model training (normalization, resizing)

 ### nonessential sub-package
   - contains OPTIONAL data manipulation techniques that can be selectively applied
   - these techniques are chosen via config (preprocessing_list, augmentation_list) for grid search
   - constants.py: defines available preprocessing/augmentation techniques and TTA variants
   - defaults.py: default configurations
   - kernel_utils.py: utility functions

  #### data_augmentation package
    - contains augmentation technique implementations (applied during training)
    - geometric_transformations.py: rotations, flips, etc.
    - color_jittering.py: color space augmentations
    - blurring.py: blur-based augmentations
    - noise_addition.py: noise injection augmentations
    - purpose: add data variations to improve model generalization

  #### preprocessing sub-package
    - contains optional preprocessing techniques (applied before ToTensor)
    - contrast_enhancement.py: histogram equalization and contrast adjustments
    - noise_reduction.py: denoising techniques (gaussian blur, etc.)
    - purpose: optional image enhancement techniques for grid search experimentation

 ### transforms sub-package
   - contains transform factory and composition logic for building complete transform pipelines
   - located at dataset_manipulation/transforms (orchestrates both essential and nonessential transforms)
   - transform_factory.py: main factory for creating train/val/test/TTA transform pipelines from config
   - transform_composition.py: composes preprocessing, augmentation, and normalization into complete pipelines
   - preprocessing_builders.py: registry of preprocessing transform builders
   - augmentation_builders.py: registry of augmentation transform builders
   - tta_builders.py: builds test-time augmentation transform pipelines
   - tta_transforms.py: applies TTA to predictions and averages results
   - transform_mode.py: transform mode definitions
   - purpose: orchestrates all transforms (essential + nonessential) into complete pipelines based on config

 ### utils sub-package
   - contains dataset manipulation-specific utilities (domain-specific, not cross-cutting)
   - image_utils.py: PIL/numpy image conversion utilities (pil_to_numpy, numpy_to_pil, ensure_uint8)
   - loading_utils.py: batch processing with progress tracking (batch_process_with_progress)
   - purpose: utilities specific to dataset manipulation operations
   - Note: These utilities were moved from utils/data/ to dataset_manipulation/utils/ to keep domain-specific code within the domain package

## modeling package
  - contains all model-related logic: architectures, training, evaluation, testing, and ensembling
  - organized by functional area (ensembling, evaluation, feature extraction, models, testing, training)

 ### ensembling sub-package
   - contains ensemble model logic for combining multiple model predictions
   - ensemble.py: Ensemble class for combining predictions from multiple models
   - methods.py: different ensembling methods (simple average, weighted average, etc.)
   - model_loader.py: loads multiple models for ensemble prediction
   - results_loader.py: loads results from multiple models for ensemble
   - constants.py: ensemble-related constants and configuration

 ### evaluation sub-package
   - contains evaluation metrics, loss functions, and post-processing
   - metrics.py: weighted R² calculation (matches competition formula), per-target R², RMSE, MAE
   - losses.py: loss function factory (SmoothL1Loss, MSELoss, etc.)
   - post_processing.py: biomass prediction post-processing utilities
   - Note: Evaluation constants (target definitions, weights, order) are in config/evaluation_constants.py (single source of truth)

 ### feature_extraction sub-package
   - contains feature extraction utilities for two-stage training
   - feature_extractor.py: extracts features from images using feature extraction models
   - feature_cache.py: caches extracted features to disk for reuse
   - purpose: supports feature extraction mode where CNN extracts features, then regression model predicts targets
   - note: Regression models have been moved to models/regression_head/

 ### grid_search_configs sub-package
   - contains hyperparameter grid definitions for grid search
   - parameter_grids.py: hyperparameter grids for end-to-end model training
   - regression_parameter_grids.py: hyperparameter grids for regression head models
   - result_analysis.py: utilities for analyzing grid search results
   - purpose: defines search spaces for hyperparameter optimization
   - note: Grid search execution logic is in pipelines/workflows/grid_search/

 ### models sub-package
   - contains all model implementations organized by type
   - organized into sub-packages: end_to_end and regression_head
   - __init__.py: provides unified exports for backward compatibility
   
  #### end_to_end sub-package
    - contains complete model architectures with built-in regression heads
    - base.py: BaseFeatureExtractionModel abstract base class (unified interface for all end-to-end models)
    - timm_model.py: TimmModel wrapper for timm library models (EfficientNet, etc.) with regression head
    - dinov2_model.py: DINOv2Model wrapper for DINOv2 models with regression head and feature fusion
    - weight_loader.py: pretrained weight loading utilities for timm models
    - __init__.py: create_model() factory function that creates end-to-end model instances from config
    - purpose: provides unified interface for different model architectures used in end-to-end training
  
  #### regression_head sub-package
    - contains tree-based regression models for two-stage training
    - regression_model.py: Wrapper for tree-based regression models (LGBM, XGBoost, Ridge)
    - purpose: regression models that operate on extracted features (used with feature extraction mode)

 ### testing sub-package
   - contains inference and submission generation logic organized into focused modules
   - dataloaders.py: test dataloader creation utilities
   - inference.py: core inference execution for end-to-end models
   - tta.py: test-time augmentation inference
   - validation.py: prediction shape validation utilities
   - submission.py: submission format conversion and file I/O
   - regression_inference.py: two-stage inference (feature extraction + regression)
   - all modules follow Single Responsibility Principle for better maintainability

 ### training sub-package
  - contains core training logic and cross-validation utilities
  - base_model_trainer.py: core training loop with early stopping, checkpointing, LR scheduling
  - feature_extraction_trainer.py: specialized trainer for feature extraction mode
  - trainer_factory.py: factory for creating appropriate trainer based on config
  - cv_splits.py: K-fold cross-validation splitting with optional stratification
  - training_components_factory.py: creates optimizers, schedulers, dataloaders
  - dataloader_factory.py: creates train/val dataloaders from config

 #### utils sub-package
   - contains training-specific utilities for checkpoint management and error handling
   - checkpoint.py: checkpoint save/load with DataParallel handling
   - checkpoint_cleanup.py: checkpoint cleanup for grid search (removes non-best checkpoints)
   - checkpoint_scores.py: score extraction from checkpoints
   - oom_handling.py: out-of-memory error handling and retry logic
   - results.py: training results creation and management
   - purpose: utilities specific to training operations (domain-specific, not cross-cutting)
 
## pipelines package
  - contains orchestration logic for complete ML workflows
  - organized into atomic operations and composite workflows

 ### atomic sub-package
   - contains single-purpose, reusable pipeline operations
   - train_only.py: train_pipeline() - trains a model (used by workflows and grid search)
   - test_only.py: test_pipeline() - runs inference and generates submission
   - export_model.py: export_model_pipeline() - exports trained model for download/submission
   - purpose: building blocks that can be composed into larger workflows

 ### workflows sub-package
   - contains composite pipelines that orchestrate multiple atomic operations
   - train_test.py: train_test_pipeline() - trains then tests (atomic.train + atomic.test)
   - train_and_export.py: train_and_export_pipeline() - trains then exports (atomic.train + atomic.export)
   - submit_best_variant.py: submit_best_variant_pipeline() - finds best variant and submits
   - submit_lightweight.py: submit_lightweight_pipeline() - lightweight submission from uploaded model
   - ensemble_pipeline.py: ensemble_pipeline() - creates ensemble from multiple models
   - contains grid_search sub-package for grid search workflows
   - purpose: complete end-to-end workflows for common ML tasks

  #### grid_search sub-package
    - contains shared infrastructure and implementation packages for different grid search types
    - all grid search types inherit from GridSearchBase and use template method pattern
    - common logic (setup, loading, saving, cleanup) centralized in base class
    - eliminates code duplication and follows DRY, SOLID principles

   ##### base sub-package
     - contains base.py with GridSearchBase abstract base class
     - provides common infrastructure for all grid search types:
       - environment setup (seed, device, directories)
       - result tracking and saving
       - checkpoint cleanup
       - progress tracking
       - template method pattern with run_grid_search() for main loop
     - all grid search implementation classes inherit from this base class
     - eliminates ~500 lines of duplication across grid search types

   ##### utils sub-package
     - contains organized utilities shared across all grid search types
     - constants.py: shared constants for all grid search types
     - helpers.py: common helper functions (variant key creation, preprocessing/augmentation extraction, etc.)
     - hyperparameters.py: hyperparameter utility functions (default hyperparameters, config application, etc.)

   ##### dataset_grid_search package
     - contains all logic for dataset grid search
     - finds best combination of optional/nonessential data manipulation techniques
     - nonessential techniques are found in the dataset_manipulation/nonessential package
     - structure:
       - grid_search_class.py: DatasetGridSearch class inheriting from GridSearchBase
       - pipeline.py: dataset_grid_search_pipeline() main entry point
       - execution.py: run_single_variant() logic for running individual variants
       - setup.py: setup utilities (deprecated functions removed, now uses base class methods)

   ##### hyperparameter_grid_search package
     - unified package containing all hyperparameter grid search implementations
     - organized into three sub-packages: base, end_to_end, and regression_head
     - both end-to-end and regression head searches share common hyperparameter infrastructure

    ###### base sub-package
      - contains hyperparameter_base.py with HyperparameterGridSearchBase abstract base class
      - provides common infrastructure for hyperparameter-specific logic:
        - parameter grid management
        - combination generation
        - hyperparameter application helpers
      - optional intermediate base class for sharing hyperparameter-related functionality

    ###### end_to_end sub-package
      - contains all logic for end-to-end hyperparameter grid searching
      - finds best hyperparameters for chosen model by searching through parameter combinations
      - uses fixed dataset configuration from saved model metadata
      - structure:
        - grid_search_class.py: HyperparameterGridSearch class inheriting from GridSearchBase
        - pipeline.py: hyperparameter_grid_search_pipeline() main entry point
        - execution.py: execute_single_combination() logic for running individual combinations
        - setup.py: setup_hyperparameter_grid_search() and related utilities

    ###### regression_head sub-package
      - contains all logic for hyperparameter grid searching specifically for regression head models
      - used after feature extraction to tune regression model hyperparameters
      - structure:
        - grid_search_class.py: RegressionGridSearch class inheriting from GridSearchBase
        - pipeline.py: regression_grid_search_pipeline() main entry point
        - execution.py: execute_single_regression_combination() logic for running individual combinations
        - setup.py: setup_regression_grid_search() and related utilities
      - Note: This is the actual implementation. The standalone regression_grid_search/ package was removed as duplicate during refactoring.

## utils package
  - contains cross-cutting utility/helper functions used across multiple packages
  - organized into domain-specific subpackages to maintain clear boundaries
  - purpose: provides reusable infrastructure while avoiding circular dependencies
  - rationale: utilities are cross-cutting concerns used by config, data, modeling, and pipelines

 ### config sub-package
   - configuration utilities for validation and updating
   - config_validator.py: validates config structure and CLI arguments
   - config_updater.py: applies config updates (preprocessing, augmentation, overrides)
   - config_utils.py: orchestrator for updating config from CLI arguments

 ### data sub-package
   - data-related utilities for preprocessing and caching (cross-cutting)
   - preprocessing_utils.py: parses and validates preprocessing/augmentation lists
   - dataset_cache_utils.py: dataset variant caching and grid generation
   - Note: image_utils.py and loading_utils.py moved to dataset_manipulation/utils/ (domain-specific)

 ### dataset_manipulation/utils sub-package
   - dataset manipulation-specific utilities (domain-specific, not cross-cutting)
   - image_utils.py: PIL/numpy image conversion utilities
   - loading_utils.py: batch processing with progress tracking
   - purpose: utilities specific to dataset manipulation operations, moved from utils/data to avoid circular dependencies

 ### notebook sub-package
   - Jupyter notebook helper functions and command handlers
   - commands/: command builders for notebook cells (ensemble, grid_search, submission)
   - descriptions/: description builders for notebook cells
   - grid_search/: grid search utilities for notebooks
   - handlers/: result handlers for notebook cells
   - core.py: core foundation utilities for notebook cells
   - train_export.py: train/export mode detection utilities

 ### system sub-package
   - foundational system-level utilities used across entire codebase
   - environment/: device detection, seed management, weight cache management, environment setup
   - infrastructure/: logging, error handling, command execution, progress tracking
   - io/: file operations (JSON load/save), path resolution (Kaggle vs local), path validation
   - memory/: memory management (cleanup, recovery)
   - Note: notebook utilities moved to utils/notebook/ (notebook-specific, not foundational)

 ### modeling sub-package
   - Note: Model-related utilities moved to modeling/utils/ (domain-specific, not cross-cutting)
   - modeling/utils/ contains:
     - batch_processing.py: batch processing utilities for model inference
     - ensemble_diagnostics/: ensemble analysis utilities (diagnostics.py, score_analysis.py, weight_calculation.py)
     - export/: model export operations (handlers.py, metadata_builder.py, metadata_loader.py, operations.py)
     - finding/: model checkpoint finding utilities (base.py, finders.py, strategies.py)
     - metadata/: metadata utilities (data_manipulation_loader.py, regression_metadata_utils.py)
     - results/: results and variant utilities (best_variant.py, results.py, variants.py)
     - submission.py: submission file utilities
     - type_definitions.py: type definitions for modeling operations

## tests package
  - contains tests to verify the codebase is working correctly
  - test_imports.py: modular import testing framework (155 lines, refactored from 593)
  - import_testing/: modular testing framework
    - discoverer.py: ModuleDiscoverer class for module discovery
    - tester.py: ImportTester class for testing imports
    - classifier.py: ErrorClassifier for categorizing errors
    - reporter.py: TestReporter for formatted output
  - README.md: test package documentation
  - purpose: verifies codebase imports work correctly and detects missing dependencies
  - note: backward compatibility code removed, now uses shared utilities from tools/core
