# __init__.py
# Data preparation package (essential operations)
#
# Provides essential data preparation operations that MUST be applied before training.
# These operations are required to prepare data for model input and cannot be skipped.
#
# Purpose:
# This package contains operations that are fundamental to the data pipeline. Without
# these operations, the model cannot process the data correctly. Examples include:
# - Loading data from files (CSV, images)
# - Resizing images to model input size
# - Normalizing pixel values
# - Creating PyTorch Dataset instances
#
# Sub-packages:
# - loading: CSV and image file I/O with comprehensive error handling.
#   Supports batch loading with progress tracking and validation.
#   Functions: load_csv, load_jpg, aggregate_train_csv
# - preprocessing: Essential preprocessing operations (resize, normalize).
#   These are always applied in transform pipelines, regardless of config.
#   Functions: resize, normalize
# - streaming: PyTorch Dataset classes for training and inference.
#   Includes standard Dataset and memory-efficient IterableDataset implementations.
#   Classes: StreamingBiomassDataset, StreamingBiomassSplitDataset
#
# Boundary Rules:
# - DO put here: File I/O, essential transforms (resize/normalize), dataset classes
# - DO NOT put here: Optional enhancements, augmentation, configurable transforms
#   (Use optional for those)
#
# Note: Optional preprocessing operations (contrast_enhancement, noise_reduction)
# are in nonessential.preprocessing, not here.

