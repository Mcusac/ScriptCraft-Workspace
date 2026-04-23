# train_export.py
# Train/export result handlers
#
# Handles results from training and export pipelines:
# - Export verification for end-to-end models
# - Export verification for regression models

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def verify_export_output(model_type: str = 'end_to_end') -> bool:
    """
    Verify that export was successful by checking for exported model files.
    
    Checks for exported model files in /kaggle/working/best_model/ and prints
    appropriate success/warning messages.
    
    Args:
        model_type: Model type ('end_to_end' or 'regression')
        
    Returns:
        True if export verified successfully, False otherwise
    """
    export_dir = Path('/kaggle/working/best_model')
    
    if not export_dir.exists():
        print("\n⚠️  Note: Export directory not found")
        print(f"   Expected location: {export_dir}")
        print("   Check training logs for export status")
        return False
    
    if model_type == 'end_to_end':
        # Check for end-to-end model (best_model.pth)
        model_path = export_dir / 'best_model.pth'
        if model_path.exists():
            print("\n✅ Export successful!")
            print(f"   Model: {model_path}")
            print(f"   Metadata: {export_dir / 'model_metadata.json'}")
            print(f"\n📥 Next: Download /kaggle/working/best_model/ folder")
            return True
        else:
            print("\n⚠️  Note: Model may be in grid search output directory")
            print("   Check outputs/hyperparameter_grid_search_*/ for exported models")
            return False
    
    elif model_type == 'regression':
        # Check for regression model (regression_model.pkl) or end-to-end model as fallback
        regression_model_path = export_dir / 'regression_model.pkl'
        end_to_end_model_path = export_dir / 'best_model.pth'
        
        if regression_model_path.exists():
            print("\n✅ Export successful!")
            print(f"   Regression model: {regression_model_path}")
            print(f"   Metadata: {export_dir / 'model_metadata.json'}")
            print(f"\n📥 Next: Download /kaggle/working/best_model/ folder")
            return True
        elif end_to_end_model_path.exists():
            print("\n✅ Export successful!")
            print(f"   Model: {end_to_end_model_path}")
            print(f"   Metadata: {export_dir / 'model_metadata.json'}")
            print(f"\n📥 Next: Download /kaggle/working/best_model/ folder")
            return True
        else:
            print("\n⚠️  Note: Expected model files not found in export directory")
            print(f"   Check {export_dir} for exported files")
            return False
    
    else:
        # Unknown model type - just check for any model file
        if (export_dir / 'best_model.pth').exists() or (export_dir / 'regression_model.pkl').exists():
            print("\n✅ Export successful!")
            print(f"   Model files found in: {export_dir}")
            print(f"\n📥 Next: Download /kaggle/working/best_model/ folder")
            return True
        else:
            print("\n⚠️  Note: Expected model files not found in export directory")
            print(f"   Check {export_dir} for exported files")
            return False
