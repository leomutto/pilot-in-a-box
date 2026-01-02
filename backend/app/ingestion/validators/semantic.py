from fastapi import HTTPException


def validate_semantic(payload: dict):
    """
    Validación semántica:
    - valores numéricos positivos
    - porcentajes entre 0 y 100
    - timestamps coherentes
    """

    errors = []

    # Ejemplo: porcentajes válidos
    ups_eff = payload["request"]["signals"]["energy"]["ups_efficiency_pct"]
    if not (0 <= ups_eff <= 100):
        errors.append(f"ups_efficiency_pct fuera de rango: {ups_eff}")

    # Ejemplo: hotspot count no negativo
    hotspot = payload["request"]["signals"]["thermal"]["hotspot_rack_count"]
    if hotspot < 0:
        errors.append(f"hotspot_rack_count no puede ser negativo: {hotspot}")

    # Ejemplo: granularity > 0
    gran = payload["request"]["time_window"]["granularity_seconds"]
    if gran <= 0:
        errors.append("granularity_seconds debe ser > 0")

    if errors:
        raise HTTPException(status_code=400, detail={"semantic_errors": errors})

    return {"status": "semantic_valid"}