"""
scripts/pipelines/__init__.py

📦 Pipeline package for managing data processing workflows.

This package provides:
- Base pipeline classes and step definitions
- Pipeline execution and validation utilities
- Domain-specific pipeline implementations
- QC and logging integration
"""

from .base_pipeline import (
    BasePipeline,
    PipelineStep
)

from .pipeline_utils import (
    PipelineStep as PipelineStepTuple,  # Named tuple version
    make_step,
    validate_pipelines,
    add_supplement_steps,
    run_qc_for_each_domain,
    run_qc_for_single_domain,
    run_qc_single_step,
    run_global_tool,
    run_pipeline_from_steps,
    timed_pipeline,
    list_pipelines,
    preview_pipeline,
    run_pipeline
)

# Define what symbols to export
__all__ = [
    # Base Pipeline
    'BasePipeline',
    'PipelineStep',
    'PipelineStepTuple',
    
    # Pipeline Utilities
    'make_step',
    'validate_pipelines',
    'add_supplement_steps',
    'run_qc_for_each_domain',
    'run_qc_for_single_domain',
    'run_qc_single_step',
    'run_global_tool',
    'run_pipeline_from_steps',
    'timed_pipeline',
    'list_pipelines',
    'preview_pipeline',
    'run_pipeline'
]
