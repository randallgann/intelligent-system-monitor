"""System metrics collection service."""

import time
from collections import deque
from datetime import datetime
from typing import Optional

import psutil


class MetricsCollector:
    """Collects and stores system metrics."""

    _instance: Optional['MetricsCollector'] = None
    _history: deque

    def __new__(cls):
        """Singleton pattern for shared history."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._history = deque(maxlen=100)
        return cls._instance

    def get_current_metrics(self) -> dict:
        """Collect current system metrics."""
        cpu_percent = psutil.cpu_percent(interval=0.1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')

        try:
            net_io = psutil.net_io_counters()
            network = {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv,
            }
        except Exception:
            network = {
                'bytes_sent': 0,
                'bytes_recv': 0,
                'packets_sent': 0,
                'packets_recv': 0,
            }

        metrics = {
            'timestamp': datetime.utcnow().isoformat(),
            'cpu_percent': cpu_percent,
            'cpu_count': psutil.cpu_count(),
            'memory_percent': memory.percent,
            'memory_total': memory.total,
            'memory_available': memory.available,
            'memory_used': memory.used,
            'disk_percent': disk.percent,
            'disk_total': disk.total,
            'disk_used': disk.used,
            'disk_free': disk.free,
            'network': network,
        }

        # Store in history
        self._history.append(metrics)

        return metrics

    def get_history(self) -> list:
        """Get historical metrics data."""
        return list(self._history)

    def get_summary(self) -> dict:
        """Get summary statistics from history."""
        if not self._history:
            return {}

        cpu_values = [m['cpu_percent'] for m in self._history]
        memory_values = [m['memory_percent'] for m in self._history]
        disk_values = [m['disk_percent'] for m in self._history]

        return {
            'cpu': {
                'current': cpu_values[-1] if cpu_values else 0,
                'avg': sum(cpu_values) / len(cpu_values),
                'min': min(cpu_values),
                'max': max(cpu_values),
            },
            'memory': {
                'current': memory_values[-1] if memory_values else 0,
                'avg': sum(memory_values) / len(memory_values),
                'min': min(memory_values),
                'max': max(memory_values),
            },
            'disk': {
                'current': disk_values[-1] if disk_values else 0,
                'avg': sum(disk_values) / len(disk_values),
                'min': min(disk_values),
                'max': max(disk_values),
            },
            'samples': len(self._history),
        }
