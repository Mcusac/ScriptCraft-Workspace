"""Code duplication detector."""

from pathlib import Path
from typing import Any
import hashlib

from analyzers.base import BaseAnalyzer
from core import module_utils, file_utils


class DuplicationDetector(BaseAnalyzer):
    """
    Detect duplicated code blocks.
    
    Uses token-based hashing to find similar code segments.
    """
    
    def __init__(self, root: Path, min_lines: int = 6):
        """
        Initialize detector.
        
        Args:
            root: Root directory
            min_lines: Minimum lines to consider for duplication
        """
        super().__init__(root)
        self.min_lines = min_lines
    
    @property
    def name(self) -> str:
        return "duplication"
    
    def analyze(self) -> dict[str, Any]:
        """Detect code duplication."""
        files = module_utils.collect_python_files(self.root)
        
        # Build hash map of code blocks
        block_hashes: dict[str, list[tuple[str, int]]] = {}
        
        for file_path in files:
            module = module_utils.file_to_module(file_path, self.root)
            if not module:
                continue
            
            content = file_utils.read_file_safe(file_path)
            if not content:
                continue
            
            lines = content.splitlines()
            
            # Generate hashes for sliding windows
            for i in range(len(lines) - self.min_lines + 1):
                block = lines[i:i + self.min_lines]
                
                # Normalize: strip whitespace, skip empty/comment-only blocks
                normalized = [line.strip() for line in block if line.strip() and not line.strip().startswith('#')]
                
                if len(normalized) < self.min_lines:
                    continue
                
                # Hash the normalized block
                block_hash = hashlib.md5('\n'.join(normalized).encode()).hexdigest()
                block_hashes.setdefault(block_hash, []).append((module, i + 1))
        
        # Find duplicates
        duplicate_blocks = []
        for block_hash, locations in block_hashes.items():
            if len(locations) > 1:
                # Multiple locations with same hash = duplication
                for i in range(len(locations) - 1):
                    duplicate_blocks.append({
                        'file1': locations[i][0],
                        'line1': locations[i][1],
                        'file2': locations[i + 1][0],
                        'line2': locations[i + 1][1],
                        'lines': self.min_lines,
                        'hash': block_hash[:8]
                    })
        
        return {
            'duplicate_blocks': duplicate_blocks,
            'total_duplicates': len(duplicate_blocks),
        }
