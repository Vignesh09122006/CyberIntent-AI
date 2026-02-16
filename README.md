# CyberIntent-AI 🛡️

A comprehensive AI-powered cybersecurity threat detection and intent prediction system that combines anomaly detection, intent analysis, and automated response mechanisms to protect your network infrastructure.

## 🌟 Features

- **Real-time Anomaly Detection**: Isolation Forest-based detection of unusual network behavior
- **Attack Intent Prediction**: Machine learning model that predicts attacker intentions
- **Risk Scoring Engine**: Multi-factor risk assessment for prioritized threat response
- **Live Monitoring Dashboard**: Real-time visualization of network activity and threats
- **Automated Response System**: Automated mitigation actions for detected threats
- **FastAPI Backend**: REST API for integration with existing systems
- **Streamlit UI**: Interactive web interface for monitoring and analysis
- **Network Simulation**: Synthetic data generation for testing and training

## 📋 Prerequisites

- Python 3.8+
- Docker & Docker Compose (optional)
- 4GB RAM minimum
- Linux/macOS/Windows

## 🚀 Quick Start

### 1. Clone Repository
```bash
git clone https://github.com/Vignesh09122006/CyberIntent-AI.git
cd CyberIntent-AI
```

### 2. Setup Environment
```bash
cp .env.example .env
bash scripts/setup.sh
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train Models
```bash
python scripts/train_models.py
```

### 5. Run Application

**Option A: Streamlit Dashboard**
```bash
streamlit run app/dashboard.py
```

**Option B: FastAPI Server**
```bash
python api/main.py
```

**Option C: Docker**
```bash
docker-compose up
```

## 📁 Project Structure

```
CyberIntent-AI/
├── data/              # Data files and generators
├── models/            # ML models and training pipeline
├── src/               # Core modules (processing, features, alerts)
├── app/               # Streamlit dashboard and components
├── api/               # FastAPI backend and routes
├── tests/             # Unit and integration tests
├── notebooks/         # Jupyter notebooks for exploration
├── configs/           # Configuration files
├── scripts/           # Setup and utility scripts
├── docs/              # Documentation and architecture
└── docker/            # Docker configuration
```

## 🧠 Models

### Anomaly Detector
- **Algorithm**: Isolation Forest
- **Purpose**: Detect unusual network patterns
- **Input**: Network features (time-series)
- **Output**: Anomaly score (0-1)

### Intent Predictor
- **Algorithm**: Gradient Boosting / Neural Network
- **Purpose**: Predict attacker intentions
- **Input**: Feature set with context
- **Output**: Intent classification (Low/Medium/High)

### Risk Scorer
- **Purpose**: Composite risk assessment
- **Input**: Anomaly scores, intent predictions
- **Output**: Risk level (0-100)

## 📊 API Endpoints

### Prediction
- `POST /api/predict` - Get anomaly and intent predictions
- `GET /api/predict/{event_id}` - Retrieve prediction details

### Monitoring
- `GET /api/monitor/status` - System health check
- `GET /api/monitor/metrics` - Real-time metrics
- `GET /api/monitor/events` - Stream of detected events

### Response
- `POST /api/response/action` - Execute response action
- `GET /api/response/history` - View response history

See [docs/API.md](docs/API.md) for full API documentation.

## 🔧 Configuration

Edit `configs/config.yaml` for main settings:
```yaml
model:
  anomaly_threshold: 0.7
  intent_threshold: 0.6
  
alert:
  enabled: true
  rules:
    - condition: "risk > 80"
      action: "email"
      
response:
  auto_enabled: true
  timeout: 300
```

## 🧪 Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific test module:
```bash
pytest tests/test_models.py -v
```

Run with coverage:
```bash
pytest tests/ --cov=src --cov=models
```

## 📚 Documentation

- [Architecture](docs/ARCHITECTURE.md) - System design overview
- [Models](docs/MODELS.md) - Detailed model documentation
- [API](docs/API.md) - API reference
- [Contributing](CONTRIBUTING.md) - Contribution guidelines

## 🔬 Notebooks

- **01_data_exploration.ipynb** - EDA and feature analysis
- **02_model_experiments.ipynb** - Model training and tuning
- **03_visualization.ipynb** - Visualization prototypes
- **04_demo_scenario.ipynb** - End-to-end demo walkthrough

## 📈 Sample Workflow

1. **Data Ingestion**: Raw network logs → Data Pipeline
2. **Feature Engineering**: Extract relevant features from logs
3. **Anomaly Detection**: Isolation Forest identifies suspicious patterns
4. **Intent Analysis**: Predict attacker intentions
5. **Risk Assessment**: Calculate composite risk score
6. **Alerting**: Generate alerts based on thresholds
7. **Response**: Execute automated remediation or notify team

## 🚨 Alert Types

- `ANOMALY_DETECTED` - Unusual pattern found
- `INTENT_PREDICTED` - Predicted attacker behavior
- `HIGH_RISK` - Risk score exceeds threshold
- `RESPONSE_TRIGGERED` - Automated response executed

## 🛡️ Response Actions

- `LOG_EVENT` - Record event details
- `ISOLATE_HOST` - Quarantine suspicious host
- `BLOCK_IP` - Add to blocklist
- `ALERT_ADMIN` - Notify security team
- `SNAPSHOT_TRAFFIC` - Capture network traffic
- `TERMINATE_SESSION` - Kill suspicious sessions

## 🐳 Docker Deployment

Build and run:
```bash
docker-compose build
docker-compose up
```

Services:
- **API**: http://localhost:8000
- **Dashboard**: http://localhost:8501
- **Docs**: http://localhost:8000/docs

## 📊 Performance

- Prediction latency: <100ms
- Throughput: 10,000+ events/second
- Memory usage: ~500MB base
- CPU: Scales with event volume

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 👨‍💻 Author

**Vignesh** - [GitHub](https://github.com/Vignesh09122006)

## 📞 Support

- 📧 Email: support@example.com
- 💬 Discussions: GitHub Discussions
- 🐛 Issues: GitHub Issues

## 🗺️ Roadmap

- [ ] Multi-model ensemble support
- [ ] Custom model integration
- [ ] Advanced visualization options
- [ ] Threat intelligence integration
- [ ] Machine learning model marketplace
- [ ] Kubernetes deployment support

---

**Stay Secure! 🔐**
