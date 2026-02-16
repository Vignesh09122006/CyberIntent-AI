# API Documentation

## Overview

CyberIntent-AI provides a comprehensive REST API for integration with external systems and automation workflows.

## Base URL
```
http://localhost:8000
```

## Authentication
Currently, the API is open. Production deployments should implement authentication via API keys or OAuth2.

## Response Format
All responses are JSON:

```json
{
  "status": "success|error",
  "data": {},
  "error": null,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

## Prediction Endpoints

### POST /api/predict/
Get anomaly and intent predictions for network events.

**Request:**
```json
{
  "events": [
    {
      "timestamp": "2024-01-15T10:00:00Z",
      "src_ip": "192.168.1.10",
      "dst_ip": "10.0.0.5",
      "src_port": 54321,
      "dst_port": 80,
      "protocol": "TCP",
      "bytes_sent": 1024,
      "bytes_received": 2048,
      "duration": 5.2,
      "failed_logins": 0,
      "successful_logins": 1
    }
  ],
  "model_type": "all"
}
```

**Response:**
```json
{
  "status": "success",
  "predictions": [
    {
      "event_id": "uuid",
      "timestamp": "2024-01-15T10:00:00Z",
      "anomaly_score": 0.35,
      "anomaly_label": "normal",
      "intent_prediction": "benign",
      "intent_probabilities": {
        "benign": 0.92,
        "brute_force": 0.02,
        "reconnaissance": 0.04,
        "data_exfiltration": 0.01,
        "ddos": 0.01
      },
      "risk_score": 25,
      "risk_level": "LOW",
      "should_alert": false
    }
  ],
  "count": 1
}
```

**Status Codes:**
- 200: Success
- 400: Bad request
- 500: Internal error

---

### GET /api/predict/{event_id}
Retrieve prediction for a specific event.

**Response:**
```json
{
  "event_id": "uuid",
  "prediction": {
    "anomaly_score": 0.35,
    "intent": "benign",
    "risk_score": 25
  }
}
```

---

### POST /api/predict/batch
Process batch predictions asynchronously.

**Request:**
Same as /api/predict/

**Response:**
```json
{
  "batch_id": "uuid",
  "status": "processing",
  "event_count": 1000
}
```

---

## Monitoring Endpoints

### GET /api/monitor/status
Get system health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "CyberIntent-AI",
  "version": "0.1.0",
  "uptime_seconds": 3600,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### GET /api/monitor/metrics
Get real-time metrics and statistics.

**Response:**
```json
{
  "total_events_processed": 10234,
  "anomalies_detected": 87,
  "threats_identified": 34,
  "high_risk_count": 12,
  "alerts_total": 28,
  "alerts_unacknowledged": 5,
  "responses_executed": 8,
  "average_prediction_time_ms": 45.2,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### GET /api/monitor/events?limit=100
Get recent detected events.

**Query Parameters:**
- `limit` (default: 100) - Maximum events to return
- `start_time` (optional) - ISO 8601 timestamp
- `end_time` (optional) - ISO 8601 timestamp

**Response:**
```json
{
  "events": [
    {
      "event_id": "uuid",
      "timestamp": "2024-01-15T10:30:00Z",
      "type": "ANOMALY",
      "severity": "MEDIUM"
    }
  ],
  "count": 10
}
```

---

### GET /api/monitor/performance
Get performance metrics.

**Response:**
```json
{
  "cpu_usage_percent": 35.2,
  "memory_usage_percent": 42.1,
  "prediction_latency_ms": 45.2,
  "throughput_events_per_second": 156.3,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Response Endpoints

### POST /api/response/action
Execute a response action.

**Query Parameters:**
- `action` - Action type (block_ip, isolate_host, etc.)
- `target` - Action target (IP, hostname, etc.)
- `auto` (default: false) - Auto-execute flag

**Request:**
```json
{
  "trigger_event": {
    "event_id": "uuid",
    "threat_type": "brute_force"
  }
}
```

**Response:**
```json
{
  "action_id": "uuid",
  "action": "block_ip",
  "target": "203.0.113.1",
  "status": "executing",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### GET /api/response/history?limit=50
Get response action history.

**Query Parameters:**
- `limit` (default: 50) - Maximum actions to return
- `status` (optional) - Filter by status (pending, executed, failed)

**Response:**
```json
{
  "actions": [
    {
      "action_id": "uuid",
      "action": "block_ip",
      "target": "203.0.113.1",
      "status": "completed",
      "timestamp": "2024-01-15T10:30:00Z",
      "result": "IP blocked"
    }
  ],
  "count": 10,
  "limit": 50
}
```

---

### GET /api/response/pending
Get pending actions awaiting approval.

**Response:**
```json
{
  "pending_actions": [
    {
      "action_id": "uuid",
      "action": "isolate_host",
      "target": "192.168.1.50",
      "status": "pending_approval",
      "timestamp": "2024-01-15T10:30:00Z"
    }
  ],
  "count": 2
}
```

---

### POST /api/response/approve/{action_id}
Approve a pending action.

**Response:**
```json
{
  "action_id": "uuid",
  "status": "approved",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

### POST /api/response/reject/{action_id}
Reject a pending action.

**Response:**
```json
{
  "action_id": "uuid",
  "status": "rejected",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

---

## Error Responses

### 400 Bad Request
```json
{
  "error": "Invalid request parameters",
  "details": "Field 'events' is required"
}
```

### 404 Not Found
```json
{
  "error": "Resource not found",
  "resource_id": "uuid"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal server error",
  "message": "An unexpected error occurred"
}
```

---

## Rate Limiting
- Not currently implemented
- Production deployments should implement rate limiting

## Pagination
For endpoints returning lists, use:
- `skip` - Number of items to skip
- `limit` - Number of items to return

## WebSocket (Future)
Real-time event streaming via WebSocket at `/api/ws/events`
