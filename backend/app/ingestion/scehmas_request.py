from typing import Optional, List
from pydantic import BaseModel, Field


# ============================================================
# TRACE INFORMATION
# ============================================================

class Trace(BaseModel):
    traceparent: str = Field(..., description="W3C traceparent header for distributed tracing")


# ============================================================
# TIME WINDOW
# ============================================================

class TimeWindow(BaseModel):
    start_utc: str
    end_utc: str
    granularity_seconds: int


# ============================================================
# ASSETS
# ============================================================

class Assets(BaseModel):
    site_id: str
    region: str
    facility_id: str
    cluster_id: str
    zone_id: str


# ============================================================
# QUALITY FLAGS
# ============================================================

class QualityFlags(BaseModel):
    missing_allowed: bool
    max_missing_ratio: float
    max_staleness_seconds: int


# ============================================================
# DATA CONTRACT
# ============================================================

class DataContract(BaseModel):
    units: str
    currency: str
    source: str
    data_classification: str
    no_pii: bool
    quality_flags: QualityFlags


# ============================================================
# SIGNALS — ENERGY
# ============================================================

class EnergySignals(BaseModel):
    it_load_kw: float
    facility_power_kw: float
    ups_efficiency_pct: float
    pue_current: float
    carbon_intensity_gco2_per_kwh: float
    energy_price_usd_per_kwh: float


# ============================================================
# SIGNALS — THERMAL
# ============================================================

class ThermalSignals(BaseModel):
    avg_rack_inlet_c: float
    p95_rack_inlet_c: float
    hotspot_rack_count: int
    supply_temp_c: float
    return_temp_c: float


# ============================================================
# SIGNALS — COOLING
# ============================================================

class CoolingSignals(BaseModel):
    cooling_setpoint_c: float
    chiller_kw: float
    fan_power_kw: float
    cooling_valve_position_pct: float


# ============================================================
# SIGNALS — WORKLOAD
# ============================================================

class JobMix(BaseModel):
    batch_pct: float
    latency_sensitive_pct: float


class WorkloadSignals(BaseModel):
    cpu_util_avg: float
    gpu_util_avg: float
    queue_depth: int
    job_mix: JobMix
    tokens_per_watt_est: float


# ============================================================
# SIGNALS ROOT
# ============================================================

class Signals(BaseModel):
    energy: EnergySignals
    thermal: ThermalSignals
    cooling: CoolingSignals
    workload: WorkloadSignals


# ============================================================
# CONSTRAINTS — HARD
# ============================================================

class HardConstraints(BaseModel):
    no_control_actions: bool
    max_setpoint_change_c: float
    max_hotspot_rack_count: int
    max_rack_inlet_p95_c: float


# ============================================================
# CONSTRAINTS — SOFT
# ============================================================

class SoftConstraints(BaseModel):
    max_risk_score: float
    prefer_lower_carbon: bool


# ============================================================
# CONSTRAINTS ROOT
# ============================================================

class Constraints(BaseModel):
    hard: HardConstraints
    soft: SoftConstraints


# ============================================================
# PREFERENCES
# ============================================================

class ObjectiveWeights(BaseModel):
    energy: float
    thermal_risk: float
    workload_efficiency: float


class Preferences(BaseModel):
    objective_weights: ObjectiveWeights
    recommendation_horizon_minutes: int
    top_k: int


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
    timeout_ms: int
    service_level_objective_ms: int
    time_window: TimeWindow
    assets: Assets
    data_contract: DataContract
    signals: Signals
    constraints: Constraints
    preferences: Preferences


# ============================================================
# TOP-LEVEL JSON REQUEST
# ============================================================

class JSONRequest(BaseModel):
    schema_version: str
    correlation_id: str
    trace: Trace
    request: RequestPayload