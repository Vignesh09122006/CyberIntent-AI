"""Real-time stream processing for network events."""

import pandas as pd
from collections import deque
from typing import Callable, Any, Optional
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


class StreamProcessor:
    """Process network events in real-time streams."""

    def __init__(self, window_size: int = 100, window_seconds: Optional[int] = None):
        """
        Initialize stream processor.
        
        Args:
            window_size: Number of events to buffer
            window_seconds: Time window in seconds (alternative to size)
        """
        self.window_size = window_size
        self.window_seconds = window_seconds
        self.event_buffer = deque(maxlen=window_size)
        self.callbacks = []

    def add_callback(self, callback: Callable[[Any], None]) -> None:
        """
        Register callback for processed events.
        
        Args:
            callback: Function to call with processed event
        """
        self.callbacks.append(callback)

    def process_event(self, event: dict) -> dict:
        """
        Process a single network event.
        
        Args:
            event: Network event dictionary
            
        Returns:
            Processed event
        """
        # Add processing timestamp
        event['processed_at'] = datetime.now()
        
        # Add to buffer
        self.event_buffer.append(event)
        
        # Call registered callbacks
        for callback in self.callbacks:
            try:
                callback(event)
            except Exception as e:
                logger.error(f"Error in callback: {e}")
        
        return event

    def process_batch(self, events: list) -> pd.DataFrame:
        """
        Process batch of events.
        
        Args:
            events: List of event dictionaries
            
        Returns:
            DataFrame of processed events
        """
        df = pd.DataFrame(events)
        
        for event in events:
            self.process_event(event)
        
        return df

    def get_windowed_events(self) -> pd.DataFrame:
        """
        Get events in current window.
        
        Returns:
            DataFrame of buffered events
        """
        return pd.DataFrame(list(self.event_buffer))

    def apply_transformation(self, transform_func: Callable) -> pd.DataFrame:
        """
        Apply transformation to windowed events.
        
        Args:
            transform_func: Function to apply
            
        Returns:
            Transformed DataFrame
        """
        df = self.get_windowed_events()
        
        if df.empty:
            return df
        
        return transform_func(df)

    def filter_events(self, condition: Callable) -> pd.DataFrame:
        """
        Filter current windowed events.
        
        Args:
            condition: Filter condition function
            
        Returns:
            Filtered DataFrame
        """
        df = self.get_windowed_events()
        
        if df.empty:
            return df
        
        return df[df.apply(condition, axis=1)]

    def get_statistics(self) -> dict:
        """Get statistics about buffered events."""
        df = self.get_windowed_events()
        
        if df.empty:
            return {}
        
        numeric_cols = df.select_dtypes(include=['number']).columns
        
        stats = {}
        for col in numeric_cols:
            stats[col] = {
                'mean': df[col].mean(),
                'std': df[col].std(),
                'min': df[col].min(),
                'max': df[col].max(),
            }
        
        return stats

    def clear_buffer(self) -> None:
        """Clear event buffer."""
        self.event_buffer.clear()
        logger.info("Event buffer cleared")
