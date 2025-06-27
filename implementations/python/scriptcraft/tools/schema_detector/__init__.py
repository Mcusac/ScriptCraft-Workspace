"""
🔍 Schema Detector Tool

Automatically detects and generates database schemas from datasets without reading sensitive data.
Supports healthcare-specific patterns and privacy-safe analysis.

Features:
- 📊 Column type inference from headers and sample data
- 🏗️ SQL schema generation (SQLite, SQL Server, PostgreSQL)  
- 🔐 Privacy-safe analysis (limited data sampling)
- 📝 Documentation generation
- 🎯 Healthcare/patient data patterns
- 📋 Index and constraint recommendations

Author: ScriptCraft Team
Version: 1.0.0
"""

from .tool import SchemaDetector

__version__ = "1.0.0"
__description__ = "🔍 Analyzes datasets and generates database schemas"
__tags__ = ["analysis", "schema", "detection", "database", "sql"]
__data_types__ = ["csv", "xlsx", "json"]
__domains__ = ["clinical", "biomarkers", "genomics", "imaging"]
__complexity__ = "intermediate"

# Export the main tool
__all__ = ['SchemaDetector'] 