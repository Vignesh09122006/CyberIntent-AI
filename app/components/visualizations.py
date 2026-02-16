"""Visualization components for Streamlit."""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np


def plot_anomaly_distribution(scores: np.ndarray, threshold: float = 0.7):
    """Plot distribution of anomaly scores."""
    fig = go.Figure(data=[
        go.Histogram(x=scores, name="Anomaly Scores", nbinsx=50)
    ])
    
    fig.add_vline(x=threshold, line_dash="dash", line_color="red", 
                  annotation_text=f"Threshold: {threshold}")
    
    fig.update_layout(
        title="Anomaly Score Distribution",
        xaxis_title="Score",
        yaxis_title="Frequency"
    )
    
    return fig


def plot_risk_timeline(risk_scores: pd.DataFrame):
    """Plot risk scores over time."""
    fig = px.line(risk_scores, x='timestamp', y='risk_score',
                  title="Risk Score Timeline",
                  labels={'timestamp': 'Time', 'risk_score': 'Risk Score'})
    
    return fig


def plot_threat_distribution(threats: pd.DataFrame):
    """Plot threat type distribution."""
    threat_counts = threats['threat_type'].value_counts()
    
    fig = px.pie(values=threat_counts.values, names=threat_counts.index,
                 title="Threat Type Distribution")
    
    return fig


def plot_heatmap(data: np.ndarray, xlabel: str, ylabel: str):
    """Plot heatmap."""
    fig = go.Figure(data=go.Heatmap(z=data))
    
    fig.update_layout(
        title="Activity Heatmap",
        xaxis_title=xlabel,
        yaxis_title=ylabel
    )
    
    return fig


def create_metric_card(label: str, value: str, delta: str = None):
    """Create a metric card."""
    col = st.columns(1)[0]
    
    with col:
        st.metric(label, value, delta=delta)
