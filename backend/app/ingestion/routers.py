from fastapi import APIRouter, HTTPException
from sqlalchemy.orm import Session

from .schemas_request import JSONRequest
from .schemas_response import JSONResponse, JSONErrorResponse
from .service import (
    validate_request_payload,
    normalize_request_payload,
    save_request_payload,
    send_request_to_blackbox,
    get_request_with_response,
    get_request_logs
)

from ..database import get_db  # Ajustar según tu proyecto


router = APIRouter(prefix="/v1/json-request", tags=["json-request"])


# ============================================================
# VALIDATE
# ============================================================

@router.post("/validate")
def validate(json_request: JSONRequest):
    return validate_request_payload(json_request)


# ============================================================
# NORMALIZE
# ============================================================

@router.post("/normalize")
def normalize(json_request: JSONRequest):
    return normalize_request_payload(json_request)


# ============================================================
# SAVE
# ============================================================

@router.post("/save")
def save(json_request: JSONRequest, db: Session = get_db()):
    return save_request_payload(json_request, db)


# ============================================================
# SEND TO BLACKBOX
# ============================================================

@router.post("/{request_id}/send")
def send(request_id: int, db: Session = get_db()):
    return send_request_to_blackbox(request_id, db)


# ============================================================
# GET REQUEST + RESPONSE
# ============================================================

@router.get("/{request_id}")
def get_request(request_id: int, db: Session = get_db()):
    return get_request_with_response(request_id, db)


# ============================================================
# GET LOGS
# ============================================================

@router.get("/{request_id}/logs")
def get_logs(request_id: int, db: Session = get_db()):
    return get_request_logs(request_id, db)