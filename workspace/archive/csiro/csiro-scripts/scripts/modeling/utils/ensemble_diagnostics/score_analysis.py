# score_analysis.py
# Score comparison and analysis functions for ensemble diagnostics

import logging
from pathlib import Path
from typing import Dict, List, Optional
import numpy as np

logger = logging.getLogger(__name__)


def load_cv_scores_from_paths(model_paths: List[str]) -> Dict[str, Optional[float]]:
    """
    Load CV scores from model metadata for each model path.
    
    Args:
        model_paths: List of model base paths (directories containing model_metadata.json)
        
    Returns:
        Dictionary mapping model_path -> cv_score (or None if not found)
    """
    cv_scores = {}
    
    for model_path in model_paths:
        base_path = Path(model_path)
        metadata_file = base_path / 'model_metadata.json'
        
        cv_score = None
        if metadata_file.exists():
            try:
                from utils.system.io import load_json_file
                metadata = load_json_file(metadata_file, expected_type=dict, file_type="Model metadata")
                cv_score = metadata.get('cv_score')
            except (FileNotFoundError, PermissionError, OSError) as e:
                # File system errors - log and continue
                logger.warning(f"Could not load CV score from {metadata_file}: {e}")
            except (KeyError, TypeError, ValueError) as e:
                # Data format errors - log and continue
                logger.warning(f"Invalid CV score format in {metadata_file}: {e}")
            except Exception as e:
                # Catch any other unexpected errors
                logger.warning(f"Unexpected error loading CV score from {metadata_file}: {e}", exc_info=True)
        
        cv_scores[model_path] = cv_score
    
    return cv_scores


def compare_cv_submission_scores(
    cv_scores: Dict[str, Optional[float]],
    submission_scores: Optional[Dict[str, float]] = None
) -> Dict[str, any]:
    """
    Compare CV scores with submission scores to identify generalization gaps.
    
    Args:
        cv_scores: Dictionary mapping model_path -> cv_score
        submission_scores: Optional dictionary mapping model_path -> submission_score
        
    Returns:
        Dictionary with comparison metrics:
        - model_comparisons: List of dicts with model_path, cv_score, submission_score, gap
        - correlation: Pearson correlation between CV and submission scores (if both available)
        - avg_gap: Average gap between CV and submission scores
        - models_with_poor_generalization: List of models with large negative gaps
    """
    if not submission_scores:
        return {
            'model_comparisons': [],
            'correlation': None,
            'avg_gap': None,
            'models_with_poor_generalization': []
        }
    
    comparisons = []
    cv_values = []
    sub_values = []
    
    # Get all unique model paths
    all_paths = set(cv_scores.keys()) | set(submission_scores.keys())
    
    for model_path in all_paths:
        cv_score = cv_scores.get(model_path)
        sub_score = submission_scores.get(model_path)
        
        gap = None
        if cv_score is not None and sub_score is not None:
            gap = sub_score - cv_score
            cv_values.append(cv_score)
            sub_values.append(sub_score)
        
        comparisons.append({
            'model_path': model_path,
            'cv_score': cv_score,
            'submission_score': sub_score,
            'gap': gap
        })
    
    # Calculate correlation if we have both scores
    correlation = None
    if len(cv_values) >= 2:
        try:
            correlation = float(np.corrcoef(cv_values, sub_values)[0, 1])
        except (ValueError, IndexError, TypeError) as e:
            # Handle cases where correlation calculation fails (e.g., constant values, wrong array shape)
            logger.debug(f"Could not calculate correlation: {e}")
        except Exception as e:
            # Catch any other unexpected errors
            logger.debug(f"Unexpected error calculating correlation: {e}", exc_info=True)
    
    # Calculate average gap
    gaps = [c['gap'] for c in comparisons if c['gap'] is not None]
    avg_gap = float(np.mean(gaps)) if gaps else None
    
    # Identify models with poor generalization (large negative gaps)
    poor_generalization = [
        c for c in comparisons
        if c['gap'] is not None and c['gap'] < -0.1  # Threshold: submission score 0.1 worse than CV
    ]
    
    return {
        'model_comparisons': comparisons,
        'correlation': correlation,
        'avg_gap': avg_gap,
        'models_with_poor_generalization': poor_generalization
    }

