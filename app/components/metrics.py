"""Metric display components."""

import streamlit as st
import pandas as pd


def display_security_metrics(metrics: dict):
    """Display security metrics in a grid."""
    cols = st.columns(len(metrics))
    
    for col, (label, value) in zip(cols, metrics.items()):
        with col:
            st.metric(label, value)


def display_threat_summary(data: pd.DataFrame):
    """Display threat summary statistics."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Events", len(data))
    
    with col2:
        anomalies = (data.get('anomaly_score', 0) > 0.7).sum() if 'anomaly_score' in data else 0
        st.metric("Anomalies", anomalies)
    
    with col3:
        high_risk = (data.get('risk_score', 0) > 70).sum() if 'risk_score' in data else 0
        st.metric("High Risk", high_risk)


def display_alert_summary(alerts: list):
    """Display alert summary."""
    if not alerts:
        st.info("No alerts")
        return
    
    severity_counts = {}
    for alert in alerts:
        severity = alert.get('severity', 'UNKNOWN')
        severity_counts[severity] = severity_counts.get(severity, 0) + 1
    
    cols = st.columns(len(severity_counts))
    
    for col, (severity, count) in zip(cols, severity_counts.items()):
        with col:
            st.metric(f"{severity} Alerts", count)
