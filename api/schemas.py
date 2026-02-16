"""API request/response schemas."""

from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from datetime import datetime


class NetworkEvent(BaseModel):
    """Network event schema."""
    timestamp: datetime
    user_id: str
    src_ip: str
    dst_ip: str
    src_port: int
    dst_port: int
    protocol: str
    bytes_sent: float
    bytes_received: float
    duration: float
    failed_logins: int = 0
    successful_logins: int = 0


class PredictionRequest(BaseModel):
    """Prediction request schema."""
    events: List[Dict]
    model_type: Optional[str] = "all"  # 'anomaly', 'intent', or 'all'


class PredictionResponse(BaseModel):
    """Prediction response schema."""
    event_id: str
    timestamp: datetime
    anomaly_score: Optional[float] = None
    anomaly_label: Optional[str] = None
    intent_prediction: Optional[str] = None
    intent_probabilities: Optional[Dict[str, float]] = None
    risk_score: Optional[float] = None
    risk_level: Optional[str] = None
    should_alert: bool


class AlertRequest(BaseModel):
    """Alert request schema."""
    alert_type: str
    severity: str
    message: str
    details: Optional[Dict] = None


class AlertResponse(BaseModel):
    """Alert response schema."""
    alert_id: str
    alert_type: str
    severity: str
    message: str
    timestamp: datetime
    acknowledged: bool = False


class ResponseActionRequest(BaseModel):
    """Response action request schema."""
    action: str
    target: str
    trigger_event: Optional[Dict] = None
    auto: bool = False


class ResponseActionResponse(BaseModel):
    """Response action response schema."""
    action_id: str
    action: str
    target: str
    status: str
    timestamp: datetime
    result: Optional[str] = None


class MetricsResponse(BaseModel):
    """Metrics response schema."""
    total_events: int
    anomalies_detected: int
    threats_identified: int
    high_risk_count: int
    alerts_raised: int
    responses_executed: int
    timestamp: datetime


class StatusResponse(BaseModel):
    """System status response schema."""
    service: str
    status: str
    version: str
    uptime_seconds: float
    metrics: MetricsResponse
