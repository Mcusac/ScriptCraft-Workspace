"""
Workflow prediction utilities for CAFA 6 protein function prediction.
Handles writing predictions to submission files.
"""

from typing import List, Any
import numpy as np

from prediction.prediction_utils import format_prediction_score, is_valid_score


def write_predictions_to_file(submission_file,
                             proteins: List[str],
                             predictions: np.ndarray,
                             mlb: Any,
                             threshold: float,
                             max_preds: int) -> int:
    """
    Write predictions to submission file.
    Consolidated prediction writing logic.
    
    Args:
        submission_file: File handle to write to
        proteins: List of protein IDs
        predictions: Prediction probabilities (n_samples, n_terms)
        mlb: MultiLabelBinarizer with classes_ attribute
        threshold: Prediction threshold
        max_preds: Maximum predictions per ontology
        
    Returns:
        int: Number of predictions written
    """
    predictions_written = 0
    
    for i, pid in enumerate(proteins):
        probs = predictions[i]
        top_indices = np.argsort(probs)[-max_preds:][::-1]
        
        for idx in top_indices:
            prob = probs[idx]
            if prob > threshold:
                term = mlb.classes_[idx]
                prob_str = format_prediction_score(prob)
                prob_float = float(prob_str)
                if is_valid_score(prob_float):
                    submission_file.write(f"{pid}\t{term}\t{prob_str}\n")
                    predictions_written += 1
    
    return predictions_written

