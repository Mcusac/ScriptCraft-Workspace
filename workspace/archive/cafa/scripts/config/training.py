"""
Training configuration constants for CAFA 6 protein function prediction.
"""

from typing import Optional

# Progress indicator settings
PROGRESS_INDICATOR_INTERVAL = 10000  # Print progress every N items

# Default random seed (can be overridden per model)
DEFAULT_RANDOM_SEED = 42

# Label propagation settings
PROPAGATE_TRAIN_LABELS: bool = False  # Propagate training labels up GO graph before training
TOP_K_LABELS: Optional[int] = None  # Restrict to top-K most frequent GO terms per ontology (e.g., 3000)

# Memory management settings
# These control memory usage during training to prevent OOM errors
USE_MEMORY_MAPPED_EMBEDDINGS: bool = True  # Use np.memmap for embeddings (read-only, on-disk)
LOAD_LABELS_PER_ONTOLOGY: bool = True  # Load labels per-ontology on-demand instead of all upfront
FREE_FEATURES_AFTER_ONTOLOGY: bool = True  # Free feature matrix after each ontology training

# Feature extraction parallelization
FEATURE_EXTRACTION_MAX_WORKERS: int = 4  # Max workers for ThreadPoolExecutor in parallel feature extraction

# Numerical constants for stability
EPSILON_SMALL: float = 1e-10  # Small epsilon for geometric mean, clipping operations
EPSILON_TINY: float = 1e-12  # Tiny epsilon for F1 score calculations

# Training workflow constants
VALIDATION_SPLIT_SIZE: float = 0.15  # Validation split ratio for threshold optimization
LARGE_LABEL_SPACE_THRESHOLD: int = 10000  # Threshold for large label spaces (affects CV fold reduction)
MEDIUM_LABEL_SPACE_THRESHOLD: int = 5000  # Threshold for medium label spaces (affects CV fold reduction)

# Model training constants
DEFAULT_N_JOBS: int = -1  # Default n_jobs for sklearn parallelization (-1 = use all cores)
DEFAULT_VALIDATION_SPLIT: float = 0.2  # Default validation split for MLP trainers
LARGE_ONTOLOGY_LABEL_THRESHOLD: int = 10000  # Threshold for large ontologies (affects streaming metrics)
REDUCED_BATCH_SIZE_LARGE_ONTOLOGY: int = 512  # Fallback batch size for large ontologies

# DataLoader constants
DATALOADER_PRELOAD_THRESHOLD_MB: int = 1000  # Threshold for GPU pre-loading (1GB)
DATALOADER_PRELOAD_MAX_MB: int = 4000  # Maximum GPU preload size (4GB)
DATALOADER_GPU_MEMORY_FRACTION: float = 0.5  # Fraction of GPU memory to use for preloading
DATALOADER_MAX_WORKERS: int = 8  # Maximum number of DataLoader workers
DATALOADER_PREFETCH_FACTOR: int = 4  # Default prefetch factor for DataLoader
DATALOADER_PREFETCH_FACTOR_LARGE_LABELS: int = 2  # Reduced prefetch factor for large label spaces (>10K labels)
DATALOADER_MULTIPROCESSING_TIMEOUT: int = 1  # Timeout for multiprocessing test (seconds)
DATALOADER_TEST_WORKERS: int = 2  # Number of workers for multiprocessing test
DATALOADER_LARGE_DATASET_THRESHOLD_MB: int = 1000  # Threshold for large dataset optimizations

# Memory-aware DataLoader settings
DATALOADER_MEMORY_AWARE_WORKERS: bool = True  # Enable memory-aware worker count calculation
DATALOADER_MAX_MEMORY_PER_WORKER_MB: int = 2000  # Maximum memory per worker (2GB) - reduces workers if exceeded
DATALOADER_LARGE_LABEL_SPACE_THRESHOLD: int = 10000  # Label count threshold for large label space optimizations
DATALOADER_MAX_WORKERS_LARGE_LABELS: int = 2  # Maximum workers for large label spaces (>10K labels) - reduces memory footprint
DATALOADER_MAX_WORKERS_VERY_LARGE_LABELS: int = 0  # Maximum workers for very large label spaces (>15K labels) - use single worker to prevent OOM
DATALOADER_VERY_LARGE_LABEL_SPACE_THRESHOLD: int = 15000  # Threshold for very large label spaces (use 0 workers)
DATALOADER_DISABLE_PERSISTENT_FOR_LARGE_LABELS: bool = True  # Disable persistent_workers for large label spaces to free memory between epochs

# Memory constants
FLOAT32_BYTES: int = 4  # Bytes per float32 element
MB_TO_BYTES: int = 1024**2  # Conversion factor: MB to bytes
GB_TO_BYTES: int = 1024**3  # Conversion factor: GB to bytes
MEMMAP_THRESHOLD_MB: int = 2000  # Memory threshold for using memory-mapped arrays (2GB)

# Model I/O constants
MODEL_FILE_EXTENSION_PKL: str = '.pkl'  # File extension for sklearn models
MODEL_FILE_EXTENSION_PTH: str = '.pth'  # File extension for PyTorch models
VALID_ONTOLOGY_CODES: list = ['F', 'P', 'C']  # Valid ontology codes

# GPU utilities constants
GPU_CHECK_TIMEOUT: int = 2  # Timeout for nvidia-smi check (seconds)

