"""
Main CLI for CAFA 6 protein function prediction pipeline.
Replaces run_pipeline.py with argument-driven orchestrator.
"""

import argparse
import sys
import time
from pathlib import Path

# Add scripts directory to path for imports (insert at front to avoid conflicts)
scripts_dir = str(Path(__file__).parent)
if scripts_dir not in sys.path:
    sys.path.insert(0, scripts_dir)

from config import get_model_config, get_pipeline_config, MODEL_CONFIGS, PIPELINE_CONFIGS, get_ontology_name, ONTOLOGY_CODES, get_ontology_hyperparams
from pipelines.pipeline_orchestrator import (
    run_full_pipeline,
    run_train_all, 
    run_train_single_ontology,
    run_train_parallel_ontologies,
    run_predict_from_saved,
    run_grid_search_pipeline
)
from utils.model_io import list_saved_models, get_model_summary
from utils.cli_utils import (
    parse_model_specs_from_args, 
    validate_pipeline_args,
    parse_feature_override,
    parse_ontology_arg,
    parse_ensemble_models,
    parse_submission_files,
    parse_weights,
    build_ensemble_kwargs,
    validate_ontology_codes
)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CAFA 6 Protein Function Prediction Pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
        Examples:
        # Full pipeline from scratch
        python scripts/run.py --pipeline full --model logistic_v1

        # Train all ontologies, save models
        python scripts/run.py --pipeline train_all --model xgboost_v1

        # Train single ontology
        python scripts/run.py --pipeline train_single --model logistic_v2 --ontology CCO

        # Predict using saved models
        python scripts/run.py --pipeline predict --model-mfo logistic_v1 --model-bpo logistic_v1 --model-cco xgboost_v1

        # Mixed models (ensemble foundation)
        python scripts/run.py --pipeline predict --model-mfo logistic_v2 --model-bpo xgboost_v1 --model-cco logistic_v1

        # List saved models
        python scripts/run.py --list-models
        """
    )
    
    # Pipeline selection
    parser.add_argument(
        '--pipeline', 
        choices=list(PIPELINE_CONFIGS.keys()),
        help='Pipeline to run'
    )
    
    # Model selection
    parser.add_argument(
        '--model',
        choices=list(MODEL_CONFIGS.keys()),
        help='Model configuration to use'
    )
    
    # Single ontology training (comma-separated for parallel: "P,C" or "F,P,C")
    parser.add_argument(
        '--ontology',
        help='Ontology code(s) for training. Single: "C". Parallel: "P,C" or "F,P,C"'
    )
    
    # Mixed model prediction
    parser.add_argument(
        '--model-mfo',
        help='Model specification for MFO (format: model_type:version)'
    )
    parser.add_argument(
        '--model-bpo', 
        help='Model specification for BPO (format: model_type:version)'
    )
    parser.add_argument(
        '--model-cco',
        help='Model specification for CCO (format: model_type:version)'
    )
    
    # Output options
    parser.add_argument(
        '--output',
        help='Custom output filename'
    )
    parser.add_argument(
        '--extra-output-name',
        help='Optional filename for a descriptive copy of submission.tsv (for record-keeping)'
    )
    
    # Feature selection
    parser.add_argument(
        '--features',
        help='Feature specification (preset name or comma-separated features). '
             'Presets: default, embeddings_only, all_with_hc. '
             'Individual: protbert, esm2, t5, hc. '
             'Examples: --features default, --features protbert,esm2,hc, --features esm2'
    )
    
    # Ensemble options
    parser.add_argument(
        '--models',
        help='Comma-separated list of model names for ensemble (applies to all ontologies). '
             'Example: --models mlp_v1,xgboost_v2'
    )
    parser.add_argument(
        '--models-f',
        help='Comma-separated model names for MFO (F) ontology. Overrides --models for F only.'
    )
    parser.add_argument(
        '--models-p',
        help='Comma-separated model names for BPO (P) ontology. Overrides --models for P only.'
    )
    parser.add_argument(
        '--models-c',
        help='Comma-separated model names for CCO (C) ontology. Overrides --models for C only.'
    )
    parser.add_argument(
        '--ensemble-method',
        choices=['average', 'weighted_average', 'max', 'geometric_mean', 
                 'rank_average', 'power_average', 'percentile', 'merge'],
        default='average',
        help='Ensemble method (default: average). '
             'For power_average, use power via code. For percentile, use percentile via code. '
             'For merge, use with 2 submissions and --prefer-submission to specify which to prefer.'
    )
    parser.add_argument(
        '--weights',
        help='Comma-separated weights for weighted_average. '
             'Example: --weights 0.6,0.4'
    )
    parser.add_argument(
        '--prefer-submission',
        choices=['submission1', 'submission2'],
        default='submission2',
        help='Which submission to prefer when using merge method (default: submission2). '
             'Only applies when --ensemble-method merge and exactly 2 submissions provided.'
    )
    parser.add_argument(
        '--padding-strategy',
        choices=['zeros', 'mean', 'noise'],
        help='Padding strategy for dimension mismatches'
    )
    parser.add_argument(
        '--power',
        type=float,
        default=1.0,
        help='Power parameter for power_average method (default: 1.0, >1 emphasizes high probs)'
    )
    parser.add_argument(
        '--percentile',
        type=float,
        default=75.0,
        help='Percentile parameter for percentile method (default: 75.0, range 0-100)'
    )
    parser.add_argument(
        '--power-default',
        type=float,
        default=1.5,
        help='Default power for power_average method in get_all_averages (default: 1.5)'
    )
    parser.add_argument(
        '--percentile-default',
        type=float,
        default=75.0,
        help='Default percentile for percentile method in get_all_averages (default: 75.0)'
    )
    parser.add_argument(
        '--output-prefix',
        help='Output filename prefix for get_all_averages pipeline (default: auto-generated)'
    )
    
    # Submission averaging options
    parser.add_argument(
        '--submissions',
        help='Comma-separated list of submission file paths for averaging. '
             'Example: --submissions sub1.tsv,sub2.tsv'
    )
    
    # Utility options
    parser.add_argument(
        '--list-models',
        action='store_true',
        help='List all saved models'
    )
    parser.add_argument(
        '--list-configs',
        action='store_true',
        help='List available model configurations'
    )
    
    # Model loading/training mode
    parser.add_argument(
        '--mode',
        choices=['train_new', 'load_only', 'load_or_train'],
        default='load_or_train',
        help='Model loading/training mode (default: load_or_train)'
    )
    
    # Grid search options
    parser.add_argument(
        '--cv',
        type=int,
        default=3,
        help='Number of cross-validation folds for grid search (default: 3)'
    )
    parser.add_argument(
        '--quick',
        action='store_true',
        help='Use smaller parameter grid for quick grid search testing'
    )
    parser.add_argument(
        '--checkpoint-path',
        type=str,
        help='Explicit path to checkpoint file for grid search resume (default: auto-detect)'
    )
    parser.add_argument(
        '--no-resume',
        action='store_true',
        help='Disable checkpoint resume for grid search (start fresh)'
    )
    
    # Model source selection
    parser.add_argument(
        '--models-source',
        choices=['input', 'working', 'both'],
        default='both',
        help='Where to load models from: "input" (MODELS_INPUT_DIR), "working" (MODELS_DIR), or "both" (check both, default)'
    )
    
    # GOA post-processing
    parser.add_argument(
        '--apply-goa-filter',
        action='store_true',
        default=True,
        help='Apply GOA negative propagation filtering to predictions (default: True). Use --no-apply-goa-filter to disable.'
    )
    parser.add_argument(
        '--no-apply-goa-filter',
        dest='apply_goa_filter',
        action='store_false',
        help='Disable GOA negative propagation filtering'
    )
    
    args = parser.parse_args()
    
    # Handle utility commands
    if args.list_models:
        print("📋 Saved Models:")
        print("=" * 50)
        summary = get_model_summary()
        print(summary)
        return
    
    if args.list_configs:
        print("📋 Available Model Configurations:")
        print("=" * 50)
        for model_name, config in MODEL_CONFIGS.items():
            print(f"{model_name}: {config['description']}")
            print(f"  Type: {config['type']}")
            print(f"  Version: {config['version']}")
            # Show per-ontology hyperparams (required for all models)
            if 'per_ontology_hyperparams' in config:
                print(f"  Per-ontology hyperparams:")
                for ont_code in ['F', 'P', 'C']:
                    if ont_code in config['per_ontology_hyperparams']:
                        print(f"    {ont_code}: {config['per_ontology_hyperparams'][ont_code]}")
            else:
                print(f"  ⚠️  Per-ontology hyperparams: (missing - model configuration incomplete)")
            print()
        return
    
    # Validate arguments using CLI utilities
    validate_pipeline_args(args, parser)
    
    # Parse model specs if needed for prediction pipeline
    if args.pipeline == 'predict_from_saved':
        model_specs = parse_model_specs_from_args(args)
    else:
        model_specs = None
    
    # Run pipeline
    print("🚀 CAFA 6 Protein Function Prediction Pipeline")
    print("=" * 60)
    print(f"Pipeline: {args.pipeline}")
    if args.model:
        model_config = get_model_config(args.model)
        
        # Override feature configuration if --features provided
        feature_override = parse_feature_override(args, parser)
        if feature_override:
            model_config.update(feature_override)
            print(f"Feature override: {args.features} -> {feature_override['features']}")
        
        print(f"Model: {model_config['description']}")
    if args.ontology:
        ont_codes, ont_names = parse_ontology_arg(args.ontology)
        if len(ont_codes) > 1:
            print(f"Ontologies: {', '.join([f'{name} ({code})' for name, code in zip(ont_names, ont_codes)])}")
        else:
            print(f"Ontology: {ont_names[0]} ({ont_codes[0]})")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        if args.pipeline == 'full_pipeline':
            result = run_full_pipeline(args.model, args.output, mode=args.mode, model_config_override=model_config if (args.model and args.features) else None)
            print(f"\n✅ Pipeline completed successfully!")
            print(f"📄 Output: {result}")
            
        elif args.pipeline == 'train_only':
            # Simple: train all ontologies with specified model
            models = run_train_all(args.model, mode=args.mode or 'train_new', model_config_override=model_config if (args.model and args.features) else None)
            print(f"\n✅ Training completed successfully!")
            print(f"🤖 Trained {len(models)} models")
            
        elif args.pipeline == 'train_single_ont':
            # Support comma-separated ontologies for parallel training
            try:
                ont_codes = validate_ontology_codes(args.ontology)
            except ValueError as e:
                print(f"⚠️  {e}")
                ont_codes = [o.strip().upper() for o in args.ontology.split(',') if o.strip().upper() in ONTOLOGY_CODES]
                if not ont_codes:
                    raise ValueError("No valid ontology codes provided")
            
            if len(ont_codes) > 1:
                # Parallel training
                models = run_train_parallel_ontologies(args.model, ont_codes, mode=args.mode, model_config_override=model_config if (args.model and args.features) else None)
                print(f"\n✅ Parallel training completed successfully!")
                print(f"🤖 Trained {len(models)} models: {', '.join(ont_codes)}")
            elif len(ont_codes) == 1:
                # Single training
                model = run_train_single_ontology(args.model, ont_codes[0], mode=args.mode, model_config_override=model_config if (args.model and args.features) else None)
                print(f"\n✅ Single ontology training completed successfully!")
                print(f"🤖 Trained {ont_codes[0]} model")
            else:
                raise ValueError("No valid ontology codes provided")
            
        elif args.pipeline == 'predict_from_saved':
            result = run_predict_from_saved(
                model_specs, 
                args.output, 
                models_source=args.models_source,
                apply_goa_filter=args.apply_goa_filter
            )
            print(f"\n✅ Prediction completed successfully!")
            print(f"📄 Output: {result}")
            
        elif args.pipeline == 'grid_search':
            checkpoint_path = Path(args.checkpoint_path) if args.checkpoint_path else None
            resume = not args.no_resume  # Default True, unless --no-resume is set
            result = run_grid_search_pipeline(
                args.model, 
                ontology=args.ontology if args.ontology else 'all',
                cv=args.cv,
                quick=args.quick,
                checkpoint_path=checkpoint_path,
                resume=resume
            )
            print(f"\n✅ Grid search completed successfully!")
            if result:
                print(f"📄 Results: {result}")
        
        elif args.pipeline == 'ensemble':
            models_per_ont = parse_ensemble_models(args, parser)
            weights = parse_weights(args.weights) if args.weights else None
            
            from pipelines.workflows.ensemble import run_ensemble_prediction_per_ontology
            ensemble_kwargs = build_ensemble_kwargs(
                args.ensemble_method,
                power=args.power,
                percentile=args.percentile
            )
            
            result = run_ensemble_prediction_per_ontology(
                models_per_ontology=models_per_ont,
                ensemble_method=args.ensemble_method,
                weights=weights,
                padding_strategy=args.padding_strategy,
                output_name=args.output,
                extra_output_name=args.extra_output_name,
                **ensemble_kwargs
            )
            print(f"\n✅ Ensemble prediction completed successfully!")
            print(f"📄 Output: {result}")
        
        elif args.pipeline == 'average_submissions':
            submission_files = parse_submission_files(args.submissions)
            weights = parse_weights(args.weights) if args.weights else None
            
            from pipelines.workflows.submission_averaging import run_submission_averaging
            ensemble_kwargs = build_ensemble_kwargs(
                args.ensemble_method,
                power=args.power,
                percentile=args.percentile
            )
            
            result = run_submission_averaging(
                submission_files=submission_files,
                weights=weights,
                output_name=args.output,
                ensemble_method=args.ensemble_method,
                prefer_submission=args.prefer_submission if args.ensemble_method == 'merge' else None,
                extra_output_name=args.extra_output_name,
                **ensemble_kwargs
            )
            print(f"\n✅ Submission averaging completed successfully!")
            print(f"📄 Output: {result}")
        
        elif args.pipeline == 'get_all_averages':
            submission_files = parse_submission_files(args.submissions)
            weights = parse_weights(args.weights) if args.weights else None
            
            from pipelines.workflows.get_all_averages import run_get_all_averages
            results = run_get_all_averages(
                submission_files=submission_files,
                weights=weights,
                power_default=args.power_default,
                percentile_default=args.percentile_default,
                output_prefix=args.output_prefix
            )
            print(f"\n✅ Get all averages completed successfully!")
            print(f"📄 Generated {len(results)} submission files:")
            for i, result in enumerate(results, 1):
                print(f"   {i}. {result}")
        
        else:
            raise ValueError(f"Unknown pipeline: {args.pipeline}")
            
    except Exception as e:
        print(f"\n❌ Pipeline failed: {e}")
        import traceback
        print("\n📋 Full traceback:")
        traceback.print_exc()
        sys.exit(1)
    
    total_time = time.time() - start_time
    print(f"\n⏱️  Total execution time: {total_time:.1f}s")


if __name__ == "__main__":
    main()
