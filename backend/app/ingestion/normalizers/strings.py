from fastapi import HTTPException

def normalize_string_basic(value: str) -> str:
    """
    Limpia strings:
    - trim
    - NO colapsa espacios internos (MASS no lo permite en enums ni IDs)
    """
    if not isinstance(value, str):
        return value

    return value.strip()


def normalize_strings(payload: dict) -> dict:
    """
    Normaliza strings clave del request sin alterar enums ni IDs.
    """
    req = payload["request"]

    # IDs: solo trim, no colapsar espacios internos
    req["request_id"] = normalize_string_basic(req["request_id"])
    req["idempotency_key"] = normalize_string_basic(req["idempotency_key"])
    req["tenant_id"] = normalize_string_basic(req["tenant_id"])

    # Enums: solo trim
    req["environment"] = normalize_string_basic(req["environment"])
    req["mode"] = normalize_string_basic(req["mode"])

    return payload