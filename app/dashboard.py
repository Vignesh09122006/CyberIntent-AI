import os
import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import joblib

# Make project root importable
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.feature_engineering import load_logs, build_features
from models.risk_scorer import compute_risk_score


@st.cache_resource
def load_models():
    """Load trained models from disk (cached)."""
    anomaly_path = ROOT / "models" / "saved" / "anomaly_model.pkl"
    intent_path = ROOT / "models" / "saved" / "intent_model.pkl"

    if not anomaly_path.exists() or not intent_path.exists():
        raise FileNotFoundError(
            "Trained models not found. Run 'python scripts/train_models.py' first."
        )

    anomaly_model = joblib.load(anomaly_path)
    intent_model = joblib.load(intent_path)
    return anomaly_model, intent_model


@st.cache_data
def load_data_with_scores():
    """
    Load raw logs, compute features, run models, and attach:
      - anomaly_score
      - intent_probability
      - risk_score
      - ground_truth (0/1 from risk_label)
    """
    data_path = ROOT / "data" / "sample_logs.csv"
    if not data_path.exists():
        raise FileNotFoundError(
            "data/sample_logs.csv not found. Run 'python scripts/generate_dataset.py' first."
        )

    # Raw for display
    raw = pd.read_csv(data_path)

    # Processed for ML
    processed = load_logs(str(data_path))
    X, y = build_features(processed)

    # Ensure timestamp is datetime in raw (if present)
    if "timestamp" in raw.columns:
        raw["timestamp"] = pd.to_datetime(raw["timestamp"], errors="coerce")

    anomaly_model, intent_model = load_models()

    anomaly_scores = anomaly_model.anomaly_score(X)
    intent_probs = intent_model.predict_proba(X)
    risk_scores = compute_risk_score(anomaly_scores, intent_probs)

    raw["ground_truth"] = y
    raw["anomaly_score"] = anomaly_scores
    raw["intent_probability"] = intent_probs
    raw["risk_score"] = risk_scores

    return raw


def main():
    st.set_page_config(
        page_title="CyberIntent-AI Dashboard",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("🛡️ CyberIntent-AI")
    st.subheader("Predicting attackers before they strike")

    st.markdown(
        """
**What you see here:**

- Anomaly score from behavior
- Intent probability that an event is part of an attack
- Combined risk score used for auto-block decisions
        """
    )

    df = load_data_with_scores()

    # Sidebar controls
    with st.sidebar:
        st.header("Controls")

        threshold = st.slider(
            "Risk threshold for auto-block",
            min_value=0.0,
            max_value=1.0,
            value=0.7,
            step=0.01,
        )

        show_only_high = st.checkbox(
            "Show only high-risk events", value=True
        )

        top_n = st.number_input(
            "Rows to display",
            min_value=50,
            max_value=int(len(df)),
            value=min(300, len(df)),
            step=50,
        )

        if "user_id" in df.columns:
            users = ["(All)"] + sorted(df["user_id"].astype(str).unique().tolist())
            selected_user = st.selectbox("Filter by user", users, index=0)
        else:
            selected_user = "(All)"

    # Filter by user
    df_view = df.copy()
    if selected_user != "(All)" and "user_id" in df_view.columns:
        df_view = df_view[df_view["user_id"].astype(str) == selected_user]

    # Sort by risk
    df_view = df_view.sort_values("risk_score", ascending=False)
    high_risk_mask = df_view["risk_score"] >= threshold
    high_risk_df = df_view[high_risk_mask]

    if show_only_high:
        table_df = high_risk_df.head(int(top_n))
    else:
        table_df = df_view.head(int(top_n))

    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total events", f"{len(df):,}")
    col2.metric("Malicious (ground truth)", int((df["ground_truth"] == 1).sum()))
    col3.metric("High-risk predicted", len(high_risk_df))
    col4.metric("Risk threshold", f"{threshold:.2f}")

    st.markdown("### Events table")

    display_cols = []
    for c in [
        "timestamp",
        "user_id",
        "ip_address",
        "action",
        "risk_score",
        "intent_probability",
        "anomaly_score",
        "ground_truth",
    ]:
        if c in table_df.columns:
            display_cols.append(c)
    if not display_cols:
        display_cols = table_df.columns

    if table_df.empty:
        st.info(
            "No events exceed the selected risk threshold. "
            "Lower the threshold or disable 'Show only high-risk events'."
        )
    else:
        st.dataframe(
            table_df[display_cols],
            use_container_width=True,
            height=400,
        )

    # Risk over time
    if "timestamp" in df.columns and df["timestamp"].notna().any():
        st.markdown("### Risk over time")
        time_df = df.sort_values("timestamp")
        chart_df = time_df[["timestamp", "risk_score"]].set_index("timestamp")
        st.line_chart(chart_df, height=250)

    # Top suspicious events
    st.markdown("### Top 10 most suspicious events")
    top10 = high_risk_df.head(10)
    if not top10.empty:
        cols = [
            c
            for c in [
                "timestamp",
                "user_id",
                "ip_address",
                "action",
                "risk_score",
                "intent_probability",
            ]
            if c in top10.columns
        ]
        st.table(top10[cols])
    else:
        st.write("No high-risk events for current settings.")

    st.markdown("---")
    st.caption(
        "Models: IsolationForest for anomaly detection + RandomForest for intent prediction."
    )


if __name__ == "__main__":
    main()
