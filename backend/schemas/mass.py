from pydantic import BaseModel, Field
from typing import Optional


# ---------------------------------------------------------
# MASS SIMPLE PAYLOAD (Contrato del cliente)
# ---------------------------------------------------------

class Device(BaseModel):
    id: str
    type: str
    location: str


class Metrics(BaseModel):
    temperature_celsius: float
    humidity_percent: float
    pressure_hpa: float


class Metadata(BaseModel):
    operator: str
    batch_id: str
    notes: Optional[str] = None


class MassPayload(BaseModel):
    mass_version: str = Field(..., example="1.1")
    timestamp: str
    device: Device
    metrics: Metrics
    metadata: Metadata


# ---------------------------------------------------------
# RESPUESTAS DEL PIPELINE MASS
# ---------------------------------------------------------

class MassValidationResponse(BaseModel):
    valid: bool
    message: str


class MassSaveResponse(BaseModel):
    id: int
    message: str = "MASS saved successfully"


class MassSendResponse(BaseModel):
    id: int
    delivered: bool
    message: str = "MASS sent successfully"


class MassLogEntry(BaseModel):
    id: int
    payload: dict
    created_at: str
    updated_at: str