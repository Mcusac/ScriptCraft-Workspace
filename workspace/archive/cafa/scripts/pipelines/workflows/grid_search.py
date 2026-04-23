"""
Grid search workflow: Data Prep -> Grid Search -> Save Results.
Handles hyperparameter tuning for specified model and ontologies.
"""

import time
from pathlib import Path
from typing import Optional

from config import (
    get_model_config, 
    get_grid_search_config, 
    KAGGLE_ENV,
    get_ontology_name,
    LARGE_LABEL_SPACE_THRESHOLD,
    MEDIUM_LABEL_SPACE_THRESHOLD
)
from pipelines.workflows.workflow_paths import setup_workflow_paths
from utils.utils_common import cleanup_memory
from preprocessing.data_prep import load_training_data, prepare_ontology_labels
from preprocessing.feature_extraction import extract_features
from grid_search.grid_search import run_grid_search, save_best_results_summary
from grid_search.nn_grid_search import run_nn_grid_search


def get_model_class_for_grid_search(model_type: str, model_config: dict = None):
    """
    Get the model class or trainer function for grid search based on model type.
    
    Args:
        model_type: Model type (e.g., 'lr', 'xgb', 'nn')
        model_config: Model configuration dict (required for 'nn' type)
        
    Returns:
        Model class to instantiate (for sklearn models) or trainer function (for nn)
    """
    if model_type == 'lr':
        from sklearn.linear_model import LogisticRegression
        return LogisticRegression
    elif model_type == 'xgb':
        from xgboost import XGBClassifier
        return XGBClassifier
    elif model_type == 'nn':
        # For neural networks, return the trainer function
        if model_config is None:
            raise ValueError("model_config required for neural network grid search")
        
        trainer_module = model_config.get('trainer_module', 'nn.mlp_trainer_v3')
        # Import the trainer function dynamically
        module_parts = trainer_module.split('.')
        if len(module_parts) == 2:
            module_name, function_name = module_parts
            if module_name == 'nn' and function_name == 'mlp_trainer_v3':
                from models.nn.mlp_trainer_v3 import train_ontology_model
                return train_ontology_model
            else:
                raise ValueError(f"Unknown trainer module: {trainer_module}")
        else:
            raise ValueError(f"Invalid trainer_module format: {trainer_module}")
    else:
        raise ValueError(f"Unknown model type: {model_type}")


def run_grid_search_pipeline(
    model_name: str, 
    ontology: str = 'all', 
    cv: int = 3, 
    quick: bool = False,
    checkpoint_path: Optional[Path] = None,
    resume: bool = True
) -> Optional[str]:
    """
    Run grid search pipeline: Data Prep -> Grid Search -> Save Results.
    
    Args:
        model_name: Model configuration name
        ontology: Ontology to tune ('F', 'P', 'C', or 'all')
        cv: Number of cross-validation folds
        quick: Use smaller parameter grid for quick testing
        checkpoint_path: Explicit path to checkpoint file (None = auto-detect)
        resume: Whether to resume from checkpoint if found (default: True)
        
    Returns:
        str: Path to consolidated results summary file
    """
    print("🔍 Starting Grid Search Pipeline")
    print("=" * 60)
    
    start_time = time.time()
    
    # Get model configuration
    model_config = get_model_config(model_name)
    print(f"📋 Model: {model_config['description']}")
    print(f"📋 Ontology: {ontology}")
    print(f"📋 CV folds: {cv}")
    print(f"📋 Quick mode: {quick}")
    
    # Set up paths
    data_dir, output_dir = setup_workflow_paths(test=False)
    
    # Data Preparation
    print("\n🔧 [STEP 1] Loading Training Data...")
    prep_start = time.time()
    
    train_seqs, train_terms, train_taxonomy = load_training_data(data_dir)
    
    # Feature extraction - use model's feature type
    # For neural networks, use fused_embeddings; for others, use hand_crafted
    if model_config['type'] == 'nn':
        feature_type = model_config.get('feature_type', 'fused_embeddings')
        feature_preset = model_config.get('feature_preset', 'default')
        extraction_config = {
            'feature_type': feature_type,
            'feature_preset': feature_preset
        }
        print(f"   Using {feature_type} features (preset: {feature_preset})")
    else:
        # For sklearn models, use handcrafted features (faster)
        extraction_config = {'feature_type': 'hand_crafted'}
    
    X_train_result, y_train_proteins = extract_features(
        sequences=train_seqs,
        config=extraction_config,
        datatype='train',
        force_memmap=False  # Grid search needs full arrays (or memmap paths)
    )
    
    # Handle memmap path (neural networks may use memmap for large embeddings)
    # For grid search, we can use memmap paths directly (nn_grid_search supports it)
    if isinstance(X_train_result, Path):
        if model_config['type'] == 'nn':
            # Neural networks can use memmap paths directly
            X_train = X_train_result
            print(f"   Using memmap features: {X_train_result}")
        else:
            # Sklearn models need arrays
            from utils.memory_efficient import load_features_memmap
            X_train = np.array(load_features_memmap(X_train_result))
    else:
        X_train = X_train_result
    
    from config import get_ontology_name, ONTOLOGY_CODES, get_all_ontologies
    
    # Determine ontologies to run
    if ontology == 'all':
        ont_codes_list = ONTOLOGY_CODES
        ontologies = get_all_ontologies()
    else:
        try:
            ont_name = get_ontology_name(ontology)
            ont_codes_list = [ontology]
            ontologies = {ontology: ont_name}
        except ValueError:
            raise ValueError(f"Invalid ontology: {ontology}")
    
    mlb_dict, y_train_dict = prepare_ontology_labels(train_terms, y_train_proteins, ont_codes_list)
    
    # Report feature info (handle both arrays and memmap paths)
    if isinstance(X_train, Path):
        # For memmap, try to get shape from metadata or estimate
        try:
            from utils.memory_efficient import load_features_memmap
            temp_X = load_features_memmap(X_train)
            n_samples, n_features = temp_X.shape
            del temp_X
            print(f"   ✓ Features: {n_features:,} (memmap)")
            print(f"   ✓ Samples: {n_samples:,}")
        except:
            print(f"   ✓ Features: memmap (shape unknown)")
    else:
        import numpy as np
        print(f"   ✓ Features: {X_train.shape[1]:,}")
        print(f"   ✓ Samples: {X_train.shape[0]:,}")
    print(f"   ⏱️  Data prep time: {time.time() - prep_start:.1f}s")
    
    # Get model class/trainer for grid search
    model_class_or_trainer = get_model_class_for_grid_search(model_config['type'], model_config)
    
    # Get grid search configuration
    gs_config = get_grid_search_config(model_config['type'])
    param_grid = gs_config['quick_param_grid'] if quick else gs_config['param_grid']
    grid_search_epochs = gs_config.get('grid_search_epochs', 10)  # For neural networks
    
    # Handle GPU availability for XGBoost using centralized utility
    if model_config['type'] == 'xgb':
        from utils.gpu_utils import check_gpu_available
        gpu_available = check_gpu_available()
        
        if not gpu_available:
            print("   ⚠️  GPU not detected - using CPU parameters")
            param_grid = {k: v for k, v in param_grid.items() if k not in ['tree_method', 'gpu_id']}
            param_grid['tree_method'] = ['hist']
        else:
            print("   ✓ GPU detected - using GPU acceleration")
    
    # Adjust n_jobs for Kaggle environment to avoid memory issues
    n_jobs = gs_config.get('n_jobs', -1)
    if KAGGLE_ENV and n_jobs == -1:
        n_jobs = 2  # Reduce parallelism on Kaggle to save memory
        print(f"   📊 Kaggle environment detected - reducing n_jobs to {n_jobs}")
    
    # Run grid search for each ontology
    print("\n🔍 [STEP 2] Running Grid Search...")
    all_results = {}
    
    from utils.ontology_utils import iterate_ontologies_with_check
    
    for ont_code, ont_name in iterate_ontologies_with_check(
        ontologies,
        y_train_dict,
        skip_message=" (no terms)"
    ):
        # Additional check for empty terms
        if y_train_dict[ont_code].shape[1] == 0:
            print(f"   ⚠️  Skipping {ont_name} ({ont_code}) - no terms")
            continue
        
        y_ont = y_train_dict[ont_code]
        print(f"\n   🎯 Grid search for {ont_name} ({ont_code})")
        print(f"      Labels: {y_ont.shape[1]} terms")
        
        gs_start = time.time()
        
        # Get per-ontology parameter grid if available
        ont_gs_config = get_grid_search_config(model_config['type'], ont_code)
        ont_param_grid = ont_gs_config['quick_param_grid'] if quick else ont_gs_config['param_grid']
        
        # Adjust CV folds for large label spaces to reduce memory pressure
        adaptive_cv = cv
        if y_ont.shape[1] > LARGE_LABEL_SPACE_THRESHOLD:
            adaptive_cv = max(2, cv - 1)  # Reduce CV folds for large label spaces
            print(f"      ⚠️  Large label space - reducing CV folds from {cv} to {adaptive_cv} for memory efficiency")
        elif y_ont.shape[1] > MEDIUM_LABEL_SPACE_THRESHOLD:
            adaptive_cv = max(2, cv - 1)  # Reduce CV folds for medium label spaces too
            print(f"      ⚠️  Medium label space - reducing CV folds from {cv} to {adaptive_cv} for memory efficiency")
        
        try:
            # Use different grid search function for neural networks
            if model_config['type'] == 'nn':
                best_params, full_results = run_nn_grid_search(
                    train_fn=model_class_or_trainer,
                    param_grid=ont_param_grid,
                    X_train=X_train,
                    y_train=y_ont,
                    ont_code=ont_code,
                    model_name=model_name,
                    cv=adaptive_cv,
                    validation_split=0.2,
                    grid_search_epochs=grid_search_epochs,
                    save_results=True,
                    output_dir=output_dir,
                    checkpoint_path=checkpoint_path,
                    resume=resume
                )
            else:
                best_params, full_results = run_grid_search(
                    model_class=model_class_or_trainer,
                    param_grid=ont_param_grid,
                    X_train=X_train,
                    y_train=y_ont,
                    ont_code=ont_code,
                    model_type=model_config['type'],
                    cv=adaptive_cv,
                    scoring=gs_config.get('scoring', 'f1_samples'),
                    n_jobs=n_jobs,
                    save_results=True,
                    output_dir=output_dir
                )
            
            all_results[ont_code] = {
                'best_params': best_params,
                'best_score': full_results['best_score'],
                'execution_time': full_results['execution_time_seconds']
            }
            
            print(f"      ✅ Best score: {full_results['best_score']:.4f}")
            print(f"      ⏱️  Time: {time.time() - gs_start:.1f}s")
            
        except Exception as e:
            print(f"      ❌ Error: {e}")
            continue
        
        finally:
            # Force garbage collection between ontologies
            cleanup_memory()
    
    # Summary and consolidated results
    print(f"\n📋 Grid Search Summary")
    print("=" * 60)
    
    if all_results:
        for ont_code, results in all_results.items():
            ont_name = get_ontology_name(ont_code)
            print(f"{ont_name} ({ont_code}):")
            print(f"  Best score: {results['best_score']:.4f}")
            print(f"  Best params: {results['best_params']}")
            print(f"  Time: {results['execution_time']:.1f}s")
            print()
        
        # Save consolidated best results summary
        try:
            summary_file = save_best_results_summary(output_dir, model_config['type'], model_config['version'])
            print(f"💾 Consolidated results saved: {summary_file}")
        except Exception as e:
            print(f"⚠️  Could not save consolidated summary: {e}")
        
        total_time = time.time() - start_time
        print(f"\n✅ Grid Search Pipeline Complete!")
        print(f"⏱️  Total execution time: {total_time:.1f}s")
        print(f"\n🎯 Next steps:")
        print(f"1. Review results in {output_dir}/grid_search_results_*.json")
        print(f"2. Check consolidated summary in {output_dir}/best_results_*.json")
        print(f"3. Update config.py {model_name} hyperparams with best parameters")
        
        return str(summary_file)
    
    else:
        print("❌ No successful grid searches completed")
        return None
