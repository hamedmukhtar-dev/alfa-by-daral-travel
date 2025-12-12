from pydantic import BaseModel
from typing import Optional


class ServiceListingCreate(BaseModel):
    category: str
    title: str
    description: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    price_from: Optional[float] = None
    price_to: Optional[float] = None
    currency: Optional[str] = "USD"


class ServiceListingResponse(ServiceListingCreate):
    id: int
    supplier_id: int
    status: str

    class Config:
        orm_mode = True
