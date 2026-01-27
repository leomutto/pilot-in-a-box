from typing import Any, Dict

def normalize_mass_payload_simple(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizador MASS Simple.
    - Recibe un dict simple
    - Limpia strings
    - Convierte números
    - Convierte booleanos
    - Normaliza listas
    - No requiere campos Enterprise
    """

    def normalize_value(value):
        if isinstance(value, str):
            v = value.strip()

            # booleanos
            if v.lower() in ["true", "yes", "1"]:
                return True
            if v.lower() in ["false", "no", "0"]:
                return False

            # números
            if v.isdigit():
                return int(v)

            try:
                return float(v)
            except:
                return v

        if isinstance(value, list):
            return [normalize_value(v) for v in value]

        if isinstance(value, dict):
            return {k: normalize_value(v) for k, v in value.items()}

        return value

    return normalize_value(payload)
