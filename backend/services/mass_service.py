from sqlalchemy.orm import Session

from backend.models.mass import MassRequest
from backend.core.validators.mass_validator import MassValidator
from backend.schemas.mass import (
    MassPayload,
    MassValidationResponse,
    MassSaveResponse,
    MassSendResponse,
    MassLogEntry
)


class MassService:

    # ---------------------------------------------------------
    # VALIDATE
    # ---------------------------------------------------------
    @staticmethod
    def validate(payload: dict) -> MassValidationResponse:
        valid, message = MassValidator.validate(payload)
        return MassValidationResponse(valid=valid, message=message)

    # ---------------------------------------------------------
    # SAVE
    # ---------------------------------------------------------
    @staticmethod
    def save(db: Session, payload: dict) -> MassSaveResponse:
        """
        Guarda el MASS simple en la base de datos.
        """
        mass = MassRequest(payload_json=payload)
        db.add(mass)
        db.commit()
        db.refresh(mass)

        return MassSaveResponse(id=mass.id)

    # ---------------------------------------------------------
    # SEND (simulado)
    # ---------------------------------------------------------
    @staticmethod
    def send(db: Session, mass_id: int) -> MassSendResponse:
        """
        Simula el envío del MASS a la blackbox.
        En el futuro se reemplaza por integración real.
        """
        mass = db.query(MassRequest).filter(MassRequest.id == mass_id).first()

        if not mass:
            return MassSendResponse(
                id=mass_id,
                delivered=False,
                message="MASS no encontrado"
            )

        # Simulación de envío exitoso
        return MassSendResponse(
            id=mass_id,
            delivered=True
        )

    # ---------------------------------------------------------
    # LOGS
    # ---------------------------------------------------------
    @staticmethod
    def get_logs(db: Session, mass_id: int) -> MassLogEntry | None:
        mass = db.query(MassRequest).filter(MassRequest.id == mass_id).first()

        if not mass:
            return None

        return MassLogEntry(
            id=mass.id,
            payload=mass.payload_json,
            created_at=str(mass.created_at),
            updated_at=str(mass.updated_at)
        )