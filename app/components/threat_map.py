"""Network threat visualization."""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go


def create_threat_map(events: pd.DataFrame):
    """Create network threat visualization."""
    if events.empty:
        st.info("No events to display")
        return
    
    # Create network flow visualization
    fig = go.Figure()
    
    # Add nodes (IPs)
    if 'src_ip' in events.columns and 'dst_ip' in events.columns:
        nodes = list(set(events['src_ip'].tolist() + events['dst_ip'].tolist()))
        
        # Create edges for threat events
        threats = events[events.get('intent_label', '') != 'benign']
        
        if not threats.empty:
            x_edges = []
            y_edges = []
            
            for _, row in threats.head(10).iterrows():
                src = nodes.index(row['src_ip']) if row['src_ip'] in nodes else 0
                dst = nodes.index(row['dst_ip']) if row['dst_ip'] in nodes else 0
                
                x_edges.extend([src, dst, None])
                y_edges.extend([0, 1, None])
            
            fig.add_trace(go.Scatter(
                x=x_edges, y=y_edges, mode='lines',
                line=dict(color='red', width=2),
                name='Threat Traffic'
            ))
    
    st.plotly_chart(fig, use_container_width=True)


def display_network_topology(events: pd.DataFrame):
    """Display network topology summary."""
    if events.empty:
        st.info("No network data")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        if 'src_ip' in events.columns:
            unique_sources = events['src_ip'].nunique()
            st.metric("Unique Source IPs", unique_sources)
    
    with col2:
        if 'dst_ip' in events.columns:
            unique_destinations = events['dst_ip'].nunique()
            st.metric("Unique Destination IPs", unique_destinations)
