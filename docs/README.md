# CyberIntent-AI Documentation

Welcome to the CyberIntent-AI documentation hub!

## Quick Links

- **[Architecture Overview](ARCHITECTURE.md)** - System design and components
- **[Model Documentation](MODELS.md)** - ML models and algorithms
- **[API Reference](API.md)** - REST API endpoints and usage
- **[Main README](../README.md)** - Project overview

## Getting Started

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Configure settings in `.env`
4. Train models: `python scripts/train_models.py`
5. Run dashboard: `streamlit run app/dashboard.py`

## Key Concepts

### Anomaly Detection
Uses Isolation Forest algorithms to detect unusual patterns in network traffic that deviate from normal behavior.

### Intent Prediction
Machine learning models that analyze attack characteristics to predict the attacker's intentions (reconnaissance, data exfiltration, etc.).

### Risk Scoring
Combines multiple signals to produce composite risk scores for threat prioritization and response decisions.

### Automated Response
Execute predefined response actions automatically when threats are detected, or queue for human approval.

## Deployment

- **Local Development**: Run Streamlit dashboard locally
- **Docker**: Use provided Docker Compose files for containerized deployment
- **Cloud**: Deploy FastAPI backend to cloud platforms (AWS, Azure, GCP)

## Support

For issues, questions, or contributions, please see [CONTRIBUTING.md](../CONTRIBUTING.md)
