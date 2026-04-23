"""
Grid search utility for hyperparameter tuning in CAFA 6 protein function prediction.
Reusable across different model types with configurable parameter grids.
"""

# Import environment-aware paths from config
try:
    from config.paths import DATA_OUTPUT_DIR
except ImportError:
    DATA_OUTPUT_DIR = None

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.model_selection import GridSearchCV, KFold
from sklearn.metrics import make_scorer, f1_score
from sklearn.multiclass import OneVsRestClassifier
from scipy.sparse import issparse


def run_grid_search(
    model_class,
    param_grid: Dict[str, List],
    X_train: np.ndarray,
    y_train: np.ndarray,
    ont_code: str,
    model_type: str = "lr",
    cv: int = 3,
    scoring: str = 'f1_samples',
    n_jobs: int = -1,
    save_results: bool = True,
    output_dir: Optional[Path] = None
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Run grid search for hyperparameter tuning.
    
    Args:
        model_class: Model class to instantiate (e.g., LogisticRegression)
        param_grid: Dictionary mapping parameter names to lists of values
        X_train: Training features (n_samples, n_features)
        y_train: Training labels (n_samples, n_labels)
        ont_code: Ontology code ('F', 'P', 'C')
        model_type: Model type string for filename ('lr', 'xgb', 'nn', etc.)
        cv: Number of cross-validation folds
        scoring: Scoring metric for evaluation
        n_jobs: Number of parallel jobs (-1 for all cores)
        save_results: Whether to save results to JSON
        output_dir: Directory to save results (defaults to kaggle/working)
        
    Returns:
        tuple: (best_params, full_results_dict)
    """
    print(f"🔍 Starting grid search for {ont_code} ontology...")
    print(f"   Parameters: {len(param_grid)} param groups")
    print(f"   CV folds: {cv}")
    print(f"   Scoring: {scoring}")
    
    start_time = time.time()
    
    # Create output directory if needed
    if output_dir is None:
        # Use environment-aware output directory from config
        if DATA_OUTPUT_DIR:
            output_dir = DATA_OUTPUT_DIR
        else:
            project_root = Path(__file__).parent.parent.parent
            output_dir = project_root / 'data' / 'output'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create model instance - check if it needs OneVsRestClassifier wrapper
    base_estimator = model_class()
    
    # XGBoost has built-in multi-label support, others need OneVsRestClassifier
    if hasattr(base_estimator, 'multi_output') and base_estimator.multi_output:
        # XGBoost and other multi-label models
        model = base_estimator
        use_estimator_prefix = False
    else:
        # LogisticRegression and other single-label models
        model = OneVsRestClassifier(base_estimator, n_jobs=n_jobs)
        use_estimator_prefix = True
    
    # Set up cross-validation - use KFold for multilabel data
    cv_strategy = KFold(n_splits=cv, shuffle=True, random_state=42)
    
    # Create scorer for multilabel classification
    if scoring == 'f1_samples':
        scorer = make_scorer(f1_score, average='samples', zero_division=0)
    else:
        scorer = scoring
    
    # Convert sparse labels to dense if needed (but keep sparse for large label spaces)
    # For large label spaces (>10k terms), sparse matrices reduce memory significantly
    if hasattr(y_train, 'toarray'):
        # Check if label space is large - keep sparse for memory efficiency
        n_labels = y_train.shape[1]
        if n_labels > 10000:
            # Keep sparse for large label spaces to reduce memory pressure
            print(f"   ⚠️  Large label space detected ({n_labels} terms) - using sparse matrices for memory efficiency")
            y_train_dense = y_train  # Keep sparse
        else:
            # Convert to dense for smaller label spaces (more efficient computation)
            y_train_dense = y_train.toarray()
    else:
        y_train_dense = y_train
    
    # Transform param_grid based on model type
    if use_estimator_prefix:
        # For OneVsRestClassifier, parameters need 'estimator__' prefix
        transformed_param_grid = {}
        for param, values in param_grid.items():
            transformed_param_grid[f'estimator__{param}'] = values
    else:
        # For XGBoost and other multi-label models, use parameters directly
        transformed_param_grid = param_grid
    
    # Run grid search
    print(f"   Running {len(transformed_param_grid)} parameter combinations...")
    grid_search = GridSearchCV(
        estimator=model,
        param_grid=transformed_param_grid,
        cv=cv_strategy,
        scoring=scorer,
        n_jobs=n_jobs,
        verbose=1,
        return_train_score=True
    )
    
    # Fit the grid search
    grid_search.fit(X_train, y_train_dense)
    
    # Extract results
    best_params_raw = grid_search.best_params_
    best_score = grid_search.best_score_
    
    # Transform best_params back to original parameter names
    best_params = {}
    for param, value in best_params_raw.items():
        if use_estimator_prefix and param.startswith('estimator__'):
            # Remove 'estimator__' prefix for OneVsRestClassifier
            original_param = param[11:]  # Remove 'estimator__' prefix
            best_params[original_param] = value
        else:
            # Keep parameter as-is for direct model usage (XGBoost, etc.)
            best_params[param] = value
    
    print(f"   ✅ Best score: {best_score:.4f}")
    print(f"   ✅ Best params: {best_params}")
    
    # Prepare full results
    results_df = pd.DataFrame(grid_search.cv_results_)
    full_results = {
        'best_params': best_params,
        'best_score': float(best_score),
        'param_grid': param_grid,
        'cv_folds': cv,
        'scoring': scoring,
        'n_samples': X_train.shape[0],
        'n_features': X_train.shape[1],
        'n_labels': y_train.shape[1],
        'timestamp': datetime.now().isoformat(),
        'execution_time_seconds': time.time() - start_time,
        'cv_results': results_df.to_dict('records')
    }
    
    # Save results if requested
    if save_results:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"grid_search_results_{model_type}_{ont_code}_{timestamp}.json"
        filepath = output_dir / filename
        
        # Convert numpy types to Python types for JSON serialization
        def convert_numpy(obj):
            if isinstance(obj, np.integer):
                return int(obj)
            elif isinstance(obj, np.floating):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return obj.tolist()
            return obj
        
        # Clean the results for JSON serialization
        clean_results = json.loads(json.dumps(full_results, default=convert_numpy))
        
        with open(filepath, 'w') as f:
            json.dump(clean_results, f, indent=2)
        
        print(f"   💾 Results saved to: {filepath}")
    
    execution_time = time.time() - start_time
    print(f"   ⏱️  Grid search completed in {execution_time:.1f}s")
    
    return best_params, full_results


def load_grid_search_results(filepath: Path) -> Dict[str, Any]:
    """
    Load grid search results from JSON file.
    
    Args:
        filepath: Path to JSON results file
        
    Returns:
        dict: Loaded results
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def compare_grid_search_results(result_files: List[Path]) -> pd.DataFrame:
    """
    Compare multiple grid search results.
    
    Args:
        result_files: List of paths to result JSON files
        
    Returns:
        DataFrame with comparison of best parameters and scores
    """
    results = []
    
    for filepath in result_files:
        data = load_grid_search_results(filepath)
        result = {
            'file': filepath.name,
            'ontology': filepath.stem.split('_')[-2],  # Extract ontology from filename
            'best_score': data['best_score'],
            'execution_time': data['execution_time_seconds'],
            **data['best_params']
        }
        results.append(result)
    
    return pd.DataFrame(results)


def get_best_params_summary(results_dir: Path, model_type: str = "logistic") -> Dict[str, Any]:
    """
    Get summary of best parameters across all ontologies.
    
    Args:
        results_dir: Directory containing grid search results
        model_type: Model type to filter results
        
    Returns:
        dict: Summary of best parameters by ontology
    """
    result_files = list(results_dir.glob(f"grid_search_results_{model_type}_*.json"))
    
    if not result_files:
        return {}
    
    summary = {}
    
    for filepath in result_files:
        data = load_grid_search_results(filepath)
        ont_code = filepath.stem.split('_')[-2]
        summary[ont_code] = {
            'best_params': data['best_params'],
            'best_score': data['best_score'],
            'timestamp': data['timestamp']
        }
    
    return summary


def save_best_results_summary(results_dir: Path, model_type: str = "logistic", 
                            version: str = "1.1") -> Path:
    """
    Save a consolidated summary of best results for easy reference.
    
    Args:
        results_dir: Directory containing grid search results
        model_type: Model type to filter results
        version: Version number for the results (e.g., "2.0", "2.1")
        
    Returns:
        Path to saved summary file
    """
    summary = get_best_params_summary(results_dir, model_type)
    
    if not summary:
        raise ValueError(f"No grid search results found for {model_type}")
    
    # Create consolidated summary
    consolidated = {
        'version': version,
        'model_type': model_type,
        'created_at': datetime.now().isoformat(),
        'ontologies': summary,
        'unified_params': _get_unified_params(summary),
        'notes': f"Grid search results for {model_type} v{version}"
    }
    
    # Save to file
    filename = f"best_results_{model_type}_v{version}.json"
    filepath = results_dir / filename
    
    with open(filepath, 'w') as f:
        json.dump(consolidated, f, indent=2)
    
    print(f"💾 Best results summary saved: {filepath}")
    return filepath


def _get_unified_params(ontology_summary: Dict[str, Any]) -> Dict[str, Any]:
    """
    Get unified parameters when ontologies have similar best params.
    
    Args:
        ontology_summary: Summary of best params by ontology
        
    Returns:
        dict: Unified parameters or note about differences
    """
    if len(ontology_summary) == 1:
        return list(ontology_summary.values())[0]['best_params']
    
    # Check if all ontologies have the same best params
    first_params = list(ontology_summary.values())[0]['best_params']
    all_same = all(
        data['best_params'] == first_params 
        for data in ontology_summary.values()
    )
    
    if all_same:
        return first_params
    else:
        return {
            'note': 'Ontologies have different optimal parameters',
            'per_ontology': {ont: data['best_params'] for ont, data in ontology_summary.items()}
        }


def load_best_results_summary(filepath: Path) -> Dict[str, Any]:
    """
    Load a consolidated best results summary.
    
    Args:
        filepath: Path to summary JSON file
        
    Returns:
        dict: Loaded summary
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def create_versioned_trainer_params(summary_file: Path) -> Dict[str, Any]:
    """
    Generate parameter updates for trainer based on best results.
    
    Args:
        summary_file: Path to best results summary
        
    Returns:
        dict: Parameter updates to apply to trainer
    """
    summary = load_best_results_summary(summary_file)
    
    # Extract unified or per-ontology parameters
    unified_params = summary['unified_params']
    
    if 'note' in unified_params:
        # Different params per ontology - return per-ontology structure
        return {
            'type': 'per_ontology',
            'params': unified_params['per_ontology'],
            'version': summary['version'],
            'notes': 'Different optimal parameters per ontology'
        }
    else:
        # Same params for all ontologies
        return {
            'type': 'unified',
            'params': unified_params,
            'version': summary['version'],
            'notes': 'Unified optimal parameters for all ontologies'
        }
