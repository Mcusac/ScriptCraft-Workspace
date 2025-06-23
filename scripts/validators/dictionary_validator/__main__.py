"""Command-line entry point for the dictionary validator."""

from scripts.pipelines.pipeline_utils import run_qc_for_each_domain
from .tool import run_dictionary_validator

if __name__ == "__main__":
    run_qc_for_each_domain(
        log_filename="dict_validation.log",
        qc_func=run_dictionary_validator,
        check_exists=False       # Our qc_func handles missing files
    ) 