import uuid
from datetime import datetime


def _timestamp() -> str:
    """
    Devuelve un timestamp UTC compacto para trazabilidad.
    Formato: YYYYMMDDTHHMMSSZ
    """
    return datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")


def generate_trace_id() -> str:
    """
    Genera un trace_id único siguiendo un formato legible y ordenable.

    Formato:
        trace-20250101T153045Z-8f3c2a1b

    Componentes:
        - Prefijo 'trace'
        - Timestamp UTC compacto
        - UUID reducido (8 caracteres)
    """
    return f"trace-{_timestamp()}-{uuid.uuid4().hex[:8]}"


def generate_span_id() -> str:
    """
    Genera un span_id corto para sub-operaciones dentro de un trace.
    """
    return uuid.uuid4().hex[:8]


def start_span(trace_id: str, name: str) -> dict:
    """
    Crea un span estructurado para representar una operación interna.

    Devuelve un diccionario con:
        - trace_id
        - span_id
        - name
        - start_timestamp
    """
    return {
        "trace_id": trace_id,
        "span_id": generate_span_id(),
        "name": name,
        "start_timestamp": _timestamp(),
    }


def end_span(span: dict) -> dict:
    """
    Completa un span agregando el timestamp de finalización.
    """
    span["end_timestamp"] = _timestamp()
    return span


def trace_event(trace_id: str, event: str, payload: dict | None = None) -> dict:
    """
    Registra un evento dentro de un trace.

    Devuelve un diccionario estructurado que puede enviarse a logs,
    auditoría o sistemas de observabilidad.
    """
    return {
        "trace_id": trace_id,
        "event": event,
        "timestamp": _timestamp(),
        "payload": payload or {},
    }