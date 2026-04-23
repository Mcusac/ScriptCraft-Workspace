"""
Training workflow modules for CAFA 6 protein function prediction.
Refactored for SOLID principles with focused, single-responsibility modules.
"""

from pipelines.workflows.training.training_orchestrator import (
    run_train_all,
    run_train_single_ontology,
    run_train_parallel_ontologies
)

__all__ = [
    'run_train_all',
    'run_train_single_ontology',
    'run_train_parallel_ontologies'
]

