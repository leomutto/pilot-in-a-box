import uuid
from datetime import datetime

TRACKING_PREFIX = "trk"  # Puedes cambiarlo si quieres distinguir servicios


def generate_tracking_id() -> str:
    """
    Genera un tracking_id único, trazable y ordenable temporalmente.

    Formato:
        trk-20250101T153045Z-8f3c2a1b

    Componentes:
        - Prefijo configurable
        - Timestamp UTC ISO8601 compacto
        - UUID reducido (8 caracteres)
    """

    # Timestamp UTC en formato compacto
    timestamp = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")

    # UUID corto para unicidad
    short_uuid = uuid.uuid4().hex[:8]

    # Tracking ID final
    return f"{TRACKING_PREFIX}-{timestamp}-{short_uuid}"