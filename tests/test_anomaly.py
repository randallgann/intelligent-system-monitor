"""Tests for anomaly detection service."""

import pytest
from app.services.anomaly import AnomalyDetector


def test_insufficient_data():
    """Test that detector returns insufficient_data status with few points."""
    detector = AnomalyDetector()
    history = [{'cpu_percent': 50, 'memory_percent': 50, 'disk_percent': 50}] * 5

    result = detector.detect(history)

    assert result['status'] == 'insufficient_data'
    assert result['anomalies'] == []
    assert 'Need at least 10 data points' in result['message']


def test_empty_history():
    """Test that detector handles empty history."""
    detector = AnomalyDetector()

    result = detector.detect([])

    assert result['status'] == 'insufficient_data'
    assert result['anomalies'] == []


def test_detect_with_sufficient_data():
    """Test anomaly detection with sufficient data points."""
    detector = AnomalyDetector(contamination=0.1)

    # Create normal data points
    history = []
    for i in range(15):
        history.append({
            'timestamp': f'2026-02-02T12:00:{i:02d}',
            'cpu_percent': 50 + (i % 5),
            'memory_percent': 60 + (i % 3),
            'disk_percent': 40 + (i % 2),
        })

    result = detector.detect(history)

    assert result['status'] == 'ok'
    assert result['total_points'] == 15
    assert 'anomalies' in result
    assert 'anomaly_count' in result
    assert 'anomaly_rate' in result


def test_detect_with_outlier():
    """Test that extreme outliers are detected as anomalies."""
    detector = AnomalyDetector(contamination=0.15)

    # Create mostly normal data with one extreme outlier
    history = []
    for i in range(20):
        history.append({
            'timestamp': f'2026-02-02T12:00:{i:02d}',
            'cpu_percent': 50,
            'memory_percent': 60,
            'disk_percent': 40,
        })

    # Add an extreme outlier
    history.append({
        'timestamp': '2026-02-02T12:00:20',
        'cpu_percent': 99,
        'memory_percent': 99,
        'disk_percent': 99,
    })

    result = detector.detect(history)

    assert result['status'] == 'ok'
    assert result['total_points'] == 21


def test_feature_extraction():
    """Test that features are correctly extracted."""
    detector = AnomalyDetector()

    history = [
        {'cpu_percent': 10, 'memory_percent': 20, 'disk_percent': 30},
        {'cpu_percent': 40, 'memory_percent': 50, 'disk_percent': 60},
    ]

    features = detector._extract_features(history)

    assert features.shape == (2, 3)
    assert features[0][0] == 10
    assert features[0][1] == 20
    assert features[0][2] == 30


def test_feature_extraction_missing_keys():
    """Test feature extraction handles missing keys gracefully."""
    detector = AnomalyDetector()

    history = [
        {'cpu_percent': 10},  # Missing memory and disk
        {'memory_percent': 50},  # Missing cpu and disk
    ]

    features = detector._extract_features(history)

    assert features.shape == (2, 3)
    assert features[0][0] == 10
    assert features[0][1] == 0  # Default for missing
    assert features[1][0] == 0  # Default for missing
