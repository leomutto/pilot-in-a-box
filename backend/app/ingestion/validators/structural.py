from ..schemas_request import JSONRequest
from fastapi import HTTPException


def validate_structural(json_request: JSONRequest):
    """
    Pydantic ya valida estructura automáticamente.
    Si llegamos aquí, el JSON es válido estructuralmente.
    """
    return {
        "status": "structural_valid",
        "schema_version": json_request.schema_version
    }