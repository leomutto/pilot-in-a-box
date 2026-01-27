from pydantic import BaseModel
from typing import Any, Dict

class MassSimplePayload(BaseModel):
    payload: Dict[str, Any]
