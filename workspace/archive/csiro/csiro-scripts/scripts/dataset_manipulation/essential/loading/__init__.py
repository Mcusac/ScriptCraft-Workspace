# __init__.py
# Data loading package
#
# Provides utilities for loading CSV files and images with comprehensive error handling.
# 
# Features:
# - CSV loading with pandas (supports batch loading with progress bars)
# - Image loading using PIL (supports JPEG, PNG, and other formats)
# - Path validation and file existence checks
# - Batch processing utilities with progress tracking
# - Consistent error handling patterns
#
# All file I/O operations include proper error handling for FileNotFoundError,
# PermissionError, and other common issues.


__all__ = ['load_jpg', 'load_jpg_batch', 'load_csv', 'load_csv_batch', 'load_and_validate_test_data']