from backend.schemas.mass import MassPayload


class MassValidator:

    @staticmethod
    def validate(payload: dict) -> tuple[bool, str]:
        """
        Valida el payload MASS simple.
        En esta versión minimalista, solo verifica que sea un dict válido.
        """
        try:
            MassPayload(**payload)
            return True, "Payload válido"
        except Exception as e:
            return False, f"Payload inválido: {str(e)}"