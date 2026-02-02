"""Tests for metrics service."""

import pytest
from app.services.metrics import MetricsCollector


def test_get_current_metrics():
    """Test that current metrics are collected."""
    collector = MetricsCollector()
    metrics = collector.get_current_metrics()

    assert 'timestamp' in metrics
    assert 'cpu_percent' in metrics
    assert 'memory_percent' in metrics
    assert 'disk_percent' in metrics
    assert 0 <= metrics['cpu_percent'] <= 100
    assert 0 <= metrics['memory_percent'] <= 100
    assert 0 <= metrics['disk_percent'] <= 100


def test_metrics_history():
    """Test that metrics are stored in history."""
    collector = MetricsCollector()

    # Collect some metrics
    for _ in range(5):
        collector.get_current_metrics()

    history = collector.get_history()
    assert len(history) >= 5
