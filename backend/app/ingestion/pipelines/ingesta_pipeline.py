from typing import Dict, Any

# Validadores existentes
from app.ingestion.validators.business import validate_business_rules
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


def run_ingesta_pipeline(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Pipeline determinista de ingesta → validación → normalización → auditoría.
    """

    # 1. Tracking ID
    tracking_id = generate_tracking_id()

    # 2. VALIDACIONES (orden recomendado)
    data = validate_structural(data)
    data = validate_contract(data)
    data = validate_business_rules(data)
    data = validate_semantic(data)

    # 3. NORMALIZACIONES (orden recomendado)
    data = normalize_keys_snake_case(data)
    data = normalize_strings(data)
    data = normalize_numbers(data)
    data = normalize_timestamps(data)
    data = normalize_units(data)

    # 4. AUDITORÍA
    audit_log(
        event="ingestion_pipeline_completed",
        payload=data,
        tracking_id=tracking_id,
    )

    # 5. Respuesta final
    return {
        "tracking_id": tracking_id,
        "normalized_data": data,
    }