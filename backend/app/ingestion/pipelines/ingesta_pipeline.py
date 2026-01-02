from typing import Dict, Any

# Validadores existentes
from app.ingestion.validators.business import validate_business
from app.ingestion.validators.contract import validate_contract
from app.ingestion.validators.semantic import validate_semantic
from app.ingestion.validators.structural import validate_structural

# Normalizadores existentes
from app.ingestion.normalizers.snake_case import normalize_keys_snake_case
from app.ingestion.normalizers.strings import normalize_strings
from app.ingestion.normalizers.numbers import normalize_numbers
from app.ingestion.normalizers.timestamps import normalize_timestamps
from app.ingestion.normalizers.units import normalize_units

# Utilidades
from app.ingestion.utils.tracking import generate_tracking_id
from app.ingestion.utils.audit import audit_log
from app.ingestion.utils.tracing import (
    generate_trace_id,
    start_span,
    end_span,
    trace_event,
)


def run_ingesta_pipeline(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pipeline determinista de ingesta → validación → normalización → auditoría,
    instrumentado con trazabilidad completa.
    """

    # === 0. TRACE ID GLOBAL ===
    trace_id = generate_trace_id()
    audit_log(event="trace_started", payload={"trace_id": trace_id})

    # === 1. Tracking ID ===
    tracking_id = generate_tracking_id()
    audit_log(event="tracking_id_generated", payload={"tracking_id": tracking_id, "trace_id": trace_id})

    # === 2. VALIDACIONES ===
    span = start_span(trace_id, "validations")
    audit_log(event="span_started", payload=span)

    data = validate_structural(data)
    audit_log(event="structural_validated", payload=trace_event(trace_id, "structural_validated"))

    data = validate_contract(data)
    audit_log(event="contract_validated", payload=trace_event(trace_id, "contract_validated"))

    data = validate_business(data)
    audit_log(event="business_validated", payload=trace_event(trace_id, "business_validated"))

    data = validate_semantic(data)
    audit_log(event="semantic_validated", payload=trace_event(trace_id, "semantic_validated"))

    span = end_span(span)
    audit_log(event="span_completed", payload=span)

    # === 3. NORMALIZACIONES ===
    span = start_span(trace_id, "normalizations")
    audit_log(event="span_started", payload=span)

    data = normalize_keys_snake_case(data)
    audit_log(event="snake_case_normalized", payload=trace_event(trace_id, "snake_case_normalized"))

    data = normalize_strings(data)
    audit_log(event="strings_normalized", payload=trace_event(trace_id, "strings_normalized"))

    data = normalize_numbers(data)
    audit_log(event="numbers_normalized", payload=trace_event(trace_id, "numbers_normalized"))

    data = normalize_timestamps(data)
    audit_log(event="timestamps_normalized", payload=trace_event(trace_id, "timestamps_normalized"))

    data = normalize_units(data)
    audit_log(event="units_normalized", payload=trace_event(trace_id, "units_normalized"))

    span = end_span(span)
    audit_log(event="span_completed", payload=span)

    # === 4. AUDITORÍA FINAL ===
    span = start_span(trace_id, "audit")
    audit_log(event="span_started", payload=span)

    audit_log(
        event="ingestion_pipeline_completed",
        payload={"data": data, "trace_id": trace_id, "tracking_id": tracking_id},
    )

    span = end_span(span)
    audit_log(event="span_completed", payload=span)

    # === 5. TRACE END ===
    audit_log(event="trace_completed", payload={"trace_id": trace_id})

    # === 6. Respuesta final ===
    return {
        "trace_id": trace_id,
        "tracking_id": tracking_id,
        "normalized_data": data,
    }