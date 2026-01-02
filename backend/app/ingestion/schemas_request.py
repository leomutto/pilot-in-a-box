from pydantic import BaseModel, Field
from typing import Dict


# ============================================================
# TRACE
# ============================================================

class Trace(BaseModel):
    traceparent: str


# ============================================================
# TIME WINDOW
# ============================================================

class TimeWindow(BaseModel):
    start_utc: str
    end_utc: str


# ============================================================
# DATA CONTRACT
# ============================================================

class DataContract(BaseModel):
    units: str  # MASS v1.1 → always "metric"


# ============================================================
# SIGNALS — ENERGY
# ============================================================

class EnergySignals(BaseModel):
    it_load_kw: float
    facility_power_kw: float
    energy_price_usd_per_kwh: float


# ============================================================
# SIGNALS — THERMAL
# ============================================================

class ThermalSignals(BaseModel):
    pue_current: float
    pue_target: float
    cooling_cop: float


# ============================================================
# SIGNALS — COOLING
# ============================================================

class CoolingSignals(BaseModel):
    chilled_water_temp_c: float
    cooling_setpoint_c: float


# ============================================================
# SIGNALS — WORKLOAD
# ============================================================

class JobMix(BaseModel):
    llm_pct: float
    vision_pct: float
    other_pct: float


class WorkloadSignals(BaseModel):
    active_users: int
    tokens_per_watt_est: float
    job_mix: JobMix


# ============================================================
# SIGNALS ROOT
# ============================================================

class Signals(BaseModel):
    energy: EnergySignals
    thermal: ThermalSignals
    cooling: CoolingSignals
    workload: WorkloadSignals


# ============================================================
# REQUEST ROOT
# ============================================================

class RequestPayload(BaseModel):
    request_id: str
    idempotency_key: str
    tenant_id: str
    environment: str
    mode: str
    timestamp_utc: str
    time_window: TimeWindow
    service_level_objective_ms: int
    data_contract: DataContract
    signals: Signals


# ============================================================
# TOP-LEVEL JSON REQUEST
# ============================================================

class JSONRequest(BaseModel):
    schema_version: str
    correlation_id: str
    trace: Trace
    request: RequestPayload