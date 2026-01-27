from pydantic import BaseModel
from typing import Any, Dict, Optional

class Trace(BaseModel):
    trace_id: str
    span_id: str

class RequestMetadata(BaseModel):
    request_id: str
    idempotency_key: str
    tenant_id: str
    environment: str
    mode: str
    timestamp_utc: str
    timeout_ms: int
    service_level_objective_ms: int
    time_window: Dict[str, Any]
    assets: Dict[str, Any]
    data_contract: Dict[str, Any]
    signals: Dict[str, Any]
    constraints: Dict[str, Any]
    preferences: Dict[str, Any]

class MassPayload(BaseModel):
    schema_version: str
    correlation_id: str
    trace: Trace
    request: RequestMetadata
    payload: Dict[str, Any]
