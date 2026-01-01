from fastapi import HTTPException
import math


def normalize_number(value):
    """
    - Convierte strings numéricos a float/int
    - Redondea floats a 3 decimales
    - Rechaza NaN, inf, -inf
    """
    if isinstance(value, str):
        try:
            value = float(value)
        except ValueError:
            raise HTTPException(status_code=400, detail=f"Valor numérico inválido: {value}")

    if isinstance(value, float):
        if math.isnan(value) or math.isinf(value):
            raise HTTPException(status_code=400, detail=f"Valor numérico inválido: {value}")
        return round(value, 3)

    return value


def normalize_numbers(payload: dict) -> dict:
    """
    Normaliza todos los números del JSON_request.
    """
    signals = payload["request"]["signals"]

    # Energy
    for key, value in signals["energy"].items():
        signals["energy"][key] = normalize_number(value)

    # Thermal
    for key, value in signals["thermal"].items():
        signals["thermal"][key] = normalize_number(value)

    # Cooling
    for key, value in signals["cooling"].items():
        signals["cooling"][key] = normalize_number(value)

    # Workload
    for key, value in signals["workload"].items():
        if key != "job_mix":
            signals["workload"][key] = normalize_number(value)

    # Job mix
    for key, value in signals["workload"]["job_mix"].items():
        signals["workload"]["job_mix"][key] = normalize_number(value)

    return payload