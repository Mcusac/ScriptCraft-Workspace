"""
Full pipeline workflow: Train All -> Predict.
End-to-end execution by delegating to training and prediction workflows.
"""

import time
from typing import Optional, Dict

from config import get_model_config
from pipelines.workflows.training import run_train_all
from pipelines.workflows.prediction import run_predict_from_saved
from utils.cli_utils import create_model_specs_from_name
from utils.logging import setup_logging


def run_full_pipeline(model_name: str, output_name: Optional[str] = None, mode: Optional[str] = None, model_config_override: Optional[Dict] = None) -> str:
    """
    Run complete pipeline: Train All -> Predict.
    Delegates to training and prediction workflows to avoid code duplication.
    
    Args:
        model_name: Model configuration name
        output_name: Optional custom output filename
        mode: Model loading/training mode ('load_or_train', 'train_new', 'load_only')
        model_config_override: Optional model config dict with overrides (e.g., feature override from CLI)
        
    Returns:
        str: Path to final submission file
    """
    setup_logging()
    print("🚀 Starting Full Pipeline")
    print("=" * 60)
    
    start_time = time.time()
    
    # Get model configuration (use override if provided)
    if model_config_override:
        model_config = model_config_override
    else:
        model_config = get_model_config(model_name)
    print(f"📋 Using model: {model_config['description']}")
    
    # Set mode (default to load_or_train for full pipeline)
    mode = mode or 'load_or_train'
    print(f"📋 Mode: {mode}")
    
    # Step 1: Train All Models (delegate to training workflow)
    print("\n🤖 [STEP 1] Training All Models...")
    print("=" * 60)
    
    models = run_train_all(model_name, mode=mode, model_config_override=model_config_override)
    
    # Step 2: Make Predictions (delegate to prediction workflow)
    print("\n🔮 [STEP 2] Making Predictions...")
    print("=" * 60)
    
    # Convert model_name to model_specs format for prediction workflow
    # model_specs: dict mapping ont_code -> (model_type, version)
    model_specs = create_model_specs_from_name(model_name)
    
    # Run prediction workflow (loads models from disk and generates submission)
    final_submission_path = run_predict_from_saved(
        model_specs=model_specs,
        output_name=output_name,
        models_source='working'  # Use working directory (where we just saved models)
    )
    
    total_time = time.time() - start_time
    print(f"\n✅ Full Pipeline Complete!")
    print(f"⏱️  Total time: {total_time:.1f}s")
    print(f"📄 Submission file: {final_submission_path}")
    
    return str(final_submission_path)
