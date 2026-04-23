"""
Unified feature extraction interface for CAFA 6 protein function prediction.
Auto-selects optimal memory strategy based on dataset size.
Defaults to memory-efficient chunked extraction with memmap for large datasets.
"""

from typing import Dict, List, Tuple, Union, Optional
from pathlib import Path
import numpy as np

from config.features import (
    parse_model_feature_config,
    get_embedding_feature_types,
    HANDCRAFTED_FEATURE_KEY,
    INDIVIDUAL_FEATURES,
    BATCH_SIZE_CONFIG,
    FEATURE_EXTRACTION_MEMORY_THRESHOLD_MB
)
from preprocessing.feature_engineering import extract_handcrafted_parallel
from preprocessing.data_streaming import load_embeddings_memmap
from preprocessing.feature_engineering.embeddings import align_embeddings
from preprocessing.feature_streaming import extract_features_batch
from utils.memory_efficient import should_use_memmap, estimate_memory_usage, save_features_memmap_with_metadata
from utils.utils_common import cleanup_memory
from config.paths import DATA_OUTPUT_DIR


def extract_features(sequences: Dict[str, str],
                    config: Dict,
                    protein_ids: Optional[List[str]] = None,
                    datatype: str = 'train',
                    force_memmap: Optional[bool] = None,
                    chunk_size: Optional[int] = None) -> Tuple[Union[np.ndarray, Path], List[str]]:
    """
    Unified feature extraction interface with automatic memory optimization.
    
    Auto-selects optimal strategy based on dataset size:
    - Small datasets (<500MB): Load full arrays (fast)
    - Medium datasets (500MB-2GB): Chunked extraction, return full array
    - Large datasets (>2GB): Chunked extraction + memmap (default)
    
    Args:
        sequences: Dict mapping protein_id -> sequence
        config: Model configuration dict (or feature_type/features tuple)
        protein_ids: Optional list of protein IDs to extract for (if None, uses all sequences)
        datatype: 'train' or 'test'
        force_memmap: Force memmap usage (True) or disable (False). None = auto-detect
        chunk_size: Optional chunk size override (defaults to config)
        
    Returns:
        tuple: (features, protein_ids)
            - features: Feature matrix (np.ndarray) or memmap path (Path) for large datasets
            - protein_ids: List of aligned protein IDs
    """
    # Parse feature configuration
    if isinstance(config, dict):
        feature_type, features = parse_model_feature_config(config)
    elif isinstance(config, tuple):
        feature_type, features = config
    else:
        raise ValueError(f"Invalid config type: {type(config)}. Expected dict or tuple.")
    
    # Filter sequences if protein_ids provided
    if protein_ids is not None:
        sequences = {pid: sequences[pid] for pid in protein_ids if pid in sequences}
    
    target_ids = list(sequences.keys())
    
    if not target_ids:
        raise ValueError("No sequences to extract features from")
    
    # Route to appropriate extraction method
    if feature_type == 'fused_embeddings' and features:
        # Fused embeddings: always use chunked extraction (memory-efficient)
        return _extract_fused_features(
            sequences=sequences,
            features=features,
            datatype=datatype,
            target_ids=target_ids,
            force_memmap=force_memmap,
            chunk_size=chunk_size
        )
    elif feature_type == 'hand_crafted':
        # Handcrafted features: extract all at once (fast, small memory footprint)
        return _extract_handcrafted_features(
            sequences=sequences,
            target_ids=target_ids
        )
    elif feature_type == 'embeddings' and features and len(features) == 1:
        # Single embedding: use memmap loading
        return _extract_single_embedding(
            sequences=sequences,
            embedding_type=features[0],
            datatype=datatype,
            target_ids=target_ids
        )
    else:
        raise ValueError(
            f"Unsupported feature configuration: type={feature_type}, features={features}. "
            f"Supported: 'fused_embeddings' with features list, 'hand_crafted', or single 'embeddings'"
        )


def _extract_fused_features(sequences: Dict[str, str],
                           features: List[str],
                           datatype: str,
                           target_ids: List[str],
                           force_memmap: Optional[bool],
                           chunk_size: Optional[int]) -> Tuple[Union[np.ndarray, Path], List[str]]:
    """
    Extract fused features using chunked extraction (memory-efficient).
    Always uses chunked extraction to avoid loading full embedding arrays.
    Writes chunks directly to memmap file to avoid accumulating all chunks in memory.
    """
    if chunk_size is None:
        chunk_size = BATCH_SIZE_CONFIG["data_loading"]["embedding_chunk_size"]
    
    if not features:
        raise ValueError("No features specified for fused feature extraction")
    
    print(f"   Extracting fused features: {features}")
    print(f"   Using chunk size: {chunk_size:,} proteins per chunk")
    
    # Check for preprocessed combined embeddings first
    embedding_types = get_embedding_feature_types()
    embedding_only_features = [f for f in features if f in embedding_types]
    
    # Separate structured features (taxonomy, ppi, top_terms)
    structured_feature_types = ['taxonomy', 'taxonomy_highlevel', 'taxonomy_top500', 'ppi', 'top_terms']
    structured_features = [f for f in features if f in structured_feature_types]
    
    if embedding_only_features:
        from preprocessing.feature_engineering.embeddings.embeddings_v1 import load_combined_embeddings
        combined_result = load_combined_embeddings(
            embedding_types=embedding_only_features,
            datatype=datatype,
            use_memmap=True
        )
        
        if combined_result is not None:
            print(f"   ✓ Using preprocessed combined embeddings: {embedding_only_features}")
            combined_embeds, combined_ids = combined_result
            
            # If only embeddings (no handcrafted), return combined directly
            if HANDCRAFTED_FEATURE_KEY not in features:
                # Align to target_ids
                from preprocessing.feature_engineering.embeddings.embeddings_v1 import align_embeddings
                aligned_embeds, aligned_ids = align_embeddings(combined_embeds, combined_ids, target_ids)
                
                if force_memmap:
                    # Save as memmap if requested
                    memmap_dir = DATA_OUTPUT_DIR / 'memmap_cache'
                    memmap_dir.mkdir(parents=True, exist_ok=True)
                    memmap_path = memmap_dir / f'combined_embeddings_{datatype}_{len(aligned_ids)}.npy'
                    memmap = np.memmap(memmap_path, dtype=np.float32, mode='w+', shape=aligned_embeds.shape)
                    memmap[:] = aligned_embeds
                    return memmap_path, aligned_ids
                else:
                    return aligned_embeds, aligned_ids
            else:
                # Has handcrafted features - will need to combine with HC later
                # Store combined embeddings for later use
                embedding_data = {'combined': (combined_embeds, combined_ids)}
                id_sets = [set(str(pid) for pid in combined_ids)]
                print(f"   ✓ Using preprocessed combined embeddings, will add handcrafted features")
        else:
            # Fall back to individual loading
            print(f"   Combined embeddings not found, loading individual embeddings...")
            embedding_data = {}
            id_sets = []
            
            for feat in embedding_only_features:
                print(f"   Loading embedding: {feat} (memory-mapped)...")
                embeds_memmap, ids = load_embeddings_memmap(feat, datatype)
                embedding_data[feat] = (embeds_memmap, ids)
                # Normalize IDs: extract accession from full UniProt format (sp|Q8VY15|NAME → Q8VY15)
                normalized_ids = []
                for pid in ids:
                    pid_str = str(pid)
                    if '|' in pid_str:
                        # Format: sp|Q8VY15|RBM25_ARATH → extract Q8VY15
                        parts = pid_str.split('|')
                        if len(parts) >= 2:
                            normalized_ids.append(parts[1])
                        else:
                            normalized_ids.append(pid_str)
                    else:
                        normalized_ids.append(pid_str)
                id_set = set(normalized_ids)
                id_sets.append(id_set)
                print(f"      Loaded {len(id_set):,} protein IDs (sample: {list(id_set)[:3] if len(id_set) > 0 else []})")
    else:
        # No embeddings, only handcrafted
        embedding_data = {}
        id_sets = []
    
    # Step 1: Find common protein IDs using set intersection (NO dense arrays)
    # This replaces align_embeddings() which was creating ~3GB of dense arrays
    if id_sets:
        # First, find intersection of embedding IDs only (for diagnostics)
        embedding_intersection = set.intersection(*id_sets) if len(id_sets) > 1 else id_sets[0]
        print(f"   Intersection of {len(id_sets)} embedding types: {len(embedding_intersection):,} proteins")
        
        # Include target_ids in intersection to ensure we only keep proteins that exist in both
        # embeddings AND sequences
        target_id_set = set(str(pid) for pid in target_ids)
        print(f"   Sequence IDs: {len(target_id_set):,} proteins (sample: {list(target_id_set)[:3] if len(target_id_set) > 0 else []})")
        
        all_id_sets = id_sets + [target_id_set]
        common_id_set = set.intersection(*all_id_sets)
        # Convert back to list maintaining order from target_ids
        common_ids = [pid for pid in target_ids if str(pid) in common_id_set]
        print(f"   Found {len(common_ids):,} common proteins across {len(id_sets)} embedding types and sequences")
        
        if len(common_ids) == 0:
            # Diagnostic: check if embedding intersection exists but doesn't match sequences
            if len(embedding_intersection) > 0:
                print(f"   [WARNING] Embeddings have {len(embedding_intersection):,} common proteins, but none match sequence IDs")
                # Check overlap
                overlap = embedding_intersection & target_id_set
                print(f"   [WARNING] Overlap between embedding IDs and sequence IDs: {len(overlap):,} proteins")
                if len(overlap) == 0 and len(embedding_intersection) > 0 and len(target_id_set) > 0:
                    # Show sample IDs to help debug format mismatch
                    emb_sample = list(embedding_intersection)[:3]
                    seq_sample = list(target_id_set)[:3]
                    print(f"   [DEBUG] Sample embedding IDs: {emb_sample}")
                    print(f"   [DEBUG] Sample sequence IDs: {seq_sample}")
    else:
        common_ids = target_ids
    
    # Step 2: Calculate total feature dimension upfront (before chunk loop)
    total_feature_dim = 0
    part_dims = []
    for feat in features:
        if feat == HANDCRAFTED_FEATURE_KEY:
            # HANDCRAFTED_FEATURE_KEY is 'hc'
            dim = INDIVIDUAL_FEATURES.get('hc', {}).get('dimensions', 90)
            label = 'handcrafted'
        elif feat in INDIVIDUAL_FEATURES:
            dim = INDIVIDUAL_FEATURES[feat]['dimensions']
            label = feat
        else:
            dim = 0
            label = feat
        
        total_feature_dim += dim
        part_dims.append(f"{label}({dim})")
    
    dims = ' + '.join(part_dims)
    print(f"   Total feature dimension: {total_feature_dim} = {dims}")
    
    # Step 3: Determine memmap usage upfront (before chunk loop)
    estimated_size_mb = (len(common_ids) * total_feature_dim * 4) / (1024 * 1024)  # float32 = 4 bytes
    save_as_memmap = force_memmap
    if save_as_memmap is None:
        # Auto-detect based on estimated size
        save_as_memmap = estimated_size_mb >= FEATURE_EXTRACTION_MEMORY_THRESHOLD_MB
    
    print(f"   Estimated feature matrix size: {estimated_size_mb:.1f}MB ({len(common_ids):,} × {total_feature_dim})")
    
    # Step 4: Build ID-to-index mappings once per embedding type (outside chunk loop)
    # Helper function to normalize ID (extract accession from full UniProt format)
    def normalize_protein_id(pid: str) -> str:
        """Normalize protein ID: sp|Q8VY15|NAME → Q8VY15"""
        if '|' in pid:
            parts = pid.split('|')
            if len(parts) >= 2:
                return parts[1]
        return pid
    
    id_mappings = {}
    using_combined = 'combined' in embedding_data
    
    if using_combined:
        # Using preprocessed combined embeddings
        combined_embeds, combined_ids = embedding_data['combined']
        id_mappings['combined'] = {normalize_protein_id(str(pid)): i for i, pid in enumerate(combined_ids)}
    else:
        # Using individual embeddings
        for feat in features:
            if feat in embedding_types:
                embeds_memmap, ids = embedding_data[feat]
                id_mappings[feat] = {normalize_protein_id(str(pid)): i for i, pid in enumerate(ids)}
    
    # Step 5: Process chunks - write directly to memmap if needed (never accumulate)
    all_protein_ids = []
    
    if save_as_memmap:
        # Process first chunk to get actual feature dimension (more reliable than config)
        # This ensures memmap shape matches actual feature dimensions
        first_chunk_ids = common_ids[:min(chunk_size, len(common_ids))]
        first_chunk_feature_parts = []
        
        for feat in features:
            if feat in embedding_types or (using_combined and feat not in [HANDCRAFTED_FEATURE_KEY]):
                if using_combined:
                    # Use combined embeddings
                    combined_embeds, combined_ids = embedding_data['combined']
                    id_to_idx = id_mappings['combined']
                    chunk_indices = [id_to_idx[str(pid)] for pid in first_chunk_ids if str(pid) in id_to_idx]
                    
                    if chunk_indices:
                        chunk_embeds = combined_embeds[chunk_indices].copy()
                        first_chunk_feature_parts.append(chunk_embeds.astype(np.float32))
                    else:
                        raise ValueError(f"No embeddings found for first chunk proteins")
                else:
                    # Use individual embeddings
                    embeds_memmap, ids = embedding_data[feat]
                    id_to_idx = id_mappings[feat]
                    chunk_indices = [id_to_idx[str(pid)] for pid in first_chunk_ids if str(pid) in id_to_idx]
                    
                    if chunk_indices:
                        chunk_embeds = embeds_memmap[chunk_indices].copy()
                        first_chunk_feature_parts.append(chunk_embeds.astype(np.float32))
                    else:
                        raise ValueError(f"No embeddings found for first chunk proteins")
                    
            elif feat == HANDCRAFTED_FEATURE_KEY:
                chunk_seqs = {pid: sequences[pid] for pid in first_chunk_ids if pid in sequences}
                hc_features = extract_features_batch(chunk_seqs, first_chunk_ids, 'hand_crafted')
                first_chunk_feature_parts.append(hc_features)
            elif feat in structured_features:
                # Load structured features (taxonomy, ppi, top_terms)
                from preprocessing.feature_engineering.structured_features import (
                    load_taxonomy_features, load_ppi_features, load_top_terms_features,
                    align_structured_features
                )
                
                if feat.startswith('taxonomy'):
                    taxonomy_level = feat.replace('taxonomy', '').replace('_', '') or 'default'
                    struct_features, struct_ids = load_taxonomy_features(datatype, taxonomy_level)
                elif feat == 'ppi':
                    struct_features, struct_ids = load_ppi_features(datatype)
                elif feat == 'top_terms':
                    struct_features, struct_ids = load_top_terms_features(datatype)
                else:
                    raise ValueError(f"Unknown structured feature: {feat}")
                
                # Align to chunk IDs
                aligned_features, aligned_ids = align_structured_features(
                    struct_features, struct_ids, first_chunk_ids
                )
                first_chunk_feature_parts.append(aligned_features.astype(np.float32))
            else:
                raise ValueError(f"Unknown feature in fused extraction: {feat}")
        
        # Get actual feature dimension from first chunk
        first_chunk_features = np.hstack(first_chunk_feature_parts)
        actual_feature_dim = first_chunk_features.shape[1]
        
        if actual_feature_dim != total_feature_dim:
            print(f"   ⚠️  Feature dimension mismatch: calculated {total_feature_dim}, actual {actual_feature_dim}")
            print(f"   Using actual dimension: {actual_feature_dim}")
            total_feature_dim = actual_feature_dim
        
        # Create memmap file with actual shape
        # Check if memmap file already exists and can be reused
        memmap_dir = DATA_OUTPUT_DIR / 'memmap_cache'
        memmap_dir.mkdir(parents=True, exist_ok=True)
        memmap_path = memmap_dir / f'fused_features_{datatype}_{len(common_ids)}.npy'
        metadata_path = memmap_path.with_suffix('.npy.meta')
        
        # Check if existing memmap file matches our requirements
        reuse_existing = False
        if memmap_path.exists() and metadata_path.exists():
            try:
                import json
                with open(metadata_path, 'r') as f:
                    existing_metadata = json.load(f)
                existing_shape = tuple(existing_metadata['shape'])
                if existing_shape == (len(common_ids), total_feature_dim):
                    print(f"   ♻️  Reusing existing memmap file: {memmap_path}")
                    reuse_existing = True
                else:
                    print(f"   ⚠️  Existing memmap shape mismatch: {existing_shape} vs ({len(common_ids)}, {total_feature_dim}) - creating new file")
            except Exception as e:
                print(f"   ⚠️  Could not read existing memmap metadata: {e} - creating new file")
        
        if reuse_existing:
            # File already exists and matches - skip extraction, just return the path
            print(f"   ✓ Skipping feature extraction - memmap file already exists and matches")
            # Still need to build all_protein_ids list for return value
            all_protein_ids = common_ids.copy()
            # Clean up first chunk memory since we're not using it
            del first_chunk_features, first_chunk_feature_parts
            cleanup_memory()
        else:
            # Create new memmap file
            memmap = np.memmap(memmap_path, dtype=np.float32, mode='w+', 
                              shape=(len(common_ids), total_feature_dim))
            print(f"   💾 Created memmap file: {memmap_path} (shape: {memmap.shape})")
            
            # Write first chunk to memmap
            memmap[0:len(first_chunk_ids), :] = first_chunk_features
            all_protein_ids.extend(first_chunk_ids)
            
            # Free first chunk memory
            del first_chunk_features, first_chunk_feature_parts
            cleanup_memory()
            
            # Process remaining chunks and write directly to memmap
            total_chunks = (len(common_ids) + chunk_size - 1) // chunk_size
            print(f"   Processing {len(common_ids):,} proteins in {total_chunks} chunks (writing directly to memmap)...")
            print(f"      Processed chunk 1/{total_chunks} ({len(first_chunk_ids):,} proteins)")
            
            for chunk_idx in range(chunk_size, len(common_ids), chunk_size):
                chunk_ids = common_ids[chunk_idx:chunk_idx+chunk_size]
                chunk_start = chunk_idx
                chunk_end = min(chunk_idx + chunk_size, len(common_ids))
                chunk_feature_parts = []
                
                # Extract each feature type for this chunk
                for feat in features:
                    if feat in embedding_types or (using_combined and feat not in [HANDCRAFTED_FEATURE_KEY]):
                        if using_combined:
                            # Use combined embeddings
                            combined_embeds, combined_ids = embedding_data['combined']
                            id_to_idx = id_mappings['combined']
                            chunk_indices = [id_to_idx[str(pid)] for pid in chunk_ids if str(pid) in id_to_idx]
                            
                            if chunk_indices:
                                chunk_embeds = combined_embeds[chunk_indices].copy()
                                chunk_feature_parts.append(chunk_embeds.astype(np.float32))
                            else:
                                raise ValueError(f"No embeddings found for chunk proteins")
                        else:
                            # Use individual embeddings
                            embeds_memmap, ids = embedding_data[feat]
                            id_to_idx = id_mappings[feat]
                            chunk_indices = [id_to_idx[str(pid)] for pid in chunk_ids if str(pid) in id_to_idx]
                            
                            if chunk_indices:
                                chunk_embeds = embeds_memmap[chunk_indices].copy()
                                chunk_feature_parts.append(chunk_embeds.astype(np.float32))
                            else:
                                raise ValueError(f"No embeddings found for chunk proteins")
                            
                    elif feat == HANDCRAFTED_FEATURE_KEY:
                        # Extract handcrafted features for this chunk
                        chunk_seqs = {pid: sequences[pid] for pid in chunk_ids if pid in sequences}
                        hc_features = extract_features_batch(chunk_seqs, chunk_ids, 'hand_crafted')
                        chunk_feature_parts.append(hc_features)
                    else:
                        raise ValueError(f"Unknown feature in fused extraction: {feat}")
                
                # Concatenate features for this chunk
                chunk_features = np.hstack(chunk_feature_parts)
                
                # Write directly to memmap at correct offset (never accumulate)
                memmap[chunk_start:chunk_end, :] = chunk_features
                all_protein_ids.extend(chunk_ids)
                
                chunk_num = (chunk_idx // chunk_size) + 1  # +1 because first chunk was already processed
                print(f"      Processed chunk {chunk_num}/{total_chunks} ({len(chunk_ids):,} proteins)")
                
                # Free chunk memory immediately
                del chunk_features, chunk_feature_parts
                cleanup_memory()
            
            # Flush memmap to disk
            memmap.flush()
            del memmap
        
        # Save metadata
        import json
        metadata_path = memmap_path.with_suffix('.npy.meta')
        metadata = {
            'shape': [len(common_ids), total_feature_dim],
            'dtype': 'float32',
            'size_mb': estimated_size_mb
        }
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        print(f"   💾 Saved features as memmap: {memmap_path} ({len(common_ids):,} × {total_feature_dim}, {estimated_size_mb:.1f}MB)")
        
        # Clean up embedding data
        del embedding_data, id_mappings
        cleanup_memory()
        
        return memmap_path, all_protein_ids
    
    else:
        # Small dataset - accumulate chunks (only for small datasets)
        all_features = []
        total_chunks = (len(common_ids) + chunk_size - 1) // chunk_size
        print(f"   Processing {len(common_ids):,} proteins in {total_chunks} chunks (small dataset - accumulating)...")
        
        for chunk_idx in range(0, len(common_ids), chunk_size):
            chunk_ids = common_ids[chunk_idx:chunk_idx+chunk_size]
            chunk_feature_parts = []
            
            # Extract each feature type for this chunk
            for feat in features:
                if feat in embedding_types or (using_combined and feat not in [HANDCRAFTED_FEATURE_KEY]):
                    if using_combined:
                        # Use combined embeddings
                        combined_embeds, combined_ids = embedding_data['combined']
                        id_to_idx = id_mappings['combined']
                        chunk_indices = [id_to_idx[str(pid)] for pid in chunk_ids if str(pid) in id_to_idx]
                        
                        if chunk_indices:
                            chunk_embeds = combined_embeds[chunk_indices].copy()
                            chunk_feature_parts.append(chunk_embeds.astype(np.float32))
                        else:
                            raise ValueError(f"No embeddings found for chunk proteins")
                    else:
                        # Use individual embeddings
                        embeds_memmap, ids = embedding_data[feat]
                        id_to_idx = id_mappings[feat]
                        chunk_indices = [id_to_idx[str(pid)] for pid in chunk_ids if str(pid) in id_to_idx]
                        
                        if chunk_indices:
                            chunk_embeds = embeds_memmap[chunk_indices].copy()
                            chunk_feature_parts.append(chunk_embeds.astype(np.float32))
                        else:
                            raise ValueError(f"No embeddings found for chunk proteins")
                        
                elif feat == HANDCRAFTED_FEATURE_KEY:
                    chunk_seqs = {pid: sequences[pid] for pid in chunk_ids if pid in sequences}
                    hc_features = extract_features_batch(chunk_seqs, chunk_ids, 'hand_crafted')
                    chunk_feature_parts.append(hc_features)
                elif feat in structured_features:
                    # Load structured features (taxonomy, ppi, top_terms)
                    from preprocessing.feature_engineering.structured_features import (
                        load_taxonomy_features, load_ppi_features, load_top_terms_features,
                        align_structured_features
                    )
                    
                    if feat.startswith('taxonomy'):
                        taxonomy_level = feat.replace('taxonomy', '').replace('_', '') or 'default'
                        struct_features, struct_ids = load_taxonomy_features(datatype, taxonomy_level)
                    elif feat == 'ppi':
                        struct_features, struct_ids = load_ppi_features(datatype)
                    elif feat == 'top_terms':
                        struct_features, struct_ids = load_top_terms_features(datatype)
                    else:
                        raise ValueError(f"Unknown structured feature: {feat}")
                    
                    # Align to chunk IDs
                    aligned_features, aligned_ids = align_structured_features(
                        struct_features, struct_ids, chunk_ids
                    )
                    chunk_feature_parts.append(aligned_features.astype(np.float32))
                else:
                    raise ValueError(f"Unknown feature in fused extraction: {feat}")
            
            chunk_features = np.hstack(chunk_feature_parts)
            all_features.append(chunk_features)
            all_protein_ids.extend(chunk_ids)
            
            print(f"      Processed chunk {chunk_idx//chunk_size + 1}/{total_chunks} ({len(chunk_ids):,} proteins)")
            
            del chunk_features, chunk_feature_parts
            cleanup_memory()
        
        # Stack all chunks (only for small datasets)
        X_fused = np.vstack(all_features)
        print(f"   Fused features: {X_fused.shape} = {dims}")
        
        # Clean up
        del embedding_data, id_mappings, all_features
        cleanup_memory()
        
        return X_fused, all_protein_ids


def _extract_handcrafted_features(sequences: Dict[str, str],
                                 target_ids: List[str]) -> Tuple[np.ndarray, List[str]]:
    """
    Extract handcrafted features (always returns full array - small memory footprint).
    """
    print(f"   Extracting handcrafted features for {len(target_ids):,} proteins...")
    features = extract_handcrafted_parallel(sequences, target_ids)
    print(f"   ✓ Handcrafted features: {features.shape}")
    return features, target_ids


def _extract_single_embedding(sequences: Dict[str, str],
                              embedding_type: str,
                              datatype: str,
                              target_ids: List[str]) -> Tuple[Union[np.ndarray, Path], List[str]]:
    """
    Extract single embedding type (uses memmap loading).
    """
    print(f"   Loading {embedding_type} embeddings (memory-mapped)...")
    
    # Load as memmap (read-only, on-disk)
    embeds_memmap, ids = load_embeddings_memmap(embedding_type, datatype)
    
    # Align to target sequences
    aligned, aligned_ids = align_embeddings(embeds_memmap, ids, target_ids)
    
    # Estimate memory usage
    estimated_mb, _ = estimate_memory_usage(aligned)
    
    # For large datasets, return memmap path instead of array
    if estimated_mb >= FEATURE_EXTRACTION_MEMORY_THRESHOLD_MB:
        from utils.memory_efficient import save_features_memmap_with_metadata
        from config.paths import DATA_OUTPUT_DIR
        
        memmap_dir = DATA_OUTPUT_DIR / 'memmap_cache'
        memmap_dir.mkdir(parents=True, exist_ok=True)
        memmap_path = memmap_dir / f'{embedding_type}_{datatype}_{len(aligned_ids)}.npy'
        memmap_path = save_features_memmap_with_metadata(aligned, memmap_path)
        print(f"   💾 Saved features as memmap: {memmap_path} ({aligned.shape}, {estimated_mb:.1f}MB)")
        
        # Free memory
        del aligned
        cleanup_memory()
        return memmap_path, aligned_ids
    else:
        print(f"   ✓ Extracted embeddings: {aligned.shape} ({estimated_mb:.1f}MB)")
        return aligned, aligned_ids

