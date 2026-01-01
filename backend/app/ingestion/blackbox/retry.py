import time
import random


class RetryConfig:
    def __init__(self, retries=3, base_delay=0.5, max_delay=5.0, jitter=True):
        self.retries = retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.jitter = jitter


def exponential_backoff(attempt, config: RetryConfig):
    delay = min(config.base_delay * (2 ** attempt), config.max_delay)
    if config.jitter:
        delay = delay * random.uniform(0.8, 1.2)
    return delay


def retry_operation(operation, config: RetryConfig):
    """
    Ejecuta una operación con reintentos y backoff exponencial.
    """
    for attempt in range(config.retries):
        try:
            return operation()
        except Exception as e:
            if attempt == config.retries - 1:
                raise e
            time.sleep(exponential_backoff(attempt, config))