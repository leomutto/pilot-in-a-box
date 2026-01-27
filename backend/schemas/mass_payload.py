# backend/schemas/mass_payload.py

from pydantic import BaseModel, Field, conint, confloat
from typing import Optional
from datetime import datetime


class Trace(BaseModel):
    traceparent: str


class TimeWindow(BaseModel):
    start_utc: datetime
    end_utc: datetime
    granularity_seconds: conint(gt=0)


class Assets(BaseModel):
    site_id: str
    region: str
    facility_id: str
    cluster_id: str
    zone_id: str


class QualityFlags(BaseModel):
    missing_allowed: bool = True
    max_missing_ratio: confloat(ge=0, le=1)
    max_staleness_seconds: conint(ge=0)


class DataContract(BaseModel):
    units: str
    currency: str
    source: str
    data_classification: str
    no_pii: bool
    quality_flags: QualityFlags


class EnergySignals(BaseModel):
    it_load_kw: float
    facility_power_kw: float
    ups_efficiency_pct: float
    pue_current: float
    carbon_intensity_gco2_per_kwh: float
    energy_price_usd_per_kwh: float


class ThermalSignals(BaseModel):
    avg_rack_inlet_c: float
    p95_rack_inlet_c: float
    hotspot_rack_count: int
    supply_temp_c: float
    return_temp_c: float


class CoolingSignals(BaseModel):
    cooling_setpoint_c: float
    chiller_kw: float
    fan_power_kw: float
    cooling_valve_position_pct: float


class JobMix(BaseModel):
    batch_pct: float
    latency_sensitive_pct: float


class WorkloadSignals(BaseModel):
    cpu_util_avg: float
    gpu_util_avg: float
    queue_depth: int
    job_mix: JobMix
    tokens_per_watt_est: float


class Signals(BaseModel):
    energy: EnergySignals
    thermal: ThermalSignals
    cooling: CoolingSignals
    workload: WorkloadSignals


class HardConstraints(BaseModel):
    no_control_actions: bool
    max_setpoint_change_c: float
    max_hotspot_rack_count: int
    max_rack_inlet_p95_c: float


class SoftConstraints(BaseModel):
    max_risk_score: float
    prefer_lower_carbon: bool


class Constraints(BaseModel):
    hard: HardConstraints
    soft: SoftConstraints


class ObjectiveWeights(BaseModel):
    energy: float
    thermal_risk: float
    workload_efficiency: float


class Preferences(BaseModel):
    objective_weights: ObjectiveWeights
    recommendation_horizon_minutes: int
    top_k: int


class MassPayload(BaseModel):
    schema_version: str
    correlation_id: Optional[str]
    trace: Trace

    request_id: str = Field(..., alias="request.request_id")
    idempotency_key: str = Field(..., alias="request.idempotency_key")
    tenant_id: str = Field(..., alias="request.tenant_id")
    environment: str = Field(..., alias="request.environment")
    mode: str = Field(..., alias="request.mode")
    timestamp_utc: datetime = Field(..., alias="request.timestamp_utc")
    timeout_ms: int = Field(..., alias="request.timeout_ms")
    service_level_objective_ms: int = Field(..., alias="request.service_level_objective_ms")

    time_window: TimeWindow = Field(..., alias="request.time_window")
    assets: Assets = Field(..., alias="request.assets")
    data_contract: DataContract = Field(..., alias="request.data_contract")
    signals: Signals = Field(..., alias="request.signals")
    constraints: Constraints = Field(..., alias="request.constraints")
    preferences: Preferences = Field(..., alias="request.preferences")

    class Config:
        populate_by_name = True
