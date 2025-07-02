"""
Supplement Prepper Enhancement

Prepares data supplements for dictionary enhancement workflows.
"""

from scriptcraft._version import __version__

__description__ = "🔧 Prepare data supplements for dictionary enhancement"
__tags__ = ["enhancement", "supplement", "preparation", "workflow"]

from .tool import SupplementPrepper, enhancement

__all__ = ["SupplementPrepper", "enhancement"]
