"""
Ontology iteration utilities for CAFA 6 protein function prediction.
Consolidates duplicate ontology iteration patterns across workflows.
"""

from typing import Dict, List, Generator, Tuple, Optional
from config import get_all_ontologies, get_ontology_name, ONTOLOGY_CODES


def iterate_ontologies_with_check(ontologies: Dict[str, str], 
                                 check_dict: Dict[str, any],
                                 skip_message: Optional[str] = None) -> Generator[Tuple[str, str], None, None]:
    """
    Iterate over ontologies with a check dictionary.
    Yields only ontologies that exist in check_dict.
    
    Args:
        ontologies: Dict mapping ont_code -> ont_name
        check_dict: Dict to check for ontology existence (e.g., y_train_dict, models_per_ontology)
        skip_message: Optional message to print when skipping (uses default if None)
        
    Yields:
        tuple: (ont_code, ont_name) for ontologies that exist in check_dict
    """
    default_skip_msg = " (no data)"
    skip_msg = skip_message if skip_message is not None else default_skip_msg
    
    for ont_code, ont_name in ontologies.items():
        if ont_code not in check_dict:
            if skip_msg:
                print(f"⚠️  Skipping {ont_name}{skip_msg}")
            continue
        yield (ont_code, ont_name)


def get_ontology_name_safe(ont_code: str) -> str:
    """
    Safely get ontology name with error handling.
    
    Args:
        ont_code: Ontology code ('F', 'P', 'C')
        
    Returns:
        str: Ontology name, or code itself if not found
    """
    try:
        return get_ontology_name(ont_code)
    except (ValueError, KeyError):
        return ont_code


def filter_ontologies_with_data(ont_codes: List[str], y_train_dict: Dict[str, any]) -> List[str]:
    """
    Filter ontology codes to only those with data in y_train_dict.
    
    Args:
        ont_codes: List of ontology codes to check
        y_train_dict: Dict mapping ont_code -> label matrix
        
    Returns:
        list: Filtered list of ontology codes that have data
    """
    return [ont_code for ont_code in ont_codes if ont_code in y_train_dict]


def get_ontology_codes_and_names(ontology_str: Optional[str] = None) -> Tuple[List[str], Dict[str, str]]:
    """
    Get ontology codes and names dict from string or all ontologies.
    
    Args:
        ontology_str: Optional comma-separated ontology codes (e.g., "F,P,C")
                     If None, returns all ontologies
        
    Returns:
        tuple: (ontology_codes, ontologies_dict) where ontologies_dict maps code -> name
    """
    if ontology_str:
        from utils.cli_utils import parse_comma_separated_string
        ont_codes = parse_comma_separated_string(ontology_str, strip=True, upper=True)
        ontologies = {code: get_ontology_name_safe(code) for code in ont_codes}
    else:
        ontologies = get_all_ontologies()
        ont_codes = list(ontologies.keys())
    
    return ont_codes, ontologies

