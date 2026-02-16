import os
import sys
from pathlib import Path

import streamlit as st
from streamlit_autorefresh import st_autorefresh
import pandas as pd
import joblib

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))

from src.feature_engineering import load_logs, build_features
from models.risk_scorer import compute_risk_score
from src.response_engine import load_risk_threshold, simulate_auto_defense


@st.cache_resource
def load_models():
    anomaly_path = ROOT / "models" / "saved" / "anomaly_model.pkl"
    intent_path = ROOT / "models" / "saved" / "intent_model.pkl"

    if not anomaly_path.exists() or not intent_path.exists():
        raise FileNotFoundError(
            "Trained models not found. Run 'python scripts/train_models.py' first."
        )

    anomaly_model = joblib.load(anomaly_path)
    intent_model = joblib.load(intent_path)
    return anomaly_model, intent_model


@st.cache_data(ttl=5)
def load_data_with_scores(data_path_str: str):
    """
    Load logs from given CSV path, compute:
      - anomaly_score
      - intent_probability
      - risk_score
      - ground_truth

    ttl=5 means cache is refreshed at most every 5 seconds.
    """
    data_path = Path(data_path_str)
    if not data_path.exists():
        raise FileNotFoundError(f"{data_path} not found")

    raw = pd.read_csv(data_path)

    processed = load_logs(str(data_path))
    X, y = build_features(processed)

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

    st.title("CyberIntent-AI")
    st.subheader("Predicting attackers before they strike")

    sample_path = ROOT / "data" / "sample_logs.csv"
    live_path = ROOT / "data" / "live_stream.csv"

    with st.sidebar:
        st.header("Mode")

        live_mode = st.checkbox(
            "Live simulation mode (use data/live_stream.csv)", value=False
        )

        auto_refresh_sec = 3
        if live_mode:
            auto_refresh_sec = st.slider(
                "Auto-refresh every (seconds)",
                min_value=1,
                max_value=10,
                value=3,
            )
            # Trigger auto-refresh
            st_autorefresh(
                interval=auto_refresh_sec * 1000,
                key="live_autorefresh",
            )
            st.caption(
                "Run 'python scripts/start_stream_simulator.py' in another "
                "terminal to feed live data."
            )

        st.header("Risk & defense controls")

        default_threshold = load_risk_threshold(default=0.7)
        st.caption(f"Default risk threshold from training: {default_threshold:.2f}")

        threshold = st.slider(
            "Risk threshold for auto-block",
            min_value=0.0,
            max_value=1.0,
            value=float(default_threshold),
            step=0.01,
        )

        min_events_for_block = st.number_input(
            "Min high-risk events before blocking an IP",
            min_value=1,
            max_value=20,
            value=3,
            step=1,
        )

        show_only_high = st.checkbox(
            "Show only high-risk events in table", value=True
        )

        top_n = st.number_input(
            "Rows to display in events table",
            min_value=50,
            max_value=5000,
            value=300,
            step=50,
        )

        filter_user = st.checkbox("Filter by user_id", value=False)
        selected_user = "(All)"
        if filter_user:
            # We'll populate choices after loading data
            selected_user = None  # placeholder

    # Choose data source based on mode
    if live_mode:
        if not live_path.exists():
            st.warning(
                "Live mode is ON but data/live_stream.csv does not exist yet.\n\n"
                "Open another terminal and run:\n"
                "`python scripts/start_stream_simulator.py --delay 0.5 --chunk-size 10`"
            )
            st.stop()
        data_path = live_path
        st.info(f"Live mode: reading {data_path}")
    else:
        data_path = sample_path
        st.caption(f"Static mode: using {data_path.name}")

    # Load and score data
    df = load_data_with_scores(str(data_path))

    # Now that df is available, update user filter options
    if filter_user and "user_id" in df.columns:
        with st.sidebar:
            users = ["(All)"] + sorted(df["user_id"].astype(str).unique().tolist())
            selected_user = st.selectbox("User", users, index=0)
    else:
        selected_user = "(All)"

    # Table view (optionally filtered by user)
    df_view = df.copy()
    if selected_user != "(All)" and "user_id" in df_view.columns:
        df_view = df_view[df_view["user_id"].astype(str) == selected_user]

    df_view = df_view.sort_values("risk_score", ascending=False)
    high_risk_mask = df_view["risk_score"] >= threshold
    high_risk_df = df_view[high_risk_mask]

    if show_only_high:
        table_df = high_risk_df.head(int(top_n))
    else:
        table_df = df_view.head(int(top_n))

    # Auto-defense always uses the full dataset (not filtered)
    defense = simulate_auto_defense(
        df, risk_threshold=threshold, min_events_for_block=min_events_for_block
    )

    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total events (this source)", f"{len(df):,}")
    col2.metric("Malicious (ground truth)", int((df["ground_truth"] == 1).sum()))
    col3.metric("High-risk events (global)", defense["high_risk_events"])
    col4.metric("Blocked IPs (simulated)", len(defense["blocked_ips"]))

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

    # Blocked IPs
    st.markdown("### Auto-defense simulation: blocked IPs")
    blocked_df = defense["blocked_df"]
    if blocked_df is not None and not blocked_df.empty:
        st.write(
            f"Blocking IPs with at least {min_events_for_block} events "
            f"above risk {threshold:.2f}."
        )
        st.table(blocked_df)
    else:
        st.write("No IPs meet the criteria for blocking at current settings.")

    st.markdown("---")
    st.caption(
        "Models: IsolationForest for anomaly detection + RandomForest for intent prediction. "
        "Risk threshold learned automatically during training. "
        "Live mode uses a streaming file that is appended over time."
    )


if __name__ == "__main__":
    main()
