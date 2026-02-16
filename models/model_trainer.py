import os
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

from src.feature_engineering import load_logs, build_features
from models.anomaly_detector import AnomalyDetector
from models.intent_predictor import IntentPredictor
from models.risk_scorer import compute_risk_score


def train_models(
    data_path: str = "data/sample_logs.csv",
    models_dir: str = "models/saved",
):
    print("📥 Loading data...")
    df = load_logs(data_path)
    X, y = build_features(df)

    print(f"✅ Data shape: X={X.shape}, y={y.shape}, positives={y.sum()}")

    # Train/test split for intent predictor
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    # 1) Train anomaly detector on normal traffic only
    print("\n🧠 Training AnomalyDetector (IsolationForest) on normal traffic...")
    normal_mask = y_train == 0
    if normal_mask.sum() == 0:
        raise ValueError("No normal samples in training data to train anomaly detector.")
    anomaly_detector = AnomalyDetector(contamination=0.05)
    anomaly_detector.fit(X_train[normal_mask])
    print(f"✅ Trained on {normal_mask.sum()} normal samples")

    # 2) Train intent predictor (supervised classifier)
    print("\n🧠 Training IntentPredictor (RandomForestClassifier)...")
    intent_model = IntentPredictor()
    intent_model.fit(X_train, y_train)
    print("✅ Intent model trained")

    # 3) Evaluate on test set
    print("\n📊 Evaluating on test set...")
    intent_probs = intent_model.predict_proba(X_test)
    intent_preds = (intent_probs >= 0.5).astype(int)

    print("\n🔹 Classification report (Intent Predictor):")
    print(classification_report(y_test, intent_preds, digits=4))

    try:
        auc = roc_auc_score(y_test, intent_probs)
        print(f"🔹 ROC AUC: {auc:.4f}")
    except ValueError:
        print("⚠️ Could not compute ROC AUC (only one class in y_test).")

    print("\n🔹 Confusion matrix (Intent Predictor):")
    print(confusion_matrix(y_test, intent_preds))

    # 4) Example combined risk score
    print("\n🧮 Computing combined risk scores for test set (example)...")
    anomaly_scores_test = anomaly_detector.anomaly_score(X_test)
    risk_scores = compute_risk_score(anomaly_scores_test, intent_probs)
    print(f"   Risk score range: {risk_scores.min():.3f} - {risk_scores.max():.3f}")

    # 5) Save models
    os.makedirs(models_dir, exist_ok=True)
    anomaly_path = os.path.join(models_dir, "anomaly_model.pkl")
    intent_path = os.path.join(models_dir, "intent_model.pkl")

    joblib.dump(anomaly_detector, anomaly_path)
    joblib.dump(intent_model, intent_path)

    print(f"\n💾 Saved anomaly model to: {anomaly_path}")
    print(f"💾 Saved intent model to:  {intent_path}")
    print("\n✅ Training complete.")


if __name__ == "__main__":
    train_models()
