"""Configuration for code health thresholds."""

from dataclasses import dataclass
from typing import Any


@dataclass
class ThresholdConfig:
    """
    Configuration for code health thresholds.
    
    All thresholds are configurable for flexibility.
    Provides sensible defaults that work out of the box.
    """
    
    # File metrics
    max_file_lines: int = 500
    max_function_lines: int = 50
    max_class_methods: int = 7
    
    # Complexity
    max_function_complexity: int = 10
    max_class_complexity: int = 50
    
    # Package cohesion
    min_package_cohesion_pct: int = 25
    
    # Import depth
    max_deep_imports: int = 30
    max_import_depth: int = 4
    
    # Code duplication
    max_duplicate_blocks: int = 5
    min_duplicate_lines: int = 6
    
    # Dead code
    max_unused_imports: int = 0
    max_unreachable_blocks: int = 0
    
    def to_dict(self) -> dict[str, Any]:
        """Convert config to dictionary."""
        return {
            'max_file_lines': self.max_file_lines,
            'max_function_lines': self.max_function_lines,
            'max_class_methods': self.max_class_methods,
            'max_function_complexity': self.max_function_complexity,
            'max_class_complexity': self.max_class_complexity,
            'min_package_cohesion_pct': self.min_package_cohesion_pct,
            'max_deep_imports': self.max_deep_imports,
            'max_import_depth': self.max_import_depth,
            'max_duplicate_blocks': self.max_duplicate_blocks,
            'min_duplicate_lines': self.min_duplicate_lines,
            'max_unused_imports': self.max_unused_imports,
            'max_unreachable_blocks': self.max_unreachable_blocks,
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> 'ThresholdConfig':
        """Create config from dictionary."""
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
