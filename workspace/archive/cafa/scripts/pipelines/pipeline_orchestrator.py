"""
Pipeline orchestrator for CAFA 6 protein function prediction.
Thin orchestration layer that routes to focused workflow modules.
"""

import sys
from pathlib import Path

# Ensure scripts directory is in path for absolute imports
scripts_dir = str(Path(__file__).parent.parent)
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

# Import focused workflow modules
from pipelines.workflows.full_pipeline import run_full_pipeline
from pipelines.workflows.training import run_train_all, run_train_single_ontology, run_train_parallel_ontologies
from pipelines.workflows.prediction import run_predict_from_saved
from pipelines.workflows.grid_search import run_grid_search_pipeline

__all__ = [
    'run_full_pipeline',
    'run_train_all',
    'run_train_single_ontology',
    'run_train_parallel_ontologies',
    'run_predict_from_saved',
    'run_grid_search_pipeline'
]
