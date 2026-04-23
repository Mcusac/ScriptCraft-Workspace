# metadata_builder.py
# Builder pattern for creating model metadata from various sources
#
# This module consolidates all metadata creation logic that was previously
# duplicated across export_model.py, training_results_utils.py, and
# model_export_utils.py. It provides a unified interface for building
# metadata dictionaries from multiple sources.

import logging
from pathlib import Path
from typing import Dict, Any, Optional, List

from config.config import Config
from modeling.training.utils.checkpoint_scores import extract_scores_from_checkpoint

logger = logging.getLogger(__name__)


class MetadataBuilder:
    """
    Builder for creating model metadata dictionaries from various sources.
    
    Supports multiple data sources with priority ordering:
    1. variant_info (from results.json) - most complete
    2. metadata_file (from existing export) - complete metadata
    3. checkpoint_path (extract from model) - extract scores
    4. config (fallback defaults) - minimal
    
    Usage:
        builder = MetadataBuilder(model_name='dinov2')
        metadata = builder.from_variant_info(variant_info)
        
        # Or with fallback chain:
        metadata = builder.from_variant_info(variant_info) or \
                   builder.from_metadata_file(metadata_path) or \
                   builder.from_checkpoint(checkpoint_path, config)
    """
    
    def __init__(self, model_name: str):
        """
        Initialize metadata builder.
        
        Args:
            model_name: Model name/architecture (e.g., 'dinov2', 'efficientnet_b3')
        """
        self.model_name = model_name
    
    def from_variant_info(self, variant_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Build metadata from variant info (from results.json).
        
        This is the most complete source as it contains all information
        from grid search results.
        
        Args:
            variant_info: Dictionary from get_best_variant_info() or similar
            
        Returns:
            Complete metadata dictionary
        """
        metadata = {
            'model_name': self.model_name,
            'preprocessing_list': variant_info.get('preprocessing_list', []),
            'augmentation_list': variant_info.get('augmentation_list', []),
            'cv_score': variant_info.get('cv_score', 0.0),
            'best_fold': variant_info.get('best_fold'),
            'best_fold_score': variant_info.get('best_fold_score'),
            'fold_scores': variant_info.get('fold_scores', []),
            'variant_id': variant_info.get('variant_id'),
            'dataset_type': variant_info.get('dataset_type', 'split')
        }
        
        # Add feature extraction info if present in variant_info
        if 'feature_extraction_model_name' in variant_info:
            metadata['feature_extraction_model_name'] = variant_info['feature_extraction_model_name']
        if 'regression_model_type' in variant_info:
            metadata['regression_model_type'] = variant_info['regression_model_type']
        
        return metadata
    
    def from_metadata_file(self, metadata_path: Path) -> Optional[Dict[str, Any]]:
        """
        Build metadata from existing metadata file.
        
        Args:
            metadata_path: Path to model_metadata.json file
            
        Returns:
            Metadata dictionary if file exists, None otherwise
        """
        if not metadata_path or not metadata_path.exists():
            return None
        
        try:
            from utils.system.io import load_json_file
            metadata_dict = load_json_file(metadata_path, expected_type=dict, file_type="Model metadata")
            
            # Ensure model_name is set
            metadata_dict['model_name'] = self.model_name
            return metadata_dict
        except Exception as e:
            logger.warning(f"Failed to load metadata from {metadata_path}: {e}")
            return None
    
    def from_checkpoint(
        self,
        checkpoint_path: Path,
        config: Optional[Config] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Build metadata by extracting scores from checkpoint.
        
        Args:
            checkpoint_path: Path to model checkpoint file
            config: Optional config object for fallback values
            
        Returns:
            Metadata dictionary if checkpoint exists, None otherwise
        """
        if not checkpoint_path or not checkpoint_path.exists():
            return None
        
        try:
            # Extract scores using centralized utility
            cv_score, fold_scores, best_fold = extract_scores_from_checkpoint(
                checkpoint_path
            )
            
            # Get preprocessing/augmentation from config or defaults
            preprocessing_list = []
            augmentation_list = []
            dataset_type = 'split'  # Default to 'split' (standard approach)
            
            if config:
                preprocessing_list = config.data.preprocessing_list or []
                augmentation_list = config.data.augmentation_list or []
                dataset_type = getattr(config.data, 'dataset_type', 'split')
            
            return {
                'model_name': self.model_name,
                'preprocessing_list': preprocessing_list,
                'augmentation_list': augmentation_list,
                'cv_score': cv_score,
                'fold_scores': fold_scores,
                'best_fold': best_fold,
                'best_fold_score': fold_scores[best_fold] if best_fold < len(fold_scores) else 0.0,
                'dataset_type': dataset_type
            }
        except Exception as e:
            logger.warning(f"Failed to extract metadata from checkpoint {checkpoint_path}: {e}")
            return None
    
    def with_config_defaults(self, config: Optional[Config] = None) -> Dict[str, Any]:
        """
        Build minimal metadata from config defaults.
        
        This is a fallback when no other source is available.
        
        Args:
            config: Optional config object for defaults
            
        Returns:
            Minimal metadata dictionary with defaults
        """
        preprocessing_list = []
        augmentation_list = []
        dataset_type = 'split'  # Default to 'split' (standard approach)
        
        if config:
            preprocessing_list = config.data.preprocessing_list or []
            augmentation_list = config.data.augmentation_list or []
            dataset_type = getattr(config.data, 'dataset_type', 'split')
        
        return {
            'model_name': self.model_name,
            'preprocessing_list': preprocessing_list,
            'augmentation_list': augmentation_list,
            'cv_score': 0.0,
            'fold_scores': [],
            'best_fold': 0,
            'best_fold_score': 0.0,
            'dataset_type': dataset_type
        }
    
    def build(
        self,
        variant_info: Optional[Dict[str, Any]] = None,
        metadata_file: Optional[Path] = None,
        checkpoint_path: Optional[Path] = None,
        config: Optional[Config] = None
    ) -> Dict[str, Any]:
        """
        Build metadata using priority order with automatic fallback.
        
        Priority:
        1. variant_info (most complete)
        2. metadata_file (complete metadata)
        3. checkpoint_path (extract scores)
        4. config defaults (minimal)
        
        Args:
            variant_info: Optional variant info from results.json
            metadata_file: Optional path to existing metadata file
            checkpoint_path: Optional path to checkpoint to extract from
            config: Optional config for fallback values
            
        Returns:
            Complete metadata dictionary
            
        Raises:
            ValueError: If no valid source provided and config is None
        """
        # Priority 1: variant_info
        if variant_info:
            return self.from_variant_info(variant_info)
        
        # Priority 2: metadata_file
        if metadata_file:
            metadata = self.from_metadata_file(metadata_file)
            if metadata:
                return metadata
        
        # Priority 3: checkpoint_path
        if checkpoint_path:
            metadata = self.from_checkpoint(checkpoint_path, config)
            if metadata:
                return metadata
        
        # Priority 4: config defaults
        if config:
            return self.with_config_defaults(config)
        
        raise ValueError(
            "Must provide at least one of: variant_info, metadata_file, "
            "checkpoint_path, or config"
        )


def prepare_model_metadata_dict(
    model_name: str,
    preprocessing_list: List[str],
    augmentation_list: List[str],
    cv_score: float,
    best_fold: int,
    best_fold_score: float,
    variant_id: Optional[str] = None,
    dataset_type: str = 'full'
) -> Dict[str, Any]:
    """
    Create model metadata dictionary from explicit parameters.
    
    This is a convenience function for creating metadata when all values
    are already known (e.g., from training results).
    
    Args:
        model_name: Name of the model architecture
        preprocessing_list: List of preprocessing techniques
        augmentation_list: List of augmentation techniques
        cv_score: Cross-validation score
        best_fold: Best fold number
        best_fold_score: Best fold score
        variant_id: Optional variant ID (for grid search models)
        dataset_type: Dataset type used ('split' or 'full', defaults to 'split')
        
    Returns:
        Dictionary with metadata
    """
    metadata = {
        'model_name': model_name,
        'preprocessing_list': preprocessing_list,
        'augmentation_list': augmentation_list,
        'cv_score': cv_score,
        'best_fold': best_fold,
        'best_fold_score': best_fold_score,
        'dataset_type': dataset_type or 'split'  # Default to 'split' if None
    }
    
    if variant_id:
        metadata['variant_id'] = variant_id
    
    return metadata


def prepare_regression_model_metadata_dict(
    regression_model_type: str,
    cv_score: float,
    fold_scores: List[float],
    hyperparameters: Dict[str, Any],
    feature_filename: str,
    variant_id: Optional[str] = None,
    variant_index: Optional[int] = None,
    best_fold: Optional[int] = None,
    best_fold_score: Optional[float] = None
) -> Dict[str, Any]:
    """
    Create regression model metadata dictionary from explicit parameters.
    
    Regression models train on pre-extracted features. The feature filename
    identifies which feature file was used for training and encodes both the
    feature extraction model (model_id) and data manipulation combo (combo_id).
    
    This function creates metadata specifically for regression head models.
    It does NOT include preprocessing_list/augmentation_list as those belong
    to the feature extraction model, not the regression head.
    
    Args:
        regression_model_type: Type of regression model ('lgbm', 'xgboost', 'ridge')
        cv_score: Cross-validation score
        fold_scores: List of scores for each fold
        hyperparameters: Model-specific hyperparameters dictionary
        feature_filename: Feature filename used for training (e.g., 'variant_0100_features.npz') - REQUIRED
        variant_id: Variant ID (e.g., 'variant_0000') - REQUIRED
        variant_index: Sequential variant index (e.g., 0, 1, 2) - REQUIRED
        best_fold: Optional best fold number
        best_fold_score: Optional best fold score
        
    Returns:
        Dictionary with regression model metadata. Does NOT include:
        - preprocessing_list (belongs to feature extraction model)
        - augmentation_list (belongs to feature extraction model)
        - dataset_type (feature extraction handles splitting, defaults to 'split')
        - feature_extraction_model_name (derived from feature_filename)
        - model_name (use regression_model_type instead)
        
    Raises:
        ValueError: If variant_id, variant_index, or feature_filename are None
    """
    # Validate required fields
    if variant_id is None:
        raise ValueError("variant_id is required for regression model metadata")
    if variant_index is None:
        raise ValueError("variant_index is required for regression model metadata")
    if not feature_filename:
        raise ValueError("feature_filename is required for regression model metadata")
    
    metadata = {
        'regression_model_type': regression_model_type,
        'variant_index': variant_index,
        'variant_id': variant_id,
        'cv_score': cv_score,
        'fold_scores': fold_scores,
        'hyperparameters': hyperparameters,
        'feature_filename': feature_filename
    }
    
    # Add optional fields if provided
    if best_fold is not None:
        metadata['best_fold'] = best_fold
    if best_fold_score is not None:
        metadata['best_fold_score'] = best_fold_score
    
    return metadata

