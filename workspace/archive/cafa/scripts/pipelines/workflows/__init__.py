"""
Workflow modules for CAFA 6 pipeline.
Each module handles a focused workflow responsibility.
"""

from pipelines.workflows.full_pipeline import run_full_pipeline
from pipelines.workflows.training import run_train_all, run_train_single_ontology
from pipelines.workflows.prediction import run_predict_from_saved

__all__ = [
    'run_full_pipeline',
    'run_train_all',
    'run_train_single_ontology',
    'run_predict_from_saved'
]
