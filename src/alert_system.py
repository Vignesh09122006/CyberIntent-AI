"""Alert system for threat notifications."""

from enum import Enum
from datetime import datetime
from typing import List, Dict, Optional, Callable
import logging

logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4


class AlertType(Enum):
    """Types of alerts."""
    ANOMALY_DETECTED = "ANOMALY_DETECTED"
    INTENT_PREDICTED = "INTENT_PREDICTED"
    HIGH_RISK = "HIGH_RISK"
    RESPONSE_TRIGGERED = "RESPONSE_TRIGGERED"
    THRESHOLD_EXCEEDED = "THRESHOLD_EXCEEDED"


class Alert:
    """Represent a security alert."""

    def __init__(
        self,
        alert_type: AlertType,
        severity: AlertSeverity,
        message: str,
        details: Dict = None,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize alert.
        
        Args:
            alert_type: Type of alert
            severity: Severity level
            message: Alert message
            details: Additional details
            timestamp: Alert timestamp
        """
        self.alert_type = alert_type
        self.severity = severity
        self.message = message
        self.details = details or {}
        self.timestamp = timestamp or datetime.now()
        self.acknowledged = False

    def to_dict(self) -> Dict:
        """Convert alert to dictionary."""
        return {
            'type': self.alert_type.value,
            'severity': self.severity.name,
            'message': self.message,
            'details': self.details,
            'timestamp': self.timestamp.isoformat(),
            'acknowledged': self.acknowledged
        }

    def __str__(self) -> str:
        """String representation."""
        return f"[{self.severity.name}] {self.alert_type.value}: {self.message}"


class AlertSystem:
    """Manage system alerts and notifications."""

    def __init__(self):
        """Initialize alert system."""
        self.alerts: List[Alert] = []
        self.handlers: List[Callable] = []
        self.thresholds = {
            'anomaly_score': 0.7,
            'risk_score': 70,
            'failed_logins': 5
        }

    def register_handler(self, handler: Callable) -> None:
        """
        Register alert handler.
        
        Args:
            handler: Function to handle alerts
        """
        self.handlers.append(handler)

    def raise_alert(self, alert: Alert) -> None:
        """
        Raise an alert.
        
        Args:
            alert: Alert to raise
        """
        self.alerts.append(alert)
        logger.warning(f"Alert raised: {alert}")
        
        # Call all handlers
        for handler in self.handlers:
            try:
                handler(alert)
            except Exception as e:
                logger.error(f"Error in alert handler: {e}")

    def check_anomaly_score(self, score: float, context: Dict = None) -> Optional[Alert]:
        """
        Check anomaly score and raise alert if needed.
        
        Args:
            score: Anomaly score (0-1)
            context: Additional context
            
        Returns:
            Alert if raised, None otherwise
        """
        if score >= self.thresholds['anomaly_score']:
            alert = Alert(
                alert_type=AlertType.ANOMALY_DETECTED,
                severity=AlertSeverity.HIGH if score > 0.85 else AlertSeverity.MEDIUM,
                message=f"Anomaly detected with score {score:.2f}",
                details={'score': score, 'context': context or {}}
            )
            self.raise_alert(alert)
            return alert
        return None

    def check_risk_score(self, score: float, context: Dict = None) -> Optional[Alert]:
        """
        Check risk score and raise alert if needed.
        
        Args:
            score: Risk score (0-100)
            context: Additional context
            
        Returns:
            Alert if raised, None otherwise
        """
        if score >= self.thresholds['risk_score']:
            severity = (
                AlertSeverity.CRITICAL if score > 85
                else AlertSeverity.HIGH if score > 75
                else AlertSeverity.MEDIUM
            )
            alert = Alert(
                alert_type=AlertType.HIGH_RISK,
                severity=severity,
                message=f"High risk activity detected ({score:.0f})",
                details={'score': score, 'context': context or {}}
            )
            self.raise_alert(alert)
            return alert
        return None

    def set_threshold(self, threshold_name: str, value: float) -> None:
        """Set alert threshold."""
        if threshold_name in self.thresholds:
            self.thresholds[threshold_name] = value
            logger.info(f"Threshold '{threshold_name}' set to {value}")

    def get_recent_alerts(self, limit: int = 10) -> List[Alert]:
        """Get recent alerts."""
        return self.alerts[-limit:] if self.alerts else []

    def acknowledge_alert(self, alert_idx: int) -> None:
        """Acknowledge an alert."""
        if 0 <= alert_idx < len(self.alerts):
            self.alerts[alert_idx].acknowledged = True

    def clear_acknowledged(self) -> None:
        """Clear acknowledged alerts."""
        self.alerts = [a for a in self.alerts if not a.acknowledged]
