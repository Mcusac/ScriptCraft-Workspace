# datasets package
# PyTorch Dataset classes
#
# Provides PyTorch IterableDataset implementation for training and inference.
#
# Components:
# - streaming_biomass_dataset: Memory-efficient IterableDataset for streaming
#   data loading. Loads images on-demand instead of pre-loading, making it
#   ideal for large datasets, grid search, and memory-constrained scenarios.
#   Supports multi-worker DataLoaders with automatic sharding.
#   Returns (image, targets) tuple.
#
# - streaming_biomass_split_dataset: Memory-efficient IterableDataset that splits
#   images into left/right halves at the midpoint. Addresses stereo/dual-view
#   nature of competition images by processing each half separately.
#   Returns (left_tensor, right_tensor, targets) tuple.
#
# The datasets integrate with the transform factory to apply preprocessing
# and augmentation pipelines, and handle data aggregation from the 5-row
# format in train.csv to single-row format per image.


__all__ = ['BaseStreamingBiomassDataset', 'StreamingBiomassDataset', 'StreamingBiomassSplitDataset']

