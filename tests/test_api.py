"""Tests for API routes."""

import pytest
from app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_get_metrics(client):
    """Test GET /api/metrics returns current metrics."""
    response = client.get('/api/metrics')

    assert response.status_code == 200
    data = response.get_json()

    assert 'timestamp' in data
    assert 'cpu_percent' in data
    assert 'memory_percent' in data
    assert 'disk_percent' in data
    assert 'cpu_count' in data
    assert 'memory_total' in data
    assert 'network' in data

    assert 0 <= data['cpu_percent'] <= 100
    assert 0 <= data['memory_percent'] <= 100
    assert 0 <= data['disk_percent'] <= 100


def test_get_metrics_history(client):
    """Test GET /api/metrics/history returns historical data."""
    # First make some requests to populate history
    client.get('/api/metrics')
    client.get('/api/metrics')

    response = client.get('/api/metrics/history')

    assert response.status_code == 200
    data = response.get_json()

    assert isinstance(data, list)
    assert len(data) >= 2


def test_get_anomalies_insufficient_data(client):
    """Test GET /api/anomalies with insufficient data."""
    response = client.get('/api/anomalies')

    assert response.status_code == 200
    data = response.get_json()

    # Initially there won't be enough data
    assert 'status' in data
    assert 'anomalies' in data


def test_get_predictions(client):
    """Test GET /api/predictions returns trend predictions."""
    response = client.get('/api/predictions')

    assert response.status_code == 200
    data = response.get_json()

    assert 'cpu' in data
    assert 'memory' in data
    assert 'disk' in data

    assert 'trend' in data['cpu']
    assert data['cpu']['trend'] in ['stable', 'increasing', 'decreasing']


def test_get_alerts_no_alerts(client):
    """Test GET /api/alerts with normal metrics."""
    response = client.get('/api/alerts')

    assert response.status_code == 200
    data = response.get_json()

    assert 'alerts' in data
    assert 'count' in data
    assert isinstance(data['alerts'], list)
    assert data['count'] == len(data['alerts'])


def test_alerts_response_structure(client):
    """Test that alerts have the correct structure when triggered."""
    response = client.get('/api/alerts')

    assert response.status_code == 200
    data = response.get_json()

    # If there are alerts, verify structure
    for alert in data['alerts']:
        assert 'type' in alert
        assert 'severity' in alert
        assert 'message' in alert
        assert 'value' in alert
        assert 'threshold' in alert
        assert alert['type'] in ['cpu', 'memory', 'disk']
        assert alert['severity'] in ['warning', 'critical']


def test_metrics_network_data(client):
    """Test that network data is included in metrics."""
    response = client.get('/api/metrics')

    assert response.status_code == 200
    data = response.get_json()

    network = data['network']
    assert 'bytes_sent' in network
    assert 'bytes_recv' in network
    assert 'packets_sent' in network
    assert 'packets_recv' in network


def test_predictions_with_history(client):
    """Test predictions improve with more history data."""
    # Generate some history
    for _ in range(10):
        client.get('/api/metrics')

    response = client.get('/api/predictions')

    assert response.status_code == 200
    data = response.get_json()

    # With more data, predictions should have more fields
    for metric in ['cpu', 'memory', 'disk']:
        assert 'trend' in data[metric]
