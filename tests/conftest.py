"""Pytest configuration and fixtures."""

import pytest
from app import create_app
from app.services.metrics import MetricsCollector


@pytest.fixture
def app():
    """Create application for testing."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(autouse=True)
def reset_metrics_singleton():
    """Reset the MetricsCollector singleton between tests."""
    # Clear the history before each test
    collector = MetricsCollector()
    collector._history.clear()
    yield
    # Clean up after test
    collector._history.clear()
