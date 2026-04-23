"""
Submission merging utilities for CAFA 6 protein function prediction.
Provides outer merge strategy that prefers one submission when both exist.
"""

import subprocess
import tempfile
from pathlib import Path
from typing import Optional, Tuple
from utils.utils_common import open_text_file
from prediction.prediction_utils import format_prediction_score, is_valid_score, cleanup_temp_files


def _sort_file_external(filepath: str, output_path: str) -> None:
    """
    Sort a TSV file by (protein_id, term) using external sort.
    Uses system sort command if available, otherwise Python-based sort.
    
    Args:
        filepath: Path to input file
        output_path: Path to output sorted file
    """
    import sys
    import os
    
    # Try system sort first (fastest, most memory-efficient)
    try:
        # Use system sort: sort by columns 1 and 2 (protein_id, term)
        # -t$'\t' specifies tab delimiter
        # -k1,2 sorts by columns 1-2
        # -T specifies temp directory (use system temp if available)
        if sys.platform == 'win32':
            # Windows: use Python-based sort
            _sort_file_python(filepath, output_path)
        else:
            # Unix/Linux: use system sort
            temp_dir = tempfile.gettempdir()
            result = subprocess.run(
                ['sort', '-t', '\t', '-k1,2', '-T', temp_dir, filepath],
                stdout=open(output_path, 'w'),
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        # Fallback to Python-based sort
        _sort_file_python(filepath, output_path)


def _sort_file_python(filepath: str, output_path: str) -> None:
    """
    Sort a TSV file by (protein_id, term) using Python.
    Memory-efficient: reads in chunks and uses external sort.
    
    Args:
        filepath: Path to input file
        output_path: Path to output sorted file
    """
    import tempfile
    import heapq
    
    # Read file and sort in chunks
    from config.prediction import SUBMISSION_SORT_CHUNK_SIZE
    chunk_size = SUBMISSION_SORT_CHUNK_SIZE
    chunk_files = []
    chunk_num = 0
    
    print(f"      Sorting file in chunks...")
    with open_text_file(filepath, 'r') as f:
        chunk = []
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 3:
                protein_id, term, score_str = parts
                try:
                    score = float(score_str)
                    if is_valid_score(score):
                        chunk.append((protein_id, term, score, line))
                except ValueError:
                    continue
            
            if len(chunk) >= chunk_size:
                # Sort chunk and write to temp file
                chunk.sort(key=lambda x: (x[0], x[1]))  # Sort by (protein_id, term)
                temp_chunk = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tsv')
                for _, _, _, orig_line in chunk:
                    temp_chunk.write(orig_line + '\n')
                temp_chunk.close()
                chunk_files.append(temp_chunk.name)
                chunk = []
                chunk_num += 1
                from config.prediction import PREDICTION_PROGRESS_INTERVALS
                if chunk_num % PREDICTION_PROGRESS_INTERVALS["chunks"] == 0:
                    print(f"         Created {chunk_num} sorted chunks...")
        
        # Write remaining chunk
        if chunk:
            chunk.sort(key=lambda x: (x[0], x[1]))
            temp_chunk = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tsv')
            for _, _, _, orig_line in chunk:
                temp_chunk.write(orig_line + '\n')
            temp_chunk.close()
            chunk_files.append(temp_chunk.name)
    
    # Merge sorted chunks
    print(f"      Merging {len(chunk_files)} sorted chunks...")
    with open(output_path, 'w') as out_file:
        # Open all chunk files
        chunk_handles = [open_text_file(f, 'r') for f in chunk_files]
        chunk_iters = [iter(f) for f in chunk_handles]
        
        # Initialize heap with first line from each chunk
        heap = []
        for i, chunk_iter in enumerate(chunk_iters):
            try:
                line = next(chunk_iter).strip()
                if line:
                    parts = line.split('\t')
                    if len(parts) == 3:
                        protein_id, term = parts[0], parts[1]
                        heap.append((protein_id, term, i, line))
            except StopIteration:
                pass
        
        heapq.heapify(heap)
        
        # Merge chunks
        while heap:
            protein_id, term, chunk_idx, line = heapq.heappop(heap)
            out_file.write(line + '\n')
            
            # Get next line from this chunk
            try:
                next_line = next(chunk_iters[chunk_idx]).strip()
                if next_line:
                    parts = next_line.split('\t')
                    if len(parts) == 3:
                        next_protein_id, next_term = parts[0], parts[1]
                        heapq.heappush(heap, (next_protein_id, next_term, chunk_idx, next_line))
            except StopIteration:
                pass
        
        # Close chunk files
        for f in chunk_handles:
            f.close()
        
        # Clean up temp files
        cleanup_temp_files([Path(f) for f in chunk_files])


def parse_submission_line(line: str) -> Optional[Tuple[str, str, float]]:
    """
    Parse a line from submission file.
    
    Args:
        line: Line from submission file
        
    Returns:
        tuple: (protein_id, term, score) or None if invalid
    """
    line = line.strip()
    if not line:
        return None
    
    parts = line.split('\t')
    if len(parts) != 3:
        return None
    
    protein_id, term, score_str = parts
    try:
        score = float(score_str)
        if 0 < score <= 1.0:
            return (protein_id, term, score)
    except ValueError:
        pass
    
    return None


def merge_submissions_outer(submission1_path: str,
                           submission2_path: str,
                           output_path: str,
                           prefer: str = 'submission2') -> str:
    """
    Merge two submission files using outer merge with preference.
    Memory-efficient streaming implementation using sorted file merge.
    
    When both submissions have predictions for the same (protein, term) pair,
    the preferred submission's confidence is used.
    
    Args:
        submission1_path: Path to first submission file
        submission2_path: Path to second submission file
        output_path: Path to output merged submission file
        prefer: Which submission to prefer when both exist ('submission1' or 'submission2')
        
    Returns:
        str: Path to merged submission file
    """
    import tempfile
    
    output_path_obj = Path(output_path)
    output_path_obj.parent.mkdir(parents=True, exist_ok=True)
    
    # Determine which file to prefer
    prefer_first = (prefer == 'submission1')
    preferred_path = submission1_path if prefer_first else submission2_path
    other_path = submission2_path if prefer_first else submission1_path
    
    print(f"   Sorting submissions for merge (preferring {prefer})...")
    
    # Sort both files externally
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tsv') as temp1:
        temp1_path = temp1.name
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tsv') as temp2:
        temp2_path = temp2.name
    
    try:
        print(f"      Sorting preferred file...")
        _sort_file_external(preferred_path, temp1_path)
        print(f"      Sorting other file...")
        _sort_file_external(other_path, temp2_path)
        
        # Stream merge both sorted files
        print(f"   Merging sorted files...")
        total_written = 0
        preferred_count = 0
        other_count = 0
        overlap_count = 0
        
        with open_text_file(temp1_path, 'r') as pref_file, open_text_file(temp2_path, 'r') as other_file, open(output_path, 'w', encoding='utf-8') as out_file:
            # Get first line from each file
            pref_line = pref_file.readline()
            other_line = other_file.readline()
            
            pref_data = parse_submission_line(pref_line) if pref_line else None
            other_data = parse_submission_line(other_line) if other_line else None
            
            from config.prediction import PREDICTION_PROGRESS_INTERVALS
            
            while pref_data is not None or other_data is not None:
                if pref_data is None:
                    # Only other file has data
                    protein_id, term, score = other_data
                    out_file.write(f"{protein_id}\t{term}\t{format_prediction_score(score)}\n")
                    total_written += 1
                    other_count += 1
                    other_line = other_file.readline()
                    other_data = parse_submission_line(other_line) if other_line else None
                elif other_data is None:
                    # Only preferred file has data
                    protein_id, term, score = pref_data
                    out_file.write(f"{protein_id}\t{term}\t{format_prediction_score(score)}\n")
                    total_written += 1
                    preferred_count += 1
                    pref_line = pref_file.readline()
                    pref_data = parse_submission_line(pref_line) if pref_line else None
                else:
                    # Both files have data - compare keys
                    pref_key = (pref_data[0], pref_data[1])  # (protein_id, term)
                    other_key = (other_data[0], other_data[1])
                    
                    if pref_key < other_key:
                        # Preferred key comes first
                        protein_id, term, score = pref_data
                        out_file.write(f"{protein_id}\t{term}\t{format_prediction_score(score)}\n")
                        total_written += 1
                        preferred_count += 1
                        pref_line = pref_file.readline()
                        pref_data = parse_submission_line(pref_line) if pref_line else None
                    elif pref_key > other_key:
                        # Other key comes first
                        protein_id, term, score = other_data
                        out_file.write(f"{protein_id}\t{term}\t{format_prediction_score(score)}\n")
                        total_written += 1
                        other_count += 1
                        other_line = other_file.readline()
                        other_data = parse_submission_line(other_line) if other_line else None
                    else:
                        # Keys match - use preferred score
                        protein_id, term, score = pref_data
                        out_file.write(f"{protein_id}\t{term}\t{format_prediction_score(score)}\n")
                        total_written += 1
                        overlap_count += 1
                        # Advance both files
                        pref_line = pref_file.readline()
                        pref_data = parse_submission_line(pref_line) if pref_line else None
                        other_line = other_file.readline()
                        other_data = parse_submission_line(other_line) if other_line else None
                
                if total_written % PREDICTION_PROGRESS_INTERVALS["predictions"] == 0:
                    print(f"      Merged {total_written:,} predictions...")
        
        print(f"   ✓ Merged submissions: {total_written:,} predictions")
        print(f"   ✓ Preferred: {prefer}")
        print(f"   ✓ From preferred only: {preferred_count - overlap_count:,}")
        print(f"   ✓ From other only: {other_count:,}")
        print(f"   ✓ Overlapping (used preferred): {overlap_count:,}")
        
    finally:
        # Clean up temp files
        cleanup_temp_files([Path(temp1_path), Path(temp2_path)])
    
    return str(output_path)

