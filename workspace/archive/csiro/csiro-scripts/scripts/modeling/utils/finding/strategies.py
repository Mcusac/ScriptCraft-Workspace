# strategies.py
# Concrete strategy implementations for finding models in various locations

import logging
from pathlib import Path
from typing import Optional, Tuple

from utils.system.io import is_kaggle_environment
from config.config import Config
from .base import ModelLocationStrategy

logger = logging.getLogger(__name__)


class KaggleInputStrategy(ModelLocationStrategy):
    """
    Strategy for finding models in Kaggle input datasets.
    
    Searches for models in /kaggle/input/*/best_model/best_model.pth.
    Used when models are uploaded as Kaggle datasets.
    """
    
    def find_model(self, variant_id: Optional[str] = None, best_fold: Optional[int] = None, **kwargs) -> Optional[Path]:
        """
        Find model checkpoint in Kaggle input datasets.
        
        Args:
            variant_id: Optional variant ID (not used in search, but for logging)
            best_fold: Optional fold number (not used in search, but for logging)
            **kwargs: Additional unused arguments
            
        Returns:
            Path to model checkpoint if found, None otherwise
        """
        if not is_kaggle_environment():
            return None
        
        from config.path_constants import KAGGLE_INPUT, BEST_MODEL_DIR_NAME, BEST_MODEL_FILE_NAME
        
        input_base = KAGGLE_INPUT
        if not input_base.exists():
            return None
        
        for dataset_dir in input_base.iterdir():
            if dataset_dir.is_dir():
                potential_model = dataset_dir / BEST_MODEL_DIR_NAME / BEST_MODEL_FILE_NAME
                if potential_model.exists():
                    logger.info(f"Found model in input dataset: {potential_model}")
                    return potential_model
        
        return None


class GridSearchStrategy(ModelLocationStrategy):
    """
    Strategy for finding models in grid search directory structure.
    
    Searches for models in: {model_dir}/dataset_grid_search/{variant_id}/fold_{best_fold}/best_model.pth
    """
    
    def find_model(self, variant_id: str, best_fold: int, config: Config, **kwargs) -> Optional[Path]:
        """
        Find model checkpoint in grid search directory structure.
        
        Args:
            variant_id: Variant ID (e.g., "variant_0067")
            best_fold: Best fold number
            config: Configuration object with paths.model_dir
            **kwargs: Additional unused arguments
            
        Returns:
            Path to model checkpoint if found, None otherwise
        """
        from config.path_constants import BEST_MODEL_FILE_NAME
        model_path = Path(config.paths.model_dir) / 'dataset_grid_search' / variant_id / f'fold_{best_fold}' / BEST_MODEL_FILE_NAME
        
        if model_path.exists():
            logger.info(f"Found model in grid search structure: {model_path}")
            return model_path
        
        return None


class HyperparameterGridSearchStrategy(ModelLocationStrategy):
    """
    Strategy for finding models in hyperparameter grid search directory structure.
    
    Searches for models in: {model_dir}/hyperparameter_grid_search/{combo_id}/fold_{best_fold}/best_model.pth
    """
    
    def find_model(self, variant_id: str, best_fold: int, config: Config, **kwargs) -> Optional[Path]:
        """
        Find model checkpoint in hyperparameter grid search directory structure.
        
        Args:
            variant_id: Combination ID (e.g., "combo_0000")
            best_fold: Best fold number
            config: Configuration object with paths.model_dir
            **kwargs: Additional unused arguments
            
        Returns:
            Path to model checkpoint if found, None otherwise
        """
        from config.path_constants import BEST_MODEL_FILE_NAME
        model_path = Path(config.paths.model_dir) / 'hyperparameter_grid_search' / variant_id / f'fold_{best_fold}' / BEST_MODEL_FILE_NAME
        
        if model_path.exists():
            logger.info(f"Found model in hyperparameter grid search structure: {model_path}")
            return model_path
        
        return None


class CSIROModelsStrategy(ModelLocationStrategy):
    """
    Strategy for finding models in csiro-models Kaggle dataset.
    
    Searches for models in /kaggle/input/csiro-models/pytorch/{model_name}/{version}/best_model.pth.
    Falls back to /kaggle/input/csiro-models/pytorch/default/{version}/best_model.pth if model-specific path not found.
    Returns the newest version found.
    """
    
    def _scan_version_directories(self, base_path: Path, context: str) -> Optional[Tuple[Path, Path]]:
        """
        Scan version directories in a base path and return the newest model + metadata.
        
        Args:
            base_path: Base path containing version directories
            context: Context string for logging (e.g., "model-specific" or "default")
            
        Returns:
            Tuple of (model_path, metadata_path) if found, None otherwise
        """
        from config.path_constants import BEST_MODEL_FILE_NAME, REGRESSION_MODEL_FILE_NAME, METADATA_FILE_NAME
        
        if not base_path.exists():
            logger.info(f"❌ {context} base path does not exist: {base_path}")
            return None
        
        logger.info(f"🔍 Checking csiro-models dataset ({context}):")
        logger.info(f"   Base path: {base_path} (exists: {base_path.exists()})")
        
        version_dirs = []
        for version_dir in base_path.iterdir():
            if version_dir.is_dir():
                # Check for both best_model.pth and regression_model.pkl
                model_file = version_dir / BEST_MODEL_FILE_NAME
                regression_file = version_dir / REGRESSION_MODEL_FILE_NAME
                logger.info(f"   Checking version {version_dir.name}:")
                logger.info(f"     {model_file} (exists: {model_file.exists()})")
                logger.info(f"     {regression_file} (exists: {regression_file.exists()})")
                
                if model_file.exists() or regression_file.exists():
                    try:
                        version_num = int(version_dir.name)
                        # Prefer .pth if both exist, otherwise use whichever exists
                        found_file = model_file if model_file.exists() else regression_file
                        version_dirs.append((version_num, version_dir, found_file))
                    except ValueError:
                        logger.warning(f"Skipping non-numeric version directory: {version_dir.name}")
                        continue
        
        if not version_dirs:
            logger.info(f"❌ No valid version directories found in {base_path}")
            return None
        
        # Sort by version number (descending) to get newest
        version_dirs.sort(key=lambda x: x[0], reverse=True)
        newest_version, newest_dir, found_file = version_dirs[0]
        
        model_path = found_file
        metadata_path = newest_dir / METADATA_FILE_NAME
        if not metadata_path.exists():
            metadata_path = None
        
        logger.info(f"✅ Found model in csiro-models ({context}): version {newest_version}")
        logger.info(f"   Path: {model_path}")
        if metadata_path:
            logger.info(f"   Metadata: {metadata_path}")
        else:
            logger.info(f"   Metadata: not found")
        
        return model_path, metadata_path
    
    def find_model(self, model_name: Optional[str] = None, **kwargs) -> Tuple[Optional[Path], Optional[Path]]:
        """
        Find model checkpoint in csiro-models Kaggle dataset.
        
        Args:
            model_name: Optional model name for model-specific folder structure.
                       If provided, checks pytorch/{model_name}/ first, then falls back to pytorch/default/.
                       For regression models (lgbm, xgboost, ridge), also checks scikitlearn/{model_name}/.
        
        Returns:
            Tuple of (model_path, metadata_path):
            - model_path: Path to model checkpoint if found, None otherwise
            - metadata_path: Path to model_metadata.json if found, None otherwise
        """
        if not is_kaggle_environment():
            return None, None
        
        from config.path_constants import KAGGLE_INPUT
        
        # Known regression model types that are stored in scikitlearn/ directory
        REGRESSION_MODEL_TYPES = {'lgbm', 'xgboost', 'ridge'}
        
        # Try model-specific path first if model_name provided
        if model_name:
            # For regression models, check scikitlearn/ directory first
            if model_name.lower() in REGRESSION_MODEL_TYPES:
                scikitlearn_base = KAGGLE_INPUT / 'csiro-models' / 'scikitlearn' / model_name
                result = self._scan_version_directories(scikitlearn_base, f"scikitlearn/{model_name}")
                if result:
                    return result
            
            # Check pytorch/ directory (for end-to-end models)
            pytorch_base = KAGGLE_INPUT / 'csiro-models' / 'pytorch' / model_name
            result = self._scan_version_directories(pytorch_base, f"pytorch/{model_name}")
            if result:
                return result
        
        # Fallback to default path if model-specific path not found
        from config.path_constants import KAGGLE_INPUT_CSIRO_MODELS
        csiro_models_base = KAGGLE_INPUT_CSIRO_MODELS
        return self._scan_version_directories(csiro_models_base, "default/fallback") or (None, None)


class WorkingDirectoryStrategy(ModelLocationStrategy):
    """
    Strategy for finding models in working directory.
    
    Searches for models in: /kaggle/working/best_model/best_model.pth or regression_model.pkl
    (or local equivalent: ../output/best_model/best_model.pth)
    """
    
    def find_model(self, config: Config, **kwargs) -> Tuple[Optional[Path], Optional[Path]]:
        """
        Find model checkpoint in working directory.
        
        Args:
            config: Configuration object (unused, required for interface consistency)
            **kwargs: Additional unused arguments
            
        Returns:
            Tuple of (model_path, metadata_path):
            - model_path: Path to model checkpoint if found, None otherwise
            - metadata_path: Path to model_metadata.json if found, None otherwise
        """
        from config.path_constants import BEST_MODEL_FILE_NAME, REGRESSION_MODEL_FILE_NAME, METADATA_FILE_NAME
        from utils.system.io import get_best_model_path
        
        best_model_dir = Path(get_best_model_path())
        working_model = best_model_dir / BEST_MODEL_FILE_NAME
        working_regression_model = best_model_dir / REGRESSION_MODEL_FILE_NAME
        
        logger.info(f"🔍 Checking working directory for models:")
        logger.info(f"   Directory: {best_model_dir}")
        logger.info(f"   Checking: {working_model} (exists: {working_model.exists()})")
        logger.info(f"   Checking: {working_regression_model} (exists: {working_regression_model.exists()})")
        
        # Prefer .pth if both exist, otherwise use whichever exists
        if working_model.exists():
            model_path = working_model
            logger.info(f"✅ Found model in working directory: {model_path}")
        elif working_regression_model.exists():
            model_path = working_regression_model
            logger.info(f"✅ Found regression model in working directory: {model_path}")
        else:
            logger.info(f"❌ No model found in working directory")
            return None, None
        
        working_metadata = best_model_dir / METADATA_FILE_NAME
        metadata_path = working_metadata if working_metadata.exists() else None
        if metadata_path:
            logger.info(f"   Metadata: {metadata_path}")
        else:
            logger.info(f"   Metadata: not found")
        
        return model_path, metadata_path

