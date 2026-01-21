from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.db.session import get_db
from backend.services.mass_service import MassService
from backend.schemas.mass import (
    MassPayload,
    MassValidationResponse,
    MassSaveResponse,
    MassSendResponse,
    MassLogEntry
)

router = APIRouter(prefix="/mass", tags=["MASS"])


@router.post("/validate", response_model=MassValidationResponse)
def validate_mass(payload: MassPayload):
    result = MassService.validate(payload.dict())
    return result


@router.post("/save", response_model=MassSaveResponse)
def save_mass(payload: MassPayload, db: Session = Depends(get_db)):
    result = MassService.save(db, payload.dict())
    return result


@router.post("/send", response_model=MassSendResponse)
def send_mass(id: int, db: Session = Depends(get_db)):
    result = MassService.send(db, id)
    return result


@router.get("/{mass_id}/logs", response_model=MassLogEntry)
def get_mass_logs(mass_id: int, db: Session = Depends(get_db)):
    result = MassService.get_logs(db, mass_id)

    if not result:
        raise HTTPException(status_code=404, detail="MASS no encontrado")

    return result