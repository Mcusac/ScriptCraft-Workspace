# dictionary_validator/utils.py

def compare_columns(dataset_cols, dictionary_cols):
    """Compare dataset vs dictionary column sets and return a detailed dictionary."""
    dataset_cols = set(dataset_cols)
    dictionary_cols = set(dictionary_cols)

    in_both = dataset_cols & dictionary_cols
    only_in_dataset = dataset_cols - dictionary_cols
    only_in_dictionary = dictionary_cols - dataset_cols

    # Case-insensitive mismatch detection
    lower_dataset = {col.lower(): col for col in dataset_cols}
    lower_dict = {col.lower(): col for col in dictionary_cols}
    case_mismatches = [
        lower_dataset[name] for name in (set(lower_dataset) & set(lower_dict))
        if lower_dataset[name] != lower_dict[name]
    ]

    return {
        "in_both": in_both,
        "only_in_dataset": only_in_dataset,
        "only_in_dictionary": only_in_dictionary,
        "case_mismatches": case_mismatches
    }

