# base.py
# Base infrastructure for grid search pipelines
# Provides common functionality shared between all grid search types

import logging
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple, Set
from abc import ABC, abstractmethod

from config.config import Config
from modeling.utils import get_top_n_results
from ..base_helpers import (
    setup_environment_helper,
    load_completed_variants_helper,
    save_variant_result_helper,
    cleanup_checkpoints_helper,
    run_final_cleanup_helper,
    clear_gpu_memory_before_variant,
    log_variant_header,
    create_result_dict,
    create_error_result_dict,
    update_best_score_helper
)

logger = logging.getLogger(__name__)


class GridSearchBase(ABC):
    """
    Base class for grid search pipelines.
    
    Provides common infrastructure for:
    - Environment setup
    - Result tracking and saving
    - Checkpoint cleanup
    - Progress tracking
    
    Subclasses should implement:
    - `_generate_variant_grid()`: Generate the grid of variants to test
    - `_run_variant()`: Execute a single variant
    - `_create_variant_key()`: Create unique key for variant tracking
    """
    
    def __init__(self, config: Config):
        """
        Initialize grid search base.
        
        Args:
            config: Configuration object with grid_search settings.
        """
        self.config = config
        self.results_file: Optional[Path] = None
        self.base_model_dir: Optional[Path] = None
        self.grid_search_dir: Optional[Path] = None
        self.device = None
        self.completed_variants: Set[Any] = set()
        self.skipped_variants: Set[Any] = set()
        self.top_variants: List[Dict[str, Any]] = []
        self.starting_index: int = 0
    
    def setup_environment(self) -> Tuple[Path, Path, Path, Any]:
        """
        Set up grid search environment.
        
        Returns:
            Tuple of (base_model_dir, grid_search_dir, device, device_info).
        """
        self.device, self.base_model_dir, self.grid_search_dir, device_info = setup_environment_helper(
            self.config,
            self._get_grid_search_type
        )
        return self.base_model_dir, self.grid_search_dir, self.device, device_info
    
    def get_train_csv_path(self) -> Path:
        """
        Get train CSV path for grid search.
        
        Returns:
            Path to train CSV file.
        """
        return Path(self.config.data.data_root) / self.config.data.train_csv
    
    def get_starting_index(self) -> int:
        """
        Get starting variant index for sequential numbering.
        
        Returns:
            Starting index (next variant_index to use).
        """
        return self.starting_index
    
    def setup_results_file(self) -> Path:
        """
        Set up results file path and initialize it if needed.
        
        Returns:
            Path to results file.
        """
        if not self.grid_search_dir:
            raise ValueError("grid_search_dir not set - call setup_environment first")
        
        results_filename = self._get_results_filename()
        self.results_file = self.grid_search_dir / results_filename
        return self.results_file
    
    @abstractmethod
    def _get_grid_search_type(self) -> str:
        """
        Get the grid search type name (e.g., 'dataset_grid_search', 'hyperparameter_grid_search').
        
        Returns:
            String identifier for this grid search type.
        """
        pass
    
    @abstractmethod
    def _get_results_filename(self) -> str:
        """
        Get the results filename for this grid search type.
        
        Returns:
            Filename for results JSON file.
        """
        pass
    
    @abstractmethod
    def _generate_variant_grid(self) -> List[Any]:
        """
        Generate the grid of variants to test.
        
        Returns:
            List of variants (format depends on subclass).
        """
        pass
    
    @abstractmethod
    def _create_variant_key(self, variant: Any) -> Any:
        """
        Create unique key for variant tracking.
        
        Args:
            variant: Variant from the grid.
            
        Returns:
            Hashable key for tracking this variant.
        """
        pass
    
    @abstractmethod
    def _run_variant(
        self, 
        variant: Any, 
        variant_index: int, 
        total_variants: int,
        actual_variant_num: Optional[int] = None,
        total_to_test: Optional[int] = None
    ) -> Tuple[Optional[float], Optional[List[float]], Dict[str, Any], Path]:
        """
        Run a single variant.
        
        Args:
            variant: Variant to run.
            variant_index: Index of variant in grid.
            total_variants: Total number of variants in grid.
            actual_variant_num: Optional actual variant number being tested (1-based, excludes skipped).
            total_to_test: Optional total number of variants actually being tested (excludes skipped).
            
        Returns:
            Tuple of (score, fold_scores, result_dict, variant_model_dir).
        """
        pass
    
    def load_completed_variants(self, keep_top_n: int) -> Tuple[Set[Any], Set[Any], List[Dict[str, Any]], int]:
        """
        Load completed and skipped variants from results file.
        
        Args:
            keep_top_n: Number of top variants to keep in memory.
            
        Returns:
            Tuple of (completed_variants_set, skipped_variants_set, top_variants_list, starting_index).
        """
        completed_variants, skipped_variants, top_variants, starting_index = load_completed_variants_helper(
            self.results_file,
            keep_top_n,
            self._create_variant_key_from_result
        )
        
        # Store in instance variables
        self.completed_variants = completed_variants
        self.skipped_variants = skipped_variants
        self.top_variants = top_variants
        self.starting_index = starting_index
        
        return completed_variants, skipped_variants, top_variants, starting_index
    
    @abstractmethod
    def _create_variant_key_from_result(self, result: Dict[str, Any]) -> Optional[Any]:
        """
        Create variant key from a result dictionary.
        
        Args:
            result: Result dictionary from JSON file.
            
        Returns:
            Variant key or None if result is invalid.
        """
        pass
    
    def save_variant_result(self, result: Dict[str, Any]) -> None:
        """
        Save variant result to results file (incremental append).
        
        Args:
            result: Variant result dictionary.
        """
        if not self.results_file:
            raise ValueError("results_file not set - call setup_environment first")
        
        save_variant_result_helper(result, self.results_file)
    
    def cleanup_checkpoints(
        self,
        variant_model_dir: Path,
        cv_score: Optional[float],
        variant_id: str
    ) -> None:
        """
        Clean up checkpoints if configured and needed.
        
        Args:
            variant_model_dir: Model directory for this variant.
            cv_score: CV score for this variant (None if failed).
            variant_id: ID of the variant.
        """
        if not self.base_model_dir or not self.results_file:
            return
        
        cleanup_checkpoints_helper(
            self.config,
            self.base_model_dir,
            self.results_file,
            variant_model_dir,
            cv_score,
            variant_id
        )
    
    def run_grid_search(
        self,
        variant_grid: List[Any],
        progress_tracker: Optional[Any] = None,
        grid_bar_id: Optional[str] = None,
        best_score: float = -float("inf"),
        best_variant: Optional[Dict[str, Any]] = None,
        keep_top_n: int = 10
    ) -> Tuple[float, Optional[Dict[str, Any]]]:
        """
        Run grid search main loop (template method).
        
        This method handles the common main loop logic:
        - Iterate through variants
        - Check if already completed/skipped
        - Run variant
        - Save result
        - Update best score and top variants
        - Cleanup checkpoints
        - Update progress (if tracker provided)
        
        Args:
            variant_grid: List of variants to test.
            progress_tracker: Optional progress tracker instance.
            grid_bar_id: Optional progress bar ID.
            best_score: Initial best score.
            best_variant: Initial best variant dict.
            keep_top_n: Number of top variants to keep.
        
        Returns:
            Tuple of (final_best_score, final_best_variant).
        """
        total_variants = len(variant_grid)
        completed_variants = self.completed_variants
        skipped_variants = self.skipped_variants
        top_variants = self.top_variants
        starting_index = self.starting_index
        
        # Initialize best from top_variants if available
        if top_variants and best_score == -float("inf"):
            best_variant = top_variants[0]
            best_score = best_variant.get("cv_score", -float("inf"))
            if best_score > -float("inf"):
                logger.info(f"Best score from existing results: {best_score:.4f}")
        
        # Calculate total variants to actually test (excluding completed and skipped)
        total_to_test = 0
        for variant in variant_grid:
            variant_key = self._create_variant_key(variant)
            if variant_key not in completed_variants and variant_key not in skipped_variants:
                total_to_test += 1
        
        if total_to_test == 0:
            logger.info("All variants already completed or skipped. Nothing to test.")
            return best_score, best_variant
        
        logger.info(f"Testing {total_to_test} new variants (skipping {total_variants - total_to_test} already completed/skipped)")
        
        # Track number of new variants created (not skipped) for sequential variant_index
        new_variant_count = 0
        
        try:
            for idx, variant in enumerate(variant_grid):
                # Create variant key
                variant_key = self._create_variant_key(variant)
                
                # Check if already completed
                if variant_key in completed_variants:
                    logger.info(f"\nSkipping variant {idx+1}/{total_variants} (already successfully completed)")
                    # Find existing result to update best score if needed
                    for r in top_variants:
                        r_key = self._create_variant_key_from_result(r)
                        if r_key == variant_key:
                            r_score = r.get("cv_score")
                            if r_score is not None and r_score > best_score:
                                best_score = r_score
                                best_variant = r
                            break
                    # Update progress for skipped variant
                    if grid_bar_id and progress_tracker:
                        progress_tracker.update(grid_bar_id, n=1)
                    continue
                
                # Check if skipped (persistent OOM)
                if variant_key in skipped_variants:
                    logger.info(f"\nSkipping variant {idx+1}/{total_variants} (previously skipped due to persistent OOM)")
                    logger.info("   This variant can be retried later with different settings")
                    if grid_bar_id and progress_tracker:
                        progress_tracker.update(grid_bar_id, n=1)
                    continue
                
                # Calculate variant_index for this new variant (sequential, not based on grid position)
                variant_index = starting_index + new_variant_count
                new_variant_count += 1
                
                # Run variant using base class method
                # Pass actual variant number (new_variant_count) and total to test for accurate logging
                cv_score, fold_scores, result, variant_model_dir = self._run_variant(
                    variant=variant,
                    variant_index=variant_index,
                    total_variants=total_variants,
                    actual_variant_num=new_variant_count,  # 1-based counter for variants actually being tested
                    total_to_test=total_to_test  # Total number of variants actually being tested
                )
                
                variant_id = result.get("variant_id", result.get("combination_id", f"variant_{variant_index:04d}"))
                
                # Save result to file using base class method
                self.save_variant_result(result)
                
                # Handle skipped variants
                if result.get("skipped", False):
                    skipped_variants.add(variant_key)
                    self.skipped_variants = skipped_variants
                    if grid_bar_id and progress_tracker:
                        progress_tracker.update(grid_bar_id, n=1)
                    continue
                
                # Update in-memory top variants list (keep only top N)
                if cv_score is not None:
                    top_variants.append(result)
                    top_variants = get_top_n_results(top_variants, keep_top_n, metric_key='cv_score')
                    
                    # Update best score
                    from modeling.utils import update_best_score
                    best_score, updated_best = update_best_score(best_score, cv_score, result)
                    if updated_best is not None:
                        best_variant = updated_best
                    
                    # Reload completed variants from file to stay in sync
                    completed_variants, skipped_variants, top_variants, starting_index = self.load_completed_variants(keep_top_n)
                    self.completed_variants = completed_variants
                    self.skipped_variants = skipped_variants
                    self.top_variants = top_variants
                    self.starting_index = starting_index
                
                # Cleanup checkpoints using base class method
                self.cleanup_checkpoints(
                    variant_model_dir=variant_model_dir,
                    cv_score=cv_score,
                    variant_id=variant_id
                )
                
                # Update progress bar after variant completion
                if grid_bar_id and progress_tracker:
                    progress_tracker.update(
                        grid_bar_id,
                        n=1,
                        CV=cv_score if cv_score is not None else None,
                        best=f"⭐{best_score:.4f}" if best_score > -float("inf") else None
                    )
        
        except KeyboardInterrupt:
            logger.warning("\n⚠️ KeyboardInterrupt received during grid search")
            logger.warning("Saving current progress before exiting...")
            logger.warning("Grid search interrupted. Progress saved. Resume will continue from next variant.")
            if grid_bar_id and progress_tracker:
                progress_tracker.close(grid_bar_id)
            raise  # Re-raise to allow proper cleanup
        
        return best_score, best_variant
    
    def run_final_cleanup(self) -> None:
        """
        Run final cleanup at the end of grid search.
        """
        run_final_cleanup_helper(self.config, self.base_model_dir, self.results_file)
    
    def clear_gpu_memory_before_variant(self) -> None:
        """
        Clear GPU memory before starting a variant.
        
        Should be called at the start of each variant execution.
        """
        clear_gpu_memory_before_variant()
    
    def update_top_variants(
        self,
        result: Dict[str, Any],
        keep_top_n: int
    ) -> None:
        """
        Update top variants list with new result.
        
        Args:
            result: Result dictionary to potentially add.
            keep_top_n: Number of top variants to keep.
        """
        cv_score = result.get('cv_score')
        if cv_score is not None:
            self.top_variants.append(result)
            self.top_variants = get_top_n_results(self.top_variants, keep_top_n, metric_key='cv_score')
    
    def _log_variant_header(
        self,
        variant_index: int,
        total_variants: int,
        variant_info: str
    ) -> None:
        """
        Log header for variant execution.
        
        Args:
            variant_index: Index of variant (0-based).
            total_variants: Total number of variants.
            variant_info: String describing the variant.
        """
        log_variant_header(variant_index, total_variants, variant_info)
    
    def _create_result_dict(
        self,
        variant_index: int,
        variant_id: str,
        cv_score: Optional[float],
        fold_scores: Optional[List[float]],
        batch_size_used: int,
        batch_size_reduced: bool,
        variant_specific_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create result dictionary for a variant.
        
        Args:
            variant_index: Index of variant.
            variant_id: ID of variant.
            cv_score: CV score (None if failed).
            fold_scores: Fold scores (None if failed).
            batch_size_used: Batch size used.
            batch_size_reduced: Whether batch size was reduced.
            variant_specific_data: Dictionary with variant-specific fields.
        
        Returns:
            Result dictionary.
        """
        return create_result_dict(
            variant_index,
            variant_id,
            cv_score,
            fold_scores,
            batch_size_used,
            batch_size_reduced,
            variant_specific_data
        )
    
    def _create_error_result_dict(
        self,
        variant_index: int,
        variant_id: str,
        error: str,
        batch_size_used: int,
        batch_size_reduced: bool,
        variant_specific_data: Dict[str, Any],
        skipped: bool = False
    ) -> Dict[str, Any]:
        """
        Create error result dictionary for a variant.
        
        Args:
            variant_index: Index of variant.
            variant_id: ID of variant.
            error: Error message.
            batch_size_used: Batch size used.
            batch_size_reduced: Whether batch size was reduced.
            variant_specific_data: Dictionary with variant-specific fields.
            skipped: Whether variant was skipped (default: False).
        
        Returns:
            Error result dictionary.
        """
        return create_error_result_dict(
            variant_index,
            variant_id,
            error,
            batch_size_used,
            batch_size_reduced,
            variant_specific_data,
            skipped
        )
    
    def _update_best_score(
        self,
        current_best_score: float,
        new_score: Optional[float],
        new_result: Dict[str, Any],
        best_result_key: str = 'best_variant'
    ) -> Tuple[float, Optional[Dict[str, Any]]]:
        """
        Update best score if new score is better.
        
        Args:
            current_best_score: Current best score.
            new_score: New score to compare.
            new_result: Result dictionary for new score.
            best_result_key: Key to use for best result in return (for logging context).
        
        Returns:
            Tuple of (updated_best_score, best_result_dict or None).
        """
        return update_best_score_helper(current_best_score, new_score, new_result, best_result_key)

