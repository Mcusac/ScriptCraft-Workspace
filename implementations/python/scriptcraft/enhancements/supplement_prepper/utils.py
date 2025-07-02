# scripts/qc/supplement_prepper/utils.py

import pandas as pd
from pathlib import Path
from typing import List, Dict, Any
from scriptcraft.common.logging import log_and_print


def merge_and_clean_supplement(file_paths: List[Path], output_path: Path) -> None:
    """
    Merge and clean supplement files.
    
    Args:
        file_paths: List of paths to supplement files
        output_path: Path where to save the merged output
    """
    log_and_print("🔄 Merging supplement files...")

    merged = pd.DataFrame()
    for file in file_paths:
        if not file.exists():
            log_and_print(f"❌ File not found: {file}")
            continue
        log_and_print(f"📄 Loading: {file.name}")
        df = pd.read_excel(file)
        merged = pd.concat([merged, df], ignore_index=True)

    if merged.empty:
        log_and_print("⚠️ No data to merge. Exiting...")
        return

    # Clean up columns
    merged = merged.loc[:, ~merged.columns.str.contains("^Unnamed", na=False)]
    merged = merged.dropna(axis=1, how='all')
    merged = merged.fillna("")

    # Build final structured rows
    final_rows: List[Dict[str, Any]] = []
    for _, row in merged.iterrows():
        variable = str(row.get('variable')).strip()
        label = str(row.get('notes')).strip()
        min_val = row.get('min')
        max_val = row.get('max')

        if not variable or variable.lower() == 'nan':
            continue

        try:
            if str(min_val).strip() and str(max_val).strip():
                min_val = int(float(min_val))
                max_val = int(float(max_val))
                value = f"{{{min_val}-{max_val}}}"
            else:
                value = "Numeric"
        except Exception:
            value = "Numeric"

        final_rows.append({
            "Main Variable": variable,
            "Label": label,
            "Value": value,
            "Missing/Unit of Measure": "-9999",
            "Level of quality check": "Supplement",
            "Visits": "",
            "Notes": "",
        })

    final_df = pd.DataFrame(final_rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_excel(output_path, index=False)

    log_and_print(f"✅ Merged supplement dictionary saved to: {output_path.resolve()}")