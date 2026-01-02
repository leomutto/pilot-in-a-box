import json
from datetime import datetime
from pathlib import Path

AUDIT_FILE = Path("audit_logs.jsonl")


def audit_log(event: str, payload: dict, tracking_id: str) -> None:
    """
    Registra un evento de auditoría en formato JSONL.
    Cada línea es un registro independiente, ideal para análisis posteriores.
    """

    entry = {
        "timestamp": datetime.utcnow().isoformat(),
        "event": event,
        "tracking_id": tracking_id,
        "payload": payload,
    }

    # Asegurar que el archivo existe
    AUDIT_FILE.touch(exist_ok=True)

    # Escribir entrada
    with AUDIT_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")