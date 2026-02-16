"""Unit tests for models."""

import pytest
import numpy as np
import pandas as pd
from models.anomaly_detector import AnomalyDetector
from models.intent_predictor import IntentPredictor
from models.risk_scorer import RiskScorer


@pytest.fixture
def sample_data():
    """Create sample test data."""
    return pd.DataFrame({
        'src_port': np.random.randint(1024, 65535, 100),
        'dst_port': np.random.randint(1, 1024, 100),
        'bytes_sent': np.random.exponential(1000, 100),
        'bytes_received': np.random.exponential(1000, 100),
        'duration': np.random.exponential(10, 100),
        'failed_logins': np.random.poisson(1, 100),
        'successful_logins': np.random.poisson(0.5, 100)
    })


def test_anomaly_detector_initialization():
    """Test anomaly detector initialization."""
    detector = AnomalyDetector()
    assert detector is not None
    assert not detector.is_trained


def test_anomaly_detector_training(sample_data):
    """Test anomaly detector training."""
    detector = AnomalyDetector()
    detector.fit(sample_data)
    assert detector.is_trained


def test_anomaly_detector_prediction(sample_data):
    """Test anomaly detection."""
    detector = AnomalyDetector()
    detector.fit(sample_data)
    
    predictions = detector.predict(sample_data)
    assert len(predictions) == len(sample_data)
    assert all(p in [-1, 1] for p in predictions)


def test_intent_predictor_initialization():
    """Test intent predictor initialization."""
    predictor = IntentPredictor()
    assert predictor is not None
    assert not predictor.is_trained


def test_intent_predictor_training(sample_data):
    """Test intent predictor training."""
    predictor = IntentPredictor()
    labels = pd.Series(['benign'] * 50 + ['brute_force'] * 50)
    
    predictor.fit(sample_data, labels)
    assert predictor.is_trained


def test_intent_predictor_prediction(sample_data):
    """Test intent prediction."""
    predictor = IntentPredictor()
    labels = pd.Series(['benign'] * 50 + ['brute_force'] * 50)
    
    predictor.fit(sample_data, labels)
    predictions = predictor.predict(sample_data)
    
    assert len(predictions) == len(sample_data)
    assert all(p in predictor.INTENT_CLASSES.keys() for p in predictions)


def test_risk_scorer_initialization():
    """Test risk scorer initialization."""
    scorer = RiskScorer()
    assert scorer is not None


def test_risk_scorer_calculation():
    """Test risk scoring."""
    scorer = RiskScorer()
    
    anomaly_scores = np.array([0.2, 0.5, 0.8, 0.9])
    intent_scores = {'benign': np.array([0.8, 0.5, 0.3, 0.2])}
    context_features = {
        'failed_logins': np.array([0, 1, 5, 10]),
        'bytes_sent': np.array([100, 1000, 1e6, 1e7])
    }
    
    scores = scorer.score(anomaly_scores, intent_scores, context_features)
    
    assert len(scores) == 4
    assert all(0 <= s <= 100 for s in scores)


def test_risk_level_classification():
    """Test risk level classification."""
    scorer = RiskScorer()
    
    assert scorer.risk_level(10) == "LOW"
    assert scorer.risk_level(40) == "MEDIUM"
    assert scorer.risk_level(60) == "HIGH"
    assert scorer.risk_level(90) == "CRITICAL"
