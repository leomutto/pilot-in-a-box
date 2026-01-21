from sqlalchemy import Column, Integer, JSON, DateTime, func
from app.db.base import Base


class MassRequest(Base):
    __tablename__ = "mass_requests"

    id = Column(Integer, primary_key=True, index=True)
    payload_json = Column(JSON, nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )