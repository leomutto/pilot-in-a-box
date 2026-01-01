def normalize_string(value: str) -> str:
    """
    Limpia strings:
    - trim
    - elimina espacios dobles
    """
    if not isinstance(value, str):
        return value

    value = value.strip()
    value = " ".join(value.split())
    return value


def normalize_strings(payload: dict) -> dict:
    """
    Normaliza strings clave del request.
    """
    req = payload["request"]

    req["request_id"] = normalize_string(req["request_id"])
    req["idempotency_key"] = normalize_string(req["idempotency_key"])
    req["tenant_id"] = normalize_string(req["tenant_id"])
    req["environment"] = normalize_string(req["environment"])
    req["mode"] = normalize_string(req["mode"])

    return payload