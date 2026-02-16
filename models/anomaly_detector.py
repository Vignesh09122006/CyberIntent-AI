from sklearn.ensemble import IsolationForest
import numpy as np


class AnomalyDetector:
    """
    Unsupervised anomaly detector using IsolationForest.
    Trained only on normal (non-attack) traffic.
    """

    def __init__(self,
                 n_estimators: int = 200,
                 contamination: float = 0.05,
                 random_state: int = 42):
        self.model = IsolationForest(
            n_estimators=n_estimators,
            contamination=contamination,
            random_state=random_state,
        )

    def fit(self, X):
        self.model.fit(X)
        return self

    def anomaly_score(self, X):
        """
        Higher score = more anomalous.
        IsolationForest.decision_function: higher = more NORMAL.
        We invert it so higher means more abnormal.
        """
        raw = self.model.decision_function(X)
        return -raw

    def predict(self, X, threshold: float = None):
        """
        Returns binary anomaly labels:
        1 = anomaly, 0 = normal
        """
        scores = self.anomaly_score(X)
        if threshold is None:
            # Default: top 5% most anomalous
            threshold = np.quantile(scores, 0.95)
        return (scores >= threshold).astype(int)
