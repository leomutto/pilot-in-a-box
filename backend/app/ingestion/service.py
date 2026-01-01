from sqlalchemy.orm import Session
from fastapi import HTTPException

from .schemas_request import JSONRequest
from .storage.models import RequestModel, ResponseModel, LogModel

# VALIDATORS
from .validators.structural import validate_structural
from .validators.semantic import validate_semantic
from .validators.business import validate_business
from .validators.contract import validate_contract

# NORMALIZERS
from .normalizers.timestamps import normalize_timestamps
from .normalizers.numbers import normalize_numbers
from .normalizers.strings import normalize_strings
from .normalizers.snake_case import normalize_keys_snake_case
from .normalizers.units import normalize_units

# BLACKBOX CLIENT
from .blackbox.client import BlackboxClient

from datetime import datetime
import hashlib
import json


# ============================================================
# HELPERS
# ============================================================

def compute_hash(payload: dict) -> str:
    """Compute SHA256 hash of normalized payload."""
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def log_event(db: Session, request_id: int, event_type: str, metadata: dict = None):
    log = LogModel(
        request_id=request_id,
        event_type=event_type,
        metadata=metadata or {}
    )
    db.add(log)
    db.commit()


# ============================================================
# VALIDATE PIPELINE
# ============================================================

def validate_request_payload(json_request: JSONRequest):
    """
    Ejecuta todos los validadores del pipeline.
    """

    payload = json_request.dict()

    # 1. Validación estructural (Pydantic + wrapper)
    structural = validate_structural(json_request)

    # 2. Validación semántica
    semantic = validate_semantic(payload)

    # 3. Validación de negocio
    business = validate_business(payload)

    # 4. Validación de contrato
    contract = validate_contract(payload)

    return {
        "status": "valid",
        "details": {
            "structural": structural,
            "semantic": semantic,
            "business": business,
            "contract": contract
        }
    }


# ============================================================
# NORMALIZE PIPELINE
# ============================================================

def normalize_request_payload(json_request: JSONRequest):
    """
    Ejecuta todos los normalizadores del pipeline.
    """

    payload = json_request.dict()

    # 1. Normalizar timestamps
    payload = normalize_timestamps(payload)

    # 2. Normalizar números
    payload = normalize_numbers(payload)

    # 3. Normalizar strings
    payload = normalize_strings(payload)

    # 4. Normalizar claves a snake_case
    payload = normalize_keys_snake_case(payload)

    # 5. Normalizar unidades
    payload = normalize_units(payload)

    return payload


# ============================================================
# SAVE
# ============================================================

def save_request_payload(json_request: JSONRequest, db: Session):
    normalized = normalize_request_payload(json_request)

    payload_hash = compute_hash(normalized)

    request_entry = RequestModel(
        request_id=json_request.request.request_id,
        idempotency_key=json_request.request.idempotency_key,
        correlation_id=json_request.correlation_id,
        traceparent=json_request.trace.traceparent,
        schema_version=json_request.schema_version,
        payload_raw=json_request.dict(),
        payload_normalized=normalized,
        hash=payload_hash,
        status="saved"
    )

    db.add(request_entry)
    db.commit()
    db.refresh(request_entry)

    log_event(db, request_entry.id, "saved")

    return {"request_db_id": request_entry.id, "status": "saved"}


# ============================================================
# SEND TO BLACKBOX (REAL CLIENT)
# ============================================================

def send_request_to_blackbox(request_id: int, db: Session):
    request_entry = db.query(RequestModel).filter(RequestModel.id == request_id).first()

    if not request_entry:
        raise HTTPException(status_code=404, detail="Request not found")

    client = BlackboxClient(base_url="http://blackbox:8000")

    try:
        response_json = client.send_request(request_entry.payload_normalized)
    except Exception as e:
        log_event(db, request_id, "blackbox_error", {"error": str(e)})
        raise HTTPException(status_code=500, detail="Error comunicando con la blackbox")

    response_entry = ResponseModel(
        request_id=request_id,
        response_raw=response_json,
        response_type="success",
        status_code="OK",
        model_version=response_json.get("model", {}).get("version", "unknown"),
        latency_ms=client.telemetry.events[-1]["metadata"].get("ms", 0)
    )

    db.add(response_entry)
    db.commit()

    log_event(db, request_id, "sent_to_blackbox")

    return {"status": "sent", "response_id": response_entry.id}


# ============================================================
# GET REQUEST + RESPONSE
# ============================================================

def get_request_with_response(request_id: int, db: Session):
    request_entry = db.query(RequestModel).filter(RequestModel.id == request_id).first()

    if not request_entry:
        raise HTTPException(status_code=404, detail="Request not found")

    responses = db.query(ResponseModel).filter(ResponseModel.request_id == request_id).all()

    return {
        "request": request_entry.payload_raw,
        "responses": [r.response_raw for r in responses]
    }


# ============================================================
# GET LOGS
# ============================================================

def get_request_logs(request_id: int, db: Session):
    logs = db.query(LogModel).filter(LogModel.request_id == request_id).all()

    return [{"event": l.event_type, "timestamp": l.timestamp, "metadata": l.metadata} for l in logs]