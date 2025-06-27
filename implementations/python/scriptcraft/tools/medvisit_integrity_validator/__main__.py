"""Command-line entry point for the medvisit integrity validator."""

from scriptcraft.common import STANDARD_KEYS
from scriptcraft.pipelines.pipeline_utils import run_qc_for_each_domain
from .tool import run_medvisit_integrity_validator

if __name__ == "__main__":
    def custom_output_filename(_): return "med_visit_comparison.xlsx"

    run_qc_for_each_domain(
        log_filename="med_visit_check.log",
        qc_func=run_medvisit_integrity_validator,
        input_key=STANDARD_KEYS["raw_data"],  # not used but required
        output_filename=custom_output_filename,
        check_exists=False
    ) 