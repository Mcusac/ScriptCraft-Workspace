"""
Pipeline Steps Module

This module handles dynamic loading and configuration of pipeline steps from config.yaml.
"""

import importlib
from typing import Dict, List, Callable, Any, Optional
from pathlib import Path

import scripts.common as cu
from .base_pipeline import BasePipeline, PipelineStep


def import_function(import_path: str) -> Callable:
    """
    Dynamically imports a function from its string path.
    
    Args:
        import_path: Full dotted path to the function
    
    Returns:
        Callable function object
    """
    module_path, func_name = import_path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    return getattr(module, func_name)


def build_step(step_def: dict) -> PipelineStep:
    """
    Builds a pipeline step from a config dictionary.
    
    Args:
        step_def: Dictionary with step configuration
    
    Returns:
        PipelineStep object
    """
    # Handle dynamic lambda function if present
    if step_def.get("func") == "scripts.tools.data_content_comparer.tool.run_content_comparer":
        func = lambda **kwargs: import_function(step_def["func"])(
            mode="rhq_mode",
            input_dir="input",
            **kwargs
        )
    else:
        func = import_function(step_def["func"])
    
    return PipelineStep(
        name=step_def["name"],
        log_filename=step_def["log"],
        qc_func=func,
        input_key=step_def.get("input_key", "raw_data"),
        output_filename=step_def.get("output_filename"),
        check_exists=step_def.get("check_exists", False),
        run_mode=step_def.get("run_mode", "domain"),
        tags=step_def.get("tags", [])
    )


class PipelineFactory:
    """Factory class for creating pipelines from configuration."""
    
    def __init__(self):
        """Initialize the pipeline factory."""
        # Try the new Config class first, fall back to old get_config
        try:
            from scripts.common.core.config import Config
            config_obj = Config.from_yaml("config.yaml")
            self.config = {
                "pipelines": config_obj.pipelines,
                "pipeline_descriptions": getattr(config_obj, "pipeline_descriptions", {})
            }
        except Exception:
            # Fall back to old config system
            self.config = cu.get_config()
        
        self.pipeline_defs = self.config.get("pipelines", {})
        self.pipelines: Dict[str, BasePipeline] = {}
    
    def _build_pipeline(self, name: str, pipeline_config: Any) -> BasePipeline:
        """
        Build a pipeline from its configuration.
        
        Args:
            name: Name of the pipeline
            pipeline_config: Pipeline configuration (can be list or dict with description/steps)
        
        Returns:
            Configured BasePipeline object
        """
        # Create a mock config object for BasePipeline
        try:
            from scripts.common.core.config import Config
            config_obj = Config.from_yaml("config.yaml")
        except Exception:
            # Create a minimal config object
            class MockConfig:
                def __init__(self):
                    self.domains = cu.get_config("domains", [])
                    self.name = name
            config_obj = MockConfig()
        
        # Extract description and steps from new config format
        if isinstance(pipeline_config, dict) and "steps" in pipeline_config:
            description = pipeline_config.get("description")
            steps_or_refs = pipeline_config["steps"]
        else:
            # Legacy format - just a list of steps
            description = None
            steps_or_refs = pipeline_config
        
        pipeline = BasePipeline(config_obj, name=name, description=description)
        
        for item in steps_or_refs:
            if isinstance(item, dict):
                if "func" in item:
                    # Build actual step
                    pipeline.add_step(build_step(item))
                elif "ref" in item:
                    # It's a reference to another pipeline
                    ref_pipeline = self.pipelines.get(item["ref"])
                    if ref_pipeline:
                        for step in ref_pipeline.steps:
                            pipeline.add_step(step)
            else:
                # Legacy single string (like "full"), treat as ref
                ref_pipeline = self.pipelines.get(item)
                if ref_pipeline:
                    for step in ref_pipeline.steps:
                        pipeline.add_step(step)
        
        return pipeline
    
    def create_pipelines(self) -> Dict[str, BasePipeline]:
        """
        Create all pipelines defined in config.
        
        Returns:
            Dictionary mapping pipeline names to BasePipeline objects
        """
        # First pass: Create pipelines that don't have references
        for name, pipeline_config in self.pipeline_defs.items():
            # Extract steps from new config format
            if isinstance(pipeline_config, dict) and "steps" in pipeline_config:
                steps_list = pipeline_config["steps"]
            else:
                steps_list = pipeline_config
                
            if all(not isinstance(item, dict) or "func" in item for item in steps_list):
                self.pipelines[name] = self._build_pipeline(name, pipeline_config)
        
        # Second pass: Create pipelines with references
        for name, pipeline_config in self.pipeline_defs.items():
            if name not in self.pipelines:
                self.pipelines[name] = self._build_pipeline(name, pipeline_config)
        
        return self.pipelines


def get_pipeline_steps() -> Dict[str, List[PipelineStep]]:
    """
    Get all pipeline steps defined in config.yaml.
    
    Returns:
        Dictionary mapping pipeline names to lists of steps
    """
    factory = PipelineFactory()
    pipelines = factory.create_pipelines()
    return {name: pipeline.steps for name, pipeline in pipelines.items()}
