#!/bin/bash
# Run demo script

echo "Starting CyberIntent-AI Demo..."

# Check if models exist
if [ ! -f models/saved/anomaly_model.pkl ]; then
    echo "Models not found. Training models..."
    python scripts/train_models.py
fi

# Generate sample data
echo "Generating sample data..."
python scripts/generate_dataset.py

# Run the dashboard
echo "Starting Streamlit dashboard..."
streamlit run app/dashboard.py

# In another terminal, you can run the API:
# python api/main.py
