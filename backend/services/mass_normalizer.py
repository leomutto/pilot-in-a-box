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
    return payload.idempotency_key or f"idem-{uuid.uuid4()}"


def _normalize_timestamp(dt: datetime) -> str:
    """
    Normaliza timestamps a ISO 8601 UTC.
    """
    return dt.replace(microsecond=0).isoformat() + "Z"


def _normalize_time_window(tw) -> Dict[str, Any]:
    return {
        "start_utc": _normalize_timestamp(tw.start_utc),
        "end_utc": _normalize_timestamp(tw.end_utc),
        "granularity_seconds": tw.granularity_seconds,
    }


def normalize_mass_payload(payload: MassPayload) -> Dict[str, Any]:
    """
    Normaliza el payload MASS para persistencia y trazabilidad.
    Compatible con MASS ENTERPRISE v1.1.
    """
    correlation_id = _ensure_correlation_id(payload)
    idempotency_key = _ensure_idempotency_key(payload)

    normalized = {
        "schema_version": payload.schema_version,
        "correlation_id": correlation_id,
        "trace": {
            "traceparent": payload.trace.traceparent
        },
        "request": {
            "request_id": payload.request_id,
            "idempotency_key": idempotency_key,
            "tenant_id": payload.tenant_id,
            "environment": payload.environment,
            "mode": payload.mode,
            "timestamp_utc": _normalize_timestamp(payload.timestamp_utc),
            "timeout_ms": payload.timeout_ms,
            "service_level_objective_ms": payload.service_level_objective_ms,
            "time_window": _normalize_time_window(payload.time_window),
            "assets": payload.assets.model_dump(),
            "data_contract": payload.data_contract.model_dump(),
            "signals": payload.signals.model_dump(),
            "constraints": payload.constraints.model_dump(),
            "preferences": payload.preferences.model_dump(),
        },
        "normalized_at_utc": datetime.utcnow().replace(microsecond=0).isoformat() + "Z",
    }

    return normalized
