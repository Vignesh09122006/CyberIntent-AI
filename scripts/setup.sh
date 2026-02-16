#!/bin/bash
# Setup script for CyberIntent-AI

echo "Setting up CyberIntent-AI..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

# Create necessary directories
mkdir -p logs
mkdir -p data/raw
mkdir -p data/processed
mkdir -p models/saved

# Create .env file if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo ".env file created. Please update with your configuration."
fi

echo "Setup completed successfully!"
echo ""
echo "To activate the environment, run:"
echo "    source venv/bin/activate"
echo ""
echo "To train models, run:"
echo "    python scripts/train_models.py"
echo ""
echo "To run the dashboard, run:"
echo "    streamlit run app/dashboard.py"
