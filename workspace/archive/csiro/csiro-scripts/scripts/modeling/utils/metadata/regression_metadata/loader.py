# loader.py
# Load operations for regression metadata

import logging
from typing import Dict, List, Any, Optional

from utils.system.io import load_json_file
from ..data_manipulation_loader import find_metadata_dir

logger = logging.getLogger(__name__)


def load_regression_variant_from_metadata(
    regression_model_type: str,
    variant_id: str,
    feature_filename: Optional[str] = None
) -> Dict[str, Any]:
    """
    Load regression model variant from metadata file.
    
    Loads hyperparameters from metadata.json. Optionally loads results from
    gridsearch_metadata.json if feature_filename is provided.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        variant_id: Variant ID to load (e.g., "variant_0000")
        feature_filename: Optional feature filename to load results for specific feature file
        
    Returns:
        Dictionary with keys:
        - 'variant': Full variant dictionary from metadata
        - 'variant_id': Variant ID
        - 'cv_score': Cross-validation score (None if not in metadata.json or gridsearch_metadata.json)
        - 'hyperparameters': Hyperparameters dictionary
        - 'feature_filename': Feature filename (None if not in metadata.json, or from gridsearch if provided)
        - 'fold_scores': Fold scores (None if not available)
        
    Raises:
        FileNotFoundError: If metadata directory or file not found
        ValueError: If regression_model_type is invalid or variant not found
    """
    # Validate regression model type
    valid_types = {'lgbm', 'xgboost', 'ridge'}
    if regression_model_type not in valid_types:
        raise ValueError(
            f"Invalid regression_model_type: {regression_model_type}. "
            f"Must be one of: {valid_types}"
        )
    
    # Find metadata directory (check both input and working)
    input_metadata_dir = find_metadata_dir()
    if input_metadata_dir is None:
        raise FileNotFoundError(
            "csiro-metadata directory not found. "
            "Expected: /kaggle/input/csiro-metadata (Kaggle) or ../csiro-metadata (local)"
        )
    
    # Check both input and working directories
    input_metadata_file = None
    working_metadata_file = None
    
    if str(input_metadata_dir).startswith('/kaggle/input'):
        input_metadata_file = input_metadata_dir / regression_model_type / 'metadata.json'
        from config.path_constants import KAGGLE_WORKING
        working_metadata_file = KAGGLE_WORKING / 'csiro-metadata' / regression_model_type / 'metadata.json'
    else:
        working_metadata_file = input_metadata_dir / regression_model_type / 'metadata.json'
    
    # Load metadata from both locations
    variants = []
    if input_metadata_file and input_metadata_file.exists():
        variants = load_json_file(
            input_metadata_file, expected_type=list, file_type="Regression metadata JSON"
        )
    
    if working_metadata_file and working_metadata_file.exists():
        working_variants = load_json_file(
            working_metadata_file, expected_type=list, file_type="Regression metadata JSON"
        )
        # Merge: add working variants, but skip if variant_id already exists
        existing_ids = {v.get('variant_id') for v in variants}
        for v in working_variants:
            if v.get('variant_id') not in existing_ids:
                variants.append(v)
    
    if not variants:
        raise FileNotFoundError(
            f"Regression metadata file not found in either location.\n"
            f"  Checked: {input_metadata_file if input_metadata_file else 'N/A'}\n"
            f"  Checked: {working_metadata_file if working_metadata_file else 'N/A'}"
        )
    
    # Find variant by variant_id
    variant = None
    for v in variants:
        if v.get('variant_id') == variant_id:
            variant = v
            break
    
    if variant is None:
        available_ids = [v.get('variant_id') for v in variants]
        # Build list of checked files for error message
        checked_files = []
        if input_metadata_file and input_metadata_file.exists():
            checked_files.append(str(input_metadata_file))
        if working_metadata_file and working_metadata_file.exists():
            checked_files.append(str(working_metadata_file))
        files_str = "\n  ".join(checked_files) if checked_files else "No metadata files found"
        raise ValueError(
            f"Regression variant {variant_id} not found in metadata files.\n"
            f"  Checked files:\n  {files_str}\n"
            f"  Available variant IDs: {available_ids}"
        )
    
    # Extract hyperparameters
    hyperparameters = variant.get('hyperparameters', {})
    if not hyperparameters:
        logger.warning(f"Variant {variant_id} has no hyperparameters in metadata")
    
    # Load from gridsearch_metadata.json if feature_filename provided
    if feature_filename:
        # Check both input and working directories
        input_gridsearch_file = None
        working_gridsearch_file = None
        
        if str(input_metadata_dir).startswith('/kaggle/input'):
            input_gridsearch_file = input_metadata_dir / regression_model_type / 'gridsearch_metadata.json'
            from config.path_constants import KAGGLE_WORKING
            working_gridsearch_file = KAGGLE_WORKING / 'csiro-metadata' / regression_model_type / 'gridsearch_metadata.json'
        else:
            working_gridsearch_file = input_metadata_dir / regression_model_type / 'gridsearch_metadata.json'
        
        # Load from both locations
        gridsearch_results = []
        if input_gridsearch_file and input_gridsearch_file.exists():
            gridsearch_results = load_json_file(
                input_gridsearch_file, expected_type=list, file_type="Regression gridsearch metadata JSON"
            )
        
        if working_gridsearch_file and working_gridsearch_file.exists():
            working_results = load_json_file(
                working_gridsearch_file, expected_type=list, file_type="Regression gridsearch metadata JSON"
            )
            # Merge results
            existing_keys = {(r.get('variant_id'), r.get('feature_filename')) for r in gridsearch_results}
            for r in working_results:
                key = (r.get('variant_id'), r.get('feature_filename'))
                if key not in existing_keys:
                    gridsearch_results.append(r)
        
        # Find result for this variant_id and feature_filename
        for result in gridsearch_results:
            if (result.get('variant_id') == variant_id and 
                result.get('feature_filename') == feature_filename):
                cv_score = result.get('cv_score')
                fold_scores = result.get('fold_scores')
                feature_filename_from_metadata = feature_filename
                break
    
    return {
        'variant': variant,
        'variant_id': variant_id,
        'cv_score': cv_score,
        'hyperparameters': hyperparameters,
        'feature_filename': feature_filename_from_metadata,
        'fold_scores': fold_scores
    }


def load_regression_gridsearch_results(
    regression_model_type: str,
    variant_id: Optional[str] = None,
    feature_filename: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Load regression grid search results from gridsearch_metadata.json.
    
    Can filter by variant_id, feature_filename, or both.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        variant_id: Optional variant ID to filter by
        feature_filename: Optional feature filename to filter by
        
    Returns:
        List of result dictionaries matching the filters
        
    Raises:
        FileNotFoundError: If metadata directory not found
        ValueError: If regression_model_type is invalid
    """
    # Validate regression model type
    valid_types = {'lgbm', 'xgboost', 'ridge'}
    if regression_model_type not in valid_types:
        raise ValueError(
            f"Invalid regression_model_type: {regression_model_type}. "
            f"Must be one of: {valid_types}"
        )
    
    # Find metadata directory (check both input and working)
    input_metadata_dir = find_metadata_dir()
    if input_metadata_dir is None:
        return []
    
    # Check both input and working directories
    input_gridsearch_file = None
    working_gridsearch_file = None
    
    if str(input_metadata_dir).startswith('/kaggle/input'):
        input_gridsearch_file = input_metadata_dir / regression_model_type / 'gridsearch_metadata.json'
        from config.path_constants import KAGGLE_WORKING
        working_gridsearch_file = KAGGLE_WORKING / 'csiro-metadata' / regression_model_type / 'gridsearch_metadata.json'
    else:
        working_gridsearch_file = input_metadata_dir / regression_model_type / 'gridsearch_metadata.json'
    
    # Load results from both locations
    results = []
    if input_gridsearch_file and input_gridsearch_file.exists():
        results = load_json_file(
            input_gridsearch_file, expected_type=list, file_type="Regression gridsearch metadata JSON"
        )
    
    if working_gridsearch_file and working_gridsearch_file.exists():
        working_results = load_json_file(
            working_gridsearch_file, expected_type=list, file_type="Regression gridsearch metadata JSON"
        )
        # Merge: add working results, but skip if variant_id+feature_filename already exists
        existing_keys = {(r.get('variant_id'), r.get('feature_filename')) for r in results}
        for r in working_results:
            key = (r.get('variant_id'), r.get('feature_filename'))
            if key not in existing_keys:
                results.append(r)
    
    # Filter results
    filtered_results = []
    for result in results:
        if variant_id and result.get('variant_id') != variant_id:
            continue
        if feature_filename and result.get('feature_filename') != feature_filename:
            continue
        filtered_results.append(result)
    
    return filtered_results
