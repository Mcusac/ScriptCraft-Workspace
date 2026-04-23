# export_model.py
# Atomic pipeline to export existing trained model
#
# This is a pure orchestrator that delegates to utilities for all operations.
# It determines the export scenario, finds the model and metadata, then
# delegates to appropriate export utilities.
#
# Architecture:
# - Orchestrator: export_model_pipeline() - determines scenario and delegates
# - Scenario Handlers: export_scenario_handlers.py - find model and metadata
# - Export Utilities: model_export_utils.py - perform actual export operations
# - Metadata Builder: metadata_builder.py - creates metadata from various sources

import json
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from config.config import Config
from utils.config import validate_pipeline_config
from modeling.utils import (
    handle_just_trained_model,
    handle_best_variant_file,
    handle_results_file,
    handle_auto_detect,
    export_from_training_dir,
    export_from_grid_search,
    export_from_single_checkpoint,
    copy_results_file
)
from modeling import (
    find_metadata_dir,
    extract_preprocessing_augmentation_from_variant
)

logger = logging.getLogger(__name__)


def _validate_exported_metadata(
    metadata: dict,
    results_file: Path,
    variant_id: str
) -> None:
    """
    Validate that exported metadata matches the source results.json.
    
    This prevents exporting wrong models by ensuring cv_score and other
    metadata match what's in the results file.
    
    Args:
        metadata: Exported metadata dictionary
        results_file: Path to source results.json file
        variant_id: Variant ID that was exported
        
    Raises:
        ValueError: If metadata doesn't match source results
    """
    if not results_file.exists():
        logger.warning("⚠️ Cannot validate metadata: results.json not found")
        return
    
    try:
        with open(results_file, 'r') as f:
            results = json.load(f)
        
        # Find the variant in results
        variant = None
        for r in results:
            if r.get('variant_id') == variant_id:
                variant = r
                break
        
        if variant is None:
            logger.warning(f"⚠️ Cannot validate: variant {variant_id} not found in results.json")
            return
        
        # Validate cv_score matches
        exported_cv = metadata.get('cv_score')
        source_cv = variant.get('cv_score')
        
        if exported_cv is not None and source_cv is not None:
            if abs(exported_cv - source_cv) > 1e-6:
                error_msg = (
                    f"❌ VALIDATION FAILED: Exported cv_score ({exported_cv:.6f}) "
                    f"does not match source cv_score ({source_cv:.6f}) in results.json\n"
                    f"This indicates the wrong model may have been exported!"
                )
                logger.error(error_msg)
                raise ValueError(error_msg)
            else:
                logger.info(f"✅ Validation passed: cv_score matches ({exported_cv:.6f})")
        
        # Validate best_fold_score matches
        exported_best_fold_score = metadata.get('best_fold_score')
        if exported_best_fold_score is not None:
            # Get best fold from variant
            fold_scores = variant.get('fold_scores', [])
            if fold_scores:
                from modeling.training.utils import find_best_fold_from_scores
                best_fold_idx, source_best_fold_score = find_best_fold_from_scores(fold_scores)
                if abs(exported_best_fold_score - source_best_fold_score) > 1e-6:
                    error_msg = (
                        f"❌ VALIDATION FAILED: Exported best_fold_score ({exported_best_fold_score:.6f}) "
                        f"does not match source best_fold_score ({source_best_fold_score:.6f}) in results.json\n"
                        f"This indicates the wrong fold may have been selected!"
                    )
                    logger.error(error_msg)
                    raise ValueError(error_msg)
                else:
                    logger.info(f"✅ Validation passed: best_fold_score matches ({exported_best_fold_score:.6f})")
        
        # Validate preprocessing and augmentation match
        # Resolve source preprocessing/augmentation from variant (may have data_manipulation.combo_id)
        source_prep = []
        source_aug = []
        try:
            metadata_dir = find_metadata_dir()
            if metadata_dir:
                source_prep, source_aug = extract_preprocessing_augmentation_from_variant(
                    variant, metadata_dir
                )
        except (ValueError, FileNotFoundError) as e:
            logger.warning(f"Could not resolve data_manipulation for validation: {e}")
            # If resolution fails, validation will fail below (which is correct)
        
        exported_prep = set(metadata.get('preprocessing_list', []))
        source_prep_set = set(source_prep)
        if exported_prep != source_prep_set:
            error_msg = (
                f"❌ VALIDATION FAILED: Preprocessing mismatch: "
                f"exported {sorted(exported_prep)} vs source {sorted(source_prep_set)}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        exported_aug = set(metadata.get('augmentation_list', []))
        source_aug_set = set(source_aug)
        if exported_aug != source_aug_set:
            error_msg = (
                f"❌ VALIDATION FAILED: Augmentation mismatch: "
                f"exported {sorted(exported_aug)} vs source {sorted(source_aug_set)}"
            )
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info("✅ All metadata validation checks passed")
            
    except ValueError:
        # Re-raise ValueError (validation failures)
        raise
    except Exception as e:
        logger.warning(f"⚠️ Error during metadata validation: {e}")
        # Don't fail export if validation fails due to unexpected errors, just warn


def export_model_pipeline(
    config: Config,
    results_file: Optional[str] = None,
    variant_id: Optional[str] = None,
    variant_info: Optional[Dict[str, Any]] = None,
    best_variant_file: Optional[str] = None,
    model_dir: Optional[str] = None,
    export_dir: Optional[str] = None
) -> None:
    """
    Export existing trained model for submission.
    
    Pure orchestrator that delegates to utilities for all operations.
    Can export from ANY source:
    - Just-trained models (via model_dir) - from recent training run
    - Grid search models (via results_file) - finds best variant from grid search
    - Best variant file (via best_variant_file) - from best_dataset_variant.json
    - CSIRO models location (auto-detect) - from /kaggle/input/csiro-models/
    
    Args:
        config: Configuration object with model, paths, and device settings.
                Must have all required attributes configured.
        results_file: Optional path to grid search results.json.
                     If provided, exports best variant from grid search.
        variant_id: Optional variant ID to export (instead of best).
                   Must be valid variant ID if provided.
        best_variant_file: Optional path to best_dataset_variant.json.
                          Must exist if provided.
        model_dir: Optional path to just-trained model directory.
                  If provided, exports model from this location (e.g., after training).
        export_dir: Optional export directory (default: uses get_best_model_path()).
                   Parent directory will be created if it doesn't exist.
        
    Returns:
        None. Exports model checkpoint and metadata to export_dir.
        
    Raises:
        ValueError: If config is None, variant_id is invalid, or conflicting options provided.
        FileNotFoundError: If results_file, best_variant_file, or model checkpoint doesn't exist.
        RuntimeError: If export fails.
    """
    # 1. Validate and setup
    validate_pipeline_config(config, required_sections=['paths', 'model'])
    
    if variant_id is not None and not isinstance(variant_id, str):
        raise TypeError(f"variant_id must be string, got {type(variant_id)}")
    
    from utils.system import get_best_model_path
    export_path = Path(export_dir or get_best_model_path())
    
    # 2. Determine scenario and delegate to appropriate handler
    if model_dir:
        # Scenario: Just-trained model
        logger.info(f"📦 Exporting just-trained model from: {model_dir}")
        # Note: variant_id and variant_info are passed through for metadata completeness
        # but may not be available in all cases (e.g., training without results_file)
        source_path, metadata = handle_just_trained_model(
            model_dir, 
            config,
            variant_id=variant_id,
            variant_info=variant_info
        )
        
        # Use export_from_training_dir (supports fold structure)
        from modeling.utils.export.operations import export_from_training_dir
        model_dir_path = Path(model_dir)
        export_from_training_dir(
            model_dir=model_dir_path,
            export_dir=export_path,
            metadata=metadata
        )
        logger.info(f"   CV Score: {metadata['cv_score']:.4f}")
        logger.info(f"   Best Fold: {metadata['best_fold']} (score: {metadata['fold_scores'][metadata['best_fold']] if metadata['best_fold'] < len(metadata['fold_scores']) else 'N/A'})")
        return
        
    elif best_variant_file:
        # Scenario: Best variant file
        logger.info(f"📦 Exporting best variant from: {best_variant_file}")
        source_path, metadata = handle_best_variant_file(best_variant_file, config, export_path)
        # handle_best_variant_file already handled export, just validate
        results_path = Path(config.paths.output_dir) / 'dataset_grid_search' / 'gridsearch_results.json'
        if results_path.exists():
            variant_id_from_meta = metadata.get('variant_id', '')
            if variant_id_from_meta:
                _validate_exported_metadata(metadata, results_path, variant_id_from_meta)
        return
        
    elif results_file:
        # Scenario: Grid search results file
        logger.info(f"📦 Exporting variant from results: {results_file}")
        results_path = Path(results_file)
        source_path, metadata = handle_results_file(results_file, variant_id, config)
        
        # Delegate to export utility
        export_from_grid_search(
            variant_id=metadata.get('variant_id', ''),
            best_fold=metadata['best_fold'],
            export_dir=export_path,
            metadata=metadata,
            config=config
        )
        
        # Copy results.json if available
        if results_path.exists():
            copy_results_file(results_path, export_path / 'results.json')
        
        # Validate exported metadata matches source
        variant_id_used = metadata.get('variant_id', variant_id or '')
        if variant_id_used:
            _validate_exported_metadata(metadata, results_path, variant_id_used)
        
        logger.info(f"   Variant: {variant_id_used}")
        logger.info(f"   CV Score: {metadata['cv_score']:.4f}")
        logger.info(f"   Best Fold: {metadata['best_fold']} (score: {metadata.get('best_fold_score', 'N/A')})")
        return
        
    else:
        # Scenario: Auto-detect from CSIRO or working directory
        logger.info("🔄 Auto-detecting model from CSIRO models or working directory...")
        source_path, metadata = handle_auto_detect(config)
        
        # Use export_from_single_checkpoint (metadata is complete from handle_auto_detect)
        from modeling.utils.export.operations import export_from_single_checkpoint
        export_from_single_checkpoint(
            checkpoint_path=source_path,
            export_dir=export_path,
            metadata=metadata
        )
        logger.info(f"   CV Score: {metadata['cv_score']:.4f}")
        logger.info(f"   Best Fold: {metadata['best_fold']} (score: {metadata['fold_scores'][metadata['best_fold']] if metadata['best_fold'] < len(metadata['fold_scores']) else 'N/A'})")
        logger.info(f"   Source: {source_path}")
        return
