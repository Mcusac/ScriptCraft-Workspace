"""
Feature extraction and embedding configurations.
"""

# Memory Thresholds
FEATURE_EXTRACTION_MEMORY_THRESHOLD_MB = 500  # Threshold for using memmap (MB)

# Feature Extraction Methods
FEATURE_EXTRACTION_METHODS = {
    "hand_crafted": {
        "name": "Hand-crafted Features",
        "description": "90 manually engineered features (AA composition, k-mers, physicochemical, CTD)",
        "dimensions": 90,
        "module": "preprocessing.feature_engineering.handcrafted",
        "extract_function": "extract_sequence_features"
    },
    "protbert": {
        "name": "ProtBERT Embeddings",
        "description": "Protein-specific BERT embeddings (1024 dimensions)",
        "dimensions": 1024,
        "module": "preprocessing.feature_engineering.embeddings",
        "extract_function": "extract_protbert_embeddings"
    },
    "esm2": {
        "name": "ESM2 Embeddings", 
        "description": "Evolutionary Scale Modeling embeddings (1280 dimensions)",
        "dimensions": 1280,
        "module": "preprocessing.feature_engineering.embeddings",
        "extract_function": "extract_esm2_embeddings"
    },
    "t5": {
        "name": "T5 Protein Embeddings",
        "description": "T5-based protein embeddings (1024 dimensions)",
        "dimensions": 1024,
        "module": "preprocessing.feature_engineering.embeddings", 
        "extract_function": "extract_t5_embeddings"
    },
    "fused_embeddings": {
        "name": "Fused Embeddings + Handcrafted",
        "description": "ProtBERT(1024) + ESM2(1280) + handcrafted(90) = 2394 dims",
        "dimensions": 2394,
        "module": "preprocessing.feature_extraction",
        "extract_function": "extract_features"
    }
}

# Batch Size Configuration - Single Source of Truth
# Centralized batch size configuration to prevent duplicates and overwrites
BATCH_SIZE_CONFIG = {
    # Embedding model inference batch sizes (per model, different memory requirements)
    "embedding_inference": {
        "protbert": 8,
        "esm2": 4,
        "t5": 2
    },
    
    # Neural network training batch sizes (CONSOLIDATED - single source)
    # Base batch sizes - will be auto-scaled based on GPU memory
    "nn_training": {
        "default": 1024,     # Base batch size
        "mlp_v1": 1024       # Base batch size for MLP v1
    },
    
    # GPU batch sizes (direct values based on GPU memory)
    # Optimized for multiple batches per epoch (batch_size < sample_count)
    # Large enough to use GPU memory but small enough for multiple iterations
    "gpu_batch_sizes": {
        "p100": {
            "memory_gb_threshold": 15,
            "batch_size": 16384  # ~4 batches per epoch for 63k samples
        },
        "t4": {
            "memory_gb_threshold": 10,
            "batch_size": 8192   # ~8 batches per epoch
        },
        "small": {
            "memory_gb_threshold": 0,
            "batch_size": 4096   # ~16 batches per epoch
        }
    },
    
    # Neural network inference batch sizes (CONSOLIDATED - single source)
    # Same as training since inference uses less memory (no gradients/optimizer states)
    "nn_inference": {
        "default": 1024,     # Same as training - inference uses less memory
        "mlp_v1": 1024       # Can override per-model if needed
    },
    
    # Prediction pipeline batch sizes (protein processing and write buffering)
    "prediction_pipeline": {
        "protein_processing": 3000,   # Number of proteins to process at once
        "write_buffer": 40000         # Write to disk every N predictions
    },
    
    # CLI defaults (for standalone scripts that override model configs)
    "cli_defaults": {
        "mlp_training": 1024  # Match training default - can be overridden via CLI flag
    },
    
    # Data loading chunk sizes (separate from training batch sizes)
    # These control how much data is loaded into memory at once during preprocessing
    # Training batch sizes remain large (e.g., 24576 for 2x T4 GPUs)
    "data_loading": {
        "sequence_chunk_size": 50000,    # Load sequences in chunks of 50K proteins
        "feature_chunk_size": 50000,      # Extract features in chunks of 50K proteins
        "embedding_chunk_size": 50000     # Load embeddings in chunks of 50K proteins
    }
}

# Embedding Configurations (batch_size now references BATCH_SIZE_CONFIG)
EMBEDDING_CONFIGS = {
    "protbert": {
        "model_name": "Rostlab/prot_bert",
        "max_length": 512,
        "batch_size": BATCH_SIZE_CONFIG["embedding_inference"]["protbert"],
        "device": "cuda" if True else "cpu"  # Will be set dynamically
    },
    "esm2": {
        "model_name": "facebook/esm2_t33_650M_UR50D",
        "max_length": 1024,
        "batch_size": BATCH_SIZE_CONFIG["embedding_inference"]["esm2"],
        "device": "cuda" if True else "cpu"  # Will be set dynamically
    },
    "t5": {
        "model_name": "Rostlab/prot_t5_xl_half_uniref50-enc",
        "max_length": 512,
        "batch_size": BATCH_SIZE_CONFIG["embedding_inference"]["t5"],
        "device": "cuda" if True else "cpu"  # Will be set dynamically
    }
}

# Individual Feature Definitions (for flexible combination)
INDIVIDUAL_FEATURES = {
    # Current embeddings (from consolidated dataset)
    "protbert": {
        "name": "ProtBERT",
        "dimensions": 1024,
        "type": "embedding",
        "description": "ProtBERT protein embeddings"
    },
    "prot_t5_xl": {
        "name": "ProtT5-XL",
        "dimensions": 1024,
        "type": "embedding",
        "description": "ProtT5-XL protein embeddings (upgrade from T5)"
    },
    
    # ESM2 variants (new from cafa-6-embeddings)
    "esm2_15b": {
        "name": "ESM2-15B",
        "dimensions": 5120,
        "type": "embedding",
        "description": "ESM2 15B parameters (highest quality, 5120 dims)"
    },
    "esm2_3b": {
        "name": "ESM2-3B",
        "dimensions": 2560,
        "type": "embedding",
        "description": "ESM2 3B parameters (high quality, 2560 dims)"
    },
    "esm2_650m": {
        "name": "ESM2-650M",
        "dimensions": 1280,
        "type": "embedding",
        "description": "ESM2 650M parameters (current baseline)"
    },
    "esm2": {
        "name": "ESM2",
        "dimensions": 1280,
        "type": "embedding",
        "description": "ESM2 evolutionary embeddings (legacy, maps to esm2_650m)"
    },
    "esm1b_650m": {
        "name": "ESM1b-650M",
        "dimensions": 1280,
        "type": "embedding",
        "description": "ESM1b 650M parameters"
    },
    
    # Ankh variants (new)
    "ankh_large": {
        "name": "Ankh-Large",
        "dimensions": None,  # TBD from actual files
        "type": "embedding",
        "description": "Ankh large embeddings",
        "available": True
    },
    "ankh3_large": {
        "name": "Ankh3-Large",
        "dimensions": None,  # TBD from actual files
        "type": "embedding",
        "description": "Ankh3 large embeddings",
        "available": True
    },
    
    # Legacy T5 (keep for compatibility)
    "t5": {
        "name": "T5",
        "dimensions": 1024,
        "type": "embedding",
        "description": "T5 protein embeddings (loaded from .rds files, legacy)",
        "available": True
    },
    
    # Handcrafted features
    "hc": {
        "name": "Handcrafted",
        "dimensions": 90,
        "type": "engineered",
        "description": "90 handcrafted features (AA comp, k-mers, physicochemical, CTD)"
    },
    
    # New structured feature types
    "taxonomy": {
        "name": "Taxonomy",
        "dimensions": None,  # TBD from files
        "type": "structured",
        "description": "Organism taxonomy classification features",
        "available": True
    },
    "taxonomy_highlevel": {
        "name": "TaxonomyHighLevel",
        "dimensions": None,  # TBD from files
        "type": "structured",
        "description": "High-level organism taxonomy features",
        "available": True
    },
    "taxonomy_top500": {
        "name": "TaxonomyTop500",
        "dimensions": None,  # TBD from files
        "type": "structured",
        "description": "Top 500 taxonomy features",
        "available": True
    },
    "ppi": {
        "name": "PPI",
        "dimensions": None,  # TBD from files
        "type": "structured",
        "description": "Protein-protein interaction features",
        "available": True
    },
    "top_terms": {
        "name": "TopTerms",
        "dimensions": None,  # TBD from files
        "type": "structured",
        "description": "Top GO terms by aspect features",
        "available": True
    },
    
    # Experimental features
    "targets_top500": {
        "name": "Top500Targets",
        "dimensions": 500,
        "type": "experimental",
        "description": "Top 500 train targets features (experimental)",
        "available": False  # Experimental feature
    }
}

# Feature key constants
HANDCRAFTED_FEATURE_KEY: str = 'hc'  # Key for handcrafted features in feature lists

# Named Presets (meaningful multi-feature combinations)
FEATURE_PRESETS = {
    "default": {
        "features": ["protbert", "esm2", "hc"],
        "description": "ProtBERT + ESM2 + handcrafted (2394 dims) - current best",
        "dimensions": 2394
    },
    "embeddings_only": {
        "features": ["protbert", "esm2"],
        "description": "ProtBERT + ESM2 embeddings only (2304 dims)",
        "dimensions": 2304
    },
    "protbert_only": {
        "features": ["protbert"],
        "description": "ProtBERT only (1024 dims) - memory-efficient",
        "dimensions": 1024
    },
    "protbert_hc": {
        "features": ["protbert", "hc"],
        "description": "ProtBERT + handcrafted (1114 dims) - balanced memory/performance",
        "dimensions": 1114
    },
    "handcrafted_only": {
        "features": ["hc"],
        "description": "Handcrafted features only (90 dims) - minimal memory",
        "dimensions": 90
    },
    "protbert_esm2_t5_hc": {
        "features": ["protbert", "esm2", "t5", "hc"],
        "description": "ProtBERT + ESM2 + T5 + handcrafted (3418 dims) - with T5",
        "dimensions": 3418
    },
    "all_with_hc": {
        "features": ["protbert", "esm2", "t5", "hc"],
        "description": "All embeddings + handcrafted (3418 dims)",
        "dimensions": 3418,
        "available": True  # T5 now available
    },
    
    # New high-quality presets
    "high_quality": {
        "features": ["esm2_15b", "protbert", "hc"],
        "description": "Highest quality: ESM2-15B + ProtBERT + HC (6234 dims)",
        "dimensions": 6234
    },
    "balanced": {
        "features": ["esm2_3b", "protbert", "hc"],
        "description": "Balanced: ESM2-3B + ProtBERT + HC (3674 dims)",
        "dimensions": 3674
    },
    "with_ankh": {
        "features": ["esm2_3b", "ankh3_large", "protbert", "hc"],
        "description": "ESM2-3B + Ankh3 + ProtBERT + HC (dimensions TBD)",
        "dimensions": None  # Calculate after determining Ankh dimensions
    },
    "with_all_features": {
        "features": ["esm2_3b", "protbert", "taxonomy", "ppi", "top_terms", "hc"],
        "description": "ESM2-3B + ProtBERT + all structured features + HC",
        "dimensions": None  # Calculate after determining feature dimensions
    },
    "maximum": {
        "features": ["esm2_15b", "esm2_3b", "protbert", "prot_t5_xl", "taxonomy", "ppi", "hc"],
        "description": "Maximum: ESM2-15B + ESM2-3B + ProtBERT + ProtT5-XL + taxonomy + PPI + HC",
        "dimensions": None  # Calculate after determining feature dimensions
    }
}


def get_embedding_feature_types() -> list:
    """
    Get list of all embedding feature types from INDIVIDUAL_FEATURES.
    
    Returns:
        list[str]: List of embedding feature keys (e.g., ['protbert', 'esm2', 't5'])
    """
    return [
        feat_key for feat_key, feat_config in INDIVIDUAL_FEATURES.items()
        if feat_config.get("type") == "embedding"
    ]


def is_valid_embedding_type(embedding_type: str) -> bool:
    """
    Check if embedding type is valid by checking against INDIVIDUAL_FEATURES.
    
    Args:
        embedding_type: Embedding type to validate (e.g., 'protbert', 'esm2', 't5')
        
    Returns:
        bool: True if valid embedding type, False otherwise
    """
    return (
        embedding_type in INDIVIDUAL_FEATURES and
        INDIVIDUAL_FEATURES[embedding_type].get("type") == "embedding"
    )


def parse_feature_spec(spec: str) -> list:
    """
    Parse feature specification string into a normalized features list.
    Treats handcrafted (hc) like any other feature for full flexibility.
    
    Args:
        spec: Either a preset name OR comma-separated individual features
              Examples: "default", "protbert,esm2,hc", "esm2"
    
    Returns:
        list[str]: Normalized features list (e.g., ["protbert", "esm2", "hc"]).
    """
    # Check if it's a named preset first
    if spec in FEATURE_PRESETS:
        preset = FEATURE_PRESETS[spec]
        if not preset.get("available", True):
            raise ValueError(f"Preset '{spec}' is not yet available: {preset.get('description')}")
        features = preset["features"]
    else:
        # Parse as comma-separated individual features
        features = [f.strip() for f in spec.split(",")]
        
        # Validate each feature
        for feat in features:
            if feat not in INDIVIDUAL_FEATURES:
                raise ValueError(
                    f"Unknown feature: '{feat}'. Available: {list(INDIVIDUAL_FEATURES.keys())} "
                    f"or presets: {list(FEATURE_PRESETS.keys())}"
                )
            if not INDIVIDUAL_FEATURES[feat].get("available", True):
                raise ValueError(
                    f"Feature '{feat}' is not yet available: {INDIVIDUAL_FEATURES[feat].get('description')}"
                )
    
    # Return full features list (embeddings + engineered)
    return features


def get_feature_dimensions(feature_spec: str) -> int:
    """
    Calculate total dimensions for a feature specification.
    
    Args:
        feature_spec: Feature specification string (preset or comma-separated)
        
    Returns:
        int: Total number of dimensions
    """
    # Check if it's a preset with pre-calculated dimensions
    if feature_spec in FEATURE_PRESETS:
        return FEATURE_PRESETS[feature_spec]["dimensions"]
    
    # Calculate from individual features
    features = [f.strip() for f in feature_spec.split(",")]
    total_dims = 0
    for feat in features:
        if feat in INDIVIDUAL_FEATURES:
            total_dims += INDIVIDUAL_FEATURES[feat]["dimensions"]
    
    return total_dims


def validate_feature_availability(features: list) -> tuple:
    """
    Check if embedding files exist for specified types.
    
    Args:
        features: List of features (embeddings and engineered) to validate
        
    Returns:
        tuple: (all_available: bool, missing: list)
    """
    from pathlib import Path
    from .paths import EMBEDDING_PATHS
    
    missing = []
    
    for feat in features:
        # Only validate embeddings that require files
        if feat not in INDIVIDUAL_FEATURES:
            missing.append(f"{feat} (unknown feature)")
            continue
        if INDIVIDUAL_FEATURES[feat].get("type") != "embedding":
            continue  # skip non-embedding features
        emb_type = feat
        if emb_type not in EMBEDDING_PATHS:
            missing.append(f"{emb_type} (not in EMBEDDING_PATHS)")
            continue
            
        emb_path = EMBEDDING_PATHS[emb_type]
        
        # Special handling for T5 embeddings (stored as .qs or .rds files)
        if emb_type == 't5':
            # Check for .qs files first (preferred format)
            train_file = emb_path / "T5_train_features.qs"
            test_file = emb_path / "T5_test_features.qs"
            # Fallback to .rds files if .qs not found
            if not train_file.exists():
                train_file = emb_path / "CAFA5_train_t5embeds.rds"
            if not test_file.exists():
                test_file = emb_path / "CAFA5_test_t5embeds.rds"
        else:
            train_file = emb_path / "train_sequences_emb.npy"
            test_file = emb_path / "testsuperset_emb.npy"
        
        if not train_file.exists():
            missing.append(f"{emb_type} train (expected: {train_file})")
        if not test_file.exists():
            missing.append(f"{emb_type} test (expected: {test_file})")
    
    return len(missing) == 0, missing


def get_feature_extraction_config(feature_type):
    """Get configuration for specified feature extraction method."""
    if feature_type not in FEATURE_EXTRACTION_METHODS:
        raise ValueError(f"Unknown feature type: {feature_type}. Available: {list(FEATURE_EXTRACTION_METHODS.keys())}")
    
    return FEATURE_EXTRACTION_METHODS[feature_type]


def get_embedding_config(embedding_type):
    """Get configuration for specified embedding type."""
    if embedding_type not in EMBEDDING_CONFIGS:
        raise ValueError(f"Unknown embedding type: {embedding_type}. Available: {list(EMBEDDING_CONFIGS.keys())}")
    
    return EMBEDDING_CONFIGS[embedding_type]


def get_optimized_batch_size(gpu_memory_gb: float = None) -> int:
    """
    Get optimized batch size based on GPU memory.
    Uses centralized gpu_batch_sizes config.
    
    Args:
        gpu_memory_gb: GPU memory in GB (if None, will try to detect)
        
    Returns:
        int: Optimized batch size for the detected GPU
    """
    if gpu_memory_gb is None:
        try:
            # Use centralized GPU utility (no circular import risk - utils doesn't import config)
            from utils.gpu_utils import get_gpu_memory_gb, check_gpu_available
            if check_gpu_available():
                gpu_memory_gb = get_gpu_memory_gb()
            else:
                # No GPU - use base training batch size
                return BATCH_SIZE_CONFIG.get("nn_training", {}).get("default", 1024)
        except:
            return BATCH_SIZE_CONFIG.get("nn_training", {}).get("default", 1024)
    
    # Find matching GPU tier from config
    gpu_configs = BATCH_SIZE_CONFIG.get("gpu_batch_sizes", {})
    
    # Check in order: p100, t4, small
    for tier_name in ["p100", "t4", "small"]:
        if tier_name in gpu_configs:
            tier_config = gpu_configs[tier_name]
            if gpu_memory_gb >= tier_config["memory_gb_threshold"]:
                return tier_config["batch_size"]
    
    # Fallback to base training batch size
    return BATCH_SIZE_CONFIG.get("nn_training", {}).get("default", 1024)


def get_gpu_optimized_batch_size(X_shape: tuple,
                                y_shape: tuple,
                                input_dim: int,
                                output_dim: int,
                                target_utilization: float = 0.70) -> int:
    """
    Calculate optimal batch size for GPU training based on available memory and model architecture.
    Targets 60-80% GPU utilization to maximize throughput without OOM errors.
    
    Args:
        X_shape: Feature matrix shape (n_samples, n_features)
        y_shape: Label matrix shape (n_samples, n_labels)
        input_dim: Model input dimension
        output_dim: Model output dimension (number of classes)
        target_utilization: Target GPU memory utilization (0.60-0.80, default: 0.70)
        
    Returns:
        int: Optimized batch size
    """
    from utils.gpu_utils import check_gpu_available, get_gpu_memory_gb
    
    if not check_gpu_available():
        # No GPU - use default batch size
        return BATCH_SIZE_CONFIG.get("nn_training", {}).get("default", 1024)
    
    # Get GPU memory
    gpu_memory_gb = get_gpu_memory_gb()
    if gpu_memory_gb == 0.0:
        # Can't determine GPU memory - use default
        return BATCH_SIZE_CONFIG.get("nn_training", {}).get("default", 1024)
    
    # Estimate memory per sample:
    # - Input features: input_dim * 4 bytes (float32)
    # - Output logits: output_dim * 4 bytes (float32)
    # - Gradients: same as forward pass
    # - Optimizer states (AdamW): 2x parameters (momentum + variance)
    # - Model parameters: (input_dim * hidden_dims + hidden_dims * output_dim) * 4 bytes
    # - Rough estimate: 3x forward pass + 2x parameters for optimizer
    
    # Estimate model parameters (simplified - assumes typical MLP architecture)
    # For MLP v2: input_dim -> 2048 -> 1024 -> 512 -> 256 -> output_dim
    # This is a rough estimate - actual model will have different architecture
    estimated_params = input_dim * 2048 + 2048 * 1024 + 1024 * 512 + 512 * 256 + 256 * output_dim
    
    # Memory per sample (forward + backward + optimizer states)
    # Forward pass: input features + hidden activations + output logits
    # - Input: input_dim * 4 bytes
    # - Hidden activations: sum of hidden_dims * 4 bytes (for gradient computation)
    # - Output logits: output_dim * 4 bytes
    # Backward pass: same activations + gradients
    # For large output_dim (many labels), output logits dominate memory
    
    # Estimate hidden activation memory (simplified: max hidden dim)
    max_hidden_dim = 2048  # MLP v2 max hidden layer
    hidden_activation_memory = max_hidden_dim * 4  # bytes per sample
    
    # Memory per sample: input + hidden activations + output (forward + backward)
    # Forward: input + hidden + output
    # Backward: gradients for all (same size)
    memory_per_sample_bytes = (
        input_dim * 4 +           # Input features
        hidden_activation_memory + # Hidden activations (max layer)
        output_dim * 4             # Output logits
    ) * 2  # Forward + backward
    
    # For very large output_dim, add extra buffer (labels take significant memory)
    if output_dim > 10000:
        # Large label space - add 50% buffer for label-related memory
        memory_per_sample_bytes = int(memory_per_sample_bytes * 1.5)
    
    memory_per_sample_mb = memory_per_sample_bytes / (1024**2)
    
    # Model memory (parameters + optimizer states)
    model_memory_mb = (estimated_params * 4 * 3) / (1024**2)  # Parameters + 2x for optimizer
    
    # Available GPU memory for batches (target utilization, minus model memory)
    # Use more conservative utilization for large label spaces
    if output_dim > 10000:
        target_utilization = 0.50  # More conservative for large label spaces
    
    available_memory_gb = gpu_memory_gb * target_utilization - (model_memory_mb / 1024)
    available_memory_mb = available_memory_gb * 1024
    
    if available_memory_mb <= 0:
        # Model is too large for GPU - use minimum batch size
        return 32
    
    # Calculate optimal batch size
    optimal_batch_size = int(available_memory_mb / memory_per_sample_mb)
    
    # Clamp to reasonable bounds - more conservative for large label spaces
    min_batch_size = 32
    if output_dim > 10000:
        # Large label space - use smaller max batch size
        max_batch_size = 2048  # Much smaller for large label spaces
    else:
        max_batch_size = 32768  # Upper limit for T4/P100 GPUs
    
    # Also consider dataset size - don't make batch size larger than dataset
    n_samples = X_shape[0]
    optimal_batch_size = min(optimal_batch_size, n_samples, max_batch_size)
    optimal_batch_size = max(optimal_batch_size, min_batch_size)
    
    # Round to nearest power of 2 for efficiency
    import math
    optimal_batch_size = 2 ** int(math.log2(optimal_batch_size))
    
    # Final safety check: for very large label spaces, cap batch size
    if output_dim > 15000:
        optimal_batch_size = min(optimal_batch_size, 512)
    
    return optimal_batch_size


def get_batch_size(category: str, model: str = None) -> int:
    """
    Get batch size from centralized configuration.
    
    Args:
        category: Batch size category ('embedding_inference', 'nn_training', 'nn_inference')
        model: Optional model name/type for model-specific batch sizes (e.g., 'mlp_v1', 'protbert')
        
    Returns:
        int: Batch size value
        
    Raises:
        ValueError: If category or model not found
        
    Examples:
        get_batch_size('nn_training')  # Returns 1024 (default)
        get_batch_size('nn_training', 'mlp_v1')  # Returns 1024 (mlp_v1 specific)
        get_batch_size('nn_inference')  # Returns 1024 (default, same as training)
        get_batch_size('embedding_inference', 'protbert')  # Returns 8
    """
    if category not in BATCH_SIZE_CONFIG:
        raise ValueError(
            f"Unknown batch size category: {category}. "
            f"Available: {list(BATCH_SIZE_CONFIG.keys())}"
        )
    
    category_config = BATCH_SIZE_CONFIG[category]
    
    # If model specified, try model-specific first, then default
    if model and model in category_config:
        return category_config[model]
    elif "default" in category_config:
        return category_config["default"]
    else:
        # For embedding_inference, model is required
        if category == "embedding_inference":
            raise ValueError(
                f"Model required for {category}. "
                f"Available models: {list(category_config.keys())}"
            )
        raise ValueError(f"No default batch size found for category: {category}")


def parse_model_feature_config(model_config: dict) -> tuple:
    """
    Parse feature configuration from model config dict.
    Extracts feature_type and features list, handling both preset and explicit feature lists.
    
    Args:
        model_config: Model configuration dict with 'feature_type' and optionally 
                     'feature_preset' or 'features' keys
        
    Returns:
        tuple: (feature_type: str, features: list or None)
            - feature_type: 'hand_crafted', 'fused_embeddings', etc.
            - features: List of feature names (e.g., ['protbert', 'esm2', 'hc']) or None
                      None if feature_type is not 'fused_embeddings'
        
    Raises:
        ValueError: If feature configuration is invalid or missing
        
    Examples:
        # Handcrafted features
        parse_model_feature_config({'feature_type': 'hand_crafted'})
        # Returns: ('hand_crafted', None)
        
        # Fused embeddings with preset
        parse_model_feature_config({'feature_type': 'fused_embeddings', 'feature_preset': 'default'})
        # Returns: ('fused_embeddings', ['protbert', 'esm2', 'hc'])
        
        # Fused embeddings with explicit list
        parse_model_feature_config({'feature_type': 'fused_embeddings', 'features': ['protbert', 'esm2']})
        # Returns: ('fused_embeddings', ['protbert', 'esm2'])
    """
    feature_type = model_config.get('feature_type', 'hand_crafted')
    
    if feature_type == 'fused_embeddings':
        # Resolve features from explicit list or preset
        # Priority: explicit 'features' list overrides 'feature_preset' (for CLI overrides)
        if 'features' in model_config:
            features = model_config['features']
            if not isinstance(features, list) or not features:
                raise ValueError("'features' must be a non-empty list when using fused_embeddings")
            # Validate each feature
            for feat in features:
                if feat not in INDIVIDUAL_FEATURES:
                    raise ValueError(
                        f"Unknown feature: '{feat}'. Available: {list(INDIVIDUAL_FEATURES.keys())} "
                        f"or presets: {list(FEATURE_PRESETS.keys())}"
                    )
                if not INDIVIDUAL_FEATURES[feat].get("available", True):
                    raise ValueError(
                        f"Feature '{feat}' is not yet available: {INDIVIDUAL_FEATURES[feat].get('description')}"
                    )
        elif 'feature_preset' in model_config:
            features = parse_feature_spec(model_config['feature_preset'])
        else:
            raise ValueError(
                "Feature configuration missing: provide 'feature_preset' or 'features' for fused_embeddings"
            )
        
        return (feature_type, features)
    else:
        # For non-fused features, no features list needed
        return (feature_type, None)
