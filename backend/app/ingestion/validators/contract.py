from fastapi import HTTPException


SUPPORTED_SCHEMA_VERSIONS = ["1.1"]
SUPPORTED_UNITS = ["kW", "kWh"]
SUPPORTED_CURRENCIES = ["USD", "EUR"]
SUPPORTED_CLASSIFICATIONS = ["internal", "restricted"]


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