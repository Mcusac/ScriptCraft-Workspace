# evaluation_constants.py
# Evaluation constants for metrics and target definitions
# 
# This module contains evaluation-related constants that are used by both
# config and modeling packages. By placing them in config, we ensure they
# are at a lower level in the dependency hierarchy than modeling, preventing
# circular imports.
#
# TARGET_WEIGHTS is the primary constant used by config.config.EvaluationConfig
# for default target weights in weighted R² calculation.
#
# NOTE: These constants are contest-specific (CSIRO biomass competition).
# This module imports from contest.csiro.config for abstraction.
# Constants are re-exported here as part of the abstraction layer design.

from typing import Dict, List
import numpy as np
import warnings

# Import from contest abstraction (defaults to CSIRO)
try:
    from contest.registry import get_contest_config
    _contest_config = get_contest_config()
except (ImportError, ValueError) as e:
    # Fallback to direct CSIRO import if registry not available
    warnings.warn(
        f"Could not load contest config from registry: {e}. "
        f"Falling back to direct CSIRO import.",
        UserWarning
    )
    from contest.csiro.config import get_csiro_config
    _contest_config = get_csiro_config()

# Re-export constants from contest config as part of abstraction layer
# CSIRO-SPECIFIC: These values come from CSIRO contest config
TARGET_WEIGHTS: Dict[str, float] = _contest_config.target_weights
TARGET_ORDER: List[str] = _contest_config.target_order
PRIMARY_TARGETS: List[str] = _contest_config.primary_targets
DERIVED_TARGETS: List[str] = _contest_config.derived_targets
ALL_TARGETS: List[str] = _contest_config.all_targets
NUM_PRIMARY_TARGETS: int = _contest_config.num_primary_targets
NUM_TOTAL_TARGETS: int = _contest_config.num_total_targets
CONSTRAINT_MATRIX: np.ndarray = _contest_config.constraint_matrix


# CSIRO-SPECIFIC: Function to compute derived target values
# Delegates to contest config as part of abstraction layer
def compute_derived_target_values(green: float, clover: float, dead: float) -> Dict[str, float]:
    """
    Compute derived target values from primary target values.
    
    Contest-specific function for CSIRO biomass competition.
    This function now delegates to the contest config abstraction.
    
    Args:
        green: Dry_Green_g value
        clover: Dry_Clover_g value
        dead: Dry_Dead_g value
        
    Returns:
        Dictionary mapping all target names to their values:
        - Dry_Green_g, Dry_Clover_g, Dry_Dead_g (primary)
        - GDM_g (green + clover)
        - Dry_Total_g (green + clover + dead)
    """
    return _contest_config.compute_derived_target_values(green, clover, dead)
