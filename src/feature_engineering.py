import pandas as pd
import numpy as np


def load_logs(path: str = "data/sample_logs.csv") -> pd.DataFrame:
    """
    Load the log dataset and normalize the label column.

    Supports:
      - risk_label column (0 = normal, 1 = malicious), OR
      - label column with values like 'benign', 'malicious', etc.
    """
    df = pd.read_csv(path)

    # Parse timestamp if present
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")

    # Normalize label to risk_label (0/1)
    if "risk_label" in df.columns:
        df["risk_label"] = df["risk_label"].astype(int)
    elif "label" in df.columns:
        # Treat benign/normal as 0, everything else as 1
        benign_values = {"benign", "normal", "legit", "legitimate"}
        df["risk_label"] = df["label"].astype(str).str.lower().apply(
            lambda v: 0 if v in benign_values else 1
        )
    else:
        raise ValueError(
            "Dataset must contain either 'risk_label' or 'label' column."
        )

    # Time-based features
    if "timestamp" in df.columns:
        df["hour"] = df["timestamp"].dt.hour
        df["is_night"] = ((df["hour"] < 7) | (df["hour"] > 20)).astype(int)
        # We won't use raw timestamp directly as a feature
        df = df.drop(columns=["timestamp"])
    else:
        df["hour"] = 0
        df["is_night"] = 0

    return df


def build_features(df: pd.DataFrame):
    """
    Build ML-friendly numeric feature matrix X and label vector y.
    Automatically handles numeric + categorical columns.
    """
    # Labels
    y = df["risk_label"].values

    # Drop label columns from features
    cols_to_drop = [c for c in ["risk_label", "label"] if c in df.columns]
    X_raw = df.drop(columns=cols_to_drop)

    # Separate numeric and categorical
    num_cols = X_raw.select_dtypes(include=["number"]).columns.tolist()
    cat_cols = X_raw.select_dtypes(include=["object", "category", "bool"]).columns.tolist()

    # Numeric features
    X_num = X_raw[num_cols].fillna(0)

    # Categorical → one-hot
    if cat_cols:
        X_cat = pd.get_dummies(
            X_raw[cat_cols].astype(str).fillna("missing"),
            prefix=cat_cols,
            drop_first=True,
        )
        X = pd.concat([X_num, X_cat], axis=1)
    else:
        X = X_num

    return X, y
