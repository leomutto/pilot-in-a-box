from datetime import datetime
from fastapi import HTTPException


def normalize_timestamp(ts: str) -> str:
    """
    Normaliza timestamps a formato ISO 8601 UTC.
    """
    try:
        dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
        return dt.astimezone().isoformat()
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