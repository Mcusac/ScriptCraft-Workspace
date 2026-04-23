# config.py
# Configuration management for model training and evaluation

from dataclasses import dataclass, is_dataclass, field
from typing import Optional, Dict, Any, List
from .evaluation_constants import TARGET_WEIGHTS, NUM_PRIMARY_TARGETS
from .path_constants import DEFAULT_IMAGE_SIZE
from .progress_config import ProgressConfig


@dataclass
class ModelConfig:
    """Model architecture configuration"""
    model_type: str = 'auto'  # 'auto' for auto-detection, 'timm' for timm models, 'dinov2' for DINOv2 models
    name: str = 'efficientnet_b0'  # Model name: timm model (e.g., 'efficientnet_b0') or HuggingFace DINOv2 (e.g., 'facebook/dinov2-base')
    pretrained: bool = True
    num_classes: int = NUM_PRIMARY_TARGETS  # Number of primary targets (default from evaluation constants)
    input_size: Optional[tuple] = None  # Will be set from pretrained_cfg if None
    # DINOv2-specific options
    use_tiles: bool = False  # Whether to use tile-based processing (DINOv2 only)
    tile_grid_size: int = 2  # Grid size for tile extraction (e.g., 2 = 2x2 = 4 tiles per half)
    # Feature extraction mode (two-stage training)
    feature_extraction_mode: bool = False  # If True, use model for feature extraction only, then train regression model on features
    feature_extraction_model_name: Optional[str] = None  # Model name for feature extraction (e.g., 'dinov2_base', 'timm_efficientnet_b3', or path like '/kaggle/input/dinov2/pytorch/base/1'). Used when feature_extraction_mode=True. Model names are automatically converted to pretrained paths via get_pretrained_weights_path().
    regression_model_type: Optional[str] = None  # Regression model type: 'lgbm', 'xgboost', 'ridge'. Used when feature_extraction_mode=True
    extract_features: bool = True  # If True, extract features from scratch. If False, try to load from cache. Used when feature_extraction_mode=True


@dataclass
class TrainingConfig:
    """Training hyperparameters"""
    batch_size: int = 32
    learning_rate: float = 1e-3
    num_epochs: int = 100
    optimizer: str = 'AdamW'  # AdamW, Adam, SGD
    loss_function: str = 'SmoothL1Loss'  # SmoothL1Loss, MSELoss
    scheduler: str = 'ReduceLROnPlateau'  # ReduceLROnPlateau, CosineAnnealingLR
    scheduler_mode: str = 'max'  # 'max' for metric, 'min' for loss
    scheduler_factor: float = 0.5
    scheduler_patience: int = 5
    early_stopping_patience: int = 10
    weight_decay: float = 1e-4
    # Mixed precision training (fp16)
    use_mixed_precision: bool = False  # Enable for memory + speed boost
    mixed_precision_dtype: str = 'float16'  # 'float16' or 'bfloat16'


@dataclass
class DataConfig:
    """Data loading and preprocessing configuration"""
    # Default data root path (uses contest abstraction, defaults to CSIRO)
    data_root: str = None  # Will be set from contest paths if None
    train_csv: str = 'train.csv'
    test_csv: str = 'test.csv'
    image_size: Optional[tuple] = None  # Will be set from model config
    normalize: bool = True
    imagenet_mean: tuple = (0.485, 0.456, 0.406)
    imagenet_std: tuple = (0.229, 0.224, 0.225)
    use_augmentation: bool = False  # Phase 4: False, Phase 6+: True
    augmentation_config: Optional[Dict[str, Any]] = None
    preprocessing_list: List[str] = None  # List of optional preprocessing techniques (empty = only essential: resize+normalize applied automatically)
    augmentation_list: List[str] = None  # List of augmentation techniques to apply (empty = no augmentation)
    dataset_type: str = 'split'  # 'split' for left/right split (default, standard approach), 'full' for full image (explicit override)
    tta_variants: Optional[List[str]] = None  # List of TTA variant names. If None, uses defaults. Available: 'original', 'h_flip', 'v_flip', 'both_flips', 'rotate_90', 'rotate_270'
    
    def __post_init__(self):
        if self.preprocessing_list is None:
            self.preprocessing_list = []
        if self.augmentation_list is None:
            self.augmentation_list = []


@dataclass
class CVConfig:
    """Cross-validation configuration"""
    n_folds: int = 5
    shuffle: bool = True
    random_state: int = 42
    stratify: Optional[str] = None  # Column name for stratification (e.g., 'State')


@dataclass
class GridSearchConfig:
    """Grid search configuration"""
    keep_top_variants: int = 20  # Number of top variants to keep during cleanup
    cleanup_interval: int = 10  # Run cleanup every N variants
    enable_cleanup: bool = True  # Enable automatic checkpoint cleanup
    delete_checkpoints_after_completion: bool = True  # Delete checkpoints immediately after variant completes (only keep results.json)
    use_streaming_dataset: bool = True  # Use streaming dataset for memory efficiency
    # OOM (Out of Memory) error handling configuration
    min_batch_size: int = 4  # Minimum batch size when reducing due to OOM errors
    batch_size_reduction_factor: int = 2  # Factor to divide batch size by when OOM occurs
    max_oom_retries: int = 2  # Maximum number of OOM retries before skipping variant/combination


@dataclass
class PathConfig:
    """Path configuration"""
    output_dir: str = 'output'
    model_dir: str = 'models'
    log_dir: str = 'logs'
    submission_file: str = 'submission.csv'


@dataclass
class EvaluationConfig:
    """Evaluation metric configuration"""
    # Target weights for weighted R² (from competition)
    target_weights: Dict[str, float] = field(default_factory=lambda: TARGET_WEIGHTS.copy())


@dataclass
class DeviceConfig:
    """Device configuration"""
    device: str = 'cuda'  # 'cuda', 'cpu', 'mps', 'tpu' (auto-detected if available)
    num_workers: int = 4
    pin_memory: bool = True
    use_multi_gpu: bool = True  # Use DataParallel if multiple GPUs available
    # Memory optimization options (enabled by default for transformers)
    reduce_workers_for_memory: bool = False   # Disabled to enable multi-core data loading
    disable_pin_memory_for_memory: bool = False  # Disabled to enable faster GPU data transfer
    # DataLoader optimization for CPU-bound data loading
    prefetch_factor: int = 4  # Number of batches to prefetch per worker (default: 2, increased for better CPU/GPU utilization)
    persistent_workers: bool = True  # Reuse workers between epochs (requires num_workers > 0, reduces worker startup overhead)


@dataclass
class Config:
    """Main configuration class combining all configs"""
    model: ModelConfig = None
    training: TrainingConfig = None
    data: DataConfig = None
    cv: CVConfig = None
    paths: PathConfig = None
    evaluation: EvaluationConfig = None
    device: DeviceConfig = None
    grid_search: GridSearchConfig = None
    progress: ProgressConfig = None
    seed: int = 42
    debug: bool = False
    
    def __post_init__(self):
        # Default configuration classes for lazy initialization
        _config_defaults = {
            'model': ModelConfig,
            'training': TrainingConfig,
            'data': DataConfig,
            'cv': CVConfig,
            'paths': PathConfig,
            'evaluation': EvaluationConfig,
            'device': DeviceConfig,
            'grid_search': GridSearchConfig,
            'progress': ProgressConfig
        }
        
        for attr, default_class in _config_defaults.items():
            if getattr(self, attr) is None:
                setattr(self, attr, default_class())
        
        # Set default data_root from contest paths if not set
        if self.data and self.data.data_root is None:
            try:
                from contest.registry import get_contest_paths
                contest_paths = get_contest_paths()
                self.data.data_root = str(contest_paths.local_data_root)
            except (ImportError, ValueError):
                # Fallback to CSIRO default if contest not available
                self.data.data_root = '../csiro-biomass'
    
    def update_from_dict(self, config_dict: Dict[str, Any]) -> None:
        """
        Update configuration from dictionary.
        
        Recursively updates nested dataclass attributes. Only updates attributes
        that exist in the Config structure; unknown keys are ignored.
        
        Args:
            config_dict: Dictionary with configuration values.
                        Structure should match Config dataclass hierarchy.
                        Keys can be top-level (e.g., 'seed', 'debug') or nested
                        (e.g., 'model': {'name': 'resnet50'}).
        
        Raises:
            TypeError: If config_dict is not a dictionary.
            ValueError: If config_dict is None or contains invalid values.
        """
        # Validate input
        if config_dict is None:
            raise ValueError("config_dict cannot be None")
        
        if not isinstance(config_dict, dict):
            raise TypeError(f"config_dict must be dict, got {type(config_dict)}")
        
        for key, value in config_dict.items():
            if hasattr(self, key):
                attr_value = getattr(self, key)
                if is_dataclass(attr_value) and not isinstance(attr_value, type):
                    # Update nested dataclass instance
                    if not isinstance(value, dict):
                        raise ValueError(
                            f"Expected dict for nested config '{key}', got {type(value)}"
                        )
                    nested = attr_value
                    for nested_key, nested_value in value.items():
                        if hasattr(nested, nested_key):
                            setattr(nested, nested_key, nested_value)
                        # Silently ignore unknown nested keys (for flexibility)
                else:
                    setattr(self, key, value)
            # Silently ignore unknown top-level keys (for flexibility)
    
    def get_model_input_size(self) -> tuple:
        """
        Get model input size, using config or default.
        
        Priority order:
        1. model.input_size (if set)
        2. data.image_size (if set)
        3. Default (256, 256)
        
        Returns:
            Tuple of (height, width) representing model input size.
            Default: (256, 256) if neither config value is set.
        """
        if self.model and self.model.input_size:
            return self.model.input_size
        if self.data and self.data.image_size:
            return self.data.image_size
        # Default for EfficientNet
        return DEFAULT_IMAGE_SIZE
    
    def ensure_dirs(self) -> None:
        """
        Ensure all output directories exist.
        
        Creates output_dir, model_dir, and log_dir if they don't exist.
        Parent directories are created as needed.
        
        Raises:
            AttributeError: If paths config is None or missing required attributes.
            PermissionError: If directories cannot be created due to permissions.
            OSError: If directory creation fails.
        """
        from utils.system import ensure_config_dirs
        ensure_config_dirs(self.paths)


# Default configuration instance (lazy initialization to avoid circular imports)
_default_config_instance: Optional[Config] = None


def get_default_config() -> Config:
    """
    Get default configuration instance (lazy initialization).
    
    Creates the default config on first call to avoid circular import issues
    when config.py is imported at module level.
    
    Returns:
        Default Config instance with all default values.
    """
    global _default_config_instance
    if _default_config_instance is None:
        _default_config_instance = Config()
    return _default_config_instance


# Create a proxy class that acts like the config instance
# This allows code to use `default_config.seed` or `config = default_config` with lazy initialization
class _DefaultConfigProxy:
    """
    Proxy object for lazy initialization of default configuration.
    
    This proxy pattern is used to prevent circular import issues when Config
    needs to reference default_config during initialization. The proxy delays
    the actual Config creation until first access, allowing the Config class
    to be fully defined before default_config is instantiated.
    
    The proxy implements attribute access delegation, so it behaves like a
    Config instance but creates the actual Config lazily on first access.
    
    This is necessary because:
    1. Config.__post_init__ may need to reference default_config
    2. default_config needs to be a Config instance
    3. Circular dependency would occur if default_config was created at module level
    
    Usage:
        default_config = _DefaultConfigProxy()
        # Later, when accessed:
        default_config.training.batch_size  # Creates Config() on first access
    """
    """Proxy class to provide default_config as an attribute-like accessor."""
    
    def __getattr__(self, name):
        """Delegate attribute access to the actual config instance."""
        return getattr(get_default_config(), name)
    
    def __setattr__(self, name, value):
        """Delegate attribute setting to the actual config instance."""
        # Use object.__setattr__ to avoid infinite recursion
        # Only set attributes that are part of the proxy itself
        if name.startswith('_proxy_'):
            object.__setattr__(self, name, value)
        else:
            # Delegate to the actual config instance
            setattr(get_default_config(), name, value)
    
    def __call__(self):
        """Allow calling as function."""
        return get_default_config()
    
    def __repr__(self):
        """String representation."""
        return f"<default_config proxy: {get_default_config()}>"
    
    def __eq__(self, other):
        """Equality comparison with actual config."""
        return get_default_config() == other
    
    def __ne__(self, other):
        """Inequality comparison with actual config."""
        return get_default_config() != other

# Create instance that can be used as both attribute accessor and callable
default_config = _DefaultConfigProxy()
