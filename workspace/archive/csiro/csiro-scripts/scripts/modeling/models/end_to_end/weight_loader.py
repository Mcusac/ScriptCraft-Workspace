# weight_loader.py
# Weight loading logic for timm models
# Handles pretrained weight loading with fallback strategies

import timm
import logging
from typing import Tuple, Optional

from utils.system import (
    setup_weight_cache,
    get_kaggle_input_weights_dir,
    configure_huggingface_cache
)

logger = logging.getLogger(__name__)


class TimmWeightLoader:
    """
    Handles loading of pretrained weights for timm models.
    
    Provides fallback strategies for offline/online scenarios and handles
    network errors gracefully.
    """
    
    def __init__(self):
        """Initialize weight loader."""
        self._pretrained_loaded = False
    
    def is_pretrained_loaded(self) -> bool:
        """Check if pretrained weights were successfully loaded."""
        return self._pretrained_loaded
    
    def _is_network_error(self, error: Exception) -> bool:
        """
        Check if an error is network-related or download-related.
        
        Args:
            error: Exception to check.
            
        Returns:
            True if error appears to be network/download related.
        """
        error_str = str(error).lower()
        network_keywords = [
            'connection', 'network', 'timeout', 'resolve', 'failed to resolve',
            'name resolution', 'temporary failure', 'max retries',
            'metadataincompletebuffer', 'incomplete', 'corrupt', 'deserializing'
        ]
        return any(keyword in error_str for keyword in network_keywords)
    
    def _try_load_pretrained_weights(self, model_name: str, num_classes: int) -> Tuple[bool, Optional[Exception], Optional[object]]:
        """
        Try to load pretrained weights for the model.
        
        Args:
            model_name: Name of timm model.
            num_classes: Number of output classes (0 for feature extraction mode).
            
        Returns:
            Tuple of (success, error, backbone). success is True if weights loaded successfully,
            False otherwise. error is the exception if loading failed, None if successful.
            backbone is the model if successful, None otherwise.
        """
        try:
            backbone = timm.create_model(
                model_name,
                pretrained=True,
                num_classes=num_classes
            )
            self._pretrained_loaded = True
            if num_classes == 0:
                logger.info(f"Successfully loaded pretrained weights for {model_name} (feature extraction mode)")
            else:
                logger.info(f"Successfully loaded pretrained weights for {model_name}")
            return True, None, backbone
        except Exception as e:
            return False, e, None
    
    def _reconfigure_cache_and_retry(self, model_name: str, num_classes: int) -> Tuple[bool, Optional[object]]:
        """
        Reconfigure HuggingFace cache and retry loading pretrained weights.
        
        Args:
            model_name: Name of timm model.
            num_classes: Number of output classes (0 for feature extraction mode).
            
        Returns:
            Tuple of (success, backbone). success is True if weights loaded successfully,
            False otherwise. backbone is the model if successful, None otherwise.
        """
        input_weights = get_kaggle_input_weights_dir()
        if input_weights is None or not input_weights.exists() or not any(input_weights.iterdir()):
            logger.warning("No weights found in input directory")
            return False, None
        
        logger.info(f"Found weights in input directory, reconfiguring cache: {input_weights}")
        configure_huggingface_cache(input_weights)
        
        try:
            backbone = timm.create_model(
                model_name,
                pretrained=True,
                num_classes=num_classes
            )
            self._pretrained_loaded = True
            if num_classes == 0:
                logger.info(f"Successfully loaded pretrained weights from input directory for {model_name} (feature extraction mode)")
            else:
                logger.info(f"Successfully loaded pretrained weights from input directory for {model_name}")
            return True, backbone
        except Exception as e2:
            logger.warning(f"Failed to load weights from input directory: {e2}")
            return False, None
    
    def load_weights(
        self,
        model_name: str,
        num_classes: int,
        pretrained: bool = True
    ) -> object:
        """
        Load model with pretrained weights, using fallback strategies if needed.
        
        Args:
            model_name: Name of timm model.
            num_classes: Number of output classes (0 for feature extraction mode).
            pretrained: Whether to attempt loading pretrained weights.
        
        Returns:
            Model backbone (timm model instance).
        
        Raises:
            RuntimeError: If model creation fails and pretrained=False.
        """
        # Setup weight cache for offline/online use
        if pretrained:
            cache_path, has_internet = setup_weight_cache()
            if cache_path:
                logger.info(f"Using offline weight cache: {cache_path}")
            elif not has_internet:
                logger.warning("No internet and no offline weights found - will fallback to non-pretrained if download fails")
        
        if not pretrained:
            # Not using pretrained weights
            backbone = timm.create_model(
                model_name,
                pretrained=False,
                num_classes=num_classes
            )
            self._pretrained_loaded = False
            return backbone
        
        # Try to load pretrained weights
        success, error, backbone = self._try_load_pretrained_weights(model_name, num_classes)
        if success:
            return backbone
        
        # If failed, try recovery strategies
        if error is not None:
            is_network_error = self._is_network_error(error)
            if is_network_error:
                logger.warning(f"Network/download error loading pretrained weights: {error}")
                # Try to reconfigure cache and retry
                success, backbone = self._reconfigure_cache_and_retry(model_name, num_classes)
                if success:
                    return backbone
        
        # Fall back to non-pretrained model
        logger.warning("Falling back to non-pretrained model")
        backbone = timm.create_model(
            model_name,
            pretrained=False,
            num_classes=num_classes
        )
        self._pretrained_loaded = False
        return backbone

