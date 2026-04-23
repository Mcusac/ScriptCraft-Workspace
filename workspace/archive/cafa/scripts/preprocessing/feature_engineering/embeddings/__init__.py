"""
Embedding feature extraction module.
Supports versioned implementations for different embedding strategies.
"""

# Import from v1 as default
from .embeddings_v1 import (
    load_embedding_data,
    align_embeddings
)

__all__ = [
    'load_embedding_data',
    'align_embeddings'
]

# Future versions can be imported explicitly:
# from .embeddings_v2 import load_fused_embeddings
