"""
Training workflow orchestrator for CAFA 6 protein function prediction.
High-level orchestration that delegates to focused modules.
"""

import time
import numpy as np
from pathlib import Path
from typing import Dict, Optional, List, Tuple, Any, Union
from sklearn.model_selection import train_test_split

from config import (
    get_model_config, get_model_trainer,
    get_all_ontologies, ONTOLOGY_CODES
)
from config.training import DEFAULT_RANDOM_SEED, FREE_FEATURES_AFTER_ONTOLOGY, VALIDATION_SPLIT_SIZE
from pipelines.workflows.workflow_paths import setup_workflow_paths
from utils.utils_common import cleanup_memory
from utils.logging import setup_logging, get_logger
from pipelines.workflows.training.data_streaming import (
    load_training_data_streaming,
    extract_features_streaming,
    prepare_labels_streaming
)
from pipelines.workflows.training.model_training import train_single_ontology_model

logger = get_logger(__name__)


def _prepare_training_data(model_config: Dict[str, Any], ont_codes: Optional[List[str]] = None) -> Tuple[Dict[str, str], np.ndarray, List[str], Dict[str, Any], Dict[str, Any]]:
    """
    Prepare training data: load sequences, extract features, prepare labels.
    Shared data preparation logic for all training functions.
    
    Args:
        model_config: Model configuration dict
        ont_codes: Optional list of ontology codes (if None, uses all)
        
    Returns:
        tuple: (train_seqs, X_train, y_train_proteins, mlb_dict, y_train_dict)
    """
    data_dir, _ = setup_workflow_paths(test=False)
    
    train_seqs, train_terms, train_taxonomy = load_training_data_streaming(data_dir, use_streaming=True)
    
    # Extract features using streaming
    X_train, y_train_proteins = extract_features_streaming(
        train_seqs, model_config, use_streaming=True
    )
    
    # Prepare labels per-ontology
    if ont_codes is None:
        ont_codes = ONTOLOGY_CODES  # ONTOLOGY_CODES is already a list
    
    mlb_dict, y_train_dict = prepare_labels_streaming(
        train_terms, y_train_proteins, ont_codes, use_per_ontology=True
    )
    
    return train_seqs, X_train, y_train_proteins, mlb_dict, y_train_dict


def _prepare_validation_split(X_train: Union[np.ndarray, Path], 
                             y_train_proteins: List[str],
                             y_train_dict: Dict[str, Any],
                             enable_threshold_opt: bool) -> Tuple[Optional[Union[np.ndarray, Path]], Dict[str, Any], Union[np.ndarray, Path], List[str]]:
    """
    Prepare validation split if threshold optimization is enabled.
    
    Args:
        X_train: Training feature matrix
        y_train_proteins: List of protein IDs
        y_train_dict: Dict mapping ont_code -> label matrix
        enable_threshold_opt: Whether to create validation split
        
    Returns:
        tuple: (X_val, y_val_dict, X_train_updated, y_train_proteins_updated)
               If enable_threshold_opt=False, returns (None, {}, X_train, y_train_proteins)
    """
    if not enable_threshold_opt:
        return None, {}, X_train, y_train_proteins
    
    logger.info("Creating validation split for threshold optimization...")
    val_indices, train_indices = train_test_split(
        np.arange(len(y_train_proteins)),
        test_size=VALIDATION_SPLIT_SIZE,
        random_state=DEFAULT_RANDOM_SEED
    )
    
    # Handle memmap path - load as memmap for indexing
    if isinstance(X_train, Path):
        from utils.memory_efficient import load_features_memmap
        X_train_memmap = load_features_memmap(X_train)
        X_val = X_train_memmap[val_indices]
        X_train_updated = X_train_memmap[train_indices]
        # Note: We return arrays here, not memmap paths, since we've already indexed
        # The original memmap file remains for potential reuse
    else:
        X_val = X_train[val_indices]
        X_train_updated = X_train[train_indices]
    
    # Update protein lists
    original_proteins = y_train_proteins.copy()
    y_train_proteins_updated = [original_proteins[i] for i in train_indices]
    y_val_proteins = [original_proteins[i] for i in val_indices] if val_indices is not None else []
    
    # Split labels per ontology
    y_val_dict = {}
    for ont_code in y_train_dict.keys():
        y_val_dict[ont_code] = y_train_dict[ont_code][val_indices]
        y_train_dict[ont_code] = y_train_dict[ont_code][train_indices]
    
    return X_val, y_val_dict, X_train_updated, y_train_proteins_updated


def _validate_ontologies_for_training(ont_codes: List[str], 
                                      y_train_dict: Dict[str, Any], 
                                      model_config: Dict[str, Any],
                                      mode: str) -> List[str]:
    """
    Validate ontologies for training and filter based on mode.
    
    Args:
        ont_codes: List of ontology codes to validate
        y_train_dict: Dict mapping ont_code -> label matrix
        model_config: Model configuration dict
        mode: Training mode ('load_or_train', 'train_new', 'load_only')
        
    Returns:
        list: Valid ontology codes that should be trained
    """
    from utils.model_io import check_model_exists
    
    valid_ont_codes = []
    for ont_code in ont_codes:
        if ont_code not in y_train_dict:
            logger.warning(f"Skipping {ont_code} (no data)")
            continue
        
        # Check if should train based on mode
        model_exists = check_model_exists(ont_code, model_config['type'], model_config['version'])
        if mode == "load_or_train" and model_exists:
            logger.info(f"{ont_code} model exists - will load instead of train")
        elif mode == "load_only" and not model_exists:
            raise FileNotFoundError(f"❌ {ont_code} model not found and mode is load_only")
        else:
            valid_ont_codes.append(ont_code)
    
    return valid_ont_codes


def run_train_all(model_name: str, mode: Optional[str] = None, model_config_override: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Run training pipeline: Data Prep -> Train All -> Save Models.
    Uses streaming data loaders to avoid loading all data into memory.
    
    Args:
        model_name: Model configuration name
        mode: Model loading/training mode ('load_or_train', 'train_new', 'load_only')
        model_config_override: Optional model config dict with overrides (e.g., feature override from CLI)
        
    Returns:
        dict: ont_code -> model (paths for neural networks, objects for sklearn)
    """
    setup_logging()
    logger.info("Starting Train All Pipeline")
    print("=" * 60)
    
    start_time = time.time()
    
    # Get and validate mode
    if mode is None:
        mode = 'train_new'
    logger.info(f"Mode: {mode}")
    
    # Get model configuration (use override if provided)
    if model_config_override:
        model_config = model_config_override
    else:
        model_config = get_model_config(model_name)
    logger.info(f"Using model: {model_config['description']}")
    
    # Data Preparation - Use streaming loaders
    logger.info("[STEP 1] Data Preparation (streaming)...")
    prep_start = time.time()
    
    train_seqs, X_train, y_train_proteins, mlb_dict, y_train_dict = _prepare_training_data(
        model_config, ont_codes=None
    )
    
    print(f"   ⏱️  Data prep time: {time.time() - prep_start:.1f}s")
    
    # Check if threshold optimization is enabled
    from config.prediction import PREDICTION_SETTINGS
    pred_settings = PREDICTION_SETTINGS
    enable_threshold_opt = pred_settings.get("enable_threshold_optimization", False)
    
    # Create validation split if threshold optimization is enabled
    X_val, y_val_dict, X_train, y_train_proteins = _prepare_validation_split(
        X_train, y_train_proteins, y_train_dict, enable_threshold_opt
    )
    
    # Train All Models - Sequential with save/cleanup to prevent GPU memory overflow
    print("\n🤖 [STEP 2] Training All Models (Sequential)...")
    train_start = time.time()
    
    ontologies = get_all_ontologies()
    models = {}
    model_times = {}
    
    from utils.ontology_utils import iterate_ontologies_with_check
    
    for ont_code, ont_name in iterate_ontologies_with_check(
        ontologies,
        y_train_dict,
        skip_message=" (no data)"
    ):
        model_result, ont_time = train_single_ontology_model(
            X_train=X_train,
            y_train_dict=y_train_dict,
            mlb_dict=mlb_dict,
            ont_code=ont_code,
            ont_name=ont_name,
            model_name=model_name,
            model_config=model_config,
            mode=mode,
            X_val=X_val,
            y_val_dict=y_val_dict,
            enable_threshold_opt=enable_threshold_opt
        )
        
        if model_result is not None:
            models[ont_code] = model_result
            model_times[ont_name] = ont_time
        
        # Free features after each ontology if enabled
        if FREE_FEATURES_AFTER_ONTOLOGY and ont_code != list(ontologies.keys())[-1]:
            # Don't free on last ontology (might be needed for return)
            # In practice, features are freed per-ontology in model_training
            pass
    
    train_elapsed = time.time() - train_start
    
    # Print training summary
    logger.info("Training Summary:")
    print("=" * 60)
    for ont_name, elapsed in model_times.items():
        logger.info(f"   {ont_name}: {elapsed:.1f}s")
    logger.info(f"   Total training time: {train_elapsed:.1f}s")
    print("=" * 60)
    
    total_time = time.time() - start_time
    logger.info("Train All Pipeline Complete!")
    logger.info(f"Total time: {total_time:.1f}s")
    logger.info(f"Trained {len(models)} models")
    
    return models


def run_train_single_ontology(model_name: str, ont_code: str, mode: Optional[str] = None, model_config_override: Optional[Dict] = None) -> Any:
    """
    Run training for single ontology: Data Prep -> Train Single -> Save Model.
    
    Args:
        model_name: Model configuration name
        ont_code: Ontology code ('F', 'P', 'C')
        mode: Model loading/training mode
        model_config_override: Optional model config dict with overrides (e.g., feature override from CLI)
        
    Returns:
        trained model object
    """
    setup_logging()
    logger.info(f"Starting Single Ontology Training: {ont_code}")
    print("=" * 60)
    
    start_time = time.time()
    
    mode = mode or 'train_new'
    logger.info(f"Mode: {mode}")
    
    # Get model configuration (use override if provided)
    if model_config_override:
        model_config = model_config_override
    else:
        model_config = get_model_config(model_name)
    logger.info(f"Using model: {model_config['description']}")
    
    # Data Preparation
    logger.info("[STEP 1] Data Preparation...")
    prep_start = time.time()
    
    train_seqs, X_train, y_train_proteins, mlb_dict, y_train_dict = _prepare_training_data(
        model_config, ont_codes=[ont_code]
    )
    
    logger.info(f"Data prep time: {time.time() - prep_start:.1f}s")
    
    # Train single model
    logger.info(f"[STEP 2] Training {ont_code} Model...")
    train_start = time.time()
    
    from config import get_ontology_name
    ont_name = get_ontology_name(ont_code)
    
    model_result, ont_time = train_single_ontology_model(
        X_train=X_train,
        y_train_dict=y_train_dict,
        mlb_dict=mlb_dict,
        ont_code=ont_code,
        ont_name=ont_name,
        model_name=model_name,
        model_config=model_config,
        mode=mode,
        enable_threshold_opt=False
    )
    
    logger.info(f"Training time: {time.time() - train_start:.1f}s")
    
    # Memory cleanup
    del train_seqs, X_train
    cleanup_memory()
    
    total_time = time.time() - start_time
    logger.info("Single Ontology Training Complete!")
    logger.info(f"Total time: {total_time:.1f}s")
    
    return model_result


def run_train_parallel_ontologies(model_name: str, ont_codes: List[str], mode: Optional[str] = None, model_config_override: Optional[Dict] = None) -> Dict[str, Any]:
    """
    Train multiple ontologies in parallel.
    Each ontology trains on a different thread, allowing better resource utilization.
    
    Args:
        model_name: Model configuration name
        ont_codes: List of ontology codes to train (e.g., ['P', 'C'])
        mode: Model loading/training mode
        model_config_override: Optional model config dict with overrides (e.g., feature override from CLI)
        
    Returns:
        dict: ont_code -> trained model (paths for neural networks, objects for sklearn)
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from multiprocessing import cpu_count
    from utils.model_io import check_model_exists
    
    setup_logging()
    logger.info(f"Starting Parallel Training: {', '.join(ont_codes)}")
    print("=" * 60)
    
    start_time = time.time()
    mode = mode or 'train_new'
    logger.info(f"Mode: {mode}")
    
    # Get model configuration (use override if provided)
    if model_config_override:
        model_config = model_config_override
    else:
        model_config = get_model_config(model_name)
    logger.info(f"Using model: {model_config['description']}")
    
    # Data Preparation (shared across all ontologies)
    logger.info("[STEP 1] Data Preparation (shared)...")
    prep_start = time.time()
    
    train_seqs, X_train, y_train_proteins, mlb_dict, y_train_dict = _prepare_training_data(
        model_config, ont_codes=ont_codes
    )
    
    logger.info(f"Data prep time: {time.time() - prep_start:.1f}s")
    
    # Validate ontologies
    valid_ont_codes = _validate_ontologies_for_training(
        ont_codes, y_train_dict, model_config, mode
    )
    
    if not valid_ont_codes:
        logger.warning("No ontologies to train in parallel")
        return {}
    
    # Train ontologies in parallel using ThreadPoolExecutor
    max_workers = min(len(valid_ont_codes), cpu_count())
    logger.info(f"[STEP 2] Training {len(valid_ont_codes)} ontologies in parallel (workers: {max_workers})...")
    
    models = {}
    model_times = {}
    
    def train_ontology_worker(ont_code: str):
        """Worker function for parallel training."""
        from config import get_ontology_name
        ont_name = get_ontology_name(ont_code)
        
        try:
            logger.info(f"[Parallel] Starting {ont_name} ({ont_code})...")
            model_result, ont_time = train_single_ontology_model(
                X_train=X_train,
                y_train_dict=y_train_dict,
                mlb_dict=mlb_dict,
                ont_code=ont_code,
                ont_name=ont_name,
                model_name=model_name,
                model_config=model_config,
                mode=mode,
                enable_threshold_opt=False
            )
            model_times[ont_name] = ont_time
            logger.info(f"[Parallel] ✓ Completed {ont_name} ({ont_code})")
            return (ont_code, model_result)
        except Exception as e:
            logger.error(f"[Parallel] ❌ Error training {ont_code}: {e}")
            import traceback
            traceback.print_exc()
            return (ont_code, None)
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_ont = {
            executor.submit(train_ontology_worker, ont_code): ont_code
            for ont_code in valid_ont_codes
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_ont):
            ont_code = future_to_ont[future]
            try:
                result_ont_code, model_result = future.result()
                if model_result is not None:
                    models[result_ont_code] = model_result
            except Exception as e:
                logger.error(f"{ont_code} training failed: {e}")
    
    total_time = time.time() - start_time
    logger.info("Parallel Training Complete!")
    logger.info(f"Total time: {total_time:.1f}s")
    logger.info(f"Trained {len(models)} models in parallel")
    
    return models

