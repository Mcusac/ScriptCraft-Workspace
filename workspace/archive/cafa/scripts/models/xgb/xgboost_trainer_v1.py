"""
XGBoost trainer for CAFA 6 protein function prediction.
Multi-label XGBoost implementation for protein function prediction.
"""

import numpy as np
from typing import Dict, Any, Optional
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import f1_score
from concurrent.futures import ProcessPoolExecutor, as_completed

from config.training import DEFAULT_RANDOM_SEED, DEFAULT_N_JOBS
from models.training_utils import (
    check_ontology_has_terms,
    merge_hyperparams,
    train_with_error_handling,
    log_training_start,
    log_training_success,
    get_ontology_gpu_mapping
)

try:
    import xgboost as xgb
    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False
    xgb = None


def train_ontology_model_xgb(X_train: np.ndarray, y_train: np.ndarray, 
                            ont_code: str, ont_name: str, gpu_id: Optional[int] = None, **hyperparams) -> Optional[OneVsRestClassifier]:
    """
    Train XGBoost model for a specific ontology.
    
    Args:
        X_train: Feature matrix (n_samples, n_features)
        y_train: Label matrix (n_samples, n_terms)
        ont_code: Ontology code ('F', 'P', 'C')
        ont_name: Ontology name ('MFO', 'BPO', 'CCO')
        gpu_id: Optional GPU ID to use (if None, auto-assigned)
        **hyperparams: Model hyperparameters
        
    Returns:
        trained model object or None if skipped
    """
    log_training_start(ont_name, "XGBoost")
    
    # Check if XGBoost is available
    if not XGBOOST_AVAILABLE:
        print(f"      ❌ XGBoost not available. Install with: pip install xgboost")
        return None
    
    # Skip if no terms for this ontology
    if not check_ontology_has_terms(y_train, ont_name):
        return None
    
    # Check for GPU availability using centralized utility
    # Note: XGBoost uses ONE GPU per model. Multi-GPU benefit comes from training
    # multiple models concurrently (e.g., F/P/C on different GPUs), not splitting
    # a single model across GPUs like PyTorch DataParallel.
    from utils.gpu_utils import get_gpu_info
    gpu_available, num_gpus, _ = get_gpu_info()
    
    # Default hyperparameters
    default_params = {
        'n_estimators': 100,
        'max_depth': 6,
        'learning_rate': 0.1,
        'random_state': DEFAULT_RANDOM_SEED,
        'n_jobs': DEFAULT_N_JOBS,
        'verbosity': 0
    }
    
    # Merge with provided hyperparameters first (may contain gpu_id)
    merged_params = merge_hyperparams(default_params, hyperparams)
    
    # Determine GPU ID (priority: explicit param > hyperparams > auto-assign > 0)
    # Auto-assignment distributes ontologies across GPUs (F->0, P->1, C->2)
    # Note: Only useful when training multiple ontologies - single model uses one GPU
    if gpu_id is not None:
        final_gpu_id = gpu_id
    elif 'gpu_id' in merged_params:
        final_gpu_id = merged_params['gpu_id']
    elif num_gpus > 1:
        # Auto-assign when training multiple ontologies concurrently
        ont_to_gpu = get_ontology_gpu_mapping()
        final_gpu_id = ont_to_gpu.get(ont_code, 0) % num_gpus
    else:
        final_gpu_id = 0
    
    # Ensure valid GPU ID
    if num_gpus > 0:
        final_gpu_id = final_gpu_id % num_gpus
    
    # Configure GPU if available
    # Note: XGBoost uses ONE GPU per model. For single model training, only one GPU is used.
    # Multi-GPU benefit: When training F/P/C models, each can use a different GPU.
    if gpu_available and num_gpus > 0:
        merged_params['tree_method'] = 'gpu_hist'
        merged_params['gpu_id'] = final_gpu_id
        # GPU optimization parameters for better utilization
        merged_params['predictor'] = 'gpu_predictor'
        merged_params['max_bin'] = 512  # Increases parallelism, better GPU VRAM usage
        merged_params['grow_policy'] = 'lossguide'  # Loss-guided tree construction (better for GPU)
        if num_gpus > 1:
            print(f"      🚀 Using GPU {final_gpu_id}/{num_gpus} for {ont_name} (multi-GPU: distribute across ontologies)")
        else:
            print(f"      🚀 GPU acceleration enabled for {ont_name}")
    else:
        merged_params['tree_method'] = 'hist'
        if 'gpu_id' in merged_params:
            del merged_params['gpu_id']
        print(f"      💻 CPU mode for {ont_name}")
    
    def _train_model():
        # Optimize data format for GPU transfer efficiency
        # Convert to float32 and ensure contiguous memory layout
        X_train_opt = np.ascontiguousarray(X_train, dtype=np.float32)
        
        # Create XGBoost classifier
        xgb_classifier = xgb.XGBClassifier(**merged_params)
        
        # Wrap in OneVsRestClassifier for multi-label
        # n_jobs=-1 enables CPU parallelization across binary classifiers
        model = OneVsRestClassifier(xgb_classifier, n_jobs=DEFAULT_N_JOBS)
        
        # Train model with optimized data format
        model.fit(X_train_opt, y_train)
        return model
    
    model = train_with_error_handling(_train_model, ont_name=ont_name)
    
    if model is not None:
        log_training_success(ont_name)
    
    return model


def _train_ontology_worker(args):
    """
    Worker function for parallel ontology training.
    Each process trains one ontology on its assigned GPU.
    
    Args:
        args: tuple of (X_train, y_train, ont_code, ont_name, gpu_id, hyperparams)
    
    Returns:
        tuple: (ont_code, model) or (ont_code, None)
    """
    X_train, y_train, ont_code, ont_name, gpu_id, hyperparams = args
    
    try:
        model = train_ontology_model_xgb(
            X_train, y_train, ont_code, ont_name, gpu_id=gpu_id, **hyperparams
        )
        return (ont_code, model)
    except Exception as e:
        print(f"      ❌ Error in worker for {ont_name}: {e}")
        import traceback
        traceback.print_exc()
        return (ont_code, None)


def train_all_ontologies_xgb(X_train: np.ndarray, y_train_dict: Dict[str, np.ndarray], 
                            ontologies: Dict[str, str], **hyperparams) -> Dict[str, OneVsRestClassifier]:
    """
    Train XGBoost models for all ontologies.
    
    When multiple GPUs are available, trains ontologies in parallel:
    - F (MFO) -> GPU 0, P (BPO) -> GPU 1, C (CCO) -> GPU 2 (wraps if fewer GPUs)
    
    Each process holds its own CUDA context, allowing multiple GPUs to be utilized
    simultaneously while CPU handles OneVsRestClassifier parallelization.
    
    Note: Each XGBoost model uses ONE GPU. Multi-GPU benefit comes from training
    multiple models concurrently on different GPUs, not splitting single model across GPUs.
    
    Args:
        X_train: Feature matrix
        y_train_dict: dict mapping ont_code -> label matrix
        ontologies: dict mapping ont_code -> ont_name
        **hyperparams: Model hyperparameters
        
    Returns:
        dict: ont_code -> trained model
    """
    print("\n[6/9] Training XGBoost models...")
    
    # Check GPU availability for parallelization decision using centralized utility
    from utils.gpu_utils import get_gpu_info
    gpu_available, num_gpus, _ = get_gpu_info()
    
    # Determine if we should parallelize (multiple GPUs and multiple ontologies)
    should_parallelize = gpu_available and num_gpus > 1 and len(ontologies) > 1
    
    if should_parallelize:
        print(f"   🚀 Parallel training enabled: {num_gpus} GPUs detected, training ontologies concurrently")
        print(f"      GPU assignment: F→GPU0, P→GPU1, C→GPU2")
        
        models = {}
        
        # Prepare arguments for parallel training
        # Each process gets explicit GPU ID (F→0, P→1, C→2)
        tasks = []
        for ont_code, ont_name in ontologies.items():
            if ont_code not in y_train_dict:
                continue
            
            # Map ontology to GPU (F→0, P→1, C→2, wraps if fewer GPUs)
            ont_to_gpu = get_ontology_gpu_mapping()
            gpu_id = ont_to_gpu.get(ont_code, 0) % num_gpus
            
            # Copy data for this process (each process needs its own copy)
            X_train_copy = X_train.copy()
            y_train_copy = y_train_dict[ont_code].copy()
            
            tasks.append((X_train_copy, y_train_copy, ont_code, ont_name, gpu_id, hyperparams))
        
        # Train ontologies in parallel using ProcessPoolExecutor
        # Each process trains one ontology on its assigned GPU
        with ProcessPoolExecutor(max_workers=len(tasks)) as executor:
            future_to_ont = {
                executor.submit(_train_ontology_worker, task): task[2] 
                for task in tasks
            }
            
            for future in as_completed(future_to_ont):
                ont_code, model = future.result()
                if model is not None:
                    models[ont_code] = model
    else:
        # Sequential training (fallback for single GPU or single ontology)
        if num_gpus > 1 and len(ontologies) == 1:
            print(f"   ℹ️  Single ontology training - parallelization not needed")
        elif not gpu_available or num_gpus <= 1:
            print(f"   ℹ️  Single GPU or CPU mode - training sequentially")
        
        models = {}
        
        # Train each ontology sequentially (each assigned to different GPU if available)
        for ont_code, ont_name in ontologies.items():
            if ont_code not in y_train_dict:
                continue
            
            y_ont = y_train_dict[ont_code]
            model = train_ontology_model_xgb(X_train, y_ont, ont_code, ont_name, **hyperparams)
            if model is not None:
                models[ont_code] = model
    
    print(f"   ✓ Trained {len(models)} XGBoost models")
    return models
