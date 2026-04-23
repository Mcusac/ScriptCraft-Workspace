# base.py
# Abstract base class for model location strategies

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional


class ModelLocationStrategy(ABC):
    """
    Abstract base class for model location strategies.
    
    Each strategy encapsulates logic for finding models in a specific location type.
    Strategies are stateless and can be reused across different contexts.
    """
    
    @abstractmethod
    def find_model(self, **kwargs) -> Optional[Path]:
        """
        Find a model checkpoint in this strategy's location.
        
        Args:
            **kwargs: Strategy-specific parameters
            
        Returns:
            Path to model checkpoint if found, None otherwise
        """
        pass

