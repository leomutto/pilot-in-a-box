# backend/models/mass_request.py

from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from db.base import Base


class MassRequest(Base):
    __tablename__ = "mass_requests"

    id = Column(Integer, primary_key=True, index=True)

    # Trazabilidad
    schema_version = Column(String, nullable=False)
    correlation_id = Column(String, index=True, nullable=False)
    idempotency_key = Column(String, index=True, nullable=False)

    # Usuario que envió el request
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")

    # Payload normalizado MASS
    payload_json = Column(JSON, nullable=False)

    # Auditoría
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)