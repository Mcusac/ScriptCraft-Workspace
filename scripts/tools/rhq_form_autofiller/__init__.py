"""
RHQ Form Autofiller Package

This package provides functionality for automating the filling of RHQ forms using pre-processed data.
"""

from .main import RHQFormAutofiller, main_runner

__version__ = "1.0.0"
__all__ = ["RHQFormAutofiller", "main_runner"]

# Register with registry if in development environment
try:
    from scripts.common.core import registry
    registry.register_tool(
        name="rhq_form_autofiller",
        description="Automates filling of RHQ forms using pre-processed data from Excel files."
    )(main_runner)
except ImportError:
    # Skip registration in shippable environment
    pass
