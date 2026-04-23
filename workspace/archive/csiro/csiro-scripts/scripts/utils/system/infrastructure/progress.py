# progress_tracker.py
# Unified progress tracking system with configurable verbosity

import time
import logging
from typing import Dict, Optional, Any
from collections import deque
from tqdm import tqdm
import torch

from config.progress_config import ProgressConfig, ProgressVerbosity

logger = logging.getLogger(__name__)


class ProgressTracker:
    """
    Unified progress tracking system with configurable verbosity.
    
    Supports nested progress bars, time estimation, memory tracking, and
    throughput calculation. Automatically adjusts output based on verbosity level.
    
    Features:
    - Nested progress bars (grid search → variant → epoch → batch)
    - Configurable verbosity levels (SILENT to DEBUG)
    - Time estimation with EMA smoothing
    - GPU/CPU memory tracking
    - Throughput calculation (samples/sec, items/sec)
    - Seamless fallback when verbosity is reduced
    """
    
    def __init__(self, config: ProgressConfig):
        """
        Initialize progress tracker.
        
        Args:
            config: Progress configuration with verbosity and display options.
        """
        self.config = config
        self.active_bars: Dict[str, tqdm] = {}
        self.bar_metadata: Dict[str, Dict[str, Any]] = {}
        self.start_times: Dict[str, float] = {}
        self.last_update_times: Dict[str, float] = {}
        self.update_counts: Dict[str, deque] = {}  # For EMA smoothing
        self._position_counter = 0  # For nested bar positioning
        
    def _should_show(self, level: int = 1) -> bool:
        """
        Check if progress should be shown at given level.
        
        Args:
            level: Nesting level (1 = top level, higher = nested)
            
        Returns:
            True if progress should be shown, False otherwise.
        """
        if self.config.verbosity == ProgressVerbosity.SILENT:
            return False
        
        # For minimal verbosity, only show top-level bars
        if self.config.verbosity == ProgressVerbosity.MINIMAL:
            return level == 1
        
        # For moderate and above, show nested bars
        return True
    
    def _get_position(self, level: int) -> int:
        """
        Get position for nested progress bar.
        
        Args:
            level: Nesting level (1 = top level, higher = nested)
            
        Returns:
            Position for tqdm bar (0 = top, higher = lower).
        """
        if level == 1:
            self._position_counter = 0
            return 0
        
        # For nested bars, position them below parent
        return self._position_counter + (level - 1)
    
    def create_bar(
        self,
        bar_id: str,
        total: int,
        desc: str,
        level: int = 1,
        unit: str = 'it',
        initial: int = 0,
        **kwargs
    ) -> Optional[str]:
        """
        Create a progress bar.
        
        Args:
            bar_id: Unique identifier for this progress bar.
            total: Total number of items to process (None for indeterminate).
            desc: Description text for the progress bar.
            level: Nesting level (1 = top level, higher = nested).
            unit: Unit of measurement ('it' for iterations, 'samples', etc.).
            initial: Initial progress value.
            **kwargs: Additional arguments passed to tqdm.
            
        Returns:
            bar_id if bar was created, None if verbosity prevents display.
        """
        if not self._should_show(level):
            return None
        
        # Close any existing bar with same ID
        if bar_id in self.active_bars:
            self.close(bar_id)
        
        # Create tqdm bar with custom format to disable native time display
        # This ensures we use only ProgressTracker's custom _format_time() method
        position = self._get_position(level)
        # Custom bar_format excludes {elapsed} and {remaining} to prevent duplicate time display
        # ProgressTracker's custom ETA will appear in {postfix} via _build_postfix()
        custom_bar_format = '{desc}: {percentage:3.0f}%|{bar}| {n}/{total} [{rate_fmt}{postfix}]'
        bar = tqdm(
            total=total,
            desc=desc,
            unit=unit,
            initial=initial,
            position=position,
            leave=(level == 1),  # Only top-level bars persist after completion
            disable=(self.config.verbosity == ProgressVerbosity.SILENT),
            bar_format=custom_bar_format,
            **kwargs
        )
        
        self.active_bars[bar_id] = bar
        self.start_times[bar_id] = time.time()
        self.last_update_times[bar_id] = time.time()
        self.update_counts[bar_id] = deque(maxlen=10)  # For EMA smoothing
        
        # Store metadata
        self.bar_metadata[bar_id] = {
            'level': level,
            'total': total,
            'unit': unit,
            'desc': desc
        }
        
        if level == 1:
            self._position_counter = 0
        else:
            self._position_counter += 1
        
        return bar_id
    
    def update(
        self,
        bar_id: str,
        n: int = 1,
        **metrics
    ) -> None:
        """
        Update progress bar.
        
        Args:
            bar_id: Identifier of the progress bar to update.
            n: Number of items to increment by (default: 1).
            **metrics: Additional metrics to display (e.g., loss=0.5, R²=0.8).
        """
        if bar_id not in self.active_bars:
            return
        
        bar = self.active_bars[bar_id]
        current_time = time.time()
        
        # Build and set postfix before updating to avoid double refresh
        # This ensures a single display refresh that includes both progress and metrics
        postfix = self._build_postfix(bar_id, **metrics)
        if postfix:
            bar.set_postfix(postfix)
        
        # Update progress (this will refresh with postfix already set)
        bar.update(n)
        
        # Track update rate for EMA smoothing
        if bar_id in self.last_update_times:
            elapsed = current_time - self.last_update_times[bar_id]
            if elapsed > 0:
                rate = n / elapsed
                self.update_counts[bar_id].append(rate)
        
        self.last_update_times[bar_id] = current_time
    
    def _build_postfix(self, bar_id: str, **metrics) -> Dict[str, Any]:
        """
        Build postfix string with metrics and additional info.
        
        Args:
            bar_id: Bar identifier.
            **metrics: Metrics to display.
            
        Returns:
            Dictionary of postfix items.
        """
        postfix = {}
        
        # Add user-provided metrics
        postfix.update(metrics)
        
        # Add time estimate if verbosity allows
        if self.config.verbosity >= ProgressVerbosity.MODERATE:
            eta = self._estimate_eta(bar_id)
            if eta is not None:
                postfix['eta'] = self._format_time(eta)
        
        # Add memory stats if enabled and verbosity allows
        if (self.config.show_memory_stats and 
            self.config.verbosity >= ProgressVerbosity.DETAILED):
            memory_info = self._get_memory_info()
            if memory_info:
                postfix.update(memory_info)
        
        # Add throughput if verbosity allows
        if self.config.verbosity >= ProgressVerbosity.DETAILED:
            throughput = self._calculate_throughput(bar_id)
            if throughput is not None:
                metadata = self.bar_metadata.get(bar_id, {})
                unit = metadata.get('unit', 'it')
                postfix[f'{unit}/s'] = f'{throughput:.1f}'
        
        return postfix
    
    def _estimate_eta(self, bar_id: str) -> Optional[float]:
        """
        Estimate time remaining using EMA smoothing.
        
        Args:
            bar_id: Bar identifier.
            
        Returns:
            Estimated seconds remaining, or None if cannot estimate.
        """
        if bar_id not in self.active_bars or bar_id not in self.bar_metadata:
            return None
        
        bar = self.active_bars[bar_id]
        metadata = self.bar_metadata[bar_id]
        total = metadata.get('total')
        
        if total is None or bar.n == 0:
            return None
        
        # Calculate average rate using EMA
        if bar_id in self.update_counts and len(self.update_counts[bar_id]) > 0:
            rates = list(self.update_counts[bar_id])
            avg_rate = sum(rates) / len(rates)
        else:
            # Fallback to simple rate
            elapsed = time.time() - self.start_times.get(bar_id, time.time())
            if elapsed == 0:
                return None
            avg_rate = bar.n / elapsed
        
        if avg_rate <= 0:
            return None
        
        remaining = total - bar.n
        eta = remaining / avg_rate
        
        return eta
    
    def _calculate_throughput(self, bar_id: str) -> Optional[float]:
        """
        Calculate throughput (items per second).
        
        Args:
            bar_id: Bar identifier.
            
        Returns:
            Throughput in items/second, or None if cannot calculate.
        """
        if bar_id not in self.start_times:
            return None
        
        elapsed = time.time() - self.start_times[bar_id]
        if elapsed == 0:
            return None
        
        if bar_id in self.active_bars:
            bar = self.active_bars[bar_id]
            return bar.n / elapsed
        
        return None
    
    def _get_memory_info(self) -> Dict[str, str]:
        """
        Get current memory usage information.
        
        Returns:
            Dictionary with memory information (GPU and/or CPU).
        """
        info = {}
        
        # GPU memory
        if torch.cuda.is_available():
            from utils.system.constants import BYTES_PER_GB
            allocated = torch.cuda.memory_allocated() / BYTES_PER_GB
            reserved = torch.cuda.memory_reserved() / BYTES_PER_GB
            info['GPU'] = f'{allocated:.1f}GB'
            if reserved > allocated:
                info['GPU_reserved'] = f'{reserved:.1f}GB'
        
        return info
    
    def _format_time(self, seconds: float) -> str:
        """
        Format time in human-readable format.
        
        Args:
            seconds: Time in seconds.
            
        Returns:
            Formatted time string (e.g., "1h 23m 45s" or "45s").
        """
        if seconds < 60:
            return f'{int(seconds)}s'
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        
        if hours > 0:
            return f'{hours}h {minutes}m {secs}s'
        else:
            return f'{minutes}m {secs}s'
    
    def set_postfix(self, bar_id: str, **metrics) -> None:
        """
        Set postfix metrics for a progress bar.
        
        Args:
            bar_id: Bar identifier.
            **metrics: Metrics to display.
        """
        if bar_id not in self.active_bars:
            return
        
        postfix = self._build_postfix(bar_id, **metrics)
        if postfix:
            self.active_bars[bar_id].set_postfix(postfix)
    
    def close(self, bar_id: str) -> None:
        """
        Close a progress bar.
        
        Args:
            bar_id: Bar identifier to close.
        """
        if bar_id in self.active_bars:
            self.active_bars[bar_id].close()
            del self.active_bars[bar_id]
        
        # Clean up metadata
        if bar_id in self.bar_metadata:
            del self.bar_metadata[bar_id]
        if bar_id in self.start_times:
            del self.start_times[bar_id]
        if bar_id in self.last_update_times:
            del self.last_update_times[bar_id]
        if bar_id in self.update_counts:
            del self.update_counts[bar_id]
    
    def close_all(self) -> None:
        """Close all active progress bars."""
        for bar_id in list(self.active_bars.keys()):
            self.close(bar_id)
    
    def get_elapsed_time(self, bar_id: str) -> Optional[float]:
        """
        Get elapsed time for a progress bar.
        
        Args:
            bar_id: Bar identifier.
            
        Returns:
            Elapsed time in seconds, or None if bar doesn't exist.
        """
        if bar_id not in self.start_times:
            return None
        
        return time.time() - self.start_times[bar_id]

