"""Automated response engine for threat mitigation."""

from enum import Enum
from typing import Dict, List, Optional, Callable
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class ResponseAction(Enum):
    """Types of response actions."""
    LOG_EVENT = "LOG_EVENT"
    ISOLATE_HOST = "ISOLATE_HOST"
    BLOCK_IP = "BLOCK_IP"
    ALERT_ADMIN = "ALERT_ADMIN"
    TERMINATE_SESSION = "TERMINATE_SESSION"
    SNAPSHOT_TRAFFIC = "SNAPSHOT_TRAFFIC"
    RATE_LIMIT = "RATE_LIMIT"


class ActionStatus(Enum):
    """Status of response action execution."""
    PENDING = "PENDING"
    EXECUTING = "EXECUTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class ResponseAction_Record:
    """Record of an executed response action."""

    def __init__(
        self,
        action_type: ResponseAction,
        target: str,
        trigger_event: Dict,
        timestamp: Optional[datetime] = None
    ):
        """
        Initialize response action record.
        
        Args:
            action_type: Type of action
            target: Target of action (IP, host, user, etc.)
            trigger_event: Event that triggered the action
            timestamp: When action was executed
        """
        self.action_type = action_type
        self.target = target
        self.trigger_event = trigger_event
        self.timestamp = timestamp or datetime.now()
        self.status = ActionStatus.PENDING
        self.result = None

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'action': self.action_type.value,
            'target': self.target,
            'status': self.status.value,
            'timestamp': self.timestamp.isoformat(),
            'result': self.result
        }


class ResponseEngine:
    """Execute automated response actions to threats."""

    def __init__(self, auto_enabled: bool = False, timeout: int = 300):
        """
        Initialize response engine.
        
        Args:
            auto_enabled: Whether to auto-execute actions
            timeout: Action timeout in seconds
        """
        self.auto_enabled = auto_enabled
        self.timeout = timeout
        self.action_handlers: Dict[ResponseAction, Callable] = {}
        self.action_history: List[ResponseAction_Record] = []

    def register_handler(self, action: ResponseAction, handler: Callable) -> None:
        """
        Register handler for action type.
        
        Args:
            action: Action type
            handler: Handler function
        """
        self.action_handlers[action] = handler
        logger.info(f"Registered handler for action: {action.value}")

    def execute_action(
        self,
        action: ResponseAction,
        target: str,
        trigger_event: Dict = None,
        auto: bool = False
    ) -> ResponseAction_Record:
        """
        Execute a response action.
        
        Args:
            action: Type of action
            target: Action target
            trigger_event: Event that triggered action
            auto: Whether this is automatic execution
            
        Returns:
            Action record
        """
        record = ResponseAction_Record(action, target, trigger_event or {})
        
        # Check if we should execute
        if auto and not self.auto_enabled:
            logger.info(f"Auto action disabled. Recording pending action: {action.value}")
            self.action_history.append(record)
            return record
        
        # Execute if handler exists
        if action in self.action_handlers:
            try:
                record.status = ActionStatus.EXECUTING
                result = self.action_handlers[action](target, trigger_event)
                record.status = ActionStatus.COMPLETED
                record.result = result
                logger.info(f"Action executed: {action.value} on {target}")
            except Exception as e:
                record.status = ActionStatus.FAILED
                record.result = str(e)
                logger.error(f"Action failed: {action.value} - {e}")
        else:
            logger.warning(f"No handler registered for action: {action.value}")
        
        self.action_history.append(record)
        return record

    def execute_multi_action(
        self,
        actions: List[tuple],
        trigger_event: Dict = None
    ) -> List[ResponseAction_Record]:
        """
        Execute multiple actions.
        
        Args:
            actions: List of (action, target) tuples
            trigger_event: Event triggering actions
            
        Returns:
            List of action records
        """
        results = []
        for action, target in actions:
            result = self.execute_action(action, target, trigger_event)
            results.append(result)
        return results

    def get_action_history(self, limit: int = 50) -> List[Dict]:
        """Get recent action history."""
        recent = self.action_history[-limit:] if self.action_history else []
        return [r.to_dict() for r in recent]

    def get_pending_actions(self) -> List[ResponseAction_Record]:
        """Get pending actions awaiting execution."""
        return [a for a in self.action_history if a.status == ActionStatus.PENDING]

    def approve_pending_action(self, action_idx: int) -> ResponseAction_Record:
        """
        Approve and execute a pending action.
        
        Args:
            action_idx: Index of pending action
            
        Returns:
            Updated action record
        """
        pending = self.get_pending_actions()
        if 0 <= action_idx < len(pending):
            action = pending[action_idx]
            return self.execute_action(
                action.action_type,
                action.target,
                action.trigger_event,
                auto=False
            )
        return None

    def clear_history(self) -> None:
        """Clear action history."""
        self.action_history.clear()
        logger.info("Action history cleared")


# Default action handlers
def log_event_handler(target: str, event: Dict) -> str:
    """Log an event."""
    logger.info(f"Event logged for {target}: {event}")
    return "Event logged"


def alert_admin_handler(target: str, event: Dict) -> str:
    """Alert administrator."""
    logger.warning(f"Admin alert for target {target}")
    return "Admin notified"


def block_ip_handler(target: str, event: Dict) -> str:
    """Block an IP address."""
    logger.warning(f"IP blocked: {target}")
    return f"IP {target} blocked"
