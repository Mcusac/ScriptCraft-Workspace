# dictionary_supplementer/utils.py

import pandas as pd
from scriptcraft.common.logging import log_and_print

def supplement_dictionary(dictionary_df: pd.DataFrame, supplement_df: pd.DataFrame, update_existing: bool = False) -> pd.DataFrame:
    """
    Merge supplement information into the cleaned dictionary.

    Args:
        dictionary_df (pd.DataFrame): Cleaned dictionary DataFrame.
        supplement_df (pd.DataFrame): Supplement DataFrame.
        update_existing (bool): If True, update existing variables' min-max info. Otherwise only add missing.

    Returns:
        pd.DataFrame: Updated dictionary DataFrame.
    """
    merged_df = dictionary_df.copy()

    added_vars = []
    updated_vars = []
    update_logs = []

    for _, row in supplement_df.iterrows():
        var_name = str(row.get("Main Variable")).strip()

        if not var_name:
            continue

        if var_name in merged_df["Main Variable"].values:
            if update_existing:
                idx_list = merged_df.index[merged_df["Main Variable"] == var_name].tolist()
                if idx_list:
                    idx = idx_list[0]
                    old_value = str(merged_df.at[idx, "Value"])
                    new_value = str(row.get("Value", old_value))

                    if old_value != new_value:
                        merged_df.at[idx, "Value"] = new_value
                        updated_vars.append(var_name)
                        update_logs.append(f"{var_name}: '{old_value}' → '{new_value}'")
        else:
            merged_df = pd.concat([merged_df, row.to_frame().T], ignore_index=True)
            added_vars.append(var_name)

    log_and_print(f"➕ Added {len(added_vars)} new variables: {added_vars if added_vars else 'None'}")
    if update_existing:
        log_and_print(f"🔄 Updated {len(updated_vars)} existing variables.")
        if update_logs:
            for log in update_logs:
                log_and_print(f"   - {log}")
    else:
        log_and_print("⚙️ Existing variables left unchanged (update_existing=False)")

    return merged_df