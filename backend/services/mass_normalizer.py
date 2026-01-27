# backend/services/mass_normalizer.py

import uuid
from datetime import datetime
from typing import Dict, Any

from schemas.mass_payload import MassPayload


def _ensure_correlation_id(payload: MassPayload) -> str:
    """
    Garantiza que exista correlation_id.
    Si no viene en el payload, se genera uno.
    """
    return payload.correlation_id or f"corr-{uuid.uuid4()}"


def _ensure_idempotency_key(payload: MassPayload) -> str:
    """
    Garantiza idempotencia.
    Si no viene en el payload, se genera uno.
    """
    return payload.request.idempotency_key or f"idem-{uuid.uuid4()}"


def _normalize_timestamp(dt: datetime) -> str:
    """
    Normaliza timestamps a ISO 8601 UTC.
    """
    return dt.replace(microsecond=0).isoformat() + "Z"


def _normalize_time_window(tw) -> Dict[str, Any]:
    return {
        "start_utc": tw["start"],
        "end_utc": tw["end"],
    }


def normalize_mass_payload(payload: MassPayload) -> Dict[str, Any]:
    """
    Normaliza el payload MASS ENTERPRISE v1.1.
    Alineado con el esquema actual MassPayload.
    """

    correlation_id = _ensure_correlation_id(payload)
    idempotency_key = _ensure_idempotency_key(payload)

    normalized = {
        "schema_version": payload.schema_version,
        "correlation_id": correlation_id,
        "trace": {
            "trace_id": payload.trace.trace_id,
            "span_id": payload.trace.span_id
        },
        "request": {
            "request_id": payload.request.request_id,
            "idempotency_key": idempotency_key,
            "tenant_id": payload.request.tenant_id,
            "environment": payload.request.environment,
            "mode": payload.request.mode,
            "timestamp_utc": payload.request.timestamp_utc,
            "timeout_ms": payload.request.timeout_ms,
            "service_level_objective_ms": payload.request.service_level_objective_ms,
            "time_window": payload.request.time_window,
            "assets": payload.request.assets,
            "data_contract": payload.request.data_contract,
            "signals": payload.request.signals,
            "constraints": payload.request.constraints,
            "preferences": payload.request.preferences,
        },
        "payload": payload.payload,
        "normalized_at_utc": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    }

    return normalized
