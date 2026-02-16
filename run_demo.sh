#!/usr/bin/env bash
set -e

echo "==========================================="
echo "🛡️  CyberIntent-AI - Demo Runner"
echo "==========================================="

# If using a venv, activate it (uncomment next line and adjust path if needed)
# source venv/bin/activate

echo "📦 Step 1/3: Generating dataset..."
python scripts/generate_dataset.py

echo
echo "🧠 Step 2/3: Training models..."
python scripts/train_models.py

echo
echo "📊 Step 3/3: Launching Streamlit dashboard..."
streamlit run app/dashboard.py
