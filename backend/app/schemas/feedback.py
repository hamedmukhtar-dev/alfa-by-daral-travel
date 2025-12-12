from pydantic import BaseModel
from typing import Optional


class FeedbackCreate(BaseModel):
    message: str
    user_name: Optional[str] = None
    user_contact: Optional[str] = None


class FeedbackResponse(FeedbackCreate):
    id: int
    ai_category: Optional[str]
    ai_sentiment: Optional[str]
    ai_priority: Optional[str]

    class Config:
        orm_mode = True
