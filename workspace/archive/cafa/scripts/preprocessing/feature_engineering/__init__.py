"""
Feature engineering module for protein sequences.
Supports multiple feature extraction methods.
"""

# Import handcrafted features as default
from .handcrafted import extract_sequence_features, extract_handcrafted_parallel

# Import embedding module (functions accessible via embeddings.*)
from . import embeddings

__all__ = ['extract_sequence_features', 'extract_handcrafted_parallel', 'embeddings']
