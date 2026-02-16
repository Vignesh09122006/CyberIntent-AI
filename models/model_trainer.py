import os
from pathlib import Path

import joblib
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    roc_auc_score,
    confusion_matrix,
    f1_score,
)
import yaml

from src.feature_engineering import load_logs, build_features
from models.anomaly_detector import AnomalyDetector
from models.intent_predictor import IntentPredictor
from models.risk_scorer import compute_risk_score


def train_models(
    data_path: str = "data/sample_logs.csv",
    models_dir: str = "models/saved",
):
    print("Loading data...")
    df = load_logs(data_path)
    X, y = build_features(df)

    print(f"Data shape: X={X.shape}, y={y.shape}, positives={y.sum()}")

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # 1) Anomaly detector on normal traffic only
    print("\nTraining AnomalyDetector (IsolationForest) on normal traffic...")
    normal_mask = y_train == 0
    if normal_mask.sum() == 0:
        raise ValueError("No normal samples in training data to train anomaly detector.")
    anomaly_detector = AnomalyDetector(contamination=0.05)
    anomaly_detector.fit(X_train[normal_mask])
    print(f"Trained on {normal_mask.sum()} normal samples")

    # 2) Intent predictor (supervised)
    print("\nTraining IntentPredictor (RandomForestClassifier)...")
    intent_model = IntentPredictor()
    intent_model.fit(X_train, y_train)
    print("Intent model trained")

    # 3) Evaluate
    print("\nEvaluating on test set...")
    intent_probs = intent_model.predict_proba(X_test)
    intent_preds = (intent_probs >= 0.5).astype(int)

    print("\nClassification report (Intent Predictor):")
    print(classification_report(y_test, intent_preds, digits=4))

    try:
        auc = roc_auc_score(y_test, intent_probs)
        print(f"ROC AUC: {auc:.4f}")
    except ValueError:
        print("Could not compute ROC AUC (only one class in y_test).")

    print("\nConfusion matrix (Intent Predictor):")
    print(confusion_matrix(y_test, intent_preds))

    # 4) Combined risk scores + threshold search
    print("\nComputing combined risk scores for test set...")
    anomaly_scores_test = anomaly_detector.anomaly_score(X_test)
    risk_scores = compute_risk_score(anomaly_scores_test, intent_probs)
    print(f"Risk score range: {risk_scores.min():.3f} - {risk_scores.max():.3f}")

    print("\nSearching best risk threshold by F1 score...")
    thresholds = np.linspace(0.1, 0.9, 17)
    best_t = 0.5
    best_f1 = 0.0

    for t in thresholds:
        preds = (risk_scores >= t).astype(int)
        f1 = f1_score(y_test, preds)
        print(f"  threshold={t:.2f} -> F1={f1:.4f}")
        if f1 > best_f1:
            best_f1 = f1
            best_t = t

    print(f"\nBest risk threshold: {best_t:.2f} (F1={best_f1:.4f})")

    # 5) Save threshold config
    cfg_dir = Path("configs")
    cfg_dir.mkdir(exist_ok=True)
    cfg_path = cfg_dir / "model_config.yaml"
    config = {
        "intent_threshold": 0.5,
        "risk_threshold": float(best_t),
        "f1_at_risk_threshold": float(best_f1),
    }
    with cfg_path.open("w") as f:
        yaml.safe_dump(config, f)
    print(f"Saved threshold config to: {cfg_path}")

    # 6) Save models
    os.makedirs(models_dir, exist_ok=True)
    anomaly_path = os.path.join(models_dir, "anomaly_model.pkl")
    intent_path = os.path.join(models_dir, "intent_model.pkl")

    joblib.dump(anomaly_detector, anomaly_path)
    joblib.dump(intent_model, intent_path)

    print(f"\nSaved anomaly model to: {anomaly_path}")
    print(f"Saved intent model to:  {intent_path}")
    print("Training complete.")


if __name__ == "__main__":
    train_models()
