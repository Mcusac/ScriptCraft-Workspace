"""Command-line entry point for the score totals checker."""

from scripts.pipelines.pipeline_utils import run_qc_for_each_domain
from .tool import run_score_totals_checker

if __name__ == "__main__":
    run_qc_for_each_domain(
        log_filename="totals_validation.log",
        qc_func=run_score_totals_checker,
        input_key="merged_data",
        filename_suffix="totals",
        check_exists=True
    ) 