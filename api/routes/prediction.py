from pathlib import Path
import sys

from fastapi import APIRouter
import joblib
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from api.schemas import EventIn, PredictionOut
from src.feature_engineering import build_features
from models.risk_scorer import compute_risk_score
from src.response_engine import load_risk_threshold


router = APIRouter(prefix="/predict", tags=["prediction"])

_anomaly_model = None
_intent_model = None


def _load_models():
    global _anomaly_model, _intent_model
    if _anomaly_model is None or _intent_model is None:
        anomaly_path = ROOT / "models" / "saved" / "anomaly_model.pkl"
        intent_path = ROOT / "models" / "saved" / "intent_model.pkl"
        if not anomaly_path.exists() or not intent_path.exists():
            raise FileNotFoundError(
                "Models not found. Run 'python scripts/train_models.py' first."
            )
        _anomaly_model = joblib.load(anomaly_path)
        _intent_model = joblib.load(intent_path)
    return _anomaly_model, _intent_model


@router.post("/event", response_model=PredictionOut)
async def predict_event(event: EventIn):
    anomaly_model, intent_model = _load_models()

    data = event.dict()
    df = pd.DataFrame([data])

    # build_features expects a 'risk_label' column; use dummy 0
    if "risk_label" not in df.columns:
        df["risk_label"] = 0

    X, _ = build_features(df)

    anomaly_scores = anomaly_model.anomaly_score(X)
    intent_probs = intent_model.predict_proba(X)
    risk_scores = compute_risk_score(anomaly_scores, intent_probs)

    anomaly_score = float(anomaly_scores[0])
    intent_prob = float(intent_probs[0])
    risk = float(risk_scores[0])

    threshold = load_risk_threshold(default=0.7)
    recommended_action = "block" if risk >= threshold else "monitor"

    return PredictionOut(
        anomaly_score=anomaly_score,
        intent_probability=intent_prob,
        risk_score=risk,
        recommended_action=recommended_action,
    )
