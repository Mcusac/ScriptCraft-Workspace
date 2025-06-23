"""Command-line entry point for the supplement prepper enhancement."""

from pathlib import Path
from scripts.common import setup_logger
from .tool import enhancement

if __name__ == "__main__":
    log_path = Path("logs") / "prepare_supplement.log"
    setup_logger(log_path)
    enhancement.enhance() 