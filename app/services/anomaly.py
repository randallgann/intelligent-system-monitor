"""Anomaly detection service using ML."""

import numpy as np
from sklearn.ensemble import IsolationForest
from typing import Optional


class AnomalyDetector:
    """Detects anomalies in system metrics using Isolation Forest."""

    def __init__(self, contamination: float = 0.1):
        """Initialize the anomaly detector.

        Args:
            contamination: Expected proportion of anomalies in the data.
        """
        self.contamination = contamination
        self.model: Optional[IsolationForest] = None

    def detect(self, history: list) -> dict:
        """Detect anomalies in metrics history.

        Args:
            history: List of metrics dictionaries.

        Returns:
            Dictionary containing anomaly detection results.
        """
        if not history or len(history) < 10:
            return {
                'anomalies': [],
                'status': 'insufficient_data',
                'message': 'Need at least 10 data points for anomaly detection',
            }

        # Extract features for anomaly detection
        features = self._extract_features(history)

        # Train model on the data
        self.model = IsolationForest(
            contamination=self.contamination,
            random_state=42,
            n_estimators=100,
        )

        # Predict anomalies (-1 for anomaly, 1 for normal)
        predictions = self.model.fit_predict(features)
        scores = self.model.decision_function(features)

        # Find anomalous points
        anomalies = []
        for i, (pred, score) in enumerate(zip(predictions, scores)):
            if pred == -1:
                anomalies.append({
                    'index': i,
                    'timestamp': history[i].get('timestamp'),
                    'score': float(score),
                    'metrics': {
                        'cpu_percent': history[i].get('cpu_percent'),
                        'memory_percent': history[i].get('memory_percent'),
                        'disk_percent': history[i].get('disk_percent'),
                    },
                })

        return {
            'anomalies': anomalies,
            'status': 'ok',
            'total_points': len(history),
            'anomaly_count': len(anomalies),
            'anomaly_rate': len(anomalies) / len(history) if history else 0,
        }

    def _extract_features(self, history: list) -> np.ndarray:
        """Extract feature matrix from metrics history."""
        features = []
        for metrics in history:
            features.append([
                metrics.get('cpu_percent', 0),
                metrics.get('memory_percent', 0),
                metrics.get('disk_percent', 0),
            ])
        return np.array(features)
