"""
Custom grid search for PyTorch neural network models.
Supports k-fold cross-validation for robust hyperparameter selection.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional, Callable, Union
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.model_selection import KFold
import torch

from utils.logging import setup_logging, get_logger
from grid_search.checkpoint_manager import (
    save_checkpoint,
    load_checkpoint,
    normalize_param_combo,
    validate_checkpoint
)

logger = get_logger(__name__)


def run_nn_grid_search(
    train_fn: Callable,
    param_grid: Dict[str, List],
    X_train: Union[np.ndarray, Path],
    y_train: csr_matrix,
    ont_code: str,
    model_name: str = "mlp_v3.1",
    cv: int = 1,
    validation_split: float = 0.2,
    grid_search_epochs: int = 10,
    save_results: bool = True,
    output_dir: Optional[Path] = None,
    checkpoint_path: Optional[Path] = None,
    resume: bool = True
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Run grid search for PyTorch neural network models with k-fold CV support.
    
    Args:
        train_fn: Training function (e.g., train_ontology_model from mlp_trainer_v3)
        param_grid: Dictionary mapping parameter names to lists of values
        X_train: Training features (n_samples, n_features) - numpy array or Path to memmap
        y_train: Training labels (n_samples, n_labels) - scipy sparse CSR matrix
        ont_code: Ontology code ('F', 'P', 'C')
        model_name: Model name for logging and file naming
        cv: Number of CV folds (1 = validation split, 3 = 3-fold CV, 5 = 5-fold CV)
        validation_split: Validation split ratio (used when cv=1)
        grid_search_epochs: Reduced epochs for grid search speed (default: 10)
        save_results: Whether to save results to JSON
        output_dir: Directory to save results (defaults to kaggle/working)
        checkpoint_path: Explicit path to checkpoint file (None = auto-detect)
        resume: Whether to resume from checkpoint if found (default: True)
        
    Returns:
        tuple: (best_params, full_results_dict)
    """
    setup_logging()
    logger.info(f"🔍 Starting neural network grid search for {ont_code} ontology...")
    logger.info(f"   Model: {model_name}")
    logger.info(f"   CV folds: {cv}")
    logger.info(f"   Grid search epochs: {grid_search_epochs}")
    
    start_time = time.time()
    
    # Set up output directory
    if output_dir is None:
        try:
            from config.paths import DATA_OUTPUT_DIR
            if DATA_OUTPUT_DIR:
                output_dir = DATA_OUTPUT_DIR
            else:
                output_dir = Path('kaggle/working')
        except ImportError:
            output_dir = Path('kaggle/working')
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate all parameter combinations
    from itertools import product
    
    param_names = list(param_grid.keys())
    param_values = list(param_grid.values())
    param_combinations = list(product(*param_values))
    
    total_combinations = len(param_combinations)
    logger.info(f"   Total parameter combinations: {total_combinations}")
    
    # Get ontology name for logging
    from config.ontologies import get_ontology_name
    ont_name = get_ontology_name(ont_code)
    
    # Check for checkpoint and resume if requested
    checkpoint = None
    tested_combinations_set = set()
    start_combo_idx = 1
    
    if resume:
        checkpoint = load_checkpoint(checkpoint_path, output_dir, model_name, ont_code)
        if checkpoint:
            # Validate checkpoint matches current grid search settings
            is_valid, error_msg = validate_checkpoint(
                checkpoint, param_grid, cv=cv, grid_search_epochs=grid_search_epochs
            )
            if not is_valid:
                logger.warning(f"   ⚠️  Checkpoint {error_msg} - ignoring checkpoint")
                checkpoint = None
            else:
                # Restore state from checkpoint
                all_results = checkpoint.get('all_results', [])
                best_params = checkpoint.get('best_params')
                best_score = checkpoint.get('best_score', -float('inf'))
                tested_combinations = checkpoint.get('tested_combinations', [])
                
                # Create set of tested combinations for fast lookup
                # Use normalize_param_combo for consistent normalization
                for tested_combo in tested_combinations:
                    normalized = normalize_param_combo(tested_combo)
                    tested_combinations_set.add(normalized)
                
                n_tested = len(tested_combinations)
                start_combo_idx = n_tested + 1
                logger.info(f"   ✅ Resuming from checkpoint: {n_tested}/{total_combinations} combinations already tested")
                logger.info(f"   ✅ Best score so far: {best_score:.4f}")
                if best_params:
                    logger.info(f"   ✅ Best params so far: {best_params}")
        else:
            logger.info(f"   📂 Starting fresh grid search (no checkpoint found)")
    
    # Initialize state (will be overwritten if checkpoint loaded)
    if checkpoint is None:
        all_results = []
        best_score = -float('inf')
        best_params = None
    
    # Prepare CV splits
    n_samples = y_train.shape[0]
    if cv == 1:
        # Single validation split
        splits = [(np.arange(int(n_samples * (1 - validation_split))), 
                  np.arange(int(n_samples * (1 - validation_split)), n_samples))]
        logger.info(f"   Using validation split ({validation_split:.0%})")
    else:
        # k-fold CV
        kfold = KFold(n_splits=cv, shuffle=True, random_state=42)
        splits = list(kfold.split(np.arange(n_samples)))
        logger.info(f"   Using {cv}-fold cross-validation")
    
    # Process each parameter combination
    # Track actual number of tested combinations (not enumerate position)
    n_actually_tested = len(tested_combinations_set) if tested_combinations_set else 0
    
    for combo_idx, param_combo in enumerate(param_combinations):
        # Build hyperparameter dict for this combination
        hyperparams = dict(zip(param_names, param_combo))
        
        # Override epochs for grid search speed
        hyperparams['epochs'] = grid_search_epochs
        
        # Check if this combination was already tested
        normalized_combo = normalize_param_combo(hyperparams)
        if normalized_combo in tested_combinations_set:
            logger.info(f"\n   [{combo_idx + 1}/{total_combinations}] Skipping (already tested): {hyperparams}")
            continue
        
        # Increment counter only for combinations we're actually testing
        n_actually_tested += 1
        logger.info(f"\n   [{n_actually_tested}/{total_combinations}] Testing: {hyperparams}")
        
        # Run CV or validation split
        fold_scores = []
        fold_losses = []
        fold_times = []
        
        for fold_idx, (train_indices, val_indices) in enumerate(splits, 1):
            fold_start = time.time()
            
            logger.info(f"      Fold {fold_idx}/{len(splits)}...")
            
            # Train model with this hyperparameter combination
            try:
                # For CV: subset data to fold's train indices, then use validation_split internally
                # The trainer will further split this into train/val for early stopping
                if isinstance(X_train, (str, Path)):
                    # Memmap paths: can't easily subset, so use full data with validation_split
                    # This means CV won't work perfectly with memmap, but validation split will
                    logger.warning("      ⚠️  Memmap detected - using validation split (CV not fully supported)")
                    model = train_fn(
                        X_train, y_train, ont_code, ont_name,
                        validation_split=validation_split,
                        **hyperparams
                    )
                else:
                    # Subset to fold's training data
                    # The trainer will use validation_split to create train/val from this subset
                    X_fold_data = X_train[train_indices]
                    y_fold_data = y_train[train_indices]
                    
                    # Train on fold's training data (trainer will split internally for early stopping)
                    model = train_fn(
                        X_fold_data, y_fold_data, ont_code, ont_name,
                        validation_split=validation_split,  # Split fold's train data into train/val
                        **hyperparams
                    )
                
                if model is None:
                    logger.warning(f"      ⚠️  Model training returned None - skipping fold")
                    continue
                
                # Evaluate on fold's validation set (val_indices)
                # This is the true hold-out set for this fold
                from models.nn.mlp_trainer_v3 import validate_epoch, SparseDataset
                from torch.utils.data import DataLoader
                from utils.gpu_utils import get_device
                
                device = get_device()
                model.eval()
                
                # Create validation dataset from fold's validation indices
                if isinstance(X_train, (str, Path)):
                    # For memmap, pass path and indices
                    val_dataset = SparseDataset(X_train, y_train, val_indices, label_smoothing=0.0)
                else:
                    val_dataset = SparseDataset(X_train, y_train, val_indices, label_smoothing=0.0)
                
                val_loader = DataLoader(val_dataset, batch_size=hyperparams.get('batch_size', 256), 
                                      shuffle=False, num_workers=0)
                
                # Use same loss as training
                from models.nn.mlp_trainer_v3 import SparseBCEWithLogitsLoss, FocalBCEWithLogitsLoss
                if hyperparams.get('use_focal_loss', False):
                    criterion = FocalBCEWithLogitsLoss(
                        alpha=hyperparams.get('focal_alpha', 0.25),
                        gamma=hyperparams.get('focal_gamma', 2.0)
                    )
                else:
                    criterion = SparseBCEWithLogitsLoss()
                
                # Validate on fold's hold-out set
                val_metrics = validate_epoch(model, val_loader, criterion, device)
                val_f1 = val_metrics['f1_score']
                val_loss = val_metrics['loss']
                
                fold_scores.append(val_f1)
                fold_losses.append(val_loss)
                fold_times.append(time.time() - fold_start)
                
                logger.info(f"         Fold {fold_idx} F1: {val_f1:.4f}, Loss: {val_loss:.4f}")
                
                # Cleanup GPU memory
                del model, val_loader, val_dataset
                if torch.cuda.is_available():
                    torch.cuda.empty_cache()
                
            except Exception as e:
                logger.error(f"      ❌ Error in fold {fold_idx}: {e}")
                continue
        
        if not fold_scores:
            logger.warning(f"   ⚠️  No successful folds for this combination - skipping")
            continue
        
        # Average scores across folds
        avg_f1 = np.mean(fold_scores)
        avg_loss = np.mean(fold_losses)
        avg_time = np.mean(fold_times)
        std_f1 = np.std(fold_scores)
        
        logger.info(f"   ✅ Avg F1: {avg_f1:.4f} (±{std_f1:.4f}), Avg Loss: {avg_loss:.4f}, Time: {avg_time:.1f}s")
        
        # Store results
        result = {
            'params': hyperparams.copy(),
            'mean_f1_score': float(avg_f1),
            'std_f1_score': float(std_f1),
            'mean_loss': float(avg_loss),
            'mean_time': float(avg_time),
            'fold_scores': [float(s) for s in fold_scores],
            'fold_losses': [float(l) for l in fold_losses]
        }
        all_results.append(result)
        
        # Update best
        if avg_f1 > best_score:
            best_score = avg_f1
            best_params = hyperparams.copy()
            logger.info(f"   🎯 New best score: {best_score:.4f}")
        
        # Add to tested combinations set
        tested_combinations_set.add(normalized_combo)
        
        # Save checkpoint after each parameter combination completes
        # Convert tested combinations set back to list of dicts (excluding epochs)
        tested_combinations_list = [
            dict(sorted_combo)  # Convert tuple back to dict
            for sorted_combo in tested_combinations_set
        ]
        save_checkpoint(
            output_dir=output_dir,
            model_name=model_name,
            ont_code=ont_code,
            param_grid=param_grid,
            all_results=all_results,
            best_params=best_params,
            best_score=best_score,
            tested_combinations=tested_combinations_list,
            total_combinations=total_combinations,
            cv=cv,
            grid_search_epochs=grid_search_epochs
        )
    
    logger.info(f"\n   ✅ Best score: {best_score:.4f}")
    logger.info(f"   ✅ Best params: {best_params}")
    
    # Prepare full results
    full_results = {
        'best_params': best_params,
        'best_score': float(best_score),
        'param_grid': param_grid,
        'cv_folds': cv,
        'grid_search_epochs': grid_search_epochs,
        'n_samples': n_samples,
        'n_labels': y_train.shape[1],
        'n_combinations_tested': len(all_results),
        'timestamp': datetime.now().isoformat(),
        'execution_time_seconds': time.time() - start_time,
        'all_results': all_results
    }
    
    # Save results if requested
    if save_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"grid_search_results_{model_name}_{ont_code}_{timestamp}.json"
        filepath = output_dir / filename
        
        # Convert numpy types to Python types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, (np.integer, np.int64)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.bool_):
                return bool(obj)
            return obj
        
        # Clean the results for JSON serialization
        clean_results = json.loads(json.dumps(full_results, default=convert_numpy))
        
        with open(filepath, 'w') as f:
            json.dump(clean_results, f, indent=2)
        
        logger.info(f"   💾 Results saved to: {filepath}")
    
    execution_time = time.time() - start_time
    logger.info(f"   ⏱️  Grid search completed in {execution_time:.1f}s ({execution_time/60:.1f} minutes)")
    
    return best_params, full_results

