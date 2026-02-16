import numpy as np


def normalize_scores(scores):
    scores = np.asarray(scores, dtype=float)
    if scores.size == 0:
        return scores
    min_s = scores.min()
    max_s = scores.max()
    if max_s - min_s < 1e-9:
        return np.zeros_like(scores)
    return (scores - min_s) / (max_s - min_s)


def compute_risk_score(anomaly_scores, intent_probs,
                       w_anomaly: float = 0.4,
                       w_intent: float = 0.6):
    """
    Combine anomaly score and intent probability into a 0–1 risk score.
    """
    a = normalize_scores(anomaly_scores)
    i = np.clip(np.asarray(intent_probs, dtype=float), 0.0, 1.0)
    risk = w_anomaly * a + w_intent * i
    return np.clip(risk, 0.0, 1.0)
