from app.schemas.mass import MassPayload
from pydantic import ValidationError


class MassValidator:
    """
    Validador del contrato MASS simple (versión 1.1).
    No incluye lógica enterprise, envelope ni campos adicionales.
    """

    @staticmethod
    def validate(payload: dict) -> tuple[bool, str]:
        """
        Valida el JSON MASS simple usando los esquemas Pydantic.
        Devuelve (True, "OK") si es válido.
        Devuelve (False, "mensaje de error") si es inválido.
        """

        try:
            MassPayload(**payload)
            return True, "Payload MASS válido"
        except ValidationError as e:
            return False, f"Error de validación MASS: {e}"