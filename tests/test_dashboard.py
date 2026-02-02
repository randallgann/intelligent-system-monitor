"""Tests for dashboard routes."""

import pytest
from app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_dashboard_index(client):
    """Test GET / returns the dashboard page."""
    response = client.get('/')

    assert response.status_code == 200
    assert b'<!DOCTYPE html>' in response.data
    assert b'Intelligent System Monitor' in response.data


def test_dashboard_contains_charts(client):
    """Test that dashboard contains chart elements."""
    response = client.get('/')

    assert response.status_code == 200
    assert b'chart.js' in response.data.lower()
    assert b'tailwindcss' in response.data.lower()


def test_dashboard_contains_metrics_cards(client):
    """Test that dashboard contains metric cards."""
    response = client.get('/')

    assert response.status_code == 200
    assert b'CPU Usage' in response.data
    assert b'Memory' in response.data


def test_health_endpoint(client):
    """Test GET /health returns healthy status."""
    response = client.get('/health')

    assert response.status_code == 200
    data = response.get_json()

    assert data['status'] == 'healthy'


def test_dashboard_api_endpoints_referenced(client):
    """Test that dashboard references API endpoints."""
    response = client.get('/')

    assert response.status_code == 200
    assert b'/api/metrics' in response.data
    assert b'/api/anomalies' in response.data


def test_dashboard_content_type(client):
    """Test that dashboard returns HTML content type."""
    response = client.get('/')

    assert response.status_code == 200
    assert 'text/html' in response.content_type


def test_health_endpoint_content_type(client):
    """Test that health endpoint returns JSON content type."""
    response = client.get('/health')

    assert response.status_code == 200
    assert 'application/json' in response.content_type
