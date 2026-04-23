# contest/registry.py
# Contest registration and detection system

from typing import Optional, Dict
import logging

from contest.base import (
    ContestConfig,
    ContestDataSchema,
    ContestPostProcessor,
    ContestPaths
)

logger = logging.getLogger(__name__)

# Global contest registry
_contest_registry: Dict[str, Dict[str, any]] = {}
_default_contest_name: Optional[str] = None


def register_contest(
    name: str,
    config: ContestConfig,
    data_schema: ContestDataSchema,
    post_processor: ContestPostProcessor,
    paths: ContestPaths
) -> None:
    """
    Register a contest implementation.
    
    Args:
        name: Contest name (e.g., 'csiro')
        config: Contest configuration instance
        data_schema: Contest data schema instance
        post_processor: Contest post-processor instance
        paths: Contest paths instance
    """
    _contest_registry[name] = {
        'config': config,
        'data_schema': data_schema,
        'post_processor': post_processor,
        'paths': paths
    }
    logger.info(f"Registered contest: {name}")


def set_default_contest(name: str) -> None:
    """Set the default contest name."""
    global _default_contest_name
    if name not in _contest_registry:
        raise ValueError(f"Contest '{name}' not registered. Available: {list(_contest_registry.keys())}")
    _default_contest_name = name
    logger.info(f"Set default contest: {name}")


def get_contest(name: Optional[str] = None) -> Dict[str, any]:
    """
    Get contest implementation by name.
    
    Args:
        name: Contest name. If None, uses default contest.
        
    Returns:
        Dictionary with 'config', 'data_schema', 'post_processor', 'paths' keys.
        
    Raises:
        ValueError: If contest not found or no default set.
    """
    if name is None:
        if _default_contest_name is None:
            raise ValueError("No default contest set. Call set_default_contest() or register_contest() first.")
        name = _default_contest_name
    
    if name not in _contest_registry:
        available = list(_contest_registry.keys())
        raise ValueError(
            f"Contest '{name}' not found. Available contests: {available}. "
            f"Register contest with register_contest() first."
        )
    
    return _contest_registry[name]


def get_contest_config(name: Optional[str] = None) -> ContestConfig:
    """Get contest config by name."""
    return get_contest(name)['config']


def get_contest_data_schema(name: Optional[str] = None) -> ContestDataSchema:
    """Get contest data schema by name."""
    return get_contest(name)['data_schema']


def get_contest_post_processor(name: Optional[str] = None) -> ContestPostProcessor:
    """Get contest post-processor by name."""
    return get_contest(name)['post_processor']


def get_contest_paths(name: Optional[str] = None) -> ContestPaths:
    """Get contest paths by name."""
    return get_contest(name)['paths']


# Auto-register CSIRO contest on import
def _auto_register_csiro():
    """Auto-register CSIRO contest."""
    try:
        from contest.csiro import (
            get_csiro_config,
            get_csiro_data_schema,
            get_csiro_post_processor,
            get_csiro_paths
        )
        register_contest(
            name='csiro',
            config=get_csiro_config(),
            data_schema=get_csiro_data_schema(),
            post_processor=get_csiro_post_processor(),
            paths=get_csiro_paths()
        )
        set_default_contest('csiro')
    except ImportError as e:
        logger.warning(f"Could not auto-register CSIRO contest: {e}")


# Auto-register on module import
_auto_register_csiro()
