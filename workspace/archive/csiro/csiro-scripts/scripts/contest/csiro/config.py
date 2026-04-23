# contest/csiro/config.py
# CSIRO biomass competition configuration

from typing import Dict, List
import numpy as np
from contest.base import ContestConfig


class CSIROConfig(ContestConfig):
    """
    CSIRO biomass competition configuration.
    
    Defines target names, weights, and derived target computation for the
    CSIRO biomass prediction competition.
    """
    
    @property
    def target_weights(self) -> Dict[str, float]:
        """CSIRO target weights for weighted R² calculation."""
        return {
            'Dry_Green_g': 0.1,
            'Dry_Dead_g': 0.1,
            'Dry_Clover_g': 0.1,
            'GDM_g': 0.2,
            'Dry_Total_g': 0.5
        }
    
    @property
    def target_order(self) -> List[str]:
        """CSIRO target order (must match target_weights keys)."""
        return ['Dry_Green_g', 'Dry_Clover_g', 'Dry_Dead_g', 'GDM_g', 'Dry_Total_g']
    
    @property
    def primary_targets(self) -> List[str]:
        """CSIRO primary targets (model outputs 3 values)."""
        return ['Dry_Green_g', 'Dry_Clover_g', 'Dry_Dead_g']
    
    @property
    def derived_targets(self) -> List[str]:
        """CSIRO derived targets (computed from primary targets)."""
        return ['GDM_g', 'Dry_Total_g']
    
    @property
    def all_targets(self) -> List[str]:
        """CSIRO all targets (primary + derived)."""
        return self.primary_targets + self.derived_targets
    
    @property
    def num_primary_targets(self) -> int:
        """CSIRO number of primary targets."""
        return 3
    
    @property
    def num_total_targets(self) -> int:
        """CSIRO total number of targets."""
        return 5
    
    @property
    def constraint_matrix(self) -> np.ndarray:
        """
        CSIRO constraint matrix for post-processing.
        
        Defines constraints:
        - GDM_g = Dry_Green_g + Dry_Clover_g
        - Dry_Total_g = GDM_g + Dry_Dead_g
        
        Order: [Dry_Green_g, Dry_Clover_g, Dry_Dead_g, GDM_g, Dry_Total_g]
        """
        return np.array([
            [-1, -1,  0,  1,  0],  # GDM_g = Dry_Green_g + Dry_Clover_g
            [ 0,  0, -1, -1,  1]   # Dry_Total_g = GDM_g + Dry_Dead_g
        ], dtype=float)
    
    def compute_derived_target_values(self, green: float, clover: float, dead: float) -> Dict[str, float]:
        """
        Compute CSIRO derived target values from primary target values.
        
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
        return {
            'Dry_Green_g': green,
            'Dry_Clover_g': clover,
            'Dry_Dead_g': dead,
            'GDM_g': green + clover,
            'Dry_Total_g': green + clover + dead
        }


# Singleton instance for easy access
_csiro_config_instance: CSIROConfig = None


def get_csiro_config() -> CSIROConfig:
    """Get singleton CSIRO config instance."""
    global _csiro_config_instance
    if _csiro_config_instance is None:
        _csiro_config_instance = CSIROConfig()
    return _csiro_config_instance
