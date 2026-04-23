"""
Embedding-based feature extraction for protein sequences.
Supports ProtBERT, ESM2, and T5 protein embeddings.
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Union, Tuple
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')


def load_combined_embeddings(embedding_types: List[str],
                            datatype: str = 'train',
                            use_memmap: bool = None,
                            combined_embeddings_dir: Optional[Path] = None) -> Optional[Tuple[np.ndarray, np.ndarray]]:
    """
    Load preprocessed combined embeddings if available.
    
    Args:
        embedding_types: List of embedding types (e.g., ['protbert', 'esm2'])
        datatype: 'train' or 'test'
        use_memmap: If True, load as memmap; if False, load full array; if None, use config default
        combined_embeddings_dir: Directory containing combined embeddings (defaults to DATA_OUTPUT_DIR/combined_embeddings)
        
    Returns:
        (embeddings, ids) if found, None otherwise
    """
    from config.paths import DATA_OUTPUT_DIR
    from config.training import USE_MEMORY_MAPPED_EMBEDDINGS
    
    if combined_embeddings_dir is None:
        combined_embeddings_dir = DATA_OUTPUT_DIR / 'combined_embeddings'
    
    # Create combination name (sorted for consistency)
    combination_name = '_'.join(sorted(embedding_types))
    embeddings_path = combined_embeddings_dir / f'{datatype}_combined_{combination_name}_embeddings.npy'
    ids_path = combined_embeddings_dir / f'{datatype}_combined_{combination_name}_ids.npy'
    
    if not embeddings_path.exists() or not ids_path.exists():
        return None
    
    # Use config default if not specified
    if use_memmap is None:
        use_memmap = USE_MEMORY_MAPPED_EMBEDDINGS
    
    try:
        # Load IDs
        ids = np.load(ids_path)
        
        # Load embeddings
        if use_memmap:
            embeds = np.load(embeddings_path, mmap_mode='r')
            print(f"   Loaded combined embeddings ({combination_name}) {datatype} as memmap: {embeds.shape} (dtype: {embeds.dtype})")
        else:
            embeds = np.load(embeddings_path)
            if embeds.dtype != np.float32:
                embeds = embeds.astype(np.float32)
            print(f"   Loaded combined embeddings ({combination_name}) {datatype}: {embeds.shape} (dtype: {embeds.dtype})")
        
        return embeds, ids
    except Exception as e:
        print(f"   [WARNING] Failed to load combined embeddings: {e}")
        return None


def check_embedding_structure(embedding_type: str, 
                              datatype: str = 'train',
                              base_path: Optional[Path] = None) -> Dict:
    """
    Diagnostic function to check embedding directory structure and identify available files.
    Helps debug file structure mismatches.
    
    Args:
        embedding_type: Embedding type (e.g., 'protbert', 'esm2_15b', etc.)
        datatype: 'train' or 'test'
        base_path: Optional base path override
        
    Returns:
        dict: Diagnostic information including:
            - base_directory_exists: bool
            - base_directory: Path
            - files_in_directory: List[str]
            - expected_paths: Dict with structure types and their paths
            - found_paths: Dict with structure types and whether paths exist
            - suggestions: List[str] with actionable suggestions
    """
    from config.paths import EMBEDDING_PATHS, CAFA6_EMBEDDINGS_DIR
    from config.features import is_valid_embedding_type
    
    result = {
        'embedding_type': embedding_type,
        'datatype': datatype,
        'base_directory': None,
        'base_directory_exists': False,
        'files_in_directory': [],
        'expected_paths': {},
        'found_paths': {},
        'suggestions': []
    }
    
    # Convert legacy 'esm2' to 'esm2_650m' BEFORE validation
    # This ensures we always use the new structure paths
    if embedding_type == 'esm2':
        embedding_type = 'esm2_650m'
    
    # Validate embedding type
    if not is_valid_embedding_type(embedding_type):
        result['suggestions'].append(f"Invalid embedding type: {embedding_type}")
        return result
    
    # Get base path
    if base_path is None:
        if embedding_type not in EMBEDDING_PATHS:
            result['suggestions'].append(f"Embedding type '{embedding_type}' not found in EMBEDDING_PATHS")
            return result
        base_path = EMBEDDING_PATHS[embedding_type]
    
    result['base_directory'] = str(base_path)
    result['base_directory_exists'] = base_path.exists()
    
    # List files in directory
    if base_path.exists():
        try:
            files = [f.name for f in base_path.iterdir() if f.is_file()]
            result['files_in_directory'] = sorted(files)
        except PermissionError:
            result['suggestions'].append(f"Cannot list files in {base_path} (permission denied)")
    
    # Check expected paths for new structure embeddings
    new_structure_embeddings = ['esm2_15b', 'esm2_3b', 'esm2_650m', 'esm1b_650m', 
                                'ankh_large', 'ankh3_large', 'protbert', 'prot_t5_xl']
    
    if embedding_type in new_structure_embeddings:
        # New structure paths
        if datatype == 'train':
            new_ids_path = CAFA6_EMBEDDINGS_DIR / 'train_sequences_ids.npy'
            new_embeddings_path = base_path / 'train.npy'
        else:
            new_ids_path = CAFA6_EMBEDDINGS_DIR / 'testsuperset_ids.npy'
            new_embeddings_path = base_path / 'test.npy'
        
        result['expected_paths']['new_structure'] = {
            'ids': str(new_ids_path),
            'embeddings': str(new_embeddings_path)
        }
        result['found_paths']['new_structure'] = {
            'ids': new_ids_path.exists(),
            'embeddings': new_embeddings_path.exists()
        }
        
        # train_sequences_emb pattern paths (both files in same directory)
        if datatype == 'train':
            sequences_ids_path = base_path / 'train_sequences_ids.npy'
            sequences_embeddings_path = base_path / 'train_sequences_emb.npy'
        else:
            sequences_ids_path = base_path / 'testsuperset_ids.npy'
            sequences_embeddings_path = base_path / 'testsuperset_emb.npy'
        
        result['expected_paths']['train_sequences_emb'] = {
            'ids': str(sequences_ids_path),
            'embeddings': str(sequences_embeddings_path)
        }
        result['found_paths']['train_sequences_emb'] = {
            'ids': sequences_ids_path.exists(),
            'embeddings': sequences_embeddings_path.exists()
        }
        
        # Legacy structure paths
        legacy_ids_path = base_path / f'{datatype}_ids.npy'
        legacy_embeddings_path = base_path / f'{datatype}_embeddings.npy'
        
        result['expected_paths']['legacy'] = {
            'ids': str(legacy_ids_path),
            'embeddings': str(legacy_embeddings_path)
        }
        result['found_paths']['legacy'] = {
            'ids': legacy_ids_path.exists(),
            'embeddings': legacy_embeddings_path.exists()
        }
    else:
        # Legacy structure only
        legacy_ids_path = base_path / f'{datatype}_ids.npy'
        legacy_embeddings_path = base_path / f'{datatype}_embeddings.npy'
        
        result['expected_paths']['legacy'] = {
            'ids': str(legacy_ids_path),
            'embeddings': str(legacy_embeddings_path)
        }
        result['found_paths']['legacy'] = {
            'ids': legacy_ids_path.exists(),
            'embeddings': legacy_embeddings_path.exists()
        }
    
    # Generate suggestions
    if not result['base_directory_exists']:
        result['suggestions'].append(f"Base directory does not exist: {base_path}")
        result['suggestions'].append(f"Check if embedding dataset is properly mounted/available")
    else:
        # Check if any expected files exist
        any_found = False
        for structure_type, found_info in result['found_paths'].items():
            if found_info.get('ids') or found_info.get('embeddings'):
                any_found = True
                break
        
        if not any_found:
            result['suggestions'].append(f"No expected embedding files found in {base_path}")
            if result['files_in_directory']:
                result['suggestions'].append(f"Found {len(result['files_in_directory'])} files, but none match expected names")
                result['suggestions'].append(f"Consider checking file naming conventions")
            else:
                result['suggestions'].append(f"Directory is empty - embedding files may not be available")
        
        # Check for similar file names
        if result['files_in_directory']:
            expected_names = ['train.npy', 'test.npy', f'{datatype}_embeddings.npy', f'{datatype}_ids.npy', 
                            'train_sequences_emb.npy', 'train_sequences_ids.npy', 
                            'testsuperset_emb.npy', 'testsuperset_ids.npy']
            similar_files = [f for f in result['files_in_directory'] 
                           if any(exp in f.lower() for exp in ['train', 'test', 'embed', 'id', 'npy', 'sequences', 'superset'])]
            if similar_files:
                result['suggestions'].append(f"Found similar files: {similar_files[:5]}")
                result['suggestions'].append(f"These might be the embedding files with different naming")
    
    return result


def load_embedding_data(embedding_type: str, 
                       datatype: str = 'train',
                       use_memmap: bool = None,
                       base_path: Optional[Path] = None) -> tuple:
    """
    Load embeddings from numpy files using config paths.
    Supports both full array loading and memory-mapped loading.
    Converts to float32 to save memory (50% reduction vs float64).
    
    Special handling for T5 embeddings which are stored as .rds files (R data format).
    Supports new consolidated embedding structure with shared ID files.
    
    Args:
        embedding_type: Embedding type (e.g., 'protbert', 'esm2', 'esm2_15b', 'ankh_large', etc.)
        datatype: 'train' or 'test'
        use_memmap: If True, load as memmap; if False, load full array; if None, use config default
        base_path: Optional base path override
        
    Returns:
        (embeddings_array_or_memmap, ids_array) - embeddings as np.ndarray or np.memmap, ids as array
    """
    from config.paths import EMBEDDING_PATHS, CAFA6_EMBEDDINGS_DIR
    from config.features import is_valid_embedding_type
    from config.training import USE_MEMORY_MAPPED_EMBEDDINGS
    
    # Convert legacy 'esm2' to 'esm2_650m' BEFORE validation
    # This ensures we always use the new structure paths
    if embedding_type == 'esm2':
        embedding_type = 'esm2_650m'
    
    # Validate embedding type using config helper
    if not is_valid_embedding_type(embedding_type):
        valid_types = ', '.join(['protbert', 'esm2', 't5', 'esm2_15b', 'esm2_3b', 'esm2_650m', 'ankh_large', 'ankh3_large'])
        raise ValueError(f"Unknown embedding_type: {embedding_type}. Choose from: [{valid_types}]")
    
    if base_path is None:
        if embedding_type not in EMBEDDING_PATHS:
            raise ValueError(f"Embedding type '{embedding_type}' not found in EMBEDDING_PATHS")
        base_path = EMBEDDING_PATHS[embedding_type]
    
    # Use config default if not specified
    if use_memmap is None:
        use_memmap = USE_MEMORY_MAPPED_EMBEDDINGS
    
    # Special handling for T5 embeddings (stored as .qs or .rds files)
    if embedding_type in ['t5', 'prot_t5_xl']:
        # Try .qs files first (more reliable, compressed format)
        qs_path = base_path / f'T5_{datatype}_features.qs'
        if qs_path.exists():
            return _load_t5_qs(qs_path, datatype, use_memmap)
        
        # Fallback to .rds files
        rds_path = base_path / f'CAFA5_{datatype}_t5embeds.rds'
        if rds_path.exists():
            return _load_t5_rds(rds_path, datatype, use_memmap)
    
    # Check for new consolidated embedding structure (shared ID files)
    # New structure: train.npy/test.npy + shared train_sequences_ids.npy/testsuperset_ids.npy
    new_structure_embeddings = ['esm2_15b', 'esm2_3b', 'esm2_650m', 'esm1b_650m', 
                                'ankh_large', 'ankh3_large', 'protbert', 'prot_t5_xl']
    
    # Track all paths checked for better error messages
    checked_paths = []
    
    if embedding_type in new_structure_embeddings:
        # New structure: shared ID files at parent directory level
        if datatype == 'train':
            new_ids_path = CAFA6_EMBEDDINGS_DIR / 'train_sequences_ids.npy'
            new_embeddings_path = base_path / 'train.npy'
        else:  # test
            new_ids_path = CAFA6_EMBEDDINGS_DIR / 'testsuperset_ids.npy'
            new_embeddings_path = base_path / 'test.npy'
        
        # Track new structure paths
        checked_paths.append(("new_structure", new_ids_path, new_embeddings_path))
        
        # Check if new structure exists
        if new_embeddings_path.exists() and new_ids_path.exists():
            ids_path = new_ids_path
            embeddings_path = new_embeddings_path
        else:
            # Try train_sequences_emb pattern (both files in same directory)
            if datatype == 'train':
                sequences_ids_path = base_path / 'train_sequences_ids.npy'
                sequences_embeddings_path = base_path / 'train_sequences_emb.npy'
            else:  # test
                sequences_ids_path = base_path / 'testsuperset_ids.npy'
                sequences_embeddings_path = base_path / 'testsuperset_emb.npy'
            
            # Track train_sequences_emb pattern paths
            checked_paths.append(("train_sequences_emb", sequences_ids_path, sequences_embeddings_path))
            
            # Check if train_sequences_emb pattern exists
            if sequences_embeddings_path.exists() and sequences_ids_path.exists():
                ids_path = sequences_ids_path
                embeddings_path = sequences_embeddings_path
            else:
                # Fallback to legacy structure
                legacy_ids_path = base_path / f'{datatype}_ids.npy'
                legacy_embeddings_path = base_path / f'{datatype}_embeddings.npy'
                checked_paths.append(("legacy", legacy_ids_path, legacy_embeddings_path))
                ids_path = legacy_ids_path
                embeddings_path = legacy_embeddings_path
    else:
        # Legacy structure: separate ID files per embedding type
        ids_path = base_path / f'{datatype}_ids.npy'
        embeddings_path = base_path / f'{datatype}_embeddings.npy'
        checked_paths.append(("legacy", ids_path, embeddings_path))
    
    try:
        # Load IDs (small, can load into memory)
        if not ids_path.exists():
            raise FileNotFoundError(f"ID file not found: {ids_path}")
        ids = np.load(ids_path)
        
        # Load embeddings (memmap or full array)
        if not embeddings_path.exists():
            raise FileNotFoundError(f"Embeddings file not found: {embeddings_path}")
        
        if use_memmap:
            # Use memmap for memory efficiency
            embeds = np.load(embeddings_path, mmap_mode='r')
            print(f"   Loaded {embedding_type} {datatype} as memmap: {embeds.shape} (dtype: {embeds.dtype})")
        else:
            # Load full array
            embeds = np.load(embeddings_path)
            # Convert to float32 to save memory (50% reduction)
            if embeds.dtype != np.float32:
                embeds = embeds.astype(np.float32)
            print(f"   Loaded {embedding_type} {datatype}: {embeds.shape} (dtype: {embeds.dtype})")
        
        return embeds, ids
    except FileNotFoundError as e:
        # Build comprehensive error message with all checked paths
        error_msg = f"Could not load {embedding_type} embeddings for {datatype}.\n\n"
        error_msg += "Checked paths:\n"
        
        for structure_type, checked_ids_path, checked_embeddings_path in checked_paths:
            error_msg += f"  [{structure_type}]\n"
            error_msg += f"    IDs: {checked_ids_path} {'✓' if checked_ids_path.exists() else '✗'}\n"
            error_msg += f"    Embeddings: {checked_embeddings_path} {'✓' if checked_embeddings_path.exists() else '✗'}\n"
        
        # Add directory diagnostics
        error_msg += f"\nDirectory diagnostics:\n"
        error_msg += f"  Base directory: {base_path} {'✓ exists' if base_path.exists() else '✗ does not exist'}\n"
        if base_path.exists():
            try:
                files = list(base_path.iterdir())
                if files:
                    error_msg += f"  Files in base directory ({len(files)} found):\n"
                    for f in sorted(files)[:20]:  # Show first 20 files
                        error_msg += f"    - {f.name}\n"
                    if len(files) > 20:
                        error_msg += f"    ... and {len(files) - 20} more files\n"
                else:
                    error_msg += f"  Base directory is empty\n"
            except PermissionError:
                error_msg += f"  Cannot list files in base directory (permission denied)\n"
        
        # Check CAFA6_EMBEDDINGS_DIR if it's different from base_path
        if embedding_type in new_structure_embeddings and CAFA6_EMBEDDINGS_DIR != base_path:
            error_msg += f"  CAFA6 embeddings root: {CAFA6_EMBEDDINGS_DIR} {'✓ exists' if CAFA6_EMBEDDINGS_DIR.exists() else '✗ does not exist'}\n"
            if CAFA6_EMBEDDINGS_DIR.exists():
                try:
                    shared_id_file = CAFA6_EMBEDDINGS_DIR / ('train_sequences_ids.npy' if datatype == 'train' else 'testsuperset_ids.npy')
                    error_msg += f"  Shared ID file: {shared_id_file} {'✓ exists' if shared_id_file.exists() else '✗ does not exist'}\n"
                except:
                    pass
        
        error_msg += f"\nOriginal error: {e}"
        error_msg += f"\n\nTip: Use check_embedding_structure('{embedding_type}', '{datatype}') for detailed diagnostics."
        
        raise FileNotFoundError(error_msg)


def _load_t5_qs(qs_path: Path, datatype: str, use_memmap: bool) -> tuple:
    """
    Load T5 embeddings from .qs file (compressed R data format).
    
    Args:
        qs_path: Path to .qs file
        datatype: 'train' or 'test'
        use_memmap: Whether to use memory mapping (not supported for .qs, will load full array)
        
    Returns:
        (embeddings_array, ids_array)
    """
    print(f"   Loading T5 {datatype} embeddings from .qs file: {qs_path}")
    
    # .qs files require R's qs package - use rpy2 to load via R
    try:
        import rpy2.robjects as ro
        from rpy2.robjects import pandas2ri
        pandas2ri.activate()
        
        # Load .qs file using R's qs package
        ro.r('if (!require("qs", quietly=TRUE)) install.packages("qs", repos="https://cloud.r-project.org")')
        ro.r(f'data <- qs::qread("{qs_path}")')
        r_data = ro.r('data')
        
        # Convert R DataFrame to pandas DataFrame
        data = pandas2ri.rpy2py(r_data)
        print(f"   Loaded using rpy2 + R qs package (converted to pandas DataFrame)")
    except ImportError:
        raise ImportError(
            "rpy2 library required for loading T5 .qs files. "
            "Install with: pip install rpy2\n"
            "Note: R must also be installed on the system."
        )
    except Exception as e:
        raise IOError(
            f"Failed to load .qs file using rpy2: {e}\n"
            f"Make sure R is installed and the 'qs' R package is available.\n"
            f"Alternatively, convert .qs files to .npy format for faster loading."
        )
    
    try:
        # Ensure we have a pandas DataFrame
        if not isinstance(data, pd.DataFrame):
            # Try to convert if it's still an R object
            try:
                data = pandas2ri.rpy2py(data)
            except:
                raise ValueError(
                    f"Unexpected data structure in .qs file. "
                    f"Expected DataFrame. Got: {type(data)}"
                )
        
        # Handle different possible structures:
        # 1. DataFrame with protein IDs as index/row names and embeddings as columns
        # 2. DataFrame with protein IDs in first column and embeddings as other columns
        
        # Debug: Print DataFrame info
        print(f"   DataFrame shape: {data.shape}, columns: {list(data.columns)[:5]}...")
        print(f"   Index type: {type(data.index)}, sample: {data.index[:3].tolist() if len(data.index) > 0 else 'empty'}")
        if len(data.columns) > 0:
            print(f"   First column dtype: {data.iloc[:, 0].dtype}, sample: {data.iloc[:3, 0].tolist()}")
        
        # Check if IDs are in index (row names) - non-numeric index likely contains IDs
        if len(data.index) > 0:
            try:
                # Strategy 1: Check if index contains non-numeric values (likely IDs)
                if not pd.api.types.is_numeric_dtype(data.index):
                    # IDs are in index - use all columns as embeddings
                    ids = data.index.astype(str).tolist()
                    # Ensure all columns are numeric before using
                    numeric_cols = data.select_dtypes(include=[np.number]).columns
                    if len(numeric_cols) == len(data.columns):
                        embeds = data.values
                    else:
                        embeds = data[numeric_cols].values
                        print(f"   [NOTE] Excluded {len(data.columns) - len(numeric_cols)} non-numeric columns from embeddings")
                
                # Strategy 2: Check if first column is explicitly an ID column
                elif len(data.columns) > 0 and str(data.columns[0]).lower() in ['protein_id', 'id', 'protein', 'proteinid']:
                    # IDs are in first column (explicit ID column name)
                    ids = data.iloc[:, 0].astype(str).tolist()
                    # Use remaining columns as embeddings (ensure they're numeric)
                    embed_cols = data.iloc[:, 1:]
                    numeric_cols = embed_cols.select_dtypes(include=[np.number]).columns
                    embeds = embed_cols[numeric_cols].values
                    if len(numeric_cols) < len(embed_cols.columns):
                        print(f"   [NOTE] Excluded {len(embed_cols.columns) - len(numeric_cols)} non-numeric columns")
                
                # Strategy 3: Check if first column looks like IDs (object dtype, string-like)
                elif len(data.columns) > 0 and pd.api.types.is_object_dtype(data.iloc[:, 0]):
                    # Check if first column values look like protein IDs (not numeric)
                    first_col_sample = data.iloc[:min(10, len(data)), 0]
                    if first_col_sample.dtype == 'object' and not pd.api.types.is_numeric_dtype(first_col_sample):
                        # First column appears to be IDs
                        ids = data.iloc[:, 0].astype(str).tolist()
                        # Use remaining columns as embeddings
                        embed_cols = data.iloc[:, 1:]
                        numeric_cols = embed_cols.select_dtypes(include=[np.number]).columns
                        embeds = embed_cols[numeric_cols].values
                        print(f"   [NOTE] Detected IDs in first column, using columns 1+ for embeddings")
                    else:
                        # Index likely contains IDs
                        ids = data.index.astype(str).tolist()
                        numeric_cols = data.select_dtypes(include=[np.number]).columns
                        embeds = data[numeric_cols].values
                else:
                    # Fallback: use index as IDs, ensure all columns are numeric
                    ids = data.index.astype(str).tolist()
                    numeric_cols = data.select_dtypes(include=[np.number]).columns
                    embeds = data[numeric_cols].values
                    if len(numeric_cols) < len(data.columns):
                        print(f"   [WARNING] Excluded {len(data.columns) - len(numeric_cols)} non-numeric columns")
            except Exception as e:
                # Final fallback: use index as IDs, numeric columns only
                ids = data.index.astype(str).tolist()
                numeric_cols = data.select_dtypes(include=[np.number]).columns
                embeds = data[numeric_cols].values
                print(f"   [WARNING] Using fallback extraction: {e}")
        else:
            raise ValueError(
                f"Unexpected DataFrame structure in .qs file. "
                f"Empty DataFrame or could not identify protein IDs. "
                f"Shape: {data.shape}, columns: {list(data.columns)}"
            )
        
        # Validate embeddings are numeric before conversion
        if embeds.size == 0:
            raise ValueError("No numeric embedding columns found in DataFrame")
        
        # Convert to numpy arrays and ensure float32
        try:
            embeds = np.asarray(embeds, dtype=np.float32)
        except (ValueError, TypeError) as e:
            # If conversion fails, there might still be non-numeric values
            raise ValueError(
                f"Failed to convert embeddings to float32. "
                f"This may indicate IDs are still included in embeddings. "
                f"Error: {e}"
            )
        ids = np.asarray(ids, dtype=str)
        
        print(f"   Loaded T5 {datatype}: {embeds.shape} (dtype: {embeds.dtype}), IDs: {len(ids)}")
        
        # Note: .qs files can't be memory-mapped, so we always return full array
        if use_memmap:
            print(f"   [NOTE] Memory mapping not supported for .qs files, loaded full array")
        
        return embeds, ids
        
    except Exception as e:
        raise IOError(
            f"Failed to load T5 embeddings from .qs file: {qs_path}\n"
            f"Error: {e}\n"
            f"Make sure the file is a valid .qs file and contains a DataFrame with protein IDs."
        )


def _load_t5_rds(rds_path: Path, datatype: str, use_memmap: bool) -> tuple:
    """
    Load T5 embeddings from .rds file (R data format).
    
    Args:
        rds_path: Path to .rds file
        datatype: 'train' or 'test'
        use_memmap: Whether to use memory mapping (not supported for .rds, will load full array)
        
    Returns:
        (embeddings_array, ids_array)
    """
    try:
        import pyreadr
    except ImportError:
        raise ImportError(
            "pyreadr library required for loading T5 .rds files. "
            "Install with: pip install pyreadr"
        )
    
    print(f"   Loading T5 {datatype} embeddings from .rds file: {rds_path}")
    
    # Try to load .rds file with pyreadr
    try:
        result = pyreadr.read_r(str(rds_path))
        
        # .rds files typically contain a single object, get the first (and usually only) key
        if not result:
            raise ValueError(f"No data found in .rds file: {rds_path}")
        
        # Get the first dataframe/array from the result
        data_key = list(result.keys())[0]
        data = result[data_key]
    except Exception as e:
        # If pyreadr fails, try alternative method using rpy2 (requires R)
        raise IOError(
            f"Failed to load .rds file with pyreadr: {e}\n"
            f"Consider using .qs files instead (T5_train_features.qs, T5_test_features.qs) "
            f"or install R and rpy2 for .rds support."
        )
    
    # Handle different possible structures:
    # 1. DataFrame with protein IDs as index and embeddings as columns
    # 2. DataFrame with protein IDs in first column and embeddings as other columns
    # 3. Matrix/array with separate IDs
    
    if hasattr(data, 'index') and hasattr(data, 'values'):
        # DataFrame structure
        if isinstance(data.index, pd.Index):
            # IDs are in index
            ids = data.index.tolist()
            embeds = data.values
        elif len(data.columns) > 0 and data.columns[0] in ['protein_id', 'id', 'ID', 'Protein_ID']:
            # IDs are in first column
            ids = data.iloc[:, 0].tolist()
            embeds = data.iloc[:, 1:].values
        else:
            # Assume first column is IDs (fallback)
            ids = data.iloc[:, 0].astype(str).tolist()
            embeds = data.iloc[:, 1:].values
    else:
        # Array/matrix structure - need to get IDs separately
        # This is a fallback - may need adjustment based on actual file structure
        raise ValueError(
            f"Unexpected data structure in .rds file. "
            f"Expected DataFrame with protein IDs. Got: {type(data)}"
        )
    
    # Convert to numpy arrays and ensure float32
    embeds = np.asarray(embeds, dtype=np.float32)
    ids = np.asarray(ids, dtype=str)
    
    print(f"   Loaded T5 {datatype}: {embeds.shape} (dtype: {embeds.dtype}), IDs: {len(ids)}")
    
    # Note: .rds files can't be memory-mapped, so we always return full array
    # If memmap was requested, we'll need to save as .npy first (future optimization)
    if use_memmap:
        print(f"   [NOTE] Memory mapping not supported for .rds files, loaded full array")
    
    return embeds, ids


def align_embeddings(embeds: np.ndarray, embed_ids: List[str], target_ids: List[str]) -> tuple:
    """
    Align embeddings to target protein order.
    Handles missing proteins gracefully.
    
    Args:
        embeds: numpy array of embeddings (n_proteins, n_features)
        embed_ids: list/array of protein IDs for embeddings
        target_ids: list/array of target protein IDs in desired order
    
    Returns:
        (aligned_embeddings, aligned_ids)
        - aligned_embeddings: numpy array in target order
        - aligned_ids: list of IDs that were successfully aligned
    """
    # Create lookup dictionary
    id_to_idx = {str(pid): i for i, pid in enumerate(embed_ids)}
    
    # Pre-allocate indices for faster alignment (avoids list appends)
    aligned_indices = []
    aligned_ids = []
    missing_ids = []
    
    for pid in target_ids:
        pid_str = str(pid)
        if pid_str in id_to_idx:
            aligned_indices.append(id_to_idx[pid_str])
            aligned_ids.append(pid)
        else:
            missing_ids.append(pid)
    
    if missing_ids:
        print(f"   [WARNING] {len(missing_ids)} proteins not found in embeddings (will be skipped)")
    
    # Use advanced indexing to create aligned array (more memory efficient)
    if aligned_indices:
        aligned_array = embeds[aligned_indices].copy()  # Copy to ensure contiguous memory
    else:
        aligned_array = np.array([])
    
    print(f"   Aligned {len(aligned_ids)}/{len(target_ids)} proteins")
    
    return aligned_array, aligned_ids


def extract_fused_embedding_features(sequence: str,
                                   embedding_types: List[str] = ['protbert', 'esm2', 't5'],
                                   embedding_data: Optional[Dict] = None) -> np.ndarray:
    """
    Extract fused features from multiple embedding types.
    
    Args:
        sequence: Protein amino acid sequence
        embedding_types: List of embedding types to use
        embedding_data: Pre-loaded embedding data
        
    Returns:
        np.ndarray: Fused feature vector
        
    Note:
        This implements the approach from the Kaggle notebook:
        - Select top 384 features from each embedding type
        - Concatenate to create 1152-dimensional fused features
    """
    raise NotImplementedError(
        "Fused embedding feature extraction not yet implemented.\n"
        "This will implement the multi-embedding approach from the Kaggle notebook:\n"
        "1. Load ProtBERT, ESM2, T5 embeddings\n"
        "2. Select top 384 features from each (by variance)\n"
        "3. Concatenate to create 1152-dimensional fused features"
    )


# Note: EMBEDDING_CONFIGS removed - use INDIVIDUAL_FEATURES from config.features instead
# This eliminates duplication and ensures single source of truth for embedding dimensions
