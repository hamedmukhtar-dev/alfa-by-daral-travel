from pydantic import BaseModel

class OfflinePaymentCreate(BaseModel):
    service_request_id: int
    method: str
    reference: str | None = None

class OfflinePaymentOut(BaseModel):
    id: int
    status: str

    class Config:
        from_attributes = True
