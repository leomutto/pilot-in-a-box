from fastapi import HTTPException

# MASS ENTERPRISE v1.1 — Valores válidos según tu contrato
SUPPORTED_SCHEMA_VERSIONS = ["1.1"]

# MASS usa "metric" como unidad de sistema
SUPPORTED_UNITS = ["metric"]

# MASS usa USD y EUR (esto ya estaba bien)
SUPPORTED_CURRENCIES = ["USD", "EUR"]

# MASS usa "INTERNAL" como clasificación
SUPPORTED_CLASSIFICATIONS = ["INTERNAL", "internal"]

def validate_contract(payload: dict):
    """
    Valida que el request cumpla el contrato MASS ENTERPRISE v1.1.
    """

    errors = []

    schema_version = payload["schema_version"]
    units = payload["request"]["data_contract"]["units"]
    currency = payload["request"]["data_contract"]["currency"]
    classification = payload["request"]["data_contract"]["data_classification"]

    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        errors.append(f"schema_version no soportada: {schema_version}")

    if units not in SUPPORTED_UNITS:
        errors.append(f"Unidad no soportada: {units}")

    if currency not in SUPPORTED_CURRENCIES:
        errors.append(f"Moneda no soportada: {currency}")

    if classification not in SUPPORTED_CLASSIFICATIONS:
        errors.append(f"Clasificación no permitida: {classification}")

    if errors:
        raise HTTPException(status_code=400, detail={"contract_errors": errors})

    return {"status": "contract_valid"}