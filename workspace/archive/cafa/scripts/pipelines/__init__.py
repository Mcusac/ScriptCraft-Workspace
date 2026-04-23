"""
Pipeline orchestration for CAFA 6 protein function prediction.
Contains high-level pipeline functions for different workflows.
"""

from .pipeline_orchestrator import (
    run_full_pipeline,
    run_train_all,
    run_train_single_ontology,
    run_predict_from_saved
)

__all__ = [
    'run_full_pipeline',
    'run_train_all',
    'run_train_single_ontology',
    'run_predict_from_saved'
]
