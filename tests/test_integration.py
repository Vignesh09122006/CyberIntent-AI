"""Integration tests."""

import pytest
import pandas as pd
from src.data_processor import DataProcessor
from src.feature_engineering import FeatureEngine
from models.anomaly_detector import AnomalyDetector
from models.intent_predictor import IntentPredictor


@pytest.fixture
def sample_csv(tmp_path):
    """Create sample CSV for testing."""
    df = pd.DataFrame({
        'timestamp': pd.date_range('2024-01-01', periods=100, freq='1min'),
        'src_ip': ['192.168.1.1'] * 100,
        'dst_ip': ['10.0.0.1'] * 100,
        'src_port': range(49152, 49252),
        'dst_port': [80, 443] * 50,
        'protocol': ['TCP'] * 100,
        'bytes_sent': [1000] * 100,
        'bytes_received': [2000] * 100,
        'duration': [5.0] * 100,
        'failed_logins': [0] * 90 + [1] * 10,
        'successful_logins': [1] * 100,
        'intent_label': ['benign'] * 90 + ['brute_force'] * 10
    })
    
    csv_path = tmp_path / "sample.csv"
    df.to_csv(csv_path, index=False)
    
    return str(csv_path), df


def test_data_loading(sample_csv):
    """Test data loading."""
    csv_path, expected_df = sample_csv
    
    df = DataProcessor.load_data(csv_path)
    assert len(df) == len(expected_df)
    assert list(df.columns) == list(expected_df.columns)


def test_data_cleaning(sample_csv):
    """Test data cleaning."""
    csv_path, _ = sample_csv
    df = DataProcessor.load_data(csv_path)
    
    cleaned = DataProcessor.clean_data(df)
    assert len(cleaned) == len(df)


def test_feature_engineering(sample_csv):
    """Test feature engineering pipeline."""
    csv_path, df = sample_csv
    
    features = FeatureEngine.create_all_features(df)
    assert len(features) == len(df)
    assert len(features.columns) > 0


def test_model_training_pipeline(sample_csv):
    """Test complete training pipeline."""
    csv_path, df = sample_csv
    
    # Feature engineering
    features = FeatureEngine.create_all_features(df)
    
    # Train anomaly detector
    detector = AnomalyDetector()
    detector.fit(features)
    predictions = detector.predict(features)
    assert len(predictions) == len(features)
    
    # Train intent predictor
    predictor = IntentPredictor()
    predictor.fit(features, df['intent_label'])
    predictions = predictor.predict(features)
    assert len(predictions) == len(features)
