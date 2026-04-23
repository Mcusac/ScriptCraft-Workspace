# aggregate_train.py
# Aggregate train.csv from 5 rows per image to 1 row per image

import pandas as pd
from pathlib import Path
from typing import Union, Optional
import logging
import warnings

from config.evaluation_constants import ALL_TARGETS

# Import contest data schema
try:
    from contest.registry import get_contest_data_schema
    _get_data_schema = get_contest_data_schema
except (ImportError, ValueError) as e:
    # Fallback to direct CSIRO import if registry not available
    warnings.warn(
        f"Could not load contest data schema from registry: {e}. "
        f"Falling back to direct CSIRO import.",
        UserWarning
    )
    from contest.csiro.data_schema import get_csiro_data_schema
    _get_data_schema = get_csiro_data_schema

logger = logging.getLogger(__name__)


def aggregate_train_csv(
    train_csv_path: Union[str, Path],
    output_path: Optional[Union[str, Path]] = None,
    data_root: Optional[Union[str, Path]] = None
) -> pd.DataFrame:
    """
    Aggregate train.csv from 5 rows per image (one per target) to 1 row per image.
    
    Original format: 5 rows per image with columns: sample_id, image_path, target_name, target, ...
    Aggregated format: 1 row per image with columns: image_id, image_path, Dry_Green_g, Dry_Clover_g, ...
    
    Args:
        train_csv_path: Path to train.csv
        output_path: Optional path to save aggregated CSV
        data_root: Optional data root for constructing full image paths
        
    Returns:
        Aggregated DataFrame with one row per image
    """
    train_csv_path = Path(train_csv_path)
    
    if not train_csv_path.exists():
        raise FileNotFoundError(f"Train CSV not found: {train_csv_path}")
    
    logger.info(f"Loading train.csv from {train_csv_path}")
    train_df = pd.read_csv(train_csv_path)
    
    # Get contest data schema for column names and sample_id parsing
    data_schema = _get_data_schema()
    
    # Parse sample_id using contest schema
    # CSIRO-SPECIFIC: Split sample_id into prefix (image_id) and suffix (target_name)
    # Uses contest schema to parse sample_id format
    sample_id_col = data_schema.sample_id_column
    if sample_id_col not in train_df.columns:
        raise ValueError(f"Missing required column '{sample_id_col}' in train.csv")
    
    # Parse sample IDs using contest schema
    parsed_ids = train_df[sample_id_col].apply(data_schema.parse_sample_id)
    train_df['sample_id_prefix'] = [p['image_id'] for p in parsed_ids]
    train_df['sample_id_suffix'] = [p['target_name'] for p in parsed_ids]
    
    # Verify that suffix matches target_name
    target_name_col = data_schema.target_name_column
    if not (train_df['sample_id_suffix'] == train_df[target_name_col]).all():
        logger.warning("Some sample_id suffixes don't match target_name")
    
    # Get metadata columns from contest schema
    # CSIRO-SPECIFIC: Columns to group by (metadata columns) - now uses contest schema
    metadata_cols = data_schema.metadata_columns
    # Remove 'image_id' from metadata_cols for groupby (we'll add sample_id_prefix)
    groupby_cols = ['sample_id_prefix', data_schema.image_path_column] + [
        col for col in metadata_cols if col not in ['image_id', 'image_path']
    ]
    
    # Aggregate: pivot target values into columns
    logger.info("Aggregating data...")
    target_name_col = data_schema.target_name_column
    target_value_col = data_schema.target_value_column
    agg_train_df = train_df.groupby(groupby_cols).apply(
        lambda df: df.set_index(target_name_col)[target_value_col]
    ).reset_index()
    agg_train_df.columns.name = None
    
    # Rename sample_id_prefix to image_id for clarity
    agg_train_df.rename(columns={'sample_id_prefix': 'image_id'}, inplace=True)
    
    # Ensure all target columns exist
    for col in ALL_TARGETS:
        if col not in agg_train_df.columns:
            agg_train_df[col] = 0.0
    
    # Reorder columns: image_id, image_path, metadata, targets
    # Uses contest schema for metadata columns
    metadata_cols_ordered = data_schema.metadata_columns
    other_cols = [col for col in agg_train_df.columns if col not in metadata_cols_ordered + ALL_TARGETS]
    agg_train_df = agg_train_df[metadata_cols_ordered + ALL_TARGETS + other_cols]
    
    logger.info(f"Aggregated to {len(agg_train_df)} images (from {len(train_df)} rows)")
    
    # Save if output path provided
    if output_path:
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        agg_train_df.to_csv(output_path, index=False)
        logger.info(f"Saved aggregated CSV to {output_path}")
    
    return agg_train_df

