# scripts/qc/supplement_splitter/utils.py

from pathlib import Path
from scriptcraft.common.logging import log_and_print
from scriptcraft.common.io import load_data
from typing import Dict
import pandas as pd


def split_supplement_into_domains(cleaned_dicts: Dict[str, Path], full_supplement_path: Path, output_dir: Path) -> Dict[str, pd.DataFrame]:
    """Splits full supplement into per-domain subset based on each domain's cleaned dictionary."""

    if not full_supplement_path.exists():
        log_and_print(f"❌ Supplement file not found: {full_supplement_path}")
        return {}

    supplement_df = load_data(full_supplement_path)
    supplement_df["Main Variable"] = supplement_df["Main Variable"].astype(str).str.strip()

    leftovers = supplement_df.copy()
    domain_supplements: Dict[str, pd.DataFrame] = {}

    for domain, dict_path in cleaned_dicts.items():
        log_and_print(f"\n🔍 Splitting supplement for: {domain}")

        if not dict_path.exists():
            log_and_print(f"⚠️ Cleaned dictionary not found for {domain}: {dict_path}")
            continue

        dict_df = load_data(dict_path)
        domain_vars = set(dict_df["Main Variable"].dropna().astype(str).str.strip())

        matched = leftovers[leftovers["Main Variable"].isin(domain_vars)]
        leftovers = leftovers[~leftovers["Main Variable"].isin(domain_vars)]

        domain_supp_path = output_dir / f"{domain}_supplement.xlsx"
        matched.to_excel(domain_supp_path, index=False)
        domain_supplements[domain] = matched
        log_and_print(f"✅ Saved domain-specific supplement: {domain_supp_path}\nShape: {matched.shape}")

    leftovers_path = output_dir / "leftover_supplement.xlsx"
    leftovers.to_excel(leftovers_path, index=False)
    log_and_print(f"📁 Saved leftover variables: {leftovers_path.resolve()}\nShape: {leftovers.shape}")
    
    return domain_supplements