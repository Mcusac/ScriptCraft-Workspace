"""
Ontology configuration for CAFA 6 protein function prediction.
Single source of truth for ontology codes and names.
"""

# Ontology code to name mapping
ONTOLOGY_MAP = {
    'F': 'MFO',  # Molecular Function Ontology
    'P': 'BPO',  # Biological Process Ontology
    'C': 'CCO'   # Cellular Component Ontology
}

# Reverse mapping: name to code
ONTOLOGY_NAME_TO_CODE = {name: code for code, name in ONTOLOGY_MAP.items()}

# All ontology codes
ONTOLOGY_CODES = list(ONTOLOGY_MAP.keys())

# All ontology names
ONTOLOGY_NAMES = list(ONTOLOGY_MAP.values())


def get_ontology_name(ont_code: str) -> str:
    """
    Get ontology name from code.
    
    Args:
        ont_code: Ontology code ('F', 'P', 'C')
        
    Returns:
        str: Ontology name ('MFO', 'BPO', 'CCO')
        
    Raises:
        ValueError: If ont_code is invalid
    """
    if ont_code not in ONTOLOGY_MAP:
        raise ValueError(f"Invalid ontology code: {ont_code}. Must be one of {ONTOLOGY_CODES}")
    return ONTOLOGY_MAP[ont_code]


def get_ontology_code(ont_name: str) -> str:
    """
    Get ontology code from name.
    
    Args:
        ont_name: Ontology name ('MFO', 'BPO', 'CCO')
        
    Returns:
        str: Ontology code ('F', 'P', 'C')
        
    Raises:
        ValueError: If ont_name is invalid
    """
    if ont_name not in ONTOLOGY_NAME_TO_CODE:
        raise ValueError(f"Invalid ontology name: {ont_name}. Must be one of {ONTOLOGY_NAMES}")
    return ONTOLOGY_NAME_TO_CODE[ont_name]


def get_all_ontologies() -> dict:
    """
    Get all ontology mappings.
    
    Returns:
        dict: {code: name} mapping
    """
    return ONTOLOGY_MAP.copy()

