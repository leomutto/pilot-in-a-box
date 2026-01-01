from fastapi import HTTPException


VALID_UNITS = ["kW", "kWh"]


def normalize_units(payload: dict) -> dict:
    """
    Normaliza unidades del data_contract.
    """
    units = payload["request"]["data_contract"]["units"]

    if units not in VALID_UNITS:
        raise HTTPException(status_code=400, detail=f"Unidad no soportada: {units}")

    return payload