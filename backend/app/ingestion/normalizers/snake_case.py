import re


def to_snake_case(key: str) -> str:
    key = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", key)
    key = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", key)
    return key.lower()


def normalize_keys_snake_case(obj):
    """
    Convierte todas las claves del JSON a snake_case.
    """
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            new_key = to_snake_case(k)
            new_dict[new_key] = normalize_keys_snake_case(v)
        return new_dict

    if isinstance(obj, list):
        return [normalize_keys_snake_case(i) for i in obj]

    return obj