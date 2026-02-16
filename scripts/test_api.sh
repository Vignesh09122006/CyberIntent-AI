#!/usr/bin/env bash
set -e

URL="http://127.0.0.1:8000/predict/event"

echo "Sending example event to $URL"
curl -s -X POST "$URL" \
  -H "Content-Type: application/json" \
  -d '{
    "timestamp": "2024-01-15 03:25:00",
    "user_id": "attacker_001",
    "ip_address": "203.0.113.10",
    "action": "port_scan",
    "status": "failed",
    "bytes_transferred": 500,
    "duration_ms": 200,
    "user_agent": "nmap"
  }' | jq .
