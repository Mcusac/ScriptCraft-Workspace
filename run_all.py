"""
Main script for running pipelines and tools using the existing pipeline framework.
"""

import sys
import yaml
from pathlib import Path

# Add implementations/python-package to Python path for dynamic imports
sys.path.insert(0, str(Path(__file__).parent / "implementations" / "python-package"))

from scriptcraft.common.core import Config
from scriptcraft.common.logging import setup_logger, log_and_print
from scriptcraft.common.cli import parse_main_args
from scriptcraft.common.pipeline import PipelineFactory, list_pipelines, preview_pipeline, run_pipeline


def get_workspace_config(args):
    """Determine which workspace config to use."""
    
    # If user specified a config file directly, use it
    if args.config != "config.yaml":
        return args.config
    
    # If user specified a workspace via CLI, use it
    if hasattr(args, 'workspace') and args.workspace != "development":
        workspace = args.workspace
        log_and_print(f"🎯 Using CLI workspace: {workspace}", verbose=True)
        return f"workspaces/{workspace}/config.yaml"
    
    # Check if root config.yaml exists and has pipelines (framework config)
    root_config_path = Path("config.yaml")
    if root_config_path.exists():
        try:
            with open(root_config_path, 'r', encoding='utf-8') as f:
                base_config = yaml.safe_load(f)
            
            # If it has pipelines, it's a framework config we can use directly
            if 'pipelines' in base_config:
                log_and_print(f"🎯 Using framework config from root config.yaml", verbose=True)
                return "config.yaml"
            
            # Otherwise, check for active workspace
            workspace = base_config.get('active_workspace', 'development')
            log_and_print(f"🎯 Using workspace from config: {workspace}", verbose=True)
            return f"workspaces/{workspace}/config.yaml"
            
        except Exception as e:
            log_and_print(f"⚠️ Error reading config.yaml: {e}", level="warning")
    
    # Fallback to default workspace
    return "workspaces/development/config.yaml"


def main():
    """Main entry point."""
    args = parse_main_args("Run pipelines and tools")
    
    # Determine config file to use
    config_path = get_workspace_config(args)
    
    # Load and validate configuration
    try:
        config = Config.from_yaml(config_path)
        config.discover_and_merge_tools()  # Merge framework tools and discover tools
        config.validate()
    except Exception as e:
        log_and_print(f"❌ Error loading configuration: {str(e)}", level="error")
        sys.exit(1)
    
    # Setup logging using PathResolver for workspace-aware paths
    log_level = "DEBUG" if args.debug else config.logging.level
    path_resolver = config.get_path_resolver()
    logger = setup_logger(
        name="run_all",
        level=log_level,
        log_file=path_resolver.get_logs_dir() / "run_all.log",
        log_format=config.logging.log_format,
        verbose=config.logging.verbose_mode or args.verbose
    )
    
    # Create pipeline factory and build pipelines
    try:
        logger.debug("🏗️ Creating PipelineFactory")
        factory = PipelineFactory(config)
        logger.debug("🔧 Building pipelines from configuration")
        pipelines = factory.create_pipelines()
        logger.info(f"✅ Successfully created {len(pipelines)} pipelines")
    except Exception as e:
        logger.error(f"❌ Error creating pipelines: {e}")
        import traceback
        logger.debug(f"Exception traceback: {traceback.format_exc()}")
        sys.exit(1)
    
    # List available pipelines and tools
    if args.list:
        logger.debug("📋 Listing available pipelines")
        
        # List pipelines using the logger directly to avoid duplicates
        logger.info("\n📋 Available Pipelines:")
        for name, pipeline in pipelines.items():
            logger.info(f"\n🔷 {name}")
            if pipeline.description:
                logger.info(f"   📝 {pipeline.description}")
            logger.info("   Steps:")
            for step in pipeline.steps:
                tags = f" [{', '.join(step.tags)}]" if step.tags else ""
                logger.info(f"   - {step.name}{tags}")
        
        logger.debug("✅ Pipeline listing completed")
        
        logger.info("\n🛠️ Available tools:")
        for name, tool in config.tools.items():
            description = tool.get('description', 'No description')
            logger.info(f"  🔧 {name}: {description}")
        logger.debug("✅ Tool listing completed")
        return
    
    # Run pipeline
    if args.pipeline:
        if args.pipeline not in pipelines:
            logger.error(f"❌ Pipeline '{args.pipeline}' not found")
            logger.info(f"Available pipelines: {list(pipelines.keys())}")
            sys.exit(1)
        
        pipeline = pipelines[args.pipeline]
        logger.info(f"🚀 Running pipeline: {args.pipeline}")
        logger.info(f"🔍 Pipeline has {len(pipeline.steps)} steps: {[step.name for step in pipeline.steps]}")
        
        if args.dry_run:
            preview_pipeline(pipeline, args.tag)
        else:
            logger.info(f"🔍 About to call run_pipeline...")
            try:
                run_pipeline(pipeline, args)
                logger.info(f"🔍 run_pipeline returned successfully")
            except Exception as e:
                logger.error(f"❌ Error in run_pipeline: {e}")
                import traceback
                logger.debug(f"Traceback: {traceback.format_exc()}")
                raise
        
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
            from scriptcraft.tools.tool_dispatcher import dispatch_tool
            dispatch_tool(args.tool, args)
        except Exception as e:
            logger.error(f"❌ Tool execution failed: {e}")
            sys.exit(1)
            
        logger.info(f"🎉 Tool '{args.tool}' completed successfully")
        return
    
    # No action specified
    logger.error("❌ No action specified. Use --list, --pipeline, or --tool")
    sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
