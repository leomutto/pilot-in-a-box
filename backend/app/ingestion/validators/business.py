from fastapi import HTTPException


def validate_business(payload: dict):
    """
    Reglas de negocio:
    - Si mode = 'shadow' → no se permiten acciones de control
    - Si environment = 'prod' → ciertos campos deben existir
    """

    errors = []

    mode = payload["request"]["mode"]
    environment = payload["request"]["environment"]

    # Regla 1: modo shadow no permite control
    if mode == "shadow":
        if payload["request"]["constraints"]["hard"]["no_control_actions"] is False:
            errors.append("En modo 'shadow' no se permiten acciones de control.")

    # Regla 2: en prod, SLO debe ser <= 5000 ms
    if environment == "prod":
        slo = payload["request"]["service_level_objective_ms"]
        if slo > 5000:
            errors.append("En 'prod', SLO debe ser <= 5000 ms.")

    if errors:
        raise HTTPException(status_code=400, detail={"business_errors": errors})

    return {"status": "business_valid"}