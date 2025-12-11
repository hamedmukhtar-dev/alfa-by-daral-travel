from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# -----------------------------
# Base Schema
# -----------------------------
class ServiceRequestBase(BaseModel):
    category: str = Field(..., example="delivery")
    title: str = Field(..., example="Send package from A to B")
    description: Optional[str] = Field(None, example="Fragile items")
    user_name: Optional[str] = Field(None, example="Hamed")
    user_phone: str = Field(..., example="+249912345678")
    city_from: Optional[str] = Field(None)
    city_to: Optional[str] = Field(None)
    price_offer: Optional[float] = None


# -----------------------------
# Create Request (Public)
# -----------------------------
class ServiceRequestCreate(ServiceRequestBase):
    pass


# -----------------------------
# Update (Admin only)
# -----------------------------
class ServiceRequestUpdate(BaseModel):
    status: Optional[str] = Field(None, example="in_progress")
    assigned_to: Optional[str] = Field(None, example="Agent-214")


# -----------------------------
# Response Model
# -----------------------------
class ServiceRequestResponse(ServiceRequestBase):
    id: int
    status: str
    assigned_to: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
