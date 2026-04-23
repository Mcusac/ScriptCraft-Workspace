"""
Prediction and submission generation for CAFA 6 protein function prediction.
Extracted from starter_model.py for modularity.
"""

import numpy as np
import pandas as pd
import os
import shutil
from pathlib import Path
from typing import Optional
from Bio import SeqIO
from preprocessing.feature_engineering import extract_handcrafted_parallel
from prediction.prediction_utils import format_prediction_score, is_valid_score
from utils.utils_common import cleanup_memory, open_text_file
from prediction.submission_merging import parse_submission_line


def load_test_sequences(test_dir):
    """
    Load test sequences from FASTA file.
    
    Args:
        test_dir: Path to data/input/Test directory
        
    Returns:
        tuple: (test_seqs, test_proteins)
    """
    print("\n[7/9] Loading test sequences...")
    
    test_seqs = {}
    test_proteins = []
    
    for rec in SeqIO.parse(test_dir / 'testsuperset.fasta', 'fasta'):
        pid = rec.id.split('|')[1] if '|' in rec.id else rec.id
        test_seqs[pid] = str(rec.seq)
        test_proteins.append(pid)
    
    print(f"   ✓ Loaded {len(test_seqs):,} test sequences")
    return test_seqs, test_proteins


def make_predictions(models, mlb_dict, test_seqs, test_proteins, output_dir, 
                    batch_size=None, prediction_threshold=None, 
                    max_preds_per_ont=None, write_batch_size=None,
                    feature_type='hand_crafted', features=None,
                    propagate_predictions=False,
                    per_ontology_feature_configs=None):
    """
    Make predictions for test sequences and write to temporary file.
    
    Args:
        models: dict mapping ont_code -> trained model (or path for MLP models)
        mlb_dict: dict mapping ont_code -> MultiLabelBinarizer
        test_seqs: dict mapping protein_id -> sequence
        test_proteins: list of protein IDs
        output_dir: Path to output directory
        batch_size: Number of proteins to process at once
        prediction_threshold: Minimum probability threshold
        max_preds_per_ont: Maximum predictions per ontology
        write_batch_size: Write to disk every N predictions
        feature_type: Feature extraction method ('hand_crafted' or 'fused_embeddings') - used if per_ontology_feature_configs is None
        features: List of features to use for fused_embeddings (e.g., ['protbert','esm2','hc']) - used if per_ontology_feature_configs is None
        propagate_predictions: Whether to propagate predictions up the GO hierarchy
        per_ontology_feature_configs: Optional dict mapping ont_code -> (feature_type, features) for mixed feature configs
        
    Returns:
        str: Path to temporary submission file
    """
    # Import config for defaults
    from config import PREDICTION_SETTINGS, get_all_ontologies, DATA_INPUT_DIR
    
    # Get default settings from config if not provided
    pred_settings = PREDICTION_SETTINGS
    if batch_size is None:
        batch_size = pred_settings["batch_size"]
    if prediction_threshold is None:
        prediction_threshold = pred_settings["prediction_threshold"]
    if max_preds_per_ont is None:
        max_preds_per_ont = pred_settings["max_preds_per_ont"]
    if write_batch_size is None:
        write_batch_size = pred_settings["write_batch_size"]
    if propagate_predictions is None:
        propagate_predictions = pred_settings.get("propagate_predictions", False)
    
    # Load OBO file and prepare parents map if prediction propagation is enabled
    parents_map = None
    if propagate_predictions:
        from utils.go_utils import parse_obo_file
        obo_path = DATA_INPUT_DIR / 'Train' / 'go-basic.obo'
        if obo_path.exists():
            print("   Loading GO ontology for prediction propagation...")
            parents_map, _ = parse_obo_file(obo_path)
        else:
            print(f"   ⚠️  Warning: OBO file not found at {obo_path}, skipping prediction propagation")
            propagate_predictions = False
    
    print("\n[8/9] Making predictions and writing to disk...")
    
    # Configuration for memory efficiency
    ontologies = get_all_ontologies()
    
    # Determine if we need per-ontology feature extraction
    use_per_ontology_features = per_ontology_feature_configs is not None
    
    if not use_per_ontology_features:
        # Extract features once for all test proteins (before ontology loop)
        # This avoids re-loading embeddings for each batch/ontology
        # Use unified extraction interface with automatic memory optimization
        print("   Extracting features for all test proteins...")
        from preprocessing.feature_extraction import extract_features
        from pathlib import Path
        
        # Build config dict for unified interface
        if feature_type == 'fused_embeddings':
            if not features:
                raise ValueError("Features list is required for fused_embeddings during prediction")
            extraction_config = {'feature_type': feature_type, 'features': features}
        else:
            extraction_config = {'feature_type': feature_type}
        
        X_test_result, aligned_test_proteins = extract_features(
            sequences=test_seqs,
            config=extraction_config,
            protein_ids=test_proteins,
            datatype='test',
            force_memmap=None  # Auto-detect - may return memmap for large test sets
        )
        
        # Handle memmap path (load into array for prediction)
        if isinstance(X_test_result, Path):
            from utils.memory_efficient import load_features_memmap
            X_test_all = np.array(load_features_memmap(X_test_result))
            print(f"   ✓ Loaded features from memmap: {X_test_result}")
        else:
            X_test_all = X_test_result
        
        # Create mapping from aligned protein IDs to indices
        protein_to_idx = {pid: idx for idx, pid in enumerate(aligned_test_proteins)}
        print(f"   ✓ Extracted features for {len(aligned_test_proteins):,} proteins (shape: {X_test_all.shape})")
    
    # Temporary file path
    temp_submission_path = output_dir / 'temp_submission.tsv'
    total_predictions_written = 0
    
    # Open file for writing (will overwrite if exists)
    with open(temp_submission_path, 'w') as submission_file:
        
        for ont_code, ont_name in ontologies.items():
            if ont_code not in models:
                continue
            
            print(f"   Predicting {ont_name}...")
            
            # Extract features per ontology if needed
            if use_per_ontology_features:
                ont_feature_type, ont_features = per_ontology_feature_configs[ont_code]
                print(f"      Extracting features: {ont_feature_type} {ont_features if ont_features else ''}")
                
                from preprocessing.feature_extraction import extract_features
                from pathlib import Path
                
                # Build config dict for this ontology
                if ont_feature_type == 'fused_embeddings':
                    if not ont_features:
                        raise ValueError(f"Features list is required for fused_embeddings for {ont_code}")
                    extraction_config = {'feature_type': ont_feature_type, 'features': ont_features}
                else:
                    extraction_config = {'feature_type': ont_feature_type}
                
                X_test_result, aligned_test_proteins = extract_features(
                    sequences=test_seqs,
                    config=extraction_config,
                    protein_ids=test_proteins,
                    datatype='test',
                    force_memmap=None
                )
                
                # Handle memmap path (load into array for prediction)
                if isinstance(X_test_result, Path):
                    from utils.memory_efficient import load_features_memmap
                    X_test_all = np.array(load_features_memmap(X_test_result))
                else:
                    X_test_all = X_test_result
                
                protein_to_idx = {pid: idx for idx, pid in enumerate(aligned_test_proteins)}
                print(f"      ✓ Extracted features: {len(aligned_test_proteins):,} proteins (shape: {X_test_all.shape})")
            
            model_data = models[ont_code]
            mlb = mlb_dict[ont_code]
            n_terms = len(mlb.classes_)
            
            # Handle both on-disk paths and in-memory models
            is_pytorch_model = False
            if isinstance(model_data, str):
                # It's a path to a saved model
                print(f"      Loading MLP model from disk: {model_data}")
                from utils.model_io import load_model as load_pytorch_model
                from models.nn import MLPModel
                from utils.gpu_utils import get_device
                import torch
                
                device = get_device()
                model, metadata = load_pytorch_model(model_data, model_class=MLPModel, device=device)
                
                # If we got a state_dict instead of model instance, reconstruct
                if isinstance(model, dict) and 'state_dict' in model:
                    model_config = model.get('config', {})
                    model = MLPModel(**model_config).to(device)
                    model.load_state_dict(model['state_dict'])
                    model.eval()
                
                is_pytorch_model = True
            else:
                # It's an in-memory model object
                # Check if it's a PyTorch model
                if hasattr(model_data, 'state_dict'):
                    model = model_data
                    is_pytorch_model = True
                    device = next(model.parameters()).device
                else:
                    model = model_data
                    is_pytorch_model = False
            
            # GPU wrapping now handled by prepare_model_for_inference() in utils/model_prediction.py
            # No need to wrap here - predict_with_model() handles it automatically
            
            # Process in batches using pre-extracted features
            # Use aligned_test_proteins for batching (some proteins may have been filtered during feature extraction)
            n_batches = (len(aligned_test_proteins) + batch_size - 1) // batch_size
            ont_predictions = 0
            batch_buffer = []
            
            for batch_idx in range(n_batches):
                start_idx = batch_idx * batch_size
                end_idx = min((batch_idx + 1) * batch_size, len(aligned_test_proteins))
                batch_protein_indices = list(range(start_idx, end_idx))
                batch_pids = [aligned_test_proteins[idx] for idx in batch_protein_indices]
                
                # Get pre-extracted features for this batch
                X_batch = X_test_all[batch_protein_indices]
                proteins_to_process = batch_pids
                
                # Get predictions for this batch using unified prediction interface
                if is_pytorch_model:
                    # Get model config for temperature scaling
                    # model_data could be a path or model object, get config from metadata if available
                    model_config = {}
                    if hasattr(model, 'hyperparams'):
                        # Try to get config from model metadata
                        model_config = {'hyperparams': getattr(model, 'hyperparams', {})}
                    else:
                        # Default config
                        model_config = {'hyperparams': {'temperature_scaling': 1.5}}
                    
                    from utils.model_prediction import predict_with_model
                    y_pred_proba = predict_with_model(
                        model=model,
                        X=X_batch,
                        model_config=model_config,
                        device=device
                    )
                    
                    # Clean up GPU memory after each batch using centralized utility
                    from utils.gpu_utils import cleanup_gpu_memory
                    cleanup_gpu_memory()
                else:
                    # Use sklearn model
                    y_pred_proba = model.predict_proba(X_batch)
                
                # Propagate predictions up GO graph if enabled
                if propagate_predictions and parents_map:
                    from utils.go_utils import propagate_predictions_batch
                    from config.prediction import PREDICTION_SETTINGS
                    pred_settings = PREDICTION_SETTINGS
                    iterations = pred_settings.get("prediction_propagation_iterations", 3)
                    
                    y_pred_proba = propagate_predictions_batch(
                        y_pred_proba, parents_map, list(mlb.classes_), iterations=iterations
                    )
                
                # Process each protein in the batch
                # Use proteins_to_process which matches the dimensions of X_batch and y_pred_proba
                for i, pid in enumerate(proteins_to_process):
                    probs = y_pred_proba[i]
                    
                    # Get top predictions
                    top_indices = np.argsort(probs)[-max_preds_per_ont:][::-1]
                    
                    for idx in top_indices:
                        prob = probs[idx]
                        
                        # Only include predictions above threshold
                        if prob > prediction_threshold:
                            term = mlb.classes_[idx]
                            prob_str = format_prediction_score(prob)
                            
                            # Ensure probability is in valid range (0, 1.000]
                            prob_float = float(prob_str)
                            if is_valid_score(prob_float):
                                batch_buffer.append(f"{pid}\t{term}\t{prob_str}\n")
                                ont_predictions += 1
                
                # CRITICAL: Delete large prediction matrix immediately after processing
                # For large ontologies (350k terms), this can be several GB per batch
                del y_pred_proba
                del X_batch
                cleanup_memory()
                
                # Write buffer to disk periodically
                if len(batch_buffer) >= write_batch_size:
                    submission_file.writelines(batch_buffer)
                    total_predictions_written += len(batch_buffer)
                    batch_buffer = []
                
                # Progress update
                from config.prediction import PREDICTION_PROGRESS_INTERVALS
                if (batch_idx + 1) % PREDICTION_PROGRESS_INTERVALS["batch"] == 0 or (batch_idx + 1) == n_batches:
                    print(f"      Batch {batch_idx+1}/{n_batches} complete "
                          f"({end_idx:,}/{len(test_proteins):,} proteins, "
                          f"{ont_predictions:,} predictions for this ontology)")
            
            # Write remaining buffer for this ontology
            if batch_buffer:
                submission_file.writelines(batch_buffer)
                total_predictions_written += len(batch_buffer)
                batch_buffer = []
            
            print(f"      ✓ {ont_name} complete: {ont_predictions:,} predictions written")
            
            # Clean up GPU and CPU memory after each ontology (for PyTorch models)
            if is_pytorch_model:
                from utils.gpu_utils import cleanup_gpu_memory
                cleanup_gpu_memory()
            
            # Force garbage collection to free any remaining prediction arrays
            cleanup_memory()
    
    print(f"   ✓ Total predictions written: {total_predictions_written:,}")
    
    # Final cleanup: free feature matrix after all ontologies are done
    del X_test_all
    cleanup_memory()
    
    return temp_submission_path


def post_process_submission(temp_submission_path, output_dir, output_name=None,
                           apply_goa_filter: bool = False,
                           extra_output_name: Optional[str] = None):
    """
    Post-process submission file to enforce 1500 term limit per protein.
    Uses memory-efficient chunked processing to avoid loading all predictions into RAM.
    Optionally applies GOA negative propagation filtering.
    
    Args:
        temp_submission_path: Path to temporary submission file
        output_dir: Path to output directory
        output_name: Optional custom output filename (default: 'submission.tsv')
        apply_goa_filter: If True, apply GOA negative propagation filtering
        extra_output_name: Optional filename for a descriptive copy of submission.tsv
        
    Returns:
        str: Path to final submission file
    """
    import heapq
    from collections import defaultdict
    
    print("\n[9/9] Post-processing submission file...")
    print("   Enforcing 1500 terms per protein limit...")
    
    if output_name is None:
        output_name = 'submission.tsv'
    final_submission_path = output_dir / output_name
    
    # Memory-efficient approach: group predictions by protein
    # Use heap to keep only top 1500 per protein during accumulation
    print("   Reading and grouping predictions by protein...")
    from collections import defaultdict
    import heapq
    
    protein_predictions = defaultdict(list)  # protein -> heap of (score, term) tuples (min-heap for top-k)
    line_count = 0
    from config.prediction import MAX_PREDICTIONS_PER_PROTEIN
    max_preds_per_protein = MAX_PREDICTIONS_PER_PROTEIN
    
    with open_text_file(temp_submission_path, 'r') as temp_file:
        for line in temp_file:
            parsed = parse_submission_line(line)
            if parsed:
                protein, term, score = parsed
                line_count += 1
                    
                # Use min-heap to keep only top 1500 predictions per protein
                # Min-heap stores (score, term), with smallest score at root
                # When full, we replace the smallest (root) if current score is larger
                if len(protein_predictions[protein]) < max_preds_per_protein:
                    heapq.heappush(protein_predictions[protein], (score, term))
                else:
                    # If heap is full, check if current score is larger than smallest
                    # heap[0] is the smallest element (root of min-heap)
                    min_score, _ = protein_predictions[protein][0]
                    if score > min_score:
                        heapq.heapreplace(protein_predictions[protein], (score, term))
                
                # Periodic cleanup and progress
                from config.prediction import PREDICTION_PROGRESS_INTERVALS
                if line_count % PREDICTION_PROGRESS_INTERVALS["large_file"] == 0:
                    cleanup_memory()
                    print(f"      Processed {line_count:,} predictions...")
    
    print(f"   Loaded {line_count:,} predictions for {len(protein_predictions):,} proteins")
    
    # Convert heaps to sorted lists and write to file
    print("   Sorting and writing top predictions per protein...")
    final_count = 0
    processed_proteins = 0
    
    with open(final_submission_path, 'w') as final_file:
        for protein, preds in protein_predictions.items():
            # Convert heap to sorted list (descending by score)
            sorted_preds = sorted(preds, reverse=True)
            
            for score, term in sorted_preds:
                score_str = format_prediction_score(score)
                final_file.write(f"{protein}\t{term}\t{score_str}\n")
                final_count += 1
            
            processed_proteins += 1
            from config.prediction import PREDICTION_PROGRESS_INTERVALS
            if processed_proteins % PREDICTION_PROGRESS_INTERVALS["proteins"] == 0:
                print(f"      Processed {processed_proteins:,} proteins...")
                # Periodic cleanup
                cleanup_memory()
    
    # Clean up protein_predictions dictionary
    del protein_predictions
    cleanup_memory()
    
    print(f"   ✓ Final submission saved to {final_submission_path}")
    print(f"   ✓ Total predictions in submission: {final_count:,}")
    print(f"   ✓ Proteins with predictions: {processed_proteins:,}")
    
    # Remove temporary file
    if os.path.exists(temp_submission_path):
        os.remove(temp_submission_path)
        print("   ✓ Temporary file cleaned up")
    
    # Display sample and statistics (memory-efficient)
    print("\n   Loading sample for display...")
    sample_df = pd.read_csv(final_submission_path, sep='\t', header=None, 
                            names=['protein', 'term', 'score'], nrows=10)
    print("\n   Sample predictions:")
    print(sample_df.to_string(index=False))
    
    # Calculate statistics (streaming approach)
    print("\n   Calculating statistics...")
    protein_counts = {}
    with open_text_file(final_submission_path, 'r') as f:
        for line in f:
            protein = line.split('\t')[0]
            protein_counts[protein] = protein_counts.get(protein, 0) + 1
    
    preds_per_protein = list(protein_counts.values())
    print(f"\n   Prediction statistics:")
    print(f"      Mean predictions per protein: {np.mean(preds_per_protein):.1f}")
    print(f"      Median predictions per protein: {np.median(preds_per_protein):.0f}")
    print(f"      Max predictions per protein: {max(preds_per_protein)}")
    print(f"      Min predictions per protein: {min(preds_per_protein)}")
    
    # Apply GOA negative propagation filtering if requested
    if apply_goa_filter:
        try:
            from prediction.goa_postprocessing import apply_goa_filtering
            from config.paths import GOA_ANNOTATIONS_PATH, DATA_INPUT_DIR
            
            print("\n🔬 Applying GOA negative propagation filtering...")
            
            # Build paths
            go_obo_path = DATA_INPUT_DIR / 'Train' / 'go-basic.obo'
            goa_annotations_path = GOA_ANNOTATIONS_PATH
            
            if not go_obo_path.exists():
                print(f"   ⚠️  Warning: OBO file not found at {go_obo_path}, skipping GOA filtering")
            elif not goa_annotations_path.exists():
                print(f"   ⚠️  Warning: GOA annotations not found at {goa_annotations_path}, skipping GOA filtering")
            else:
                # Apply filtering
                filtered_path = apply_goa_filtering(
                    str(final_submission_path),
                    str(goa_annotations_path),
                    str(go_obo_path),
                    str(final_submission_path.with_suffix('')) + '_filtered.tsv'
                )
                
                # Replace original with filtered version
                import shutil
                shutil.move(filtered_path, final_submission_path)
                print(f"   ✓ GOA filtering complete, updated submission saved")
        except Exception as e:
            print(f"   ⚠️  Warning: GOA filtering failed: {e}")
            print(f"   Continuing with unfiltered submission...")
    
    # Create descriptive copy if extra_output_name is provided
    if extra_output_name:
        extra_path = output_dir / extra_output_name
        shutil.copy2(final_submission_path, extra_path)
        print(f"   ✓ Copy created: {extra_output_name}")
    
    return final_submission_path
