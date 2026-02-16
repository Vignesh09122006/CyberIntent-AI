"""Live monitoring page."""

import streamlit as st

st.set_page_config(
    page_title="Live Monitor - CyberIntent-AI",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Live Monitor")
st.markdown("Real-time network activity monitoring")

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["Live Events", "Active Sessions", "Threat Map"])

with tab1:
    st.subheader("Real-time Events Stream")
    st.write("Streaming network events...")

with tab2:
    st.subheader("Active Sessions")
    st.write("Current network sessions...")

with tab3:
    st.subheader("Network Threat Map")
    st.write("Geographic threat visualization...")
