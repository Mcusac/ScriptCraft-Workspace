"""
Model persistence utilities for CAFA 6 protein function prediction.
Handles saving, loading, and metadata tracking for trained models.
"""

import pickle
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List, Union
import numpy as np

# Import environment-aware paths from config
try:
    from config import MODELS_DIR, MODELS_INPUT_DIR
    from config.training import (
        MODEL_FILE_EXTENSION_PKL,
        MODEL_FILE_EXTENSION_PTH,
        VALID_ONTOLOGY_CODES
    )
except ImportError:
    MODELS_DIR = None
    MODELS_INPUT_DIR = None
    MODEL_FILE_EXTENSION_PKL = '.pkl'
    MODEL_FILE_EXTENSION_PTH = '.pth'
    VALID_ONTOLOGY_CODES = ['F', 'P', 'C']

# Try to import torch for PyTorch model support
try:
    import torch
    TORCH_AVAILABLE = True
except Exception as e:
    TORCH_AVAILABLE = False



def save_model(model: Any, mlb: Any, ont_code: str, model_type: str, version, 
               metrics: Optional[Dict[str, Any]] = None, hyperparams: Optional[Dict[str, Any]] = None, 
               output_dir: Optional[Path] = None) -> str:
    """
    Save trained model with metadata.
    
    Args:
        model: Trained model object
        mlb: MultiLabelBinarizer object
        ont_code: Ontology code ('F', 'P', 'C')
        model_type: Model type short name (e.g., 'lr', 'xgb', 'nn')
        version: Version number (e.g., "1.0", "1.1")
        metrics: Optional validation metrics dict
        hyperparams: Optional hyperparameters dict
        output_dir: Output directory (defaults to kaggle/working/models)
        
    Returns:
        str: Path to saved model file
        
    Raises:
        ValueError: If required parameters are invalid
        IOError: If file cannot be written
    """
    # Validate inputs
    if not model:
        raise ValueError("Model cannot be None")
    if not mlb:
        raise ValueError("MultiLabelBinarizer cannot be None")
    if ont_code not in VALID_ONTOLOGY_CODES:
        raise ValueError(f"Invalid ontology code: {ont_code}")
    if not model_type or not isinstance(model_type, str):
        raise ValueError(f"Invalid model type: {model_type}")
    # Allow both int and string versions (e.g., "1.1")
    if not (isinstance(version, (int, str)) and (isinstance(version, int) and version >= 1 or isinstance(version, str) and version.replace('.', '').isdigit())):
        raise ValueError(f"Invalid version: {version}")
    
    if output_dir is None:
        # Use environment-aware models directory from config
        if MODELS_DIR:
            output_dir = MODELS_DIR
        else:
            project_root = Path(__file__).parent.parent.parent
            output_dir = project_root / 'data' / 'models'
    
    # Create version folder structure: models/{type}/{version}/
    type_dir = output_dir / model_type
    version_dir = type_dir / f"{version}"
    
    try:
        version_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise IOError(f"Cannot create version directory {version_dir}: {e}")
    
    # Create filename: {model_type}_{version}_{ont_code}.pkl
    filename = f"{model_type}_{version}_{ont_code}{MODEL_FILE_EXTENSION_PKL}"
    model_path = version_dir / filename
    
    # Prepare metadata
    metadata = {
        'model_type': model_type,
        'version': version,
        'ont_code': ont_code,
        'timestamp': datetime.now().isoformat(),
        'hyperparams': hyperparams or {},
        'metrics': metrics or {},
        'n_features': getattr(model, 'n_features_in_', None),
        'n_classes': len(mlb.classes_) if mlb else None
    }
    
    try:
        # Save model and metadata
        model_data = {
            'model': model,
            'mlb': mlb,
            'metadata': metadata
        }
        
        with open(model_path, 'wb') as f:
            pickle.dump(model_data, f)
        
        # Save metadata as separate JSON for easy inspection
        metadata_path = version_dir / f"{model_type}_{version}_{ont_code}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"   [OK] Saved {model_type} {version} model for {ont_code} to {model_path}")
        return str(model_path)
        
    except Exception as e:
        raise IOError(f"Failed to save model to {model_path}: {e}")


def load_model(ont_code, model_type, version='latest', models_dir=None, models_source='both'):
    """
    Load saved model and metadata using clean naming format.
    
    Args:
        ont_code: Ontology code ('F', 'P', 'C')
        model_type: Model type short name (e.g., 'lr', 'xgb', 'nn')
        version: Version number or 'latest'
        models_dir: Models directory (if specified, only checks this directory, overrides models_source)
        models_source: Where to load from - 'input' (MODELS_INPUT_DIR only), 
                      'working' (MODELS_DIR only), or 'both' (check both, MODELS_DIR first)
        
    Returns:
        tuple: (model, mlb, metadata)
        
    Raises:
        FileNotFoundError: If model file not found in specified location(s)
    """
    # Determine search directories: MODELS_DIR first, then MODELS_INPUT_DIR as fallback
    search_dirs = []
    
    if models_dir is not None:
        # Explicit directory provided - ensure absolute path (overrides models_source)
        models_dir_path = Path(models_dir)
        if not models_dir_path.is_absolute():
            models_dir_path = models_dir_path.resolve()
        else:
            models_dir_path = models_dir_path.resolve()
        search_dirs.append(models_dir_path)
    else:
        # Use models_source to determine which directories to check
        if models_source == 'working' or models_source == 'both':
            if MODELS_DIR:
                models_dir_path = Path(MODELS_DIR) if not isinstance(MODELS_DIR, Path) else MODELS_DIR
                if not models_dir_path.is_absolute():
                    models_dir_path = models_dir_path.resolve()
                else:
                    models_dir_path = models_dir_path.resolve()
                search_dirs.append(models_dir_path)
        
        if models_source == 'input' or models_source == 'both':
            if MODELS_INPUT_DIR:
                models_input_dir_path = Path(MODELS_INPUT_DIR) if not isinstance(MODELS_INPUT_DIR, Path) else MODELS_INPUT_DIR
                if not models_input_dir_path.is_absolute():
                    models_input_dir_path = models_input_dir_path.resolve()
                else:
                    models_input_dir_path = models_input_dir_path.resolve()
                search_dirs.append(models_input_dir_path)
        
        # Error if no directories found (no silent fallbacks)
        if not search_dirs:
            source_desc = f"models_source='{models_source}'"
            if models_source == 'working':
                raise ValueError(f"No models directory found. MODELS_DIR is not set. ({source_desc})")
            elif models_source == 'input':
                raise ValueError(f"No models input directory found. MODELS_INPUT_DIR is not set. ({source_desc})")
            else:
                raise ValueError(f"No models directories found. MODELS_DIR and MODELS_INPUT_DIR are not set. ({source_desc})")
    
    if version == 'latest':
        # Find the latest version across all search directories
        all_model_files = []
        
        for models_dir_path in search_dirs:
            type_dir = models_dir_path / model_type
            if type_dir.exists():
                for version_dir in type_dir.iterdir():
                    if version_dir.is_dir():
                        # NN models use .pth, others use .pkl
                        file_ext = MODEL_FILE_EXTENSION_PTH if model_type == 'nn' else MODEL_FILE_EXTENSION_PKL
                        pattern = f"{model_type}_*_{ont_code}{file_ext}"
                        all_model_files.extend(list(version_dir.glob(pattern)))
        
        if not all_model_files:
            dirs_str = ', '.join(str(d) for d in search_dirs)
            raise FileNotFoundError(f"No {model_type} models found for {ont_code} in {dirs_str}")
        
        # Extract version numbers and find latest
        versions = []
        for f in all_model_files:
            try:
                # Extract version from filename like "lr_1.1_F.pkl"
                parts = f.stem.split('_')
                if len(parts) >= 3:
                    v_str = parts[1]
                    # Convert to comparable format (e.g., "1.1" -> 1.1)
                    if '.' in v_str:
                        v_num = float(v_str)
                    else:
                        v_num = int(v_str)
                    versions.append((v_num, f))
            except (ValueError, IndexError):
                continue
        
        if not versions:
            dirs_str = ', '.join(str(d) for d in search_dirs)
            raise FileNotFoundError(f"No valid {model_type} models found for {ont_code} in {dirs_str}")
        
        # Get latest version
        latest_version, model_path = max(versions, key=lambda x: x[0])
        print(f"   [OK] Loading latest {model_type} {latest_version} model for {ont_code} from {model_path.parent.parent.parent.name}")
    else:
        # Load specific version: check both locations
        # NN models use .pth, others use .pkl
        file_ext = MODEL_FILE_EXTENSION_PTH if model_type == 'nn' else MODEL_FILE_EXTENSION_PKL
        filename = f"{model_type}_{version}_{ont_code}{file_ext}"
        model_path = None
        checked_paths = []
        load_errors = []
        
        # Try MODELS_DIR first, then MODELS_INPUT_DIR
        # If loading from one location fails, try the next
        for models_dir_path in search_dirs:
            # Ensure absolute path
            models_dir_path = models_dir_path.resolve() if isinstance(models_dir_path, Path) else Path(models_dir_path).resolve()
            
            # Check if base directory exists
            if not models_dir_path.exists():
                checked_paths.append(f"[DIR NOT FOUND] {models_dir_path}")
                continue
            
            # First, check version folder structure: models/{type}/{version}/{filename}
            version_path = models_dir_path / model_type / f"{version}" / filename
            checked_paths.append(str(version_path))
            if version_path.exists():
                # Try to load from this location
                try:
                    # For NN models, do a quick validation that the file can be loaded
                    if model_type == 'nn':
                        import torch
                        checkpoint = torch.load(version_path, map_location='cpu')
                        model_config = checkpoint.get('model_config', {})
                        # Check if required config values are present
                        if not model_config.get('input_dim') or not model_config.get('output_dim'):
                            load_errors.append(f"{version_path}: Missing required model_config (input_dim or output_dim is None)")
                            continue
                    
                    model_path = version_path
                    break
                except Exception as e:
                    # Loading failed from this location, try next
                    load_errors.append(f"{version_path}: {str(e)}")
                    continue
            
            # Fallback: Check flat directory structure (files directly in directory)
            # This handles cases like /kaggle/input/cafa6-models/pytorch/neural-network/4/nn_3.1_P.pth
            flat_path = models_dir_path / filename
            checked_paths.append(str(flat_path))
            if flat_path.exists():
                # Try to load from flat structure
                try:
                    # For NN models, do a quick validation that the file can be loaded
                    if model_type == 'nn':
                        import torch
                        checkpoint = torch.load(flat_path, map_location='cpu')
                        model_config = checkpoint.get('model_config', {})
                        # Check if required config values are present
                        if not model_config.get('input_dim') or not model_config.get('output_dim'):
                            load_errors.append(f"{flat_path}: Missing required model_config (input_dim or output_dim is None)")
                            continue
                    
                    model_path = flat_path
                    break
                except Exception as e:
                    # Loading failed from this location, try next
                    load_errors.append(f"{flat_path}: {str(e)}")
                    continue
        
        if model_path is None:
            paths_str = '\n    '.join(checked_paths)
            dirs_str = ', '.join(str(d) for d in search_dirs)
            error_msg = f"Model not found or failed to load: {filename}\n"
            error_msg += f"Searched in directories: {dirs_str}\n"
            error_msg += f"Checked paths:\n    {paths_str}"
            if load_errors:
                error_msg += f"\nLoad errors:\n    " + "\n    ".join(load_errors)
            raise FileNotFoundError(error_msg)
        
        print(f"   [OK] Loading {model_type} {version} model for {ont_code} from {model_path.parent.parent.parent.name if 'models' in str(model_path.parent) else model_path.parent.name}")
    
    # Load model data
    if model_type == 'nn':
        # For NN models, load PyTorch model and MLB separately
        from models.nn import MLPModel
        import torch
        
        # Load MLB from same directory as model file
        # Supports both nested (models/{type}/{version}/) and flat directory structures
        mlb_path = model_path.parent / f"{model_type}_{version}_{ont_code}_mlb{MODEL_FILE_EXTENSION_PKL}"
        
        if not mlb_path.exists():
            # If not found, try alternative naming (without version in filename)
            alt_mlb_path = model_path.parent / f"{model_type}_{ont_code}_mlb{MODEL_FILE_EXTENSION_PKL}"
            if alt_mlb_path.exists():
                mlb_path = alt_mlb_path
            else:
                raise FileNotFoundError(
                    f"MultiLabelBinarizer file not found for {ont_code}. "
                    f"Checked: {mlb_path} and {alt_mlb_path}"
                )
        
        import pickle
        with open(mlb_path, 'rb') as f:
            mlb = pickle.load(f)
        
        # Load PyTorch model
        from utils.gpu_utils import get_device
        device_obj = get_device()
        device = 'cuda' if str(device_obj) == 'cuda' else 'cpu'  # Convert torch.device to string
        model, metadata = load_pytorch_model(model_path, model_class=MLPModel, device=device)
        
        return model, mlb, metadata
    else:
        # For sklearn models, load from pickle
        with open(model_path, 'rb') as f:
            model_data = pickle.load(f)
        
        # Load MLB from saved model data
        if 'mlb' not in model_data:
            raise ValueError(
                "MultiLabelBinarizer ('mlb') not found in saved model data. "
                "Model file may be corrupted or in unsupported format."
            )
        mlb = model_data['mlb']
        
        return model_data['model'], mlb, model_data['metadata']


def list_saved_models(ont_code=None, models_dir=None):
    """
    List all saved models with metadata.
    Searches both MODELS_DIR (working) and MODELS_INPUT_DIR (dataset).
    Prefers working directory models when duplicates exist.
    
    Args:
        ont_code: Filter by ontology code (optional)
        models_dir: Models directory (defaults to searching both MODELS_DIR and MODELS_INPUT_DIR)
        
    Returns:
        list: List of model info dictionaries
    """
    # Determine search directories
    search_dirs = []
    
    if models_dir is not None:
        # Explicit directory provided
        search_dirs = [Path(models_dir)]
    else:
        # Check MODELS_DIR first (working directory - prefer these when duplicates exist)
        if MODELS_DIR:
            search_dirs.append(Path(MODELS_DIR))
        # Then check MODELS_INPUT_DIR (dataset)
        if MODELS_INPUT_DIR:
            search_dirs.append(Path(MODELS_INPUT_DIR))
        
        # Fallback for local dev
        if not search_dirs:
            project_root = Path(__file__).parent.parent.parent
            search_dirs.append(project_root / 'data' / 'models')
    
    model_dict = {}  # Use dict to deduplicate: key = (type, version, ont_code)
    model_list = []
    
    # Search all directories (in order: MODELS_DIR first, then MODELS_INPUT_DIR)
    for models_dir_path in search_dirs:
        if not models_dir_path.exists():
            continue
            
        # Search version subdirectories: models/{type}/{version}/*.pkl
        for type_dir in models_dir_path.iterdir():
            if not type_dir.is_dir():
                continue
            
            for version_dir in type_dir.iterdir():
                if not version_dir.is_dir():
                    continue
                
                for model_file in version_dir.glob("*_*_*.pkl"):
                    try:
                        parts = model_file.stem.split('_')
                        if len(parts) >= 3:
                            m_type = parts[0]
                            v_str = parts[1]
                            m_ont = parts[2]
                            
                            if ont_code and m_ont != ont_code:
                                continue
                            
                            # Create deduplication key
                            key = (m_type, v_str, m_ont)
                            
                            # Only add if not already found (MODELS_DIR takes precedence)
                            if key not in model_dict:
                                # Load metadata if available
                                metadata_file = model_file.with_stem(f"{m_type}_{v_str}_{m_ont}_metadata")
                                metadata_path = metadata_file.with_suffix('.json')
                                
                                metadata = None
                                if metadata_path.exists():
                                    with open(metadata_path, 'r') as f:
                                        metadata = json.load(f)
                                
                                model_info = {
                                    'model_type': m_type,
                                    'version': v_str,
                                    'ont_code': m_ont,
                                    'path': str(model_file),
                                    'metadata': metadata
                                }
                                model_dict[key] = model_info
                                model_list.append(model_info)
                    except (ValueError, IndexError):
                        continue
    
    return sorted(model_list, key=lambda x: (x['model_type'], float(x['version'].replace('.', '')), x['ont_code']))


def check_model_exists(ont_code: str, model_type: str, version: Union[int, str], 
                      models_dir: Optional[Path] = None) -> bool:
    """
    Check if a model file exists.
    Searches MODELS_DIR (working) first, then MODELS_INPUT_DIR (dataset).
    
    Args:
        ont_code: Ontology code ('F', 'P', 'C')
        model_type: Model type (e.g., 'lr', 'xgb', 'nn')
        version: Version number or 'latest'
        models_dir: Models directory (defaults to checking both MODELS_DIR and MODELS_INPUT_DIR)
        
    Returns:
        bool: True if model exists, False otherwise
    """
    # Determine search directories
    search_dirs = []
    
    if models_dir is not None:
        # Explicit directory provided
        search_dirs = [Path(models_dir)]
    else:
        # Check MODELS_DIR first, then MODELS_INPUT_DIR
        if MODELS_DIR:
            search_dirs.append(Path(MODELS_DIR))
        if MODELS_INPUT_DIR:
            search_dirs.append(Path(MODELS_INPUT_DIR))
        
        # Fallback for local dev
        if not search_dirs:
            project_root = Path(__file__).parent.parent.parent
            search_dirs.append(project_root / 'data' / 'models')
    
    # Check if any directory exists
    if not any(d.exists() for d in search_dirs):
        return False
    
    # Determine file extension based on model type
    file_ext = MODEL_FILE_EXTENSION_PTH if model_type == 'nn' else MODEL_FILE_EXTENSION_PKL
    
    if version == 'latest':
        # Check if any version exists across all search directories
        model_files = []
        
        for models_dir_path in search_dirs:
            if not models_dir_path.exists():
                continue
                
            type_dir = models_dir_path / model_type
            
            # Search version subdirectories
            if type_dir.exists():
                for version_dir in type_dir.iterdir():
                    if version_dir.is_dir():
                        pattern = f"{model_type}_*_{ont_code}{file_ext}"
                        model_files.extend(list(version_dir.glob(pattern)))
        
        return len(model_files) > 0
    else:
        # Check for specific version - try all locations
        filename = f"{model_type}_{version}_{ont_code}{file_ext}"
        
        for models_dir_path in search_dirs:
            if not models_dir_path.exists():
                continue
                
            type_dir = models_dir_path / model_type
            version_path = type_dir / f"{version}" / filename
            
            if version_path.exists():
                return True
        
        return False


def get_model_summary(models_dir=None):
    """
    Get a summary of all saved models.
    
    Args:
        models_dir: Models directory (defaults to kaggle/working/models)
        
    Returns:
        str: Formatted summary string
    """
    if models_dir is None and MODELS_DIR:
        models_dir = MODELS_DIR
    models = list_saved_models(models_dir=models_dir)
    
    if not models:
        return "No saved models found."
    
    # Group by model type and ontology
    summary = {}
    for model in models:
        key = f"{model['model_type']} v{model['version']}"
        if key not in summary:
            summary[key] = {}
        summary[key][model['ont_code']] = model
    
    # Format summary
    lines = ["Saved Models Summary:", "=" * 50]
    
    for model_key, ontologies in summary.items():
        lines.append(f"\n{model_key}:")
        for ont_code in ['F', 'P', 'C']:
            if ont_code in ontologies:
                model = ontologies[ont_code]
                lines.append(f"  {ont_code}: {model['timestamp']} "
                           f"(n_features={model['n_features']}, "
                           f"n_classes={model['n_classes']})")
            else:
                lines.append(f"  {ont_code}: Not available")
    
    return "\n".join(lines)


def save_pytorch_model(model: Any, model_path: Union[str, Path], 
                      metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Save PyTorch model with optional metadata.
    
    Args:
        model: PyTorch model to save
        model_path: Path to save the model (.pth file)
        metadata: Optional metadata dictionary
        
    Returns:
        str: Path to saved model file
        
    Raises:
        ImportError: If PyTorch is not available
        IOError: If model cannot be saved
    """
    if not TORCH_AVAILABLE:
        raise ImportError("PyTorch is required for saving PyTorch models")
    
    model_path = Path(model_path)
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    try:
        # Unwrap DataParallel if present (save underlying model)
        if hasattr(model, 'module'):
            actual_model = model.module
            print(f"   [INFO] Unwrapping DataParallel before saving")
        else:
            actual_model = model
        
        # Save model state dict
        torch.save({
            'model_state_dict': actual_model.state_dict(),
            'model_class': actual_model.__class__.__name__,
            'model_config': {
                'input_dim': getattr(actual_model, 'input_dim', None),
                'output_dim': getattr(actual_model, 'output_dim', None),
                'hidden_dims': getattr(actual_model, 'hidden_dims', None),
                'dropout_rate': getattr(actual_model, 'dropout_rate', None)
            },
            'metadata': metadata or {}
        }, model_path)
        
        print(f"   ✓ Saved PyTorch model to {model_path}")
        return str(model_path)
        
    except Exception as e:
        raise IOError(f"Failed to save PyTorch model to {model_path}: {e}")


def load_pytorch_model(model_path: Union[str, Path], model_class=None, 
                      device: str = 'cpu') -> Tuple[Any, Dict[str, Any]]:
    """
    Load PyTorch model from file.
    
    Args:
        model_path: Path to saved model (.pth file)
        model_class: Model class to instantiate (if None, will try to infer)
        device: Device to load model on
        
    Returns:
        tuple: (loaded_model, metadata)
        
    Raises:
        ImportError: If PyTorch is not available
        FileNotFoundError: If model file doesn't exist
        IOError: If model cannot be loaded
    """
    if not TORCH_AVAILABLE:
        raise ImportError("PyTorch is required for loading PyTorch models")
    
    model_path = Path(model_path)
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file {model_path} not found")
    
    try:
        # Load model data
        checkpoint = torch.load(model_path, map_location=device)
        
        # Extract model configuration
        model_config = checkpoint.get('model_config', {})
        metadata = checkpoint.get('metadata', {})
        
        # Validate required config values
        if model_class is not None:
            required_keys = ['input_dim', 'output_dim']
            missing_keys = [key for key in required_keys if model_config.get(key) is None]
            if missing_keys:
                raise ValueError(
                    f"Model config missing required keys: {missing_keys}. "
                    f"Found keys: {list(model_config.keys())}. "
                    f"This may indicate a corrupted or incomplete model file."
                )
        
        # Create model instance if model_class provided
        if model_class is not None:
            # Filter out None values to avoid issues with optional parameters
            filtered_config = {k: v for k, v in model_config.items() if v is not None}
            model = model_class(**filtered_config)
            model.load_state_dict(checkpoint['model_state_dict'])
            model.to(device)
            model.eval()
        else:
            # Return state dict and config for manual model creation
            model = {
                'state_dict': checkpoint['model_state_dict'],
                'config': model_config,
                'class_name': checkpoint.get('model_class', 'Unknown')
            }
        
        print(f"   ✓ Loaded PyTorch model from {model_path}")
        return model, metadata
        
    except Exception as e:
        raise IOError(f"Failed to load PyTorch model from {model_path}: {e}")


def save_model_universal(model: Any, model_path: Union[str, Path], 
              metadata: Optional[Dict[str, Any]] = None) -> str:
    """
    Universal model saving function that handles both sklearn and PyTorch models.
    
    Args:
        model: Model to save (sklearn or PyTorch)
        model_path: Path to save the model
        metadata: Optional metadata dictionary
        
    Returns:
        str: Path to saved model file
    """
    model_path = Path(model_path)
    
    # Check if it's a PyTorch model
    if TORCH_AVAILABLE and hasattr(model, 'state_dict'):
        return save_pytorch_model(model, model_path, metadata)
    else:
        # Use pickle for sklearn models
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(model_path, 'wb') as f:
                pickle.dump({
                    'model': model,
                    'metadata': metadata or {}
                }, f)
            
            print(f"   ✓ Saved model to {model_path}")
            return str(model_path)
            
        except Exception as e:
            raise IOError(f"Failed to save model to {model_path}: {e}")


def load_model_universal(model_path: Union[str, Path], model_class=None, 
              device: str = 'cpu') -> Tuple[Any, Dict[str, Any]]:
    """
    Universal model loading function that handles both sklearn and PyTorch models.
    
    Args:
        model_path: Path to saved model
        model_class: Model class for PyTorch models (optional)
        device: Device for PyTorch models
        
    Returns:
        tuple: (loaded_model, metadata)
    """
    model_path = Path(model_path)
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file {model_path} not found")
    
    # Check file extension to determine type
    if model_path.suffix == MODEL_FILE_EXTENSION_PTH:
        if not TORCH_AVAILABLE:
            raise ImportError("PyTorch is required for loading .pth files")
        return load_pytorch_model(model_path, model_class, device)
    else:
        # Use pickle for sklearn models
        try:
            with open(model_path, 'rb') as f:
                data = pickle.load(f)
            
            if isinstance(data, dict) and 'model' in data:
                return data['model'], data.get('metadata', {})
            else:
                # Legacy format - just the model
                return data, {}
                
        except Exception as e:
            raise IOError(f"Failed to load model from {model_path}: {e}")
