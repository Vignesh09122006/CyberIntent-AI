"""Data preprocessing and cleaning module."""

import pandas as pd
import numpy as np
from typing import List, Optional, Tuple
import logging

logger = logging.getLogger(__name__)


class DataProcessor:
    """Handle data preprocessing, cleaning, and validation."""

    @staticmethod
    def load_data(filepath: str) -> pd.DataFrame:
        """
        Load data from file.
        
        Args:
            filepath: Path to data file (CSV, JSON, etc.)
            
        Returns:
            Loaded DataFrame
        """
        if filepath.endswith('.csv'):
            return pd.read_csv(filepath)
        elif filepath.endswith('.json'):
            return pd.read_json(filepath)
        else:
            raise ValueError(f"Unsupported file format: {filepath}")

    @staticmethod
    def clean_data(df: pd.DataFrame, drop_duplicates: bool = True) -> pd.DataFrame:
        """
        Clean and validate data.
        
        Args:
            df: Input DataFrame
            drop_duplicates: Whether to drop duplicate rows
            
        Returns:
            Cleaned DataFrame
        """
        df = df.copy()
        
        # Drop duplicates
        if drop_duplicates:
            df = df.drop_duplicates()
            logger.info(f"Dropped duplicates. New shape: {df.shape}")
        
        # Handle missing values
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        for col in numeric_cols:
            if df[col].isna().sum() > 0:
                df[col].fillna(df[col].median(), inplace=True)
        
        return df

    @staticmethod
    def normalize_data(df: pd.DataFrame, columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        Normalize numeric columns to [0, 1].
        
        Args:
            df: Input DataFrame
            columns: Specific columns to normalize (None = all numeric)
            
        Returns:
            Normalized DataFrame
        """
        df = df.copy()
        
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns
        
        for col in columns:
            if col in df.columns:
                min_val = df[col].min()
                max_val = df[col].max()
                if max_val - min_val > 0:
                    df[col] = (df[col] - min_val) / (max_val - min_val)
        
        return df

    @staticmethod
    def filter_by_time_window(
        df: pd.DataFrame,
        time_column: str,
        hours: int = 24
    ) -> pd.DataFrame:
        """
        Filter data to recent time window.
        
        Args:
            df: Input DataFrame
            time_column: Name of timestamp column
            hours: Number of hours to look back
            
        Returns:
            Filtered DataFrame
        """
        df = df.copy()
        df[time_column] = pd.to_datetime(df[time_column])
        
        cutoff = pd.Timestamp.now() - pd.Timedelta(hours=hours)
        return df[df[time_column] >= cutoff]

    @staticmethod
    def split_train_test(
        df: pd.DataFrame,
        test_size: float = 0.2,
        random_state: int = 42
    ) -> Tuple[pd.DataFrame, pd.DataFrame]:
        """
        Split data into train and test sets.
        
        Args:
            df: Input DataFrame
            test_size: Proportion for test set
            random_state: Random seed
            
        Returns:
            Tuple of (train_df, test_df)
        """
        test_split = int(len(df) * test_size)
        test_df = df.sample(n=test_split, random_state=random_state)
        train_df = df.drop(test_df.index)
        
        return train_df, test_df
