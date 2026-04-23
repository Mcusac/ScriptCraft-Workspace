# ensemble.py
# Main ensemble orchestrator for combining multiple models

import copy
import logging
import torch
import numpy as np
from typing import List, Optional, Tuple

from .model_loader import ModelConfig
from .methods import EnsemblingMethod

logger = logging.getLogger(__name__)


class Ensemble:
    """
    Ensemble of multiple models for combined predictions.
    
    Coordinates model loading, inference, and prediction combination.
    """
    
    def __init__(
        self,
        models: List[torch.nn.Module],
        model_configs: List[ModelConfig],
        ensembling_method: EnsemblingMethod,
        device: torch.device,
        score_type: str = 'cv'
    ):
        """
        Initialize ensemble.
        
        Args:
            models: List of loaded models (in eval mode, on device)
            model_configs: List of ModelConfig objects corresponding to models
            ensembling_method: Method to use for combining predictions
            device: Device models are on
            score_type: Which scores to use for weighting: 'cv', 'submission', 'combined' (default: 'cv')
        """
        if len(models) != len(model_configs):
            raise ValueError(
                f"Number of models ({len(models)}) must match "
                f"number of configs ({len(model_configs)})"
            )
        
        self.models = models
        self.model_configs = model_configs
        self.ensembling_method = ensembling_method
        self.device = device
        self.score_type = score_type
    
    def predict(
        self,
        images: torch.Tensor,
        return_individual: bool = False
    ) -> np.ndarray:
        """
        Run inference with all models and combine predictions.
        
        NOTE: This method assumes images are already preprocessed correctly.
        For ensemble inference with per-model preprocessing, use predict_with_individual_preprocessing().
        
        Args:
            images: Input tensor of shape (B, C, H, W) - must be preprocessed correctly
            return_individual: If True, also returns individual predictions
        
        Returns:
            Combined predictions array of shape (B, 3).
            If return_individual=True, returns tuple (combined, individual_list)
        """
        all_predictions = []
        
        with torch.no_grad():
            for idx, model in enumerate(self.models):
                outputs = model(images)
                predictions = outputs.detach().cpu().numpy()
                all_predictions.append(predictions)
        
        # Get weights for methods that require scores
        weights = None
        method_name = self.ensembling_method.get_name()
        if method_name in {'weighted_average', 'ranked_average', 'percentile_average'}:
            weights = self._extract_weights()
            if weights is None or any(w is None for w in weights):
                logger.warning("Some models have None scores, falling back to simple average")
                from .methods import SimpleAverageEnsemble
                self.ensembling_method = SimpleAverageEnsemble()
                weights = None
        
        # Combine predictions
        combined = self.ensembling_method.combine(all_predictions, weights)
        
        if return_individual:
            return combined, all_predictions
        return combined
    
    def predict_with_individual_preprocessing(
        self,
        test_csv_path: str,
        data_root: str,
        config,
        return_individual: bool = False
    ) -> np.ndarray:
        """
        Run inference with each model using its own preprocessing from metadata.
        
        Each model is run with its own preprocessing configuration (from model_metadata.json),
        ensuring predictions match what the model was trained with.
        
        Args:
            test_csv_path: Path to test.csv file
            data_root: Root directory for images
            config: Base configuration object (will be copied and modified per model)
            return_individual: If True, also returns individual predictions
        
        Returns:
            Combined predictions array of shape (N, 3) where N is number of unique images.
            If return_individual=True, returns tuple (combined, individual_list)
        """
        from modeling.testing import create_test_dataloader
        
        all_predictions = []
        
        logger.info(f"Running inference with {len(self.models)} models using individual preprocessing...")
        
        for idx, (model, model_config) in enumerate(zip(self.models, self.model_configs), 1):
            logger.info(
                f"Model {idx}/{len(self.models)}: {model_config.variant_id} "
                f"(preprocessing: {model_config.preprocessing_list if model_config.preprocessing_list else 'default'})"
            )
            
            # Create config copy for this model
            model_config_obj = copy.deepcopy(config)
            
            # Set dataset_type from model_config (CRITICAL - must match what was used during training)
            dataset_type = model_config.dataset_type
            model_config_obj.data.dataset_type = dataset_type
            
            # Apply this model's preprocessing to the config copy
            from utils.config.config_updater import apply_preprocessing_to_config
            apply_preprocessing_to_config(
                model_config_obj,
                model_config.preprocessing_list,
                suppress_default_logging=True
            )
            
            # Create dataloader with this model's preprocessing and dataset_type
            test_loader = create_test_dataloader(
                test_csv_path=test_csv_path,
                data_root=data_root,
                config=model_config_obj,
                dataset_type=dataset_type
            )
            
            # Run inference for this model
            model_predictions = []
            with torch.no_grad():
                for batch in test_loader:
                    outputs = self._process_inference_batch(batch, model, dataset_type)
                    predictions = outputs.detach().cpu().numpy()
                    model_predictions.append(predictions)
            
            # Concatenate all batches for this model
            model_pred_array = np.concatenate(model_predictions, axis=0)
            all_predictions.append(model_pred_array)
            
            logger.info(f"  Model {idx} predictions shape: {model_pred_array.shape}")
        
        # Get weights for methods that require scores
        weights = None
        method_name = self.ensembling_method.get_name()
        if method_name in {'weighted_average', 'ranked_average', 'percentile_average'}:
            weights = self._extract_weights()
            if weights is None or any(w is None for w in weights):
                logger.warning("Some models have None scores, falling back to simple average")
                from .methods import SimpleAverageEnsemble
                self.ensembling_method = SimpleAverageEnsemble()
                weights = None
        
        # Combine predictions
        combined = self.ensembling_method.combine(all_predictions, weights)
        
        if return_individual:
            return combined, all_predictions
        return combined
    
    def _process_inference_batch(
        self,
        batch: Tuple,
        model: torch.nn.Module,
        dataset_type: str
    ) -> torch.Tensor:
        """
        Process a single batch for inference, handling both full and split dataset types.
        
        Args:
            batch: Batch from DataLoader - either (images, targets) for 'full' dataset,
                   or (left_img, right_img, targets) for 'split' dataset
            model: Model to run inference with (supports dual input for split datasets)
            dataset_type: 'full' or 'split' - determines batch format
        
        Returns:
            Model outputs tensor
        
        Note:
            For split dataset type, the model processes both left and right images
            and averages their outputs for final predictions.
        """
        from modeling.utils import process_batch_for_model
        
        return process_batch_for_model(batch, model, self.device, dataset_type)
    
    def _extract_weights(self) -> Optional[List[float]]:
        """
        Extract weights from model configs based on score_type.
        
        Returns:
            List of weights (scores) or None if no valid scores available
        """
        logger.info(f"Extracting weights using score_type='{self.score_type}'")
        
        if self.score_type == 'cv':
            weights = [mc.cv_score for mc in self.model_configs]
            logger.info(f"CV scores extracted: {[f'{w:.4f}' if w is not None else 'None' for w in weights]}")
        elif self.score_type == 'submission':
            weights = [mc.submission_score for mc in self.model_configs]
            logger.info(f"Submission scores extracted: {[f'{w:.4f}' if w is not None else 'None' for w in weights]}")
        elif self.score_type == 'combined':
            # Weighted combination: DEFAULT_CV_WEIGHT * cv + DEFAULT_SUBMISSION_WEIGHT * submission
            weights = []
            for mc in self.model_configs:
                cv = mc.cv_score
                sub = mc.submission_score
                if cv is not None and sub is not None:
                    from modeling.ensembling.constants import DEFAULT_CV_WEIGHT, DEFAULT_SUBMISSION_WEIGHT
                    weights.append(DEFAULT_CV_WEIGHT * cv + DEFAULT_SUBMISSION_WEIGHT * sub)
                elif cv is not None:
                    weights.append(cv)
                elif sub is not None:
                    weights.append(sub)
                else:
                    weights.append(None)
            logger.info(f"Combined scores extracted: {[f'{w:.4f}' if w is not None else 'None' for w in weights]}")
        else:
            # Default to CV
            weights = [mc.cv_score for mc in self.model_configs]
            logger.info(f"CV scores extracted (default): {[f'{w:.4f}' if w is not None else 'None' for w in weights]}")
        
        return weights
    
    def __call__(self, images: torch.Tensor) -> np.ndarray:
        """Convenience method: call ensemble like a function."""
        return self.predict(images)
