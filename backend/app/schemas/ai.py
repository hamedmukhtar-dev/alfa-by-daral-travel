from pydantic import BaseModel
from typing import Optional


class AIRequest(BaseModel):
    user_id: Optional[int] = None
    message: str


class AIIntent(BaseModel):
    intent: str
    confidence: float


class AIResponse(BaseModel):
    reply: str
    intent: str
    confidence: float
