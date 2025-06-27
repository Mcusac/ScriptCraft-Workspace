"""
ScriptCraft Tools Package

This package contains all tools for data processing, validation, transformation, and automation.
Tools are organized by functionality but all accessible through a unified interface.

Example Usage:
    from scriptcraft.tools import (
        # Data Processing Tools
        DataContentComparer,
        SchemaDetector,
        
        # Validation Tools  
        DictionaryDrivenChecker,
        ReleaseConsistencyChecker,
        ScoreTotalsChecker,
        FeatureChangeChecker,
        DictionaryValidator,
        MedVisitIntegrityValidator,
        
        # Transformation Tools
        DictionaryCleaner,
        DateFormatStandardizer,
        
        # Automation Tools
        RHQFormAutofiller,
        AutomatedLabeler
    )

Tool Discovery:
    from scriptcraft.tools import get_available_tools, list_tools_by_category
    
    # Get all tools
    tools = get_available_tools()
    
    # Get tools by category
    validation_tools = list_tools_by_category("validation")
"""

import importlib
import pkgutil
from pathlib import Path
from typing import Dict, List, Optional, Type, Any

from scriptcraft.common.core import BaseTool


# Tool categories for organization
TOOL_CATEGORIES = {
    "analysis": [
        "data_content_comparer",
        "schema_detector"
    ],
    "validation": [
        "dictionary_driven_checker", 
        "release_consistency_checker",
        "score_totals_checker", 
        "feature_change_checker",
        "dictionary_validator",
        "medvisit_integrity_validator"
    ],
    "transformation": [
        "dictionary_cleaner",
        "date_format_standardizer"
    ],
    "automation": [
        "rhq_form_autofiller",
        "automated_labeler"
    ]
}

# Cache for loaded tools to avoid re-loading
_cached_tools: Optional[Dict[str, BaseTool]] = None


def get_available_tools() -> Dict[str, BaseTool]:
    """
    Get all available tools from the tools directory.
    
    Returns:
        Dict mapping tool names to their instances
    """
    global _cached_tools
    
    # Return cached tools if already loaded
    if _cached_tools is not None:
        return _cached_tools
    
    tools = {}
    
    # Get the tools directory path
    tools_dir = Path(__file__).parent
    
    # Import all tool modules
    for _, name, is_pkg in pkgutil.iter_modules([str(tools_dir)]):
        if is_pkg and not name.startswith('_'):
            try:
                # Import the tool module
                module = importlib.import_module(f".{name}", package="scriptcraft.tools")
                
                # Look for the tool instance or tool class
                tool_instance = None
                
                # Check for common tool instance names
                for attr_name in ['tool', 'main_tool', name.replace('_', '').lower()]:
                    if hasattr(module, attr_name):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, BaseTool):
                            tool_instance = attr
                            break
                        elif isinstance(attr, type) and issubclass(attr, BaseTool):
                            # Instantiate the tool class
                            tool_instance = attr()
                            break
                
                # If no instance found, look for any BaseTool subclass
                if not tool_instance:
                    for attr_name in dir(module):
                        attr = getattr(module, attr_name)
                        if isinstance(attr, type) and issubclass(attr, BaseTool) and attr != BaseTool:
                            tool_instance = attr()
                            break
                
                if tool_instance:
                    tools[name] = tool_instance
                    
            except Exception as e:
                print(f"Warning: Failed to load tool {name}: {e}")
    
    # Cache the tools
    _cached_tools = tools
    return tools


def list_tools_by_category(category: Optional[str] = None) -> Dict[str, List[str]]:
    """
    List tools organized by category.
    
    Args:
        category: Optional specific category to filter by
        
    Returns:
        Dict mapping categories to lists of tool names
    """
    if category:
        return {category: TOOL_CATEGORIES.get(category, [])}
    
    return TOOL_CATEGORIES.copy()


def get_tool_categories() -> List[str]:
    """Get list of available tool categories."""
    return list(TOOL_CATEGORIES.keys())


def run_tool(tool_name: str, **kwargs) -> None:
    """
    Run a specific tool by name.
    
    Args:
        tool_name: Name of the tool to run
        **kwargs: Arguments to pass to the tool's run method
    """
    tools = get_available_tools()
    
    if tool_name not in tools:
        available = list(tools.keys())
        raise ValueError(f"Tool '{tool_name}' not found. Available tools: {available}")
    
    tool = tools[tool_name]
    tool.run(**kwargs)


def discover_tool_metadata(tool_name: str) -> Dict[str, Any]:
    """
    Get metadata about a specific tool.
    
    Args:
        tool_name: Name of the tool
        
    Returns:
        Dict containing tool metadata
    """
    tools = get_available_tools()
    
    if tool_name not in tools:
        return {}
    
    tool = tools[tool_name]
    
    # Determine category
    category = "uncategorized"
    for cat, tool_list in TOOL_CATEGORIES.items():
        if tool_name in tool_list:
            category = cat
            break
    
    return {
        "name": tool_name,
        "description": getattr(tool, "description", ""),
        "category": category,
        "class_name": tool.__class__.__name__,
        "module": tool.__class__.__module__
    }


# Import specific tool classes for direct access
# These will be updated as tools are properly integrated

# Direct imports for commonly used tools
try:
    from .data_content_comparer import DataContentComparer
except ImportError:
    DataContentComparer = None

try:
    from .rhq_form_autofiller import RHQFormAutofiller
except ImportError:
    RHQFormAutofiller = None

try:
    from .automated_labeler import AutomatedLabeler
except ImportError:
    AutomatedLabeler = None

# Validation tools (moved from checkers)
try:
    from .dictionary_driven_checker import DictionaryDrivenChecker
except ImportError:
    DictionaryDrivenChecker = None

try:
    from .release_consistency_checker import ReleaseConsistencyChecker
except ImportError:
    ReleaseConsistencyChecker = None

try:
    from .score_totals_checker import ScoreTotalsChecker
except ImportError:
    ScoreTotalsChecker = None

try:
    from .feature_change_checker import FeatureChangeChecker
except ImportError:
    FeatureChangeChecker = None

# Validators (moved from validators)
try:
    from .dictionary_validator import DictionaryValidator
except ImportError:
    DictionaryValidator = None

try:
    from .medvisit_integrity_validator import MedVisitIntegrityValidator
except ImportError:
    MedVisitIntegrityValidator = None

# Transformers (moved from transformers)
try:
    from .dictionary_cleaner import DictionaryCleaner
except ImportError:
    DictionaryCleaner = None

try:
    from .date_format_standardizer import DateFormatStandardizer
except ImportError:
    DateFormatStandardizer = None

try:
    from .schema_detector import SchemaDetector
except ImportError:
    SchemaDetector = None


# Export available tools
__all__ = [
    # Core functions
    'get_available_tools',
    'list_tools_by_category', 
    'get_tool_categories',
    'run_tool',
    'discover_tool_metadata',
    
    # Tool classes (available if imported successfully)
    'DataContentComparer',
    'SchemaDetector',
    'RHQFormAutofiller', 
    'AutomatedLabeler',
    'DictionaryDrivenChecker',
    'ReleaseConsistencyChecker',
    'ScoreTotalsChecker',
    'FeatureChangeChecker',
    'DictionaryValidator',
    'MedVisitIntegrityValidator',
    'DictionaryCleaner',
    'DateFormatStandardizer'
]

# Filter out None values from __all__
__all__ = [name for name in __all__ if globals().get(name) is not None or name in [
    'get_available_tools', 'list_tools_by_category', 'get_tool_categories', 
    'run_tool', 'discover_tool_metadata'
]]
