import requests
from fastapi import HTTPException

from .retry import retry_operation, RetryConfig
from .telemetry import Telemetry


class BlackboxClient:
    def __init__(self, base_url: str, timeout_seconds: int = 5):
        self.base_url = base_url
        self.timeout = timeout_seconds
        self.telemetry = Telemetry()

    def _post(self, endpoint: str, payload: dict):
        """
        Envia un POST a la blackbox con timeout y manejo de errores.
        """

        url = f"{self.base_url}{endpoint}"

        def operation():
            response = requests.post(url, json=payload, timeout=self.timeout)

            if response.status_code >= 500:
                raise Exception("Blackbox error 5xx")

            if response.status_code >= 400:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=response.json()
                )

            return response.json()

        retry_cfg = RetryConfig(retries=3, base_delay=0.5, max_delay=3.0)

        # Medir latencia
        wrapped = self.telemetry.measure_latency(
            lambda: retry_operation(operation, retry_cfg)
        )

        return wrapped()

    def send_request(self, payload: dict):
        """
        Envía el JSON_request normalizado a la blackbox.
        """
        self.telemetry.record("send_attempt", {"payload_hash": payload.get("hash")})
        return self._post("/recommend", payload)