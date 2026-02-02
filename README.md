# Intelligent System Monitor

An AI-powered system monitoring dashboard with predictive analytics, anomaly detection, and intelligent alerting. Built with Python and Flask for the backend, with machine learning capabilities for performance prediction.

## Features

- **Real-time System Metrics**: Monitor CPU, memory, disk, and network usage
- **AI-Driven Anomaly Detection**: Machine learning models detect unusual system behavior
- **Predictive Analytics**: Forecast resource usage trends and potential issues
- **Smart Alerting**: Intelligent alerts based on learned usage patterns
- **Interactive Dashboard**: Modern web interface with real-time charts
- **REST API**: Programmatic access to all metrics and predictions

## Tech Stack

- **Backend**: Python 3.11+ with Flask
- **ML/AI**: scikit-learn for anomaly detection, Prophet for time-series forecasting
- **Frontend**: HTML5, Tailwind CSS, Chart.js
- **Metrics Collection**: psutil for system metrics
- **Deployment**: Docker, Google Cloud Run

## Project Structure

```
intelligent-system-monitor/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── dashboard.py     # Dashboard routes
│   │   └── api.py           # REST API endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── metrics.py       # System metrics collection
│   │   ├── anomaly.py       # Anomaly detection ML
│   │   └── predictor.py     # Time-series predictions
│   ├── templates/
│   │   ├── base.html
│   │   └── dashboard.html
│   └── static/
│       ├── css/
│       └── js/
├── tests/
│   └── test_metrics.py
├── Dockerfile
├── requirements.txt
├── config.py
└── run.py
```

## Getting Started

### Prerequisites

- Python 3.11+
- pip

### Local Development

```bash
# Clone the repository
git clone https://github.com/randallgann/intelligent-system-monitor.git
cd intelligent-system-monitor

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python run.py
```

Visit `http://localhost:5000` to view the dashboard.

### Docker

```bash
# Build the image
docker build -t intelligent-system-monitor .

# Run the container
docker run -p 5000:5000 intelligent-system-monitor
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/metrics` | GET | Current system metrics |
| `/api/metrics/history` | GET | Historical metrics data |
| `/api/anomalies` | GET | Detected anomalies |
| `/api/predictions` | GET | Resource usage predictions |
| `/api/alerts` | GET | Active alerts |

## Configuration

Environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_ENV` | Environment (development/production) | production |
| `PORT` | Server port | 5000 |
| `METRICS_INTERVAL` | Metrics collection interval (seconds) | 5 |
| `ANOMALY_THRESHOLD` | Anomaly detection sensitivity | 0.95 |

## Deployment

### Google Cloud Run

```bash
# Deploy to Cloud Run
gcloud run deploy intelligent-system-monitor \
  --source . \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

## License

MIT License - see [LICENSE](LICENSE) for details.

## Author

Randall Gann - [gannsystems.pro](https://gannsystems.pro)
