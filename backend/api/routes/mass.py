from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from db.session import get_db
from models.mass_request import MassRequest
from dependencies.dependencies import current_user

# Esquemas
from schemas.mass_simple import MassSimplePayload
from schemas.mass_payload import MassPayload

# Normalizadores
from services.mass_normalizer_simple import normalize_mass_payload_simple
from services.mass_normalizer import normalize_mass_payload

router = APIRouter(prefix="/mass", tags=["mass"])


# ---------------------------------------------------------
# MASS SIMPLE — POST /mass
# ---------------------------------------------------------
@router.post("")
def create_mass_simple_request(
    payload: MassSimplePayload,
    db: Session = Depends(get_db),
    user=Depends(current_user)
):
    """
    MASS Simple endpoint.
    - Recibe solo { "payload": {...} }
    - Normaliza el payload simple
    - Genera automáticamente los campos Enterprise faltantes
    - Guarda en la misma tabla MassRequest
    """

    try:
        normalized = normalize_mass_payload_simple(payload.payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Normalization error: {str(e)}"
        )

    # Campos Enterprise generados automáticamente
    correlation_id = f"corr-{datetime.utcnow().timestamp()}"
    idempotency_key = f"idemp-{user.id}-{datetime.utcnow().timestamp()}"

    mass_entry = MassRequest(
        user_id=user.id,
        schema_version="1.0-simple",
        correlation_id=correlation_id,
        idempotency_key=idempotency_key,
        payload_json=normalized,
        created_at=datetime.utcnow()
    )

    db.add(mass_entry)
    db.commit()
    db.refresh(mass_entry)

    return {
        "status": "ACCEPTED",
        "mass_request_id": mass_entry.id,
        "correlation_id": correlation_id,
        "idempotency_key": idempotency_key,
        "payload_normalized": normalized,
        "received_at_utc": mass_entry.created_at.isoformat() + "Z"
    }


# ---------------------------------------------------------
# MASS ENTERPRISE — POST /mass/generate
# ---------------------------------------------------------
@router.post("/generate")
def generate_mass_request(
    payload: MassPayload,
    db: Session = Depends(get_db),
    user=Depends(current_user)
):
    """
    MASS Enterprise endpoint.
    - Requiere el contrato completo Enterprise
    - Normaliza el payload Enterprise
    - Guarda con audit trail completo
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
# GET /mass/{mass_id}
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
