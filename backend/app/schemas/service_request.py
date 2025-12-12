from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ServiceRequestCreate(BaseModel):
    category: str
    title: str
    description: Optional[str] = None
    user_name: Optional[str] = None
    user_phone: str
    city_from: Optional[str] = None
    city_to: Optional[str] = None
    price_offer: Optional[float] = None


class ServiceRequestUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[str] = None


class ServiceRequestResponse(BaseModel):
    id: int
    category: str
    title: str
    description: Optional[str]
    user_name: Optional[str]
    user_phone: str
    city_from: Optional[str]
    city_to: Optional[str]
    price_offer: Optional[float]
    intent_score: str
    status: str
    assigned_to: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
