import time


class Telemetry:
    def __init__(self):
        self.events = []

    def record(self, event_type: str, metadata: dict = None):
        self.events.append({
            "event": event_type,
            "metadata": metadata or {},
            "timestamp": time.time()
        })

    def measure_latency(self, func):
        """
        Decorador para medir latencia de una operación.
        """
        def wrapper(*args, **kwargs):
            start = time.time()
            result = func(*args, **kwargs)
            end = time.time()
            self.record("latency", {"ms": int((end - start) * 1000)})
            return result
        return wrapper