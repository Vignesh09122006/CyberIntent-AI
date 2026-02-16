from pathlib import Path
from typing import Dict, Any

import pandas as pd
import yaml


ROOT = Path(__file__).resolve().parents[1]


def load_risk_threshold(default: float = 0.7) -> float:
    """
    Load default risk threshold from configs/model_config.yaml if present.
    """
    cfg_path = ROOT / "configs" / "model_config.yaml"
    if cfg_path.exists():
        try:
            with cfg_path.open("r") as f:
                cfg = yaml.safe_load(f) or {}
            return float(cfg.get("risk_threshold", default))
        except Exception:
            return default
    return default


def simulate_auto_defense(
    df: pd.DataFrame,
    risk_threshold: float,
    min_events_for_block: int = 3,
) -> Dict[str, Any]:
    """
    Simulate automatic defense actions:
    - Count high-risk events
    - Aggregate by IP
    - Decide which IPs to 'block'
    """
    if "risk_score" not in df.columns or "ip_address" not in df.columns:
        return {
            "high_risk_events": 0,
            "blocked_ips": [],
            "blocked_df": pd.DataFrame(),
        }

    high = df[df["risk_score"] >= risk_threshold]
    high_count = len(high)

    if high.empty:
        return {
            "high_risk_events": 0,
            "blocked_ips": [],
            "blocked_df": pd.DataFrame(),
        }

    summary = (
        high.groupby("ip_address")
        .agg(
            events=("risk_score", "count"),
            max_risk=("risk_score", "max"),
        )
        .reset_index()
    )

    blocked = summary[summary["events"] >= min_events_for_block].copy()
    blocked = blocked.sort_values("max_risk", ascending=False)

    return {
        "high_risk_events": high_count,
        "blocked_ips": blocked["ip_address"].tolist(),
        "blocked_df": blocked,
    }
