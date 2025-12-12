from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class WalletOut(BaseModel):
    balance: float

class OfflineCreditRequest(BaseModel):
    amount: float
    note: Optional[str] = None

class WalletTransactionOut(BaseModel):
    id: int
    amount: float
    status: str
    note: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
