"""Command-line entry point for the date format standardizer."""

from scripts.common import STANDARD_KEYS
from scripts.pipelines.pipeline_utils import run_qc_for_each_domain
from .tool import run_date_format_standardizer

if __name__ == "__main__":
    run_qc_for_each_domain(
        log_filename="date_format_standardizer.log",
        qc_func=run_date_format_standardizer,
        input_key=STANDARD_KEYS["processed_data"],
        output_filename="date_format_standardized.csv",
        check_exists=True
    ) 