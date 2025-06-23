"""Command-line entry point for the automated labeler tool."""

from scripts.common.cli import ParserFactory
from .tool import tool

def parse_cli_args():
    parser = ParserFactory.create_tool_parser("automated_labeler", "🏷️ Automated Labeler Tool")
    
    # Add tool-specific arguments
    parser.add_argument("--input-excel", required=True, 
                       help="Path to Excel input file.")
    parser.add_argument("--template", required=True, 
                       help="Path to DOCX template file.")
    parser.add_argument("--output-filename", default="Labels.docx", 
                       help="Output file name (default: Labels.docx).")
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_cli_args()
    tool.run(
        input_paths=[args.input_excel, args.template],
        output_dir=args.output_dir,
        output_filename=args.output_filename
    ) 