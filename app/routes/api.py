"""REST API routes."""

from flask import Blueprint, jsonify, current_app
from app.services.metrics import MetricsCollector
from app.services.anomaly import AnomalyDetector

api_bp = Blueprint('api', __name__)

# Initialize services
metrics_collector = MetricsCollector()
anomaly_detector = AnomalyDetector()


@api_bp.route('/metrics')
def get_metrics():
    """Get current system metrics."""
    metrics = metrics_collector.get_current_metrics()
    return jsonify(metrics)


@api_bp.route('/metrics/history')
def get_metrics_history():
    """Get historical metrics data."""
    history = metrics_collector.get_history()
    return jsonify(history)


@api_bp.route('/anomalies')
def get_anomalies():
    """Get detected anomalies."""
    history = metrics_collector.get_history()
    anomalies = anomaly_detector.detect(history)
    return jsonify(anomalies)


@api_bp.route('/predictions')
def get_predictions():
    """Get resource usage predictions."""
    history = metrics_collector.get_history()
    predictions = {
        'cpu': _predict_trend(history, 'cpu_percent'),
        'memory': _predict_trend(history, 'memory_percent'),
        'disk': _predict_trend(history, 'disk_percent'),
    }
    return jsonify(predictions)


@api_bp.route('/alerts')
def get_alerts():
    """Get active alerts."""
    metrics = metrics_collector.get_current_metrics()
    alerts = []

    cpu_threshold = current_app.config.get('CPU_ALERT_THRESHOLD', 80.0)
    memory_threshold = current_app.config.get('MEMORY_ALERT_THRESHOLD', 85.0)
    disk_threshold = current_app.config.get('DISK_ALERT_THRESHOLD', 90.0)

    if metrics['cpu_percent'] > cpu_threshold:
        alerts.append({
            'type': 'cpu',
            'severity': 'warning' if metrics['cpu_percent'] < 90 else 'critical',
            'message': f"CPU usage is high: {metrics['cpu_percent']:.1f}%",
            'value': metrics['cpu_percent'],
            'threshold': cpu_threshold,
        })

    if metrics['memory_percent'] > memory_threshold:
        alerts.append({
            'type': 'memory',
            'severity': 'warning' if metrics['memory_percent'] < 95 else 'critical',
            'message': f"Memory usage is high: {metrics['memory_percent']:.1f}%",
            'value': metrics['memory_percent'],
            'threshold': memory_threshold,
        })

    if metrics['disk_percent'] > disk_threshold:
        alerts.append({
            'type': 'disk',
            'severity': 'warning' if metrics['disk_percent'] < 95 else 'critical',
            'message': f"Disk usage is high: {metrics['disk_percent']:.1f}%",
            'value': metrics['disk_percent'],
            'threshold': disk_threshold,
        })

    return jsonify({'alerts': alerts, 'count': len(alerts)})


def _predict_trend(history, metric_key):
    """Simple trend prediction based on recent history."""
    if not history or len(history) < 5:
        return {'trend': 'stable', 'prediction': None}

    values = [h.get(metric_key, 0) for h in history[-10:]]
    avg_recent = sum(values[-5:]) / 5
    avg_older = sum(values[:5]) / 5

    diff = avg_recent - avg_older
    if diff > 5:
        trend = 'increasing'
    elif diff < -5:
        trend = 'decreasing'
    else:
        trend = 'stable'

    return {
        'trend': trend,
        'current': avg_recent,
        'predicted': min(100, max(0, avg_recent + diff)),
        'change': diff,
    }
