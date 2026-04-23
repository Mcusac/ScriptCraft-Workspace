"""
CLI utilities for CAFA 6 protein function prediction.
Contains business logic for parsing CLI arguments and model specifications.
Separated from run.py to keep CLI interface focused.
"""

from typing import Dict, Tuple, Optional, List, Any
from config import get_model_config, get_model_config_by_type_version, get_ontology_name, ONTOLOGY_CODES


def parse_comma_separated_string(s: str, strip: bool = True, upper: bool = False) -> List[str]:
    """
    Parse comma-separated string into list of strings.
    
    Args:
        s: Comma-separated string (e.g., "a,b,c" or "a, b, c")
        strip: If True, strip whitespace from each item
        upper: If True, convert each item to uppercase
        
    Returns:
        list: List of parsed strings
    """
    if not s:
        return []
    
    items = s.split(',')
    if strip:
        items = [item.strip() for item in items]
    if upper:
        items = [item.upper() for item in items]
    
    return items


def parse_comma_separated_floats(s: str) -> List[float]:
    """
    Parse comma-separated string into list of floats.
    
    Args:
        s: Comma-separated string of numbers (e.g., "0.5,0.3,0.2")
        
    Returns:
        list: List of floats
        
    Raises:
        ValueError: If any value cannot be converted to float
    """
    if not s:
        return []
    
    items = parse_comma_separated_string(s, strip=True, upper=False)
    try:
        return [float(item) for item in items]
    except ValueError as e:
        raise ValueError(f"Invalid float value in comma-separated string '{s}': {e}")


def parse_model_spec(spec: str) -> Tuple[str, str]:
    """
    Parse model specification string.
    
    Examples:
        'logistic_regression:1.0' -> ('logistic_regression', '1.0')
        'xgboost:1' -> ('xgboost', '1')
        'mlp:v3.1' -> ('mlp', '3.1')  # 'v' prefix is stripped
        'logistic_v1_1' -> ('logistic_regression', '1.1')
    
    Args:
        spec: Model specification string (either 'type:version' or model config name)
    
    Returns:
        tuple: (model_type, version) where version is a string (normalized, 'v' prefix stripped)
    """
    if ':' in spec:
        model_type, version = spec.split(':', 1)
        # Strip leading 'v' prefix if present (normalize to match MODEL_CONFIGS format)
        if version.startswith('v'):
            version = version[1:]
        # Keep version as string - model_io.py handles both int and string versions
        return (model_type, version)
    else:
        # Assume it's a model config name
        model_config = get_model_config(spec)
        return (model_config['type'], model_config['version'])


def parse_model_specs_from_args(args) -> Optional[Dict[str, Tuple[str, str]]]:
    """
    Parse model specifications from CLI arguments.
    Handles both single model (--model) and per-ontology models (--model-mfo/--model-bpo/--model-cco).
    
    Args:
        args: Parsed argparse arguments
        
    Returns:
        dict: Mapping of ont_code -> (model_type, version) or None if not applicable
    """
    model_specs = {}
    
    # If --model is provided, use it for all ontologies (convenience)
    if args.model:
        model_tuple = parse_model_spec(args.model)
        model_specs['F'] = model_tuple
        model_specs['P'] = model_tuple
        model_specs['C'] = model_tuple
    else:
        # Otherwise, use per-ontology specs
        if args.model_mfo:
            model_specs['F'] = parse_model_spec(args.model_mfo)
        if args.model_bpo:
            model_specs['P'] = parse_model_spec(args.model_bpo)
        if args.model_cco:
            model_specs['C'] = parse_model_spec(args.model_cco)
    
    return model_specs if model_specs else None


def validate_submissions_arg(args, parser) -> None:
    """
    Validate submissions argument for pipelines that require it.
    
    Args:
        args: Parsed argparse arguments
        parser: ArgumentParser instance for raising errors
    """
    if not hasattr(args, 'submissions') or not args.submissions:
        parser.error("--submissions is required for this pipeline")


def validate_pipeline_args(args, parser) -> None:
    """
    Validate pipeline arguments and raise parser errors if invalid.
    
    Args:
        args: Parsed argparse arguments
        parser: ArgumentParser instance for raising errors
    """
    if not args.pipeline:
        parser.error("--pipeline is required")
    
    if args.pipeline in ['full_pipeline', 'train_only', 'grid_search'] and not args.model:
        parser.error(f"--model is required for pipeline '{args.pipeline}'")
    
    if args.pipeline == 'train_single_ont' and not args.ontology:
        parser.error("--ontology is required for single ontology training")
    
    if args.pipeline == 'predict_from_saved':
        model_specs = parse_model_specs_from_args(args)
        if not model_specs:
            parser.error("At least one model specification is required for prediction (use --model or --model-mfo/--model-bpo/--model-cco)")
    
    if args.pipeline in ['average_submissions', 'get_all_averages']:
        validate_submissions_arg(args, parser)


def validate_ontology_codes(ontology_str: str) -> list:
    """
    Validate and parse ontology codes from comma-separated string.
    
    Args:
        ontology_str: Comma-separated ontology codes (e.g., "F,P,C" or "CCO")
        
    Returns:
        list: Valid ontology codes
        
    Raises:
        ValueError: If any ontology code is invalid
    """
    # Use centralized parser
    ont_codes = parse_comma_separated_string(ontology_str, strip=True, upper=True)
    
    # Validate against known ontology codes
    valid_ont_codes = [o for o in ont_codes if o in ONTOLOGY_CODES]
    
    if len(valid_ont_codes) != len(ont_codes):
        invalid = set(ont_codes) - set(valid_ont_codes)
        raise ValueError(f"Invalid ontology codes: {invalid}. Valid codes: {ONTOLOGY_CODES}")
    
    return valid_ont_codes


def parse_weights(weights_str: str) -> List[float]:
    """
    Parse weights from comma-separated string.
    
    Args:
        weights_str: Comma-separated string of weights (e.g., "0.5,0.3,0.2")
        
    Returns:
        list: List of floats, or empty list if weights_str is None/empty
    """
    if not weights_str:
        return []
    return parse_comma_separated_floats(weights_str)


def normalize_weights(weights: List[float]) -> List[float]:
    """
    Normalize weights to sum to 1.0.
    
    Args:
        weights: List of weight values
        
    Returns:
        list: Normalized weights that sum to 1.0
        
    Raises:
        ValueError: If sum of weights is zero
    """
    if not weights:
        return []
    
    total = sum(weights)
    if total == 0:
        raise ValueError("Cannot normalize weights: sum is zero")
    
    return [w / total for w in weights]


def validate_and_adjust_weights(weights: List[float], expected_count: int) -> List[float]:
    """
    Validate and adjust weights to match expected count.
    If weights don't match count, renormalize them.
    
    Args:
        weights: List of weight values
        expected_count: Expected number of weights
        
    Returns:
        list: Adjusted and normalized weights
    """
    if not weights:
        return []
    
    if len(weights) != expected_count:
        # Adjust to match expected count (take first N or pad with equal weights)
        if len(weights) > expected_count:
            weights = weights[:expected_count]
        else:
            # Pad with equal weights
            remaining = expected_count - len(weights)
            equal_weight = (1.0 - sum(weights)) / remaining if remaining > 0 else 0.0
            weights = weights + [equal_weight] * remaining
    
    return normalize_weights(weights)


def build_ensemble_kwargs(ensemble_method: str, power: Optional[float] = None, 
                          percentile: Optional[float] = None, **kwargs) -> Dict[str, Any]:
    """
    Build ensemble kwargs dictionary based on ensemble method.
    
    Args:
        ensemble_method: Ensemble method name ('power_average', 'percentile', etc.)
        power: Power parameter for power_average method
        percentile: Percentile parameter for percentile method
        **kwargs: Additional kwargs to include
        
    Returns:
        dict: Ensemble kwargs dictionary
    """
    ensemble_kwargs = {}
    
    if ensemble_method == 'power_average' and power is not None:
        ensemble_kwargs['power'] = power
    elif ensemble_method == 'percentile' and percentile is not None:
        ensemble_kwargs['percentile'] = percentile
    
    # Add any additional kwargs
    ensemble_kwargs.update(kwargs)
    
    return ensemble_kwargs


def get_model_config_safe(model_type: str, version: str, ont_code: Optional[str] = None) -> Dict[str, Any]:
    """
    Safely get model config by type and version with error handling.
    
    Args:
        model_type: Model type ('lr', 'xgb', 'nn')
        version: Model version (e.g., '1.0')
        ont_code: Optional ontology code for error messages
        
    Returns:
        dict: Model configuration
        
    Raises:
        ValueError: If model config not found
    """
    try:
        return get_model_config_by_type_version(model_type, version)
    except ValueError as e:
        ont_msg = f" on {ont_code}" if ont_code else ""
        raise ValueError(f"Model config not found for {model_type} v{version}{ont_msg}: {e}")


def parse_feature_override(args, parser) -> Optional[Dict[str, Any]]:
    """
    Parse feature override from CLI arguments.
    
    Args:
        args: Parsed argparse arguments
        parser: ArgumentParser instance for raising errors
        
    Returns:
        dict: Updated model config with feature override, or None if no override
    """
    if not args.features:
        return None
    
    from config.features import parse_feature_spec, validate_feature_availability, INDIVIDUAL_FEATURES
    
    try:
        features = parse_feature_spec(args.features)
        # Validate immediately to fail fast
        emb_features = [f for f in features if INDIVIDUAL_FEATURES.get(f, {}).get('type') == 'embedding']
        ok, missing = validate_feature_availability(emb_features)
        if not ok:
            parser.error("Missing embedding files: " + ", ".join(missing))
        
        return {
            'feature_type': 'fused_embeddings',
            'features': features
        }
    except ValueError as e:
        parser.error(f"Invalid feature specification: {e}")


def parse_ontology_arg(ontology_str: str) -> Tuple[List[str], List[str]]:
    """
    Parse ontology argument and return codes and names.
    
    Args:
        ontology_str: Comma-separated ontology codes or single code
        
    Returns:
        tuple: (ontology_codes, ontology_names)
    """
    ont_codes = parse_comma_separated_string(ontology_str, strip=True, upper=True)
    ont_names = [get_ontology_name(code) if code in ONTOLOGY_CODES else code for code in ont_codes]
    return ont_codes, ont_names


def parse_ensemble_models(args, parser) -> Dict[str, List[str]]:
    """
    Parse ensemble models from CLI arguments.
    Handles both per-ontology specs (--models-f/--models-p/--models-c) and default (--models).
    
    Args:
        args: Parsed argparse arguments
        parser: ArgumentParser instance for raising errors
        
    Returns:
        dict: Mapping of ont_code -> list of model names
        
    Raises:
        SystemExit: If no models specified (via parser.error)
    """
    models_per_ont = {}
    
    # Check for per-ontology specification
    if args.models_f or args.models_p or args.models_c:
        if args.models_f:
            models_per_ont['F'] = parse_comma_separated_string(args.models_f, strip=True, upper=False)
        if args.models_p:
            models_per_ont['P'] = parse_comma_separated_string(args.models_p, strip=True, upper=False)
        if args.models_c:
            models_per_ont['C'] = parse_comma_separated_string(args.models_c, strip=True, upper=False)
        
        # Fallback to --models for ontologies not specified
        if args.models:
            default_models = parse_comma_separated_string(args.models, strip=True, upper=False)
            for ont_code in ['F', 'P', 'C']:
                if ont_code not in models_per_ont:
                    models_per_ont[ont_code] = default_models
    elif args.models:
        # Same models for all ontologies
        default_models = parse_comma_separated_string(args.models, strip=True, upper=False)
        models_per_ont = {ont: default_models for ont in ['F', 'P', 'C']}
    else:
        parser.error("--models or (--models-f/--models-p/--models-c) required for ensemble pipeline")
    
    return models_per_ont


def parse_submission_files(submissions_str: str) -> List[str]:
    """
    Parse submission files from comma-separated string.
    
    Args:
        submissions_str: Comma-separated string of file paths
        
    Returns:
        list: List of file paths
    """
    return parse_comma_separated_string(submissions_str, strip=True, upper=False)


def create_model_specs_from_name(model_name: str) -> Dict[str, Tuple[str, str]]:
    """
    Create model_specs dict from model configuration name.
    Maps all ontologies to the same model (type, version).
    
    Args:
        model_name: Model configuration name (e.g., 'logistic_v1_1')
        
    Returns:
        dict: Mapping of ont_code -> (model_type, version) for all ontologies
    """
    model_config = get_model_config(model_name)
    model_type = model_config['type']
    version = model_config['version']
    
    # Create specs for all ontologies
    model_specs = {}
    for ont_code in ONTOLOGY_CODES:  # ONTOLOGY_CODES is already a list
        model_specs[ont_code] = (model_type, version)
    
    return model_specs


def build_ensemble_flags(method: str, 
                        weights: Optional[List[float]] = None,
                        percentile: float = 75.0,
                        power: float = 1.5) -> str:
    """
    Build ensemble method CLI flags from config parameters.
    DRY helper for notebook ensemble cells.
    
    Args:
        method: Ensemble method ('rank_average', 'percentile', 'max', 
                'weighted_average', 'average', 'power_average')
        weights: Weights for weighted_average (must sum to 1.0)
        percentile: Percentile value for percentile method (0-100)
        power: Power value for power_average method (>0)
        
    Returns:
        str: CLI flag string ready for command (e.g., "--ensemble-method rank_average --weights 0.2,0.4,0.4")
        
    Example:
        >>> build_ensemble_flags('weighted_average', weights=[0.2, 0.4, 0.4])
        '--ensemble-method weighted_average --weights 0.2,0.4,0.4'
    """
    flags = f"--ensemble-method {method}"
    
    if method == 'weighted_average' and weights:
        weights_str = ','.join(map(str, weights))
        flags += f" --weights {weights_str}"
    elif method == 'percentile':
        flags += f" --percentile {percentile}"
    elif method == 'power_average':
        flags += f" --power {power}"
    
    return flags

