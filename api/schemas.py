from typing import Optional

from pydantic import BaseModel, Field


class EventIn(BaseModel):
    timestamp: Optional[str] = Field(
        None, example="2024-01-15 03:21:00"
    )
    user_id: Optional[str] = Field(
        "user_001", example="user_001"
    )
    ip_address: Optional[str] = Field(
        "192.168.1.10", example="192.168.1.10"
    )
    action: str = Field("login", example="login")
    status: str = Field("success", example="success")
    bytes_transferred: Optional[int] = Field(0, example=1024)
    duration_ms: Optional[int] = Field(0, example=250)
    user_agent: Optional[str] = Field("api-client", example="curl/7.68.0")


class PredictionOut(BaseModel):
    anomaly_score: float
    intent_probability: float
    risk_score: float
    recommended_action: str
