"""
Path configuration and environment detection for CAFA 6 protein function prediction.
Unified path resolution for both dev and Kaggle environments.
"""

from pathlib import Path
import os

# Path Configuration - Unified for Dev and Kaggle
# Check if we're in Kaggle environment
if os.path.exists('/kaggle/input'):
    # Kaggle environment
    DATA_INPUT_DIR = Path('/kaggle/input/cafa-6-protein-function-prediction')
    DATA_OUTPUT_DIR = Path('/kaggle/working')
    PROJECT_ROOT = Path('/kaggle')
else:
    # Local development environment - detect project root correctly
    current_dir = Path.cwd()
    
    # If we're in kaggle/working, go up to project root
    if current_dir.name == 'working' and (current_dir.parent / 'input').exists():
        PROJECT_ROOT = current_dir.parent.parent
    else:
        PROJECT_ROOT = current_dir
    
    DATA_INPUT_DIR = PROJECT_ROOT / 'kaggle' / 'input' / 'cafa-6-protein-function-prediction'
    DATA_OUTPUT_DIR = PROJECT_ROOT / 'kaggle' / 'working'

MODELS_DIR = DATA_OUTPUT_DIR / 'models'

# Models dataset path (read-only, for uploaded model datasets)
# Check if Kaggle models dataset exists
if os.path.exists('/kaggle/input'):
    # Kaggle environment - find models dataset (supports multiple versions: /1/, /2/, /3/, etc.)
    base_path = Path('/kaggle/input/cafa6-models/other/default')
    MODELS_INPUT_DIR = None
    
    if base_path.exists():
        # Find all version directories (1, 2, 3, etc.) and use the highest one
        version_dirs = []
        for item in base_path.iterdir():
            if item.is_dir() and item.name.isdigit():
                models_path = item / 'models'
                if models_path.exists():
                    version_dirs.append((int(item.name), models_path))
        
        if version_dirs:
            # Use the highest version number
            _, MODELS_INPUT_DIR = max(version_dirs, key=lambda x: x[0])
            print(f"   [INFO] Using models dataset version: {max(v for v, _ in version_dirs)}")
    
    # Also check for alternative pytorch/neural-network structure (flat directory)
    # Path: /kaggle/input/cafa6-models/pytorch/neural-network/{version}/
    pytorch_base = Path('/kaggle/input/cafa6-models/pytorch/neural-network')
    if pytorch_base.exists() and MODELS_INPUT_DIR is None:
        # Find all version directories and use the highest one
        pytorch_version_dirs = []
        for item in pytorch_base.iterdir():
            if item.is_dir() and item.name.isdigit():
                if item.exists():
                    pytorch_version_dirs.append((int(item.name), item))
        
        if pytorch_version_dirs:
            # Use the highest version number
            _, MODELS_INPUT_DIR = max(pytorch_version_dirs, key=lambda x: x[0])
            print(f"   [INFO] Using pytorch models dataset version: {max(v for v, _ in pytorch_version_dirs)}")
else:
    # Local development environment - mirror Kaggle structure, find latest version
    base_path = PROJECT_ROOT / 'kaggle' / 'input' / 'cafa6-models' / 'other' / 'default'
    MODELS_INPUT_DIR = None
    
    if base_path.exists():
        version_dirs = []
        for item in base_path.iterdir():
            if item.is_dir() and item.name.isdigit():
                models_path = item / 'models'
                if models_path.exists():
                    version_dirs.append((int(item.name), models_path))
        
        if version_dirs:
            _, MODELS_INPUT_DIR = max(version_dirs, key=lambda x: x[0])
            print(f"   [INFO] Using models dataset version: {max(v for v, _ in version_dirs)}")
    
    # Also check for alternative pytorch/neural-network structure (flat directory)
    pytorch_base = PROJECT_ROOT / 'kaggle' / 'input' / 'cafa6-models' / 'pytorch' / 'neural-network'
    if pytorch_base.exists() and MODELS_INPUT_DIR is None:
        pytorch_version_dirs = []
        for item in pytorch_base.iterdir():
            if item.is_dir() and item.name.isdigit():
                if item.exists():
                    pytorch_version_dirs.append((int(item.name), item))
        
        if pytorch_version_dirs:
            _, MODELS_INPUT_DIR = max(pytorch_version_dirs, key=lambda x: x[0])
            print(f"   [INFO] Using pytorch models dataset version: {max(v for v, _ in pytorch_version_dirs)}")

# New consolidated CAFA6 embeddings dataset
if os.path.exists('/kaggle/input'):
    CAFA6_EMBEDDINGS_DIR = Path('/kaggle/input/cafa-6-embeddings')
else:
    CAFA6_EMBEDDINGS_DIR = PROJECT_ROOT / 'kaggle' / 'input' / 'cafa-6-embeddings'

# Embedding dataset paths (new consolidated structure + legacy fallback)
EMBEDDINGS_DIR = PROJECT_ROOT / 'kaggle' / 'input'
EMBEDDING_PATHS = {
    # ESM2 variants (new from cafa-6-embeddings)
    'esm2_15b': CAFA6_EMBEDDINGS_DIR / 'esm2_15B',
    'esm2_3b': CAFA6_EMBEDDINGS_DIR / 'esm2_3B',
    'esm2_650m': CAFA6_EMBEDDINGS_DIR / 'esm2_650M',
    'esm1b_650m': CAFA6_EMBEDDINGS_DIR / 'esm1b_650M',
    
    # Ankh variants (new)
    'ankh_large': CAFA6_EMBEDDINGS_DIR / 'ankh_large',
    'ankh3_large': CAFA6_EMBEDDINGS_DIR / 'ankh3_large',
    
    # Current embeddings (from consolidated dataset)
    'protbert': CAFA6_EMBEDDINGS_DIR / 'protBERT',
    'prot_t5_xl': CAFA6_EMBEDDINGS_DIR / 'protT5_xl',
    
    # Legacy paths (fallback for old datasets)
    'esm2': EMBEDDINGS_DIR / 'CAFA 5 EMS-2 Embeddings Numpy',
    't5': EMBEDDINGS_DIR / 'CAFA5 supplementary calcs for ML',
    'train_targets': EMBEDDINGS_DIR / 'train_targets_top500'
}

# New feature types from cafa-6-embeddings
FEATURE_PATHS = {
    'taxonomy': CAFA6_EMBEDDINGS_DIR / 'taxonomy',
    'taxonomy_highlevel': CAFA6_EMBEDDINGS_DIR / 'taxonomy_highlevel',
    'taxonomy_top500': CAFA6_EMBEDDINGS_DIR / 'taxonomy_top500',
    'ppi': CAFA6_EMBEDDINGS_DIR / 'ppi',
    'top_terms_by_aspect': CAFA6_EMBEDDINGS_DIR / 'top_terms_by_aspect'
}

# GOA annotations for post-processing
if os.path.exists('/kaggle/input'):
    GOA_ANNOTATIONS_PATH = Path('/kaggle/input/protein-go-annotations')
else:
    GOA_ANNOTATIONS_PATH = PROJECT_ROOT / 'kaggle' / 'input' / 'protein-go-annotations'

# For Kaggle environment, override legacy paths with Kaggle paths
if os.path.exists('/kaggle/input'):
    EMBEDDING_PATHS.update({
        'esm2': Path('/kaggle/input/cafa-5-ems-2-embeddings-numpy'),
        't5': Path('/kaggle/input/cafa5-supp-pre-calcs-for-ml'),
        'train_targets': Path('/kaggle/input/train-targets-top500')
    })

# Environment Detection
KAGGLE_ENV = os.path.exists('/kaggle/input')
