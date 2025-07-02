"""
ScriptCraft Tools Package

This package contains all tools for data processing, validation, transformation, and automation.
Tools are organized by functionality but all accessible through a unified interface.

Example Usage:
    from scriptcraft.tools import (
        # All tools are now available
        RHQFormAutofiller, DataContentComparer, SchemaDetector, 
        DictionaryDrivenChecker, ReleaseConsistencyChecker, ScoreTotalsChecker,
        FeatureChangeChecker, DictionaryValidator, MedVisitIntegrityValidator,
        DictionaryCleaner, DateFormatStandardizer, AutomatedLabeler
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


# === TOOL IMPORTS ===
# Import all standardized tools
try:
    from .rhq_form_autofiller import RHQFormAutofiller
except ImportError:
    RHQFormAutofiller = None

try:
    from .data_content_comparer import DataContentComparer
except ImportError:
    DataContentComparer = None

try:
    from .schema_detector import SchemaDetectorTool as SchemaDetector
except ImportError:
    SchemaDetector = None

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

try:
    from .dictionary_validator import DictionaryValidator
except ImportError:
    DictionaryValidator = None

try:
    from .medvisit_integrity_validator import MedVisitIntegrityValidator
except ImportError:
    MedVisitIntegrityValidator = None

try:
    from .dictionary_cleaner import DictionaryCleaner
except ImportError:
    DictionaryCleaner = None

try:
    from .date_format_standardizer import DateFormatStandardizer
except ImportError:
    DateFormatStandardizer = None

try:
    from .automated_labeler import AutomatedLabeler
except ImportError:
    AutomatedLabeler = None
