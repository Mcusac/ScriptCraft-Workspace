"""
ScriptCraft Tools Package

This package contains all tools for data processing, validation, transformation, and automation.
Tools are organized by functionality but all accessible through a unified interface.

Example Usage:
    from scriptcraft.tools import (
        # Automation Tools (exemplar)
        RHQFormAutofiller,
        
        # Other tools (will be available after refactoring)
        # DataContentComparer, SchemaDetector, DictionaryDrivenChecker, etc.
    )

Tool Discovery:
    from scriptcraft.tools import get_available_tools, list_tools_by_category
    
    # Get all tools
    tools = get_available_tools()
    
    # Get tools by category
    validation_tools = list_tools_by_category("validation")
"""

# Import the unified registry system from the new registry package
from scriptcraft.common.registry import (
    get_available_tools,
    list_tools_by_category,
    run_tool,
    discover_tool_metadata,
    registry
)

# Convenience function for backward compatibility
def get_tool_categories() -> list:
    """Get list of available tool categories."""
    return list(registry.get_tools_by_category().keys())


# === EXPLICIT TOOL EXPORTS ===
# Import only the exemplar tool explicitly
try:
    from .rhq_form_autofiller import RHQFormAutofiller
except ImportError:
    RHQFormAutofiller = None

# Placeholder for other tools (will be imported after refactoring)
DataContentComparer = None
SchemaDetector = None
DictionaryDrivenChecker = None
ReleaseConsistencyChecker = None
ScoreTotalsChecker = None
FeatureChangeChecker = None
DictionaryValidator = None
MedVisitIntegrityValidator = None
DictionaryCleaner = None
DateFormatStandardizer = None
AutomatedLabeler = None

__all__ = [
    # Tool discovery functions
    'get_available_tools', 'list_tools_by_category', 'get_tool_categories',
    'run_tool', 'discover_tool_metadata',
    
    # Tool classes (exemplar only for now)
    'RHQFormAutofiller',
    
    # Placeholder exports for other tools
    'DataContentComparer', 'SchemaDetector', 'DictionaryDrivenChecker', 
    'ReleaseConsistencyChecker', 'ScoreTotalsChecker', 'FeatureChangeChecker', 
    'DictionaryValidator', 'MedVisitIntegrityValidator', 'DictionaryCleaner', 
    'DateFormatStandardizer', 'AutomatedLabeler'
]
