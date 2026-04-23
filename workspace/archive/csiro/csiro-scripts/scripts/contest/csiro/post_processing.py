# contest/csiro/post_processing.py
# CSIRO biomass competition post-processing

import numpy as np
import pandas as pd
from typing import Union, List, Optional
import logging

from contest.base import ContestPostProcessor
from contest.csiro.config import get_csiro_config

logger = logging.getLogger(__name__)


class CSIROPostProcessor(ContestPostProcessor):
    """
    CSIRO biomass competition post-processor.
    
    Enforces physical constraints on predictions:
    1. GDM_g = Dry_Green_g + Dry_Clover_g
    2. Dry_Total_g = GDM_g + Dry_Dead_g
    
    Uses matrix projection to find the closest valid solution.
    """
    
    def __init__(self):
        """Initialize CSIRO post-processor with config."""
        self.config = get_csiro_config()
    
    def post_process(
        self,
        predictions: Union[pd.DataFrame, np.ndarray],
        target_cols: Optional[List[str]] = None
    ) -> pd.DataFrame:
        """
        Post-process CSIRO biomass predictions to enforce physical constraints.
        
        Enforces contest-specific physical constraints defined by constraint matrix.
        Uses matrix projection to find the closest valid solution that satisfies
        these constraints, even if the model predictions are inconsistent.
        
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
        if target_cols is None:
            target_cols = self.config.target_order.copy()
        
        # Convert to DataFrame if needed
        if isinstance(predictions, np.ndarray):
            if predictions.ndim != 2 or predictions.shape[1] != self.config.num_total_targets:
                raise ValueError(
                    f"Predictions array must be 2D with {self.config.num_total_targets} columns, "
                    f"got shape {predictions.shape}"
                )
            df_preds = pd.DataFrame(predictions, columns=target_cols)
        elif isinstance(predictions, pd.DataFrame):
            df_preds = predictions.copy()
            
            # Verify all required columns exist
            missing_cols = set(target_cols) - set(df_preds.columns)
            if missing_cols:
                raise ValueError(
                    f"Missing required columns in predictions: {missing_cols}. "
                    f"Required: {target_cols}"
                )
        else:
            raise ValueError(
                f"predictions must be DataFrame or numpy array, got {type(predictions)}"
            )
        
        # Ensure columns are in correct order
        if not all(col in df_preds.columns for col in target_cols):
            return df_preds  # Can't process if columns missing
        
        # Extract values in correct order
        Y = df_preds[target_cols].values.T  # Shape: (num_total_targets, N)
        
        # Use constraint matrix from config
        # Constraint matrix defines: C @ Y = 0 where C is the constraint matrix
        C = self.config.constraint_matrix
        
        # Project onto constraint subspace
        # Find Y_reconciled such that C @ Y_reconciled = 0 and minimizes ||Y_reconciled - Y||
        try:
            # Compute projection matrix: P = I - C^T @ (C @ C^T)^(-1) @ C
            CCt = C @ C.T
            inv_CCt = np.linalg.inv(CCt)
            P = np.eye(self.config.num_total_targets) - C.T @ inv_CCt @ C
            
            # Project: Y_reconciled = P @ Y
            Y_reconciled = (P @ Y).T  # Shape: (N, num_total_targets)
            
        except np.linalg.LinAlgError:
            # Fallback to pseudo-inverse if matrix is singular
            logger.warning("Constraint matrix is singular, using pseudo-inverse")
            CCt = C @ C.T
            inv_CCt = np.linalg.pinv(CCt)
            P = np.eye(self.config.num_total_targets) - C.T @ inv_CCt @ C
            Y_reconciled = (P @ Y).T
        
        # Clip to non-negative (biomass cannot be negative)
        Y_reconciled = np.clip(Y_reconciled, 0, None)
        
        # Create output DataFrame
        df_out = df_preds.copy()
        df_out[target_cols] = Y_reconciled
        
        # Additional simple corrections to ensure consistency
        # (in case projection didn't perfectly satisfy constraints due to clipping)
        if 'GDM_g' in df_out.columns and 'Dry_Green_g' in df_out.columns and 'Dry_Clover_g' in df_out.columns:
            df_out['GDM_g'] = df_out['Dry_Green_g'] + df_out['Dry_Clover_g']
        if 'Dry_Total_g' in df_out.columns and 'GDM_g' in df_out.columns and 'Dry_Dead_g' in df_out.columns:
            df_out['Dry_Total_g'] = df_out['GDM_g'] + df_out['Dry_Dead_g']
        
        # Final clip to ensure non-negative
        for col in target_cols:
            df_out[col] = df_out[col].clip(lower=0)
        
        return df_out


# Singleton instance for easy access
_csiro_post_processor_instance: CSIROPostProcessor = None


def get_csiro_post_processor() -> CSIROPostProcessor:
    """Get singleton CSIRO post-processor instance."""
    global _csiro_post_processor_instance
    if _csiro_post_processor_instance is None:
        _csiro_post_processor_instance = CSIROPostProcessor()
    return _csiro_post_processor_instance
