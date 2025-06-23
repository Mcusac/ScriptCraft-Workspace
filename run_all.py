"""
Main script for running pipelines and tools using the existing pipeline framework.
"""

import sys
from pathlib import Path

from scripts.common.core import Config
from scripts.common.logging import setup_logger, log_and_print
from scripts.common.cli import parse_main_args
from scripts.pipelines.pipeline_steps import PipelineFactory
from scripts.pipelines.pipeline_utils import list_pipelines, preview_pipeline, run_pipeline


def main():
    """Main entry point."""
    args = parse_main_args("Run pipelines and tools")
    
    # Load and validate configuration
    try:
        config = Config.from_yaml(args.config)
        config.validate()
    except Exception as e:
        log_and_print(f"❌ Error loading configuration: {str(e)}", level="error")
        sys.exit(1)
    
    # Setup logging
    logger = setup_logger(
        name="run_all",
        level=config.logging.level,
        log_file=Path(config.logging.log_dir) / "run_all.log",
        log_format=config.logging.log_format,
        verbose=config.logging.verbose_mode
    )
    
    # Create pipeline factory and build pipelines
    try:
        factory = PipelineFactory()
        pipelines = factory.create_pipelines()
    except Exception as e:
        logger.error(f"❌ Error creating pipelines: {e}")
        sys.exit(1)
    
    # List available pipelines and tools
    if args.list:
        list_pipelines(pipelines)
        
        log_and_print("\n🛠️ Available tools:")
        for name, tool in config.tools.items():
            description = tool.get('description', 'No description')
            log_and_print(f"  🔧 {name}: {description}")
        return
    
    # Run pipeline
    if args.pipeline:
        if args.pipeline not in pipelines:
            logger.error(f"❌ Pipeline '{args.pipeline}' not found")
            logger.info(f"Available pipelines: {list(pipelines.keys())}")
            sys.exit(1)
        
        pipeline = pipelines[args.pipeline]
        logger.info(f"🚀 Running pipeline: {args.pipeline}")
        
        if args.dry_run:
            preview_pipeline(pipeline, args.tag)
        else:
            run_pipeline(pipeline, args)
        
        logger.info(f"🎉 Pipeline '{args.pipeline}' completed successfully")
        return
    
    # Run tool (via tool dispatcher)
    if args.tool:
        if args.tool not in config.tools:
            logger.error(f"❌ Tool '{args.tool}' not found")
            sys.exit(1)
        
        logger.info(f"🛠️ Running tool: {args.tool}")
        
        # Import and use tool dispatcher
        try:
            from scripts.tools.tool_dispatcher import dispatch_tool
            dispatch_tool(args.tool, args)
            logger.info(f"🎉 Tool '{args.tool}' completed successfully")
        except Exception as e:
            logger.error(f"❌ Tool execution failed: {e}")
            sys.exit(1)
        return
    
    # No action specified
    logger.error("❌ No action specified. Use --list, --pipeline, or --tool")
    sys.exit(1)


if __name__ == "__main__":
    main()
