from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from db.session import get_db
from models.mass_request import MassRequest
from dependencies.dependencies import current_user
from schemas.mass_payload import MassPayload
from services.mass_normalizer import normalize_mass_payload

router = APIRouter(prefix="/mass", tags=["mass"])


# ---------------------------------------------------------
# Create MASS Request (MASS Simple v1.0 — aligned with Enterprise v1.1)
# ---------------------------------------------------------
@router.post("/generate")
def generate_mass_request(
    payload: MassPayload,
    db: Session = Depends(get_db),
    user=Depends(current_user)
):
    """
    MASS Simple endpoint.
    - Valida el payload con MassPayload (tipado, versionado, trazable)
    - Normaliza el payload para persistencia
    - Guarda en DB con audit trail
    - Devuelve un ACK con metadata
    """

    try:
        normalized = normalize_mass_payload(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Normalization error: {str(e)}"
        )

    mass_entry = MassRequest(
        user_id=user.id,
        schema_version=payload.schema_version,
        correlation_id=normalized["correlation_id"],
        idempotency_key=normalized["request"]["idempotency_key"],
        payload_json=normalized,
        created_at=datetime.utcnow()
    )

    db.add(mass_entry)
    db.commit()
    db.refresh(mass_entry)

    return {
        "status": "ACCEPTED",
        "mass_request_id": mass_entry.id,
        "correlation_id": normalized["correlation_id"],
        "idempotency_key": normalized["request"]["idempotency_key"],
        "received_at_utc": mass_entry.created_at.isoformat() + "Z"
    }


# ---------------------------------------------------------
# Retrieve MASS Request
# ---------------------------------------------------------
@router.get("/{mass_id}")
def get_mass_request(
    mass_id: int,
    db: Session = Depends(get_db),
    user=Depends(current_user)
):
    """
    Devuelve un MASS request almacenado.
    """

    entry = db.query(MassRequest).filter(
        MassRequest.id == mass_id,
        MassRequest.user_id == user.id
    ).first()

    if not entry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="MASS request not found"
        )

    return {
        "id": entry.id,
        "schema_version": entry.schema_version,
        "correlation_id": entry.correlation_id,
        "idempotency_key": entry.idempotency_key,
        "payload": entry.payload_json,
        "created_at": entry.created_at.isoformat() + "Z"
    }
