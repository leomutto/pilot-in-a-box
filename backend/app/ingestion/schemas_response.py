from typing import List, Optional
from pydantic import BaseModel, Field


# ============================================================
# TRACE INFORMATION
# ============================================================

class Trace(BaseModel):
    traceparent: str = Field(..., description="W3C traceparent header for distributed tracing")


# ============================================================
# MODEL INFORMATION
# ============================================================

class ModelInfo(BaseModel):
    name: str
    version: str
    policy_id: str


# ============================================================
# STATUS INFORMATION
# ============================================================

class ValidationStatus(BaseModel):
    schema_valid: bool
    missing_ratio: float
    staleness_seconds: int


class ResponseStatus(BaseModel):
    code: str
    warnings: Optional[List[str]] = []
    validation: Optional[ValidationStatus] = None
    message: Optional[str] = None
    retryable: Optional[bool] = None


# ============================================================
# SUMMARY INFORMATION
# ============================================================

class EstimatedImpact24h(BaseModel):
    energy_kwh: float
    energy_cost_usd: float
    pue_delta: float
    co2e_kg: float


class Guardrails(BaseModel):
    shadow_read_only_enforced: bool
    constraints_satisfied: bool


class Summary(BaseModel):
    confidence: float
    risk_score: float
    estimated_impact_24h: EstimatedImpact24h
    guardrails: Guardrails


# ============================================================
# RECOMMENDATION ACTION
# ============================================================

class RecommendationAction(BaseModel):
    type: str
    target: str
    current: float
    suggested: float
    delta: float
    units: str


# ============================================================
# EXPECTED IMPACT
# ============================================================

class ExpectedImpact(BaseModel):
    facility_power_kw_delta: float
    pue_delta: float
    co2e_kg_per_day_delta: float


# ============================================================
# EXPLAINABILITY
# ============================================================

class Explainability(BaseModel):
    narrative: str
    reason_codes: List[str]
    organism_tags: List[str]


# ============================================================
# RECOMMENDATION TRACE
# ============================================================

class RecommendationTrace(BaseModel):
    input_fingerprint: str
    feature_set_version: str
    decision_id: str
    generated_at_utc: str


# ============================================================
# RECOMMENDATION ITEM
# ============================================================

class RecommendationItem(BaseModel):
    rec_id: str
    priority: int
    category: str
    action: RecommendationAction
    expected_impact: ExpectedImpact
    explainability: Explainability
    trace: RecommendationTrace


# ============================================================
# AUDIT INFORMATION
# ============================================================

class AuditInfo(BaseModel):
    mode: str
    no_control_actions_enforced: bool
    latency_ms: int
    slo_ms: int
    service_health: str


# ============================================================
# RESPONSE PAYLOAD ROOT
# ============================================================

class ResponsePayload(BaseModel):
    request_id: str
    idempotency_key: str
    model: Optional[ModelInfo] = None
    status: ResponseStatus
    summary: Optional[Summary] = None
    recommendations: Optional[List[RecommendationItem]] = None
    audit: Optional[AuditInfo] = None


# ============================================================
# TOP-LEVEL SUCCESS RESPONSE
# ============================================================

class JSONResponse(BaseModel):
    schema_version: str
    correlation_id: str
    trace: Optional[Trace] = None
    response: ResponsePayload


# ============================================================
# TOP-LEVEL ERROR RESPONSE
# ============================================================

class JSONErrorResponse(BaseModel):
    schema_version: str
    correlation_id: str
    response: ResponsePayload