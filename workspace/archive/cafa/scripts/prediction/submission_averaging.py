"""
Submission file averaging for CAFA 6 protein function prediction.
Combines multiple submission files using various ensemble methods.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Optional, Dict, Tuple
from collections import defaultdict
from utils.logging import setup_logging, get_logger
from utils.utils_common import open_text_file
from prediction.ensemble import ensemble_predictions
from prediction.prediction_utils import is_valid_score, validate_go_term_format, cleanup_temp_files

logger = get_logger(__name__)


def load_submission(filepath: str) -> Dict[Tuple[str, str], float]:
    """
    Load submission file into dictionary format.
    
    Args:
        filepath: Path to submission.tsv file
        
    Returns:
        dict: {(protein_id, term): score}
        
    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format is invalid
    """
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"Submission file not found: {filepath}")
    
    setup_logging()
    logger.info(f"Loading: {filepath.name}")
    
    from prediction.prediction_utils import parse_submission_line
    
    predictions = {}
    
    with open_text_file(filepath, 'r') as f:
        for line_num, line in enumerate(f, 1):
            result = parse_submission_line(line)
            if result is None:
                # parse_submission_line returns None for empty/invalid lines
                # But we want to raise errors for invalid format
                line = line.strip()
                if line:  # Only raise error if line is not empty
                    parts = line.split('\t')
                    if len(parts) != 3:
                        raise ValueError(
                            f"Invalid format at line {line_num}: expected 3 tab-separated columns, got {len(parts)}"
                        )
                    # If format is correct but parse failed, it's a score issue
                    protein_id, term, score_str = parts
                    try:
                        score = float(score_str)
                        if not is_valid_score(score):
                            raise ValueError(f"Score out of range (0, 1]: {score}")
                    except ValueError as e:
                        raise ValueError(f"Invalid score at line {line_num}: {e}")
                continue
            
            protein_id, term, score = result
            predictions[(protein_id, term)] = score
    
    logger.info(f"      ✓ Loaded {len(predictions):,} predictions")
    return predictions


def average_submissions(submission_files: List[str],
                       weights: Optional[List[float]] = None,
                       output_path: Optional[str] = None,
                       ensemble_method: str = 'average',
                       **ensemble_kwargs) -> str:
    """
    Combine multiple submission files using various ensemble methods.
    Memory-efficient streaming implementation for large files.
    
    Args:
        submission_files: List of paths to submission files
        weights: Optional weights for weighted_average (must sum to 1.0)
        output_path: Optional output path (default: temp_averaged_submission.tsv)
        ensemble_method: Ensemble method ('average', 'weighted_average', 'max', 
                       'geometric_mean', 'rank_average', 'power_average', 'percentile')
        **ensemble_kwargs: Additional method-specific parameters:
            - power (float): Power for power_average method (default: 1.0)
            - percentile (float): Percentile for percentile method (default: 75.0)
        
    Returns:
        str: Path to ensembled submission file
        
    Raises:
        ValueError: If weights are invalid or files have incompatible format
    """
    import tempfile
    import heapq
    from prediction.submission_merging import _sort_file_external, parse_submission_line
    from prediction.prediction_utils import format_prediction_score, is_valid_score, validate_go_term_format, cleanup_temp_files
    
    if not submission_files:
        raise ValueError("submission_files cannot be empty")
    
    if len(submission_files) == 1:
        print("   ⚠️  Only one submission file provided, copying as-is")
        return submission_files[0]
    
    setup_logging()
    logger.info(f"Ensembling {len(submission_files)} submission files using method: {ensemble_method}")
    
    # Validate weights for weighted_average
    if ensemble_method == 'weighted_average':
        if weights is None:
            # Default to equal weights
            weights = [1.0 / len(submission_files)] * len(submission_files)
            logger.info(f"Using equal weights: {weights}")
        else:
            if len(weights) != len(submission_files):
                raise ValueError(
                    f"Number of weights ({len(weights)}) must match number of submission files ({len(submission_files)})"
                )
            if not np.isclose(sum(weights), 1.0):
                raise ValueError(f"Weights must sum to 1.0, got {sum(weights)}")
            logger.info(f"Weights: {weights}")
    
    # For 2 files, use merge (handled by workflow)
    # For 3+ files, use sorted streaming with grouping
    if len(submission_files) == 2:
        # Fallback to old method for 2 files (shouldn't happen, but handle it)
        logger.warning("2 files detected - consider using merge method instead")
    
    # Sort all files externally
    logger.info("Sorting submission files...")
    sorted_files = []
    temp_files = []
    
    try:
        for i, filepath in enumerate(submission_files):
            temp_sorted = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.tsv')
            temp_sorted_path = temp_sorted.name
            temp_sorted.close()
            temp_files.append(temp_sorted_path)
            
            logger.info(f"   Sorting file {i+1}/{len(submission_files)}...")
            _sort_file_external(filepath, temp_sorted_path)
            sorted_files.append(temp_sorted_path)
        
        # Stream through all sorted files simultaneously and group by (protein_id, term)
        logger.info("Streaming through sorted files and computing ensemble...")
        
        # Open all sorted files
        file_handles = [open_text_file(f, 'r') for f in sorted_files]
        file_iters = [iter(f) for f in file_handles]
        
        # Initialize heap with first line from each file
        heap = []
        for file_idx, file_iter in enumerate(file_iters):
            try:
                line = next(file_iter).strip()
                if line:
                    data = parse_submission_line(line)
                    if data:
                        protein_id, term, score = data
                        heapq.heappush(heap, ((protein_id, term), file_idx, score, line))
            except StopIteration:
                pass
        
        # Group by (protein_id, term) and compute ensemble
        from config.prediction import PREDICTION_PROGRESS_INTERVALS
        current_key = None
        current_scores_by_file = {}  # file_idx -> score
        total_written = 0
        
        # Set output path
        if output_path is None:
            output_path = 'temp_averaged_submission.tsv'
        output_path = Path(output_path)
        
        with open(output_path, 'w') as out_file:
            while heap:
                (protein_id, term), file_idx, score, line = heapq.heappop(heap)
                key = (protein_id, term)
                
                if current_key is None:
                    current_key = key
                    current_scores_by_file = {}
                
                if key == current_key:
                    # Same key - collect score (keep highest if duplicate from same file)
                    if file_idx not in current_scores_by_file:
                        current_scores_by_file[file_idx] = score
                    else:
                        # If same file has multiple entries for same key, keep max
                        current_scores_by_file[file_idx] = max(current_scores_by_file[file_idx], score)
                else:
                    # New key - process previous group
                    if current_scores_by_file:
                        # Build prediction matrix for this group
                        # Shape: (1, 1) since we're processing one (protein, term) at a time
                        prediction_vectors = []
                        for i in range(len(submission_files)):
                            if i in current_scores_by_file:
                                prediction_vectors.append(np.array([[current_scores_by_file[i]]], dtype=np.float32))
                            else:
                                prediction_vectors.append(np.array([[0.0]], dtype=np.float32))
                        
                        # Prepare kwargs for ensemble_predictions
                        ensemble_kwargs_final = ensemble_kwargs.copy()
                        if ensemble_method == 'weighted_average':
                            ensemble_kwargs_final['weights'] = weights
                        
                        # Compute ensemble
                        ensembled = ensemble_predictions(
                            predictions_list=prediction_vectors,
                            method=ensemble_method,
                            **ensemble_kwargs_final
                        )
                        
                        # Write if score > 0
                        final_score = ensembled.flat[0]
                        if final_score > 0:
                            out_file.write(f"{current_key[0]}\t{current_key[1]}\t{format_prediction_score(final_score)}\n")
                            total_written += 1
                            if total_written % PREDICTION_PROGRESS_INTERVALS["predictions"] == 0:
                                logger.info(f"      Processed {total_written:,} predictions...")
                    
                    # Start new group
                    current_key = key
                    current_scores_by_file = {file_idx: score}
                
                # Get next line from this file
                try:
                    next_line = next(file_iters[file_idx]).strip()
                    if next_line:
                        next_data = parse_submission_line(next_line)
                        if next_data:
                            next_protein_id, next_term, next_score = next_data
                            heapq.heappush(heap, ((next_protein_id, next_term), file_idx, next_score, next_line))
                except StopIteration:
                    pass
            
            # Process last group
            if current_scores_by_file:
                prediction_vectors = []
                for i in range(len(submission_files)):
                    if i in current_scores_by_file:
                        prediction_vectors.append(np.array([[current_scores_by_file[i]]], dtype=np.float32))
                    else:
                        prediction_vectors.append(np.array([[0.0]], dtype=np.float32))
                
                ensemble_kwargs_final = ensemble_kwargs.copy()
                if ensemble_method == 'weighted_average':
                    ensemble_kwargs_final['weights'] = weights
                
                ensembled = ensemble_predictions(
                    predictions_list=prediction_vectors,
                    method=ensemble_method,
                    **ensemble_kwargs_final
                )
                
                final_score = ensembled.flat[0]
                if final_score > 0:
                    out_file.write(f"{current_key[0]}\t{current_key[1]}\t{final_score:.3g}\n")
                    total_written += 1
        
        # Close file handles
        for f in file_handles:
            f.close()
        
        logger.info(f"✓ Wrote {total_written:,} ensembled predictions")
        
    finally:
        # Clean up temp files
        cleanup_temp_files([Path(f) for f in temp_files])
    
    return str(output_path)


def validate_submission_format(filepath: str) -> Tuple[bool, List[str]]:
    """
    Validate submission file format.
    Memory-efficient: only reads sample lines, doesn't load entire file.
    
    Args:
        filepath: Path to submission file
        
    Returns:
        tuple: (is_valid: bool, issues: List[str])
    """
    issues = []
    
    filepath = Path(filepath)
    if not filepath.exists():
        issues.append(f"File not found: {filepath}")
        return False, issues
    
    try:
        from config.prediction import VALIDATION_SAMPLE_SIZE
        sample_size = VALIDATION_SAMPLE_SIZE
        line_count = 0
        valid_predictions = 0
        
        with open_text_file(filepath, 'r') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                
                line_count += 1
                
                # Only validate first sample_size lines
                if line_count > sample_size:
                    break
                
                parts = line.split('\t')
                if len(parts) != 3:
                    issues.append(
                        f"Invalid format at line {line_num}: expected 3 tab-separated columns, got {len(parts)}"
                    )
                    return False, issues
                
                protein_id, term, score_str = parts
                
                # Check GO term format
                is_valid_term, term_error = validate_go_term_format(term)
                if not is_valid_term:
                    issues.append(f"Invalid GO term at line {line_num}: {term_error}")
                    return False, issues
                
                # Check score format
                try:
                    score = float(score_str)
                    if not is_valid_score(score):
                        issues.append(f"Score out of range at line {line_num}: {score} (expected 0 < score <= 1.0)")
                        return False, issues
                    valid_predictions += 1
                except ValueError:
                    issues.append(f"Invalid score format at line {line_num}: {score_str}")
                    return False, issues
        
        # Check if file is empty
        if line_count == 0:
            issues.append("File contains no predictions")
            return False, issues
        
        if valid_predictions == 0:
            issues.append("File contains no valid predictions")
            return False, issues
        
    except Exception as e:
        issues.append(f"Failed to read file: {e}")
        return False, issues
    
    if issues:
        return False, issues
    
    return True, []

