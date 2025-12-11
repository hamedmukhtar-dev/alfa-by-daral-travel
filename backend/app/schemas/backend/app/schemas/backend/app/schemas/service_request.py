from pydantic import BaseModel
from typing import Any


class ServiceRequestCreate(BaseModel):
    service_type: str
    payload: dict[str, Any]


class ServiceRequestRead(BaseModel):
    id: int
    service_type: str
    status: str
    payload: dict | None = None

    class Config:
        orm_mode = True
