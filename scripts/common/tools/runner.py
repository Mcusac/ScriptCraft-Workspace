# scripts/common/tool_runner.py

import argparse
from pathlib import Path
from ..logging import setup_logging_with_timestamp, log_and_print
from ..io import get_project_root, resolve_path, ensure_output_dir
from ..io.paths import get_config

def run_tool(logic_func, args=None):
    """
    🏁 Standard runner for tools that require input/output/log setup.
    
    Args:
        logic_func (function): The main tool function to execute.
            Expected signature:
            logic_func(input_dir, output_dir, log_dir, input_file, med_id, config)
    """
    parser = argparse.ArgumentParser(description=f"Run {logic_func.__name__}")
    parser.add_argument("--input_dir", default="input", help="Input directory (default: input/).")
    parser.add_argument("--output_dir", default="output", help="Output directory (default: output/).")
    parser.add_argument("--log_dir", default="logs", help="Log directory (default: logs/).")
    parser.add_argument("--input", type=str, help="Input file name (optional).")
    parser.add_argument("--med_id", type=str, help="Optional Med_ID to filter (optional).")
    
    if args is None:
        args = parser.parse_args()
    else:
        args = parser.parse_args(args)
    
    config = get_config()
    project_root = get_project_root()
    input_dir = resolve_path(args.input_dir, project_root)
    output_dir = ensure_output_dir(resolve_path(args.output_dir, project_root))
    log_dir = ensure_output_dir(resolve_path(args.log_dir, project_root))

    log_file = setup_logging_with_timestamp(log_dir, mode=logic_func.__name__)
    log_and_print(f"🚀 Running tool: {logic_func.__name__}")
    log_and_print(f"📂 Input Dir: {input_dir.resolve()}")
    log_and_print(f"📂 Output Dir: {output_dir.resolve()}")

    logic_func(
        input_dir=input_dir,
        output_dir=output_dir,
        log_dir=log_dir,
        input_file=args.input,
        med_id=args.med_id,
        config=config
    )

    log_and_print("✅ Tool completed.")
