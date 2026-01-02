from datetime import datetime, timezone
from fastapi import HTTPException

def normalize_timestamp(ts: str) -> str:
    """
    Normaliza timestamps a formato ISO 8601 UTC con sufijo 'Z',
    sin convertir la hora a la zona local.
    """
    try:
        # Aceptar tanto "Z" como "+00:00"
        if ts.endswith("Z"):
            dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(ts)

        # Forzar UTC sin cambiar la hora
        dt = dt.astimezone(timezone.utc)

        # Devolver siempre en formato ISO 8601 con Z
        return dt.replace(tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")

    except Exception:
        raise HTTPException(status_code=400, detail=f"Timestamp inválido: {ts}")


def normalize_timestamps(payload: dict) -> dict:
    """
    Normaliza todos los timestamps relevantes del request.
    """
    payload["request"]["timestamp_utc"] = normalize_timestamp(
        payload["request"]["timestamp_utc"]
    )

    payload["request"]["time_window"]["start_utc"] = normalize_timestamp(
        payload["request"]["time_window"]["start_utc"]
    )

    payload["request"]["time_window"]["end_utc"] = normalize_timestamp(
        payload["request"]["time_window"]["end_utc"]
    )

    return payload