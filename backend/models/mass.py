from sqlalchemy import Column, Integer, JSON, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class MassRequest(Base):
    __tablename__ = "mass_requests"

    id = Column(Integer, primary_key=True, index=True)

    # Asociación con usuario (clave para seguridad y escalabilidad)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User")

    # Payload flexible (ideal para MASS Simple y MASS Enterprise)
    payload_json = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )