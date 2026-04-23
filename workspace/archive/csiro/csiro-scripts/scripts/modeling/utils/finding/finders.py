# finders.py
# Context classes that combine strategies for specific use cases

import logging
from pathlib import Path
from typing import Optional, Tuple

from config.config import Config
from .strategies import (
    KaggleInputStrategy,
    GridSearchStrategy,
    HyperparameterGridSearchStrategy,
    CSIROModelsStrategy,
    WorkingDirectoryStrategy
)

logger = logging.getLogger(__name__)


class GridSearchModelFinder:
    """
    Context class for finding models for grid search variants.
    
    Uses a combination of strategies:
    1. KaggleInputStrategy: Check uploaded datasets
    2. HyperparameterGridSearchStrategy: Check hyperparameter grid search structure (combo_XXXX)
    3. GridSearchStrategy: Check dataset grid search structure (variant_XXXX)
    """
    
    def __init__(self):
        """Initialize finder with appropriate strategies."""
        self.kaggle_input_strategy = KaggleInputStrategy()
        self.hyperparameter_grid_search_strategy = HyperparameterGridSearchStrategy()
        self.grid_search_strategy = GridSearchStrategy()
    
    def find_model(
        self,
        variant_id: str,
        best_fold: int,
        config: Config
    ) -> Path:
        """
        Find model checkpoint for a grid search variant.
        
        Searches in multiple locations:
        1. Kaggle input datasets (/kaggle/input/*/best_model/best_model.pth)
        2. Hyperparameter grid search structure (hyperparameter_grid_search/combo_XXXX/)
        3. Dataset grid search structure (dataset_grid_search/variant_XXXX/)
        
        Args:
            variant_id: Variant ID (e.g., "variant_0067" or "combo_0000")
            best_fold: Best fold number
            config: Configuration object with paths
            
        Returns:
            Path to model checkpoint
            
        Raises:
            FileNotFoundError: If model checkpoint cannot be found in any location
        """
        # 1. Check in input datasets (from uploaded best_model folder)
        model_path = self.kaggle_input_strategy.find_model(
            variant_id=variant_id,
            best_fold=best_fold
        )
        
        # 2. Check hyperparameter grid search structure (for combo_XXXX)
        if model_path is None or not model_path.exists():
            model_path = self.hyperparameter_grid_search_strategy.find_model(
                variant_id=variant_id,
                best_fold=best_fold,
                config=config
            )
        
        # 3. Fallback to dataset grid search structure (for variant_XXXX)
        if model_path is None or not model_path.exists():
            model_path = self.grid_search_strategy.find_model(
                variant_id=variant_id,
                best_fold=best_fold,
                config=config
            )
        
        if model_path is None or not model_path.exists():
            from config.path_constants import KAGGLE_INPUT, BEST_MODEL_DIR_NAME, BEST_MODEL_FILE_NAME
            
            error_msg = (
                f"Model checkpoint not found for variant {variant_id}, fold {best_fold}.\n"
                f"Searched locations:\n"
                f"  - {KAGGLE_INPUT}/*/{BEST_MODEL_DIR_NAME}/{BEST_MODEL_FILE_NAME} (from uploaded dataset)\n"
                f"  - {Path(config.paths.model_dir) / 'hyperparameter_grid_search' / variant_id / f'fold_{best_fold}' / BEST_MODEL_FILE_NAME} (hyperparameter grid search structure)\n"
                f"  - {Path(config.paths.model_dir) / 'dataset_grid_search' / variant_id / f'fold_{best_fold}' / BEST_MODEL_FILE_NAME} (dataset grid search structure)\n"
                f"\nOptions:\n"
                f"  1. Run export_model pipeline to prepare best model for download, then upload as dataset\n"
                f"  2. Make sure grid search completed and model exists in working directory"
            )
            raise FileNotFoundError(error_msg)
        
        return model_path


class LightweightSubmissionModelFinder:
    """
    Context class for finding models for lightweight submission pipeline.
    
    Uses a combination of strategies:
    1. Explicit path (if provided)
    2. CSIROModelsStrategy: Check csiro-models dataset
    3. WorkingDirectoryStrategy: Check working directory
    """
    
    def __init__(self):
        """Initialize finder with appropriate strategies."""
        self.csiro_models_strategy = CSIROModelsStrategy()
        self.working_directory_strategy = WorkingDirectoryStrategy()
    
    def _validate_model_path(self, found_model_path: Path) -> None:
        """
        Validate that found_model_path is a valid file (not a directory).
        
        Args:
            found_model_path: Path to validate
            
        Raises:
            ValueError: If path is a directory
            FileNotFoundError: If path is not a valid file
        """
        if found_model_path.is_dir():
            raise ValueError(
                f"Internal error: find_model returned a directory instead of a file.\n"
                f"Path: {found_model_path}\n"
                f"Finder class: {self.__class__.__name__}\n"
                f"Model path: {model_path}\n"
                f"This indicates a bug in the model finder logic. Please report this issue."
            )
        
        if not found_model_path.is_file():
            raise FileNotFoundError(
                f"Model path is not a valid file: {found_model_path}\n"
                f"Expected a checkpoint file (.pth or .pkl), but got: {found_model_path}"
            )
    
    def find_model(
        self,
        model_path: Optional[str],
        config: Config,
        model_name: Optional[str] = None
    ) -> Tuple[Path, Optional[Path]]:
        """
        Find model checkpoint for lightweight submission pipeline.
        
        Searches in multiple locations:
        1. Explicit model_path if provided
        2. csiro-models Kaggle dataset (model-specific or default)
        3. Working directory
        
        Args:
            model_path: Optional explicit model path
            config: Configuration object with paths
            model_name: Optional model name for model-specific folder structure
            
        Returns:
            Tuple of (model_path, metadata_path):
            - model_path: Path to model checkpoint
            - metadata_path: Path to model_metadata.json if found, None otherwise
            
        Raises:
            FileNotFoundError: If model checkpoint cannot be found in any location
        """
        found_model_path = None
        found_metadata_path = None
        
        # Track all locations that were actually checked
        checked_locations = []
        
        if model_path:
            # Use explicit path
            logger.info(f"🔍 Checking explicit model path: {model_path}")
            found_model_path = Path(model_path)
            checked_locations.append((str(found_model_path), found_model_path.exists()))
            
            if not found_model_path.exists():
                raise FileNotFoundError(f"Model path not found: {found_model_path}")
            
            from config.path_constants import BEST_MODEL_FILE_NAME, REGRESSION_MODEL_FILE_NAME, METADATA_FILE_NAME
            
            # If path is a directory, look for checkpoint file inside it
            if found_model_path.is_dir():
                # Prefer best_model.pth (most common checkpoint name)
                best_model_path = found_model_path / BEST_MODEL_FILE_NAME
                checked_locations.append((str(best_model_path), best_model_path.exists()))
                
                if best_model_path.exists():
                    found_model_path = best_model_path
                else:
                    # Check for regression model (feature extraction mode)
                    regression_model_path = found_model_path / REGRESSION_MODEL_FILE_NAME
                    checked_locations.append((str(regression_model_path), regression_model_path.exists()))
                    
                    if regression_model_path.exists():
                        found_model_path = regression_model_path
                        logger.info(f"Using regression model file: {found_model_path}")
                    else:
                        # Look for any .pth files in the directory
                        pth_files = list(found_model_path.glob('*.pth'))
                        if pth_files:
                            found_model_path = pth_files[0]
                            logger.info(f"Using checkpoint file: {found_model_path}")
                        else:
                            # Look for any .pkl files in the directory
                            pkl_files = list(found_model_path.glob('*.pkl'))
                            if pkl_files:
                                found_model_path = pkl_files[0]
                                logger.info(f"Using regression model file: {found_model_path}")
                            else:
                                raise FileNotFoundError(
                                    f"Model path is a directory but no checkpoint file found: {Path(model_path)}\n"
                                    f"Expected files: best_model.pth, regression_model.pkl, or any .pth/.pkl file\n"
                                    f"Directory contents: {list(found_model_path.iterdir())}"
                                )
                
                # Look for metadata in the same directory (parent of the checkpoint file)
                metadata_candidate = found_model_path.parent / METADATA_FILE_NAME
                if metadata_candidate.exists():
                    found_metadata_path = metadata_candidate
            
            # Explicit validation: ensure we never return a directory path
            self._validate_model_path(found_model_path)
            
            return found_model_path, found_metadata_path
        
        # Search for model in csiro-models with new path structure
        logger.info(f"🔍 Strategy 1: Checking csiro-models dataset")
        found_model_path, found_metadata_path = self.csiro_models_strategy.find_model(model_name=model_name)
        if found_model_path:
            checked_locations.append((str(found_model_path), True))
        else:
            # Track that we checked csiro-models (even though we don't have exact paths)
            from config.path_constants import KAGGLE_INPUT
            if model_name:
                csiro_base = KAGGLE_INPUT / 'csiro-models' / 'pytorch' / model_name
            else:
                from config.path_constants import KAGGLE_INPUT_CSIRO_MODELS
                csiro_base = KAGGLE_INPUT_CSIRO_MODELS
            checked_locations.append((f"{csiro_base}/*/best_model.pth or regression_model.pkl", False))
        
        # Fallback to working directory
        if found_model_path is None or not found_model_path.exists():
            logger.info(f"🔍 Strategy 2: Checking working directory")
            from utils.system.io import get_best_model_path
            from config.path_constants import BEST_MODEL_FILE_NAME, REGRESSION_MODEL_FILE_NAME
            
            best_model_dir = Path(get_best_model_path())
            working_model = best_model_dir / BEST_MODEL_FILE_NAME
            working_regression_model = best_model_dir / REGRESSION_MODEL_FILE_NAME
            
            checked_locations.append((str(working_model), working_model.exists()))
            checked_locations.append((str(working_regression_model), working_regression_model.exists()))
            
            found_model_path, found_metadata_path = self.working_directory_strategy.find_model(config=config)
        
        if found_model_path is None or not found_model_path.exists():
            # Build error message from actual checked locations
            error_lines = ["Model checkpoint not found.", "Searched locations:"]
            for location_path, exists in checked_locations:
                status = "✅ exists" if exists else "❌ not found"
                error_lines.append(f"  - {location_path} ({status})")
            
            error_lines.append("")
            error_lines.append("Options:")
            error_lines.append(f"  1. Upload model as csiro-models Kaggle dataset with structure: pytorch/{model_name or 'default'}/{{version}}/best_model.pth or regression_model.pkl")
            error_lines.append("  2. Make sure model_metadata.json is included in the same version directory")
            
            error_msg = "\n".join(error_lines)
            raise FileNotFoundError(error_msg)
        
        # Final validation: ensure we never return a directory path
        self._validate_model_path(found_model_path)
        
        return found_model_path, found_metadata_path

