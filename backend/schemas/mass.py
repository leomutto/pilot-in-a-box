from pydantic import BaseModel
from typing import Any
from datetime import datetime

class MassRequestBase(BaseModel):
    id: int
    user_id: int
    payload_json: Any
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True