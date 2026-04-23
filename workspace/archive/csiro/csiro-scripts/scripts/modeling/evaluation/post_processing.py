# post_processing.py
# Post-processing functions for enforcing physical constraints on predictions
# 
# NOTE: The constraint logic in this file is contest-specific (CSIRO biomass competition).
# This module delegates to the contest abstraction for flexibility.
# CSIRO-SPECIFIC: This file provides the public API and delegates to contest abstraction

import numpy as np
import pandas as pd
from typing import Union, List, Optional
import logging
import warnings

logger = logging.getLogger(__name__)

# Import from contest abstraction
try:
    from contest.registry import get_contest_post_processor
    _get_post_processor = get_contest_post_processor
except (ImportError, ValueError) as e:
    # Fallback to direct CSIRO import if registry not available
    warnings.warn(
        f"Could not load contest post-processor from registry: {e}. "
        f"Falling back to direct CSIRO import.",
        UserWarning
    )
    from contest.csiro.post_processing import get_csiro_post_processor
    _get_post_processor = get_csiro_post_processor


# CSIRO-SPECIFIC: Public API function that delegates to contest abstraction
def post_process_biomass(
    predictions: Union[pd.DataFrame, np.ndarray],
    target_cols: Optional[List[str]] = None
) -> pd.DataFrame:
    """
    Post-process biomass predictions to enforce physical constraints.
    
    Enforces contest-specific physical constraints defined by the contest configuration.
    For CSIRO biomass competition:
    1. GDM_g = Dry_Green_g + Dry_Clover_g
    2. Dry_Total_g = GDM_g + Dry_Dead_g
    
    Uses matrix projection to find the closest valid solution that satisfies
    these constraints, even if the model predictions are inconsistent.
    
    This function now delegates to the contest post-processor abstraction.
    
    Args:
        predictions: Predictions to post-process. Can be:
                    - DataFrame with target columns
                    - NumPy array of shape (N, num_total_targets) with columns in target_order
        target_cols: List of target column names in order. If None, uses target_order from config.
                    Must match the order expected by constraint matrix.
    
    Returns:
        DataFrame with post-processed predictions that satisfy physical constraints.
        All values are clipped to be non-negative.
    
    Raises:
        ValueError: If predictions format is invalid or missing required columns.
    """
    processor = _get_post_processor()
    return processor.post_process(predictions, target_cols)

