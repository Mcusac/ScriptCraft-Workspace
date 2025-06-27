"""Command-line entry point for the dictionary cleaner."""

from scriptcraft.common import STANDARD_KEYS
from scriptcraft.pipelines.pipeline_utils import run_qc_for_each_domain
from .tool import run_dictionary_cleaner

if __name__ == "__main__":
    run_qc_for_each_domain(
        log_filename="dictionary_cleaner.log",
        qc_func=run_dictionary_cleaner,
        input_key=STANDARD_KEYS["dictionary"],
        check_exists=True
    ) 