from sklearn.ensemble import RandomForestClassifier
import numpy as np


class IntentPredictor:
    """
    Supervised classifier predicting malicious intent (0/1).
    """

    def __init__(self,
                 n_estimators: int = 200,
                 random_state: int = 42):
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            n_jobs=-1,
            class_weight="balanced",
        )

    def fit(self, X, y):
        self.model.fit(X, y)
        return self

    def predict_proba(self, X):
        """Return probability of class 1 (attack)."""
        return self.model.predict_proba(X)[:, 1]

    def predict(self, X, threshold: float = 0.5):
        proba = self.predict_proba(X)
        return (proba >= threshold).astype(int)
