# progress_config.py
# Progress tracking configuration

import os
from dataclasses import dataclass


class ProgressVerbosity:
    """Verbosity levels for progress tracking"""
    SILENT = 0      # No progress output
    MINIMAL = 1     # Basic progress bars only
    MODERATE = 2    # Progress + time estimates + key metrics
    DETAILED = 3    # Everything + memory + throughput
    DEBUG = 4       # Maximum detail for debugging


@dataclass
class ProgressConfig:
    """Configuration for progress tracking system"""
    verbosity: int = None  # Will be set from env or default
    show_epoch_progress: bool = True
    show_batch_progress: bool = False  # Usually too verbose
    show_data_loading: bool = True
    show_memory_stats: bool = True
    refresh_rate: float = 0.5  # seconds between progress bar updates
    
    def __post_init__(self):
        """Validate and set defaults from environment variables"""
        # Check environment variables
        env_verbosity = os.environ.get('CSIRO_PROGRESS_VERBOSITY')
        if env_verbosity is not None:
            try:
                self.verbosity = int(env_verbosity)
            except ValueError:
                # Map string names to verbosity levels
                verbosity_map = {
                    'silent': ProgressVerbosity.SILENT,
                    'minimal': ProgressVerbosity.MINIMAL,
                    'moderate': ProgressVerbosity.MODERATE,
                    'detailed': ProgressVerbosity.DETAILED,
                    'debug': ProgressVerbosity.DEBUG
                }
                self.verbosity = verbosity_map.get(env_verbosity.lower(), ProgressVerbosity.MODERATE)
        
        # Set default if not set
        if self.verbosity is None:
            self.verbosity = ProgressVerbosity.MODERATE
        
        # Check if progress is completely disabled
        if os.environ.get('CSIRO_PROGRESS_DISABLE', '').lower() in ('1', 'true', 'yes'):
            self.verbosity = ProgressVerbosity.SILENT
        
        # Validate verbosity level
        if not (ProgressVerbosity.SILENT <= self.verbosity <= ProgressVerbosity.DEBUG):
            raise ValueError(
                f"verbosity must be between {ProgressVerbosity.SILENT} and "
                f"{ProgressVerbosity.DEBUG}, got {self.verbosity}"
            )
        
        if self.refresh_rate <= 0:
            raise ValueError(f"refresh_rate must be positive, got {self.refresh_rate}")

