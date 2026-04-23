"""
Pipeline configurations for CAFA 6 protein function prediction.
"""

# Pipeline Configurations
PIPELINE_CONFIGS = {
    "full_pipeline": {
        "name": "Full Pipeline",
        "description": "End-to-end: data prep → train all → predict → submit",
        "workflow_module": "pipelines.workflows.full_pipeline",
        "workflow_function": "run_full_pipeline"
    },
    "train_only": {
        "name": "Training Pipeline", 
        "description": "Train models for all ontologies",
        "workflow_module": "pipelines.workflows.training",
        "workflow_function": "run_training_pipeline"
    },
    "train_single_ont": {
        "name": "Single Ontology Training",
        "description": "Train model for one ontology only",
        "workflow_module": "pipelines.workflows.training",
        "workflow_function": "run_train_single_ontology"
    },
    "predict_from_saved": {
        "name": "Prediction Pipeline",
        "description": "Load models → predict → generate submission",
        "workflow_module": "pipelines.workflows.prediction", 
        "workflow_function": "run_prediction_pipeline"
    },
    "grid_search": {
        "name": "Grid Search Pipeline",
        "description": "Hyperparameter tuning via grid search",
        "workflow_module": "pipelines.workflows.grid_search",
        "workflow_function": "run_grid_search_pipeline"
    },
    "ensemble": {
        "name": "Ensemble Pipeline",
        "description": "Ensemble predictions from multiple models",
        "workflow_module": "pipelines.workflows.ensemble",
        "workflow_function": "run_ensemble_prediction"
    },
    "average_submissions": {
        "name": "Submission Averaging",
        "description": "Average multiple submission files",
        "workflow_module": "pipelines.workflows.submission_averaging",
        "workflow_function": "run_submission_averaging"
    },
    "get_all_averages": {
        "name": "Get All Averages",
        "description": "Generate all 7 ensemble method submissions in one run",
        "workflow_module": "pipelines.workflows.get_all_averages",
        "workflow_function": "run_get_all_averages"
    }
}


def get_pipeline_config(pipeline_name):
    """Get pipeline configuration."""
    if pipeline_name not in PIPELINE_CONFIGS:
        raise ValueError(f"Unknown pipeline: {pipeline_name}. Available: {list(PIPELINE_CONFIGS.keys())}")
    
    return PIPELINE_CONFIGS[pipeline_name]
