import os


class Config:
    """Application configuration."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

    # Metrics configuration
    METRICS_INTERVAL = int(os.environ.get('METRICS_INTERVAL', 5))
    METRICS_HISTORY_SIZE = int(os.environ.get('METRICS_HISTORY_SIZE', 100))

    # Anomaly detection configuration
    ANOMALY_THRESHOLD = float(os.environ.get('ANOMALY_THRESHOLD', 0.95))
    ANOMALY_WINDOW_SIZE = int(os.environ.get('ANOMALY_WINDOW_SIZE', 20))

    # Alert configuration
    CPU_ALERT_THRESHOLD = float(os.environ.get('CPU_ALERT_THRESHOLD', 80.0))
    MEMORY_ALERT_THRESHOLD = float(os.environ.get('MEMORY_ALERT_THRESHOLD', 85.0))
    DISK_ALERT_THRESHOLD = float(os.environ.get('DISK_ALERT_THRESHOLD', 90.0))
