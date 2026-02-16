"""
Train all models (anomaly detector + intent predictor).
"""

import sys
import os

CURRENT_DIR = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from models.model_trainer import train_models


def main():
    print("=" * 60)
    print("🧠  CyberIntent-AI Model Trainer")
    print("=" * 60)
    train_models(
        data_path="data/sample_logs.csv",
        models_dir="models/saved",
    )


if __name__ == "__main__":
    main()
