from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    JSON,
    Enum,
    Text
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


# ============================================================
# REQUESTS TABLE
# ============================================================

class RequestModel(Base):
    __tablename__ = "requests"

    id = Column(Integer, primary_key=True, index=True)
    
    # Identificadores del contrato
    request_id = Column(String, index=True, nullable=False)
    idempotency_key = Column(String, index=True, nullable=False)
    correlation_id = Column(String, index=True, nullable=False)
    traceparent = Column(String, nullable=True)

    schema_version = Column(String, nullable=False)

    # JSON original enviado por la UI
    payload_raw = Column(JSONB, nullable=False)

    # JSON normalizado por el backend
    payload_normalized = Column(JSONB, nullable=False)

    # Estado del request dentro del pipeline
    status = Column(String, default="pending", nullable=False)

    # Hash del payload_normalized (sha256)
    hash = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación con responses
    responses = relationship("ResponseModel", back_populates="request", cascade="all, delete-orphan")

    # Relación con logs
    logs = relationship("LogModel", back_populates="request", cascade="all, delete-orphan")


# ============================================================
# RESPONSES TABLE
# ============================================================

class ResponseModel(Base):
    __tablename__ = "responses"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)

    # JSON completo devuelto por la blackbox (success o error)
    response_raw = Column(JSONB, nullable=False)

    # success | error
    response_type = Column(String, nullable=False)

    # Código de estado: OK, DEADLINE_EXCEEDED, etc.
    status_code = Column(String, nullable=False)

    # Versión del modelo de la blackbox (si existe)
    model_version = Column(String, nullable=True)

    latency_ms = Column(Integer, nullable=True)

    received_at = Column(DateTime, default=datetime.utcnow)

    # Relación inversa
    request = relationship("RequestModel", back_populates="responses")


# ============================================================
# LOGS TABLE
# ============================================================

class LogModel(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)

    request_id = Column(Integer, ForeignKey("requests.id"), nullable=False)

    # validated, normalized, saved, sent_to_blackbox, response_received, error, retry, etc.
    event_type = Column(String, nullable=False)

    timestamp = Column(DateTime, default=datetime.utcnow)

    # Metadata adicional del evento
    metadata = Column(JSONB, nullable=True)

    # Relación inversa
    request = relationship("RequestModel", back_populates="logs")