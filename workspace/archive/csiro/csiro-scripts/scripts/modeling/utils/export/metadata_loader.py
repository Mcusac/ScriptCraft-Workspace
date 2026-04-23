# metadata_loader_utils.py
# Utilities for loading model metadata from various sources
#
# This module is responsible for loading model metadata (preprocessing, augmentation, best_fold)
# from various sources with fallback logic. It does NOT load model weights.
#
# Model Loading Architecture:
# The model loading system is organized into distinct responsibilities:
#
# 1. Model Path Finding (model_finder_utils):
#    - Finds model checkpoint paths in various locations
#    - Uses strategy pattern to organize location-specific logic
#    - Returns Path objects to checkpoint files
#
# 2. Model Metadata Loading (this module):
#    - Loads preprocessing_list, augmentation_list, best_fold
#    - Tries multiple sources with fallback logic
#    - Does NOT load model weights
#
# 3. Model Weight Loading (checkpoint):
#    - Loads actual model weights from checkpoint files
#    - Handles DataParallel wrapping/unwrapping
#    - Returns model state dicts and checkpoint metadata
#
# 4. Ensemble Orchestration (ensembling/model_loader):
#    - Higher-level orchestrator for loading multiple models
#    - Combines path finding, weight loading, and validation
#    - Manages memory and model creation
#
# Responsibility boundaries:
# - This module: Metadata extraction from JSON files (model_metadata.json, results.json)
# - model_finder_utils: Finding checkpoint file paths
# - checkpoint: Loading PyTorch checkpoint weights
# - ensembling/model_loader: Multi-model orchestration

import logging
from pathlib import Path
from typing import Dict, Any, Optional

from ..results.best_variant import get_best_variant_info
from ..metadata.data_manipulation_loader import (
    find_metadata_dir,
    get_combo_details
)
from utils.system.io import load_json_file

logger = logging.getLogger(__name__)


def _is_regression_model_metadata(metadata: Dict[str, Any], model_path: Optional[Path] = None) -> bool:
    """
    Detect if metadata is for a regression model.
    
    Args:
        metadata: Metadata dictionary
        model_path: Optional model path (for file extension check)
    
    Returns:
        True if this is regression model metadata, False otherwise
    """
    # Check for regression_model_type field
    if 'regression_model_type' in metadata:
        return True
    
    # Check file extension if model_path provided
    if model_path and model_path.suffix == '.pkl':
        return True
    
    return False


def load_model_metadata(
    metadata_path: Optional[Path],
    results_file: Optional[Path],
    model_path: Optional[Path] = None
) -> Dict[str, Any]:
    """
    Load model metadata from various sources with fallback logic.
    
    Tries sources in order:
    1. Explicit metadata_path (model_metadata.json)
    2. Explicit results_file (results.json)
    3. results.json near model_path
    4. Defaults (empty preprocessing/augmentation, fold 0)
    
    Args:
        metadata_path: Optional path to model_metadata.json
        results_file: Optional path to results.json (fallback)
        model_path: Optional model path to search for nearby results.json
        
    Returns:
        Dictionary with keys:
        - preprocessing_list: List of preprocessing techniques (default: [])
        - augmentation_list: List of augmentation techniques (default: [])
        - best_fold: Best fold number (default: 0)
        - dataset_type: Dataset type used ('full' or 'split', default: 'split')
        - feature_extraction_model_name: Name of feature extraction model (if available, for end-to-end models)
        - regression_model_type: Type of regression model (if available)
        - feature_filename: Feature filename (for regression models)
        - variant_id: Variant ID (for regression models)
        - variant_index: Variant index (for regression models)
    """
    preprocessing_list = []
    augmentation_list = []
    best_fold = 0  # Default
    dataset_type = 'split'  # Default value (standard approach)
    feature_extraction_model_name = None
    regression_model_type = None
    feature_filename = None
    variant_id = None
    variant_index = None
    
    # 1. Try explicit metadata_path
    if metadata_path and metadata_path.exists():
        logger.info(f"Loading metadata from: {metadata_path}")
        try:
            metadata = load_json_file(metadata_path, expected_type=dict, file_type="Model metadata")
            
            # Check if this is a regression model
            is_regression = _is_regression_model_metadata(metadata, model_path)
            
            if is_regression:
                # Regression model: skip data_manipulation validation
                # Regression models work on already-extracted features, so preprocessing/augmentation
                # belong to feature extraction, not regression
                preprocessing_list = []
                augmentation_list = []
                
                best_fold = metadata.get('best_fold', 0)
                regression_model_type = metadata.get('regression_model_type')
                feature_filename = metadata.get('feature_filename')
                variant_id = metadata.get('variant_id')
                variant_index = metadata.get('variant_index')
                
                logger.info(f"  Regression Model Type: {regression_model_type}")
                logger.info(f"  Variant ID: {variant_id}")
                logger.info(f"  Variant Index: {variant_index}")
                logger.info(f"  Feature Filename: {feature_filename}")
                logger.info(f"  Best Fold: {best_fold}")
                logger.info(f"  (Preprocessing/augmentation not applicable - regression works on extracted features)")
                
                return {
                    'preprocessing_list': preprocessing_list,
                    'augmentation_list': augmentation_list,
                    'best_fold': best_fold,
                    'dataset_type': 'split',  # Default for regression (feature extraction handles splitting)
                    'regression_model_type': regression_model_type,
                    'feature_filename': feature_filename,
                    'variant_id': variant_id,
                    'variant_index': variant_index
                }
            else:
                # End-to-end model: require data_manipulation.combo_id
                data_manipulation = metadata.get('data_manipulation')
                if data_manipulation:
                    combo_id = data_manipulation.get('combo_id')
                    if combo_id:
                        metadata_dir = find_metadata_dir()
                        if metadata_dir:
                            try:
                                combo_details = get_combo_details(combo_id, metadata_dir)
                                preprocessing_list = combo_details['preprocessing_list']
                                augmentation_list = combo_details['augmentation_list']
                            except Exception as e:
                                logger.warning(f"Failed to resolve combo_id {combo_id}: {e}")
                else:
                    # No data_manipulation field - this should not happen with new format for end-to-end models
                    raise ValueError(
                        f"Metadata file {metadata_path} missing data_manipulation field. "
                        "All end-to-end model metadata must use data_manipulation.combo_id format."
                    )
                
                best_fold = metadata.get('best_fold', 0)
                dataset_type = metadata.get('dataset_type', 'split')  # Default to 'split'
                feature_extraction_model_name = metadata.get('feature_extraction_model_name')
                
                logger.info(f"  Preprocessing: {preprocessing_list if preprocessing_list else '[]'}")
                logger.info(f"  Augmentation: {augmentation_list if augmentation_list else '[]'}")
                logger.info(f"  Best Fold: {best_fold}")
                logger.info(f"  Dataset Type: {dataset_type}")
                if feature_extraction_model_name:
                    logger.info(f"  Feature Extraction Model: {feature_extraction_model_name}")
                
                return {
                    'preprocessing_list': preprocessing_list,
                    'augmentation_list': augmentation_list,
                    'best_fold': best_fold,
                    'dataset_type': dataset_type,
                    'feature_extraction_model_name': feature_extraction_model_name
                }
        except Exception as e:
            logger.warning(f"Failed to load from metadata.json: {e}")
    
    # 2. Try explicit results_file
    if results_file and results_file.exists():
        logger.info(f"Loading variant info from results.json: {results_file}")
        try:
            variant_info = get_best_variant_info(results_file)
            
            # Check if this is a regression model
            is_regression = variant_info.get('regression_model_type') is not None
            
            if is_regression:
                # Regression model: preprocessing/augmentation not applicable
                preprocessing_list = []
                augmentation_list = []
                best_fold = variant_info.get('best_fold', 0)
                regression_model_type = variant_info.get('regression_model_type')
                feature_filename = variant_info.get('feature_filename')
                variant_id = variant_info.get('variant_id')
                variant_index = variant_info.get('variant_index')
                
                logger.info(f"  Regression Model Type: {regression_model_type}")
                logger.info(f"  Variant ID: {variant_id}")
                logger.info(f"  Variant Index: {variant_index}")
                logger.info(f"  Feature Filename: {feature_filename}")
                logger.info(f"  Best Fold: {best_fold}")
                
                return {
                    'preprocessing_list': preprocessing_list,
                    'augmentation_list': augmentation_list,
                    'best_fold': best_fold,
                    'dataset_type': 'split',  # Default for regression
                    'regression_model_type': regression_model_type,
                    'feature_filename': feature_filename,
                    'variant_id': variant_id,
                    'variant_index': variant_index
                }
            else:
                # End-to-end model
                preprocessing_list = variant_info.get('preprocessing_list', [])
                augmentation_list = variant_info.get('augmentation_list', [])
                best_fold = variant_info.get('best_fold', 0)
                dataset_type = variant_info.get('dataset_type', 'split')  # Default to 'split'
                feature_extraction_model_name = variant_info.get('feature_extraction_model_name')
                
                logger.info(f"  Preprocessing: {preprocessing_list if preprocessing_list else '[]'}")
                logger.info(f"  Augmentation: {augmentation_list if augmentation_list else '[]'}")
                logger.info(f"  Best Fold: {best_fold}")
                logger.info(f"  Dataset Type: {dataset_type}")
                if feature_extraction_model_name:
                    logger.info(f"  Feature Extraction Model: {feature_extraction_model_name}")
                
                return {
                    'preprocessing_list': preprocessing_list,
                    'augmentation_list': augmentation_list,
                    'best_fold': best_fold,
                    'dataset_type': dataset_type,
                    'feature_extraction_model_name': feature_extraction_model_name
                }
        except Exception as e:
            logger.warning(f"Failed to load from results.json: {e}")
    
    # 3. Try results.json near model_path
    if model_path:
        potential_results = model_path.parent / 'gridsearch_results.json'
        
        if potential_results.exists():
            logger.info(f"Found results file: {potential_results}")
            try:
                variant_info = get_best_variant_info(potential_results)
                
                # Check if this is a regression model
                is_regression = variant_info.get('regression_model_type') is not None
                
                if is_regression:
                    # Regression model: preprocessing/augmentation not applicable
                    preprocessing_list = []
                    augmentation_list = []
                    best_fold = variant_info.get('best_fold', 0)
                    regression_model_type = variant_info.get('regression_model_type')
                    feature_filename = variant_info.get('feature_filename')
                    variant_id = variant_info.get('variant_id')
                    variant_index = variant_info.get('variant_index')
                    
                    logger.info(f"  Regression Model Type: {regression_model_type}")
                    logger.info(f"  Variant ID: {variant_id}")
                    logger.info(f"  Feature Filename: {feature_filename}")
                    logger.info(f"  Best Fold: {best_fold}")
                    
                    return {
                        'preprocessing_list': preprocessing_list,
                        'augmentation_list': augmentation_list,
                        'best_fold': best_fold,
                        'dataset_type': 'split',  # Default for regression
                        'regression_model_type': regression_model_type,
                        'feature_filename': feature_filename,
                        'variant_id': variant_id,
                        'variant_index': variant_index
                    }
                else:
                    # End-to-end model
                    preprocessing_list = variant_info.get('preprocessing_list', [])
                    augmentation_list = variant_info.get('augmentation_list', [])
                    best_fold = variant_info.get('best_fold', 0)
                    dataset_type = variant_info.get('dataset_type', 'split')  # Default to 'split'
                    feature_extraction_model_name = variant_info.get('feature_extraction_model_name')
                    
                    logger.info(f"  Preprocessing: {preprocessing_list if preprocessing_list else '[]'}")
                    logger.info(f"  Augmentation: {augmentation_list if augmentation_list else '[]'}")
                    logger.info(f"  Best Fold: {best_fold}")
                    logger.info(f"  Dataset Type: {dataset_type}")
                    if feature_extraction_model_name:
                        logger.info(f"  Feature Extraction Model: {feature_extraction_model_name}")
                    
                    return {
                        'preprocessing_list': preprocessing_list,
                        'augmentation_list': augmentation_list,
                        'best_fold': best_fold,
                        'dataset_type': dataset_type,
                        'feature_extraction_model_name': feature_extraction_model_name
                    }
            except Exception as e:
                logger.warning(f"Failed to load from results file: {e}")
    
    # 4. Defaults
    logger.info("No metadata or results.json found - using default configuration")
    logger.info("(No preprocessing/augmentation will be applied)")
    return {
        'preprocessing_list': preprocessing_list,
        'augmentation_list': augmentation_list,
        'best_fold': best_fold,
        'dataset_type': dataset_type,  # Defaults to 'split'
        'feature_extraction_model_name': feature_extraction_model_name,
        'regression_model_type': regression_model_type,
        'feature_filename': feature_filename,
        'variant_id': variant_id,
        'variant_index': variant_index
    }

