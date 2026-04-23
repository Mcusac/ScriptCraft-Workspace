# __init__.py
# Dataset manipulation package
# 
# Provides dataset loading, preprocessing, augmentation, and transform composition.
# 
# Package Organization:
# This package is split into two main sub-packages based on necessity:
#
# - essential: Essential data preparation operations (ALWAYS required)
#   These operations are necessary to prepare data for model input. They must be
#   applied before training/inference can proceed.
#   - loading: CSV and image file I/O with comprehensive error handling
#   - preprocessing: Essential preprocessing operations (resize, normalize)
#   - streaming: PyTorch Dataset classes for training and inference
#
# - nonessential: Optional data manipulation operations (CONFIGURABLE)
#   These operations enhance data quality or provide augmentation, but are not
#   required for basic functionality. They are controlled via config flags.
#   - preprocessing: Optional preprocessing (contrast_enhancement, noise_reduction)
#   - data_augmentation: Training-time augmentations (geometric, color, blur, noise)
#   - kernel_utils: Shared utilities for kernel size validation (used by blur/noise operations)
#
# - transforms: Transform pipeline composition using factory pattern
#   Orchestrates both essential and nonessential transforms into complete pipelines
#   - transform_factory: Factory for creating train/val/test/TTA transform pipelines
#   - transform_composition: Composes preprocessing, augmentation, and normalization
#   - preprocessing_builders: Registry of preprocessing transform builders
#   - augmentation_builders: Registry of augmentation transform builders
#   - tta_builders: Builds test-time augmentation transform pipelines
#
# Boundary Rules:
# - Use essential for: loading files, essential transforms (resize/normalize), dataset classes
# - Use nonessential for: optional enhancements, augmentation, transform composition
# - Normalization is always automatically applied and should not be included in preprocessing_list
#
# Import Guidelines:
# - External code should use package-level imports: `from dataset_manipulation.essential import ...`
# - For nonessential, use direct imports to avoid circular dependencies:
#   - from dataset_manipulation.nonessential.preprocessing import contrast_enhancement, noise_reduction
# - For transforms, use direct imports:
#   - from dataset_manipulation.transforms.transform_factory import build_train_transform, build_val_transform, build_tta_transforms

# Lazy imports to avoid circular import issues
# Import functions only when accessed, not at module level
def __getattr__(name):
    """Lazy import for functions and classes to avoid circular dependencies."""
    # Loading functions
    if name == 'load_jpg':
        from .essential.loading import load_jpg
        return load_jpg
    elif name == 'load_jpg_batch':
        from .essential.loading import load_jpg_batch
        return load_jpg_batch
    elif name == 'load_csv':
        from .essential.loading.load_csv import load_csv
        return load_csv
    elif name == 'load_csv_batch':
        from .essential.loading.load_csv import load_csv_batch
        return load_csv_batch
    elif name == 'load_and_validate_test_data':
        from .essential.loading.load_csv import load_and_validate_test_data
        return load_and_validate_test_data
    elif name == 'aggregate_train_csv':
        from .essential.loading.aggregate_train import aggregate_train_csv
        return aggregate_train_csv
    # Preprocessing functions
    elif name == 'normalize':
        from .essential.preprocessing.normalization import normalize
        return normalize
    elif name == 'resize':
        from .essential.preprocessing.resizing import resize
        return resize
    # Streaming dataset classes
    elif name == 'StreamingBiomassDataset':
        from .essential.streaming.streaming_biomass_dataset import StreamingBiomassDataset
        return StreamingBiomassDataset
    elif name == 'StreamingBiomassSplitDataset':
        from .essential.streaming.streaming_biomass_split_dataset import StreamingBiomassSplitDataset
        return StreamingBiomassSplitDataset
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

__all__ = [
    # Loading
    'load_jpg', 'load_jpg_batch', 
    'load_csv', 'load_csv_batch',
    'load_and_validate_test_data',
    'aggregate_train_csv',
    # Preprocessing
    'normalize', 'resize',
    # Streaming datasets
    'StreamingBiomassDataset',
    'StreamingBiomassSplitDataset',
]